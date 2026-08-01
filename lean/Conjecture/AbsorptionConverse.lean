/-
The absorption converse: eventually constant increment implies ray membership.

This is the direction of the absorption criterion that `absorb_increment` does
not supply, and it is what bridges an eventual-increment hypothesis to
`finite_start`. With it, Theorem 18 holds in the form the paper states and
Corollary 20 consumes.

The argument is the paper's: a fixed quantity is divisible by every large index,
hence zero. Rather than introduce `Int` for that quantity, the key identity is
kept subtraction-free as

    P * q + c (s+2) = B m s + c * P,        P = s + j + 1,

after which `q > c` and `q < c` are each contradicted by choosing `j` past both
`B m s` and `c (s+2)`.

Mathlib-free.
-/
import Conjecture.Basic
import Conjecture.FiniteStart

namespace Conjecture

/-- The increment hypothesis pins every remainder from `s` on. -/
private theorem remainder_of_increment {m s c : Nat}
    (hinc : ∀ j, B m (s + j + 1) = B m (s + j) + c) (j : Nat) :
    R m (s + j) = c := by
  have h := hinc j
  rw [B_succ] at h
  show B m (s + j) % (s + j + 1) = c
  omega

/-- With constant increment the orbit is arithmetic. -/
private theorem orbit_arithmetic {m s c : Nat}
    (hinc : ∀ j, B m (s + j + 1) = B m (s + j) + c) :
    ∀ j, B m (s + j) = B m s + c * j := by
  intro j
  induction j with
  | zero => simp
  | succ i ih =>
      have e : s + (i + 1) = (s + i) + 1 := by omega
      rw [e, hinc i, ih, Nat.mul_succ]
      omega

/-- The arithmetic core, stated for an arbitrary index so that no abbreviation
tactic is needed (`set` is mathlib). Choosing `j` past both `B0` and `c(s+2)`
makes each strict comparison of the quotient against `c` impossible. -/
private theorem ray_of_key {b0 c s j q : Nat}
    (hkey : (s + j + 1) * q + c * (s + 2) = b0 + c * (s + j + 1))
    (hbig1 : b0 ≤ j) (hbig2 : c * (s + 2) ≤ j) :
    b0 = c * (s + 2) := by
  have hcomm : (s + j + 1) * c = c * (s + j + 1) := Nat.mul_comm _ _
  rcases Nat.lt_trichotomy q c with hlt | heq | hgt
  · exfalso
    have hstep : (s + j + 1) * (q + 1) ≤ (s + j + 1) * c :=
      Nat.mul_le_mul (Nat.le_refl _) (by omega)
    have hexp : (s + j + 1) * (q + 1) = (s + j + 1) * q + (s + j + 1) :=
      Nat.mul_succ _ _
    omega
  · rw [heq] at hkey
    omega
  · exfalso
    have hstep : (s + j + 1) * (c + 1) ≤ (s + j + 1) * q :=
      Nat.mul_le_mul (Nat.le_refl _) (by omega)
    have hexp : (s + j + 1) * (c + 1) = (s + j + 1) * c + (s + j + 1) :=
      Nat.mul_succ _ _
    omega

/-- **Absorption converse.** If the increment is `c` at every index from `s` on,
then the orbit lies on the absorbing ray at `s`.

In paper terms: eventual increment `c` from index `t = s+1` forces
`b_t = c(t+1)` and `c < t`. -/
theorem ray_of_eventual_increment {m s c : Nat}
    (hinc : ∀ j, B m (s + j + 1) = B m (s + j) + c) :
    B m s = c * (s + 2) ∧ c < s + 1 := by
  -- `c` is a remainder modulo `s+1`, so it is already small.
  have hc : c < s + 1 := by
    have h0 := remainder_of_increment hinc 0
    have hlt : R m (s + 0) < s + 0 + 1 :=
      Nat.mod_lt (B m (s + 0)) (show 0 < s + 0 + 1 by omega)
    omega
  refine ⟨?_, hc⟩
  -- Evaluate at one index past both obstructions.
  have hdec := div_mod_id m (s + (B m s + c * (s + 2)))
  rw [remainder_of_increment hinc (B m s + c * (s + 2)),
      orbit_arithmetic hinc (B m s + c * (s + 2))] at hdec
  -- Rebuild the subtraction-free key identity.
  have e1 : c * (s + (B m s + c * (s + 2)) + 1)
      = c * (s + 1) + c * (B m s + c * (s + 2)) := by
    have e : s + (B m s + c * (s + 2)) + 1 = (s + 1) + (B m s + c * (s + 2)) := by
      omega
    rw [e, Nat.mul_add]
  have e2 : c * (s + 2) = c * (s + 1) + c := Nat.mul_succ c (s + 1)
  exact ray_of_key
    (b0 := B m s) (c := c) (s := s) (j := B m s + c * (s + 2))
    (q := Q m (s + (B m s + c * (s + 2)))) (by omega) (by omega) (by omega)

/-- **Theorem 18, in the paper's form.** If the orbit from `m ≥ 1` has constant
increment `c` from some index on, then `m < (c+3)(3c+5)`.

This is `finite_start` with its ray hypothesis discharged, so the chain from an
eventual-increment assumption to the bound is now fully formal. -/
theorem finite_start_of_increment {m s c : Nat} (hm : 1 ≤ m)
    (hinc : ∀ j, B m (s + j + 1) = B m (s + j) + c) :
    m < (c + 3) * (3 * c + 5) := by
  obtain ⟨hb, hc⟩ := ray_of_eventual_increment hinc
  exact finite_start hm hb hc

/-! ## Round trip

`absorb_increment` produces exactly the hypothesis `finite_start_of_increment`
consumes, so the two directions of the absorption criterion compose. Instantiated
at the certificate row `(m,t,c,b_t) = (5,7,2,16)`, which is also Table 1 of the
paper: the ray at Lean index `6` yields constant increment `2`, and that in turn
yields the bound `5 < 55`. -/
example : 5 < (2 + 3) * (3 * 2 + 5) :=
  finite_start_of_increment (m := 5) (s := 6) (c := 2) (by omega)
    (absorb_increment (m := 5) (k := 6) (c := 2) (by rfl) (by omega))

end Conjecture
