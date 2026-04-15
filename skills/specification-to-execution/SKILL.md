---
name: specification-to-execution
description: "Orchestrate execution artifacts from an approved specification pack. Use when a user needs an execution plan and local task tracking created from approved specification context."
license: MIT
metadata:
  version: "0.2.2"
  author: "urban (https://github.com)"
  layer: coordination
  dependencies:
    - document-traceability
    - artifact-naming
    - write-approval-view
    - execution-planning
    - task-generation
---

## Purpose

Coordinate execution artifacts from an approved specification pack into one stable execution root. Keep workflow order, provenance, lineage, and plan-to-task traceability explicit while specialist skills own the execution-plan and task-tracking contracts.

## Workflow rules

- Root workflow identity: `specification-to-execution`
- Workflow source of truth: approved `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md`
- Resolve one stable `<project-name>` and one stable execution spec-pack root for the full run; default root: `.specs/<project-name>/`
- Use specialist skills in this order: `execution-planning` -> `task-generation`
- Keep deterministic provenance and the workflow-owned `source_artifacts` map on every execution artifact
- Keep traceability explicit from the approved spec pack through plan streams and local tasks
- Preserve operator-facing runtime-edge behavior into plan and tasks when the approved spec pack describes it
- This workflow coordinates execution artifacts; it does not replace child artifact contracts
- Ask when ambiguity changes scope, sequencing, task boundaries, lineage, approval rules, or another blocking category

## Source artifact lineage

Use this exact workflow-owned `source_artifacts` map:

- `execution-plan.md` -> `charter`, `user_stories`, `requirements`, `technical_design`
- `execution-tasks.md` -> `execution_plan`

Resolved execution paths normally are:

- `charter` -> `<spec-pack-root>/charter.md`
- `user_stories` -> `<spec-pack-root>/user-stories.md`
- `requirements` -> `<spec-pack-root>/requirements.md`
- `technical_design` -> `<spec-pack-root>/technical-design.md`
- `execution_plan` -> `<spec-pack-root>/execution-plan.md`

Do not add extra source-artifact keys casually.

## Inputs

- approved `charter.md`
- approved `user-stories.md`
- approved `requirements.md`
- approved `technical-design.md`
- repository context when local structure affects sequencing or task slicing
- known constraints, milestones, dependencies, or validation expectations
- optional explicit execution destination root
- optional explicit artifact slug or preferred basename

## Outputs

- `<spec-pack-root>/execution-plan.md`
- `<spec-pack-root>/execution-tasks.md`
- derived approval views under `<spec-pack-root>/approval/` when execution approval is requested or required
- one execution artifact pack aligned to the approved specification artifacts

## Workflow

1. Confirm the user needs execution artifacts from an approved specification pack, then resolve one `<project-name>` and one execution spec-pack root for the full run.
2. Establish `generated_by.root_skill = specification-to-execution`; if execution approval is requested or required, use `<spec-pack-root>/approval/` for derived approval views.
3. Run `execution-planning`, write `<spec-pack-root>/execution-plan.md`, stamp `source_artifacts.charter`, `source_artifacts.user_stories`, `source_artifacts.requirements`, and `source_artifacts.technical_design`, and confirm the plan sequences approved work rather than inventing new scope.
4. Run `task-generation`, write `<spec-pack-root>/execution-tasks.md`, stamp `source_artifacts.execution_plan`, and confirm the tasks decompose the plan into thin local execution slices.
5. Run the consistency pass across plan traceability, task references, sequencing, runtime-edge obligations, and remaining uncertainty.
6. When execution approval is requested or required, generate and validate the needed per-artifact approval views and the final execution-pack approval view under `<spec-pack-root>/approval/`.
7. Deliver the execution artifact pack for implementation or review.

## Approval flow

- Use approval views only when execution approval is requested or already required.
- When a plan or task approval checkpoint exists, generate or refresh the per-artifact approval view for the exact current canonical snapshot before asking for approval.
- When full execution-pack review is requested, generate the final pack approval view after the consistency pass.
- Approval of a derived approval view counts as approval of the exact canonical snapshot it was derived from.
- Any canonical artifact change invalidates prior approval for that artifact and requires a regenerated approval view.
- Approval is whole-artifact only.
- No artifact may be approved while any `TODO: Confirm` remains.
- Approval views must derive from the canonical artifact only, persist under `<spec-pack-root>/approval/` in Markdown and HTML, and trace substantive claims back to exact canonical locations.
- When asking for approval on an HTML review surface in the terminal, include the resolved HTML path and the matching absolute `file://` URI for that file.

## Validation

- Confirm one stable `<project-name>` and one stable execution spec-pack root are used across the pack.
- Confirm `execution-plan.md` and `execution-tasks.md` exist in the chosen root.
- Confirm both execution artifacts record `generated_by.root_skill = specification-to-execution`.
- Confirm exact `source_artifacts` keys and resolved paths match this workflow's lineage map.
- Confirm plan references the companion specification artifacts and tasks reference the execution plan with grouped execution structure.
- Confirm runtime-edge obligations are either preserved explicitly or recorded as `None in approved spec` / `None in parent plan`.
- When execution approval is requested or required, confirm approval checkpoints use fresh approval views for the current canonical snapshots.
- When execution approval is requested or required, confirm each approval view passed `bash ../write-approval-view/scripts/validate_approval_view.sh ...` with the correct mode.
