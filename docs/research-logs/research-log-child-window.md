# Research log: canonical child-boundary windows

## 1. Combining the two interior alternatives

At an interior parent start, Lemma 92 gives uniqueness exactly when

\[
x\le H,\qquad 2d'<H.
\]

The returned-residue equation and the parent parity imply

\[
x\equiv
2^{r+2}(n+k+4)-2^{k+r+2}n-n-k-r-4
\pmod H.
\]

Choosing the least positive representative \(\rho\) makes

\[
x=\rho+jH,\qquad
D'-3=\rho+jH+2d'
\]

for one \(j\ge0\). Thus both inequalities are equivalent to the single
window hit

\[
\rho\le D'-3<\rho+H.
\]

A miss is exactly nonuniqueness.

## 2. What the residue does not give for free

For fixed \(k,r\), the coefficient of \(n\) in the residue is odd, so
\(n\mapsto\rho\) permutes all classes modulo \(H\). This rules out a fixed
proper congruence class as the source of repeated child-boundary hits.

It does not imply equidistribution along one orbit: both \(k\) and \(r\)
change, and the orbit chooses a highly dependent subsequence of indices.
Any density argument based only on the permutation property would therefore
be heuristic.

## 3. Surviving target

The safe-map problem is now to prove that a hypothetical infinite path
cannot keep its successor gap in the first moving window at every unique
interior gate. Equivalently, prove that later-window misses occur often
enough to make the exact nonunique inequalities accumulate.

The first-window identity also gives \(2A'=n'+5-\rho\). Hence the next block
is unit exactly when \(2\rho\le n'+4\). A longer child block forces
\(H>(n'+4)/2\), and therefore an almost-logarithmic preceding gap. This is
a genuine inter-gate restriction and applies to every unique gate, including
one starting in the parent layer. Together with Theorem 91, it leaves the
exhaustive alternative of infinitely many nonunique gates or infinitely many
sparse long-block resets. Both remain compatible with the current block-count
lower bound. The disjoint reset gaps give the further count
\(O(N/\log N)\) through time \(N\); this zero-density fact still permits an
infinite renewal sequence.
