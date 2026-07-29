# Research log: arbitrary-terminal ridge chains

## Exact generalized map

For a pure ridge word `1^K 0^z`, let the last up-step create `e=-v`.
Writing `A=Q+h+3` and `S=Q+K` gives

```text
N  = 2^K A-K-3-v,
z  = floor(log2(S/v)),
A' = 2^(z+1) v+2.
```

Two consecutive pure ridges therefore satisfy

```text
2^K A+z+K'+1+v'-v = 2^K' A'.
```

The low bits give the exact congruence

```text
2^min(K,K') divides z+K'+1+v'-v.
```

## Adversarial finite search

Raw-state and parameter-space probes reject every naive monotonic
extension of the unit-terminal result. The valid parent

```text
(n,q,r) = (38,18,5)
```

starts eight consecutive pure ridges with `(K,v,z)` values

```text
(1,13,0), (1,11,0), (1,1,4), (1,15,0),
(1,9,1), (1,18,0), (1,16,0), (1,6,1).
```

The ninth ridge has mixed positive digits. Across bounded exact searches,
`K`, `v`, `z`, `2^z v`, and the next ridge width all move in both
directions. These observations are falsification evidence, not the proof
of a universal length bound.

## Surviving restriction

If the congruence representative has absolute value below its modulus, it
must vanish and forces

```text
v' = v-z-K'-1 <= v-2.
```

That descent cannot persist forever. Consequently any infinite pure tail
in the sublinear branch must have infinitely many adjacent pairs where at
least one of `z,K'+1,v,v'` is exponential in `min(K,K')`. This is Theorem
72. It does not cover ridges with mixed zero/up positive portions.
