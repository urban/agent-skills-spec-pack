---
name: user-story-authoring
description: Produce user-story artifacts from approved product framing and repository context. Use when a user wants canonical user stories authored before detailed requirements, design, or execution planning.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: planning
  domain: specification-authoring
  dependencies:
    - artifact-naming
    - document-traceability
    - visual-diagramming
    - write-user-stories
---

## Rules

- Keep this role focused on user-visible outcomes because requirements, design, and planning belong downstream.
- Use `artifact-naming` to resolve and preserve `<project-name>` because the rest of the spec pack depends on stable paths.
- Use `document-traceability` to stamp canonical provenance and `source_artifacts.charter` because this artifact depends on the approved charter.
- Use the `write-user-stories` contract for artifact frontmatter, sentence shape, and uncertainty handling because downstream skills rely on canonical stories.
- Use approved charter context when it exists because goals, actors, and success criteria should shape the story set.
- Use `visual-diagramming` when persona journeys, actor touchpoints, or branching user paths will communicate story context faster than prose alone.
- Ask for clarification when missing detail changes actor, action, benefit, or scope; otherwise continue and mark `TODO: Confirm`.
- Inspect repository context only when existing behavior or integrations materially shape the stories.

## Constraints

- Output must be one Markdown artifact at `docs/specs/<project-name>/user-stories.md`.
- Every final story must stay compatible with the `write-user-stories` contract.
- The artifact must record `source_artifacts.charter = docs/specs/<project-name>/charter.md`.
- Keep grouping concise and readable, but do not replace story sentences with summaries.
- When diagrams are used, keep the stories canonical and use the diagram to add actor context rather than replace the story contract.
- Do not mix charter-level scope framing, detailed requirements, architecture, task breakdowns, or implementation notes into the artifact.

## Requirements

Inputs:

- approved charter or equivalent product framing
- desired outcomes and known users or stakeholders
- goals, non-goals, and scope boundaries when available
- repository evidence when existing behavior affects the story set

Output:

- one complete user-story artifact at `docs/specs/<project-name>/user-stories.md`

In scope:

- identifying user-visible outcomes
- writing canonical actor-action-benefit stories
- grouping related stories under concise headings when useful
- adding persona or actor diagrams when they clarify stages, touchpoints, or branching paths
- stamping deterministic authored-document provenance and source-artifact lineage
- preserving explicit uncertainty markers where story fields are unresolved

Out of scope:

- redefining goals, non-goals, personas, or success criteria already owned by the charter
- detailed technical requirements
- technical design
- implementation planning or code changes

## Workflow

1. Confirm the user wants user stories authored after product framing and before detailed requirements, design, or implementation work.
2. Resolve `<project-name>` with `artifact-naming` and keep it stable for the run.
3. Capture `root_skill` from the active authored workflow and set `producing_skill = user-story-authoring`.
4. Gather the approved charter context, outcomes, actors, goals, non-goals, and scope boundaries.
5. Inspect the repository only when existing behavior, integrations, or constraints materially shape user-visible outcomes.
6. Identify distinct user-visible outcomes and split bundled requests into separate stories when needed.
7. Use `visual-diagramming` to decide whether a journey or flowchart would clarify personas, actor touchpoints, or branching user paths.
8. Draft `docs/specs/<project-name>/user-stories.md` using the `write-user-stories` contract.
9. Stamp canonical provenance with `source_artifacts.charter`.
10. Mark unresolved actor, action, or benefit fields as `TODO: Confirm` instead of guessing.
11. Validate the artifact with `bash ../write-user-stories/scripts/validate_user_stories.sh docs/specs/<project-name>/user-stories.md` and use `bash ../write-user-stories/scripts/validate_story.sh '<story>'` for sentence-level debugging when needed.
12. Deliver the draft and request approval before requirements, design, or planning proceeds.

## Gotchas

- If stories describe technical tasks, later requirements inherit engineering chores instead of user value. Rewrite them around what a user or stakeholder experiences.
- If one story bundles multiple outcomes, downstream planning cannot tell what should be sliced first. Split independent user-visible outcomes into separate stories.
- If you guess the actor or benefit to make the sentence read smoothly, the whole spec pack gets built on invented intent. Use `TODO: Confirm` inline when a story field is uncertain.
- If grouping headings replace the canonical story sentences, the artifact reads fine to humans but breaks contract compatibility for downstream skills. Treat headings as wrappers, not substitutes.
- If you add a persona diagram and then repeat its stages in prose, the artifact grows without adding insight. Use supporting text for constraints, exceptions, or unresolved questions only.
- If repository behavior already constrains the story set and you ignore it, the stories overpromise against the actual product surface. Inspect the code when current behavior materially matters.
- If the benefit clause is vague filler, the story passes syntax checks while still hiding the real value. State the concrete benefit or mark it `TODO: Confirm`.
- If stories restate goals, non-goals, or success criteria as prose instead of turning them into user-visible outcomes, they duplicate the charter artifact and blur pack boundaries. Keep stories on outcomes.
- If `source_artifacts.charter` is missing, downstream requirements cannot prove which approved framing shaped the stories. Keep the lineage explicit.

## Deliverables

- `docs/specs/<project-name>/user-stories.md`
- canonical user stories aligned to the shared actor-action-benefit contract
- explicit `TODO: Confirm` markers for unresolved story fields
- deterministic provenance plus `source_artifacts.charter`
- optional persona or actor diagrams that add context without replacing canonical story sentences
- a draft ready for user review before downstream artifact work

## Validation Checklist

- artifact path is `docs/specs/<project-name>/user-stories.md`
- every final story uses the canonical actor-action-benefit contract
- `source_artifacts.charter` points to the approved charter
- unresolved story fields are marked `TODO: Confirm`
- implementation strategy is not mixed into the artifact
- the artifact passes the shared user-stories validator

## Deterministic Validation

- `bash ../write-user-stories/scripts/validate_user_stories.sh docs/specs/<project-name>/user-stories.md`
