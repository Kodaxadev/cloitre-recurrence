# Compressed orbit analysis

Priority 3 asked for compression rather than brute force. This is the part of the
project that worked best: verification of the conjecture was extended from
$m\le2\times10^5$ to $m\le10^{7}$ (a 50× wider range) while doing **less** total
arithmetic than the baseline, by exploiting the fact that orbits merge.

## 1. The idea

The forward map at index $n$ is

$$f_n(b)=b+(b\bmod n)=2b-n\lfloor b/n\rfloor,$$

affine with slope 2 on each block $[kn,(k+1)n)$. By Theorem 11 it is **at most
2-to-1**, and collisions happen exactly when $n$ is even, $|x-y|=n/2$, and $x,y$ sit
in adjacent blocks. Two starts that collide once are identical forever.

So instead of iterating each start separately, iterate the **set** of distinct
reachable values in lockstep over $n$:

$$L_2=\{1,\dots,M\},\qquad L_{n+1}=f_n\big(L_n\setminus A_n\big),$$

where $A_n=\{b\in L_n : (n+1)\mid b,\ b/(n+1)<n\}$ are the values that stabilize at
index $n$ (Theorem 2). Then

> **every $m\le M$ stabilizes by index $N$ $\iff$ $L_N=\varnothing$.**

Emptiness of the live set is a *complete* verification. No per-start bookkeeping is
needed at all.

## 2. Making a step cost $O(|L_n|)$

The naive obstacle is that $f_n$ is not monotone, so the image of a sorted list is
unsorted and would need an $O(L\log L)$ re-sort every step. But images of block $k$
lie in $[kn,(k+2)n)$, so **only adjacent blocks can interleave**. Processing blocks
in increasing order and carrying a small buffer, a rolling two-way merge restores
sorted order in $O(L)$:

```
for each block k, in increasing order:
    img  <- f_n(values in block k)          # already sorted: slope 2
    merge(carry, img) -> merged             # two-way, O(|carry|+|img|)
    emit merged values < (k+1)*n            # final: later blocks land above
    carry <- the rest
```
Correct because every later block's image is $\ge(k+1)n$. Deduplication during the
emit is where merging is actually harvested. (`search-framework/src/sweep.rs`.)

Both implementations are checked against a brute-force `BTreeSet` reference and
against the per-start solver in the unit tests.

## 3. Results

Sweep work is $\sum_n |L_n|$; per-start work is $\sum_m t(m)$. Both are exact
iteration counts, measured, not estimated.

| range $M$ | per-start $\sum_m t(m)$ | sweep $\sum_n|L_n|$ | **compression** | sweep wall time |
|---|---|---|---|---|
| $2\times10^4$ | 2,189,157,723 | 6,990,207 | **313×** | 0.82 s |
| $2\times10^5$ | 8,914,267,251 | 24,582,592 | **363×** | 2.56 s |
| $10^6$ | 39,081,652,939 | 64,334,330 | **608×** | 4.71 s |
| $10^7$ | — (not run: would be $\sim10^{12}$) | 1,706,026,290 | $\sim$**1900×** | 149 s |

The compression ratio grows with $M$, because the live set decays like a power of
$n$ while the number of starts grows linearly.

**Verification achieved.** $L_N=\varnothing$ at $N=327{,}695{,}232$ for $M=10^7$:
every start up to ten million stabilizes, the last one at index 327,695,231.

## 4. The census: which orbits are they?

Carrying one extra `u64` per live value — the smallest start reaching it — turns
the sweep into a complete census (`src/witness.rs`, `src/bin/record.rs`). Each
absorbing event then yields a triple $(t,c,m)$, and the identity

$$\#\text{records} + \#\text{merges} + \#\text{live} = \#\text{starts}$$

is asserted at the end of every run, which *proves* the census covers the whole
range rather than merely appearing to.

| $M$ | distinct orbits | starts per orbit |
|---|---|---|
| $2\times10^4$ | 406 | 49× |
| $2\times10^5$ | 1,299 | 154× |
| $10^6$ | 3,043 | 329× |
| $10^7$ | **9,911** | **1009×** |

Ten million starting values give only **9,911 genuinely different orbits.** The
count grows roughly like $M^{1/2}$, which is the same exponent as the entry index
$n_0\approx\sqrt{2m}$ — consistent with each orbit "capturing" a neighbourhood of
starts of width $\sim\sqrt m$.

### Top of the census ($m\le10^7$)

| $t$ | $c$ | smallest $m$ | $c/t$ |
|---|---|---|---|
| 327,695,231 | 81,923,126 | 1,320,111 | 0.249998 |
| 303,967,101 | 75,990,326 | 2,283,283 | 0.250 |
| 133,301,871 | 33,324,063 | 1,529,233 | 0.250 |
| 90,502,807 | 22,627,131 | 3,350,571 | 0.250 |
| 89,913,893 | 22,476,689 | 2,608,579 | 0.250 |

All ten leading rows were re-verified independently in u128 from the literal
definition, including 500 steps past $t$ to confirm the increments are constant.
The $c/t\to1/4$ law is visible to six digits at $t=3\times10^8$.

## 5. What the compression bought mathematically

Not just speed. The census is what makes **Theorem 18** usable: because it
enumerates *all* $m\le10^7$ with a checked covering identity, it establishes that
certain increments are never attained — which, combined with the bound
$m<(c+3)(3c+5)$, is a proof rather than an observation. Without the compression the
$10^7$ enumeration would have cost $\sim10^{12}$ iterations; with it, 149 seconds.

## 6. Compression ideas that did NOT work

Recorded because negative results are results.

* **Interval / affine propagation.** Since $f_n$ is affine on blocks, one can carry
  the live set as a union of intervals rather than points. This is compact early
  (at $n\approx700$ the live set is ~45% dense in its range), but it fails as soon
  as absorbing values must be *removed*: each removal is a single point and splits
  an interval. The number of fragments then grows like $n$ per step and overtakes
  the point representation almost immediately. Abandoned.
* **Symbolic states.** Representing a live set as a residue class plus offsets
  fails for the reason established in `invariant-search.md` §C: $b_{n+1}\bmod M$ is
  not a function of $(n\bmod M, b\bmod M)$ for any $M\in[2,64]$, so residue classes
  are not preserved and there is nothing to propagate symbolically.
* **Backward tree from the absorbing ray.** Preimages of a state at index $n$ are
  $b_{n-1}=(b+k(n-1))/2$ over the valid $k$, about 1.5 on average — so the backward
  tree *branches*, growing rather than shrinking. Useful for structural questions,
  useless as a search compression.
* **Memoization on $(n,b)$.** Subsumed by the sweep: the sweep *is* the optimal
  memoization, since it visits each distinct $(n,b)$ exactly once by construction.

## 7. Reproduction

```bash
cargo run --release --bin sweep  -- --lo 1 --hi 10000000 --max-n 2000000000
cargo run --release --bin record -- --lo 1 --hi 10000000 --out ../data/census_10M.csv
```
Both are deterministic and print a digest; the census asserts its covering identity
and will abort rather than report an uncovered range.
