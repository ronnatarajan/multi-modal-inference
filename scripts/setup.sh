#!/usr/bin/env bash
# One-shot setup: Python env + pinned Qwen2.5-Omni-7B weights, all stored on scratch.
# Safe to re-run: it skips finished steps and resumes partial downloads.
#
# Usage (from the repo root):  bash scripts/setup.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
source scripts/env.sh

command -v uv >/dev/null || { echo "Installing uv..."; curl -LsSf https://astral.sh/uv/install.sh | sh; export PATH="$HOME/.local/bin:$PATH"; }

echo "==> Large files go to: $PROJECT_SCRATCH"

# 1. Virtual environment on scratch, symlinked as .venv so VS Code and scripts find it.
[ -x "$PROJECT_SCRATCH/venv/bin/python" ] || uv venv --python 3.12 "$PROJECT_SCRATCH/venv"
ln -sfn "$PROJECT_SCRATCH/venv" .venv

# 2. Python packages (exact versions).
uv pip install --python .venv/bin/python -r requirements.txt --index-strategy unsafe-best-match
ln -sfn "$(.venv/bin/python -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())')" .venv/bin/ffmpeg

# 3. Model weights at the pinned commit, symlinked into models/.
mkdir -p models
ln -sfn "$MODEL_DIR" models/Qwen2.5-Omni-7B
.venv/bin/hf download "$MODEL_REPO" --revision "$MODEL_REVISION" --local-dir "$MODEL_DIR"

# 4. Prove the weights are byte-identical to everyone else's.
echo "==> Verifying checksums (takes a minute)..."
(cd "$MODEL_DIR" && sha256sum -c "$REPO_ROOT/scripts/model.sha256")

echo "==> Done. Test with: .venv/bin/python scripts/smoke_test.py"
