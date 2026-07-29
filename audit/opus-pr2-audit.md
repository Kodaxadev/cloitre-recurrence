# Independent AI audit of PR #2 at `55d0d6d`

## Identity and evidence boundary

The supplied audit reviewed branch `research/safe-checkpoint-monotonicity` at

```text
55d0d6ddc7b0f82dfcbdf67119bf28b082b80053
```

Its source text was 11,256 bytes with SHA-256

```text
bff8405e1b6122128e0a55450d9c37607d1a3fc31888737acc9d8f7e245dfe7f
```

The reviewer worked read-only and reported building scratch verifiers from
Lemma 42's safe map without importing repository implementations or
constants. The scratch source and its full outputs were not supplied as
tracked artifacts. This report is therefore independent review evidence, not
a self-contained reproduction package or human peer review.

## Independently reported checks

The reviewer reported:

- a complete \(10^7\)-start enumeration with zero unresolved starts and an
  exact match to all 106 omissions through 1823;
- 273,440 unit-wrap gates checking the candidate interval, parity,
  reconstruction, and uniqueness iff condition;
- 44,448 arbitrary-block gates checking Lemmas 92--94 and both uniqueness
  classes;
- a full bounded determinant grid for Corollary 95;
- 1,313,400 zero epochs checking Lemma 53's least-index characterization;
- the unique Lemma 87 parent-boundary triple and its terminal raw path;
- 633,890 real ridges checking Lemma 73 and 623,110 adjacent pairs checking
  Corollary 74;
- 41,948 interior gates checking Corollary 102's exhaustive split.

No defective theorem statement was reported. The reviewer classified the
post-freeze imports T58 and L63 as not audited, and identified L100 as the
highest-value target for a second symbolic pass.

## Findings reconciled in the repository

### Corollary 86

The reviewer noted that the lower-neighbor proof did not explicitly check
the parent lower bound. The proof now records

\[
s'>H\Longrightarrow2^{r+2}(s-4)>n+r+5,
\]

which makes \(s-4\ge1\) automatic.

### Lemma 87

The displayed rational list has two formally positive integer evaluations at
\(r=1\). The second comes from the even-\(r\), \(\delta_0=5\) branch and is
incompatible with \(r=1\). Both the research proof and compact manuscript now
state this parity label explicitly.

### Lemma 100

The original statement required four consecutive parent-boundary starts of
one block length, while the proof and regression test used only three starts
and equality of the first two block lengths. A line-by-line dependency check
shows that equations (98.2)--(98.3) are local and require exactly:

1. three consecutive parent-boundary starts;
2. equal positive-block lengths at the first two starts.

Lemma 100 is now stated in this stronger local form. The Python and native
Rust checks exhaust arbitrary bounded-quotient starts through \(n\le700\)
and find 30 three-start parent-boundary runs. Five also have equal first-two
block lengths and therefore satisfy the full lemma hypothesis; both
implementations confirm strict gap increase on those five. This eliminates
the prior zero-coverage concern without conflating the broader and
theorem-applicable counts.
The compact proof also states why \(\delta'=-1\) forces
\(\delta=1-d_j\in\{0,1\}\).

## Remaining audit frontier

The review leaves three distinct obligations:

1. audit T58 and L63 before treating T77 as independently reviewed;
2. give C89--T90 a fully quantified asymptotic pass;
3. archive a reproducible implementation or certificate for the independent
   \(10^7\) enumeration if K6 is to be independently reproducible from the
   repository.

The original stabilization conjecture remains open.

Follow-up: [`continuation-t58-l63.md`](continuation-t58-l63.md) closes item
1, and [`continuation-c89-t90.md`](continuation-c89-t90.md) closes item 2.
Item 3 remains open.
