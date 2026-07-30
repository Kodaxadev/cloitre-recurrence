# Future directions: the safe-map frontier

Extracted from [`future-directions.md`](future-directions.md) so each file
stays inside the repository's per-file length gate. This is section 6 of that
document, unchanged apart from this header and the section title below.

## Equidistribution of $e_n \bmod (n+2)$ — the actual obstruction

By Theorem 2 the conjecture is exactly "every orbit meets a multiple of $n+1$",
and by Theorem 6 the motion between hits is doubling with a **moving modulus**.
Fixed-modulus doubling has a complete equidistribution theory; the moving-modulus
case appears to have none.

**Do:** look for the smallest non-trivial model with the same structure —
$x_{n+1} \equiv 2x_n \pmod{n+c}$ with a window constraint — and ask whether *any*
capture theorem is provable there, even under an extra hypothesis such as $n$
restricted to a sparse set. A negative answer (a constructed non-capturing orbit
in the relaxed model) would be as informative as a positive one, because it would
localise exactly which feature of the real recurrence does the work.

**Success:** a capture theorem for any moving-modulus doubling system, or an
explicit counterexample in the relaxed model.

Theorem 39 and Lemmas 40--41 now make the smallest useful intermediate target
more precise. For a positive no-down tail, start the pure map

```text
e_(n+1)=2e_n mod(n+2)
```

with quotient zero and let `U_n` count wraps. Prove that some zero digit must
satisfy `U_n+2e_n>=n+1`, or that the pure orbit captures. The compressed
`pure --safe-sweep` computation proves this separately at each selected start
index and shows an apparent `O(sqrt(n))` lifetime. A uniform upper bound of any
finite form would rule out eventual monotone escape.

Lemma 80 and Corollary 81 now rule out long wrap blocks as the missing
mechanism: every positive block satisfies \(2^kU<n\), and an infinite safe
path has \(k\le\log_2\log_2n+o(1)\). Corollary 82 also forces at least
\((1-o(1))n/(\log n\log\log n)\) completed positive blocks by a zero epoch.
The remaining target must therefore control the residues of these frequent
aperiodic bounded or slowly growing blocks, rather than force one block to
exceed the state window.

Lemma 83 now supplies the first exact residue gate for that target. If a
positive block of length \(k\) returns with residue \(f\), and \(r\)
zero-only blocks precede the next positive block, then

\[
f\equiv m+3\pmod{2^k},\qquad
\frac{m+r+3}{2^{r+2}}<f\le\frac{m-V+r}{2^{r+1}}.
\]

**Do:** determine whether infinitely many unique gates can be compatible
with the autonomous overshoot map. Use the lifted class modulo \(2^{k+1}\),
not only the displayed weaker congruence. In the nonunique case, exploit
\(2^{k+r+3}<G+r-3\) across the quantitatively frequent blocks from
Corollary 82, rather than treating each gate independently.

For the unit-wrap case, Lemma 85 replaces the gate by the affine
coordinates \((n,D,s)\), and Corollary 86 makes uniqueness equivalent to
explicit lower and upper boundary layers. The bounded search already finds
seven consecutive unique unit-wrap gates, so a useful next argument must
show that those boundary layers cannot be followed indefinitely; a small
constant-chain assumption is not justified.

Lemma 87 now eliminates three consecutive uses of the parent boundary:
the only compatible triple is an explicit terminal path. More strongly,
Corollary 88 observes that any failure of

\[
D+r-3<2^{r+5}
\]

forces this inequality at the next unique gate. Thus it holds at least once
every two gates of a continuing unique unit-wrap chain.
**Do:** combine these frequent logarithmic zero-only gaps with the exact
successor residues, rather than only their lengths. Their frequency alone
still permits the \(n/\log n\) quotient scale required by Theorem 45.
Corollary 89 makes this compatibility quantitative: a hypothetical
all-unit, all-unique tail must have \(D_j\ge(1/2-o(1))j\log_2j\) and quotient
scale between constants \(1\) and \(2\) times \(n/\log_2n\).
Theorem 90 closes that constant gap: non-short gates would force
\(U\ge D/2\), contradicting Corollary 89's \(U/D\to0\). Hence every late
gate is short and any surviving all-unit/all-unique tail must satisfy

\[
D_j\sim j\log_2j,\qquad
\frac{U_j\log_2n_j}{n_j}\to1.
\]

**Do:** analyze the equality case of Theorem 45. A contradiction can no
longer come from first-order density in this subcase; it must use the exact
residues or a second-order loss from the moving logarithmic zero-run ceiling.

Theorem 91 completes that equality-case analysis for an all-unit/all-unique
tail. It proves \(L-5\le r\le L\), bounds the positive excess by \(47\), and
uses the resulting finite affine-dyadic forms to contradict unavoidable
same-epoch pairs. The eventual-no-down branch is therefore reduced further:

> infinitely many blocks have length at least two, or infinitely many gates
> are nonunique.

**Do:** treat these two alternatives quantitatively. For longer blocks,
combine the extra wrap count with the exact parent equation. For nonunique
gates, accumulate \(2^{k+r+3}<G+r-3\) rather than bounding isolated gaps.

Lemma 92 now puts both alternatives in one exact boundary language. With

\[
x=2^{r+2}f-m-r-3,\qquad H=2^{k+r+3},
\]

nonuniqueness is equivalent to

\[
x>H\quad\text{or}\quad(d\ge2\text{ and }2d'\ge H).
\]

**Do:** classify consecutive unique gates in the parent layer \(d\le1\)
for arbitrary \(k\). A bounded affine search through
\(k,k',r,r'\le16\) finds only three patterns, but no uniform parameter
bound is proved. Corollary 95 eliminates a hidden singular family: every
fixed tuple has at most one rational start. The task is therefore to bound
the unbounded parameters themselves. In the complementary interior layer,
accumulate the sharp inequality \(G+r-3<2^{k+r+4}\) together with the
block-count lower bound.

Lemma 96 now proves that consecutive parent-boundary starts have
\(k_{j+1}\le k_j\), even without uniqueness. Thus a persistent parent-layer
tail has one eventual block length \(k\). **Do:** fix that \(k\), write
\(A_j=A_0+jk+d_j-d_0\), and combine the divisibility

\[
2^{r_j+1}-1\mid
(2^k-1)A_j+r_j-k+d_j+1-d_{j+1}
\]

with the exact uniqueness boundary. The remaining parameters are the gaps
\(r_j\) and the two defect bits, not the block lengths.
A bounded affine scan through \(k,r_j\le12\) finds no four-start
constant-length parent-layer pattern, but a proof must control unbounded
gaps rather than extrapolate from that search.

Theorem 99 proves exactly why a bounded search cannot finish this branch:
any surviving fixed-\(k\) parent tail must have unbounded gaps, although

\[
r_j\le\log_2 A_j+O_k(1),\qquad
K\le\liminf\frac1J\sum_{j<J}r_j
\le\limsup\frac1J\sum_{j<J}r_j\le2K+1.
\]

**Do:** exploit the rare large-gap indices. Equation (98.3) makes each such
gap a positive jump of the returned residue, while (98.2) simultaneously
divides that residue by \(2^{r_j+1}-1\). A contradiction must compare a
large gap with the accumulated budget before and after it, rather than use
only its pointwise logarithmic ceiling.

Lemma 100 and Theorem 101 complete that comparison: equal gaps are singular,
decreasing gaps violate an exact power-of-two divisibility, and strictly
increasing gaps contradict Theorem 99's bounded mean. The parent boundary
cannot persist.

**Do:** work only with the exhaustive alternatives in Corollary 102. At
infinitely many interior starts \(d\ge2\), either the gate is nonunique or
uniqueness forces the child boundary

\[
2d'<2^{k+r+3}.
\]

Lemma 103 and Corollary 104 combine these into one exact test. With
\(H=2^{k+r+3}\) and the explicit canonical origin \(\rho_{k,r}(n)\), an
interior gate is unique exactly when

\[
\rho\le D'-3<\rho+H;
\]

a miss into any later translate is exactly nonuniqueness. Corollary 105 says
the origin permutes all dyadic residues for fixed \(k,r\), but it does not
give equidistribution along the dependent orbit.

**Do:** derive an inter-gate law for the window displacement
\(D'-3-\rho\). Show either that repeated first-window hits force a forbidden
parameter repetition/periodicity, or that later-window misses occur with a
frequency that can be accumulated across Corollary 82's frequent positive
blocks.

Lemma 106 supplies the first inter-gate law:
\(2A'=n'+5-\rho\), so the child block is unit exactly when
\(2\rho\le n'+4\). Corollaries 107--108 sharpen the exhaustive frontier.
Every infinite safe path has infinitely many nonunique gates, or infinitely
many unique longer-child gates whose gaps satisfy

\[
\frac r{\log_2n'}\longrightarrow1.
\]

Corollary 109 shows that the latter reset gates number only
\(O(N/\log N)\) through index \(N\). Their zero density in absolute time does
not make them finite or sparse among positive blocks.

Lemma 110 now counts every locally valid gate state exactly:

\[
|\mathcal F|
=1+j+\min\!\left(\lfloor d/2\rfloor,\lfloor2d'/H\rfloor\right).
\]

Thus every later-window translate creates a lower candidate. Only
displacement stored in the child defect can be absorbed by finite parent
defect headroom.

Lemma 113 now supplies the missing inter-gate transfer: the child excess
determines its returned residue, and equals it for a unit child. Consecutive
unit blocks therefore obey

\[
f_{i+1}=2^{r_i+2}f_i-n_i-r_i-5.
\]

The pure-upper subcase has an exact inequality test, but a literal safe path
already contains six consecutive pure-upper gates. Fixed short-transience
and simple defect monotonicity are therefore false.

Theorem 118 now controls the asymptotic scale of the hypothetical infinite
all-unit pure-upper case:

\[
\frac12\le\liminf\frac{n_J}{J\log_2J}
\le\limsup\frac{n_J}{J\log_2J}\le1.
\]

Equivalently, adjacent gaps must repeatedly supply logarithmic size, while
the quotient ratio stays in the nondegenerate window \([1,2]\). This matches
the critical safe-map scale rather than contradicting it.

Lemma 119 now supplies the second-order obstruction:

\[
f_{i+2}\equiv f_{i+1}-r_{i+1}-2
\pmod {2^{\min(r_i,r_{i+1})+2}}.
\]

Corollary 120 first excludes ladder coefficients below five. Theorem 121
makes the remaining unit branch exhaustive. Either every gap
diverges and these moduli grow without bound, or one bounded gap and one
bounded returned residue recur infinitely often. The renewal starts then
occupy one fixed residue class, and their exits lie on one fixed dyadic
ladder after isolated logarithmic gaps.

Theorem 122 excludes the densest fixed-ladder recurrence: the same
\((R,a)\) renewal cannot occur at every other gate three times in
succession. Any surviving ladder mechanism must insert at least two other
gates in one of every two successive renewal intervals.

Lemma 123 handles arbitrary return spacing at the word level. A prescribed
gap word and its two endpoint residues determine at most one start index.
Thus successive visits to one fixed \((R,a)\) pair must use pairwise
distinct intervening words. Since Theorem 118 bounds the gap alphabet by
\(O(\log J)\), Corollary 124 gives

\[
M_{R,a}(J)
\le(1+o(1))\frac{J\log_2\log_2J}{\log_2J}.
\]

Every fixed ladder pair therefore has zero block density, although it may
still recur infinitely often.

Lemma 125 rewrites every equal-endpoint word as the sparse-binary equation

\[
B(n_p+3)=(2^S-1)a+W
\]

and shows that a fixed-ladder return has
\(S\equiv0\pmod {2^{R+2}}\). This does not collapse the word set:
Proposition 126 gives, for every \(7\le a\le32\) with \(3\nmid a\),
infinitely many literal pure-upper segments with two occurrences of
\((R,a)=(1,a)\) and unbounded intervening span. Thus Theorem 122 is sharp
in the number of renewals, and single-interval integrality is not enough.

Lemma 127 now gives the exact cross-word equation required at successive
return intervals. Lemma 128 independently puts every outgoing gate from a
fixed returned residue into one disjoint dyadic window. Along chronological
returns, the selected exponents are nondecreasing; if an exponent repeats,
the child residue decreases by the exact index difference. Proposition 129
then eliminates every Proposition 126 segment as an infinite-tail seed:
there is one forced continuation gate and no pure-upper gate after it.

Theorem 130 then collapses the word framing entirely. The disjointness proof
inside Lemma 128 uses only two of the pure-upper inequalities and only
\(D\le n\), so it applies at *every* block, not just at matched renewals. The
outgoing exponent is therefore forced,

\[
h^\ast=\min\{h\ge2:\ 2^hf\ge n+h+4\},
\]

and the mechanism is a deterministic partial map on \((n,U,f)\). The
cross-word equation (127.5) stops being a condition to solve: it holds
automatically along any orbit, because the whole gap word is a function of the
starting state. Lemma 131 removes the wrap count from the forced data, so a
sweep at \(U=0\) is exhaustive over every wrap count at once. The resulting
exhaustive computation (K15) finds a ceiling of five gates, attained only at
the K14 witness, while the Proposition 126 family reaches only four.

Theorem 133 extends the forcing to every block length, and Corollary 134
quantifies what freedom is left: the returned residue at a pure-upper gate
ranges over an interval of length exactly \(2^{k+1}\), so the unit case very
nearly selects one residue while longer blocks admit exponentially more.

**Do next, arbitrary-length branch:** control the joint sequence of block
lengths and returned residues under forced gaps. The one-step arithmetic is
complete — Corollary 134 for the residue band, (134.2) for the length/gap
trade — and no chain argument exists. The target is a multi-step obstruction
replacing the closed recurrence the unit case lost: for \(\ell=1\) Lemma 113
collapses excess and child residue, which is what produced Lemma 119's
three-residue compatibility and Theorem 118's two-step product bound. Seek the
analogue that survives an intervening block length, for instance an exact
relation among \(f_i\), \(f_{i+2}\) and \(k_{i+1}\).

**Do next, fixed-ladder branch:** it no longer has a combinatorial dimension
to search, so what remains there is a termination proof for one forced
one-dimensional orbit. No inequality argument can supply it: the constraints
alone admit chains of length \(O(n/\log n)\), and the observed ceiling of five
is arithmetic rather than metric. The concrete target is a 2-adic obstruction
built on

\[
v_2\bigl(n_{i+1}+3+f_{i+1}\bigr)=h_i+v_2(f_i),
\]

which is (130.7) in valuation form and couples the forced exponents to the
2-adic valuations of the residues. The exhaustive sweep is now cheap enough to
test any candidate invariant against every orbit below \(5\times10^9\). In the
growing-modulus branch, combine nested congruences across overlapping triples
with the state-window bounds. In the mixed-block case, treat near-maximal
unique gaps as renewal points and accumulate both headroom terms from
Lemma 110.

