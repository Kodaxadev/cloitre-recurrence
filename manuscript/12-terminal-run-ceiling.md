# The terminal-run state-window ceiling

Suppose \(R\ge1\) consecutive up-digits begin at index \(t\), with
\(Q=q_t\), and their last up-step creates \(e_{t+R}=-v\). Assume this is
the terminal positive run before the next down-step.

## Lemma 78 (terminal-run inequality)

\[
2^R(t+3-e_t)=t+R+3+v \tag{12.1}
\]

and

\[
2^R(Q+4)\le t+Q+2R+3. \tag{12.2}
\]

Indeed, \(A_n=n+3-e_n\) doubles at each up-step, proving (12.1).
The state window gives \(A_t\ge Q+4\), while Lemma 63 gives
\(v\le Q+R\). Substitution proves (12.2). \(\square\)

## Corollary 79 (log-log ceiling)

In a counterexample with \(q_n=o(n)\), every sequence of terminal runs
beginning at \(t\to\infty\) satisfies

\[
2^R\le(1+o(1))\log_2t,\qquad
R\le\log_2\log_2t+o(1). \tag{12.3}
\]

If \(R>t\), then (12.2) and \(Q\le t\) would give
\(5\cdot2^R\le4R+3\), impossible. Hence \(R\le t\). Equation (12.2) now
gives

\[
5\cdot2^R\le4t+3,
\]

so \(R=O(\log t)\). Theorem 56 gives

\[
Q\ge(1-o(1))\frac{t}{\log_2t}.
\]

Using also \(Q=o(t)\) and \(R=o(t)\) in (12.2) proves the first bound in
(12.3); taking a base-two logarithm proves the second. \(\square\)

This does not close the growing-run branch of Theorem 77. The modulus
allowed by (12.3) may still be logarithmic in the absolute index, and the
parameters forced by Theorem 75 need not have a smaller upper bound.
