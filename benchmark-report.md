# Benchmark report

Hardware: Windows 11, 16 logical cores. Toolchain: `rustc 1.94.0`, `--release`,
`opt-level=3`, `lto=fat`, `codegen-units=1`, **`overflow-checks = true`**.
Zero external dependencies in either crate.

All timings below are wall clock from the binaries' own instrumentation. Every
variant compared is asserted to produce *identical* output, so no speedup here was
obtained by computing something weaker.

---

## 1. The inner loop: eliminating the division

The obvious implementation iterates $b\mapsto b+(b\bmod n)$ and tests absorption
with $(n+1)\mid b$ — two 64-bit divisions per step. Working in $(q,r)$ coordinates
instead makes the step division-free: with $d=2r-q$,

$$-(n{+}1) < -q \le d \le 2n-2 < 2(n{+}1),$$

so reducing $d$ modulo $n+1$ is a **single conditional add or subtract**, and the
quotient update is the corresponding $\pm1$ (Lemma 4). Absorption becomes `q == r`,
costing nothing.

Workload: starts $1..2\times10^4$, **2,189,157,723 iterations**, single-threaded.

| variant | seconds | ns/iteration | speedup |
|---|---|---|---|
| `b`-form, 2 divisions/step | 31.33 | 14.31 | 1.00× |
| `b`-form, 1 division/step | 21.02 | 9.60 | 1.49× |
| **`(q,r)`-form, division-free** | **8.63** | **3.94** | **3.63×** |

`cargo run --release --bin bench -- --lo 1 --hi 20000`

### Cost of overflow checks: zero

| profile | ns/iteration (division-free) |
|---|---|
| `release` (overflow-checks **on**) | 3.942 |
| `bench-nocheck` (overflow-checks off) | 4.615 |

The checked build measured *faster* here; the difference is codegen noise, not a
real effect. Conclusion: **there is no reason to run this workload unchecked**, so
every result in this project was produced with arithmetic overflow checking
enabled. A silent wraparound would invalidate every claim, and it costs nothing to
exclude.

Range safety, independently: $b_n\le b_{n_0}+n^2/2$ (Theorem 5), so $b$ stays below
$2^{63}$ for all $n<4\times10^9$. The largest value actually reached in this project
is $b_t=2.68\times10^{16}$ at $t=3.28\times10^8$ — a factor $690$ below the `u64`
ceiling. The checks confirm this rather than assume it.

---

## 2. Per-start scan vs compressed sweep

| range | per-start scan (16 threads) | sweep (1 thread) | sweep iterations | compression |
|---|---|---|---|---|
| $2\times10^4$ | 4.75 s | **0.82 s** | 6,990,207 | 313× |
| $2\times10^5$ | 21.54 s | **2.56 s** | 24,582,592 | 363× |
| $10^6$ | 80.43 s | **4.71 s** | 64,334,330 | 608× |
| $10^7$ | not attempted ($\sim10^{12}$ iters) | **149.2 s** | 1,706,026,290 | $\sim$1900× |

The sweep is single-threaded and still beats a 16-thread scan by 17× at $M=10^6$.
Two separate effects:

1. **Algorithmic** — orbits merge, so the sweep does $\sum_n|L_n|$ work instead of
   $\sum_m t(m)$ (see `compressed-orbit-analysis.md`).
2. **Load balance** — the per-start scan is badly imbalanced. Single-threaded the
   division-free scan of $1..2\times10^4$ takes 8.63 s; on 16 threads it takes
   4.75 s, a speedup of only **1.8×**, because one orbit ($m=11489$, $t=2.76\times10^6$)
   dominates its chunk. The heavy tail that makes the problem interesting also
   makes naive parallelism nearly useless. The sweep has no such problem: its work
   is intrinsically synchronised across $n$.

### Memory

| range | peak live values | peak resident |
|---|---|---|
| $10^6$ | $10^6$ | ~24 MB |
| $10^7$ | $10^7$ | ~240 MB (sweep) / ~400 MB (witness census) |

Peak is always at the very first step, since $|L_2|=M$ and the set only shrinks
(it halves immediately at $n=2$ by the pair-merging theorem). $M=10^8$ would need
roughly 2.4 GB and is the natural next target.

---

## 3. Verification cost

Independent re-verification is deliberately *not* optimised — it re-derives
everything from the literal definition in `u128`, with no $(q,r)$ shortcut and no
prologue, and additionally runs past $t$ to confirm increments are constant.

| task | rows | time |
|---|---|---|
| Rust `u128` full re-verification of $m\le2\times10^5$ | 200,000 | ~9 min, 16 threads, **0 failures** |
| Rust `u128` re-verification of the 10 record orbits (tail 500) | 10 | 41 s, **0 failures** |
| Python arbitrary-precision deep check of a seeded sample | 4,003 | ~6 min, **0 failures** |
| Python OEIS cross-check (A073117 head, A117846 all 68 terms, both parities) | — | ~4 min, **0 failures** |

Verification costs roughly 25× more than the search that produced the data. That
ratio is the right way round.

---

## 4. Determinism and reproducibility

* **Output order is thread-count independent.** The scan writes rows strictly in
  increasing $m$ regardless of `--threads` or `--block`; results are collected per
  chunk and emitted in order.
* **Digests.** Each binary prints an FNV-1a-64 digest over the numeric results
  only. Reruns with different thread counts must produce identical digests.
  Recorded: scan $1..2\times10^5$ → `0x230b00411fa7c340`; scan $1..10^6$ →
  `0x888496cf7dd808f5`; census $1..10^7$ → `0xf554b190e8bd0eee`.
* **Checkpoint / resume.** The scan writes `<done>,<digest>,<max_t>,<argmax>` after
  every block via write-temp-then-rename, and resumes from it. Tested by
  interrupting and restarting.
* **Self-checking runs.** The sweep asserts
  `merges + absorbed + live == starts` and the census asserts
  `records + merges + live == starts`. Both abort rather than report an
  unverified range. These are not diagnostics — they are what makes the $10^7$
  enumeration usable as a *proof* input for Corollary 20.

## 5. Reproduction

```bash
cd search-framework && cargo test --release          # 37 tests
cargo run --release --bin bench   -- --lo 1 --hi 20000
cargo run --release --bin sweep   -- --lo 1 --hi 10000000 --max-n 2000000000
cargo run --release --bin record  -- --lo 1 --hi 10000000 --out ../data/census_10M.csv
cd ../verification-framework && cargo run --release -- --csv ../data/scan_200k.csv
python verify.py --oeis
```
