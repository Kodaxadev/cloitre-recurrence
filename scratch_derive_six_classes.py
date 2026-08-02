#!/usr/bin/env python3
"""
Complete derivation of the six classes from symbolic n<=56 reduction.
"""

# We have the conditions for two consecutive h=2 gates:
# 1. L_2 at step 0: 4f_0 >= n_0 + 6
# 2. M_2 at step 0: f_1 = 4f_0 - n_0 - 5 <= 16
# 3. L_2 at step 1: 4f_1 >= n_1 + 6 = n_0 + 8
# 4. M_2 at step 1: f_2 = 4f_1 - n_1 - 5 <= 16
# 5. Unit state congruence: n_0 + 3 + f_0 ≡ 0 (mod 4)
# 6. Unit state bounds: f_0 <= D_0 - 3 = n_0 - 2U_0 - 3, 4f_0 <= n_0 + D_0 + 2 = 2n_0 - 2U_0 + 2

# From (2): n_0 >= 4f_0 - 21
# From (3): 4(4f_0 - n_0 - 5) >= n_0 + 8 => 16f_0 - 4n_0 - 20 >= n_0 + 8 => 16f_0 >= 5n_0 + 28 => n_0 <= (16f_0 - 28)/5
# From (1): n_0 <= 4f_0 - 6
# From (4): f_2 = 4f_1 - n_1 - 5 = 4(4f_0 - n_0 - 5) - (n_0 + 2) - 5 = 16f_0 - 5n_0 - 27 <= 16 => 16f_0 <= 5n_0 + 43 => n_0 >= (16f_0 - 43)/5

# Also from unit state: f_0 <= n_0 - 2U_0 - 3 <= n_0 - 3 => n_0 >= f_0 + 3
# And 4f_0 <= 2n_0 - 2U_0 + 2 <= 2n_0 + 2 => n_0 >= 2f_0 - 1

# So overall bounds on n_0:
# Lower: max(f_0 + 3, 2f_0 - 1, 4f_0 - 21, (16f_0 - 43)/5)
# Upper: min(4f_0 - 6, (16f_0 - 28)/5)

# Let's compute for each f_0 and find integer n_0 satisfying congruence

print("=== Derivation of six classes ===")
print()

for f0 in range(1, 30):
    lower = max(f0 + 3, 2*f0 - 1, 4*f0 - 21, (16*f0 - 43)/5)
    upper = min(4*f0 - 6, (16*f0 - 28)/5)
    
    if lower > upper:
        continue
    
    # Congruence: n_0 ≡ -3 - f_0 (mod 4)
    target_mod = (-3 - f0) % 4
    
    # Find integer n_0 in [ceil(lower), floor(upper)] with correct congruence
    n_min = int(lower) if lower == int(lower) else int(lower) + 1
    n_max = int(upper)
    
    solutions = []
    for n0 in range(n_min, n_max + 1):
        if n0 % 4 == target_mod:
            solutions.append(n0)
    
    if solutions:
        print(f"f_0 = {f0}: n_0 in [{lower:.1f}, {upper:.1f}], n ≡ {target_mod} (mod 4)")
        print(f"  Integer solutions: {solutions}")
        
        # For each solution, check if it actually produces two h=2 gates
        for n0 in solutions:
            # Check if there exists U_0 making this a valid unit state with two h=2 gates
            # We'll verify with the canonical gate function
            pass
        print()

# Now let's verify the exact six classes with the canonical gate function
from dataclasses import dataclass
from typing import Optional, Tuple

@dataclass(frozen=True)
class UnitState:
    n: int
    U: int
    f: int

def is_unit_state_canonical(n: int, U: int, f: int) -> bool:
    D = n - 2 * U
    return (
        n >= 2
        and U >= 0
        and f >= 1
        and (n + 3 + f) % 4 == 0
        and f <= D - 3
        and 4 * f <= n + D + 2
    )

def h_star(n: int, f: int) -> int:
    h = 2
    while (f << h) < n + h + 4:
        h += 1
    return h

def gate_canonical(n: int, U: int, f: int) -> Optional[Tuple[int, int, int, int]]:
    D = n - 2 * U
    defect = D - 3 - f
    if defect < 4 or defect % 2 != 0:
        return None
    h = h_star(n, f)
    g = (f << h) - n - h - 3
    if g < 1 or g > (1 << (h + 2)):
        return None
    child_D = D + h - 2
    if child_D - 3 - g < (1 << (h + 2)):
        return None
    return h, g, n + h, U + 1

print("=== Verification of six classes with canonical gate ===")
print()

for f0 in range(1, 30):
    lower = max(f0 + 3, 2*f0 - 1, 4*f0 - 21, (16*f0 - 43)/5)
    upper = min(4*f0 - 6, (16*f0 - 28)/5)
    
    if lower > upper:
        continue
    
    target_mod = (-3 - f0) % 4
    n_min = int(lower) if lower == int(lower) else int(lower) + 1
    n_max = int(upper)
    
    for n0 in range(n_min, n_max + 1):
        if n0 % 4 != target_mod:
            continue
        
        # Check if there's any U_0 that works
        max_U = (n0 - f0 - 3) // 2
        found = False
        for U0 in range(0, max_U + 1):
            if not is_unit_state_canonical(n0, U0, f0):
                continue
            g1 = gate_canonical(n0, U0, f0)
            if g1 is None:
                continue
            h1, f1, n1, U1 = g1
            if h1 != 2:
                continue
            g2 = gate_canonical(n1, U1, f1)
            if g2 is None:
                continue
            h2, f2, n2, U2 = g2
            if h2 != 2:
                continue
            found = True
            break
        
        if found:
            print(f"VALID CLASS: (n={n0}, f={f0})")
            # Show the U range
            valid_Us = []
            for U0 in range(0, max_U + 1):
                if not is_unit_state_canonical(n0, U0, f0):
                    continue
                g1 = gate_canonical(n0, U0, f0)
                if g1 is None:
                    continue
                h1, f1, n1, U1 = g1
                if h1 != 2:
                    continue
                g2 = gate_canonical(n1, U1, f1)
                if g2 is None:
                    continue
                h2, f2, n2, U2 = g2
                if h2 != 2:
                    continue
                valid_Us.append(U0)
            print(f"  U in {valid_Us} (count={len(valid_Us)})")
            print()