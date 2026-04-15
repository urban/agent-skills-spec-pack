---
name: requirements
description: "Produce requirements artifacts from approved product framing and approved user stories. Use when a user needs product obligations, constraints, and dependencies defined before technical design or implementation."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: specification-authoring
  dependencies:
    - write-requirements
---

## Purpose

Produce `requirements.md` from approved charter and story context. Translate approved behavior into verifiable obligations, constraints, data rules, integrations, and dependencies without re-owning product framing, architecture, or planning.

## Boundaries

- Output filename: `requirements.md`
- Source of truth: approved `./charter.md` and `./user-stories.md`; use repository evidence when existing behavior, integrations, or platform constraints materially affect the requirements
- Artifact contract: follow `../write-requirements/SKILL.md`
- In scope:
  - write numbered functional requirements derived from approved stories
  - translate story `Situation` and `Observation` into preconditions, edge conditions, and verifiable checks when relevant
  - record non-functional requirements, technical constraints, data rules, integrations, and dependencies
  - preserve explicit uncertainty where needed
- Out of scope:
  - redefining approved goals, non-goals, personas, or success criteria
  - technical architecture or implementation strategy
  - execution planning or code changes
  - workflow-wide `source_artifacts` lineage policy
- Ask only when ambiguity changes scope, constraints, integrations, dependencies, verifiability, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- approved `./charter.md`
- approved `./user-stories.md`
- known constraints, integrations, data rules, and dependencies
- repository evidence when existing behavior materially affects scope

## Output

- `requirements.md`
- one requirements artifact downstream design and implementation can trust for product obligations, constraints, and dependencies

## Workflow

1. Load approved `./charter.md` and `./user-stories.md`; inspect repo evidence only where existing behavior or integrations materially constrain the requirements.
2. Draft `requirements.md` with the `write-requirements` contract.
3. Translate approved story behavior into verifiable obligations; use `US1.x` IDs for `Story traceability`, `Actor` and `Action` for the required behavior, `Situation` for triggers and edge conditions, `Outcome` for value-bearing results, and `Observation` for externally checkable expectations.
4. Keep requirements externally meaningful and verifiable; move architecture and task-level detail out of the artifact.
5. Classify quality constraints, data rules, integrations, and dependencies into the right non-`FR` sections.
6. Keep charter framing in `./charter.md` unless a short traceability note is needed.
7. Mark unresolved high-impact details as `TODO: Confirm`.
8. Validate with `bash ../write-requirements/scripts/validate_requirements.sh <resolved-requirements-path>`.
9. Deliver for approval before downstream design or implementation.

## Validation

- Run: `bash ../write-requirements/scripts/validate_requirements.sh <resolved-requirements-path>`
- Confirm filename is `requirements.md`, section order matches the shared contract, and numbering uses the shared taxonomy.
- Confirm at least one functional requirement exists and every functional requirement has `Story traceability` with approved `US1.x` or `TODO: Confirm`.
- Confirm requirements trace back to approved story behavior and stay verifiable.
- Confirm product framing, architecture, and implementation sequencing are not mixed into the artifact.
- Confirm unresolved high-impact details stay `TODO: Confirm`.

## Approval-view focus

- highest-impact obligations and story-backed scope anchors
- integration contracts, data rules, and validation hotspots
- non-functional constraints most likely to shape technical design
- any `TODO: Confirm` item that would distort downstream design if left vague
