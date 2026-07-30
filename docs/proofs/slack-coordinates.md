# Threshold-slack coordinates for the block chain

Extracted from [`block-chain-closed-map.md`](block-chain-closed-map.md),
which proves the closed map itself. This note covers the change of
coordinates aimed at a descent argument, and what it does and does not buy.
All notation is that of Theorem 137.

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
same tension as everywhere else in the project, but now carried by two bounded
threshold errors rather than by an unbounded residue.

## Lemma 141 (how many slack values the congruence leaves)

Fix $n_{i+1}$ together with the relevant parameter, and count the integers in
each slack window that lie in the class required by (140.7).

For the gap slack with $r_i\ge1$, the count of $a\in[0,n_{i+1}]$ with
$a\equiv-(n_{i+1}+4)\pmod{2^{r_i+2}}$ satisfies

\[
\boxed{1\le\#\{a\}\le f_i.}
\tag{141.1}
\]

For the block slack with $k_{i+1}\ge2$, the count of
$b\in[0,n_{i+1}+k_{i+1}+2]$ with
$b\equiv-(n_{i+1}+k_{i+1}+5)\pmod{2^{k_{i+1}+1}}$ satisfies

\[
\boxed{2\le\#\{b\}\le A_{i+1}.}
\tag{141.2}
\]

### Proof

A residue class modulo $M$ meets an interval of $W$ consecutive integers in at
most $\lceil W/M\rceil$ points. For (141.1), $W=n_{i+1}+1$ and
$M=2^{r_i+2}\ge(n_{i+1}+4)/f_i$ by $\alpha_i\ge0$, so the count is at most
$\lceil f_i(n_{i+1}+1)/(n_{i+1}+4)\rceil\le f_i$; it is at least one because
$\alpha_i$ itself lies in the window.

For (141.2), $W=n_{i+1}+k_{i+1}+3$ and $M=2^{k_{i+1}+1}\ge(n_{i+1}+k_{i+1}+5)/A_{i+1}$
by $\beta_{i+1}\ge0$, giving the upper bound as before. For the lower bound, a
zero-epoch start has $A_{i+1}\ge4$, so by (140.5)

\[
4\cdot2^{k_{i+1}+1}\le2^{k_{i+1}+1}A_{i+1}=\beta_{i+1}+n_{i+1}+k_{i+1}+5
<2\bigl(n_{i+1}+k_{i+1}+3\bigr)+2,
\]

hence

\[
\boxed{2^{k_{i+1}+2}<n_{i+1}+k_{i+1}+4.}
\tag{141.3}
\]

So $M$ is below half the window width and the class meets it at least twice.
$\square$

## Corollary 142 (the forced-slack dichotomy is one-sided)

By (141.3) the block slack $\beta_{i+1}$ is **never** arithmetically forced: its
modulus provably cannot cover its window, so at least two candidates always
remain.

The gap slack $\alpha_i$ can be forced, and exactly then

\[
\boxed{f_i\le2.}
\tag{142.1}
\]

### Proof of (142.1)

Write $N=n_{i+1}$, $M=2^{r_i+2}$ and $\alpha=\alpha_i=Mf_i-(N+4)$, so
$\alpha\in[0,N]$ by (140.4)--(140.5). Suppose $\alpha$ is the only member of its
class modulo $M$ in $[0,N]$. Then

\[
\alpha<M
\qquad\text{and}\qquad
\alpha+M>N,
\tag{142.2}
\]

since otherwise $\alpha-M$ or $\alpha+M$ would be a second member of the class
inside $[0,N]$. Substituting $\alpha=Mf_i-(N+4)$ turns (142.2) into

\[
M(f_i-1)<N+4,
\qquad
M(f_i+1)>2N+4.
\]

Multiplying the first by $(f_i+1)$ and the second by $(f_i-1)$ and comparing
eliminates $M$:

\[
(f_i+1)(N+4)>(f_i-1)(2N+4),
\qquad\text{i.e.}\qquad
N(f_i-3)<8.
\tag{142.3}
\]

Every gate in question has $N\ge8$, so (142.3) gives $f_i\le3$.

It remains to exclude $f_i=3$. Then (142.2) reads $N+2<2M<N+4$, forcing
$2M=N+3$ and hence

\[
N=2^{r_i+3}-3.
\]

Theorem 137 now determines the whole continuation. The child overshoot is
$A'=N+4-3\cdot2^{r_i+1}=2^{r_i+1}+1$, the forced block length is $k'=1$, and the
child returns at index $N+2=2^{r_i+3}-1$ with residue

\[
f'=N+1+4-2A'=2^{r_i+2}.
\]

At that return state $2f'=2^{r_i+3}=(N+2)+1$. So the zero test
$2e\le n-U$ fails for **every** wrap count, because $2f'$ already exceeds the
index $N+2$; and the wrap test $2e>n+2$ fails because
$2f'=2^{r_i+3}<2^{r_i+3}+1$. The safe map therefore terminates there, and no next
positive block exists.

Hence $f_i=3$ cannot occur at a gate between two returning positive blocks, and
$f_i\le2$. $\square$

The two regimes are distinguished by *why* uniqueness holds. If the modulus
covers the window, $2^{r_i+2}>n_{i+1}$, then $\alpha_i\le n_{i+1}$ forces
$f_i=1$. Uniqueness can also hold by alignment with the modulus *not* covering
the window, and then $f_i=2$. Both are within (142.1); neither is excluded by the
counting bound of Lemma 141 alone, which is why (142.2) is needed.

Consequently, for a hypothetical infinite orbit the natural dichotomy

1. gaps and block lengths stay below their logarithmic uniqueness thresholds, or
2. infinitely many transitions have an arithmetically forced slack,

degenerates on the $\beta$ side: branch 2 is reachable only through $\alpha$, and
by (142.1) only at gates whose incoming returned residue is $1$ or $2$. On a
pure-upper chain Corollary 120 gives $f_i\ge5$, so **neither** slack is ever
forced there and branch 1 holds at every step.

Bounded check at $n\le150$, the figures `verify_block_chain_map.py` reports in
CI: of $26{,}293$ gates with $r_i\ge1$, the gap modulus covers its window in
$711$, and a further $525$ have a unique $\alpha_i$ by alignment alone. The
verifier asserts $f_i\le2$ on **both** kinds, and separately that the
modulus-dominant kind has $f_i=1$. Of $21{,}579$ gates with $k_{i+1}\ge2$, none
has a unique $\beta_{i+1}$.

Over a wider sweep to $n\le200$ the observed split is exact: $f_i=1$ at every one
of the $1{,}717$ modulus-dominant gates and $f_i=2$ at every one of the $846$
alignment-unique gates, with $f_i=3$ occurring at $6$ configurations, all of them
terminating and none of them a gate between two returning blocks — as the proof
of (142.1) requires.

**What this redirects.** A descent cannot come from $\beta$-uniqueness, because
that never occurs. It must come either from the $\alpha$ side — where forcing
costs $f_i\le2$, an extremely restrictive state — or from the interaction of the
two windows across a step, which is what (140.3) couples. The two regimes should
be separated before the recurrence is manipulated, exactly as the alignment
count above separates modulus dominance from accidental uniqueness.

## What the coordinate change does and does not buy

To be precise about what has and has not changed: the expanding factors
$2^{k_{i+1}}$ and $2^{r_{i+1}+1}$ are still present in the exact recurrence
(140.3). What the change of coordinates buys is that the *admissibility*
restrictions become statements about bounded slacks lying in prescribed residue
classes to growing dyadic moduli, instead of statements about where an expanding
residue lands. That is a better starting point for a descent argument, but it is
not a removal of the expansion.

