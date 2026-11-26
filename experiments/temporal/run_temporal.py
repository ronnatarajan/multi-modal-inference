"""Temporal change prompting runner. Same workflow as run_baseline.py: loads the model ONCE, then waits for runs.

Start it with:  bash experiments/temporal/start.sh            (tmux session "vlm", default data/sampled100)

Then at the prompt:
    temporal> prompts/describe_speaker_focused.txt m=3                 # all questions, 3 segments
    temporal> prompts/describe_speaker_focused.txt m=3 min=3 limit=20  # test: first 20 questions on clips >= 3 s
    temporal> q

m=1 is the baseline (identical output), so it isn't needed here: use the run_baseline.py results.
The describe prompt, experiments/temporal/prompts/earlier_segments.txt, decompose.txt and decide.txt are
re-read every run. Python changes need a restart (= new session).

Each run writes experiments/temporal/results/<dataset>/<prompt name>_m<m>.jsonl (then _2, _3, ...), plus
<same name>.prompt.txt with the exact describe prompt and earlier-segments block used.
"""
import argparse
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))

import temporal  # noqa: E402  (registers the segment frame reader; must come before any request is built)
from pipeline import decide_request, decompose, parse_answer  # noqa: E402
from qwen_omni import MODEL_NAME, generate, load_llm  # noqa: E402
from run_baseline import load_items  # noqa: E402  (same question ids as the baseline, so runs can be paired)


def new_out_path(out_dir, stem):
    path = out_dir / f"{stem}.jsonl"
    k = 2
    while path.exists():
        path = out_dir / f"{stem}_{k}.jsonl"
        k += 1
    return path


def run_experiment(llm, processor, items, prompt_path, m, data_dir, out_dir, tag=""):
    describe_prompt = prompt_path.read_text()
    block = temporal.EARLIER_BLOCK.read_text()
    videos = list(dict.fromkeys(item["video"] for item in items))
    paths = {v: data_dir / "videos" / v for v in videos}
    t_start = time.time()

    # 1. Describe, segment by segment (VLM, video + audio).
    plans, seg_descs, joined = temporal.describe_all(llm, processor, [paths[v] for v in videos], describe_prompt, m)
    print(f"Described {len(videos)} clips in {time.time() - t_start:.0f}s", flush=True)

    # 2. Decompose (GPT-OSS on RCAC), as in the baseline.
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=4) as pool:
        assertions = dict(zip(videos, pool.map(decompose, (joined[paths[v]] for v in videos))))
    print(f"Decomposed {len(videos)} descriptions in {time.time() - t0:.0f}s", flush=True)

    # 3. Decide (VLM, text only), as in the baseline.
    t0 = time.time()
    replies = generate(llm, [decide_request(processor, assertions[item["video"]], item) for item in items])
    print(f"Decided {len(items)} questions in {time.time() - t0:.0f}s", flush=True)

    out_path = new_out_path(out_dir, f"{prompt_path.stem}_m{m}{tag}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.with_suffix(".prompt.txt").write_text(
        describe_prompt + "\n\n--- experiments/temporal/prompts/earlier_segments.txt ---\n" + block)
    rel_prompt = str(prompt_path.relative_to(ROOT)) if prompt_path.is_relative_to(ROOT) else str(prompt_path)
    correct = unparsed = split_q = split_correct = 0
    with open(out_path, "w") as f:
        for item, reply in zip(items, replies):
            p = plans[paths[item["video"]]]
            pred = parse_answer(reply)
            ok = pred == item["answer"]
            correct += ok
            unparsed += pred is None
            if p["m_eff"] > 1:
                split_q += 1
                split_correct += ok
            segments = [{"label": s["label"], "start": round(s["start"], 3), "end": round(s["end"], 3),
                         "frames": s["frames"], "description": d}
                        for s, d in zip(p["segments"], seg_descs[paths[item["video"]]])]
            f.write(json.dumps({"qid": item["qid"], "video": item["video"], "model": MODEL_NAME,
                                "describe_prompt": rel_prompt, "method": "temporal",
                                "m": m, "m_eff": p["m_eff"], "duration": round(p["duration"], 3),
                                "segments": segments,
                                "fact": item["fact"],
                                "inference_A": item["inference_A"], "inference_B": item["inference_B"],
                                "description": joined[paths[item["video"]]],
                                "assertions": assertions[item["video"]], "reply": reply,
                                "pred": pred, "answer": item["answer"], "correct": ok},
                               ensure_ascii=False) + "\n")

    counts = {k: sum(plans[paths[v]]["m_eff"] == k for v in videos) for k in (1, 2, 3)}
    print(f"\nAccuracy: {correct}/{len(items)} = {correct / len(items):.3f}")
    if split_q:
        print(f"Accuracy on split clips (>= 2 s): {split_correct}/{split_q} = {split_correct / split_q:.3f}")
    print(f"Unparseable replies: {unparsed}")
    print(f"Clips with 1 / 2 / 3 segments: {counts[1]} / {counts[2]} / {counts[3]}")
    print(f"Total time: {time.time() - t_start:.0f}s  -> {out_path.relative_to(ROOT)}\n", flush=True)


def parse_line(line, default_limit):
    """'<prompt file> m=<2|3> [limit=N] [min=S] [range=A:B]' -> (path, m, limit, min_s, rng), or an error string.
    range=A:B takes questions A+1..B (0-based, B exclusive), like run_baseline.py's 'A:B'."""
    parts = line.split()
    opts = {}
    for part in parts[1:]:
        key, sep, value = part.partition("=")
        if not sep or key not in ("m", "limit", "min", "range"):
            return "Usage: <prompt file> m=<1|2|3> [limit=N] [min=SECONDS] [range=A:B]"
        opts[key] = value
    try:
        m = int(opts.get("m", ""))
        limit = int(opts["limit"]) if "limit" in opts else default_limit
        min_s = float(opts.get("min", 0))
        rng = None
        if "range" in opts:
            a, b = (int(x) for x in opts["range"].split(":"))
            if not 0 <= a < b:
                raise ValueError
            rng = (a, b)
    except ValueError:
        return "Usage: <prompt file> m=<1|2|3> [limit=N] [min=SECONDS] [range=A:B]"
    if m not in (1, 2, 3):
        return "m must be 1, 2 or 3"
    path = Path(parts[0]) if Path(parts[0]).is_absolute() else ROOT / parts[0]
    if not path.is_file():
        return f"No such file: {path}"
    return path, m, limit, min_s, rng


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--limit", type=int, default=None, help="default number of questions per run (default: all)")
    parser.add_argument("--data", default="data/sampled100", help="dataset folder (default: data/sampled100)")
    args = parser.parse_args()
    data_dir = Path(args.data) if Path(args.data).is_absolute() else ROOT / args.data
    if not (data_dir / "vibe_task.jsonl").is_file():
        raise SystemExit(f"No vibe_task.jsonl in {data_dir}")
    out_dir = HERE / "results" / data_dir.name
    all_items = load_items(data_dir)
    print(f"Dataset: {data_dir.name} ({len(all_items)} questions) -> results in {out_dir.relative_to(ROOT)}/",
          flush=True)

    t0 = time.time()
    llm, processor = load_llm()
    print(f"\nModel loaded in {time.time() - t0:.0f}s. Ready.", flush=True)

    durations = {}
    while True:
        try:
            line = input("temporal> ").strip()
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n(type q to quit)")
            continue
        if line in ("q", "quit", "exit"):
            break
        if not line:
            continue
        parsed = parse_line(line, args.limit)
        if isinstance(parsed, str):
            print(parsed)
            continue
        prompt_path, m, limit, min_s, rng = parsed
        items, tag = all_items, ""
        if rng:
            items = all_items[rng[0]:rng[1]]
            tag = f"_q{rng[0] + 1}-{min(rng[1], len(all_items))}"
        if min_s:
            for v in {i["video"] for i in items} - durations.keys():
                durations[v] = temporal.plan(data_dir / "videos" / v, 1)["duration"]
            items = [i for i in items if durations[i["video"]] >= min_s]
        items = items[:limit]
        if not items:
            print("No questions match.")
            continue
        try:
            run_experiment(llm, processor, items, prompt_path, m, data_dir, out_dir, tag)
        except KeyboardInterrupt:
            print("\nRun stopped. Model is still loaded.")
        except Exception as e:  # e.g. RCAC API down: report it and keep the model loaded
            print(f"Run failed: {type(e).__name__}: {e}\nModel is still loaded; fix the problem and try again.")


if __name__ == "__main__":
    main()
