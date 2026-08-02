#!/usr/bin/env python3
"""
CORRECTED CHECKPOINT WITH THREE FINAL CORRECTIONS
==================================================

Finite-Reduction Theorem for Consecutive Zero Gaps on the All-Unit Branch

---

CORRECTION 1: Direct proof of n_0 <= 56

From two consecutive h=2 gates:
- M_2 at step 0: f_1 <= 2^{2+2} = 16
- L_2 at step 1: 4 f_1 >= n_1 + 6 = n_0 + 8

Combining directly: n_0 + 8 <= 4 f_1 <= 64, therefore n_0 <= 56.

The inequality n_0 <= (16f_0 - 28)/5 is an additional consequence of substituting
f_1 = 4f_0 - n_0 - 5, not the justification for the absolute bound.

---

CORRECTION 2: Exact meaning of "no gate"

In the canonical theory (Theorem 130, unit-chain-determinism.md):
- T(n,U,f) is a PARTIAL map defined exactly when P, M_{h*}, U_{h*} hold.
- gate_canonical returning None means: the state is a valid unit state (Lemma 117)
  but NO pure-upper unit gate exists from it.
- The ALL-UNIT FIBRE ends at this state (the all-unit partial map is undefined).
- The safe path MAY continue through a long block (k >= 2) or terminate entirely.
- For excluding an infinite ALL-UNIT orbit: "no gate" = the all-unit branch cannot continue.

---

CORRECTION 3: Budget bound floor(N/2) with correct patterns

No-adjacent-zero constraint means the sequence of r_i has no two consecutive zeros.
The minimum number of positive r_i in N positions is floor(N/2), achieved by
alternating 0,1,0,1,... (pattern (0,1,0) for N=3, not (1,0,0) which has adjacent zeros
at positions 1,2 if extended).

floor(N/2) is combinatorially optimal from the no-adjacent-zero constraint alone.
Dynamical sharpness (whether actual orbits achieve this bound) is a separate question.

---

ORIGINAL RESULTS (unchanged):

1. Symbolic reduction n_0 <= 56 (direct proof above)
2. Six congruence classes from finite exhaustion after n_0 <= 56:
   (n,f) = (36,13), (39,14), (42,15), (45,16), (48,17), (51,18)
3. U_0 <= f_0 - 10 derivation (Theorem, exact substitution into U_2)
4. 39-state certificate (independent implementation, exact arithmetic)
5. All 39 have no continuing all-unit gate after two zero gaps
6. No adjacent zero gaps in infinite all-unit orbit (Theorem)
7. Budget bound G_N >= G_0 + floor(N/2) (Corollary, combinatorially optimal)

---

CLASSIFICATION SUMMARY

| Component | Status |
|-----------|--------|
| Symbolic reduction n_0 <= 56 | Theorem (direct: n_0+8 <= 4f_1 <= 64) |
| Six congruence classes | Exhaustive finite computation (after n_0 <= 56) |
| U_0 <= f_0 - 10 | Theorem (exact substitution into U_2) |
| 39-state certificate | Exhaustive finite computation (independent) |
| All-unit fibre ends at step 3 | Exhaustive finite computation (independent) |
| No adjacent zero gaps in infinite all-unit orbit | Theorem (symbolic + finite certificate) |
| Budget bound G_N >= G_0 + floor(N/2) | Corollary (combinatorially optimal from constraint) |

---

FILES (Scratch, Untracked)
- scratch_r0_WITHDRAWN.py
- scratch_verify_U_bound.py
- scratch_derive_six_classes.py
- scratch_check_failures.py
- scratch_r0_independent2.py
- scratch_r0_certificate.py
- scratch_CORRECTED_CHECKPOINT.py (this file)

No repository files modified.
"""
print("Corrected checkpoint with three corrections - see comments above")