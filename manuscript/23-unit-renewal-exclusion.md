# Strict alternating renewals

## Theorem 122

Let six consecutive unit blocks have returned residues
\(f_0,\ldots,f_5\) and gaps \(r_0,\ldots,r_4\). It is impossible that

\[
r_0=r_2=r_4=R,\qquad f_1=f_3=f_5=a \tag{23.1}
\]

for fixed integers \(R\ge0\), \(a\ge1\).

### Proof

Put \(A=2^{R+2}\), \(L_j=r_{2j+1}\), \(x_j=f_{2j}\).
The repeated bounded-gap identity gives

\[
A(x_{j+1}-x_j)=L_j+R+4. \tag{23.2}
\]

Hence every \(L_j\equiv-R-4\pmod A\), and \(x_{j+1}>x_j\).
Combining (23.2) with the intervening large-gap recurrence gives

\[
x_j=F(L_j),\quad
F(L)=
\frac{aA2^{L+2}+aA-(A+1)L-2A-R-4}{A(A+1)}.
\tag{23.3}
\]

On the required residue class,

\[
F(L+A)-F(L)
=\frac{a2^{L+2}(2^A-1)}{A+1}-1
>L+1
\ge\frac{L+R+4}{A}. \tag{23.4}
\]

Since \(x_1>x_0\), monotonicity forces \(L_1\ge L_0+A\); then (23.4)
contradicts (23.2). \(\square\)

Thus fixed-ladder renewals from Theorem 121 cannot recur at every other
gate three times consecutively. Longer or irregular return spacings remain
possible.
