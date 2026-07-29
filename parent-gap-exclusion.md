# Excluding a persistent parent-boundary tail

## Scope

Corollary 97 reduces a hypothetical persistent parent-boundary tail to one
fixed positive block length. Theorem 99 gives bounded mean for its zero-only
gaps. This note proves that those same gaps would have to increase strictly,
which excludes the tail.

Retain the fixed length \(k\), gaps \(r_j\), returned residues \(f_j\), and
defects \(d_j\in\{0,1\}\). Put

\[
K=2^kk-k-1,\qquad
\delta_j=d_{j+1}-d_j.
\]

## Lemma 100 (fixed-length parent gaps increase)

Suppose three consecutive positive-block starts are in the parent boundary
layer, and the positive blocks at the first two starts have the same length
\(k\). Then their two zero-only gaps satisfy

\[
\boxed{r_{j+1}>r_j.} \tag{100.1}
\]

### Proof

The derivations of (98.2)--(98.3) are local: at indices \(j,j+1\) they use
only the three displayed defects and equality of the first two block
lengths. Hence those identities apply under the present hypotheses; no
fourth start or assumption on the third block length is needed.

Corollary 95 excludes \(r_{j+1}=r_j\). Suppose

\[
r'=r_{j+1}<r_j=r.
\]

Write

\[
f=f_j,\quad f'=f_{j+1},\quad
\delta=\delta_j,\quad\delta'=\delta_{j+1},
\]

\[
Q=r-K-2^k\delta,\qquad h=r-r'\ge1.
\]

Equation (98.3) gives

\[
f'=f+Q. \tag{100.2}
\]

Subtracting (98.2) at the two consecutive starts, using
\(A_{j+1}=A_j+k+\delta\), gives

\[
2^{r'+1}f'-2^{r+1}f=r'+1-\delta'. \tag{100.3}
\]

Substitute (100.2) and \(r=r'+h\):

\[
\boxed{
2^{r'+1}\bigl(Q-(2^h-1)f\bigr)
=r'+1-\delta'.
} \tag{100.4}
\]

If \(r'\ge1\), the right side is one of
\(r',r'+1,r'+2\), strictly between zero and \(2^{r'+1}\). This contradicts
the divisibility in (100.4).

It remains to take \(r'=0\). Then the right side is \(1-\delta'\).
If \(\delta'=0\), it is not divisible by two.

If \(\delta'=-1\), equation (100.4) gives

\[
Q=(2^r-1)f+1.
\]

Here \(d_{j+1}=1\), so \(\delta\in\{0,1\}\), and therefore \(Q\le r\).
But \(r\ge1\) and the right side is at least \(2^r\ge r+1\), a
contradiction.

Finally let \(\delta'=1\). Then

\[
Q=(2^r-1)f, \tag{100.5}
\]

and \(d_{j+1}=0\), so \(\delta=-d_j\).

If \(d_j=0\), then \(Q=r-K\le r\). Equation (100.5) forces

\[
k=1,\qquad r=1,\qquad f=1.
\]

But (98.2) then gives \(A_j=2<4\), impossible.

If \(d_j=1\) and \(k\ge2\), then

\[
Q=r-K+2^k<r,
\]

again contradicting (100.5). For \(k=1\), equation (100.5) becomes

\[
r+2=(2^r-1)f.
\]

It forces \(r=1,f=3\); the case \(r=2\) is not integral and
\(r\ge3\) is too large. Equation (98.2) then gives \(A_j=7\), so

\[
U_j=A_j-d_j-4=2,\qquad
n_j=2A_j-5+f=12.
\]

The required residue

\[
e_j=(n_j-U_j-d_j)/2=9/2
\]

is not integral. Every decreasing case is impossible, proving (100.1).
\(\square\)

## Theorem 101 (no persistent parent-boundary tail)

No infinite safe path can eventually have defect \(d\le1\) at every
positive-block start.

### Proof

Assume such a tail exists. Corollary 97 makes its positive block length
eventually equal to one fixed \(k\). Lemma 100 then makes its gaps strictly
increasing:

\[
r_j\ge r_0+j.
\]

Their Cesaro means therefore diverge. This contradicts Theorem 99, which
bounds the upper mean by \(2K+1\). \(\square\)

## Corollary 102 (surviving arbitrary-block gates)

Every hypothetical infinite safe path has infinitely many positive-block
starts with \(d\ge2\). At each such start, the outgoing gate is either:

1. nonunique; or
2. unique and in the child boundary layer \(2d'<2^{k+r+3}\).

### Proof

Theorem 101 gives infinitely many starts outside the parent layer.
Apply the exact alternatives in Lemma 92 and Corollary 93. \(\square\)

This removes the parent boundary as an eventual escape mechanism. It does
not yet exclude infinitely many nonunique gates or an aperiodic sequence of
unique child-boundary gates.
