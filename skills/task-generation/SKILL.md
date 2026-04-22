---
name: task-generation
description: "Produce local task-tracking artifacts from an approved execution plan. Use when a user needs execution-ready tasks with explicit dependencies and plan traceability."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: implementation-planning
  dependencies:
    - write-task-tracking
---

## Purpose

Produce `execution-tasks.md` from an approved execution plan. Decompose plan streams into thin local execution slices with stable dependencies and traceability without rewriting the plan.

## Boundaries

- Output filename: `execution-tasks.md`
- Source of truth: approved `./execution-plan.md`; use companion spec artifacts only when task boundaries or dependencies need clarification
- Artifact contract: follow `../write-task-tracking/SKILL.md`
- In scope:
  - decompose implementation streams into grouped tracer-bullet tasks
  - assign stable task IDs, statuses, dependencies, and plan references
  - preserve traceability back to the execution plan
  - preserve runtime-edge behavior and verification when the plan requires it
  - surface blockers or ambiguity that affect task sequencing
- Out of scope:
  - rewriting the execution plan
  - code changes
  - external issue creation
- Ask only when ambiguity changes task boundaries, dependency shape, runtime-edge behavior, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- approved `./execution-plan.md`
- companion `./charter.md`, `./user-stories.md`, `./requirements.md`, and `./technical-design.md` when needed to clarify task boundaries
- repository context when needed to find real seams or sequencing constraints

## Output

- `execution-tasks.md`
- one local task-tracking artifact implementation can trust for grouped execution slices, dependencies, and plan traceability

## Workflow

1. Load the parent plan from `./execution-plan.md`, then read `./references/tracer-bullets.md`.
2. Extract implementation streams, work breakdown items, sequencing constraints, validation checkpoints, runtime-edge obligations, and traceability anchors from the plan.
3. Use companion spec artifacts only when task boundaries or dependencies need clarification.
4. Slice the work into thin tracer-bullet tasks grouped by stream.
5. Assign stable task IDs, explicit dependencies, statuses, and plan references.
6. For runtime-edge work, include both structural and behavior-verifying acceptance criteria instead of only bootstrap steps.
7. Draft `execution-tasks.md` with the shared contract.
8. Mark unresolved high-impact task-boundary or dependency ambiguity as `TODO: Confirm`.
9. Validate with `bash ../write-task-tracking/scripts/validate_tasks.sh <resolved-execution-tasks-path>`.
10. Deliver the local task-tracking artifact for execution.

## Validation

- Run: `bash ../write-task-tracking/scripts/validate_tasks.sh <resolved-execution-tasks-path>`
- Confirm filename is `execution-tasks.md`, section order matches the shared contract, and at least one stream group exists.
- Confirm every task has an ID, status, dependencies, plan references, and at least two acceptance-criteria bullets.
- Confirm dependencies are behavior-oriented and runtime-edge obligations are preserved explicitly or recorded as `None in parent plan`.
- Confirm plan references preserve capability-area, `US1.x`, requirement, or design traceability where relevant.
- Confirm unresolved high-impact details stay `TODO: Confirm`.

## Approval-view focus

- highest-risk task groups and dependency chains
- runtime-edge tasks where structural work could be mistaken for verified behavior
- blockers and ambiguous task boundaries most likely to stall implementation
- traceability gaps that would make execution drift from the approved plan
- artifact approval profile owned here lives in `./assets/approval-view-profile.json`
- keep that profile aligned with this skill's review framing; do not rely on a generic template

## References

- [`./references/tracer-bullets.md`](./references/tracer-bullets.md): Read when: slicing plan work into thin end-to-end tasks or checking whether a dependency is behavior-oriented enough.
