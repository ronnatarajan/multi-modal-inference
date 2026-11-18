"""Quick check that the model loads and can watch + listen to a VIBE clip.

Usage:  .venv/bin/python scripts/smoke_test.py [path/to/video.mp4]
"""
import sys
import time
from pathlib import Path

import torch
from qwen_omni_utils import process_mm_info

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from qwen_omni import GENERATION_KWARGS, load_model

video = sys.argv[1] if len(sys.argv) > 1 else "vibe/videos/video_44.mp4"

t0 = time.time()
model, processor = load_model()
print(f"Model loaded in {time.time() - t0:.0f}s", flush=True)

# Qwen requires this exact system prompt when using audio.
SYSTEM = ("You are Qwen, a virtual human developed by the Qwen Team, Alibaba Group, capable of "
          "perceiving auditory and visual inputs, as well as generating text and speech.")
conversation = [
    {"role": "system", "content": [{"type": "text", "text": SYSTEM}]},
    {"role": "user", "content": [
        {"type": "video", "video": video},
        {"type": "text", "text": "Describe what the people do and say in this clip, in two sentences."},
    ]},
]
text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
audios, images, videos = process_mm_info(conversation, use_audio_in_video=True)
inputs = processor(text=text, audio=audios, images=images, videos=videos, return_tensors="pt",
                   padding=True, use_audio_in_video=True).to(model.device, model.dtype)

t0 = time.time()
out = model.generate(**inputs, use_audio_in_video=True, **GENERATION_KWARGS)
reply = processor.batch_decode(out[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0]

print(f"Video: {video}  (answered in {time.time() - t0:.0f}s)")
print(f"Model reply: {reply.strip()}")
print(f"Peak GPU memory: {torch.cuda.max_memory_allocated() / 1e9:.1f} GB")
print("SMOKE TEST PASSED")
