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

Then

\[
\boxed{G_{i+1}=G_i+r_i+1-k_i,}
\tag{143.1}
\]

and the safe path continues from block $i$'s return state to a next positive
block **if and only if**

\[
\boxed{\alpha_i\le G_{i+1}-4.}
\tag{143.2}
\]

### Proof

For (143.1), substitute $n_{i+1}=n_i+k_i+1+r_i$ and $U_{i+1}=U_i+k_i$ into the
definition: $n_{i+1}-2U_{i+1}=(n_i-2U_i)+r_i+1-k_i$.

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

## What this settles, and what it does not

It gives no descent, and none is claimed. The conditions above are jointly
satisfiable along an infinite chain: with $k_i=1$ and $r_i=c$ constant, (143.1)
gives $G_i=G_0+ci$ exactly, (144.2) is vacuous, (144.1) asks only
$f_i\le G_0+ci-3$, and the window in (144.3) has width $\sim ci$ against the
fixed modulus $2^{c+2}$, so it is eventually far wider than the modulus. Ruling
that regime out is a statement about the deterministic map, which chooses
$f_{i+1}$ with no freedom left. Necessary conditions a putative infinite orbit
can satisfy prove nothing about whether one runs.

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
