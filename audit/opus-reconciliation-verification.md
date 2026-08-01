# Independent verification of the audit reconciliation

## Identity and evidence boundary

The follow-up audit supplied after commit `4c2a211` was 5,730 bytes with
SHA-256

```text
a0e8a4301ccd92e919d6fa247748d294a63b7d924166780f712b79e4badd1738
```

The reviewer re-audited the reconciliation rather than accepting the
repository's continuation reports. Its scratch implementation and full
output remain untracked, so this is independent AI review evidence, not a
self-contained reproduction package or human peer review.

## Confirmed reconciliation

The reviewer independently confirmed:

- commit `4c2a211` and its clean remote branch identity;
- Corollary 86's added parent lower-bound implication;
- Lemma 87's parity exclusion of the second formal integer candidate;
- the corrected \(D_{2t}\) paired subsequence and two-stage bootstrap in
  Corollary 89 and Theorem 90;
- Theorem 58's rebound inequality and order of limits;
- Lemma 63's exact terminal thresholds;
- the continuation-audit status of Theorems 77, 90, and 101.

No defect was found in the six audited cuts.

## Exact Lemma 100 recheck

An independent safe-map enumeration through \(n\le700\) found:

- 30 three-start parent-boundary windows;
- exactly five satisfying equality of the first two positive-block lengths;
- zero violations of strict second-gap growth.

The five initial raw states \((n,q,e)\), with
\((k_{\rm first},k_{\rm third},r_{\rm first},r_{\rm second})\), are:

```text
(12,  2,   5; 1, 1, 0, 1)
(39,  4,  17; 2, 2, 1, 2)
(41,  3,  19; 2, 2, 0, 1)
(174, 2,  86; 4, 3, 0, 3)
(492, 3, 244; 5, 4, 0, 1)
```

Thus the theorem-applicable cases span first-two block lengths
\(\{1,2,4,5\}\), and the third block length is not fixed. This gives
bounded empirical support for the symbolic dependency statement: Lemma 100
uses equality only for the first two block lengths. The Python and Rust
regressions now pin these exact witnesses.

## Remaining limits

The reviewer retained three limitations:

1. the independent \(10^7\) enumeration source and output are unarchived;
2. human specialist review is still absent;
3. the T46--T57, C64--T72, and L78--C82 band was outside the six cuts and
   remained separately scoped for audit at the time of the review.

The subsequent internal pass is recorded in
[`scoped-post-freeze-band.md`](scoped-post-freeze-band.md). It does not
replace human specialist review.

The original stabilization conjecture remains open.
