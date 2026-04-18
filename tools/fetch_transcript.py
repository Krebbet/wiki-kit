"""Fetch a YouTube transcript as markdown."""
from __future__ import annotations

import argparse
import re
import sys
import tempfile
from pathlib import Path

import yt_dlp

from tools._common import (
    next_numbered_filename,
    slugify,
    today_iso,
    write_frontmatter,
)


def capture(url: str, out_dir: Path, slug: str | None, timestamp_every: int) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wk-yt-") as d:
        tmp = Path(d)
        info, vtt_path = _download_subs(url, tmp)
        transcript_md = _vtt_to_markdown(vtt_path, timestamp_every)

    title = info.get("title")
    channel = info.get("channel") or info.get("uploader")
    duration = info.get("duration")
    upload_date = info.get("upload_date")
    thumbnail = info.get("thumbnail")

    effective_slug = slug or slugify(title or "video")
    filename = next_numbered_filename(out_dir, effective_slug)
    fm = write_frontmatter({
        "url": url,
        "title": title or "(untitled)",
        "channel": channel,
        "upload_date": upload_date,
        "duration": duration,
        "thumbnail_url": thumbnail,
        "captured_on": today_iso(),
        "capture_method": "youtube",
    })
    body = f"# {title or '(untitled)'}\n\n{transcript_md}\n"
    out_path = out_dir / filename
    out_path.write_text(fm + body, encoding="utf-8")
    return out_path


def _download_subs(url: str, workdir: Path) -> tuple[dict, Path]:
    opts = {
        "writesubtitles": True,
        "writeautomaticsub": True,
        "skip_download": True,
        "subtitleslangs": ["en", "en-US", "en-GB"],
        "subtitlesformat": "vtt",
        "outtmpl": str(workdir / "%(id)s.%(ext)s"),
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
    vtt_files = list(workdir.glob("*.vtt"))
    if not vtt_files:
        raise RuntimeError("no subtitles available for this video")
    return info, vtt_files[0]


_TIMESTAMP_RE = re.compile(r"^(\d{2}):(\d{2}):(\d{2})\.\d+ --> ")


def _vtt_to_markdown(vtt_path: Path, timestamp_every: int) -> str:
    # TODO: YouTube auto-captions emit rolling cues where each new cue restates
    # the tail of the previous one. We don't dedupe yet, so transcripts are
    # ~2-3x longer than necessary. Tracked for a follow-up.
    lines = vtt_path.read_text(encoding="utf-8").splitlines()
    last_stamp_emitted: int = -timestamp_every  # ensures first stamp at 0
    paragraphs: list[str] = []  # each item is a paragraph; joined with \n\n
    current_buf: list[str] = []  # text accumulating into the current paragraph
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _TIMESTAMP_RE.match(line)
        if m:
            hh, mm, ss = (int(x) for x in m.groups())
            current_start = hh * 3600 + mm * 60 + ss
            i += 1
            text_parts: list[str] = []
            while i < len(lines) and lines[i].strip() and not _TIMESTAMP_RE.match(lines[i]):
                text_parts.append(re.sub(r"<[^>]+>", "", lines[i]).strip())
                i += 1
            text = " ".join(tp for tp in text_parts if tp)
            if not text:
                continue
            if current_start - last_stamp_emitted >= timestamp_every:
                if current_buf:
                    paragraphs.append(" ".join(current_buf))
                current_buf = [f"**[{hh:02d}:{mm:02d}:{ss:02d}]** {text}"]
                last_stamp_emitted = current_start
            else:
                current_buf.append(text)
        else:
            i += 1
    if current_buf:
        paragraphs.append(" ".join(current_buf))
    return "\n\n".join(paragraphs).strip()


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fetch a YouTube transcript as markdown.")
    p.add_argument("--url", required=True)
    p.add_argument("--out", required=True, type=Path)
    p.add_argument("--slug", default=None)
    p.add_argument("--timestamp-every", type=int, default=30)
    args = p.parse_args(argv)
    try:
        written = capture(args.url, args.out, args.slug, args.timestamp_every)
    except Exception as e:
        print(f"fetch_transcript failed: {e}", file=sys.stderr)
        return 1
    print(written)
    return 0


if __name__ == "__main__":
    sys.exit(main())
