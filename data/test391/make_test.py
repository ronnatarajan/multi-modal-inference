"""Build data/test391: the held-out TEST set. It shares no clips with data/sampled100 (now the dev set).

It is every question on the English VIBE clips that are NOT in sampled100 (175 clips, 391 questions).
Clips are shuffled with a fixed seed, keeping each clip's questions together, so `<prompt> N` in the
runner (which takes the first N questions) gives a random sample of clips, not the lowest video numbers.

Run from the repo root, with vibe/ in place:
    python3 data/test391/make_test.py
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "data" / "test391"
SEED = 577

test_videos = {json.loads(line)["video"] for line in open(ROOT / "data" / "sampled100" / "vibe_task.jsonl")}
english = set(json.load(open(ROOT / "data" / "sampled100" / "english_videos.json"))["videos"])
items = [json.loads(line) for line in open(ROOT / "vibe" / "vibe_task.jsonl")]

by_video = {}
for item in items:
    if item["video"] in english and item["video"] not in test_videos:
        by_video.setdefault(item["video"], []).append(item)

videos = sorted(by_video, key=lambda v: int(v.split("_")[1].split(".")[0]))
random.Random(SEED).shuffle(videos)

with open(OUT / "vibe_task.jsonl", "w") as f:
    for v in videos:
        for item in by_video[v]:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
(OUT / "video_ids.txt").write_text("\n".join(videos) + "\n")

# The runner reads <data>/videos/<file>. Link to the full dataset instead of copying ~200 MB into git.
link = OUT / "videos"
if not link.exists():
    link.symlink_to(Path("..") / ".." / "vibe" / "videos")

n = sum(len(by_video[v]) for v in videos)
assert not set(videos) & test_videos
print(f"wrote {n} questions on {len(videos)} clips to {OUT.relative_to(ROOT)}/ (no clip overlap with sampled100)")
