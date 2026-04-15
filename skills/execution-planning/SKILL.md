---
name: execution-planning
description: "Produce execution-plan artifacts from an approved specification pack. Use when a user needs implementation coordination documented before coding begins."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: implementation-planning
  dependencies:
    - write-execution-plan
---

## Purpose

Produce `execution-plan.md` from an approved specification pack. Turn approved scope into implementation streams, sequencing, validation checkpoints, and progress tracking without re-owning product scope or generating local task tracking.

## Boundaries

- Output filename: `execution-plan.md`
- Source of truth: approved `./charter.md`, `./user-stories.md`, `./requirements.md`, and `./technical-design.md`; use repository context only when local structure affects sequencing or validation
- Artifact contract: follow `../write-execution-plan/SKILL.md`
- In scope:
  - align implementation work to approved artifacts
  - define implementation streams and grouped work breakdown
  - document dependency order, validation checkpoints, risks, and progress tracking
  - preserve runtime-edge behavioral obligations when they exist upstream
  - carry forward capability areas, `US1.x` story IDs, requirement IDs, and design anchors where they shape execution
- Out of scope:
  - rewriting scope decisions
  - generating local task-tracking artifacts
  - code changes
- Ask only when ambiguity changes sequencing, task boundaries, runtime-edge behavior, validation, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- approved `./charter.md`
- approved `./user-stories.md`
- approved `./requirements.md`
- approved `./technical-design.md`
- repository context when local structure affects sequencing or validation
- known constraints, dependencies, milestones, or validation expectations

## Output

- `execution-plan.md`
- one execution-plan artifact downstream task tracking and implementation can trust for sequencing, validation, and coordination

## Workflow

1. Load the approved companion artifacts; inspect repo structure, integration points, and test surfaces only where they materially affect sequencing or validation.
2. Read stories for capability areas, `US1.x` IDs, boundary or failure stories, and observable outcomes.
3. Read requirements for obligation IDs and verifiable constraints.
4. Read technical design for interfaces, integration points, implementation strategy, failure or recovery strategy, and any operator-facing runtime-edge obligations.
5. Translate the approved specification into a small number of meaningful implementation streams.
6. Preserve runtime-edge behavior in stream objectives, work breakdown, and validation checkpoints when upstream artifacts describe it.
7. Draft `execution-plan.md` with the shared contract.
8. Mark unresolved high-impact execution detail as `TODO: Confirm`.
9. Validate with `bash ../write-execution-plan/scripts/validate_plan.sh <resolved-execution-plan-path>`.
10. Deliver the plan as the implementation coordination artifact.

## Validation

- Run: `bash ../write-execution-plan/scripts/validate_plan.sh <resolved-execution-plan-path>`
- Confirm filename is `execution-plan.md`, section order matches the shared contract, and `Scope Alignment` references charter, user stories, requirements, and technical design.
- Confirm `Story capability areas:`, `Story anchors:`, and `Runtime-edge obligations:` are explicit.
- Confirm at least one implementation stream exists and work breakdown, sequencing, validation checkpoints, risks, and progress tracking are explicit.
- Confirm streams and checkpoints visibly trace to capability areas, `US1.x`, requirement IDs, and design concerns where relevant.
- Confirm unresolved high-impact details stay `TODO: Confirm`.

## Approval-view focus

- highest-risk streams and sequencing decisions
- runtime-edge obligations and how they are preserved into implementation
- validation checkpoints most likely to catch false progress
- blockers or `TODO: Confirm` items that could distort task generation
