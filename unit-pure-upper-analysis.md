# Unit-block pure-upper chains

## Scope

Corollary 115 gives an exact local test for a pure-upper unit gate. This
note removes the irrelevant initial quotient, characterizes a returning
unit block without simulating its digits, and derives the asymptotic scale
of any hypothetical infinite chain made entirely from this mechanism.

The conclusion is a restriction, not a contradiction.

## Lemma 116 (quotient erasure preserves a safe digit word)

Suppose a finite or infinite safe-map path starts at
\((n_0,U_0,e_0)\). Replace its initial state by

\[
(\widetilde n_0,\widetilde U_0,\widetilde e_0)
=(n_0,0,e_0).
\]

Then the new path has exactly the same zero/wrap digit word for as long as
the original path continues, with

\[
\boxed{
\widetilde n_t=n_t,\qquad
\widetilde e_t=e_t,\qquad
\widetilde U_t=U_t-U_0.
} \tag{116.1}
\]

Consequently every finite or infinite pure-upper gate word has a
quotient-zero realization with the same block lengths, gaps, returned
residues, canonical translates, and spacings. Its parent and child defects
are increased by \(U_0\).

### Proof

The lowered initial state is valid because
\(0<e_0<n_0-U_0\le n_0\). Induct on the safe digits.

If the original digit is zero, then

\[
2e_t\le n_t-U_t
\le n_t-(U_t-U_0),
\]

so the lowered state also takes a zero digit. Both residues double and
neither wrap count changes.

If the original digit is a wrap, then \(2e_t>n_t+2\). The lowered width is
at most \(n_t\), so its zero test fails and the same wrap occurs. Both
residues subtract the same modulus \(n_t+2\), and both wrap counts increase
by one. This proves (116.1).

All gate data except the defects depend only on the common indices,
residues, and digit word. Replacing \(U_t\) by \(U_t-U_0\) increases every
defect \(n_t-U_t-2e_t\) by \(U_0\). Hence the pure-upper inequalities remain
valid. \(\square\)

## Lemma 117 (exact returning-unit state test)

Let \(n\ge2\) and \(U\ge0\) be integers, and put \(D=n-2U\). An integer
\(f\) reconstructs a valid safe state whose next positive block has
exactly one wrap and returns with residue \(f\) if and only if

\[
\boxed{
\begin{gathered}
n+3+f\equiv0\pmod4,\\
f\ge1,\qquad
f\le D-3,\qquad
4f\le n+D+2.
\end{gathered}
} \tag{117.1}
\]

The reconstructed start residue and defect are

\[
\boxed{
e=\frac{n+3+f}{4},\qquad
d=\frac{D-3-f}{2}.
} \tag{117.2}
\]

### Proof

At the start, a zero digit is equivalent to

\[
2e\le n-U.
\]

After that zero, one wrap occurs exactly when \(4e>n+3\), and its returned
residue is

\[
f=4e-n-3.
\]

Thus \(f\ge1\), while the initial zero condition becomes \(f\le D-3\).
After the wrap the state is \((n+2,U+1,f)\). It returns to a zero epoch
exactly when

\[
2f\le n+1-U,
\]

which is \(4f\le n+D+2\). Solving the displayed definition of \(f\) for
\(e\), and then substituting into \(d=n-U-2e\), gives (117.2).

Conversely, (117.1) makes (117.2) integral and reverses each inequality.
It therefore reconstructs the zero, the single wrap, and the following
zero test exactly. \(\square\)

## Theorem 118 (two-gap critical scale)

Suppose a hypothetical infinite safe tail consists entirely of unit
positive blocks and every gate is pure-upper. Index its block starts by
\(i\ge0\), and let \(n_i,U_i,D_i,f_i,r_i\) have the meanings of
Corollary 114. Then, for every \(i\ge1\),

\[
\boxed{
n_i<2^{r_{i-1}+r_i+6}.
} \tag{118.1}
\]

If \(J\to\infty\), then

\[
\boxed{
\frac12
\le
\liminf_{J\to\infty}\frac{n_J}{J\log_2J}
\le
\limsup_{J\to\infty}\frac{n_J}{J\log_2J}
\le1.
} \tag{118.2}
\]

The accumulated quotient lies in the complementary critical window

\[
\boxed{
1
\le
\liminf_{J\to\infty}\frac{U_J\log_2n_J}{n_J}
\le
\limsup_{J\to\infty}\frac{U_J\log_2n_J}{n_J}
\le2.
} \tag{118.3}
\]

### Proof

Pure upper at gate \(i-1\) and Corollary 115 give

\[
f_i\le2^{r_{i-1}+4}.
\]

Rearranging Corollary 114 at gate \(i\) gives

\[
n_i=2^{r_i+2}f_i-f_{i+1}-r_i-5
<2^{r_i+2}f_i.
\]

Combining the two inequalities proves (118.1).

Put

\[
S_J=\sum_{i=0}^{J-1}r_i.
\]

Since \(U_J=U_0+J\), the index recurrence gives

\[
n_J=n_0+2J+S_J. \tag{118.4}
\]

Taking logarithms in (118.1), then summing for
\(1\le i\le J-1\), yields

\[
2S_J
>
\sum_{i=1}^{J-1}\log_2n_i-6(J-1). \tag{118.5}
\]

Here \(n_i\ge2i\), so

\[
\sum_{i=1}^{J-1}\log_2n_i
\ge
(J-1)+\log_2((J-1)!)
=J\log_2J-O(J).
\]

Equations (118.4)--(118.5) give

\[
n_J\ge\frac12J\log_2J-O(J). \tag{118.6}
\]

In the other direction, Corollary 115 gives

\[
2^{r_i+4}\le D_{i+1}-4<n_{i+1}.
\]

Since the start indices increase,

\[
S_J\le J\log_2n_J-4J.
\]

Together with (118.4), this gives

\[
n_J\le J\log_2n_J+O(J). \tag{118.7}
\]

Writing \(y_J=n_J/J\) in (118.7) gives

\[
y_J\le\log_2J+\log_2y_J+O(1).
\]

For \(y_J\ge4\), the bound \(\log_2y_J\le y_J/2\) first gives
\(y_J\le2\log_2J+O(1)\); hence \(y_J=O(\log J)\). Substitution back into
(118.7) gives

\[
n_J\le J\log_2J+O(J\log_2\log_2J).
\tag{118.8}
\]

Equations (118.6) and (118.8) prove (118.2). They also imply
\(\log n_J/\log J\to1\). Finally,

\[
\frac{U_J\log_2n_J}{n_J}
=
\frac{U_J}{J}\,
\frac{\log_2n_J}{\log_2J}\,
\left(\frac{n_J}{J\log_2J}\right)^{-1}.
\]

The first two factors tend to one, so taking reciprocal liminf and limsup
in (118.2) proves (118.3). \(\square\)

## Consequence and limitation

An all-unit pure-upper tail cannot have bounded gaps. More sharply, every
adjacent pair contains a gap of size at least

\[
\frac12\log_2n_i-3.
\]

Its block starts must live between the half-critical and critical
\(J\log J\) scales. This matches, rather than contradicts, the universal
quotient-growth theorem. Longer positive blocks and mixtures of lower and
upper nonuniqueness also remain possible.

## Lemma 119 (three-residue compatibility)

For any three consecutive unit positive blocks in Corollary 114,

\[
\boxed{
2^{r_i+2}f_i+f_{i+2}+r_{i+1}+2
=
\left(2^{r_{i+1}+2}+1\right)f_{i+1}.
} \tag{119.1}
\]

If \(m_i=\min(r_i,r_{i+1})\), then

\[
\boxed{
f_{i+2}\equiv f_{i+1}-r_{i+1}-2
\pmod {2^{m_i+2}}.
} \tag{119.2}
\]

The first gap is also recovered exactly from adjacent states:

\[
\boxed{
r_i+2
=
v_2(n_{i+1}+3+f_{i+1})-v_2(f_i).
} \tag{119.3}
\]

### Proof

Corollary 114 at indices \(i\) and \(i+1\) gives

\[
2^{r_i+2}f_i-f_{i+1}=n_i+r_i+5
\]

and

\[
2^{r_{i+1}+2}f_{i+1}-f_{i+2}
=n_i+r_i+r_{i+1}+7.
\]

Subtracting proves (119.1). Both power terms in (119.1) vanish modulo
\(2^{m_i+2}\), proving (119.2). Finally, the first recurrence and
\(n_{i+1}=n_i+r_i+2\) give

\[
n_{i+1}+3+f_{i+1}=2^{r_i+2}f_i.
\]

Taking 2-adic valuations proves (119.3). \(\square\)

## Corollary 120 (two-gate ladder headroom)

For two consecutive pure-upper unit gates \(i\) and \(i+1\),

\[
\boxed{f_{i+1}\ge5.} \tag{120.1}
\]

More precisely,

\[
\boxed{
(f_{i+1}-4)n_{i+2}
\ge
2f_{i+1}U_{i+2}+4f_{i+1}+12+4f_{i+2}.
} \tag{120.2}
\]

### Proof

The identity preceding (119.3), applied at \(i+1\), is

\[
n_{i+2}+3+f_{i+2}
=2^{r_{i+1}+2}f_{i+1}.
\]

Corollary 115 at gate \(i+1\) gives

\[
4\cdot2^{r_{i+1}+2}
\le D_{i+2}-4=n_{i+2}-2U_{i+2}-4.
\]

Substitute the first equality into the second and multiply by
\(f_{i+1}>0\). Rearrangement gives (120.2). Its right-hand side is
positive, so \(f_{i+1}-4>0\), proving (120.1). \(\square\)

## Theorem 121 (growing-modulus or fixed-ladder dichotomy)

Every hypothetical infinite all-unit pure-upper tail satisfies exactly one
of the following exhaustive alternatives.

1. The gaps satisfy \(r_i\to\infty\). Consequently the modulus
   \(2^{\min(r_i,r_{i+1})+2}\) in (119.2) tends to infinity.
2. There are fixed integers \(R\ge0\) and
   \(5\le a\le2^{R+4}\), and infinitely many indices \(i_j\), such that

   \[
   \boxed{
   r_{i_j}=R,\qquad f_{i_j+1}=a,
   } \tag{121.1}
   \]

   \[
   r_{i_j-1}\longrightarrow\infty,\qquad
   r_{i_j+1}\longrightarrow\infty,
   \tag{121.2}
   \]

   the renewal starts lie in one fixed residue class,

   \[
   \boxed{
   n_{i_j+1}+3+a=2^{R+2}f_{i_j},
   \qquad
   n_{i_j+1}\equiv-a-3\pmod {2^{R+2}},
   } \tag{121.3}
   \]

   and the states after the following large gap lie on one fixed dyadic
   ladder:

   \[
   \boxed{
   n_{i_j+2}+3+f_{i_j+2}
   =a\,2^{r_{i_j+1}+2}.
   } \tag{121.4}
   \]

### Proof

If \(r_i\to\infty\), the first alternative and its modulus claim follow
from Lemma 119.

Otherwise some finite set of gap values occurs infinitely often. Passing
to a subsequence fixes one such value \(r_{i_j}=R\). The two-gap bound
(118.1), applied at \(i_j\) and \(i_j+1\), gives

\[
r_{i_j-1}>\log_2n_{i_j}-R-6,\qquad
r_{i_j+1}>\log_2n_{i_j+1}-R-6.
\]

The start indices diverge, proving (121.2). Pure upper at gate \(i_j\)
gives \(1\le f_{i_j+1}\le2^{R+4}\), while Corollary 120 gives
\(f_{i_j+1}\ge5\). A second subsequence therefore fixes this returned
residue at some \(a\), proving (121.1).

Applying the exact identity

\[
n_{i+1}+3+f_{i+1}=2^{r_i+2}f_i
\]

at \(i=i_j\) proves (121.3), and applying it at \(i=i_j+1\) proves
(121.4). The two cases are mutually exclusive and exhaust whether \(r_i\)
tends to infinity. \(\square\)

## New frontier

The unit pure-upper branch is now reduced to two arithmetic mechanisms:
a growing-modulus congruence chain, or recurrent visits to one fixed
dyadic ladder separated by logarithmic gaps. Neither mechanism is excluded.
The next proof target is to show that the exact state window cannot support
either mechanism indefinitely.
