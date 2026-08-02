#!/usr/bin/env python3
"""Search for longer r=0 runs up to larger bound."""

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

# Search for consecutive r=0 runs up to n=5000
print("Searching for consecutive r=0 runs up to n=5000...")
max_run = 0
best_start = None

for n in range(10, 5000):
    for u in range(0, (n - 6) // 2 + 1):
        d = n - 2*u
        if d < 8:
            continue
        for f in range(1, d - 2):
            if not is_unit_state(n, u, f):
                continue
            # Follow the orbit
            run = 0
            cn, cu, cf = n, u, f
            while True:
                nxt = gate(cn, cu, cf)
                if nxt is None:
                    break
                h, g, n2, u2 = nxt
                if h == 2:
                    run += 1
                    cn, cu, cf = n2, u2, g
                else:
                    break
            if run > max_run:
                max_run = run
                best_start = (n, u, f)
                print("New max run: " + str(run) + " at start n=" + str(n) + ", U=" + str(u) + ", f=" + str(f))

print("\nMaximum consecutive r=0 run length found: " + str(max_run))
print("Best start: " + str(best_start))

# Also check the closed form prediction
print("\n=== Closed form analysis ===")
print("f_i = (f_0 - n_0/3 - 17/9) * 4^i + (2/3)i + n_0/3 + 17/9")
print("For integer f_i, the coefficient C = f_0 - n_0/3 - 17/9 must be such that C*4^i is integer for all i in the run.")
print("Since 4^i grows, |C| must be very small for a long run.")
print("C = 0 requires 9f_0 = 3n_0 + 17, impossible since 17 not divisible by 3.")
print("So |C| >= 1/9.")
print("For i=3, |C|*4^3 >= 64/9 > 7, so f_3 deviates by >7 from the linear part.")
print("The window for f_i is roughly n_i/4 +/- 4, width ~8.")
print("So run length <= 3 is expected.")