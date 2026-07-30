/-
Foundational identities: the orbit `B`, the absorbing ray, congruence
propagation, pair merging, and the doubling coordinate `E`.

Mathlib-free. See `lean/Conjecture.lean` for the module index and the axiom
audit, and `lean/README.md` for what is deliberately NOT formalized.
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

end Conjecture
