#!/usr/bin/env python3
"""
Second independent implementation of the all-unit gate map.
Does not import the first scratch implementation.
Uses exact definitions from unit-chain-determinism.md (Theorem 130).
"""

from dataclasses import dataclass
from typing import Optional, Tuple, List


@dataclass(frozen=True)
class UnitState:
    n: int
    U: int
    f: int


def is_unit_state_canonical(n: int, U: int, f: int) -> bool:
    """Lemma 117 / Theorem 130 (130.0): exact unit state test."""
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
    """Theorem 130 (130.2): h* = min{h >= 2 : 2^h f >= n + h + 4}."""
    h = 2
    while (f << h) < n + h + 4:
        h += 1
    return h


def gate_canonical(n: int, U: int, f: int) -> Optional[Tuple[int, int, int, int]]:
    """
    Theorem 130: the forced gate.
    Returns (h, g, n', U') where h = r + 2, g = returned residue.
    """
    D = n - 2 * U
    defect = D - 3 - f
    # Condition P: defect >= 4 and even
    if defect < 4 or defect % 2 != 0:
        return None
    
    h = h_star(n, f)
    g = (f << h) - n - h - 3  # 2^h f - n - h - 3
    
    # Condition M_h: g <= 2^{h+2}
    if g < 1 or g > (1 << (h + 2)):
        return None
    
    # Condition U_h: D + h - 2 - 3 - g >= 2^{h+2}
    child_D = D + h - 2
    if child_D - 3 - g < (1 << (h + 2)):
        return None
    
    return h, g, n + h, U + 1


def main():
    print("=== Second independent implementation ===")
    print("Canonical gate function from Theorem 130")
    print()
    
    # Test the f' > f case at (35, 0, 14)
    n, U, f = 35, 0, 14
    print(f"Test state: n={n}, U={U}, f={f}")
    print(f"  is_unit_state: {is_unit_state_canonical(n, U, f)}")
    print(f"  D = {n - 2*U}")
    print(f"  defect = {n - 2*U - 3 - f}")
    print(f"  4f = {4*f}, n+6 = {n+6}")
    print(f"  3f = {3*f}, n+5 = {n+5}")
    
    result = gate_canonical(n, U, f)
    if result:
        h, g, n2, U2 = result
        print(f"  Gate: h={h}, g={g}, n'={n2}, U'={U2}")
        print(f"  f' > f: {g > f}")
    else:
        print("  No gate")
    
    print()
    
    # Now the finite-reduction argument:
    # For h=2 gate: g = 4f - n - 5, and M_h gives g <= 2^{2+2} = 16
    # So f_1 <= 16 for any surviving h=2 gate.
    # If next gate also has h=2: 4f_1 >= n_1 + 6 = n_0 + 8
    # So n_0 <= 4*16 - 8 = 56.
    
    print("=== Finite-reduction argument verification ===")
    print("Claim: Every run with >= 2 consecutive h=2 gates begins at n <= 56.")
    print()
    
    # Enumerate all canonical admissible states with n <= 56
    # that begin at least two consecutive h=2 transitions.
    
    candidates = []
    for n in range(2, 57):
        for U in range(0, (n - 2) // 2 + 1):
            D = n - 2 * U
            if D < 8:
                continue
            for f in range(1, D - 2):
                if not is_unit_state_canonical(n, U, f):
                    continue
                
                # First gate
                g1 = gate_canonical(n, U, f)
                if g1 is None:
                    continue
                h1, f1, n1, U1 = g1
                if h1 != 2:
                    continue
                
                # Second gate
                g2 = gate_canonical(n1, U1, f1)
                if g2 is None:
                    continue
                h2, f2, n2, U2 = g2
                if h2 != 2:
                    continue
                
                # Third gate (check if exists)
                g3 = gate_canonical(n2, U2, f2)
                
                candidates.append({
                    'start': (n, U, f),
                    'step1': (h1, f1, n1, U1),
                    'step2': (h2, f2, n2, U2),
                    'step3': g3
                })
    
    print(f"Found {len(candidates)} states with at least 2 consecutive h=2 gates:")
    print()
    
    for c in candidates:
        n, U, f = c['start']
        h1, f1, n1, U1 = c['step1']
        h2, f2, n2, U2 = c['step2']
        g3 = c['step3']
        
        print(f"Start: (n={n}, U={U}, f={f})")
        print(f"  Step 1: h={h1}, f'={f1}, n'={n1}, U'={U1}")
        print(f"  Step 2: h={h2}, f''={f2}, n''={n2}, U''={U2}")
        if g3:
            h3, f3, n3, U3 = g3
            print(f"  Step 3: h={h3}, f'''={f3}, n'''={n3}, U'''={U3}")
        else:
            print(f"  Step 3: TERMINATES")
        print()
    
    # Check if any has a third h=2 gate
    third_h2 = [c for c in candidates if c['step3'] and c['step3'][0] == 2]
    print(f"States with 3 consecutive h=2 gates: {len(third_h2)}")
    
    # Also check the maximum n among candidates
    max_n = max(c['start'][0] for c in candidates) if candidates else 0
    print(f"Maximum starting n: {max_n}")


if __name__ == "__main__":
    main()