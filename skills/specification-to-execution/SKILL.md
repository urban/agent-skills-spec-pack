---
name: specification-to-execution
description: "Orchestrate execution artifacts from an approved specification pack. Use when a user needs an execution plan and local task tracking created from approved specification context."
license: MIT
metadata:
  version: "0.2.0"
  author: "urban (https://github.com)"
  layer: coordination
  dependencies:
    - document-traceability
    - artifact-naming
    - execution-planning
    - task-generation
---

## Rules

- Treat the approved specification pack as the source of truth because this workflow coordinates execution rather than redefining scope.
- Keep this workflow at the coordination layer because specialist skills own the execution-plan and task-tracking contracts.
- Use `artifact-naming` to resolve one stable `<project-name>` for the workflow because the execution artifacts must align to one authored spec-pack root.
- Use `.specs/<project-name>/` as the default execution spec-pack root unless the user provides an explicit destination.
- Establish `generated_by.root_skill` as `specification-to-execution` for every artifact emitted from this workflow.
- Run specialist entry skills in order because task generation depends on an approved execution plan.
- Keep traceability explicit from charter, stories, requirements, and design into plan streams and local tasks.
- When source artifacts describe an operator-facing runtime edge, preserve that behavior into plan streams and tasks instead of weakening it into package bootstrap only.
- If missing detail changes task boundaries, sequencing, or validation, ask or mark `TODO: Confirm` instead of inventing certainty.

## Constraints

- This workflow coordinates execution artifacts; it does not replace underlying specialist or foundational contracts.
- Final output must include `execution-plan.md` and `execution-tasks.md`.
- Coordination must use specialist skills for artifact-producing work and may use `artifact-naming` only for workflow-wide naming and placement coordination.
- Every execution artifact must carry deterministic provenance rooted in this workflow plus the canonical `source_artifacts` lineage required by this workflow.
- Do not rewrite the approved specification pack inside this workflow.

## Source Artifact Lineage

This workflow owns the canonical `source_artifacts` lineage map for execution artifacts.

Use exactly these `source_artifacts` artifact-type keys in this workflow:

- `execution-plan.md` -> `charter`, `user_stories`, `requirements`, `technical_design`
- `execution-tasks.md` -> `execution_plan`

Resolved execution paths should normally be:

- `charter` -> `<spec-pack-root>/charter.md`
- `user_stories` -> `<spec-pack-root>/user-stories.md`
- `requirements` -> `<spec-pack-root>/requirements.md`
- `technical_design` -> `<spec-pack-root>/technical-design.md`
- `execution_plan` -> `<spec-pack-root>/execution-plan.md`

For execution planning specifically:

- `execution-planning` produces `execution-plan.md`
- the shared `write-execution-plan` contract defines the plan structure
- this workflow defines that `execution-plan.md` records exactly `source_artifacts.charter`, `source_artifacts.user_stories`, `source_artifacts.requirements`, and `source_artifacts.technical_design` resolved to the execution spec-pack root

For task generation specifically:

- `task-generation` produces `execution-tasks.md`
- the shared `write-task-tracking` contract defines the task structure
- this workflow defines that `execution-tasks.md` records exactly `source_artifacts.execution_plan = <spec-pack-root>/execution-plan.md`

Do not add extra source artifact-types casually.

## Requirements

Inputs:

- approved charter artifact
- approved user stories artifact
- approved requirements artifact
- approved technical-design artifact
- repository context when local structure affects sequencing or task slicing
- known constraints, milestones, dependencies, or validation expectations
- optional explicit execution destination root
- optional explicit artifact slug or preferred basename

Outputs:

- `.specs/<project-name>/execution-plan.md`
- `.specs/<project-name>/execution-tasks.md`
- one execution artifacts pack aligned to the approved specification artifacts

In scope:

- resolving one workflow-wide `<project-name>` with `artifact-naming`
- selecting and preserving one execution spec-pack root for the workflow
- orchestrating specialist entry skills from execution planning through task generation
- establishing root workflow provenance and canonical `source_artifacts` lineage for plan and tasks
- checking that tasks trace back to the execution plan and approved spec pack
- surfacing blockers or ambiguity that affect sequencing or task boundaries

Out of scope:

- rewriting charter, stories, requirements, or technical design
- code changes
- external issue creation

## Workflow

1. Confirm the user needs execution artifacts created from an approved specification pack.
2. Resolve `<project-name>` once with `artifact-naming`, honoring an explicit artifact slug or preferred basename when provided.
3. Resolve the execution spec-pack root once for the full run, defaulting to `.specs/<project-name>/` unless the user provides an explicit destination.
4. Establish `root_skill = specification-to-execution` for the execution artifacts in this run.
5. Run `execution-planning`, write the result to `<spec-pack-root>/execution-plan.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md`, `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, `source_artifacts.requirements = <spec-pack-root>/requirements.md`, and `source_artifacts.technical_design = <spec-pack-root>/technical-design.md`, and confirm the plan sequences approved work rather than inventing new scope.
6. Run `task-generation`, write the result to `<spec-pack-root>/execution-tasks.md`, stamp `source_artifacts.execution_plan = <spec-pack-root>/execution-plan.md`, and confirm the tasks decompose the plan into thin local execution slices.
7. Perform a consistency pass:
   - `Scope Alignment` in the plan references the companion specification artifacts
   - plan streams visibly align to user-story capability areas, requirement IDs, and technical-design concerns
   - plan and tasks preserve operator-facing runtime-edge obligations when the approved source artifacts describe them
   - runtime-edge tasks include both structural and behavior-verifying acceptance criteria
   - task groups and task references map back to the execution plan
   - unresolved sequencing or task-boundary issues remain marked `TODO: Confirm`
8. Deliver the execution artifacts pack for implementation.

## Gotchas

- If this workflow starts filling gaps in the approved spec pack, execution artifacts quietly become a second design pass. Send scope changes back to the specification artifacts instead.
- If task generation starts before the plan is stable, local tracking drifts from approved sequencing immediately. Lock the plan first, then slice tasks from it.
- If `<project-name>` changes between plan and tasks, traceability breaks right when implementation starts. Resolve naming once and preserve it across both outputs.
- If the execution spec-pack root drifts between plan and tasks, the coordination artifacts split even when the content still aligns. Resolve placement once for the workflow.
- If tasks are accepted without checking plan references, the tracking artifact becomes a flat backlog instead of a coordination surface. Confirm every task set still points back to the plan.
- If runtime-edge behavior in the approved spec gets translated into only structural bootstrap work, implementation loses the operator-facing contract that made the runtime edge necessary. Keep behavior and verification explicit in both plan and tasks.
- If capability areas, requirement IDs, or design anchors disappear between spec, plan, and task artifacts, downstream execution loses reversibility and reviewability. Keep those anchors visible where they matter.
- If unresolved blockers are hidden to make the pack look execution-ready, implementation inherits false certainty and stalls later. Keep `TODO: Confirm` visible where evidence is missing.

## Deliverables

- `.specs/<project-name>/execution-plan.md`
- `.specs/<project-name>/execution-tasks.md`
- explicit traceability from approved specification artifacts through plan and tasks
- deterministic provenance and source-artifact lineage on both execution artifacts
- explicit `TODO: Confirm` markers for unresolved execution ambiguity
- an execution artifacts pack ready for implementation

## Validation Checklist

- `artifact-naming` was used to resolve one stable `<project-name>` for the workflow
- execution plan exists at `<spec-pack-root>/execution-plan.md`
- local task-tracking artifact exists at `<spec-pack-root>/execution-tasks.md`
- both execution artifacts record `generated_by.root_skill = specification-to-execution`
- `execution-plan.md` records exactly `source_artifacts.charter`, `source_artifacts.user_stories`, `source_artifacts.requirements`, and `source_artifacts.technical_design` resolved to the execution spec-pack root
- `execution-tasks.md` records exactly `source_artifacts.execution_plan = <spec-pack-root>/execution-plan.md`
- plan references the companion specification artifacts
- tasks reference the execution plan and preserve grouped execution structure
- runtime-edge obligations are either preserved explicitly or recorded as `None in approved spec`
- unresolved high-impact details are marked `TODO: Confirm`
