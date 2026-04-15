---
name: write-charter
description: "Define and validate canonical charter artifacts. Use when a workflow creates, derives, reviews, or validates scope-baseline documentation for a specification pack."
license: MIT
metadata:
  version: "0.2.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared charter artifact contract: canonical section order, `SC1.x` success-criterion numbering, minimum scope-framing content, template shape, and deterministic validation. Keep authored and derived charter artifacts compatible without owning workflow-wide lineage policy.

## Contract

- Artifact shape:
  - one Markdown artifact
  - canonical frontmatter when the workflow stamps provenance
  - keep every required section even when unresolved; use `TODO: Confirm` instead of deleting sections
  - required sections, in order:
    1. `Goals`
    2. `Non-Goals`
    3. `Personas / Actors`
    4. `Success Criteria`
- Scope boundary:
  - charter defines the scope baseline, actors, and measurable definition of done
  - do not include detailed user stories, detailed requirements, technical design, implementation strategy, file paths, or task breakdowns
  - this skill does not own workflow-wide `source_artifacts` policy
- Minimum content:
  - at least one goal bullet
  - at least one numbered `SC1.x` success criterion
  - goals and non-goals are explicit
  - personas or actors stay concrete where known, else `TODO: Confirm`
  - every success criterion is specific enough to verify
  - unresolved or weakly supported high-impact details use `TODO: Confirm`

## Inputs

- user intent or source material defining the problem and desired outcomes
- known scope boundaries, users, stakeholders, and success measures

## Outputs

- one canonical charter Markdown artifact compatible across authoring, derivation, review, and downstream specification work
- the shared template at `./assets/charter-template.md`
- deterministic validation via `./scripts/validate_charter.sh`

## Workflow

1. Start from `./assets/charter-template.md`.
2. Record goals and explicit non-goals before downstream artifacts add detail.
3. Identify the personas or actors who receive value or constrain scope.
4. Write measurable success criteria with `SC1.x` identifiers.
5. Replace unresolved high-impact details with `TODO: Confirm`.
6. Validate with `bash ./scripts/validate_charter.sh <charter-file>`.

## Validation

- Run: `bash ./scripts/validate_charter.sh <charter-file>`
- Confirm section order and `SC1.x` numbering match the shared contract.
- Confirm goals, non-goals, actors, and success criteria stay framing-level, not behavior, design, or task detail.
- Confirm canonical frontmatter is valid when the workflow stamps provenance.
