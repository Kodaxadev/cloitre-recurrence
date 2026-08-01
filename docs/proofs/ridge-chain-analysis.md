# Compatibility of consecutive unit-terminal ridges

Proposition 66 shows that a single valid post-down ridge can have a
vanishing up-step fraction. This note tests whether its exact mechanism can
repeat indefinitely. It cannot: three consecutive ridges cannot all consist
of an initial up-run followed by a terminal zero-run whose last up-step
creates \(e=-1\).

## Definition

Call a segment between consecutive down-steps a **unit-terminal ridge** if
its intervening digit word is

\[
1^K0^z,\qquad K\ge1,
\]

and the \(K\)-th up-step leaves \(e=-1\). Let \(N\) be its post-down start
index, \(Q=q_N\), and \(h=N-Q-e_N\), as in Lemma 62.

## Lemma 67: unit-terminal compatibility

For a unit-terminal ridge,

\[
N=2^K(Q+h+3)-K-4. \tag{67.1}
\]

Put \(S=Q+K\). Then

\[
z=\lfloor\log_2S\rfloor. \tag{67.2}
\]

At the next down-step, the following post-down ridge starts with parameters

\[
N'=N+K+z+1,\qquad
Q'=S-1,\qquad
h'=2^{z+1}-S, \tag{67.3}
\]

and consequently

\[
\boxed{\displaystyle Q'+h'+3=2^{z+1}+2.} \tag{67.4}
\]

### Proof

Before the up-run, the exact coordinate is \(e_N=N-Q-h\). Iterating \(K\)
up-steps gives

\[
e_{N+K}=N+K+3-2^K(Q+h+3).
\]

This equals \(-1\) exactly when (67.1) holds. The quotient after the up-run
is \(S\). Lemma 63 with terminal magnitude \(v=1\) gives (67.2) and the
next down gap \(h'=2^{z+1}-S\). The index advances across \(K+z\)
intervening digits and the down-step itself, proving the first formula in
(67.3). A down-step lowers the quotient by one, proving the second.
Substitution gives (67.4). \(\square\)

## Lemma 68: incompatible increasing dyadic scales

Let \(J,H\ge1\) and \(1\le z\le z'\). Then

\[
2^J(2^{z+1}+2)+z'+H+1
\ne
2^H(2^{z'+1}+2). \tag{68.1}
\]

### Proof

Write \(A_t=2^{t+1}+2\).

If \(H>J\), the function

\[
G(H,z')=2^HA_{z'}-(z'+H+1)
\]

increases strictly in both arguments. Hence

\[
G(H,z')\ge G(J+1,z)
>2^JA_z,
\]

where the last inequality is \(2^JA_z>z+J+3\), immediate for
\(J,z\ge1\). This contradicts (68.1).

If \(H=J\), equality would give

\[
2^J(A_{z'}-A_z)=z'+J+1.
\]

The case \(z'=z\) is impossible. For \(z'>z\), the left side minus the
right side increases with \(z'\), and at \(z'=z+1\) it is already positive
because \(2^{J+z+1}>z+J+2\).

Finally suppose \(H<J\) and put \(p=J-H\ge1\). Equality would imply

\[
2^H(A_{z'}-2^pA_z)=z'+H+1>0.
\]

Therefore \(z'\ge z+p+1\). For such \(z'\), the left side minus the right
side increases with \(z'\). At its smallest possible value,

\[
A_{z+p+1}-2^pA_z
=2^{p+1}(2^z-1)+2,
\]

and multiplication by \(2^H\) makes this at least
\(2^{J+z}>z+J+2\), the corresponding right side. This is again a
contradiction. \(\square\)

## Theorem 69: no three consecutive unit-terminal ridges

Once the terminal quotient of the first segment is at least two, an orbit
cannot contain three consecutive unit-terminal ridges.

### Proof

Suppose three such segments exist. Let their up-run lengths be
\(K_1,K_2,K_3\), and let the first two terminal zero counts be \(z_1,z_2\).
The hypothesis makes \(z_1\ge1\).

If \(S_j\) is the quotient after the \(j\)-th up-run, (67.3) gives

\[
S_2=(S_1-1)+K_2\ge S_1.
\]

Thus \(z_2=\lfloor\log_2S_2\rfloor\ge z_1\).

Apply (67.1) to the second segment and (67.4) to its parent. Advancing to
the third parent with (67.3), then applying (67.1) to the third segment,
forces

\[
2^{K_2}(2^{z_1+1}+2)+z_2+K_3+1
=2^{K_3}(2^{z_2+1}+2).
\]

This contradicts Lemma 68 with
\((J,H,z,z')=(K_2,K_3,z_1,z_2)\). \(\square\)

## Scope

Theorem 69 closes only the exact mechanism in Proposition 66. It does not
exclude a chain whose positive portion contains interspersed zero- and
up-steps, or whose sign-changing final up-step creates \(e=-v\) with
\(v>1\). Those more general inter-segment compatibility problems remain
open.

## Lemma 70: arbitrary terminal magnitude

Call a ridge **pure** if its intervening word is \(1^K0^z\), \(K\ge1\).
Suppose its last up-step creates \(e=-v\). With

\[
A=Q+h+3,\qquad S=Q+K,
\]

its parameters satisfy

\[
1\le v\le S,\qquad
N=2^KA-K-3-v,\qquad
z=\left\lfloor\log_2\frac Sv\right\rfloor. \tag{70.1}
\]

The next post-down ridge has

\[
\begin{aligned}
N'&=N+K+z+1,\\
Q'&=S-1,\\
h'&=2^{z+1}v-S,\\
A'=Q'+h'+3&=2^{z+1}v+2.
\end{aligned} \tag{70.2}
\]

If the next ridge is also pure, with parameters \(K',v',z'\), then

\[
\boxed{\displaystyle
2^KA+z+K'+1+v'-v=2^{K'}A'.} \tag{70.3}
\]

### Proof

The up-run formula is

\[
e_{N+K}=N+K+3-2^KA.
\]

Setting it equal to \(-v\) proves the middle identity in (70.1), while
the up threshold gives \(v\le S\). Lemma 63 gives the zero count and
terminal gap, and the down-step gives the first two updates in (70.2).
Their substitution gives the last update.

Finally,

\[
N'=2^KA+z-2-v.
\]

Applying the middle identity of (70.1) to the next pure ridge and equating
the two expressions for \(N'\) proves (70.3). \(\square\)

## Corollary 71: adjacent dyadic congruence

For consecutive pure ridges, put \(m=\min(K,K')\). Then

\[
\boxed{\displaystyle
2^m\mid z+K'+1+v'-v.} \tag{71.1}
\]

In particular, if

\[
z+K'+1+v+v'<2^m, \tag{71.2}
\]

then

\[
v'=v-z-K'-1\le v-2. \tag{71.3}
\]

### Proof

Both power-weighted terms in (70.3) are divisible by \(2^m\), proving
(71.1). Under (71.2), the absolute value of the divisible integer is
strictly smaller than \(2^m\), so it is zero. This is (71.3). \(\square\)

## Theorem 72: complexity forced on an infinite pure tail

Suppose a sublinear counterexample has infinitely many down-steps and,
from some point onward, every ridge is pure. Index those ridges by \(j\)
and use \(K_j,v_j,z_j\) as above. Put

\[
m_j=\min(K_j,K_{j+1}).
\]

Then \(m_j\to\infty\), and for infinitely many \(j\),

\[
\boxed{\displaystyle
\max\{z_j,\ K_{j+1}+1,\ v_j,\ v_{j+1}\}
\ge 2^{m_j-2}.} \tag{72.1}
\]

Thus an infinite pure-tail counterexample cannot keep its zero counts,
adjacent up-run lengths, and terminal magnitudes all subexponential in the
smaller adjacent up-run length.

### Proof

Theorem 58 forces a rebound of length tending to infinity after every late
down-step. Since a pure ridge contains no later up-step, its total up-run
length satisfies \(K_j\to\infty\), hence \(m_j\to\infty\).

Let

\[
E_j=z_j+K_{j+1}+1+v_{j+1}-v_j.
\]

Corollary 71 makes \(E_j\) divisible by \(2^{m_j}\). The equality
\(E_j=0\) implies

\[
v_{j+1}=v_j-z_j-K_{j+1}-1\le v_j-2.
\]

Positive integers cannot decrease this way on every sufficiently late
step, so \(E_j\ne0\) infinitely often. At each such index,

\[
2^{m_j}\le |E_j|
\le z_j+(K_{j+1}+1)+v_j+v_{j+1}.
\]

One of the four nonnegative summands is at least one quarter of the left
side, proving (72.1). \(\square\)

## General limitation

Arbitrary terminal magnitudes destroy all simple monotonicity visible in
the unit case. Exact valid examples have \(v,z,K\), the terminal dyadic
scale \(2^zv\), and the next width \(A'\) each moving in both directions;
pure chains of length eight already occur. Theorem 72 is therefore a
complexity obstruction, not termination. Mixed positive words remain
outside even this generalized pure-ridge map.
