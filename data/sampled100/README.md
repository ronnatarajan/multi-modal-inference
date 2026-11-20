# sampled100: main test set

100 English VIBE videos and every question on them (238 questions). Picked from the dataset alone, with no
model outputs, using a fixed seed (577), so rerunning gives the same set.

## Files

- `videos.txt`: the 100 chosen videos.
- `vibe_task.jsonl`: their 238 questions, in the same format as `vibe/vibe_task.jsonl`.
- `tags.jsonl`: the tags used for the spread (show, cue type, meaning, negated) for each question.
- `english_videos.json`: the 275 English videos and the show each one is from.
- `sample.py` and `tags.py`: the selection code.

To regenerate (from the repo root, with `vibe/` in place):

```bash
.venv/bin/python data/sampled100/sample.py vibe data/sampled100/english_videos.json data/sampled100
```

## How the videos were picked

1. **English only.** The release has no language field. The clips fall into two groups by the tool that
   encoded them (the `encoder` tag in each mp4). The 158 clips encoded with `Lavf61.7.100` are Chinese dramas
   with Chinese subtitles burned in, and the 275 encoded with `Lavf58.29.100` are English sitcoms. This was
   checked by viewing frames, and it matches the paper (clips from English and Chinese shows in MC-EIU).
2. **Show.** The release has no show field either. Each English clip was labelled by viewing a frame: 258
   *Friends* and 17 *The Big Bang Theory* (videos 8, 14, 19, 26, 34, 43, 52, 59, 80, 102, 105, 116, 137, 148,
   287, 359, 428). These labels are by eye and could contain a mistake.
3. **Tags** (`tags.py`, keyword rules on the dataset text):
   - *cue type* of the `fact`: face, smile/laugh, gaze, hands/gesture, posture/movement, voice/speech.
   - *meaning* named in the correct inference: anger, joy, sadness, fear/anxiety, surprise,
     disgust/contempt, calm, engagement, intensity/emphasis, confusion, or other. VIBE has no emotion labels;
     these are keyword matches on the inference text, and one inference can get several.
4. **Draw.** Each show gets a quota: proportional, but at least 10 videos, so TBBT gets 10 and Friends 90.
   Within each show, videos are drawn by seeded weighted sampling without replacement. A video's weight is
   the average rarity of its tags (1 / how many pool videos share each tag), so videos with rare cues or
   meanings are more likely to be picked without favouring videos that have many questions. Every question
   of a chosen video is kept. The A/B answer and negation were not used to choose, and are only reported.

## Spread

| | English pool | sampled100 |
|---|---|---|
| Videos / questions | 275 / 629 | 100 / 238 |
| Friends / TBBT videos | 258 / 17 | 90 / 10 |
| Videos with 1 / 2 / 3 / 4 / 5 / 6 questions | 98 / 81 / 46 / 23 / 23 / 4 | 33 / 28 / 18 / 10 / 11 / 0 |

| Cue type (share of questions) | Pool | Sample |
|---|---|---|
| Face | 53% | 47% |
| Smile/laugh | 12% | 16% |
| Hands/gesture | 14% | 13% |
| Gaze | 8% | 8% |
| Voice/speech | 7% | 9% |
| Posture/movement | 6% | 7% |

| Meaning in correct inference (share of tags) | Pool | Sample |
|---|---|---|
| Intensity/emphasis | 24% | 18% |
| Anger | 17% | 14% |
| Joy | 13% | 15% |
| Engagement/attention | 10% | 10% |
| Sadness | 8% | 9% |
| Fear/anxiety | 8% | 8% |
| Surprise | 6% | 7% |
| Calm/relaxed | 3% | 5% |
| Disgust/contempt | 3% | 4% |
| Confusion/uncertainty | 2% | 2% |
| Other (no keyword) | 6% | 8% |

Answer A / B: 49% / 51% (pool 51% / 49%). Correct inference is a negation: 15% (pool 15%).
