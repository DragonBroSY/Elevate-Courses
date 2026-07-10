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

Also drains pdf-inbox/: any file dropped there is copied to docs/assets/,
listed in docs/notes/resources.md, and moved to pdf-inbox/published/
(gitignored, so it isn't duplicated in the repo).

Run automatically via push.sh (or GitHub Actions on every push), or manually:
  python publish_notes.py
"""

import hashlib
import re
import shutil
from pathlib import Path

VAULT_ROOT   = Path(__file__).parent
DOCS_NOTES   = VAULT_ROOT / "docs" / "notes"
DOCS_ASSETS  = VAULT_ROOT / "docs" / "assets"
PDF_INBOX    = VAULT_ROOT / "pdf-inbox"
PDF_DONE     = PDF_INBOX / "published"
RESOURCES_MD = DOCS_NOTES / "resources.md"
IMG_EXTS     = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".heic"}


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


# -- PDF inbox -----------------------------------------------------------------

def humanize_filename(stem):
    """Turn a filename stem into a readable title: camelCase/snake_case/kebab-case -> Title Case."""
    s = re.sub(r"[_\-]+", " ", stem)
    s = re.sub(r"(?<=[a-z0-9])(?=[A-Z])", " ", s)
    return " ".join(w.capitalize() for w in s.split())


def process_pdf_inbox():
    """Copy any files dropped in pdf-inbox/ to docs/assets/ and return their names."""
    if not PDF_INBOX.exists():
        return []

    PDF_DONE.mkdir(parents=True, exist_ok=True)
    dropped = [
        f for f in sorted(PDF_INBOX.iterdir())
        if f.is_file() and not f.name.startswith(".") and f.name.lower() != "readme.md"
    ]

    added = []
    for f in dropped:
        dest = DOCS_ASSETS / f.name
        if dest.exists():
            print(f"    WARNING {f.name} already exists in docs/assets/, not overwriting")
        else:
            shutil.copy2(f, dest)
            print(f"  + pdf-inbox: {f.name} -> docs/assets/")
        added.append(f.name)
        f.rename(PDF_DONE / f.name)

    return added


def update_resources_table(new_files):
    """Insert a row per new file into the 'PDFs & Documents' table in resources.md."""
    if not new_files or not RESOURCES_MD.exists():
        return

    lines = RESOURCES_MD.read_text(encoding="utf-8").splitlines()

    try:
        heading_idx = next(i for i, l in enumerate(lines) if l.strip() == "## PDFs & Documents")
        sep_idx = next(
            i for i in range(heading_idx, len(lines))
            if lines[i].strip().startswith("|") and set(lines[i].strip()) <= set("|- ")
        )
    except StopIteration:
        print("    WARNING resources.md missing a '## PDFs & Documents' table, skipping")
        return

    insert_at = sep_idx + 1
    if insert_at < len(lines) and lines[insert_at].strip() == "| — | — |":
        del lines[insert_at]

    existing = {
        l.split("](")[1].split(")")[0].rsplit("/", 1)[-1]
        for l in lines[insert_at:]
        if l.strip().startswith("|") and "](" in l
    }

    new_rows = [
        f"| [{humanize_filename(Path(name).stem)}](../assets/{name.replace(' ', '%20')}) | — |"
        for name in new_files
        if name not in existing
    ]

    for row in reversed(new_rows):
        lines.insert(insert_at, row)

    if new_rows:
        RESOURCES_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
        print(f"  Updated resources.md ({len(new_rows)} new entr{'y' if len(new_rows)==1 else 'ies'})")


# -- Main ---------------------------------------------------------------------

def publish():
    DOCS_NOTES.mkdir(parents=True, exist_ok=True)
    DOCS_ASSETS.mkdir(parents=True, exist_ok=True)

    inbox_files = process_pdf_inbox()
    update_resources_table(inbox_files)

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
