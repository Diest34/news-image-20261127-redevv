#!/usr/bin/env python3
"""News Image -- 27 November 2026.

Reproduces this entry's image: the program takes the entry artwork
that ships alongside it in the repository (``entry.png``, a front page
built for this bounty by ``build_image.py``) and places an exact copy
at ``/output/entry.png``. The picture itself is not generated here;
this script exists so the entry can be rebuilt deterministically and
the delivered file checked byte for byte.

Usage:
    python3 main.py

Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for
/output:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

from __future__ import annotations

import hashlib
import os
import shutil
import sys
from pathlib import Path

# The image lives beside this script in the repository.
SOURCE_NAME = "entry.png"

# The grader gives the program a writable /output; locally the
# environment variable stands in for it.
OUTPUT_PATH = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")) / "entry.png"

# The eight magic bytes every PNG file starts with.
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def digest(path: Path) -> str:
    """Return the hex SHA-256 digest of the file at *path*."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME

    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    with source.open("rb") as handle:
        if handle.read(len(PNG_SIGNATURE)) != PNG_SIGNATURE:
            print(f"error: {source} is not a PNG file", file=sys.stderr)
            return 1

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, OUTPUT_PATH)

    if digest(source) != digest(OUTPUT_PATH):
        print("error: copy differs from source", file=sys.stderr)
        return 1

    size = OUTPUT_PATH.stat().st_size
    print(f"wrote {OUTPUT_PATH} ({size} bytes, sha256 {digest(OUTPUT_PATH)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
