# Project notes for Claude Code

Baseline pipeline for VIBE (video social-perception A/B questions): Qwen3-Omni-30B on vLLM describes each clip
(video + audio) → GPT-OSS-120B (RCAC API, `llm.py`) decomposes the description → Qwen3-Omni answers A/B.
Files: `qwen_omni.py` (model loading, every setting is a fix for Scholar's GB10 nodes, read the comments
before changing any), `pipeline.py` (prompts → requests), `run_baseline.py` (interactive runner), `prompts/`.
Setup and usage for humans: README.md "Running the baseline".

## Running the model: always through tmux

The model takes ~5.5 min to load, and on GB10 nodes **its memory is not freed when the process exits**
(it stays held with no process visible; only a new OnDemand session clears it). So:

- Start it once per session: `bash scripts/start.sh [--limit N]`. This runs `run_baseline.py` in tmux session `vlm`.
  Never run `run_baseline.py` or `scripts/smoke_test.py` as your own background task: your tasks die when
  Claude Code restarts, and that kills the model and strands the memory.
- Wait for it: `until tmux capture-pane -t vlm -p | grep -qE "Ready\.|Error|Only .* GB"; do sleep 5; done`
- Run an experiment: `tmux send-keys -t vlm "prompts/<file>.txt [limit]" Enter`, then wait for
  `Total time:` (or `Run failed`) and read the summary with `tmux capture-pane -t vlm -p -S -60`.
  Full outputs are in `results/<prompt name>[_N].jsonl`.
- Never kill session `vlm`, Ctrl-C the loader, or start a second model load on the same node. To stop for
  the day, send `q`. If startup prints `Only N GB GPU memory free`, tell the user to start a new OnDemand session.
- Prompt and `.txt` edits apply on the next run without restarting; Python edits need a restart (= new session).

## Reproducibility (the team's top requirement)

Five people run this and must get identical outputs. Don't change sampling, `VLLM_BATCH_INVARIANT`,
prefix caching, pinned versions (`requirements.txt`), the weights revision (`scripts/env.sh`), or the
frame sampling without telling the user: any of these changes everyone's results. `scripts/smoke_test.py`
must print fingerprint `00a0f821ec7552e2` (see README).

## GB10 failure modes already solved (don't rediscover them)

- Any single GPU allocation ≥ 4 GiB faults with "CUDA error: illegal memory access" (plain PyTorch too) →
  `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`. An illegal-memory-access crash is this, not a kernel bug.
- Default mmap weight loading hangs forever on scratch (NFS) → `safetensors_load_strategy="eager"`.
- Triton needs `Python.h` → the venv must use uv's managed Python (setup.sh does this), not /usr/bin/python3.
- FlashInfer sampler JIT needs `ninja` → `VLLM_USE_FLASHINFER_SAMPLER=0`.
- torchcodec can't find FFmpeg and torchvision's video reader is gone → frames are read with PyAV (`qwen_omni.py`).
- Cheap debugging without a fresh node: same `LLM()` args plus `load_format="dummy"`,
  `hf_overrides={"thinker_config": {"text_config": {"num_hidden_layers": 2}}}`, `gpu_memory_utilization=0.12`.
