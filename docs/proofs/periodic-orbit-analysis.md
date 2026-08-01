# Eventually periodic quotient changes

This note isolates the exact arithmetic obstruction to an eventually periodic
quotient-change sequence. The obstruction is proved. The finite search through
period 54 is computational evidence only.

## Setup

Let

$$a_n=\Delta q_n\in\{-1,0,+1\}$$

after entry into the invariant region $q_n\le n$. The exact doubling law is

$$e_{n+1}=2e_n-a_n(n+2).$$

Assume that from some phase index $N$, the digit word has period $p$:

$$a_{N+j+p}=a_{N+j}.$$

Write one period as $(a_0,\ldots,a_{p-1})$ and define

$$
M=2^p-1,\qquad
C=\sum_{j=0}^{p-1}2^{p-1-j}a_j,\qquad
D=\sum_{j=0}^{p-1}2^{p-1-j}a_j(j+2).
$$

The offset $j+2$ uses $N$ as the variable phase index; the actual forcing term
is $a_j(N+j+2)$.

## Theorem 25 (periodic-word integrality obstruction)

If the word is realized by an admissible infinite orbit, then

$$A=\frac{C}{M},\qquad z=pA=\frac{pC}{M}\in\mathbb Z,$$

and the phase values of the doubling coordinate are forced to be

$$\boxed{e_N=AN+B,\qquad B=\frac{z+D}{M}.}$$

In particular, a necessary and sufficient condition for this forced phase value
to be an integer for at least one integer phase $N$ is

$$\boxed{\gcd(C,M)\mid(z+D).}$$

If this divisibility fails, the periodic word cannot occur on any integer orbit,
reachable or otherwise.

### Proof

Unrolling the doubling law through one period gives

$$e_{N+p}=2^p e_N-CN-D.$$

An affine particular solution $E(N)=AN+B$ must satisfy

$$A(N+p)+B=2^p(AN+B)-CN-D.$$

Equating coefficients gives

$$A=\frac{C}{M},\qquad B=\frac{pA+D}{M}.$$

This particular solution is not merely asymptotic. The difference between any
other solution and $E$ is multiplied by $2^p$ on every cycle. Every admissible
state has $-q_n\le e_n\le n-1-q_n$, hence $e_n=O(n)$. A nonzero difference would
grow exponentially and leave this linear window. Therefore $e_N=AN+B$ exactly.

Both $e_N$ and $e_{N+p}$ are integers, so their difference $pA=z$ is an integer.
Then

$$e_N=\frac{CN+z+D}{M}.$$

The linear congruence

$$CN\equiv-(z+D)\pmod M$$

has an integer solution exactly when $\gcd(C,M)$ divides $z+D$. $\square$

## Asymptotic state constraints

Let

$$\mu=\frac1p\sum_{j=0}^{p-1}a_j.$$

Then $q_{N+kp+j}=\mu(N+kp)+O(1)$. If $A_j$ is the slope of $e$ at phase $j$,
the slopes obey

$$A_{j+1}=2A_j-a_j,\qquad A_p=A_0.$$

Admissibility requires, at every phase,

$$0\le\mu+A_j\le1$$

for the remainder window, plus the digit decision inequalities

$$
\begin{array}{c|c}
a_j & \mu+2A_j\\ \hline
-1 & \le0\\
0 & [0,1]\\
+1 & \ge1.
\end{array}
$$

Boundary cases still require checking the affine intercepts, because the exact
transition inequalities are strict on one side.

## Lemma 28 (finite-state slope reduction)

For a realizable period-$p$ word, put $S=\sum_j a_j$. There are integers
$v_j=pA_j$ satisfying

$$
v_{j+1}=2v_j-pa_j,\qquad
-S\le v_j\le p-S.
$$

Moreover $0\le S\le p/2$, and away from boundary equalities the digit is
determined by the integer $S+2v_j$:

$$
\begin{array}{c|c}
S+2v_j & a_j\\ \hline
<0 & -1\\
0 & -1\text{ or }0\\
0< S+2v_j<p & 0\\
p & 0\text{ or }+1\\
>p & +1.
\end{array}
$$

### Proof

Theorem 25 gives $pA_0\in\mathbb Z$, and
$A_{j+1}=2A_j-a_j$ propagates integrality to every phase. Set $v_j=pA_j$.
The remainder slope is

$$\mu+A_j=\frac{S+v_j}{p},$$

so its state window is exactly $-S\le v_j\le p-S$. The growth ceiling gives
$0\le\mu=S/p\le1/2$. Finally the leading coefficient of
$2r_j-q_j$ is

$$\mu+2A_j=\frac{S+2v_j}{p},$$

and comparison with the quotient-change thresholds $0$ and $1$ gives the
table. $\square$

This turns the slope search into closed walks of the doubling map modulo $p$
on at most $2p+1$ integer states. Only the two boundary states can branch.

## Theorem 29 (all denominator-3 slope cycles are impossible)

No admissible eventually periodic integer orbit can have a phase slope $A_j$
whose reduced denominator is $3$.

### Proof

Theorem 25 gives $pA_j\in\mathbb Z$. A denominator-3 slope therefore requires
$3\mid p$. It is also a periodic point of doubling, so
$3\mid2^p-1$, which requires $p$ even. Write

$$p=6h,\qquad m=p/2=3h.$$

Rotate the phase so $A_0=1/3$; any exact integer orbit remains exact after a
phase rotation. Modulo $1$, doubling alternates $1/3$ and $2/3$. The only lifts
in the universal slope window $[-1,1]$ are

$$-\frac23,\quad\frac13,\quad-\frac13,\quad\frac23.$$

Let $\mu=S/p$ be the quotient slope. The state window
$-\mu\le A_j\le1-\mu$ excludes $-2/3$ because $\mu\le1/2$. If
$\mu<1/3$, it also excludes $-1/3$, forcing the alternating digit word
$(0,+1)$ and hence $\mu=1/2$, a contradiction. If $\mu>1/3$, it excludes
$2/3$, forcing $(+1,-1)$ and hence $\mu=0$, again a contradiction. Therefore

$$\mu=\frac13.$$

Starting at $A=1/3$, every two-step return is one of

$$
\begin{array}{c|c|c}
\text{block} & \text{slope path} & \text{digits}\\ \hline
X & \frac13\to-\frac13\to\frac13 & (+1,-1)\\
Y & \frac13\to \frac23\to\frac13 & (0,+1).
\end{array}
$$

There are $m=3h$ blocks. Since their digit sums are respectively $0$ and $1$,
the identity $S=p/3=2h$ forces exactly $h$ blocks of type $X$ and $2h$ of
type $Y$.

Put

$$M=2^p-1=4^m-1,\qquad G=M/3.$$

At the chosen phase, $A_0=1/3$, so $C=G$, $z=p/3=2h$, and
$\gcd(C,M)=G$. First take every block to be $Y$. Direct summation gives

$$
D_Y=\sum_{\ell=0}^{m-1}2^{p-2-2\ell}(2\ell+3),
\qquad
z+D_Y=\frac{11G}{3}.
$$

Replacing the $Y$ block at position $\ell$ by $X$ decreases $D$ by exactly

$$2^{p-1-2\ell}=2\cdot4^{m-1-\ell}.$$

Thus, for a set $R\subset\{0,\ldots,m-1\}$ of $h$ selected exponents,

$$z+D=\frac{11G}{3}-2\sum_{t\in R}4^t.$$

Theorem 25 would require $G\mid z+D$. Since
$0<2\sum_{t\in R}4^t<2G$, this congruence forces

$$
\sum_{t\in R}4^t=\frac G3
\quad\text{or}\quad
\sum_{t\in R}4^t=\frac{5G}{6}.
$$

The second value is not an integer because $G$ is odd. For the first, use
$m=3h$:

$$
\frac G3=\frac{4^{3h}-1}{9}
=7\sum_{j=0}^{h-1}4^{3j}.
$$

In base $4$, each separated factor $7$ contributes the digits $13$, so this
integer has digits equal to $3$. But a sum of distinct powers
$\sum_{t\in R}4^t$ has only base-4 digits $0$ and $1$. Equality is impossible.
$\square$

This proves the phase-integrality failure for an infinite family that accounts
for most of the finite-search cycles. The boundary reduction and further
all-period denominator results continue in
[`periodic-boundary-reduction.md`](periodic-boundary-reduction.md) and
[`periodic-denominator-families.md`](periodic-denominator-families.md).

## Exhaustive search through period 54

The Rust binary `search-framework/src/bin/periodic.rs` performs an
integrality-first exhaustive enumeration:

1. Lemma 28 generates only self-consistent finite-state slope cycles.
2. Theorem 25 rejects words whose phase value can never be integral.
3. Surviving boundary cases, if any, are retained for exact checking.

Command:

```bash
cd search-framework
cargo run --release --bin periodic -- --min-period 1 --max-period 54
```

Result:

| period | slope-cycle representations | exact integer candidates |
|---:|---:|---:|
| 1--5 | 0 | 0 |
| 6 | 6 | 0 |
| 7--11 | 0 | 0 |
| 12 | 30 | 0 |
| 13--17 | 0 | 0 |
| 18 | 186 | 0 |
| 20 | 4 | 0 |
| 21 | 24 | 0 |
| 24 | 990 | 0 |
| 30 | 6,006 | 0 |
| 36 | 37,218 | 0 |
| 40 | 4 | 0 |
| 42 | 233,088 | 0 |
| 48 | 1,470,942 | 0 |
| 54 | 9,374,208 | 0 |
| all other periods $\le54$ | 0 | 0 |

All **11,122,706** nonzero cycle representations failed the phase-integrality
divisibility condition. Repeated shorter words may appear at a multiple of
their minimal period, so this total deliberately overcounts distinct words.
That does not affect the conclusion for minimal periods through 54.

The Rust counts at periods 6 and 12 are regression-tested. Its finite-state
generator was also cross-checked against the independent Python implementation,
which in turn was cross-checked against direct enumeration of all $3^p$ words
through period 12.

### Proper-divisor witness phenomenon

Every failed cycle through period 54 is already rejected modulo a factor coming
from a **proper divisor** $k\mid p$:

$$
\gcd\!\left(\gcd(C,2^p-1),\,2^k-1\right)
\nmid z+D.
$$

Examples:

| period $p$ | first witness periods $k$ observed |
|---:|---|
| 6, 12 | 3 |
| 18 | 3, 9 |
| 21 | 3, 7 |
| 24 | 3, 4, 8, 12 |
| 30 | 3, 5, 15 |
| 42 | 2, 3, 7, 21 |
| 48 | 3, 4, 8, 12, 16, 24 |
| 54 | 3, 6, 9, 27 |

**Computational conjecture.** Every nonzero self-consistent slope cycle has such
a proper-divisor witness. A proof would exclude all eventually periodic digit
orbits by induction on the period. The current data verifies this only through
54; it is not promoted to a theorem.

## Classification and limitation

**Theorem:** Theorems 25 and 29, plus Lemma 28.

**Computational evidence:** no eventually periodic nonzero digit word of period
at most 54 can occur on an integer orbit.

**Open:** prove the divisibility obstruction fails for every nonzero admissible
periodic word—possibly through the proper-divisor conjecture—or find the first
exact word that passes it. Even an exact word would initially give a
counterexample from an arbitrary state; reachability from $b_1=m$ would remain
a separate requirement.
