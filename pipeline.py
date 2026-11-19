"""Baseline pipeline: VLM describes the clip -> LLM turns it into assertions -> VLM picks A or B."""
import re
from pathlib import Path

import av
from qwen_omni_utils import process_mm_info

from llm import ask_llm
from qwen_omni import GENERATION_KWARGS

PROMPTS = Path(__file__).resolve().parent / "prompts"
DECOMPOSE_PROMPT = (PROMPTS / "decompose.txt").read_text()
DECIDE_PROMPT = (PROMPTS / "decide.txt").read_text()

N_FRAMES = 30     # frames sampled per clip; short clips use all their frames instead (see n_frames)
USE_AUDIO = True  # give the clip's audio to VLM call 1


def fill(template, **values):
    """Fill {name} placeholders. Unlike str.format, literal braces elsewhere in the prompt are left alone."""
    for name, value in values.items():
        template = template.replace("{" + name + "}", value)
    return template


def n_frames(video_path):
    """N_FRAMES, or the clip's own frame count if it is shorter (rounded down to even, as Qwen requires)."""
    with av.open(str(video_path)) as container:
        total = container.streams.video[0].frames
    return min(N_FRAMES, total - total % 2)


def _generate(model, processor, user_content, use_audio=False):
    """Run one chat turn and return the model's text reply."""
    conversation = [{"role": "user", "content": user_content}]
    text = processor.apply_chat_template(conversation, add_generation_prompt=True, tokenize=False)
    audios, images, videos = process_mm_info(conversation, use_audio_in_video=use_audio)
    inputs = processor(text=text, audio=audios, images=images, videos=videos, return_tensors="pt",
                       padding=True, use_audio_in_video=use_audio).to(model.device, model.dtype)
    out = model.generate(**inputs, use_audio_in_video=use_audio, **GENERATION_KWARGS)
    if isinstance(out, tuple):  # Qwen3-Omni returns (text_ids, audio)
        out = out[0]
    return processor.batch_decode(out[:, inputs["input_ids"].shape[1]:], skip_special_tokens=True)[0].strip()

#this is the VLM call one, which is just describing the video
def describe(model, processor, video_path, prompt):
    """VLM call 1: watch the clip (video + audio) and describe it using `prompt`. Never sees the question."""
    content = [
        {"type": "video", "video": str(video_path), "nframes": n_frames(video_path)},
        {"type": "text", "text": prompt},
    ]
    return _generate(model, processor, content, use_audio=USE_AUDIO)

#this is the llm decomposition step
def decompose(description):
    """LLM call: rewrite the VLM's description as a list of one-observation assertions."""
    return ask_llm(fill(DECOMPOSE_PROMPT, description=description))

#this is the call to vlm to make the final decision (no video sent here)
def decide(model, processor, assertions, item):
    """VLM call 2: text only. Reads the assertions + fact + A/B and answers."""
    prompt = fill(DECIDE_PROMPT, assertions=assertions, fact_text=item["fact"],
                  inference_A=item["inference_A"], inference_B=item["inference_B"])
    return _generate(model, processor, [{"type": "text", "text": prompt}])


def parse_answer(reply):
    """Pull 'A' or 'B' from the last 'Answer: X' in the reply. None if missing."""
    matches = re.findall(r"Answer:\s*\**\s*([AB])\b", reply)
    return matches[-1] if matches else None
