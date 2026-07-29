# Sparse down-steps in the sublinear branch

After entry, let \(P(n),D(n)\) count the up- and down-steps before index
\(n\), and put \(C(n)=P(n)+D(n)\).

## Theorem 58 (sublinear down-step sparsity)

If a counterexample satisfies \(q_n=o(n)\), then

\[
\frac{D(n)}{C(n)}\to0,\qquad
\frac{P(n)}{C(n)}\to1,\qquad
\frac{q_n}{C(n)}\to1,\qquad
\frac{D(n)}n\to0. \tag{8.1}
\]

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
