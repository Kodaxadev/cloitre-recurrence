# Cruthúnas adoption-gap audit

This is a read-only adoption inventory for Cloitre, the first case study for the
general OEIS research-governance harness. Cloitre-specific mathematics remains
in this repository; no recurrence, stabilization, language, prover, certificate,
or workflow assumption is promoted into Cruthúnas.

## 1. Audit identity

| Field | Value |
|---|---|
| Cloitre repository | `Kodaxadev/cloitre-recurrence` |
| Audited Cloitre source SHA | `ee9d052015e658a8941f237130ba4aa7df03d29c` |
| Required Cloitre base SHA | `d990512d386b6365e4b835a72ac634ce9ddda9f0` |
| Cruthúnas repository | `Kodaxadev/cruthunas` |
| Pinned framework SHA | `49840431d02e8c7cae7d35e82bf3fd4095dc397b` |
| Operating system | `Windows-11-10.0.26200-SP0` |
| Audit Python | `Python 3.14.3` |
| Framework checkout | Detached worktree at the pinned SHA |
| Installation command | `C:\Users\Justi\AppData\Local\Temp\cruthunas-audit-venv-4984043\Scripts\python.exe -m pip install --disable-pip-version-check -e C:\Users\Justi\Downloads\Alpha\cruthunas-4984043-audit` |
| Audit command | `C:\Users\Justi\AppData\Local\Temp\cruthunas-audit-venv-4984043\Scripts\cruthunas.exe adoption gaps --root . --json` |
| Run 1 UTC | `2026-08-01T15:38:41.1101826Z` to `2026-08-01T15:38:42.9779814Z` |
| Run 2 UTC | `2026-08-01T15:38:58.6117425Z` to `2026-08-01T15:38:59.7785006Z` |
| Determinism | Byte-identical and semantically identical |
| Canonical JSON encoding | UTF-8, keys sorted, compact separators, Unicode preserved |
| Canonical JSON SHA-256 | `20cdadadd84113a13ce1b74e8d08e8d560acd965fdfc3ac9b41967c56d44e0fb` |
| Captured raw bytes | 79,832-byte UTF-16LE PowerShell capture; SHA-256 `6e6fdea0a37948080eb19ac668cc594d64ca9eb306b5d6518f4a019c0d19565a` |
| Reporter findings | 95 |
| Reporter classification | 89 automatic; 6 manual |

The pinned reporter does not emit a severity field. The following is an explicit
auditor-assigned migration-risk classification, not framework output:

| Auditor severity | Count | Basis |
|---|---:|---|
| High | 7 | Two identifier/manual cases, four identity cases, and the legacy evidence-manifest decision |
| Medium | 16 | Ten missing governed paths and six unpinned workflow actions |
| Low | 72 | Lossless lexical padding suggestions, still subject to global mapping review |

Reporter categories were: 74 `historical_claim_ids`, 4
`identity_independence`, 1 `manual_migration`, 10 `project_structure`, and 6
`workflow_pinning`. Exit code 1 is the documented result when gaps exist; both
runs produced valid reports and did not fail operationally.

The audited source SHA is the clean pre-report head. This report was not fed
back into its own reporter input, which would create self-referential ID and
independence-language occurrences; the final report commit is recorded in the
PR update rather than misidentified as the audited source.

## 2. Executive verdict

**FRAMEWORK DEFECT — adoption reporter failed or produced demonstrably incorrect findings**

The raw output is deterministic and useful, and this report inventories all 95
emitted findings. It is not sufficient by itself for a complete migration:

1. `C2.1` is misread as the shorter automatic token `C2`, losing the `.1` and
   producing an incorrect canonical suggestion.
2. Affirmative independence language such as “independently regenerated and
   checked” is not reported.

Both defects have minimal deterministic reproductions in section 12. No
conclusion about complete historical-ID or identity coverage may rely on this
reporter version. Cloitre is not adopted, conformant, or promoted.

## 3. Full finding inventory

### Inventory conventions

For findings 1–74 the exact code is `claim_id.incompatible`, the category is
`historical_claim_ids`, and the reporter reason is that a lexical token fails
the canonical pattern `^[A-Z][0-9]{3,}$`. Except for findings 46 and 47, the
later mechanical action would be to retain the historical token as an alias and
register the padded canonical ID only after a global collision and meaning
review. The common dependency is an authorized project manifest, canonical
ledger, and reviewed ID map. Applying any mapping would alter reference and
provenance boundaries even when it does not alter the mathematical statement;
therefore no source text may be rewritten automatically.

| # | Reported mapping | Class | Risk | Every reported occurrence | Accuracy |
|---:|---|---|---|---|---|
| 1 | `K13` → `K013` | automatic | Low | `aperiodic-tail-analysis.md`<br>`audit/theorem-dependency.md`<br>`certificates/safe_n1000000.txt`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 2 | `T18` → `T018` | automatic | Low | `audit/cruthunas-adoption-plan.md`<br>`audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 3 | `K11` → `K011` | automatic | Low | `audit/evidence-manifest.md`<br>`audit/theorem-dependency.md`<br>`research-log.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 4 | `C19` → `C019` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 5 | `C20` → `C020` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 6 | `C23` → `C023` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 7 | `C9` → `C009` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 8 | `K1` → `K001` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 9 | `L12` → `L012` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 10 | `L21` → `L021` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 11 | `L26` → `L026` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 12 | `L28` → `L028` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 13 | `L3` → `L003` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 14 | `L33` → `L033` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 15 | `L4` → `L004` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 16 | `L40` → `L040` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 17 | `L41` → `L041` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 18 | `L42` → `L042` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 19 | `L43` → `L043` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 20 | `L44` → `L044` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 21 | `L8` → `L008` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 22 | `O1` → `O001` | automatic | Low | `audit/theorem-dependency.md`<br>`periodic-denominator-families.md` | Lexically accurate; association needs review |
| 23 | `O2` → `O002` | automatic | Low | `audit/theorem-dependency.md`<br>`periodic-denominator-families.md` | Lexically accurate; association needs review |
| 24 | `T1` → `T001` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 25 | `T10` → `T010` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 26 | `T13` → `T013` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 27 | `T14` → `T014` | automatic | Low | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 28 | `T2` → `T002` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 29 | `T22` → `T022` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 30 | `T24` → `T024` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 31 | `T25` → `T025` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 32 | `T27` → `T027` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 33 | `T32` → `T032` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 34 | `T36` → `T036` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 35 | `T38` → `T038` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 36 | `T39` → `T039` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 37 | `T45` → `T045` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 38 | `T5` → `T005` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 39 | `T6` → `T006` | automatic | Low | `audit/theorem-dependency.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 40 | `C7` → `C007` | automatic | Low | `literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 41 | `H1` → `H001` | automatic | Low | `literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 42 | `H5` → `H005` | automatic | Low | `literature-review.md`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 43 | `Q1` → `Q001` | automatic | Low | `literature-review.md` | Lexically accurate; association needs review |
| 44 | `Q2` → `Q002` | automatic | Low | `literature-review.md`<br>`scripts/coverage_and_tail.py`<br>`theorem-status.md` | Lexically accurate; association needs review |
| 45 | `G3` → `G003` | automatic | Low | `periodic-orbit-analysis.md` | Lexically accurate; association needs review |
| 46 | `C2` → `C002` | automatic | High | `theorem-status.md` | **Incorrect:** this is the prefix of `C2.1`; the suggestion loses `.1` |
| 47 | `CJ1` → no suggestion | manual | High | `theorem-status.md` | Accurate: two-letter prefix has no lossless automatic canonical mapping |
| 48 | `H2` → `H002` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 49 | `H3` → `H003` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 50 | `H4` → `H004` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 51 | `H6` → `H006` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 52 | `K10` → `K010` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 53 | `K12` → `K012` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 54 | `K2` → `K002` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 55 | `K3` → `K003` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 56 | `K4` → `K004` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 57 | `K5` → `K005` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 58 | `K6` → `K006` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 59 | `K7` → `K007` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 60 | `K8` → `K008` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 61 | `K9` → `K009` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 62 | `P16` → `P016` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 63 | `P17` → `P017` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 64 | `R1` → `R001` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 65 | `R2` → `R002` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 66 | `R3` → `R003` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 67 | `R4` → `R004` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 68 | `R5` → `R005` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 69 | `T11` → `T011` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 70 | `T29` → `T029` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 71 | `T30` → `T030` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 72 | `T31` → `T031` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 73 | `T34` → `T034` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |
| 74 | `T35` → `T035` | automatic | Low | `theorem-status.md` | Lexically accurate; association needs review |

Finding 46 must not be applied. `C2.1` is not a valid current Cruthúnas alias
because aliases match `^[A-Z][A-Z0-9-]*$`; preserving its punctuation therefore
requires a framework or human mapping decision. Finding 47 may preserve `CJ1`
as an alias, but choosing its one-letter canonical namespace risks collision
with the `C` corollary family and cannot be guessed.

### Identity and legacy-record findings

| # | Exact code, class, risk, path | Current state and reporter reason | Accuracy and later action | Dependencies and scientific boundary |
|---:|---|---|---|
| 75 | `identity.unstructured_assertion`; manual; High; `research-log.md` | Prose calls a tool an “independent verifier” without governed identity metadata. | Accurate as an unstructured assertion, but it is a retrospective research-log anecdote, not typed reproduction evidence. Retain as background unless a human supplies provenance. | Requires creator/requester/originator/environment/artifact separation. Reclassification could change an evidence boundary. |
| 76 | `identity.unstructured_assertion`; manual; High; `theorem-status.md` | Three “independent implementations” are asserted for K3–K5. | Accurate. Different implementations are documented; independent human authority is not. Do not promote to `INDEPENDENT_REPRODUCTION`. | Requires claim mapping and durable actor/process/environment records. It affects verification status. |
| 77 | `identity.unstructured_assertion`; manual; High; `verification-framework/src/main.rs` | Source comments and output label the Rust verifier independent. | Accurate as an implementation-boundary assertion, not proof of independent authority. Preserve code; later evidence may cite it only with full provenance. | Requires mapped computational claims, creator identity, commands, artifacts, and environment. It affects evidence class, not mathematics. |
| 78 | `identity.unstructured_assertion`; manual; High; `verification-framework/verify.py` | Module/output text calls the Python path a third independent verifier. | Accurate on the same limited basis as finding 77. Language and arithmetic differences alone do not prove independent authority. | Same dependency and verification-status boundary as finding 77. |
| 79 | `migration.record_manual`; manual; High; `audit/evidence-manifest.md` | A Markdown manifest cannot be converted without claim-by-claim and release-scope choices. | Accurate. It mixes tagged Git artifacts, logical digests, external ignored files, commands, and scope caveats. No direct conversion is safe. | Requires frozen-release analysis, claim IDs, typed evidence contracts, actor identities, and explicit `establishes`/`does_not_establish`. Wrong conversion would change claim support. |

### Governed-path findings

Findings 80–89 all have exact code `structure.missing`, automatic
classification, Medium risk, and message “Required governed project path is
missing.” Each path is in fact absent. Later creation is mechanically defined
by the pinned framework but still requires an authorized experimental-init PR;
none may be copied or invented in this audit. Their common dependency is an
approved exact framework pin and project identity. Creating them does not prove
a scientific claim, but their contents define every later governance boundary.

| # | Missing path | Required later decision or action |
|---:|---|---|
| 80 | `.cruthunas/project.yaml` | Initialize only as `experimental`, exact commit pinned, `non-conformant`; no release version |
| 81 | `RESEARCH_CHARTER.md` | Review a Cloitre-specific charter; the present audit plan is not a substitute |
| 82 | `claims/claims.yaml` | Create an empty canonical ledger; do not import theorem statuses |
| 83 | `claims/schema.json` | Copy the pinned canonical claim schema through the atomic init path |
| 84 | `schemas/claim-proposal-v1.json` | Copy through atomic init; no local schema edits |
| 85 | `schemas/evidence-v1.json` | Copy through atomic init; no evidence records yet |
| 86 | `schemas/exemption-v1.json` | Copy through atomic init; create no exemption |
| 87 | `schemas/framework-release-v1.json` | Copy schema only; experimental mode has no framework-release assertion |
| 88 | `schemas/project-v1.json` | Copy through atomic init and validate manifest against it |
| 89 | `schemas/transition-v1.json` | Copy through atomic init; create no scientific transition |

### Workflow findings

Findings 90–95 all have exact code `workflow.unpinned_action`, automatic
classification, Medium risk, path `.github\workflows\ci.yml`, and message that
the action reference is not a full commit SHA. Every finding is accurate.
The later action is a separate workflow-only PR that resolves each named ref to
a reviewed immutable SHA while retaining a readable version comment. That PR
depends on upstream-action verification and must rerun all jobs. It changes
reproduction provenance, not a mathematical statement, but can affect whether
CI is admissible as evidence.

| # | Line | Reported reference |
|---:|---:|---|
| 90 | 23 | `actions/checkout@v7` |
| 91 | 24 | `dtolnay/rust-toolchain@1.94.0` |
| 92 | 40 | `actions/checkout@v7` |
| 93 | 41 | `actions/setup-python@v6` |
| 94 | 76 | `actions/checkout@v7` |
| 95 | 78 | `leanprover/lean-action@v1` |

The compiler selection `1.94.0` is version-specific, but the action
implementation itself is still a moving non-SHA reference. No workflow
container or Dockerfile image finding was emitted because this repository has
neither a workflow container nor a Dockerfile.

## 4. Governed-structure gaps

The repository has none of the ten required governed files. In addition:

- There is no typed `audit/evidence/` root, `audit/transitions/` root, or
  `audit/exemptions/` root. Under the pinned framework, these directories are
  transaction-created when records exist; empty directory creation is not
  evidence.
- `audit/evidence-manifest.md` is a historical Markdown release/provenance
  record, not the typed evidence root.
- There is no `.cruthunas/project.yaml`, so project mode, framework commit,
  conformance, and release compatibility cannot yet be validated.
- A later pilot must use `mode: experimental`, pin one exact framework commit,
  record `conformance: non-conformant`, and make no framework-version or release
  assertion.
- `schemas/framework-release-v1.json` is a required local schema, but an actual
  framework-release attestation is not required or justified in experimental
  mode.
- There is no project `skills/` directory and no adapter adoption manifest, so
  the reporter correctly emitted no adapter gap. This does not authorize adapter
  synchronization.

No prospective structure was created.

## 5. Historical claim identifiers

`theorem-status.md` is the main historical ledger; proof files and
`audit/theorem-dependency.md` provide meaning and dependencies. Prefixes encode
different historical roles, not globally interchangeable namespaces:

| Class | Existing meaning | Prospective rule | Main risk |
|---|---|---|---|
| `T1`, `T18` | Theorems | Mechanical zero-padding, e.g. `T001`, `T018`; retain original alias | Association must match the exact theorem statement across files |
| `C2.1`, `C7`, `C19` | Corollaries | Simple integer forms can pad; `C2.1` cannot be preserved by the current alias schema | Decimal subnumbering is lost by the reporter and schema |
| `K1`–`K13` | Bounded computational results/certificates | Mechanical padding, e.g. `K001` | Must not be converted into proof or independent-reproduction status |
| `CJ1` | Original open conjecture | Human chooses a one-letter canonical ID; `CJ1` can be a historical alias | `C` namespace collision and loss of “conjecture” semantics |
| `L3`–`L44` | Lemmas | Mechanical padding, e.g. `L003` | Exact source and transitive proof dependencies must be reviewed |
| `P16`, `P17` | Propositions | Mechanical padding to `P016`, `P017` | Current schema has no `PROPOSITION` kind; a kind decision is required |
| `R1`–`R5` | Refuted/rejected ideas | Mechanical padding | These are refutations/corrections, not positive theorem claims |
| `H*`, `Q*`, `G3`, `O1`, `O2` | Heuristics, prior questions/claims, a periodic candidate, and open branches | Lexical padding is possible | Prefix meaning varies; some entries may be background rather than governable claims |

The reporter's 74 ID findings contain 72 sound lexical padding hints, one valid
manual case (`CJ1`), and one defective truncation (`C2` from `C2.1`). A reviewed
mapping must also decide whether every ledger row is a canonical claim at all.
No identifier was rewritten.

## 6. Existing-file mapping

This table records candidates only. Prose is not silently reinterpreted as
structured evidence.

| Existing material | Possible future surface | Qualification |
|---|---|---|
| `theorem-status.md` | Candidate claim-intake source and historical alias registry | Not a canonical ledger; rows mix proof, computation, heuristic, open, and refuted statuses |
| `partial-proofs.md` | Candidate source documents and proof locations | Candidate canonical proof source, but requires exact statement/attribution/dependency review |
| `bounded-quotient-analysis.md` | Candidate source for L21–T27 | Proof document; not evidence metadata |
| `periodic-orbit-analysis.md` | Candidate source/background for T25–T29 and computations | Mixes proof, search, limitation, and generated results; unsuitable for direct migration |
| `periodic-boundary-reduction.md` | Candidate source for T32–T38 | Proof document plus finite certificate discussion; split proof from computation |
| `aperiodic-tail-analysis.md` | Candidate source for T39–T45 and K13 | Mixes symbolic claims, computational probe, and certificate algorithm |
| `audit/evidence-manifest.md` | Candidate release provenance and artifact inventory | Manual typed-evidence mapping only; current file is a later correction about the frozen tag |
| `audit/fresh-proof-review.md` | Candidate internal-review record | Fresh-context internal audit only; reviewer identity is not durably recorded; never external review |
| `audit/theorem-dependency.md` | Candidate dependency/provenance source | Human-reviewed extraction required; the current graph omits at least the absorption use visible in the T18 proof |
| `audit/release-readiness.md` | Candidate internal-review/release-scope record | Assessment only; explicitly records missing external review and other blockers |
| `supplement/03-reproduction.md` | Candidate reproduction-command provenance | Commands and expected outputs are useful, but environment/actor/artifact records are not typed |
| `independent/` | Candidate computation/reproduction artifacts | Separate Python implementations; directory name and code separation do not establish independent authority |
| `verification-framework/` | Candidate computation/reproduction artifacts | Rust `u128` and Python literal-recurrence checks; implementation separation only |
| `search-framework/` | Candidate primary computation artifacts | Primary Rust search/certificate implementation; zero external Rust dependencies |
| `.github/workflows/ci.yml` | Candidate automated reproduction workflow | Six action refs are not SHA-pinned; workflow exists only after the frozen tag |
| `CITATION.cff` | Candidate attribution, AI-use, and later release-metadata record | Names `Kodaxadev`, discloses AI assistance, and points to the immutable tag commit; file is not in the tag |
| `research-log.md` | Candidate provenance/correction-history background | First-person exploratory chronology; unsuitable for automatic claim or evidence creation |
| `certificates/` and tracked `data/` | Candidate immutable computation artifacts | Hash and claim-scope mapping required; an artifact is not evidence without a typed record |
| `manuscript/` | Candidate compact source-document set | Best proof-facing sources, but later corrections must be separated from tagged versions |
| `README.md`, analyses, and future directions | Background and navigation | Not canonical claims or evidence merely because they summarize results |

## 7. Identity and independence gaps

The existing repository supports the following limited statements:

- Different implementations exist: primary Rust `u64` quotient/remainder code,
  separate Rust `u128` raw-recurrence code, and Python arbitrary-precision code.
- Different languages and arithmetic widths reduce some shared-bug risks.
- Some processes are described as fresh-context or independently implemented.

It does **not** presently establish, in Cruthúnas terms:

- a distinct creator, requester, originator, and approver for claim records;
- who authored each verifier or certificate and under what environment;
- that separate code was developed without access to the original algorithm;
- an independent human authority for any reproduction;
- a named external human reviewer or venue review.

`audit/fresh-proof-review.md` explicitly calls its review internal and not
external peer review. `CITATION.cff` discloses AI assistance and maintainer
curation. Neither the fresh-context protocol nor separate agent/model sessions
can be treated as independent human authority. Multiple implementations may be
backfilled as `COMPUTATION` after provenance is supplied; they must not become
`REPRODUCTION` or `INDEPENDENT_REPRODUCTION` merely from directory names,
languages, or matching outputs.

## 8. Workflow and environment gaps

- GitHub Actions: six mutable tag/version references need full-SHA pinning in a
  separate PR. The existing PR run at audited head `ee9d052...` passed all three
  jobs, but a green run does not cure provenance pinning.
- Containers: none are referenced; no container digest gap exists.
- Rust: local `cargo 1.94.0`/`rustc 1.94.0`; both crates have zero external
  dependencies and lockfiles containing only their workspace package.
- Python: project verification scripts use the standard library. CI selects
  Python 3.13; this audit ran successfully on 3.14.3, so the exact interpreter
  still belongs in future evidence metadata.
- Lean/Lake: `leanprover/lean4:v4.32.1` is pinned by `lean-toolchain` and the
  package has no mathlib dependency. Both `lake build` and direct `lean` passed.
- Reproduction commands are documented, but most historical results lack a
  typed environment, actor, source revision, and artifact link per claim.
- The full ten-million census and full million-state safe regeneration are
  deliberately excluded from ordinary CI. This audit did not regenerate them.
- `data/scan_1M.csv` and `data/scan_200k.csv` are ignored and absent from the
  isolated audit checkout. Copies exist in the separate original worktree with
  the exact hashes recorded by the later evidence manifest, but they are not in
  Git and cannot be recovered from the tag.

## 9. Frozen audit-release boundary

The boundary is:

- research snapshot: `f19ffcd75d04a05529878ce0226088f2f3221c0b`;
- annotated tag object: `14b14ebffd92c18358c84aa6fa25595d3f630c07`;
- immutable tag `v0.1.0-audit` and tagged audit commit:
  `46e4780dc4955c1fd21110aebcbc6da688794668`;
- later corrected `main`/audit base:
  `d990512d386b6365e4b835a72ac634ce9ddda9f0`;
- audited charter head: `ee9d052015e658a8941f237130ba4aa7df03d29c`.

The tag contains the compact proof dossier, certificates, code, and the first
evidence manifest. It does not contain CI, `CITATION.cff`, Lean/Lake package
files, the README redesign, the corrected archive-byte hash table, or the later
Theorem 5/T38 premise repair. Consequently:

- T18 and the small-spectrum certificate are present in the tagged artifact;
- the exact Git-archive hash corrections are supported by later `main`, not by
  the manifest text frozen inside the tag;
- the completed T38 premise chain and automated CI are later-state support;
- the two ignored scan CSV files are outside Git and outside the release;
- later files may describe or verify the immutable tag, but they do not become
  members of that release retroactively.

No tag, tag object, release, or frozen file was moved, recreated, or
reinterpreted as a Cruthúnas release.

## 10. Proposed migration sequence

The two reporter defects create a concrete prerequisite. The default sequence
is retained after a new framework-only step zero.

### PR 0 — repair Cruthúnas adoption reporting

- **Scope:** In the Cruthúnas repository, recognize punctuated IDs without
  prefix truncation and broaden affirmative independence-language coverage;
  add the two section-12 fixtures as deterministic tests.
- **Prohibited:** No Cloitre mutation, automatic migration, schema relaxation by
  accident, or reinterpretation of existing evidence.
- **Inputs/outputs:** Minimal fixtures and pinned reporter code; a reviewed
  framework commit with passing tests and documented expected output.
- **Review/stop:** Framework maintainer plus adversarial fixture review; stop if
  exact-token semantics or explicit-nonclaim filtering regresses.

### PR 1 — experimental minimum structure

- **Scope:** Run the atomic init path at a newly authorized exact framework SHA
  to add the manifest, empty ledger, unfrozen charter, and schemas.
- **Prohibited:** Claims, evidence, transitions, exemptions, adapters,
  conformance, release, or scientific-text edits.
- **Inputs/outputs:** Reviewed project identity/maintainer and framework pin;
  `experimental`/`non-conformant` minimum structure.
- **Review/stop:** Governance review and clean full check; stop on overwrite,
  moving ref, release assertion, or any nonempty claim ledger.

### PR 2 — reviewed historical-ID map

- **Scope:** Decide canonical IDs and historical aliases without rewriting the
  historical documents.
- **Prohibited:** Claim registration/status changes and guessed `C2.1`/`CJ1`
  mappings.
- **Inputs/outputs:** `theorem-status.md`, dependency graph, corrected reporter;
  a reviewed mapping decision record.
- **Review/stop:** Mathematical owner plus governance reviewer; stop on any
  collision, ambiguous role, invalid alias, or statement mismatch.

### PR 3 — one dependency-free atomic claim

- **Scope:** Propose, review, and register one exact dependency-free claim
  through the atomic command path; T001 is recommended in section 11.
- **Prohibited:** Importing historical “proved” status, backfilling proof
  evidence, or registering T018 with omitted dependencies.
- **Inputs/outputs:** Exact source statement, ID map, durable identities; one
  Gate-4 `OPEN`/`UNCHECKED` claim plus registration evidence/history.
- **Review/stop:** Independent registration approver required by policy; stop if
  statement, quantifiers, attribution, limitation, or identity is uncertain.

### PR 4 — register the T18 dependency chain, then T018

- **Scope:** Register the reviewed direct/transitive prerequisites in dependency
  order, then propose/register exact T018 without changing proof status.
- **Prohibited:** Batch status promotion, inferred dependencies, or using C20
  computation as proof of T18.
- **Inputs/outputs:** T1/L3/L4/L12/T13/T14 source chain and reviewed mapping;
  atomic records with no dangling dependency.
- **Review/stop:** Line-by-line mathematical dependency review; stop on a graph/
  source mismatch or missing durable authority.

### PR 5 — bounded evidence backfill

- **Scope:** Add only typed proof, computation, formalization, or internal-review
  evidence whose existing immutable artifacts and metadata satisfy the contract.
- **Prohibited:** Invented actors/environments, `REPRODUCTION`, external review,
  or full-census independence claims.
- **Inputs/outputs:** Hash-bound artifacts and commands; typed evidence with
  explicit `establishes` and `does_not_establish`.
- **Review/stop:** Evidence/provenance review; stop when any required identity,
  environment, artifact, source revision, or independence boundary is absent.

### PR 6 — one bounded transition

- **Scope:** Process one supported claim-axis transition end to end after its
  evidence exists.
- **Prohibited:** Multi-claim promotion, conformance, external review, or release
  status.
- **Inputs/outputs:** One claim, evidence set, requester and distinct approval;
  one atomic transition with complete chronology.
- **Review/stop:** Policy and mathematical review; stop if evidence does not
  support the exact target axis.

### PR 7 — workflow pinning and adapter decision

- **Scope:** Pin workflows in one PR; evaluate adapter adoption separately and
  synchronize only if explicitly authorized.
- **Prohibited:** Combining workflow changes with scientific or claim changes.
- **Inputs/outputs:** Verified upstream action SHAs and, separately, an adapter
  adoption decision; reproducible CI and optional reviewed adapter manifest.
- **Review/stop:** Supply-chain review and full CI; stop on upstream ambiguity,
  drift, or a generated-file policy gap.

Every bounded PR must rerun `cruthunas adoption gaps` and compare deterministic
output. Migration must not start from the defective reporter pin without a new
explicitly authorized framework SHA.

## 11. First governed-claim recommendation

### T18 assessment

- **Prospective ID/alias:** `T018`, historical alias `T18`.
- **Exact statement:** For every integer start `m ≥ 1`, define the recurrence by
  `b₂ = m` and `bₙ₊₁ = bₙ + (bₙ mod n)`. For every eventual integer increment
  `c`, if the orbit stabilizes with eventual increment `c`, then
  `m < (c+3)(3c+5)`.
- **Source/proof:** `manuscript/01-foundations-and-spectrum.md`, “Theorem 18
  (the increment bounds the start)”; the longer proof also appears in
  `partial-proofs.md` §5b.
- **Dependencies:** Definitions; the bounded-regime entry L3; quotient-step
  control L4/L12; forced rebound T13; ratchet T14; and the absorption
  characterization used to identify `q_t=r_t=c`. The current dependency graph
  shows L3 and T14 directly but does not show every dependency visible in the
  proof text.
- **Attribution:** `theorem-status.md` labels it new. `CITATION.cff` attributes
  the AI-assisted, maintainer-curated package to `Kodaxadev`, but no typed claim
  originator/author record exists.
- **Review:** `audit/fresh-proof-review.md` records a passing fresh internal
  review. It does not name a durable independent human authority. External
  review is explicitly pending.
- **Formalization:** Lean does not formalize T18.
- **Evidence candidates:** The two proof sources and internal-review record are
  candidates; theorem tests and `scripts/test_theorem18.py` are computation
  support, not proof or independent reproduction. None can be backfilled until
  missing identities and typed boundaries are supplied rather than inferred.
- **Scientific boundary:** T18 is unconditional conditional-on-stabilization; it
  does not prove universal stabilization. C20 additionally needs the complete
  small finite certificate. The 106-omission census is a different, weaker
  independence boundary.

### Recommendation

Do **not** make T018 the first atomic registration. The pinned command refuses a
proposal with dependencies that are not already registered canonical claims.
Omitting those dependencies would create a misleading canonical record.

Use dependency-free, foundational `T001` (historical `T1`, the absorption
equivalence) as the first end-to-end pilot because its exact proof is compact,
its source is stable, and a corresponding foundational Lean declaration exists.
The first permissible claim operation, only after PRs 0–2 and with durable
identity supplied, is a `cruthunas claim propose ... --id T001 --alias T1
--dry-run --json` preview. Registration must still begin `OPEN`/`UNCHECKED` and
must not import the historical theorem status.

T018 remains the first headline-result target after its reviewed dependency
chain is registered. No claim operation is permissible in the current
non-adopted repository.

## 12. False-positive and false-negative assessment

### Confirmed defect A — punctuated historical ID

Minimal fixture outside both repositories:

```text
theorem-status.md: | C2.1 | positive eventual increment | proved |
```

Expected: one manual incompatible-ID finding for the exact historical token
`C2.1`, because the current alias schema cannot preserve its punctuation.
Actual: the reporter emitted automatic `C2 → C002`, silently truncating `.1`.
This is both a false positive for exact `C2` and a false negative for `C2.1`.

### Confirmed defect B — affirmative independence wording

Minimal fixture outside both repositories:

```text
evidence.md: The certificate is independently regenerated and checked.
```

Expected: `identity.unstructured_assertion`. Actual: no non-structure finding.
The same blind spot occurs in actual files including
`compressed-orbit-analysis.md`, `audit/evidence-manifest.md`,
`audit/release-readiness.md`, `independent/verify_safe_certificate.py`,
`independent/verify_small_spectrum.py`, `partial-proofs.md`,
`periodic-orbit-analysis.md`, `README.md`, `supplement/02-certificates.md`, and
`search-framework/tests/dynamics.rs`.

### Other classification checks

- The four emitted identity findings are not treated as proof of independence;
  source-code self-descriptions remain manual provenance questions.
- Explicit negative language such as “not external peer review” and “no second
  implementation” was not incorrectly promoted.
- Mathematical uses such as “independently of `q`” were not flagged, which is
  correct.
- Requirements/future-review wording was not counted as completed evidence.
- No schema examples exist in Cloitre, and the reporter did not mistake the
  frozen audit tag for Cruthúnas conformance.
- Workflow paths are serialized with Windows backslashes while other report
  paths use forward slashes. This limits cross-platform digest portability; it
  is recorded as a framework follow-up, not used as a third confirmed semantic
  defect here.
- The reporter supplies no severity; the audit classifications in section 1
  are explicitly human-added.

These defects must be fixed on a separate Cruthúnas framework branch with the
minimal fixtures above. No Cloitre-side workaround is permitted, and any later
migration must rerun a newly authorized pinned reporter.

## 13. Validation

### Commands and results

| Command/check | Result |
|---|---|
| Required Git identity/status/base/diff checks | Pass; clean at `ee9d052...`, merge-base `d990512...`, charter-only branch diff |
| `cargo test --release --manifest-path search-framework/Cargo.toml` | Pass; 39 tests, 0 failed |
| `cargo test --release --manifest-path verification-framework/Cargo.toml` | Pass; 0 test failures |
| Verification Rust `--selftest` | Pass |
| Python compile of four CI scripts | Pass |
| `verification-framework/verify.py --oeis` | Pass; 25 A073117 terms and 68 A117846 terms matched, plus stated checks |
| `independent/verify_small_spectrum.py` | Pass; canonical certificate hash matched; 5 and 7 excluded on complete bounded ranges |
| `independent/verify_safe_certificate.py --n 10000 --max-steps 20000` | Pass |
| `scripts/periodic_phase_blocks.py --max-denominator 501` | Pass; 463 families, 0 phase-integral survivors, expected digest |
| Four committed artifact hashes from CI | Pass; 4/4 matched |
| `lake build` | Pass on Lean 4.32.1 |
| `lean lean/Conjecture.lean` | Pass; only the file's printed standard axiom dependencies |
| Reporter run 1 | Expected exit 1 with gaps; valid JSON; Git status/diff clean |
| Reporter run 2 | Expected exit 1 with gaps; byte/semantic match; Git status/diff clean |
| Corrected minimal defect reproductions | Pass as reproductions; actual output differs from expected semantics as documented |

Skipped by design: the full ten-million-start census, full million-state safe
certificate regeneration, ignored row-by-row scan regeneration, workflow
mutation, and any project/framework toolchain installation beyond the isolated
Cruthúnas audit virtual environment. The environment limitation is Python
3.14.3 rather than CI's 3.13; all selected Python checks passed.

Before the audit, the worktree was clean and contained only the charter commit
over the required base. After both reporter runs it remained clean. This report
is the only new repository file. Existing research files are unchanged, raw
JSON remains outside the repository, and no migration action occurred.

### Boundary confirmation

| Action | Occurred? |
|---|---|
| Cruthúnas initialization | No |
| Project-manifest creation | No |
| Claim-ledger creation | No |
| Historical-ID rewrite | No |
| Claim-status change | No |
| Evidence backfill | No |
| Transition creation | No |
| Workflow mutation | No |
| Adapter synchronization | No |
| Frozen-tag mutation | No |
| Release or tag creation | No |
| Conformance claim | No |
| CR-1 promotion | No |
