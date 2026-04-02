---
name: write-requirements
description: Write and validate canonical software requirements artifacts. Use when a task creates, derives, reviews, or validates requirements and needs stable section order, numbering, and uncertainty handling for downstream design and planning.
metadata:
  version: 0.1.0
  layer: foundational
  dependencies:
    - document-traceability
---

## Rules

- Keep this artifact focused on product obligations and constraints because product framing and success criteria belong in the charter.
- Use the `document-traceability` contract for canonical frontmatter, timestamps, provenance, source-artifact lineage, and shared validation.
- Use deterministic requirement identifiers because design, planning, and review need stable references.
- Keep requirements externally meaningful and testable because vague statements cannot be validated.
- Mark unresolved high-impact ambiguity as `TODO: Confirm` instead of guessing.
- When deriving from code, describe implemented reality rather than imagined original intent.

## Constraints

- Output must be one Markdown artifact.
- Frontmatter must use canonical authored-document fields from `document-traceability`.
- `source_artifacts` must include exactly `charter` and `user_stories`.
- Required sections must appear in canonical order.
- Requirement identifiers must use the shared prefixes:
  - `FR1.x` for Functional Requirements
  - `NFR2.x` for Non-Functional Requirements
  - `TC3.x` for Technical Constraints
  - `DR4.x` for Data Requirements
  - `IR5.x` for Integration Requirements
  - `DEP6.x` for Dependencies
- Do not include goals, non-goals, persona catalogs, success-criterion sections, file paths, code snippets, commit sequencing, or task breakdowns as requirements content.
- If a required section has no confirmed items yet, keep the section and use `TODO: Confirm`.

## Requirements

A valid requirements artifact must include these sections in this order:

1. `Functional Requirements`
2. `Non-Functional Requirements`
3. `Technical Constraints`
4. `Data Requirements`
5. `Integration Requirements`
6. `Dependencies`
7. `Further Notes`

Minimum content expectations:

- canonical provenance and timestamp frontmatter
- `source_artifacts.charter` and `source_artifacts.user_stories`
- at least one numbered `FR1.x` requirement
- every requirement is specific enough to verify
- unresolved or weakly supported details use `TODO: Confirm`

Inputs:

- approved product framing, approved stories, repository evidence, or other source material defining the behavior and constraints
- known constraints, integrations, data rules, and dependencies
- root orchestration context needed to stamp `generated_by`

Output:

- one requirements Markdown artifact that downstream design, planning, and review work can reference directly

## Workflow

1. Draft from [`assets/requirements-template.md`](./assets/requirements-template.md) so canonical ordering stays intact.
2. Stamp canonical frontmatter from `document-traceability`, including `source_artifacts.charter` and `source_artifacts.user_stories`.
3. Start from approved stories or evidence-backed behavior before adding detailed constraints.
4. Write numbered functional requirements with `FR1.x` identifiers.
5. Capture quality expectations, constraints, data rules, integrations, and dependencies with the shared identifier taxonomy.
6. Keep scope framing and success checks in the charter instead of duplicating them here.
7. Replace unresolved high-impact details with `TODO: Confirm` instead of inventing specifics.
8. Validate the finished artifact with [`scripts/validate_requirements.sh`](./scripts/validate_requirements.sh).

## Gotchas

- If provenance omits either upstream artifact, later design and planning cannot prove the obligation chain. Keep both lineage roles explicit.
- If requirements include technical design choices, later architecture work becomes fake because the solution was smuggled in as scope. Keep requirements focused on externally meaningful obligations and constraints.
- If goals, personas, or success criteria are copied into this artifact, the pack drifts into redundancy and later edits split across files. Leave product framing to the charter.
- If numbering is ad hoc, design and plan documents cannot reference requirements stably across revisions. Use the shared prefix taxonomy every time.
- If derived requirements describe what the system probably meant to do, you create a cleaner story than the code actually supports. Document implemented reality and mark weak inferences with `TODO: Confirm`.
- If empty sections are deleted instead of marked unresolved, downstream skills cannot tell whether the category was considered or forgotten. Keep the section and use `TODO: Confirm`.
- If functional requirements are written as tasks or file edits, planning inherits implementation trivia instead of product obligations. State behavior and constraints, not commit steps.

## Deliverables

- A Markdown requirements artifact with canonical frontmatter and section order.
- Deterministic identifiers across all requirement categories.
- Explicit functional requirements, non-functional requirements, constraints, integrations, data requirements, and dependencies.
- Clear `TODO: Confirm` markers for unresolved high-impact details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation.
- `source_artifacts.charter` and `source_artifacts.user_stories` are present.
- All required sections exist and are in the correct order.
- At least one `FR1.x` requirement exists.
- Product framing and success-criterion sections are not mixed into the artifact.
- Technical design and task-level detail are not mixed into the artifact.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_requirements.sh <requirements-file>`
