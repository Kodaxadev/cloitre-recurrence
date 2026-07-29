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

## 8. Unit-wrap induced coordinates and chain correction

The first quotient-zero search made a five-gate chain look potentially
extremal. That was a sampling artifact: allowing nonzero accumulated quotient
finds seven consecutive unique gates from the valid state
\((n,U,e)=(36,9,13)\). An exhaustive native scan of all 20,771,000 valid
positive-block zero epochs with \(2\le n\le1000\) found no longer chain, but
this finite result is not a theorem.

For a unit-wrap block, the coordinates

\[
D=n-2U,\qquad s=4e-n-3
\]

give the exact successor excess

\[
s'=2^{r+2}s-n-r-5,\qquad D'=D+r.
\]

Lemma 85 gives the exact candidate set in one residue class modulo \(4\).
Corollary 86 then identifies uniqueness with two explicit boundary layers.
This is a sharper target for a chain argument, but both alternatives remain
possible and the original conjecture remains open.

## 9. The parent-boundary branch cannot persist

For a unit-wrap start, put \(\delta=D-s\). The parent-boundary alternative
in Corollary 86 is exactly \(\delta<7\). Parity reduces this to
\(\delta\in\{3,5\}\).

Eliminating the intermediate state between two transitions gives

\[
(2^{r+2}-2^{r'+2})D
=2^{r'+2}r+2^{r+2}\delta
-(2^{r'+2}+1)\delta'-2r'-2+\delta''.
\]

The cases \(r=r'\), \(r>r'\), and \(r<r'\) can all be solved exactly.
Only

\[
(n,D,s):(12,8,5)\to(14,8,3)\to(17,9,4)
\]

survives, with \((r,r')=(0,1)\), and that path immediately enters the
terminating strip. Thus three consecutive parent-boundary starts are
impossible on an infinite path.

Corollary 88 strengthens this with the exact uniqueness test: a failure of
the short-gap inequality forces the successor parent boundary to be inactive.
Thus at least one gate in every two of a continuing unique unit-wrap chain
satisfies
\(D+r-3<2^{r+5}\). This forces frequent logarithmic zero-only gaps, but their
frequency remains compatible with the known \(n/\log n\) quotient scale.

Summing those gaps gives Corollary 89. If an infinite tail were both
all-unit-wrap and all-unique, then

\[
\liminf_j\frac{D_j}{j\log_2j}\ge\frac12,
\qquad
1\le\liminf_j\frac{U_j\log_2n_j}{n_j}
\le\limsup_j\frac{U_j\log_2n_j}{n_j}\le2.
\]

This pins the subcase to the same critical scale as Theorem 45, within a
factor of two, but does not close it.

Theorem 90 removes that remaining factor. A non-short unique gate must use
the parent boundary; its exact deficit equation and the failed short-gap
inequality imply \(U\ge D/2\). Corollary 89 instead gives \(U/D\to0\), so
every sufficiently late gate is short. Summing at every gate and matching
Theorem 45 yields the exact equality regime

\[
D_j\sim j\log_2j,\qquad
\frac{U_j\log_2n_j}{n_j}\to1.
\]

This is first-order rigidity, not termination. The unresolved issue is now
whether the exact integer residues can realize the equality case
aperiodically.

## 10. The critical unit-wrap tail is impossible

Theorem 91 resolves that equality case. The exact child-zero bound and
Theorem 90 give, with \(L=\lfloor\log_2n\rfloor\),

\[
L-5\le r\le L.
\]

The transition then bounds every late positive excess by \(1\le s<48\).
Thus the gap offset \(h=L-r\) and consecutive excesses range over finite
sets. If two starts share one dyadic epoch, their exact formulas imply

\[
2^{L-3}K=-L+h'+s'-s''-2
\]

for one integer \(K\). This is impossible for large \(L\): nonzero \(K\)
makes the left side exponential, while \(K=0\) forces \(L\le49\).

But a positive-block start advances only \(r+2\le L+2\). Every crossing into
a new large dyadic epoch therefore leaves the following start in that same
epoch, producing exactly the forbidden pair. Hence an infinite safe path
cannot be eventually all-unit and all-unique.

The surviving safe-map alternatives are now explicit: infinitely many
blocks of length at least two, or infinitely many nonunique gates.

## 11. Arbitrary blocks have the same exact two-boundary gate

The one-sided lattice count in Corollary 84 can be made exact without
assuming \(k=1\). For a returned residue \(f\), define

\[
x=2^{r+2}f-m-r-3,\qquad H=2^{k+r+3}.
\]

If \(d=A-U-4\) is the parent defect and \(d'\) is the defect at the next
positive-block start, direct substitution gives

\[
G+r-3-x=2d'.
\]

The lower neighboring gate value survives exactly when \(x>H\). The upper
neighbor survives exactly when \(d\ge2\) and \(2d'\ge H\). Hence

\[
\text{unique}\iff
x\le H\ \text{and}\ (d\le1\ \text{or}\ 2d'<H).
\]

This is Lemma 92. It shows that longer blocks do not introduce a third
uniqueness mechanism: they use the same parent/child boundary split as the
unit-wrap coordinates. The independent raw census confirms both directions
on 27,030 gates.

The same coordinates also give the affine compatibility equation

\[
(2^{k+r+1}-1)U-(2^{r+1}-1)n
=2^{r+1}(k+4)-2^{k+r+1}(d+4)-r-1+d'.
\]

Applying it to two consecutive gates produces a two-by-two linear system.
Except when its explicit determinant vanishes, every fixed parameter tuple
determines at most one rational start. This is Lemma 94.

The determinant ratio is

\[
\frac{2^{k+r+1}-1}{2^{r+1}-1}
=2^k+\frac{2^k-1}{2^{r+1}-1}.
\]

Its parameter ranges are disjoint for distinct \(k\), and it is strictly
decreasing in \(r\). Thus singularity requires identical block/gap pairs.
The remaining binary-defect equation has one formal solution, but it makes
the starting residue half-integral. Corollary 95 therefore removes the
singular case entirely for three parent-boundary starts.

A bounded affine search for two consecutive unique gates whose three starts
all have \(d\le1\) finds only three parameter patterns through
\(k,k',r,r'\le16\), including the terminal unit-wrap pattern and two
length-two patterns. This is useful evidence for the next classification
target, but the bound is computational and has not been promoted to a
theorem.

## 12. Parent-boundary block lengths cannot increase

At consecutive parent-boundary starts, let \(A=U+d+4\), let the first block
have length \(k\), let \(r\) zero-only blocks follow it, and let \(f\) be
its returned residue. The affine equation becomes

\[
(2^{r+1}-1)f=(2^k-1)A+r-k+d+1-d',
\]

while the next start index is

\[
n'=2^kA+f+r-3.
\]

Put \(C=(2^k-1)A\). The same equation and \(f\ge1\) give the sharp bound

\[
f+r\le C+1.
\]

At the next start \(A'=A+k+d'-d\). The stopping test for its block already
holds at \(j=k\), because

\[
n'+k+5\le(2^{k+1}-1)A+k+3
\le2^{k+1}A'.
\]

Hence the next block length is at most \(k\). A tail that stays in the
parent layer must therefore have one eventual constant block length.

A bounded affine scan finds no four consecutive parent-boundary starts with
that constant length through \(k,r,r',r''\le12\). This sharpens the next
target but remains finite evidence; no uniform four-start exclusion is
claimed.
