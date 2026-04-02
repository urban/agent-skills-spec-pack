---
name: specification-authoring
description: Orchestrate an authored specification pack for a new product or major feature. Use when a user wants charter, user-story, requirements, and technical-design artifacts created before downstream coordination or implementation.
metadata:
  version: 0.1.0
  layer: orchestration
  dependencies:
    - charter
    - user-story-authoring
    - requirements
    - technical-design
---

## Rules

- Keep this workflow at the orchestration layer because expertise skills own artifact-specific contracts and validation.
- Resolve one stable `<project-name>` early and preserve it across every authored artifact because path drift breaks downstream alignment.
- Establish `generated_by.root_skill` as `specification-authoring` for every artifact emitted from this workflow.
- Run expertise entry skills in order because charter sets scope and success, stories define user-visible outcomes, requirements define product obligations, and design explains the solution.
- Do not start `user-story-authoring` until the user explicitly approves `docs/specs/<project-name>/charter.md`.
- Do not start `requirements` until the user explicitly approves `docs/specs/<project-name>/user-stories.md`.
- Do not start `technical-design` until the user explicitly approves `docs/specs/<project-name>/requirements.md`.
- Do not start the final cross-artifact consistency pass or final pack delivery until the user explicitly approves `docs/specs/<project-name>/technical-design.md`.
- Keep cross-artifact review explicit because workflow value comes from alignment, not from merely invoking four skills.
- If missing detail changes scope or artifact shape, ask or mark `TODO: Confirm` instead of letting downstream artifacts invent certainty.

## Constraints

- This workflow coordinates artifacts; it does not replace underlying expertise or foundational contracts.
- Final output must include charter, user stories, requirements, and technical design.
- Orchestration dependencies stay limited to expertise entry skills; do not name foundational contract skills here.
- Every authored artifact must carry deterministic provenance rooted in this workflow plus artifact-specific `source_artifacts` lineage.
- Never author the full specification pack in one uninterrupted pass unless the user explicitly waives stage-by-stage approval.
- Do not start downstream coordination or implementation from this workflow unless the user explicitly asks for that next phase.

## Requirements

Inputs:

- product idea, feature request, or approved problem statement
- desired outcomes, goals, and scope boundaries
- repository context when existing code, integrations, or constraints matter
- clarification on unknowns that would materially change the artifact set

Outputs:

- `docs/specs/<project-name>/charter.md`
- `docs/specs/<project-name>/user-stories.md`
- `docs/specs/<project-name>/requirements.md`
- `docs/specs/<project-name>/technical-design.md`
- one authored spec pack with a stable `<project-name>` reused across all artifacts

In scope:

- orchestrating expertise entry skills in authored order
- preserving pack-wide naming and scope consistency
- establishing root workflow provenance for every authored artifact
- checking that artifacts map cleanly from charter through design

Out of scope:

- redefining expertise-level artifact contracts in this workflow
- producing execution coordination artifacts
- doing implementation work
- hiding unresolved scope or intent behind polished prose

## Workflow

1. Confirm the user wants a specification pack authored before downstream coordination or implementation.
2. Resolve `<project-name>` once and preserve it for the full run.
3. Establish `root_skill = specification-authoring` for all authored artifacts in this run.
4. Co-create or confirm the core outcomes, goals, non-goals, personas / actors, success criteria, and scope boundaries.
5. Run `charter`, draft `docs/specs/<project-name>/charter.md`, present it to the user, and wait for explicit approval before continuing.
6. If the user does not approve the charter, revise it or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
7. Run `user-story-authoring`, draft `docs/specs/<project-name>/user-stories.md`, present it to the user, and wait for explicit approval before continuing.
8. If the user does not approve the story set, revise stories or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
9. Run `requirements`, draft `docs/specs/<project-name>/requirements.md`, present it to the user, and wait for explicit approval before continuing.
10. If the user does not approve the requirements, revise requirements or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
11. Run `technical-design`, draft `docs/specs/<project-name>/technical-design.md`, present it to the user, and wait for explicit approval before continuing.
12. If the user does not approve the technical design, revise design or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
13. Perform a cross-artifact consistency pass:

- charter scope, actors, and success criteria support the story set
- stories stay within approved charter scope
- user-visible requirements map to approved stories
- requirements do not re-own goals, non-goals, personas, or success criteria from the charter
- requirements map to design
- every artifact carries canonical provenance and the correct `source_artifacts` roles
- unresolved items stay explicit as `TODO: Confirm`

14. Deliver the authored specification pack for approval or downstream coordination.

## Approval Contract

- Approval must be explicit user confirmation in the conversation.
- Silence, implied satisfaction, a request for a full specification pack, or lack of objections does not count as approval.
- A request to continue only counts as approval for the artifact currently under review unless the user explicitly waives stage-by-stage approval.
- If approval is ambiguous, ask for confirmation before continuing.

## Gotchas

- If you let each role pick its own artifact name, the pack looks complete but downstream links and review context split across multiple directories. Resolve `<project-name>` once before any artifact is written.
- If user stories start before the charter is stable, actors and success checks drift and later requirements look aligned only because they copied the drift forward. Fix the charter first, then author stories from it.
- If requirements start before the stories are stable, product obligations get formalized around behavior the user has not approved yet. Fix story coverage first, then derive requirements from it.
- If you produce `user-stories.md` before `charter.md` is explicitly approved, produce `requirements.md` before `user-stories.md` is explicitly approved, or produce `technical-design.md` before `requirements.md` is explicitly approved, you have violated the workflow even if the documents are high quality. Stop, return to the last approved artifact, and re-enter the gated review flow.
- If requirements restate goals, non-goals, personas, or success criteria that the charter already owns, the pack grows redundant and future edits drift across files. Keep each artifact on its side of the boundary.
- If technical design is allowed to solve imagined future needs, architecture quietly becomes the place where scope expands. Push speculative work back to requirements or mark it `TODO: Confirm`.
- If provenance is missing or the wrong source-artifact roles are stamped, later feedback cannot tell which authored branch drifted. Validate metadata before treating the pack as approved.
- If you treat the workflow as a thin router and skip the consistency pass, contradictions survive in polished artifacts until implementation exposes them. Explicitly trace charter to stories, stories to requirements, and requirements to design.
- If unresolved decisions are smoothed over for readability, every downstream artifact repeats the guess and makes it harder to unwind later. Keep `TODO: Confirm` markers visible wherever evidence is missing.

## Deliverables

- one authored specification pack under `docs/specs/<project-name>/`
- aligned charter, user stories, requirements, and technical design artifacts
- deterministic provenance and source-artifact lineage on every authored artifact
- explicit `TODO: Confirm` markers for unresolved decisions
- a pack ready for approval or downstream coordination

## Validation Checklist

- one stable `<project-name>` is reused across the full pack
- charter, user stories, requirements, and technical design artifacts all exist
- every authored artifact records `generated_by.root_skill = specification-authoring`
- every authored artifact records the correct `source_artifacts` roles for its kind
- the user explicitly approved `docs/specs/<project-name>/charter.md` before `docs/specs/<project-name>/user-stories.md` was authored, unless the user explicitly waived stage-by-stage approval
- the user explicitly approved `docs/specs/<project-name>/user-stories.md` before `docs/specs/<project-name>/requirements.md` was authored, unless the user explicitly waived stage-by-stage approval
- the user explicitly approved `docs/specs/<project-name>/requirements.md` before `docs/specs/<project-name>/technical-design.md` was authored, unless the user explicitly waived stage-by-stage approval
- the user explicitly approved `docs/specs/<project-name>/technical-design.md` before the final cross-artifact consistency pass and final pack delivery, unless the user explicitly waived stage-by-stage approval
- charter scope, actors, and success criteria map to stories
- user-visible requirements map to stories and requirements map to design
- unresolved issues are marked explicitly instead of guessed
- major contradictions across the pack are resolved or surfaced for review
