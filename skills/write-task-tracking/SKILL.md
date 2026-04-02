---
name: write-task-tracking
description: Write and validate canonical local task-tracking artifacts derived from execution plans. Use when a task turns an approved plan into grouped tracer-bullet implementation tasks with explicit status, dependencies, and plan traceability.
metadata:
  version: 0.1.0
  layer: foundational
  dependencies:
    - document-traceability
---

## Rules

- Keep task tracking downstream of an approved execution plan because local tasks should implement a plan, not redefine it.
- Use the `document-traceability` contract for canonical frontmatter, timestamps, provenance, source-artifact lineage, and shared validation.
- Group tasks by implementation stream because stream context preserves execution intent and sequencing.
- Keep tasks tracer-bullet shaped: thin, end-to-end, independently verifiable, and production-bound.
- Record dependencies in terms of working behavior, not architecture-layer order, because implementation sequencing should reflect what must exist to verify progress.
- Preserve plan references on every task because local task state must stay traceable to plan commitments.
- Require one explicit runtime-edge obligations field so task generation must say either what operator-facing runtime behavior is preserved or `None in parent plan`.
- Runtime-edge tasks must include both structural and behavior-verifying acceptance criteria.
- Mark unresolved task-boundary ambiguity as `TODO: Confirm`.

## Constraints

- Output must be one Markdown artifact.
- Frontmatter must use canonical authored-document fields from `document-traceability`.
- `source_artifacts` must include exactly `plan`.
- Required sections must appear in canonical order.
- `Task Summary` must include `Runtime-edge obligations:`.
- Every task must include a stable identifier, status, dependency field, and plan references.
- At least one stream group must exist.
- Every task must include at least two acceptance-criteria bullets.
- Do not collapse the artifact into issue-tracker boilerplate, commit scripts, or architecture-only layer tasks.

## Requirements

A valid task-tracking artifact must include these sections in this order:

1. `Task Summary`
2. `Stream Groups`
3. `Dependency Map`
4. `Tracking Notes`

Minimum content expectations:

- canonical provenance and timestamp frontmatter
- `source_artifacts.plan`
- `Runtime-edge obligations:` in `Task Summary`
- at least one grouped implementation stream
- at least one task identifier with status, dependency field, and plan references
- every task has at least two acceptance-criteria bullets
- explicit dependency and sequencing notes
- explicit tracking notes for active work and blockers
- `TODO: Confirm` where a high-impact task detail is not yet confirmed

Inputs:

- approved execution plan
- companion charter, user stories, requirements, and technical design when needed for clarification
- any current implementation status or blockers
- root orchestration context needed to stamp `generated_by`

Output:

- one local task-tracking Markdown artifact that can be updated across implementation turns

## Workflow

1. Confirm the approved execution plan and its companion specification artifacts.
2. Draft from [`assets/tasks-template.md`](./assets/tasks-template.md) so section order stays canonical.
3. Stamp canonical frontmatter from `document-traceability`, including `source_artifacts.plan`.
4. Extract implementation streams, work breakdown items, sequencing constraints, validation checkpoints, and runtime-edge obligations from the plan.
5. Record `Runtime-edge obligations:` in `Task Summary`, using `None in parent plan` only when the plan explicitly says no runtime edge is in scope.
6. Slice the work into grouped tracer-bullet tasks with stable task identifiers.
7. Add status, dependency fields, and plan references to every task.
8. Use companion specification artifacts only when task boundaries or dependencies need clarification.
9. Summarize cross-stream sequencing in the dependency map and capture active blockers in tracking notes.
10. Mark unresolved high-impact task details as `TODO: Confirm`.
11. Validate the finished artifact with [`scripts/validate_tasks.sh`](./scripts/validate_tasks.sh).

## Gotchas

- If you generate tasks directly from requirements or design instead of the plan, local tracking drifts from approved sequencing immediately. Start from the execution plan and use specs only for clarification.
- If tasks are architecture-layer chores like “update backend” or “touch frontend,” they cannot be verified independently and stall tracer-bullet delivery. Slice tasks around thin working behavior.
- If stream grouping disappears, the artifact becomes a flat backlog and loses the plan's coordination model. Keep tasks nested under the execution streams they implement.
- If dependencies are written as vague order hints, later turns cannot tell what must land first. Name the concrete prerequisite task or behavior.
- If tasks lack plan references, reviewers cannot trace whether local work still matches the approved plan. Add explicit plan linkage to each task.
- If status fields are inconsistent or missing, the document turns into narrative notes instead of a tracking surface. Use stable status fields on every task from the start.
- If runtime-edge obligations disappear between plan and tasks, implementation will satisfy structure while missing behavior. Carry the obligations into task summary and into task acceptance criteria.
- If blockers get buried in prose, the next implementation turn overcommits and breaks flow. Put active blockers and sequencing risks in `Tracking Notes` where they are easy to update.

## Deliverables

- A Markdown task-tracking artifact with canonical frontmatter and section order.
- Grouped tracer-bullet tasks with stable identifiers, statuses, dependencies, and plan references.
- A dependency map and tracking notes that make active sequencing and blockers explicit.
- A runtime-edge obligations statement plus task acceptance criteria that preserve operator-facing behavior when needed.
- Clear `TODO: Confirm` markers for unresolved high-impact task details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation.
- `source_artifacts.plan` is present.
- All required sections exist and are in the correct order.
- `Task Summary` includes `Runtime-edge obligations:`.
- At least one implementation stream group is present.
- Every task has an identifier, status, dependencies, and plan references.
- Every task has at least two acceptance-criteria bullets.
- Dependencies are behavior-oriented rather than layer-oriented.
- The artifact remains local task tracking rather than a rewritten plan, issue tracker, or commit script.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_tasks.sh <tasks-file>`
