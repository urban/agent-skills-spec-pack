---
name: execution-planning
description: Produce execution-plan artifacts from approved charter, user stories, requirements, and technical design. Use when a user wants implementation coordination documented before coding starts.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: planning
  domain: implementation-planning
  dependencies:
    - artifact-naming
    - document-traceability
    - write-execution-plan
---

## Rules

Turn an approved specification pack into an execution-oriented plan.

- Treat approved charter, user stories, requirements, and technical design as the source of truth because this role coordinates implementation rather than redefining scope.
- Use `artifact-naming` to resolve and preserve `<project-name>` because the plan must align with the companion skill-pack artifacts.
- Use `document-traceability` to stamp canonical provenance plus `source_artifacts.charter`, `source_artifacts.user_stories`, `source_artifacts.requirements`, and `source_artifacts.technical_design`.
- Use the `write-execution-plan` contract for section order, traceability, runtime-edge preservation, and validation because downstream task tracking depends on that shape.
- Group work into meaningful implementation streams because flat work lists hide sequencing and dependency structure.
- Explicitly inspect the approved source artifacts for operator-facing runtime-edge obligations and preserve that behavior into streams, work breakdown, and validation checkpoints.
- Mark unresolved execution ambiguity as `TODO: Confirm` instead of forcing false certainty into the plan.

## Constraints

- Output must be one Markdown artifact at `.specs/<project-name>/execution-plan.md`.
- The artifact must stay compatible with the `write-execution-plan` contract.
- The artifact must record `source_artifacts.charter`, `source_artifacts.user_stories`, `source_artifacts.requirements`, and `source_artifacts.technical_design`.
- `Scope Alignment` must reference the companion charter, user stories, requirements, and technical design artifacts.
- If the approved source artifacts describe a runtime edge, the plan must preserve operator-facing runtime behavior rather than reducing the work to package or command existence.
- Do not restate full charter, requirements, or technical design as if the plan owns them.
- Do not turn the plan into commit-by-commit instructions, file inventories, or code snippets.

## Requirements

Inputs:

- approved charter artifact for the same `<project-name>`
- approved user stories artifact for the same `<project-name>`
- approved requirements artifact for the same `<project-name>`
- approved technical design artifact for the same `<project-name>`
- repository context when local structure affects sequencing or validation
- known constraints, dependencies, milestones, or validation expectations

Output:

- one complete execution plan at `.specs/<project-name>/execution-plan.md`

In scope:

- aligning implementation work to approved artifacts
- defining implementation streams and grouped work breakdown
- documenting dependency order, validation checkpoints, risks, and progress tracking
- preserving explicit traceability back to the spec pack
- preserving runtime-edge behavioral obligations when they exist upstream

Out of scope:

- rewriting scope decisions
- generating local task-tracking artifacts
- code changes

## Workflow

1. Confirm the user wants an execution plan before coding and gather the approved companion artifacts.
2. Resolve `<project-name>` with `artifact-naming` and keep it stable for the run.
3. Capture `root_skill` from the active execution workflow and set `producing_skill = execution-planning`.
4. Inspect repository structure, integration points, and test surfaces when they materially affect sequencing or validation.
5. Read the approved technical design and requirements explicitly for operator-facing runtime-edge obligations such as input decoding, service assembly, runner invocation, and outcome rendering.
6. Translate the approved scope into a small number of meaningful implementation streams.
7. Group work under those streams instead of outputting a flat task dump.
8. Preserve runtime-edge behavior in both work breakdown and validation checkpoints when upstream artifacts describe it.
9. Draft `.specs/<project-name>/execution-plan.md` using the `write-execution-plan` contract.
10. Stamp canonical provenance plus required source-artifact lineage.
11. Mark unresolved high-impact execution details as `TODO: Confirm`.
12. Validate with `bash ../write-execution-plan/scripts/validate_plan.sh .specs/<project-name>/execution-plan.md`.
13. Deliver the plan as the implementation coordination artifact.

## Gotchas

- If the plan starts rewriting charter, requirements, or design, downstream execution loses the boundary between approved scope and implementation choices. Keep the companion artifacts as references, not editable content.
- If work is emitted as a flat backlog, dependency reasoning disappears and parallelization becomes guesswork. Build stream structure first, then place work inside it.
- If `Scope Alignment` does not point back to the charter, user stories, requirements, and technical design, later task generation cannot prove what the plan is implementing. Keep traceability explicit.
- If runtime-edge obligations from the approved spec get flattened into bootstrap chores, the plan loses the operator-facing behavior that implementation must prove. Keep decode, composition, invocation, rendering, and verification visible when they are in scope.
- If validation checkpoints are generic, implementation can look complete while missing the only tests that matter. Tie checkpoints to the actual streams and risk areas.
- If progress tracking is vague or absent, later updates turn the artifact into narrative notes instead of a coordination surface. Add explicit tracking fields from the first draft.
- If unresolved sequencing risks are hidden to make the plan look polished, task tracking inherits false certainty and stalls later. Use `TODO: Confirm` where order or prerequisites are not yet proved.

## Deliverables

- `.specs/<project-name>/execution-plan.md`
- explicit scope alignment references to charter, user stories, requirements, and technical design
- named implementation streams with grouped work breakdown
- explicit runtime-edge obligations field with preserved operator-facing behavior or `None in approved spec`
- dependency strategy, validation checkpoints, risks, and progress tracking
- validation passing via the shared execution-plan validator

## Validation Checklist

- artifact path is `.specs/<project-name>/execution-plan.md`
- section order follows the `write-execution-plan` contract
- required source-artifact roles are present
- `Scope Alignment` references charter, user stories, requirements, and technical design
- runtime-edge obligations are recorded explicitly
- at least one implementation stream exists
- work breakdown, sequencing, validation checkpoints, and progress tracking are explicit
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-execution-plan/scripts/validate_plan.sh .specs/<project-name>/execution-plan.md`
