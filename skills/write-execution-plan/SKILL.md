---
name: write-execution-plan
description: "Define and validate canonical execution-plan artifacts. Use when a workflow creates, derives, reviews, or validates implementation coordination from approved specification context."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared execution-plan artifact contract: canonical section order, scope-alignment fields, runtime-edge obligations handling, minimum coordination content, template shape, and deterministic validation.

## Contract

- Artifact shape:
  - one Markdown artifact
  - canonical frontmatter when the workflow stamps provenance
  - required sections, in order:
    1. `Execution Summary`
    2. `Scope Alignment`
    3. `Implementation Streams`
    4. `Work Breakdown`
    5. `Dependency and Sequencing Strategy`
    6. `Validation Checkpoints`
    7. `Risks and Mitigations`
    8. `Progress Tracking`
    9. `Further Notes`
- Scope Alignment must include:
  - companion `Charter`, `User Stories`, `Requirements`, and `Technical Design` references
  - `Story capability areas:`
  - `Story anchors:` with `US1.x` IDs or `TODO: Confirm`
  - `Runtime-edge obligations:` with preserved operator-facing behavior or `None in approved spec`
- Minimum content:
  - at least one named implementation stream
  - grouped work items under the stream model
  - explicit sequencing notes, validation checkpoints, risks, and progress tracking fields
  - explicit traceability back to companion spec artifacts
  - `TODO: Confirm` where high-impact execution detail is unresolved
- Scope boundary:
  - execution plans coordinate implementation; they do not rewrite charter, user stories, requirements, or technical design
  - preserve runtime-edge behavior and verification when upstream artifacts describe it
  - organize streams and work around capability areas, `US1.x` story IDs, requirement IDs, and technical-design interfaces or failure strategy where relevant
  - do not turn the artifact into commit instructions, file inventories, or code snippets

## Inputs

- approved or derived charter, user stories, requirements, and technical design
- known implementation constraints, milestones, or sequencing risks

## Outputs

- one canonical execution-plan Markdown artifact compatible across review and downstream task tracking
- the shared template at `./assets/plan-template.md`
- deterministic validation via `./scripts/validate_plan.sh`

## Workflow

1. Start from `./assets/plan-template.md`.
2. Translate the approved specification into a small set of meaningful implementation streams instead of flat tasks.
3. Carry forward capability areas, `US1.x` story IDs, requirement IDs, and design anchors where they shape sequencing or validation.
4. Record `Runtime-edge obligations:` explicitly, using `None in approved spec` only when the upstream artifacts do not describe one.
5. Group work under streams with enough detail to coordinate implementation without becoming commit instructions.
6. Record sequencing rationale, validation checkpoints, execution risks, and progress-tracking fields.
7. Mark unresolved high-impact execution detail as `TODO: Confirm`.
8. Validate with `bash ./scripts/validate_plan.sh <plan-file>`.

## Validation

- Run: `bash ./scripts/validate_plan.sh <plan-file>`
- Confirm section order and required `Scope Alignment` fields match the shared contract.
- Confirm at least one implementation stream exists and work stays grouped under that stream model.
- Confirm runtime-edge obligations, sequencing, validation checkpoints, and progress tracking are explicit.
- Confirm canonical frontmatter is valid when the workflow stamps provenance.
