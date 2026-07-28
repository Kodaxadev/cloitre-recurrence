#!/usr/bin/env python3
"""Two focused questions.

(1) Abercrombie's open question in A117846: "Do the values a(n) include all
    positive numbers?"  We test coverage of small increments and measure the
    lower envelope of c as a function of the start m, which is what decides
    whether an unattained small value could still appear for larger starts.

(2) The tail law for the stabilization index, measured over STARTS (uniform in
    m), which is the distribution the 1/n capture heuristic actually predicts.
    Measuring over distinct orbits instead is biased and gives a different
    exponent.
"""
import argparse
import csv
import math
from collections import defaultdict

p = argparse.ArgumentParser()
p.add_argument("--scan", default="../data/scan_200k.csv")
p.add_argument("--census", default="../data/census_10M.csv")
a = p.parse_args()

# ---------------------------------------------------------------- per start
rows = []
with open(a.scan, newline="") as fh:
    for r in csv.DictReader(fh):
        rows.append((int(r["m"]), int(r["t"]), int(r["c"])))
rows.sort()
M = len(rows)
print(f"per-start rows: {M}")

print("\n(2) TAIL LAW over starts, P(t > N), m uniform in 1..200000")
print(f"{'N':>10} {'#starts>N':>10} {'P':>10} {'N*P':>12} {'N^0.5*P':>10}")
ts = sorted(t for _, t, _ in rows)
for e in range(2, 8):
    N = 10 ** e
    k = sum(1 for t in ts if t > N)
    P = k / M
    print(f"{N:>10} {k:>10} {P:>10.5f} {N*P:>12.1f} {math.sqrt(N)*P:>10.3f}")

# The heuristic predicts P(t>N) ~ C*sqrt(m_typ)/N once N exceeds the entry
# index sqrt(2m). Fit the exponent by regression on the decades above 10^3.
pts = []
for e in range(3, 7):
    N = 10 ** e
    k = sum(1 for t in ts if t > N)
    if k:
        pts.append((math.log(N), math.log(k / M)))
sx = sum(x for x, _ in pts) / len(pts)
sy = sum(y for _, y in pts) / len(pts)
slope = sum((x - sx) * (y - sy) for x, y in pts) / sum((x - sx) ** 2 for x, _ in pts)
print(f"fitted exponent: P(t>N) ~ N^({slope:.3f})     (pure 1/n heuristic predicts -1)")

# ------------------------------------------------------- lower envelope of c
print("\n(1a) LOWER ENVELOPE of c(m) over dyadic blocks of starts")
print(f"{'block':>18} {'min c':>8} {'min c/sqrt(m)':>14} {'max c':>12}")
lo = 1
while lo < 200000:
    hi = min(lo * 2, 200000)
    blk = [(m, c) for m, _, c in rows if lo <= m < hi]
    if blk:
        mn = min(c for _, c in blk)
        mx = max(c for _, c in blk)
        print(f"{f'[{lo},{hi})':>18} {mn:>8} {mn/math.sqrt(lo):>14.3f} {mx:>12}")
    lo = hi

# ------------------------------------------------- which small c are attained
cs_scan = {c for _, _, c in rows}
cs_cen = set()
with open(a.census, newline="") as fh:
    for r in csv.DictReader(fh):
        cs_cen.add(int(r["c"]))

print("\n(1b) SMALL INCREMENT COVERAGE")
for name, s, bound in (("m <= 200,000 (per-start scan)", cs_scan, 200_000),
                       ("m <= 10,000,000 (census)", cs_cen, 10_000_000)):
    miss = [k for k in range(1, 201) if k not in s]
    print(f"  {name}")
    print(f"    missing from 1..200 : {miss}")

# For every unattained small c, what start would be needed? Use the measured
# envelope min c(m) >= alpha*sqrt(m) to bound the search that would be required.
env = min((c / math.sqrt(m)) for m, _, c in rows if m > 1000)
print(f"\n  measured envelope constant: min over m>1000 of c/sqrt(m) = {env:.4f}")
print(f"  => c = k can only arise from m <~ (k/{env:.4f})^2")
for k in sorted({kk for kk in range(1, 30) if kk not in cs_cen}):
    print(f"     c = {k:<3} would need m <~ {int((k/env)**2):,}  "
          f"(exhaustively checked to 10,000,000: NOT attained)")

# ----------------------------------------------------- 316 cluster structure
print("\n(3) THE 316 CLUSTER (MathOverflow Q2)")
bym = defaultdict(list)
for m, _, c in rows:
    bym[c].append(m)
for c in (313, 314, 315, 316, 317, 318):
    v = bym.get(c, [])
    print(f"  c={c}: {len(v):>4} starts <=200000, smallest {v[0] if v else '-'}, "
          f"largest {v[-1] if v else '-'}")
best = sorted(bym.items(), key=lambda kv: -len(kv[1]))[:8]
print("  most popular increments among starts <= 200000:")
for c, v in best:
    print(f"    c = {c:<8} attained by {len(v)} starts")
