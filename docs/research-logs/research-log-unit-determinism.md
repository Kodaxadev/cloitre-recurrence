# Research log: forcing the fixed-ladder gate

## Where the previous checkpoint left the problem

After Lemma 127 and Lemma 128 the fixed-ladder branch looked like a
compatibility problem. Each return word was rigid, and two successive words
had to satisfy the cross-word equation (127.5). The open question was phrased
as an infinite-chain problem for that equation under the nondecreasing
dyadic-window constraint, and a bounded search had turned up 35 positive
equal-endpoint return words with no compatible consecutive pair.

That framing was more complicated than the object required.

## The observation

Lemma 128 already proved that the pure-upper windows at a fixed returned
residue are disjoint and ordered. The proof of that disjointness uses only two
of the pure-upper inequalities and only the inequality $D\le n$. It therefore
does not depend on the returned residue being fixed, nor on the word being a
return word, nor on the wrap count. Applied at every block instead of at
matched renewals, it says the outgoing gap of an all-unit pure-upper block is
*unique* — so there is nothing to choose.

Working that through gave Theorem 130. The forced exponent has a closed form,

\[
h^\ast=\min\{h\ge2:\ 2^hf\ge n+h+4\},
\]

and the gate exists exactly when three explicit inequalities hold at that one
$h^\ast$. The successor is automatically a valid unit state, so no separate
admissibility bookkeeping is needed either.

Consequences that were not visible in the word framing:

* The cross-word equation (127.5) is not a constraint to be solved. Along any
  orbit it holds automatically, because the whole gap word is a function of the
  starting state. What remains is whether one particular deterministic orbit
  survives forever.
* The wrap count never enters the forced data. Lemma 131 makes this exact:
  the $(n,f)$ trajectory is independent of $U$, and both $U$-dependent tests
  relax as $U$ falls. So a sweep at $U=0$ decides every wrap count at once.
  Lemma 116 had only preserved digit words; it did not compare chain lengths.

## What the computation then showed

Determinism also collapses the search cost. The canonical-translate condition
pins $f$ to about four consecutive integers once $(n,h)$ is fixed, so the set
of states with an outgoing gate is enumerable in $O(N\log N)$. Iterating each
is $O(1)$ amortized.

The result is flat and unexpected: the longest all-unit pure-upper chain is
**five gates**, first available at index $978$, and that witness is exactly
K14. No six-gate chain exists anywhere in the swept range — $5\times10^9$ start
indices, $133{,}599{,}589{,}858$ live gate states, every wrap count. The two
enumerations — by residue in $O(N^2)$ and by exponent in $O(N\log N)$ — agree
exactly on state counts and on the table of least start indices, which is the
main guard against an enumeration bug.

The explicit infinite family of Proposition 126 turns out to be *shorter* than
the sporadic record. Iterating the forced map in exact arbitrary-precision
arithmetic reproduces its gap word $(1,L,1,L)$, its residues $(a,c,a,c-S)$,
and its termination after exactly four gates, for 36 parameter pairs. That
confirms Proposition 129 by a completely different route from its proof, and
it means the family's unbounded span buys no extra chain length at all.

## What was tried and did not work

A termination proof from the inequalities alone. The natural quantities all
stay consistent:

* $P_iP_{i+1}\gtrsim n/4$ with each $P_i\lesssim n/4$ reproduces Theorem 118's
  adjacent-gap bound and nothing stronger.
* $D_iD_{i+1}\gtrsim4n$ gives only $D_i\gtrsim2\sqrt n$, which is compatible
  with the observed regime.
* The gap budget $D_J\le J\log_2D_J-4J+D_0$ permits chains of length
  $O(n/\log n)$.

So the ceiling of five is arithmetic, not metric, and no inequality argument
can produce it. This is worth recording as a boundary: the remaining obstacle
in this branch is the same expanding-map-hits-small-target problem as the
conjecture itself, now compressed into a one-dimensional forced orbit.

The heuristic count in H7 quantifies that. Under an equidistribution model for
the successor residue the expected number of chains of length $J$ starting
beyond index $N$ becomes summable at $J=5$ and is $O(\log N/N^2)$ at $J=6$.
The model matches the observed data — a single minimal length-5 witness — but
it is an equidistribution assumption, which is exactly what the project does
not have.

## Status

Theorem 130's uniqueness half is machine-checked. `gate_exponent_unique` in
`lean/Conjecture.lean` proves that $D\le n$, $f\ge1$ and both window
inequalities at $h$ and at $h'$ force $h=h'$, with an axiom audit confirming no
`sorryAx`. The safe-map interpretation around it is not formalized.

The chain ceiling is a finite computation. It is stated as such in K15 and is
not a theorem. What it does settle is that the fixed-ladder frontier no longer
has an unexplored combinatorial dimension: there is one orbit per starting
state, the orbits are cheap to follow, and every one of them so far dies by the
sixth gate.
