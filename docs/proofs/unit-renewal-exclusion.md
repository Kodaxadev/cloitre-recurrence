# Excluding strict alternating unit renewals

## Scope

Theorem 121 leaves a fixed-ladder alternative in which one bounded gap and
one returned residue recur infinitely often. This note excludes the most
rigid version of that mechanism: the same renewal cannot occur at every
other gate three times in succession.

The result concerns arbitrary consecutive unit blocks. Pure upper is needed
only when applying it to Theorem 121.

## Theorem 122 (no three strict alternating renewals)

Consider six consecutive unit positive blocks with returned residues
\(f_0,\ldots,f_5\) and intervening gaps \(r_0,\ldots,r_4\). There are no
integers \(R\ge0\) and \(a\ge1\) for which

\[
\boxed{
r_0=r_2=r_4=R,\qquad
f_1=f_3=f_5=a.
} \tag{122.1}
\]

Consequently, in the fixed-ladder alternative of Theorem 121, three
successive occurrences of the fixed pair \((R,a)\) cannot have both
successive occurrence-index differences equal to two gates.

### Proof

Assume (122.1), and put

\[
A=2^{R+2},\qquad
L_0=r_1,\qquad L_1=r_3,\qquad
x_0=f_0,\qquad x_1=f_2.
\]

The unit recurrence across the first bounded gap gives

\[
n_1+3+a=Ax_0. \tag{122.2}
\]

The next occurrence begins after gaps \(L_0,R\), so applying the same
identity there and subtracting (122.2) gives

\[
A(x_1-x_0)=L_0+R+4. \tag{122.3}
\]

In particular,

\[
L_0\equiv-R-4\pmod A,\qquad x_1>x_0. \tag{122.4}
\]

The large-gap recurrence between these two renewals is

\[
x_1=a2^{L_0+2}-Ax_0+a-L_0-2. \tag{122.5}
\]

Substituting (122.3) into (122.5) shows that \(x_0=F(L_0)\), where

\[
F(L)=
\frac{
aA2^{L+2}+aA-(A+1)L-2A-R-4
}{
A(A+1)
}. \tag{122.6}
\]

Repeating the same calculation for the second pair of renewals gives

\[
x_1=F(L_1),\qquad
L_1\equiv-R-4\pmod A. \tag{122.7}
\]

For every \(L\ge0\),

\[
F(L+A)-F(L)
=
\frac{a2^{L+2}(2^A-1)}{A+1}-1. \tag{122.8}
\]

Here \(A=2^{R+2}\ge R+4\) and \(A\ge4\). Therefore

\[
\frac{2^A-1}{A+1}>1
\]

and

\[
F(L+A)-F(L)
>2^{L+2}-1
>L+1
\ge\frac{L+R+4}{A}. \tag{122.9}
\]

Thus \(F\) is strictly increasing on the residue class in (122.4).
Since \(x_1>x_0\), equations (122.6)--(122.7) force
\(L_1\ge L_0+A\). Equations (122.8)--(122.9) then give

\[
x_1-x_0
=F(L_1)-F(L_0)
>\frac{L_0+R+4}{A},
\]

contradicting (122.3). \(\square\)

## Limitation

Theorem 122 excludes strict alternation only. Fixed-ladder renewals may
still recur with two or more other gates between some successive visits,
and the growing-modulus branch of Theorem 121 is unaffected.
