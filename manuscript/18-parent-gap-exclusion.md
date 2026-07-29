# Excluding the persistent parent boundary

Retain a fixed-length parent-boundary tail from Corollary 97, with block
length \(k\), gaps \(r_j\), residues \(f_j\), and defects
\(d_j\in\{0,1\}\). Put

\[
K=2^kk-k-1,\qquad\delta_j=d_{j+1}-d_j.
\]

## Lemma 100 (fixed-length parent gaps increase)

For three consecutive parent-boundary starts, if the positive blocks at the
first two starts have the same length,

\[
\boxed{r_{j+1}>r_j.} \tag{18.1}
\]

### Proof

The local derivation of Lemma 98's identities at \(j,j+1\) uses only these
three defects and the equality of the first two block lengths. It does not
use a fourth start or the third block length.

Equality is excluded by Corollary 95. Suppose \(r'=r_{j+1}<r_j=r\).
Write \(f=f_j\), \(f'=f_{j+1}\),
\(\delta=\delta_j\), and \(\delta'=\delta_{j+1}\). Lemma 98 gives

\[
f'=f+Q,\qquad Q=r-K-2^k\delta. \tag{18.2}
\]

Subtracting the two boundary equations gives

\[
2^{r'+1}f'-2^{r+1}f=r'+1-\delta'. \tag{18.3}
\]

For \(h=r-r'\ge1\), combine (18.2)--(18.3):

\[
2^{r'+1}\bigl(Q-(2^h-1)f\bigr)=r'+1-\delta'. \tag{18.4}
\]

If \(r'\ge1\), the right side lies strictly between zero and
\(2^{r'+1}\), contradicting divisibility.

Let \(r'=0\). If \(\delta'=0\), the right side is odd. If
\(\delta'=-1\), then \(Q=(2^r-1)f+1\), but
\(d_{j+1}=1\), hence \(\delta=1-d_j\in\{0,1\}\), and this gives
\(Q\le r<2^r\).

If \(\delta'=1\), then \(Q=(2^r-1)f\) and
\(\delta=-d_j\). For \(d_j=0\), the only formal possibility is
\((k,r,f)=(1,1,1)\), which gives \(A_j=2<4\). For \(d_j=1\), all
\(k\ge2\) give \(Q<r\). At \(k=1\), the only integral possibility is
\((r,f)=(1,3)\), which gives

\[
(n_j,U_j,d_j)=(12,2,1)
\]

and the nonintegral residue \(e_j=9/2\). Thus no decrease is valid.
\(\square\)

## Theorem 101 (no persistent parent-boundary tail)

No infinite safe path can eventually have \(d\le1\) at every
positive-block start.

### Proof

Corollary 97 makes the block length eventually constant. Lemma 100 then
makes the gaps strictly increasing, so their Cesaro means diverge. This
contradicts Theorem 99's upper mean bound \(2K+1\). \(\square\)

## Corollary 102 (surviving arbitrary-block gates)

Every hypothetical infinite safe path has infinitely many starts with
\(d\ge2\). Each outgoing gate is either nonunique or is unique in the child
boundary layer

\[
2d'<2^{k+r+3}.
\]

### Proof

Combine Theorem 101 with Lemma 92 and Corollary 93. \(\square\)

The child-boundary and nonunique alternatives remain open.
