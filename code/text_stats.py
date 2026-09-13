#!/usr/bin/env python3
"""Count word frequencies in a UTF-8 text file.

English words and numbers are grouped case-insensitively. Chinese text is
counted character by character so that the program works without external
tokenization packages.
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from pathlib import Path


TOKEN_RE = re.compile(r"[A-Za-z0-9_]+|[\u4e00-\u9fff]")


def tokens(text: str) -> list[str]:
    """Return normalized English/numeric tokens and Chinese characters."""
    return [token.lower() for token in TOKEN_RE.findall(text)]


def count_words(path: Path) -> Counter[str]:
    """Read *path* as UTF-8 and count its tokens."""
    return Counter(tokens(path.read_text(encoding="utf-8")))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Count text token frequencies")
    parser.add_argument("input", type=Path, help="UTF-8 text file to analyze")
    parser.add_argument("--top", type=int, default=10, help="number of rows to show")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    if args.top < 1:
        raise SystemExit("--top must be a positive integer")
    if not args.input.is_file():
        raise SystemExit(f"input file not found: {args.input}")

    counts = count_words(args.input)
    print(f"file: {args.input}")
    print(f"tokens: {sum(counts.values())}")
    print(f"unique: {len(counts)}")
    print("rank token count")
    for rank, (token, count) in enumerate(
        sorted(counts.items(), key=lambda item: (-item[1], item[0]))[: args.top],
        start=1,
    ):
        print(f"{rank:>4} {token:<12} {count:>5}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
