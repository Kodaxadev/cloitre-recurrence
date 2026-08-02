#!/usr/bin/env python3
"""
WITHDRAWN: The "Zero-gap run bound theorem" claimed in the previous checkpoint
is INCORRECT and WITHDRAWN.

Errors:
1. Algebraic error: From n <= 4f - 6, replacing n+5 by 4f-1 in 3f > n+5
   gives a stronger SUFFICIENT condition, not an equivalence. The state
   (n=35, U=0, f=14) has h=2 and f'=16 > 14, directly contradicting the
   claim that increase is impossible.

2. Closed-form error: The admissible window width is G-3, not ~8, and G can
   be arbitrarily large. The inequality |C|*4^3 >= 64/9 does not force escape
   from that window.

This file preserves the scratch work but labels the proof as WITHDRAWN.
The finite computation results (max run length 2 up to n=5000) remain valid
as finite computation, but the universal bound proof is invalid.
"""
print("WITHDRAWN - see comments above")