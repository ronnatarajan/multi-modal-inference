# Multi-Modal Inference

Exploring how visual, audio, and textual information can improve social perception and emotion reasoning in video, with a focus on communication between vision-language models (VLMs) and large language models (LLMs).

> **Status:** Research planning. This README describes proposed experiments; it does not report completed implementations or results.

## Running the baseline

Baseline: Qwen3-Omni-30B watches each clip (video + audio) and describes it → GPT-OSS-120B splits the description into single observations → Qwen3-Omni picks A or B. The model runs on vLLM on Scholar's **GB10 (spark) nodes**. All the Scholar-specific fixes are already in the code, so these steps should just work.

### Mac terminal workflow for Scholar

Replace `PURDUE_USERNAME` with your Purdue username. See the [Scholar SSH guide](https://www.rcac.purdue.edu/knowledge/scholar/accounts) and [Scholar Spark guide](https://www.rcac.purdue.edu/knowledge/scholar/scholar-spark).

**Mac terminal:** Connect to Scholar and keep this SSH session open while the interactive allocation runs.

```bash
ssh PURDUE_USERNAME@scholar.rcac.purdue.edu
```

**Scholar login node:** Create the checkout parent directory and request an interactive Spark allocation. Run setup and inference on the allocated node.

```bash
mkdir -p ~/cs577
sinteractive -A scholar --partition=spark-interactive --qos=normal \
  --time=02:00:00 --nodes=1 --cpus-per-task=10 --gres=gpu:1
```

**Allocated Spark compute node:** Initialize the Spark module tree and verify your allocation. Expect a `scholar-k*` or `scholar-l*` hostname, `aarch64`, and a Slurm job ID.

```bash
source /etc/profile
module load modtree/spark
hostname
uname -m
echo "$SLURM_JOB_ID"
```

For the initial checkout, clone the private repository into `~/cs577/multi-modal-inference` if GitHub authentication is configured on Scholar. Your Mac's GitHub authentication does not automatically carry over. Alternatively, copy your local clone once from a **second Mac terminal** after creating `~/cs577`:

```bash
rsync -av \
  --exclude='.venv' --exclude='.env' --exclude='models/' \
  --exclude='vibe/' --exclude='__pycache__/' \
  ~/Desktop/multi-modal-inference \
  PURDUE_USERNAME@scholar.rcac.purdue.edu:~/cs577/
```

For ongoing Codex development, edit the Scholar checkout directly with the RCAC MCP bridge. Check the registrations with `codex mcp list` on the Mac and confirm the session exposes remote file and command tools. Read `/etc/agents.d/AGENTS.md` before working on Scholar.

**Allocated Spark compute node, one-time setup:**

```bash
cd ~/cs577/multi-modal-inference
bash scripts/setup.sh
cp -n .env.example .env
nano .env
```

Enter `RCAC_API_KEY` privately in the editor and keep `.env` out of Git. Setup puts the pinned environment, model and caches on scratch. It uses the team's shared weights when accessible and downloads the pinned Qwen3-Omni-30B-A3B-Instruct weights to personal scratch if the shared config is unreadable. If the shared weights fail validation, use `SHARED_MODEL_DIR= bash scripts/setup.sh`. Reuse the installed environment and weights across sessions. Run setup again if scratch has purged them.

Place the [VIBE dataset](https://huggingface.co/datasets/taniarini/vibe/tree/main) at `vibe/vibe_task.jsonl` and `vibe/videos/`. The dataset is distributed separately from Git. If you already have it locally, put the large dataset on scratch and symlink it into the checkout. On Scholar, run `source scripts/env.sh`, check space with `myquota`, then run `mkdir -p "$PROJECT_SCRATCH/vibe"`. From the **second Mac terminal**, copy the dataset using the default scratch path:

```bash
rsync -av ~/Desktop/multi-modal-inference/vibe/ \
  PURDUE_USERNAME@scholar.rcac.purdue.edu:/scratch/scholar/PURDUE_USERNAME/multi-modal-inference/vibe/
```

Back in the **Spark shell**, if the checkout has no `vibe` entry, run `ln -s "$PROJECT_SCRATCH/vibe" vibe`.

**Allocated Spark compute node, each session:**

```bash
cd ~/cs577/multi-modal-inference
bash scripts/start.sh --limit 15
tmux attach -t vlm
```

For the 238-question sampled test set, start with `bash scripts/start.sh --data data/sampled100`. The launcher currently checks for the default `vibe/vibe_task.jsonl` even when `--data` is supplied.

**Application prompt:** Wait about 5.5 minutes for `Ready.`, then enter `prompts/describe_speaker_focused.txt` at `describe>`. Enter another description prompt path to rerun, or append a question limit, for example `prompts/describe_speaker_focused.txt 50`. The description, decomposition and decision prompts are read from disk for each run. Python changes take effect when a new runner starts.

Results go to `results/<prompt name>.jsonl` with the exact description prompt in `results/<name>.prompt.txt`. Reruns get suffixes such as `_2`. Results for `--data data/sampled100` go under `results/sampled100/`.

- Press **Ctrl+B**, release, then press **D** to detach without interrupting Python. Reattach with `tmux attach -t vlm` on the same compute node. A login-node shell sees its own tmux server.
- **Ctrl+C** interrupts the foreground operation. During a baseline run, the runner catches it and returns to `describe>`. During model startup, it can stop the loader.
- Keep the parent SSH session and interactive allocation open. The Slurm wall time applies even when tmux is detached.
- When finished, enter `q` at `describe>`, then exit the remaining tmux shell and leave the allocation. The launcher leaves the shell open to preserve errors. If it says `Already running`, attach and check whether you see `describe>`, loader output, or an idle shell.
- On GB10, model memory can stay occupied after Python exits. After a crash or an `Only N GB GPU memory free` error, follow the repository recovery procedure and start a fresh Spark session on a node with free memory. Keep one model load per session.

**Reproducibility check** (optional, in a fresh session; it uses up that session's memory): `.venv/bin/python scripts/smoke_test.py` must print `Alone vs batched identical: True` and fingerprint **`00a0f821ec7552e2`** (36 frames, current `prompts/describe_speaker_focused.txt`; editing that prompt or the frame count changes it). A different fingerprint means your setup differs from everyone else's: weights, package versions, or not a GB10.

**Other methods** live in `experiments/`, each with its own README, runner and results, and reuse the shared model code. Temporal change prompting: [`experiments/temporal/`](experiments/temporal/README.md).

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

## Pipeline

- `qwen_omni.py` loads Qwen3-Omni-30B-A3B-Instruct through the vLLM Python API.
- `llm.py` calls GPT-OSS-120B through RCAC GenAI.
- `pipeline.py` builds requests with `describe_request()` and `decide_request()`, calls GPT-OSS in `decompose()`, and extracts A or B with `parse_answer()`.
- `run_baseline.py` describes and decomposes once per video, then answers each question from its claims and writes one JSONL row per question.
- `prompts/` contains the baseline prompts. Select the description prompt at `describe>`.

### Describe prompt

We combined VIBE's Level 1 face and body prompts (from its emotion-prediction experiment) into one prompt and added speech. Speech only shows up if the prompt ends with a response format that has a `Speech: "..."` slot; a plain "quote what the speaker says" instruction is ignored.

Two candidates (which should we use?):

- [`prompts/describe_speaker_focused.txt`](prompts/describe_speaker_focused.txt): speaker-focused. Fewer assertions, but less room for hallucination. Sample: [`results/describe_speaker_focused.jsonl`](results/describe_speaker_focused.jsonl)
- [`prompts/describe_speaker_and_surroundings.txt`](prompts/describe_speaker_and_surroundings.txt): speaker + surroundings. More assertions, and more room for hallucination. Sample: [`results/describe_speaker_and_surroundings.jsonl`](results/describe_speaker_and_surroundings.jsonl)

## Results

Results will be added as the implementation develops.
