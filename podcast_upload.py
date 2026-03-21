#!/usr/bin/env python3
"""
Elevate Courses — Podcast Auto-Uploader
Drop audio files into audio-inbox/ → auto-uploads to Cloudflare R2
→ updates docs/feed.xml → pushes to GitHub Pages
"""

import os
import re
import json
import time
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from xml.etree import ElementTree as ET
from xml.dom import minidom

import boto3
from botocore.config import Config
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from dotenv import load_dotenv

try:
    from mutagen import File as MutagenFile
    HAS_MUTAGEN = True
except ImportError:
    HAS_MUTAGEN = False

# ── Load credentials from .env ─────────────────────────────────────────────
load_dotenv(Path(__file__).parent / ".env")

# ── Paths ──────────────────────────────────────────────────────────────────
VAULT_DIR    = Path(__file__).parent
INBOX_DIR    = VAULT_DIR / "audio-inbox"
UPLOADED_DIR = INBOX_DIR / "uploaded"
DOCS_DIR     = VAULT_DIR / "docs"
EPISODES_FILE = VAULT_DIR / "episodes.json"
FEED_FILE    = DOCS_DIR / "feed.xml"

# ── Podcast identity ───────────────────────────────────────────────────────
PODCAST_TITLE       = "Elevate Courses"
PODCAST_DESCRIPTION = "Private pilot flight training recordings by DragonBroSY. Real cockpit audio, ground sessions, and study material. New episodes added after every lesson."
PODCAST_AUTHOR      = "DragonBroSY"
GITHUB_PAGES_URL    = "https://dragonbrosy.github.io/Elevate-Courses"
PODCAST_COVER_URL   = f"{GITHUB_PAGES_URL}/cockpit.jpg"

# ── R2 config (from .env) ──────────────────────────────────────────────────
R2_ACCOUNT_ID  = os.environ["R2_ACCOUNT_ID"]
R2_ACCESS_KEY  = os.environ["R2_ACCESS_KEY_ID"]
R2_SECRET_KEY  = os.environ["R2_SECRET_ACCESS_KEY"]
R2_BUCKET      = os.environ.get("R2_BUCKET", "elevate-audio")
R2_PUBLIC_URL  = os.environ["R2_PUBLIC_URL"].rstrip("/")   # e.g. https://pub-xxxx.r2.dev

AUDIO_EXTENSIONS = {".mp3", ".m4a", ".wav", ".aac", ".opus"}
WAV_CONVERT_EXTS = {".wav"}  # these get converted to MP3 before upload

# ── R2 client ──────────────────────────────────────────────────────────────
def get_r2_client():
    return boto3.client(
        "s3",
        endpoint_url=f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com",
        aws_access_key_id=R2_ACCESS_KEY,
        aws_secret_access_key=R2_SECRET_KEY,
        config=Config(
            signature_version="s3v4",
            request_checksum_calculation="when_required",
            response_checksum_validation="when_required",
        ),
        region_name="auto",
    )

# ── Helpers ────────────────────────────────────────────────────────────────
def get_duration(path: Path) -> int:
    if not HAS_MUTAGEN:
        return 0
    try:
        audio = MutagenFile(path)
        if audio and audio.info:
            return int(audio.info.length)
    except Exception:
        pass
    return 0

def format_duration(seconds: int) -> str:
    h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
    return f"{h:02d}:{m:02d}:{s:02d}"

def mime_type(path: Path) -> str:
    return {
        ".mp3":  "audio/mpeg",
        ".m4a":  "audio/mp4",
        ".wav":  "audio/wav",
        ".aac":  "audio/aac",
        ".opus": "audio/ogg",
    }.get(path.suffix.lower(), "audio/mpeg")

def parse_title(stem: str) -> str:
    """Generate a clean episode title from the filename stem.
    Handles patterns like TX01_MIC009_20260320_192305_orig
    """
    tx  = re.search(r'TX(\d+)', stem, re.IGNORECASE)
    dt  = re.search(r'(\d{8})_(\d{6})', stem)
    day = re.search(r'day(\d+)', stem, re.IGNORECASE)

    parts = []
    if tx:
        parts.append(f"Session {int(tx.group(1)):02d}")
    elif day:
        parts.append(f"Day {int(day.group(1)):02d}")

    if dt:
        try:
            d = datetime.strptime(dt.group(1), "%Y%m%d")
            t = datetime.strptime(dt.group(2), "%H%M%S")
            parts.append(d.strftime("%B %d, %Y"))
            parts.append(t.strftime("%H:%M") + "Z")
        except ValueError:
            pass
    elif re.search(r'\d{8}', stem):
        m = re.search(r'(\d{8})', stem)
        try:
            d = datetime.strptime(m.group(1), "%Y%m%d")
            parts.append(d.strftime("%B %d, %Y"))
        except ValueError:
            pass

    if not parts:
        # Fallback: clean up underscores/dashes
        cleaned = re.sub(r'[_\-]+', ' ', stem).strip()
        return cleaned.title()

    return " — ".join(parts)

def parse_shownotes(stem: str, filename: str) -> str:
    """Auto-generate show notes from filename metadata."""
    tx  = re.search(r'TX(\d+)', stem, re.IGNORECASE)
    mic = re.search(r'MIC(\d+)', stem, re.IGNORECASE)
    dt  = re.search(r'(\d{8})_(\d{6})', stem)

    lines = [f"Elevate Courses — flight training recording by DragonBroSY."]

    if tx:
        lines.append(f"Session: TX{tx.group(1).zfill(2)}")
    if mic:
        lines.append(f"Microphone track: MIC{mic.group(1).zfill(3)}")
    if dt:
        try:
            d = datetime.strptime(dt.group(1), "%Y%m%d")
            t = datetime.strptime(dt.group(2), "%H%M%S")
            lines.append(f"Recorded: {d.strftime('%B %d, %Y')} at {t.strftime('%H:%M')} Zulu")
        except ValueError:
            pass

    lines.append("")
    lines.append("Topics may include: pre-flight, ATC communications, maneuvers, navigation, emergency procedures, and debrief.")
    lines.append("")
    lines.append("Subscribe to Elevate Courses to follow the full private pilot training journey.")

    return "\n".join(lines)

def load_episodes() -> list:
    if EPISODES_FILE.exists():
        return json.loads(EPISODES_FILE.read_text(encoding="utf-8"))
    return []

def save_episodes(episodes: list):
    EPISODES_FILE.write_text(
        json.dumps(episodes, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )

def already_uploaded(filename: str, episodes: list) -> bool:
    return any(ep["filename"] == filename for ep in episodes)

def wait_for_stable(path: Path, stable_secs: int = 5) -> bool:
    """Wait until file size stops changing — ensures large files are fully copied."""
    prev_size, stable_count = -1, 0
    for _ in range(120):
        try:
            size = path.stat().st_size
        except FileNotFoundError:
            return False
        if size > 0 and size == prev_size:
            stable_count += 1
            if stable_count >= stable_secs:
                return True
        else:
            stable_count = 0
        prev_size = size
        time.sleep(1)
    return False

# ── Core pipeline ──────────────────────────────────────────────────────────
def upload_to_r2(path: Path) -> str:
    client = get_r2_client()
    key = path.name
    size_mb = path.stat().st_size / 1_000_000
    print(f"  Uploading {key} ({size_mb:.0f} MB) to R2...")
    client.upload_file(
        str(path), R2_BUCKET, key,
        ExtraArgs={"ContentType": mime_type(path)},
        Callback=UploadProgress(path.stat().st_size),
    )
    print()
    return f"{R2_PUBLIC_URL}/{key}"

class UploadProgress:
    def __init__(self, total: int):
        self.total = total
        self.uploaded = 0

    def __call__(self, chunk: int):
        self.uploaded += chunk
        pct = self.uploaded / self.total * 100
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"\r  [{bar}] {pct:.0f}%", end="", flush=True)

def build_feed(episodes: list):
    DOCS_DIR.mkdir(exist_ok=True)
    rss = ET.Element("rss", {
        "version": "2.0",
        "xmlns:itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
    })
    ch = ET.SubElement(rss, "channel")
    ET.SubElement(ch, "title").text           = PODCAST_TITLE
    ET.SubElement(ch, "link").text            = GITHUB_PAGES_URL
    ET.SubElement(ch, "description").text     = PODCAST_DESCRIPTION
    ET.SubElement(ch, "language").text        = "en-us"
    ET.SubElement(ch, "itunes:author").text   = PODCAST_AUTHOR
    ET.SubElement(ch, "itunes:explicit").text = "false"
    ET.SubElement(ch, "itunes:type").text     = "episodic"
    ET.SubElement(ch, "itunes:category", {"text": "Education"})
    ET.SubElement(ch, "itunes:image", {"href": PODCAST_COVER_URL})
    img = ET.SubElement(ch, "image")
    ET.SubElement(img, "url").text   = PODCAST_COVER_URL
    ET.SubElement(img, "title").text = PODCAST_TITLE
    ET.SubElement(img, "link").text  = GITHUB_PAGES_URL

    for ep in sorted(episodes, key=lambda x: x["date"], reverse=True):
        item = ET.SubElement(ch, "item")
        ET.SubElement(item, "title").text       = ep["title"]
        ET.SubElement(item, "description").text = ep.get("description", ep["title"])
        ET.SubElement(item, "pubDate").text      = ep["date"]
        ET.SubElement(item, "guid", {"isPermaLink": "false"}).text = ep["url"]
        ET.SubElement(item, "enclosure", {
            "url":    ep["url"],
            "length": str(ep["size"]),
            "type":   ep["mime"],
        })
        if ep.get("duration"):
            ET.SubElement(item, "itunes:duration").text = format_duration(ep["duration"])

    raw = ET.tostring(rss, encoding="unicode")
    pretty = minidom.parseString(raw).toprettyxml(indent="  ")
    lines = pretty.split("\n")
    body = "\n".join(lines[1:]) if lines[0].startswith("<?xml") else pretty
    FEED_FILE.write_text('<?xml version="1.0" encoding="UTF-8"?>\n' + body, encoding="utf-8")
    print(f"  feed.xml updated ({len(episodes)} episode(s))")

def git_push(filename: str):
    subprocess.run(["git", "add", "docs/feed.xml", "episodes.json"], cwd=VAULT_DIR, check=True)
    result = subprocess.run(
        ["git", "commit", "-m", f"podcast: add {filename}"],
        cwd=VAULT_DIR, capture_output=True, text=True
    )
    if "nothing to commit" not in result.stdout:
        subprocess.run(["git", "push"], cwd=VAULT_DIR, check=True)
        print("  Pushed to GitHub.")

def convert_to_mp3(path: Path) -> Path:
    """Convert WAV (or other lossless) to MP3 128kbps for Spotify compatibility."""
    mp3_path = path.with_suffix(".mp3")
    print(f"  Converting {path.name} → {mp3_path.name} (MP3 128kbps)...")
    result = subprocess.run(
        ["ffmpeg", "-i", str(path), "-codec:a", "libmp3lame", "-b:a", "128k",
         "-y", str(mp3_path)],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        raise RuntimeError(f"ffmpeg failed: {result.stderr[-300:]}")
    print(f"  Converted: {mp3_path.stat().st_size / 1_000_000:.1f} MB")
    return mp3_path

def process_file(path: Path):
    if path.suffix.lower() not in AUDIO_EXTENSIONS:
        return

    print(f"\n{'─'*50}")
    print(f"New file detected: {path.name}")

    print("  Waiting for file to finish copying...")
    if not wait_for_stable(path):
        print("  Timed out waiting — skipping.")
        return

    # Convert WAV → MP3 before upload (Spotify rejects large WAVs)
    if path.suffix.lower() in WAV_CONVERT_EXTS:
        try:
            path = convert_to_mp3(path)
        except Exception as e:
            print(f"  Conversion failed: {e}")
            return

    episodes = load_episodes()
    if already_uploaded(path.name, episodes):
        print("  Already uploaded — skipping.")
        return

    title      = parse_title(path.stem)
    shownotes  = parse_shownotes(path.stem, path.name)
    pub_date   = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")

    print(f"  Title:      {title}")
    print(f"  Show notes: {shownotes.splitlines()[0]}...")

    try:
        url = upload_to_r2(path)
        episodes.append({
            "filename":    path.name,
            "title":       title,
            "url":         url,
            "date":        pub_date,
            "duration":    get_duration(path),
            "size":        path.stat().st_size,
            "mime":        mime_type(path),
            "description": shownotes,
        })
        save_episodes(episodes)
        build_feed(episodes)
        git_push(path.name)

        UPLOADED_DIR.mkdir(exist_ok=True)
        path.rename(UPLOADED_DIR / path.name)
        print(f"\n  DONE → {GITHUB_PAGES_URL}/feed.xml")
        print(f"{'─'*50}")

    except Exception as e:
        print(f"  ERROR: {e}")

# ── File watcher ───────────────────────────────────────────────────────────
class AudioHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(Path(event.src_path))

def main():
    INBOX_DIR.mkdir(exist_ok=True)
    print("=" * 50)
    print("  Elevate Courses — Podcast Auto-Uploader")
    print("=" * 50)
    print(f"  Inbox:  {INBOX_DIR}")
    print(f"  Feed:   {GITHUB_PAGES_URL}/feed.xml")
    print(f"  Player: {GITHUB_PAGES_URL}")
    print("  Drop audio files into audio-inbox/ to publish")
    print("=" * 50)

    # Process any files already sitting in inbox
    for f in INBOX_DIR.iterdir():
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS:
            process_file(f)

    observer = Observer()
    observer.schedule(AudioHandler(), str(INBOX_DIR), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping watcher...")
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
