"""Baseline pipeline: VLM describes the clip -> LLM turns it into assertions -> VLM picks A or B.

The VLM steps only build requests here; qwen_omni.generate() runs a whole list of them as one batch.
"""
import re
from pathlib import Path

import av

from llm import ask_llm
from qwen_omni import build_request

PROMPTS = Path(__file__).resolve().parent / "prompts"

N_FRAMES = 36     # frames per clip; short clips use all their frames instead (see n_frames). 36 so temporal
                  # prompting can split it evenly into 1, 2 or 3 segments of even (paired) frame counts
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


#this is the VLM call one, which is just describing the video
def describe_request(processor, video_path, prompt):
    """VLM call 1: watch the clip (video + audio) and describe it using `prompt`. Never sees the question."""
    content = [
        {"type": "video", "video": str(video_path), "nframes": n_frames(video_path)},
        {"type": "text", "text": prompt},
    ]
    return build_request(processor, content, use_audio=USE_AUDIO)


#this is the llm decomposition step
def decompose(description):
    """LLM call: rewrite the VLM's description as a list of one-observation assertions.
    The prompt is re-read every call so edits apply without restarting."""
    return ask_llm(fill((PROMPTS / "decompose.txt").read_text(), description=description))


#this is the call to vlm to make the final decision (no video sent here)
def decide_request(processor, assertions, item):
    """VLM call 2: text only. Reads the assertions + fact + A/B and answers.
    The prompt is re-read every call so edits apply without restarting."""
    prompt = fill((PROMPTS / "decide.txt").read_text(), assertions=assertions, fact_text=item["fact"],
                  inference_A=item["inference_A"], inference_B=item["inference_B"])
    return build_request(processor, [{"type": "text", "text": prompt}])


def parse_answer(reply):
    """Pull 'A' or 'B' from the last 'Answer: X' in the reply. None if missing."""
    matches = re.findall(r"Answer:\s*\**\s*([AB])\b", reply)
    return matches[-1] if matches else None
