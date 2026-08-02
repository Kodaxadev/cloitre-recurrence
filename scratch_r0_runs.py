#!/usr/bin/env python3
"""Analyze the f' > f case and check for consecutive r=0 runs."""

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

# Check the f' > f case
n, u, f = 35, 0, 14
print("Initial state: n=" + str(n) + ", U=" + str(u) + ", f=" + str(f))
print("d=" + str(n-2*u) + ", defect=" + str(n-2*u-3-f) + ", 4f=" + str(4*f) + ", n+6=" + str(n+6))
print("3f=" + str(3*f) + ", n+5=" + str(n+5))

nxt = gate(n, u, f)
print("Gate result: h=" + str(nxt[0]) + ", f'=" + str(nxt[1]) + ", n'=" + str(nxt[2]) + ", U'=" + str(nxt[3]))

# Now check if the next state also has r=0
n2, u2, f2 = nxt[2], nxt[3], nxt[1]
print("\nNext state: n=" + str(n2) + ", U=" + str(u2) + ", f=" + str(f2))
nxt2 = gate(n2, u2, f2)
if nxt2:
    print("Next gate: h=" + str(nxt2[0]) + ", f''=" + str(nxt2[1]) + ", n''=" + str(nxt2[2]) + ", U''=" + str(nxt2[3]))
else:
    print("No gate (terminates)")

# Now search for consecutive r=0 runs
print("\n=== Searching for consecutive r=0 runs ===")
max_run = 0
for n in range(10, 500):
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
                print("New max run: " + str(run) + " at start n=" + str(n) + ", U=" + str(u) + ", f=" + str(f))

print("\nMaximum consecutive r=0 run length found: " + str(max_run))