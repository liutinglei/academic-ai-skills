"""Parse plain-text peer-review comments into numbered comment blocks.

The parser is intentionally conservative. It preserves source text and only
starts a new block when a line looks like a reviewer/editor heading or an
explicit numbered comment marker.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


HEADING_RE = re.compile(
    r"^\s*(?P<label>(reviewer|referee|editor|examiner|supervisor)\s*#?[\w.-]*|author response)\s*:?\s*$",
    re.IGNORECASE,
)
COMMENT_RE = re.compile(
    r"^\s*(?:(?:comment|point|issue|concern|major comment|minor comment)\s*)?(?P<num>\d+)[.)\:]\s+(?P<body>.+)$",
    re.IGNORECASE,
)
BULLET_RE = re.compile(r"^\s*[-*]\s+(?P<body>.+)$")


@dataclass
class ParsedComment:
    """A single parsed review comment."""

    id: str
    source: str
    text: str


def normalize_source(label: str | None, fallback_index: int) -> str:
    if not label:
        return f"Reviewer {fallback_index}"
    cleaned = " ".join(label.strip().rstrip(":").split())
    return cleaned[:1].upper() + cleaned[1:]


def parse_comments(text: str) -> list[ParsedComment]:
    comments: list[ParsedComment] = []
    current_source: str | None = None
    current_lines: list[str] = []
    source_counts: dict[str, int] = {}
    fallback_source_index = 1

    def flush() -> None:
        nonlocal current_lines
        if not current_lines:
            return
        source = normalize_source(current_source, fallback_source_index)
        source_counts[source] = source_counts.get(source, 0) + 1
        comment_id = f"{source}, Comment {source_counts[source]}"
        body = "\n".join(line.rstrip() for line in current_lines).strip()
        if body:
            comments.append(ParsedComment(id=comment_id, source=source, text=body))
        current_lines = []

    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        if not line.strip():
            if current_lines and current_lines[-1] != "":
                current_lines.append("")
            continue

        heading = HEADING_RE.match(line)
        if heading:
            flush()
            current_source = normalize_source(heading.group("label"), fallback_source_index)
            if current_source.startswith("Reviewer "):
                fallback_source_index += 1
            continue

        explicit = COMMENT_RE.match(line)
        bullet = BULLET_RE.match(line)
        if explicit:
            flush()
            current_lines = [explicit.group("body").strip()]
        elif bullet:
            flush()
            current_lines = [bullet.group("body").strip()]
        else:
            current_lines.append(line.strip())

    flush()
    return comments


def format_markdown(comments: list[ParsedComment]) -> str:
    blocks = []
    for comment in comments:
        blocks.append(f"## {comment.id}\n\n{comment.text}")
    return "\n\n".join(blocks) + ("\n" if blocks else "")


def read_input(path: str | None) -> str:
    if path:
        return Path(path).read_text(encoding="utf-8")
    return sys.stdin.read()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", help="Plain-text review file. Reads stdin when omitted.")
    parser.add_argument("--json", action="store_true", help="Output JSON instead of Markdown.")
    args = parser.parse_args(argv)

    comments = parse_comments(read_input(args.input))
    if args.json:
        print(json.dumps([asdict(comment) for comment in comments], ensure_ascii=False, indent=2))
    else:
        print(format_markdown(comments), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
