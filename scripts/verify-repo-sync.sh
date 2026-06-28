#!/usr/bin/env bash
# Compare local tree with origin/main file list (read-only check).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== ISAAI local file inventory ==="
find . -type f ! -path './.git/*' | sort | wc -l | xargs echo "Local files:"

if git remote get-url origin &>/dev/null; then
  git fetch origin main --quiet 2>/dev/null || echo "WARN: could not fetch origin (offline?)"
  if git rev-parse origin/main &>/dev/null 2>&1; then
    echo ""
    echo "=== Files on origin/main not in local working tree ==="
    git diff --name-only HEAD origin/main 2>/dev/null || git ls-tree -r --name-only origin/main | while read -r f; do
      [[ -f "$f" ]] || echo "MISSING: $f"
    done
  fi
else
  echo "No origin remote configured."
fi

echo ""
echo "=== Critical paths ==="
for p in README.md docs/Documentation docs/guides .github/workflows src scripts tests presentations; do
  if [[ -e "$p" ]]; then echo "OK  $p"; else echo "MISS $p"; fi
done
