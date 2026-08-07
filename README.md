<p align="center">
  <img src="assets/readme-hero.svg" alt="Cloitre recurrence research package" width="100%">
</p>

<p align="center">
  <a href="https://github.com/Kodaxadev/cloitre-recurrence/actions/workflows/ci.yml"><img src="https://github.com/Kodaxadev/cloitre-recurrence/actions/workflows/ci.yml/badge.svg" alt="Research checks"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-d9a441.svg" alt="MIT License"></a>
  <a href="https://github.com/Kodaxadev/cloitre-recurrence/tree/v0.1.0-audit"><img src="https://img.shields.io/badge/audit-v0.1.0--audit-2b8a7e.svg" alt="Audit release"></a>
  <img src="https://img.shields.io/badge/conjecture-open-c0392b.svg" alt="Conjecture open">
</p>

<p align="center">
  <strong>Proofs · exact certificates · compressed computation · partial Lean formalization</strong>
</p>

---

## 1. The recurrence and the open conjecture

For a positive integer \(m\), define

\[
b_1=m,\qquad b_{n+1}=b_n+(b_n\bmod n).
\]

The **Cloitre stabilization conjecture** asks whether, for every start \(m\), the increments \(b_{n+1}-b_n\) are eventually constant. The problem appears in [OEIS A073117](https://oeis.org/A073117), [OEIS A117846](https://oeis.org/A117846), and [MathOverflow 191518](https://mathoverflow.net/questions/191518/mod-sequences-that-seem-to-become-constant-and-the-number-316).

> [!IMPORTANT]
> **The universal stabilization conjecture remains open.** This repository contains internally audited partial theorems, certified finite results, and reproducible computational evidence — not a proof of universal stabilization. Nothing below closes it, and no computational result in §4 should be read as a termination theorem.

### The organizing coordinate

Write

\[
b_n=q_n n+r_n,\qquad 0\le r_n<n,\qquad e_n=r_n-q_n.
\]

Then the recurrence becomes

\[
\boxed{e_{n+1}=2e_n-\Delta q_n(n+2)},
\qquad
e_{n+1}\equiv2e_n\pmod{n+2}.
\]

Stabilization is exactly the event \(e_n=0\). This exposes the dynamics as a doubling map with a moving modulus, and it supplies the main organizing coordinate for everything that follows.

By T2 the conjecture is equivalently: *every orbit eventually meets a multiple of \(n+1\)*. The target has exactly one admissible element per even index, and the motion between hits is an exact doubling map — **expanding**. Two natural contraction arguments (an affine Lyapunov function; an orbit with \(e_n\) affine in \(n\)) are ruled out. So the obstruction has the same shape as Collatz's: an expanding map whose measure-zero target is hit with probability one under the natural model, with no mechanism forcing an individual orbit to comply.

## 2. What is proved

These are unconditional theorems with proofs written out in the cited sources. "Internally proved" means a complete proof passed a fresh-context internal audit; it does **not** mean an external specialist has refereed it.

| Result | Statement | Source |
|---|---|---|
| **Finite-start bound** | If the orbit from \(m\) has eventual increment \(c\), then \(m<(c+3)(3c+5)\). This converts every fixed-increment question into a finite computation | [`partial-proofs.md`](docs/proofs/partial-proofs.md) |
| **Nonsurjectivity** | The eventual increments are **not** surjective onto the positive integers; the smallest omitted values are \(5\) and \(7\). Unconditional — it does not assume the conjecture | [`partial-proofs.md`](docs/proofs/partial-proofs.md) |
| **Growth bounds** | Every bounded-quotient orbit stabilizes, so any counterexample has \(q_n\to\infty\), \(q_n=\Omega_m(n/\log n)\), and \(b_n=\Omega_m(n^2/\log n)\) | [`bounded-quotient-analysis.md`](docs/proofs/bounded-quotient-analysis.md) |
| **Aperiodicity** | No admissible nonzero eventually periodic quotient-change sequence exists, so any counterexample must be genuinely aperiodic | [`periodic-orbit-analysis.md`](docs/proofs/periodic-orbit-analysis.md) |
| **Safe-map descent** | For an eventually-no-down tail there is an exact two-counter safe map; Theorem 46 propagates the \(N=10^6\) checkpoint downward to every earlier index | [`safe-map-checkpoint-analysis.md`](docs/proofs/safe-map-checkpoint-analysis.md) |

**Nonsurjectivity answers a stated open question** in OEIS A117846 (Abercrombie, 2007): *"Do the values a(n) include all positive numbers?"* — **No.**

> [!CAUTION]
> The two-counter map covers the **eventually-no-down branch only**. A hypothetical counterexample with infinitely many quotient down-steps lies outside this reduction.

The complete classified list of every claim the project touches — theorem, computational, heuristic, conjecture, refuted — is [`docs/theorem-status.md`](docs/theorem-status.md). It is the authoritative ledger; this README summarizes it and never overrides it.

## 3. The current structural reduction

The active frontier is the safe map for the eventually-no-down branch. The work since the checkpoint has progressively removed *search freedom* from that branch: what began as a branching gate search is now a single deterministic orbit, and the surviving obstruction is one explicit recurrence.

| Step | What it establishes |
|---|---|
| **T130**, **T133**, **L135/L136** | Continuation is **forced, not branching**. The outgoing exponent is an explicit minimum \(h^\ast=\min\{h\ge2:2^hf\ge n+h+4\}\); the gap-dependent windows admit at most one exponent at *every* block length; block length and the zero-only gap are likewise forced |
| **L131** | The wrap count is inert — the \((n,f)\) orbit is independent of \(U\), so a sweep at \(U=0\) is exhaustive over all wrap counts |
| **T137**, **T138**, **C139** | The mechanism closes into a deterministic map \(\Psi\) on four integers \((n,U,k,f)\), which is a **triangular skew product** with \(U\) a passive accumulator entering only through the zero test |
| **L140**, **L141**, **C142** | Threshold-slack coordinates invert the map and bound the candidate counts; the forcing dichotomy is **one-sided** — block slack is never arithmetically forced |
| **L143**, **C144** | Admissibility becomes a single slack inequality against the budget \(G_i=n_i-2U_i\), rather than a test applied from outside |
| **T145** | The first bound on the length of a \(\Psi\)-orbit: a chain of \(N\ge2\) consecutive positive blocks satisfies \(N\le3C-13\), where \(C=\max_i(n_i-2U_i)\). Its arithmetic core is machine-checked in Lean |
| **C146** | An infinite chain has **unbounded** budget, \(\sup_i G_i=\infty\). A dichotomy, not an exclusion of either branch |
| **C147** | On an all-unit chain the survival test and the residue cap are the same inequality at successive indices. The remaining obstruction is a **one-dimensional expanding recurrence aimed at a moving admissible window** |

> [!CAUTION]
> **This is not a termination theorem.** T145 does not bound \(C\) in terms of \((n_0,U_0)\), so it does not bound orbit length absolutely. C146 gives unboundedness of the budget, *not* divergence in general — divergence follows only in the all-unit branch, where the budget is monotone. C147 states the surviving obstruction sharply; it does not resolve it.

Sources: [`block-chain-closed-map.md`](docs/proofs/block-chain-closed-map.md), [`slack-coordinates.md`](docs/proofs/slack-coordinates.md), [`admissible-budget.md`](docs/proofs/admissible-budget.md), [`unit-chain-determinism.md`](docs/proofs/unit-chain-determinism.md), [`general-gate-determinism.md`](docs/proofs/general-gate-determinism.md).

## 4. The exhaustive computational frontier

Everything in this section is **established by exhaustive finite computation inside a proved bound**. It is true as stated and says nothing beyond its stated range. None of it is a theorem about all orbits.

### Global census

|  | Previous baseline | This project |
|---|---:|---:|
| Verified starting values | \(m\le2\times10^5\) | \(m\le10^7\) |
| Longest stabilization index | \(9{,}363{,}863\) | **\(327{,}695{,}231\)** |
| Smallest start attaining record | \(31{,}873\) | **\(1{,}320{,}111\)** |
| Eventual increment there | \(2{,}341{,}202\) | **\(81{,}923{,}126\)** |
| Distinct compressed orbits | — | **9,911 from \(10^7\) starts** |

The primary sweep advances the live set in lockstep and checks the covering identity `merges + absorbed + live == starts` before reporting a completed range.

### The all-unit gap-word classification (K18, K19)

Inside the proved bounds from C114 and C115, the all-unit pure-upper words are now classified exhaustively. The bound is the proved part; K18 and K19 are the exhaustive computation inside it.

| | Words | Normalized \(U=0\) seeds | States | Continue further |
|---|---:|---:|---:|---|
| **K18** — two gaps | 6 | 93 | 2,706 | 342 have a defined third gate |
| **K19** — three gaps | 9 realized | 14 | 342 | 74 have a defined fourth gate |

The fourth-gate frontier is narrow: `1011` has 16 states, `0213` has 24, and `2022` has 34.

> [!CAUTION]
> An undefined next gate means only that T130's all-unit partial map is **undefined there**. That is not termination of the safe trajectory, and none is claimed. K18 and K19 constrain one restricted all-unit mechanism; they do not bear on the general branch, and they do not resolve C147.

Both certificates are regenerated in CI on Ubuntu and Windows and compared byte for byte. Their canonical byte counts and SHA-256 identities are registered in [`docs/theorem-status.md`](docs/theorem-status.md), which is the single source for those values.

## 5. Formal verification

The Lean 4 development is **mathlib-free** — no cache download, no network, no proof-library dependency — compiles clean with **no `sorry`**, and ends with an axiom audit. It is checked with Lean 4.32.2, whose pin matters: 4.32.2 fixes a kernel soundness bug present in 4.32.1.

**Formalized:**

* the orbit, absorption, congruence propagation, and the doubling law for \(e_n\);
* gate-exponent uniqueness and gap-predicate upward closure;
* the forced rebound and the quotient ratchet;
* the block-chain length bound — the arithmetic core of **T145**;
* entry, the quadratic step, and **the finite-start theorem \(m<(c+3)(3c+5)\)**, in both the ray form and the paper's eventual-increment form;
* Lemma 3's explicit entry bound.

**Not formalized:** the growth bounds, all-period exclusion, and the two-counter / expanding-window reduction of §3. Those remain prose proofs with internal audit only.

Three external checks run over the compiled development: Lean's bundled `leanchecker`, a pinned independent Rust kernel (`nanoda`), and the axiom audit itself, which permits only `propext`, `Classical.choice`, `Quot.sound`, and `Lean.trustCompiler`. Any declaration reaching for anything else — including `sorryAx` — fails. See [`lean/README.md`](lean/README.md).

### Verification stack

| Layer | Role |
|---|---|
| [`search-framework/`](search-framework/) | Zero-dependency Rust dynamics, compressed sweep, census, periodic and safe-map tools |
| [`verification-framework/`](verification-framework/) | Independent `u128` raw-\(b\) verifier |
| `verification-framework/verify.py` | Third implementation using arbitrary-precision Python integers |
| [`independent/`](independent/) | Independent certificate regenerators that reimplement the raw maps and import no project code |
| [`lean/`](lean/) | Mathlib-free Lean formalization with an axiom audit |
| `scripts/check_lean_nanoda.sh` | Pinned independent-kernel check of the Lean environment |
| [`certificates/`](certificates/), [`data/`](data/) | Compact certificates and datasets; see [`data/README.md`](data/README.md) for column formats |

## 6. Reproducibility

### One command

```bash
docker build -t cloitre . && docker run --rm cloitre
```

`scripts/reproduce.sh` runs the core fast scientific checks locally against pinned toolchains (Rust 1.94.0, Python 3.13, Lean 4.32.2), and prints at the end the heavy commands that are deliberately excluded. CI adds what one host cannot supply: platform-matrix execution, cross-platform certificate comparison, documentation and TeX structural checks, and the hosted paper-reproducibility environment.

### What continuous integration covers

The research workflow runs on pull requests and on manual workflow dispatch; pushes to `main` run it automatically. A plain push to a research branch does **not** trigger it, so exact-SHA evidence on a research branch comes from a pull request or from `gh workflow run ci.yml --ref <branch>`.

A run provides:

* **Rust** theorem and verifier tests, on Ubuntu **and** Windows;
* **Python** certificates and OEIS checks, on Ubuntu **and** Windows;
* **cross-platform certificate determinism** — the K18 and K19 reports produced by the two operating systems are downloaded and compared byte for byte, so agreement is a gate rather than an out-of-band claim;
* **Lean** compilation, the axiom audit, `leanchecker`, and the pinned external kernel;
* the **arXiv draft** build, including a byte-for-byte PDF reproducibility check.

### Selected fast checks

```bash
cargo test --release --manifest-path search-framework/Cargo.toml
cargo test --release --manifest-path verification-framework/Cargo.toml
python verification-framework/verify.py --oeis
python independent/verify_small_spectrum.py
python independent/verify_safe_checkpoint.py
python independent/verify_unit_determinism.py 200 400 30000
python independent/verify_unit_gap_words.py --report artifacts/unit-gap-words.json
python independent/verify_unit_gap_extensions.py --report artifacts/unit-gap-extensions.json
python independent/verify_admissible_slack.py 200
python scripts/periodic_phase_blocks.py --max-denominator 501
lake env lean lean/Conjecture.lean
lake env leanchecker Conjecture
bash scripts/check_lean_nanoda.sh
```

The full \(10^7\) census, the \(N=10^6\) safe-map regeneration, and the deep chain sweeps behind K1–K8, K13, K15 and K17 take hours and are not in CI. Their exact commands are printed at the end of `scripts/reproduce.sh` and recorded with expected digests in [`supplement/03-reproduction.md`](supplement/03-reproduction.md).

`scripts/check_doc_links.py` verifies in CI that every relative link and inline path reference across all documentation resolves.

## 7. Where to read next

**If you want the claims:** start at [`docs/theorem-status.md`](docs/theorem-status.md) — every claim, classified into disjoint classes, with the proof source for each.

**If you want the mathematics:** [`manuscript/README.md`](manuscript/README.md) is the statement-and-proof dossier; [`audit/theorem-dependency.md`](audit/theorem-dependency.md) shows the dependency spine and where the critical cuts are.

**If you want the current frontier:** [`docs/future-directions/future-directions-safe-map.md`](docs/future-directions/future-directions-safe-map.md).

**If you want the evidence boundaries:** [`audit/evidence-manifest.md`](audit/evidence-manifest.md) for artifact hashes and release identity, [`supplement/README.md`](supplement/README.md) for the claim-to-evidence matrix, and [`audit/release-readiness.md`](audit/release-readiness.md) for what "internally proved" does and does not mean.

Further internal audits, each a point-in-time record of a scoped pass: [`fresh-proof-review.md`](audit/fresh-proof-review.md), [`opus-pr2-audit.md`](audit/opus-pr2-audit.md), [`continuation-t58-l63.md`](audit/continuation-t58-l63.md), [`continuation-c89-t90.md`](audit/continuation-c89-t90.md), [`opus-reconciliation-verification.md`](audit/opus-reconciliation-verification.md), [`scoped-post-freeze-band.md`](audit/scoped-post-freeze-band.md), [`tail-123-142.md`](audit/tail-123-142.md).

### Repository layout

| Path | Contents |
|---|---|
| [`docs/`](docs/) | All research notes. [`docs/theorem-status.md`](docs/theorem-status.md) is the ledger and authoritative index; `docs/proofs/`, `docs/research-logs/`, `docs/future-directions/` and `docs/notes/` are what it cites. See [`docs/README.md`](docs/README.md) |
| [`lean/`](lean/) | Mathlib-free Lean 4 formalization, with an axiom audit |
| [`manuscript/`](manuscript/) | Statement-and-proof dossier and the [arXiv draft](manuscript/arxiv/) |
| [`search-framework/`](search-framework/) | Zero-dependency Rust dynamics, sweeps, and safe-map tools |
| [`verification-framework/`](verification-framework/) | Independent `u128` Rust verifier and a third Python implementation |
| [`independent/`](independent/) | Independent regenerators that import no project code |
| [`certificates/`](certificates/), [`data/`](data/) | Compact certificates and datasets |
| [`audit/`](audit/) | Internal audit passes, evidence boundaries, and the dependency graph |
| [`scripts/`](scripts/) | Reproduction, checkers, and analysis utilities |
| [`supplement/`](supplement/) | Algorithms, finite completeness arguments, and reproduction commands |

<details>
<summary><strong>Research notes and specialized analyses</strong></summary>

| File | Contents |
|---|---|
| [`partial-proofs.md`](docs/proofs/partial-proofs.md) | foundational proofs and finite-start theorem |
| [`bounded-quotient-analysis.md`](docs/proofs/bounded-quotient-analysis.md) | entry ridge, rebound cascade, bounded quotient, growth bound |
| [`sharp-counterexample-growth.md`](docs/proofs/sharp-counterexample-growth.md) | parameterized rebounds and sharp growth |
| [`periodic-orbit-analysis.md`](docs/proofs/periodic-orbit-analysis.md) | affine-phase obstruction and finite periodic search |
| [`periodic-denominator-families.md`](docs/proofs/periodic-denominator-families.md) | denominator-family exclusions |
| [`periodic-boundary-reduction.md`](docs/proofs/periodic-boundary-reduction.md) | universal boundary subset-equation reduction |
| [`aperiodic-tail-analysis.md`](docs/proofs/aperiodic-tail-analysis.md) | future-digit identity and monotone-tail safe map |
| [`zero-epoch-overshoot-analysis.md`](docs/proofs/zero-epoch-overshoot-analysis.md) | zero-epoch boundary and overshoot analysis |
| [`safe-map-checkpoint-analysis.md`](docs/proofs/safe-map-checkpoint-analysis.md) | checkpoint monotonicity and signed-distance safe map |
| [`sparse-downstep-analysis.md`](docs/proofs/sparse-downstep-analysis.md) | down-step density, spacing, weighted rebound budget, and ridge dilution |
| [`ridge-segment-analysis.md`](docs/proofs/ridge-segment-analysis.md) | terminal negative suffix, down-epoch defect coding, and exact diluted ridge families |
| [`ridge-chain-analysis.md`](docs/proofs/ridge-chain-analysis.md) | unit and arbitrary-terminal pure-ridge compatibility, dyadic congruence, and conditional complexity obstruction |
| [`mixed-ridge-analysis.md`](docs/proofs/mixed-ridge-analysis.md) | arbitrary mixed-ridge defect, terminal-run congruence, and exhaustive dyadic boundary-ladder dichotomy |
| [`terminal-run-analysis.md`](docs/proofs/terminal-run-analysis.md) | exact state-window inequality and log-log ceiling for terminal positive up-runs |
| [`safe-wrap-run-analysis.md`](docs/proofs/safe-wrap-run-analysis.md) | exact state-window inequality and log-log ceiling for safe-map wrap blocks |
| [`safe-block-gate-analysis.md`](docs/proofs/safe-block-gate-analysis.md) | exact dyadic compatibility gate between adjacent positive safe-map blocks |
| [`unit-wrap-gate-analysis.md`](docs/proofs/unit-wrap-gate-analysis.md) | induced unit-wrap coordinates and exact uniqueness-boundary test |
| [`unit-wrap-chain-analysis.md`](docs/proofs/unit-wrap-chain-analysis.md) | persistence obstruction and critical-scale bounds for unique unit-wrap chains |
| [`unit-wrap-critical-exclusion.md`](docs/proofs/unit-wrap-critical-exclusion.md) | dyadic-epoch contradiction excluding the all-unit/all-unique tail |
| [`general-gate-boundary-analysis.md`](docs/proofs/general-gate-boundary-analysis.md) | exact two-boundary uniqueness test for positive blocks of arbitrary length |
| [`parent-boundary-gate-analysis.md`](docs/proofs/parent-boundary-gate-analysis.md) | affine parent-layer compatibility and nonincreasing block lengths |
| [`parent-gap-exclusion.md`](docs/proofs/parent-gap-exclusion.md) | strict gap growth and exclusion of the persistent parent boundary |
| [`child-boundary-window.md`](docs/proofs/child-boundary-window.md) | canonical residue decomposition and exact interior uniqueness window |
| [`gate-multiplicity-analysis.md`](docs/proofs/gate-multiplicity-analysis.md) | exact candidate count and upper-ambiguity two-block ceiling |
| [`gate-transfer-analysis.md`](docs/proofs/gate-transfer-analysis.md) | exact child-residue transfer and unit-block pure-upper recurrence |
| [`unit-pure-upper-analysis.md`](docs/proofs/unit-pure-upper-analysis.md) | quotient normalization, exact unit-state test, and critical-scale theorem |
| [`unit-renewal-exclusion.md`](docs/proofs/unit-renewal-exclusion.md) | exponential obstruction to three strict alternating fixed-ladder renewals |
| [`unit-word-rigidity.md`](docs/proofs/unit-word-rigidity.md) | fixed-word endpoint rigidity and zero-density renewal bound |
| [`unit-word-arithmetic.md`](docs/proofs/unit-word-arithmetic.md) | sparse-binary endpoint equation and sharp two-renewal families |
| [`unit-word-composition.md`](docs/proofs/unit-word-composition.md) | exact word composition, dyadic windows, and termination of the explicit family |
| [`unit-chain-determinism.md`](docs/proofs/unit-chain-determinism.md) | forced-gate determinism, inert wrap count, exhaustive chain ceiling, and heuristic count |
| [`general-gate-determinism.md`](docs/proofs/general-gate-determinism.md) | forced pure-upper gap at arbitrary block length |
| [`block-chain-closed-map.md`](docs/proofs/block-chain-closed-map.md) | closed forms for gap and block length, and the four-integer deterministic map |
| [`slack-coordinates.md`](docs/proofs/slack-coordinates.md) | threshold-slack coordinates, admissible-slack counts, and the one-sided forcing dichotomy |
| [`admissible-budget.md`](docs/proofs/admissible-budget.md) | the budget inequality, the chain-length bound, and the expanding-window reduction |
| [`symbolic-analysis.md`](docs/notes/symbolic-analysis.md) | doubling model, heuristics, and failures |
| [`compressed-orbit-analysis.md`](docs/notes/compressed-orbit-analysis.md) | compression design and rejected approaches |
| [`invariant-search.md`](docs/notes/invariant-search.md) | negative invariant and potential searches |
| [`benchmark-report.md`](docs/notes/benchmark-report.md) | performance measurements for the search framework |
| [`literature-review.md`](docs/notes/literature-review.md) | prior work and attribution |
| [`research-log.md`](docs/research-logs/research-log.md) | exploratory chronology and corrections |
| [`research-log-aperiodic.md`](docs/research-logs/research-log-aperiodic.md) | continuation chronology |
| [`research-log-ridge-chains.md`](docs/research-logs/research-log-ridge-chains.md) | arbitrary-terminal ridge-chain derivation and rejected monotonicity routes |
| [`research-log-mixed-ridges.md`](docs/research-logs/research-log-mixed-ridges.md) | mixed-ridge derivation, bounded falsification, and surviving low-bit target |
| [`research-log-parent-gaps.md`](docs/research-logs/research-log-parent-gaps.md) | fixed-length parent-gap exclusion and surviving child-boundary target |
| [`research-log-child-window.md`](docs/research-logs/research-log-child-window.md) | child-window derivation and orbitwise-equidistribution warning |
| [`research-log-gate-transfer.md`](docs/research-logs/research-log-gate-transfer.md) | pure-upper persistence falsification and exact residue-transfer derivation |
| [`research-log-safe-wraps.md`](docs/research-logs/research-log-safe-wraps.md) | safe-wrap balance dead end, log-log ceiling, and quantitative block recurrence |
| [`research-log-unit-determinism.md`](docs/research-logs/research-log-unit-determinism.md) | collapse of the cross-word framing, forced-gate derivation, and the inequality routes that fail |
| [`future-directions.md`](docs/future-directions/future-directions.md) | ranked unresolved directions |
| [`future-directions-safe-map.md`](docs/future-directions/future-directions-safe-map.md) | safe-map frontier: current targets and the surviving obstruction |

</details>

## Frozen audit release

The exploratory snapshot is commit `f19ffcd75d04a05529878ce0226088f2f3221c0b`.

The complete immutable audit package is tagged:

**[`v0.1.0-audit`](https://github.com/Kodaxadev/cloitre-recurrence/tree/v0.1.0-audit)** → `46e4780dc4955c1fd21110aebcbc6da688794668`

Later README, metadata, and CI maintenance do not alter that frozen record.

## Citation

Citation metadata are provided in [`CITATION.cff`](CITATION.cff). The package is AI-assisted and maintainer-curated; that boundary is stated explicitly in the citation metadata and audit documents.

---

<p align="center">
  <strong>The central conjecture is open. The partial results, certificates, and exact scope boundaries are the contribution of this repository.</strong>
</p>
