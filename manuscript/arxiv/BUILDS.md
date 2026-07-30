# Compiled build record

Compiled PDFs are **not** tracked in this repository. This file is the provenance
record instead: it says which source commit produced each build, what that build
lacked, and its SHA-256.

## Why the PDFs are not tracked

The repository's convention for large generated artifacts is to exclude them and
record their hashes — that is what `.gitignore` does for `data/scan_*.csv`, with
the hashes in [`../../audit/evidence-manifest.md`](../../audit/evidence-manifest.md).

That convention transfers to PDFs only partly, and the difference is worth
stating plainly.

`data/scan_*.csv` is **deterministic**: rerun the sweep and you get a
byte-identical file, so its recorded hash lets anyone verify the artifact
corresponds to the source. A `pdflatex` build is **not** deterministic by
default. Each of the builds below embeds a wall-clock `/CreationDate` and a
time-derived `/ID`, so recompiling the same source produces a different file with
a different hash.

So for the three superseded builds listed below, a hash documents **custody** —
this exact file existed and was produced from that commit — but it does **not**
document **correspondence**, because a reviewer rebuilding from the same source
cannot reproduce them. Do not read that table as more than custody. This
limitation applies to those builds only; it no longer applies to new ones.

**This has since been fixed, and the fix is enforced.** `scripts/build_paper.sh`
exports a fixed `SOURCE_DATE_EPOCH`, and `main.tex` sets `\pdftrailerid{}`.
CI compiles the paper twice, independently, and fails if the bytes differ.

The two changes were not guesswork. With only `SOURCE_DATE_EPOCH` set, CI
measured two builds of identical source as differing in exactly one field:

```
CreationDate  D:20260101000000Z   identical
ModDate       D:20260101000000Z   identical
Producer      pdfTeX-1.40.25      identical
ID            15A1E0AA...         DIFFERENT
              6E8B4E30...
```

Same length, 324743 bytes both. So the dates were already handled and the
trailer id was the only remaining cause. After fixing it, both builds hash to
`84b75af2ba44b033a00720c49e61ddd301636f24a84d59654dce6cf438a7e171`.

A hash of a build produced this way documents **correspondence** with its
source, not merely custody, and the release build can be verified by anyone who
rebuilds from the tag.

## Superseded builds

None of these is a release. Each was invalidated by a later correction, and all
three predate the current title. They are kept outside the repository, in a
sibling directory, purely as a record.

| Source commit | SHA-256 | Superseded because |
|---|---|---|
| `2d6fc17` | `408ca0094e446d4ecf532d2a70ead1ae585e1059f82cbec51573e0b731018d29` | Section 7's Lean boundary predates the formalization of Theorem 18 and the absorption converse; attribution and title both later corrected |
| `8151cd0` | `d56facf28b3de5c3c738d45451ab6643c3f184d2e274093b206cfab6ec7814e9` | Attribution still credited A073117 to Cloitre rather than Zumkeller; title later corrected |
| `2211b19` | `47b25535bd0600d3554efa94846a6560f631b61f00b50e4d5e0d1d6e57c89e9d` | Predates the neutral title applied in `910f6a9`; otherwise current |

Each was compiled twice with `pdflatex` under TeX Live 2025 and reported 8 pages,
no errors, no undefined references or citations, and no overfull or underfull
boxes.

## Release build

When the paper is frozen:

1. Apply the remaining editorial batch — the author details in
   [`README.md`](README.md).
2. Run `bash scripts/build_paper.sh`, or download the artifact from the CI run.
   The build is already deterministic, so no extra step is needed.
3. Tag the commit and record the build's hash here. Because the build is
   reproducible, that hash is verifiable by anyone rebuilding from the tag.
4. Attach the PDF to the GitHub Release rather than committing it. A Release
   asset is immutable, tied to a tag, and does not enter git history — where a
   binary cannot later be removed without rewriting it.

The superseded builds can be deleted once a release exists. Their value is the
table above, not the files: a stale PDF carrying a plausible commit hash in its
filename is exactly the confusion the title-page hash removal was guarding
against.
