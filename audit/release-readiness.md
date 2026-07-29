# Release-readiness assessment

Date: 2026-07-28

This repository is ready for an external mathematical audit. It is not yet
ready to claim a proof of the original stabilization conjecture, and it should
not be represented as one.

## Strongest completed result

The main unconditional theorem is

\[
  c(m)=c \quad\Longrightarrow\quad m<(c+3)(3c+5).
\]

Its proof is in
[`manuscript/01-foundations-and-spectrum.md`](../manuscript/01-foundations-and-spectrum.md).
Combined with the complete independent certificate for every \(m<260\), it
proves that 5 and 7 are the smallest positive integers that do not occur as
eventual increments. The certificate, verifier, and hashes are documented in
[`supplement/02-certificates.md`](../supplement/02-certificates.md) and
[`evidence-manifest.md`](evidence-manifest.md).

## Coherent secondary contribution

The compact dossier also proves that a non-stabilizing orbit must have

\[
  q_n=\Omega_m(n/\log n),\qquad
  b_n=\Omega_m(n^2/\log n),
\]

and that its quotient-change word cannot be eventually periodic. The proofs
and their dependencies are isolated in
[`manuscript/02-counterexample-restrictions.md`](../manuscript/02-counterexample-restrictions.md),
[`manuscript/03-periodic-exclusion.md`](../manuscript/03-periodic-exclusion.md),
and [`theorem-dependency.md`](theorem-dependency.md).

## Scope correction

The two-counter safe map is exact only for the eventually-no-down branch.
It does not cover a hypothetical counterexample having infinitely many
down-steps. The appropriate next termination statement is therefore:

> Every valid entry state of the eventually-no-down safe map reaches its
> terminating middle strip.

Proving this would eliminate that branch, not settle the full conjecture by
itself. The equivalence and its boundary are stated in
[`manuscript/04-aperiodic-frontier.md`](../manuscript/04-aperiodic-frontier.md).

## Evidence now independently closed

- A literal arbitrary-precision Python implementation exhausts all \(m<260\)
  and emits the complete small-spectrum certificate.
- A separate arbitrary-precision Python implementation reproduces the Rust
  \(N=10^6\) safe-sweep endpoint, all accounting totals, and the full
  per-layer trajectory digest.
- A fresh proof-facing reviewer passed the main symbolic chains after one
  computational-evidence omission was repaired. See
  [`fresh-proof-review.md`](fresh-proof-review.md).
- Rust tests, the independent verification framework, Python syntax checks,
  the all-period denominator certificate, and the Lean build pass. Exact
  commands and limitations are in
  [`supplement/03-reproduction.md`](../supplement/03-reproduction.md).

## Remaining publication blockers

1. No human specialist has independently refereed the proofs.
2. An independent AI auditor reports a complete scratch re-enumeration of all
   \(m\le10^7\), with zero unresolved starts and an exact match to the 106
   omissions through 1823. The scratch implementation and full output were not
   archived in this repository, so the numerical agreement is independently
   reported but repository-local reproducibility remains open; see
   [`opus-pr2-audit.md`](opus-pr2-audit.md).
3. Lean checks only the statements actually present in
   [`lean/Conjecture.lean`](../lean/Conjecture.lean). The finite-start theorem,
   all-period exclusion, growth theorem, and safe-map equivalence are not
   formalized there.
4. The original conjecture remains open.

## Narrow external-review request

Ask a specialist to verify three cuts, in this order:

1. the reachability hypotheses and strict inequalities in the finite-start
   bound;
2. the reduced-slope and boundary branches in the all-period exclusion;
3. the exact equivalence and stated scope of the eventually-no-down safe map.

The reviewer should begin with the compact manuscript and dependency graph,
without the exploratory research logs. The computational supplement can then
be consulted only where a proof invokes a finite certificate.
