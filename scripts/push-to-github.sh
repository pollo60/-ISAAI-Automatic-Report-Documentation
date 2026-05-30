#!/usr/bin/env bash
# Run this in Terminal.app (interactive) so macOS can prompt for GitHub login.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "Branch: $(git branch --show-current)"
echo "Commits to push:"
git log origin/main..HEAD --oneline 2>/dev/null || git log --oneline -5

echo ""
echo "Pushing to origin main..."
git push -u origin main

echo "Done. Verify: https://github.com/pollo60/-ISAAI-Automatic-Report-Documentation"
