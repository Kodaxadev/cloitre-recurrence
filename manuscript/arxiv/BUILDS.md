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

### Exactly what that buys, and what it does not

What has been demonstrated is **same-environment repeatability**: identical
source, compiled twice on the same runner with the same TeX Live, gives
identical bytes. That is strictly weaker than source-only reproducibility, and
the difference matters for a reviewer.

CI compiles on `ubuntu-latest` with TeX Live 2023/Debian, pdfTeX 1.40.25,
installing texlive packages from the runner's current APT repositories. The
[`Dockerfile`](../../Dockerfile) is Debian bookworm, which ships TeX Live 2022.
Those are two different environments, and this is not a hypothetical worry —
run `30574944526` compiled the same source in both and measured the result:

| | `ubuntu-latest` | `debian:bookworm-slim` |
|---|---|---|
| pdfTeX | 3.141592653-2.6-1.40.25 | 3.141592653-2.6-1.40.24 |
| TeX Live | 2023/Debian, `texlive-base 2023.20240207-1` | 2022/Debian, `texlive-base 2022.20230122-3` |
| bytes | 324,668 | 324,470 |
| SHA-256 | `84b75af2…` | `d0ec921b…` |

`CreationDate` and `ModDate` agreed, and `/ID` was absent from both, so the two
fixes hold across the change. What differs is `/Producer` and 198 bytes of
output. **A reviewer who rebuilds from the tag under a different TeX Live gets a
valid PDF with a different hash, and that is not evidence of tampering.**

The claim this record therefore makes is:

> The build is byte-repeatable **within a recorded TeX environment**.
> Verifying a PDF hash needs both the tagged source and that environment.

To make the two operational rather than rhetorical, every build now writes
`environment.txt` beside the PDF, holding the pdfTeX banner and the exact
version of every installed `texlive*` package. A recorded hash is meaningful
only next to that file, and the release provenance records the pair.

The table above is not a one-off. CI reruns that comparison on every push, in a
step that never fails the build — a difference there is expected behaviour of
TeX Live, not a defect here — so the release row below can record what the
cross-release answer was for the build being released, rather than assuming it
is still what it was measured to be today.

Full source-only reproducibility, if it is ever wanted, needs the build
environment itself pinned immutably: a base image pinned by OCI digest and
packages from an immutable snapshot, with the image digest recorded alongside
the source and PDF hashes. That is deliberately not done here — it trades CI
robustness for a guarantee this draft does not need — and so it is not claimed.

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
3. Tag the commit and record here **three** things, not one: the hash, the
   contents of the build's `environment.txt`, and what the cross-release step
   reported for that build. The hash alone is not checkable; the hash next to
   its environment is.
4. Attach the PDF to the GitHub Release rather than committing it. A Release
   asset is immutable, tied to a tag, and does not enter git history — where a
   binary cannot later be removed without rewriting it.

The superseded builds can be deleted once a release exists. Their value is the
table above, not the files: a stale PDF carrying a plausible commit hash in its
filename is exactly the confusion the title-page hash removal was guarding
against.
