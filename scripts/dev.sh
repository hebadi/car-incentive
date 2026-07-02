#!/usr/bin/env bash
set -euo pipefail

# IncentiveDrive Local Dev Servers
# Starts the API and web app together, streams both logs, and stops
# both cleanly on Ctrl+C.
# Usage:
#   ./scripts/dev.sh

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$ROOT_DIR"

LOG_DIR="$ROOT_DIR/.dev-logs"
mkdir -p "$LOG_DIR"

cleanup() {
  echo ""
  echo "Stopping dev servers..."
  kill "$API_PID" "$WEB_PID" 2>/dev/null || true
}
trap cleanup EXIT INT TERM

(cd apps/api && source .venv/bin/activate && uvicorn app.main:app --reload --port 8000) > "$LOG_DIR/api.log" 2>&1 &
API_PID=$!

npm run dev:web > "$LOG_DIR/web.log" 2>&1 &
WEB_PID=$!

echo "API starting on http://localhost:8000 (logs: $LOG_DIR/api.log)"
echo "Web starting on http://localhost:3000 (logs: $LOG_DIR/web.log)"
echo "Press Ctrl+C to stop both."
echo ""

tail -f "$LOG_DIR/api.log" "$LOG_DIR/web.log"
