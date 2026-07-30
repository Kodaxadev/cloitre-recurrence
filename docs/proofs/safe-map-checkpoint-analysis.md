# Checkpoint monotonicity for the two-counter safe map

This note sharpens the exact eventually-no-down reduction. It proves two
structural statements; it does not prove that every safe path terminates.

## Setup

For an index \(N\ge2\), let \(P(N)\) denote:

> Every quotient-zero safe-map state with \(1\le e<N\) eventually enters
> the terminating strip.

The state after a finite prefix need not still have quotient zero. Lemma 41
is what permits its quotient to be reset to zero without shortening a
positive no-down continuation.

## Theorem 46: checkpoint monotonicity

For every \(N\ge2\),

\[
P(N+1)\Longrightarrow P(N).
\]

Equivalently, if an infinite quotient-zero safe path exists at \(N\), one
exists at every later index. Thus the set of failing starting indices, if
nonempty, is an upward-closed interval of integers.

### Proof

Suppose a quotient-zero state \((N,0,e)\) has an infinite positive no-down
continuation. Its first transition reaches a valid state

\[
(N+1,q',e'),\qquad q'\in\{0,1\},\qquad 0<e'<N+1,
\]

whose positive no-down continuation is still infinite. By quotient-zero
dominance (Lemma 41), \((N+1,0,e')\) follows the same digit and \(e\)
sequence for at least as long. In particular, for every finite length it
has a continuation of that length, so its deterministic continuation is
infinite. This proves failure at \(N+1\). Iteration proves failure at every
later index, and the stated implication is its contrapositive. \(\square\)

### Certified consequence

The independently regenerated safe-sweep certificate proves \(P(10^6)\):
all \(999{,}999\) initial residues are eliminated by index \(1{,}009{,}019\).
Theorem 46 therefore makes the same certificate prove \(P(N)\) for every

\[
2\le N\le10^6.
\]

Lemma 41 then rules out an infinite positive no-down continuation from any
valid quotient at any of those indices, not only from quotient zero.

This remains a finite computer-assisted statement. Theorem 46 also changes
the uniform proof target: it is enough to prove \(P(N_j)\) on any unbounded
sequence of checkpoints \(N_j\), rather than separately at every index.

## Lemma 47: signed-distance form

In Lemma 43's coordinates put

\[
H=h+U+2,\qquad s=e+H=n+2,\qquad x=H-e+1=s+1-2e.
\]

Every safe transition is exactly

\[
\begin{array}{rcll}
(s,x,U)&\mapsto&(s+1,\,2x-s,\,U),&x\ge U+3,\\
(s,x,U)&\mapsto&(s+1,\,2x+s,\,U+1),&x\le0.
\end{array}
\]

The path terminates precisely when

\[
1\le x\le U+2.
\]

At every valid state,

\[
|x|<s,\qquad x\equiv s+1\pmod2.
\]

### Proof

The zero condition \(e+U+2\le H\) is \(x\ge U+3\). Under the zero update
\((e,H)\mapsto(2e,H-e+1)\),

\[
x'=(H-e+1)-2e+1=2x-s.
\]

The wrap condition \(e>H\) is \(x\le0\). Under
\((e,H)\mapsto(e-H,2H+1)\),

\[
x'=(2H+1)-(e-H)+1=2x+s.
\]

Lemma 43's gap \(H-U-2<e\le H\) becomes
\(1\le x\le U+2\). Positivity of \(e,H\) gives \(|x|<s\), and the
definition \(x=s+1-2e\) gives the parity assertion. \(\square\)

## Corollary 48: parity of a least failure

If \(P(N)\) ever fails and \(N_*\) is the least failing index, then every
infinite quotient-zero witness at \(N_*\) has odd \(e\). If \(N_*\) is odd,
such a witness is not reachable from an original start \(b_1=m\).

### Proof

If an infinite witness at \(N_*\) had even \(e\), the valid quotient-zero
state

\[
(N_*-1,0,e/2)
\]

would take one safe zero-step to \((N_*,0,e)\). It would therefore have an
infinite continuation, contradicting the minimality of \(N_*\).

At every odd index \(n\ge3\), Corollary 9 gives even \(b_n\). Moreover

\[
b_n-e_n=q_n(n+1),
\]

so \(b_n\equiv e_n\pmod2\) when \(n\) is odd. Hence every reachable
\(e_n\) is even at an odd index, whereas a least-failure witness is odd.
\(\square\)

This does not exclude a least failure at an even index. It shows that the
uniform safe-map termination statement is stronger than the
reachability-restricted statement actually needed for the recurrence.

## Lemma 49: quotient clearance

Along a quotient-zero safe path, let \(U_n\) be its current quotient. At
each zero step define the nonnegative slack

\[
\sigma_n=n-U_n-2e_n.
\]

Fix an integer \(Q\ge0\) for which \((N,Q,e_N)\) is valid. The path begun
with quotient \(Q\) follows the same digits and \(e\)-values through a
given prefix if and only if

\[
\sigma_n\ge Q
\]

at every zero step in that prefix. Wrap steps impose no additional
condition.

Consequently, if the quotient-zero path is infinite and

\[
\delta=\min_{\{n:a_n=0\}}\sigma_n,
\]

then every valid initial quotient \(0\le Q\le\delta\) has the same infinite
positive no-down continuation.

### Proof

As long as the digit and \(e\) sequences agree, the two quotients differ
by the constant \(Q\). A wrap is characterized by \(2e_n>n+2\),
independently of the quotient. A zero is safe for the shifted path exactly
when

\[
U_n+Q+2e_n<n+1,
\]

which, by integrality, is \(\sigma_n\ge Q\). Induction proves the prefix
statement. An infinite path has zero steps because Lemma 44 forbids an
infinite wrap run; hence the displayed minimum exists in the
well-ordered nonnegative integers. \(\square\)

## Theorem 50: boundary forced at an even least failure

Suppose \(N_*\) is the least index for which \(P(N_*)\) fails and \(N_*\)
is even. Every infinite witness \(e\) at \(N_*\) satisfies

\[
e\ \text{odd},\qquad 2e\le N_*,
\]

and its path has a zero step with

\[
n-U_n-2e_n=0. \tag{50.1}
\]

Thus the only remaining even-index least-failure mechanism begins with a
zero and later reaches the exact lower edge of the forbidden strip.

### Proof

Direct evaluation gives \(P(2),P(4),P(6)\). In increasing order of
starting residue \(e=1,\ldots,N-1\), the numbers of safe transitions before
termination are

\[
\begin{array}{c|c}
N&\text{safe-transition counts}\\ \hline
2&(1)\\
4&(2,4,0)\\
6&(4,1,11,0,2).
\end{array}
\]

These nine finite traces use only the displayed safe-map rule, not the
large certificate. Hence assume \(N_*\ge8\).
Corollary 48 makes \(e\) odd.

First suppose the initial step is a wrap. Put

\[
f=e-\frac{N_*+2}{2}.
\]

Then \(1\le f\le N_*/2-2\). The state \((N_*,1,f)\) takes a safe zero
step to exactly the state reached when \((N_*,0,e)\) wraps, so it has an
infinite continuation.

If \(f\) is even, \((N_*-1,0,f/2)\) zero-steps to
\((N_*,0,f)\), which dominates \((N_*,1,f)\). If \(f\) is odd, the valid
state

\[
\left(N_*-1,0,\frac{f+N_*+1}{2}\right)
\]

wraps directly to \((N_*,1,f)\). Either case produces failure at
\(N_*-1\), a contradiction. Hence the witness starts with a zero, so
\(2e\le N_*\).

Let \(\delta\) be the minimum zero-step slack from Lemma 49. If
\(\delta\ge1\), then \((N_*,1,e)\) has the same infinite continuation.
Because \(e\) is odd and \(e\le N_*/2\), the valid state

\[
\left(N_*-1,0,\frac{e+N_*+1}{2}\right)
\]

wraps to \((N_*,1,e)\), again contradicting minimality. Therefore
\(\delta=0\), which is (50.1). \(\square\)

## Lemma 51: accelerated zero-epoch map

At any safe zero step, put

\[
W=n-U,\qquad d=W-2e\ge0.
\]

After taking that zero step, let \(k\ge0\) be the length of the maximal
following wrap run: the least integer \(j\ge0\) such that

\[
2^{j+1}(U+d+4)\ge W+U+j+5. \tag{51.1}
\]

At the first non-wrap state,

\[
W^+=W+1,\qquad U^+=U+k,
\]

and the candidate slack for another zero step is exactly

\[
d^+
=2^{k+1}(U+d+4)-W-2U-2k-7. \tag{51.2}
\]

If \(d^+\ge0\), that state takes a zero step with slack (51.2); if
\(d^+<0\), the safe path terminates there. Thus (51.1)--(51.2) accelerate
one zero step and its entire wrap run into one return-or-termination test.

### Proof

The initial zero sends \(W\) to \(W+1\), leaves \(U\) fixed, and sends
\(e\) to \(W-d\). Hence the new gap \(h=W+1-e\) is \(d+1\), and

\[
D_0=h+U+3=U+d+4.
\]

After \(j\) wraps, Lemma 44 gives

\[
D_j=2^j(U+d+4),\quad U_j=U+j,\quad
h_j=D_j-U-j-3,
\]

while \(W+1=e_j+h_j\) remains fixed. The state wraps exactly when

\[
e_j>h_j+U_j+2,
\]

which becomes

\[
2^{j+1}(U+d+4)<W+U+j+5.
\]

The exponential left side eventually exceeds the linear right side, so
the least failing index is the stated \(k\). At that state,

\[
h_k-e_k=2h_k-(W+1)
=2^{k+1}(U+d+4)-W-2U-2k-7.
\]

Nonnegative gap is the zero condition \(e_k\le h_k\); negative gap at a
state that no longer wraps lies in Lemma 43's terminating strip.
\(\square\)

## Corollary 52: exact exit from the zero-slack boundary

Suppose \(d=0\), so \(W=2e\), and the path survives to another zero
epoch. Then:

1. the intervening wrap run is nonempty;
2. the next zero slack \(d^+\) is odd and positive;
3. the residue at that next zero epoch is
   \[
   e^+=\frac{2e+1-d^+}{2}\le e;
   \]
4. equality \(e^+=e\) holds exactly when \(d^+=1\).

The local equality cases form the explicit infinite family

\[
e=(2^k-1)(U+4)-k,\qquad U\ge0,\quad k\ge1, \tag{52.1}
\]

where the boundary zero is followed by exactly \(k\) wraps and then a
zero step with the same residue and slack one.

If a later zero epoch is again on the boundary, its residue is strictly
larger than at the preceding boundary. More precisely, if \(\ell\) zero
transitions separate the two boundary epochs, then \(\ell\) is even and

\[
e_{\mathrm{new}}=e_{\mathrm{old}}+\frac{\ell}{2}. \tag{52.2}
\]

### Proof

After a boundary zero, \(W+1=2e+1\) is odd. The next state cannot take
another zero; if the path survives, it therefore wraps at least once.
Formula (51.2) is odd when \(d=0\), so survival to a zero makes
\(d^+\ge1\) odd. The residue formula and its equality condition follow
from \(2e^++d^+=W+1=2e+1\).
Once (51.1) holds it persists, since its left side doubles while its
right side adds one. For (52.1), the wrap inequality has margin \(e\) at
\(k-1\), so all earlier states wrap, while (51.2) equals one at \(k\).
This proves the family assertion.

Finally, \(W\) increases by one at each zero transition and is unchanged
by wraps. Boundary values of \(W=2e\) are even, so two distinct boundary
epochs are separated by a positive even number \(\ell\) of zero
transitions. Equation (52.2) follows. \(\square\)

## Remaining obstruction

Lemma 47 conjugates the surviving branch to centered doubling in the
expanding interval \((-s,s)\), with a one-sided forbidden interval
\([1,U+2]\). Theorem 45 forces \(U=\Omega(s/\log s)\) on an infinite
path, but a growing target does not by itself force a particular
deterministic orbit to hit it. No pointwise decreasing potential follows
from this coordinate change.

Theorem 50 isolates the escape hatch in the backward argument: at a
zero-slack state, increasing the starting quotient by one terminates rather
than reproducing the infinite path. Excluding infinite paths through these
exact boundary states would eliminate the even-index least-failure case.

Corollary 52 blocks naive descent: the first returning residue cannot
increase, but a later boundary can have larger residue. The smallest example is

\[
(n,U,e)=(14,0,7)\longrightarrow(18,2,8),
\]

with digits \(0,1,1,0\). Any global argument must therefore use more than
monotonicity of the boundary residue.
