# Fixed-word rigidity and sparse renewals

## Lemma 123

For \(p+1\) consecutive unit positive blocks, put

\[
s_0=0,\qquad s_{t+1}=s_t+r_t+2.
\]

For the fixed gap word define

\[
\begin{aligned}
P_0&=1,&B_0&=C_0=0,\\
P_{t+1}&=2^{r_t+2}P_t,&
B_{t+1}&=2^{r_t+2}B_t+1,\\
C_{t+1}&=2^{r_t+2}C_t+s_t+r_t+5.
\end{aligned}
\]

Then

\[
n_t=n_0+s_t,\qquad f_t=P_tf_0-B_tn_0-C_t. \tag{24.1}
\]

Because \(p\ge1\) implies \(B_p>0\), fixed endpoint residues
\(f_0=a,f_p=b\) force

\[
n_0=\frac{P_pa-C_p-b}{B_p}. \tag{24.2}
\]

Thus a fixed nonempty gap word with fixed endpoint residues occurs at
most once.

### Proof

Induct in the exact unit recurrence

\[
n_{t+1}=n_t+r_t+2,\qquad
f_{t+1}=2^{r_t+2}f_t-n_t-r_t-5.
\]

The coefficient recurrences above are exactly those obtained after
substituting (24.1). Also \(B_1=1\), proving positivity and (24.2).
\(\square\)

## Corollary 124

On a hypothetical infinite all-unit pure-upper tail, fix \(R\ge0,a\ge1\)
and let

\[
M_{R,a}(J)=\#\{1\le i\le J:r_{i-1}=R,\ f_i=a\}.
\]

Then

\[
\limsup_{J\to\infty}
\frac{M_{R,a}(J)\log_2J}
{J\log_2\log_2J}\le1. \tag{24.3}
\]

In particular, every fixed renewal pair has zero density.

### Proof

The gap words between successive occurrences have common endpoint residue
\(a\), so Lemma 123 makes them pairwise distinct. Bounded \(M_{R,a}(J)\)
is trivial. Otherwise, for large \(J\), put \(K=M_{R,a}(J)-1\). The
interval lengths sum to at most \(J\).

Let \(A_J=1+\max_{i<J}r_i\). Corollary 115 and Theorem 118 give

\[
A_J=O(\log J),\qquad
\log_2A_J\le(1+o(1))\log_2\log_2J.
\]

Also \(A_J\ge2\) eventually.

For fixed \(\lambda>1\), more than
\((1-1/\lambda)K\) intervals have length at most
\(P_\lambda=\lceil\lambda J/K\rceil\). Counting distinct words gives

\[
\left(1-\frac1\lambda\right)K
\le A_J^{P_\lambda+1}. \tag{24.4}
\]

Taking \(\lambda=2\) first implies \(K/J\to0\). For arbitrary fixed
\(\lambda>1\), logarithms in (24.4) then give

\[
\frac KJ
\left(\log_2K+\log_2(1-1/\lambda)\right)
\le(\lambda+o(1))\log_2\log_2J.
\]

On every subsequence relevant to a positive limsup in (24.3),
the parenthesized logarithm divided by \(\log_2J\) tends to one. The
limsup is at most every \(\lambda>1\), hence at most one. \(\square\)

The result permits infinitely many sparse, aperiodic returns and does not
exclude the growing-modulus alternative of Theorem 121.
