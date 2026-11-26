# test391: held-out test set

391 questions on 175 English VIBE clips: every English clip that is **not** in `data/sampled100`.
It shares no clips with `sampled100`.

| Set | Role | Questions | Clips |
| --- | --- | --- | --- |
| `data/sampled100` | **dev**: develop prompts here, in batches, against the baseline | 238 | 100 |
| `data/test391` | **test**: run each finished method once, never tune on it | 391 | 175 |

`sampled100` was used to develop `mainprompt` v1-v3, so it is the dev set. Keep `test391` for final
numbers only: don't look at its per-question results while changing a prompt.

Already on record here (run before this set was made the test set, with v3 already final):
`describe_speaker_and_surroundings` and `mainprompt_v3` on the first 200 questions.

## Running (final evaluation only)

```bash
bash scripts/start.sh --data data/test391
```

then at `describe>`: `prompts/<prompt>` for all 391 (or `prompts/<prompt> 200` to match the runs above).
Results go to `results/test391/`. Clips are in a seeded random order (questions of one clip stay
together), so the first N questions are a random sample of clips; the first 200 cover 87 clips.

## Files

- `vibe_task.jsonl`: the 391 questions, same format as `vibe/vibe_task.jsonl`.
- `video_ids.txt`: the 175 clips, in run order.
- `videos`: a link to `../../vibe/videos` (the full dataset), so the clips are not copied into git.
- `make_test.py`: rebuilds the set (`python3 data/test391/make_test.py`, seed 577).
