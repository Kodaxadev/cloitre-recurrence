#!/usr/bin/env python3
"""
Check why f=6,7,8 classes fail the canonical gate verification.
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

# Check the f=6,7,8 cases
for n0, f0 in [(11, 6), (14, 7), (17, 8)]:
    print(f"Checking (n={n0}, f={f0}):")
    print(f"  n+3+f = {n0+3+f0} ≡ {(n0+3+f0)%4} (mod 4)")
    max_U = (n0 - f0 - 3) // 2
    print(f"  max_U from f <= D-3: {max_U}")
    for U0 in range(0, max_U + 1):
        if not is_unit_state_canonical(n0, U0, f0):
            print(f"  U={U0}: NOT a unit state")
            continue
        D = n0 - 2*U0
        print(f"  U={U0}: D={D}, defect={D-3-f0}, 4f={4*f0}, n+D+2={n0+D+2}")
        g1 = gate_canonical(n0, U0, f0)
        if g1 is None:
            print(f"  U={U0}: NO GATE")
            continue
        h1, f1, n1, U1 = g1
        print(f"  U={U0}: h={h1}, f'={f1}, n'={n1}, U'={U1}")
        if h1 != 2:
            print(f"  U={U0}: h != 2")
            continue
        g2 = gate_canonical(n1, U1, f1)
        if g2 is None:
            print(f"  U={U0}: second gate NONE")
            continue
        h2, f2, n2, U2 = g2
        print(f"  U={U0}: second gate h={h2}, f''={f2}")
        if h2 != 2:
            print(f"  U={U0}: second h != 2")
    print()

# Also check f=19 to see why it fails
print("Checking f=19:")
n0 = 55  # from bounds
f0 = 19
print(f"  n+3+f = {n0+3+f0} ≡ {(n0+3+f0)%4} (mod 4)")
max_U = (n0 - f0 - 3) // 2
print(f"  max_U: {max_U}")
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
    print(f"  U={U0}: WORKS!")
print("  (no valid U found)")