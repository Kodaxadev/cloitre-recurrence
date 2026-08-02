#!/usr/bin/env python3
"""
Verify the L_h/M_h generalization against the canonical implementation.

From Theorem 130:
- L_h: 2^h f >= n + h + 4
- M_h: 2^h f <= n + h + 3 + 2^{h+2}
- Returned residue: g = 2^h f - n - h - 3
- So M_h <=> g <= 2^{h+2} = 2^{r+4} where h = r+2

For two consecutive steps i and i+1:
- Step i: h_i = r_i + 2, f_{i+1} = 2^{h_i} f_i - n_i - h_i - 3, n_{i+1} = n_i + h_i
- M_h at step i: f_{i+1} <= 2^{h_i+2} = 2^{r_i+4}
- L_h at step i+1: 2^{h_{i+1}} f_{i+1} >= n_{i+1} + h_{i+1} + 4 = n_{i+1} + r_{i+1} + 6

Combining: n_{i+1} + r_{i+1} + 6 <= 2^{h_{i+1}} f_{i+1} <= 2^{h_{i+1}} * 2^{h_i+2} = 2^{r_i+r_{i+1}+6}

So: n_{i+1} + r_{i+1} + 6 <= 2^{r_i + r_{i+1} + 6}

This is the exact integer inequality.
"""

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

def check_LM_inequality(n: int, U: int, f: int) -> bool:
    """Check the combined L_{h_{i+1}} / M_{h_i} inequality for a valid two-step sequence."""
    g1 = gate_canonical(n, U, f)
    if g1 is None:
        return True  # vacuously true if no first gate
    h1, f1, n1, U1 = g1
    r1 = h1 - 2
    
    g2 = gate_canonical(n1, U1, f1)
    if g2 is None:
        return True  # vacuously true if no second gate
    h2, f2, n2, U2 = g2
    r2 = h2 - 2
    
    # The inequality: n_{i+1} + r_{i+1} + 6 <= 2^{r_i + r_{i+1} + 6}
    lhs = n1 + r2 + 6
    rhs = 1 << (r1 + r2 + 6)
    
    return lhs <= rhs

def check_all_orbits(n_max: int = 5000):
    """Check the inequality on all valid two-step all-unit sequences."""
    violations = []
    checked = 0
    
    for n in range(2, n_max + 1):
        for U in range(0, (n - 2) // 2 + 1):
            D = n - 2 * U
            if D < 8:
                continue
            for f in range(1, D - 2):
                if not is_unit_state_canonical(n, U, f):
                    continue
                
                g1 = gate_canonical(n, U, f)
                if g1 is None:
                    continue
                h1, f1, n1, U1 = g1
                r1 = h1 - 2
                
                g2 = gate_canonical(n1, U1, f1)
                if g2 is None:
                    continue
                h2, f2, n2, U2 = g2
                r2 = h2 - 2
                
                checked += 1
                lhs = n1 + r2 + 6
                rhs = 1 << (r1 + r2 + 6)
                
                if lhs > rhs:
                    violations.append((n, U, f, h1, f1, n1, U1, h2, f2, n2, U2, lhs, rhs))
    
    print(f"Checked {checked} two-step sequences up to n={n_max}")
    print(f"Violations: {len(violations)}")
    
    if violations:
        for v in violations[:10]:
            print(f"  VIOLATION: n={v[0]}, U={v[1]}, f={v[2]}, h1={v[3]}, f1={v[4]}, n1={v[5]}, h2={v[8]}, f2={v[9]}, n2={v[10]}, lhs={v[11]}, rhs={v[12]}")
    else:
        print("No violations found.")
    
    return violations

def check_weaker_inequality(n_max: int = 5000):
    """Check the weaker form: r_i + r_{i+1} >= ceil(log2(n_{i+1}+6)) - 6"""
    import math
    
    violations = []
    checked = 0
    
    for n in range(2, n_max + 1):
        for U in range(0, (n - 2) // 2 + 1):
            D = n - 2 * U
            if D < 8:
                continue
            for f in range(1, D - 2):
                if not is_unit_state_canonical(n, U, f):
                    continue
                
                g1 = gate_canonical(n, U, f)
                if g1 is None:
                    continue
                h1, f1, n1, U1 = g1
                r1 = h1 - 2
                
                g2 = gate_canonical(n1, U1, f1)
                if g2 is None:
                    continue
                h2, f2, n2, U2 = g2
                r2 = h2 - 2
                
                checked += 1
                # Weaker form: r1 + r2 >= ceil(log2(n1 + 6)) - 6
                # Since n1 + r2 + 6 <= 2^{r1+r2+6}, we have n1 + 6 <= 2^{r1+r2+6}
                # So r1 + r2 + 6 >= log2(n1 + 6)
                # r1 + r2 >= log2(n1 + 6) - 6
                # Integer form: r1 + r2 >= ceil(log2(n1 + 6)) - 6
                required = (n1 + 6).bit_length() - 1  # floor(log2(n1+6))
                if (1 << required) < n1 + 6:
                    required += 1  # ceil
                required -= 6
                required = max(0, required)  # truncate at zero
                
                if r1 + r2 < required:
                    violations.append((n, U, f, r1, r2, n1, required))
    
    print(f"\nWeaker inequality check (truncated at 0):")
    print(f"Checked {checked} sequences")
    print(f"Violations: {len(violations)}")
    
    if violations:
        for v in violations[:10]:
            print(f"  VIOLATION: n={v[0]}, U={v[1]}, f={v[2]}, r1={v[3]}, r2={v[4]}, n1={v[5]}, required={v[6]}")
    else:
        print("No violations of truncated weaker form.")
    
    return violations

def check_exact_inequality_no_truncation(n_max: int = 5000):
    """Check the exact inequality without truncation: r1+r2 >= log2(n1+6) - 6"""
    import math
    
    violations = []
    checked = 0
    
    for n in range(2, n_max + 1):
        for U in range(0, (n - 2) // 2 + 1):
            D = n - 2 * U
            if D < 8:
                continue
            for f in range(1, D - 2):
                if not is_unit_state_canonical(n, U, f):
                    continue
                
                g1 = gate_canonical(n, U, f)
                if g1 is None:
                    continue
                h1, f1, n1, U1 = g1
                r1 = h1 - 2
                
                g2 = gate_canonical(n1, U1, f1)
                if g2 is None:
                    continue
                h2, f2, n2, U2 = g2
                r2 = h2 - 2
                
                checked += 1
                # Exact real-valued bound
                required = math.log2(n1 + 6) - 6
                
                if r1 + r2 < required:
                    violations.append((n, U, f, r1, r2, n1, required))
    
    print(f"\nExact real-valued inequality check (no truncation):")
    print(f"Checked {checked} sequences")
    print(f"Violations: {len(violations)}")
    
    if violations:
        for v in violations[:10]:
            print(f"  VIOLATION: n={v[0]}, U={v[1]}, f={v[2]}, r1={v[3]}, r2={v[4]}, n1={v[5]}, required={v[6]:.3f}")
    else:
        print("No violations of exact real-valued form.")
    
    return violations

def sum_over_pairs(n_max: int = 5000):
    """Sum the inequality over disjoint pairs along orbits."""
    import math
    
    results = []
    
    for n in range(2, n_max + 1):
        for U in range(0, (n - 2) // 2 + 1):
            D = n - 2 * U
            if D < 8:
                continue
            for f in range(1, D - 2):
                if not is_unit_state_canonical(n, U, f):
                    continue
                
                # Follow the orbit and collect pairs
                orbit = []
                cn, cu, cf = n, U, f
                while True:
                    g = gate_canonical(cn, cu, cf)
                    if g is None:
                        break
                    h, gf, nn, nU = g
                    orbit.append((cn, cu, cf, h, gf, nn, nU))
                    cn, cu, cf = nn, nU, gf
                
                if len(orbit) < 2:
                    continue
                
                # Sum over disjoint pairs (0,1), (2,3), ...
                sum_r = 0
                sum_bound = 0
                for i in range(0, len(orbit) - 1, 2):
                    _, _, _, h1, _, n1, _ = orbit[i]
                    _, _, _, h2, _, n2, _ = orbit[i+1]
                    r1 = h1 - 2
                    r2 = h2 - 2
                    sum_r += r1 + r2
                    # Bound from n_{i+1} + r_{i+1} + 6 <= 2^{r_i+r_{i+1}+6}
                    # => r_i + r_{i+1} >= log2(n_{i+1} + r_{i+1} + 6) - 6
                    # Weaker: r_i + r_{i+1} >= log2(n_{i+1} + 6) - 6
                    bound = math.log2(n1 + 6) - 6
                    sum_bound += max(0, bound)
                
                if sum_bound > 0:
                    results.append((sum_r, sum_bound, len(orbit)))
    
    if results:
        print(f"\nSum over disjoint pairs (N={len(results)} orbits with >=2 steps):")
        max_ratio = max(r/b for r,b in results if b > 0)
        min_ratio = min(r/b for r,b in results if b > 0)
        print(f"  Max ratio sum_r / sum_bound: {max_ratio:.3f}")
        print(f"  Min ratio sum_r / sum_bound: {min_ratio:.3f}")
        
        # Check if sum_r >= sum_bound always holds
        violations = [(r,b) for r,b in results if r < b]
        print(f"  Violations of sum_r >= sum_bound: {len(violations)}")
        if violations:
            for v in violations[:5]:
                print(f"    sum_r={v[0]:.3f}, sum_bound={v[1]:.3f}")

if __name__ == "__main__":
    check_all_orbits(5000)
    check_weaker_inequality(5000)
    check_exact_inequality_no_truncation(5000)
    sum_over_pairs(5000)