# Lean 4 formalization

**Status: compiles clean, no `sorry`, no proof-library dependencies.**

```bash
lake build --wfail                     # compile; warnings are errors
lake env leanchecker Conjecture        # Lean's bundled checker
bash scripts/check_lean_nanoda.sh       # independent Rust checker
```

Checked with **Lean 4.32.2**. The file is deliberately **mathlib-free** so it can
be verified by a bare `lean` binary with no `lake` project, no cache download and
no network. The cost is that `ring`, `linarith` and `push_cast` are unavailable:
every nonlinear rewrite is supplied by hand (`Nat.add_mul`, `Nat.mul_add`,
`Int.mul_sub`) and `omega` closes the linear part. `omega` abstracts nonlinear
subterms as atoms, so the helper lemmas exist to make those atoms match
syntactically.

The compiler pin matters: Lean 4.32.2 fixes a kernel soundness bug present in
4.32.1. CI also pins the external-checker revisions instead of following
mutable branches. The nanoda check permits only `propext`, `Classical.choice`,
`Quot.sound`, and `Lean.trustCompiler`. Unpermitted prelude axioms are skipped;
any checked declaration that uses one, including `sorryAx`, fails.

## Axiom audit

Run at the end of the file. Every theorem reports only Lean's standard axioms —
crucially **`sorryAx` appears nowhere**, so nothing is stubbed:

```
absorb_step, absorb_forever, absorb_increment, increment_forces_remainder,
congruence_propagation, even_at_even_index, pair_merging,
E_doubling_nat, E_doubling_mod, E_doubling, B_monotone
    depends on axioms: [propext, Quot.sound]
E_zero_of_ray
    depends on axioms: [propext, Classical.choice, Quot.sound]
```

## What is formalized

| Lean name | Paper statement |
|---|---|
| `B` | the orbit; `B m k = b_{k+1}`, so `B m 0 = b_1 = m` |
| `B_one` | `b_2 = b_1` (because `b_1 mod 1 = 0`) |
| `B_le_succ`, `B_monotone` | the orbit is non-decreasing |
| `ray_mod` | on the ray `b = c(n+1)` the remainder is exactly `c` |
| `absorb_step` | **Theorem 1**, one step: the ray is forward invariant |
| `absorb_forever` | **Theorem 1**: the orbit stays on the ray at every later index |
| `absorb_increment` | **Theorem 1**: every later increment equals `c` — the actual content of the conjecture's conclusion |
| `increment_forces_remainder` | converse half of Theorem 1 |
| `congruence_propagation` | **Lemma 8**: `d ∣ n ⟹ b_{n+1} ≡ 2 b_n (mod d)` |
| `even_at_even_index` | **Corollary 9**: `b_j` even for odd `j ≥ 3` |
| `pair_odd`, `pair_even`, `pair_merging` | **Theorem 10**: orbits of `2k+1` and `2k+2` coincide from index 3 |
| `Q`, `R`, `E` | `q_n`, `r_n`, and the doubling coordinate `e_n = r_n − q_n` |
| `B_succ_qr` | the transition equation `b_{n+1} = q_n·n + 2 r_n` |
| `E_doubling_nat` | **Theorem 6**, exact subtraction-free form |
| `E_doubling_mod` | **Theorem 6** as a congruence in `Nat` |
| `E_doubling` | **Theorem 6** over `Int`: `(n+2) ∣ (e_{n+1} − 2 e_n)` |
| `E_zero_iff`, `E_zero_of_ray` | stabilization is exactly `e = 0` |

The indexing shift (`B m k = b_{k+1}`) is not cosmetic: it makes the recurrence
structurally recursive, so Lean accepts the definition without a termination
proof and `k+1` is always a positive modulus by construction.

`E_doubling_nat` is the statement worth reading. Over `Int` the theorem is
`e_{n+1} − 2e_n = (q_n − q_{n+1})(n+2)`, but subtraction on `Nat` truncates, so
it is stated as the equivalent identity

```
r_{n+1} + 2 q_n + (n+2) q_{n+1}  =  q_{n+1} + 2 r_n + (n+2) q_n
```

which is exact, has no side conditions at all, and immediately yields both the
`Nat` congruence and the signed `Int` divisibility.

## What is deliberately NOT formalized

Following the instruction to formalize only non-speculative results:

* **Theorems 13, 14, 18** (forced rebound, ratchet, and the bound `m < (c+3)(3c+5)`).
  These are proved on paper and machine-tested exhaustively in
  `search-framework/tests/theorems.rs`, but formalizing them needs case analysis
  on the sign of `2r − q` together with the entry lemma, which is a substantially
  larger development — realistically it wants mathlib. This is the single most
  valuable next formalization target, because Theorem 18 is what makes
  Corollary 20 (the answer to Abercrombie's question) a proof rather than an
  observation.
* **Lemma 3** (entry in `O(√m)` steps) — needs a summation bound.
* **The conjecture itself** — unproved, so there is nothing to formalize.
* **Everything heuristic** — `κ → 1/4`, the epoch transition matrix, the tail
  law. These are explicitly *not* theorems and must not be given the appearance
  of one by being written in Lean.

## Next steps

1. Add mathlib as a pinned dependency, then formalize Lemma 4 (bounded
   quotient) and Lemma 12 — both are pure case analysis on `2r − q`.
2. Theorem 13, then Theorem 14 by the two-clause induction used on paper
   (`q_k ≥ q_n − 1`, and `q_k = q_n − 1 ⟹ Δq_k = +1`).
3. Theorem 18, which then needs only Lemma 3 to be complete.
4. A verified checker for the finite enumeration, which would make Corollary 20
   end-to-end machine-checked.
