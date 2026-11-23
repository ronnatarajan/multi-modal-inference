"""Baseline (describe -> decompose -> decide) with Qwen3-Omni on vLLM. Loads the model ONCE, then waits
for you to type a describe prompt file; run as many as you like without reloading.

Start it with:  bash scripts/start.sh        (runs this inside tmux so it survives disconnects)
or directly:    .venv/bin/python run_baseline.py [--limit N] [--data DIR]

--data picks the dataset folder (vibe_task.jsonl + videos/), default vibe/. For the main test set:
    bash scripts/start.sh --data data/sampled100

Then at the prompt:
    describe> prompts/describe_speaker_focused.txt          # run it on the first N questions
    describe> prompts/describe_speaker_focused.txt 30       # override the limit for this run
    describe> q                                             # quit (or Ctrl-D)

The describe prompt, decompose.txt and decide.txt are re-read every run, so edit them and run again.
Changes to Python code need a restart. Ctrl-C stops the current run but keeps the model loaded.

Why stay open: loading takes ~5.5 min, and on Scholar's GB10 nodes the memory isn't given back
when the model exits, so a second load on the same node fails. Keep this running all session.

Each run writes results/<prompt name>.jsonl (then _2, _3, ... if it already exists) plus a copy of
the exact prompt text used, results/<same name>.prompt.txt. With --data other than vibe/, results go in
results/<dataset folder name>/ instead (e.g. results/sampled100/).
"""
import argparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from pipeline import decide_request, decompose, describe_request, parse_answer
from qwen_omni import MODEL_NAME, generate, generate_in_chunks, load_llm

ROOT = Path(__file__).resolve().parent


def load_items(data_dir):
    items = [json.loads(line) for line in open(data_dir / "vibe_task.jsonl")]
    # task_id is the video id, shared by all questions on that video, so give each question its own id.
    per_video = {}
    for item in items:
        k = per_video.get(item["task_id"], 0)
        item["qid"] = f"{item['task_id']}_{k}"
        per_video[item["task_id"]] = k + 1
    return items


def new_out_path(out_dir, prompt_path):
    """<out_dir>/<name>.jsonl, or <name>_2.jsonl, _3, ... so earlier runs are never overwritten."""
    path = out_dir / f"{prompt_path.stem}.jsonl"
    k = 2
    while path.exists():
        path = out_dir / f"{prompt_path.stem}_{k}.jsonl"
        k += 1
    return path


def run_experiment(llm, processor, items, prompt_path, data_dir, out_dir):
    describe_prompt = prompt_path.read_text()
    videos = list(dict.fromkeys(item["video"] for item in items))  # unique, in order
    t_start = time.time()

    # 1. Describe every clip (VLM, video + audio), in chunks of clips to keep RAM flat (see qwen_omni.CHUNK).
    descriptions = dict(zip(videos, generate_in_chunks(
        llm, videos, lambda v: describe_request(processor, data_dir / "videos" / v, describe_prompt))))
    print(f"Described {len(videos)} clips in {time.time() - t_start:.0f}s", flush=True)

    # 2. Decompose (GPT-OSS on RCAC). Few threads: the server allows 20 calls/min and ask_llm retries on 429.
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=4) as pool:
        assertions = dict(zip(videos, pool.map(decompose, (descriptions[v] for v in videos))))
    print(f"Decomposed {len(videos)} descriptions in {time.time() - t0:.0f}s", flush=True)

    # 3. Decide every question (VLM, text only), one batch.
    t0 = time.time()
    replies = generate(llm, [decide_request(processor, assertions[item["video"]], item) for item in items])
    print(f"Decided {len(items)} questions in {time.time() - t0:.0f}s", flush=True)

    out_path = new_out_path(out_dir, prompt_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.with_suffix(".prompt.txt").write_text(describe_prompt)
    rel_prompt = str(prompt_path.relative_to(ROOT)) if prompt_path.is_relative_to(ROOT) else str(prompt_path)
    correct = unparsed = 0
    with open(out_path, "w") as f:
        for item, reply in zip(items, replies):
            pred = parse_answer(reply)
            correct += pred == item["answer"]
            unparsed += pred is None
            f.write(json.dumps({"qid": item["qid"], "video": item["video"], "model": MODEL_NAME,
                                "describe_prompt": rel_prompt,
                                "fact": item["fact"],
                                "inference_A": item["inference_A"], "inference_B": item["inference_B"],
                                "description": descriptions[item["video"]],
                                "assertions": assertions[item["video"]], "reply": reply,
                                "pred": pred, "answer": item["answer"], "correct": pred == item["answer"]},
                               ensure_ascii=False) + "\n")

    print(f"\nAccuracy: {correct}/{len(items)} = {correct / len(items):.3f}")
    print(f"Unparseable replies: {unparsed}")
    print(f"Videos described: {len(videos)}")
    print(f"Total time: {time.time() - t_start:.0f}s  -> {out_path.relative_to(ROOT)}\n", flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="default number of questions per run (default: all)")
    parser.add_argument("--data", default="vibe", help="dataset folder with vibe_task.jsonl + videos/ (default: vibe)")
    args = parser.parse_args()
    data_dir = Path(args.data) if Path(args.data).is_absolute() else ROOT / args.data
    if not (data_dir / "vibe_task.jsonl").is_file():
        raise SystemExit(f"No vibe_task.jsonl in {data_dir}")
    out_dir = ROOT / "results" if data_dir.resolve() == (ROOT / "vibe").resolve() else ROOT / "results" / data_dir.name
    all_items = load_items(data_dir)
    print(f"Dataset: {data_dir.relative_to(ROOT) if data_dir.is_relative_to(ROOT) else data_dir} "
          f"({len(all_items)} questions) -> results in {out_dir.relative_to(ROOT)}/", flush=True)

    t0 = time.time()
    llm, processor = load_llm()
    print(f"\nModel loaded in {time.time() - t0:.0f}s. Ready.", flush=True)

    while True:
        try:
            line = input("describe> ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n(type q to quit)")
            continue
        if line in ("q", "quit", "exit"):
            break
        if not line:
            continue
        parts = line.split()
        prompt_path = Path(parts[0]) if Path(parts[0]).is_absolute() else ROOT / parts[0]
        if not prompt_path.is_file():
            print(f"No such file: {prompt_path}")
            continue
        limit = args.limit
        if len(parts) > 1:
            if not parts[1].isdigit():
                print("Usage: <prompt file> [limit]")
                continue
            limit = int(parts[1])
        try:
            run_experiment(llm, processor, all_items[:limit], prompt_path, data_dir, out_dir)
        except KeyboardInterrupt:
            print("\nRun stopped. Model is still loaded.")
        except Exception as e:  # e.g. RCAC API down: report it and keep the model loaded
            print(f"Run failed: {type(e).__name__}: {e}\nModel is still loaded; fix the problem and try again.")


if __name__ == "__main__":
    main()
