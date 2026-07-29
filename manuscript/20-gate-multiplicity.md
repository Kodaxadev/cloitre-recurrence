# Exact gate multiplicity

Retain the arbitrary-gate notation, including

\[
x=\rho+jH,\qquad H=2^{k+r+3},
\]

and let \(\mathcal F\) be the exact candidate set.

## Lemma 110 (exact multiplicity)

Put

\[
\lambda=\min\{e-1,j\},\qquad
\mu=\min\left\{\left\lfloor\frac d2\right\rfloor,
\left\lfloor\frac{2d'}H\right\rfloor\right\}.
\]

Then

\[
\mathcal F=\{f+t2^{k+1}:-\lambda\le t\le\mu\},
\qquad |\mathcal F|=1+\lambda+\mu. \tag{20.1}
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

Intersecting these integer intervals proves (20.1). \(\square\)

## Corollary 111 (displacement budget)

\[
\bigl(|\mathcal F|-1\bigr)H\le D'-3-\rho. \tag{20.2}
\]

Indeed, \(\lambda\le j\), \(\mu H\le2d'\), and
\(D'-3-\rho=jH+2d'\). \(\square\)

This quantifies both nonuniqueness mechanisms exactly. It does not exclude
repeated nonunique gates because the parent residue and defect windows can
truncate arbitrarily large canonical displacement.
