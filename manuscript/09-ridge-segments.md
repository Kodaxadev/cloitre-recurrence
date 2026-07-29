# Terminal structure of post-down ridge segments

## Lemma 63 (terminal negative suffix)

Let a finite no-down segment start with \(e>0\) and end immediately before
a down-step. Let \(t\) be its last up-step and set

\[
Q=q_{t+1},\qquad v=-e_{t+1}.
\]

Then \(1\le v\le Q\). If \(z\) zero digits follow before the down-step,
then

\[
e_{t+1+j}=-2^jv,\qquad
2^zv\le Q<2^{z+1}v. \tag{9.1}
\]

Consequently

\[
z=\left\lfloor\log_2\frac Qv\right\rfloor,\qquad
h_{\rm next}=2^{z+1}v-Q\in[1,Q]. \tag{9.2}
\]

Indeed, only an up-step can take \(e\) from positive to negative, and no
later up-step is possible. The up threshold gives \(v\le Q\). Each
subsequent zero doubles the negative coordinate until
\(Q+2e<0\), which gives (9.1); substituting the terminal remainder into
\(h=q-2r\) gives (9.2). \(\square\)

## Corollary 64 (unbounded zero plateaus)

In a sublinear infinite-down counterexample, some post-down segments contain
zero runs whose lengths tend to infinity.

For a segment of length \(L\) with \(U\) up-steps, its zero digits occupy at
most \(U+1\) runs. Hence its longest zero run \(M\) satisfies

\[
M\ge\frac{L-U}{U+1}. \tag{9.3}
\]

Corollary 61 supplies a subsequence with \(L\to\infty\), \(U/L\to0\), and
\(U\to\infty\), so the right side tends to infinity. During a zero run
beginning at \(s\),

\[
2^M|e_s|\le s+M, \tag{9.4}
\]

because zero digits double \(e\) and the terminal state window bounds its
absolute value. \(\square\)

The long zero run need not be the terminal negative suffix of Lemma 63; it
may occur earlier with positive \(e\). This is the unresolved case.

## Lemma 65 (down-epoch defect coding)

At a down-step \(d\), set

\[
h_d=q_d-2r_d,\qquad B_d=q_d+h_d+2=2-2e_d.
\]

Then

\[
B_d=\sum_{k>d}\frac{(1-a_k)(k+2)}{2^{k-d}}. \tag{9.5}
\]

All terms are nonnegative: up-, zero-, and down-steps have coefficients
zero, one, and two. For consecutive down-steps \(d<d'\),

\[
B_d=
\sum_{\substack{d<k<d'\\a_k=0}}\frac{k+2}{2^{k-d}}
+\frac{2(d'+2)+B_{d'}}{2^{d'-d}}. \tag{9.6}
\]

Indeed, multiply Theorem 39's future-digit identity at \(d\) by two and
subtract it from the all-up sum

\[
\sum_{k>d}\frac{k+2}{2^{k-d}}=d+4.
\]

This proves (9.5); splitting its nonnegative series at \(d'\) proves
(9.6). \(\square\)
