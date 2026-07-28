# The stabilization conjecture for `b(n+1) = b(n) + (b(n) mod n)`

OEIS [A073117](https://oeis.org/A073117) / [A117846](https://oeis.org/A117846).
Conjectured by Benoit Cloitre (2002), restated by Alex Abercrombie (2007):
for every starting value $m$ the increments $b_{n+1}-b_n$ are eventually constant.

**The conjecture remains open.** What this project produced:

## Results

**A published open question, answered — unconditionally.**
OEIS A117846 asks *"Do the values a(n) include all positive numbers?"*
The answer is **no**. The smallest eventual increments that never occur are
**5 and 7**; exactly **106** of the increments $1,\dots,1823$ never occur.

This follows from a new theorem plus a finite computation, and does **not**
assume the stabilization conjecture:

> **Theorem 18.** If the orbit from $m$ has eventual increment $c$, then $m<(c+3)(3c+5)$.

This gives an effective finite candidate set for each increment. Whenever every
candidate orbit in that set has been resolved, computation can prove absence;
before this bound, no finite scan could do so.

**New structural theory.** The substitution $e_n = r_n - q_n$ (where
$b_n=q_nn+r_n$) turns the recurrence into an exact modular doubling map,

> **Theorem 6.** $e_{n+1} = 2e_n - \Delta q_n (n+2)$, hence $e_{n+1}\equiv 2e_n \pmod{n+2}$,

with stabilization exactly $e_n=0$ — a *repelling* fixed point. $\Delta q_n$ is
literally the digit sequence of $e$ in signed binary. This explains why every
Lyapunov/invariant approach must fail, and two versions of that are proved
(Propositions 16, 17). Also new: the capture criterion (C7), congruence
propagation and parity (L8, C9), consecutive-step bounds (L12), the **forced
rebound** (T13) and the **ratchet** (T14) — the only monotonicity this system has,
and the engine behind Theorem 18.

The continuation adds an **entry ridge** ($q_{n_0}\in\{n_0-2,n_0-1\}$ at first
entry), an exact **rebound cascade**, and the theorem that every bounded-quotient
orbit stabilizes. In fact there is a dichotomy: either the orbit stabilizes or
$q_n\to\infty$. A zero-run count sharpens this: any counterexample must satisfy
$q_n=\Omega_m(n/\log n)$ and $b_n=\Omega_m(n^2/\log n)$.

For eventually periodic quotient changes, an exact affine-phase calculation now
gives a necessary divisibility condition. Exhaustive enumeration rejects every
nonzero minimal period through 54. The continuation now proves more:
**no nonzero eventually periodic quotient-change orbit exists at any period
or rational phase denominator** (Theorem 38). Genuinely aperiodic escape
remains open. An independent exact certificate verifies every reduced
denominator through 501.

For the aperiodic frontier, Theorem 39 gives an exact infinite future-digit
formula. Lemmas 40--41 reduce every eventually monotone escape to a
quotient-zero moving-modulus survivor problem. An exact compressed sweep of
all 999,999 positive states at index one million empties after 9,019 steps;
a bound uniform in the starting index remains open. Lemmas 43--44 put the
survivor map in exact binary-Euclidean coordinates, and Theorem 45 shows that
any monotone counterexample would have
$\liminf q_n\log_2(n)/n\ge1$.

**Verification extended 50×, with less arithmetic than the baseline.**

| | previous baseline | this project |
|---|---|---|
| verified range | $m \le 2\times10^5$ | $m\le 10^7$ |
| longest stabilization | $t=9{,}363{,}863$ at $m=31{,}873$ | $t=\mathbf{327{,}695{,}231}$ at $m=\mathbf{1{,}320{,}111}$ |
| eventual increment there | $2{,}341{,}202$ | $81{,}923{,}126$ |
| wall time | — | 149 s |

by advancing the *set* of live values in lockstep instead of one start at a time
(**313–1900× fewer iterations**; $10^7$ starts collapse to **9,911** distinct
orbits). The stated baseline was reproduced exactly first.

**Quantitative structure.** The quotient-change process has an exactly predicted
transition matrix, matching measurement to four decimals, whose stationary
distribution $(\tfrac18,\tfrac12,\tfrac38)$ self-consistently forces $q_n/n\to1/4$
— confirmed by $c/t = 0.249998$ at $t=3.3\times10^8$.

**Negative results, on record.** 17 candidate potentials rejected; affine Lyapunov
functions ruled out exactly; no modular invariant for any $M\in[2,64]$; and the
standard tail heuristic **refuted** (measured $N^{-0.655}$, predicted $N^{-1}$ or
$N^{-1/2}$).

## Reading order

| file | contents |
|---|---|
| [`audit/evidence-manifest.md`](audit/evidence-manifest.md) | **frozen audit entry point** — source commit, artifact hashes, and evidence boundaries |
| [`audit/theorem-dependency.md`](audit/theorem-dependency.md) | theorem dependency graph and critical audit cuts |
| [`audit/fresh-proof-review.md`](audit/fresh-proof-review.md) | blind proof-facing review and resolved findings |
| [`audit/release-readiness.md`](audit/release-readiness.md) | publication status, open risks, and the next narrow review request |
| [`manuscript/README.md`](manuscript/README.md) | compact proof dossier, separated from exploratory history |
| [`supplement/README.md`](supplement/README.md) | algorithms, certificates, completeness arguments, and reproduction |
| [`theorem-status.md`](theorem-status.md) | **start here** — every claim, classified as proved / computational / heuristic / refuted |
| [`partial-proofs.md`](partial-proofs.md) | the proofs |
| [`bounded-quotient-analysis.md`](bounded-quotient-analysis.md) | entry ridge, rebound cascade, and bounded-quotient theorem |
| [`periodic-orbit-analysis.md`](periodic-orbit-analysis.md) | exact obstruction and finite search for periodic quotient changes |
| [`periodic-denominator-families.md`](periodic-denominator-families.md) | all-period exclusions for phase-slope denominators 5, 7, 9, and 11 |
| [`periodic-boundary-reduction.md`](periodic-boundary-reduction.md) | reduction of every rational periodic slope to exact boundary subset equations |
| [`aperiodic-tail-analysis.md`](aperiodic-tail-analysis.md) | future-digit identity and the exact moving-modulus reduction for monotone tails |
| [`research-log-aperiodic.md`](research-log-aperiodic.md) | continued chronology for the aperiodic and monotone-tail attack |
| [`symbolic-analysis.md`](symbolic-analysis.md) | the doubling picture; where heuristics hold and where they break |
| [`literature-review.md`](literature-review.md) | what was already known, and by whom |
| [`compressed-orbit-analysis.md`](compressed-orbit-analysis.md) | the compression method, and the four that failed |
| [`invariant-search.md`](invariant-search.md) | comprehensive negative results |
| [`benchmark-report.md`](benchmark-report.md) | timings, determinism, reproduction |
| [`research-log.md`](research-log.md) | chronology, including mistakes |
| [`future-directions.md`](future-directions.md) | ranked next steps |
| [`lean/`](lean/) | machine-checked formalization (no `sorry`) |

## Audit phase

The exploratory snapshot is frozen at Git commit
`f19ffcd75d04a05529878ce0226088f2f3221c0b`. Subsequent work is limited to
audit packaging, independent verification, and corrections. The proposed paper
title is **Structural and arithmetic restrictions on stabilization in a modular
additive recurrence**.

The two-counter safe map is not a reduction of every unresolved orbit. It is
equivalent to the eventually-no-down branch after the branch's entry state is
fixed. A hypothetical non-stabilizing orbit with infinitely many down-steps is
outside that map. The exact scope and dependency boundary are recorded in the
[theorem graph](audit/theorem-dependency.md).

## Layout

```
search-framework/        Rust, zero dependencies
  src/dynamics.rs          division-free (q,r) iteration
  src/sweep.rs             compressed set sweep
  src/witness.rs           sweep + orbit census
  src/bin/{scan,sweep,record,epochs,invariant,bench,periodic,resets,monotone,pure}.rs
  tests/                   adversarial tests vs. a naive reference + OEIS ground truth
verification-framework/  independent: u128, raw b-form, no shared code
  verify.py                third implementation, arbitrary precision
lean/Conjecture.lean     Lean 4.32.1, mathlib-free, compiles clean
data/                    census, scans, profiles
computational-results.csv  top 2000 orbits by stabilization index
```

## Reproducing

```bash
cd search-framework && cargo test --release
cargo run --release --bin record -- --lo 1 --hi 10000000 --out ../data/census_10M.csv
cd ../verification-framework && cargo run --release -- --csv ../data/scan_200k.csv
python verify.py --oeis
lean ../lean/Conjecture.lean
```

Every binary prints an FNV-1a-64 digest and is deterministic across thread counts.
The sweep and census assert their covering identities
(`merges + absorbed + live == starts`) and abort rather than report an unverified
range — that assertion is what licenses Corollary 20.

## Correctness posture

Three independent implementations (Rust `u64` in $(q,r)$ coordinates; Rust `u128`
in raw $b$-form; Python arbitrary-precision), agreeing on: all 68 published terms
of A117846 in both parities, A073117's $a(397)=38606=398\cdot97$, all 200,000 rows
of the $2\times10^5$ scan, and the ten record orbits checked 500 steps past
stabilization. Arithmetic overflow checking is enabled in every build that
produced a result — it costs nothing measurable here.

The independent verifier earned its keep once: it rejected two rows of a
spot-check file whose values I had typed by hand rather than extracted
programmatically. See `research-log.md`.
