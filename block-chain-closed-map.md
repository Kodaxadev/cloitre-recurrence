# The adjacent-block chain is a closed deterministic map

## Scope

Theorem 130 made the all-unit pure-upper mechanism a deterministic map on three
integers. Theorem 133 forced the gap at every block length but left the next
block length as an extra datum, so the general mechanism appeared not to close.
That appearance was wrong.

This note gives closed forms for both remaining data — the zero-only gap and the
next block length — and assembles them into one deterministic map on four
integers. The map is exact for *every* adjacent-positive-block gate, not only
pure-upper ones, and it needs no digit simulation.

Throughout, a **block description** is a tuple $(n,U,k,f)$: a positive block of
length $k$ starting at the safe state with index $n$ and wrap count $U$, which
returns to a zero epoch with residue $f$. Its return index is $m=n+k+1$, being
one zero digit plus $k$ wraps. Recall Lemma 83: with $A=n+4-2e$,

\[
f=n+k+4-2^kA.
\tag{135.0}
\]

## Lemma 135 (the intermediate residues, and the forced block length)

Let a block start at $(n,U,e)$ with $A=n+4-2e\ge1$. After its leading zero digit
and $j\ge1$ wraps, the state has index $n+1+j$ and residue

\[
\boxed{\varphi_j=n+j+4-2^jA.}
\tag{135.1}
\]

The wrap run stops after exactly

\[
\boxed{k=\min\{K\ge1:\ 2^{K+1}A\ge n+K+5\}}
\tag{135.2}
\]

wraps, and the set of $K$ satisfying the inequality in (135.2) is upward closed,
so the minimum is well defined. The block's returned residue is
$f=\varphi_k$, which is (135.0).

### Proof

For $j=1$ the leading zero gives index $n+1$ and residue $2e$, and the first
wrap gives index $n+2$ and residue $4e-n-3$, which is
$n+5-2A=\varphi_1$. Inductively, a wrap at index $n+j$ with residue
$\varphi_{j-1}$ produces index $n+j+1$ and residue
$2\varphi_{j-1}-(n+j+1)$; substituting (135.1) at $j-1$ gives

\[
2\bigl(n+j+3-2^{j-1}A\bigr)-(n+j+1)=n+j+5-2^jA,
\]

which is $\varphi_j$ after reindexing. This proves (135.1).

At index $n+1+j$ with residue $\varphi_j$, the next digit is another wrap
exactly when $2\varphi_j>(n+1+j)+2$. So the run stops after $K$ wraps exactly
when

\[
2\bigl(n+K+4-2^KA\bigr)\le n+K+3,
\]

that is $2^{K+1}A\ge n+K+5$. Since $A\ge1$, raising $K$ by one increases the
left side by $2^{K+1}A\ge2$ and the right side by $1$, so the inequality is
upward closed in $K$ and the run stops at the least such $K$. $\square$

At a zero-epoch start the zero test gives $2e\le n-U\le n$, hence $A\ge4$, so
the hypothesis $A\ge1$ is automatic.

## Lemma 136 (the forced gap, at every gate)

Let a block description $(n,U,k,f)$ be followed on the safe path by another
positive block. Then the number of intervening zero-only blocks is

\[
\boxed{r=\min\{r\ge0:\ 2^{r+2}f\ge m+r+4\},\qquad m=n+k+1,}
\tag{136.1}
\]

and the predicate in (136.1) is upward closed in $r$. The next positive block
starts at

\[
\boxed{n'=m+r,\qquad U'=U+k,\qquad e'=2^rf.}
\tag{136.2}
\]

### Proof

At the return state, index $m$ and residue $f$. The next block begins there: its
leading zero gives index $m+1$ and residue $2f$, and it is a *positive* block
exactly when a wrap follows, that is $2(2f)>(m+1)+2$, i.e. $4f\ge m+4$. This is
the inequality of (136.1) at $r=0$.

If instead $4f\le m+3$, no wrap occurs, so that block is zero-only and returns
at index $m+1$ with residue $2f$. Replacing $(m,f)$ by $(m+1,2f)$ and repeating
shows that the block reached after $j$ zero-only blocks is positive exactly when
$2^{j+2}f\ge m+j+4$. Hence the number of zero-only blocks is the least such $j$,
which is (136.1), and (136.2) records the resulting start data.

Upward closure holds because raising $r$ by one doubles the left side, adding
$2^{r+2}f\ge4$, while the right side gains $1$. $\square$

Lemma 136 is unconditional: it does not assume the gate is pure-upper. So the
gap $r^\ast$ of Theorem 133 is not merely the unique gap *compatible with the
pure-upper windows* — it is the gap the dynamics always take. Theorem 133 is the
static counterpart: the two window inequalities alone already single it out.

## Theorem 137 (closed deterministic map on four integers)

Define, for a block description $(n,U,k,f)$ with $m=n+k+1$,

\[
\boxed{
\begin{aligned}
r&=\min\{r\ge0:\ 2^{r+2}f\ge m+r+4\},\\
n'&=m+r,\qquad U'=U+k,\\
A'&=n'+4-2^{r+1}f,\\
k'&=\min\{K\ge1:\ 2^{K+1}A'\ge n'+K+5\},\\
f'&=n'+k'+4-2^{k'}A',
\end{aligned}
}
\tag{137.1}
\]

and put $\Psi(n,U,k,f)=(n',U',k',f')$. If the safe path continues from
$(n,U,k,f)$ to another returning positive block, that block's description is
exactly $\Psi(n,U,k,f)$.

Equivalently, the returned residues obey the closed two-step recurrence

\[
\boxed{
f'=2^{k'+r+1}f-\bigl(2^{k'}-1\bigr)(n'+4)+k'.
}
\tag{137.2}
\]

Hence the whole adjacent-positive-block mechanism — pure-upper or not, any block
lengths — is a deterministic orbit in four integers, computed without simulating
a single digit.

### Proof

Lemma 136 gives $r$, $n'$, $U'$ and $e'=2^rf$, hence
$A'=n'+4-2e'=n'+4-2^{r+1}f$. Lemma 135 applied to the child block gives $k'$
and $f'=n'+k'+4-2^{k'}A'$. Substituting $A'$ into the last expression,

\[
f'=n'+k'+4-2^{k'}\bigl(n'+4-2^{r+1}f\bigr)
 =2^{k'+r+1}f-\bigl(2^{k'}-1\bigr)(n'+4)+k',
\]

which is (137.2). $\square$

Setting $k=k'=1$ recovers Theorem 130: then $m=n+2$, (136.1) reads
$2^{r+2}f\ge n+r+6$, and (137.2) collapses to
$f'=2^{r+2}f-n'-3$, which is (130.7). So Theorem 130 is the unit fibre of
Theorem 137, and its extra strength was never closure — it was that the unit
fibre is invariant, so three integers suffice there.

The upward-closure steps in Lemmas 135 and 136 are the same doubling-dominates-
drift fact already machine-checked as `pow_dominates_linear`; the Lean theorem
`Conjecture.gap_predicate_upward_closed` states the (136.1) instance directly.
Everything else here is manuscript mathematics with computational checks: the
safe-map coordinates, the block conventions, and the identification of $\Psi$
with the dynamics are not formalized.

## Theorem 138 (triangular skew product over a three-integer base)

Let $\pi(n,U,k,f)=(n,k,f)$, and let $\widehat\Psi(n,k,f)=(n',k',f')$ be given by
(137.1) with the line for $U'$ deleted. Then

\[
\boxed{
\pi\circ\Psi=\widehat\Psi\circ\pi,
\qquad
U'=U+k,
}
\tag{138.1}
\]

so $\Psi$ is a triangular skew product over $\widehat\Psi$ in which the wrap
count is a passive accumulator:

\[
\boxed{U_i=U_0+\sum_{j<i}k_j.}
\tag{138.2}
\]

### Proof

Inspect (137.1): none of $r$, $n'$, $A'$, $k'$, $f'$ mentions $U$. The only
occurrence of $U$ in the whole map is the line $U'=U+k$. $\square$

**Where $U$ is still needed.** The wrap count is not removable from the problem,
only from the arithmetic. In the safe map, $U$ occurs exactly once — in the zero
test $U+2e\le n$ — and nowhere in the wrap test $2e>n+2$. So $U$ does not
influence any digit choice; it decides only whether a step is possible at all,
that is, termination. The admissible dynamics therefore remain
four-dimensional, but the fourth coordinate is a functional of the base orbit
through (138.2), not an independent variable.

## Corollary 139 (the $U=0$ reduction, at every block length)

For fixed $(n,e)$, lowering the wrap count leaves every wrap/zero choice
unchanged wherever the original path continues, and can only postpone
termination. Consequently the digit word at wrap count $U$ is a **prefix** of the
digit word at wrap count $0$, the number of successive returning positive blocks
is nonincreasing in $U$, and

\[
\boxed{
\begin{gathered}
\text{an infinite admissible orbit exists}\\
\Longleftrightarrow\quad
\text{one exists with } U_0=0.
\end{gathered}
}
\tag{139.1}
\]

### Proof

By the previous remark the wrap test is $U$-free, so a wrap taken at $(n,U,e)$ is
taken at $(n,U'',e)$ for every $U''\le U$; and the zero test $U+2e\le n$ only
becomes easier as $U$ falls. Induction on the digits gives the prefix property,
which is Lemma 116. Each additional digit can only add blocks, giving the
monotonicity.

For (139.1), the right-to-left direction is trivial. For left-to-right, take any
infinite admissible orbit from $(n_0,U_0,e_0)$; the prefix property makes the
orbit from $(n_0,0,e_0)$ infinite as well. $\square$

So the whole eventually-no-down search reduces to the three-variable base
dynamics $\widehat\Psi$ started from $U_0=0$, with the accumulator
$U_i=\sum_{j<i}k_j$ supplying the admissibility test. Corollary 139 is the
arbitrary-length generalization of Lemma 131, which proved the same reduction
for the unit fibre only.

## Lemma 140 (threshold-slack coordinates)

The two minima in (137.1) are thresholds, so it is natural to record how far each
is exceeded. Put

\[
\boxed{
\alpha_i=2^{r_i+2}f_i-(n_{i+1}+4),
\qquad
\beta_{i+1}=2^{k_{i+1}+1}A_{i+1}-(n_{i+1}+k_{i+1}+5).
}
\tag{140.1}
\]

Then the map inverts to

\[
\boxed{
2A_{i+1}=n_{i+1}+4-\alpha_i,
\qquad
2f_{i+1}=n_{i+1}+k_{i+1}+3-\beta_{i+1},
}
\tag{140.2}
\]

the slacks satisfy the coupled recurrence

\[
\boxed{
\begin{aligned}
\beta_{i+1}&=2^{k_{i+1}}\bigl(n_{i+1}+4-\alpha_i\bigr)-(n_{i+1}+k_{i+1}+5),\\
\alpha_{i+1}&=2^{r_{i+1}+1}\bigl(n_{i+1}+k_{i+1}+3-\beta_{i+1}\bigr)-(n_{i+2}+4),
\end{aligned}
}
\tag{140.3}
\]

and they obey

\[
\alpha_i\ge0,
\qquad
\beta_{i+1}\ge0,
\tag{140.4}
\]

\[
\alpha_i\le n_{i+1}\ \ (r_i\ge1),
\qquad
\beta_{i+1}<n_{i+1}+k_{i+1}+3\ \ (k_{i+1}\ge2),
\tag{140.5}
\]

\[
\alpha_i\equiv n_{i+1}\ (2),
\qquad
\beta_{i+1}\equiv n_{i+1}+k_{i+1}+1\ (2),
\tag{140.6}
\]

\[
\boxed{
\alpha_i\equiv-(n_{i+1}+4)\ \bigl(2^{r_i+2}\bigr),
\qquad
\beta_{i+1}\equiv-(n_{i+1}+k_{i+1}+5)\ \bigl(2^{k_{i+1}+1}\bigr).
}
\tag{140.7}
\]

### Proof

(140.2) is (140.1) solved for $A_{i+1}$ and $f_{i+1}$ using
$A_{i+1}=n_{i+1}+4-2^{r_i+1}f_i$ and $f_{i+1}=n_{i+1}+k_{i+1}+4-2^{k_{i+1}}A_{i+1}$.
Substituting the first half of (140.2) into the definition of $\beta_{i+1}$ gives
the first line of (140.3), and substituting the second half into the definition
of $\alpha_{i+1}$ gives the second.

(140.4) is the defining inequality of each minimum. For (140.5), minimality at
$r_i\ge1$ says the inequality fails at $r_i-1$, i.e.
$2^{r_i+1}f_i\le n_{i+1}+2$, which with (140.2) is $\alpha_i\le n_{i+1}$;
minimality at $k_{i+1}\ge2$ says $2^{k_{i+1}}A_{i+1}\le n_{i+1}+k_{i+1}+3$,
which is the stated bound on $\beta_{i+1}$.

(140.6) is integrality of $A_{i+1}$ and $f_{i+1}$ read off (140.2). Finally
(140.7) is immediate from (140.1): $\alpha_i+n_{i+1}+4=2^{r_i+2}f_i$ and
$\beta_{i+1}+n_{i+1}+k_{i+1}+5=2^{k_{i+1}+1}A_{i+1}$. $\square$

The point of (140.7) is that the modulus **grows with the parameter it is
attached to**: a long gap forces a high-order congruence on $\alpha_i$, and a long
block forces one on $\beta_{i+1}$. Together with the two-sided bounds (140.4)
and (140.5) — which confine each slack to a window of width $O(n)$ — this is the
same tension as everywhere else in the project, but now written as two threshold
errors rather than as an expanding residue. It is the intended starting point for
a descent or growing-modulus argument, and it is a cleaner one than iterating
(137.2) directly, because the exponential factors appear only inside the
congruence moduli.

## Verification

`independent/verify_block_chain_map.py` reads block descriptions off literal
safe-map traces produced by a from-scratch implementation and checks four
things:

* the intermediate-residue formula (135.1) at every wrap of every block;
* the forced block length (135.2) against the literal wrap count, for both
  returning and terminating blocks;
* the forced gap (136.1) against the literal number of zero-only blocks, at
  every gate rather than only pure-upper ones;
* that **iterating** $\Psi$ from the first block description of a path
  reproduces every later description exactly;
* the semiconjugacy (138.1), by running the base map with no $U$ argument and
  checking $U'=U+k$ separately;
* Corollary 139's prefix property and block-count monotonicity, over every
  admissible raised wrap count;
* all of Lemma 140: the inversions (140.2), the coupled recurrence (140.3), the
  bounds (140.4)--(140.5), the parities (140.6), and the growing congruences
  (140.7).

At index bound $200$ this covers $132{,}975$ returning and $8{,}094$
terminating blocks, $114{,}777$ gates, and $114{,}777$ successive descriptions
reproduced by iteration over $16{,}732$ paths, with no mismatch. The semiconjugacy
and every slack relation are checked on the same $114{,}777$ gates, and
Corollary 139's prefix property on $109{,}373$ raised wrap counts, of which
$81{,}944$ give strictly fewer blocks. The block-length formula is checked on
terminating blocks too, so Lemma 135 needs no returning hypothesis.

## Consequence and limitation

The structural picture is now uniform. Every surviving branch of the safe-map
analysis — the fixed ladder, the arbitrary-length pure-upper branch, and the
nonunique gates of Corollary 102 — is one forward orbit of $\Psi$. There is no
gap word to enumerate, no block-length word to enumerate, and no digit
simulation. A hypothetical infinite safe path is an infinite $\Psi$-orbit.

What this does not do is bound the orbit. $\Psi$ is expanding: (137.2)
multiplies the residue by $2^{k'+r+1}\ge4$ and subtracts a term of size
$2^{k'}n'$, and survival requires the difference to land in the narrow admissible
band of Corollary 134. That is the same expanding-map-hits-small-target
obstruction as everywhere else in this project, now stated for a single
four-integer orbit rather than for a search over words.

The concrete gain is that a chain argument now has something to work with. The
unit case reached Lemma 119's three-residue compatibility and Theorem 118's
two-step product bound only because it had a closed recurrence; (137.2) is the
general closed recurrence, so the analogous two-step elimination is available in
principle. Carrying it out is the open problem.
