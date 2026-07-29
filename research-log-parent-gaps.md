# Research log: closing the persistent parent boundary

## 1. The fixed-length recurrence

After Corollary 97, a persistent parent-layer tail has one block length
\(k\). With

\[
K=2^kk-k-1,\qquad \delta_j=d_{j+1}-d_j,
\]

Lemma 98 gives

\[
f_{j+1}-f_j=r_j-K-2^k\delta_j.
\]

Combining consecutive boundary equations gives

\[
2^{r_{j+1}+1}f_{j+1}-2^{r_j+1}f_j
=r_{j+1}+1-\delta_{j+1}.
\]

## 2. Decreasing gaps fail divisibility

Assume \(r'=r_{j+1}<r_j=r\) and put \(h=r-r'\). Eliminating
\(f_{j+1}\) yields

\[
2^{r'+1}\left(
r-K-2^k\delta_j-(2^h-1)f_j
\right)
=r'+1-\delta_{j+1}.
\]

For \(r'\ge1\), the right side lies strictly between zero and the power of
two on the left. At \(r'=0\), parity leaves two formal cases. One has
\(A=2<4\); the other gives \((n,U,d)=(12,2,1)\) and the half-integral
residue \(e=9/2\).

Thus a fixed-length parent sequence has strictly increasing gaps.

## 3. The parent tail is impossible

Strictly increasing nonnegative gaps have divergent Cesaro mean. Theorem 99
bounds that mean by \(2K+1\). Hence no infinite safe path can eventually
remain at \(d\le1\).

The surviving safe alternatives are now exact: infinitely many interior
starts have either nonunique gates or unique gates in the child boundary
layer. The next proof search should not return to the eliminated
parent-boundary mechanism.
