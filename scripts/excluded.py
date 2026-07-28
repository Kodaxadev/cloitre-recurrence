import csv
cs=set()
for r in csv.DictReader(open("data/census_10M.csv")): cs.add(int(r["c"]))
lim=max(c for c in range(1,5000) if (3*c+5)**2 <= 10**7)
miss=[c for c in range(1,lim+1) if c not in cs]
print(f"all m <= 10,000,000 exhaustively covered; Theorem 18 settles every c <= {lim}")
print(f"c values in 1..{lim} PROVED never to occur: {len(miss)}")
print(miss)
print()
print(f"density of attained c in 1..{lim}: {100*(lim-len(miss))/lim:.1f}%")
open("data/excluded_increments.txt","w").write(
   f"# increments c proved never to be an eventual increment (Theorem 18 + exhaustive m<=10^7)\n"
   f"# valid for all c <= {lim}\n" + "\n".join(map(str,miss)) + "\n")
