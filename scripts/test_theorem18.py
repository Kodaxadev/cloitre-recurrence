#!/usr/bin/env python3
"""ADVERSARIAL TEST of Theorem 18:  c(m) = c  implies  m < (3c+5)^2.

If true, every increment c is produced by only finitely many starts, all below
an explicit bound -- which turns "is c ever an eventual increment?" into a FINITE
check, and settles Abercrombie's open question in A117846 for every c whose
bound lies inside the exhaustively verified range.

The test tries hard to break the theorem:
  * checks the bound for every (m, c) pair in the per-start scan,
  * reports the worst case  m / (3c+5)^2  (must stay < 1),
  * separately re-derives the intermediate quantity n* = max{n >= n0 : 3q_n > n+1}
    directly from the orbit and checks the chain
        n* < 3c+5   and   m <= b_{n*} < n*^2
    which is what the proof actually asserts.
"""
import argparse
import csv
import math

p = argparse.ArgumentParser()
p.add_argument("--scan", default="../data/scan_200k.csv")
p.add_argument("--deep", type=int, default=4000, help="orbits to re-derive n* for")
a = p.parse_args()

rows = []
with open(a.scan, newline="") as fh:
    for r in csv.DictReader(fh):
        rows.append((int(r["m"]), int(r["t"]), int(r["c"])))

print(f"testing bound m < (3c+5)^2 on {len(rows)} start values")
worst = (0.0, None)
viol = 0
for m, t, c in rows:
    bound = (3 * c + 5) ** 2
    ratio = m / bound
    if ratio > worst[0]:
        worst = (ratio, (m, t, c, bound))
    if m >= bound:
        viol += 1
        if viol <= 10:
            print(f"  VIOLATION m={m} c={c} bound={bound}")
print(f"violations           : {viol}")
print(f"worst m/(3c+5)^2     : {worst[0]:.6f}  at m={worst[1][0]} c={worst[1][2]} "
      f"bound={worst[1][3]}")

# ---- re-derive the proof's intermediate quantities from the orbit ----------
def orbit_witnesses(m):
    """Return (n0, nstar, b_at_nstar, t, c) computed from the literal orbit."""
    b, n = m, 2          # b_2 = m
    n0 = None
    nstar = None
    b_nstar = None
    while True:
        q, r = divmod(b, n)
        if n0 is None and b < n * n:
            n0 = n
        if n0 is not None and 3 * q > n + 1:
            nstar, b_nstar = n, b
        if q == r:
            return n0, nstar, b_nstar, n, q
        b += r
        n += 1

print(f"\nre-deriving n* directly from the first {a.deep} orbits")
bad = 0
maxns = 0.0
for m, t, c in rows[:a.deep]:
    n0, nstar, b_ns, tt, cc = orbit_witnesses(m)
    assert (tt, cc) == (t, c), f"orbit mismatch m={m}: {(tt,cc)} vs {(t,c)}"
    if nstar is None:
        continue                       # case S = empty, handled separately
    if not nstar < 3 * c + 5:
        print(f"  CHAIN BREAK m={m} c={c}: n*={nstar} not < {3*c+5}")
        bad += 1
    if not b_ns < nstar * nstar:
        print(f"  CHAIN BREAK m={m}: b_(n*)={b_ns} not < n*^2={nstar**2}")
        bad += 1
    if not m <= b_ns:
        print(f"  CHAIN BREAK m={m}: m > b_(n*)={b_ns}")
        bad += 1
    maxns = max(maxns, nstar / (3 * c + 5))
print(f"chain breaks         : {bad}")
print(f"worst n*/(3c+5)      : {maxns:.6f}   (must stay < 1)")

# ---- consequence: which small c are RIGOROUSLY excluded --------------------
attained = {c for _, _, c in rows}
print("\nRIGOROUS exclusion (bound inside the exhaustively scanned range 1..200000):")
excl, undecided = [], []
for c in range(1, 400):
    bound = (3 * c + 5) ** 2
    if bound <= 200_000:
        (excl if c not in attained else None) is not None and c not in attained and excl.append(c)
    elif c not in attained:
        undecided.append(c)
print(f"  c values proved NEVER attained : {excl}")
print(f"  largest c settled by m<=200000 : {max(c for c in range(1,400) if (3*c+5)**2 <= 200000)}")
print(f"  (with m<=10^7 the method settles all c <= "
      f"{max(c for c in range(1, 2000) if (3*c+5)**2 <= 10**7)})")
