#!/usr/bin/env python3
"""
CORRECTED AND STRENGTHENED CHECKPOINT
=====================================

Finite-Reduction Theorem for Consecutive Zero Gaps on the All-Unit Branch

WITHDRAWN STATEMENTS (from previous checkpoint):
- "Zero-gap run bound theorem" claiming universal bound via closed form (algebraic error)
- U-ranges U=0..10 through U=0..15 (incorrect, used insufficient bound floor((n-f-3)/2))
- Budget bound floor(N/3) (weakened; correct bound is floor(N/2))

---

1. SYMBOLIC REDUCTION: n <= 56

From Theorem 130 (unit-chain-determinism.md), an all-unit gate with h=2 has:
- Returned residue: f_1 = 4f_0 - n_0 - 5
- Condition M_2: f_1 <= 2^{2+2} = 16
- If next gate also has h=2: condition L_2 gives 4f_1 >= n_1 + 6 = n_0 + 8

Substituting f_1:
  4(4f_0 - n_0 - 5) >= n_0 + 8
  16f_0 - 4n_0 - 20 >= n_0 + 8
  16f_0 >= 5n_0 + 28
  n_0 <= (16f_0 - 28)/5

From M_2: f_1 <= 16 => 4f_0 - n_0 - 5 <= 16 => n_0 >= 4f_0 - 21
From L_2 at step 0: 4f_0 >= n_0 + 6 => n_0 <= 4f_0 - 6

Combining: n_0 <= min(4f_0 - 6, (16f_0 - 28)/5)

For f_0 >= 13, (16f_0 - 28)/5 <= 4f_0 - 6, so n_0 <= (16f_0 - 28)/5.
For f_0 = 18: n_0 <= (288 - 28)/5 = 52.
For f_0 = 19: n_0 <= (304 - 28)/5 = 55.2, but congruence and other bounds eliminate it.

The absolute maximum over all f_0 is n_0 <= 56 (achieved at f_0=19 with n_0=55 before congruence elimination).

---

2. EXACT SIX-CLASS FINITE EXHAUSTION

Adding the unit state congruence n_0 + 3 + f_0 ≡ 0 (mod 4) and the child-survival condition U_2 (which enforces U_0 <= f_0 - 10, derived below) yields exactly six congruence classes:

| f_0 | n_0 = 3f_0 - 3 | Congruence | U_0 range | Count |
|-----|----------------|------------|-----------|-------|
| 13  | 36             | n ≡ 0 (mod 4) | 0..3      | 4     |
| 14  | 39             | n ≡ 3 (mod 4) | 0..4      | 5     |
| 15  | 42             | n ≡ 2 (mod 4) | 0..5      | 6     |
| 16  | 45             | n ≡ 1 (mod 4) | 0..6      | 7     |
| 17  | 48             | n ≡ 0 (mod 4) | 0..7      | 8     |
| 18  | 51             | n ≡ 3 (mod 4) | 0..8      | 9     |

Total: 39 canonical admissible states.

Derivation of n_0 = 3f_0 - 3:
From the bounds n_0 >= max(f_0+3, 2f_0-1, 4f_0-21, (16f_0-43)/5) and n_0 <= min(4f_0-6, (16f_0-28)/5),
the interval contains exactly one integer satisfying the congruence n_0 ≡ -3-f_0 (mod 4),
and that integer is n_0 = 3f_0 - 3 (verified for f_0 = 13..18; for f_0 <= 12 the child-survival condition U_2 fails;
for f_0 >= 19 the congruence forces n_0 outside the interval).

Derivation of U_0 <= f_0 - 10:
The first gate's child-survival condition (U_2 in Theorem 130) is:
  D_0 - 3 - f_1 >= 16, where D_0 = n_0 - 2U_0, f_1 = f_0 - 2.
Substituting n_0 = 3f_0 - 3:
  (3f_0 - 3 - 2U_0) - 3 - (f_0 - 2) >= 16
  2f_0 - 4 - 2U_0 >= 16
  f_0 - U_0 >= 10
  U_0 <= f_0 - 10.

This is the tight bound; the unit state condition f_0 <= D_0 - 3 gives U_0 <= (n_0 - f_0 - 3)/2 = f_0 - 3,
which is weaker for f_0 >= 13.

---

3. COMPLETE 39-STATE CERTIFICATE (Independent Verification)

Verifier: scratch_r0_independent2.py (no shared code with first implementation)
Canonical gate function: Exact Theorem 130 definitions from unit-chain-determinism.md

All 39 states with two consecutive h=2 gates:

(n=36, f=13): U=0,1,2,3
  Step 1: h=2, f'=11, n'=38, U'=U+1
  Step 2: h=2, f''=1, n''=40, U''=U+2
  Step 3: NO GATE (terminates)

(n=39, f=14): U=0,1,2,3,4
  Step 1: h=2, f'=12, n'=41, U'=U+1
  Step 2: h=2, f''=2, n''=43, U''=U+2
  Step 3: NO GATE (terminates)

(n=42, f=15): U=0,1,2,3,4,5
  Step 1: h=2, f'=13, n'=44, U'=U+1
  Step 2: h=2, f''=3, n''=46, U''=U+2
  Step 3: NO GATE (terminates)

(n=45, f=16): U=0,1,2,3,4,5,6
  Step 1: h=2, f'=14, n'=47, U'=U+1
  Step 2: h=2, f''=4, n''=49, U''=U+2
  Step 3: NO GATE (terminates)

(n=48, f=17): U=0,1,2,3,4,5,6,7
  Step 1: h=2, f'=15, n'=50, U'=U+1
  Step 2: h=2, f''=5, n''=52, U''=U+2
  Step 3: NO GATE (terminates)

(n=51, f=18): U=0,1,2,3,4,5,6,7,8
  Step 1: h=2, f'=16, n'=53, U'=U+1
  Step 2: h=2, f''=6, n''=55, U''=U+2
  Step 3: NO GATE (terminates)

---

4. EXACT MEANING OF "NO GATE" (TERMINATION)

In the canonical theory (Theorem 130, unit-chain-determinism.md):
- The map T(n,U,f) is a PARTIAL map defined exactly when conditions P, M_h*, U_h* hold.
- gate_canonical returning None means: the state (n,U,f) is a valid unit state (satisfies Lemma 117),
  but NO pure-upper unit gate exists from it.
- This means the all-unit fibre ENDS at this state. The safe path may continue via a non-unit gate
  (long block, k >= 2), but the all-unit pure-upper mechanism cannot continue.
- In the context of an infinite ALL-UNIT orbit (where every block has k=1), "no gate" means
  the orbit TERMINATES (cannot be infinite all-unit).

Repository terminology (block-chain-closed-map.md, Theorem 137):
- The all-unit branch is the fibre k_i = 1 of the full Ψ-map.
- A state with no outgoing unit gate exits the all-unit fibre; it may enter the long-block branch (k >= 2)
  or terminate the safe path entirely (if no gate of any length exists).
- For the purpose of excluding an infinite ALL-UNIT orbit, "no gate" = termination of that branch.

---

5. STRONGEST VALID INFINITE-ORBIT COROLLARY

Theorem (No adjacent zero gaps in an infinite all-unit orbit):
If an infinite all-unit Ψ-orbit exists, it cannot contain two consecutive zero gaps (r_i = r_{i+1} = 0).
Proof: Every occurrence of two consecutive zero gaps is one of the 39 states above, and all 39
terminate at the third step (no continuing all-unit gate). Therefore an infinite all-unit orbit
has no adjacent zero gaps.

Corollary (Linear budget bound, strengthened):
In any infinite all-unit orbit, every pair of consecutive transitions contains at least one
with r_i >= 1. The budget G_i = n_i - 2U_i satisfies G_{i+1} = G_i + r_i (Corollary 147).
Therefore for any N >= 0:
  G_N - G_0 = sum_{i=0}^{N-1} r_i >= floor(N/2).

Boundary cases:
- N = 0: sum over empty set = 0, floor(0/2) = 0. Bound holds (0 >= 0).
- N = 1: sum = r_0 >= 0, floor(1/2) = 0. Bound holds (r_0 >= 0).
- N = 2: sum = r_0 + r_1. Since not both can be zero, at least one >= 1, so sum >= 1.
  floor(2/2) = 1. Bound holds (sum >= 1).
- N = 3: sum = r_0 + r_1 + r_2. Pairs (0,1) and (1,2) each have at least one >= 1,
  so sum >= 2? Actually: if r_0=0 then r_1>=1; if r_1=0 then r_0>=1 and r_2>=1.
  Minimum sum is 1 (e.g., 1,0,0 or 0,1,0 or 0,0,1 but last impossible since r_1=0,r_2=0 forbidden).
  Wait: r_1=0,r_2=0 is forbidden. So patterns: (1,0,1) sum=2, (1,1,0) sum=2, (0,1,1) sum=2,
  (1,0,0) sum=1, (0,1,0) sum=1, (0,0,1) sum=1. Minimum is 1.
  floor(3/2) = 1. Bound holds (sum >= 1).

The bound floor(N/2) is tight for N=1,2,3.

---

6. CLASSIFICATION SUMMARY

| Component | Status |
|-----------|--------|
| Symbolic reduction n_0 <= 56 | Theorem (exact integer algebra from Theorem 130 conditions) |
| Six congruence classes (n=3f-3, f=13..18) | Exhaustive finite computation (enumeration after symbolic n<=56 reduction) |
| U_0 <= f_0 - 10 derivation | Theorem (exact substitution into U_2 condition) |
| 39-state certificate | Exhaustive finite computation (independent implementation, exact arithmetic) |
| Termination of all 39 at step 3 | Exhaustive finite computation (independent implementation) |
| No adjacent zero gaps in infinite all-unit orbit | Theorem (symbolic reduction + finite certificate) |
| Budget bound G_N >= G_0 + floor(N/2) | Corollary (follows from theorem + C147 budget recurrence) |

---

7. FILES (Scratch, Untracked)

- scratch_r0_WITHDRAWN.py — records the withdrawn incorrect proof
- scratch_verify_U_bound.py — U <= f-10 derivation
- scratch_derive_six_classes.py — six-class derivation from symbolic bounds
- scratch_check_failures.py — why f=6,7,8,19 are excluded
- scratch_r0_independent2.py — second independent canonical implementation
- scratch_r0_certificate.py — complete 39-state certificate

No repository files modified.
"""
print("Corrected checkpoint complete - see comments above")