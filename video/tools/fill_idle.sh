#!/usr/bin/env bash
# While a narration run is going (PID $1), use the idle cores: align the lines it has finished, then render every
# scene whose narration is complete (render_all.py --ready-only). One extra job at a time beside synthesis.
set -u
cd "$(dirname "$0")/../.."
LOG=video/build/logs/fill_idle.log
while kill -0 "$1" 2>/dev/null; do
  echo "== $(date +%T) align" >> "$LOG"
  OMP_NUM_THREADS=4 uv run --project video/tts python -E -s -u video/tts/align.py --threads 4 >> "$LOG" 2>&1
  kill -0 "$1" 2>/dev/null || break
  echo "== $(date +%T) render ready scenes" >> "$LOG"
  uv run --project video/scenes python -I video/tools/render_all.py --ready-only >> "$LOG" 2>&1
  grep -E "^(ok|FAIL) |scenes rendered" "$LOG" | tail -1
  sleep 120
done
echo "fill_idle: narration run $1 ended at $(date +%T)"
