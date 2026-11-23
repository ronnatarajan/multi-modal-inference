#!/usr/bin/env bash
# Start the temporal runner in tmux session "vlm" (same rules as scripts/start.sh: one model load per node).
#
# Usage (from the repo root):  bash experiments/temporal/start.sh [--data DIR] [--limit N]
#   then:  tmux attach -t vlm      (detach again with Ctrl-b then d; don't press Ctrl-C while it loads)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"
SESSION=vlm

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Session '$SESSION' already exists (a model may already be loaded on this node). Attach: tmux attach -t $SESSION"
    exit 0
fi

nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | grep -q GB10 \
    || { echo "Not on a GB10 (spark) node. Start an OnDemand session on a spark node."; exit 1; }
[ -x .venv/bin/python ] || { echo "No .venv. Run: bash scripts/setup.sh"; exit 1; }
[ -f models/Qwen3-Omni-30B-A3B-Instruct/config.json ] || { echo "No model weights. Run: bash scripts/setup.sh"; exit 1; }
[ -f .env ] && grep -q "^RCAC_API_KEY=." .env \
    || { echo "No RCAC_API_KEY in .env (needed for the decompose step). Copy .env.example to .env and fill it in."; exit 1; }

ARGS=""
for a in "$@"; do ARGS+=" $(printf '%q' "$a")"; done

tmux new-session -d -s "$SESSION" -x 220 -y 50
tmux set-option -t "$SESSION" history-limit 100000
tmux send-keys -t "$SESSION" "source scripts/env.sh && .venv/bin/python experiments/temporal/run_temporal.py$ARGS" Enter

echo "Loading the model for temporal prompting in tmux session '$SESSION' (~5.5 min)."
echo "  Watch / type runs:  tmux attach -t $SESSION     (detach: Ctrl-b then d)"
echo "  When it says 'Ready.', type e.g.:  prompts/describe_speaker_focused.txt m=3"
echo "  Don't kill the session until you're done for the day: memory isn't freed on exit (see README)."
