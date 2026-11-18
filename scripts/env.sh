# Source this file (don't execute it):  source scripts/env.sh
#
# Points every large download/cache at scratch so the 25 GB home quota is never touched.
# Purdue RCAC sets $RCAC_SCRATCH (e.g. /scratch/scholar/<user>); override PROJECT_SCRATCH to use elsewhere.
# also stores what exact model to download 

export PROJECT_SCRATCH="${PROJECT_SCRATCH:-${RCAC_SCRATCH:-${SCRATCH:?Set PROJECT_SCRATCH to a large-storage directory}}/multi-modal-inference}"

export HF_HOME="$PROJECT_SCRATCH/cache/huggingface"   # Hugging Face hub/datasets cache
export UV_CACHE_DIR="$PROJECT_SCRATCH/cache/uv"       # uv package cache (this is what filled home last time)
export PIP_CACHE_DIR="$PROJECT_SCRATCH/cache/pip"
export UV_PYTHON_INSTALL_DIR="$PROJECT_SCRATCH/cache/uv-python"
export UV_LINK_MODE=copy                              # cache and venv share a filesystem; avoids hardlink warnings
export TORCH_HOME="$PROJECT_SCRATCH/cache/torch"

# Exact model snapshot every teammate should use (Hugging Face commit hash, immutable).
export MODEL_REPO="Qwen/Qwen2.5-Omni-7B"
export MODEL_REVISION="ae9e1690543ffd5c0221dc27f79834d0294cba00"
export MODEL_DIR="$PROJECT_SCRATCH/models/Qwen2.5-Omni-7B"

mkdir -p "$HF_HOME" "$UV_CACHE_DIR" "$PIP_CACHE_DIR" "$TORCH_HOME" "$PROJECT_SCRATCH/models"
