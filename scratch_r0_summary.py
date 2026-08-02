#!/usr/bin/env python3
"""Summary of r=0 classification."""

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

count_lt = 0
count_eq = 0
count_gt = 0
eq_cases = []

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
            if h == 2:
                if g < f:
                    count_lt += 1
                elif g == f:
                    count_eq += 1
                    eq_cases.append((n, u, f, g, n2, u2))
                else:
                    count_gt += 1

print("f' < f: " + str(count_lt))
print("f' = f: " + str(count_eq))
print("f' > f: " + str(count_gt))
print()
print("f' = f cases:")
for c in eq_cases:
    print("  n=" + str(c[0]) + ", U=" + str(c[1]) + ", f=" + str(c[2]) + ", f'=" + str(c[3]) + ", n'=" + str(c[4]) + ", U'=" + str(c[5]))