import csv, math
rows=[(int(r["n"]),int(r["live_before"]),int(r["absorbed"]),int(r["merged"]),int(r["live_after"]))
      for r in csv.DictReader(open("data/sweep_10M.csv"))]
print(f"logged rows: {len(rows)}")
print("\nlive-set decay (distinct values still running at index n), 1..10^7")
print(f"{'n':>12} {'live':>10} {'n*live':>16}")
targets=[10,100,1000,10**4,10**5,10**6,10**7,10**8,3*10**8]
i=0
for T in targets:
    best=None
    for (n,lb,ab,mg,la) in rows:
        if n<=T: best=(n,la)
        else: break
    if best: print(f"{best[0]:>12} {best[1]:>10} {best[0]*best[1]:>16,}")
tot_absorb=sum(r[2] for r in rows)
print(f"\ntotal absorbed events logged : {tot_absorb}")
# where does the work go?
work=sum(r[1] for r in rows)
print(f"sum of live_before (work)    : {work:,}")
cum=0; 
for (n,lb,ab,mg,la) in rows:
    cum+=lb
    if cum>=work//2:
        print(f"half the sweep work is done by index n = {n:,}")
        break
mx=max(rows,key=lambda r:r[2])
print(f"busiest index (most absorptions): n={mx[0]}, {mx[2]} absorbed")
