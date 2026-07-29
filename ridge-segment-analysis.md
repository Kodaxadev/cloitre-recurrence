# Terminal structure of a post-down ridge segment

This note continues Corollary 61 and Lemma 62. It classifies the final
sign change before the next quotient down-step and isolates a second
necessary feature of a sublinear infinite-down counterexample.

## Lemma 63: terminal negative-suffix map

After entry, consider a finite digit interval beginning at a state with
\(e>0\), containing only zero- and up-steps, and ending immediately before
a down-step. Suppose the interval contains at least one up-step. Let \(t\)
be the index of its last up-step and put

\[
Q=q_{t+1},\qquad v=-e_{t+1}.
\]

Then \(v\) is a positive integer with

\[
1\le v\le Q. \tag{63.1}
\]

If \(z\) is the number of zero digits after that up-step and before the
down-step, then

\[
e_{t+1+j}=-2^jv\qquad(0\le j\le z), \tag{63.2}
\]

\[
2^zv\le Q<2^{z+1}v,\qquad
z=\left\lfloor\log_2\frac Qv\right\rfloor. \tag{63.3}
\]

At the terminal down-step, if

\[
h_{\mathrm{next}}=q-2r,
\]

then

\[
\boxed{\displaystyle
h_{\mathrm{next}}=2^{z+1}v-Q,\qquad
1\le h_{\mathrm{next}}\le Q.} \tag{63.4}
\]

Thus the last up-step and its negative zero suffix form an exact dyadic
remainder map from \((Q,v)\) to the next post-down ridge parameter.

### Proof

The interval starts with positive \(e\), while a down-step requires

\[
q+2e<0
\]

and hence negative \(e\). A zero-step doubles \(e\) and cannot change its
sign. Therefore an up-step changes the sign. Once \(e<0\), another up-step
is impossible because \(q+2e<q\le n<n+1\). Thus the sign-changing up-step
is unique and is the last up-step.

At index \(t\),

\[
e_{t+1}=2e_t-(t+2)=-v.
\]

The up threshold is \(q_t+2e_t\ge t+1\), which becomes
\(v\le q_t+1=Q\); negativity gives \(v\ge1\). Subsequent zero-steps leave
the quotient equal to \(Q\) and double the negative coordinate, proving
(63.2).

At a state with \(e=-2^jv\), the digit is zero exactly while

\[
Q-2^{j+1}v\ge0.
\]

The upper zero threshold is automatic because \(Q\le n\). The digit becomes
a down-step at \(j=z\). The last safe state and the terminal failure
therefore give (63.3). At that terminal state,

\[
r=Q-2^zv,
\]

so

\[
h_{\mathrm{next}}
=Q-2r=2^{z+1}v-Q.
\]

The two inequalities in (63.3) give the bounds in (63.4). \(\square\)

## Corollary 64: unbounded zero plateaus

In a sublinear counterexample with infinitely many down-steps, use the
subsequence of post-down segments from Corollary 61. Let \(M_j\) be the
longest run of consecutive zero digits in the \(j\)-th segment. Then

\[
M_j\longrightarrow\infty \tag{64.1}
\]

along a further subsequence.

More quantitatively, if the segment has length \(L_j\) and \(U_j\) up-steps,
then

\[
M_j\ge\frac{L_j-U_j}{U_j+1}. \tag{64.2}
\]

At the beginning \(s\) of any such zero run of length \(M\),

\[
2^M|e_s|\le s+M. \tag{64.3}
\]

### Proof

The \(L_j-U_j\) zero digits form at most \(U_j+1\) runs, proving (64.2).
Corollary 61 gives \(U_j/L_j\to0\), while its forced rebound bound gives
\(U_j\to\infty\). Hence the right side of (64.2) tends to infinity.

Along a zero run, \(e_{s+M}=2^Me_s\). The state window after entry gives
\(|e_{s+M}|\le s+M\), proving (64.3). \(\square\)

## Remaining obstruction

Lemma 63 completely determines the negative suffix, but the long zero
plateau supplied by Corollary 64 may occur earlier while \(e>0\). A
contradiction still requires controlling how a small positive integer
created after an up-step can survive long enough to feed the next ridge.
