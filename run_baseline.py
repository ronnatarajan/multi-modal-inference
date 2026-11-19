"""Run the baseline (describe -> decompose -> decide) over VIBE and print accuracy.

Usage:  .venv/bin/python run_baseline.py --describe prompts/describe_speaker_and_surroundings.txt
                                         [--limit N] [--out results/baseline.jsonl]
"""
import argparse
import json
import time
from pathlib import Path

from pipeline import decide, decompose, describe, parse_answer
from qwen_omni import load_model

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser()
parser.add_argument("--describe", required=True, help="describe prompt file, e.g. prompts/describe_speaker_and_surroundings.txt")
parser.add_argument("--model", default="qwen2.5-omni-7b", help="VLM to use: qwen2.5-omni-7b or qwen3-omni-30b")
parser.add_argument("--limit", type=int, default=None, help="only run the first N questions")
parser.add_argument("--out", default="results/baseline.jsonl")
args = parser.parse_args()
describe_prompt = (ROOT / args.describe).read_text()

items = [json.loads(line) for line in open(ROOT / "vibe/vibe_task.jsonl")]
# task_id is the video id, shared by all questions on that video (and some share the same fact too),
# so give each question its own id: video_2_0, video_2_1, ...
per_video = {}
for item in items:
    k = per_video.get(item["task_id"], 0)
    item["qid"] = f"{item['task_id']}_{k}"
    per_video[item["task_id"]] = k + 1
items = items[:args.limit]
model, processor = load_model(args.model)

out_path = ROOT / args.out
out_path.parent.mkdir(parents=True, exist_ok=True)
cache = {}  #this might help us save time, but probably not as useful until we start to combine steps 
correct = unparsed = 0

with open(out_path, "w") as f:
    for i, item in enumerate(items):
        t0 = time.time()
        if item["video"] not in cache:
            description = describe(model, processor, ROOT / "vibe/videos" / item["video"], describe_prompt)
            cache[item["video"]] = (description, decompose(description))
        description, assertions = cache[item["video"]]

        t1 = time.time()
        reply = decide(model, processor, assertions, item)
        t2 = time.time()
        pred = parse_answer(reply)
        correct += pred == item["answer"]
        unparsed += pred is None

        f.write(json.dumps({"qid": item["qid"], "video": item["video"], "model": args.model,
                            "describe_prompt": args.describe,
                            "fact": item["fact"],
                            "inference_A": item["inference_A"], "inference_B": item["inference_B"],
                            "description": description, "assertions": assertions, "reply": reply,
                            "pred": pred, "answer": item["answer"], "correct": pred == item["answer"]},
                           ensure_ascii=False) + "\n")
        f.flush()
        print(f"[{i + 1}/{len(items)}] {item['qid']}: pred={pred} answer={item['answer']}"
              f"  (describe+decompose {t1 - t0:.0f}s, decide {t2 - t1:.0f}s)", flush=True)

print(f"\nAccuracy: {correct}/{len(items)} = {correct / len(items):.3f}")
print(f"Unparseable replies: {unparsed}")
print(f"Videos described: {len(cache)}")
