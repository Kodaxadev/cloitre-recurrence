# Excluding the critical all-unit unique tail

## Scope

This note uses Theorem 90 from
[unit-wrap-chain-analysis.md](unit-wrap-chain-analysis.md). It excludes an
infinite safe tail in which every positive block has one wrap and every
adjacent-block gate is unique. It does not exclude tails containing longer
wrap blocks or infinitely many nonunique gates.

## Theorem 91 (no eventual all-unit, all-unique tail)

No infinite safe path can eventually have both of the following properties:

1. every positive block has exactly one wrap;
2. every adjacent positive-block gate is unique.

### Proof

Assume such a tail exists and index its positive-block starts by \(j\).
Write their coordinates as \((n_j,U_j,D_j,s_j)\), let \(r_j\) be the
zero-only gap to the next positive block, and put

\[
L_j=\lfloor\log_2n_j\rfloor.
\]

Theorem 90 gives

\[
D_j/n_j\longrightarrow1 \tag{91.1}
\]

and, for every sufficiently large \(j\),

\[
D_j+r_j-3<2^{r_j+5}. \tag{91.2}
\]

The exact child-zero condition in Lemma 85 gives

\[
2^{r_j+1}s_j\le n_j-U_j+r_j+1.
\]

Since \(s_j\ge1\) and \(U_j\ge0\),

\[
2^{r_j+1}\le n_j+r_j+1. \tag{91.3}
\]

For large \(j\), (91.3) first implies \(r_j<n_j\). If
\(r_j\ge L_j+1\), then its left side is at least \(2^{L_j+2}\), while

\[
n_j+r_j+1<2n_j+1\le2^{L_j+2}-1,
\]

a contradiction. Hence

\[
r_j\le L_j. \tag{91.4}
\]

By (91.1), eventually \(D_j-3\ge n_j/2\). Combining this with (91.2)
gives

\[
n_j/2<2^{r_j+5},
\]

so

\[
L_j-5\le r_j\le L_j. \tag{91.5}
\]

Define the offset

\[
h_j=L_j-r_j\in\{0,1,2,3,4,5\}. \tag{91.6}
\]

The exact transition is

\[
2^{r_j+2}s_j=n_j+r_j+5+s_{j+1}. \tag{91.7}
\]

At the next positive start,
\(s_{j+1}\le D_j+r_j-3\le n_j+r_j-3\). Equations (91.4), (91.5), and
(91.7) therefore give, for all sufficiently large \(j\),

\[
1\le s_j<48. \tag{91.8}
\]

Thus both \(h_j\) and \(s_j\) range over fixed finite sets.

Now suppose two consecutive starts lie in the same dyadic epoch:

\[
L_j=L_{j+1}=L.
\]

From (91.7) and \(r_j=L-h_j\),

\[
n_j
=2^{L-h_j+2}s_j-L+h_j-5-s_{j+1}. \tag{91.9}
\]

Since \(n_{j+1}=n_j+r_j+2\), this also gives

\[
n_{j+1}=2^{L-h_j+2}s_j-s_{j+1}-3. \tag{91.10}
\]

Apply (91.9) at \(j+1\) and compare with (91.10):

\[
2^{L-3}K
=-L+h_{j+1}+s_{j+1}-s_{j+2}-2, \tag{91.11}
\]

where

\[
K=2^{5-h_j}s_j-2^{5-h_{j+1}}s_{j+1}\in\mathbb Z.
\]

If \(K\ne0\), the left side of (91.11) has absolute value at least
\(2^{L-3}\), while (91.6) and (91.8) bound the right side by \(L+49\).
This is impossible for \(L\ge9\). If \(K=0\), equation (91.11) instead
forces

\[
L=h_{j+1}+s_{j+1}-s_{j+2}-2\le49.
\]

Consequently no two consecutive sufficiently late starts can share a dyadic
epoch \(L\ge50\).

But (91.4) gives

\[
n_{j+1}-n_j=r_j+2\le L_j+2. \tag{91.12}
\]

Whenever a late transition crosses from epoch \(L\) to a larger epoch,
(91.12) shows

\[
2^{L+1}\le n_{j+1}<2^{L+1}+L+2<2^{L+2},
\]

so \(L_{j+1}=L+1\). Applying (91.12) once more gives

\[
n_{j+2}<2^{L+1}+2L+5<2^{L+2},
\]

while \(n_{j+2}\ge2^{L+1}\). Hence
\(L_{j+2}=L_{j+1}=L+1\), producing two consecutive starts in the same
arbitrarily large epoch. This contradicts (91.11).

Therefore the assumed tail cannot exist.

## Consequence

Any hypothetical infinite safe path must contain either infinitely many
positive blocks with at least two wraps or infinitely many nonunique
adjacent-block gates. This is an exhaustive alternative within the
eventually-no-down branch, but neither surviving option is yet excluded.
