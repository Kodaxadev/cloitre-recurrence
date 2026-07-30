# arXiv draft package

## Working title

**The Eventual-Increment Spectrum of Cloitre's Recurrence Is Not Surjective**

This package is the first focused paper extracted from the broader `cloitre-recurrence` repository. It contains only the completed finite-start theorem and the independently certified proof that 5 and 7 are the smallest omitted eventual increments.

## Source basis

Repository: `Kodaxadev/cloitre-recurrence`  
Drafted from commit: `7ccda13f112f3768a35d28759891aaa0689e3c77`

Primary source files used:

- `partial-proofs.md`
- `manuscript/01-foundations-and-spectrum.md`
- `supplement/02-certificates.md`
- `supplement/03-reproduction.md`
- `certificates/spectrum_m259.csv`

## Layout

`main.tex` holds the preamble, title, abstract and bibliography, and pulls in one
file per section from `sections/`. arXiv accepts multi-file sources, and the split
keeps each file inside the repository's per-file length gate.

| File | Section |
|---|---|
| `sections/01-introduction.tex` | statement of the main theorem |
| `sections/02-coordinates.tex` | quotient/remainder coordinates and absorption |
| `sections/03-entry.tex` | entry lemma, bounded quotient, doubling coordinate |
| `sections/04-ratchet.tex` | forced rebound and the ratchet |
| `sections/05-finite-start.tex` | Theorem: `m < (c+3)(3c+5)` |
| `sections/06-spectrum.tex` | the smallest omitted increments |
| `sections/07-certificate.tex` | certificate and reproducibility boundary |
| `sections/08-open.tex` | open problems |
| `sections/09-disclosure.tex` | acknowledgments and AI-assistance disclosure |

## Build

Run twice so cross-references resolve:

```bash
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

No bibliography tool is required; references are embedded in `main.tex`.

A structural check that needs no LaTeX installation — environment balance,
cross-references, citations, `\input` targets, brace balance — is run in CI:

```bash
python scripts/check_tex_structure.py
```

## Reproduce the finite certificate

From the repository root:

```powershell
python independent\verify_small_spectrum.py
Get-FileHash -Algorithm SHA256 certificates\spectrum_m259.csv
```

Expected SHA-256:

```text
66a06cff15735c4a3caf98575f29afbcd881fbef06334616fbc3bc772b7ab084
```

## Current status

- The finite-start theorem is written as a complete symbolic proof.
- The 259-row certificate is independently regenerated using arbitrary-precision literal recurrence dynamics, and a fresh recomputation agrees with all 259 rows.
- Universal stabilization remains open.
- Theorem 18 and the nonsurjectivity theorem are not formalized in Lean. Its two load-bearing steps, the forced-rebound lemma and the ratchet, now are.
- Human specialist review remains pending.

## Repository review applied to this draft

- **Ratchet proof gap, fixed.** The original proof asserted that an occupancy of
  level `q_u - 1` "must have been produced by the preceding down-step", which is
  the step needing proof: a flat step at that level could otherwise precede a
  further descent. Section 4 now carries the two-alternative induction, with a
  remark on why the second alternative is not optional, and the same induction is
  machine-checked in Lean (`Conjecture.ratchet`).
- **Bounded-quotient lemma**, final sentence: the implication
  `b_n < n^2  =>  q_n < n` that connects it to the entry lemma is now written out
  rather than bundled into "Consequently".
- **Lean boundary** in Section 7 restated: Sections 2–4 are formalized; what is
  missing for Theorem 18 is the entry lemma and the quadratic step
  `(n0-1)^2 < (c+2)n0  =>  n0 <= c+4`.
- `\bibitem{repository}` was never cited; Section 7 now cites it.
- Verified numerically: every witness in Table 1, both candidate bounds
  (160 and 260), the absence of increments 5 and 7 below 260, and agreement of
  all 259 certificate rows with an independent recomputation.

## Editorial next steps

1. Obtain a line-by-line human mathematical review of the finite-start theorem.
2. Confirm historical attribution and bibliography wording.
3. Add author contact details and ORCID, if applicable.
4. Archive an immutable release containing the manuscript source, verifier, certificate, and hashes.
5. Compile with arXiv's TeX environment before submission; no LaTeX toolchain is present in this development environment, so only the structural check has been run here.
