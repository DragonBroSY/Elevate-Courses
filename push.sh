#!/bin/zsh
cd "$(dirname "$0")"
git add -A
git commit -m "vault: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || echo "nothing to commit"
git push
