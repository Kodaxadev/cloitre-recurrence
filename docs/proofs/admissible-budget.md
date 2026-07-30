# The budget coordinate, and admissibility as a slack inequality

Companion to [`slack-coordinates.md`](slack-coordinates.md), which covers the
change of coordinates itself and the counting bounds that follow from it. That
note is about which slacks are arithmetically *possible*. This one is about
whether the path survives to use them, which is a different question and had
been living outside those coordinates. All notation is that of Theorem 137.

## Lemma 143 (admissibility is a slack inequality)

Theorem 138 made the wrap count passive but not absent. It accumulates by
$U_{i+1}=U_i+k_i$ and decides termination through the zero test, which is the
one part of the dynamics the coordinates of Lemma 140 do not see: everything in
Lemma 141 and Corollary 142 is a statement about arithmetic possibility, never
about survival. Put

\[
\boxed{G_i:=n_i-2U_i.}
\]

— the quantity Theorem 133 already carries as $D$, with

\[
G_{i+1}=G_i+r_i+1-k_i
\tag{143.1}
\]

being (133.1) restated. What is new is that the *survival* of the path is a
statement about $\alpha$ and $G$ alone: the safe path continues from block $i$'s
return state to a next positive block **if and only if**

\[
\boxed{\alpha_i\le G_{i+1}-4.}
\tag{143.2}
\]

### Proof

(143.1) is (133.1); substituting $n_{i+1}=n_i+k_i+1+r_i$ and $U_{i+1}=U_i+k_i$
into the definition gives $n_{i+1}-2U_{i+1}=(n_i-2U_i)+r_i+1-k_i$ directly.

For (143.2), start at the return state $(m_i,U_{i+1},f_i)$ and follow the safe
map. By Lemma 136 the candidate digits sit at indices $m_i+j$ for
$0\le j\le r_i$, the digit at $m_i+j$ having residue $2^jf_i$, and the wrap count
is $U_{i+1}$ throughout because no wrap occurs among them. That no wrap occurs
is forced:

* at $j=0$, because the parent block's wrap run stopped at the return state,
  which is exactly the failure $2f_i\le m_i+2$ of the wrap test there;
* at $1\le j\le r_i$, because the predicate of (136.1) fails at $r=j-1<r_i$,
  giving $2^{j+1}f_i\le m_i+j+2$, again the failure of the wrap test.

So at each of these indices the safe map either takes a zero digit or has no
move at all. The zero digit at $m_i+j$ needs $U_{i+1}+2^{j+1}f_i\le m_i+j$; write
$Z_j=m_i+j-U_{i+1}-2^{j+1}f_i$ for its slack. Then

\[
Z_{j+1}-Z_j=1-2^{j+1}f_i\le1-2f_i\le-1,
\]

so $Z$ is strictly decreasing, and $Z_0,\dots,Z_{r_i}$ are all nonnegative
precisely when $Z_{r_i}\ge0$. The whole gap therefore stands or falls on its
last test,

\[
U_{i+1}+2^{r_i+1}f_i\le n_{i+1},
\]

and by (140.1) $2^{r_i+1}f_i=\tfrac12(\alpha_i+n_{i+1}+4)$, so this reads
$2U_{i+1}+\alpha_i+n_{i+1}+4\le2n_{i+1}$, that is $\alpha_i\le G_{i+1}-4$.

If it holds, the zero digit at $n_{i+1}$ is taken, and the predicate of (136.1)
at $r_i$ gives $2^{r_i+2}f_i\ge n_{i+1}+4>n_{i+1}+3$, which is the wrap test at
index $n_{i+1}+1$: a positive block begins. If it fails, neither test passes at
that index and the safe map halts. $\square$

Equivalently $A_{i+1}\ge U_{i+1}+4$. So (143.2) is Lemma 53's zero-epoch bound
transported to the child and read in slack coordinates. The content is not a new
inequality; it is that this one is expressible in $(\alpha,G)$ at all.

## Corollary 144 (what the budget costs)

\[
\boxed{f_i\le G_i-3,}
\tag{144.1}
\]

with equality only when $k_i=1$;

\[
\boxed{k_i\ge2\ \Longrightarrow\ G_i\ge2U_i+11;}
\tag{144.2}
\]

and, at every gate the path survives,

\[
\boxed{n_{i+1}+4\ \le\ 2^{r_i+2}f_i\ \le\ n_{i+1}+G_{i+1}.}
\tag{144.3}
\]

### Proof

Block $i$ starts at a zero epoch, so its own zero test gives $A_i\ge U_i+4$.
Feeding that into (135.0),

\[
f_i=n_i+k_i+4-2^{k_i}A_i
\le G_i-\bigl(2^{k_i}-2\bigr)U_i+k_i+4-2^{k_i+2},
\]

using $n_i=G_i+2U_i$. The middle term is nonpositive because $k_i\ge1$, and
$k+4-2^{k+2}$ equals $-3$ at $k=1$ and decreases in $k$, its increment being
$1-2^{k+2}<0$. This is (144.1); equality needs both $(2^{k_i}-2)U_i=0$ and
$k_i+4-2^{k_i+2}=-3$, hence $k_i=1$.

For (144.2), $k_i\ge2$ means the predicate of (135.2) fails at $K=1$, that is
$4A_i\le n_i+5$; with $A_i\ge U_i+4$ this gives $n_i\ge4U_i+11$.

(144.3) is (143.2) together with $\alpha_i\ge0$, written through
$\alpha_i=2^{r_i+2}f_i-(n_{i+1}+4)$. $\square$

The three price different things against the same budget. (144.1) prices the
returned residue, with no reference to the index — a bound by $G$ alone, where
(140.5) could only offer $O(n)$. (144.2) prices block length: every block longer
than a single wrap needs $G_i\ge2U_i+11$, so on any chain where $G_i<2U_i+11$
throughout, **every** block has $k_i=1$ and the unit fibre of Theorem 130 is not
a special case but the only case. (144.3) says a surviving gate must
land a dyadic multiple inside a window whose width *is* the budget less four.

## Theorem 145 (a long chain needs a large budget)

Let a safe path carry $N\ge2$ consecutive positive blocks with descriptions
$(n_i,U_i,k_i,f_i)$ for $0\le i<N$, and put $C=\max_{i<N}G_i$. Then

\[
\boxed{N\le3C-13,}
\qquad\text{equivalently}\qquad
\max_{i<N}\bigl(n_i-2U_i\bigr)\ \ge\ \frac{N+13}{3}.
\tag{145.1}
\]

### Proof

Two standing facts. First $U_i\ge i$, because $U_i=U_0+\sum_{j<i}k_j$ with
$U_0\ge0$ and every $k_j\ge1$. Second $G_i\ge4$, because $f_i\ge1$ and (144.1).

*Long blocks happen early.* If $k_i\ge2$ then (144.2) gives
$C\ge G_i\ge2U_i+11\ge2i+11$, so $i\le\tfrac12(C-11)$. Hence $k_i=1$ for every
$i>\tfrac12(C-11)$.

*Zero gaps happen early.* Let $i\le N-2$, so that block $i+1$ exists. If $r_i=0$
then the predicate of (136.1) holds at $r=0$, that is $4f_i\ge n_{i+1}+4$. Now

\[
n_{i+1}=G_{i+1}+2U_{i+1}
=\bigl(G_i+r_i+1-k_i\bigr)+2\bigl(U_i+k_i\bigr)
=G_i+r_i+1+k_i+2U_i
\ \ge\ G_i+2i+2,
\]

using $r_i=0$, $k_i\ge1$ and $U_i\ge i$. With $f_i\le G_i-3$ from (144.1),

\[
4G_i-12\ \ge\ 4f_i\ \ge\ n_{i+1}+4\ \ge\ G_i+2i+6,
\qquad\text{so}\qquad
3G_i\ge2i+18 .
\tag{145.2}
\]

Hence $3C\ge2i+18$, and therefore $r_i\ge1$ for every $i$ with
$2i\ge3C-17$ and $i\le N-2$.

*The budget then climbs.* Since $C\ge4$ we have $3C-17\ge C-10$, so the gap
condition is the binding one. Let $i_0$ be least with $2i_0\ge3C-17$; then both
statements apply from $i_0$ on, and for $i_0\le i\le N-2$ we have $k_i=1$ and
$r_i\ge1$, whence by (143.1)

\[
G_{i+1}=G_i+r_i\ \ge\ G_i+1 .
\]

If $N-1\ge i_0$ this gives $C\ge G_{N-1}\ge G_{i_0}+(N-1-i_0)\ge N+3-i_0$, so
$N\le C-3+i_0$; and if $N-1<i_0$ then $N\le i_0$, which is weaker. For $C\ge6$,
$2i_0\le3C-16$ and the bound reads $2N\le5C-22$, which is at most $6C-26$ since
$C\ge4$, so $N\le3C-13$. For $C\le5$ we have $i_0=0$ and $N\le C-3$: at $C=5$
that is $N\le2=3C-13$, and at $C=4$ it is $N\le1$, contradicting $N\ge2$. So
$N\ge2$ already forces $C\ge5$, and (145.1) holds in every case. $\square$

**A refinement, and why it is not the headline.** The proof above actually
delivers $2N+22\le5C$ whenever $C\ge6$, which beats (145.1) once $C\ge15$ and
loses to it below that; and at $C=5$ it is false outright, since it would give
$N\le1$ where $N\le2$ is what the argument yields. A statement needing that case
split is worse than the clean uniform one, so (145.1) is what is claimed. The
sharper intermediate step (145.2) is worth having on its own account: it says a
zero gap at block $i$ requires budget at least $(2i+18)/3$. Together with
(144.2), *both* $r_i=0$ and $k_i\ge2$ demand a budget linear in the block index,
which is the real mechanism here — past a linear threshold every step is forced
to be a single wrap with a positive gap, and then the budget can only climb.

## Corollary 146 (the dichotomy an infinite chain faces)

An infinite chain of positive blocks has $G_i\to\infty$, and

\[
\boxed{
\text{either } k_i=1 \text{ for all large } i,
\quad\text{or}\quad
G_i\ge2i+11 \text{ infinitely often.}
}
\tag{146.1}
\]

### Proof

$G_i\to\infty$: if $G_i\le C$ for all $i$ then every finite prefix is a chain of
the kind Theorem 145 bounds, so $N\le3C-13$ for every $N$, which is false.

For (146.1), suppose $k_i\ge2$ for infinitely many $i$. Each such $i$ has
$G_i\ge2U_i+11\ge2i+11$ by (144.2). $\square$

So an infinite chain either has an eventually all-unit tail — the fibre Theorem
130 already treats as a three-integer map — or its budget grows at least
linearly, which by (144.1) forces the returned residues to grow with it. The two
branches are not symmetric, and the first is the one with existing machinery.

## Corollary 147 (on the unit fibre there is only one inequality)

If block $i+1$ is a single wrap, $k_{i+1}=1$, then

\[
\boxed{f_{i+1}=\alpha_i+1.}
\tag{147.1}
\]

Consequently, along an all-unit chain the survival condition (143.2) and the
residue cap (144.1) are the *same* inequality read at successive indices, and the
chain is the orbit of

\[
\boxed{
f_{i+1}=2^{r_i+2}f_i-n_{i+1}-3,
\qquad
n_{i+1}=n_i+2+r_i,
\qquad
G_{i+1}=G_i+r_i,
}
\tag{147.2}
\]

in which $r_i$ is the least gap making $f_{i+1}\ge1$ and admissibility is exactly
$f_{i+1}\le G_{i+1}-3$.

### Proof

By (140.2), $2A_{i+1}=n_{i+1}+4-\alpha_i$. With $k_{i+1}=1$, (135.0) reads
$f_{i+1}=n_{i+1}+5-2A_{i+1}$, which is $\alpha_i+1$. Then (143.2) says
$f_{i+1}-1\le G_{i+1}-4$, that is $f_{i+1}\le G_{i+1}-3$, which is (144.1) at
$i+1$. The recursion is (137.2) at $k'=1$ with (143.1) at $k_i=1$; minimality of
$r_i$ is (136.1), and $\alpha_i\ge0$ is $f_{i+1}\ge1$. $\square$

So the unit fibre carries no independent admissibility test at all. Every
constraint on it is one cap, $f_i\le G_i-3$, applied once per block — which is
why Corollary 146's first branch is the tractable-looking one, and also why it
has resisted: (147.2) is a one-dimensional expanding recursion required to land
in a window that moves.

**How the window moves.** The surviving gate needs $2^{r_i+2}f_i$ inside
$[n_{i+1}+4,\ n_{i+1}+G_{i+1}]$ by (144.3), so the relevant quantity is the
window's width relative to the index, $G/n$. Along a unit chain that ratio
increases exactly when

\[
\boxed{r_iU_i>G_i,}
\tag{147.3}
\]

since $G_{i+1}n_i>G_in_{i+1}$ unwinds to $r_i(n_i-G_i)>2G_i$ and $n_i-G_i=2U_i$.
The threshold is $r_i\approx G_i/U_i$, and $G_{i+1}-G_i=r_i$ — so the gap needed
to stop the target shrinking is the same gap that widens the budget, and the
regime $G_i\sim ci$ with $r_i\sim c$ sits exactly on the boundary. That is the
obstruction of Theorem 137 in its sharpest available form: not an inequality
that fails, but one that holds with nothing to spare.

## What this settles, and what it does not

Theorem 145 is a bound on chain length, and it is the first: Theorem 137 closed
the mechanism into one orbit but, as recorded there, did not bound it. It is
still not a termination proof, and the gap is precise. $C$ is measured along the
chain, not read off its start, and nothing here bounds $C$ in terms of
$(n_0,U_0)$ — the growth $G_{i+1}-G_i=r_i+1-k_i$ is capped only by
$2^{r_i+2}\le n_{i+1}+G_{i+1}$, which permits $r_i$ of order $\log n$. So (145.1)
says a long chain must spend budget, not that the budget runs out.

Nor do the conditions of Corollary 144 rule out an infinite chain on their own.
With $k_i=1$ and $r_i=c$ constant, (143.1) gives $G_i=G_0+ci$ exactly, (144.2) is
vacuous, (144.1) asks only $f_i\le G_0+ci-3$, and the window in (144.3) has width
$\sim ci$ against the fixed modulus $2^{c+2}$, so it is eventually far wider than
the modulus. Excluding that regime is a statement about the deterministic map,
which chooses $f_{i+1}$ with no freedom left; necessary conditions a putative
orbit can satisfy prove nothing about whether one runs. Consistent with this,
(145.1) is loose where it can be measured: over every chain with start index
$n\le200$ the largest $N/(3C-13)$ observed is $0.25$, at the shortest chains,
and long chains sit below $0.1$.

What it does settle is where the wrap count lives. Before, the admissible
dynamics was Theorem 138's base map plus an accumulator $U_i=U_0+\sum_{j<i}k_j$
carrying a test applied from outside. Now it is a map on $(n,k,f,G)$ in which
$G$ obeys the linear recurrence (143.1), driven by data the base map already
produces, and survival is the single inequality (143.2) between the gap slack
and the budget. Corollary 139's reduction to $U_0=0$ becomes the statement that
$G_0$ is taken as large as the initial pair allows.

It also redirects where a descent could come from. Corollary 142 showed the
$\beta$ side can never be forced and the $\alpha$ side only at $f_i\le2$. (143.2)
says the $\alpha$ side is where survival is decided as well, so both the
arithmetic rigidity and the dynamical constraint now sit on the same slack.

## Verification

`independent/verify_admissible_slack.py` checks all of the above against literal
safe-map traces. The equivalence is the point, so each gate is decided twice —
once by (143.2), once by stepping the raw safe map forward from the return state
until it wraps or dies. A one-directional check would have been satisfied by any
sufficient condition and would not have been evidence.

At index bound $200$ that is $132{,}975$ gates, of which $122{,}180$ continue and
$10{,}795$ die, with no disagreement in either direction. Where the path
continues, the index at which its leading zero was taken is checked against the
$n_{i+1}$ predicted by (136.1), so the $\alpha_i$ tested is the child's rather
than a fiction. (143.1), (144.1), (144.2) and (144.3) are checked on the same
gates; $56{,}357$ blocks have $k_i\ge2$, and equality in (144.1) is rare, one
case in range.

Corollary 147 needs consecutive pairs rather than single blocks, so it is checked
separately: (147.1) on all $66{,}822$ single-wrap children, together with the
collapse it produces — that (143.2) at the parent and (144.1) at the child are
then the same condition — and (147.3) on all $66{,}929$ unit parents,
cross-multiplied so the ratio comparison stays in integers.

Theorem 145 is checked over every chain of two or more blocks in the same range,
together with the two facts its proof leans on that are not inequalities being
tested elsewhere: $G_i\ge4$ at every block, and $C\ge5$ whenever $N\ge2$. The
tightest ratio and the longest chain are reported rather than only asserted,
because a bound that is never approached should say so.
