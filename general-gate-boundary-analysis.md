# Exact boundaries for arbitrary safe-block gates

## Scope

This note sharpens Corollary 84 from a sufficient uniqueness bound to an
if-and-only-if test for a positive block of any length. It unifies the two
boundary mechanisms seen in Corollary 86, but it does not exclude either
mechanism from an infinite path.

Retain the setup of Lemma 83. A zero epoch \((n,U,e)\) begins a positive
block of length \(k\ge1\), which returns to

\[
(m,V,f),\qquad m=n+k+1,\qquad V=U+k.
\]

Let \(r\ge0\) zero-only blocks precede the next positive block. Put

\[
A=n+4-2e,\qquad d=A-U-4,\qquad G=m-2V,
\]

and define the child excess and lattice spacing

\[
x=2^{r+2}f-m-r-3,\qquad H=2^{k+r+3}.
\]

The defect at the next positive-block start is

\[
d'=m+r-V-2^{r+1}f.
\]

Both \(d\) and \(d'\) are nonnegative integers.

## Lemma 92 (exact arbitrary-block uniqueness boundary)

The gate quantities satisfy

\[
\boxed{1\le x\le G+r-3} \tag{92.1}
\]

and

\[
\boxed{G+r-3-x=2d'.} \tag{92.2}
\]

The realized adjacent-block gate is unique if and only if

\[
\boxed{
x\le H
\quad\text{and}\quad
\bigl(d\le1\ \text{or}\ x+H>G+r-3\bigr).
} \tag{92.3}
\]

Equivalently,

\[
\boxed{
\text{unique}
\iff
x\le H
\quad\text{and}\quad
\bigl(d\le1\ \text{or}\ 2d'<H\bigr).
} \tag{92.4}
\]

### Proof

The strict lower gate endpoint in Lemma 83 is exactly \(x>0\). Multiplying
its upper endpoint by \(2^{r+2}\) gives

\[
2^{r+2}f\le2(m-V+r).
\]

After subtracting \(m+r+3\), this becomes \(x\le G+r-3\), proving
(92.1). Direct substitution gives

\[
\begin{aligned}
G+r-3-x
&=m-2V+r-3-\bigl(2^{r+2}f-m-r-3\bigr)\\
&=2\bigl(m+r-V-2^{r+1}f\bigr)=2d',
\end{aligned}
\]

which proves (92.2).

By Lemma 83, every gate candidate lies in one residue class modulo
\(2^{k+1}\). Replacing \(f\) by \(f-2^{k+1}\) replaces \(x\) by \(x-H\)
and \(A\) by \(A+2\). Because \(k\ge1\), failure of the first stopping test
gives \(2A<n+5\). Since \(A\equiv n\pmod2\), this implies \(A\le n\), so
\(A+2\le n+2\). All other parent bounds only improve. Hence the lower
neighbor is admissible exactly when

\[
x-H\ge1,
\]

or equivalently \(x>H\).

Replacing \(f\) by \(f+2^{k+1}\) replaces \(x\) by \(x+H\) and \(d\) by
\(d-2\). This upper neighbor is admissible exactly when

\[
d\ge2
\quad\text{and}\quad
x+H\le G+r-3.
\]

The exact reconstruction direction of Corollary 84 shows that these
neighbor tests are sufficient, not merely necessary. Farther lattice
neighbors cannot survive if the corresponding adjacent neighbor fails.
Thus neither neighbor is admissible exactly under (92.3). Substituting
(92.2) gives (92.4). \(\square\)

## Corollary 93 (exact nonunique alternative)

An adjacent positive-block gate is nonunique if and only if

\[
\boxed{
x>H
\quad\text{or}\quad
\bigl(d\ge2\ \text{and}\ 2d'\ge H\bigr).
} \tag{93.1}
\]

In particular, if a unique gate has \(d\ge2\), then

\[
\boxed{G+r-3<2^{k+r+4}.} \tag{93.2}
\]

### Proof

Equation (93.1) is the logical complement of (92.4). If the gate is unique
and \(d\ge2\), equations (92.3) and \(x\le H\) give

\[
G+r-3<x+H\le2H=2^{k+r+4}.
\]

This is (93.2). \(\square\)

## Consequence and limitation

Corollary 84 only proved that multiple candidates force a short combined
wrap/zero gap. Lemma 92 identifies both exact causes: either the lower
child neighbor survives, or both the parent and upper-child defects are
away from their boundary layers. Longer blocks therefore have the same
two-boundary structure as unit-wrap blocks.

The parent layer \(d\le1\) remains a genuine escape route, and (93.2) is
compatible with the logarithmic gap scale. These formulas reorganize the
two surviving cases after Theorem 91; they do not prove safe-map
termination.

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

the four block parameters and three defects determine at most one rational
pair \((n,U)\), hence at most one integral starting state.

### Proof

The returned residue has the two exact descriptions

\[
f=n+k+4-2^k(U+d+4)
\]

and

\[
d'=n-U+r+1-2^{r+1}f.
\]

Substitution and rearrangement give (94.1).

At the next positive-block start,

\[
n'=n+k+r+1,\qquad U'=U+k.
\]

Apply (94.1) again with \((n',U',\ell,r',d',d'')\), then move the known
increments to the right side. The two equations are linear in \(n,U\);
their coefficient determinant is (94.2). A nonzero determinant gives at
most one rational solution. \(\square\)

For the parent-boundary classification target, all three defects lie in
\(\{0,1\}\). Thus Lemma 94 reduces any fixed pair of block/gap parameters
to one divisibility and validity check. The parameters themselves remain
unbounded, so this reduction is not a finite proof.

## Corollary 95 (no singular parent-boundary family)

Suppose three consecutive positive-block starts have

\[
d,d',d''\in\{0,1\}.
\]

Then their two block/gap parameter pairs
\((k,r)\) and \((\ell,r')\) determine at most one rational starting pair
\((n,U)\). In particular, the determinant-zero case of Lemma 94 contains no
valid integral state.

### Proof

For one parameter pair define

\[
R(k,r)=
\frac{2^{k+r+1}-1}{2^{r+1}-1}
=2^k+\frac{2^k-1}{2^{r+1}-1}.
\]

For fixed \(k\), this is strictly decreasing in \(r\). If \(\ell<k\), then

\[
R(\ell,r')\le2^{\ell+1}-1\le2^k-1<R(k,r).
\]

Thus the determinant in (94.2) vanishes exactly when

\[
(k,r)=(\ell,r'). \tag{95.1}
\]

Assume (95.1), put \(a=2^{r+1}\), and equate the two right sides after the
known index and quotient increments are moved across. Direct simplification
gives

\[
a(M-r-1)=d''-d'-(r+1), \tag{95.2}
\]

where

\[
M=k(2^k-1)-2^k(d-d').
\]

If \(r\ge1\), the right side of (95.2) has absolute value at most \(r+2\),
whereas every nonzero left side has absolute value at least
\(2^{r+1}>r+2\). A zero left side is also impossible because the right side
is then at most \(-r<0\).

Let \(r=0\). Equation (95.2) becomes

\[
2(M-1)=d''-d'-1.
\]

Checking the three possible right-side values shows that compatibility
forces

\[
(k,r,d,d',d'')=(1,0,0,0,1).
\]

For these values, (94.1) is

\[
3U-n=-7.
\]

Hence \(n-U-d=2U+7\) is odd, contradicting the parity needed for the
integral residue

\[
e=(n-U-d)/2.
\]

Therefore no valid state lies in the singular case. Lemma 94 now gives the
claimed uniqueness for every fixed parameter tuple. \(\square\)
