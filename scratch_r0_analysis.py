#!/usr/bin/env python3
"""Exact analysis of r=0 (h=2) zero-gap runs on the all-unit branch."""

# Algebraic check: r=0 means h=2
# f' = 4f - n - 5  (since n' = n+2, h=2: f' = 2^2 f - n' - 3 = 4f - (n+2) - 3 = 4f - n - 5)
# f' > f  <=>  3f > n + 5
# f' = f  <=>  3f = n + 5
# f' < f  <=>  3f < n + 5

# Forced h=2 condition: 2^2 f >= n + 2 + 4  =>  4f >= n + 6
# Also from M_h: 4f <= n + 2 + 3 + 2^4 = n + 21  (but tighter bounds from admissibility)

print('Algebraic conditions for r=0 (h=2):')
print('  Forced h=2: 4f >= n + 6')
print("  f' > f: 3f > n + 5")
print("  f' = f: 3f = n + 5")
print("  f' < f: 3f < n + 5")
print()
print('From 4f >= n+6, we get n <= 4f - 6')
print('Then 3f > n+5 becomes 3f > (4f-6)+5 = 4f-1 => f < 1')
print("So f' > f is IMPOSSIBLE when h=2 is forced!")
print()
print("Check f' = f: 3f = n+5 => n = 3f-5")
print('  Need 4f >= n+6 = 3f+1 => f >= 1 (always true for f>=1)')
print('  Also need n >= 2 => 3f-5 >= 2 => f >= 3')
print("  So f' = f is possible for f >= 3 with n = 3f-5")
print()
print("Check f' < f: 3f < n+5 => n > 3f-5")
print('  Combined with 4f >= n+6 => n <= 4f-6')
print('  So 3f-5 < n <= 4f-6')
print('  This requires 3f-5 < 4f-6 => f > 1')
print("  So f' < f is possible for f >= 2 with n in (3f-5, 4f-6]")

# Now enumerate exact admissible all-unit states with r=0
def is_unit_state(n, u, f):
    d = n - 2*u
    return (n >= 2 and u >= 0 and f >= 1 and (n + 3 + f) % 4 == 0 
            and f <= d - 3 and 4*f <= n + d + 2)

def minimal_exponent(n, f):
    h = 2
    while (f << h) < n + h + 4:
        h += 1
    return h

def gate(n, u, f):
    d = n - 2*u
    defect = d - 3 - f
    if defect < 4 or defect % 2 != 0:
        return None
    h = minimal_exponent(n, f)
    g = (f << h) - n - h - 3
    if g < 1 or g > (1 << (h + 2)):
        return None
    child_d = d + h - 2
    if child_d - 3 - g < (1 << (h + 2)):
        return None
    return h, g, n + h, u + 1

print("\n=== Exact enumeration of admissible all-unit states with r=0 (h=2) ===")
print("n, U, f, h, f', n', U', classification")

count_lt = 0
count_eq = 0
count_gt = 0

for n in range(10, 500):
    for u in range(0, (n - 6) // 2 + 1):
        d = n - 2*u
        if d < 8:
            continue
        for f in range(1, d - 2):
            if not is_unit_state(n, u, f):
                continue
            nxt = gate(n, u, f)
            if nxt is None:
                continue
            h, g, n2, u2 = nxt
            if h == 2:  # r = 0
                if g < f:
                    cls = "f' < f"
                    count_lt += 1
                elif g == f:
                    cls = "f' = f"
                    count_eq += 1
                else:
                    cls = "f' > f"
                    count_gt += 1
                print(f"{n}, {u}, {f}, {h}, {g}, {n2}, {u2}, {cls}")

print(f"\nSummary: f' < f: {count_lt}, f' = f: {count_eq}, f' > f: {count_gt}")