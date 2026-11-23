# Temporal change prompting

Proposal Section 3.1. Does describing a clip piece by piece, in order, help the model notice how the speaker
changes over time, compared with describing the whole clip at once?

Only stage 1 (describe) differs from the baseline. Decompose and decide are the baseline's (`pipeline.py`,
`prompts/decompose.txt`, `prompts/decide.txt`), and all model settings come from the shared `qwen_omni.py`.

## Method

- **Segments.** Each clip is cut into *m* equal time segments, *m* = 2 or 3. (*m* = 1 is the baseline; use the
  `run_baseline.py` results for it.)
- **Frames.** The baseline's 36 frames are split evenly: 18 per segment for *m* = 2, 12 for *m* = 3, evenly
  spaced within each segment.
- **Audio.** Each segment gets only the audio for its own time window.
- **Short clips.** Every segment must be at least 1 s long, so a clip gets *m*_eff = min(*m*, ⌊length in s⌋)
  segments. A clip under 2 s is never split: it gets exactly the baseline's request and description. In
  sampled100 (100 clips):

  | | 1 segment (= baseline) | 2 segments | 3 segments |
  |---|---|---|---|
  | *m* = 2 | 33 | 67 | – |
  | *m* = 3 | 33 | 39 | 28 |

- **Prompt.** Every segment gets the baseline describe prompt unchanged (`prompts/describe_speaker_focused.txt`).
  Segment 1 gets only that. Later segments also get the earlier segments' descriptions, through
  [`prompts/earlier_segments.txt`](prompts/earlier_segments.txt), which is placed before the baseline prompt.
- **Order.** Round 1 describes segment 1 of every clip as one batch (plus every unsplit clip), round 2
  segment 2, and so on.
- **Output.** The segment descriptions are joined with time labels and sent to decompose in place of the
  baseline's single description:

  ```
  Beginning (0.0-1.2 s):
  ...
  Middle (1.2-2.3 s):
  ...
  End (2.3-3.5 s):
  ...
  ```

**What a result means.** The method changes two things relative to the baseline: the clip is segmented, and
later segments see the earlier descriptions. A difference from the baseline is the effect of the method as a
whole; it does not say which of the two caused it. (Separating them would need one more condition: segments
without the earlier-descriptions block.)

## Running it

Needs a fresh OnDemand session on a GB10 node, like the baseline (one model load per node).

```bash
bash experiments/temporal/start.sh        # tmux session "vlm", dataset data/sampled100 (238 questions)
tmux attach -t vlm                        # detach with Ctrl-b then d; don't press Ctrl-C while it loads
```

At `temporal>`:

```
prompts/describe_speaker_focused.txt m=3 min=3 limit=20   # test: first 20 questions on clips >= 3 s
prompts/describe_speaker_focused.txt m=2                  # full run, all 238 questions
prompts/describe_speaker_focused.txt m=3
q                                                         # quit for the day
```

`prompts/earlier_segments.txt` and the describe, decompose and decide prompts are re-read every run, so they
can be edited between runs without reloading. Python changes need a new session.

Results go to `results/sampled100/<prompt name>_m<m>.jsonl` in this folder (`_2`, `_3`, ... for reruns),
with `<same name>.prompt.txt` holding the exact describe prompt and earlier-segments block used. Rows have the
baseline's fields plus `m`, `m_eff`, `duration` and `segments` (label, start, end, frames and description of
each segment); `description` is the joined text that went to decompose.

**What to check in the test run** (then edit `prompts/earlier_segments.txt` if needed):

- Does the time order (beginning/middle/end) survive into `assertions`? If not, decompose needs a change, and
  that change would have to apply to every method, the baseline included.
- Words cut at a segment boundary: garbled, missing or quoted twice.
- Segments with no speech: does the model say so, or invent words?
- Does every segment describe the same main speaker?

## Comparing with the baseline

```bash
.venv/bin/python experiments/temporal/compare.py \
    results/sampled100/describe_speaker_focused.jsonl \
    experiments/temporal/results/sampled100/describe_speaker_focused_m2.jsonl \
    experiments/temporal/results/sampled100/describe_speaker_focused_m3.jsonl
```

For every run: accuracy on all questions and on the split clips (≥ 2 s), with an exact McNemar test on the
paired answers. The two runs must use the same frame count (36) and the same questions.

## Files

- `temporal.py`: segment planning, the segment frame reader, segment prompts, stage 1 for all clips.
- `run_temporal.py`: the interactive runner (same workflow as `run_baseline.py`).
- `start.sh`: starts the runner in tmux.
- `compare.py`: accuracy and McNemar test against a reference run.
- `prompts/earlier_segments.txt`: the block that passes earlier descriptions forward.
- `results/`: this method's results.
