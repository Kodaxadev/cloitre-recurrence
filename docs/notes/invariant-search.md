# Invariant search

Priority 4 asked for invariants, and for every candidate to be attacked before
being reported. **Everything was rejected.** That is the honest headline, and the
rejections are informative: two of them upgraded into proved non-existence
theorems (Propositions 16 and 17 in `partial-proofs.md`).

The tool is `search-framework/src/bin/invariant.rs`. It is a *falsifier*: a
candidate is assumed false and reported only if a large adversarial sample fails
to kill it. Sample used below: **2,169,736 reachable transitions** drawn from 3,000
distinct orbits (all $m\le3000$), up to 3,000 steps each.

```bash
cargo run --release --bin invariant -- --lo 1 --hi 3000 --per-orbit 3000 --grid 120
```

---

## A. Candidate potential functions

Each candidate $V$ was tested for monotonicity ($V$ non-increasing along every
reachable transition). A single increase kills it.

| candidate $V(n,q,r)$ | verdict | transitions where $V$ increases |
|---|---|---|
| $q$ | REJECTED | 787,202 (36%) |
| $r$ | REJECTED | 1,085,110 (50%) |
| $\lvert e\rvert$ | REJECTED | 1,361,394 (63%) |
| $\lvert e\rvert/(n+2)$ | REJECTED | 1,361,394 (63%) |
| $e^2/(n+2)^2$ | REJECTED | 1,361,394 (63%) |
| $\lvert q-n/4\rvert$ | REJECTED | 941,300 (43%) |
| $\lvert r-n/2\rvert$ | REJECTED | 1,110,283 (51%) |
| $\lvert 2r-q\rvert$ | REJECTED | 1,178,482 (54%) |
| $n-q$ | REJECTED | 1,382,534 (64%) |
| $q/n$ | REJECTED | 787,202 (36%) |
| $r/n$ | REJECTED | 1,085,110 (50%) |
| $\lvert e\rvert/n$ | REJECTED | 1,361,394 (63%) |
| $\ln(1+\lvert e\rvert)$ | REJECTED | 1,361,394 (63%) |
| $v_2(b)$ (2-adic valuation) | REJECTED | 1,043,811 (48%) |
| $\gcd(b,n+1)$ | REJECTED | 1,084,274 (50%) |
| $-\gcd(b,n+1)$ | REJECTED | 1,085,462 (50%) |
| $b/(n(n+1))$ | REJECTED | 1,002,706 (46%) |

Not one candidate is even *close*: every family fails on 36–64% of transitions.
These are not marginal rejections that better constants could rescue.

**Why this had to happen.** $|e|/(n+2)$ is the natural "distance to absorption",
and Theorem 6 says $e_{n+1}\equiv 2e_n \pmod{n+2}$: the distance *doubles* at
every step until it wraps. The absorbing state is a repelling fixed point of a
doubling map, so no distance-like quantity can decrease. Any Lyapunov-style
approach to this problem is doomed for a structural reason, not a tuning reason.

---

## B. Affine Lyapunov functions — decided exactly, not sampled

Rather than grid-search $V=\alpha q+\beta r+\gamma n+\delta$ against millions of
transitions, the problem was reduced to an exact 3-variable feasibility question:

* $V$ non-increasing $\iff$ $\alpha\,\Delta q+\beta\,\Delta r+\gamma\le0$ for every
  observed $(\Delta q,\Delta r)$ $\iff$ the same on the **convex hull** of those points;
* $V$ bounded below $\iff$ $\alpha u+\beta v+\gamma\ge0$ on the convex hull of the
  observed $(q/n,\,r/n)$.

Both hulls are tiny, so feasibility is decided directly instead of statistically.

```
hull of (dq, dr)   : 4 vertices  [(-1, 2), (1, -1894), (0, 1120), (-1, 2660)]
hull of (q/n, r/n) : 18 vertices [(0, 0.5), (0.222, 0), (0.979, 0), (0.984, 0.016), ...]
grid resolution    : 1/120 per coefficient
nontrivial feasible directions : 0
```

**Verdict: no affine Lyapunov function exists.** The reason is short enough to
state: non-increase forces $\tfrac{\alpha}{4}+\tfrac{\beta}{2}+\gamma\le0$, while
boundedness below forces $\tfrac{\alpha}{4}+\beta v+\gamma\ge0$ for all
$v\in[0,1)$ — reachable states realise $r/n$ arbitrarily close to both endpoints.
Together these force $\beta=0$ and $\gamma=-\alpha/4$, leaving
$V=\alpha(q-n/4)+\delta$, which increases on every up-step. Hence
$\alpha=\beta=\gamma=0$. This is Proposition 17, and the machine search confirms it
constructively.

---

## C. Modular invariants

Question: is there a modulus $M$ for which $b_{n+1}\bmod M$ is determined by
$(n\bmod M,\ b\bmod M)$? If so, the dynamics would project onto a finite graph and
the whole problem would collapse.

**Answer: no, for every $M\in[2,64]$.** Explicit witnesses (two states agreeing
mod $M$ whose successors differ):

| $M$ | witness $(n,b)$ | successors differ |
|---|---|---|
| 2 | $(7,10)$ | 0 vs 1 |
| 3 | $(8,13)$ | 2 vs 0 |
| 4 | $(7,10)$ | 0 vs 1 |
| 5 | $(12,30)$ | 3 vs 1 |
| 6 | $(8,13)$ | 2 vs 0 |
| 7 | $(13,36)$ | 3 vs 4 |
| 8 | $(11,26)$ | 4 vs 6 |

The obstruction is intrinsic: $b_{n+1}$ depends on $b_n\bmod n$, and $b_n\bmod n$
is not a function of $b_n\bmod M$ unless $M\mid n$ — which cannot hold for a fixed
$M$ at consecutive indices.

**What survives.** Exactly one congruence structure does hold, and it is a theorem
rather than a search result:

$$d\mid n \;\Longrightarrow\; b_{n+1}\equiv 2b_n \pmod d \qquad \text{(Lemma 8)}$$

with the corollary that $b_j$ is even for every odd $j\ge3$ (Corollary 9). This is
a genuine invariant — it just does not propagate across consecutive steps, so it
constrains reachability without constraining the dynamics.

---

## D. Other families, and why they were dropped

| family | outcome |
|---|---|
| **Quadratic / higher polynomial** in $(n,q,r)$ | The obstruction in §B is scale-free: it comes from $e$ doubling. Any $V$ that is a continuous function of $(q/n, r/n)$ inherits it. Polynomial candidates were sampled ($e^2/(n+2)^2$ above) and fail identically. |
| **Entropy-like** ($-\sum p\log p$ over digit statistics) | The digit process is stationary with the measured law $(\tfrac18,\tfrac12,\tfrac38)$; entropy is *constant* along a typical orbit, so it carries no information about capture. |
| **Lexicographic** on $(q,r)$ or $(\lvert e\rvert, n)$ | Requires a well-order compatible with the map. Fails immediately: $q$ increases 36% of the time and $\lvert e\rvert$ 63% of the time, in every combination. |
| **Graph-theoretic** (finite quotient of the state graph) | Ruled out by §C: no finite quotient by a modulus exists. The state graph on $(n,b)$ is genuinely infinite and non-recurrent. |
| **Probabilistic / martingale** | $e_n$ is *not* a martingale — $\mathbb{E}[e_{n+1}]=2\mathbb{E}[e_n]$ modulo the wrap, and $q_n$ has systematic drift $+\tfrac14$. The natural candidate $q_n-n/4$ is a mean-zero random walk under the heuristic, but its increments are bounded and it is recurrent, so it gives no capture argument. |
| **Symbolic regression** | Not run. Given that the exact governing law is already known in closed form (Theorem 6), regression could only rediscover it; and the space of monotone candidates was closed off exactly in §B. Spending the budget on Theorem 18 was the better trade. |

---

## E. The one thing that did work

The search for a *decreasing* quantity failed completely. What succeeded was a
search for a **structural constraint** — and it came from the epoch analysis, not
from the invariant catalogue:

$$\Delta q_n=-1 \ \text{and}\ 3q_n\le n+1 \;\Longrightarrow\; \Delta q_{n+1}=+1 .$$

This is Theorem 13. It is not an invariant; it is a forced-move rule. Iterated, it
becomes the **ratchet** (Theorem 14): in the region the orbit actually occupies,
$q$ can never fall more than 1 below where it has been, and every dip is repaired
on the next step. That is the only monotonicity in this system, it is one-sided and
conditional, and it is strong enough to yield Theorem 18 and answer an open OEIS
question.

The lesson recorded for future work: for an expanding map, do not look for a
potential that decreases. Look for **moves that are forced**.
