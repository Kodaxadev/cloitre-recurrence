# Exact gate multiplicity

Retain the arbitrary-gate notation, including

\[
x=\rho+jH,\qquad H=2^{k+r+3},
\]

and let \(\mathcal F\) be the exact candidate set.

## Lemma 110 (exact multiplicity)

Put

\[
\mu=\min\left\{\left\lfloor\frac d2\right\rfloor,
\left\lfloor\frac{2d'}H\right\rfloor\right\}.
\]

Then

\[
\mathcal F=\{f+t2^{k+1}:-j\le t\le\mu\},
\qquad |\mathcal F|=1+j+\mu. \tag{20.1}
\]

Indeed, replacing \(f\) by \(f+t2^{k+1}\) replaces

\[
A\mapsto A-2t,\qquad d\mapsto d-2t,\qquad x\mapsto x+tH.
\]

The parent bounds \(U+4\le A-2t\le n+2\) are exactly

\[
1-e\le t\le\lfloor d/2\rfloor.
\]

The child bounds \(1\le x+tH\le G+r-3\), using
\(x=\rho+jH\) and \(G+r-3-x=2d'\), are exactly

\[
-j\le t\le\lfloor2d'/H\rfloor.
\]

Their intersection initially has lower endpoint
\(\max\{1-e,-j\}\). Moreover,

\[
eH-x=
2^{r+2}\bigl((2^k-1)n+2^{k+2}-k-4\bigr)
+n+k+r+4>0.
\]

Hence \(x=\rho+jH\le eH\), so \(j\le e-1\); the parent residue bound never
truncates the lower candidates. This completes the stated interval.
\(\square\)

## Corollary 111 (displacement budget)

\[
\bigl(|\mathcal F|-1\bigr)H\le D'-3-\rho. \tag{20.2}
\]

Indeed, \(\mu H\le2d'\), and
\(D'-3-\rho=jH+2d'\). \(\square\)

Every missed canonical window creates one actual lower candidate, so
unbounded \(j\) forces unbounded multiplicity. Only the upper part can be
truncated, by the parent defect.

## Corollary 112 (upper-nonunique two-block ceiling)

If \(d\ge2\), \(2d'\ge H\), and the child block has length \(\ell\), then

\[
2^{k+r+\ell+2}<n'+\ell+4. \tag{20.3}
\]

Indeed, at the child start \(A'=U'+d'+4\), while the failed stopping test
before its length-\(\ell\) block gives
\(2^\ell A'<n'+\ell+4\). Since \(d'\ge H/2\),
\(2^{\ell-1}H< n'+\ell+4\), which is (20.3). \(\square\)
