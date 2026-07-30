# Human review checklist

## Mathematical proof

- [ ] Verify the transition equations in Section 2.
- [ ] Verify the absorption equivalence.
- [ ] Verify the entry lemma and forward invariance of `b_n < n^2`.
- [ ] Verify the bounded-quotient transition range `Delta q in {-1,0,1}`.
- [ ] Verify the forced-rebound inequality.
- [ ] Verify the ratchet induction and interval endpoints.
- [ ] Verify both cases of the finite-start theorem.
- [ ] In the empty-set case, verify that `(n0-1)^2 < (c+2)n0` forces `n0 <= c+4`.
- [ ] In the nonempty-set case, verify `q_(n*) <= c+2` and `n* < 3c+5`.
- [ ] Verify that the strict inequalities are preserved in the final bound.

## Certificate

- [ ] Run `independent/verify_small_spectrum.py` from a clean checkout.
- [ ] Confirm all 259 rows are regenerated exactly.
- [ ] Confirm SHA-256 `66a06cff15735c4a3caf98575f29afbcd881fbef06334616fbc3bc772b7ab084`.
- [ ] Confirm no row has increment 5 or 7.
- [ ] Confirm witnesses for increments 1, 2, 3, 4, and 6.
- [ ] Confirm first absorption indices rather than merely later absorbing indices.
- [ ] Confirm the 64-step tail check is implemented as described.

## Scope and presentation

- [ ] Confirm the paper never claims universal stabilization.
- [ ] Confirm the spectrum is defined existentially, not as a total map on all starts.
- [ ] Confirm the larger 10M census is not needed for the main theorem.
- [ ] Confirm the Lean boundary is stated correctly.
- [ ] Review AI-assistance disclosure.
- [ ] Review title, abstract, and historical attribution.
