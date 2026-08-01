# Research notes

Everything here is working mathematical material. The authoritative index is
[`theorem-status.md`](theorem-status.md), which classifies every claim the
project touches into disjoint classes — proved, computational, heuristic,
conjecture, refuted — and cites the document holding each proof.

Start there. These directories are what it cites.

| Directory | Contents |
|---|---|
| [`proofs/`](proofs/) | Every document the ledger's *Where* column cites: statements and proofs of the numbered lemmas, corollaries and theorems |
| [`research-logs/`](research-logs/) | Chronology, including the approaches that failed and why |
| [`future-directions/`](future-directions/) | Ranked open problems and the current frontier |
| [`notes/`](notes/) | Material that carries no numbered claim: literature review, benchmarks, negative searches, heuristic models, implementation design |

The split between `proofs/` and `notes/` is mechanical, not editorial: a document
is in `proofs/` exactly when `theorem-status.md` cites it as the source of a
numbered claim. `symbolic-analysis.md` is in `notes/` because the ledger cites it
only from the *Heuristic* and *Refuted* tables.

## Entry points

* [`theorem-status.md`](theorem-status.md) — the claim ledger
* [`proofs/partial-proofs.md`](proofs/partial-proofs.md) — foundational proofs
  and the finite-start theorem
* [`future-directions/future-directions.md`](future-directions/future-directions.md)
  — ranked unresolved directions
* [`future-directions/future-directions-safe-map.md`](future-directions/future-directions-safe-map.md)
  — the safe-map frontier, where the current work is

Audit material lives outside this directory, in [`../audit/`](../audit/), because
it reviews these documents rather than belonging to them.

## Conventions

Cross-references between notes use the bare filename in backticks, for example
`` `theorem-status.md` ``. Every basename in the repository is unique, so these
resolve unambiguously. `scripts/check_doc_links.py` verifies in CI that every
relative link and every inline path reference still resolves; it is what makes a
reorganization like this one safe to perform.
