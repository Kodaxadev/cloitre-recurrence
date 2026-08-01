# Scoped audit of the remaining post-freeze theorem band

## Scope

This pass addresses the band explicitly left outside the Opus six-cut
audit:

- Theorem 46 through Corollary 57;
- Corollary 64 through Theorem 72;
- Lemma 78 through Corollary 82.

The proof sources were checked against the exact transition laws and the
dependency cuts in [`theorem-dependency.md`](theorem-dependency.md).
The independent raw-transition verifiers were rerun as regression evidence.
This remains an internal AI proof audit, not external peer review.

## Checkpoint and zero-epoch chain, T46--C57

**Verdict: passed.**

- T46 correctly converts arbitrarily long deterministic prefixes into one
  infinite continuation; its contrapositive gives checkpoint monotonicity.
- C48 and T50 use valid predecessor states in both parity branches. At an
  even least failure, the initial-wrap case and every positive
  quotient-clearance slack both contradict minimality.
- L51's least non-wrap index has the correct strict predecessor threshold;
  its returned slack is exactly the zero-versus-termination test.
- C52's boundary return has odd positive slack, and later boundary epochs
  increase by half their even zero-transition separation.
- L53's autonomous coordinate has the exact parity and state-window bounds.
  C54 telescopes with a remainder bounded by \((n_j+2)/2^{n_j}\).
- T55 charges every positive block except the final one and loses only the
  stated endpoint block. Its recurrence conclusions distinguish zero
  blocks, positive blocks, and intermediate wrap states correctly.
- T56 fixes the rebound length before taking the tail limit. C57's
  floor choice satisfies the finite threshold before the asymptotic
  substitution.

No defective statement or missing case was found.

## Ridge chain, C64--T72

**Verdict: passed.**

- C64's pigeonhole bound diverges because \(U_j/L_j\to0\); the state window
  gives its dyadic zero-run bound.
- L65 subtracts the actual future tail from the closed all-up tail. All
  weights are nonnegative, so the consecutive-down split and limiting
  iteration are justified.
- P66 reconstructs a valid local family only; it does not claim global
  reachability.
- L67 and L70 use the terminal negative-suffix thresholds with the correct
  adjacent index advance.
- L68 covers all three exponent orders. In its \(H<J\) branch one has
  \(J\ge2\), which makes the final strict exponential bound valid even at
  the smallest parameters.
- T69 uses a terminal quotient at least two exactly to ensure \(z_1\ge1\).
- C71 controls the absolute divisible defect strictly below its modulus.
- T72 first obtains \(K_j\to\infty\) from T58, then uses positive-integer
  descent to force infinitely many nonzero congruence defects.

No defect was found. Theorems 69 and 72 retain their stated pure-ridge
scope.

## Terminal and safe-wrap ceilings, L78--C82

**Verdict: passed.**

- L78's endpoint identity and state-window substitution give both sides of
  the finite terminal-run inequality.
- C79 first proves \(R=O(\log t)\), making \(R/t\to0\), before inserting
  the T56 quotient lower bound. The order of substitutions is valid.
- L80 uses strict minimality at \(k-1\); subtracting \(2^{k+2}\) preserves
  the strict wrap-block bound.
- C81 applies T45 only after its lower denominator is positive.
- C82 counts all completed positive blocks at a zero epoch, absorbs the
  finite prefix into one constant, and takes \(n\to\infty\) before
  \(\varepsilon\downarrow0\).

No defect was found. These are ceilings and recurrence-rate restrictions,
not termination statements.

## Computational regression

The supporting independent runs cover:

- 2,138 parameterized rebound cascades;
- 999,985 floor-threshold endpoints;
- 1,088 post-down zero budgets;
- 2,210 terminal ridge segments;
- 34,816 unit-chain incompatibilities;
- 518 arbitrary-terminal pure ridges and 171 adjacent congruences;
- 84,575 accelerated zero epochs and 25,357 wrap transitions in the
  safe-map verifier.

Finite agreement supports but does not prove the symbolic claims.

## Remaining boundary

The post-freeze band named by the follow-up auditor now has a scoped internal
pass. Human specialist review remains absent. The independent
\(10^7\)-enumeration source and full output also remain unarchived, and the
original conjecture remains open.
