# Sparse down-steps in the sublinear branch

After entry, let \(P(n),D(n)\) count the up- and down-steps before index
\(n\), and put \(C(n)=P(n)+D(n)\).

## Theorem 58 (sublinear down-step sparsity)

If a counterexample satisfies \(q_n=o(n)\), then

\[
\frac{D(n)}{C(n)}\to0,\qquad
\frac{P(n)}{C(n)}\to1,\qquad
\frac{q_n}{C(n)}\to1,\qquad
\frac{C(n)}n\to0,\qquad
\frac{D(n)}n\to0. \tag{8.1}
\]

In particular, up- and down-steps both have zero time density, while zero
digits have density one.

Furthermore,

\[
\liminf\frac{C(n)\log_2n}{n}\ge1,\qquad
\liminf\frac{P(n)\log_2n}{n}\ge1. \tag{8.2}
\]

If \(d_1<d_2<\cdots\) are the down-step indices, then

\[
d_{j+1}-d_j
\ge
\left\lfloor\log_2\frac{d_j}{q_{d_j}}\right\rfloor-1
\to\infty \tag{8.3}
\]

for all sufficiently large \(j\).

### Proof

Fix \(s\ge2\) and \(M_s=2^{s+2}\). Sublinearity gives an index \(N_s\)
after which \(M_sq_k\le k\). Let \(D_s,C_s\) count down-steps and all
quotient changes on \([N_s,n)\). Theorem 56's disjoint rebound blocks give

\[
D_s(n)\le\frac{C_s(n)+s}{s+1}. \tag{8.4}
\]

The same rebound implication makes every down-step after \(N_s\) followed
by \(s\) up-steps. Hence \(d_{j+1}-d_j\ge s+1\) eventually. Letting the
fixed integer \(s\) grow proves (8.3).

More explicitly, at a down-step \(k\ge16q_k\), choose
\(s=\lfloor\log_2(k/q_k)\rfloor-2\). Then \(2^{s+2}q_k\le k\), so the same
argument forces \(s\) up-steps and gives the displayed lower bound.

Theorem 24 gives \(q_n\to\infty\). Since
\(\lvert q_n-q_{N_s}\rvert\le C_s(n)\), we have \(C_s(n)\to\infty\).
Divide (8.4) by \(C_s(n)\), remove the fixed initial prefix, and take
\(n\to\infty\) with \(s\) fixed. The resulting upper bound is
\(1/(s+1)\); now let \(s\to\infty\). This proves \(D/C\to0\).
The remaining limits follow from

\[
P/C=1-D/C,\qquad
q_n-q_{n_0}=C-2D,
\]

and Theorem 56. \(\square\)

## Corollary 59 (growth dichotomy)

Every counterexample either has \(\limsup q_n/n>0\), and hence
\(\limsup b_n/n^2>0\), or has \(q_n=o(n)\) and satisfies Theorem 58.

Divergent spacing and zero density still do not imply eventual absence of
down-steps.

## Lemma 60 (weighted rebound budget)

On a pre-absorption interval \([u,n)\), let \(P_{u,n}\) count up-steps and,
for each down-step \(k\), put

\[
\rho_k=\max\left\{0,
\left\lfloor\log_2\frac{k}{q_k}\right\rfloor-2\right\}.
\]

Then

\[
\sum_{\substack{u\le k<n\\a_k=-1}}\rho_k
\le P_{u,n}+\lfloor\log_2n\rfloor. \tag{8.5}
\]

Indeed, Theorem 22 forces \(\rho_k\) up-steps immediately after the
down-step. These charged blocks are disjoint. All are counted by \(P_{u,n}\)
except possibly the final block crossing the right endpoint, whose length is
at most \(\lfloor\log_2n\rfloor\). \(\square\)

## Corollary 61 (post-down ridge dilution)

Suppose down-steps are infinite, at indices \(d_1<d_2<\cdots\). Let
\(L_j=d_{j+1}-d_j-1\), and let \(U_j\) count up-steps strictly between
these two down-steps. Then

\[
L_j\to\infty,\qquad
\frac{\sum_{j<J}U_j}{\sum_{j<J}L_j}\to0. \tag{8.6}
\]

Hence some subsequence satisfies \(U_j/L_j\to0\). Along that subsequence,
the forced initial rebound length

\[
R_j=\left\lfloor\log_2\frac{d_j}{q_{d_j}}\right\rfloor-2
\]

obeys \(R_j\to\infty\) but \(R_j/L_j\to0\).

Indeed, Theorem 58 gives \(P(n)/n,D(n)/n\to0\). The completed intervening
segments have total length asymptotic to their final index and contain at
most \(P(n)=o(n)\) up-steps. The weighted average in (8.6) follows, and a
nonnegative weighted average tending to zero has a subsequence of component
ratios tending to zero. \(\square\)

## Lemma 62 (post-down zero budget)

Suppose a down-step at \(N-1\) reaches \((N,Q,e_N)\), and put
\(h=N-Q-e_N\), so \(1\le h\le Q+1\). If the next \(L\) digits contain
no down-step and \(\mathcal Z=\{i<L:a_{N+i}=0\}\), then

\[
Q+h+3
=\sum_{i\in\mathcal Z}\frac{N+i+2}{2^{i+1}}
+\frac{N+L+3-e_{N+L}}{2^L}. \tag{8.7}
\]

Consequently the zero sum is strictly smaller than \(Q+h+3\).

Indeed, unroll the doubling law over \(L\) steps. The same weighted sum
with every digit equal to one is

\[
N+3-\frac{N+L+3}{2^L}.
\]

Subtracting the actual digit sum and using
\(e_N=N-Q-h\) gives (8.7). Its terminal numerator is positive because
\(e_{N+L}<N+L\). \(\square\)
