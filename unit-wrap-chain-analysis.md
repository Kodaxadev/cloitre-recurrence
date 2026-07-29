# Persistent unit-wrap gate chains

## Scope

This note uses the unit-wrap coordinates and exact uniqueness test from
[unit-wrap-gate-analysis.md](unit-wrap-gate-analysis.md). It classifies
persistent use of the parent boundary and derives the scale forced on a
hypothetical infinite all-unit, all-unique chain. It does not cover longer
wrap blocks or nonunique gates and does not prove termination.

## Lemma 87 (three parent-boundary starts are terminal)

Consider three consecutive unit-wrap positive-block starts
\((n_i,D_i,s_i)\), for \(i=0,1,2\), and let \(r_i\) be the zero-only gap
from start \(i\) to start \(i+1\). If

\[
s_i>D_i-7\qquad(i=0,1,2), \tag{87.1}
\]

then the coordinates are forced:

\[
\begin{array}{c|ccc}
i&n_i&D_i&s_i\\ \hline
0&12&8&5\\
1&14&8&3\\
2&17&9&4
\end{array}
\qquad(r_0,r_1)=(0,1). \tag{87.2}
\]

The third start is \((n,U,e)=(17,4,6)\). Its unit-wrap block returns to
\((19,5,4)\), and the safe map terminates after the following zero step.
Consequently an infinite unit-wrap path cannot have three consecutive starts
in the parent boundary layer.

### Proof

Put

\[
\delta_i=D_i-s_i.
\]

Equations (85.1) and (87.1) give
\(\delta_i\in\{3,4,5,6\}\). Since \(n_i\equiv D_i\pmod2\) and
\(s_i\equiv1-n_i\pmod4\), every \(\delta_i\) is odd, hence

\[
\delta_i\in\{3,5\}. \tag{87.3}
\]

For one transition, write \(r=r_i\) and \(a=2^{r+2}\). From (85.2),

\[
n_i=(a-1)D_i-a\delta_i-2r-5+\delta_{i+1}. \tag{87.4}
\]

Reduction modulo \(4\) also gives

\[
\delta_{i+1}=
\begin{cases}
\delta_i,&r_i\ \text{odd},\\
8-\delta_i,&r_i\ \text{even}.
\end{cases} \tag{87.5}
\]

Apply (87.4) to the first two transitions. Put
\(r=r_0\), \(r'=r_1\), \(a=2^{r+2}\), and \(a'=2^{r'+2}\). Eliminating
\(n_1=n_0+r+2\) and \(D_1=D_0+r\) gives

\[
\begin{aligned}
(a-a')D_0={}&a'r+a\delta_0-(a'+1)\delta_1\\
             &-2r'-2+\delta_2. \tag{87.6}
\end{aligned}
\]

We solve this equation in nonnegative \(r,r'\), using (87.3)--(87.5).

If \(r=r'\), the right side of (87.6) is nonzero. For odd \(r\) it is
\(r(a-2)-2>0\). For even \(r\), the two possible values are

\[
a(r-2)-2r-4,\qquad a(r+2)-2r,
\]

neither of which vanishes for even \(r\ge0\).

Suppose \(r>r'\). Reduction of (87.6) modulo \(a'\) forces

\[
a'\mid\delta_2-\delta_1-2r'-2.
\]

Using (87.5), the nonzero absolute value on the right is smaller than \(a'\)
unless \(r'=0\). With \(r'=0\), write \(D_0=\delta_0+J\). The four parity
and deficit cases give

\[
J\in
\left\{
\frac r{2^r-1},
\frac{r-1}{2^r-1},
\frac{r-3}{2^r-1},
\frac{r+2}{2^r-1}
\right\}. \tag{87.7}
\]

The only positive integral possibility is \(r=1,\delta_0=3,J=1\), but
(87.4) then gives \(n_0=0<D_0\), so it is not a valid state.

Finally suppose \(r<r'\). Set \(d=r'-r\), \(M=2^d-1\), and

\[
t=\frac{\delta_1+2r'+2-\delta_2}{2^{r+2}}.
\]

Divisibility in (87.6) makes \(t\) integral, and rearrangement gives

\[
D_0=\delta_1-r+
\frac{t-(r+\delta_0-\delta_1)}{M}. \tag{87.8}
\]

If \(r\ge2\), validity \(D_0\ge\delta_0+1\) would force \(t\ge M\), whereas

\[
t\le\frac{r+d+2}{2^{r+1}}<2^d-1=M.
\]

The final inequality holds at \(r=2,d=1\), and increasing either integer
increases the right side faster than the numerator on the left.

If \(r=1\), (87.5) gives \(\delta_1=\delta_0\); validity would force
\(t\ge2M+1\), while \(t\le(r'+2)/4<2^{r'}-1=2M+1\).

Thus \(r=0\). If \((\delta_0,\delta_1)=(5,3)\), validity in (87.8) would
require \(t-2\ge3(2^{r'}-1)\), whereas
\(t\le(r'+2)/2<3(2^{r'}-1)+2\). If
\((\delta_0,\delta_1)=(3,5)\), then

\[
t=\lfloor r'/2\rfloor+1,\qquad
2^{r'}-1\mid t+2.
\]

For \(r'=1\) this gives \(D_0=8\); for \(r'=2\), \(3\nmid4\); and for
\(r'\ge3\), \(0<t+2<2^{r'}-1\). Thus \(r'=1\) is the only solution.
Equation (87.4) and (85.2) now give exactly (87.2).

In raw safe coordinates, the last start follows

\[
(17,4,6)\to(18,4,12)\to(19,5,4)\to(20,5,8).
\]

At the last state, \(15<2e=16\le n+2=22\), so it lies in the terminating
middle strip. This proves the claim.

## Corollary 88 (non-short unique gates are isolated)

In any chain of \(L\) consecutive unique unit-wrap gates, at least
\(\lfloor L/2\rfloor\) gates satisfy

\[
\boxed{D+r-3<2^{r+5}.} \tag{88.1}
\]

In particular, for each such gate,

\[
r>\log_2(D+r-3)-5. \tag{88.2}
\]

### Proof

Put \(H=2^{r+4}\). Every unique gate satisfies the lower-boundary condition

\[
s'\le H. \tag{88.3}
\]

If its parent boundary is inactive, Corollary 86 also gives

\[
s'+H>D+r-3,
\]

so (88.1) follows. Now suppose instead that a unique gate fails (88.1).
Writing \(D'=D+r\), failure and (88.3) imply

\[
D'\ge2H+3,\qquad
\delta'=D'-s'\ge H+3>7. \tag{88.4}
\]

Thus the parent boundary is inactive at the successor. If that successor
has another unique gate, the preceding argument forces (88.1) there.
Failures of (88.1) therefore cannot be consecutive. At least one gate in
each disjoint pair satisfies it, proving the count. Taking base-two
logarithms gives (88.2).

This is a quantitative obstruction, not a termination proof. The lower bound
on \(r\) remains compatible with quotient growth on the \(n/\log n\) scale.

## Corollary 89 (scale of an infinite unique unit-wrap chain)

Suppose an infinite safe path consists of unit-wrap positive blocks and every
adjacent-block gate is unique. Index its positive-block starts by \(j\), with
coordinates \((n_j,U_j,D_j,s_j)\). Then

\[
\boxed{
\liminf_{j\to\infty}\frac{D_j}{j\log_2j}\ge\frac12.
} \tag{89.1}
\]

Moreover,

\[
\boxed{
1\le
\liminf_{j\to\infty}\frac{U_j\log_2n_j}{n_j}
\le
\limsup_{j\to\infty}\frac{U_j\log_2n_j}{n_j}
\le2.
} \tag{89.2}
\]

### Proof

Every unit-wrap block increments \(U\) once, while (85.2) gives

\[
U_j=U_0+j,\qquad
D_{j+1}=D_j+r_j,\qquad
n_j=D_j+2U_j. \tag{89.3}
\]

First, \(D_j\to\infty\). Otherwise its nonnegative integer increments would
eventually have \(r_j=0\). But then \(s_j\le D_j-3\) would stay bounded while
the next-positive condition \(4s_j>n_j+5\) would fail as
\(n_j=D_j+2U_j\to\infty\).

Apply Corollary 88 to the two gates beginning at indices \(2t,2t+1\).
For one of them, monotonicity of \(D\) and (88.2) give

\[
D_{2t+2}-D_{2t}
>
\log_2(D_{2t}-3)-5. \tag{89.4}
\]

For every \(\varepsilon>0\), the right side is at least
\((1-\varepsilon)\log_2D_{2t}\) for all large \(t\). The resulting sequence
eventually increases by more than one, so \(D_{2t}\gg t\). Summing (89.4)
and using

\[
\sum_{u\le t}\log_2u=t\log_2t-O(t)
\]

gives

\[
\liminf_{t\to\infty}
\frac{D_{2t}}{t\log_2t}\ge1.
\]

Monotonicity between even indices proves (89.1).

The first inequality in (89.2) is Theorem 45 along this subsequence. For the
last, (89.1), (89.3), and the eventual decrease of
\(\log_2x/x\) imply

\[
\limsup_{j\to\infty}
\frac{(U_0+j)\log_2n_j}{n_j}\le2.
\]

The middle inequality is tautological.

The constants \(1\) and \(2\) do not contradict one another. Thus this
corollary confines an infinite unique unit-wrap chain to a critical
near-\(n/\log n\) quotient regime but does not exclude it.

## Theorem 90 (critical-scale rigidity)

Under the hypotheses of Corollary 89, every sufficiently late gate satisfies

\[
\boxed{D_j+r_j-3<2^{r_j+5}.} \tag{90.1}
\]

Moreover, the two critical ratios have exact limits:

\[
\boxed{
\frac{D_j}{j\log_2j}\longrightarrow1,
\qquad
\frac{U_j\log_2n_j}{n_j}\longrightarrow1.
} \tag{90.2}
\]

### Proof

Let \(a=2^{r+2}\), so \(2^{r+5}=8a\), and put
\(\delta=D-s\). From the transition in Lemma 85,

\[
\delta'
=2U-(a-2)D+a\delta+2r+5. \tag{90.3}
\]

Suppose a unique gate fails (90.1). The child-boundary alternative in
Corollary 86 would imply (90.1), so the parent boundary must be active.
Thus \(\delta\in\{3,5\}\). Failure also gives

\[
D\ge8a-r+3. \tag{90.4}
\]

Since \(\delta'\ge3\), equation (90.3) yields

\[
2U\ge(a-2)D-5a-2r-2. \tag{90.5}
\]

The lower bound (90.4) implies

\[
(a-3)D\ge5a+2r+2. \tag{90.6}
\]

For \(r=0\), its two sides are at least \(35\) and \(22\). For \(r\ge1\),
\(r\le a/4\), so (90.4) gives \(D>7a\), while \(a-3\ge5\); this is more
than enough for (90.6). Combining (90.5)--(90.6) gives

\[
U\ge D/2. \tag{90.7}
\]

But Corollary 89 and \(U_j=U_0+j\) imply \(U_j/D_j\to0\). Hence only
finitely many gates can fail (90.1).

For every sufficiently late \(j\), (90.1) gives

\[
D_{j+1}-D_j=r_j>\log_2(D_j-3)-5. \tag{90.8}
\]

The same summation used in Corollary 89, now at every gate rather than once
per pair, proves

\[
\liminf_{j\to\infty}\frac{D_j}{j\log_2j}\ge1. \tag{90.9}
\]

Together with \(U_j=U_0+j\), \(n_j=D_j+2U_j\), and the eventual decrease of
\(\log_2x/x\), this gives

\[
\limsup_{j\to\infty}\frac{U_j\log_2n_j}{n_j}\le1.
\]

Theorem 45 supplies the reverse lower limit, proving the second limit in
(90.2).

Finally, (90.9) gives \(U_j/D_j\to0\), so \(n_j/D_j\to1\). The second
limit in (90.2) then implies

\[
\frac{j\log_2D_j}{D_j}\longrightarrow1.
\]

Taking logarithms shows \(\log D_j/\log j\to1\), and substitution proves
the first limit in (90.2).

This theorem forces exact critical asymptotics but still permits an aperiodic
integer trajectory at that scale.
