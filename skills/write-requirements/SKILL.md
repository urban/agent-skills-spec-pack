---
name: write-requirements
description: "Define and validate canonical requirements artifacts. Use when a workflow creates, derives, reviews, or validates product obligations that must stay stable for downstream design and planning."
license: MIT
metadata:
  version: "0.4.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared requirements artifact contract: canonical section order, identifier taxonomy, minimum traceability and verifiability rules, template shape, and deterministic validation. Keep authored and derived requirements artifacts compatible without owning workflow-wide lineage policy.

## Contract

- Artifact shape:
  - one Markdown artifact
  - canonical frontmatter when the workflow stamps provenance
  - keep every required section even when unresolved; use `TODO: Confirm` instead of deleting sections
  - required sections, in order:
    1. `Functional Requirements`
    2. `Non-Functional Requirements`
    3. `Technical Constraints`
    4. `Data Requirements`
    5. `Integration Requirements`
    6. `Dependencies`
    7. `Further Notes`
- Identifier taxonomy:
  - `FR1.x` for Functional Requirements
  - `NFR2.x` for Non-Functional Requirements
  - `TC3.x` for Technical Constraints
  - `DR4.x` for Data Requirements
  - `IR5.x` for Integration Requirements
  - `DEP6.x` for Dependencies
- Scope boundary:
  - requirements formalize product obligations and constraints, not charter framing, technical design, or execution planning
  - do not include goals, non-goals, persona catalogs, success-criterion sections, file paths, code snippets, commit sequencing, or task breakdowns as requirements content
  - implementation-enforced constraints are allowed when phrased as stable obligations rather than a code tour
  - this skill does not own workflow-wide `source_artifacts` policy
- Minimum content:
  - at least one numbered `FR1.x` requirement
  - every functional requirement includes `Story traceability` with one or more `US1.x` story IDs or `TODO: Confirm`
  - every requirement is specific enough to verify
  - approved or reconstructed story behavior should be translated into obligations instead of copied verbatim
  - source-backed runtime, framework, protocol, parser, tooling, validation, data, integration, and dependency constraints belong in the right non-`FR` sections when they materially shape behavior or operations
  - command aliases, shared flag semantics, accepted source grammars, and explicit validation rules belong in requirements when they are part of the observable contract
  - unresolved or weakly supported high-impact details use `TODO: Confirm`
  - derived requirements describe implemented reality rather than imagined original intent

## Inputs

- approved product framing, approved stories, repository evidence, or other source material defining behavior and constraints
- known constraints, integrations, data rules, and dependencies

## Outputs

- one canonical requirements Markdown artifact compatible across authoring, derivation, review, and downstream design or planning
- the shared template at `./assets/requirements-template.md`
- deterministic validation via `./scripts/validate_requirements.sh`

## Workflow

1. Start from `./assets/requirements-template.md`.
2. Begin with approved or evidence-backed user-visible behavior before adding detailed constraints.
3. Translate story behavior into verifiable obligations; use `Actor`, `Situation`, `Action`, `Outcome`, and `Observation` to preserve triggers, behavior, value, and checkability, and carry relevant `US1.x` IDs into `Story traceability` notes.
4. Number requirements with the shared taxonomy and place each source-backed constraint in the right family instead of forcing everything into `FR`.
5. Keep charter framing, architecture, and planning detail out of the artifact.
6. Replace unresolved high-impact details with `TODO: Confirm`.
7. Validate with `bash ./scripts/validate_requirements.sh <requirements-file>`.

## Validation

- Run: `bash ./scripts/validate_requirements.sh <requirements-file>`
- Confirm section order and identifier taxonomy match the shared contract.
- Confirm at least one `FR1.x` exists and every functional requirement has `Story traceability` with `US1.x` or `TODO: Confirm`.
- Confirm requirements are verifiable, externally meaningful, and use the right category for high-impact constraints.
- Confirm canonical frontmatter is valid when the workflow stamps provenance.
