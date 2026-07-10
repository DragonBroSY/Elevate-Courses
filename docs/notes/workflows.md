---
layout: note
publish: true
title: "Workflows"
date: 2026-03-13
topics: "workflow, publishing, git, obsidian-git, podcast, GitHub Pages"
---

How this site is built and maintained.

---

## 0. Starting a Writing Session

**Always run `start.sh` before writing.** This pulls any edits made on GitHub
(web edits, auto-published changes) to your local vault first — preventing conflicts.

```bash
./start.sh
```

Or manually:

```bash
git pull
```

Skip this and you risk your next `push.sh` overwriting GitHub edits.

---

## 1. Publishing Notes

Write in Obsidian → push → GitHub Actions → live site.

**To publish a note:**

1. Add frontmatter to any vault `.md` file:
   ```yaml
   ---
   publish: true
   title: "Day 7 — Navigation"
   date: 2026-03-24
   topics: "VOR, GPS, pilotage"
   ---
   ```
2. Push (`push.sh` or Obsidian Git plugin)
3. GitHub Actions runs `publish_notes.py` automatically
4. Site updates in ~1 min

**What `publish_notes.py` does:**
- Copies `![[image embeds]]` → `docs/assets/`
- Converts Obsidian wikilinks to standard markdown links
- Writes rendered note to `docs/notes/<slug>.md`
- Regenerates `docs/notes/index.md` and `docs/sitemap.xml`

---

## 2. Adding PDFs / Files

Drop the file into `pdf-inbox/` → push. That's it.

`publish_notes.py` (run automatically by GitHub Actions on every push) will:
- Copy it to `docs/assets/`
- Add a row to `docs/notes/resources.md` (title auto-generated from the filename)
- Move the original into `pdf-inbox/published/` (gitignored, so it isn't duplicated in the repo)

Edit the auto-added row in `resources.md` afterward if you want a nicer title/description —
that edit sticks; the inbox only *adds* rows, it never overwrites existing ones.

(Manual alternative, if you want more control over the title/section up front: drop the
file straight into `docs/assets/` yourself and add the `resources.md` row by hand.)

---

## 3. Podcast Episodes

Drop an `.mp3` into `audio-inbox/` → run `podcast_upload.py`:

```bash
python podcast_upload.py
```

This uploads the file to Cloudflare R2, updates `docs/feed.xml`, and pushes to GitHub Pages. The episode appears on the homepage and in any podcast app subscribed to the RSS feed.

---

## 4. Editing the Homepage

`docs/index.html` is plain HTML — edit it directly and push. GitHub Pages serves it as-is (Jekyll does not process it since it has no frontmatter).

---

## Infrastructure

| Thing | What it is |
|-------|-----------|
| `push.sh` | Shortcut: `git add -A && commit && push` |
| `publish_notes.py` | Obsidian → Jekyll converter |
| `.github/workflows/publish-notes.yml` | Runs `publish_notes.py` in the cloud on every push |
| `docs/` | Everything served by GitHub Pages |
| `docs/_config.yml` | Jekyll config (theme: minima) |
| `docs/_layouts/note.html` | Note page template |
| `docs/assets/` | Images, PDFs, static files |
| `docs/notes/` | Auto-generated — do not edit directly |
