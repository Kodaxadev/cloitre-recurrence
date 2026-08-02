# Cruthúnas historical-ID mapping decision record

## Provenance and posture

- Cloitre source: `1099e0207b9febde120a5cb44f3dd691188309d2`
- Cruthúnas framework pin: `f60d61d19254759a1c395cae52663f82212a8121`
- Mode: `experimental`
- Conformance: `non-conformant`
- Ledger state: empty (`claims: []`)
- Purpose: mapping decision only

This document does not register claims. It does not rewrite historical IDs or
import historical proof status. It does not create evidence or begin migration.
The source-file cells describe occurrences at the recorded Cloitre source and
exclude this decision record itself.

## Decision rules and limits

An identifier matching `^[A-Z][0-9]+$` receives a lexical candidate formed by
zero-padding its numeric suffix to at least three digits. The unchanged
historical spelling is retained here as the prospective alias. This accepts only
the identifier spelling; it does not accept the statement, proof, status,
dependencies, or suitability for the claim ledger.

`C2.1` and `CJ1` are manual cases. Their historical spellings remain preserved
in this record, but the current alias contract cannot represent `C2.1`
losslessly and no one-letter namespace can be chosen for `CJ1` without a later
policy decision. This record therefore chooses no padded,
punctuation-flattened, or guessed-namespace replacement for either manual ID.

Decision status has this narrow meaning:

- `accepted-candidate`: the lexical mapping is accepted for possible later use.
- `unresolved`: the lexical spelling is available, but claim-versus-evidence,
  exploration, namespace, or alias-policy questions remain.
- `excluded-from-claim-map`: the token is not a future claim candidate in this
  map; later governance may still preserve it in another record class.

## Group A — theorem-like IDs

These are claim-like historical theorem labels. Their mappings are accepted
candidates only; no historical theorem or proof status is imported.

| historical ID | proposed canonical ID | alias retained | source files | historical role | mapping class | risk | decision status | notes |
|---|---|---|---|---|---|---|---|---|
| `T1` | `T001` | `T1` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Exact statement association remains for later review. |
| `T2` | `T002` | `T2` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T5` | `T005` | `T5` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T6` | `T006` | `T6` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T10` | `T010` | `T10` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T11` | `T011` | `T11` | `theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T13` | `T013` | `T13` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T14` | `T014` | `T14` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T18` | `T018` | `T18` | `audit/cruthunas-adoption-plan.md`<br>`audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Not registered; dependency chain still governs any later proposal. |
| `T22` | `T022` | `T22` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T24` | `T024` | `T24` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T25` | `T025` | `T25` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T27` | `T027` | `T27` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T29` | `T029` | `T29` | `theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T30` | `T030` | `T30` | `theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T31` | `T031` | `T31` | `theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T32` | `T032` | `T32` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T34` | `T034` | `T34` | `theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T35` | `T035` | `T35` | `theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T36` | `T036` | `T36` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T38` | `T038` | `T38` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T39` | `T039` | `T39` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `T45` | `T045` | `T45` | `audit/theorem-dependency.md`<br>`theorem-status.md` | theorem | mechanical-padding | low | accepted-candidate | Status is not imported. |

## Group B — lemma IDs

These are claim-like dependency labels. Mapping does not validate their stated
dependencies or import proof status.

| historical ID | proposed canonical ID | alias retained | source files | historical role | mapping class | risk | decision status | notes |
|---|---|---|---|---|---|---|---|---|
| `L3` | `L003` | `L3` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L4` | `L004` | `L4` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L8` | `L008` | `L8` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L12` | `L012` | `L12` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L21` | `L021` | `L21` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L26` | `L026` | `L26` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L28` | `L028` | `L28` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L33` | `L033` | `L33` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L40` | `L040` | `L40` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L41` | `L041` | `L41` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L42` | `L042` | `L42` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L43` | `L043` | `L43` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |
| `L44` | `L044` | `L44` | `audit/theorem-dependency.md`<br>`theorem-status.md` | lemma/dependency | mechanical-padding | low | accepted-candidate | Dependency review remains required. |

## Group C — corollary IDs

Integer-only corollary labels have accepted lexical candidates. The punctuated
identifier remains manual and unresolved.

| historical ID | proposed canonical ID | alias retained | source files | historical role | mapping class | risk | decision status | notes |
|---|---|---|---|---|---|---|---|---|
| `C7` | `C007` | `C7` | `literature-review.md`<br>`theorem-status.md` | corollary | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `C9` | `C009` | `C9` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | corollary | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `C19` | `C019` | `C19` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | corollary | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `C20` | `C020` | `C20` | `audit/theorem-dependency.md`<br>`literature-review.md`<br>`theorem-status.md` | computer-assisted corollary | mechanical-padding | low | accepted-candidate | Mapping does not establish proof or evidence. |
| `C23` | `C023` | `C23` | `audit/theorem-dependency.md`<br>`theorem-status.md` | corollary | mechanical-padding | low | accepted-candidate | Status is not imported. |
| `C2.1` | unresolved | `C2.1` | `theorem-status.md` | punctuated corollary | manual-required | high | unresolved | Punctuation is not losslessly representable by the current alias contract. |

## Group D — computational, result, and non-claim-like IDs

All one-letter numeric spellings below have deterministic padded forms. Their
future record class is not thereby decided. Bounded results may become claims or
evidence; heuristics and open branches may remain exploration; prior-work
questions, mathematical notation, and rejected ideas are excluded from this
claim map.

| historical ID | proposed canonical ID | alias retained | source files | historical role | mapping class | risk | decision status | notes |
|---|---|---|---|---|---|---|---|---|---|
| `K1` | `K001` | `K1` | `audit/theorem-dependency.md`<br>`theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K2` | `K002` | `K2` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K3` | `K003` | `K3` | `theorem-status.md` | reproduction result | maybe-not-a-claim | medium | unresolved | Could belong to reproduction evidence rather than the ledger. |
| `K4` | `K004` | `K4` | `theorem-status.md` | reproduction result | maybe-not-a-claim | medium | unresolved | Could belong to reproduction evidence rather than the ledger. |
| `K5` | `K005` | `K5` | `theorem-status.md` | reproduction result | maybe-not-a-claim | medium | unresolved | Could belong to reproduction evidence rather than the ledger. |
| `K6` | `K006` | `K6` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K7` | `K007` | `K7` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K8` | `K008` | `K8` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K9` | `K009` | `K9` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K10` | `K010` | `K10` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Includes a beyond-range conjectural limitation. |
| `K11` | `K011` | `K11` | `audit/evidence-manifest.md`<br>`audit/theorem-dependency.md`<br>`research-log.md`<br>`theorem-status.md` | computational certificate result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K12` | `K012` | `K12` | `theorem-status.md` | bounded computational result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `K13` | `K013` | `K13` | `aperiodic-tail-analysis.md`<br>`audit/theorem-dependency.md`<br>`certificates/safe_n1000000.txt`<br>`theorem-status.md` | computational certificate result | maybe-not-a-claim | medium | unresolved | Decide later between finite claim and computation evidence. |
| `P16` | `P016` | `P16` | `theorem-status.md` | proposition | mechanical-padding | medium | accepted-candidate | Future claim kind requires a separate schema/policy decision. |
| `P17` | `P017` | `P17` | `theorem-status.md` | proposition | mechanical-padding | medium | accepted-candidate | Future claim kind requires a separate schema/policy decision. |
| `O1` | `O001` | `O1` | `audit/theorem-dependency.md`<br>`periodic-denominator-families.md` | open branch/cycle label | maybe-not-a-claim | high | unresolved | Branch-versus-claim semantics remain undecided. |
| `O2` | `O002` | `O2` | `audit/theorem-dependency.md`<br>`periodic-denominator-families.md` | open branch/cycle label | maybe-not-a-claim | high | unresolved | Branch-versus-claim semantics remain undecided. |
| `H1` | `H001` | `H1` | `literature-review.md`<br>`theorem-status.md` | heuristic | maybe-not-a-claim | medium | unresolved | May remain Gate 3 exploration. |
| `H2` | `H002` | `H2` | `theorem-status.md` | heuristic | maybe-not-a-claim | medium | unresolved | May remain Gate 3 exploration. |
| `H3` | `H003` | `H3` | `theorem-status.md` | heuristic | maybe-not-a-claim | medium | unresolved | May remain Gate 3 exploration. |
| `H4` | `H004` | `H4` | `theorem-status.md` | mixed heuristic | maybe-not-a-claim | medium | unresolved | Mixed proved/heuristic wording needs later separation. |
| `H5` | `H005` | `H5` | `literature-review.md`<br>`theorem-status.md` | heuristic | maybe-not-a-claim | medium | unresolved | May remain Gate 3 exploration. |
| `H6` | `H006` | `H6` | `theorem-status.md` | heuristic | maybe-not-a-claim | medium | unresolved | May remain Gate 3 exploration. |
| `Q1` | `Q001` | `Q1` | `literature-review.md` | prior-work question label | maybe-not-a-claim | high | excluded-from-claim-map | Labels a MathOverflow question, not a Cloitre claim. |
| `Q2` | `Q002` | `Q2` | `literature-review.md`<br>`scripts/coverage_and_tail.py`<br>`theorem-status.md` | prior-work question label | maybe-not-a-claim | high | excluded-from-claim-map | Labels a MathOverflow question, not a Cloitre claim. |
| `G3` | `G003` | `G3` | `periodic-orbit-analysis.md` | ordinary mathematical use | maybe-not-a-claim | high | excluded-from-claim-map | Reporter tokenizes LaTeX `G/3`; this is not a historical ID. |
| `R1` | `R001` | `R1` | `theorem-status.md` | refuted/rejected idea | maybe-not-a-claim | high | excluded-from-claim-map | Preserve as historical rejection, not a positive claim candidate. |
| `R2` | `R002` | `R2` | `theorem-status.md` | refuted/rejected idea | maybe-not-a-claim | high | excluded-from-claim-map | Preserve as historical rejection, not a positive claim candidate. |
| `R3` | `R003` | `R3` | `theorem-status.md` | refuted/rejected idea | maybe-not-a-claim | high | excluded-from-claim-map | Preserve as historical rejection, not a positive claim candidate. |
| `R4` | `R004` | `R4` | `theorem-status.md` | refuted/rejected idea | maybe-not-a-claim | high | excluded-from-claim-map | Preserve as historical rejection, not a positive claim candidate. |
| `R5` | `R005` | `R5` | `theorem-status.md` | refuted/rejected idea | maybe-not-a-claim | high | excluded-from-claim-map | Preserve as historical rejection, not a positive claim candidate. |

## Group E — conjecture/manual namespace

| historical ID | proposed canonical ID | alias retained | source files | historical role | mapping class | risk | decision status | notes |
|---|---|---|---|---|---|---|---|---|
| `CJ1` | unresolved | `CJ1` | `theorem-status.md` | original open conjecture | manual-required | high | unresolved | A two-letter prefix risks namespace collision and semantic loss. |

## Decision summary

- 72 one-letter numeric tokens have deterministic padded spellings.
- 43 claim-like lexical mappings are `accepted-candidate`: 23 theorems, 13
  lemmas, 5 integer-only corollaries, and 2 propositions.
- 21 mechanically spellable IDs remain unresolved because they may instead be
  computation/reproduction evidence, exploration, or open-branch records.
- 8 mechanically spellable tokens are excluded from this claim map: 2
  prior-work questions, 1 ordinary mathematical-use token, and 5 rejected ideas.
- 2 IDs remain manual and unresolved: exact `C2.1` and `CJ1`. No truncated `C2`
  or guessed canonical replacement is recorded.

This map is not a ledger. A proposed canonical ID is only a possible future
identifier. It does not imply that a statement, proof, status, evidence record,
or claim exists, and it does not begin migration. Any future proposal or
registration requires its own atomic authorization and exact statement,
dependency, provenance, limitation, and policy review.
