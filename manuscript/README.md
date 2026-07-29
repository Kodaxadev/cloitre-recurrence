# Structural and arithmetic restrictions on stabilization in a modular additive recurrence

## Abstract

For a positive integer \(m\), define

\[
b_1=m,\qquad b_{n+1}=b_n+(b_n\bmod n).
\]

It is unknown whether every orbit eventually has constant first difference.
We establish an effective bound connecting a stabilizing start to its eventual
increment: if the eventual increment is \(c\), then

\[
m<(c+3)(3c+5).
\]

Together with a certified finite enumeration, this proves that the eventual
increments are not surjective onto the positive integers; the smallest omitted
values are \(5\) and \(7\). We also prove that every nonstabilizing orbit has
quotient \(q_n=\Omega_m(n/\log n)\), hence
\(b_n=\Omega_m(n^2/\log n)\), and that its quotient-change sequence cannot be
eventually periodic. For the special case of an eventually nondecreasing
quotient, we derive an exact two-counter termination system. The latter
reduction does not cover hypothetical counterexamples with infinitely many
quotient down-steps. We nevertheless show that in the sublinear-quotient
branch, such down-steps must have zero density both in time and among quotient
changes, and that their individual spacings must diverge. Exact finite ridges
can nevertheless have vanishing up-step density. We derive their pure-chain
compatibility law and show that any infinite arbitrary-terminal pure tail
would require exponentially large local parameters infinitely often. An exact
defect expansion extends the compatibility law to arbitrary mixed ridges and
isolates the unresolved low-order terminal-run obstruction.

## Manuscript assembly

The manuscript is intentionally modular for audit. Read or concatenate these
files in order:

1. [`01-foundations-and-spectrum.md`](01-foundations-and-spectrum.md)
2. [`02-counterexample-restrictions.md`](02-counterexample-restrictions.md)
3. [`03-periodic-exclusion.md`](03-periodic-exclusion.md)
4. [`04-aperiodic-frontier.md`](04-aperiodic-frontier.md)
5. [`05-zero-epoch-boundary.md`](05-zero-epoch-boundary.md)
6. [`06-autonomous-zero-epoch-map.md`](06-autonomous-zero-epoch-map.md)
7. [`07-sharp-growth.md`](07-sharp-growth.md)
8. [`08-sparse-downsteps.md`](08-sparse-downsteps.md)
9. [`09-ridge-segments.md`](09-ridge-segments.md)
10. [`10-ridge-chains.md`](10-ridge-chains.md)
11. [`11-mixed-ridges.md`](11-mixed-ridges.md)

Only definitions, statements, proofs, and explicit claim boundaries belong
here. Algorithms, benchmarks, certificates, and reproduction instructions
belong in `../supplement/`.

## Status

The original stabilization conjecture remains open. The strongest completed
result is the finite-start bound and its computer-assisted nonsurjectivity
corollary. Theorem numbering follows `../theorem-status.md` to preserve
traceability to the frozen research snapshot
`f19ffcd75d04a05529878ce0226088f2f3221c0b`.
Theorems 46, 50, 55, 56, 58, 69, 72, and 75; Proposition 66; Lemmas 47,
49, 51, 53, 60, 62, 63, 65, 67, 68, 70, and 73; and Corollaries 48, 52,
54, 57, 59, 61, 64, 71, and 74 are post-freeze additions
and have not yet received the fresh-context audit applied to the frozen
theorem chain.

## Formalization boundary

The Lean file formalizes absorption, congruence propagation, parity, pair
merging, and the exact \(e\)-doubling congruence. It does not formalize the
finite-start bound, growth restrictions, periodic exclusion, or the
two-counter reduction.
