# The pure-upper gap never branches, at any block length

## Scope

Theorem 130 in [`unit-chain-determinism.md`](unit-chain-determinism.md) forces
the outgoing gap of a pure-upper *unit* gate. The argument turns out not to use
the unit hypothesis: it needs only the two gap-dependent pure-upper
inequalities and $D\le n$. This note states and proves the general version.

The consequence is that the surviving arbitrary-length branch left open by
Corollary 102 also has no gap-word freedom. It is not a termination result.

## Theorem 133 (forced pure-upper gap)

Let a positive block of length $k\ge1$ start at $(n,U,e)$ with $D=n-2U$ and
parent defect $d=n-U-2e$, return to a zero epoch with residue $f\ge1$, and be
followed by $r\ge0$ zero-only blocks. Then

\[
m=n+k+1,\qquad
n'=m+r,\qquad
U'=U+k,\qquad
D'=D+r+1-k,
\tag{133.1}
\]

the canonical spacing is $H=2^{k+r+3}$, and the child excess is
$x=2^{r+2}f-m-r-3$. The gate is pure-upper exactly when $d\ge2$,
$1\le x\le H$ and $D'-3-x\ge H$. Writing $h=r+2$, the conditions $x\ge1$ and
$D'-3-x\ge H$ are the two windows

\[
n+k+h+3\le2^hf,
\qquad
2^h\bigl(f+2^{k+1}\bigr)+2\le n+D+2h,
\tag{133.2}
\]

and **at most one $h$ satisfies both**. The remaining condition $d\ge2$ does
not involve $r$, so the outgoing gap of a pure-upper gate is forced at every
block length:

\[
\boxed{r^\ast=\min\{r\ge0:\ 2^{r+2}f\ge n+k+r+5\}.}
\tag{133.3}
\]

### Proof

The block spends one zero digit and $k$ wraps, so it returns at index $n+k+1$
with wrap count $U+k$. The $r$ zero-only blocks advance the index by $r$ and
leave the wrap count alone, so $n'=n+k+1+r$ and

\[
D'=n'-2U'=(n+k+1+r)-2U-2k=D+r+1-k,
\]

which is (133.1). Corollary 84 gives $H=2^{k+r+3}$, and Lemma 103 gives
$D'-3=x+2d'$, so the upper mechanism $2d'\ge H$ is $D'-3-x\ge H$.

Substituting (133.1),

\[
(D+r+1-k)-3-\bigl(2^{r+2}f-(n+k+1)-r-3\bigr)\ge2^{k+r+3},
\]

which rearranges to $2^{r+2}\bigl(f+2^{k+1}\bigr)\le n+D+2r+2$, the second
window of (133.2) with $h=r+2$. The first window is $x\ge1$ rewritten.

For uniqueness, let the first window hold at $h$ and let $h'>h$. Because
$f+2^{k+1}\ge1$, each doubling adds at least $2$, so

\[
2^{h'}\bigl(f+2^{k+1}\bigr)\ \ge\ 2^{h+1}\bigl(f+2^{k+1}\bigr)+2(h'-h-1),
\]

while the first window gives
$2^{h+1}\bigl(f+2^{k+1}\bigr)\ge2\cdot2^hf\ge2(n+k+h+3)$. Combining the two,

\[
2^{h'}\bigl(f+2^{k+1}\bigr)+2\ \ge\ 2n+2k+2h'+6\ >\ n+D+2h',
\]

since $D\le n$. So the second window fails at every $h'>h$, and monotonicity of
$2^hf-n-h$ in $h$ makes the first window fail below $r^\ast+2$. $\square$

Theorem 130 is the case $k=1$, where $2^{k+1}=4$ and (133.2) reads
$n+h+4\le2^hf$ and $2^h(f+4)+2\le n+D+2h$.

**Exact formalization boundary.** The Lean theorem
`Conjecture.gate_exponent_unique` machine-checks one statement and no more: that
the two inequalities of (133.2) at $h$ and at $h'$, together with $D\le n$ and
$f\ge1$, force $h=h'$. `Conjecture.unit_gate_exponent_unique` is its $k=1$
specialization. Both pass the axiom audit with no `sorryAx`.

Everything else in Theorem 133 is manuscript mathematics supported by
computational checks, not formalized: the safe-map coordinates (133.1), the
identification of the pure-upper conditions with (133.2), the closed form
(133.3) for $r^\ast$, and the interpretation of the whole as a statement about
safe-map gates. In particular the Lean theorem knows nothing about the safe map;
it is a fact about two inequalities over the naturals.

## Verification

`independent/verify_general_gate_determinism.py` reads adjacent positive-block
pairs off literal safe-map traces produced by a from-scratch implementation and
checks, for each one:

* the coordinates (133.1), including $m=n+k+1$, $U'=U+k$, $n'=m+r$ and
  $D'=D+r+1-k$;
* Lemma 103's identity $D'-3=x+2d'$ against the literal child defect;
* that the reduced pure-upper test agrees with the literal excess and child
  defect whenever it fires, and that (133.2) then holds;
* that scanning all gaps $0\le r<60$ finds at most one admissible gap.

At index and residue bound $400$ this covers $345{,}785$ adjacent-block
coordinates and $53{,}201$ literal pure-upper gates, with no parent state
admitting two gaps.

## Corollary 134 (the residue window has width exactly $2^{k+1}$)

At a pure-upper gate in the notation of Theorem 133, the parent's returned
residue is confined to

\[
\boxed{
\frac{m+r+3}{2^{r+2}}\ <\ f\ \le\ 2^{k+1}+\frac{m+r+3}{2^{r+2}}.
}
\tag{134.1}
\]

Hence for fixed $(n,k,r)$ at most $2^{k+1}$ integers $f$ are admissible.

### Proof

The condition $x\ge1$ is $2^{r+2}f>m+r+3$, the left inequality. The canonical
translate condition $x\le H=2^{k+r+3}$ is

\[
2^{r+2}f-m-r-3\le2^{k+r+3},
\]

that is $2^{r+2}\bigl(f-2^{k+1}\bigr)\le m+r+3$, the right inequality.
$\square$

This is the exact quantitative form of the difference between the unit and
general cases. At $k=1$ the window admits at most four integers, which after the
congruence modulo $4$ leaves essentially one — the rigidity behind (132.2) and
Theorem 130. Each extra unit of block length doubles the room. The trade is not
free: Corollary 112 caps $k_i+r_i+k_{i+1}$ near $\log_2n$, so a long parent
block buys residue freedom only by forcing a short gap and a short child block.

Checked on $40{,}322$ literal pure-upper gates from raw traces with
$n\le260$, the figure reported by `verify_pure_upper_run.py` in CI, where the
observed widths are exactly $4,8,16,32$ for $k=1,2,3,4$.

### Why the general ceiling exceeds the unit ceiling

The unit ceiling of five (K15) comes from a two-step *product* bound. For a
unit child, Lemma 113 makes the excess and the child's returned residue the
same number, $g=x$. Combined with the canonical translate condition
$x\le2^{r+4}$ and with $2^{r_i+2}f_i\approx n$, that gives

\[
2^{r_i+2}\cdot2^{r_{i+1}+2}\ \gtrsim\ n/4,
\]

which is Theorem 118. It pins every gap near $\tfrac12\log_2n$ and makes the
unit system critically tight at every step.

For a child block of length $\ell\ge2$ the coincidence fails. Lemma 113 gives

\[
g=n'+\ell+4-2^{\ell-1}(n'+5-x),
\]

so the returned residue is not the excess, the recursion does not close in
$(n,U,f)$, and the two-step product bound does not survive. What remains is the
one-sided ceiling of Corollary 112,

\[
2^{k_i+r_i+k_{i+1}+2}\ \le\ n_{i+1}+k_{i+1}+3,
\tag{134.2}
\]

an upper bound on how fast consecutive parameters may grow rather than a lower
bound forcing them to be large. (Directly: the upper mechanism gives
$d'\ge2^{k_i+r_i+2}$, so $A'\ge2^{k_i+r_i+2}$, and Lemma 83 applied to the child
block of length $\ell=k_{i+1}$ needs $2^\ell A'\le n'+\ell+3$ for its returned
residue to stay positive.) That is the extra room, and it is consistent
with the observed ceiling rising from five to six.

## Exhaustive computation: the length of a pure-upper run

Because Theorem 133 leaves no gap-word freedom, the only remaining question
about the mechanism is how many pure-upper gates can occur in a row. That is a
finite computation at each index. As in Lemma 131 the wrap count can be
normalized away, this time by Lemma 116 directly: lowering $U_0$ preserves the
digit word and raises both gate defects, while the canonical translate $x$
depends only on indices and residues. So a pure-upper run can only lengthen
when $U_0$ falls, and sweeping $U_0=0$ decides every wrap count at once.

The record run over all normalized safe states with $n\le6{,}000$ is **six**,
first available at $(n,U,e)=(960,0,199)$ — and it is the K14 run, entered eleven
indices later. So R8 is sharp in the range checked: "pure-upper ambiguity is a
transient of length at most five" is false, and nothing longer than six occurs
either. Reading the six gates off the trace:

| $n$ | $U$ | $e$ | $k$ | $r$ | $f$ | $x$ | $d'$ |
|-----|-----|-----|-----|-----|-----|-----|------|
| 971 | 5 | 482 | 6 | 0 | 277 | 127 | 413 |
| 978 | 11 | 277 | 1 | 1 | 127 | 32 | 461 |
| 981 | 12 | 254 | 1 | 3 | 32 | 35 | 461 |
| 986 | 13 | 256 | 1 | 3 | 35 | 126 | 417 |
| 991 | 14 | 280 | 1 | 1 | 126 | 11 | 475 |
| 994 | 15 | 252 | 1 | 5 | 11 | 404 | 281 |

This matches the K14 table in `gate-transfer-analysis.md` row for row, including
its defect pairs, and confirms the shape recorded there: six consecutive
pure-upper gates, the first from a block of length six and the remaining five
from unit blocks. The unit sub-chain of five is exactly the K15 record, and the
K14 state $(971,5,482)$ gives six both literally and after normalization.

Two implementations agree: `search-framework/src/bin/pure_upper_run.rs` over the
project's `safe_step`, and a from-scratch block decomposition in Python, which
match on the record, the witness, the K14 state and this table.

## Consequence and limitation

Corollary 102 leaves two surviving alternatives for a hypothetical infinite
safe path: infinitely many nonunique gates, or infinitely many unique gates in
the child boundary layer. Both permit blocks of arbitrary length. Theorem 133
says that wherever the pure-upper mechanism is active in those branches, the
gap is not a free parameter, so no analysis of them needs to enumerate gap
words.

The limitation is sharper than for the unit case. For $k\ge2$ the child start
residue is $e'=2^rf$, so the child *state* is determined, but recovering the
next pair $(k',f')$ requires the child's own block length. The reduced data
therefore does not close into a map on a fixed number of integers, which is
exactly what Theorem 130 gains from the unit hypothesis. And, as in the unit
case, forcing the gap is a removal of search freedom, not a termination
argument.

## The frontier after Theorem 133

The open problem in this branch is no longer gap enumeration. With the gaps
forced, what is unconstrained is the joint sequence

\[
(k_0,f_0),\ (k_1,f_1),\ (k_2,f_2),\ \dots
\]

of block lengths and returned residues. Corollary 134 says each $f_i$ ranges
over an interval of length $2^{k_i+1}$, and (134.2) says the block lengths and
the forced gap trade against one another inside a $\log_2n$ budget. Those are
one-step constraints; neither pins the sequence.

**Target.** A multi-step obstruction that replaces the closed recurrence the
unit case had. Concretely, Theorem 130 worked because Lemma 113 collapses excess
and child residue at $\ell=1$, giving $f_{i+1}=2^{h_i}f_i-n_{i+1}-3$ and hence
both the telescoping identity and Theorem 118's two-step product bound. For
$\ell\ge2$ that recurrence is lost. What is needed is an identity over two or
more gates that survives the intervening block length — for instance an exact
relation among $f_i,f_{i+2}$ and $k_{i+1}$ analogous to Lemma 119's
three-residue compatibility, from which a descent or a modulus can be
accumulated. Until such a relation exists, the branch has exact one-step
arithmetic and no chain argument, which is precisely the state the unit case was
in before Lemma 119.
