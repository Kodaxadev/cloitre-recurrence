# Exact arbitrary-block gate boundaries

Retain Lemma 83's adjacent positive-block gate. A zero epoch
\((n,U,e)\) begins a block of length \(k\ge1\), returns to
\((m,V,f)\), and is followed by \(r\ge0\) zero-only blocks before the next
positive block. Define

\[
A=n+4-2e,\quad d=A-U-4,\quad G=m-2V,
\]

\[
x=2^{r+2}f-m-r-3,\quad H=2^{k+r+3},
\]

and let

\[
d'=m+r-V-2^{r+1}f
\]

be the defect at the next positive-block start.

## Lemma 92 (exact arbitrary-block uniqueness boundary)

One has

\[
1\le x\le G+r-3,\qquad G+r-3-x=2d'. \tag{17.1}
\]

The gate is unique if and only if

\[
\boxed{
x\le H
\quad\text{and}\quad
\bigl(d\le1\ \text{or}\ 2d'<H\bigr).
} \tag{17.2}
\]

### Proof

Multiplying Lemma 83's gate interval by \(2^{r+2}\) and subtracting
\(m+r+3\) gives the bounds on \(x\). Direct substitution gives the defect
identity in (17.1).

Gate candidates differ by \(2^{k+1}\). Moving to the lower neighbor sends
\((x,A)\) to \((x-H,A+2)\). Because \(k\ge1\), the failed first stopping
test and parity give \(A\le n\), so the parent upper bound remains valid.
Thus the lower neighbor survives exactly when \(x>H\).

Moving to the upper neighbor sends \((x,d)\) to \((x+H,d-2)\). It survives
exactly when

\[
d\ge2,\qquad x+H\le G+r-3.
\]

Corollary 84's exact reconstruction makes these tests sufficient. Hence
both neighbors fail exactly when

\[
x\le H,\qquad d\le1\ \text{or}\ x+H>G+r-3.
\]

Use (17.1) to obtain (17.2). \(\square\)

## Corollary 93 (exact nonunique alternative)

The gate is nonunique if and only if

\[
\boxed{
x>H
\quad\text{or}\quad
\bigl(d\ge2\ \text{and}\ 2d'\ge H\bigr).
} \tag{17.3}
\]

If it is unique and \(d\ge2\), then

\[
\boxed{G+r-3<2^{k+r+4}.} \tag{17.4}
\]

### Proof

The first assertion is the complement of (17.2). In the stated unique
case, \(x\le H\) and \(x+H>G+r-3\), so
\(G+r-3<2H=2^{k+r+4}\). \(\square\)

This is an exact boundary localization for arbitrary block lengths, not a
termination theorem.

## Lemma 94 (affine defect compatibility)

Every adjacent positive-block gate satisfies

\[
\boxed{
\bigl(2^{k+r+1}-1\bigr)U
-\bigl(2^{r+1}-1\bigr)n
=2^{r+1}(k+4)-2^{k+r+1}(d+4)-r-1+d'.
} \tag{17.5}
\]

For two consecutive gates with fixed parameters
\((k,r,d,d')\) and \((\ell,r',d',d'')\), define

\[
a=2^{r+1},\ b=2^{k+r+1},\
a'=2^{r'+1},\ b'=2^{\ell+r'+1}.
\]

If

\[
\Delta=(b'-1)(a-1)-(b-1)(a'-1)\ne0, \tag{17.6}
\]

then the parameters determine at most one rational pair \((n,U)\).

### Proof

The returned residue obeys

\[
f=n+k+4-2^k(U+d+4)
\]

and the child defect obeys

\[
d'=n-U+r+1-2^{r+1}f.
\]

Substitution proves (17.5). Apply it again at
\((n+k+r+1,U+k)\). The resulting two linear equations have determinant
(17.6), proving the claim. \(\square\)

When \(d,d',d''\in\{0,1\}\), this reduces every fixed parent-boundary
parameter tuple to one rational state and its integral validity checks.
It does not bound the parameters.
