#!/usr/bin/env python3
"""Find the f' > f case for r=0."""

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
            if h == 2 and g > f:
                print("f' > f case: n=" + str(n) + ", U=" + str(u) + ", f=" + str(f) + ", f'=" + str(g) + ", n'=" + str(n2) + ", U'=" + str(u2))
                print("  d=" + str(d) + ", defect=" + str(d-3-f) + ", 4f=" + str(4*f) + ", n+6=" + str(n+6))
                print("  3f=" + str(3*f) + ", n+5=" + str(n+5))