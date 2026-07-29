# Theorem status ledger

Every claim this project touches, classified. The classes are disjoint and the
classification is the point: nothing is promoted without a proof.

* **Theorem / Lemma** — proved, proof written out in the cited proof file.
* **Computational** — established by exhaustive finite computation, with the
  range stated. True as stated; says nothing beyond that range.
* **Heuristic** — a prediction from a non-rigorous model. May be wrong.
* **Conjecture** — believed, unproved, no proof strategy in hand.
* **Refuted** — tested and false.

---

## A. Proved (unconditional)

| # | Statement | Where | Status |
|---|-----------|-------|--------|
| T1 | Constant increments from $t$ $\iff$ $b_t=c(t+1)$, $c<t$ $\iff$ $q_t=r_t$ | `partial-proofs.md` §1 | **Theorem** (folklore) |
| T2 | If $b_n<n^2$: stabilized at $n$ $\iff$ $(n+1)\mid b_n$ | §1 | **Theorem** (known, MO 191518, 2025) |
| C2.1 | $m\ge1 \Rightarrow c\ge1$ | §1 | **Corollary** |
| L3 | Entry: $\exists\,n_0\le\lceil\sqrt{2m}\rceil+2$ with $b_{n_0}<n_0^2$; no absorbing index skipped | §2 | **Lemma** |
| L4 | $q_n\le n$ forward invariant; $\Delta q_n\in\{-1,0,+1\}$ | §2 | **Lemma** (known) |
| T5 | $\limsup q_n/n \le 1/2$ | §2 | **Theorem** |
| **T6** | $e_{n+1}=2e_n-\Delta q_n(n+2)$, so $e_{n+1}\equiv2e_n \pmod{n+2}$ | §3 | **Theorem — new** |
| **C7** | First capture at $n+1$ $\iff$ $n$ even and $e_n=\pm(n+2)/2$ | §3 | **Corollary — new** |
| **L8** | $d\mid n \Rightarrow b_{n+1}\equiv 2b_n \pmod d$ | §3 | **Lemma — new** |
| **C9** | $b_j$ even for every odd $j\ge3$ | §3 | **Corollary — new** |
| T10 | Pair merging: $b_3(2k-1)=b_3(2k)=2k$ | §4 | **Theorem** (known, A117846) |
| T11 | $f_n(x)=f_n(y)$, $x\ne y$ $\iff$ $n$ even, $|x-y|=n/2$, adjacent blocks | §4 | **Theorem** (known, MO) |
| **L12** | Two consecutive $+1$ force $3q_n\le n-9$; two consecutive $-1$ force $3q_n>2n+3$ | §5 | **Lemma — new** |
| **T13** | $\Delta q_n=-1$ and $3q_n\le n+1$ $\Rightarrow$ $\Delta q_{n+1}=+1$ | §5 | **Theorem — new** |
| **T14** | Ratchet: while $3q\le n+1$, $q$ never falls more than 1 below its window start | §5 | **Theorem — new** |
| **L21** | At first entry $n_0\ge3$, $q_{n_0}\in\{n_0-2,n_0-1\}$ | `bounded-quotient-analysis.md` | **Lemma — new** |
| **T22** | Exact rebound cascade; if $\Delta q_n=-1$ and $n\ge7q_n+1$, the next two steps are $+1,+1$ | `bounded-quotient-analysis.md` | **Theorem — new** |
| **C23** | Every bounded-quotient orbit stabilizes; every counterexample has unbounded $q_n$ | `bounded-quotient-analysis.md` | **Corollary — new** |
| **T24** | Quotient dichotomy: stabilization, or $q_n\to\infty$ (hence $b_n/n\to\infty$) | `bounded-quotient-analysis.md` | **Theorem — new** |
| **T25** | Exact integrality obstruction for every eventually periodic $\Delta q$ word | `periodic-orbit-analysis.md` | **Theorem — new** |
| **L26** | A nonabsorbed run of $\Delta q=0$ has length at most $\lfloor\log_2 n\rfloor$ | `bounded-quotient-analysis.md` | **Lemma — new** |
| **T27** | Before absorption, $q_n\ge n/[3(\lfloor\log_2n\rfloor+1)]-n_0/3-3$ | `bounded-quotient-analysis.md` | **Theorem — new** |
| **L28** | Every periodic slope pattern reduces to a finite doubling cycle modulo its period | `periodic-orbit-analysis.md` | **Lemma — new** |
| **T29** | Every eventually periodic slope cycle with reduced denominator $3$ is impossible | `periodic-orbit-analysis.md` | **Theorem — new** |
| **T18** | $c(m)=c \Rightarrow m<(c+3)(3c+5)$ | §5b | **Theorem — new** |
| **C19** | $\{m: c(m)=c\}$ finite and effectively bounded | §5b | **Corollary — new** |
| **C20** | Not every positive integer is an eventual increment; smallest missing are 5 and 7 | §5b | **Computer-assisted corollary — independent complete certificate for $m<260$** |
| P16 | Only affine-in-$n$ orbit for $e_n$ is the absorbing one | §6 | **Proposition — new** |
| P17 | No non-trivial affine Lyapunov function $\alpha q+\beta r+\gamma n+\delta$ | §6 | **Proposition — new** |
| **T30** | Every eventually periodic slope cycle with reduced denominator $5$ is impossible | `periodic-denominator-families.md` | **Theorem - new** |
| **T31** | Every eventually periodic slope cycle with reduced denominator $7$ is impossible | `periodic-denominator-families.md` | **Theorem - new** |
| **T32** | Every nonintegral eventually periodic slope must lie on an admissibility boundary | `periodic-boundary-reduction.md` | **Theorem - new** |
| **L33** | Every surviving boundary family has the exact choice ratio $K/R=N/d$ | `periodic-boundary-reduction.md` | **Lemma - new** |
| **T34** | Every eventually periodic slope cycle with reduced denominator $9$ is impossible | `periodic-denominator-families.md` | **Theorem - new** |
| **T35** | Every eventually periodic slope cycle with reduced denominator $11$ is impossible | `periodic-denominator-families.md` | **Theorem - new** |
| **T36** | Every surviving periodic boundary family satisfies an exact base-$2^L$ subset equation | `periodic-boundary-reduction.md` | **Theorem - new** |
| **T38** | No admissible integer orbit has an eventually periodic nonzero quotient-change word | `periodic-boundary-reduction.md` | **Theorem - new** |
| **T39** | Every tail satisfies the exact convergent future-digit identity (39.1) | `aperiodic-tail-analysis.md` | **Theorem - new** |
| **L40** | Every nonabsorbed tail without down-steps is a moving-modulus doubling orbit avoiding (40.1) | `aperiodic-tail-analysis.md` | **Lemma - new** |
| **L41** | For fixed positive $e$, quotient zero dominates every no-down continuation with larger quotient | `aperiodic-tail-analysis.md` | **Lemma - new** |
| **L42** | Every dominant positive no-down path obeys the exact two-counter safe map | `aperiodic-tail-analysis.md` | **Lemma - new** |
| **L43** | The two-counter map has an exact binary-Euclidean form with forbidden gap $h<e\le h+U+2$ | `aperiodic-tail-analysis.md` | **Lemma - new** |
| **L44** | On a positive wrap run, $h+q+3$ doubles exactly at every step | `aperiodic-tail-analysis.md` | **Lemma - new** |
| **T45** | An eventually monotone counterexample has $\liminf q_n\log_2(n)/n\ge1$ and the same normalized lower bound for $b_n/n$ | `aperiodic-tail-analysis.md` | **Theorem - new** |
| **T46** | Safe-map termination at checkpoint $N+1$ implies termination at $N$; failure is upward-closed in the starting index | `safe-map-checkpoint-analysis.md` | **Theorem - new; fresh audit pending** |
| **L47** | The safe map is centered doubling in a signed-distance coordinate with terminating hole $1\le x\le U+2$ | `safe-map-checkpoint-analysis.md` | **Lemma - new; fresh audit pending** |
| **C48** | Every witness at a least failing safe-map index has odd $e$; at an odd least index it is unreachable from $b_1=m$ | `safe-map-checkpoint-analysis.md` | **Corollary - new; fresh audit pending** |
| **L49** | Initial quotient $Q$ preserves a safe prefix exactly while every zero-step slack is at least $Q$ | `safe-map-checkpoint-analysis.md` | **Lemma - new; fresh audit pending** |
| **T50** | An even least safe-map failure must start below the midpoint and later hit exact zero quotient slack | `safe-map-checkpoint-analysis.md` | **Theorem - new; fresh audit pending** |
| **L51** | Zero steps and their maximal wrap runs admit the exact accelerated return-or-termination map (51.1)--(51.2) | `safe-map-checkpoint-analysis.md` | **Lemma - new; fresh audit pending** |
| **C52** | A zero-slack boundary exits to positive odd slack; local equality is classified, while later boundary residues strictly increase | `safe-map-checkpoint-analysis.md` | **Corollary - new; fresh audit pending** |
| **L53** | The accelerated overshoot pair $(n,A)$ evolves autonomously; the wrap counter only selects return versus termination | `zero-epoch-overshoot-analysis.md` | **Lemma - new; fresh audit pending** |
| **C54** | Every infinite safe path would satisfy an exact sparse dyadic identity over its zero epochs | `zero-epoch-overshoot-analysis.md` | **Corollary - new; fresh audit pending** |
| **T55** | A positive-wrap block run has the explicit bound (55.1); every infinite safe path has infinitely many $00$ pairs and eventually $U\le(n-4)/2$ | `zero-epoch-overshoot-analysis.md` | **Theorem - new; fresh audit pending** |
| **T56** | Every counterexample, with or without infinitely many down-steps, has $\liminf q_n\log_2(n)/n\ge1$ and the same normalized lower bound for $b_n$ | `sharp-counterexample-growth.md` | **Theorem - new; fresh audit pending** |
| **C57** | Every counterexample has the explicit unit-leading rate $q_n\ge(1-O(1/\log\log n))n/\log_2n-O_m(1)$ | `sharp-counterexample-growth.md` | **Corollary - new; fresh audit pending** |
| **T58** | In every sublinear counterexample, down-steps have zero density in time and among quotient changes, their individual spacings diverge, and $q_n/C(n)\to1$ | `sparse-downstep-analysis.md` | **Theorem - new; fresh audit pending** |
| **C59** | Every counterexample either has positive $\limsup q_n/n$, or belongs to the sparse-downstep sublinear class of T58 | `sparse-downstep-analysis.md` | **Corollary - new; fresh audit pending** |
| **L60** | On every finite interval, the total logarithmic rebound weight of down-steps is bounded by the up-step count plus one logarithmic endpoint loss | `sparse-downstep-analysis.md` | **Lemma - new; fresh audit pending** |
| **C61** | A sublinear infinite-down counterexample requires increasingly long post-down segments with up-step fraction tending to zero along a subsequence | `sparse-downstep-analysis.md` | **Corollary - new; fresh audit pending** |
| **L62** | Every finite post-down no-down segment satisfies an exact dyadic budget for all of its zero digits | `sparse-downstep-analysis.md` | **Lemma - new; fresh audit pending** |
| **L63** | The terminal negative suffix before a down-step is an exact dyadic remainder map | `ridge-segment-analysis.md` | **Lemma - new; fresh audit pending** |
| **C64** | A sublinear infinite-down counterexample has unbounded pure-zero runs inside its post-down segments | `ridge-segment-analysis.md` | **Corollary - new; fresh audit pending** |
| **L65** | At every down-step, all future zero- and down-step defects form an exact nonnegative dyadic expansion with an exact consecutive-down recurrence | `ridge-segment-analysis.md` | **Lemma - new; fresh audit pending** |

**C20 answers a stated open question** in OEIS A117846 (Abercrombie, 2007):
*"Do the values a(n) include all positive numbers?"* — **No.**
This is unconditional: it does not assume the stabilization conjecture.

---

## B. Established by exhaustive computation

| # | Statement | Range | Method |
|---|-----------|-------|--------|
| K1 | Every $m$ stabilizes | $1\le m\le 10^{7}$ | compressed sweep + witness census, accounting identity checked |
| K2 | Record: $t=327{,}695{,}231$, $c=81{,}923{,}126$, smallest $m=1{,}320{,}111$ | $m\le10^{7}$ | census; re-verified in u128 |
| K3 | Previous baseline $t=9{,}363{,}863$, $c=2{,}341{,}202$ at $m=31{,}873$ reproduced exactly | $m\le2\times10^{5}$ | 3 independent implementations |
| K4 | All 68 published terms of A117846 reproduced (both parities) | — | 3 independent implementations |
| K5 | A073117 $a(397)=38606=398\cdot97$ reproduced | — | 3 independent implementations |
| K6 | Exactly 106 of the increments $1..1823$ never occur (94.2% attained) | complete for $c\le1823$ | K1 + Theorem 18 |
| K7 | $10^{7}$ starts collapse to **9,911** distinct orbits (1009× compression) | $m\le10^{7}$ | witness census |
| K8 | 316 is the *joint* most-shared increment (9 orbits) — 313/314/315 have 8 | $m\le10^{7}$ | census |
| K9 | No nonzero eventually periodic $\Delta q$ word passes exact integrality | minimal periods $p\le54$ | 11,122,706 cycle representations |
| K10 | Every periodic failure has a proper-divisor factor witness | periods $p\le54$ | exact divisor diagnostics; conjectural beyond range |
| K11 | No nonzero eventually periodic slope orbit has reduced denominator $d\le501$ | all periods; 250 odd denominators, 463 boundary families | Theorems 32 and 36 + exact base-digit certificates |
| K12 | Longest arbitrary-state no-down segments are 75, 223, and 822 steps at indices 100, 1000, and 10000 | all positive-$e$ states at each index | exact exhaustive `monotone` scan |
| K13 | No valid positive state at any index $2\le N\le10^6$ has an infinite no-down continuation; at the checkpoint $N=10^6$ the compressed safe set empties at $1{,}009{,}019$ | all $999{,}999$ positive $e$ values at the checkpoint + Lemma 41 + Theorem 46 | Rust and independent Python generators; matching trajectory digest |

K8 answers MathOverflow Q2 ("what is special about 316?"): **essentially nothing**;
it wins by a margin of one over its immediate neighbours.

---

## C. Heuristic (explicitly not proved)

| # | Statement | Evidence | Status |
|---|-----------|----------|--------|
| H1 | $b_n \sim n^2/4$, i.e. $q_n/n\to1/4$ | measured $0.250075$ on the record orbit; $c/t=0.249998$ at $t=3.3\times10^8$ | **Heuristic** |
| H2 | $r_n/n$ equidistributes on $[0,1)$ | $\chi^2=13.4$ on 19 df over $2.76\times10^6$ steps | **Heuristic** |
| H3 | $\Delta q$ frequencies $(\tfrac18,\tfrac12,\tfrac38)$ | measured $(0.12506, 0.49997, 0.37497)$ | **Heuristic** |
| H4 | Epoch chain has transition matrix with rows $(0,0,1)$, $(\tfrac18,\tfrac12,\tfrac38)$, $(\tfrac16,\tfrac23,\tfrac16)$ | measured to 4 decimals; row 1 is **proved** (T13) | **Heuristic + partly proved** |
| H5 | Capture probability $\approx \tfrac{1}{2n}$ per step (one admissible target, even $n$ only) | see `symbolic-analysis.md` | **Heuristic** |
| H6 | $c(m)\gtrsim0.92\sqrt m$ (lower envelope) | flat across all dyadic blocks to $2\times10^5$ | **Heuristic** |
| CJ1 | Every $m$ stabilizes (the conjecture) | $m\le10^{7}$ | **Conjecture — OPEN** |

---

## D. Refuted / rejected

| # | Candidate | How it died |
|---|-----------|-------------|
| R1 | $P(t>N)\sim C/N$ (naive tail law) | measured exponent $-0.655$, not $-1$; and the refined model predicts $-1/2$. Both wrong. See `symbolic-analysis.md` §5 |
| R2 | 17 candidate monotone potentials ($|e|$, $|e|/(n+2)$, $q/n$, $v_2(b)$, $\gcd(b,n+1)$, …) | all increase on $\ge35\%$ of $2.17\times10^6$ sampled transitions |
| R3 | Any affine Lyapunov function | P17; exact convex-hull feasibility test returns 0 directions |
| R4 | Modular invariant: $b_{n+1}\bmod M$ a function of $(n\bmod M, b\bmod M)$ | fails for every $M\in[2,64]$, explicit witnesses |
| R5 | Non-absorbing orbit with $e_n$ affine in $n$ | P16 — killed by the admissibility window |

---

## E. What would settle the conjecture

By T2 the conjecture is exactly: *every orbit eventually meets a multiple of $n+1$*.
By C7 the target has exactly one admissible element per even index. By T6 the
motion between hits is an exact doubling map — **expanding**. P16 and P17 rule out
the two natural contraction arguments. So the obstruction is the same as Collatz's:
an expanding map whose measure-zero target is hit with probability one under the
natural model, with no mechanism forcing an individual orbit to comply.

A proof would need either
(i) an equidistribution theorem for $e_n \bmod (n+2)$ strong enough to force a hit
(this is genuinely hard — the modulus moves every step), or
(ii) a completely different, arithmetic obstruction to the existence of an orbit
that avoids $e_n=0$ forever.

See `future-directions.md`.
