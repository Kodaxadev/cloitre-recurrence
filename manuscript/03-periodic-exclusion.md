# 3. Exclusion of eventually periodic quotient dynamics

Assume that the digit word \(a_n=q_{n+1}-q_n\) is periodic from some
index \(N\), with period \(p\). Write one period as
\((a_0,\ldots,a_{p-1})\), and define

\[
M=2^p-1,\quad
C=\sum_{j=0}^{p-1}2^{p-1-j}a_j,\quad
D=\sum_{j=0}^{p-1}2^{p-1-j}a_j(j+2). \tag{3.1}
\]

## Theorem 25 (periodic-word integrality)

If this word occurs on an admissible infinite orbit, then

\[
A=\frac CM,\qquad z=pA\in\mathbb Z,
\]

and the phase state is exactly

\[
e_N=AN+B,\qquad B=\frac{z+D}{M}. \tag{3.2}
\]

An integer phase \(N\) can satisfy (3.2) only if

\[
\gcd(C,M)\mid(z+D). \tag{3.3}
\]

### Proof

Unrolling (1.2) through one period gives

\[
e_{N+p}=2^pe_N-CN-D.
\]

An affine particular solution \(E(N)=AN+B\) forces (3.2). The difference
between any other solution and \(E\) is multiplied by \(2^p\) every
period, whereas admissibility gives \(e_n=O(n)\). That difference must
therefore vanish identically.

Both \(e_N\) and \(e_{N+p}\) are integers, so their difference
\(pA=z\) is integral. Equation (3.2) becomes the congruence

\[
CN\equiv-(z+D)\pmod M,
\]

which is soluble only under (3.3). \(\square\)

Let

\[
\mu=\frac1p\sum_{j=0}^{p-1}a_j
\]

be the quotient slope, and let \(A_j\) be the slope of \(e\) at phase
\(j\). Then

\[
A_{j+1}=2A_j-a_j,\qquad
-\mu\le A_j\le1-\mu,\qquad
\frac1p\sum_jA_j=\mu. \tag{3.4}
\]

## Theorem 32 (boundary reduction)

Suppose the periodic word is nonzero and some \(A_j\) has reduced
denominator \(d>1\). Then:

1. \(d\) is odd;
2. the fractional numerators form a doubling cycle modulo \(d\) of length
   \(L=\operatorname{ord}_d(2)<d\);
3. \(\mu=(d-y)/d\) for a residue \(y\) in that cycle.

### Proof

Theorem 25 makes \(d\) divide \(2^p-1\), hence \(d\) is odd. Reduction of
\(A_{j+1}=2A_j-a_j\) modulo one sends the reduced numerator \(x\) to
\(2x\bmod d\). Since \(\gcd(x,d)=1\), the resulting cycle has length
\(L=\operatorname{ord}_d(2)\), with \(0<L<d\).

For a residue \(x\), the only lifts in the window (3.4) are

\[
\frac xd\quad\text{if}\quad\mu\le\frac{d-x}{d},
\qquad
\frac xd-1\quad\text{if}\quad\mu\ge\frac{d-x}{d}. \tag{3.5}
\]

If \(\mu\) differs from every threshold in (3.5), every lift is unique.
The lifted slopes and their digits then repeat after \(L\) steps.
Theorem 25 applied to that shorter period makes \(LA_j\) integral, which
would require \(d\mid L\), contradicting \(0<L<d\). Thus \(\mu\) is one
of the boundary values. \(\square\)

Rotate the fractional cycle so its boundary residue is last. Let
\(B=2^L\), and let \(a_0,\ldots,a_{L-1}\) be the digit block when the
boundary takes its positive lift. Put

\[
C=\sum_{j=0}^{L-1}a_j2^{L-1-j},\qquad
E=\sum_{j=0}^{L-1}a_j2^{L-1-j}(j+2). \tag{3.6}
\]

For \(R\) repeated blocks, let \(T\) be the set of blocks in which the
boundary takes its negative lift, and put

\[
G=\frac{B^R-1}{d},\qquad
\alpha=\frac{d[E(B-1)+LC]}{(B-1)^2}. \tag{3.7}
\]

## Theorem 36 (block subset equation)

Phase integrality requires, for some integer \(J\),

\[
2\sum_{t\in T}B^t=(\alpha-J)G. \tag{3.8}
\]

### Proof

The positive block has phase slope \(C/(B-1)\). In block \(\ell\), its
contribution to the phase numerator of Theorem 25 is

\[
B^{R-1-\ell}[E+LC\ell].
\]

Summing the geometric progression and its derivative, and including the
integer phase-slope numerator, cancels the terms proportional to \(R\).
The all-positive phase numerator is exactly \(\alpha G\).

Changing the final boundary lift decreases it by one. In the associated
digit block, the preceding digit increases by one and the final digit
decreases by two. Their absolute-index terms cancel, changing the phase
numerator by \(-2B^{R-1-\ell}\). Summing over the selected blocks and
reindexing gives

\[
\alpha G-2\sum_{t\in T}B^t.
\]

Theorem 25 requires divisibility by \(G\), which is (3.8). \(\square\)

## Theorem 38 (no nonzero eventually periodic digit orbit)

No admissible integer orbit has an eventually periodic, nonzero
quotient-change word.

### Proof

First consider integral phase slopes. If \(0<\mu\le1/2\), the window
\([-\mu,1-\mu]\) contains only the integer \(0\), contradicting the mean
identity in (3.4). If \(\mu=0\), the same identity forces every phase
slope and every digit to be zero. Thus a nonzero word has a nonintegral
phase slope.

Theorem 32 supplies an odd denominator \(d>1\) and a boundary family. If
every boundary lift has the same sign, the lifted slope word has period
\(L<d\), contradicting Theorem 25 as in Theorem 32. Hence
\(T\) is nonempty and proper, and \(R\ge2\).

Put \(H=B-1\) and \(S_R=1+B+\cdots+B^{R-1}\). Since
\(L=\operatorname{ord}_d(2)\), \(d\mid H\). If the first slope is \(s/d\),
then \(C=sH/d\). Substitution into (3.7) changes (3.8), after
multiplication by \(d\), into

\[
2d\sum_{t\in T}B^t=F S_R,\qquad
F=dE+Ls-JH. \tag{3.9}
\]

Because \(T\) is nonempty and proper,

\[
0<F<2d. \tag{3.10}
\]

Let \(\epsilon_0,\epsilon_1\in\{0,1\}\) be the first two base-\(B\)
digits of the subset. Reducing (3.9) modulo \(B\) gives

\[
2d\epsilon_0\equiv F\pmod B.
\]

Since \(d<B\) and \(0<F<2d<2B\), either

\[
\epsilon_0=0,\ F=B,
\qquad\text{or}\qquad
\epsilon_0=1,\ F=2d-B.
\]

In the first case, subtracting the constant digit and dividing by \(B\)
makes the next digit satisfy

\[
2d\epsilon_1\equiv1\pmod B,
\]

impossible because \(2d\epsilon_1\) and \(B\) are even. In the second
case, the next digit requires \(B\) to divide either \(B-2d+1\) or
\(B+1\); both are odd while \(B\) is even. This contradiction proves the
theorem. \(\square\)

The finite denominator-\(501\) certificate in the supplement is an
independent finite check of the boundary machinery. It is not used to
extend Theorem 38 beyond a computational range; the two-digit argument
above is the claimed universal step.
