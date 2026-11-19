"""Load the VLM. Use load_model() and GENERATION_KWARGS in all project code.

Models (pick with load_model(name)):
  qwen2.5-omni-7b  Qwen2.5-Omni-7B (default, the baseline model)
  qwen3-omni-30b   Qwen3-Omni-30B-A3B-Instruct (larger model for comparison, ~66 GB)
"""
import os
import sys
from pathlib import Path

import torch
from transformers import (Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor,
                          Qwen3OmniMoeForConditionalGeneration, Qwen3OmniMoeProcessor, set_seed)

MODELS_DIR = Path(__file__).resolve().parent / "models"
MODELS = {
    "qwen2.5-omni-7b": (Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor, "Qwen2.5-Omni-7B"),
    "qwen3-omni-30b": (Qwen3OmniMoeForConditionalGeneration, Qwen3OmniMoeProcessor, "Qwen3-Omni-30B-A3B-Instruct"),
}
MODEL_DIR = MODELS_DIR / "Qwen2.5-Omni-7B"

# Use the ffmpeg that setup.sh puts in .venv/bin (Scholar has none). Needed to read audio from videos.
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]

# Greedy decoding so the same input always gives the same output.
# Omni's generate() ignores max_new_tokens; the text cap must be passed as thinker_max_new_tokens
# (default 1024). Normal descriptions are under ~250 tokens; the cap only cuts off repetition loops.
GENERATION_KWARGS = dict(do_sample=False, thinker_max_new_tokens=512, return_audio=False)


def load_model(name="qwen2.5-omni-7b"):
    set_seed(0)
    model_class, processor_class, folder = MODELS[name]
    extra = {}
    if name == "qwen3-omni-30b":
        extra["enable_audio_output"] = False  # skip loading the speech-output modules (text output only)
    model = model_class.from_pretrained(MODELS_DIR / folder, dtype=torch.bfloat16, device_map="cpu", **extra)
    # device_map="cuda" hangs on GB10 nodes when the model is on scratch, so move weights manually.
    for p in list(model.parameters()) + list(model.buffers()):
        p.data = p.data.clone().to("cuda")
    model.disable_talker()  # text output only; saves GPU memory
    return model.eval(), processor_class.from_pretrained(MODELS_DIR / folder)
