# Search and census algorithms

## Literal per-start solver

The reference recurrence is

```text
b <- b + (b mod n)
n <- n + 1
```

Absorption at index \(n\) is tested by

```text
(n+1) divides b, and b/(n+1) < n.
```

The optimized solver first enters \(q_n\le n\), then advances
\((q,r)\) without division. With \(d=2r-q\), exactly one case applies:

```text
d < 0       : (q,r) <- (q-1,d+n+1)
0 <= d<n+1 : (q,r) <- (q,d)
d >= n+1   : (q,r) <- (q+1,d-n-1)
```

Overflow checks are enabled in the release profile.

## Compressed live-set sweep

At index \(n\), define

\[
f_n(b)=b+(b\bmod n).
\]

If two starts reach the same value at the same index, their future orbits are
identical. The sweep therefore stores only the sorted set of distinct live
values.

On a quotient block \(kn\le b<(k+1)n\),

\[
f_n(b)=2b-kn,
\]

which is strictly increasing. Its image lies in
\([kn,(k+2)n)\), so only adjacent block images can interleave. The
implementation restores sorted order by a rolling two-way merge and drops
duplicates.

At each index:

1. remove absorbing values;
2. map every remaining value through \(f_n\);
3. merge equal images;
4. assert the covering identity.

The per-step identity is

```text
live_before = absorbed + merged + live_after.
```

Summed over the run, an empty live set proves that every represented start has
either absorbed or merged into an orbit that later absorbed.

## Witness census

The witness variant stores `(value, smallest_start)` and keeps the smallest
start whenever images merge. Every absorbing value yields

```text
(stabilization index, eventual increment, smallest witness).
```

Its terminal identity is

```text
number of records + number of merges = number of starts.
```

This is sufficient to recover:

- every distinct eventual increment in the range;
- the maximum stabilization index;
- a concrete start witnessing every distinct orbit;
- the total number of merged starts.

It does not retain the eventual increment separately for every merged start,
because equality of current values already proves equality of their futures.

## Completeness conditions

The finite claim “all starts in `[lo,hi]` stabilize” is licensed only when:

1. the initial live set is exactly every integer in `[lo,hi]`;
2. absorption removal uses the proved criterion;
3. every nonabsorbed live value is mapped exactly once;
4. deduplication removes only equal values at the same index;
5. the covering identity holds;
6. the live set becomes empty before the configured index cap;
7. arithmetic does not overflow.

Unit tests compare the optimized merge with a `BTreeSet` reference and compare
witness records with literal per-start solving on bounded ranges.

## Current finite range

The frozen evidence reports:

```text
starts:                 1 through 10,000,000
distinct orbit records: 9,911
record start:           1,320,111
record index:           327,695,231
record increment:       81,923,126
census FNV-1a-64:       0xf554b190e8bd0eee
```

The FNV value is a deterministic regression digest, not a cryptographic
commitment. The corresponding files are bound by SHA-256 in the audit
manifest.
