# Unit-leading growth without a monotonicity hypothesis

Theorem 27 used two forced up-steps after each sufficiently deep
down-step and obtained a leading constant \(1/3\). The exact rebound
cascade permits any fixed number of charged up-steps.

## Theorem 56 (universal unit-leading logarithmic growth)

Let \(n_0\) be the entry index and \(n\) a nonabsorbed index. For
\(s\ge2\), put

\[
\alpha_s=\frac{s-1}{s+1},\qquad
M_s=2^{s+2},\qquad H=\lfloor\log_2n\rfloor.
\]

If \(H+1\ge\alpha_sM_s\), then

\[
q_n\ge\alpha_s\frac{n}{H+1}-n_0-5. \tag{7.1}
\]

Consequently every counterexample satisfies

\[
\liminf_{n\to\infty}\frac{q_n\log_2n}{n}\ge1,\qquad
\liminf_{n\to\infty}\frac{b_n\log_2n}{n^2}\ge1. \tag{7.2}
\]

### Proof

On an interval \([u,n)\) with \(M_sq_k\le k\), let \(E,U,D\) count
nonzero, up, and down digits. Lemma 26 gives

\[
E\ge\frac{n-u-H}{H+1}. \tag{7.3}
\]

Theorem 22 and \(k\ge M_sq_k\) force at least \(s\) up-steps after every
down-step. The blocks are disjoint, with at most \(s\) charged steps lost
at the right endpoint. Thus

\[
U\ge sD-s,\qquad
q_n-q_u=E-2D\ge\alpha_sE-2. \tag{7.4}
\]

Choose \(u\) just after the last index \(h<n\) with \(M_sq_h>h\). Then
\(q_u>u/M_s-2\), and the hypothesis on \(H\) gives
\(q_u>\alpha_su/(H+1)-2\). Equations (7.3)--(7.4) yield (7.1).
If no such \(h\) exists, take \(u=n_0\); the stated constant is a common
weakening.

For a counterexample, fix \(s\) and let \(n\to\infty\). The lower limit
in (7.2) is at least \(\alpha_s\). Letting the fixed integer \(s\) tend
to infinity gives one. The bound for \(b_n\) follows from
\(b_n\ge nq_n\). \(\square\)

This theorem applies whether quotient down-steps occur finitely or
infinitely often. It does not by itself force capture.
