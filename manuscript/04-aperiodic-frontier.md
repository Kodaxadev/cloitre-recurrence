# 4. The aperiodic frontier

Theorem 38 excludes eventually periodic nonzero digit words. It does not
exclude genuinely aperiodic dynamics.

## Theorem 39 (future-digit identity)

At every index \(N\),

\[
e_N=\sum_{k=0}^{\infty}
\frac{a_{N+k}(N+k+2)}{2^{k+1}}. \tag{4.1}
\]

### Proof

Unrolling (1.2) through \(L\) steps and dividing by \(2^L\) gives

\[
e_N=
\sum_{k=0}^{L-1}
\frac{a_{N+k}(N+k+2)}{2^{k+1}}
+\frac{e_{N+L}}{2^L}.
\]

The state window gives \(|e_{N+L}|\le N+L\), so the final term tends to
zero. The same linear-over-exponential estimate gives absolute convergence.
\(\square\)

## Lemma 40 (eventually no-down tails)

Suppose an orbit never absorbs and has no quotient down-step from index
\(N\) onward. Then for every \(n\ge N\),

\[
e_n>0,\qquad a_n\in\{0,1\},\qquad
e_{n+1}=2e_n\bmod(n+2),
\]

where the remainder is positive, and

\[
2e_n<n+1-q_n
\quad\text{or}\quad
2e_n>n+2. \tag{4.2}
\]

### Proof

If \(e_n<0\), an up-step is impossible. Consecutive zero-steps would
double this negative integer while \(q_n\) remained fixed, eventually
violating \(e_n\ge-q_n\); hence a down-step would be forced. Since
\(e_n=0\) is absorption, an infinite no-down tail must have \(e_n>0\).

Its digits are therefore zero or one. A positive up-step satisfies

\[
e_{n+1}=2e_n-(n+2)>0,
\]

equivalently \(2e_n>n+2\). A safe zero-step requires its transition
numerator to remain below the up threshold:

\[
q_n+2e_n<n+1.
\]

These are exactly the two inequalities in (4.2), and both agree with
least-positive-residue doubling. The omitted middle interval produces
either nonpositive \(e_{n+1}\) or capture. \(\square\)

## Lemma 41 (quotient-zero dominance)

Fix an index \(N\) and \(0<e<N\). If the valid state \((N,q,e)\) has a
positive no-down continuation, then \((N,0,e)\) has the same digit and
\(e\) sequence for at least as long.

### Proof

By Lemma 40, a positive up-step is characterized by
\(2e>N+2\), independently of \(q\). A zero-step for the larger quotient
satisfies \(q+2e<N+1\), which remains true after replacing \(q\) by zero.
Induction gives the same pure doubling choices and \(e\)-values, while
the quotient difference remains constant. \(\square\)

## Lemma 42 (two-counter safe map)

Start the dominant path at index \(N\) with quotient zero. Let \(U,Z\)
count its up and zero digits, and define

\[
n=N+U+Z,\qquad w=n-U=N+Z.
\]

Every positive safe transition is exactly

\[
\begin{array}{rcll}
(e,w,U)&\mapsto&(2e,w+1,U),&2e\le w,\\
(e,w,U)&\mapsto&(2e-w-U-2,w,U+1),&2e>w+U+2.
\end{array} \tag{4.3}
\]

If neither condition holds, the positive no-down continuation terminates.

### Proof

Along this path \(q=U\). A safe zero-step is

\[
U+2e<n+1,
\]

which, by integrality and \(n=w+U\), is \(2e\le w\). It doubles \(e\)
and increments \(w\). A positive up-step is
\(2e>n+2=w+U+2\); it subtracts \(n+2\), increments \(U\), and leaves
\(w=n-U\) unchanged. The remaining strip is exactly the interval omitted
by Lemma 40. \(\square\)

## Lemma 43 (binary-Euclidean form)

Put \(h=w-e\). Then \(e,h>0\), and (4.3) is equivalent to

\[
\begin{array}{rcll}
(e,h,U)&\mapsto&(2e,h-e+1,U),&e\le h,\\
(e,h,U)&\mapsto&(e-h-U-2,2h+U+2,U+1),&e>h+U+2.
\end{array} \tag{4.4}
\]

The terminating gap is

\[
h<e\le h+U+2. \tag{4.5}
\]

### Proof

Substitute \(w=e+h\) into both conditions and updates in (4.3). For a
zero-step,

\[
h'=w+1-2e=h-e+1.
\]

For an up-step,

\[
e'=e-h-U-2,\qquad h'=w-e'=2h+U+2.
\]

The gap between their conditions is (4.5). \(\square\)

## Lemma 44 (wrap-run doubling)

On a positive no-down segment put \(h_n=n-r_n\). If \(k\) consecutive
up-steps begin at index \(n\), then

\[
h_{n+k}+q_{n+k}+3=2^k(h_n+q_n+3)
<n+k+3. \tag{4.6}
\]

### Proof

At one positive up-step,

\[
q'=q+1,\qquad e'=2e-(n+2),\qquad
h'=n'-q'-e'=2h+q+2.
\]

Thus \(h'+q'+3=2(h+q+3)\), proving the equality by induction.
During the run \(n-q\) is constant and \(e>0\), hence
\(h<n-q\); this gives the strict inequality in (4.6). \(\square\)

## Theorem 45 (growth on a monotone escape)

Suppose a nonabsorbed orbit has no down-step at digit indices in
\([N,n)\). If \(L=\lfloor\log_2n\rfloor\), then

\[
q_n-q_N\ge\frac{n-N-L}{L+1}. \tag{4.7}
\]

An eventually nondecreasing counterexample would therefore satisfy

\[
\liminf_{n\to\infty}\frac{q_n\log_2n}{n}\ge1,\qquad
\liminf_{n\to\infty}\frac{b_n\log_2n}{n^2}\ge1. \tag{4.8}
\]

### Proof

Let \(P=q_n-q_N\) count up-steps, and let \(Z\) count zero-steps.
There are at most \(P+1\) zero runs, each of length at most \(L\) by
Lemma 26. Hence

\[
n-N=P+Z\le P+(P+1)L,
\]

which is (4.7). For fixed \(N\), multiply the resulting lower bound on
\(q_n/n\) by \(\log_2n\) and pass to the limit inferior. Since
\(b_n\ge nq_n\), (4.8) follows. \(\square\)

## Exact unresolved statement and its limitation

The following would eliminate eventually no-down counterexamples:

> For every \(N\ge2\) and \(1\le e<N\), the map (4.3) eventually enters
> its terminating middle strip.

This statement is not equivalent to the original conjecture. Even if proved,
a nonstabilizing orbit with infinitely many down-steps would remain possible.
