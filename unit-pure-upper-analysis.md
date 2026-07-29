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
