# Autonomous overshoot and forced double-zero recurrence

This note continues Lemma 51's accelerated zero-epoch map. It proves a
global restriction on every hypothetical infinite safe path; it does not
prove termination.

## Lemma 53: autonomous overshoot map

At a zero epoch, retain

\[
W=n-U,\qquad d=W-2e\ge0,
\]

and define the overshoot coordinate

\[
A=U+d+4.
\]

Then

\[
U+4\le A\le n+2,\qquad A\equiv n\pmod2. \tag{53.1}
\]

Let \(k\) be the maximal following wrap-run length from Lemma 51. It is
the least \(j\ge0\) satisfying

\[
2^{j+1}A\ge n+j+5. \tag{53.2}
\]

Put

\[
n'=n+k+1,\qquad U'=U+k,\qquad
A'=2^{k+1}A-(n'+2). \tag{53.3}
\]

Then \(2\le A'\le n'+2\) and \(A'\equiv n'\pmod2\). The first non-wrap
state terminates exactly when

\[
2\le A'\le U'+3,
\]

and returns to a zero epoch exactly when \(A'\ge U'+4\).
In particular, the arithmetic evolution of \((n,A)\) in (53.2)--(53.3)
is autonomous: \(U\) only selects between return and termination.

### Proof

The lower bound in (53.1) is \(d\ge0\). Since \(e\ge1\),
\(d=W-2e\le W-2\), which gives \(A\le U+W+2=n+2\).
Also \(d\equiv W\pmod2\), so \(A\equiv U+W=n\pmod2\).

Equation (53.2) is (51.1) with \(W+U=n\). Substituting (51.2) gives

\[
U'+d'+4=2^{k+1}A-n-k-3=2^{k+1}A-(n'+2),
\]

which is (53.3). Minimality in (53.2) gives \(A'\ge2\). If \(k=0\),
(53.1) gives \(A'\le n'=n+1\). If \(k\ge1\), minimality at \(k-1\)
gives \(2^kA\le n+k+3\), hence \(A'\le n+k+3=n'+2\).
Parity follows from (53.3). Finally,

\[
d'=A'-U'-4,
\]

so Lemma 51's return condition \(d'\ge0\) is exactly the stated
threshold. \(\square\)

## Corollary 54: sparse dyadic coding

Let \(n_0<n_1<\cdots\) be the zero epochs of an infinite safe path, and
let \(A_i\) be their overshoot coordinates. Then

\[
\frac{A_i}{2^{n_i}}
=\sum_{j=i+1}^{\infty}\frac{n_j+2}{2^{n_j}}. \tag{54.1}
\]

Thus every infinite path would encode a dyadic rational by its sparse
set of zero epochs.

### Proof

Writing \(L_i=n_{i+1}-n_i=k_i+1\), (53.3) gives

\[
\frac{A_{i+1}}{2^{n_{i+1}}}
=\frac{A_i}{2^{n_i}}-\frac{n_{i+1}+2}{2^{n_{i+1}}}.
\]

Telescope. The remainder tends to zero because
\(2\le A_j\le n_j+2\). \(\square\)

## Theorem 55: quantitative recurrence of double zeros

At a zero epoch define

\[
G=W-U=n-2U.
\]

Let \(k_i\) be the wrap-run length following its zero digit. Suppose a
safe path begins at \((U_0,G_0)\) with a run of \(R\ge1\) consecutive
positive blocks

\[
k_0,k_1,\ldots,k_{R-1}\ge1,
\]

where the last block may terminate rather than return. Then \(G_0\ge4\).
If \(R\ge2\), then

\[
2R\le3G_0-2U_0-14. \tag{55.1}
\]

Consequently every infinite safe path has:

1. infinitely many \(k_i=0\), hence infinitely many consecutive digit
   pairs \(00\);
2. infinitely many positive \(k_i\), hence infinitely many wraps;
3. after its first positive block,
   \[
   n-2U\ge4
   \]
   at every state, and therefore \(U\le(n-4)/2\).

### Proof

A positive block means that the state immediately after its zero digit
wraps. At that state the width is \(W+1\), its residue is at most \(W\),
and its modulus is \(W+U+3\). Therefore

\[
2W>W+U+3,
\]

so \(G=W-U\ge4\). If a block of length \(k\) returns to a zero epoch,

\[
G'=G+1-k,\qquad U'=U+k. \tag{55.2}
\]

At the last wrap, the same validity argument gives \(G\ge k+3\), hence
\(G'\ge4\). Thus \(G_i\) is nonincreasing along consecutive positive
blocks.

For any block except the last one, the next block is also positive.
The first-wrap condition there gives

\[
2d'\le G'-4. \tag{55.3}
\]

Using \(W=U+G\), formula (51.2) becomes

\[
d'=(2^{k+1}-3)U+2^{k+1}d+2^{k+3}-G-2k-7.
\]

Substitute this and (55.2) into (55.3), then discard the nonnegative
\(d\)-term:

\[
2(2^{k+1}-3)U+2^{k+4}-3k-11\le3G.
\]

For \(k\ge1\), the left side is at least \(2U+18\). Hence, for
\(i=0,\ldots,R-2\),

\[
2U_i+18\le3G_i\le3G_0.
\]

Since \(U_i\ge U_0+i\), taking \(i=R-2\) proves (55.1).

Lemma 44 makes every wrap run finite, so an infinite path has infinitely
many zero epochs. If only finitely many \(k_i\) were zero, an arbitrarily
long positive-block run would contradict (55.1). If only finitely many
were positive, the path would eventually consist solely of zero digits;
then \(e\) would double while \(W\) grew linearly, contradicting
\(0<e<W\). This proves the first two assertions.

Finally, a returning positive block has \(G'\ge4\), a zero block
increments \(G\), and every intermediate wrap state has
\(n-2U=G+1-j\ge G'\). The final assertion follows. \(\square\)

## What remains open

The autonomous map (53.2)--(53.3), the dyadic identity (54.1), and the
forced recurrence of \(00\) still permit aperiodic infinite words. A
complete proof would need to show that no such word can satisfy both the
overshoot threshold and the growing termination threshold \(A\le U+3\).
