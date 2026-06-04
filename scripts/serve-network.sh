#!/usr/bin/env bash
# Serve the dashboard on all network interfaces so others on your LAN can open it.
set -euo pipefail

PORT="${1:-8080}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "YOUR_LOCAL_IP")

echo "Serving EASY Residency S3 dashboard from:"
echo "  $PROJECT_ROOT"
echo
echo "  On this Mac:     http://localhost:$PORT"
echo "  On same Wi‑Fi:    http://${IP}:$PORT"
echo
echo "Press Ctrl+C to stop."
echo

cd "$PROJECT_ROOT"
exec python3 -m http.server "$PORT" --bind 0.0.0.0
