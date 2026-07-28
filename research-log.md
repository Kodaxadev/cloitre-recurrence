# Research log

Chronological, including the dead ends and the one place I broke my own test.

---

### 1. Orientation and literature (first pass)

Identified the problem as OEIS **A073117** by searching the $m=1$ orbit
`1,1,2,4,4,8,10,13,18,18,26,30,36,46`. From there the reference set fell out
quickly: A117846 (the conjecture in the exact form given in the brief), A074482/3/4
(shifted-modulus family), A066910 (first differences). One MathOverflow thread
(191518). arXiv and Crossref: **zero hits**.

Conclusion: the conjecture is genuinely open, first stated by Cloitre in 2002 with
the parenthetical "seems provable", restated by Abercrombie in 2007. Full details
and attribution split in `literature-review.md`.

Two things in the literature changed how I planned the work:

* A 2025 MathOverflow answer already contains the divisibility criterion, the
  merge criterion, and the $n^2/4$ growth law. So those are **not** new, and I
  reproved them rather than claiming them.
* A117846 contains a *second*, separate open question — "Do the values a(n)
  include all positive numbers?" — that nobody appears to have attacked. I filed
  that as a target because it looked more tractable than the main conjecture.

### 2. Deriving the state coordinates before writing any code

Worked out the $(q,r)$ transition equations by hand and noticed that with
$d = 2r-q$ the bounds $-(n{+}1) < d < 2(n{+}1)$ hold whenever $q\le n$. That makes
the modular reduction a single conditional add/subtract — **the whole iteration is
division-free**. This is a 3.6× speedup and it decided the architecture.

Then substituted $e = r - q$ and got

$$e_{n+1} = 2e_n - \Delta q_n (n+2)$$

which is the entire dynamics in one line, and shows the absorbing state is a
*repelling* fixed point of a doubling map. At that point I expected all Lyapunov
and invariant searches to fail, and said so in advance. They did.

Hand-checked on $m=5$: $e$ ran $-1, -2, 1, 2, 4, 0$ against moduli $4,5,6,7,8$,
capturing at $n=7$ with $c=2$ and $b_7 = 16 = 2\cdot 8$. Matched a Python
brute force exactly.

### 3. Framework, and the tests that mattered

Zero-dependency Rust. The test suite was written to be adversarial rather than
confirmatory: every lemma is checked against a naive implementation of the literal
definition, and the OEIS data is used as ground truth (all 68 published terms of
A117846, both parities; A073117's $a(397)=38606=398\cdot97$).

`consecutive_step_bounds` asserts that both patterns actually occur before
checking them, so the test cannot pass vacuously. That habit caught nothing here
but was cheap.

### 4. Reproducing the stated baseline

Scan of $m \le 200{,}000$: **21.5 s**, 0 unresolved, longest $t = 9{,}363{,}863$ at
$m = 31{,}873$ with $c = 2{,}341{,}202$. Exactly the numbers in the brief. Treated
as confirmed only after the independent `u128` verifier reproduced all 200,000 rows
from the literal definition (0 failures) and a Python arbitrary-precision checker
re-derived a seeded sample.

Noticed immediately that $c/t = 0.250025$. That is the $n^2/4$ law, and it made
the reported baseline self-consistent — a useful sanity signal *before* trusting it.

### 5. Compression — the part that worked

Rather than scanning further, exploited that the forward map is at most 2-to-1
(Theorem 11) by advancing the **set** of live values in lockstep over $n$. Key
implementation point: images of block $k$ land in $[kn,(k+2)n)$, so only adjacent
blocks interleave and a rolling two-way merge restores sorted order in $O(L)$
instead of $O(L\log L)$.

Results: $10^7$ starts verified in **149 s**, versus roughly $10^{12}$ iterations
for the per-start method. Compression 313× → 363× → 608× → ~1900× as $M$ grows.
Ten million starts collapse to **9,911 distinct orbits**.

New record found: $t = 327{,}695{,}231$ at $m = 1{,}320{,}111$, with
$c = 81{,}923{,}126$ and $c/t = 0.249998$ — 35× beyond the previous record.

Dead ends recorded in `compressed-orbit-analysis.md` §6: interval propagation
(fragments as soon as absorbed points are removed), symbolic/residue states (no
modulus works — see below), backward trees (they *branch*, average ~1.5).

### 6. Epoch analysis — the unexpected result

Analysing only quotient-change moments produced a transition matrix that is not
i.i.d.:

```
from -1 -> (0.00001, 0.00008, 0.99991)
from  0 -> (0.12504, 0.49990, 0.37506)
from +1 -> (0.16681, 0.66679, 0.16641)
```

I derived $(\tfrac18,\tfrac12,\tfrac38)$ and $(\tfrac16,\tfrac23,\tfrac16)$ from
equidistribution, and they matched to four decimals. The first row is not a
heuristic at all — it is forced. Chasing why produced **Theorem 13**: if
$\Delta q_n = -1$ and $3q_n \le n+1$ then $\Delta q_{n+1} = +1$, unconditionally.

The stationary vector of the predicted matrix is exactly $(\tfrac18,\tfrac12,\tfrac38)$
and gives $\mathbb E[\Delta q] = \tfrac14$, self-consistently reproducing $\kappa=1/4$.

### 7. From a forced move to a theorem

Theorem 13 iterated gives the **ratchet** (Theorem 14): while $3q \le n+1$, the
quotient never falls more than 1 below where it has been, and every dip is undone
on the next step. That is the only monotonicity in this system.

The consequence took a while to see: run the ratchet *backwards* from the
absorbing index. It bounds $q$ at the last index where $3q > n+1$, which bounds
that index by $3c+5$; the quotient bound $q\le c+2$ then bounds $b$ there by
$(c+3)(3c+5)$ — and $b$ is non-decreasing, so it bounds $m$.
**Theorem 18: $c(m)=c \Rightarrow m<(c+3)(3c+5)$.**
(My first version used the cruder $b<(n^*)^2$ and got $(3c+5)^2$; sharpening it
was free and raised the range of $c$ settled below from 1052 to 1823.)

This converts "is $c$ ever an eventual increment?" from an infinite question into
a finite one. Combined with the exhaustive $10^7$ census: exactly **106** of the
increments $1..1823$ never occur, smallest $5$ and $7$. That answers Abercrombie's
2007 question in the negative, unconditionally — it does not assume the
stabilization conjecture.

Before believing it I tested the bound and *every intermediate link of the proof
chain* against $10^6$ orbits: 0 violations, worst $m/\big((c+3)(3c+5)\big) = 0.367$, worst
$n^*/(3c+5) = 0.936$. That last number is what convinced me — the bound is nearly
attained, so it is not vacuously true.

### 8. Invariant search — comprehensive negative results

All 17 candidate potentials rejected, each failing on 36–64% of 2.17M sampled
transitions. Affine Lyapunov functions ruled out *exactly* (not statistically) by
reducing to convex-hull feasibility in three variables: 0 feasible directions.
No modulus in $[2,64]$ gives a well-defined induced map.

None of this was surprising given §2 — $e$ doubles, so nothing decreases. The
value is in having it on record with explicit witnesses.

### 9. Where the heuristic broke

The naive model predicts $\Pr[t>N]\sim N^{-1}$; my refined version (one admissible
target, even indices only) predicts $N^{-1/2}$. **Measured: $N^{-0.655}$.** Neither
is right. Recorded as a refutation rather than smoothed over; the likely causes
(merging correlates trials; $\kappa$ fluctuates) are written up in
`symbolic-analysis.md` §5 as an open problem.

### 10. Formalization

Installed Lean 4.32.1 rather than shipping unchecked proof scripts. Wrote the
formalization mathlib-free so it verifies with a bare `lean` invocation.
Compiles clean; the axiom audit shows no `sorryAx` anywhere. Theorems 13/14/18 are
deliberately *not* formalized — they need real case analysis and would want
mathlib; claiming them in Lean without checking them would be worse than not
doing it.

---

## Mistakes and corrections

* **I fabricated test data and my own verifier caught it.** Building a
  spot-check file for the top-3 record orbits, I typed the $b_t$ values for rows 2
  and 3 by hand instead of reading them from the census. The independent verifier
  rejected both rows. The $t$ values it recomputed matched the census exactly, so
  the framework was fine and my input file was wrong — but this is precisely the
  failure mode that a verifier which only re-checked internal consistency would
  have missed. Redone by extracting rows programmatically; all 10 then passed.
* **Wrote a 5.5 GB CSV by accident.** The sweep logged every index; at
  $M=10^7$ that is 327 million rows. Replaced with `--every` sampling and deleted
  the oversized artifacts.
* **Over-read one statistic.** The pooled-ensemble $\chi^2$ for $r/n$ uniformity
  is ~3300, which looks like a decisive rejection of equidistribution. It is an
  artefact of pooling short orbits at small $n$; the single-long-orbit test gives
  $\chi^2 = 13.4$ on 19 df. Both numbers are reported rather than just the
  convenient one.
* **Initial Lean attempt used mathlib tactics** (`ring`, `linarith`, `push_cast`)
  that do not exist in a bare toolchain. Rewritten with explicit distributivity
  lemmas; the `Nat`-only form of Theorem 6 that this forced is actually a cleaner
  statement than the `Int` one.

## What I did not do

* No zbMATH/MathSciNet search (subscription-only here). arXiv and Crossref were
  both empty, so the risk of a missed paper is low but not zero.
* No verification beyond $m = 10^7$. The next natural step, $M=10^8$, needs ~2.4 GB
  and roughly 25 minutes — it is bounded by memory, not by ideas.
* No symbolic regression. The exact governing law is already known in closed form
  (Theorem 6), so regression could only rediscover it, and the space of monotone
  candidates had already been closed off exactly.
* **No progress on the conjecture itself.** Every structural result here
  constrains the dynamics without forcing capture, and `theorem-status.md` §E says
  precisely why the remaining gap is Collatz-hard.

---

### 11. Continuation: entry ridge and rebound cascade

Re-examining the entry lemma exposed a reachability constraint that the first
pass had left on the table. At the first index $n_0\ge3$ with
$b_{n_0}<n_0^2$, monotonicity and minimality give

$$(n_0-1)^2\le b_{n_0}<n_0^2,$$

so $q_{n_0}$ is exactly $n_0-2$ or $n_0-1$. Every reachable orbit therefore
enters the division-free regime on its top two quotient levels.

The forced rebound also extends exactly. If a down-step has
$h=q_n-2r_n>0$, then after that step and $k$ subsequent up-steps, the deficit
from the top of the remainder window is

$$\delta_k=2^k(h+q_n+2)-q_n-k-2.$$

This gives a closed condition for every further up-step. In particular,
$n\ge7q_n+1$ makes a down-step force two up-steps, for a net gain of one.
It follows that a bounded quotient permits only finitely many down-steps and
up-steps; the quotient is then constant, $e$ doubles forever, and the linear
state window forces $e=0$. Therefore **every bounded-quotient orbit
stabilizes**, and any counterexample must have unbounded quotient.

Combining this with the ratchet strengthens "unbounded" to
**$q_n\to\infty$**. If a fixed band $q\le Q$ were revisited arbitrarily late,
the last low-regime window leading to each visit would have to start before
$3(Q+2)$. Hence the whole tail would eventually stay in the ratchet regime.
Starting the ratchet at successive record values would then force $q_n\to
\infty$, contradicting those returns. The resulting dichotomy is: stabilization
with eventually constant quotient, or divergent quotient and superlinear
$b_n$.

The complete proof and its explicit limitations are in
`bounded-quotient-analysis.md`. The exact cascade was tested over every
admissible state with $2\le n\le160$, not only reachable states.

### 12. Periodic digits: exact obstruction, not a blanket dismissal

The earlier claim that integrality rules out periodic quotient-change patterns
was directionally right but not proved. Writing a period-$p$ word as
$(a_0,\ldots,a_{p-1})$ and unrolling one cycle gives

$$e_{N+p}=2^p e_N-CN-D.$$

The linear state window kills the exponentially growing homogeneous solution,
so the phase value is forced exactly, not asymptotically:

$$e_N=\frac{C}{2^p-1}N+\frac{pC/(2^p-1)+D}{2^p-1}.$$

This yields a necessary linear-congruence condition for integrality. A focused
enumerator found rationally admissible words at periods 6, 12, and 18, but all
222 failed that exact phase congruence. No nonzero periodic word through period
18 can occur even from an arbitrary integer state. This is a finite negative
result, not a proof for all periods; `periodic-orbit-analysis.md` keeps that
boundary explicit.

The first generator enumerated signed words directly. Rewriting the phase slope
as $A_j=v_j/p$ produced a much smaller exact state machine:

$$v_{j+1}=2v_j-pa_j,\qquad -S\le v_j\le p-S.$$

For fixed digit sum $S$, the next digit is deterministic except at the two
thresholds $S+2v_j\in\{0,p\}$. This extended the exhaustive search to minimal
period 42. Moving the same exact state machine to the zero-dependency Rust
framework extended the search through period 54: **11,122,706** cycle
representations and no phase-integral candidate. Repeated shorter words are
intentionally harmless overcounts. The rapid growth at periods 48 and 54 makes
clear that enumeration cannot substitute for an all-period proof.

### 13. Quantitative growth forced on a counterexample

The quotient dichotomy can be made quantitative. On a run of $L$ zero quotient
changes, $e$ is multiplied by $2^L$. A nonabsorbed orbit has integer
$|e|\ge1$, while the state window at index $n$ has size only $O(n)$, so every
zero-run ending by $n$ has length at most $\lfloor\log_2 n\rfloor$.

In the deep regime $8q_k\le k$, every down-step forces two up-steps and those
three-step blocks are disjoint. Counting nonzero digits between the bounded
zero-runs therefore forces a net quotient gain. Starting just after the last
index with $8q_k>k$ gives the uniform bound

$$
q_n\ge
\frac{n}{3(\lfloor\log_2 n\rfloor+1)}
-\frac{n_0}{3}-3.
$$

Thus a counterexample would have $b_n=\Omega_m(n^2/\log n)$, not merely
superlinear growth. The remaining logarithm measures the precise gap: the
current theory does not prevent each quotient gain from being separated by a
maximal doubling run.

### 14. Reset geometry and a candidate period induction

The longest real orbit in the census ($m=1{,}320{,}111$) has zero-runs as long
as 26 and repeatedly resets to $e=\pm1$, so a pointwise improvement of the
zero-run bound is false. But the small resets do not remain sparse: the same
orbit contains up-event streaks of length 33. Starting from the deliberately
extreme arbitrary state $(n,q,r)=(10^9,100,101)$ gives a zero-run of length 29,
then nearly five million up-events in the next ten million steps. This is
computational evidence for an amortized burst principle, not a theorem.

The periodic congruence diagnostics exposed a cleaner proof candidate. Every
one of the 11,122,706 failed cycles through period 54 is already rejected by a
factor $2^k-1$ associated with a proper divisor $k\mid p$. If this
proper-divisor witness can be proved for every self-consistent slope cycle,
minimal-period induction will rule out all eventually periodic digit orbits.
The exact statement and observed witness periods are now recorded in
`periodic-orbit-analysis.md`.

The dominant witness family can be closed rigorously. A reduced slope
denominator of 3 forces $p=6h$, quotient slope $\mu=1/3$, and a word made from
two two-step blocks. Phase integrality reduces to a subset sum of distinct
powers of 4 equalling either $G/3$ or $5G/6$, where
$G=(4^{3h}-1)/3$. The second is nonintegral; the first has repeating base-4
digit 3, while a subset of powers of 4 has only digits 0 and 1. Therefore no
denominator-3 periodic cycle exists at any period. This is Theorem 29, the first
all-period elimination beyond affine words.

The same lift-threshold method excludes reduced phase-slope denominator 5 for
all periods (Theorem 30). Denominator 7 has one rigid three-cycle and one
boundary family; the latter reduces to an impossible base-eight subset sum
using `(123457)_8` (Theorem 31). These are infinite-family results, but they
do not cover arbitrary denominators or aperiodic escape.

The lift argument generalizes further. For any reduced denominator `d>1`,
the denominator is odd and non-boundary lifts repeat after
`L=ord_d(2)<d` phases. Reapplying phase integrality to that shorter period
would require `d|L`, a contradiction. Thus every periodic counterexample
must lie exactly on a lift threshold. Lemma 33 gives the exact fraction of
repeated boundary blocks that must choose the negative lift. This turns each
denominator into finitely many subset-choice families (Theorem 32).

For denominator 9, the reduction leaves one six-step boundary family with
two-thirds negative boundary lifts. Relative to an all-negative baseline,
phase integrality would require a sum of powers of 64 to equal `G/84`, where
`G=(64^(3h)-1)/9` is odd. This is impossible, excluding denominator 9 for
every period (Theorem 34).

Denominator 11 also leaves one boundary family. Its ten-step block switch
changes the phase numerator by `128*1024^t`. The only possible integral
phase multiples would equate a number of 2-adic valuation at least 7 with
one of valuation 0 or 2. This excludes denominator 11 at every period
(Theorem 35).

Rotating any boundary cycle so its optional lift is last makes every block
switch universal: it changes the phase numerator by exactly `-2*(2^L)^t`.
The all-positive baseline also has a closed ratio independent of the number
of repeated blocks. Thus every rational periodic slope, at every
denominator, now reduces to one exact base-`2^L` subset equation
(Theorem 36). The remaining problem is to rule out every such digit
certificate uniformly.

The scale parameter can be removed from that finite certificate. Every
admissible repeat count is a multiple of a least repeat count `R_0`; the
larger target is the minimal target multiplied by
`1+B^R_0+...+B^((h-1)R_0)`. Its base-`B` digits are literal concatenations,
and parity is unchanged. Exact enumeration of all 250 odd denominators
through 501 finds 81 with no boundary family and rejects all 463 families
for every scale. Thus no nonzero eventually periodic slope orbit has reduced
denominator at most 501 (Corollary 37 / K11). The 501 bound is computational,
not a claim about arbitrary denominators.

The finite pattern exposes a two-digit universal contradiction. Since
`d|(2^L-1)`, Theorem 36 simplifies every boundary certificate to

```text
2d sum epsilon_t B^t = F(1+B+...+B^(R-1)),  0<F<2d.
```

Modulo the even base `B`, the first subset digit forces `F=B` or
`F=2d-B`. In the first case the next digit requires an even modulus to
divide an odd residue `1`; in the second it must divide one of two odd
residues. Both are impossible. Therefore no nonzero eventually periodic
quotient-change word is admissible at any denominator or period
(Theorem 38). Any counterexample to stabilization must be genuinely
aperiodic in addition to satisfying the earlier growth bounds.

### 15. The aperiodic frontier

Unrolling the doubling law to infinity gives the exact tail formula

```text
e_N = sum a_(N+k)(N+k+2)/2^(k+1).
```

This is not an asymptotic model: the state-window remainder vanishes
exponentially. It says that `e_N/(N+2)` shadows the signed binary value of the
entire future digit word within `2/(N+2)` (Theorem 39).

An eventually monotone counterexample has an even sharper form. Its `e` value
must stay positive, so every up-step must overshoot the usual threshold enough
to leave the next `e` positive. The resulting tail follows exactly
`e_(n+1)=2e_n mod (n+2)` and must avoid the interval
`n+1-q_n <= 2e_n <= n+2` (Lemma 40). Exhaustive scans of every positive-`e`
state at indices 100, 1000, and 10000 find maximum no-down durations 75, 223,
and 822. The apparent square-root scale is evidence, not yet a theorem.
