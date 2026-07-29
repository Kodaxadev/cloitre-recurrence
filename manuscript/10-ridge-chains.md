# Compatibility of unit-terminal ridge chains

Call a segment between consecutive down-steps **unit-terminal** if its
intervening word is \(1^K0^z\), \(K\ge1\), and the last up-step leaves
\(e=-1\).

## Lemma 67 (unit-terminal compatibility)

At the post-down start \((N,Q,e_N)\), put \(h=N-Q-e_N\). A unit-terminal
ridge satisfies

\[
N=2^K(Q+h+3)-K-4. \tag{10.1}
\]

If \(S=Q+K\), then \(z=\lfloor\log_2S\rfloor\), and the next post-down
parameters are

\[
N'=N+K+z+1,\quad Q'=S-1,\quad h'=2^{z+1}-S. \tag{10.2}
\]

In particular,

\[
Q'+h'+3=2^{z+1}+2. \tag{10.3}
\]

Indeed, iterating the up-coordinate formula gives

\[
e_{N+K}=N+K+3-2^K(Q+h+3).
\]

Setting this equal to \(-1\) proves (10.1); Lemma 63 with \(v=1\) gives
the remaining formulas. \(\square\)

## Lemma 68 (incompatible increasing dyadic scales)

For \(J,H\ge1\) and \(1\le z\le z'\),

\[
2^J(2^{z+1}+2)+z'+H+1
\ne2^H(2^{z'+1}+2). \tag{10.4}
\]

Put \(A_t=2^{t+1}+2\). If \(H>J\), then
\(2^HA_{z'}-(z'+H+1)\) is increasing in both arguments and already
exceeds \(2^JA_z\) at \((H,z')=(J+1,z)\). If \(H=J\), subtracting the
power terms gives zero when \(z'=z\), and for \(z'>z\) the left side
grows faster than \(z'+J+1\), starting with
\(2^{J+z+1}>z+J+2\).

If \(H<J\), write \(p=J-H\). Equality would require

\[
2^H(A_{z'}-2^pA_z)=z'+H+1>0,
\]

so \(z'\ge z+p+1\). At that smallest value,

\[
A_{z+p+1}-2^pA_z=2^{p+1}(2^z-1)+2,
\]

and multiplication by \(2^H\) makes this at least
\(2^{J+z}>z+J+2\), the corresponding right side. The difference
increases thereafter. \(\square\)

## Theorem 69 (no three consecutive unit-terminal ridges)

Once the first terminal quotient is at least two, three consecutive
unit-terminal ridges are impossible.

For three alleged segments, let the last two up-run lengths be \(J,H\)
and the first two terminal zero counts be \(z,z'\). Formula (10.2) makes
the quotient after the second up-run at least that after the first, so
\(z'\ge z\); the quotient hypothesis gives \(z\ge1\). Combining (10.1)
for the last two segments with (10.3) at their parents forces exactly the
forbidden equality (10.4). \(\square\)

This does not exclude more general ridges with mixed positive digits or
terminal magnitude \(v>1\).

## Lemma 70 (arbitrary terminal magnitude)

For a pure ridge \(1^K0^z\), let its last up-step create \(e=-v\), and
put \(A=Q+h+3\), \(S=Q+K\). Then

\[
1\le v\le S,\quad
N=2^KA-K-3-v,\quad
z=\left\lfloor\log_2\frac Sv\right\rfloor. \tag{10.5}
\]

At the next post-down start,

\[
N'=N+K+z+1,\quad Q'=S-1,\quad
h'=2^{z+1}v-S,\quad A'=2^{z+1}v+2. \tag{10.6}
\]

If the next ridge is pure with \(K',v'\), equating its version of (10.5)
with (10.6) gives

\[
2^KA+z+K'+1+v'-v=2^{K'}A'. \tag{10.7}
\]

These formulas follow directly from the up-run solution and Lemma 63.
\(\square\)

## Corollary 71 (adjacent dyadic congruence)

For \(m=\min(K,K')\),

\[
2^m\mid z+K'+1+v'-v. \tag{10.8}
\]

If \(z+K'+1+v+v'<2^m\), the divisible integer has absolute value below
its modulus and hence vanishes:

\[
v'=v-z-K'-1\le v-2. \tag{10.9}
\]

## Theorem 72 (complexity on an infinite pure tail)

Suppose a sublinear infinite-down counterexample is eventually a chain of
pure ridges. Write \(m_j=\min(K_j,K_{j+1})\). Then \(m_j\to\infty\), and
infinitely often

\[
\max\{z_j,K_{j+1}+1,v_j,v_{j+1}\}\ge2^{m_j-2}. \tag{10.10}
\]

Indeed, Theorem 58 gives \(K_j\to\infty\). The integer

\[
E_j=z_j+K_{j+1}+1+v_{j+1}-v_j
\]

is divisible by \(2^{m_j}\). If \(E_j=0\) eventually, then the positive
integers \(v_j\) eventually decrease by at least two at every step, which
is impossible. Thus \(E_j\ne0\) infinitely often, when

\[
2^{m_j}\le |E_j|
\le z_j+(K_{j+1}+1)+v_j+v_{j+1}.
\]

One of the four terms proves (10.10). This is not termination: exact
arbitrary-\(v\) pure chains of length eight exist, and mixed positive words
are not covered. \(\square\)
