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

## Theorem 46 (checkpoint monotonicity)

Let \(P(N)\) mean that every quotient-zero safe-map start
\((N,0,e)\), \(1\le e<N\), terminates. Then

\[
P(N+1)\Longrightarrow P(N).
\]

Equivalently, if an infinite quotient-zero safe path exists at one index,
one exists at every later index.

### Proof

After one step, an infinite path from \((N,0,e)\) gives an infinite positive
no-down continuation from a valid state \((N+1,q',e')\). Lemma 41 replaces
that state by \((N+1,0,e')\) without shortening the continuation. Thus
failure at \(N\) implies failure at \(N+1\); take the contrapositive.
\(\square\)

Consequently, the independently certified statement \(P(10^6)\) also proves
\(P(N)\) for every \(2\le N\le10^6\). Lemma 41 extends this conclusion to
every valid positive state at those indices. More generally, it is enough
to prove \(P(N)\) on an unbounded sequence of checkpoints.

## Lemma 47 (signed-distance form)

In the coordinates of Lemma 43 put

\[
H=h+U+2,\qquad s=e+H=n+2,\qquad x=H-e+1=s+1-2e.
\]

Then the two safe branches are

\[
\begin{array}{rcll}
(s,x,U)&\mapsto&(s+1,2x-s,U),&x\ge U+3,\\
(s,x,U)&\mapsto&(s+1,2x+s,U+1),&x\le0,
\end{array} \tag{4.9}
\]

and termination is exactly \(1\le x\le U+2\). Moreover,
\(|x|<s\) and \(x\equiv s+1\pmod2\).

### Proof

The zero condition \(e+U+2\le H\) is \(x\ge U+3\), and its update gives
\[
x'=(H-e+1)-2e+1=2x-s.
\]
The wrap condition \(e>H\) is \(x\le0\), and its update gives
\[
x'=(2H+1)-(e-H)+1=2x+s.
\]
The terminating gap \(H-U-2<e\le H\) becomes
\(1\le x\le U+2\). The final assertions follow immediately from
\(e,H>0\) and \(x=s+1-2e\). \(\square\)

## Corollary 48 (parity of a least safe-map failure)

If \(P(N)\) fails and \(N_*\) is the least failing index, every infinite
quotient-zero witness at \(N_*\) has odd \(e\). If \(N_*\) is odd, such a
witness is unreachable from an original start \(b_1=m\).

### Proof

An even witness \(e\) has the valid predecessor
\((N_*-1,0,e/2)\), whose first safe zero-step reaches
\((N_*,0,e)\), contradicting minimality. At odd \(n\), Corollary 9 gives
even \(b_n\), while \(b_n-e_n=q_n(n+1)\) is even. Thus every reachable
\(e_n\) is even at an odd index. \(\square\)

The even-index least-failure case remains open; the next two results isolate
the exact boundary mechanism that such a failure must use.

## Lemma 49 (quotient clearance)

Along a quotient-zero safe path, define at every zero step

\[
\sigma_n=n-U_n-2e_n\ge0.
\]

A valid path begun with initial quotient \(Q\ge0\) follows the same digits
and \(e\)-values through a prefix exactly when \(\sigma_n\ge Q\) at every
zero step in that prefix.

### Proof

While the paths agree, their quotients differ by \(Q\). Wraps depend only
on \(2e_n>n+2\). A zero remains safe exactly when
\(U_n+Q+2e_n<n+1\), equivalently \(\sigma_n\ge Q\). Induct.
\(\square\)

## Theorem 50 (boundary at an even least failure)

If \(N_*\) is the least failing checkpoint and is even, every infinite
witness satisfies

\[
e\ \text{odd},\qquad 2e\le N_*,
\]

and its path has a zero step satisfying \(n-U_n-2e_n=0\).

### Proof

The cases \(N_*\le6\) terminate directly, and Corollary 48 makes \(e\)
odd. If the first step wraps, set \(f=e-(N_*+2)/2\). Then
\((N_*,1,f)\) zero-steps to the same next state. If \(f\) is even, it is
dominated by the image of \((N_*-1,0,f/2)\); if \(f\) is odd, it is the
wrap image of
\[
\left(N_*-1,0,\frac{f+N_*+1}{2}\right).
\]
Both contradict minimality. Thus \(2e\le N_*\).

If every zero slack were at least one, Lemma 49 would give the same
infinite path from \((N_*,1,e)\). Since \(e\) is odd, this state is the
wrap image of
\[
\left(N_*-1,0,\frac{e+N_*+1}{2}\right),
\]
again a contradiction. Hence some zero slack is zero. \(\square\)

## Exact unresolved statement and its limitation

The following would eliminate eventually no-down counterexamples:

> For every \(N\ge2\) and \(1\le e<N\), the map (4.3) eventually enters
> its terminating middle strip.

This statement is not equivalent to the original conjecture. Even if proved,
a nonstabilizing orbit with infinitely many down-steps would remain possible.
