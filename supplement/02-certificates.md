# Finite certificates and verification boundaries

## Census certificate

The \(10^7\) witness census consists of:

- `data/census_10M.csv`: one row per distinct absorbed orbit;
- `data/census_10M.log`: terminal counts and deterministic digest;
- `data/sweep_10M.log`: live-set profile and terminal exhaustion;
- `data/excluded_increments.txt`: spectrum consequence using Theorem 18.

The certificate is compact because merged starts have identical future orbits.
The accounting identity is the completeness witness.

### Independent checks

The independent Rust verifier:

- uses raw \(b\)-form rather than \((q,r)\);
- uses `u128` rather than `u64`;
- finds the first absorbing index independently;
- checks hundreds of increments after the claimed index.

The Python verifier uses arbitrary-precision integers and checks the recurrence
behaviorally. All 200,000 rows of the smaller scan were rechecked by independent
Rust; Python deep-checked a deterministic sample. Selected \(10^7\)-range record
orbits were also rechecked.

### Remaining independence limitation

No second implementation currently reproduces the complete \(10^7\) compressed
census from the full start interval. The raw verifiers validate rows, but do not
independently establish the large census covering identity. Corollary 20 for
increments 5 and 7 is independently checked much more cheaply because
Theorem 18 restricts the required starts to \(m<160\) and \(m<260\).

The complete table `certificates/spectrum_m259.csv` contains every start
\(1\le m<260\). The standalone arbitrary-precision script
`independent/verify_small_spectrum.py` regenerates it from the literal
recurrence, confirms 64 constant increments after every first absorption,
checks its SHA-256, excludes 5 and 7, and prints witnesses for 1, 2, 3, 4, and
6. This closes the finite proof obligation for the “smallest missing”
statement without relying on the \(10^7\) census.

## Periodic denominator certificate

The command

```text
python scripts/periodic_phase_blocks.py --max-denominator 501
```

enumerates 250 odd denominators, finds 463 surviving boundary families, and
rejects every exact base-\(2^L\) subset equation. Its logical-record digest is

```text
1508d04cc91c8a007d17028efb24fe72
6785f4f210272721d8fc7f6149d4bb06
```

The script asserts this value. This is a finite cross-check of the boundary
reduction, not the proof of the all-denominator Theorem 38.

## Safe-map certificate

For start index \(N=10^6\), the quotient-zero safe sweep begins with all
\(999,999\) values \(1\le e<N\). At equal \(e\), the path with fewer wraps
dominates; retaining it is licensed by Lemma 41.

The frozen Rust result is

```text
ending index:      1,009,019
danger rejections: 2,756
captures:          9
dominated merges:  997,234
live states:       0
```

and satisfies

```text
999,999 = 2,756 + 9 + 997,234 + 0.
```

This proves only the stated finite-index result. The independent
arbitrary-precision generator `independent/verify_safe_certificate.py` now
reproduces the complete run using raw thresholds and a two-list linear merge.
Both implementations agree on every terminal count, the ending index, and the
full-layer trajectory digest

```text
0xffe3df00b02fcb2d.
```

The frozen cross-implementation summary is
`certificates/safe_n1000000.txt`.

## Cryptographic preservation

File SHA-256 values and the frozen source commit are recorded in
`../audit/evidence-manifest.md`. Any regenerated artifact must be compared by
content and hash; matching only headline counts is insufficient for a release
certificate.
