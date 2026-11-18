"""Load Qwen2.5-Omni-7B. Use load_model() and GENERATION_KWARGS in all project code."""
import os
import sys
from pathlib import Path

import torch
from transformers import Qwen2_5OmniForConditionalGeneration, Qwen2_5OmniProcessor, set_seed

MODEL_DIR = Path(__file__).resolve().parent / "models" / "Qwen2.5-Omni-7B"

# Use the ffmpeg that setup.sh puts in .venv/bin (Scholar has none). Needed to read audio from videos.
os.environ["PATH"] = str(Path(sys.executable).parent) + os.pathsep + os.environ["PATH"]

# Greedy decoding so the same input always gives the same output.
GENERATION_KWARGS = dict(do_sample=False, max_new_tokens=256, return_audio=False)


def load_model():
    set_seed(0)
    model = Qwen2_5OmniForConditionalGeneration.from_pretrained(MODEL_DIR, dtype=torch.bfloat16, device_map="cpu")
    # device_map="cuda" hangs on GB10 nodes when the model is on scratch, so move weights manually.
    for p in list(model.parameters()) + list(model.buffers()):
        p.data = p.data.clone().to("cuda")
    model.disable_talker()  # text output only; saves ~2 GB GPU memory
    return model.eval(), Qwen2_5OmniProcessor.from_pretrained(MODEL_DIR)
