"""Check that the model works AND is reproducible: one clip alone vs. the same clip inside a batch must give
identical text. Prints a fingerprint of the outputs; everyone's should match the one in README.md.

Usage:  .venv/bin/python scripts/smoke_test.py      (loads the model, ~5.5 min; after it exits, the node's
        memory stays held, so run the baseline in a NEW session)
"""
import hashlib
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pipeline import describe_request
from qwen_omni import generate, load_llm

PROMPT = (ROOT / "prompts/describe_speaker_focused.txt").read_text()
VIDEOS = [ROOT / f"vibe/videos/video_{i}.mp4" for i in (1, 2, 3, 4)]

if __name__ == "__main__":
    t0 = time.time()
    llm, processor = load_llm()
    print(f"Model loaded in {time.time() - t0:.0f}s", flush=True)

    reqs = [describe_request(processor, v, PROMPT) for v in VIDEOS]

    t0 = time.time()
    alone = generate(llm, [reqs[0]])[0]
    print(f"1 clip alone: {time.time() - t0:.1f}s", flush=True)

    t0 = time.time()
    batch = generate(llm, reqs)
    print(f"{len(reqs)} clips batched: {time.time() - t0:.1f}s", flush=True)

    for v, text in zip(VIDEOS, batch):
        print(f"\n--- {v.name} ---\n{text}")

    same = alone == batch[0]
    print(f"\nAlone vs batched identical: {same}")
    print("Fingerprint (compare with README):", hashlib.sha256("\n".join(batch).encode()).hexdigest()[:16])
    print("SMOKE TEST PASSED" if same else "SMOKE TEST FAILED: output depends on batch")
