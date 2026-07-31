# Cruthúnas experimental adoption audit plan

**Status:** Planned, non-mutating audit  
**Cloitre source base:** `d990512d386b6365e4b835a72ac634ce9ddda9f0`  
**Cruthúnas framework commit:** `49840431d02e8c7cae7d35e82bf3fd4095dc397b`  
**Framework maturity:** CR-0 — Exploration

## Purpose

Run the deterministic Cruthúnas adoption-gap reporter against the existing Cloitre repository and produce a complete migration inventory without changing claim status, evidence, workflows, release records, or historical research content.

This audit is the first step of the governed-case phase. It does not adopt Cloitre, establish Cruthúnas conformance, or authorize any automatic correction.

## Required output

The completed audit must record:

1. the exact Cloitre source SHA and Cruthúnas framework SHA;
2. the exact command and environment used;
3. the deterministic finding count and a SHA-256 digest of the raw JSON output;
4. every finding grouped by structure, historical claim IDs, workflow/container pinning, actor identity and independence, adapters, framework mode/release compatibility, and legacy or untyped records;
5. whether each gap is mechanically correctable or requires a human evidence or migration decision;
6. a mapping from existing Cloitre files to prospective Cruthúnas canonical surfaces;
7. a bounded implementation order for later pull requests;
8. a recommended first governed claim, including canonical ID, historical alias, dependencies, evidence candidates, and unresolved authority boundaries.

The raw JSON output should remain an uncommitted review artifact unless a separate decision establishes a generated-file drift check. The committed audit report must be human-readable and trace every conclusion to the raw finding code or inspected repository file.

## Mandatory boundaries

This work unit must not:

- run `cruthunas init` against the existing repository;
- create `.cruthunas/project.yaml`;
- rewrite or normalize historical claim IDs;
- create canonical claim, evidence, proposal, exemption, or transition records;
- change `theorem-status.md`, proofs, computations, certificates, or research logs;
- change claim, verification, publication, review, or release language;
- pin or modify project workflows or containers;
- synchronize adapters;
- modify the frozen `v0.1.0-audit` tag or its records;
- create a release, tag, conformance claim, external-review claim, or Cruthúnas maturity promotion;
- edit the Cruthúnas framework repository.

## Initial claim candidate

Unless the audit identifies a stronger blocker, evaluate historical claim `T18` as the first later governed claim:

- prospective canonical ID: `T018`;
- retained historical alias: `T18`;
- statement: the finite-start bound `c(m)=c \Rightarrow m<(c+3)(3c+5)`;
- reason: it is a bounded proof claim, supports the certified omitted-increment result, and exercises historical-alias migration without requiring the universal conjecture to move.

The audit may recommend a different first claim, but it must explain why that choice has fewer unverifiable dependencies or authority gaps.

## Acceptance conditions

- The audit runs against the exact pinned source and framework commits.
- The report is deterministic, findings-first, and read-only with respect to existing research records.
- Automatic gaps are not automatically applied.
- Manual gaps are not guessed or converted into evidence.
- Existing repository checks remain green.
- The final diff contains only the audit charter and completed audit-report material authorized by this work unit.
- Cloitre remains non-adopted and non-conformant at completion.
