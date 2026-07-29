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
