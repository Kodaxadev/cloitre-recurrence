# Entry ridge and rebound cascade

This note records three unconditional results obtained after the initial research
pass. They do **not** prove stabilization. Their value is to narrow the shape of
any counterexample.

## Notation

Write

$$b_n=q_n n+r_n,\qquad 0\le r_n<n,$$

and let $a_n=\Delta q_n=q_{n+1}-q_n\in\{-1,0,+1\}$ after entry into
$b_n<n^2$. A state is absorbing exactly when $r_n=q_n$.

## Lemma 21 (entry ridge)

Let $n_0\ge3$ be the first index for which $b_{n_0}<n_0^2$. Then

$$q_{n_0}\in\{n_0-2,n_0-1\}.$$

### Proof

Minimality gives $b_{n_0-1}\ge(n_0-1)^2$. The recurrence is
non-decreasing, so

$$(n_0-1)^2\le b_{n_0}<n_0^2.$$

Dividing by $n_0$ and taking floors gives

$$n_0-2\le q_{n_0}\le n_0-1.$$

Both quantities are integers. $\square$

This is stronger than the previously used entry statement $q_{n_0}<n_0$:
every reachable orbit enters the division-free regime on its top two quotient
levels. It is a reachability constraint, not a statement about arbitrary
admissible $(n,q,r)$ states.

## Theorem 22 (exact rebound cascade)

Suppose $a_n=-1$ and put

$$h=q_n-2r_n,$$

so $1\le h\le q_n$. Immediately after the down-step, and after $k\ge0$
subsequent up-steps, define the deficit

$$\delta_k=(n+1+k)-r_{n+1+k}.$$

As long as those $k$ up-steps occur,

$$q_{n+1+k}=q_n-1+k$$

and

$$\boxed{\delta_k=2^k(h+q_n+2)-q_n-k-2.}$$

The next step is an up-step if and only if

$$\boxed{n+1\ge
2^{k+1}(h+q_n+2)-q_n-2k-4.}$$

Consequently, $s\ge1$ consecutive up-steps after the down-step are forced by

$$n+1\ge(2^{s+1}-1)q_n+2^{s+1}-2s-2.$$

In particular,

$$a_n=-1,\quad n\ge7q_n+1
\quad\Longrightarrow\quad
(a_{n+1},a_{n+2})=(+1,+1).$$

Thus sufficiently deep in the low-quotient regime, a loss of one quotient unit
forces a gain of two.

### Proof

The down-step gives

$$q_{n+1}=q_n-1,\qquad r_{n+1}=n+1-h,$$

so $\delta_0=h$. If the next transition is up, then

$$
\begin{aligned}
\delta_{k+1}
&=(n+2+k)-r_{n+2+k}\\
&=2\delta_k+(q_n-1+k)+2\\
&=2\delta_k+q_n+k+1.
\end{aligned}
$$

Induction solves this recurrence as

$$\delta_k=2^k(h+q_n+2)-q_n-k-2.$$

At index $N=n+1+k$, an up-step occurs exactly when
$2r_N-q_N\ge N+1$. Substituting
$r_N=N-\delta_k$ and $q_N=q_n-1+k$ reduces this to

$$n+1\ge2\delta_k+q_n,$$

which is the displayed exact condition. Since $h\le q_n$, the condition for
the $s$-th up-step is implied by

$$n+1\ge(2^{s+1}-1)q_n+2^{s+1}-2s-2.$$

The right side increases with the step number, so this forces all preceding
up-steps as well. Taking $s=2$ gives $n+1\ge7q_n+2$, equivalently
$n\ge7q_n+1$. $\square$

## Corollary 23 (bounded quotient forces stabilization)

If $(q_n)$ is bounded, then the orbit stabilizes. Equivalently, every
non-stabilizing orbit has unbounded quotient:

$$\boxed{\text{non-stabilizing}\quad\Longrightarrow\quad
\sup_n q_n=\infty.}$$

### Proof

Assume $q_n\le Q$ from some point onward. Once $n\ge7Q+1$, every down-step
is followed by two up-steps by Theorem 22. These three-step blocks are disjoint,
because their last two steps are up-steps. If there were infinitely many
down-steps, every block would contribute a net quotient gain of one, while all
steps outside the blocks are zero or up. This contradicts $q_n\le Q$.

There are therefore only finitely many down-steps. Boundedness then also permits
only finitely many up-steps, since

$$q_n=q_N+\#\{\text{up-steps}\}-\#\{\text{down-steps}\}.$$

Hence $q_n$ is eventually constant. The exact doubling law then becomes
$e_{n+1}=2e_n$. But the state window gives

$$-q_n\le e_n=r_n-q_n\le n-1-q_n,$$

which grows only linearly, whereas a nonzero value doubled forever grows
exponentially. Thus $e_n=0$ at some index, which is exactly absorption. $\square$

## What this does and does not achieve

The preceding corollary combines with the ratchet theorem from
`partial-proofs.md` to give a stronger dichotomy.

## Theorem 24 (quotient dichotomy)

Every orbit satisfies exactly one of the following:

1. it stabilizes, and $q_n$ is eventually constant; or
2. it does not stabilize, and $q_n\to\infty$.

### Proof

Only the second implication remains. Suppose the orbit does not stabilize.
Corollary 23 says $(q_n)$ is unbounded. Assume for contradiction that it does
not tend to infinity. Then some fixed $Q$ satisfies $q_n\le Q$ at arbitrarily
large indices $n$.

For each such $n$, let $s\le n$ begin the final low-quotient window: either $s$
is the entry index, or $s-1$ is the last index before $n$ with

$$3q_{s-1}>s,$$

and $3q_k\le k+1$ for every $k\in[s,n]$. In the second case,
$q_s\ge q_{s-1}-1>s/3-1$. The ratchet theorem gives

$$Q\ge q_n\ge q_s-1>s/3-2.$$

Thus every such window start satisfies $s<3(Q+2)$, apart from the one fixed
entry index, which is also bounded.

Consequently there can be no high-quotient index $k$ with
$3q_k>k+1$ beyond a fixed bound: any later occurrence of $q_n\le Q$ would have
a final window start after $k$, contradicting the bound on $s$. The entire tail
therefore lies in the low-quotient regime.

Apply the ratchet theorem from any tail index $j$. It gives
$q_k\ge q_j-1$ for every $k\ge j$. Since $(q_n)$ is unbounded, for every $H$
there is a tail index $j$ with $q_j\ge H+1$, after which $q_k\ge H$ forever.
Hence $q_n\to\infty$, contradicting the assumption. $\square$

Therefore a counterexample must grow superlinearly:

$$q_n\to\infty
\quad\Longrightarrow\quad
\frac{b_n}{n}=q_n+\frac{r_n}{n}\to\infty.$$

These results rule out a counterexample with a bounded, eventually periodic, or
recurrently small quotient. They also show that every counterexample must
contain infinitely many up-steps. They do not prove that $q_n/n$ stays away
from zero, that down-steps occur infinitely often, or that the capture state
$e_n=0$ is forced.

## Lemma 26 (zero-run bound)

Suppose an orbit has not absorbed. Any run of $L$ consecutive zero quotient
changes ending at an index at most $N$ satisfies

$$\boxed{L\le\lfloor\log_2 N\rfloor.}$$

### Proof

During a zero-step the exact law is $e_{k+1}=2e_k$. If a run starts at $j$,
then

$$e_{j+L}=2^L e_j.$$

The orbit has not absorbed, so the integer $e_j$ is nonzero and
$|e_j|\ge1$. The state window at the end of the run gives

$$|e_{j+L}|=|r_{j+L}-q_{j+L}|\le j+L\le N.$$

Therefore $2^L\le N$. $\square$

## Theorem 27 (quantitative pre-absorption growth)

Let $n_0$ be the entry index from Lemma 3. At every index
$n\ge\max(n_0,4)$ reached before absorption,

$$\boxed{
q_n\ge
\frac{n}{3(\lfloor\log_2 n\rfloor+1)}
-\frac{n_0}{3}-3.
}$$

Consequently, every counterexample satisfies

$$q_n=\Omega_m\!\left(\frac{n}{\log n}\right),
\qquad
b_n=\Omega_m\!\left(\frac{n^2}{\log n}\right).
$$

### Proof

Put $H=\lfloor\log_2 n\rfloor$. First consider any interval of digit indices
$[u,n)$ on which

$$8q_k\le k.$$

Let $E$ be the number of nonzero digits and $Z$ the number of zero digits in
that interval. There are at most $E+1$ zero-runs, and Lemma 26 bounds each by
$H$. Hence

$$n-u=E+Z\le E(H+1)+H,$$

so

$$E\ge\frac{n-u-H}{H+1}.$$

Every down-step in the interval satisfies $k\ge8q_k\ge7q_k+1$ whenever
$q_k\ge1$; a down-step is impossible when $q_k=0$. Theorem 22 therefore pairs
each down-step with the next two up-steps. These triples are disjoint. At most
one triple can be cut off by the right endpoint. If $U$ and $D$ count up- and
down-steps, this gives $U\ge2D-2$, and therefore

$$q_n-q_u=U-D=E-2D\ge\frac{E-4}{3}.$$

Combining the last two displays,

$$q_n\ge q_u+\frac{n-u-H}{3(H+1)}-\frac43. \tag{27.1}$$

Now choose $u$ immediately after the last index $h<n$ with $8q_h>h$. If no
such index exists after entry, take $u=n_0$. By construction, the interval
$[u,n)$ satisfies the deep-regime condition.

In the first case, $u=h+1$ and one quotient step gives

$$q_u\ge q_h-1>\frac{h}{8}-1=\frac{u}{8}-\frac98.$$

For $n\ge4$, $H\ge2$ and

$$\frac18\ge\frac{1}{3(H+1)}.$$

Substitution in (27.1) therefore gives

$$q_n\ge\frac{n}{3(H+1)}-3.$$

In the second case, (27.1) with $u=n_0$ and $q_{n_0}\ge0$ gives

$$q_n\ge\frac{n}{3(H+1)}-\frac{n_0}{3}-2.$$

The displayed theorem uses the weaker common constant. Finally
$b_n=q_nn+r_n\ge q_nn$, which gives the quadratic-over-logarithmic bound.
$\square$

The logarithm is the remaining loss in this argument. Removing it requires
more than the fact that $e$ doubles during zero-runs: one must control how small
$|e|$ can become after a quotient change, or prove that down-steps recur with
positive density.
