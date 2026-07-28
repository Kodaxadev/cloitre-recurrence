# Sharp logarithmic growth for every counterexample

Theorem 27 proved \(q_n=\Omega_m(n/\log n)\) with explicit leading
constant \(1/3\). The factor came from charging each down-step against
only two forced rebound steps. The exact cascade in Theorem 22 permits
arbitrarily long fixed charges, which sharpens the limiting constant to
one without assuming that down-steps eventually stop.

## Theorem 56: universal sharp logarithmic growth

Let \(n_0\) be the entry index and let \(n\ge\max(n_0,4)\) be reached
before absorption. Fix an integer \(s\ge2\), and put

\[
\alpha_s=\frac{s-1}{s+1},\qquad
M_s=2^{s+2},\qquad H=\lfloor\log_2n\rfloor.
\]

Whenever

\[
H+1\ge\alpha_sM_s, \tag{56.1}
\]

one has

\[
q_n\ge
\alpha_s\frac{n}{H+1}-n_0-5. \tag{56.2}
\]

Consequently every nonstabilizing orbit satisfies

\[
\boxed{\displaystyle
\liminf_{n\to\infty}\frac{q_n\log_2 n}{n}\ge1}
\tag{56.3}
\]

and

\[
\boxed{\displaystyle
\liminf_{n\to\infty}\frac{b_n\log_2 n}{n^2}\ge1.}
\tag{56.4}
\]

### Proof

First consider an interval of digit indices \([u,n)\) on which

\[
M_sq_k\le k. \tag{56.5}
\]

Let \(E,Z,U,D\) be its numbers of nonzero, zero, up, and down digits.
As in Theorem 27, Lemma 26 bounds every zero run by \(H\), so

\[
E\ge\frac{n-u-H}{H+1}. \tag{56.6}
\]

Every down-step has \(q_k\ge1\). From (56.5),

\[
k\ge2^{s+2}q_k.
\]

This implies Theorem 22's sufficient condition

\[
k+1\ge
(2^{s+1}-1)q_k+2^{s+1}-2s-2,
\]

so the down-step is followed by at least \(s\) consecutive up-steps.
The resulting blocks are disjoint. At most one block crosses the right
endpoint, losing at most \(s\) of its charged up-steps. Hence

\[
U\ge sD-s.
\]

Since \(E=U+D\),

\[
D\le\frac{E+s}{s+1}
\]

and therefore

\[
q_n-q_u=U-D=E-2D
\ge\alpha_sE-\frac{2s}{s+1}
\ge\alpha_sE-2. \tag{56.7}
\]

Combining (56.6)--(56.7) gives

\[
q_n\ge q_u+
\alpha_s\frac{n-u-H}{H+1}-2. \tag{56.8}
\]

Now let \(h<n\) be the last post-entry index with \(M_sq_h>h\), and set
\(u=h+1\). If such \(h\) exists, then

\[
q_u\ge q_h-1>\frac{h}{M_s}-1
>\frac{u}{M_s}-2.
\]

Condition (56.1) gives \(1/M_s\ge\alpha_s/(H+1)\), so

\[
q_u>\alpha_s\frac{u}{H+1}-2.
\]

Substitution in (56.8) yields

\[
q_n>\alpha_s\frac{n}{H+1}-5.
\]

If no such \(h\) exists, take \(u=n_0\) in (56.8) and use
\(q_{n_0}\ge0\). Since \(H/(H+1)<1\), this gives the common weakening
(56.2).

For a counterexample, fix \(s\). Condition (56.1) holds for every
sufficiently large \(n\). Multiplying (56.2) by
\(\log_2n/n\) and taking the lower limit gives

\[
\liminf_{n\to\infty}\frac{q_n\log_2n}{n}\ge\alpha_s.
\]

This holds for every fixed \(s\ge2\), and
\(\sup_s\alpha_s=1\), proving (56.3). Finally
\(b_n=nq_n+r_n\ge nq_n\), which proves (56.4). \(\square\)

## Significance and limitation

Theorem 56 removes the factor-three loss from Theorem 27 and makes the
sharp monotone-tail constant of Theorem 45 unconditional for every
counterexample. It still does not force absorption: growth on the
\(n/\log n\) scale is compatible with both unresolved branches.
