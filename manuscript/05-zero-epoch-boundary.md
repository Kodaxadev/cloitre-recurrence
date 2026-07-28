# Zero-epoch acceleration and the surviving boundary

Continue with the safe map of Lemmas 42--43. At a state taking a zero
step, define

\[
W=n-U,\qquad d=W-2e\ge0.
\]

Call such a state a zero epoch.

## Lemma 51 (accelerated zero-epoch map)

After a zero epoch, let \(k\) be the length of the maximal following wrap
run. It is the least \(j\ge0\) for which

\[
2^{j+1}(U+d+4)\ge W+U+j+5. \tag{5.1}
\]

At the first non-wrap state,

\[
W^+=W+1,\qquad U^+=U+k,
\]

and its candidate zero slack is

\[
d^+=2^{k+1}(U+d+4)-W-2U-2k-7. \tag{5.2}
\]

The path returns to a zero epoch exactly when \(d^+\ge0\); otherwise it
terminates at that state.

### Proof

The initial zero produces \(W+1\), residue \(W-d\), and hence gap
\(h=d+1\). Put \(D=h+U+3=U+d+4\). After \(j\) wraps, Lemma 44 gives

\[
D_j=2^jD,\qquad U_j=U+j,\qquad h_j=D_j-U-j-3,
\]

while \(W+1=e_j+h_j\) is fixed. The wrap inequality
\(e_j>h_j+U_j+2\) is precisely the strict reverse of (5.1).
At the first non-wrap state,

\[
h_k-e_k=2h_k-(W+1)=d^+.
\]

Nonnegative gap is the zero branch; negative gap, once the wrap
inequality has failed, is the terminating middle strip. \(\square\)

## Corollary 52 (zero-slack exit)

Suppose \(d=0\), so \(W=2e\), and the path survives to another zero
epoch. The intervening wrap run is nonempty, the next slack \(d^+\) is
odd and positive, and

\[
e^+=\frac{2e+1-d^+}{2}\le e.
\]

Equality holds exactly for \(d^+=1\). These local equality cases are the
explicit infinite family

\[
e=(2^k-1)(U+4)-k,\qquad U\ge0,\quad k\ge1, \tag{5.3}
\]

where exactly \(k\) wraps lead to a zero epoch with the same residue and
slack one.

If two boundary epochs are separated by \(\ell>0\) zero transitions,
then \(\ell\) is even and

\[
e_{\rm new}=e_{\rm old}+\frac{\ell}{2}. \tag{5.4}
\]

### Proof

After a boundary zero, \(W+1=2e+1\) is odd. Survival forces at least one
wrap, and (5.2) makes the next nonnegative slack odd. This proves the
first assertions. Setting \(d^+=1\) in (5.2) gives (5.3). Conversely,
(5.3) makes the wrap inequality strict through \(k-1\) and makes (5.2)
equal one at \(k\).

Every zero transition increments \(W\), while wraps leave it fixed.
Boundary values \(W=2e\) are even, proving (5.4). \(\square\)

## Limitation

The local inequality \(e^+\le e\) does not give a global descent between
boundary visits. For example, direct symbolic transitions give

\[
(14,0,7)\xrightarrow{0}(15,0,14)
\xrightarrow{1}(16,1,11)
\xrightarrow{1}(17,2,4)
\xrightarrow{0}(18,2,8).
\]

Both endpoints have zero slack, and the residue increased from \(7\) to
\(8\). Thus excluding the boundary mechanism in Theorem 50 requires a
global arithmetic argument, not monotonicity of the boundary residue.
