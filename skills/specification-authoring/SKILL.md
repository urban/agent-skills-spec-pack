---
name: specification-authoring
description: "Orchestrate authored specification work for a new product or major feature. Use when a user needs a coordinated charter, user-stories, requirements, and technical-design pack created from approved product framing."
license: MIT
metadata:
  version: "0.2.0"
  author: "urban (https://github.com)"
  layer: coordination
  dependencies:
    - document-traceability
    - artifact-naming
    - charter
    - user-story-authoring
    - requirements
    - technical-design
---

## Rules

- Keep this workflow at the coordination layer because specialist skills own artifact-specific contracts and validation.
- Use `artifact-naming` to resolve one stable `<project-name>` for the workflow because the authored spec-pack root must stay consistent across all artifacts.
- Resolve one stable authored spec-pack root early and preserve it across every authored artifact because placement drift breaks downstream alignment.
- Use `.specs/<project-name>/` as the default authored spec-pack root unless the user provides an explicit destination.
- Establish `generated_by.root_skill` as `specification-authoring` for every artifact emitted from this workflow.
- Run specialist entry skills in order because charter sets scope and success, stories define user-visible outcomes, requirements define product obligations, and design explains the solution.
- Do not start `user-story-authoring` until the user explicitly approves `charter.md`.
- Do not start `requirements` until the user explicitly approves `user-stories.md`.
- Do not start `technical-design` until the user explicitly approves `requirements.md`.
- Do not start the final cross-artifact consistency pass or final pack delivery until the user explicitly approves `technical-design.md`.
- Keep cross-artifact review explicit because workflow value comes from alignment, not from merely invoking four skills.
- If missing detail changes scope or artifact shape, ask or mark `TODO: Confirm` instead of letting downstream artifacts invent certainty.

## Constraints

- This workflow coordinates artifacts; it does not replace underlying specialist or foundational contracts.
- Final output must include `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` in one authored spec pack.
- Coordination must use specialist skills for artifact-producing work and may use `artifact-naming` only for workflow-wide naming and placement coordination.
- Every authored artifact must carry deterministic provenance rooted in this workflow plus the canonical `source_artifacts` lineage required by this workflow.
- Never author the full specification pack in one uninterrupted pass unless the user explicitly waives stage-by-stage approval.
- Do not start downstream coordination or implementation from this workflow unless the user explicitly asks for that next phase.

## Source Artifact Lineage

This workflow owns the canonical `source_artifacts` lineage map for authored artifacts.

Use exactly these `source_artifacts` artifact-type keys in this workflow:

- `charter.md` -> `source_artifacts: {}`
- `user-stories.md` -> `charter`
- `requirements.md` -> `charter`, `user_stories`
- `technical-design.md` -> `charter`, `user_stories`, `requirements`

Resolved authored paths should normally be:

- `charter` -> `<spec-pack-root>/charter.md`
- `user_stories` -> `<spec-pack-root>/user-stories.md`
- `requirements` -> `<spec-pack-root>/requirements.md`

For authored user stories specifically:

- `user-story-authoring` produces `user-stories.md`
- the shared `write-user-stories` contract defines the story structure
- this workflow defines that authored `user-stories.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md`

Do not add extra source artifact-types casually.

## Requirements

Inputs:

- product idea, feature request, or approved problem statement
- desired outcomes, goals, and scope boundaries
- repository context when existing code, integrations, or constraints matter
- optional explicit authored destination root
- optional explicit artifact slug or preferred basename
- clarification on unknowns that would materially change the artifact set

Outputs:

- `.specs/<project-name>/charter.md`
- `.specs/<project-name>/user-stories.md`
- `.specs/<project-name>/requirements.md`
- `.specs/<project-name>/technical-design.md`
- one authored spec pack rooted at the chosen authored spec-pack root

In scope:

- resolving one workflow-wide `<project-name>` with `artifact-naming`
- selecting and preserving one authored spec-pack root for the workflow
- orchestrating specialist entry skills in authored order
- preserving pack-wide placement and scope consistency
- establishing root workflow provenance and canonical `source_artifacts` lineage for every authored artifact
- checking that artifacts map cleanly from charter through design

Out of scope:

- redefining specialist-level artifact contracts in this workflow
- producing execution artifacts
- doing implementation work
- hiding unresolved scope or intent behind polished prose

## Workflow

1. Confirm the user needs authored specification work for a new product or major feature before downstream coordination or implementation.
2. Resolve `<project-name>` once with `artifact-naming`, honoring an explicit artifact slug or preferred basename when provided.
3. Resolve the authored spec-pack root once for the full run, defaulting to `.specs/<project-name>/` unless the user provides an explicit destination.
4. Establish `root_skill = specification-authoring` for all authored artifacts in this run.
5. Co-create or confirm the core outcomes, goals, non-goals, personas / actors, success criteria, and scope boundaries.
6. Run `charter`, write the result to `<spec-pack-root>/charter.md`, present it to the user, and wait for explicit approval before continuing.
7. If the user does not approve the charter, revise it or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
8. Run `user-story-authoring`, write the result to `<spec-pack-root>/user-stories.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md`, present it to the user, and wait for explicit approval before continuing.
9. If the user does not approve the story set, revise stories or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
10. Run `requirements`, write the result to `<spec-pack-root>/requirements.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md` and `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, present it to the user, and wait for explicit approval before continuing.
11. If the user does not approve the requirements, revise requirements or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
12. Run `technical-design`, write the result to `<spec-pack-root>/technical-design.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md`, `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, and `source_artifacts.requirements = <spec-pack-root>/requirements.md`, present it to the user, and wait for explicit approval before continuing.
13. If the user does not approve the technical design, revise design or mark unresolved points as `TODO: Confirm`, then present the updated artifact again and wait for explicit approval.
14. Perform a cross-artifact consistency pass:

- `charter.md` scope, actors, and success criteria support the story set
- `user-stories.md` stays within approved charter scope and uses the shared five-field story contract
- user-visible requirements map to approved stories
- `requirements.md` does not re-own goals, non-goals, personas, or success criteria from `charter.md`
- `requirements.md` maps to `technical-design.md`
- every artifact carries canonical provenance and the `source_artifacts` artifact-type keys required by this workflow
- unresolved items stay explicit as `TODO: Confirm`

15. Deliver the authored specification pack for approval or downstream coordination.

## Approval Contract

- Approval must be explicit user confirmation in the conversation.
- Silence, implied satisfaction, a request for a full specification pack, or lack of objections does not count as approval.
- A request to continue only counts as approval for the artifact currently under review unless the user explicitly waives stage-by-stage approval.
- If approval is ambiguous, ask for confirmation before continuing.

## Gotchas

- If the workflow does not preserve one authored spec-pack root, the pack looks complete but downstream links and review context split across multiple directories. Resolve placement once before any artifact is written.
- If `<project-name>` is re-derived mid-workflow, the pack can fork into multiple roots even when the artifact content is consistent. Resolve naming once and preserve it for the full run.
- If user stories start before the charter is stable, actors and success checks drift and later requirements look aligned only because they copied the drift forward. Fix the charter first, then author stories from it.
- If requirements start before the stories are stable, product obligations get formalized around behavior the user has not approved yet. Fix story coverage first, then derive requirements from it.
- If you produce `user-stories.md` before `charter.md` is explicitly approved, produce `requirements.md` before `user-stories.md` is explicitly approved, or produce `technical-design.md` before `requirements.md` is explicitly approved, you have violated the workflow even if the documents are high quality. Stop, return to the last approved artifact, and re-enter the gated review flow.
- If requirements restate goals, non-goals, personas, or success criteria that the charter already owns, the pack grows redundant and future edits drift across files. Keep each artifact on its side of the boundary.
- If technical design is allowed to solve imagined future needs, architecture quietly becomes the place where scope expands. Push speculative work back to requirements or mark it `TODO: Confirm`.
- If provenance is missing or the wrong source-artifact types are stamped, later feedback cannot tell which authored branch drifted. Validate metadata before treating the pack as approved.
- If you treat the workflow as a thin router and skip the consistency pass, contradictions survive in polished artifacts until implementation exposes them. Explicitly trace charter to stories, stories to requirements, and requirements to design.
- If unresolved decisions are smoothed over for readability, every downstream artifact repeats the guess and makes it harder to unwind later. Keep `TODO: Confirm` markers visible wherever evidence is missing.

## Deliverables

- one authored specification pack under the chosen authored spec-pack root
- aligned `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md`
- deterministic provenance and source-artifact lineage on every authored artifact
- explicit `TODO: Confirm` markers for unresolved decisions
- a pack ready for approval or downstream coordination

## Validation Checklist

- one stable `<project-name>` is used to resolve the authored spec-pack root
- one stable authored spec-pack root is reused across the full pack
- `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` all exist in the chosen authored spec-pack root
- every authored artifact records `generated_by.root_skill = specification-authoring`
- `user-stories.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md`
- `requirements.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md` and `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`
- `technical-design.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md`, `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, and `source_artifacts.requirements = <spec-pack-root>/requirements.md`
- the user explicitly approved `charter.md` before `user-stories.md` was authored, unless the user explicitly waived stage-by-stage approval
- the user explicitly approved `user-stories.md` before `requirements.md` was authored, unless the user explicitly waived stage-by-stage approval
- the user explicitly approved `requirements.md` before `technical-design.md` was authored, unless the user explicitly waived stage-by-stage approval
- the user explicitly approved `technical-design.md` before the final cross-artifact consistency pass and final pack delivery, unless the user explicitly waived stage-by-stage approval
- charter scope, actors, and success criteria map to stories
- user-visible requirements map to stories and requirements map to design
- unresolved issues are marked explicitly instead of guessed
- major contradictions across the pack are resolved or surfaced for review
