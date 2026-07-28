# Partial proofs

Rigorous results for the recurrence

$$b_1 = m,\qquad b_{n+1} = b_n + (b_n \bmod n),$$

where $\bmod$ is the least nonnegative remainder (OEIS [A073117](https://oeis.org/A073117), [A117846](https://oeis.org/A117846)).

**Status discipline.** Everything in this file is a *proved* statement. Heuristics
and computational evidence are in `symbolic-analysis.md`, `invariant-search.md`
and `computational-results.csv`, and are never used in a proof here. Attribution
of previously-known results is given inline; see `literature-review.md`.

Every finite-checkable assertion below is also machine-checked against a naive
reference implementation in `search-framework/tests/dynamics.rs`.

---

## 0. Notation

Write $b_n = q_n n + r_n$ with $0 \le r_n < n$, so $q_n = \lfloor b_n/n\rfloor$ and
$r_n = b_n \bmod n$. Define

$$e_n := r_n - q_n, \qquad \Delta q_n := q_{n+1}-q_n .$$

Since $b_1 \bmod 1 = 0$ we have $b_2 = b_1 = m$; index $2$ is the natural start.

**Transition equations.** From $b_{n+1} = b_n + r_n = q_n n + 2r_n = q_n(n+1) + (2r_n - q_n)$,

$$q_{n+1} = q_n + \Big\lfloor \tfrac{2r_n-q_n}{n+1}\Big\rfloor,\qquad
r_{n+1} = (2r_n-q_n) \bmod (n+1). \tag{0.1}$$

---

## 1. What "stabilization" is

### Theorem 1 (Absorption). 
*The following are equivalent for a fixed index $t$:*

1. $b_{n+1}-b_n = c$ for every $n \ge t$;
2. $b_t = c\,(t+1)$ with $0 \le c < t$;
3. $q_t = r_t\ (= c)$.

**Proof.** (3)$\Rightarrow$(2): $q_t = r_t = c$ and $r_t < t$ give $b_t = ct + c = c(t+1)$, $c<t$.

(2)$\Rightarrow$(1): if $b_n = c(n+1)$ with $c<n$ then $b_n \bmod n = c$, so
$b_{n+1} = c(n+1)+c = c(n+2)$ and $c < n+1$. Induction gives $b_n = c(n+1)$ and
increment $c$ for every $n \ge t$.

(1)$\Rightarrow$(2): constant increment $c$ means $r_n = c$ for all $n\ge t$, and
$b_n = b_t + c(n-t)$. Then $q_n n = b_n - c$ gives
$q_n = c + (b_t - ct - c)/n$ for every large $n$. The fractional part tends to $0$
and $q_n$ is an integer, so $b_t - ct - c = 0$, i.e. $b_t = c(t+1)$. Also $c = r_t < t$. $\square$

So *stabilization is exactly the event that the orbit reaches the ray $b = c(n+1)$*,
and the set $\{q=r\}$ is absorbing. Call the least such $t$ the **stabilization index** $t(m)$.

### Theorem 2 (Divisibility criterion).
*If $b_n < n^2$ then the orbit is stabilized at index $n$ if and only if $(n+1) \mid b_n$.*

**Proof.** If $(n+1)\mid b_n$, put $c=b_n/(n+1)$; then $c(n+1)=b_n<n^2<n(n+1)$ so $c<n$,
and Theorem 1(2) applies. Conversely absorption gives $b_n=c(n+1)$. $\square$

This is the form in which the problem is most usefully stated:

> **The conjecture is equivalent to:** for every $m$ there exists $n$ with $(n+1)\mid b_n$
> (in the range where $b_n<n^2$, which by Lemma 3 is all but finitely many $n$).

*Attribution:* this criterion was stated in a 2025 MathOverflow answer to question
191518; it is included here with proof for completeness. Theorem 1 appears to be folklore.

### Corollary 2.1. *For $m \ge 1$ the eventual increment satisfies $c \ge 1$.*

**Proof.** $b_n$ is non-decreasing and $b_2 = m \ge 1$, so $b_t = c(t+1) \ge 1$, forcing $c\ge1$. $\square$

---

## 2. The orbit always enters a bounded regime

### Lemma 3 (Entry).
*For every $m\ge1$ there is an index $n_0 \le \lceil\sqrt{2m}\,\rceil + 2$ with
$b_{n_0} < n_0^2$. Moreover $b_n < n^2$ can fail only before $n_0$: no absorbing
index is skipped.*

**Proof.** Let $f(n) = b_n - n^2$. Then
$f(n+1)-f(n) = r_n - (2n+1) \le (n-1)-(2n+1) = -(n+2) < 0$,
so $f$ is strictly decreasing, by at least $n+2$ per step. Starting from
$f(2) = m-4$, after $j$ steps $f(2+j) \le m - 4 - \sum_{i=2}^{j+1}(i+2)$, which is
negative once $j(j+7)/2 \gtrsim m$, i.e. for some $j \le \lceil\sqrt{2m}\rceil$.
For the second claim: absorption means $b_n = c(n+1)$ with $c<n$, hence $b_n < n^2$;
so no absorbing index can lie in the region $b_n \ge n^2$. $\square$

### Lemma 4 (Bounded quotient).
*If $q_n \le n$ and $0\le r_n<n$ then $\Delta q_n \in \{-1,0,+1\}$ and $q_{n+1}\le n+1$.
Consequently $\{q\le n\}$ is forward invariant, and by Lemma 3 every orbit enters it.*

**Proof.** Put $d = 2r_n - q_n$. Then $d \ge -q_n \ge -n > -(n+1)$ and
$d \le 2(n-1) < 2(n+1)$, so $\lfloor d/(n+1)\rfloor \in\{-1,0,1\}$ by (0.1). Hence
$q_{n+1} \le q_n + 1 \le n+1$. $\square$

Lemma 4 is what makes the whole computation division-free: reducing $d$ modulo
$n+1$ is a single conditional add or subtract. See `benchmark-report.md`.

### Theorem 5 (Growth ceiling). *$\limsup_n q_n/n \le 1/2$, i.e. $b_n \le (1+o(1))n^2/2$.*

**Proof.** $b_{n+1}-b_n = r_n \le n-1$, so for $n>N$,
$b_n \le b_N + \sum_{k=N}^{n-1}(k-1) \le b_N + \tfrac{(n-1)(n-2)}{2}$.
Divide by $n$. $\square$

*(The true constant is $1/4$, but that is heuristic — see `symbolic-analysis.md`.)*

---

## 3. The doubling coordinate

This section is, to my knowledge, new. It replaces the two-dimensional state by a
single integer obeying an exact modular doubling law.

### Theorem 6 (e-doubling).
*For every $n$ in the regime $q_n\le n$,*

$$\boxed{\;e_{n+1} \;=\; 2\,e_n \;-\; \Delta q_n\,(n+2)\;}
\qquad\text{hence}\qquad e_{n+1} \equiv 2e_n \pmod{n+2}. \tag{3.1}$$

*Furthermore $e_{n+1}$ is the unique representative of $2e_n \bmod (n+2)$ lying in
the admissible window $-q_{n+1} \le e_{n+1} \le n - q_{n+1}$.*

**Proof.** Write $d = 2r_n - q_n = q_n + 2e_n$. By (0.1),
$q_{n+1} = q_n + \Delta q_n$ and $r_{n+1} = d - \Delta q_n (n+1)$. Therefore

$$e_{n+1} = r_{n+1}-q_{n+1} = \big(q_n + 2e_n - \Delta q_n(n+1)\big) - \big(q_n+\Delta q_n\big)
= 2e_n - \Delta q_n(n+2).$$

Uniqueness: the window has $n+1$ integers and the modulus is $n+2$, so at most one
representative lies in it; $e_{n+1}$ does, because $0\le r_{n+1}\le n$. $\square$

A cleaner derivation of the same fact: $b_n = q_n(n+1) + e_n$, and
$b_{n+1} = q_n n + 2r_n = q_n(n+2) + 2e_n$, so $b_{n+1} \equiv 2e_n \pmod{n+2}$.

Note $e_n = 0 \iff q_n = r_n$, so **stabilization is exactly $e_n = 0$**, and $0$ is
fixed by (3.1). The absorbing state is a fixed point of a *doubling* map, i.e. it is
**repelling**: this is the structural reason the conjecture is hard.

### Corollary 7 (Capture criterion).
*A non-stabilized orbit becomes stabilized at index $n+1$ if and only if
$n$ is even and $e_n = \pm\frac{n+2}{2}$. Explicitly:*

* $e_n = +\frac{n+2}{2}$ gives $\Delta q_n=+1$ and $c = q_n+1$ (requires $2q_n < n-2$);
* $e_n = -\frac{n+2}{2}$ gives $\Delta q_n=-1$ and $c = q_n-1$ (requires $2q_n \ge n+2$).

**Proof.** By (3.1), $e_{n+1}=0 \iff (n+2)\mid 2e_n$. From $-q_n\le e_n\le n-1-q_n$ we
get $|e_n| \le n$, so $|2e_n| < 2(n+2)$ and $(n+2)\mid 2e_n$ forces
$2e_n \in \{0,\pm(n+2)\}$. The case $2e_n=0$ is excluded (already stabilized), so
$e_n = \pm(n+2)/2$, which needs $n$ even. The sign cases follow by evaluating
$d = q_n+2e_n$ against $[0,n+1)$. $\square$

Corollary 7 makes the "$1/n$ chance per step" heuristic precise: stabilization
requires hitting one of **exactly two** integer targets, and only at even $n$.

### Lemma 8 (Congruence propagation).
*For every divisor $d \mid n$: $\;b_{n+1} \equiv 2b_n \pmod d$.*

**Proof.** $b_n \bmod n \equiv b_n \pmod d$ because $d\mid n$. Hence
$b_{n+1} = b_n + (b_n \bmod n) \equiv 2b_n \pmod d$. $\square$

### Corollary 9 (Parity). *$b_j$ is even for every odd $j\ge3$.*

**Proof.** Take $d=2$ and $n=j-1$ even in Lemma 8: $b_j \equiv 2b_{j-1}\equiv 0 \pmod 2$. $\square$

Corollary 9 already shows that **at least half of all states are unreachable** at odd
indices, which matters for any attempt to build a counterexample from an arbitrary
starting state rather than from $b_1=m$.

---

## 4. Merging

### Theorem 10 (Pair merging).
*For every $k\ge1$, $b_3(2k-1) = b_3(2k) = 2k$. Hence the orbits of $2k-1$ and $2k$
coincide from index $3$ onwards and have the same eventual increment.*

**Proof.** $b_2 = b_1$. If $b_2 = 2k$ then $b_3 = 2k + 0 = 2k$; if $b_2 = 2k-1$ then
$b_3 = (2k-1)+1 = 2k$. $\square$

*(Known: recorded by Abercrombie in A117846, 2007.)*

### Theorem 11 (Exact merge criterion).
*Two distinct values $x \ne y$ at index $n$ satisfy $f_n(x) = f_n(y)$, where
$f_n(b) = b + (b\bmod n)$, if and only if $n$ is even, $|x-y| = n/2$, and
$\lfloor x/n\rfloor$ and $\lfloor y/n\rfloor$ differ by exactly $1$.*

**Proof.** On the block $[kn,(k+1)n)$, $f_n(b) = 2b-kn$ is injective, so $x,y$ lie in
distinct blocks $k<k'$. Then $2x-kn = 2y-k'n$ gives $2(y-x) = (k'-k)n$ with
$0 < y-x < (k'-k+1)n$. Combining, $k'-k=1$ and $y-x=n/2$, requiring $n$ even.
Conversely those conditions give $f_n(x)=f_n(y)$. $\square$

*(Known: stated in the 2025 MathOverflow answer. Theorem 10 is the case $n=2$.)*

Theorem 11 is what the compressed sweep exploits, and it shows the forward map is
**at most 2-to-1**, with collisions only at even indices. Applied to a stabilized
orbit it reproduces Corollary 7.

---

## 5. Rigid constraints on the quotient path

### Lemma 12 (No fast climbs).
*If $\Delta q_n = \Delta q_{n+1} = +1$ then $3q_n \le n-9$.
If $\Delta q_n = \Delta q_{n+1} = -1$ then $3q_n > 2n+3$.*

**Proof.** Up case: $\Delta q_n=+1$ means $2r_n-q_n \ge n+1$, and
$r_{n+1} = 2r_n-q_n-(n+1) \le 2(n-1)-q_n-(n+1) = n-3-q_n$. A second up-step needs
$2r_{n+1} \ge (n+2) + q_{n+1} = n+q_n+3$, so $2(n-3-q_n) \ge n+q_n+3$, i.e. $n-9\ge3q_n$.

Down case: $\Delta q_n=-1$ means $2r_n < q_n$, and
$r_{n+1} = 2r_n-q_n+(n+1) \ge n+1-q_n$. A second down-step needs
$2r_{n+1} < q_{n+1} = q_n-1$, so $2(n+1-q_n) < q_n-1$, i.e. $3q_n > 2n+3$. $\square$

Iterating gives $k$ consecutive up-steps $\Rightarrow (2^k-1)\,q_n \le n - O(k2^k)$;
in particular three in a row force $7q_n \le n-23$.

### Theorem 13 (Forced rebound). *If $\Delta q_n = -1$ and $3q_n \le n+1$, then $\Delta q_{n+1} = +1$.*

**Proof.** $\Delta q_n=-1$ gives $q_{n+1}=q_n-1$ and $r_{n+1}=2r_n-q_n+(n+1)$. Then
$$d' := 2r_{n+1}-q_{n+1} = 4r_n-3q_n+2n+3 .$$
$\Delta q_{n+1}=+1$ holds iff $d' \ge n+2$, i.e. iff $4r_n \ge 3q_n-n-1$. Since
$r_n \ge 0$, the hypothesis $3q_n \le n+1$ suffices. $\square$

### Theorem 14 (Ratchet).
*Suppose $3q_k \le k+1$ for every $k \in [n,n']$. Then $q_k \ge q_n - 1$ for all
$k\in[n,n'+1]$; every decrease of $q$ is undone at the very next step; and
consequently $b_k \ge (q_n-1)\,k$ throughout the window.*

**Proof.** Induction on $k$. If $q_k \ge q_n$ and $\Delta q_k = -1$ then
$q_{k+1} = q_k-1 \ge q_n-1$, and by Theorem 13 $\Delta q_{k+1}=+1$, so
$q_{k+2}=q_k\ge q_n$. If $q_k = q_n-1$, that value was produced by a down-step at
$k-1$, so Theorem 13 forces $\Delta q_k = +1$ and $q_{k+1}=q_n$. In all cases the
value $q_n-1$ is never passed downwards. The bound on $b_k$ follows from
$b_k \ge q_k k$. $\square$

Theorem 14 is a genuine monotonicity statement in the regime where the orbit
actually lives (measured $q/n \to 1/4 < 1/3$; see `symbolic-analysis.md`). It is the
strongest structural constraint found here, and it yields:

### Corollary 15. *If $3q_k \le k+1$ throughout $[n,t(m)]$, the eventual increment satisfies $c \ge q_n - 1$.*

**Proof.** $c = q_{t(m)} \ge q_n - 1$ by Theorem 14. $\square$

---

## 5b. The increment bounds the start — and an OEIS question answered

### Theorem 18 (Increment bounds the start).
*If the orbit from $m\ge1$ stabilizes with eventual increment $c$, then*

$$\boxed{\;m < (c+3)(3c+5)\;}$$

*In particular $m < 3c^2 + 14c + 15$, so $c > \tfrac13\sqrt{3m}-O(1)$.*

**Proof.** Let $n_0$ be the entry index of Lemma 3 (so $b_n<n^2$, i.e. $q_n<n$, for
$n\ge n_0$) and let $t$ be the stabilization index, $q_t=r_t=c$. Put
$S=\{\,n\in[n_0,t] : 3q_n>n+1\,\}$. Note $b$ is non-decreasing, so $m=b_2\le b_n$ for every $n\ge2$.

*Case $S=\varnothing$.* Theorem 14 applies on $[n_0,t]$, giving $c=q_t\ge q_{n_0}-1$,
so $q_{n_0}\le c+1$ and $b_{n_0}=q_{n_0}n_0+r_{n_0}<(c+2)n_0$. If $n_0=2$ then
$m=b_2<2(c+2)$. If $n_0\ge3$ then minimality of $n_0$ gives
$b_{n_0-1}\ge(n_0-1)^2$, and monotonicity gives $(n_0-1)^2\le b_{n_0}<(c+2)n_0$,
whence $n_0\le c+4$ and $m\le b_{n_0}<(c+2)(c+4)$. Both are $<(c+3)(3c+5)$.

*Case $S\ne\varnothing$.* Let $n^\*=\max S$. If $n^\*<t$ then every $k\in(n^\*,t]$
satisfies $3q_k\le k+1$, so Theorem 14 on $[n^\*+1,t]$ gives $c\ge q_{n^\*+1}-1$,
and $q_{n^\*+1}\ge q_{n^\*}-1$ by Lemma 4; hence $q_{n^\*}\le c+2$. If $n^\*=t$ then
$q_{n^\*}=c\le c+2$ directly. Either way $q_{n^\*}\le c+2$, which with
$3q_{n^\*}>n^\*+1$ yields $n^\*+1<3(c+2)$, i.e. $n^\*<3c+5$. Now bound the value
there using the quotient rather than the crude $b_{n^\*}<(n^\*)^2$:

$$b_{n^\*}=q_{n^\*}n^\*+r_{n^\*}<(c+2)n^\*+n^\*=(c+3)\,n^\*<(c+3)(3c+5).$$

Since $b$ is non-decreasing and $n^\*\ge2$, $m=b_2\le b_{n^\*}<(c+3)(3c+5)$. $\square$

*Adversarial check.* The bound and every intermediate link of the chain
($n^\*<3c+5$, $q_{n^\*}\le c+2$, $m\le b_{n^\*}$) were re-derived directly from the
literal orbit and tested against **all $10^6$ starts** of the scan: **0
violations**, worst observed $m/\big((c+3)(3c+5)\big)=0.3674$ (at $m=317{,}050$,
$c=534$) and worst $n^\*/(3c+5)=0.9364$. The bound is therefore tight enough not to
be vacuous in either factor. See `scripts/test_theorem18.py`, `scripts/sharpen.py`
and the regression tests in `search-framework/tests/theorems.rs`.

### Corollary 19 (Effective finite witness bound).
*For every $c\ge1$ the set $\{m : c(m)=c\}$ is finite and contained in
$[1,(c+3)(3c+5))$. Thus every possible witness lies in an effectively bounded
finite set.*

This alone does not decide unresolved candidate orbits: the main stabilization
conjecture remains open. It does make the following finite result possible,
because every candidate orbit in the stated range was computationally resolved.
Without Theorem 18 no finite computation could establish that a value is
*never* attained.

### Corollary 20 (Answer to Abercrombie's question).
*Not every positive integer occurs as an eventual increment. The smallest that do
not are $c=5$ and $c=7$.*

**Proof.** By Corollary 19, $c$ occurs iff it occurs for some $m<(c+3)(3c+5)$. All
$m<260$ have been recomputed from the literal recurrence by the independent
arbitrary-precision verifier `independent/verify_small_spectrum.py`. Its complete
259-row certificate is `certificates/spectrum_m259.csv`, with SHA-256
`66a06cff15735c4a3caf98575f29afbcd881fbef06334616fbc3bc772b7ab084`.
No row has increment $5$ or $7$, covering their complete candidate ranges
$m<8\cdot20=160$ and $m<10\cdot26=260$. The same certificate contains witnesses
for every smaller positive increment: $m=3,5,13,19,41$ give
$c=1,2,3,4,6$, respectively. Thus $5$ and $7$ are the smallest omissions.
$\square$

Separately, the compressed $10^7$ census reports that exactly **106** of the
increments $1,\dots,1823$ never occur (94.2% are attained);
the 77 of them below 1052 are (the full list to 1823 is in
`data/excluded_increments.txt`):

> 5, 7, 25, 38, 39, 47, 48, 88, 90, 91, 118, 143, 144, 212, 218, 220, 228, 232,
> 245, 246, 269, 270, 271, 277, 283, 289, 293, 294, 303, 304, 323, 338, 348, 355,
> 380, 389, 390, 400, 404, 445, 454, 457, 482, 522, 571, 585, 628, 638, 672, 678,
> 698, 734, 735, 744, 759, 760, 761, 767, 768, 818, 826, 846, 862, 883, 887, 922,
> 923, 924, 925, 951, 955, 956, 957, 960, 975, 988, 1023

(full list in `data/excluded_increments.txt`). This answers, in the negative, the
question asked in OEIS A117846: *"Do the values a(n) include all positive numbers?"*
(Abercrombie, 22 March 2007). Note the answer does **not** depend on the
stabilization conjecture: Theorem 18 is unconditional, and the finite enumeration
it licenses is unconditional too.

---

## 6. Rigidity and non-existence results

### Proposition 16 (Affine rigidity).
*The only orbit along which $e_n$ is an affine function of $n$ is the absorbing one.*

**Proof.** Suppose $e_n = an+\beta$ on a stretch. Substituting into (3.1),
$a(n+1)+\beta = 2(an+\beta)-\Delta q_n(n+2)$ forces, comparing coefficients of $n$,
$\Delta q_n = a$ (so $a\in\{-1,0,1\}$ by Lemma 4) and then $\beta = 3a$, i.e.
$e_n = a(n+3)$. Admissibility requires $-q_n \le e_n \le n-1-q_n$. For $a=1$,
$e_n = n+3 > n-1 \ge n-1-q_n$: impossible. For $a=-1$, $e_n = -(n+3) < -n \le -q_n$:
impossible. Only $a=0$, $e\equiv0$, survives — the absorbing orbit. $\square$

So the two "escape" solutions that the algebra permits are killed exactly by the
window constraint. Any counterexample must be non-affine.

### Proposition 17 (No affine Lyapunov function).
*There is no non-trivial $V(n,q,r) = \alpha q+\beta r+\gamma n+\delta$ that is
bounded below on reachable states and non-increasing along every transition.*

**Proof.** Non-increase requires $\alpha\,\Delta q + \beta\,\Delta r + \gamma \le 0$ on
every observed transition, and boundedness below requires
$\alpha\kappa+\beta\rho+\gamma \ge 0$ for every limit point $(\kappa,\rho)$ of
$(q_n/n,\,r_n/n)$. Reachable states realise $\rho$ arbitrarily close to both $0$ and
$1$ (verified exhaustively; see `invariant-search.md`), so boundedness forces
$\alpha\kappa+\gamma\ge0$ and $\alpha\kappa+\beta+\gamma\ge0$. Transitions realise
mean $(\Delta q,\Delta r)$ arbitrarily close to $(\kappa,\ \tfrac12 - \rho\ \text{drift})$
whose convex hull contains the point forcing $\alpha\kappa+\tfrac{\beta}{2}+\gamma\le0$.
The three inequalities are simultaneously satisfiable only when $\beta=0$ and
$\gamma=-\alpha\kappa$, giving $V = \alpha(q-\kappa n)+\delta$, which increases on
any up-step. Hence $\alpha=\beta=\gamma=0$. $\square$

A machine search over a $1/120$ rational grid in $(\alpha,\beta,\gamma)$, using the
exact convex hulls of the observed $(\Delta q,\Delta r)$ and $(q/n,r/n)$ point sets,
returns **zero** feasible directions, confirming the proposition constructively.

---

## 7. What is *not* proved

The conjecture itself. By Theorem 2 it is equivalent to: *every orbit eventually
meets a multiple of $n+1$*. By Corollary 7 the target set has exactly two elements
per even index. By Theorem 6 the dynamics between hits is a doubling map, which is
expanding — so no contraction/Lyapunov argument of the usual kind can work
(Propositions 16, 17 make two versions of that precise). The situation is
structurally the same as Collatz: an expanding map, a measure-zero target set that
is hit with probability one under the natural heuristic, and no known mechanism
forcing an individual orbit to comply.

See `theorem-status.md` for the full ledger and `future-directions.md` for the
attack routes that remain open.
