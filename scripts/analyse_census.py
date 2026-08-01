#!/usr/bin/env python3
"""Structural analysis of the compressed orbit census.

Answers, from data:
  * Abercrombie's open question in A117846: "Do the values a(n) include all
    positive numbers?"  -> which integers occur as eventual increments c.
  * the tail law  P(t > N) ~ C/N  predicted by the 1/n capture heuristic
  * the  c ~ t/4  law predicted by  b_n ~ n^2/4
  * cluster structure: how many distinct starts share each c (the "316 effect")
"""
import argparse
import csv
import math
from collections import Counter

p = argparse.ArgumentParser()
p.add_argument("--census", default="../data/census_10M.csv")
p.add_argument("--hi", type=int, default=10_000_000)
p.add_argument("--out", default="../data/computational-results.csv")
a = p.parse_args()

recs = []
with open(a.census, newline="") as fh:
    for r in csv.DictReader(fh):
        recs.append((int(r["t"]), int(r["c"]), int(r["witness_m"]), int(r["b_t"])))
print(f"distinct orbits in census : {len(recs)}")
print(f"starts covered            : 1..{a.hi}")
print(f"compression               : {a.hi / len(recs):.1f}x")

# --- internal consistency ---------------------------------------------------
bad = [r for r in recs if r[3] != r[1] * (r[0] + 1) or r[1] >= r[0]]
print(f"rows failing b_t=c(t+1), c<t : {len(bad)}")
assert not bad

# --- the c ~ t/4 law --------------------------------------------------------
ratios = [c / t for t, c, _, _ in recs]
big = [c / t for t, c, _, _ in recs if t > 10_000]
print(f"\nc/t over all orbits       : mean {sum(ratios)/len(ratios):.6f}")
print(f"c/t for t > 10^4          : mean {sum(big)/len(big):.6f}  "
      f"min {min(big):.6f}  max {max(big):.6f}   (predicted 0.25)")

# --- Abercrombie's coverage question ----------------------------------------
cs = sorted({c for _, c, _, _ in recs})
cset = set(cs)
missing = [k for k in range(1, 4001) if k not in cset]
print(f"\ndistinct c values attained : {len(cs)}")
print(f"largest c attained         : {max(cs)}")
print(f"missing from 1..4000       : {len(missing)}")
print(f"smallest missing c         : {missing[0] if missing else 'none'}")
print(f"first 25 missing           : {missing[:25]}")
for lim in (10, 50, 100, 500, 1000, 2000, 4000):
    have = sum(1 for k in range(1, lim + 1) if k in cset)
    print(f"  c in 1..{lim:<5} attained : {have}/{lim}  ({100*have/lim:.1f}%)")

# --- tail law  P(t > N) ~ C/N ----------------------------------------------
ts = sorted(t for t, _, _, _ in recs)
print(f"\ntail law: N * P(t > N) should be roughly constant")
print(f"{'N':>12} {'#orbits>N':>10} {'N*P':>14}")
for e in range(3, 9):
    N = 10 ** e
    k = sum(1 for t in ts if t > N)
    print(f"{N:>12} {k:>10} {N * k / len(recs):>14.1f}")

# --- clustering: how many starts share an increment -------------------------
cnt = Counter(c for _, c, _, _ in recs)
top = cnt.most_common(12)
print(f"\nincrement values shared by the most distinct orbits:")
for c, k in top:
    print(f"  c = {c:<10} shared by {k} distinct orbits")
print(f"316 shared by {cnt.get(316, 0)} distinct orbits "
      f"(the MathOverflow 'mysterious 316')")

# --- write the consolidated results table -----------------------------------
recs.sort(key=lambda r: -r[0])
with open(a.out, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["rank", "t", "c", "witness_m", "b_t", "c_over_t"])
    for i, (t, c, m, b) in enumerate(recs[:2000], 1):
        w.writerow([i, t, c, m, b, f"{c/t:.9f}"])
print(f"\nwrote top 2000 orbits to {a.out}")

# --- growth of the record as a function of the search bound -----------------
print("\nrecord stabilization index as the start bound grows:")
best = {}
for t, c, m, _ in recs:
    for e in range(1, 8):
        lim = 10 ** e
        if m <= lim and t > best.get(lim, (0, 0, 0))[0]:
            best[lim] = (t, c, m)
print(f"{'bound':>10} {'record t':>14} {'c':>12} {'m':>10} {'t/bound^1.5':>12}")
for e in range(1, 8):
    lim = 10 ** e
    if lim in best:
        t, c, m = best[lim]
        print(f"{lim:>10} {t:>14} {c:>12} {m:>10} {t / lim**1.5:>12.3f}")
