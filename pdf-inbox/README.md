Drop any PDF (or other file) here and push.

On the next publish run, `publish_notes.py` copies it into `docs/assets/`,
adds a row to `docs/notes/resources.md`, and moves the original into
`published/` (gitignored — not duplicated in the repo).

No frontmatter, no naming convention — just drop the file.
