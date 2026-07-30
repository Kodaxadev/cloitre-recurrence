/-
Ingredients for Theorem 18, the finite-start bound `m < (c+3)(3c+5)`.

Indexing as elsewhere: the paper's index `n` is `k+1`, so the paper's
`b_n < n^2` reads `B m k < (k+1)*(k+1)` and its `3 q_n ≤ n+1` reads
`3 * Q m k ≤ k + 2`.

Note on the entry lemma. The paper bounds the entry index by
`⌈√(2m)⌉ + 2`, but that bound is never used in the proof of Theorem 18: the
proof needs only that *some* index satisfies `b_n < n^2`, together with
minimality of the least such index. So no summation estimate is required here,
and the crude bound `B m k ≤ m + k*k` suffices.

Mathlib-free.
-/
import Conjecture.Basic
import Conjecture.Ratchet

namespace Conjecture

/-! ## Entry: some index satisfies `b_n < n^2` -/

/-- A crude but sufficient growth bound: each step adds at most `k`. -/
theorem orbit_upper_bound (m : Nat) : ∀ k, B m k ≤ m + k * k := by
  intro k
  induction k with
  | zero => simp
  | succ i ih =>
      have hmod : B m i % (i + 1) ≤ i := by
        have := Nat.mod_lt (B m i) (show 0 < i + 1 by omega)
        omega
      have hexp : (i + 1) * (i + 1) = i * i + i + i + 1 := by
        rw [Nat.succ_mul, Nat.mul_succ]
        omega
      rw [B_succ]
      omega

/-- **Entry.** Once `k` reaches `m`, the orbit is below the square. In paper
terms: `b_n < n^2` holds at `n = m + 1`, so the entry set is nonempty. -/
theorem entry_exists {m k : Nat} (h : m ≤ k) : B m k < (k + 1) * (k + 1) := by
  have hb := orbit_upper_bound m k
  have hexp : (k + 1) * (k + 1) = k * k + k + k + 1 := by
    rw [Nat.succ_mul, Nat.mul_succ]
    omega
  omega

/-- Below the square the quotient is below the index: the paper's
`b_n < n^2 ⟹ q_n < n`, which is what puts the orbit in the bounded-quotient
region. -/
theorem quotient_lt_index {m k : Nat} (h : B m k < (k + 1) * (k + 1)) :
    Q m k < k + 1 := by
  -- `Q m k = B m k / (k+1)`, so this is division by a bound.
  show B m k / (k + 1) < k + 1
  exact Nat.div_lt_of_lt_mul (by omega)

/-! ## The quadratic step

In the empty-`S` case the paper needs `(n₀-1)^2 < (c+2) n₀ ⟹ n₀ ≤ c+4`. With
`n₀ = j+1` this is the contrapositive below, stated without subtraction. -/

/-- If `j ≥ c+4` then `(c+2)(j+1) < j^2`. Contrapositive of the paper's step
`(n₀-1)^2 < (c+2)n₀ ⟹ n₀ ≤ c+4`, with `n₀ = j+1`. -/
theorem quadratic_step {j c : Nat} (h : c + 4 ≤ j) : (c + 2) * (j + 1) < j * j := by
  have hmul : (c + 4) * j ≤ j * j := Nat.mul_le_mul_right j h
  have hsplit : (c + 4) * j = (c + 2) * j + 2 * j := by
    have e : c + 4 = (c + 2) + 2 := by omega
    rw [e, Nat.succ_mul, Nat.succ_mul]
    omega
  have hgoal : (c + 2) * (j + 1) = (c + 2) * j + (c + 2) := Nat.mul_succ _ _
  omega

/-! ## A least witness

`Nat.find` lives in mathlib, so the least element of a nonempty decidable set of
naturals is extracted here by strong induction. -/

private theorem least_of_exists {P : Nat → Prop} [DecidablePred P] :
    ∀ n, P n → ∃ k, P k ∧ ∀ j, j < k → ¬ P j := by
  intro n
  induction n using Nat.strongRecOn with
  | ind n ih =>
      intro hn
      by_cases hex : ∃ j, j < n ∧ P j
      · obtain ⟨j, hjlt, hpj⟩ := hex
        exact ih j hjlt hpj
      · exact ⟨n, hn, fun j hj hpj => hex ⟨j, hj, hpj⟩⟩

/-- The least index at which the orbit drops below the square, together with its
defining minimality. -/
theorem least_entry (m : Nat) :
    ∃ k, B m k < (k + 1) * (k + 1) ∧
      ∀ j, j < k → ¬ (B m j < (j + 1) * (j + 1)) :=
  least_of_exists m (entry_exists (Nat.le_refl m))

/-- The greatest index at most `N` satisfying a decidable predicate. -/
private theorem greatest_of_exists {P : Nat → Prop} [DecidablePred P] :
    ∀ N, (∃ j, j ≤ N ∧ P j) →
      ∃ k, k ≤ N ∧ P k ∧ ∀ j, k < j → j ≤ N → ¬ P j := by
  intro N
  induction N with
  | zero =>
      intro ⟨j, hj, hpj⟩
      have : j = 0 := by omega
      subst this
      exact ⟨0, Nat.le_refl _, hpj, fun j h1 h2 => absurd h2 (by omega)⟩
  | succ i ih =>
      intro ⟨j, hj, hpj⟩
      by_cases htop : P (i + 1)
      · exact ⟨i + 1, Nat.le_refl _, htop, fun j h1 h2 => absurd h2 (by omega)⟩
      · have hjle : j ≤ i := by
          rcases Nat.lt_or_ge j (i + 1) with h | h
          · omega
          · exact absurd hpj (by have : j = i + 1 := by omega
                                 rw [this]; exact htop)
        obtain ⟨k, hkle, hpk, hmax⟩ := ih ⟨j, hjle, hpj⟩
        refine ⟨k, by omega, hpk, ?_⟩
        intro j h1 h2
        rcases Nat.lt_or_ge j (i + 1) with h | h
        · exact hmax j h1 (by omega)
        · have : j = i + 1 := by omega
          rw [this]; exact htop

/-! ## Forward invariance and the region bound -/

/-- The paper's `b_n < n^2` is forward invariant. -/
theorem entry_forward {m k : Nat} (h : B m k < (k + 1) * (k + 1)) :
    B m (k + 1) < (k + 1 + 1) * (k + 1 + 1) := by
  have hmod : B m k % (k + 1) ≤ k := by
    have := Nat.mod_lt (B m k) (show 0 < k + 1 by omega)
    omega
  have e1 : (k + 1) * (k + 1) = k * k + k + k + 1 := by
    rw [Nat.succ_mul, Nat.mul_succ]; omega
  have e2 : (k + 1 + 1) * (k + 1 + 1) = (k + 1) * (k + 1) + (k + 1) + (k + 1) + 1 := by
    rw [Nat.succ_mul (k + 1), Nat.mul_succ (k + 1)]; omega
  rw [B_succ]
  omega

/-- From the least entry index onwards, the orbit stays below the square. -/
theorem entry_forward_all {m k : Nat} (h : B m k < (k + 1) * (k + 1)) :
    ∀ j, B m (k + j) < (k + j + 1) * (k + j + 1) := by
  intro j
  induction j with
  | zero => exact h
  | succ i ih =>
      have e : k + (i + 1) = (k + i) + 1 := by omega
      rw [e]
      exact entry_forward ih

/-! ## Reading the absorbing ray -/

/-- On the ray the quotient is `c`, matching `ray_mod` for the remainder. -/
theorem ray_quotient {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    Q m k = c := by
  have hr : R m k = c := ray_mod hb hc
  have hd := div_mod_id m k
  rw [hr] at hd
  -- `ray_form` is private in `Basic`, so rebuild the split here.
  have e1 : c * (k + 2) = c * (k + 1) + c := Nat.mul_succ c (k + 1)
  have e2 : c * (k + 1) = (k + 1) * c := Nat.mul_comm c (k + 1)
  exact Nat.eq_of_mul_eq_mul_left (show 0 < k + 1 by omega) (by omega)

/-- The start is a lower bound for the whole orbit from index 1 on. -/
theorem start_le {m k : Nat} (h : 1 ≤ k) : m ≤ B m k := by
  have h1 : B m 1 = m := B_one m
  have := B_monotone m h
  omega

/-- The absorbing ray already lies below the square, so the least entry index is
at most the absorption index. -/
theorem ray_below_square {m k c : Nat} (hb : B m k = c * (k + 2)) (hc : c < k + 1) :
    B m k < (k + 1) * (k + 1) := by
  have hmul : c * (k + 2) ≤ k * (k + 2) := Nat.mul_le_mul_right (k + 2) (by omega)
  have e1 : k * (k + 2) = k * k + k + k := by
    rw [Nat.mul_succ, Nat.mul_succ]; try omega
  have e2 : (k + 1) * (k + 1) = k * k + k + k + 1 := by
    rw [Nat.succ_mul, Nat.mul_succ]; try omega
  omega

/-! ## The final numeric comparisons

Both are proved by chaining monotonicity rather than expanding binomials, which
keeps every `omega` call linear in its atoms. -/

private theorem bound_small (c : Nat) : 2 * (c + 2) < (c + 3) * (3 * c + 5) := by
  have h1 : (c + 3) * 5 ≤ (c + 3) * (3 * c + 5) :=
    Nat.mul_le_mul (Nat.le_refl (c + 3)) (show (5 : Nat) ≤ 3 * c + 5 by omega)
  omega

private theorem bound_empty (c : Nat) : (c + 4) * (c + 2) < (c + 3) * (3 * c + 5) := by
  have h1 : (c + 4) * (c + 2) ≤ (3 * c + 5) * (c + 2) :=
    Nat.mul_le_mul (show c + 4 ≤ 3 * c + 5 by omega) (Nat.le_refl (c + 2))
  have h2 : (3 * c + 5) * (c + 3) = (3 * c + 5) * (c + 2) + (3 * c + 5) :=
    Nat.mul_succ (3 * c + 5) (c + 2)
  have h3 : (3 * c + 5) * (c + 3) = (c + 3) * (3 * c + 5) := Nat.mul_comm _ _
  omega

private theorem bound_nonempty (c : Nat) :
    (3 * c + 4) * (c + 3) < (c + 3) * (3 * c + 5) := by
  -- Stated with `3*c+5` on the left so it shares an atom with `h2`.
  have h1 : (3 * c + 5) * (c + 3) = (3 * c + 4) * (c + 3) + (c + 3) :=
    Nat.succ_mul (3 * c + 4) (c + 3)
  have h2 : (3 * c + 5) * (c + 3) = (c + 3) * (3 * c + 5) := Nat.mul_comm _ _
  omega

/-! ## Theorem 18 -/

/-- **Theorem 18 (finite-start bound), from the ray hypothesis.** If the orbit
from `m ≥ 1` lies on the absorbing ray at index `s`, that is `B m s = c (s+2)`
with `c < s+1`, then

    m < (c+3)(3c+5).

The proof is the paper's, with the ratchet supplying both cases.

**Scope.** The hypothesis here is membership of the ray, which by the absorption
criterion is equivalent to eventual increment `c`. Only one direction of that
equivalence is formalized: `absorb_increment` shows ray implies constant
increment. The converse — eventually constant increment implies ray membership —
rests on a limiting divisibility argument that is *not* formalized, and
`increment_forces_remainder` is only its one-step fragment. So a fully formal
route from "the orbit stabilizes with increment `c`" to this bound is not yet
closed. -/
theorem finite_start {m s c : Nat} (hm : 1 ≤ m)
    (hb : B m s = c * (s + 2)) (hc : c < s + 1) :
    m < (c + 3) * (3 * c + 5) := by
  have hQs : Q m s = c := ray_quotient hb hc
  have hsq : B m s < (s + 1) * (s + 1) := ray_below_square hb hc
  obtain ⟨k0, hk0, hmin⟩ := least_entry m
  -- The ray is already below the square, so the least entry index precedes it.
  have hk0s : k0 ≤ s := by
    rcases Nat.lt_or_ge s k0 with h | h
    · exact absurd hsq (hmin s h)
    · exact h
  -- Index 0 is impossible because `B m 0 = m ≥ 1`.
  have hk01 : 1 ≤ k0 := by
    rcases Nat.lt_or_ge 0 k0 with h | h
    · exact h
    · exfalso
      have hz : k0 = 0 := by omega
      rw [hz] at hk0
      rw [B_zero] at hk0
      omega
  -- From the entry index on, the quotient is below the index.
  have hQle : ∀ j, Q m (k0 + j) ≤ k0 + j := fun j =>
    Nat.le_of_lt_succ (quotient_lt_index (entry_forward_all hk0 j))
  -- `m` is a lower bound for the orbit from index 1 on.
  have hmle : ∀ k, 1 ≤ k → m ≤ B m k := fun k hk => start_le hk
  -- Split on whether the paper's set `S` is empty.
  by_cases hS : ∃ k, k0 ≤ k ∧ k ≤ s ∧ k + 2 < 3 * Q m k
  · -- Nonempty: take the greatest such index.
    obtain ⟨kstar, hkle, ⟨hkge, hbad⟩, hmax⟩ :=
      greatest_of_exists (P := fun k => k0 ≤ k ∧ k + 2 < 3 * Q m k) s
        (by obtain ⟨k, h1, h2, h3⟩ := hS; exact ⟨k, h2, h1, h3⟩)
    -- Above `kstar` the smallness condition holds.
    have hsmall : ∀ j, kstar < j → j ≤ s → 3 * Q m j ≤ j + 2 := by
      intro j h1 h2
      rcases Nat.lt_or_ge (j + 2) (3 * Q m j) with h | h
      · exact absurd ⟨by omega, h⟩ (hmax j h1 h2)
      · omega
    -- The quotient at `kstar` is at most `c + 2`.
    have hQks : Q m kstar ≤ c + 2 := by
      rcases Nat.lt_or_ge kstar s with hlt | hge
      · -- Ratchet on `[kstar+1, s]`, then one step back down.
        obtain ⟨len, hlen⟩ : ∃ len, s = (kstar + 1) + len := ⟨s - (kstar + 1), by omega⟩
        have hr := ratchet (m := m) (u := kstar + 1) len
          (fun j hj => hsmall (kstar + 1 + j) (by omega) (by omega)) len (Nat.le_refl len)
        rw [← hlen] at hr
        obtain ⟨d, hd⟩ : ∃ d, kstar = k0 + d := ⟨kstar - k0, by omega⟩
        have hdrop : Q m kstar ≤ Q m (kstar + 1) + 1 :=
          quotient_drop_le_one_of_le (by rw [hd]; have := hQle d; omega)
        omega
      · have : kstar = s := by omega
        rw [this, hQs]
        omega
    -- Hence `kstar` is small, and the orbit value at `kstar` bounds `m`.
    have hks4 : kstar + 1 ≤ 3 * c + 4 := by omega
    have hdec : (kstar + 1) * Q m kstar + R m kstar = B m kstar := div_mod_id m kstar
    have hrlt : R m kstar ≤ kstar := by
      have := Nat.mod_lt (B m kstar) (show 0 < kstar + 1 by omega)
      have hR : R m kstar = B m kstar % (kstar + 1) := rfl
      omega
    have hstep1 : (kstar + 1) * Q m kstar ≤ (kstar + 1) * (c + 2) :=
      Nat.mul_le_mul (Nat.le_refl (kstar + 1)) hQks
    have hstep2 : (kstar + 1) * (c + 3) = (kstar + 1) * (c + 2) + (kstar + 1) :=
      Nat.mul_succ (kstar + 1) (c + 2)
    have hstep3 : (kstar + 1) * (c + 3) ≤ (3 * c + 4) * (c + 3) :=
      Nat.mul_le_mul hks4 (Nat.le_refl (c + 3))
    have hstep4 := bound_nonempty c
    have := hmle kstar (by omega)
    omega
  · -- Empty: the ratchet applies on all of `[k0, s]`.
    have hsmall : ∀ k, k0 ≤ k → k ≤ s → 3 * Q m k ≤ k + 2 := by
      intro k h1 h2
      rcases Nat.lt_or_ge (k + 2) (3 * Q m k) with h | h
      · exact absurd ⟨k, h1, h2, h⟩ hS
      · omega
    obtain ⟨len, hlen⟩ : ∃ len, s = k0 + len := ⟨s - k0, by omega⟩
    have hr := ratchet (m := m) (u := k0) len
      (fun j hj => hsmall (k0 + j) (by omega) (by omega)) len (Nat.le_refl len)
    rw [← hlen] at hr
    have hQk0 : Q m k0 ≤ c + 1 := by omega
    have hdec : (k0 + 1) * Q m k0 + R m k0 = B m k0 := div_mod_id m k0
    have hrlt : R m k0 ≤ k0 := by
      have := Nat.mod_lt (B m k0) (show 0 < k0 + 1 by omega)
      have hR : R m k0 = B m k0 % (k0 + 1) := rfl
      omega
    have hstep1 : (k0 + 1) * Q m k0 ≤ (k0 + 1) * (c + 1) :=
      Nat.mul_le_mul (Nat.le_refl (k0 + 1)) hQk0
    have hstep2 : (k0 + 1) * (c + 2) = (k0 + 1) * (c + 1) + (k0 + 1) :=
      Nat.mul_succ (k0 + 1) (c + 1)
    have hmk : m ≤ B m k0 := hmle k0 hk01
    -- Collect the orbit facts once, so no later rewrite has to touch `B`.
    have hB : B m k0 < (k0 + 1) * (c + 2) := by omega
    have hmb : m < (k0 + 1) * (c + 2) := by omega
    -- Bound `k0` by `c + 3`, the paper's `n₀ ≤ c + 4`.
    have hk0le : k0 + 1 ≤ c + 4 := by
      rcases Nat.lt_or_ge (c + 3) k0 with hbig | hok
      · exfalso
        obtain ⟨p, hp⟩ : ∃ p, k0 = p + 1 := ⟨k0 - 1, by omega⟩
        have hprev : ¬ (B m p < (p + 1) * (p + 1)) := hmin p (by omega)
        have hmono : B m p ≤ B m k0 := B_monotone m (by omega)
        have hqs := quadratic_step (j := p + 1) (c := c) (by omega)
        have hcomm : (c + 2) * (p + 1 + 1) = (p + 1 + 1) * (c + 2) := Nat.mul_comm _ _
        have hk : (k0 + 1) * (c + 2) = (p + 1 + 1) * (c + 2) := by rw [hp]
        omega
      · omega
    rcases Nat.lt_or_ge k0 2 with hsmallk | hbigk
    · -- `k0 = 1`, the paper's `n₀ = 2`.
      have h1 : k0 = 1 := by omega
      have hsm := bound_small c
      rw [h1] at hmb
      omega
    · -- `k0 ≥ 2`: the quadratic step already bounded `k0`.
      have hstep3 : (k0 + 1) * (c + 2) ≤ (c + 4) * (c + 2) :=
        Nat.mul_le_mul hk0le (Nat.le_refl (c + 2))
      have := bound_empty c
      omega

/-! ## Non-vacuity

The hypotheses of `finite_start` are satisfiable, so the theorem is not empty.
For `m = 5` the orbit reaches the ray at Lean index `6`, that is paper index
`t = 7`, with increment `c = 2` and `b_t = 16`. This is the row
`(m,t,c,b_t) = (5,7,2,16)` of the committed certificate
`certificates/spectrum_m259.csv`, and the same witness appears in Table 1 of the
paper. -/
example : B 5 6 = 2 * (6 + 2) := by rfl

example : (2 : Nat) < 6 + 1 := by omega

/-- The instance of Theorem 18 at that witness: `5 < 5 * 11 = 55`. -/
example : 5 < (2 + 3) * (3 * 2 + 5) :=
  finite_start (m := 5) (s := 6) (c := 2) (by omega) (by rfl) (by omega)

end Conjecture
