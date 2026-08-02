#!/usr/bin/env python3
"""Analyze the length-2 r=0 run and derive closed form."""

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

# Analyze the length-2 run
n, u, f = 36, 0, 13
print("Start: n=" + str(n) + ", U=" + str(u) + ", f=" + str(f))
print("d=" + str(n-2*u) + ", defect=" + str(n-2*u-3-f) + ", 4f=" + str(4*f) + ", n+6=" + str(n+6))

nxt = gate(n, u, f)
print("Step 1: h=" + str(nxt[0]) + ", f'=" + str(nxt[1]) + ", n'=" + str(nxt[2]) + ", U'=" + str(nxt[3]))

n2, u2, f2 = nxt[2], nxt[3], nxt[1]
print("State 2: n=" + str(n2) + ", U=" + str(u2) + ", f=" + str(f2))
print("d=" + str(n2-2*u2) + ", defect=" + str(n2-2*u2-3-f2) + ", 4f=" + str(4*f2) + ", n+6=" + str(n2+6))

nxt2 = gate(n2, u2, f2)
print("Step 2: h=" + str(nxt2[0]) + ", f''=" + str(nxt2[1]) + ", n''=" + str(nxt2[2]) + ", U''=" + str(nxt2[3]))

n3, u3, f3 = nxt2[2], nxt2[3], nxt2[1]
print("State 3: n=" + str(n3) + ", U=" + str(u3) + ", f=" + str(f3))
nxt3 = gate(n3, u3, f3)
if nxt3:
    print("Step 3: h=" + str(nxt3[0]) + ", f'''=" + str(nxt3[1]))
else:
    print("Step 3: terminates")

# Derive closed form for t consecutive r=0 steps
print("\n=== Closed form for t consecutive r=0 steps ===")
print("Recurrence: f_{i+1} = 4 f_i - n_i - 5, with n_{i+1} = n_i + 2")
print("Let n_i = n_0 + 2i")
print("Then f_{i+1} = 4 f_i - (n_0 + 2i) - 5 = 4 f_i - n_0 - 2i - 5")
print()
print("This is a linear non-homogeneous recurrence.")
print("Homogeneous solution: f_i^h = C * 4^i")
print("Particular solution: try f_i^p = A*i + B")
print("  A(i+1) + B = 4(A*i + B) - n_0 - 2i - 5")
print("  A*i + A + B = 4A*i + 4B - n_0 - 2i - 5")
print("  Coefficients of i: A = 4A - 2 => 3A = 2 => A = 2/3")
print("  Constants: A + B = 4B - n_0 - 5 => 2/3 + B = 4B - n_0 - 5 => 3B = n_0 + 17/3 => B = n_0/3 + 17/9")
print("General solution: f_i = C * 4^i + (2/3)i + n_0/3 + 17/9")
print("At i=0: f_0 = C + n_0/3 + 17/9 => C = f_0 - n_0/3 - 17/9")
print("So f_i = (f_0 - n_0/3 - 17/9) * 4^i + (2/3)i + n_0/3 + 17/9")
print()
print("For integer arithmetic, multiply by 9:")
print("9 f_i = (9 f_0 - 3 n_0 - 17) * 4^i + 6i + 3 n_0 + 17")
print()
print("Check with n_0=36, f_0=13:")
print("  9*13 = 117, 3*36+17 = 125, so C*9 = 117-125 = -8")
print("  i=0: (-8)*1 + 0 + 125 = 117 => f_0 = 13 ✓")
print("  i=1: (-8)*4 + 6 + 125 = -32 + 131 = 99 => f_1 = 11... wait, that's not 16")
print()
print("Let me recheck the algebra...")
print("f_1 = 4*13 - 36 - 5 = 52 - 41 = 11? But gate gave 16!")
print("Wait, n_1 = n_0 + 2 = 38, not 37?")
print("Gate: n' = n + h = 36 + 2 = 38. But earlier output said n'=37?")
print("Let me check: h=2, so n' = n + h = n + 2. Yes, n' = 38.")
print("But the output said n'=37. Let me recheck...")

# Recheck
n, u, f = 36, 0, 13
nxt = gate(n, u, f)
print("Recheck: n=" + str(n) + ", h=" + str(nxt[0]) + ", n'=" + str(nxt[2]))
print("n' should be n + h = " + str(n + nxt[0]))