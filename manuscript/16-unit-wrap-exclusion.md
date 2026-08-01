# 16. Excluding the critical unit-wrap tail

### Theorem 91

No infinite safe path can eventually have every positive block of length one
and every adjacent-block gate unique.

#### Proof

Assume such a tail and use the coordinates of Sections 14--15. Put
\(L_j=\lfloor\log_2n_j\rfloor\). Theorem 90 gives \(D_j/n_j\to1\) and

\[
D_j+r_j-3<2^{r_j+5} \tag{16.1}
\]

for every late gate. The child-zero condition gives

\[
2^{r_j+1}\le2^{r_j+1}s_j\le n_j-U_j+r_j+1
\le n_j+r_j+1.
\]

It follows that \(r_j\le L_j\). Since \(D_j-3\ge n_j/2\) eventually,
(16.1) also gives

\[
L_j-5\le r_j\le L_j. \tag{16.2}
\]

Let \(h_j=L_j-r_j\in\{0,\ldots,5\}\). The exact transition

\[
2^{r_j+2}s_j=n_j+r_j+5+s_{j+1}
\]

and \(s_{j+1}\le D_j+r_j-3\) imply

\[
1\le s_j<48 \tag{16.3}
\]

for all late \(j\).

Suppose \(L_j=L_{j+1}=L\). The transition at \(j\) gives

\[
n_{j+1}=2^{L-h_j+2}s_j-s_{j+1}-3.
\]

The corresponding formula for the start \(j+1\) yields

\[
2^{L-3}
\left(2^{5-h_j}s_j-2^{5-h_{j+1}}s_{j+1}\right)
=-L+h_{j+1}+s_{j+1}-s_{j+2}-2. \tag{16.4}
\]

The parenthesized quantity is an integer. If it is nonzero, the left side
has magnitude at least \(2^{L-3}\), while (16.2)--(16.3) bound the right
side by \(L+49\). If it is zero, (16.4) forces \(L\le49\). Thus no two
late starts share an epoch \(L\ge50\).

On the other hand,

\[
n_{j+1}-n_j=r_j+2\le L_j+2.
\]

After any crossing from epoch \(L\) to \(L+1\), the new index is less than
\(2^{L+1}+L+2\). The following step is still below
\(2^{L+1}+2L+5<2^{L+2}\), so those two starts share epoch \(L+1\).
Arbitrarily large crossings therefore contradict (16.4).

Hence the assumed tail is impossible.

Any infinite safe path must consequently contain infinitely many blocks of
length at least two or infinitely many nonunique gates. The theorem does not
exclude either alternative.
