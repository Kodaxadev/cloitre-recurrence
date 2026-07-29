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

Lemma 87 now eliminates three consecutive uses of the parent boundary:
the only compatible triple is an explicit terminal path. More strongly,
Corollary 88 observes that any failure of

\[
D+r-3<2^{r+5}
\]

forces this inequality at the next unique gate. Thus it holds at least once
every two gates of a continuing unique unit-wrap chain.
**Do:** combine these frequent logarithmic zero-only gaps with the exact
successor residues, rather than only their lengths. Their frequency alone
still permits the \(n/\log n\) quotient scale required by Theorem 45.
Corollary 89 makes this compatibility quantitative: a hypothetical
all-unit, all-unique tail must have \(D_j\ge(1/2-o(1))j\log_2j\) and quotient
scale between constants \(1\) and \(2\) times \(n/\log_2n\).
Theorem 90 closes that constant gap: non-short gates would force
\(U\ge D/2\), contradicting Corollary 89's \(U/D\to0\). Hence every late
gate is short and any surviving all-unit/all-unique tail must satisfy

\[
D_j\sim j\log_2j,\qquad
\frac{U_j\log_2n_j}{n_j}\to1.
\]

**Do:** analyze the equality case of Theorem 45. A contradiction can no
longer come from first-order density in this subcase; it must use the exact
residues or a second-order loss from the moving logarithmic zero-run ceiling.

Theorem 91 completes that equality-case analysis for an all-unit/all-unique
tail. It proves \(L-5\le r\le L\), bounds the positive excess by \(47\), and
uses the resulting finite affine-dyadic forms to contradict unavoidable
same-epoch pairs. The eventual-no-down branch is therefore reduced further:

> infinitely many blocks have length at least two, or infinitely many gates
> are nonunique.

**Do:** treat these two alternatives quantitatively. For longer blocks,
combine the extra wrap count with the exact parent equation. For nonunique
gates, accumulate \(2^{k+r+3}<G+r-3\) rather than bounding isolated gaps.

Lemma 92 now puts both alternatives in one exact boundary language. With

\[
x=2^{r+2}f-m-r-3,\qquad H=2^{k+r+3},
\]

nonuniqueness is equivalent to

\[
x>H\quad\text{or}\quad(d\ge2\text{ and }2d'\ge H).
\]

**Do:** classify consecutive unique gates in the parent layer \(d\le1\)
for arbitrary \(k\). A bounded affine search through
\(k,k',r,r'\le16\) finds only three patterns, but no uniform parameter
bound is proved. Corollary 95 eliminates a hidden singular family: every
fixed tuple has at most one rational start. The task is therefore to bound
the unbounded parameters themselves. In the complementary interior layer,
accumulate the sharp inequality \(G+r-3<2^{k+r+4}\) together with the
block-count lower bound.

Lemma 96 now proves that consecutive parent-boundary starts have
\(k_{j+1}\le k_j\), even without uniqueness. Thus a persistent parent-layer
tail has one eventual block length \(k\). **Do:** fix that \(k\), write
\(A_j=A_0+jk+d_j-d_0\), and combine the divisibility

\[
2^{r_j+1}-1\mid
(2^k-1)A_j+r_j-k+d_j+1-d_{j+1}
\]

with the exact uniqueness boundary. The remaining parameters are the gaps
\(r_j\) and the two defect bits, not the block lengths.
A bounded affine scan through \(k,r_j\le12\) finds no four-start
constant-length parent-layer pattern, but a proof must control unbounded
gaps rather than extrapolate from that search.

Theorem 99 proves exactly why a bounded search cannot finish this branch:
any surviving fixed-\(k\) parent tail must have unbounded gaps, although

\[
r_j\le\log_2 A_j+O_k(1),\qquad
K\le\liminf\frac1J\sum_{j<J}r_j
\le\limsup\frac1J\sum_{j<J}r_j\le2K+1.
\]

**Do:** exploit the rare large-gap indices. Equation (98.3) makes each such
gap a positive jump of the returned residue, while (98.2) simultaneously
divides that residue by \(2^{r_j+1}-1\). A contradiction must compare a
large gap with the accumulated budget before and after it, rather than use
only its pointwise logarithmic ceiling.

Lemma 100 and Theorem 101 complete that comparison: equal gaps are singular,
decreasing gaps violate an exact power-of-two divisibility, and strictly
increasing gaps contradict Theorem 99's bounded mean. The parent boundary
cannot persist.

**Do:** work only with the exhaustive alternatives in Corollary 102. At
infinitely many interior starts \(d\ge2\), either the gate is nonunique or
uniqueness forces the child boundary

\[
2d'<2^{k+r+3}.
\]

Lemma 103 and Corollary 104 combine these into one exact test. With
\(H=2^{k+r+3}\) and the explicit canonical origin \(\rho_{k,r}(n)\), an
interior gate is unique exactly when

\[
\rho\le D'-3<\rho+H;
\]

a miss into any later translate is exactly nonuniqueness. Corollary 105 says
the origin permutes all dyadic residues for fixed \(k,r\), but it does not
give equidistribution along the dependent orbit.

**Do:** derive an inter-gate law for the window displacement
\(D'-3-\rho\). Show either that repeated first-window hits force a forbidden
parameter repetition/periodicity, or that later-window misses occur with a
frequency that can be accumulated across Corollary 82's frequent positive
blocks.

Lemma 106 supplies the first inter-gate law:
\(2A'=n'+5-\rho\), so the child block is unit exactly when
\(2\rho\le n'+4\). Corollaries 107--108 sharpen the exhaustive frontier.
Every infinite safe path has infinitely many nonunique gates, or infinitely
many unique longer-child gates whose gaps satisfy

\[
\frac r{\log_2n'}\longrightarrow1.
\]

Corollary 109 shows that the latter reset gates number only
\(O(N/\log N)\) through index \(N\). Their zero density in absolute time does
not make them finite or sparse among positive blocks.

Lemma 110 now counts every locally valid gate state exactly:

\[
|\mathcal F|
=1+j+\min\!\left(\lfloor d/2\rfloor,\lfloor2d'/H\rfloor\right).
\]

Thus every later-window translate creates a lower candidate. Only
displacement stored in the child defect can be absorbed by finite parent
defect headroom.

Lemma 113 now supplies the missing inter-gate transfer: the child excess
determines its returned residue, and equals it for a unit child. Consecutive
unit blocks therefore obey

\[
f_{i+1}=2^{r_i+2}f_i-n_i-r_i-5.
\]

The pure-upper subcase has an exact inequality test, but a literal safe path
already contains six consecutive pure-upper gates. Fixed short-transience
and simple defect monotonicity are therefore false.

Theorem 118 now controls the asymptotic scale of the hypothetical infinite
all-unit pure-upper case:

\[
\frac12\le\liminf\frac{n_J}{J\log_2J}
\le\limsup\frac{n_J}{J\log_2J}\le1.
\]

Equivalently, adjacent gaps must repeatedly supply logarithmic size, while
the quotient ratio stays in the nondegenerate window \([1,2]\). This matches
the critical safe-map scale rather than contradicting it.

**Do next:** use the exact returning-unit test of Lemma 117 to eliminate
\((e,d)\) and analyze the remaining integer recurrence in \((n,U,f,r)\).
The target is a second-order obstruction coupling three or more gaps, not
another one-gap ceiling. In the mixed-block case, treat near-maximal unique
gaps as renewal points and accumulate both headroom terms from Lemma 110.

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
