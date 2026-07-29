# Research log: upper ambiguity and residue transfer

## Question

Lemma 110 leaves one difficult nonunique mechanism: the canonical translate
can remain \(j=0\) while a large child defect activates an upper candidate.
The first attempted target was that consecutive occurrences of this
"pure-upper" mechanism have uniformly short duration.

## Falsification sequence

Exact safe-map searches gave:

| Search domain | States | Longest pure-upper run |
|---|---:|---:|
| Quotient-zero starts, \(n\le700\) | 60,900 | 5 |
| All valid positive starts, \(n\le700\) | 7,115,324 | 5 |
| All valid positive starts, \(n\le1500\) | 70,172,124 | 6 |
| Quotient-zero starts, \(n\le10,000\) | 12,495,000 | 6 |

The length-six record begins on a valid safe path at
\((n,U,e)=(971,5,482)\). Its block/gap word is

\[
(k_i,r_i)=
(6,0),(1,1),(1,3),(1,3),(1,1),(1,5).
\]

Thus every proposed bound below six is false. The searches do not establish
that six is maximal, and the witness is not claimed reachable from an
original start \(b_1=m\).

Simple defect monotonicity is also false. Along the witness the successive
defects are

\[
2,\ 413,\ 461,\ 461,\ 417,\ 475,\ 281.
\]

The upper storage can be replenished as well as consumed.

## Symbolic finite-word check

For a fixed digit word, every safe-step condition is a linear integer
inequality in the initial \((n,U,e)\). The script
`independent/synthesize_pure_upper.py` encodes those inequalities directly.
It reconstructs the six-gate word without invoking project transition code.

`independent/search_pure_upper_pattern.py` performs a bounded depth-first
search over block/gap alphabets. Solver-node, block, gap, and initial-index
bounds are explicit. Several length-seven searches exhausted their wall-time
budgets before their node budgets; those runs provide no negative evidence
and are not recorded as certificates.

## Exact transfer found

The failed monotonicity route exposed a stronger algebraic identity. If
\(x\) is a gate's child excess, then the child overshoot is

\[
2A'=n'+5-x.
\]

Consequently a child block of length \(\ell\) returns with residue

\[
g=n'+\ell+4-2^{\ell-1}(n'+5-x).
\]

For a unit child, \(g=x\). This makes consecutive unit blocks a closed
affine recurrence and gives an exact pure-upper inequality test. These are
Lemma 113 and Corollaries 114--115.

## Verification

The independent Python raw-gate census checks the transfer on 27,030 gates,
including 15,342 unit-child gates. The native Rust test checks the same
identity through the primary safe-map implementation. Both pin the
six-gate witness explicitly.

## Remaining target

There is no evidence for a fixed pure-upper chain bound. The defensible next
question is whether the unit-block affine recurrence admits pure-upper words
of unbounded length. Either an unbounded construction or a proof that every
sufficiently long word forces a longer child block would materially simplify
the surviving nonunique branch.
