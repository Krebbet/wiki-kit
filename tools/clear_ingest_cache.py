"""Clear a topic's /.ingest/ cache directory.

Removes all per-source summaries and run.json for a topic, forcing the
next /ingest run over the same dir to re-dispatch every source from
scratch.

Usage:
    poetry run python -m tools.clear_ingest_cache <topic-dir>
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path


def clear(topic_dir: Path) -> bool:
    """Remove <topic_dir>/.ingest/ if it exists. Return True if something was removed."""
    ingest = topic_dir / ".ingest"
    if not ingest.exists() and not ingest.is_symlink():
        return False
    # Safety: the path we're about to delete must itself be named `.ingest`,
    # even after symlink resolution. Guards against a symlinked `.ingest`
    # pointing at some other directory the user cares about.
    resolved = ingest.resolve()
    if resolved.name != ".ingest":
        raise ValueError(
            f"{ingest} resolves to {resolved}, which is not a .ingest directory; refusing to delete"
        )
    shutil.rmtree(ingest)
    return True


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Clear a topic's .ingest/ cache.")
    p.add_argument("topic_dir", type=Path, help="Directory containing an .ingest/ cache.")
    args = p.parse_args(argv)

    topic = args.topic_dir
    if not topic.is_dir():
        print(f"clear_ingest_cache: not a directory: {topic}", file=sys.stderr)
        return 2
    removed = clear(topic)
    print(f"cleared {topic}/.ingest/" if removed else f"{topic}/.ingest/ already absent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
