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

## 6. Boundary recurrence and backward clearance

A bounded search does not support the claim that a path hitting zero slack
must revisit it. Among quotient-zero starts with \(N\le1000\), paths occur
that survive more than 180 further transitions after their only boundary
hit. Arbitrary boundary states show the same behavior.

The exact backward-clearance calculation also recovers the existing
logarithmic budget rather than improving it. A reverse zero preimage keeps
clearance but halves the residue, while a reverse wrap preimage consumes one
unit of clearance. Thus logarithmically many reverse zero steps can be paid
for by one wrap, dual to Theorem 45's forward zero-run count.

## 7. The adjacent-block gate

A positive block of length \(k\) returning to \((m,V,f)\) satisfies

\[
m+3-f=2^kA.
\]

If \(r\) zero-only blocks precede the next positive block, the return residue
also lies in

\[
\frac{m+r+3}{2^{r+2}}<f\le\frac{m-V+r}{2^{r+1}}.
\]

The interval has length \((G+r-3)/2^{r+2}\). The parent equation first puts
\(f\) in one class modulo \(2^k\); the parity \(A\equiv n\pmod2\) lifts this
to one class modulo \(2^{k+1}\). This yields Lemma 83 and Corollary 84:
the gate is unique unless \(2^{k+r+3}<G+r-3\).

The independent raw verifier and native Rust test agree on 29,630 bounded
gates, of which 9,718 are unique and 19,912 admit multiple candidates.
These counts are regression evidence, not an asymptotic distribution claim.

Unique gates are not isolated. The valid quotient-zero start
\((n,U,e)=(61,0,49)\) contains five consecutive unique gates with
\((k,r)\) pairs
\[
(2,1),(1,2),(2,3),(1,2),(1,4).
\]
Thus a proof must control chains of exact gates; it cannot assume that the
nonunique alternative occurs between every two positive blocks.
