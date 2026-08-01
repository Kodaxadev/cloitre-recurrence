/-
Lemma 3's explicit entry bound: `n_0 ≤ ⌈√(2m)⌉ + 2`.

`Conjecture/FiniteStart.lean` formalizes only what Theorem 18 consumes —
existence of an entry index plus minimality — because the proof of Theorem 18
never uses the size of that index. This module supplies the sharp bound the paper
states, for completeness.

Square roots and ceilings are avoided. Since `⌈√(2m)⌉` is by definition the least
`k` with `k² ≥ 2m`, the statement "`n_0 ≤ ⌈√(2m)⌉ + 2`" is equivalent to

    k² ≥ 2m  →  b_{k+2} < (k+2)²,

which is `entry_at_sqrt_bound` below and mentions neither. Paper index `k+2` is
Lean index `k+1`.

Mathlib-free.
-/
import Conjecture.Basic

namespace Conjecture

/-- Doubled orbit bound: `2 b_{i+2} ≤ 2m + i(i+1)`.

This is the paper's telescoped sum `F(n+1) − F(n) ≤ −(n+2)`, carried in the
doubled form so the triangular number needs no division. -/
theorem orbit_bound_doubled (m : Nat) :
    ∀ i, 2 * B m (1 + i) ≤ 2 * m + i * (i + 1) := by
  intro i
  induction i with
  | zero =>
      have h : B m (1 + 0) = m := B_one m
      omega
  | succ j ih =>
      have hidx : 1 + (j + 1) = (1 + j) + 1 := by omega
      have hmod : B m (1 + j) % (1 + j + 1) ≤ 1 + j := by
        have := Nat.mod_lt (B m (1 + j)) (show 0 < 1 + j + 1 by omega)
        omega
      have hexp : (j + 1) * (j + 1 + 1) = j * (j + 1) + 2 * (j + 1) := by
        have e1 : (j + 1) * (j + 1 + 1) = (j + 1) * (j + 1) + (j + 1) :=
          Nat.mul_succ _ _
        have e2 : (j + 1) * (j + 1) = j * (j + 1) + (j + 1) :=
          Nat.succ_mul j (j + 1)
        omega
      rw [hidx, B_succ]
      omega

/-- **Lemma 3, explicit bound.** If `k² ≥ 2m` then the orbit is already below the
square at paper index `k+2`. Since `⌈√(2m)⌉` is the least such `k`, this is
exactly `n_0 ≤ ⌈√(2m)⌉ + 2`. -/
theorem entry_at_sqrt_bound {m k : Nat} (h : 2 * m ≤ k * k) :
    B m (k + 1) < (k + 2) * (k + 2) := by
  have hb := orbit_bound_doubled m k
  have hidx : 1 + k = k + 1 := by omega
  rw [hidx] at hb
  -- `k(k+1) = k² + k`.
  have e1 : k * (k + 1) = k * k + k := Nat.mul_succ k k
  -- `(k+2)² = k² + 4k + 4`.
  have e2 : (k + 2) * (k + 2) = k * k + 4 * k + 4 := by
    -- Stated with `k+2` on the left so it shares an atom with the goal.
    have a1 : (k + 2) * (k + 2) = (k + 1) * (k + 2) + (k + 2) :=
      Nat.succ_mul (k + 1) (k + 2)
    have a2 : (k + 1) * (k + 2) = k * (k + 2) + (k + 2) :=
      Nat.succ_mul k (k + 2)
    have a3 : k * (k + 2) = k * (k + 1) + k := Nat.mul_succ k (k + 1)
    omega
  omega

/-- The bound in the form the paper states it: the least entry index is at most
`⌈√(2m)⌉ + 2`, where `k` is any witness to `k² ≥ 2m` and `least_entry`'s index is
compared against it. -/
theorem least_entry_le_sqrt_bound {m k : Nat} (h : 2 * m ≤ k * k)
    {k0 : Nat} (hk0 : ∀ j, j < k0 → ¬ (B m j < (j + 1) * (j + 1))) :
    k0 ≤ k + 1 := by
  rcases Nat.lt_or_ge (k + 1) k0 with hlt | hge
  · exact absurd (entry_at_sqrt_bound h) (hk0 (k + 1) hlt)
  · exact hge

end Conjecture
