# Affine dynamics on the parent gate boundary

## Scope

This note continues Lemma 92's arbitrary-block gate coordinates. It derives
an affine compatibility equation, eliminates its singular case for
parent-boundary triples, and proves that block lengths cannot increase while
consecutive starts stay in the parent layer. It does not exclude variable
zero-only gaps.

## Lemma 94 (affine defect compatibility)

Every adjacent positive-block gate satisfies

\[
\boxed{
\bigl(2^{k+r+1}-1\bigr)U
-\bigl(2^{r+1}-1\bigr)n
=2^{r+1}(k+4)-2^{k+r+1}(d+4)-r-1+d'.
} \tag{94.1}
\]

Consequently, fix two consecutive gates with parameters
\((k,r,d,d')\) and \((\ell,r',d',d'')\). Put

\[
a=2^{r+1},\quad b=2^{k+r+1},\quad
a'=2^{r'+1},\quad b'=2^{\ell+r'+1}.
\]

Unless

\[
\boxed{
\Delta=(b'-1)(a-1)-(b-1)(a'-1)=0,
} \tag{94.2}
\]

the parameters determine at most one rational pair \((n,U)\).

### Proof

The returned residue has the exact descriptions

\[
f=n+k+4-2^k(U+d+4)
\]

and

\[
d'=n-U+r+1-2^{r+1}f.
\]

Substitution gives (94.1). At the next positive-block start,

\[
n'=n+k+r+1,\qquad U'=U+k.
\]

Apply (94.1) again with \((n',U',\ell,r',d',d'')\). The resulting two
linear equations in \(n,U\) have determinant (94.2). \(\square\)

## Corollary 95 (no singular parent-boundary family)

Suppose three consecutive positive-block starts have

\[
d,d',d''\in\{0,1\}.
\]

Then every fixed pair of block/gap parameters determines at most one
rational starting pair \((n,U)\). The determinant-zero case contains no
valid integral state.

### Proof

Define

\[
R(k,r)=
\frac{2^{k+r+1}-1}{2^{r+1}-1}
=2^k+\frac{2^k-1}{2^{r+1}-1}.
\]

For fixed \(k\), this decreases strictly in \(r\). If \(\ell<k\), then

\[
R(\ell,r')\le2^{\ell+1}-1\le2^k-1<R(k,r).
\]

Thus (94.2) vanishes exactly when \((k,r)=(\ell,r')\). Put
\(a=2^{r+1}\) and equate the two right sides. Simplification gives

\[
a(M-r-1)=d''-d'-(r+1), \tag{95.1}
\]

\[
M=k(2^k-1)-2^k(d-d').
\]

For \(r\ge1\), a nonzero left side has magnitude at least
\(2^{r+1}>r+2\), while a zero left side cannot equal the strictly negative
right side. For \(r=0\), the binary cases leave only

\[
(k,r,d,d',d'')=(1,0,0,0,1).
\]

Equation (94.1) then reads \(3U-n=-7\), so
\(n-U-d=2U+7\) is odd and \(e=(n-U-d)/2\) is not integral. \(\square\)

## Lemma 96 (block lengths decrease on the parent layer)

Suppose two consecutive positive-block starts have defects

\[
d,d'\in\{0,1\}.
\]

If their positive block lengths are \(k\) and \(\ell\), then

\[
\boxed{\ell\le k.} \tag{96.1}
\]

No uniqueness assumption is needed.

### Proof

Put \(A=U+d+4\ge4\), and let \(f\) be the returned residue. The next start
has \(A'=A+k+d'-d\). Equation (94.1) gives

\[
\boxed{
(2^{r+1}-1)f
=(2^k-1)A+r-k+d+1-d'.
} \tag{96.2}
\]

Its index is

\[
\boxed{n'=2^kA+f+r-3.} \tag{96.3}
\]

Put

\[
C=(2^k-1)A,\qquad c=-k+d+1-d'\le1.
\]

We first prove

\[
\boxed{f+r\le C+1.} \tag{96.4}
\]

For \(r=0\), this follows directly from (96.2). Let \(r\ge1\) and put
\(a=2^{r+1}\). Since \(f\ge1\), equation (96.2) gives

\[
C\ge a-1-r-c\ge a-r-2.
\]

Moreover,

\[
\begin{aligned}
(C+1)(a-1)-(a-1)(f+r)
&=(a-2)C-ar+a-1-c\\
&\ge(a-1)(a-2-2r)\ge0.
\end{aligned}
\]

The last inequality uses \(2^{r+1}\ge2r+2\). This proves (96.4).

At the next start,

\[
A'=A+k+d'-d.
\]

By Lemma 53, the next block length \(\ell\) is the least \(j\ge0\) with

\[
2^{j+1}A'\ge n'+j+5.
\]

At \(j=k\), equations (96.3)--(96.4) give

\[
n'+k+5
\le(2^{k+1}-1)A+k+3.
\]

It remains to compare this with

\[
2^{k+1}A'
=2^{k+1}A+2^{k+1}(k+d'-d).
\]

If \(k=1\), then \(k+d'-d\ge0\), and its zero case has
\(A\ge4=k+3\). If \(k\ge2\), then
\(k+d'-d\ge k-1\), so

\[
A+2^{k+1}(k+d'-d)\ge k+3.
\]

Thus the stopping test already holds at \(j=k\), proving
\(\ell\le k\). \(\square\)

## Corollary 97 (eventual constant length on a parent-layer tail)

If every sufficiently late positive-block start has defect at most one,
then its positive block lengths are eventually constant.

### Proof

Lemma 96 makes those positive integer lengths nonincreasing. \(\square\)

The remaining parent-layer problem has a fixed block length but may still
have variable zero-only gaps.
