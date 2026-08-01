# Dyadic gates between positive safe-map blocks

This section gives an exact compatibility law between adjacent positive
blocks in the eventually-no-down safe map.

## Lemma 83 (adjacent positive-block gate)

Let a zero epoch \((n,U,e)\) have a positive wrap block of length \(k\ge1\)
and return to \((m,V,f)\), where \(m=n+k+1\) and \(V=U+k\). Suppose \(r\)
zero-only blocks then occur before the next positive block. With
\(A=n+4-2e\),

\[
m+3-f=2^kA,\qquad f\equiv m+3\pmod{2^k}, \tag{14.1}
\]

and the parity \(A\equiv n\pmod2\) sharpens the congruence to

\[
f\equiv m+3-2^k(m-k-1)\pmod{2^{k+1}}. \tag{14.2}
\]

Moreover,

\[
\frac{m+r+3}{2^{r+2}}
<f\le
\frac{m-V+r}{2^{r+1}}. \tag{14.3}
\]

### Proof

Lemma 53 gives
\[
m+4-2f=2^{k+1}A-(m+2),
\]
which rearranges to (14.1). Reducing it modulo \(2^{k+1}\) gives (14.2).
If \(r=0\), zero-epoch validity gives the upper bound in (14.3). For
\(r\ge1\), the last zero-only return gives
\(2^{r+1}f\le m-V+r\). The next block is positive exactly when
\(2^{r+2}f>m+r+3\), proving the lower bound. \(\square\)

## Corollary 84 (unique state or short gap)

Put \(G=m-2V\). For fixed \(m,V,k,r\), the number of integers satisfying
the lifted congruence, interval, and parent bounds is exactly the number of
locally valid returned residues and is at most

\[
\left\lceil
\frac{G+r-3}{2^{k+r+3}}
\right\rceil. \tag{14.4}
\]

Here the parent bounds are
\[
V-k+4\le(m+3-f)/2^k\le m-k+1.
\]
Hence either the returned residue and preceding zero epoch are uniquely
determined, or

\[
2^{k+r+3}<G+r-3. \tag{14.5}
\]

### Proof

The interval in (14.3) has length
\((G+r-3)/2^{r+2}\), while the lifted congruence class has spacing
\(2^{k+1}\). Conversely, a candidate defines
\[
A=(m+3-f)/2^k,\quad n=m-k-1,\quad U=V-k,\quad
e=(n+4-A)/2.
\]
The lifted congruence and parent bounds make this a valid zero epoch.
Lemma 53 reconstructs the specified \(k\)-wrap return, and (14.3)
reconstructs the \(r\) zero-only blocks and following positive block.
Thus the gate is exact, and the spacing proves (14.4).
Two points in the half-open interval require its length to be strictly
greater than that spacing, giving (14.5).
\(\square\)

The unique alternative remains possible; this is a compatibility
dichotomy, not termination.
