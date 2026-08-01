# Research Governance

This repository is maintained by Kodaxadev. Contributions are evaluated by evidence quality, reproducibility, scope discipline, and compatibility with the claim ledger—not by contributor status or tool choice.

## Claim states

- **Open:** not proved or refuted.
- **Heuristic:** supported by patterns or informal reasoning only.
- **Computational:** established only over an explicitly stated finite domain.
- **Internally proved:** a complete argument is present and has passed internal adversarial review.
- **Certified:** backed by a reproducible certificate or independent implementation over the stated domain.
- **Externally reviewed:** checked by an identified independent specialist or formal venue.

These labels are not interchangeable. CI success, Lean compilation, and model agreement do not constitute external mathematical review.

## Acceptance standard

A claim change must update every affected statement, dependency, evidence boundary, and reproduction instruction. Corrections are preferred over preserving a prior narrative. Material disagreements should be recorded rather than silently removed.

## Maintainer decisions

The maintainer controls merges, releases, status labels, and the frozen audit record. Rejected changes may be reconsidered when new evidence is supplied. Major status upgrades should receive a fresh-context review and, where practical, independent reproduction.

## Releases and corrections

Frozen releases are immutable records. Later corrections must be made in a new commit or release with the affected claim and evidence boundary identified explicitly.
