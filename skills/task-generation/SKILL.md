---
name: task-generation
description: Break an execution plan into grouped tracer-bullet tasks with explicit dependencies and local tracking. Use when a user wants an approved implementation plan decomposed into execution-ready tasks.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: planning
  domain: implementation-planning
  dependencies:
    - document-traceability
    - write-task-tracking
---

## Rules

- Treat the parent execution plan as the coordination source of truth because this role decomposes approved work rather than redefining it.
- Use `document-traceability` to stamp canonical provenance plus `source_artifacts.plan`.
- Use the `write-task-tracking` contract for section order, task fields, runtime-edge preservation, and validation because local tracking must stay stable across turns.
- Keep each task tracer-bullet shaped: thin, end-to-end, independently verifiable, and production-bound.
- Group tasks by implementation stream because stream context preserves the plan's sequencing logic.
- Record dependencies in terms of working behavior, not architecture-layer order.
- If the plan carries runtime-edge obligations, preserve those obligations in tasks and include both structural and behavior-verifying acceptance criteria.
- Use `TODO: Confirm` when ambiguity changes task boundaries or dependency shape.

## Constraints

- Output must be one Markdown artifact at `.specs/<project-name>/execution-tasks.md`.
- The artifact must stay compatible with the `write-task-tracking` contract.
- The artifact must record `source_artifacts.plan = .specs/<project-name>/execution-plan.md`.
- Every task must include a stable identifier, status, dependency field, and plan references.
- Tasks must remain local tracking artifacts; do not create GitHub issues or external tickets.
- Do not create layer-only tasks that deliver no verifiable end-to-end behavior.

## Requirements

Inputs:

- an approved execution plan at `.specs/<project-name>/execution-plan.md` or equivalent
- companion charter, user stories, requirements, and technical design when needed to clarify task boundaries
- repository context when needed to find real seams or sequencing constraints

Output:

- one local task-tracking artifact at `.specs/<project-name>/execution-tasks.md`

In scope:

- decomposing implementation streams into grouped tracer-bullet tasks
- assigning stable task IDs, statuses, dependencies, and plan references
- preserving traceability back to the execution plan
- preserving runtime-edge behavior and verification when the plan requires it
- surfacing blockers or ambiguity that affect task sequencing

Out of scope:

- rewriting the execution plan
- code changes
- external issue creation

## Workflow

1. Confirm the user wants local implementation tasks created from an approved execution plan.
2. Load the parent plan, then read [`references/tracer-bullets.md`](./references/tracer-bullets.md).
3. Capture `root_skill` from the active execution workflow and set `producing_skill = task-generation`.
4. Extract implementation streams, work breakdown items, sequencing constraints, validation checkpoints, and runtime-edge obligations from the plan.
5. Use companion specification artifacts only when task boundaries or dependencies need clarification.
6. Slice the work into thin tracer-bullet tasks grouped by stream.
7. Assign stable task IDs, explicit dependencies, statuses, and plan references.
8. For runtime-edge work, include both structural and behavior-verifying acceptance criteria instead of only bootstrap steps.
9. Draft `.specs/<project-name>/execution-tasks.md` using the `write-task-tracking` contract.
10. Stamp canonical provenance with `source_artifacts.plan`.
11. Mark unresolved high-impact task-boundary or dependency ambiguity as `TODO: Confirm`.
12. Validate with `bash ../write-task-tracking/scripts/validate_tasks.sh .specs/<project-name>/execution-tasks.md`.
13. Deliver the local task-tracking artifact for execution.

## Gotchas

- If tasks are generated directly from charter, requirements, or design instead of the execution plan, local tracking drifts from approved sequencing immediately. Start from the plan and use other artifacts only to clarify boundaries.
- If tasks are split by architecture layer, they stop being independently verifiable and feedback arrives too late. Slice around thin working behavior instead.
- If stream grouping disappears, the artifact becomes a flat backlog and loses the coordination model that made the plan useful. Keep every task nested under its implementation stream.
- If dependencies are phrased as vague order hints, later turns cannot tell what truly blocks what. Name the prerequisite task or working behavior explicitly.
- If task IDs or statuses are inconsistent, the document turns into prose notes instead of a tracking surface. Keep stable fields on every task from the first draft.
- If runtime-edge tasks stop at command or file existence checks, the operator-facing behavior never gets proved. Keep acceptance criteria on decoding, wiring, invocation, rendering, or equivalent visible outcomes when the plan requires them.
- If blockers and sequencing ambiguity are buried in narrative, the next implementation turn overcommits and stalls. Put them where the tracking artifact expects them and mark `TODO: Confirm` when needed.

## Deliverables

- `.specs/<project-name>/execution-tasks.md`
- grouped tracer-bullet tasks with stable identifiers, statuses, dependencies, and plan references
- explicit `source_artifacts.plan` lineage and deterministic provenance
- local tracking structure suitable for iterative implementation updates
- validation passing via the shared task-tracking validator

## References

- [`references/tracer-bullets.md`](./references/tracer-bullets.md): Read when: slicing execution-plan work into thin end-to-end tasks or deciding whether a dependency is behavior-oriented enough.

## Validation Checklist

- artifact path is `.specs/<project-name>/execution-tasks.md`
- parent execution plan was used as the source of truth
- `source_artifacts.plan` points to the approved plan
- at least one implementation stream group exists
- every task has an ID, status, dependencies, and plan references
- dependencies are behavior-oriented rather than layer-oriented
- runtime-edge obligations are preserved explicitly or recorded as `None in parent plan`
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-task-tracking/scripts/validate_tasks.sh .specs/<project-name>/execution-tasks.md`
