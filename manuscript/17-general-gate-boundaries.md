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

## Corollary 95 (no singular parent-boundary family)

If three consecutive positive-block starts have
\(d,d',d''\in\{0,1\}\), then every fixed pair of block/gap parameters
\((k,r),(\ell,r')\) determines at most one rational start.

### Proof

Put

\[
R(k,r)=\frac{2^{k+r+1}-1}{2^{r+1}-1}
=2^k+\frac{2^k-1}{2^{r+1}-1}.
\]

This decreases strictly with \(r\). If \(\ell<k\), then
\(R(\ell,r')\le2^{\ell+1}-1<2^k<R(k,r)\). Hence the determinant in
(17.6) vanishes exactly when \((k,r)=(\ell,r')\).

In that case compatibility of the two affine equations simplifies to

\[
2^{r+1}(M-r-1)=d''-d'-(r+1), \tag{17.7}
\]

\[
M=k(2^k-1)-2^k(d-d').
\]

For \(r\ge1\), a nonzero left side has magnitude greater than \(r+2\), and
a zero left side cannot equal the strictly negative right side. For \(r=0\),
the binary defect cases leave only

\[
(k,r,d,d',d'')=(1,0,0,0,1).
\]

Equation (17.5) then reads \(3U-n=-7\), so
\(n-U-d=2U+7\) is odd and \(e=(n-U-d)/2\) is not integral. Thus no valid
state lies in the singular case. \(\square\)

The unbounded block and gap parameters, not a singular affine family, are
the remaining obstruction.

## Lemma 96 (block lengths decrease on the parent layer)

Suppose two consecutive positive-block starts have
\(d,d'\in\{0,1\}\), and let their block lengths be \(k,\ell\). Then

\[
\boxed{\ell\le k.} \tag{17.8}
\]

No uniqueness assumption is needed.

### Proof

Put \(A=U+d+4\ge4\), and let \(f\) be the first block's returned residue.
At the next positive start,

\[
A'=A+k+d'-d.
\]

The affine defect equation gives

\[
(2^{r+1}-1)f
=(2^k-1)A+r-k+d+1-d', \tag{17.9}
\]

and the next index is

\[
n'=2^kA+f+r-3. \tag{17.10}
\]

Put \(C=(2^k-1)A\) and \(c=-k+d+1-d'\le1\). We claim

\[
f+r\le C+1. \tag{17.11}
\]

For \(r=0\), this is immediate from (17.9). For \(r\ge1\), put
\(a=2^{r+1}\). Since \(f\ge1\), equation (17.9) gives
\(C\ge a-r-2\). Therefore

\[
\begin{aligned}
(C+1)(a-1)-(a-1)(f+r)
&=(a-2)C-ar+a-1-c\\
&\ge(a-1)(a-2-2r)\ge0,
\end{aligned}
\]

proving (17.11).

At the next start, \(A'=A+k+d'-d\). Lemma 53 characterizes \(\ell\) as
the least \(j\) satisfying \(2^{j+1}A'\ge n'+j+5\). At \(j=k\),
(17.10)--(17.11) give

\[
n'+k+5\le(2^{k+1}-1)A+k+3.
\]

For \(k=1\), the inequality
\(A+2^{k+1}(k+d'-d)\ge k+3\) follows from \(A\ge4\).
For \(k\ge2\), it follows from \(k+d'-d\ge k-1\). Hence
\(2^{k+1}A'\ge n'+k+5\), so \(\ell\le k\). \(\square\)

## Corollary 97 (eventual constant length on a parent-layer tail)

If every sufficiently late positive-block start has defect at most one,
then its positive block lengths are eventually constant.

### Proof

Lemma 96 makes those positive integer lengths nonincreasing. \(\square\)

The remaining parent-layer problem therefore has a fixed block length but
may still have variable zero-only gaps.
