---
name: write-task-tracking
description: "Define and validate canonical local task-tracking artifacts. Use when a workflow creates, derives, reviews, or validates execution tasks from an approved plan."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared task-tracking artifact contract: canonical section order, task fields, tracer-bullet expectations, runtime-edge obligations handling, template shape, and deterministic validation.

## Contract

- Artifact shape:
  - one Markdown artifact
  - canonical frontmatter when the workflow stamps provenance
  - required sections, in order:
    1. `Task Summary`
    2. `Stream Groups`
    3. `Dependency Map`
    4. `Tracking Notes`
- `Task Summary` must include:
  - `Parent plan:`
  - `Scope:`
  - `Tracking intent:`
  - `Story / requirement / design anchors:`
  - `Runtime-edge obligations:` with preserved operator-facing behavior or `None in parent plan`
- Task contract:
  - at least one stream group
  - every task uses `#### Task TASK-ID`
  - every task includes `Title`, `Status`, `Blocked by`, `Plan references`, `What to build`, `Acceptance criteria`, and `Notes`
  - every task has at least two acceptance-criteria bullets
  - tasks stay tracer-bullet shaped: thin, end-to-end, independently verifiable, and production-bound
  - dependencies are behavior-oriented rather than layer-oriented
- Scope boundary:
  - preserve parent-plan traceability to capability areas, `US1.x` story IDs, requirement IDs, and design anchors where relevant
  - runtime-edge tasks must include both structural and behavior-verifying acceptance criteria
  - keep the artifact as local tracking, not issue-tracker boilerplate, copied plan sections, or architecture-only chores
  - use `TODO: Confirm` where high-impact task detail is unresolved

## Inputs

- approved execution plan
- companion charter, user stories, requirements, and technical design when needed for clarification
- current implementation status or blockers when available

## Outputs

- one canonical local task-tracking Markdown artifact compatible across execution turns
- the shared template at `./assets/tasks-template.md`
- deterministic validation via `./scripts/validate_tasks.sh`

## Workflow

1. Start from `./assets/tasks-template.md`.
2. Extract implementation streams, work breakdown items, sequencing constraints, validation checkpoints, and runtime-edge obligations from the parent plan.
3. Carry forward capability areas, `US1.x` story IDs, requirement IDs, and design anchors through plan references where tasks need that context.
4. Record `Runtime-edge obligations:` in `Task Summary`, using `None in parent plan` only when the parent plan explicitly says no runtime edge is in scope.
5. Slice the work into grouped tracer-bullet tasks with stable identifiers, statuses, dependency fields, and plan references.
6. Summarize cross-stream sequencing in the dependency map and active blockers in tracking notes.
7. Mark unresolved high-impact task detail as `TODO: Confirm`.
8. Validate with `bash ./scripts/validate_tasks.sh <tasks-file>`.

## Validation

- Run: `bash ./scripts/validate_tasks.sh <tasks-file>`
- Confirm section order and required task fields match the shared contract.
- Confirm at least one stream group exists and every task has at least two acceptance-criteria bullets.
- Confirm dependencies stay behavior-oriented and runtime-edge obligations are preserved where needed.
- Confirm canonical frontmatter is valid when the workflow stamps provenance.
