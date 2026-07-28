# 2. Restrictions on a counterexample

Continue with \(a_n=q_{n+1}-q_n\in\{-1,0,1\}\) after entry.

## Theorem 22 (rebound cascade)

Suppose \(a_n=-1\) and put \(h=q_n-2r_n\), so
\(1\le h\le q_n\). After \(k\ge0\) subsequent up-steps, define

\[
\delta_k=(n+1+k)-r_{n+1+k}.
\]

As long as those up-steps occur,

\[
\delta_k=2^k(h+q_n+2)-q_n-k-2. \tag{2.1}
\]

The next step is upward exactly when

\[
n+1\ge2^{k+1}(h+q_n+2)-q_n-2k-4. \tag{2.2}
\]

In particular,

\[
a_n=-1,\quad n\ge7q_n+1
\quad\Longrightarrow\quad
(a_{n+1},a_{n+2})=(1,1). \tag{2.3}
\]

### Proof

The down-step gives

\[
q_{n+1}=q_n-1,\qquad r_{n+1}=n+1-h,
\]

so \(\delta_0=h\). If the next transition is upward, direct substitution
gives

\[
\delta_{k+1}=2\delta_k+q_n+k+1.
\]

Solving this recurrence proves (2.1). At index \(N=n+1+k\), the condition
for an up-step is \(2r_N-q_N\ge N+1\). Substitution of (2.1) yields
(2.2). Since \(h\le q_n\), the first \(s\) up-steps are forced by

\[
n+1\ge(2^{s+1}-1)q_n+2^{s+1}-2s-2.
\]

Taking \(s=2\) proves (2.3). \(\square\)

## Corollary 23 (bounded quotient forces stabilization)

If \((q_n)\) is bounded, then the orbit stabilizes.

### Proof

Assume \(q_n\le Q\) eventually. Once \(n\ge7Q+1\), every down-step begins
a disjoint three-step block consisting of one down-step followed by two
up-steps. Each block has net quotient gain one, and every step outside the
blocks is zero or upward. Infinitely many down-steps would contradict
boundedness.

There are therefore finitely many down-steps. Boundedness then permits only
finitely many up-steps because

\[
q_n=q_N+\#\{\text{up}\}-\#\{\text{down}\}.
\]

Thus \(q_n\) is eventually constant. Equation (1.2) then gives
\(e_{n+1}=2e_n\). The state window

\[
-q_n\le e_n\le n-1-q_n
\]

is only linear in \(n\), so a nonzero integer cannot double forever inside
it. Hence \(e_n=0\) at some index, which is absorption. \(\square\)

## Theorem 24 (quotient dichotomy)

Every orbit either stabilizes, or \(q_n\to\infty\).

### Proof

A nonstabilizing orbit has unbounded quotient by Corollary 23. Suppose it
does not tend to infinity. Then some fixed \(Q\) satisfies \(q_n\le Q\)
at arbitrarily large indices.

For each such \(n\), let \(s\) begin the final interval ending at \(n\)
on which \(3q_k\le k+1\). If this is not the original entry index, then
\(3q_{s-1}>s\), so

\[
q_s\ge q_{s-1}-1>s/3-1.
\]

The ratchet theorem yields

\[
Q\ge q_n\ge q_s-1>s/3-2.
\]

Thus all such window starts are bounded. Since indices with \(q_n\le Q\)
occur arbitrarily far out, no index satisfying \(3q_k>k+1\) can occur
beyond a fixed bound. The entire tail is therefore in the ratchet regime.

Starting the ratchet at any tail index \(j\) gives
\(q_k\ge q_j-1\) for every \(k\ge j\). Unboundedness now implies that for
every \(H\), some \(j\) has \(q_j\ge H+1\), after which \(q_k\ge H\).
Thus \(q_n\to\infty\), a contradiction. \(\square\)

## Lemma 26 (zero-run bound)

Before absorption, a run of \(L\) consecutive zero digits ending by index
\(N\) satisfies

\[
L\le\lfloor\log_2N\rfloor.
\]

### Proof

During a zero run, \(e\) doubles. If it starts at \(j\), then
\(e_{j+L}=2^Le_j\). Nonabsorption makes \(|e_j|\ge1\), while the state
window gives \(|e_{j+L}|\le j+L\le N\). Hence \(2^L\le N\). \(\square\)

## Theorem 27 (quantitative growth before absorption)

Let \(n_0\) be the entry index. At every nonabsorbed index
\(n\ge\max(n_0,4)\),

\[
q_n\ge
\frac{n}{3(\lfloor\log_2n\rfloor+1)}
-\frac{n_0}{3}-3. \tag{2.4}
\]

Consequently, every counterexample satisfies

\[
q_n=\Omega_m(n/\log n),\qquad
b_n=\Omega_m(n^2/\log n). \tag{2.5}
\]

### Proof

Set \(H=\lfloor\log_2n\rfloor\). First consider an interval
\([u,n)\) on which \(8q_k\le k\). Let \(E\) and \(Z\) be its numbers of
nonzero and zero digits. There are at most \(E+1\) zero runs, so Lemma 26
gives

\[
n-u=E+Z\le E(H+1)+H,\qquad
E\ge\frac{n-u-H}{H+1}. \tag{2.6}
\]

Every down-step in this interval satisfies the hypothesis of (2.3), except
that a down-step is already impossible when \(q_k=0\). The resulting
down-up-up blocks are disjoint; at most one is cut by the right endpoint.
If \(U,D\) count up- and down-steps, then

\[
U\ge2D-2,\qquad
q_n-q_u=U-D=E-2D\ge\frac{E-4}{3}. \tag{2.7}
\]

Combining (2.6) and (2.7),

\[
q_n\ge q_u+\frac{n-u-H}{3(H+1)}-\frac43. \tag{2.8}
\]

Choose \(u\) immediately after the last \(h<n\) with \(8q_h>h\), or set
\(u=n_0\) if no such index occurs after entry. In the first case,

\[
q_u\ge q_h-1>\frac{u}{8}-\frac98.
\]

Because \(H\ge2\), \(1/8\ge1/[3(H+1)]\); substitution in (2.8) gives the
stronger bound \(q_n\ge n/[3(H+1)]-3\). In the second case, (2.8) gives
\(q_n\ge n/[3(H+1)]-n_0/3-2\). Their common weakening is (2.4).
Finally, \(b_n\ge nq_n\), proving (2.5). \(\square\)

These theorems constrain every counterexample at every sufficiently large
index. They do not prove that down-steps cease, that \(q_n/n\) stays bounded
away from zero, or that the absorbing state is reached.
