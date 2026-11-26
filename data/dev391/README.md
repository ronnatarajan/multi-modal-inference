# dev391: development set (no overlap with the test set)

391 questions on 175 English VIBE clips: every English clip that is **not** in `data/sampled100`.
Use this set to try out and compare prompt changes. Keep `data/sampled100` for final evaluation only,
so its numbers stay an honest held-out test.

| Set | Use | Questions | Clips |
| --- | --- | --- | --- |
| `data/dev391` | develop and compare prompts, as often as needed | 391 | 175 |
| `data/sampled100` | final test, once per finished method | 238 | 100 |

The first 50 questions of `sampled100` were already used to develop `mainprompt` v1-v3, so for the test
score of those prompts use the held-out 187 (questions 51-238 minus video_72); `scripts/summarize_results.py`
reports that split.

## Running

```bash
bash scripts/start.sh --data data/dev391
```

then at `describe>`: `prompts/<prompt> 100` for a quick run or `prompts/<prompt>` for all 391.
Results go to `results/dev391/`. Clips are in a seeded random order (questions of one clip stay
together), so the first N questions are a random sample of clips; the first 100 questions cover 42 clips.
Compare two prompts on the **same** N, e.g.
`python3 scripts/compare_runs.py results/dev391/<a>.jsonl results/dev391/<b>.jsonl`.

## Files

- `vibe_task.jsonl`: the 391 questions, same format as `vibe/vibe_task.jsonl`.
- `video_ids.txt`: the 175 clips, in run order.
- `videos`: a link to `../../vibe/videos` (the full dataset), so the clips are not copied into git.
  Needs `vibe/` in place, as for the baseline.
- `make_dev.py`: rebuilds the set (`python3 data/dev391/make_dev.py`, seed 577).
