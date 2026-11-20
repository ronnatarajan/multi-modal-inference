"""Pick 100 English VIBE videos (all their questions) with a spread of shows, cue types and emotions.

Inputs are the dataset only: vibe/vibe_task.jsonl text, plus the language/show of each clip
(see english_videos.json and its notes). Fixed seed => same selection every time.

Usage (from the repo root):  .venv/bin/python data/sampled100/sample.py vibe data/sampled100/english_videos.json data/sampled100
"""
import collections, json, math, random, shutil, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from tags import tag

SEED = 577
N_VIDEOS = 100
MIN_PER_SHOW = 10   # a show smaller than its proportional share still gets at least this many videos

vibe, meta_path, out_dir = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
dry = "--dry-run" in sys.argv
meta = json.load(open(meta_path))["videos"]          # {"video_1.mp4": {"show": "Friends"}, ...} English only

rows = [json.loads(l) for l in open(vibe / "vibe_task.jsonl")]
per_video = collections.Counter()
for r in rows:                                        # same per-question ids as run_baseline.py
    r["qid"] = f"{r['task_id']}_{per_video[r['task_id']]}"
    per_video[r["task_id"]] += 1
    r.update(tag(r))

by_video = collections.defaultdict(list)
for r in rows:
    if r["video"] in meta:
        by_video[r["video"]].append(r)
pool = sorted(by_video, key=lambda v: int(v[6:-4]))


def video_tags(v):
    qs = by_video[v]
    return {f"cue:{q['cue']}" for q in qs} | {f"emo:{e}" for q in qs for e in q["emotions"]}


# How common each tag is across the English pool (counted per video).
tag_freq = collections.Counter(t for v in pool for t in video_tags(v))
# Weight: rarer tags make a video more likely to be drawn. Averaged (not summed) over the video's tags,
# so videos with many questions aren't favoured just for having more tags.
weight = {v: sum(1 / tag_freq[t] for t in video_tags(v)) / len(video_tags(v)) for v in pool}

# Show quotas: proportional, but at least MIN_PER_SHOW for small shows.
shows = collections.Counter(meta[v]["show"] for v in pool)
quota = {s: max(MIN_PER_SHOW, round(N_VIDEOS * n / len(pool))) for s, n in shows.items()}
largest = max(quota, key=lambda s: shows[s])
quota[largest] = N_VIDEOS - sum(q for s, q in quota.items() if s != largest)

# Weighted sampling without replacement (Efraimidis-Spirakis): key = u^(1/w), take the top k per show.
rng = random.Random(SEED)
keys = {v: rng.random() ** (1 / weight[v]) for v in pool}   # one draw per video, in fixed pool order
chosen = []
for s in sorted(quota):
    cands = [v for v in pool if meta[v]["show"] == s]
    chosen += sorted(cands, key=lambda v: -keys[v])[:quota[s]]
chosen.sort(key=lambda v: int(v[6:-4]))
questions = [q for v in chosen for q in by_video[v]]


def spread(videos):
    qs = [q for v in videos for q in by_video[v]]
    return {
        "videos": len(videos), "questions": len(qs),
        "show (videos)": collections.Counter(meta[v]["show"] for v in videos),
        "questions per video": collections.Counter(len(by_video[v]) for v in videos),
        "cue (questions)": collections.Counter(q["cue"] for q in qs),
        "emotion in correct inference (questions)": collections.Counter(e for q in qs for e in q["emotions"]),
        "correct inference negated": collections.Counter("negated" if q["negated"] else "not negated" for q in qs),
        "answer": collections.Counter(q["answer"] for q in qs),
    }


full, samp = spread(pool), spread(chosen)
for k in full:
    if not isinstance(full[k], collections.Counter):
        print(f"{k}: pool {full[k]}  sample {samp[k]}")
        continue
    print(f"\n{k}")
    nf, ns = sum(full[k].values()), sum(samp[k].values())
    for name, n in sorted(full[k].items(), key=lambda x: (-x[1], str(x[0]))):
        m = samp[k].get(name, 0)
        print(f"  {str(name):24s} pool {n:4d} ({100*n/nf:4.1f}%)   sample {m:4d} ({100*m/ns:4.1f}%)")

if not dry:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "video_ids.txt").write_text("\n".join(chosen) + "\n")
    # Same layout as vibe/: videos/ next to vibe_task.jsonl.
    (out_dir / "videos").mkdir(exist_ok=True)
    for v in chosen:
        shutil.copy2(vibe / "videos" / v, out_dir / "videos" / v)
    keep = ("task_id", "video", "fact", "inference_A", "inference_B", "answer")
    with open(out_dir / "vibe_task.jsonl", "w") as f:
        for q in questions:
            f.write(json.dumps({k: q[k] for k in keep}, ensure_ascii=False) + "\n")
    with open(out_dir / "tags.jsonl", "w") as f:
        for q in questions:
            f.write(json.dumps({"qid": q["qid"], "video": q["video"], "show": meta[q["video"]]["show"],
                                "cue": q["cue"], "emotions": q["emotions"], "negated": q["negated"]}) + "\n")
    print(f"\nWrote {len(chosen)} videos / {len(questions)} questions to {out_dir}")
