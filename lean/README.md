# Lean 4 formalization

**Status: compiles clean, no `sorry`, no proof-library dependencies.**

```bash
lake build --wfail                     # compile; warnings are errors
lake env lean lean/Conjecture.lean     # compile and print the axiom audit
lake env leanchecker Conjecture        # Lean's bundled checker
bash scripts/check_lean_nanoda.sh       # independent Rust checker
```

Checked with **Lean 4.32.2**. The development is deliberately **mathlib-free**:
no cache download, no network, no proof-library dependency. The cost is that
`ring`, `linarith`, `push_cast` and `by_contra` are unavailable, so every
nonlinear rewrite is supplied by hand (`Nat.add_mul`, `Nat.mul_add`,
`Nat.succ_mul`, `Int.mul_sub`), trichotomy is split with `Nat.lt_or_ge`, and
`omega` closes the linear part. `omega` abstracts nonlinear subterms as atoms, so
the helper lemmas exist to make those atoms match syntactically.

## Modules

| File | Contents |
|---|---|
| `Conjecture/Basic.lean` | the orbit `B`, absorption, congruence propagation, pair merging, and `Q`/`R`/`E` with the doubling law |
| `Conjecture/Gate.lean` | pure `Nat` arithmetic: gate-exponent uniqueness and gap-predicate upward closure |
| `Conjecture/Ratchet.lean` | forced rebound and the quotient ratchet |
| `Conjecture/FiniteStart.lean` | entry, the quadratic step, and Theorem 18 from the ray hypothesis |
| `Conjecture/AbsorptionConverse.lean` | eventual increment implies the ray, and Theorem 18 in the paper's form |
| `Conjecture/EntryBound.lean` | Lemma 3's explicit entry bound, square-root-free |
| `Conjecture.lean` | module index and the axiom audit |

It was one file until the modules exceeded the repository's per-file length gate.
Use `lake env lean` rather than a bare `lean` invocation now that imports are
involved.

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
E_doubling_nat, E_doubling_mod, E_doubling, B_monotone,
gate_exponent_unique, unit_gate_exponent_unique, gap_predicate_upward_closed,
quotient_drop_le_one, forced_rebound, ratchet,
entry_exists, quadratic_step, least_entry, ray_of_eventual_increment,
orbit_bound_doubled, entry_at_sqrt_bound, least_entry_le_sqrt_bound
    depends on axioms: [propext, Quot.sound]
E_zero_of_ray, finite_start, finite_start_of_increment
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
| `down_step_linear` | the subtraction-free linear relation across a down-step; the two quadratic terms cancel |
| `quotient_drop_le_one` | the part of **Lemma 4** the ratchet needs: `q` never falls by more than one while `3q_n ≤ n+1` |
| `forced_rebound` | **Theorem 13**: a down-step in the small-quotient region is undone at the next step |
| `ratchet` | **Theorem 14**: over `len` small-quotient indices from `u`, `q` never falls two below `q_u` |
| `gate_exponent_unique` | **Theorem 133**: at most one exponent satisfies both pure-upper windows |
| `unit_gate_exponent_unique` | **Theorem 130**, the `k = 1` case |
| `gap_predicate_upward_closed` | **Lemma 136**: the forced-gap predicate is upward closed, so its minimum is well defined |
| `orbit_upper_bound`, `entry_exists` | **Lemma 3**, in the form Theorem 18 needs: some index satisfies `b_n < n^2` |
| `entry_forward`, `entry_forward_all` | forward invariance of `b_n < n^2` |
| `quotient_lt_index` | `b_n < n^2` implies `q_n < n`, putting the orbit in the bounded-quotient region |
| `least_entry` | the least entry index and its minimality |
| `quadratic_step` | the nonlinear step `(n_0-1)^2 < (c+2)n_0 => n_0 <= c+4` |
| `ray_quotient`, `ray_below_square`, `start_le` | reading the absorbing ray |
| `finite_start` | **Theorem 18** from the ray hypothesis: `m < (c+3)(3c+5)` |
| `ray_of_eventual_increment` | **absorption converse**: eventual increment `c` forces `b_t = c(t+1)` and `c < t` |
| `finite_start_of_increment` | **Theorem 18** in the paper's form, from the eventual-increment hypothesis |
| `orbit_bound_doubled` | the telescoped sum `2 b_{i+2} <= 2m + i(i+1)`, doubled so the triangular number needs no division |
| `entry_at_sqrt_bound`, `least_entry_le_sqrt_bound` | **Lemma 3**'s explicit bound `n_0 <= ceil(sqrt(2m)) + 2` |

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

* **Theorem 137** (the closed block-chain map) and everything else in the
  safe-map development. `Conjecture/Gate.lean` formalizes only arithmetic facts
  about inequalities over `Nat`; it knows nothing about the safe map, and the
  identification of those inequalities with safe-map gates is not formalized.
* **The conjecture itself** — unproved, so there is nothing to formalize.
* **Everything heuristic** — `κ → 1/4`, the epoch transition matrix, the tail
  law. These are explicitly *not* theorems and must not be given the appearance
  of one by being written in Lean.

## Next steps

1. **Done:** Theorems 13 and 14, and Theorem 18 from the ray hypothesis. The
   ratchet uses the two-clause invariant *either `q ≥ q_u`, or `q = q_u − 1` and
   the next step is forced up*; the second clause is not optional, and its
   absence was a gap in the compressed paper argument.
2. **Done:** the absorption converse. Rather than introduce `Int` for the fixed
   quantity, the key identity is kept subtraction-free as
   `P q + c(s+2) = B m s + c P` with `P = s+j+1`, and one index past both
   `B m s` and `c(s+2)` contradicts each strict comparison of `q` against `c`.
   `absorb_increment` produces exactly the hypothesis `finite_start_of_increment`
   consumes, so both directions of the absorption criterion now compose.
3. **Done:** Lemma 3's explicit bound. Square roots and ceilings are avoided by
   noting that `⌈√(2m)⌉` is *by definition* the least `k` with `k² ≥ 2m`, so the
   bound is equivalent to `k² ≥ 2m → b_{k+2} < (k+2)²`, which mentions neither.
   The telescoped sum is carried doubled so the triangular number needs no
   division.
4. A verified checker for the finite enumeration, which would make Corollary 20
   end-to-end machine-checked.
