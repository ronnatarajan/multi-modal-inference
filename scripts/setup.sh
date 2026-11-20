#!/usr/bin/env bash
# One-shot setup: Python env + pinned Qwen3-Omni-30B weights, all stored on scratch.
# Safe to re-run: it skips finished steps and resumes partial downloads.
# Run it on a GB10 (spark) node so the GPU matches everyone else's.
#
# Usage (from the repo root):  bash scripts/setup.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
source scripts/env.sh

command -v uv >/dev/null || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }

echo "==> Large files go to: $PROJECT_SCRATCH"

# 1. Virtual environment on scratch, symlinked as .venv so VS Code and scripts find it.
#    Uses uv's own Python, not /usr/bin/python3.12: Triton compiles a C helper at startup and needs
#    Python.h, which the system Python lacks. (Named venv-vllm so it never reuses an older HF venv.)
uv python install 3.12.16
[ -x "$PROJECT_SCRATCH/venv-vllm/bin/python" ] || uv venv --managed-python --python 3.12.16 "$PROJECT_SCRATCH/venv-vllm"
ln -sfn "$PROJECT_SCRATCH/venv-vllm" .venv

# 2. Python packages (exact versions).
uv pip install --python .venv/bin/python -r requirements.txt
ln -sfn "$(.venv/bin/python -c 'import os, imageio_ffmpeg; print(os.path.realpath(imageio_ffmpeg.get_ffmpeg_exe()))')" .venv/bin/ffmpeg

# 3. Model weights at the pinned commit, symlinked into models/.
#    By default, use the team's shared read-only copy on Scholar scratch (no 66 GB download).
#    To download your own copy instead:  SHARED_MODEL_DIR= bash scripts/setup.sh
SHARED_MODEL_DIR="${SHARED_MODEL_DIR-/scratch/scholar/park1643/multi-modal-inference/models/Qwen3-Omni-30B-A3B-Instruct}"
mkdir -p models
if [ -n "$SHARED_MODEL_DIR" ] && [ -r "$SHARED_MODEL_DIR/config.json" ]; then
    echo "==> Using the shared weights at $SHARED_MODEL_DIR"
    WEIGHTS="$SHARED_MODEL_DIR"
else
    [ -n "$SHARED_MODEL_DIR" ] && echo "==> Shared weights not readable at $SHARED_MODEL_DIR; downloading your own copy (66 GB)."
    WEIGHTS="$MODEL_DIR"
    .venv/bin/hf download "$MODEL_REPO" --revision "$MODEL_REVISION" --local-dir "$WEIGHTS"
fi
ln -sfn "$WEIGHTS" models/Qwen3-Omni-30B-A3B-Instruct

# 4. Prove the weights are byte-identical to everyone else's.
echo "==> Verifying checksums (66 GB, takes a few minutes)..."
(cd "$WEIGHTS" && sha256sum -c "$REPO_ROOT/scripts/model.sha256")

echo "==> Done. Start the model with: bash scripts/start.sh"
