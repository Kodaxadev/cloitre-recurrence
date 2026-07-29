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
