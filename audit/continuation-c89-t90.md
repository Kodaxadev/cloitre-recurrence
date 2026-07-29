# Continuation audit: Corollary 89 and Theorem 90

## Scope and evidence boundary

This is the quantified asymptotic pass requested by
[`opus-pr2-audit.md`](opus-pr2-audit.md). It checks Corollary 89 and
Theorem 90 in
[`unit-wrap-chain-analysis.md`](../unit-wrap-chain-analysis.md), together
with their compact versions in
[`manuscript/15-unit-wrap-gates.md`](../manuscript/15-unit-wrap-gates.md).

The imported local boundary statements Corollaries 86 and 88 were rederived
in the Opus audit. Theorem 45 was audited before this post-freeze cut. This
pass focuses on the tail quantifiers, bootstrap summations, constants, and
limit conversions. These are symbolic asymptotic claims; bounded
computation cannot prove them.

## Corollary 89

### Divergence of \(D_j\)

The unit-wrap transition gives

\[
U_j=U_0+j,\qquad D_{j+1}=D_j+r_j,\qquad n_j=D_j+2U_j.
\]

Thus \(D_j\) is nondecreasing. If it were bounded, its nonnegative integer
increments would eventually satisfy \(r_j=0\). Then
\(s_j\le D_j-3\) would remain bounded, contradicting the next-positive
condition \(4s_j>n_j+5\) because \(n_j\to\infty\). Hence \(D_j\to\infty\).

### Pairwise logarithmic bootstrap

Corollary 88 gives, for every sufficiently late pair,

\[
D_{2t+2}-D_{2t}>
\log_2(D_{2t}-3)-5.
\]

For fixed \(\varepsilon>0\), the right side is eventually at least
\((1-\varepsilon)\log_2D_{2t}\). Because \(D_{2t}\to\infty\), the
increment is eventually at least one, and therefore
\(D_{2t}\ge t-O(1)\). Substitution back into the logarithm gives

\[
\log_2D_{2u}\ge\log_2u-O(1).
\]

Summing now yields

\[
D_{2t}\ge
(1-\varepsilon)t\log_2t-O_\varepsilon(t).
\]

Letting \(\varepsilon\downarrow0\) proves

\[
\liminf_t\frac{D_{2t}}{t\log_2t}\ge1.
\]

For \(j=2t\) or \(2t+1\), monotonicity and
\(j\log_2j\sim2t\log_2t\) give the claimed all-index constant \(1/2\).

### Quotient-scale upper constant

Put \(f(x)=\log_2x/x\), which is decreasing for all sufficiently large
\(x\). Since \(n_j\ge D_j\), for each fixed \(\varepsilon>0\) and all
large \(j\),

\[
\frac{U_j\log_2n_j}{n_j}
\le (U_0+j)f(D_j)
\le (U_0+j)
 f\!\left((\tfrac12-\varepsilon)j\log_2j\right).
\]

The upper limit of the right side is
\((1/2-\varepsilon)^{-1}\). Letting
\(\varepsilon\downarrow0\) gives the constant \(2\). Theorem 45 supplies
the lower-limit constant \(1\).

**Finding:** Corollary 89 is valid. The compact manuscript contained
\(D_{3t}\) in one logarithm; this was a transcription typo and has been
corrected to \(D_{2t}\). The bootstrap summation is now explicit in both
proofs.

## Theorem 90

### Eventual short-gate inequality

Put \(a=2^{r+2}\) and \(\delta=D-s\). If a unique gate fails

\[
D+r-3<8a,
\]

then Corollary 86's child-boundary alternative is impossible, so the parent
boundary is active and \(\delta\in\{3,5\}\). Failure gives
\(D\ge8a-r+3\). From

\[
\delta'=2U-(a-2)D+a\delta+2r+5\ge3
\]

one obtains

\[
2U\ge(a-2)D-5a-2r-2.
\]

The needed comparison

\[
(a-3)D\ge5a+2r+2
\]

holds directly at \(r=0\): \(a=4\), \(D\ge35\), and the two sides are at
least \(35\) and \(22\). For \(r\ge1\), \(r\le a/4\),
\(D>7a\), and \(a-3\ge5\), which is stronger than required. Therefore
every failing gate has \(U\ge D/2\).

Corollary 89 gives \(D_j\gg j\log j\), while \(U_j=U_0+j\), so
\(U_j/D_j\to0\). Only finitely many gates can fail.

### Every-gate bootstrap and exact constants

At every sufficiently late gate,

\[
D_{j+1}-D_j=r_j>
\log_2(D_j-3)-5.
\]

The same two-stage argument now applies at every index: first
\(D_j\ge j-O(1)\), then
\(\log_2D_j\ge\log_2j-O(1)\), and finally

\[
\liminf_j\frac{D_j}{j\log_2j}\ge1.
\]

The decreasing-function argument above now gives

\[
\limsup_j\frac{U_j\log_2n_j}{n_j}\le1.
\]

Theorem 45 supplies the reverse lower limit, hence this ratio tends to one.
Also \(U_j/D_j\to0\), so \(n_j/D_j\to1\) and

\[
\frac{j\log_2D_j}{D_j}\to1.
\]

Equivalently \(D_j/(j\log_2D_j)\to1\). Taking logarithms gives

\[
\log D_j=\log j+\log\log D_j+o(1),
\]

so \(\log D_j/\log j\to1\). Substitution proves
\(D_j/(j\log_2j)\to1\).

**Finding:** no mathematical defect found in Theorem 90. The proof's
boundary inference, small-\(r\) split, failure exclusion, all-gate
summation, and final inversion are valid. The summation quantifiers are now
written explicitly in both proof versions.

## Effect on the audit frontier

This closes item 2 in the Opus audit. Together with
[`continuation-t58-l63.md`](continuation-t58-l63.md), every mathematical
dependency that the supplied audit marked conditional has now received a
symbolic continuation pass. The remaining Opus evidence obligation is to
archive the independent \(10^7\)-enumeration implementation or certificate.

The original stabilization conjecture remains open.
