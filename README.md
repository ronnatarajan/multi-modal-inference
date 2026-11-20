# Multi-Modal Inference

Exploring how visual, audio, and textual information can improve social perception and emotion reasoning in video, with a focus on communication between vision-language models (VLMs) and large language models (LLMs).

> **Status:** Research planning. This README describes proposed experiments; it does not report completed implementations or results.

## Running the baseline

Baseline: Qwen3-Omni-30B watches each clip (video + audio) and describes it → GPT-OSS-120B splits the description into single observations → Qwen3-Omni picks A or B. The model runs on vLLM on Scholar's **GB10 (spark) nodes**. All the Scholar-specific fixes are already in the code, so these steps should just work.

**One-time setup** (on a spark node, ~15 min, everything goes to your scratch):

1. `bash scripts/setup.sh`: installs the pinned environment, links the model weights, and verifies their checksums. By default it uses the team's shared read-only copy of the weights on Scholar scratch (`/scratch/scholar/park1643/multi-modal-inference/models/Qwen3-Omni-30B-A3B-Instruct`), so there's no download.
   - **Backup: download your own copy** (66 GB, to your scratch). Use this if the shared copy is unreachable (setup does it automatically then), gone, or fails the checksum:
     ```bash
     SHARED_MODEL_DIR= bash scripts/setup.sh
     ```
     It downloads the same pinned revision, so results are identical either way.
2. `cp .env.example .env` and put your RCAC GenAI key in it (used for the decompose step).
3. Put the VIBE data in `vibe/` (`vibe_task.jsonl` + `videos/`). It's not in git.

**Each session:**

```bash
bash scripts/start.sh --limit 15   # loads the model in a tmux session (~5.5 min)
tmux attach -t vlm                 # watch it; detach with Ctrl-b then d (it keeps running)
```

When it says `Ready.`, type prompt files at `describe>`:

```
describe> prompts/describe_speaker_focused.txt       # runs the first 15 questions
describe> prompts/describe_speaker_focused.txt 50    # this run only: first 50
describe> q                                          # quit when you're done for the day
```

- Prompt files (`describe_*.txt`, `decompose.txt`, `decide.txt`) are re-read on every run: edit, then run again. Python changes need a restart.
- Results go to `results/<prompt name>.jsonl` (`_2`, `_3`, … for reruns, never overwritten), with a copy of the exact prompt in `results/<name>.prompt.txt`.
- Speed: ~5 s per clip when batched (was ~5 min with HF transformers).

**Keep the model loaded all session.** On the GB10 nodes, memory isn't freed when the model exits, so a second load on the same node fails (`Only N GB GPU memory free`). If that happens, or after any crash, start a new OnDemand session. That's why `start.sh` keeps one copy loaded in tmux instead of reloading per run.

**Reproducibility check** (optional, in a fresh session; it uses up that session's memory): `.venv/bin/python scripts/smoke_test.py` must print `Alone vs batched identical: True` and fingerprint **`dcd85083db0cab17`**. A different fingerprint means your setup differs from everyone else's: weights, package versions, or not a GB10.

Using Claude Code? `CLAUDE.md` tells it how to drive the tmux session for you.

## Motivation

Social reasoning depends on subtle cues: facial expressions, body language, gaze, interactions between people, and changes over time. A video description can omit an important cue, introduce an unsupported detail, or assign the wrong meaning to something that is visible. These errors can affect the downstream model's answer.

This project investigates whether better visual representations and more reliable VLM-to-LLM communication improve performance on video-based social perception tasks. It also compares VLM-based pipelines with potentially less expensive 3D convolutional neural network (CNN) approaches.

## Research Questions

- How does performance change when combining video, text, and audio?
- Can structured descriptions and targeted follow-up questions recover missed social cues?
- Can cue verification reduce the effect of hallucinated visual details?
- Does separating physical observations from interpretation improve reasoning?
- How do frozen and task-adapted 3D CNNs compare with VLM-to-LLM pipelines in accuracy and computational cost?
- How sensitive are results to frame sampling, model choice, and adaptation strategy?

## Proposed Approach
prompt modifications, finetune the vlm:
potential prompt mods:
give the vlm a format it must follow for its output to make sure it doesn't miss stuff (ex. Speaker face: … Speaker body: … Other people present: … What others are doing: … Physical contact between anyone: … Where the speaker is looking: … ) → dr goldwasser what their prompt was for vlm
Openai built in vs our own loop for formatting 
Back and forth between LLM and VLM: 
LLM-asks-VLM questioning (ChatCaptioner-style). The LLM reads the first description and asks targeted follow-ups: “What are the people in front of Phoebe doing?” 
Calibrated voting (VIBE-style). Run several pipelines and combine their answers, weighting each by its accuracy on a small calibration set. 
For prompt attach last k messages along with summary of conversation?  (ask goldwasser about this if its possible to do this with vibe dataset)

### Visual Encoder Comparison

Compare the existing multimodal architecture discussed in the project notes with a VLM-to-LLM pipeline:

| Approach | Planned role |
| --- | --- |
| Frozen 3D CNN | Reproduce the reference architecture's visual baseline |
| Adapted 3D CNN | Explore linear probing and task-specific fine-tuning |
| VLM + LLM | Generate visual observations, then combine them with available text and audio information for reasoning |

Explore alternative visual embedding formats and parameter-efficient adaptation, including LoRA where supported by the selected architecture.

### More Reliable Visual Descriptions

Organize experiments around three possible sources of error:

| Error type | Proposed methods |
| --- | --- |
| Missed cues | Structured descriptions, task-aware prompts, targeted LLM-to-VLM follow-ups, and separate descriptions of the beginning, middle, and end of a clip |
| Hallucinated cues | Verification questions, consistency across multiple descriptions, and visible/uncertain confidence tags |
| Misinterpreted cues | Observation-only descriptions and prompts that ask the LLM to consider counter-evidence before answering |

An initial structured description template is:

```text
Speaker face:
Speaker body:
Other people present:
What others are doing:
Physical contact between anyone:
Where the speaker is looking:
Uncertain or unclear observations:
```

The VLM should describe observable details without assigning emotions or motives. The LLM then interprets those details using the available context.

Task-aware descriptions will be tested separately because providing a suggested interpretation may bias the description. Evaluation prompts must avoid revealing target labels.

### Verification and Reasoning

The proposed pipeline is:

1. Sample frames from the video.
2. Generate structured visual observations.
3. Ask targeted follow-up questions about missing or ambiguous details.
4. Verify the cues that the reasoning model intends to use.
5. Condense observations and answers into a summary of relevant facts.
6. Combine the summary with available textual and audio information to produce a task prediction.

Additional experiments will compare descriptions across models and test calibrated voting across multiple pipelines. Voting weights should be estimated using a separate calibration set.

## Experimental Plan

### Datasets

- **VIBE:** Primary evaluation dataset proposed in the project notes.
- **MELD:** Additional dataset proposed for evaluation; task alignment and preprocessing remain to be defined.

Dataset access, licenses, splits, and preprocessing details will be documented before implementation.

### Modality Ablations

Evaluate the following input configurations:

| Configuration | Video | Text | Audio |
| --- | :---: | :---: | :---: |
| Video only | ✓ | | |
| Video + text | ✓ | ✓ | |
| Video + audio | ✓ | | ✓ |
| Video + audio + text | ✓ | ✓ | ✓ |

### Candidate Models

The brainstorming notes identify these candidates; final selection will depend on availability, hardware requirements, and support for the planned experiments:

- InternVL2: 4B, 8B, and 26B variants
- Qwen2.5-VL: 3B and 7B variants
- CogVLM2-Video
- GPT-4o mini as an optional comparison model

The main VLM experiments are intended to use open-source models. The downstream LLM and audio-processing approach remain to be selected.

### Variables to Compare

- Frame count and sampling strategy, including testing beyond the 30-frame limit discussed in the notes where model support permits.
- Free-form versus structured visual descriptions.
- Single-pass descriptions versus iterative VLM/LLM questioning.
- Unfiltered versus verified cues.
- Single descriptions versus consistency across repeated descriptions or different models.
- Frozen models versus task-specific adaptation.
- Individual pipelines versus calibrated ensembles.

### Evaluation

Report scores using the selected datasets' task-appropriate evaluation protocols. Also track computational cost and latency to assess tradeoffs between CNN and VLM approaches.

Keep training, calibration, and evaluation data separate. Review representative failures to distinguish omitted cues, unsupported details, and incorrect interpretations. Metrics, training parameters, and hardware details remain to be finalized.

## Related Work

The project notes draw on:

- VIBE and its discussion of visual social perception, observation-level cues, and calibrated voting.
- A multimodal video/text/audio paper using a 3D CNN visual component.
- ChatCaptioner-style iterative questioning between an LLM and a visual model.
- LLoVi-style summarization before downstream reasoning.
- Hu et al. (2025) and Liu et al. (2025b), mentioned in connection with frame sampling.

Full bibliographic references and links remain to be added after confirming the exact papers.

## Roadmap

- [ ] Confirm reference papers, dataset access, and evaluation tasks.
- [ ] Select models and define the compute budget.
- [ ] Reproduce the baseline pipeline.
- [ ] Run modality and frame-sampling ablations.
- [ ] Implement structured descriptions and iterative questioning.
- [ ] Evaluate cue verification and observation-only prompting.
- [ ] Compare model adaptation and calibrated voting.
- [ ] Report results, costs, and failure analysis.

## Setup

Run these on a Scholar GPU node.

1. Clone the repo and run setup. This installs the Python environment and downloads Qwen2.5-Omni-7B (~22 GB). It takes about 10–20 minutes.

   ```bash
   git clone <repo-url>
   cd multi-modal-inference
   bash scripts/setup.sh
   ```

   Everything large is saved to your scratch folder, not home (home has a 25 GB limit).

2. Download `vibe.zip` from the [VIBE dataset page](https://huggingface.co/datasets/taniarini/vibe/tree/main) (you may need to log in and accept the terms first). Unzip it and put the `vibe` folder in the repo's main folder.

3. Add your GPT-OSS key: [genai.rcac.purdue.edu](https://genai.rcac.purdue.edu/) → Profile → Settings → Account → Secret. Then:

   ```bash
   cp .env.example .env   # paste the key after RCAC_API_KEY=
   ```

4. Test that it works:

   ```bash
   .venv/bin/python scripts/smoke_test.py
   ```

   It should describe a video clip and print `SMOKE TEST PASSED`.

Notes:

- Load the model in code with `from qwen_omni import load_model, GENERATION_KWARGS`. Don't call `from_pretrained` directly, because it hangs on Scholar's GB10 nodes.
- Run `source scripts/env.sh` before installing packages or downloading other models, so they go to scratch.
- Scratch deletes files that go unused for a long time. If the model or `.venv` goes missing, run `bash scripts/setup.sh` again.

## Pipeline

- `qwen_omni.py`: loads Qwen2.5-Omni-7B (the VLM).
- `llm.py`: calls GPT-OSS-120B (the LLM).
- `pipeline.py`: the three steps.
  - `describe()`: inital VLM call, the VLM watches the clip (video + audio) and describes it.
  - `decompose()`: LLM spliting the description into claims.
  - `decide()`: Final VLM call to perform the task, no video input
  - `parse_answer()`: pulls A or B out of the reply.
- `run_baseline.py`: runs `describe` → `decompose` → `decide` over VIBE (one description per video), saves one line per question to `results/`, and prints accuracy.
- `prompts/`: one prompt per step. The describe prompt is picked with `--describe`.

### Describe prompt

We combined VIBE's Level 1 face and body prompts (from its emotion-prediction experiment) into one prompt and added speech. Speech only shows up if the prompt ends with a response format that has a `Speech: "..."` slot; a plain "quote what the speaker says" instruction is ignored.

Two candidates (which should we use?):

- [`prompts/describe_speaker_focused.txt`](prompts/describe_speaker_focused.txt): speaker-focused. Fewer assertions, but less room for hallucination. Sample: [`results/describe_speaker_focused.jsonl`](results/describe_speaker_focused.jsonl)
- [`prompts/describe_speaker_and_surroundings.txt`](prompts/describe_speaker_and_surroundings.txt): speaker + surroundings. More assertions, and more room for hallucination. Sample: [`results/describe_speaker_and_surroundings.jsonl`](results/describe_speaker_and_surroundings.jsonl)

## Results

Results will be added as the implementation develops.
