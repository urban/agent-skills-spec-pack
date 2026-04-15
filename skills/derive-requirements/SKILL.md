---
name: derive-requirements
description: "Reconstruct requirements artifacts from repository evidence and reconstructed user-visible behavior. Use when a user needs implemented product obligations documented for an existing system."
license: MIT
metadata:
  version: "0.4.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - reconstruct-implementation-constraints
    - write-requirements
---

## Purpose

Produce `requirements.md` from repository evidence. Reconstruct implemented obligations, constraints, data rules, integrations, and dependencies without inventing unsupported product history or turning the artifact into technical design.

## Boundaries

- Output filename: `requirements.md`
- Source of truth: repository code, tests, manifests, entrypoints, schemas, parsers, config, error types, and integrations; reconstructed `./charter.md` and `./user-stories.md` are supporting context, and stronger repository evidence wins
- Artifact contract: follow `../write-requirements/SKILL.md`
- In scope:
  - reconstruct implemented requirements, constraints, and dependencies
  - recover code-enforced runtime, validation, parsing, integration, dependency, and operational constraints
  - preserve explicit uncertainty where actor intent, scope rationale, or verification framing cannot be proved
  - align requirements to reconstructed story behavior when `./user-stories.md` is available
  - back up an existing report before overwrite
- Out of scope:
  - unsupported goals, non-goals, personas, or success criteria presented as fact
  - cleaner imagined intent or speculative product history
  - technical design, execution tasks, or workflow-wide `source_artifacts` lineage policy
  - commit history, PR text, or external docs as primary evidence
- Ask only when ambiguity changes scope, destination, evidence threshold, artifact shape, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- repository source code
- repository tests, manifests, config, and project structure when present
- runtime entrypoints, command definitions, schemas, parsers, validators, error types, and integrations when present
- optional scope paths from the user
- optional output destination from the user
- reconstructed `./charter.md`, `./user-stories.md`, and optional `./technical-design.md` when present

## Output

- `requirements.md`
- a timestamped backup in the same directory before overwrite when the destination already exists
- one reconstructed requirements artifact downstream work can trust for implemented obligations, constraints, and dependencies

## Workflow

1. Confirm analysis scope and destination; default to the full repository when the user does not narrow it.
2. Inspect code, tests, manifests, config, entrypoints, and command surfaces to inventory user-visible behavior and execution-relevant constraints.
3. Use `../reconstruct-implementation-constraints/SKILL.md` to recover source-backed runtime, validation, parsing, integration, lifecycle, dependency, packaging, and failure constraints.
4. Classify recovered facts into the shared requirement families: `FR`, `NFR`, `TC`, `DR`, `IR`, and `DEP`.
5. Use reconstructed `./user-stories.md` when present to preserve behavioral traceability; carry relevant `US1.x` IDs into `Story traceability` notes and use story context to recover triggers, outcomes, and observations the code supports.
6. If the destination already exists, create a timestamped backup in the same directory before overwrite.
7. Draft `requirements.md` with the shared contract; keep the artifact externally meaningful and verifiable instead of turning it into an architecture tour.
8. If reconstructed `./technical-design.md` is available in the same run, backfill missing high-impact non-`FR` items it surfaces before final delivery.
9. Mark weak evidence, unprovable actor intent, unclear rationale, or uncertain verification framing as `TODO: Confirm`.
10. Validate with `bash ../write-requirements/scripts/validate_requirements.sh <resolved-requirements-path>`.
11. Deliver the result as reconstructed implemented requirements, not speculative history.

## Validation

- Run: `bash ../write-requirements/scripts/validate_requirements.sh <resolved-requirements-path>`
- Confirm backup exists before overwrite when needed and filename is `requirements.md`.
- Confirm section order and numbering match the shared contract.
- Confirm functional requirements use reconstructed `US1.x` traceability or `TODO: Confirm` and describe implemented behavior rather than guessed original intent.
- Confirm high-impact runtime, parser, validation, integration, dependency, alias, shared-flag, and accepted-input constraints are captured in the right non-`FR` sections when source-backed.
- Confirm requirements remain externally meaningful and verifiable, and unresolved high-impact details stay `TODO: Confirm`.

## Approval-view focus

- highest-impact recovered obligations and the evidence behind them
- evidence-backed constraints on inputs, validation, integrations, and operations
- low-confidence requirement areas and any inferred-versus-observed distinction
- findings that pressure reconciliation with reconstructed technical design
