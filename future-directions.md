# Future directions

Ordered by my estimate of value per unit effort. Each entry says what to do and
what would count as success, because "study X further" is not a direction.

---

## 1. Formalize Theorem 18 (highest value, clearly finite effort)

Corollary 20 — the answer to Abercrombie's question — currently rests on a
paper proof plus an exhaustive computation. The paper proof is short and was
tested against 200,000 orbits including every intermediate link, but it is not
machine-checked.

**Do:** port `lean/Conjecture.lean` into a `lake` project with mathlib, then
formalize in order: Lemma 4 (bounded quotient, pure case analysis on $2r-q$),
Lemma 12, Theorem 13, Theorem 14 (the two-clause induction is already written out
in `partial-proofs.md` §5), Lemma 3, then Theorem 18.

**Success:** `theorem increment_bounds_start : c(m) = c → m < (3*c+5)^2` with no
`sorry`. Then a verified finite checker over $m < (c+3)(3c+5)$ would make "5 is never
an eventual increment" end-to-end machine-checked — a fully formal answer to a
published open question, which is publishable on its own.

## 2. Sharpen Theorem 18 further — *(first round already DONE)*

The original chain proved $m<(3c+5)^2$ by way of $b_{n^*}<(n^*)^2$. That threw
away a factor ~3, because $q_{n^*}\le c+2$ is available and gives
$b_{n^*}=q_{n^*}n^*+r_{n^*}<(c+3)n^*$ directly. **This is now done**: the bound in
`partial-proofs.md` is $m<(c+3)(3c+5)$, verified with 0 violations across all
$10^6$ starts, and it raised the settled range from $c\le1052$ to $c\le1823$ at
zero computational cost.

What remains loose: worst observed $m/\big((c+3)(3c+5)\big)$ is $0.367$, so there
is still a factor ~2.7 in hand, while $n^*/(3c+5)$ reaches $0.936$ and is close to
sharp. So the remaining slack is **not** in the bound on $n^*$ — it is in
$m \le b_{n^*}$, which is very weak for small $m$ (the orbit grows a lot between
index 2 and $n^*$).

**Do:** bound $b_{n^*}$ downward in terms of $m$ using Lemma 3 — the orbit
increases by $r_k \le k-1$ per step, so $b_{n^*} \le m + (n^*)^2/2$, giving
$m > b_{n^*} - (3c+5)^2/2$ in the useful direction, and combine with
$q_{n^*} > (n^*+1)/3$.

**Success:** a bound of the form $m < \alpha c^2$ with $\alpha < 3$, or a proof
that $\alpha = 3$ is optimal. Each factor of 3 saved extends the settled range of
$c$ by $\sqrt3$ for free.

## 3. Explain the tail exponent $-0.655$

The clearest place where the theory is simply wrong. Naive model: $N^{-1}$.
Refined model (one admissible target, even $n$ only): $N^{-1/2}$. Measured:
$N^{-0.655}$, stable over three decades.

**Do:** (a) measure the exponent over *distinct orbits* from the $10^7$ census and
over starts separately, to isolate how much is clustering; (b) measure the
empirical capture rate directly — count, at each $n$, live orbits versus those
absorbed, and fit $\alpha(n)$ rather than assuming it constant; (c) check whether
the second target ($\kappa \ge 1/2$) is genuinely never available, or available on
a thin set of $n$ that contributes.

**Success:** either a corrected exponent with a derivation, or a demonstration
that the exponent drifts and has no limit. Both are publishable observations, and
this is the kind of question where computation can actually settle things.

## 4. Push verification to $10^8$

Bounded by memory, not by ideas: the sweep needs ~8 bytes per live start, so
$10^8$ needs ~2.4 GB, at an estimated 20–30 minutes.

**Do:** shard the start range and exploit that the live set halves at $n=2$
(Theorem 10) — initialise at index 3 with only the even values, halving peak
memory for free. Then external-memory or streaming for $10^9$.

**Success:** verified range extended another decade, and — more valuable — the
increment spectrum settled for all $c \lesssim 5700$, enough to see whether the
density of unattained increments (5.8% below 1823) converges, drifts, or vanishes.

## 5. Is the set of unattained increments infinite?

New question, opened by Theorem 18. Currently 106 unattained values below 1823,
with the count in $[1,X]$ growing roughly linearly in $X$ so far.

**Do:** compute the density on successive dyadic ranges as the census grows.
Under the $c\gtrsim0.92\sqrt m$ envelope, $c$ is attainable only from
$m\lesssim1.2c^2$ starts, which map onto $O(c)$ distinct orbits — so a Poisson
heuristic predicts a *positive limiting density* of unattained values.

**Success:** a heuristic prediction of the density with a matching measurement.
Proving the set is infinite is probably as hard as the main conjecture; measuring
it is not.

## 6. Equidistribution of $e_n \bmod (n+2)$ — the actual obstruction

By Theorem 2 the conjecture is exactly "every orbit meets a multiple of $n+1$",
and by Theorem 6 the motion between hits is doubling with a **moving modulus**.
Fixed-modulus doubling has a complete equidistribution theory; the moving-modulus
case appears to have none.

**Do:** look for the smallest non-trivial model with the same structure —
$x_{n+1} \equiv 2x_n \pmod{n+c}$ with a window constraint — and ask whether *any*
capture theorem is provable there, even under an extra hypothesis such as $n$
restricted to a sparse set. A negative answer (a constructed non-capturing orbit
in the relaxed model) would be as informative as a positive one, because it would
localise exactly which feature of the real recurrence does the work.

**Success:** a capture theorem for any moving-modulus doubling system, or an
explicit counterexample in the relaxed model.

Theorem 39 and Lemmas 40--41 now make the smallest useful intermediate target
more precise. For a positive no-down tail, start the pure map

```text
e_(n+1)=2e_n mod(n+2)
```

with quotient zero and let `U_n` count wraps. Prove that some zero digit must
satisfy `U_n+2e_n>=n+1`, or that the pure orbit captures. The compressed
`pure --safe-sweep` computation proves this separately at each selected start
index and shows an apparent `O(sqrt(n))` lifetime. A uniform upper bound of any
finite form would rule out eventual monotone escape.

Lemma 80 and Corollary 81 now rule out long wrap blocks as the missing
mechanism: every positive block satisfies \(2^kU<n\), and an infinite safe
path has \(k\le\log_2\log_2n+o(1)\). Corollary 82 also forces at least
\((1-o(1))n/(\log n\log\log n)\) completed positive blocks by a zero epoch.
The remaining target must therefore control the residues of these frequent
aperiodic bounded or slowly growing blocks, rather than force one block to
exceed the state window.

Lemma 83 now supplies the first exact residue gate for that target. If a
positive block of length \(k\) returns with residue \(f\), and \(r\)
zero-only blocks precede the next positive block, then

\[
f\equiv m+3\pmod{2^k},\qquad
\frac{m+r+3}{2^{r+2}}<f\le\frac{m-V+r}{2^{r+1}}.
\]

**Do:** determine whether infinitely many unique gates can be compatible
with the autonomous overshoot map. Use the lifted class modulo \(2^{k+1}\),
not only the displayed weaker congruence. In the nonunique case, exploit
\(2^{k+r+3}<G+r-3\) across the quantitatively frequent blocks from
Corollary 82, rather than treating each gate independently.

For the unit-wrap case, Lemma 85 replaces the gate by the affine
coordinates \((n,D,s)\), and Corollary 86 makes uniqueness equivalent to
explicit lower and upper boundary layers. The bounded search already finds
seven consecutive unique unit-wrap gates, so a useful next argument must
show that those boundary layers cannot be followed indefinitely; a small
constant-chain assumption is not justified.

## 7. Resolve the low-order mixed-ridge defect

Lemma 73 now encodes every zero in an arbitrary ridge by

\[
W=\sum_{i\in\mathcal Z^+}(N+i+2)2^{P-1-i}.
\]

Corollary 74 extracts a modulus from the final positive up-run, and Theorem
75 forces exponential local complexity if those terminal runs grow. Theorem
77 now handles failure of that growth exactly: one fixed terminal length must
recur, forcing infinitely many shadows of its finite dyadic boundary ladder.

**Do:** track the nested low bits of \(W_j\) across repeated visits to the
same dyadic ladder, with reachability parity imposed at each index. In the
growing-run branch, improve Corollary 79's log-log ceiling into upper bounds
for the specific parameters appearing in Theorem 75.

**Success:** exclude recurrent visits to every fixed ladder, or show that the
exponential parameter forced by growing terminal runs exceeds its
state-window bound. A constructed infinite arbitrary-state chain would also
be decisive for understanding whether reachability is essential.

## 8. The general-starting-index question

The conjecture is about orbits from $b_1 = m$. Nothing is known about orbits
started at an arbitrary state $(n_0, b)$. These are *not* all reachable —
Corollary 9 already excludes half of them at odd indices.

**Do:** decide whether some admissible non-reachable state has a non-stabilizing
orbit. §6 of `symbolic-analysis.md` shows the shape is not obstructed (periodic
digit patterns such as $(+1,0,0,0)$ satisfy the window constraint with
$\kappa=1/4$); Theorem 38 now proves that exact integrality obstructs every
eventually periodic pattern.

**Success:** exhibiting a non-stabilizing orbit from *any* starting state would be
a major result — it would show the conjecture is a statement about reachability
from $b_1=m$, not about the recurrence, and would redirect the whole problem.

## 9. The shifted family A074482/3/4

Cloitre's original conjecture was for $b_{n+1} = b_n + (b_n \bmod (n+a))$ for every
integer $a$. Everything in this project was done for $a=0$.

**Do:** re-run the framework with the shift parameter; the $(q,r)$ transition and
the $e$-doubling law both survive with $n+2 \to n+a+2$, so this is mostly
plumbing. Wilson's b-files cover $n=0..10000$ and would be an immediate
cross-check.

**Success:** confirming that Theorem 18 generalises (it should, with $a$-dependent
constants) would answer the coverage question for the whole family at once.

---

## What I would not spend more time on

* **Invariant and Lyapunov searches.** Closed off exactly, not just empirically:
  $e$ doubles, so nothing decreases (Propositions 16, 17, and
  `invariant-search.md`). Further search here is guaranteed waste.
* **Symbolic regression.** The governing law is already in closed form.
* **Larger per-start scans.** Strictly dominated by the compressed sweep at every
  range tested; the only reason to run one is cross-validation, which is done.
* **A direct attack on the conjecture.** `theorem-status.md` §E states the gap:
  an expanding map, a measure-zero target hit with probability one under the
  natural model, and no mechanism forcing an individual orbit to comply. That is
  the Collatz wall, and nothing found here moves it.
