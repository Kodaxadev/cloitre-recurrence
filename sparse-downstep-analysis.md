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
C(n)=P(n)+D(n)
\]

be the number of quotient-changing digits.

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
\frac{D(n)}n\longrightarrow0, \tag{58.2}
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

which proves (58.2). Finally combine \(C(n)/q_n\to1\) and
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
