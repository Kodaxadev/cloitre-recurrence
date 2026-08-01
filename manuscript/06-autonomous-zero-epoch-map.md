# Autonomous zero-epoch dynamics

At a zero epoch, retain \(W=n-U\) and \(d=W-2e\ge0\), and put

\[
A=U+d+4.
\]

## Lemma 53 (autonomous overshoot)

One has

\[
U+4\le A\le n+2,\qquad A\equiv n\pmod2.
\]

If \(k\) is the maximal following wrap-run length, then \(k\) is the
least \(j\ge0\) satisfying

\[
2^{j+1}A\ge n+j+5. \tag{6.1}
\]

At the first non-wrap state,

\[
n'=n+k+1,\quad U'=U+k,\quad
A'=2^{k+1}A-(n'+2). \tag{6.2}
\]

Here \(2\le A'\le n'+2\) and \(A'\equiv n'\pmod2\). The state terminates
for \(2\le A'\le U'+3\), and returns to a zero epoch for
\(A'\ge U'+4\). Thus \((n,A)\) evolves autonomously; \(U\) only decides
which side of the terminating threshold the overshoot occupies.

### Proof

The coordinate bounds follow from \(0\le d\le W-2\) and
\(d\equiv W\pmod2\). Equations (6.1)--(6.2) are Lemma 51 after using
\(W+U=n\). Minimality in (6.1) gives the bounds on \(A'\), while
\(d'=A'-U'-4\) gives the branch classification. \(\square\)

## Corollary 54 (sparse dyadic coding)

For zero epochs \(n_0<n_1<\cdots\) of an infinite safe path,

\[
\frac{A_i}{2^{n_i}}
=\sum_{j=i+1}^{\infty}\frac{n_j+2}{2^{n_j}}. \tag{6.3}
\]

Indeed, (6.2) divided by \(2^{n_{i+1}}\) telescopes, and
\(A_j/2^{n_j}\to0\).

## Theorem 55 (forced double zeros)

At a zero epoch put \(G=W-U=n-2U\), and let \(k_i\) be the following
wrap-run lengths. If \(R\ge1\) consecutive blocks satisfy \(k_i\ge1\),
then \(G_0\ge4\); if \(R\ge2\), then

\[
2R\le3G_0-2U_0-14. \tag{6.4}
\]

Consequently, every infinite safe path contains infinitely many pairs
\(00\), infinitely many wraps, and eventually satisfies

\[
n-2U\ge4
\]

at every state.

### Proof

A zero followed by a wrap requires \(2W>W+U+3\), so \(G\ge4\).
A positive block of length \(k\) that returns obeys

\[
G'=G+1-k,\qquad U'=U+k,
\]

and validity at its last wrap gives \(G\ge k+3\), hence \(G'\ge4\).
If the next block is also positive, its first-wrap condition gives
\(2d'\le G'-4\). Formula (5.2) becomes

\[
d'=(2^{k+1}-3)U+2^{k+1}d+2^{k+3}-G-2k-7.
\]

Substitution yields \(2U+18\le3G\). Apply this at the penultimate block,
using \(U_i\ge U_0+i\) and \(G_i\le G_0\), to obtain (6.4).

An infinite path has infinitely many zero epochs because wrap runs are
finite. An eventual absence of \(k_i=0\) contradicts (6.4); an eventual
absence of positive \(k_i\) makes \(e\) double forever against \(e<W\).
The bound \(n-2U\ge4\) is preserved through both zero blocks and returning
positive blocks. \(\square\)

These restrictions do not exclude an aperiodic infinite overshoot orbit.
