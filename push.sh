#!/bin/zsh
cd "$(dirname "$0")"

# Sync published Obsidian notes → Jekyll site
python publish_notes.py

git add -A
git commit -m "vault: $(date '+%Y-%m-%d %H:%M')" 2>/dev/null || echo "nothing to commit"
git push
