---
name: execution-planning
description: "Produce execution-plan artifacts from an approved specification pack. Use when a user needs implementation coordination documented before coding begins."
license: MIT
metadata:
  version: "0.3.0"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: implementation-planning
  dependencies:
    - write-execution-plan
---

## Rules

Turn an approved specification pack into an execution-oriented plan.

- Treat approved charter, user stories, requirements, and technical design as the source of truth because this role coordinates implementation rather than redefining scope.
- Produce the artifact as `execution-plan.md`.
- Use the `write-execution-plan` contract for section order, traceability, runtime-edge preservation, and validation because downstream task tracking depends on that shape.
- Group work into meaningful implementation streams because flat work lists hide sequencing and dependency structure.
- Explicitly inspect approved source artifacts from `./charter.md`, `./user-stories.md`, `./requirements.md`, and `./technical-design.md` for operator-facing runtime-edge obligations and preserve that behavior into streams, work breakdown, and validation checkpoints.
- Use user-story capability areas and `US1.x` story IDs to shape implementation streams and traceability notes.
- Use requirement IDs to anchor execution obligations.
- Use technical-design interfaces, integration points, and failure strategy to shape sequencing and checkpoints.
- Mark unresolved execution ambiguity as `TODO: Confirm` instead of forcing false certainty into the plan.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `execution-plan.md`.
- The artifact must stay compatible with the `write-execution-plan` contract.
- `Scope Alignment` must reference the companion charter, user stories, requirements, and technical-design artifacts.
- If the approved source artifacts describe a runtime edge, the plan must preserve operator-facing runtime behavior rather than reducing the work to package or command existence.
- Do not restate full charter, copied five-field user stories, requirements, or technical design as if the plan owns them.
- Do not turn the plan into commit-by-commit instructions, file inventories, or code snippets.

## Requirements

Inputs:

- approved charter artifact
- approved user stories artifact
- approved requirements artifact
- approved technical-design artifact
- repository context when local structure affects sequencing or validation
- known constraints, dependencies, milestones, or validation expectations

Output:

- one complete execution plan named `execution-plan.md`

In scope:

- aligning implementation work to approved artifacts
- defining implementation streams and grouped work breakdown
- documenting dependency order, validation checkpoints, risks, and progress tracking
- preserving explicit traceability back to the spec pack
- preserving runtime-edge behavioral obligations when they exist upstream
- carrying forward user-story capability areas, `US1.x` story IDs, requirements traceability, and technical-design interfaces or failure strategy into execution structure

Out of scope:

- rewriting scope decisions
- generating local task-tracking artifacts
- code changes

## Workflow

1. Confirm the user needs execution-plan artifacts from an approved specification pack before coding begins, then gather the approved companion artifacts.
2. Inspect repository structure, integration points, and test surfaces when they materially affect sequencing or validation.
3. Read the approved user stories for capability areas, `US1.x` story IDs, boundary/failure stories, and observable outcomes.
4. Read the approved requirements for concrete obligation IDs and verifiable constraints.
5. Read the approved technical design for interfaces, integration points, implementation strategy, and failure/recovery strategy.
6. Read the approved technical design and requirements explicitly for operator-facing runtime-edge obligations such as input decoding, service assembly, runner invocation, and outcome rendering.
7. Translate the approved scope into a small number of meaningful implementation streams.
8. Group work under those streams instead of outputting a flat task dump.
9. Preserve runtime-edge behavior in both work breakdown and validation checkpoints when upstream artifacts describe it.
10. Draft `execution-plan.md` using the `write-execution-plan` contract.
11. Mark unresolved high-impact execution details as `TODO: Confirm`.
12. Validate with `bash ../write-execution-plan/scripts/validate_plan.sh <resolved-execution-plan-path>`.
13. Deliver the plan as the implementation coordination artifact.

## Gotchas

- If the plan starts rewriting charter, requirements, or design, downstream execution loses the boundary between approved scope and implementation choices. Keep the companion artifacts as references, not editable content.
- If work is emitted as a flat backlog, dependency reasoning disappears and parallelization becomes guesswork. Build stream structure first, then place work inside it.
- If `Scope Alignment` does not point back to the charter, user stories, requirements, and technical design, later task generation cannot prove what the plan is implementing. Keep traceability explicit.
- If execution streams ignore capability areas, story IDs, requirement IDs, or technical-design boundaries, the plan looks organized but downstream tasks drift from the spec pack. Keep those anchors visible.
- If runtime-edge obligations from the approved spec get flattened into bootstrap chores, the plan loses the operator-facing behavior that implementation must prove. Keep decode, composition, invocation, rendering, and verification visible when they are in scope.
- If validation checkpoints are generic, implementation can look complete while missing the only tests that matter. Tie checkpoints to the actual streams, obligations, interfaces, and risk areas.
- If progress tracking is vague or absent, later updates turn the artifact into narrative notes instead of a coordination surface. Add explicit tracking fields from the first draft.
- If unresolved sequencing risks are hidden to make the plan look polished, task tracking inherits false certainty and stalls later. Use `TODO: Confirm` where order or prerequisites are not yet proved.

## Deliverables

- `execution-plan.md`
- explicit scope alignment references to charter, user stories, requirements, and technical design
- scope and work traceability that references relevant `US1.x` story IDs when stories are available
- named implementation streams with grouped work breakdown
- explicit runtime-edge obligations field with preserved operator-facing behavior or `None in approved spec`
- dependency strategy, validation checkpoints, risks, and progress tracking
- validation passing via the shared execution-plan validator

## Validation Checklist

- artifact filename is `execution-plan.md`
- section order follows the `write-execution-plan` contract
- `Scope Alignment` references charter, user stories, requirements, and technical design
- runtime-edge obligations are recorded explicitly
- at least one implementation stream exists
- work breakdown, sequencing, validation checkpoints, and progress tracking are explicit
- streams and checkpoints visibly trace to capability areas, `US1.x` story IDs, requirement IDs, and design concerns where relevant
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-execution-plan/scripts/validate_plan.sh <resolved-execution-plan-path>`
