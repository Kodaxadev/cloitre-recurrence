/-
Formalization of the proved core of the A073117 / A117846 stabilization problem.

  b_1 = m,   b_{n+1} = b_n + (b_n mod n)

Indexing: `B m k` denotes `b_{k+1}`, so `B m 0 = b_1 = m` and the recurrence
becomes `B m (k+1) = B m k + B m k % (k+1)`, which is structurally recursive.
The paper's index `n` is therefore `k+1` throughout.

The development is deliberately MATHLIB-FREE. Because mathlib is unavailable,
`ring`, `linarith`, `push_cast` and `by_contra` are not used; every nonlinear
rewrite is supplied explicitly and `omega` finishes the linear part, so the
non-linear subterms it abstracts as atoms are made to match by hand.

It is now split across modules, so check it through lake rather than with a bare
`lean` invocation:

    lake env lean lean/Conjecture.lean

Modules:
  * `Conjecture.Basic`   -- the orbit, absorption, congruence, pairs, doubling
  * `Conjecture.Gate`    -- pure Nat arithmetic for the gate exponent
  * `Conjecture.Ratchet` -- forced rebound and the quotient ratchet

Formalized:
  * Theorem 1  (Absorption): the ray b = c(n+1) is invariant; increments are c
  * Theorem 6  (Doubling coordinate) in the form (n+2) ∣ (e_{n+1} - 2 e_n)
  * Lemma 8    (Congruence propagation) and Corollary 9 (parity)
  * Theorem 10 (Pair merging) and orbit coincidence from index 3 on
  * Theorem 13 (Forced rebound) and Theorem 14 (Ratchet), the load-bearing
                steps of the finite-start bound
  * Theorem 133 (Gate exponent uniqueness) and its unit case Theorem 130,
                plus Lemma 136's upward closure

NOT formalized, and stated as such in lean/README.md: the finite-start bound
itself (Theorem 18), the growth bounds, the all-period exclusion, the safe-map
reduction, and every claim above index 130 except the arithmetic noted.
-/

import Conjecture.Basic
import Conjecture.Gate
import Conjecture.Ratchet
import Conjecture.FiniteStart
import Conjecture.AbsorptionConverse
import Conjecture.EntryBound

/-! ## Axiom audit -- confirms nothing below depends on `sorryAx`. -/
section Audit
open Conjecture
#print axioms Conjecture.absorb_step
#print axioms Conjecture.absorb_forever
#print axioms Conjecture.absorb_increment
#print axioms Conjecture.increment_forces_remainder
#print axioms Conjecture.congruence_propagation
#print axioms Conjecture.even_at_even_index
#print axioms Conjecture.pair_merging
#print axioms Conjecture.E_doubling_nat
#print axioms Conjecture.E_doubling_mod
#print axioms Conjecture.E_doubling
#print axioms Conjecture.E_zero_of_ray
#print axioms Conjecture.B_monotone
#print axioms Conjecture.gate_exponent_unique
#print axioms Conjecture.unit_gate_exponent_unique
#print axioms Conjecture.gap_predicate_upward_closed
#print axioms Conjecture.quotient_drop_le_one
#print axioms Conjecture.forced_rebound
#print axioms Conjecture.ratchet
#print axioms Conjecture.entry_exists
#print axioms Conjecture.quadratic_step
#print axioms Conjecture.least_entry
#print axioms Conjecture.finite_start
#print axioms Conjecture.ray_of_eventual_increment
#print axioms Conjecture.finite_start_of_increment
#print axioms Conjecture.entry_at_sqrt_bound
#print axioms Conjecture.least_entry_le_sqrt_bound
end Audit
