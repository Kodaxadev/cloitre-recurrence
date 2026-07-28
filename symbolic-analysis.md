# Symbolic analysis: the orbit as a binary expansion

This file develops the structure that makes the recurrence intelligible, and is
careful to mark where proof stops and heuristic begins. The proofs are in
`partial-proofs.md`; here they are assembled into a picture.

## 1. The right coordinate

With $b_n=q_n n+r_n$ and $e_n:=r_n-q_n$, Theorem 6 gives the exact law

$$e_{n+1}=2e_n-\Delta q_n\,(n+2),\qquad \Delta q_n\in\{-1,0,+1\},$$

with $e_{n+1}$ pinned to the admissible window $-q_{n+1}\le e_{n+1}\le n-q_{n+1}$
(length $n+1$, modulus $n+2$ — so the representative is unique). Stabilization is
exactly $e_n=0$.

Rescale: $\varepsilon_n := e_n/n$, $\kappa_n := q_n/n$. The window becomes
$[-\kappa,\,1-\kappa)$, a unit interval, and the law becomes

$$\varepsilon_{n+1} \;=\; 2\varepsilon_n - \Delta q_n .$$

**This is the binary shift map.** $\Delta q_n$ is not an auxiliary statistic — it is
literally the $n$-th *digit* of $\varepsilon$ in a signed binary expansion with
digit set $\{-1,0,+1\}$ and a $\kappa$-dependent choice of representative.

Consequences, all rigorous given the exact law:

* The absorbing state $\varepsilon=0$ is a **fixed point of a doubling map**, hence
  **repelling** (multiplier 2). Capture is never approached gradually; it happens
  by an exact integer coincidence or not at all. This is the structural reason no
  contraction argument can work, and why Propositions 16 and 17 come out negative.
* Telescoping the exact law over a non-stabilizing orbit gives the
  **exact series representation**
  $$e_N \;=\; \sum_{k\ge N}\Delta q_k\,(k+2)\,2^{\,N-k-1},$$
  convergent because $|e_n|\le n$ grows only polynomially. So the present state is
  determined by the *entire future* digit string, and conversely. The admissibility
  constraint $-q_N\le e_N\le N-1-q_N$ therefore constrains only the first
  $O(\log N)$ digits — which is exactly the content of Lemma 12 (a run of $k$
  up-steps forces $(2^k-1)q_n\lesssim n$) and Theorem 13.

## 2. Where the orbit lives: $\kappa\to1/4$

Under the digit picture, if $\varepsilon$ equidistributes on its unit window then
the digit is $-1$ on a set of measure $\kappa/2$, $0$ on measure $1/2$, $+1$ on
measure $(1-\kappa)/2$. Hence

$$\mathbb{E}[\Delta q] \;=\; \frac{1-2\kappa}{2}.$$

Since $q_n\approx\kappa n$ forces $dq/dn=\kappa$ in steady state, the fixed point is

$$\kappa=\frac{1-2\kappa}{2}\ \Longrightarrow\ \boxed{\kappa=\tfrac14},$$

and the feedback $d\kappa/dn=(1-4\kappa)/(2n)$ is negative, so $\kappa=1/4$ is
**attracting**. Therefore $b_n\sim n^2/4$ and the eventual increment satisfies
$c\approx t/4$.

**Status: heuristic** (it assumes equidistribution). **Evidence:** on the record
orbit $m=1{,}320{,}111$, $c/t = 0.249998$ at $t=3.3\times10^8$. Across the whole
$m\le2\times10^5$ scan, $\kappa$ measured over $2.76\times10^6$ steps of the
$m=11489$ orbit is $0.250075$. Rigorously we only have $\limsup\kappa\le1/2$
(Theorem 5).

## 3. The epoch chain — an exactly predicted transition matrix

Analysing only the quotient-change epochs (Priority 5) produced the sharpest
quantitative structure found in this project. Conditioning on the previous digit
and using equidistribution of $r/n$:

**After $\Delta q=0$.** $r$ is uniform on $[0,n)$; thresholds give
$(\tfrac\kappa2,\ \tfrac12,\ \tfrac{1-\kappa}{2}) = (\tfrac18,\tfrac12,\tfrac38)$.

**After $\Delta q=+1$.** An up-step leaves $r_{n+1}=2r_n-q_n-(n+1)$, which ranges
over $[0,\,n-3-q_n]$ — an interval of length $\approx\tfrac34 n$, not $n$. Redoing
the thresholds on that shorter interval gives
$$\Big(\tfrac16,\ \tfrac23,\ \tfrac16\Big).$$

**After $\Delta q=-1$.** A down-step leaves $r_{n+1}\ge n+1-q_n$, which with
$\kappa\approx\tfrac14$ is far above the up-threshold. This case is **not
heuristic**: Theorem 13 proves that $\Delta q_n=-1$ and $3q_n\le n+1$ force
$\Delta q_{n+1}=+1$. The row is $(0,0,1)$ except on the measure-zero-in-practice
event $\kappa>1/3$.

So the predicted transition matrix (rows = previous digit $-1,0,+1$) is

$$P=\begin{pmatrix}0&0&1\\[2pt] \tfrac18&\tfrac12&\tfrac38\\[2pt] \tfrac16&\tfrac23&\tfrac16\end{pmatrix}$$

and its stationary vector is exactly $\pi=(\tfrac18,\tfrac12,\tfrac38)$ — internally
consistent with the marginal law, and with $\mathbb{E}_\pi[\Delta q]=\tfrac14$ as
required by $\kappa=1/4$. (Check: $\pi P=\pi$ holds identically.)

**Measured**, on the single orbit $m=11489$ over $2{,}755{,}610$ steps:

| row | predicted | measured |
|---|---|---|
| from $-1$ | $(0,\ 0,\ 1)$ | $(0.00001,\ 0.00008,\ 0.99991)$ |
| from $0$ | $(0.125,\ 0.5,\ 0.375)$ | $(0.12504,\ 0.49990,\ 0.37506)$ |
| from $+1$ | $(0.1\overline{6},\ 0.\overline{6},\ 0.1\overline{6})$ | $(0.16681,\ 0.66679,\ 0.16641)$ |
| marginal | $(0.125,\ 0.5,\ 0.375)$ | $(0.12506,\ 0.49997,\ 0.37497)$ |
| mean gap between changes | $2$ | $1.9999$ |

Agreement to four decimals on every entry, with the $(0,0,1)$ row explained by a
theorem rather than by the model. Equidistribution of $r/n$ itself: $\chi^2=13.44$
on 19 degrees of freedom over 20 bins — indistinguishable from uniform.

*(Caveat, recorded honestly: pooling many orbits of different lengths gives
$\chi^2\approx3300$. That is an artefact of pooling short orbits at small $n$,
where $r/n$ is coarsely discrete, not evidence against equidistribution. The
single-long-orbit test is the meaningful one.)*

## 4. Why capture is rare, made precise

By Corollary 7, capture at $n+1$ requires **$n$ even** and $e_n=\pm(n+2)/2$. Now
note which sign is even *available*:

* $e_n=+\tfrac{n+2}{2}$ needs $r_n=q_n+\tfrac{n+2}{2}\le n-1$, i.e. $q_n<\tfrac n2-1$ — satisfied when $\kappa\approx\tfrac14$;
* $e_n=-\tfrac{n+2}{2}$ needs $q_n\ge\tfrac{n+2}{2}$, i.e. $\kappa\ge\tfrac12$ — **not** satisfied.

So in the regime the orbit actually occupies there is exactly **one** admissible
target, reachable only at even $n$. With $e_n$ spread over a window of length $n$,

$$\Pr[\text{capture at step } n] \;\approx\; \tfrac12\cdot\tfrac1n \;=\; \frac{1}{2n}.$$

Summing $\sum 1/(2n)$ diverges, so capture is almost sure and the conjecture is
what one should expect — but only logarithmically, which is why stabilization
times are enormous and heavy-tailed.

## 5. Where the heuristic FAILS — a genuine negative result

The model predicts $\Pr[t>N]\propto N^{-\alpha}$ with $\alpha=1/2$ (one target,
even indices), or $\alpha=1$ under the cruder two-target version used in the
MathOverflow answer. **Measured over starts $m\le2\times10^5$:**

| $N$ | $10^3$ | $10^4$ | $10^5$ | $10^6$ |
|---|---|---|---|---|
| $\Pr[t>N]$ | 0.6209 | 0.2353 | 0.0503 | 0.0068 |

A log-log fit over $10^3..10^6$ gives

$$\Pr[t>N] \sim N^{-0.655}.$$

That sits between the two predictions and matches **neither**. The naive
$\alpha=1$ model is decisively wrong (it underestimates $\Pr[t>10^6]$ by a factor
16); the refined $\alpha=1/2$ model errs the other way. Both are reported here as
refuted in their stated form.

Two effects the model omits, either of which could account for the gap:

1. **Merging correlates the trials.** $10^7$ starts collapse to only 9,911 distinct
   orbits, so the effective number of independent experiments is ~1000× smaller
   than the number of starts, and the empirical tail over starts is a heavily
   clustered statistic. But the tail measured over *distinct orbits* is also
   heavier than $1/N$ (see `compressed-orbit-analysis.md`), so this is not the
   whole story.
2. **$\kappa$ is not exactly $1/4$ along a single orbit**; it fluctuates, and the
   availability of the second target ($\kappa\ge1/2$) is not permanently zero.

Resolving this is a concrete, tractable open problem — see `future-directions.md`.

## 6. Rigidity: why no cheap counterexample exists

Two natural constructions of a non-stabilizing orbit are killed outright:

* **Affine escape.** Solving $e_n=an+\beta$ against the exact law forces
  $\Delta q_n\equiv a$ and $e_n=a(n+3)$. For $a=\pm1$ this violates the
  admissibility window by exactly 3 and 4 respectively. Only $a=0$ survives — the
  absorbing orbit (Proposition 16).
* **Periodic digit strings.** A periodic $\Delta q$ pattern with mean $\mu$ produces
  an exact affine value on each phase, not merely an asymptotic one. Admissibility
  permits several rational slope cycles, but `periodic-orbit-analysis.md` derives
  the required phase-integrality congruence. The boundary and block reductions in
  `periodic-boundary-reduction.md` turn it into a two-digit parity contradiction
  for every denominator and period (Theorem 38).

So a counterexample cannot be eventually affine or eventually periodic. Any
counterexample must be genuinely aperiodic.
