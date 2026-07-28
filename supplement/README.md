# Computational supplement

This supplement is separate from the proof manuscript. It records algorithms,
finite completeness arguments, certificates, independent checks, and exact
reproduction commands.

## Claim-to-evidence matrix

| Claim | Required evidence | Current evidence |
|---|---|---|
| Every \(m\le10^7\) stabilizes | Complete live-set exhaustion with covering identity | Rust compressed sweep and witness census |
| Record orbit in that range | Witness-bearing census plus raw recurrence check | Census; selected records rechecked in independent `u128` |
| Increment 5 and 7 are absent | Theorem 18 plus complete resolution below 160 and 260 | Independent literal recurrence verifier and complete 259-row certificate |
| 106 increments through 1823 are absent | Theorem 18 plus complete \(10^7\) census | `data/excluded_increments.txt` |
| Periodic denominator families through 501 fail | Exact family enumeration and immutable digest | 463-family Python certificate |
| Safe map at \(N=10^6\) empties | Dominance theorem plus complete compressed state exhaustion | Rust and independent Python generators agree on every terminal count and the trajectory digest |

## Independence boundary

The project has three recurrence implementations:

1. optimized Rust `u64` quotient-remainder dynamics;
2. independent Rust `u128` raw-\(b\) recurrence;
3. Python arbitrary-precision raw-\(b\) recurrence.

The second and third implementations strongly check orbit rows, arithmetic,
minimal absorption indices, and published OEIS values. They do not independently
reproduce the complete \(10^7\) compressed census. That distinction must remain
explicit.

Two additional audit implementations are narrower and intentionally share no
project code: `independent/verify_small_spectrum.py` regenerates the complete
\(m<260\) spectrum, and `independent/verify_safe_certificate.py` regenerates
the \(N=10^6\) safe-map certificate using sorted image lists rather than the
Rust ordered-map implementation. The bounded regression verifier
`independent/verify_safe_checkpoint.py` checks Theorem 46's local dominance,
Lemma 47's signed coordinates, Corollary 48's even-witness predecessor,
Lemma 49's quotient clearance, and Theorem 50's complementary-residue
constructions directly from raw \((n,q,e)\) thresholds; it is not a
substitute for their symbolic proofs.

## Files

- [`01-search-and-census.md`](01-search-and-census.md): algorithms and
  completeness invariants.
- [`02-certificates.md`](02-certificates.md): finite certificate definitions,
  hashes, and independence limits.
- [`03-reproduction.md`](03-reproduction.md): exact commands and expected
  outputs.

Cryptographic artifact hashes are in
[`../audit/evidence-manifest.md`](../audit/evidence-manifest.md).
