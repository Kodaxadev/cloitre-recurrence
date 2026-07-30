/-
Formalization of the proved core of the A073117 / A117846 stabilization problem.

  b_1 = m,   b_{n+1} = b_n + (b_n mod n)

Indexing: `B m k` denotes `b_{k+1}`, so `B m 0 = b_1 = m` and the recurrence
becomes `B m (k+1) = B m k + B m k % (k+1)`, which is structurally recursive.

This file is deliberately MATHLIB-FREE so it can be checked by a bare `lean`
binary with no package setup:

    lean lean/Conjecture.lean

Because mathlib is unavailable, `ring`, `linarith` and `push_cast` are not used;
every nonlinear rewrite is supplied explicitly and `omega` finishes the linear
part (it abstracts non-linear subterms as atoms, so the atoms are made to match
by hand).

Formalized here:
  * Theorem 1  (Absorption): the ray b = c(n+1) is invariant; increments are c
  * Theorem 10 (Pair merging) and orbit coincidence from index 3 on
  * Lemma 8    (Congruence propagation) and Corollary 9 (parity)
  * Theorem 6  (Doubling coordinate) in the form (n+2) ∣ (e_{n+1} - 2 e_n)

See lean/README.md for what is deliberately NOT formalized.
-/

namespace Conjecture

/-! ## Arithmetic helpers (stand-ins for `ring`) -/

private theorem nat_mul_add2 (a b : Nat) : a * (b + 2) = a * b + a + a := by
  rw [Nat.mul_add]; omega

private theorem nat_mul_add3 (a b : Nat) : a * (b + 3) = a * b + a + a + a := by
  rw [Nat.mul_add]; omega

/-- `c * (k+2) = c + (k+1) * c`, the shape needed by `Nat.add_mul_mod_self_left`. -/
private theorem ray_form (c k : Nat) : c * (k + 2) = c + (k + 1) * c := by
  have h1 : c * (k + 2) = c * k + c + c := nat_mul_add2 c k
  have h2 : (k + 1) * c = k * c + 1 * c := Nat.add_mul k 1 c
  have h3 : c * k = k * c := Nat.mul_comm c k
  omega

private theorem ray_succ (c k : Nat) : c * (k + 3) = c * (k + 2) + c := by
  have h1 : c * (k + 3) = c * k + c + c + c := nat_mul_add3 c k
  have h2 : c * (k + 2) = c * k + c + c := nat_mul_add2 c k
  omega

/-! ## The orbit -/

/-- `B m k = b_{k+1}`, the orbit of the recurrence started at `b_1 = m`. -/
def B (m : Nat) : Nat → Nat
  | 0     => m
  | k + 1 => B m k + B m k % (k + 1)

@[simp] theorem B_zero (m : Nat) : B m 0 = m := rfl

@[simp] theorem B_succ (m k : Nat) : B m (k + 1) = B m k + B m k % (k + 1) := rfl

/-- `b_2 = b_1`, because `b_1 mod 1 = 0`. -/
theorem B_one (m : Nat) : B m 1 = m := by
  rw [B_succ, B_zero, Nat.mod_one]; omega

/-- The orbit is non-decreasing. -/
theorem B_le_succ (m k : Nat) : B m k ≤ B m (k + 1) := by
  rw [B_succ]; omega

theorem B_monotone (m : Nat) {j k : Nat} (h : j ≤ k) : B m j ≤ B m k := by
  induction k with
  | zero =>
    have : j = 0 := by omega
    subst this; exact Nat.le_refl _
  | succ n ih =>
    rcases Nat.lt_or_ge j (n + 1) with hj | hj
    · exact Nat.le_trans (ih (by omega)) (B_le_succ m n)
    · have : j = n + 1 := by omega
      subst this; exact Nat.le_refl _

/-! ## Theorem 1 — the absorbing state

In the shifted indexing, `b_n = c*(n+1)` with `c < n` at `n = k+1` reads
`B m k = c*(k+2)` with `c < k+1`. -/

/-- The remainder on the ray is exactly `c`. -/
theorem ray_mod {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    B m k % (k + 1) = c := by
  rw [hb, ray_form c k, Nat.add_mul_mod_self_left, Nat.mod_eq_of_lt hc]

/-- One absorbing step: the ray `b = c(n+1)` is forward invariant. -/
theorem absorb_step {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    B m (k + 1) = c * (k + 3) ∧ c < k + 2 := by
  refine ⟨?_, by omega⟩
  rw [B_succ, ray_mod hb hc, hb, ray_succ c k]

/-- Absorption persists forever: the orbit stays on the ray at every later index. -/
theorem absorb_forever {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    ∀ j, B m (k + j) = c * (k + j + 2) ∧ c < k + j + 1 := by
  intro j
  induction j with
  | zero => exact ⟨hb, hc⟩
  | succ i ih =>
    obtain ⟨hb', hc'⟩ := ih
    have h := absorb_step (m := m) (k := k + i) (c := c) hb' hc'
    have e : k + (i + 1) = (k + i) + 1 := by omega
    rw [e]
    exact ⟨h.1, h.2⟩

/-- Once absorbed, every subsequent increment equals `c`. This is the statement
the conjecture is about: `b_{n+1} - b_n = c` for all large `n`. -/
theorem absorb_increment {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    ∀ j, B m (k + j + 1) = B m (k + j) + c := by
  intro j
  obtain ⟨h1, h2⟩ := absorb_forever hb hc j
  have h := absorb_step (m := m) (k := k + j) (c := c) h1 h2
  have e : c * (k + j + 3) = c * (k + j + 2) + c := ray_succ c (k + j)
  rw [h.1, h1, e]

/-- Converse half of Theorem 1: a constant increment `c < n` forces the
remainder to be `c`. -/
theorem increment_forces_remainder {m k c : Nat}
    (hstep : B m (k + 1) = B m k + c) : B m k % (k + 1) = c := by
  rw [B_succ] at hstep; omega

/-! ## Lemma 8 — congruence propagation, and Corollary 9 — parity -/

/-- If `d ∣ n` then `b_{n+1} ≡ 2 b_n (mod d)`. Here `n = k+1`. -/
theorem congruence_propagation {m k d : Nat} (hd : d ∣ (k + 1)) :
    B m (k + 1) % d = (2 * B m k) % d := by
  have key : B m k % (k + 1) % d = B m k % d := Nat.mod_mod_of_dvd _ hd
  have h2 : 2 * B m k = B m k + B m k := by omega
  rw [B_succ, h2, Nat.add_mod, key, ← Nat.add_mod]

/-- Corollary 9: `b_j` is even for every odd `j ≥ 3`; in this indexing,
`B m k` is even whenever `k` is even and positive. -/
theorem even_at_even_index {m k : Nat} (h : 2 ∣ (k + 1)) : B m (k + 1) % 2 = 0 := by
  have hc := congruence_propagation (m := m) (k := k) (d := 2) h
  have : (2 * B m k) % 2 = 0 := by omega
  omega

/-! ## Theorem 10 — pair merging -/

theorem pair_odd (k : Nat) : B (2 * k + 1) 2 = 2 * k + 2 := by
  have h : (2 * k + 1) % 2 = 1 := by omega
  rw [B_succ, B_one, h]

theorem pair_even (k : Nat) : B (2 * k + 2) 2 = 2 * k + 2 := by
  have h : (2 * k + 2) % 2 = 0 := by omega
  rw [B_succ, B_one, h]

/-- The orbits of `2k+1` and `2k+2` are literally equal from index 3 onwards. -/
theorem pair_merging (k : Nat) :
    ∀ j, B (2 * k + 1) (2 + j) = B (2 * k + 2) (2 + j) := by
  intro j
  induction j with
  | zero => rw [pair_odd, pair_even]
  | succ i ih =>
    have e : 2 + (i + 1) = (2 + i) + 1 := by omega
    rw [e, B_succ, B_succ, ih]

/-! ## Theorem 6 — the doubling coordinate

`q_n = b_n / n`, `r_n = b_n mod n`, `e_n = r_n - q_n`. At `n = k+1` these are
`Q m k`, `R m k`, `E m k`. `E` is taken in `Int` because `e` is genuinely signed.
-/

def Q (m k : Nat) : Nat := B m k / (k + 1)
def R (m k : Nat) : Nat := B m k % (k + 1)
def E (m k : Nat) : Int := (R m k : Int) - (Q m k : Int)

theorem div_mod_id (m k : Nat) : (k + 1) * Q m k + R m k = B m k :=
  Nat.div_add_mod _ _

/-- The exact one-step relation `b_{n+1} = q_n n + 2 r_n`, here at `n = k+1`. -/
theorem B_succ_qr (m k : Nat) : B m (k + 1) = (k + 1) * Q m k + 2 * R m k := by
  have h := div_mod_id m k
  rw [B_succ]
  show B m k + R m k = (k + 1) * Q m k + 2 * R m k
  omega

/-- **Theorem 6, exact form.** The one-step law for the doubling coordinate
`e_n = r_n - q_n`, written without subtraction so it lives in `Nat`:

  `r_{n+1} + 2 q_n + (n+2) q_{n+1}  =  q_{n+1} + 2 r_n + (n+2) q_n`.

Rearranged over `Int` this says exactly `e_{n+1} - 2 e_n = (q_n - q_{n+1})(n+2)`,
i.e. `e_{n+1} ≡ 2 e_n (mod n+2)`, with the quotient increment `Δq_n` as the
coefficient — which is what makes `Δq` the digit sequence of `e`. -/
theorem E_doubling_nat (m k : Nat) :
    R m (k + 1) + 2 * Q m k + (k + 3) * Q m (k + 1)
      = Q m (k + 1) + 2 * R m k + (k + 3) * Q m k := by
  have h1 : B m (k + 1) = (k + 1) * Q m k + 2 * R m k := B_succ_qr m k
  have h2 : (k + 1 + 1) * Q m (k + 1) + R m (k + 1) = B m (k + 1) := div_mod_id m (k + 1)
  have e1 : (k + 3) * Q m k = (k + 1) * Q m k + 2 * Q m k := by
    have a1 : (k + 3) * Q m k = k * Q m k + 3 * Q m k := Nat.add_mul k 3 (Q m k)
    have a2 : (k + 1) * Q m k = k * Q m k + 1 * Q m k := Nat.add_mul k 1 (Q m k)
    omega
  have e2 : (k + 3) * Q m (k + 1) = (k + 1 + 1) * Q m (k + 1) + Q m (k + 1) := by
    have a1 : (k + 3) * Q m (k + 1) = k * Q m (k + 1) + 3 * Q m (k + 1) :=
      Nat.add_mul k 3 (Q m (k + 1))
    have a2 : (k + 1 + 1) * Q m (k + 1) = k * Q m (k + 1) + 2 * Q m (k + 1) :=
      Nat.add_mul k 2 (Q m (k + 1))
    omega
  omega

/-- **Theorem 6, congruence form.** `e_{n+1} ≡ 2 e_n (mod n+2)`, stated without
subtraction: `r_{n+1} + 2 q_n ≡ q_{n+1} + 2 r_n (mod n+2)`. -/
theorem E_doubling_mod (m k : Nat) :
    (R m (k + 1) + 2 * Q m k) % (k + 3) = (Q m (k + 1) + 2 * R m k) % (k + 3) := by
  calc (R m (k + 1) + 2 * Q m k) % (k + 3)
      = (R m (k + 1) + 2 * Q m k + (k + 3) * Q m (k + 1)) % (k + 3) :=
        (Nat.add_mul_mod_self_left _ _ _).symm
    _ = (Q m (k + 1) + 2 * R m k + (k + 3) * Q m k) % (k + 3) := by
        rw [E_doubling_nat m k]
    _ = (Q m (k + 1) + 2 * R m k) % (k + 3) := Nat.add_mul_mod_self_left _ _ _

/-- **Theorem 6, signed form.** `(n+2) ∣ (e_{n+1} - 2 e_n)` over `Int`, with the
witness `q_n - q_{n+1} = -Δq_n`. -/
theorem E_doubling (m k : Nat) :
    ((k : Int) + 3) ∣ (E m (k + 1) - 2 * E m k) := by
  have hn := E_doubling_nat m k
  have c1 : (((k + 3) * Q m k : Nat) : Int) = ((k : Int) + 3) * ((Q m k : Nat) : Int) := by
    rw [Int.natCast_mul]; simp
  have c2 : (((k + 3) * Q m (k + 1) : Nat) : Int)
      = ((k : Int) + 3) * ((Q m (k + 1) : Nat) : Int) := by
    rw [Int.natCast_mul]; simp
  refine ⟨(Q m k : Int) - (Q m (k + 1) : Int), ?_⟩
  have e3 : ((k : Int) + 3) * ((Q m k : Int) - (Q m (k + 1) : Int))
      = ((k : Int) + 3) * (Q m k : Int) - ((k : Int) + 3) * (Q m (k + 1) : Int) :=
    Int.mul_sub _ _ _
  unfold E
  omega

/-- Stabilization is exactly `e = 0`. -/
theorem E_zero_iff (m k : Nat) : E m k = 0 ↔ Q m k = R m k := by
  unfold E; omega

/-- On the absorbing ray the coordinate `e` really is zero. -/
theorem E_zero_of_ray {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    E m k = 0 := by
  have hr : R m k = c := ray_mod hb hc
  have hq : Q m k = c := by
    have h := div_mod_id m k
    rw [hr] at h
    have hb' : B m k = c + (k + 1) * c := by rw [hb, ray_form c k]
    have : (k + 1) * Q m k = (k + 1) * c := by omega
    exact Nat.eq_of_mul_eq_mul_left (by omega) this
  rw [E_zero_iff, hq, hr]

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
end Audit
