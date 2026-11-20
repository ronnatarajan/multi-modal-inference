#!/usr/bin/env bash
# Start the model in a tmux session named "vlm" (loads once, ~5.5 min, then waits for prompts).
# tmux keeps it running if VS Code / the browser / Claude Code disconnects; it ends with your OnDemand job.
#
# Usage (from the repo root):  bash scripts/start.sh [--limit N]
#   then:  tmux attach -t vlm      watch it / type prompts   (detach again with Ctrl-b then d)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"
SESSION=vlm

if tmux has-session -t "$SESSION" 2>/dev/null; then
    echo "Already running. Attach with: tmux attach -t $SESSION"
    exit 0
fi

# Checks that would otherwise fail several minutes into loading.
nvidia-smi --query-gpu=name --format=csv,noheader 2>/dev/null | grep -q GB10 \
    || { echo "Not on a GB10 (spark) node. Start an OnDemand session on a spark node."; exit 1; }
[ -x .venv/bin/python ] || { echo "No .venv. Run: bash scripts/setup.sh"; exit 1; }
[ -f models/Qwen3-Omni-30B-A3B-Instruct/config.json ] || { echo "No model weights. Run: bash scripts/setup.sh"; exit 1; }
[ -f .env ] && grep -q "^RCAC_API_KEY=." .env \
    || { echo "No RCAC_API_KEY in .env (needed for the decompose step). Copy .env.example to .env and fill it in."; exit 1; }
[ -f vibe/vibe_task.jsonl ] || { echo "No VIBE data in vibe/ (vibe_task.jsonl + videos/)."; exit 1; }

# Arguments go into the tmux command line, so quote each one.
ARGS=""
for a in "$@"; do ARGS+=" $(printf '%q' "$a")"; done

tmux new-session -d -s "$SESSION" -x 220 -y 50
tmux set-option -t "$SESSION" history-limit 100000
# After the program exits, keep the shell open so any error stays readable.
tmux send-keys -t "$SESSION" "source scripts/env.sh && .venv/bin/python run_baseline.py$ARGS" Enter

echo "Loading the model in tmux session '$SESSION' (~5.5 min)."
echo "  Watch / type prompts:  tmux attach -t $SESSION     (detach: Ctrl-b then d)"
echo "  When it says 'Ready.', type a prompt file at 'describe>', e.g. prompts/describe_speaker_focused.txt"
echo "  Don't kill the session until you're done for the day: memory isn't freed on exit (see README)."
