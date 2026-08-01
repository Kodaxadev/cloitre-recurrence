#!/usr/bin/env python3
"""Validate every relative link and inline path reference in tracked Markdown.

Two classes are checked:

* Markdown links `[text](path)` whose target is a relative path. Anchors and
  external URLs are ignored; an anchor on a real file is checked for the file.
* Inline code spans naming a tracked file, like `` `theorem-status.md` ``. These
  are how this repository cross-references its own notes, so they rot exactly
  like links do. Only spans that look like a repository path are considered,
  and only when the basename matches something tracked, so ordinary prose in
  backticks is not flagged.

Exit status is non-zero if any reference does not resolve.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

LINK = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
CODE_SPAN = re.compile(r"`([^`\s]+\.(?:md|py|rs|lean|toml|sh|yml|csv|txt|cff))`")
EXTERNAL = ("http://", "https://", "mailto:", "#")


def tracked_files() -> list[Path]:
    out = subprocess.run(
        ["git", "ls-files"], capture_output=True, text=True, check=True
    ).stdout.split("\n")
    return [Path(p) for p in out if p]


def main() -> int:
    files = tracked_files()
    tracked = {p.as_posix() for p in files}
    by_name: dict[str, list[str]] = {}
    for p in files:
        by_name.setdefault(p.name, []).append(p.as_posix())

    broken: list[str] = []
    ambiguous: list[str] = []
    checked_links = 0
    checked_spans = 0

    for doc in [p for p in files if p.suffix == ".md"]:
        text = doc.read_text(encoding="utf-8", errors="replace")

        for target in LINK.findall(text):
            if target.startswith(EXTERNAL):
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            checked_links += 1
            resolved = (doc.parent / path_part).as_posix()
            resolved = Path(resolved).resolve().relative_to(Path.cwd().resolve())
            if resolved.as_posix() not in tracked and not resolved.is_dir():
                broken.append(f"{doc}: link -> {target}")

        for name in CODE_SPAN.findall(text):
            base = Path(name).name
            if base not in by_name:
                continue
            checked_spans += 1
            candidates = by_name[base]
            # A bare basename is fine if it is unique in the repository.
            # `README.md` is excluded: it is a generic word, not a path.
            if name == base:
                if len(candidates) > 1 and base != "README.md":
                    ambiguous.append(f"{doc}: `{name}` matches {candidates}")
                continue
            # A span with a separator may be written relative to the document
            # or relative to the repository root. Either resolving is enough.
            root = Path.cwd().resolve()
            options = []
            for candidate in ((doc.parent / name), Path(name)):
                try:
                    options.append(
                        candidate.resolve().relative_to(root).as_posix()
                    )
                except ValueError:
                    continue
            if not any(option in tracked for option in options):
                broken.append(f"{doc}: path span -> `{name}`")

    print(f"markdown files scanned: {sum(1 for p in files if p.suffix == '.md')}")
    print(f"relative links checked: {checked_links}")
    print(f"inline path spans checked: {checked_spans}")

    if ambiguous:
        print(f"\nambiguous basenames ({len(ambiguous)}):")
        for item in ambiguous:
            print(f"  {item}")
    if broken:
        print(f"\nBROKEN REFERENCES ({len(broken)}):")
        for item in broken:
            print(f"  {item}")
        return 1
    print("\nall references resolve")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
