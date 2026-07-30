/-
Theorem 13 (forced rebound) and Theorem 14 (the ratchet): the load-bearing
steps of the finite-start bound, Theorem 18.

Mathlib-free, so `by_contra`, `linarith` and `ring` are unavailable; the
non-linear rewrites are supplied by hand and `omega` closes the linear part.
-/
import Conjecture.Basic

namespace Conjecture

/-! ## Theorem 13 and Theorem 14: the quotient ratchet

These are the load-bearing steps of the finite-start bound (Theorem 18). In the
shifted indexing, the paper's index `n` is `k+1`, so the paper's smallness
hypothesis `3 q_n ≤ n + 1` reads `3 * Q m k ≤ k + 2`, a down-step at `n` reads
`Q m (k+1) + 1 = Q m k`, and an up-step at `n+1` reads
`Q m (k+2) = Q m (k+1) + 1`. -/

/-- The exact linear relation across one down-step. Writing `P = Q m (k+1)`,
this is the paper's `r_{n+1} = 2 r_n - q_n + n + 1` with all subtraction cleared:
the two quadratic terms cancel, leaving something `omega` can use. -/
private theorem down_step_linear {m k : Nat} (hdown : Q m (k + 1) + 1 = Q m k) :
    Q m (k + 1) + R m (k + 1) = (k + 1) + 2 * R m k := by
  have h1 : (k + 1 + 1) * Q m (k + 1) + R m (k + 1) = B m (k + 1) :=
    div_mod_id m (k + 1)
  have h2 : B m (k + 1) = (k + 1) * Q m k + 2 * R m k := B_succ_qr m k
  have h3 : (k + 1) * Q m k = (k + 1) * Q m (k + 1) + (k + 1) := by
    rw [← hdown, Nat.mul_succ]
  have h4 : (k + 1 + 1) * Q m (k + 1) = (k + 1) * Q m (k + 1) + Q m (k + 1) :=
    Nat.succ_mul (k + 1) (Q m (k + 1))
  omega

/-- The quotient never falls by more than one while it is small. This is the
part of the bounded-quotient lemma that the ratchet needs. -/
theorem quotient_drop_le_one {m k : Nat} (hsmall : 3 * Q m k ≤ k + 2) :
    Q m k ≤ Q m (k + 1) + 1 := by
  -- `by_contra` is a mathlib tactic, so split on trichotomy by hand.
  rcases Nat.lt_or_ge (Q m (k + 1) + 1) (Q m k) with hcon | hok
  · exfalso
    have hge : Q m (k + 1) + 2 ≤ Q m k := by omega
    have h1 : (k + 1 + 1) * Q m (k + 1) + R m (k + 1) = B m (k + 1) :=
      div_mod_id m (k + 1)
    have h2 : B m (k + 1) = (k + 1) * Q m k + 2 * R m k := B_succ_qr m k
    have hlt : R m (k + 1) < k + 1 + 1 := Nat.mod_lt _ (by omega)
    -- Monotonicity of multiplication turns the gap of two into `Q m (k+1) ≥ k+1`.
    have hmul : (k + 1) * (Q m (k + 1) + 2) ≤ (k + 1) * Q m k :=
      Nat.mul_le_mul (Nat.le_refl (k + 1)) hge
    have hexp : (k + 1) * (Q m (k + 1) + 2)
        = (k + 1) * Q m (k + 1) + (k + 1) + (k + 1) := by
      rw [Nat.mul_add]
      omega
    have h4 : (k + 1 + 1) * Q m (k + 1) = (k + 1) * Q m (k + 1) + Q m (k + 1) :=
      Nat.succ_mul (k + 1) (Q m (k + 1))
    omega
  · exact hok

/-- **Theorem 13 (forced rebound).** A down-step in the small-quotient region is
immediately undone. -/
theorem forced_rebound {m k : Nat}
    (hdown : Q m (k + 1) + 1 = Q m k)
    (hsmall : 3 * Q m k ≤ k + 2) :
    Q m (k + 2) = Q m (k + 1) + 1 := by
  have hlin := down_step_linear hdown
  have hlt : R m (k + 1) < k + 1 + 1 := Nat.mod_lt _ (by omega)
  -- The next numerator `2 R m (k+1) - Q m (k+1)` lands in `[k+3, 2(k+3))`.
  obtain ⟨rho, hrho⟩ : ∃ rho, 2 * R m (k + 1) = Q m (k + 1) + (k + 3) + rho :=
    ⟨2 * R m (k + 1) - (Q m (k + 1) + (k + 3)), by omega⟩
  have hrholt : rho < k + 3 := by omega
  -- Rebuild `B m (k+2)` as `(k+3) * (Q m (k+1) + 1) + rho`.
  have hB : B m (k + 2) = (k + 1 + 1) * Q m (k + 1) + 2 * R m (k + 1) :=
    B_succ_qr m (k + 1)
  have hsplit : (k + 3) * Q m (k + 1)
      = (k + 1 + 1) * Q m (k + 1) + Q m (k + 1) :=
    Nat.succ_mul (k + 1 + 1) (Q m (k + 1))
  have hcollect : (k + 3) * Q m (k + 1) + (k + 3) = (k + 3) * (Q m (k + 1) + 1) :=
    (Nat.mul_succ (k + 3) (Q m (k + 1))).symm
  have hform : B m (k + 2) = rho + (k + 3) * (Q m (k + 1) + 1) := by omega
  show B m (k + 2) / (k + 2 + 1) = Q m (k + 1) + 1
  have e3 : k + 2 + 1 = k + 3 := by omega
  rw [e3, hform, Nat.add_mul_div_left _ _ (show 0 < k + 3 by omega),
      Nat.div_eq_of_lt hrholt]
  omega

/-- **Theorem 14 (ratchet).** If the quotient stays small for `len` consecutive
indices from `u`, it never falls two below its value at `u`.

The induction carries a stronger invariant than the bare conclusion: at every
index the quotient is either at or above its starting value, or exactly one below
*and* forced back up at the next step. Without the second disjunct the argument
has a gap, because a flat step at one below the starting value would otherwise be
allowed to precede a further descent. -/
theorem ratchet {m u : Nat} (len : Nat)
    (hsmall : ∀ j, j < len → 3 * Q m (u + j) ≤ (u + j) + 2) :
    ∀ j, j ≤ len → Q m u ≤ Q m (u + j) + 1 := by
  -- `invariant j` is the strengthened statement at index `u + j`.
  have key : ∀ j, j ≤ len →
      Q m u ≤ Q m (u + j) ∨
        (Q m u = Q m (u + j) + 1 ∧ Q m (u + j + 1) = Q m (u + j) + 1) := by
    intro j
    induction j with
    | zero => intro _; exact Or.inl (Nat.le_refl _)
    | succ i ih =>
        intro hle
        have hi : i < len := by omega
        have hsm : 3 * Q m (u + i) ≤ (u + i) + 2 := hsmall i hi
        have hstep : u + (i + 1) = (u + i) + 1 := by omega
        rcases ih (by omega) with hat | ⟨hone, hup⟩
        · -- At or above the starting level.
          have hdrop : Q m (u + i) ≤ Q m ((u + i) + 1) + 1 :=
            quotient_drop_le_one hsm
          rcases Nat.lt_or_ge (Q m ((u + i) + 1)) (Q m u) with hlow | hhigh
          · -- The only way below is a down-step from exactly `Q m u`.
            have hdown : Q m ((u + i) + 1) + 1 = Q m (u + i) := by omega
            have := forced_rebound (m := m) (k := u + i) hdown hsm
            rw [hstep]
            exact Or.inr ⟨by omega, by
              have e : u + i + 1 + 1 = u + i + 2 := by omega
              rw [e]; exact this⟩
          · rw [hstep]; exact Or.inl hhigh
        · -- Exactly one below, with the next step already forced upward.
          rw [hstep]
          exact Or.inl (by omega)
  intro j hj
  rcases key j hj with hat | ⟨hone, _⟩
  · omega
  · omega

end Conjecture
