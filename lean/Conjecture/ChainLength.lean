/-
Theorem 145: a chain of `N` consecutive positive blocks satisfies `N ≤ 3C - 13`,
where `C` bounds the budget `G = n - 2U` along the chain.

Pure Nat arithmetic -- like `Conjecture.Gate`, this module knows nothing about
the orbit or the safe map. What is formalized is the combinatorial core: given
sequences satisfying the inequalities the safe map is proved to satisfy in
`docs/proofs/admissible-budget.md`, the length bound follows. That those
inequalities *do* hold of the safe map is Corollary 144 and Lemma 136, which are
manuscript mathematics with raw-trace checks, and is NOT formalized here.

Every hypothesis below names its source:

  `budget_step`   (143.1)   G' + k = G + r + 1
  `residue_cap`   (144.1)   f + 3 ≤ G
  `long_block`    (144.2)   2 ≤ k → 2U + 11 ≤ G
  `zero_gap`      (136.1)   r = 0 → n' + 4 ≤ 4f, with n' = G' + 2U'
  `wraps_grow`    (138.2)   i ≤ U i, since U accumulates the block lengths

Stated with `N + 13 ≤ 3 * C` rather than `N ≤ 3 * C - 13` so that truncated
subtraction plays no part in the statement.

Mathlib-free.
-/

namespace Conjecture

/-! ## Theorem 145: the length of a block chain is bounded by its budget -/

section ChainLength

variable {N C : Nat} {G U r k f : Nat → Nat}

/-- A zero gap can only occur early. If `r i = 0` then the gap predicate holds
at `r = 0`, which caps the child index against `4f`; since `f` is capped by the
budget and the child index grows with `i`, this bounds `i`.

This is the contrapositive: past the threshold, every gap is positive. -/
theorem gap_pos_of_late
    (hcap : ∀ i, i < N → G i ≤ C)
    (hfour : ∀ i, i < N → 4 ≤ G i)
    (hwraps : ∀ i, i < N → i ≤ U i)
    (hres : ∀ i, i < N → f i + 3 ≤ G i)
    (hzero : ∀ i, i + 1 < N → r i = 0 → G (i + 1) + 2 * U (i + 1) + 4 ≤ 4 * f i)
    (i : Nat) (hi : i + 1 < N) (hlate : 2 * C < i + 11) :
    1 ≤ r i := by
  rcases Nat.lt_or_ge 0 (r i) with h | h
  · omega
  · -- `r i = 0`, so the child index is squeezed between `2i + 10` and `4C - 16`.
    have hzero' := hzero i hi (by omega)
    have hres' := hres i (by omega)
    have hcap' := hcap i (by omega)
    have hfour' := hfour (i + 1) hi
    have hwraps' := hwraps (i + 1) hi
    omega

/-- A block longer than one wrap can only occur early: it needs
`2U + 11 ≤ G ≤ C`, and `U` is at least the block index. -/
theorem block_unit_of_late
    (hcap : ∀ i, i < N → G i ≤ C)
    (hwraps : ∀ i, i < N → i ≤ U i)
    (hone : ∀ i, i < N → 1 ≤ k i)
    (hlong : ∀ i, i < N → 2 ≤ k i → 2 * U i + 11 ≤ G i)
    (i : Nat) (hi : i < N) (hlate : C < 2 * i + 11) :
    k i = 1 := by
  rcases Nat.lt_or_ge (k i) 2 with h | h
  · have := hone i hi
    omega
  · have hlong' := hlong i hi h
    have hcap' := hcap i hi
    have hwraps' := hwraps i hi
    omega

/-- Past the threshold `2C ≤ i + 10`, both `k i = 1` and `1 ≤ r i`, so the
budget climbs by at least one at every step. -/
theorem budget_climbs
    (hcap : ∀ i, i < N → G i ≤ C)
    (hfour : ∀ i, i < N → 4 ≤ G i)
    (hwraps : ∀ i, i < N → i ≤ U i)
    (hone : ∀ i, i < N → 1 ≤ k i)
    (hres : ∀ i, i < N → f i + 3 ≤ G i)
    (hlong : ∀ i, i < N → 2 ≤ k i → 2 * U i + 11 ≤ G i)
    (hzero : ∀ i, i + 1 < N → r i = 0 → G (i + 1) + 2 * U (i + 1) + 4 ≤ 4 * f i)
    (hstep : ∀ i, i + 1 < N → G (i + 1) + k i = G i + r i + 1)
    (i : Nat) (hi : i + 1 < N) (hlate : 2 * C ≤ i + 10) :
    G i + 1 ≤ G (i + 1) := by
  have hk : k i = 1 :=
    block_unit_of_late hcap hwraps hone hlong i (by omega) (by omega)
  have hr : 1 ≤ r i :=
    gap_pos_of_late hcap hfour hwraps hres hzero i hi (by omega)
  have hs := hstep i hi
  omega

/-- Iterating the climb: `t` steps past the threshold raise the budget by `t`. -/
theorem budget_climbs_iter
    (hcap : ∀ i, i < N → G i ≤ C)
    (hfour : ∀ i, i < N → 4 ≤ G i)
    (hwraps : ∀ i, i < N → i ≤ U i)
    (hone : ∀ i, i < N → 1 ≤ k i)
    (hres : ∀ i, i < N → f i + 3 ≤ G i)
    (hlong : ∀ i, i < N → 2 ≤ k i → 2 * U i + 11 ≤ G i)
    (hzero : ∀ i, i + 1 < N → r i = 0 → G (i + 1) + 2 * U (i + 1) + 4 ≤ 4 * f i)
    (hstep : ∀ i, i + 1 < N → G (i + 1) + k i = G i + r i + 1)
    (i : Nat) (hlate : 2 * C ≤ i + 10) :
    ∀ t, i + t < N → G i + t ≤ G (i + t) := by
  intro t
  induction t with
  | zero =>
    intro _
    -- `i + 0` is definitionally `i`, but `omega` abstracts the two as distinct
    -- atoms, so the reduction is made explicit.
    show G i + 0 ≤ G i
    omega
  | succ s ih =>
    intro hlt
    have hprev : G i + s ≤ G (i + s) := ih (by omega)
    have hclimb : G (i + s) + 1 ≤ G (i + s + 1) :=
      budget_climbs hcap hfour hwraps hone hres hlong hzero hstep (i + s)
        (by omega) (by omega)
    show G i + (s + 1) ≤ G (i + s + 1)
    omega

/-- **Theorem 145.** A chain of `N ≥ 2` consecutive positive blocks whose budget
never exceeds `C` satisfies `N + 13 ≤ 3 * C`.

Equivalently `N ≤ 3C - 13`, and equivalently again: a chain of length `N` must
somewhere reach budget at least `(N + 13) / 3`. -/
theorem chain_length_bound
    (hN : 2 ≤ N)
    (hcap : ∀ i, i < N → G i ≤ C)
    (hfour : ∀ i, i < N → 4 ≤ G i)
    (hwraps : ∀ i, i < N → i ≤ U i)
    (hone : ∀ i, i < N → 1 ≤ k i)
    (hres : ∀ i, i < N → f i + 3 ≤ G i)
    (hlong : ∀ i, i < N → 2 ≤ k i → 2 * U i + 11 ≤ G i)
    (hzero : ∀ i, i + 1 < N → r i = 0 → G (i + 1) + 2 * U (i + 1) + 4 ≤ 4 * f i)
    (hstep : ∀ i, i + 1 < N → G (i + 1) + k i = G i + r i + 1) :
    N + 13 ≤ 3 * C := by
  -- The budget at the first block already forces `4 ≤ C`.
  have hC4 : 4 ≤ C := by
    have h0 := hfour 0 (by omega)
    have h1 := hcap 0 (by omega)
    omega
  -- Past index `2C - 10` the budget climbs by one per block.
  have hlate : 2 * C ≤ (2 * C - 10) + 10 := by omega
  have hclimb :=
    budget_climbs_iter hcap hfour hwraps hone hres hlong hzero hstep
      (2 * C - 10) hlate
  rcases Nat.lt_or_ge (2 * C - 10) (N - 1) with h | h
  · -- The chain outlasts the threshold, so the climb runs to its last block.
    have hreach : (2 * C - 10) + (N - 1 - (2 * C - 10)) < N := by omega
    have hgrow := hclimb (N - 1 - (2 * C - 10)) hreach
    have hstart := hfour (2 * C - 10) (by omega)
    have hend := hcap ((2 * C - 10) + (N - 1 - (2 * C - 10))) hreach
    omega
  · -- The chain ends before the threshold, which is the weaker bound.
    omega

/-! ## The hypotheses are satisfiable

A theorem with eight hypotheses is worth nothing if they cannot hold together,
so here they are discharged against a literal chain: the safe-map start
`(n, U, e) = (8, 0, 7)`, whose two blocks have

    budgets 7, 7    wrap counts 1, 2    lengths 1, 1
    residues 4, 2   gaps 0, 2

closed up as `G i = 7`, `U i = i + 1`, `k i = 1`, `f i = 4 - 2i`, `r i = 2i`.
The conclusion `15 ≤ 21` is not the point; the point is that every hypothesis of
`chain_length_bound` holds simultaneously, so it is not vacuous. This chain is
also the extremal one found by `independent/verify_admissible_slack.py`: it has
the largest observed ratio of length to bound, `2 / (3 * 7 - 13)`. -/
example : (2 : Nat) + 13 ≤ 3 * 7 :=
  chain_length_bound (N := 2) (C := 7)
    (G := fun _ => 7) (U := fun i => i + 1) (r := fun i => 2 * i)
    (k := fun _ => 1) (f := fun i => 4 - 2 * i)
    (by omega)
    (by intro i _; omega)
    (by intro i _; omega)
    (by intro i _; omega)
    (by intro i _; omega)
    (by intro i _; omega)
    (by intro i _ _; omega)
    (by intro i hi _; omega)
    (by intro i hi; omega)

end ChainLength

end Conjecture
