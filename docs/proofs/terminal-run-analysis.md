# State-window ceiling for terminal up-runs

Theorem 77 splits the sublinear infinite-down branch according to whether
terminal positive up-runs grow. This note bounds the scale of any such run.
The bound is exact at finite indices and becomes logarithmic in the index
after the universal quotient lower bound is applied.

## Lemma 78: exact terminal-run inequality

Suppose \(R\ge1\) consecutive up-digits begin at index \(t\), with quotient
\(Q=q_t\), and the last up-step creates

\[
e_{t+R}=-v,\qquad v\ge1.
\]

Assume this is a terminal run: no later up-step occurs before the next
down-step. Then

\[
\boxed{\displaystyle
2^R(t+3-e_t)=t+R+3+v} \tag{78.1}
\]

and

\[
\boxed{\displaystyle
2^R(Q+4)\le t+Q+2R+3.} \tag{78.2}
\]

### Proof

For \(A_n=n+3-e_n\), every up-step gives \(A_{n+1}=2A_n\).
After \(R\) consecutive up-steps,

\[
A_{t+R}=2^RA_t.
\]

The endpoint defect is \(-v\), so

\[
A_{t+R}=t+R+3+v,
\]

which proves (78.1).

The state window \(r_t\le t-1\) and \(e_t=r_t-Q\) give

\[
t+3-e_t\ge Q+4.
\]

The quotient after the run is \(Q+R\). Lemma 63 gives
\(v\le Q+R\), because the last up-step is the sign-changing up-step
before the terminal negative suffix. Applying both inequalities to
(78.1) proves (78.2). \(\square\)

## Corollary 79: log-log ceiling in a sublinear counterexample

Suppose a counterexample has \(q_n=o(n)\). For every sequence of terminal
up-runs beginning at indices \(t\to\infty\), with lengths \(R(t)\),

\[
\boxed{\displaystyle
2^{R(t)}\le(1+o(1))\log_2 t} \tag{79.1}
\]

and consequently

\[
\boxed{\displaystyle
R(t)\le\log_2\log_2t+o(1).} \tag{79.2}
\]

In particular, the growing-run branch of Theorem 77 can grow only on the
log-log index scale.

### Proof

First suppose \(R>t\). Since \(Q\le t<R\), (78.2) would give

\[
5\cdot2^R\le4R+3,
\]

which is false for every \(R\ge1\). Thus \(R\le t\). Applying this,
\(Q\le t\), and \(Q\ge1\) to (78.2) gives

\[
5\cdot2^R\le4t+3.
\]

Therefore \(R=O(\log t)\), and hence \(R/t\to0\).

Theorem 56 gives

\[
\liminf_{t\to\infty}\frac{Q\log_2t}{t}\ge1,
\]

so

\[
Q\ge(1-o(1))\frac{t}{\log_2t}.
\]

Because \(Q/t\to0\) by hypothesis and \(R/t\to0\), (78.2) now yields

\[
2^R
\le\frac{t+Q+2R+3}{Q+4}
\le(1+o(1))\log_2t.
\]

Taking base-two logarithms proves (79.2). \(\square\)

## Limitation

This ceiling does not contradict Theorem 75. Its forced parameter has
lower scale \(2^{\min(R_j,R_{j+1})}\), while Corollary 79 permits that
scale to be logarithmic in the absolute index. The terminal magnitudes
\(v_j\), zero counts, and neighboring prefix lengths may all exceed a
logarithmic bound. Closing the growing-run branch requires a sharper
upper bound on those parameters or a stronger modulus than the terminal
run alone supplies.
