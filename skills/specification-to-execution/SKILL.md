---
name: specification-to-execution
description: Orchestrate execution coordination artifacts from an approved specification pack. Use when a user wants an execution plan and local task tracking created from approved charter, user stories, requirements, and technical design.
metadata:
  version: 0.1.0
  layer: orchestration
  dependencies:
    - execution-planning
    - task-generation
---

## Rules

- Treat the approved specification pack as the source of truth because this workflow coordinates execution rather than redefining scope.
- Keep this workflow at the orchestration layer because role skills own the execution-plan and task-tracking contracts.
- Establish `generated_by.root_skill` as `specification-to-execution` for every artifact emitted from this workflow.
- Run role entry skills in order because task generation depends on an approved execution plan.
- Keep traceability explicit from charter, stories, requirements, and design into plan streams and local tasks.
- When source artifacts describe an operator-facing runtime edge, preserve that behavior into plan streams and tasks instead of weakening it into package bootstrap only.
- If missing detail changes task boundaries, sequencing, or validation, ask or mark `TODO: Confirm` instead of inventing certainty.

## Constraints

- This workflow coordinates execution artifacts; it does not replace underlying role or foundational contracts.
- Final output must include an execution plan and a local task-tracking artifact.
- Orchestration dependencies stay limited to role entry skills; do not name foundational contract skills here.
- Every execution artifact must carry deterministic provenance rooted in this workflow plus artifact-specific `source_artifacts` lineage.
- Do not rewrite the approved specification pack inside this workflow.

## Requirements

Inputs:

- approved charter artifact for one `<project-name>`
- approved user stories artifact for the same `<project-name>`
- approved requirements artifact for the same `<project-name>`
- approved technical design artifact for the same `<project-name>`
- repository context when local structure affects sequencing or task slicing
- known constraints, milestones, dependencies, or validation expectations

Outputs:

- `docs/plans/<project-name>-plan.md`
- `docs/tasks/<project-name>-tasks.md`
- one execution coordination pack aligned to the approved specification artifacts

In scope:

- orchestrating role entry skills from execution planning through task generation
- preserving one stable `<project-name>` across execution artifacts
- establishing root workflow provenance for plan and tasks
- checking that tasks trace back to the execution plan and approved spec pack
- surfacing blockers or ambiguity that affect sequencing or task boundaries

Out of scope:

- rewriting charter, stories, requirements, or technical design
- code changes
- external issue creation

## Workflow

1. Confirm the user wants execution coordination artifacts created from an approved specification pack.
2. Resolve or confirm one stable `<project-name>` across the approved charter, user-story, requirements, and technical-design artifacts.
3. Establish `root_skill = specification-to-execution` for the execution artifacts in this run.
4. Run `execution-planning` and confirm the plan sequences approved work rather than inventing new scope.
5. Run `task-generation` and confirm the tasks decompose the plan into thin local execution slices.
6. Perform a consistency pass:
   - `Scope Alignment` in the plan references the companion specification artifacts
   - plan and tasks preserve operator-facing runtime-edge obligations when the approved source artifacts describe them
   - runtime-edge tasks include both structural and behavior-verifying acceptance criteria
   - task groups and task references map back to the execution plan
   - unresolved sequencing or task-boundary issues remain marked `TODO: Confirm`
7. Deliver the execution coordination pack for implementation.

## Gotchas

- If this workflow starts filling gaps in the approved spec pack, execution artifacts quietly become a second design pass. Send scope changes back to the specification artifacts instead.
- If task generation starts before the plan is stable, local tracking drifts from approved sequencing immediately. Lock the plan first, then slice tasks from it.
- If `<project-name>` changes between plan and tasks, traceability breaks right when implementation starts. Preserve one stable name across both outputs.
- If tasks are accepted without checking plan references, the tracking artifact becomes a flat backlog instead of a coordination surface. Confirm every task set still points back to the plan.
- If runtime-edge behavior in the approved spec gets translated into only structural bootstrap work, implementation loses the operator-facing contract that made the runtime edge necessary. Keep behavior and verification explicit in both plan and tasks.
- If unresolved blockers are hidden to make the pack look execution-ready, implementation inherits false certainty and stalls later. Keep `TODO: Confirm` visible where evidence is missing.

## Deliverables

- `docs/plans/<project-name>-plan.md`
- `docs/tasks/<project-name>-tasks.md`
- explicit traceability from approved specification artifacts through plan and tasks
- deterministic provenance and source-artifact lineage on both execution artifacts
- explicit `TODO: Confirm` markers for unresolved execution ambiguity
- an execution coordination pack ready for implementation

## Validation Checklist

- orchestration dependencies stay limited to role entry skills
- approved charter, user stories, requirements, and technical design were used as the execution source of truth
- execution plan exists at `docs/plans/<project-name>-plan.md`
- local task-tracking artifact exists at `docs/tasks/<project-name>-tasks.md`
- both execution artifacts record `generated_by.root_skill = specification-to-execution`
- plan references the companion specification artifacts
- tasks reference the execution plan and preserve grouped execution structure
- runtime-edge obligations are either preserved explicitly or recorded as `None in approved spec`
- unresolved high-impact details are marked `TODO: Confirm`
