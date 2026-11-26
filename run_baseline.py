"""Baseline (describe -> decompose -> decide) with Qwen3-Omni on vLLM. Loads the model ONCE, then waits
for you to type a describe prompt file; run as many as you like without reloading.

Start it with:  bash scripts/start.sh        (runs this inside tmux so it survives disconnects)
or directly:    .venv/bin/python run_baseline.py [--limit N] [--data DIR]

--data picks the dataset folder (vibe_task.jsonl + videos/), default vibe/. For the main test set:
    bash scripts/start.sh --data data/sampled100

Then at the prompt:
    describe> prompts/describe_speaker_focused.txt          # run it on the first N questions
    describe> prompts/describe_speaker_focused.txt 30       # override the limit for this run
    describe> prompts/describe_speaker_focused.txt 30:60    # questions 31-60 only (-> <name>_q31-60.jsonl)
    describe> prompts/describe_speaker_focused.txt+prompts/mainprompt_v4 50:100
                                                            # combined: describe with both, join, then decompose
    describe> q                                             # quit (or Ctrl-D)

The describe prompt, decompose.txt and decide.txt are re-read every run, so edit them and run again.
Changes to Python code need a restart. Don't press Ctrl-C during a run: it also reaches vLLM's engine
process, which shuts down (EngineDeadError on every later run), and on GB10 its memory stays held.

Why stay open: loading takes ~5.5 min, and on Scholar's GB10 nodes the memory isn't given back
when the model exits, so a second load on the same node fails. Keep this running all session.

Each run writes results/<prompt name>.jsonl (then _2, _3, ... if it already exists) plus a copy of
the exact prompt text used, results/<same name>.prompt.txt, and the clip descriptions as soon as they
exist, results/<same name>.descriptions.json. With --data other than vibe/, results go in
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


def new_out_path(out_dir, name, tag=""):
    """<out_dir>/<name><tag>.jsonl, or <name><tag>_2.jsonl, _3, ... so earlier runs are never overwritten."""
    stem = name + tag
    path = out_dir / f"{stem}.jsonl"
    k = 2
    while path.exists():
        path = out_dir / f"{stem}_{k}.jsonl"
        k += 1
    return path


def parse_range(arg, n_items):
    """'N' -> questions [0, N); 'A:B' -> questions [A, B) (0-based, B exclusive, so 30:60 = questions 31-60).
    Returns (start, end, tag for the output file name) or None if the argument is malformed."""
    if arg.isdigit():
        return 0, int(arg), ""
    a, sep, b = arg.partition(":")
    if sep and a.isdigit() and b.isdigit() and int(a) < int(b):
        a, b = int(a), min(int(b), n_items)
        return a, b, f"_q{a + 1}-{b}"
    return None


def run_experiment(llm, processor, items, prompt_paths, data_dir, out_dir, tag=""):
    """prompt_paths: one describe prompt, or several (combined run): each clip is described once per prompt and
    the descriptions are joined ("Description 1: ...", "Description 2: ...") before decompose."""
    prompts = [p.read_text() for p in prompt_paths]
    describe_prompt = prompts[0] if len(prompts) == 1 else "\n\n".join(
        f"--- Description {i + 1}: {p.name} ---\n{text}" for i, (p, text) in enumerate(zip(prompt_paths, prompts)))
    videos = list(dict.fromkeys(item["video"] for item in items))  # unique, in order
    t_start = time.time()

    # 1. Describe every clip (VLM, video + audio), in chunks of clips to keep RAM flat (see qwen_omni.CHUNK).
    per_prompt = [dict(zip(videos, generate_in_chunks(
        llm, videos, lambda v, text=text: describe_request(processor, data_dir / "videos" / v, text))))
        for text in prompts]
    if len(prompts) == 1:
        descriptions = per_prompt[0]
    else:
        descriptions = {v: "\n\n".join(f"Description {i + 1}:\n{d[v]}" for i, d in enumerate(per_prompt))
                        for v in videos}
    print(f"Described {len(videos)} clips x {len(prompts)} prompt(s) in {time.time() - t_start:.0f}s", flush=True)

    # Save the descriptions now, so a failure in the steps below doesn't lose them and slow clips can be
    # inspected. A failed run leaves this file without a .jsonl; the next run with this prompt overwrites it.
    out_path = new_out_path(out_dir, "+".join(p.stem for p in prompt_paths), tag)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.with_suffix(".prompt.txt").write_text(describe_prompt)
    out_path.with_suffix(".descriptions.json").write_text(json.dumps(descriptions, ensure_ascii=False, indent=1))

    # 2. Decompose (GPT-OSS on RCAC). Few threads: the server allows 20 calls/min and ask_llm retries on 429.
    # A description that still fails after ask_llm's retries is skipped (its questions count as wrong and
    # are marked decompose_failed) instead of failing the whole run.
    def safe_decompose(video):
        try:
            return decompose(descriptions[video])
        except Exception as e:
            print(f"Decompose failed for {video}: {type(e).__name__}: {e}", flush=True)
            return None

    t0 = time.time()
    with ThreadPoolExecutor(max_workers=4) as pool:
        assertions = dict(zip(videos, pool.map(safe_decompose, videos)))
    failed = [v for v in videos if assertions[v] is None]
    print(f"Decomposed {len(videos) - len(failed)}/{len(videos)} descriptions in {time.time() - t0:.0f}s", flush=True)

    # 3. Decide every question whose clip was decomposed (VLM, text only), one batch.
    t0 = time.time()
    todo = [item for item in items if assertions[item["video"]] is not None]
    decided = dict(zip((item["qid"] for item in todo),
                       generate(llm, [decide_request(processor, assertions[item["video"]], item) for item in todo])))
    replies = [decided.get(item["qid"]) for item in items]
    print(f"Decided {len(todo)} questions in {time.time() - t0:.0f}s", flush=True)

    rel_prompt = "+".join(str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p) for p in prompt_paths)
    correct = unparsed = 0
    with open(out_path, "w") as f:
        for item, reply in zip(items, replies):
            pred = parse_answer(reply) if reply is not None else None
            correct += pred == item["answer"]
            unparsed += pred is None and reply is not None
            f.write(json.dumps({"qid": item["qid"], "video": item["video"], "model": MODEL_NAME,
                                "describe_prompt": rel_prompt,
                                "fact": item["fact"],
                                "inference_A": item["inference_A"], "inference_B": item["inference_B"],
                                "description": descriptions[item["video"]],
                                "assertions": assertions[item["video"]], "reply": reply,
                                "pred": pred, "answer": item["answer"], "correct": pred == item["answer"],
                                "decompose_failed": assertions[item["video"]] is None},
                               ensure_ascii=False) + "\n")

    print(f"\nAccuracy: {correct}/{len(items)} = {correct / len(items):.3f}")
    print(f"Unparseable replies: {unparsed}")
    if failed:
        n_failed = sum(assertions[item["video"]] is None for item in items)
        print(f"Decompose failed (counted wrong): {len(failed)} clips, {n_failed} questions: {', '.join(failed)}")
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
        # "a.txt+b.txt" = combined run: describe each clip with both prompts and join the descriptions.
        prompt_paths = [Path(s) if Path(s).is_absolute() else ROOT / s for s in parts[0].split("+")]
        missing = [p for p in prompt_paths if not p.is_file()]
        if missing:
            print(f"No such file: {missing[0]}")
            continue
        start, end, tag = 0, args.limit, ""
        if len(parts) > 1:
            parsed = parse_range(parts[1], len(all_items))
            if parsed is None:
                print("Usage: <prompt file> [N | A:B]   (N = first N questions; A:B = questions A+1..B, e.g. 30:60)")
                continue
            start, end, tag = parsed
        try:
            run_experiment(llm, processor, all_items[start:end], prompt_paths, data_dir, out_dir, tag)
        except KeyboardInterrupt:
            print("\nRun stopped. Model is still loaded.")
        except Exception as e:  # e.g. RCAC API down: report it and keep the model loaded
            print(f"Run failed: {type(e).__name__}: {e}\nModel is still loaded; fix the problem and try again.")


if __name__ == "__main__":
    main()
