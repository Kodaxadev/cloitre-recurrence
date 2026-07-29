# A dyadic gate between positive safe-map blocks

This note links one positive safe-map wrap block to the next. It gives an
exact residue class, a sharp interval, and a uniqueness criterion for the
intermediate zero epoch. It does not prove termination.

## Setup

Let a zero epoch \((n,U,e)\) be followed by a positive wrap block of length
\(k\ge1\), returning to the zero epoch

\[
(m,V,f),\qquad m=n+k+1,\qquad V=U+k.
\]

Let \(r\ge0\) be the number of consecutive zero-only blocks after this
return and before the next positive block. Thus the next positive block
begins at the zero epoch

\[
(m+r,V,2^rf).
\]

Put

\[
G=m-2V.
\]

## Lemma 83: adjacent positive-block gate

Retain the preceding zero epoch's overshoot coordinate

\[
A=n+4-2e.
\]

Then the returned residue satisfies the exact parent equation

\[
\boxed{m+3-f=2^kA.} \tag{83.1}
\]

In particular,

\[
\boxed{f\equiv m+3\pmod{2^k}.} \tag{83.2}
\]

The parity condition \(A\equiv n\pmod2\), with \(n=m-k-1\), lifts this
by one bit:

\[
\boxed{
f\equiv m+3-2^k(m-k-1)\pmod{2^{k+1}}.
} \tag{83.3}
\]

The intervening zero-only run and the next positive block also force

\[
\boxed{
\frac{m+r+3}{2^{r+2}}
<f\le
\frac{m-V+r}{2^{r+1}}.
} \tag{83.4}
\]

### Proof

At the returned zero epoch, Lemma 53 gives

\[
A'=m+4-2f=2^{k+1}A-(m+2).
\]

Rearranging proves

\[
2(m+3-f)=2^{k+1}A,
\]

which is (83.1), hence (83.2). Lemma 53 gives \(A\equiv n\pmod2\).
Substitute \(n=m-k-1\) into (83.1) modulo \(2^{k+1}\) to obtain
(83.3).

If \(r=0\), zero-epoch validity gives \(2f\le m-V\), which is the upper
bound in (83.4). If \(r\ge1\), the last zero-only block begins with residue
\(2^{r-1}f\) and width \(m-V+r-1\). Its return condition is

\[
2^{r+1}f\le m-V+r.
\]

This is again the upper bound. The next block is positive exactly when the
zero step from \((m+r,V,2^rf)\) is followed by a wrap. By Lemma 53, or
directly from the safe-map threshold, this is

\[
2^{r+2}f>m+r+3,
\]

which is the strict lower bound. \(\square\)

## Corollary 84: unique-state or short-gap dichotomy

For fixed \(m,V,k,r\), define the admissible gate

\[
\mathcal F=
\left\{
x\in\mathbb Z:
\begin{array}{l}
x\equiv m+3-2^k(m-k-1)\pmod{2^{k+1}},\\[2pt]
(m+r+3)/2^{r+2}<x\le(m-V+r)/2^{r+1},\\[2pt]
V-k+4\le(m+3-x)/2^k\le m-k+1
\end{array}
\right\}.
\]

Then \(\mathcal F\) is exactly the set of locally valid returned residues
with these fixed counters. In particular \(f\in\mathcal F\), and

\[
\boxed{
|\mathcal F|
\le
\left\lceil
\frac{G+r-3}{2^{k+r+3}}
\right\rceil.
} \tag{84.1}
\]

Consequently every adjacent pair of positive blocks has one of two forms:

1. **unique gate:** if
   \[
   2^{k+r+3}>G+r-3,
   \]
   then \(f\), and hence the preceding zero epoch, is uniquely determined;
2. **short combined gap:** if at least two gate values are admissible, then
   \[
   \boxed{2^{k+r+3}<G+r-3.} \tag{84.2}
   \]

### Proof

The interval in (83.4) has exact length

\[
\frac{2(m-V+r)-(m+r+3)}{2^{r+2}}
=\frac{G+r-3}{2^{r+2}}.
\]

The lifted congruence has spacing \(2^{k+1}\). The parent-coordinate bounds
in the definition of \(\mathcal F\) are Lemma 53's
\(V-k+4\le A\le m-k+1\), after using (83.1); they can only remove
candidates.

Conversely, take \(x\in\mathcal F\), put
\[
A_x=\frac{m+3-x}{2^k},\qquad
n=m-k-1,\qquad U=V-k,
\]
and define \(e=(n+4-A_x)/2\). The lifted congruence makes \(e\) integral,
and the parent bounds make \((n,U,e)\) a valid zero epoch. Equation (83.1)
gives
\[
2^kA_x=m+3-x<m+3=n+k+4.
\]
Thus the \((k-1)\)-st stopping test still fails. The interval makes
\((m,V,x)\) a valid zero epoch: its upper endpoint implies
\(2x\le m-V\). Hence
\(2^{k+1}A_x=2(m+3-x)\ge m+4=n+k+5\); Lemma 53 therefore gives exactly
\(k\) wraps and that returned epoch. For \(r>0\), the upper endpoint at the
last zero-only block implies every earlier return condition by backward
induction. The strict lower endpoint makes the following block positive.
Thus \(\mathcal F\) is exact.

A half-open interval of length \(D\) contains at most
\(\lceil D/2^{k+1}\rceil\) points of the lifted class, proving (84.1).
If the displayed ratio is below one, the nonempty gate contains exactly one
value. Equation (83.1) then determines \(A\), hence
\(e=(m-k+3-A)/2\). A half-open interval containing two points spaced by
\(2^{k+1}\) must have length strictly greater than that spacing, which gives
(84.2). \(\square\)

## Significance and limitation

Lemma 83 is an exact compatibility law for arbitrary adjacent positive
safe-map blocks. Corollary 84 says that a long zero-only separation cannot
retain multiple possible return states unless the state gap \(G\) is
exponentially large in \(k+r\). Unique gates remain arithmetically possible,
so the dichotomy is not a contradiction.
