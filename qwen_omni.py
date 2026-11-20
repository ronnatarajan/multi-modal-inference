"""Load Qwen3-Omni-30B-A3B-Instruct with vLLM and run batches of requests. Use load_llm(), build_request()
and generate() in all project code. Set up with:  bash scripts/setup.sh

Reproducibility across teammates (everything below is fixed in code, don't override per run):
  - VLLM_BATCH_INVARIANT=1: a request's output doesn't depend on what else is in the batch,
    so running --limit 10 or the full set gives the same text for the same video.
  - Greedy decoding (temperature 0), fixed seed, prefix caching off.
  - Frames/audio come from qwen-omni-utils (frames decoded with PyAV, evenly spaced).
  - Pinned versions (requirements.txt), weights (scripts/model.sha256), GPU type (GB10 spark nodes).

Every os.environ / LLM() setting below works around a specific failure on Scholar's GB10 nodes;
see the comment on each before changing it.
"""
import os
import sys
import threading
from pathlib import Path

os.environ["VLLM_BATCH_INVARIANT"] = "1"  # must be set before vllm is imported
# On Scholar's GB10 nodes any single GPU allocation of 4 GiB or more faults ("illegal memory access") when
# touched past 4 GiB, in plain PyTorch too. vLLM's KV cache is one ~13 GB buffer. Expandable segments build
# big buffers from smaller mapped pieces, which works (tested up to 32 GiB).
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
# FlashInfer's top-k/top-p sampler JIT-compiles at startup and needs `ninja`; we decode greedily anyway.
os.environ["VLLM_USE_FLASHINFER_SAMPLER"] = "0"
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
# Use the ffmpeg that setup puts next to python (Scholar has none). librosa needs it to read audio from mp4s,
# and audioread remembers "no ffmpeg" for the life of the process, so check now, not 5 minutes into loading.
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]
import shutil
import subprocess
if not shutil.which("ffmpeg") or subprocess.run(["ffmpeg", "-version"], capture_output=True).returncode != 0:
    sys.exit("ffmpeg not found or broken next to python (needed for clip audio). Re-run: bash scripts/setup.sh")

import av
import numpy as np
import torch
from qwen_omni_utils import process_mm_info
from qwen_omni_utils.v2_5 import vision_process
from transformers import Qwen3OmniMoeProcessor
from vllm import LLM, SamplingParams

MODEL_NAME = "qwen3-omni-30b"
MODEL_DIR = Path(__file__).resolve().parent / "models" / "Qwen3-Omni-30B-A3B-Instruct"

# Greedy. Normal descriptions are under ~250 tokens; the cap only cuts off repetition loops.
SAMPLING = SamplingParams(temperature=0.0, max_tokens=512, seed=0)


def _read_video_pyav(ele):
    """Frame reader for qwen-omni-utils. torchcodec can't find FFmpeg libs on Scholar and
    torchvision.io.read_video is gone in torchvision 0.29, so decode with PyAV (bundles FFmpeg).
    Same frame choice as qwen-omni-utils' torchvision reader: evenly spaced, rounded indices."""
    path = ele["video"].removeprefix("file://")
    with av.open(path) as container:
        stream = container.streams.video[0]
        frames = [f.to_ndarray(format="rgb24") for f in container.decode(stream)]
        video_fps = float(stream.average_rate)
    video = torch.from_numpy(np.stack(frames)).permute(0, 3, 1, 2)  # (T, C, H, W) uint8
    total = video.shape[0]
    nframes = vision_process.smart_nframes(ele, total_frames=total, video_fps=video_fps)
    idx = torch.linspace(0, total - 1, nframes).round().long()
    return video[idx], nframes / max(total, 1e-6) * video_fps


vision_process.VIDEO_READER_BACKENDS["pyav"] = _read_video_pyav
vision_process.FORCE_QWENVL_VIDEO_READER = "pyav"


def drop_weight_cache():
    """Evict the weight files from the Linux page cache (no root needed). On GB10 the GPU shares RAM with
    the CPU, and GPU allocations don't reclaim cached file pages: when they run out of real memory they
    fail with "illegal memory access" instead of OOM. So a cached copy of the 66 GB of weights must go."""
    for path in MODEL_DIR.glob("*.safetensors"):
        fd = os.open(path, os.O_RDONLY)
        os.posix_fadvise(fd, 0, 0, os.POSIX_FADV_DONTNEED)
        os.close(fd)


def _keep_dropping_weight_cache(stop):
    """Run during loading: every shard read fills the page cache, so evict it continuously, not just at the end."""
    while not stop.wait(2):
        drop_weight_cache()


def load_llm(gpu_memory_utilization=0.70):
    """Load Qwen3-Omni (text output only). Takes a few minutes the first time (compiles kernels)."""
    drop_weight_cache()
    # On GB10 nodes, memory from an earlier model run stays held after it exits (it did not drain in 10+ min).
    # Fail right away with the fix instead of minutes into loading.
    free, total = torch.cuda.mem_get_info()
    if free < gpu_memory_utilization * total:
        sys.exit(f"Only {free / 1e9:.0f} GB GPU memory free, need {gpu_memory_utilization * total / 1e9:.0f} GB. "
                 "An earlier model run on this node is still holding memory (it isn't freed on exit). "
                 "Start a new OnDemand session.")
    stop = threading.Event()
    threading.Thread(target=_keep_dropping_weight_cache, args=(stop,), daemon=True).start()
    llm = LLM(
        model=str(MODEL_DIR),
        dtype="bfloat16",
        seed=0,
        max_model_len=16384,  # a 30-frame clip + audio + prompt is a few thousand tokens
        max_num_seqs=8,
        limit_mm_per_prompt={"image": 0, "video": 1, "audio": 1},
        enable_prefix_caching=False,
        # Read each shard fully into RAM. The default (mmap) hangs on GB10 nodes when the weights are on
        # scratch (NFS).
        safetensors_load_strategy="eager",
        # No CUDA graphs for now (slower per token; fused MoE kernels still apply). The earlier graph-capture
        # crash was the 4 GiB allocation bug, and graphs worked in a 2-layer test with expandable segments,
        # so this can likely be switched off once a full run is confirmed.
        enforce_eager=True,
        gpu_memory_utilization=gpu_memory_utilization,  # fraction of the GB10's 128 GB unified memory
    )
    stop.set()
    drop_weight_cache()
    return llm, Qwen3OmniMoeProcessor.from_pretrained(MODEL_DIR)


def build_request(processor, user_content, use_audio=False):
    """Turn one user turn (a chat content list: video/text items) into a vLLM request."""
    conversation = [{"role": "user", "content": user_content}]
    prompt = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    audios, images, videos = process_mm_info(conversation, use_audio_in_video=use_audio)
    mm = {}
    if videos:
        mm["video"] = videos[0]
    if audios:
        mm["audio"] = audios[0]
    req = {"prompt": prompt}
    if mm:
        req["multi_modal_data"] = mm
        req["mm_processor_kwargs"] = {"use_audio_in_video": use_audio}
    return req


def generate(llm, requests):
    """Run a list of requests as one batch; returns the reply texts in the same order."""
    outputs = llm.generate(requests, SAMPLING)
    return [o.outputs[0].text.strip() for o in outputs]
