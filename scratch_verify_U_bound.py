#!/usr/bin/env python3
"""
Verify the exact U-bound derivation: U <= f - 10 from the child-survival condition.
"""

# From the six classes: n = 3f - 3, f_1 = f - 2
# D = n - 2U = 3f - 3 - 2U
# Child-survival condition for first gate (h=2): D - 3 - f_1 >= 16
# Substitute:
#   (3f - 3 - 2U) - 3 - (f - 2) >= 16
#   3f - 3 - 2U - 3 - f + 2 >= 16
#   2f - 4 - 2U >= 16
#   2f - 2U >= 20
#   f - U >= 10
#   U <= f - 10

print("Derivation of U <= f - 10:")
print("  n = 3f - 3")
print("  f_1 = f - 2")
print("  D = n - 2U = 3f - 3 - 2U")
print("  Child-survival: D - 3 - f_1 >= 16")
print("  (3f - 3 - 2U) - 3 - (f - 2) >= 16")
print("  2f - 4 - 2U >= 16")
print("  2f - 2U >= 20")
print("  f - U >= 10")
print("  U <= f - 10")
print()

# Check the ranges
for f in [13, 14, 15, 16, 17, 18]:
    n = 3*f - 3
    max_U = f - 10
    print(f"f={f}, n={n}: U in [0, {max_U}] -> {max_U + 1} states")

total = sum(f - 10 + 1 for f in [13, 14, 15, 16, 17, 18])
print(f"\nTotal states: {total}")

# Also verify the other bound: floor((n - f - 3)/2)
print("\nComparison with floor((n - f - 3)/2):")
for f in [13, 14, 15, 16, 17, 18]:
    n = 3*f - 3
    bound1 = f - 10
    bound2 = (n - f - 3) // 2
    print(f"f={f}, n={n}: U<=f-10={bound1}, floor((n-f-3)/2)={bound2}, min={min(bound1, bound2)}")