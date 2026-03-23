#!/usr/bin/env python3
"""
publish_notes.py — Obsidian -> Jekyll publisher

Scans vault root for .md files tagged with `publish: true` in frontmatter.
For each tagged note:
  - Copies referenced images (![[...]]) to docs/assets/
  - Converts Obsidian syntax to standard markdown
  - Writes the note to docs/notes/<slug>.md with Jekyll frontmatter
  - Regenerates docs/notes/index.md and docs/sitemap.xml

Overwrite protection:
  A source_hash of the vault file is stored in the generated frontmatter.
  On the next run, if the hash hasn't changed (vault not edited), the
  generated file is left untouched — preserving any edits made on GitHub.
  If the vault file changed, it overwrites (vault wins).

Run automatically via push.sh, or manually:
  python publish_notes.py
"""

import hashlib
import re
import shutil
from pathlib import Path

VAULT_ROOT  = Path(__file__).parent
DOCS_NOTES  = VAULT_ROOT / "docs" / "notes"
DOCS_ASSETS = VAULT_ROOT / "docs" / "assets"
IMG_EXTS    = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".heic"}


# -- Helpers ------------------------------------------------------------------

def src_hash(path):
    """Short MD5 of a file's contents."""
    return hashlib.md5(path.read_bytes()).hexdigest()[:12]


def parse_frontmatter(text):
    """Return (dict, body_str). Handles missing or malformed frontmatter."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    fm_block = text[3:end].strip()
    body = text[end + 4:].lstrip("\n")
    fm = {}
    for line in fm_block.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm, body


# -- Obsidian -> Markdown -----------------------------------------------------

def collect_images(text):
    """Return list of image filenames referenced in ![[...]] embeds."""
    found = []
    for m in re.finditer(r"!\[\[([^\]]+)\]\]", text):
        name = m.group(1).split("|")[0].strip()
        if Path(name).suffix.lower() in IMG_EXTS:
            found.append(name)
    return found


def convert(text, assets_prefix="../assets"):
    """Convert Obsidian-flavoured markdown to standard markdown."""

    # ![[image.png]] or ![[image.png|size]] -> standard img
    def embed(m):
        raw = m.group(1).split("|")[0].strip()
        ext = Path(raw).suffix.lower()
        if ext in IMG_EXTS:
            encoded = raw.replace(" ", "%20")
            return f"![{raw}]({assets_prefix}/{encoded})"
        return f"*({raw})*"

    text = re.sub(r"!\[\[([^\]]+)\]\]", embed, text)

    # [[Note|alias]] -> [alias](note-slug)
    def wikilink_alias(m):
        slug = m.group(1).strip().lower().replace(" ", "-")
        return f"[{m.group(2).strip()}]({slug})"

    text = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", wikilink_alias, text)

    # [[Note]] -> [Note](note-slug)
    def wikilink(m):
        target = m.group(1).strip()
        slug   = target.lower().replace(" ", "-")
        return f"[{target}]({slug})"

    text = re.sub(r"\[\[([^\]|]+)\]\]", wikilink, text)

    return text


# -- Main ---------------------------------------------------------------------

def publish():
    DOCS_NOTES.mkdir(parents=True, exist_ok=True)
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)

    published = []  # [(title, slug, date, topics)]

    for md_path in sorted(VAULT_ROOT.glob("*.md")):
        raw = md_path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(raw)

        if fm.get("publish", "").lower() != "true":
            continue

        title    = fm.get("title", md_path.stem)
        date_str = fm.get("date", "")
        topics   = fm.get("topics", "")
        slug     = md_path.stem.lower().replace(" ", "-")
        out_path = DOCS_NOTES / f"{slug}.md"
        current_hash = src_hash(md_path)

        # Overwrite protection: skip if vault source unchanged since last publish
        if out_path.exists():
            existing_fm, _ = parse_frontmatter(out_path.read_text(encoding="utf-8"))
            if existing_fm.get("source_hash") == current_hash:
                print(f"  = {md_path.name} (skipped, no vault changes)")
                published.append((title, slug, date_str, topics))
                continue

        print(f"  + {md_path.name}")

        # Copy images to docs/assets/
        for img_name in collect_images(raw):
            src = VAULT_ROOT / img_name
            dst = DOCS_ASSETS / img_name
            if src.exists():
                shutil.copy2(src, dst)
            else:
                print(f"    WARNING image not found: {img_name}")

        # Build output
        converted   = convert(body)
        date_line   = f"\ndate: {date_str}"    if date_str else ""
        topics_line = f"\ntopics: \"{topics}\"" if topics   else ""

        output = (
            f'---\nlayout: note\ntitle: "{title}"'
            f"{date_line}{topics_line}\nsource_hash: {current_hash}\n---\n\n{converted}"
        )

        out_path.write_text(output, encoding="utf-8")
        published.append((title, slug, date_str, topics))

    # Regenerate index
    if published:
        rows = "\n".join(
            f"| [{title}]({slug}) | {topics} |"
            for title, slug, _, topics in published
        )
        index = (
            "---\nlayout: note\ntitle: \"Course Notes\"\n---\n\n"
            "| Note | Topics |\n|------|--------|\n"
            + rows + "\n\n"
            "---\n\n"
            "- [Resources](resources) - PDFs, charts, reference links\n"
            "- [Workflows](workflows) - How this site works\n"
        )
        (DOCS_NOTES / "index.md").write_text(index, encoding="utf-8")

    # Regenerate sitemap
    base = "https://dragonbrosy.github.io/Elevate-Courses"
    urls = [f"  <url><loc>{base}/</loc></url>",
            f"  <url><loc>{base}/notes/</loc></url>"]
    for _, slug, _, _ in published:
        urls.append(f"  <url><loc>{base}/notes/{slug}</loc></url>")
    sitemap = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(urls) + "\n"
        "</urlset>\n"
    )
    (VAULT_ROOT / "docs" / "sitemap.xml").write_text(sitemap, encoding="utf-8")
    print(f"  Updated sitemap ({len(published) + 2} URLs)")

    return len(published)


if __name__ == "__main__":
    print("Publishing notes...")
    n = publish()
    print(f"Done - {n} note(s) published.")
