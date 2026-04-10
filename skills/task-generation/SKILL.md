---
name: task-generation
description: "Produce local task-tracking artifacts from an approved execution plan. Use when a user needs execution-ready tasks with explicit dependencies and plan traceability."
license: MIT
metadata:
  version: "0.3.0"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: implementation-planning
  dependencies:
    - write-task-tracking
---

## Rules

- Treat the parent execution plan as the coordination source of truth because this role decomposes approved work rather than redefining it.
- Produce the artifact as `execution-tasks.md`.
- Use the `write-task-tracking` contract for section order, task fields, runtime-edge preservation, and validation because local tracking must stay stable across turns.
- Keep each task tracer-bullet shaped: thin, end-to-end, independently verifiable, and production-bound.
- Group tasks by implementation stream because stream context preserves the plan's sequencing logic.
- Record dependencies in terms of working behavior, not architecture-layer order.
- If the plan in `./execution-plan.md` carries runtime-edge obligations, preserve those obligations in tasks and include both structural and behavior-verifying acceptance criteria.
- Carry forward plan references to capability areas, `US1.x` story IDs, requirement IDs, and technical-design anchors when they help preserve traceability.
- Use `TODO: Confirm` when ambiguity changes task boundaries or dependency shape.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `execution-tasks.md`.
- The artifact must stay compatible with the `write-task-tracking` contract.
- Every task must include a stable identifier, status, dependency field, and plan references.
- Tasks must remain local tracking artifacts; do not create GitHub issues or external tickets.
- Do not create layer-only tasks that deliver no verifiable end-to-end behavior.
- Do not reduce tasks to generic implementation chores that drop the plan's capability, requirement, or design traceability.

## Requirements

Inputs:

- an approved execution plan or equivalent
- companion charter, user stories, requirements, and technical design when needed to clarify task boundaries
- repository context when needed to find real seams or sequencing constraints

Output:

- one local task-tracking artifact named `execution-tasks.md`

In scope:

- decomposing implementation streams into grouped tracer-bullet tasks
- assigning stable task IDs, statuses, dependencies, and plan references
- preserving traceability back to the execution plan
- preserving runtime-edge behavior and verification when the plan requires it
- surfacing blockers or ambiguity that affect task sequencing
- carrying through capability-area, `US1.x` story, requirement, and design traceability from the plan when useful

Out of scope:

- rewriting the execution plan
- code changes
- external issue creation

## Workflow

1. Confirm the user needs local task-tracking artifacts created from an approved execution plan.
2. Load the parent plan from `./execution-plan.md`, then read [`references/tracer-bullets.md`](./references/tracer-bullets.md).
3. Extract implementation streams, work breakdown items, sequencing constraints, validation checkpoints, runtime-edge obligations, and upstream traceability anchors from the plan.
4. Use companion specification artifacts only when task boundaries or dependencies need clarification.
5. Slice the work into thin tracer-bullet tasks grouped by stream.
6. Assign stable task IDs, explicit dependencies, statuses, and plan references.
7. For runtime-edge work, include both structural and behavior-verifying acceptance criteria instead of only bootstrap steps.
8. Preserve capability-area, `US1.x` story-ID, requirement-ID, and design-anchor references where they help keep the task tied to the approved spec pack.
9. Draft `execution-tasks.md` using the `write-task-tracking` contract.
10. Mark unresolved high-impact task-boundary or dependency ambiguity as `TODO: Confirm`.
11. Validate with `bash ../write-task-tracking/scripts/validate_tasks.sh <resolved-execution-tasks-path>`.
12. Deliver the local task-tracking artifact for execution.

## Gotchas

- If tasks are generated directly from charter, requirements, or design instead of the execution plan, local tracking drifts from approved sequencing immediately. Start from the plan and use other artifacts only to clarify boundaries.
- If tasks are split by architecture layer, they stop being independently verifiable and feedback arrives too late. Slice around thin working behavior instead.
- If stream grouping disappears, the artifact becomes a flat backlog and loses the coordination model that made the plan useful. Keep every task nested under its implementation stream.
- If dependencies are phrased as vague order hints, later turns cannot tell what truly blocks what. Name the prerequisite task or working behavior explicitly.
- If task IDs or statuses are inconsistent, the document turns into prose notes instead of a tracking surface. Keep stable fields on every task from the first draft.
- If capability areas, `US1.x` story IDs, requirement IDs, or design anchors disappear from plan references where they matter, the task list becomes locally coherent but globally untraceable. Keep the right anchors visible.
- If runtime-edge tasks stop at command or file existence checks, the operator-facing behavior never gets proved. Keep acceptance criteria on decoding, wiring, invocation, rendering, or equivalent visible outcomes when the plan requires them.
- If blockers and sequencing ambiguity are buried in narrative, the next implementation turn overcommits and stalls. Put them where the tracking artifact expects them and mark `TODO: Confirm` when needed.

## Deliverables

- `execution-tasks.md`
- grouped tracer-bullet tasks with stable identifiers, statuses, dependencies, and plan references
- local tracking structure suitable for iterative implementation updates
- plan references that preserve relevant `US1.x` story IDs, requirement IDs, and design anchors
- validation passing via the shared task-tracking validator

## References

- [`references/tracer-bullets.md`](./references/tracer-bullets.md): Read when: slicing execution-plan work into thin end-to-end tasks or deciding whether a dependency is behavior-oriented enough.

## Validation Checklist

- artifact filename is `execution-tasks.md`
- parent execution plan was used as the source of truth
- at least one implementation stream group exists
- every task has an ID, status, dependencies, and plan references
- dependencies are behavior-oriented rather than layer-oriented
- runtime-edge obligations are preserved explicitly or recorded as `None in parent plan`
- plan references preserve capability-area, `US1.x` story, requirement, or design traceability where relevant
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-task-tracking/scripts/validate_tasks.sh <resolved-execution-tasks-path>`
