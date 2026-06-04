#!/usr/bin/env bash
# Check that X profile URLs in data/projects.json return HTTP 200 (or redirect).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
JSON="$PROJECT_ROOT/data/projects.json"

if [[ ! -f "$JSON" ]]; then
  echo "Missing $JSON" >&2
  exit 1
fi

echo "Checking X profile URLs from $JSON..."
echo

urls=$(python3 - <<'PY'
import json, sys
with open(sys.argv[1]) as f:
    data = json.load(f)
for p in data["projects"]:
    for h in p.get("x_handles", []):
        url = h.get("profile_url")
        if url:
            print(url)
PY
"$JSON")

ok=0
fail=0
while IFS= read -r url; do
  [[ -z "$url" ]] && continue
  code=$(curl -sL -o /dev/null -w "%{http_code}" -A "Mozilla/5.0" "$url" || echo "000")
  if [[ "$code" =~ ^(200|301|302|403)$ ]]; then
    echo "OK   ($code) $url"
    ((ok++)) || true
  else
    echo "FAIL ($code) $url"
    ((fail++)) || true
  fi
done <<< "$urls"

echo
echo "Done: $ok ok, $fail failed"
exit "$fail"
