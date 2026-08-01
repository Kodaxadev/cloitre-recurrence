# Sparse down-steps in every sublinear counterexample

Theorem 56 permits a sharper classification of the branch with infinitely
many quotient down-steps. It does not prove that the branch is empty.

After the entry index \(n_0\), let

\[
P(n)=\#\{k\in[n_0,n):a_k=1\},\qquad
D(n)=\#\{k\in[n_0,n):a_k=-1\},
\]

and let

\[
C(n)=P(n)+D(n),\qquad
Z(n)=\#\{k\in[n_0,n):a_k=0\}
\]

be the numbers of quotient-changing and zero digits.

## Theorem 58: down-step sparsity under sublinear quotient growth

Suppose a counterexample satisfies

\[
q_n=o(n).
\]

Then

\[
\frac{D(n)}{C(n)}\longrightarrow0,\qquad
\frac{P(n)}{C(n)}\longrightarrow1,\qquad
\frac{q_n}{C(n)}\longrightarrow1. \tag{58.1}
\]

Moreover,

\[
\frac{C(n)}n\longrightarrow0,\qquad
\frac{P(n)}n\longrightarrow0,\qquad
\frac{D(n)}n\longrightarrow0,\qquad
\frac{Z(n)}n\longrightarrow1, \tag{58.2}
\]

and

\[
\liminf_{n\to\infty}\frac{C(n)\log_2n}{n}\ge1,\qquad
\liminf_{n\to\infty}\frac{P(n)\log_2n}{n}\ge1. \tag{58.3}
\]

At a down-step \(q_k\ge1\). For any such index \(k\) with
\(k\ge16q_k\), put

\[
R_k=\left\lfloor\log_2\frac{k}{q_k}\right\rfloor-2.
\]

Then \(R_k\ge2\) and the next \(R_k\) digits are all up-steps. In
particular, if down-steps occur at the infinite sequence of digit indices
\(d_1<d_2<\cdots\), then

\[
d_{j+1}-d_j
\ge
\left\lfloor\log_2\frac{d_j}{q_{d_j}}\right\rfloor-1
\longrightarrow\infty. \tag{58.4}
\]

More precisely, for every fixed \(s\ge2\), all sufficiently late down-steps
are followed immediately by at least \(s\) consecutive up-steps.

Thus an infinite-down counterexample with sublinear quotient would be an
asymptotically one-sided quotient process: down-steps may remain infinite,
but they have zero density both in time and among quotient changes, and
their individual spacings diverge.

### Proof

Fix \(s\ge2\) and put \(M_s=2^{s+2}\). Since \(q_k/k\to0\), there is an
index \(N_s\ge n_0\) such that

\[
M_sq_k\le k\qquad(k\ge N_s). \tag{58.5}
\]

At any down-step \(k\ge N_s\), the parameterized rebound implication used
in Theorem 56 therefore forces \(a_{k+1}=\cdots=a_{k+s}=1\). If down-steps
are infinite, this gives \(d_{j+1}-d_j\ge s+1\) for all sufficiently large
\(j\). Since \(s\) is arbitrary, the limit assertion in (58.4) follows.

For the explicit bound, let
\(h=\lfloor\log_2(k/q_k)\rfloor\) and \(s=h-2\). The premise \(k\ge16q_k\)
gives \(s\ge2\), while \(2^{s+2}q_k\le k\). The same rebound implication
forces \(s=R_k\) up-steps and therefore places the next down-step at least
\(s+1=h-1\) indices later. Finally \(q_{d_j}/d_j\to0\), so this explicit
lower bound also tends to infinity.

Count digits on \([N_s,n)\), writing \(P_s,D_s,C_s\) for the corresponding
counts. The parameterized rebound argument in Theorem 56 applies to the
whole interval. Every down-step forces \(s\) up-steps, the blocks are
disjoint, and at most \(s\) charged steps cross the right endpoint.
Therefore

\[
P_s\ge sD_s-s,\qquad
D_s\le\frac{C_s+s}{s+1}. \tag{58.6}
\]

Theorem 24 gives \(q_n\to\infty\). Since

\[
|q_n-q_{N_s}|\le C_s(n),
\]

we have \(C_s(n)\to\infty\). Divide (58.6) by \(C_s\):

\[
\limsup_{n\to\infty}\frac{D_s(n)}{C_s(n)}
\le\frac1{s+1}.
\]

Changing the initial index alters both counts by only a fixed amount, so
the same inequality holds for \(D(n)/C(n)\). Since it holds for every
fixed \(s\),

\[
\frac{D(n)}{C(n)}\to0.
\]

The first two assertions of (58.1) follow. The exact count identity

\[
q_n-q_{n_0}=P(n)-D(n)=C(n)-2D(n)
\]

gives \(q_n/C(n)\to1\). Since \(D\le C\le n-n_0\),

\[
0\le\frac{D(n)}n\le\frac{D(n)}{C(n)}\to0,
\]

and \(C/n=(C/q_n)(q_n/n)\to0\). Hence \(P/n\to0\), while
\(Z=n-n_0-C\) gives \(Z/n\to1\). This proves (58.2). Finally combine
\(C(n)/q_n\to1\) and
\(P(n)/C(n)\to1\) with Theorem 56 to obtain (58.3). \(\square\)

## Corollary 59: counterexample growth dichotomy

Every counterexample lies in exactly one of the following classes:

1. \(\limsup q_n/n>0\), and consequently
   \[
   \limsup b_n/n^2>0;
   \]
2. \(q_n=o(n)\), and all conclusions of Theorem 58 hold.

In the second class, if down-steps are infinite, both their individual
spacings and the cumulative average number of quotient changes per down-step
tend to infinity.

### Proof

Because \(q_n/n\ge0\), failure of \(q_n=o(n)\) is exactly
\(\limsup q_n/n>0\). Also \(b_n\ge nq_n\). In the sublinear class,
\(D/C\to0\); if \(D\to\infty\), then \(C/D\to\infty\). \(\square\)

## Limitation

Zero density is not finite occurrence. Theorem 58 reduces a sublinear
infinite-down counterexample to sparse interruptions separated by
increasingly long one-sided segments. The current safe-map theorem does not
give a uniform termination time for those segments, so divergent spacing
still does not imply that down-steps occur only finitely often.

## Lemma 60: weighted rebound budget

On any pre-absorption digit interval \([u,n)\) after entry, let \(P_{u,n}\)
be the number of up-steps. For every down-step index \(k\in[u,n)\), put

\[
\rho_k=
\max\left\{0,\left\lfloor\log_2\frac{k}{q_k}\right\rfloor-2\right\}.
\]

Then

\[
\boxed{\displaystyle
\sum_{\substack{u\le k<n\\a_k=-1}}\rho_k
\le P_{u,n}+\lfloor\log_2n\rfloor.} \tag{60.1}
\]

Thus deep down-steps consume a quantitatively disjoint budget of subsequent
up-steps; only the final charged block can cross the right endpoint.

### Proof

At a down-step \(q_k\ge1\). If \(\rho_k\ge1\), then

\[
2^{\rho_k+2}q_k\le k.
\]

For \(s=\rho_k\), the difference between this lower bound for \(k+1\) and
Theorem 22's sufficient right side is at least

\[
(2^{s+1}+1)q_k-2^{s+1}+2s+3\ge2s+4.
\]

Thus Theorem 22 applies, so
\(a_{k+1},\ldots,a_{k+\rho_k}\) are all up-steps. Charged blocks belonging
to distinct down-steps are disjoint, because no down-step can occur inside
one of them.

Every block contained in \([u,n)\) is therefore counted by \(P_{u,n}\).
If a block crosses \(n\), it belongs to the last down-step in the interval,
and there can be no second crossing block. Its omitted length is at most

\[
\rho_k\le\lfloor\log_2 k\rfloor\le\lfloor\log_2n\rfloor.
\]

Adding this single endpoint allowance proves (60.1). \(\square\)

## Corollary 61: necessary dilution of post-down ridge segments

Assume the sublinear counterexample has infinitely many down-steps
\(d_1<d_2<\cdots\). Put

\[
L_j=d_{j+1}-d_j-1
\]

and let \(U_j\) count up-steps at the intervening digit indices
\((d_j,d_{j+1})\). Then

\[
L_j\longrightarrow\infty,\qquad
\frac{\sum_{j<J}U_j}{\sum_{j<J}L_j}\longrightarrow0. \tag{61.1}
\]

Consequently there is a subsequence \(j_\nu\) such that

\[
\frac{U_{j_\nu}}{L_{j_\nu}}\longrightarrow0. \tag{61.2}
\]

If \(R_j=\lfloor\log_2(d_j/q_{d_j})\rfloor-2\) is the forced rebound
length from Theorem 58, then along the same sufficiently late subsequence,

\[
R_j\le U_j,\qquad \frac{R_j}{L_j}\longrightarrow0. \tag{61.3}
\]

Thus a sublinear infinite-down counterexample would require arbitrarily
long post-down ridge segments whose up-step fraction tends to zero, despite
an initial forced up-run whose length tends to infinity.

### Proof

Theorem 58 gives \(L_j\to\infty\). Up to a fixed initial and terminal
prefix,

\[
\sum_{j<J}L_j=d_J-d_1-(J-1),\qquad
\sum_{j<J}U_j\le P(d_J).
\]

Because \(D(d_J)/d_J\to0\), the first sum is asymptotic to \(d_J\);
because \(P(d_J)/d_J\to0\), their ratio tends to zero. This proves (61.1).
A weighted average of nonnegative ratios can tend to zero only if some
subsequence of the ratios tends to zero, proving (61.2). Theorem 58 gives
\(R_j\le U_j\) eventually, so (61.3) follows. \(\square\)

## Lemma 62: exact zero budget on a post-down ridge

Suppose a down-step at index \(N-1\) reaches the state
\((N,Q,e_N)\), and put

\[
h=N-Q-e_N.
\]

Then \(1\le h\le Q+1\). Suppose the next \(L\) digits contain no
down-step, and let

\[
\mathcal Z=\{0\le i<L:a_{N+i}=0\}.
\]

Writing \(e_{N+L}\) for the terminal state coordinate, one has the exact
identity

\[
\boxed{\displaystyle
Q+h+3
=
\sum_{i\in\mathcal Z}\frac{N+i+2}{2^{i+1}}
+\frac{N+L+3-e_{N+L}}{2^L}.} \tag{62.1}
\]

In particular,

\[
\sum_{i\in\mathcal Z}\frac{N+i+2}{2^{i+1}}<Q+h+3. \tag{62.2}
\]

If \(i_0\) is the first zero offset, then

\[
2^{i_0+1}>\frac{N+i_0+2}{Q+h+3}. \tag{62.3}
\]

Thus the whole finite zero pattern, not only its first digit, has a dyadic
budget controlled by the narrow post-down ridge.

### Proof

Write the parent down-step as \((N-1,q,r)\). Then

\[
Q=q-1,\qquad e_N=N-h-Q,\qquad h=q-2r,
\]

so \(1\le h\le q=Q+1\). Unrolling the exact doubling law over the
following \(L\) digits gives

\[
e_N=
\sum_{i=0}^{L-1}
\frac{a_{N+i}(N+i+2)}{2^{i+1}}
+\frac{e_{N+L}}{2^L}. \tag{62.4}
\]

The corresponding sum with every digit equal to one is

\[
\sum_{i=0}^{L-1}\frac{N+i+2}{2^{i+1}}
=N+3-\frac{N+L+3}{2^L}. \tag{62.5}
\]

Subtract (62.4) from (62.5) and use
\(N+3-e_N=Q+h+3\). This proves (62.1). The terminal numerator is
positive because every valid state has \(e_{N+L}<N+L\), proving (62.2).
Keeping only the first zero term gives (62.3). \(\square\)
