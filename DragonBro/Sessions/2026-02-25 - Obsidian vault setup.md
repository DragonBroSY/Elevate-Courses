# 2026-02-25 - Obsidian vault setup
Tags: #meta #session

## Project
[[Projects/3D Tours]], [[Projects/Build Site]], [[Projects/Flight Training]]

## Goal
Set up an Obsidian vault to track project decisions, directions from Claude, and session history — accessible outside of Claude Code.

## What We Did
- Created vault at `~/obsidian/DragonBro/` with Projects/, Sessions/, Decisions/ folders
- Wrote starter notes for 3D Tours, Build Site, and Flight Training from memory
- Created `_template.md` for future projects
- Created `Decisions/master-decisions-log.md` for cross-project decisions
- Initialized git repo, pushed to GitHub (DragonBroSY/DragonBro-vault, private)
- Created `~/.claude/commands/exit.md` — custom `/exit` slash command that generates a session note

## Decisions Made
- Vault stored at `~/obsidian/DragonBro/` (not iCloud, avoids file-restore issue)
- One vault for all projects, folder-per-project structure
- Sessions/ folder for dated session notes
- `/exit` command generates Obsidian-ready markdown at end of each Claude Code session

## Commands / Paths to Remember
- Vault: `~/obsidian/DragonBro/`
- GitHub: https://github.com/DragonBroSY/DragonBro-vault
- Open vault: `open "obsidian://open?path=/Users/bs16/obsidian/DragonBro"`
- Sync: `cd ~/obsidian/DragonBro && git add -A && git commit -m "session notes" && git push`
- Slash command: type `/exit` in Claude Code at end of session

## Result
Vault is live, git-tracked, and pushed to GitHub. Session notes workflow established via `/exit`.
