# Safe-wrap block investigation

This log records the route from the zero-epoch balance identities to
Lemma 80 and Corollaries 81--82. The original stabilization conjecture
remains open.

## 1. The balance identity is not enough

If zero epochs are indexed by \(i\) and their following wrap lengths are
\(k_i\), then

\[
W_i=W_0+i,\qquad
U_i=U_0+\sum_{j<i}k_j,\qquad
G_i=G_0+i-\sum_{j<i}k_j.
\]

Equivalently,

\[
\sum_{j<i}(k_j-1)=G_0-G_i.
\]

This is exact, but it does not force termination. For example, an abstract
alternating pattern \(k_i=0,2,0,2,\ldots\) keeps the partial balance bounded.
The threshold inequalities, not bookkeeping alone, must be used.

## 2. Minimality gives the missing local bound

At a zero epoch, Lemma 53 makes \(k\) the least integer satisfying

\[
2^{k+1}A\ge n+k+5,\qquad A\ge U+4.
\]

For a positive block, the failed test at \(k-1\) is therefore

\[
2^k(U+4)\le2^kA<n+k+4.
\]

The elementary inequality \(2^{k+2}\ge k+4\) then gives \(2^kU<n\).
This became Lemma 80.

## 3. Global consequences

Theorem 45 supplies \(U_n\ge(1-o(1))n/\log_2n\) on an infinite safe path.
Combining it with \(2^kU<n\) gives

\[
k\le\log_2\log_2n+o(1).
\]

Thus an unbounded-wrap-block argument cannot prove termination unless it
uses more than block length.

The same two bounds also force quantitative recurrence. If \(B(n)\) counts
completed positive blocks before a zero epoch, then the total wrap count is
at most \(B(n)(1+o(1))\log_2\log_2n\), apart from a fixed prefix. Hence

\[
\liminf
\frac{B(n)\log_2n\log_2\log_2n}{n}\ge1.
\]

## 4. Verification

The native safe-map test checks Lemma 80 on the bounded grid
\(2\le W\le100\), \(0\le U\le60\). The independent arbitrary-precision
verifier checks the same strict endpoints directly from raw \((n,q,e)\)
transitions while covering 84,575 accelerated zero epochs and 25,357 wrap
transitions.

These are regression checks of the finite algebra. Corollaries 81--82 remain
symbolic consequences of Theorem 45 and are not established by enumeration.

## 5. Surviving target

By Theorems 38 and 55, any infinite safe path would have an aperiodic block
sequence containing infinitely many positive terms. Corollaries 81--82 make
those positive blocks both frequent, on the
\(n/(\log n\log\log n)\) scale, and individually short, on the
\(\log\log n\) scale. The remaining problem is to control the residues of
these blocks relative to the moving terminating strip.
