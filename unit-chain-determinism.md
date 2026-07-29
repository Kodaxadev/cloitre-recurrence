# The all-unit pure-upper mechanism is a deterministic map

## Scope

Lemma 128 showed that the pure-upper windows at a fixed returned residue are
disjoint. This note draws the structural consequence that was left implicit:
the *whole* all-unit pure-upper mechanism has no branching at all. Every gate
is forced, so a hypothetical infinite tail is the forward orbit of a single
state under one explicit partial map on three integers.

Two things follow. First, the wrap count drops out of the forced data
entirely, which makes the normalization of Lemma 116 *exact* for chain
lengths rather than merely digit-preserving. Second, the search for a long
tail becomes a finite deterministic computation whose cost is linear in the
index bound, not quadratic.

The results below are a reduction and an exhaustive finite computation. They
do not prove that the mechanism terminates.

## Notation

Throughout, a *unit state* is a triple $(n,U,f)$ of integers satisfying the
exact test of Lemma 117, with $D=n-2U$:

\[
n+3+f\equiv0\pmod4,
\qquad
1\le f,\qquad f\le D-3,\qquad 4f\le n+D+2.
\tag{130.0}
\]

For an integer $h\ge2$ write

\[
\begin{aligned}
\mathrm{P} &:\quad D\ge f+7, \\
\mathrm{L}_h &:\quad 2^hf\ge n+h+4, \\
\mathrm{M}_h &:\quad 2^hf\le n+h+3+2^{h+2}, \\
\mathrm{U}_h &:\quad 2^h(f+4)\le n+D+2h-2.
\end{aligned}
\tag{130.1}
\]

## Theorem 130 (no branching)

Let $(n,U,f)$ be a unit state. Then $D-3-f$ is even, and the block has an
outgoing pure-upper unit gate with zero-only gap $r=h-2$ if and only if
$\mathrm{P}$, $\mathrm{L}_h$, $\mathrm{M}_h$ and $\mathrm{U}_h$ all hold.

At most one integer $h\ge2$ satisfies $\mathrm{L}_h$ and $\mathrm{U}_h$
together, and the only candidate is

\[
\boxed{
h^\ast(n,f)=\min\{h\ge2:\ 2^hf\ge n+h+4\}.
}
\tag{130.2}
\]

Consequently the mechanism is the **deterministic partial map**

\[
\boxed{
T(n,U,f)=\bigl(n+h^\ast,\ U+1,\ 2^{h^\ast}f-n-h^\ast-3\bigr),
}
\tag{130.3}
\]

defined exactly when $\mathrm{P}$, $\mathrm{M}_{h^\ast}$ and
$\mathrm{U}_{h^\ast}$ hold, and its value is again a unit state. Every
hypothetical infinite all-unit pure-upper tail is the forward orbit of one
state under $T$; distinct tails share no state.

### Proof

By (130.0), $n+f\equiv1\pmod4$ is odd, so $n-f$ is odd and
$D-3-f=(n-f)-3-2U$ is even. Hence $d=(D-3-f)/2$ is an integer and
$\mathrm{P}$ is exactly $d\ge2$.

Corollary 114 with $h=r+2$ gives the returned residue of the next block,

\[
g=2^hf-n-h-3,
\tag{130.4}
\]

and Corollary 115 lists the pure-upper conditions as $d\ge2$,
$1\le g\le2^{r+4}$ and $D+r-3-g\ge2^{r+4}$. Since $2^{r+4}=2^{h+2}$ and
$r=h-2$, substituting (130.4) turns $g\ge1$ into $\mathrm{L}_h$, turns
$g\le2^{h+2}$ into $\mathrm{M}_h$, and turns the last inequality into

\[
2^hf-n-h-3\le D+h-5-2^{h+2},
\]

which rearranges to $\mathrm{U}_h$. This proves the characterization.

For the uniqueness, note first that $g$ is strictly increasing in $h$: raising
$h$ to $h+1$ adds $2^hf-1>0$. So $\mathrm{L}_h$ fails for $h<h^\ast$ and
holds for $h\ge h^\ast$, and $h^\ast$ is well defined because $2^hf$ grows
exponentially while $n+h+4$ grows linearly.

Now let $\mathrm{L}_h$ hold and let $h'>h$. Expanding
$2^{h+1}(f+4)=2\cdot2^hf+8\cdot2^h$ and applying $\mathrm{L}_h$,

\[
2^{h+1}(f+4)\ \ge\ 2n+2h+8+8\cdot2^h.
\tag{130.5}
\]

Because $f+4\ge1$, each further doubling adds at least $2$, so

\[
2^{h'}(f+4)\ \ge\ 2^{h+1}(f+4)+2(h'-h-1).
\tag{130.6}
\]

Combining (130.5) and (130.6),

\[
2^{h'}(f+4)\ \ge\ 2n+2h'+6+8\cdot2^h.
\]

If $\mathrm{U}_{h'}$ also held, then $2^{h'}(f+4)\le n+D+2h'-2$, so

\[
n+8+8\cdot2^h\le D,
\]

contradicting $D\le n$. Hence no $h'>h$ satisfies $\mathrm{U}_{h'}$, and only
$h=h^\ast$ can satisfy both windows.

Finally, the successor is a unit state. Its congruence is automatic:

\[
(n+h)+3+g=2^hf,
\tag{130.7}
\]

which is divisible by $4$ because $h\ge2$. Writing $D'=D+h-2$, condition
$\mathrm{U}_{h}$ with $\mathrm{L}_h$ gives $g\le D'-3-2^{h+2}\le D'-3$, and
$\mathrm{M}_h$ together with $\mathrm{U}_h$ gives $2g\le D'-3$, whence
$4g\le2D'-6\le n'+D'+2$. $\square$

The uniqueness half of Theorem 130 is machine-checked. The Lean theorems
`Conjecture.gate_exponent_unique` and its unit specialization
`Conjecture.unit_gate_exponent_unique` in `lean/Conjecture.lean` prove exactly
the statement "$D\le n$, $f\ge1$, and both windows at $h$ and at $h'$ imply
$h=h'$", with an axiom audit showing no `sorryAx`.

The uniqueness argument does not use the unit hypothesis at all. Theorem 133 in
[`general-gate-determinism.md`](general-gate-determinism.md) forces the gap of
a pure-upper gate at every block length. What the unit case adds is closure:
only for $k=1$ does the reduced data $(n,U,f)$ map into itself, which is what
makes (130.3) a self-contained map on three integers.

## Lemma 131 (the wrap count is inert)

Let $(n,U,f)$ be a unit state and let $\Lambda(n,U,f)\in\{0,1,\dots\}\cup
\{\infty\}$ be the number of successive pure-upper unit gates available from
it. Then:

1. $h^\ast$, the successor index $n+h^\ast$, the successor residue $g$, and
   the conditions $\mathrm{L}_h$, $\mathrm{M}_h$ depend only on $(n,f)$.
2. $\mathrm{P}$ and $\mathrm{U}_h$ are monotone in the wrap count: if they
   hold at $(n,U',f)$ and $U\le U'$, they hold at $(n,U,f)$.
3. Therefore the $(n_i,f_i)$ coordinates of the orbit do not depend on $U_0$
   at all, and

   \[
   \boxed{\Lambda(n,U,f)\ \le\ \Lambda(n,0,f)
   \qquad\text{for every }U\ge0.}
   \tag{131.1}
   \]

### Proof

Claim 1 is immediate from (130.2) and (130.4): neither expression mentions
$U$ or $D$. Claim 2 holds because lowering $U$ raises $D=n-2U$, and both
$\mathrm{P}$ and $\mathrm{U}_h$ are of the form "something $\le D$" up to
constants independent of $U$.

For claim 3, suppose the orbit of $(n,U,f)$ takes $j$ gates. By claim 1 the
orbit of $(n,0,f)$ has the same indices $n_i$, the same exponents $h_i$ and
the same residues $f_i$ for as long as it continues, while its wrap counts
are $U_i-U$. At each step $i<j$ the conditions $\mathrm{P}$ and
$\mathrm{U}_{h_i}$ held with the larger wrap count, so by claim 2 they hold
with the smaller one, and $\mathrm{M}_{h_i}$ is unchanged. Induction on $i$
gives $\Lambda(n,0,f)\ge j$. $\square$

This is strictly stronger than Lemma 116, which preserved digit words but did
not compare chain lengths. Its point is that a sweep over normalized states
$U=0$ is an **exhaustive** sweep over all wrap counts simultaneously.

## Corollary 132 (structure of the orbit graph)

1. **Thin predecessors.** A unit state $(n',U',f')$ has at most
   $v_2(n'+3+f')-1$ pure-upper unit predecessors, namely
   $\bigl(n'-h,\ U'-1,\ (n'+3+f')/2^h\bigr)$ for those $h\ge2$ with
   $2^h\mid n'+3+f'$. Hence the gate graph is a forest of in-trees, and the
   $T$-orbit through any state is unique in both directions up to branching
   of predecessors.
2. **Bounded repetition.** For fixed $(a,h)$, at most $2^{h+1}$ indices $i$
   on one chain have $(f_i,h_i)=(a,h)$.
3. **Counting.** At most $\lceil(n-3)/4\rceil$ chains start at index $n$, one
   for each admissible residue, and each is decided in
   $O(\Lambda\log n)$ integer operations.

### Proof

For 1, (130.7) says a predecessor with exponent $h$ has residue
$(n'+3+f')/2^h$, which must be a positive integer, and $h\ge2$; the count of
admissible $h$ is at most $v_2(n'+3+f')-1$.

For 2, if $i<j$ with $f_i=f_j=a$ and $h_i=h_j=h$, then (130.7) at both
indices gives $n_{i+1}+3+f_{i+1}=2^ha=n_{j+1}+3+f_{j+1}$, so

\[
f_{j+1}=f_{i+1}-(n_{j+1}-n_{i+1})\le f_{i+1}-2.
\tag{132.1}
\]

By $\mathrm{M}_h$ and $\mathrm{L}_h$ every such $f_{\bullet+1}$ lies in
$[1,2^{h+2}]$, so there are at most $2^{h+1}$ occurrences.

For 3, the residues admissible at index $n$ are the $f$ in $[1,n-3]$ in one
class modulo $4$, and Theorem 130 makes the continuation a deterministic
iteration whose per-step cost is dominated by computing $h^\ast\le\log_2n$.
$\square$

## Exhaustive computation

Condition $\mathrm{M}_h$ confines $f$ to at most four consecutive integers
once $(n,h)$ is fixed:

\[
\frac{n+h+4}{2^h}\ \le\ f\ \le\ \frac{n+h+3}{2^h}+4 .
\tag{132.2}
\]

So the set of unit states with at least one outgoing pure-upper gate is
enumerated in $O(N\log N)$ time up to index $N$, instead of the $O(N^2)$ cost
of scanning all residues. Combined with (131.1), a sweep at $U=0$ decides
every wrap count at once. The binary `search-framework/src/bin/unit_chain.rs`
does this; `independent/verify_unit_determinism.py` re-derives the same data
from a from-scratch safe-map implementation.

Least start index that supports a chain of a given length:

| gates | least start index $n$ | residue $f$ |
|-------|----------------------|-------------|
| 1 | 22 | 7 |
| 2 | 36 | 13 |
| 3 | 62 | 11 |
| 4 | 93 | 16 |
| 5 | 978 | 127 |
| 6 | none for $n\le5\times10^9$ | — |

The sweep to $n\le5\times10^9$ examined $136{,}410{,}065{,}917$ candidate
triples $(n,h,f)$ and iterated all $133{,}599{,}589{,}858$ of them that have an
outgoing gate. By Lemma 131 this covers every wrap count. Below $n\le20{,}000$
the same table was reproduced by the independent $O(N^2)$ residue scan, which
also agreed on the live-state count ($175{,}868$); the Python verifier
reproduces it from a from-scratch safe map to $n\le30{,}000$.

The length-$5$ record is exactly the K14 witness: the deterministic map
reproduces its gap word $(1,3,3,1,5)$ and all of its returned residues from
the single state $(n,U,f)=(978,11,127)$. The swept range also contains the
smallest Proposition 126 segment, whose first block sits at index
$n_0-3=3{,}340{,}530{,}083$, so that family is inside the exhaustive range too.

The explicit infinite family of Proposition 126 was re-derived independently
through $T$ in exact integer arithmetic for $a\in\{7,8,10,11\}$ and
$q\in\{4,16,28\}$. In every case the forced gap word is $(1,L,1,L)$ with
$L=S-5$, the residues are $(a,c,a,c-S)$, and the orbit stops after exactly
four gates. This confirms Proposition 129 by a route independent of its
proof, and shows the family is *shorter* than the sporadic length-$5$
witness.

## Heuristic H7 (why length six should not exist)

At a unit state, $\mathrm{L}_{h^\ast}$ and the failure of
$\mathrm{L}_{h^\ast-1}$ force

\[
n+h^\ast+4\ \le\ 2^{h^\ast}f\ <\ 2n+2h^\ast+6,
\]

so the successor residue $g$ lies in an interval of length about $n$, while
$\mathrm{M}_{h^\ast}$ demands $g\le2^{h^\ast+2}\approx4n/f$. Modelling $g$ as
equidistributed in its interval and independent across steps gives survival
probability $\approx4/f$ per gate, with the next residue roughly uniform on
$[1,4n/f]$. Writing $Q_J(\phi)$ for the chance of $J$ further gates from
residue $\phi$ at index $n$, the model is

\[
Q_1(\phi)=\frac4\phi,
\qquad
Q_{J+1}(\phi)=\frac1n\sum_{\psi\le4n/\phi}Q_J(\psi).
\tag{132.3}
\]

Summing $Q_J$ over the $\approx n$ admissible residues gives the expected
number $E_J(n)$ of length-$J$ chains starting at index $n$:

| $J$ | $E_J(n)$ | $\sum_{n\le N}E_J(n)$ |
|-----|----------|------------------------|
| 1 | $4\log n$ | $\asymp N\log N$ |
| 2 | $O(1)$ | $\asymp N$ |
| 3 | $8\log^2n/n$ | $\asymp\log^3N$ |
| 4 | $O(1/n)$ | $O(\log N)$ |
| 5 | $O(\log n/n^2)$ | $O(1)$ |
| 6 | $O(1/n^3)$ | $O(1)$, tail beyond $N$ is $O(\log N/N^2)$ |

The model therefore predicts finitely many length-$5$ chains in total, which
matches the observed single minimal witness, and an expected number of
length-$6$ chains beyond the verified range of order $10^{-19}$. This is a
non-rigorous equidistribution model, exactly the assumption the project does
not have; it is recorded as a heuristic, not as evidence of a proof.

## Consequence and limitation

The fixed-ladder frontier changes shape. Before, a hypothetical infinite tail
had, at each block, a choice of outgoing gap constrained by inequalities;
the open problem was compatibility among the choices, expressed by the
cross-word equation (127.5). Theorem 130 removes the choice: the gap word is
a *function* of the initial state, the cross-word equation is automatically
satisfied along any orbit, and what remains is whether one particular
deterministic orbit avoids failure forever.

That is a genuine simplification and it makes the search complete and cheap.
It is not a termination proof. The forced map is expanding — one step
multiplies the residue by $2^{h^\ast}\ge4$ and subtracts a linear term — and
survival needs the image to land in a window of relative width $O(1/f)$. This
is the same expanding-map-hits-small-target obstruction identified in
`theorem-status.md` §E, now localized to a one-dimensional deterministic
orbit. No inequality argument can settle it: the constraints alone admit
chains of length $O(n/\log n)$, and the observed ceiling of five is
arithmetic, not metric.
