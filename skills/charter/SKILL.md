---
name: charter
description: Produce charter artifacts from product intent and repository context. Use when a user wants a scope baseline with goals, non-goals, personas, and success criteria.
metadata:
  version: 0.2.0
  layer: specialist
  archetype: planning
  domain: specification-authoring
  dependencies:
    - write-charter
---

## Rules

- Keep this role focused on the charter artifact because it is the approval-gated scope baseline and user stories, requirements, and design belong downstream.
- Produce the charter as `charter.md` and keep the artifact limited to scope framing.
- Use the `write-charter` contract for section order, success-criterion numbering, uncertainty handling, and final validation because downstream roles depend on that shared shape.
- Ground the artifact in user intent first, then repository evidence when existing code or integrations constrain scope.
- Ask for clarification when missing detail changes goals, non-goals, actors, or success criteria; otherwise keep moving and mark `TODO: Confirm`.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `charter.md`.
- The artifact must stay compatible with the `write-charter` contract.
- Do not mix detailed functional requirements, technical design, or execution sequencing into the artifact.
- The charter must be approved before downstream specification work proceeds unless the user explicitly waives staged approval.
- Keep unresolved high-impact details explicit as `TODO: Confirm` instead of inventing certainty.

## Requirements

Inputs:

- product idea, feature request, or approved problem statement
- desired outcomes, goals, and scope boundaries
- known actors, stakeholders, and success measures
- repository evidence when existing behavior affects framing

Output:

- one complete charter artifact named `charter.md`

In scope:

- defining goals and non-goals
- naming personas and actors
- recording measurable success criteria
- preserving explicit uncertainty markers where needed

Out of scope:

- detailed user stories
- detailed requirements
- technical architecture
- implementation task planning
- code changes

## Workflow

1. Confirm the user wants a charter artifact before downstream specification or implementation work.
2. Gather desired outcomes, goals, non-goals, personas / actors, and success signals.
3. Inspect the repository only when existing code, integrations, or platform boundaries materially affect scope or success criteria.
4. Draft `charter.md` using the `write-charter` contract rather than inventing a new structure.
5. Keep the artifact on the approved scope baseline; move user-visible behaviors, detailed requirements, and design ideas out of the document.
6. Mark unresolved high-impact details as `TODO: Confirm`.
7. Validate with `bash ../write-charter/scripts/validate_charter.sh <resolved-charter-path>`.
8. Deliver the draft and request approval before user stories, requirements, or technical design proceed.

## Gotchas

- If goals are written without explicit non-goals, later artifacts quietly absorb adjacent ideas as scope. Make exclusion explicit before story writing starts.
- If personas are vague, user stories inherit generic actors and weak downstream behavior. Name concrete actors or use `TODO: Confirm`.
- If success criteria stay aspirational, reviewers cannot tell whether the spec pack is done or merely polished. Make completion signals concrete enough to verify.
- If you let this artifact accumulate behaviors or architecture, it becomes a second requirements document and duplicates downstream work. Keep it on framing only.
- If repository evidence already constrains scope and you ignore it, the charter reads clean but contradicts the product the team has to evolve. Inspect the code when it materially affects framing.
- If missing details are guessed to keep momentum, later artifacts inherit invented certainty and have to unwind it. Use `TODO: Confirm` for high-impact unknowns.

## Deliverables

- `charter.md`
- explicit goals, non-goals, personas / actors, and success criteria
- validation passing via the shared charter validator
- a draft ready for user review before user stories, requirements, or technical design

## Validation Checklist

- artifact filename is `charter.md`
- section order follows the `write-charter` contract
- goals and non-goals are explicit
- at least one success criterion exists
- detailed requirements and implementation strategy are not mixed into the artifact
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-charter/scripts/validate_charter.sh <resolved-charter-path>`
