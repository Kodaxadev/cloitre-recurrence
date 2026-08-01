# Contributing

Contributions are welcome, especially independent proof review, reproducibility checks, computational verification, documentation corrections, and clearly scoped research ideas.

## Before opening a pull request

1. Read `README.md`, `theorem-status.md`, and `audit/evidence-manifest.md`.
2. State exactly which claim, artifact, script, or document your change affects.
3. Separate proved statements, computations, heuristics, and conjectures.
4. Do not describe a bounded computation as a universal result.
5. Preserve the frozen `v0.1.0-audit` release. New work belongs on the current development branch.

## Mathematical contributions

For a proof, counterexample, or correction, include:

- a precise statement;
- all assumptions and quantifiers;
- a complete argument or minimal failing case;
- dependencies on earlier lemmas;
- what remains unproved;
- whether the result has been independently checked.

A model-generated proof is treated as unverified until a human-readable argument is checked against the repository's claim ledger and evidence boundaries.

## Computational contributions

Include the command, environment, expected output, range covered, integer-width assumptions, runtime/memory notes, and a digest or certificate when practical. Independent implementations should avoid importing the primary implementation.

## Development checks

Run the checks relevant to your change. The standard fast suite is documented under `Reproduction` in `README.md`.

## Pull requests

Keep pull requests focused. Explain the claim boundary, tests run, generated artifacts changed, and any unresolved concern. A passing CI run does not by itself establish mathematical correctness.
