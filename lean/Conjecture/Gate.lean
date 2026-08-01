/-
Theorem 133 and its unit case Theorem 130: the pure-upper gate exponent is
unique, plus the upward closure of Lemma 136's gap predicate.

Pure Nat arithmetic -- this module knows nothing about the orbit or the safe
map. Mathlib-free.
-/

namespace Conjecture

/-! ## Theorem 130: the pure-upper unit gate exponent is unique

The two pure-upper window inequalities of Lemma 128, written without any
subtraction, are

    lower h :  n + h + 4 ≤ 2^h * f
    upper h :  2^h * (f + 4) + 2 ≤ n + D + 2 * h

with `D = n - 2U ≤ n`. At most one exponent satisfies both, so the all-unit
pure-upper subsystem is a deterministic map. This is the arithmetic core of
Theorem 130; the safe-map interpretation is not formalized. -/

/-- `1 ≤ 2 ^ h`, proved by hand because mathlib is unavailable. -/
private theorem two_pow_pos (h : Nat) : 1 ≤ 2 ^ h := by
  induction h with
  | zero => rw [Nat.pow_zero]; omega
  | succ j ih => rw [Nat.pow_succ]; omega

/-- `2 ^ (h+1) * c = 2 ^ h * c + 2 ^ h * c`: the doubling rewrite `omega` needs
with both factors abstracted as one atom. -/
private theorem pow_succ_mul_split (h c : Nat) :
    2 ^ (h + 1) * c = 2 ^ h * c + 2 ^ h * c := by
  rw [Nat.pow_succ, Nat.mul_assoc, Nat.two_mul, Nat.mul_add]

/-- Doubling dominates the linear drift: `2^(h+1+k) * c ≥ 2^(h+1) * c + 2k`
whenever `c ≥ 1`. -/
private theorem pow_dominates_linear (h c : Nat) (hc : 1 ≤ c) :
    ∀ k : Nat, 2 ^ (h + 1) * c + 2 * k ≤ 2 ^ (h + 1 + k) * c := by
  have hpos : 2 ≤ 2 ^ (h + 1) * c := by
    have hmul : 1 * 1 ≤ 2 ^ h * c := Nat.mul_le_mul (two_pow_pos h) hc
    have hsplit := pow_succ_mul_split h c
    omega
  intro k
  induction k with
  | zero =>
      have e : h + 1 + 0 = h + 1 := by omega
      rw [e]
      omega
  | succ j ih =>
      have e : h + 1 + (j + 1) = (h + 1 + j) + 1 := by omega
      have hstep : 2 ^ (h + 1 + (j + 1)) * c
          = 2 ^ (h + 1 + j) * c + 2 ^ (h + 1 + j) * c := by
        rw [e]
        exact pow_succ_mul_split (h + 1 + j) c
      rw [hstep]
      omega

/-- One step of the lower window inequality: `lower h` forces
`2^(h+1) * (f + c) ≥ 2n + 2k + 2h + 6` for any offset `c`. -/
private theorem lower_forces_next (n k h f c : Nat)
    (lo : n + k + h + 3 ≤ 2 ^ h * f) :
    2 * n + 2 * k + 2 * h + 6 ≤ 2 ^ (h + 1) * (f + c) := by
  have hsplit : 2 ^ (h + 1) * (f + c) = 2 ^ h * (f + c) + 2 ^ h * (f + c) :=
    pow_succ_mul_split h (f + c)
  have hmono : 2 ^ h * f ≤ 2 ^ h * (f + c) :=
    Nat.mul_le_mul_left (2 ^ h) (Nat.le_add_right f c)
  omega

/-- **Theorem 133 (the pure-upper gap never branches).** For a positive block
of any length `k` with returned residue `f`, at most one exponent satisfies
both pure-upper window inequalities. Here `c` stands for the canonical offset
`2^(k+1)`, which the argument only needs to be a natural number.

Theorem 130 is the unit case `k = 1`, `c = 4`, where the lower window reads
`n + h + 4 ≤ 2^h * f` and the upper window reads
`2^h * (f + 4) + 2 ≤ n + D + 2h`. -/
theorem gate_exponent_unique {n D f k c h h' : Nat}
    (hD : D ≤ n) (hf : 1 ≤ f)
    (lo : n + k + h + 3 ≤ 2 ^ h * f)
    (hi : 2 ^ h * (f + c) + 2 ≤ n + D + 2 * h)
    (lo' : n + k + h' + 3 ≤ 2 ^ h' * f)
    (hi' : 2 ^ h' * (f + c) + 2 ≤ n + D + 2 * h') :
    h = h' := by
  -- A strictly larger exponent always breaks the upper inequality.
  have key : ∀ a b : Nat, n + k + a + 3 ≤ 2 ^ a * f → a < b →
      ¬ (2 ^ b * (f + c) + 2 ≤ n + D + 2 * b) := by
    intro a b hlo hab hup
    obtain ⟨j, hj⟩ : ∃ j, b = a + 1 + j := ⟨b - (a + 1), by omega⟩
    have hdom := pow_dominates_linear a (f + c) (by omega) j
    have hnext := lower_forces_next n k a f c hlo
    rw [hj] at hup
    omega
  rcases Nat.lt_trichotomy h h' with hlt | heq | hgt
  · exact absurd hi' (key h h' lo hlt)
  · exact heq
  · exact absurd hi (key h' h lo' hgt)

/-- **Lemma 136, upward closure.** The predicate `m + r + 4 ≤ 2^(r+2) * f`
defining the forced gap is upward closed in `r`, so the minimum in (136.1) is
well defined. The same doubling argument gives the (135.2) instance. -/
theorem gap_predicate_upward_closed {m f r r' : Nat} (hf : 1 ≤ f)
    (hr : m + r + 4 ≤ 2 ^ (r + 2) * f) (hle : r ≤ r') :
    m + r' + 4 ≤ 2 ^ (r' + 2) * f := by
  obtain ⟨j, hj⟩ : ∃ j, r' = r + j := ⟨r' - r, by omega⟩
  -- `pow_dominates_linear` at exponent base `r + 1` gives the drift bound.
  have hdom := pow_dominates_linear (r + 1) f hf j
  -- Normalize both exponents so `omega` sees the same atoms as `hr`.
  have hhi : r + 1 + 1 + j = r' + 2 := by omega
  have hlo : r + 1 + 1 = r + 2 := by omega
  rw [hhi, hlo] at hdom
  omega

/-- The unit case of Theorem 133, in the exact shape used by Theorem 130. -/
theorem unit_gate_exponent_unique {n D f h h' : Nat}
    (hD : D ≤ n) (hf : 1 ≤ f)
    (lo : n + h + 4 ≤ 2 ^ h * f)
    (hi : 2 ^ h * (f + 4) + 2 ≤ n + D + 2 * h)
    (lo' : n + h' + 4 ≤ 2 ^ h' * f)
    (hi' : 2 ^ h' * (f + 4) + 2 ≤ n + D + 2 * h') :
    h = h' :=
  gate_exponent_unique (k := 1) (c := 4) hD hf (by omega) hi (by omega) hi'

end Conjecture
