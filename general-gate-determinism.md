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
$n+h+4\le2^hf$ and $2^h(f+4)+2\le n+D+2h$. The Lean theorem
`Conjecture.gate_exponent_unique` proves the uniqueness in the general form of
(133.2); `Conjecture.unit_gate_exponent_unique` is the specialization used for
Theorem 130. Both pass the axiom audit with no `sorryAx`.

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
