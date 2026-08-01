# Sparse-binary unit-word arithmetic

## Lemma 125

In Lemma 123, let

\[
S=s_p,\qquad d_j=S-s_{j+1},\qquad
B=\sum_{j=0}^{p-1}2^{d_j},\qquad
W=\sum_{j=0}^{p-1}d_j2^{d_j}.
\]

Then

\[
P_p=2^S,\qquad B_p=B,\qquad C_p=(S+3)B-W. \tag{25.1}
\]

In particular, equal endpoint residues \(f_0=f_p=a\) satisfy

\[
\boxed{B(n_p+3)=(2^S-1)a+W.} \tag{25.2}
\]

The exponents obey

\[
S>d_0>\cdots>d_{p-1}=0,\quad
S-d_0=r_0+2,\quad d_{j-1}-d_j=r_j+2. \tag{25.3}
\]

If the endpoints are successive occurrences of the fixed renewal pair
\((R,a)\), then

\[
\boxed{S\equiv0\pmod {2^{R+2}},\qquad
p\ge2,\qquad d_{p-2}=R+2.} \tag{25.4}
\]

### Proof

Unroll the three coefficient recurrences in Lemma 123. Every contribution
to \(B_p\) has suffix multiplier \(2^{S-s_{j+1}}=2^{d_j}\). The contribution
to \(C_p\) inserted at that gate is
\(s_j+r_j+5=s_{j+1}+3=S+3-d_j\), proving (25.1).
Substitution into Lemma 123 gives (25.2), and the gap definitions give
(25.3).

At each occurrence of \((R,a)\), Corollary 114 gives
\(n+3+a\equiv0\pmod {2^{R+2}}\). Subtract at the two endpoints to obtain
the span congruence. A one-gate word would have
\(S=R+2<2^{R+2}\), so \(p\ge2\); the final incoming gap is \(R\), yielding
the last exponent in (25.4). \(\square\)

## Proposition 126

Let \(7\le a\le32\), \(3\nmid a\), and

\[
q\equiv4a\pmod {12}.
\]

Put

\[
S=8q,\quad L=S-5,\quad T=2^S,
\]

\[
n_0=\frac{a(T-1)+24}{9}-S-3,\quad
b=\frac{n_0+3+a}{8},\quad
c=\frac{a2^{S-3}+a+3}{9}.
\tag{25.5}
\]

There is a literal four-block all-unit pure-upper safe-map segment

\[
\begin{array}{c|cccc}
&-1&0&1&2\\ \hline
n&n_0-3&n_0&n_0+S-3&n_0+S\\
U&0&1&2&3\\
f&b&a&c&a
\end{array}
\]

with gaps \((1,L,1)\). Thus \((R,a)=(1,a)\) occurs twice, and the
intervening span is unbounded as \(q\to\infty\) in its residue class.

### Proof

The congruence on \(q\) implies \(q\equiv a\pmod3\) and \(4\mid q\).
Using \(2^6\equiv1\pmod9\) proves that \(n_0\) is integral. Reduction
modulo eight makes \(b\) integral, while

\[
c=a2^{S-3}-n_0-S
\]

makes \(c\) integral. The four unit congruences and three transitions are

\[
\begin{gathered}
n_0+b\equiv0\pmod4,\quad n_0+3+a=8b,\\
n_0+S+c=a2^{S-3},\quad n_0+S+3+a=8c,\\
b\xrightarrow{\,1\,}a
\xrightarrow{\,L\,}c
\xrightarrow{\,1\,}a.
\end{gathered}
\]

For the first congruence,
\(8(n_0+b)=aT-9S\), divisible by \(32\).

Here \(S\ge32\) and \(n_0\ge3\,340\,530\,086\). The only
scale-sensitive unit/pure-upper inequalities reduce to

\[
\begin{aligned}
a(T/4-1)&\ge15,\\
(36-a)T&\ge8a+24,\\
(7a-36)T&\ge16a+768,
\end{aligned}
\]

which hold for \(7\le a\le32\), \(T\ge2^{32}\). The remaining inequalities
are immediate linear consequences of the displayed lower bound for \(n_0\).
Lemma 117 and Corollary 115 reconstruct the segment. \(\square\)

This construction makes Theorem 122 sharp in the number of renewals. It
does not provide an infinite chain or establish reachability from \(b_1=m\).
Proposition 129 proves that the family exits pure-upper after one further
gate.
