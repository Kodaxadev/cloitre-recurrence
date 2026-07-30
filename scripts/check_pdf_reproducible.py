#!/usr/bin/env python3
"""Compare two independently produced PDFs and report whether they are identical.

    scripts/check_pdf_reproducible.py A.pdf B.pdf [--require]

A `pdflatex` build is not byte-reproducible by default: it embeds a wall-clock
`/CreationDate` and a time-derived `/ID`. Setting `SOURCE_DATE_EPOCH` fixes the
dates from TeX Live 2016 on; the trailer id needs `\\pdftrailerid{}`, which
`main.tex` now sets. With both in place the builds match, and CI and
`scripts/reproduce.sh` pass `--require` so a regression fails rather than warns.

Without `--require` the difference is reported and the exit status stays zero.
That mode is for diagnosis on a toolchain where equality does not hold: the
field-by-field breakdown below says which of the four is responsible, which is
how the trailer id was identified as the last one.
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

FIELDS = {
    "CreationDate": rb"/CreationDate\s*\(([^)]*)\)",
    "ModDate": rb"/ModDate\s*\(([^)]*)\)",
    "ID": rb"/ID\s*\[\s*<([0-9A-Fa-f]+)>",
    "Producer": rb"/Producer\s*\(([^)]*)\)",
}


def metadata(data: bytes) -> dict[str, str]:
    found: dict[str, str] = {}
    for name, pattern in FIELDS.items():
        match = re.search(pattern, data)
        found[name] = match.group(1).decode("latin-1") if match else "(absent)"
    return found


def main(argv: list[str]) -> int:
    args = [a for a in argv[1:] if not a.startswith("--")]
    require = "--require" in argv[1:]
    if len(args) != 2:
        print(__doc__)
        return 2

    first, second = Path(args[0]), Path(args[1])
    for path in (first, second):
        if not path.is_file():
            print(f"missing: {path}")
            return 2

    blobs = [path.read_bytes() for path in (first, second)]
    digests = [hashlib.sha256(blob).hexdigest() for blob in blobs]

    print(f"{first}: {digests[0]}  ({len(blobs[0])} bytes)")
    print(f"{second}: {digests[1]}  ({len(blobs[1])} bytes)")

    if digests[0] == digests[1]:
        print("\nREPRODUCIBLE: two independent builds produced identical bytes.")
        print("A recorded hash of this PDF therefore documents correspondence")
        print("with its source, not merely custody of one file.")
        return 0

    print("\nNOT REPRODUCIBLE: the builds differ.")
    left, right = metadata(blobs[0]), metadata(blobs[1])
    for name in FIELDS:
        mark = "  " if left[name] == right[name] else "->"
        print(f"{mark} {name:13} {left[name]}")
        if left[name] != right[name]:
            print(f"   {'':13} {right[name]}")
    print(
        "\nA hash of such a build documents custody only: a reviewer rebuilding\n"
        "from the same source cannot reproduce it. The dates are pinned by\n"
        "SOURCE_DATE_EPOCH in scripts/build_paper.sh and the trailer id by\n"
        "\\pdftrailerid{} in main.tex, so if one of those four fields is marked\n"
        "above, check that both are still in effect. If none is marked, the\n"
        "difference is in the page content and this toolchain differs from the\n"
        "one CI uses."
    )
    return 1 if require else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
