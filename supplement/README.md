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
Lemma 49's quotient clearance, Theorem 50's complementary-residue
constructions, and Lemma 51--Corollary 52's accelerated zero-epoch formulas
directly from raw \((n,q,e)\) thresholds. It also checks Lemma 53's
autonomous overshoot, Theorem 55's positive-block bound, and Lemma 80's
wrap-block state-window inequalities; it is not a substitute for their
symbolic proofs.
`independent/verify_safe_block_gates.py` separately checks Lemma 83's exact
parent equation and interval, plus Corollary 84's lattice count and strict
multiple-candidate alternative, on 29,630 bounded raw gates. It reconstructs
and executes every alternative candidate to check that the gate is exact.
It also checks Lemma 85 and Corollary 86 on every unit-wrap gate in that
census, on 9,682 additional gates with arbitrary bounded accumulated quotient,
and reproduces a valid chain of seven consecutive unique gates.
It also checks Lemma 87's two-gap Diophantine compatibility through
\(0\le r,r'\le64\) and executes the unique surviving terminal path directly.
Corollaries 88--89 and Theorem 90 are symbolic consequences and are not
inferred from the bounded enumeration.
Theorem 91 is likewise symbolic; the bounded seven-gate search is supporting
falsification evidence, not its proof. The independent verifier additionally
checks the finite affine-dyadic obstruction for every \(50\le L<65\) and the
epoch-crossing inequality through \(L<1000\).
The native `safe_block_gates` Rust test repeats the same census and
reconstruction through the safe-map implementation and independently checks
the parent-boundary compatibility grid and terminal path.

`independent/verify_general_gate_boundaries.py` independently re-enumerates
27,030 adjacent arbitrary-length raw gates and checks both directions of
Lemma 92 and Corollary 93. It classifies all 18,619 nonunique gates in that
census by the exact lower-neighbor or paired-upper-boundary alternative.
Separately, a bounded affine parameter scan through
\(k,k',r,r'\le16\) finds three consecutive unique parent-boundary patterns.
That last count is exploratory finite evidence, not a theorem or a claim
that the three patterns are globally exhaustive. The checker also isolates
the sole determinant-zero binary-defect tuple within that grid and verifies
the parity obstruction used symbolically in Corollary 95.
The same raw census checks all 107 observed transitions whose two positive
starts both have defect at most one and confirms the block-length
monotonicity of Lemma 96. The native Rust gate census repeats that check
through the primary safe-map implementation.
For those transitions the Python checker also verifies Lemma 98's exact
returned-residue equation and next-index identity directly from raw states.
The unboundedness and Cesaro conclusions of Theorem 99 are symbolic; no
finite census is presented as evidence for their infinite-tail quantifiers.
Finally, an affine scan through \(k,r,r',r''\le12\) finds no four
consecutive parent-boundary starts with the same positive block length.
This is evidence for the fixed-length target after Corollary 97, not a
uniform exclusion theorem.

`independent/verify_parent_gap_dynamics.py` checks Lemma 100 on arbitrary
bounded-quotient parent-boundary starts through \(n\le500\), finding five
constant-length triples and confirming strict gap increase in each. It also
rejects the two formal decreasing-gap exceptions by their exact state-bound
and parity failures. The native Rust test independently reproduces the same
five transitions. Theorem 101 itself is symbolic.

`independent/verify_child_boundary_window.py` reuses the independent raw
transition enumerator, but not project dynamics code, to check Lemma 103 on
27,030 gates and Corollary 104 on 25,646 interior gates. It finds 7,380 first-window unique
gates and 18,266 later-window nonunique gates, with exact agreement in both
directions. It also exhausts all residues for 30 bounded \((k,r)\) pairs to
check Corollary 105's permutation statement. The native Rust gate census
independently checks the canonical residue, translate decomposition, and
window iff condition through the primary safe-map implementation. These
finite checks support the identities; they do not prove orbitwise
equidistribution or termination. Python checks Lemma 106's exact next-block
band and Corollary 107's unit-versus-long threshold on all 8,411 unique
gates in its raw census; the native Rust census independently checks the
same statements on its 9,718 unique gates.

The exploratory Rust binary `gate_chain` searches these chains without
assuming that the accumulated quotient is zero. Exhausting all 20,771,000
valid positive-block zero epochs with \(2\le n\le1000\) found seven
consecutive unique unit-wrap gates from \((n,U,e)=(36,9,13)\), and no longer
chain. This is bounded evidence, not a uniform chain bound. From
`search-framework/`, reproduce it with:

```powershell
cargo run --release --bin gate_chain -- --min-n 2 --max-n 1000 --all-quotients
```
`independent/verify_sharp_growth.py` separately checks Theorem 56's
parameterized rebound implication on arbitrary states and its finite
inequality on literal starting orbits. It also tests Corollary 57's
optimized floor choice on two long record orbits and Theorem 58's finite
low-window down-step charge and explicit rebound-length bound on arbitrary
states. It also checks Lemma 60's weighted budget on arbitrary finite
prefixes and Lemma 62's integer-scaled post-down zero identity. These
bounded checks support the algebra and endpoint handling; they do not prove
the asymptotic limits.

The exact Rust probe `search-framework/src/bin/ridge.rs` exhausts selected
post-down ridge states and reports the longest segment and the smallest
observed up-step fraction above a requested length. It is an exploratory
falsification tool. Proposition 66 now refutes the universal positive-density
target exactly; the probe remains useful for testing stronger
reachability-sensitive replacements.

`independent/verify_ridge_segments.py` separately checks Lemma 63's
sign-changing last up-step, negative zero suffix, and next-ridge remainder,
plus Lemma 65's consecutive-down defect recurrence, using raw transitions.
It also checks Proposition 66's arbitrary-precision diluted family through
\(K=12\), plus a bounded grid of Lemma 68's incompatible scale equation.
The arbitrary-terminal checks validate 518 pure ridges and 171 adjacent
instances of Lemmas 70--71 on bounded raw states, and reproduce an exact
valid chain of eight pure ridges. The native
`ridge_segments` Rust test checks the same identities, the special family
through the largest listed parameters fitting `u64`, and distinct bounded
scale and arbitrary-terminal grids.

`independent/verify_mixed_ridges.py` checks Lemma 73's arbitrary positive-zero
defect, its adjacent compatibility equation, Corollary 74's terminal-run
congruence, Lemma 76's complete terminal dyadic ladder, and Lemma 78's
finite state-window inequality on 6,846 raw ridges and 6,486 adjacent
pairs. It also reproduces a valid local prefix of 100 ridges whose terminal
up-runs all have length at most two. The separate native Rust
`mixed_ridges` test checks the same identities on a distinct bounded grid.
Neither prefix is claimed reachable from \(b_1=m\), and the finite checks
do not prove Theorems 75/77 or Corollary 79.

The exploratory native `ridge_trace` binary measures initial, internal, and
terminal up-runs on literal recurrence orbits and verifies the normalized
last-zero parity identity at every completed mixed ridge. It is a
falsification tool, not a certificate.

## Files

- [`01-search-and-census.md`](01-search-and-census.md): algorithms and
  completeness invariants.
- [`02-certificates.md`](02-certificates.md): finite certificate definitions,
  hashes, and independence limits.
- [`03-reproduction.md`](03-reproduction.md): exact commands and expected
  outputs.

Cryptographic artifact hashes are in
[`../audit/evidence-manifest.md`](../audit/evidence-manifest.md).
