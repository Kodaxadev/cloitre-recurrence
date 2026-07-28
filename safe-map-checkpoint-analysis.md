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

## Remaining obstruction

Lemma 47 conjugates the surviving branch to centered doubling in the
expanding interval \((-s,s)\), with a one-sided forbidden interval
\([1,U+2]\). Theorem 45 forces \(U=\Omega(s/\log s)\) on an infinite
path, but a growing target does not by itself force a particular
deterministic orbit to hit it. No pointwise decreasing potential follows
from this coordinate change.
