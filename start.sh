#!/bin/zsh
# Run this before every writing session to sync GitHub edits to local vault.
cd "$(dirname "$0")"
echo "Pulling latest from GitHub..."
git pull
echo "Good to go. Start writing!"
