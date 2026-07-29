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

## Critical-scale consequence

The unit recurrence gives more than the one-gate ceiling. Pure upper at the
preceding gate bounds \(f_i\), while the next recurrence reconstructs \(n_i\);
together they give

\[
n_i<2^{r_{i-1}+r_i+6}.
\]

Summing this overlapping two-gap inequality gives a half-critical lower
bound on the block-start scale. Summing the pure-upper headroom ceiling gives
the matching critical upper bound. These are recorded as Theorem 118:

\[
\frac12\le\liminf\frac{n_J}{J\log_2J}
\le\limsup\frac{n_J}{J\log_2J}\le1.
\]

The independent Python and Rust checks verify quotient erasure on 166,156
literal transitions, both directions of the exact returning-unit state test
on 24,140 arbitrary bounded states, and the local two-gap inequality on 580
consecutive pure-unit pairs.

## Second-order compatibility

Subtracting two consecutive unit recurrences eliminates the absolute index:

\[
2^{r_i+2}f_i+f_{i+2}+r_{i+1}+2
=\left(2^{r_{i+1}+2}+1\right)f_{i+1}.
\]

Modulo the smaller adjacent power of two, this becomes a growing dyadic
congruence whenever all gaps diverge. If the gaps do not diverge, Theorem
118 isolates every recurrent bounded gap between two gaps tending to
infinity. The returned residue after the bounded gap lies in a finite set,
so a subsequence fixes it. Its renewal starts occupy one residue class
modulo the bounded-gap power of two, and its exits land exactly on one
dyadic ladder after the following large gap. Corollary 120 excludes ladder
coefficients below five by combining that exact identity with the next
pure-upper headroom ceiling. The resulting exhaustive alternative is
Theorem 121.

The strict alternating specialization can be eliminated completely. If the
same \((R,a)\) renewal occurs at gaps \(0,2,4\), the intervening large gaps
belong to one residue class modulo \(A=2^{R+2}\). The compatible incoming
residue is an explicit function \(F(L)\), but

\[
F(L+A)-F(L)
=\frac{a2^{L+2}(2^A-1)}{A+1}-1
\]

is exponentially larger than the linear residue change forced between the
renewals. This contradiction is Theorem 122. It excludes strict
alternation, not irregular returns.

Python and Rust check the compatibility identity on 3,250 arbitrary
three-unit transitions and the local ladder identity on all 580 pure-unit
triples in the bounded raw census. They also inspect 167 six-unit windows
and check Theorem 122's exponential inequality on 1,280 Python and 192 Rust
parameter tuples.

Two attempted search improvements were rejected rather than committed. A
single disjunctive SMT model and a reduced two-variable incremental model
both timed out at six gates over small bounded gap alphabets. Those timeouts
are tooling results and provide no negative mathematical evidence.

Lemma 123 subsequently gave a global word-level restriction: a fixed gap
word and two endpoint residues determine at most one start. Its entropy
consequence, Corollary 124, forces each fixed renewal pair to zero block
density.

Unrolling the same coefficients one step further produced Lemma 125. If
\(S\) is the word span and \(d_j\) are its suffix exponents, then

\[
B(n_p+3)=(2^S-1)a+W,\qquad
B=\sum2^{d_j},\quad W=\sum d_j2^{d_j}.
\]

Successive occurrences of \((R,a)\) also force
\(S\equiv0\pmod {2^{R+2}}\). An initial unrestricted subset search timed
out and supplied no evidence. A targeted exact search then found an
infinite family rather than a finiteness obstruction. For
\(7\le a\le32\), \(3\nmid a\), and \(q\equiv4a\pmod {12}\), the gap word
\((8q-5,1)\) sits between two occurrences of \((1,a)\) in a literal
four-block pure-upper safe-map segment. Proposition 126 proves the family
symbolically. It makes Theorem 122 sharp and rejects any strategy based
only on one return word's integrality or local headroom.

## Remaining target

There is still no evidence for a fixed pure-upper chain bound. Theorem 118
forces the critical scale, while Theorem 121 reduces the all-unit branch to
growing congruence moduli or recurrent visits to one fixed dyadic ladder.
Theorem 122 removes three strict alternating returns, while Proposition 126
shows that two occur at arbitrarily large spans. The next useful target is
therefore exact compatibility between successive *different* return words,
or exclusion of the growing-modulus mechanism.
