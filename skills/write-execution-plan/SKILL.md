---
name: write-execution-plan
description: "Write and validate canonical execution-plan artifacts. Use when a task creates, derives, reviews, or validates implementation coordination from approved specification context."
license: MIT
metadata:
  version: "0.3.0"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Rules

- Keep execution plans downstream of approved charter, user stories, requirements, and technical design because plans coordinate implementation; they do not redefine scope.
- Preserve canonical frontmatter shape and validate created artifacts with the shared provenance validator when the workflow stamps provenance.
- Group work into meaningful implementation streams because flat task dumps hide sequencing and ownership.
- Preserve explicit traceability back to companion specification artifacts because execution work must stay anchored to approved inputs.
- Record sequencing, validation checkpoints, and progress tracking explicitly because these are the plan's core value.
- Require one explicit runtime-edge obligations field so authored planning must say either what operator-facing runtime behavior is preserved or `None in approved spec`.
- When runtime-edge obligations exist upstream, preserve behavior and verification, not only structure.
- Organize stream objectives and work breakdown around approved user-story capability areas, story identifiers, requirement identifiers, and technical-design interfaces or failure strategy where relevant.
- When canonical user stories are available, use their `US1.x` identifiers in scope alignment and traceability notes so plan and task artifacts can link back to stable story anchors.
- Mark unresolved execution ambiguity as `TODO: Confirm` because invented certainty creates bad sequencing.

## Constraints

- Output must be one Markdown artifact.
- The shared execution-plan contract does not define workflow-wide `source_artifacts` policy.
- Required sections must appear in canonical order.
- `Scope Alignment` must reference companion charter, user-story, requirements, and technical-design artifacts.
- `Scope Alignment` must include `Story capability areas:`, `Story anchors:`, and `Runtime-edge obligations:` lines.
- Include implementation streams, work breakdown, sequencing, validation checkpoints, risks, and progress tracking.
- Do not collapse the plan into rewritten charter, copied five-field user stories, requirements prose, architecture prose, commit scripts, or file-by-file coding instructions.

## Requirements

A valid execution plan must include these sections in this order:

1. `Execution Summary`
2. `Scope Alignment`
3. `Implementation Streams`
4. `Work Breakdown`
5. `Dependency and Sequencing Strategy`
6. `Validation Checkpoints`
7. `Risks and Mitigations`
8. `Progress Tracking`
9. `Further Notes`

Minimum content expectations:

- canonical frontmatter shape when provenance is stamped for the workflow
- explicit references to companion charter, user stories, requirements, and technical design
- explicit `Story capability areas:` and `Story anchors:` lines in `Scope Alignment`
- an explicit `Runtime-edge obligations:` line with preserved behavior or `None in approved spec`
- at least one named implementation stream
- grouped work items under the stream model
- explicit sequencing notes
- explicit progress-tracking fields
- `TODO: Confirm` where high-impact execution detail is unresolved

Inputs:

- approved or derived charter
- approved or derived user stories
- approved or derived requirements
- approved or derived technical design
- any known implementation constraints, milestones, or sequencing risks

Output:

- one execution plan Markdown artifact that downstream task-tracking or implementation work can consume directly

## Workflow

1. Confirm the approved scope and identify the companion charter, user stories, requirements, and technical-design artifacts.
2. Draft from [`assets/plan-template.md`](./assets/plan-template.md) so section order stays canonical.
3. Translate the approved specification into major implementation streams rather than flat tasks.
4. Use user-story capability areas and `US1.x` story IDs to shape stream boundaries, work clusters, and traceability notes.
5. Use requirement IDs to anchor concrete obligations and validation needs.
6. Use technical-design interfaces, integration points, and failure strategy to shape sequencing, coordination risk, and validation checkpoints.
7. Record `Runtime-edge obligations:` explicitly from the approved source artifacts, using `None in approved spec` only when the upstream artifacts do not describe one.
8. Group work items under those streams with enough detail to coordinate implementation without becoming commit instructions.
9. Record dependency order, sequencing rationale, validation checkpoints, and major execution risks.
10. Add progress-tracking fields that let later turns update status without changing the contract.
11. Mark unresolved high-impact execution details as `TODO: Confirm`.
12. Validate the finished artifact with [`scripts/validate_plan.sh`](./scripts/validate_plan.sh).

## Gotchas

- If the plan rewrites product scope, reviewers lose the boundary between approved intent and execution choices. Treat charter, stories, requirements, and design as upstream inputs, not editable plan content.
- If you dump a flat backlog instead of implementation streams, dependency reasoning disappears and parallel work becomes guesswork. Group work by meaningful execution stream first.
- If `Scope Alignment` omits companion artifacts, downstream task generation cannot prove what the plan is implementing. Reference the source artifacts explicitly.
- If `Scope Alignment` carries capability areas but not canonical `US1.x` story IDs, later story renames make plan traceability brittle. Keep the story anchors explicit.
- If `Runtime-edge obligations:` is missing or hand-waved, operator-facing behavior quietly drops out of the plan. State the preserved behavior explicitly or record `None in approved spec`.
- If the plan ignores user-story capability areas, story IDs, requirement IDs, or design interfaces, execution streams become arbitrary and traceability weakens. Anchor streams and checkpoints to those upstream structures.
- If work items become commit-by-commit instructions, the plan ages immediately and stops being reusable. Keep it at coordination level, not terminal-command level.
- If validation checkpoints are vague, implementation can appear complete while missing the only tests that matter. Name concrete checkpoints tied to the plan's streams, obligations, and risks.
- If progress tracking is an afterthought, later updates mutate the plan into ad hoc notes and break reviewability. Include explicit status fields from the start.
- If unresolved sequencing risks get smoothed over, task tracking inherits false certainty and stalls later. Use `TODO: Confirm` where ordering or prerequisites are not actually known.
- If workflow lineage rules are embedded here, the foundational contract stops being reusable across execution workflows. Leave workflow-specific `source_artifacts` policy to coordination.

## Deliverables

- A Markdown execution plan with canonical frontmatter shape and section order.
- Explicit traceability to charter, user stories, requirements, and technical design.
- Scope and work traceability that references relevant `US1.x` story IDs when stories are available.
- Named implementation streams, grouped work breakdown, sequencing, validation checkpoints, and progress tracking.
- A runtime-edge obligations statement that preserves operator-facing behavior or records `None in approved spec`.
- Clear `TODO: Confirm` markers for unresolved high-impact execution details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation when the workflow stamps provenance.
- All required sections exist and are in the correct order.
- `Scope Alignment` references charter, user stories, requirements, and technical design.
- `Scope Alignment` includes `Story capability areas:`, `Story anchors:`, and `Runtime-edge obligations:`.
- At least one implementation stream is present.
- Work breakdown, sequencing, validation checkpoints, and progress tracking are explicit.
- Streams and checkpoints trace to user-story capability areas, `US1.x` story IDs, requirement IDs, and design concerns where relevant.
- The artifact remains a coordination plan rather than rewritten charter, stories, requirements, design, or commit instructions.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_plan.sh <plan-file>`
