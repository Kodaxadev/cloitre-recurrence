# arXiv draft package

## Working title

Currently in `main.tex`:

**The Eventual-Increment Spectrum of Cloitre's Recurrence Is Not Surjective**

Superseded by the decision recorded under "The title: decided" below, which is
held for the editorial batch and not yet applied.

This package is the first focused paper extracted from the broader `cloitre-recurrence` repository. It contains only the completed finite-start theorem and the independently certified proof that 5 and 7 are the smallest omitted eventual increments.

## Source basis

Repository: `Kodaxadev/cloitre-recurrence`

### Provenance convention

The commit hash is **not** on the title page, and should not be put back there.
A commit cannot contain its own hash: writing the hash into `main.tex` creates a
new commit with a different hash, so the printed line is stale the moment it is
written. That is what happened to the earlier `7ccda13...` line — the draft was
then corrected in a later commit and the title page still named the old one.

Provenance therefore lives here, in metadata that can be updated after a commit
without recompiling the PDF:

| Field | Value |
|---|---|
| Content basis | the commit containing this file |
| Release tag | *not yet created* |

For an immutable release, tag the commit and record the tag above. A tag is
created after the commit it names, so it carries no circularity:

```bash
git tag -a v0.1.0-paper -m "arXiv draft: eventual-increment spectrum" <commit>
git push origin v0.1.0-paper
```

Cite the tag, not a branch, in any archived version.

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
- Theorem 18 is machine-checked in Lean **in the form stated in the paper** (`Conjecture.finite_start_of_increment`), composing `finite_start` with the absorption converse `ray_of_eventual_increment`. The forced-rebound lemma, the ratchet and the quadratic step are also formalized. One gap remains: the nonsurjectivity theorem, whose finite exhaustion is checked by an independent program rather than in the proof assistant.
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
- **Lean boundary** in Section 7 rewritten twice. Theorem 18 is now itself
  machine-checked from the ray hypothesis, so the paragraph now states the two
  boundaries that actually remain: the converse half of the absorption criterion,
  and the finite exhaustion behind the nonsurjectivity theorem. The entry lemma
  is formalized in the form the proof consumes — existence plus minimality — and
  the paper now says the `⌈√(2m)⌉ + 2` bound is not needed for Theorem 18, which
  is true of the paper's own proof. Section 7 was then rewritten a third time
  when the absorption converse landed, and now states that both directions of the
  absorption criterion are formalized.
- `\bibitem{repository}` was never cited; Section 7 now cites it.
- **Attribution audit, done against the primary sources.** Fetched OEIS A073117
  and A117846 and the MathOverflow question metadata directly:
  - **A073117 is not Cloitre's.** The sequence was contributed by
    **R. Zumkeller, 19 Aug 2002**. **B. Cloitre** added a comment **one day
    later**, 20 Aug 2002, conjecturing stabilization for the *general* family
    `b(n+1) = b(n) + b(n) mod (n+a)`. So the conjecture is Cloitre's; the
    sequence is Zumkeller's. The introduction now says exactly this and the
    bibliography records both.
  - A117846 and the surjectivity question are **A. Abercrombie, 22 Mar 2007** —
    the paper was already correct, and the question is present verbatim as
    *"Do the values a(n) include all positive numbers?"*
  - The MathOverflow title was slightly wrong: it is
    *"Mod sequences that seem to become constant**;** and the number 316"*,
    asked by **Joseph O'Rourke, 26 Dec 2014**. Corrected, and the asker is now
    credited.
  - The ledger's "known" attributions were checked against the actual answers:
    T2 and T11 appear in RavenclawPrefect's answer (2025-09-03), pair merging in
    Gjergji Zaimi's (2014-12-29). Both now carry author and date.

## Compile status

The source has been compiled twice with `pdflatex` under TeX Live 2025 at the
commit that introduced the attribution corrections: 8 pages, no errors, no
undefined references or citations, no overfull or underfull boxes, preflight
passed, all pages visually inspected. That compile is current — it supersedes the
two earlier ones, which were invalidated by successive Section 7 rewrites.

**Editorial changes are batched from here.** Purely editorial edits to
`main.tex` and `sections/` are held until the release freeze rather than landed
one at a time, because each one invalidates the compiled PDF. Correctness changes
still land immediately. Pending batch:

| Change | Status |
|---|---|
| Retitle to the neutral option (below) | decided, held for the batch |
| Author contact details and ORCID | needs the author |

## The title: decided

The author's decision is the **neutral option**:

> The Eventual-Increment Spectrum of the Recurrence
> `b(n+1) = b(n) + (b(n) mod n)` Is Not Surjective

It avoids implying that Cloitre introduced this specific sequence, while the
introduction still describes it as the recurrence underlying Cloitre's
conjecture. "Zumkeller–Cloitre recurrence" would credit both but would coin an
eponym with no established use.

This has **not yet been applied to `main.tex`** — it is in the batch above, so
that the current compile stays valid until the freeze. The repository name and
`CITATION.cff` are a separate question and are unchanged.

### The audit that raised it

The title said *"Cloitre's Recurrence"*. The **conjecture** is Cloitre's but the
**sequence** is Zumkeller's, and Cloitre's comment concerns the general `n+a`
family rather than this specific recurrence. The three options weighed were:

1. Keep it, read as "the recurrence of Cloitre's conjecture".
2. Credit both, as "the Zumkeller–Cloitre recurrence".
3. Neutral: name the recurrence rather than a person.

Option 3 was chosen. Option 2 was rejected because it would coin an eponym with
no established use.

The repository name and `CITATION.cff` also say "Cloitre recurrence". Those are
a separate question — they name the research package rather than assert
mathematical priority, and changing them would break the citation identity
already pinned at `v0.1.0-audit`. They are unchanged.
- Verified numerically: every witness in Table 1, both candidate bounds
  (160 and 260), the absence of increments 5 and 7 below 260, and agreement of
  all 259 certificate rows with an independent recomputation.

## Editorial next steps

1. Obtain a line-by-line human mathematical review of the finite-start theorem.
2. Confirm historical attribution and bibliography wording.
3. Add author contact details and ORCID, if applicable.
4. Archive an immutable release containing the manuscript source, verifier, certificate, and hashes.
5. Tag the release commit and fill in the tag in the provenance table above.
6. Apply the batched editorial changes, then recompile once.
7. Compile with arXiv's TeX environment before submission. TeX Live 2025 gives a
   clean 8-page build, but arXiv's own preview is a separate submission-stage
   check.
