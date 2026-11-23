"""Temporal change prompting: stage 1 only (describe). Stages 2-3 (decompose, decide) are the baseline's.

Each clip is cut into m equal time segments (m = 1, 2 or 3). The 36 frames (pipeline.N_FRAMES) are split
evenly between them, and each segment gets only the audio for its own time window. Segments are described in
order; every segment gets the baseline describe prompt, and segments after the first also get the earlier
segments' descriptions (prompts/earlier_segments.txt). The descriptions are then joined with time labels.

Every segment must be at least MIN_SEGMENT_S long, so a clip gets m_eff = min(m, floor(length / 1 s))
segments. A clip with m_eff = 1 is described exactly like the baseline (same request, same output).

All model settings come from the shared qwen_omni.py / pipeline.py; nothing there is changed.
"""
import math
import sys
from pathlib import Path

import av
import numpy as np
import torch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from qwen_omni_utils.v2_5 import vision_process  # noqa: E402

from pipeline import N_FRAMES, USE_AUDIO, describe_request, fill, n_frames  # noqa: E402  (imports qwen_omni)
from qwen_omni import build_request, generate_in_chunks  # noqa: E402

HERE = Path(__file__).resolve().parent
EARLIER_BLOCK = HERE / "prompts" / "earlier_segments.txt"  # re-read every run, so it can be edited live

MIN_SEGMENT_S = 1.0
LABELS = {2: ["First half", "Second half"], 3: ["Beginning", "Middle", "End"]}


# --- frame reader -------------------------------------------------------------------------------------
# qwen_omni.py's PyAV reader always samples the whole clip. This one samples only a segment's frames when the
# request carries "segment_frames" = [first, end) frame indices, and otherwise hands off to the baseline reader,
# so whole-clip requests are read exactly as in the baseline.

_baseline_reader = vision_process.VIDEO_READER_BACKENDS["pyav"]


def _read_video_segment(ele):
    if "segment_frames" not in ele:
        return _baseline_reader(ele)
    start, end = ele["segment_frames"]
    path = ele["video"].removeprefix("file://")
    with av.open(path) as container:
        stream = container.streams.video[0]
        frames = [f.to_ndarray(format="rgb24") for f in container.decode(stream)]
        video_fps = float(stream.average_rate)
    video = torch.from_numpy(np.stack(frames)).permute(0, 3, 1, 2)  # (T, C, H, W) uint8
    nframes = ele["nframes"]
    # Evenly spaced, rounded indices inside the segment: the baseline's rule, applied to the segment.
    idx = torch.linspace(start, end - 1, nframes).round().long()
    return video[idx], nframes / (end - start) * video_fps


vision_process.VIDEO_READER_BACKENDS["pyav_segment"] = _read_video_segment
vision_process.FORCE_QWENVL_VIDEO_READER = "pyav_segment"


# --- planning segments ----------------------------------------------------------------------------------

def plan(video_path, m):
    """How a clip is split for m segments: m_eff and, per segment, label, frame range, times and frame count."""
    with av.open(str(video_path)) as container:
        stream = container.streams.video[0]
        total, fps = stream.frames, float(stream.average_rate)
    duration = total / fps
    m_eff = max(1, min(m, math.floor(duration / MIN_SEGMENT_S)))
    if m_eff == 1:
        return {"m_eff": 1, "duration": duration,
                "segments": [{"label": "Whole clip", "first_frame": 0, "end_frame": total,
                              "start": 0.0, "end": duration, "frames": n_frames(video_path)}]}
    per_segment = N_FRAMES // m_eff
    assert per_segment * m_eff == N_FRAMES and per_segment % 2 == 0, "N_FRAMES must split into even shares"
    segments = []
    for k in range(m_eff):
        first, end = round(k * total / m_eff), round((k + 1) * total / m_eff)
        assert end - first >= per_segment, f"{video_path}: segment {k} has only {end - first} frames"
        segments.append({"label": LABELS[m_eff][k], "first_frame": first, "end_frame": end,
                         "start": first / fps, "end": end / fps, "frames": per_segment})
    return {"m_eff": m_eff, "duration": duration, "segments": segments}


def _time_label(seg):
    return f"{seg['label']} ({seg['start']:.1f}-{seg['end']:.1f} s)"


def join_descriptions(clip_plan, descriptions):
    """The text that goes to decompose: one description for an unsplit clip, else labelled segments."""
    if clip_plan["m_eff"] == 1:
        return descriptions[0]
    return "\n\n".join(f"{_time_label(seg)}:\n{d}" for seg, d in zip(clip_plan["segments"], descriptions))


def segment_text(prompt, clip_plan, k, earlier, block):
    """Prompt for segment k: the baseline prompt, plus the earlier segments' descriptions after segment 0."""
    if k == 0:
        return prompt
    seg = clip_plan["segments"][k]
    earlier_text = "\n\n".join(f"{_time_label(s)}:\n{d}" for s, d in zip(clip_plan["segments"][:k], earlier))
    return fill(block, part=_time_label(seg).lower(), earlier=earlier_text, prompt=prompt)


def segment_request(processor, video_path, seg, text):
    """One segment's describe request: its own frames, and its own audio (video_start/video_end)."""
    content = [
        {"type": "video", "video": str(video_path), "nframes": seg["frames"],
         "segment_frames": [seg["first_frame"], seg["end_frame"]],
         "video_start": seg["start"], "video_end": seg["end"]},
        {"type": "text", "text": text},
    ]
    return build_request(processor, content, use_audio=USE_AUDIO)


def describe_all(llm, processor, video_paths, prompt, m, run=generate_in_chunks):
    """Stage 1 for every clip. Round k describes segment k of every clip that has one (in chunks of clips,
    see qwen_omni.CHUNK). Returns {path: plan}, {path: [segment descriptions]}, {path: joined description}."""
    block = EARLIER_BLOCK.read_text()
    plans = {v: plan(v, m) for v in video_paths}
    descs = {v: [] for v in video_paths}
    for k in range(max(p["m_eff"] for p in plans.values())):
        todo = [v for v in video_paths if plans[v]["m_eff"] > k]

        def make_request(v, k=k):
            if plans[v]["m_eff"] == 1:
                return describe_request(processor, v, prompt)  # exactly the baseline request
            text = segment_text(prompt, plans[v], k, descs[v], block)
            return segment_request(processor, v, plans[v]["segments"][k], text)

        for v, d in zip(todo, run(llm, todo, make_request)):
            descs[v].append(d)
        print(f"  round {k + 1}: described {len(todo)} segments", flush=True)
    return plans, descs, {v: join_descriptions(plans[v], descs[v]) for v in video_paths}
