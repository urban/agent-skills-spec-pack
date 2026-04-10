---
name: user-story-authoring
description: "Produce user-stories artifacts from approved product framing and relevant repository context. Use when a user needs user-visible behavior captured before detailed requirements, technical design, or execution planning."
license: MIT
metadata:
  version: "0.3.0"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: specification-authoring
  dependencies:
    - write-user-stories
    - visual-diagramming
---

## Rules

- Keep this role focused on user-visible behavior and value because requirements, design, and implementation planning belong downstream.
- Produce the artifact as `user-stories.md`.
- Start from actors, not features.
- Use the `write-user-stories` contract for the canonical artifact structure, story fields, story identifiers, quality checks, anti-pattern review, and validation.
- Use approved charter context from `./charter.md` when it exists because goals, actors, boundaries, and success framing should shape the story set.
- Ask for clarification when missing detail materially changes actors, situations, actions, outcomes, observations, or scope; otherwise continue and mark uncertainty as `TODO: Confirm`.
- Inspect repository context only when existing behavior, integrations, or constraints materially shape the authored stories.
- Use `visual-diagramming` only when persona journeys, actor touchpoints, or branching paths are clearer in a diagram than in prose.
- When journey or actor-flow wording, syntax safety, or readability is unclear, load the relevant `visual-diagramming` guidance instead of inventing one-off diagram conventions.
- Do not turn functional requirements, technical constraints, engineering tasks, or architecture decisions into user stories.

## Constraints

- Output must be one Markdown artifact named `user-stories.md`.
- Every final story must stay compatible with the `write-user-stories` contract.
- Group stories by capability area.
- Every final story must include a unique `US1.x` story identifier plus `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`.
- Include happy-path stories and relevant boundary or failure stories.
- Keep stories small enough to map cleanly to acceptance criteria and implementation slices.
- Do not restate charter scope framing, detailed requirements, architecture, or task breakdowns inside the stories artifact.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Requirements

Inputs:

- approved charter or equivalent product framing
- desired outcomes and known users or stakeholders
- goals, non-goals, and scope boundaries when available
- repository evidence when existing behavior affects the story set

Output:

- one complete user-stories artifact named `user-stories.md`

In scope:

- determining system purpose from approved framing
- identifying and prioritizing primary, secondary, operational, and system actors when useful
- identifying user-visible capability areas
- drafting canonical stories with unique `US1.x` identifiers plus `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`
- splitting oversized stories into buildable slices
- adding boundary and failure stories for visible errors, forbidden actions, review boundaries, safety boundaries, and controllability boundaries
- grouping stories by capability area
- adding persona or actor diagrams when they clarify stages, touchpoints, or branching paths
- preserving explicit uncertainty markers where story details remain unresolved

Out of scope:

- redefining goals, non-goals, personas, or success criteria already owned by the charter
- detailed functional requirements
- technical design
- engineering tasks
- code changes

## Workflow

1. Confirm the user needs user-stories artifacts from approved product framing before detailed requirements, technical design, or execution planning.
2. Gather approved framing from available inputs and `./charter.md` when present.
3. Determine the system purpose in user-facing terms.
4. Identify and prioritize real actors before drafting any stories.
5. Identify user-visible capability areas.
6. Inspect the repository only when existing behavior or integrations materially change the authored story set.
7. Draft stories in `user-stories.md` using the `write-user-stories` template and five-field schema.
8. Assign unique `US1.x` story identifiers in artifact order so downstream requirements can reference canonical story blocks directly.
9. Split oversized or multi-behavior stories.
10. Add boundary and failure stories for invalid inputs, visible errors, forbidden writes, review gates, provenance needs, controllability limits, and other visible trust boundaries when relevant.
11. For AI-assisted systems, keep human agency primary when possible and include stories for reviewability, provenance, controllability, and human-authored versus machine-generated boundaries.
12. Use `visual-diagramming` only when a journey or actor-flow diagram clarifies the capability set.
13. Load the relevant `visual-diagramming` guidance when journey structure, branching flow, or Mermaid syntax safety is unclear.
14. Review the draft against `../write-user-stories/references/story-quality-checklist.md` and `../write-user-stories/references/anti-patterns.md`.
15. Validate with `bash ../write-user-stories/scripts/validate_user_stories.sh <resolved-user-stories-path>` and use `bash ../write-user-stories/scripts/validate_story.sh <story-file>` for story-level debugging when needed.
16. Deliver the draft and request approval before downstream requirements, design, or planning proceeds.

## Gotchas

- If stories begin from feature buckets instead of actors, they look organized but still miss why anyone cares. Start from actors and situations.
- If the system becomes the default actor, human value and control boundaries disappear. Use system actors only when they are genuinely the right frame.
- If a story omits `Observation`, the behavior cannot be verified cleanly. Make success or failure externally visible.
- If story IDs are missing, duplicated, or unstable, requirements fall back to fragile title matching. Keep one unique `US1.x` identifier on every final story.
- If one story contains multiple actions or outcomes, downstream work inherits an epic disguised as a story. Split it.
- If implementation details dominate, the artifact stops being user-story authoring and starts leaking requirements or design. Rewrite in user-visible language.
- If only happy paths are captured, safety, trust, and failure behavior stay implicit until too late. Add explicit boundary and failure stories.
- If grouping headings replace canonical story blocks, the artifact becomes readable but contract-incompatible. Keep headings as wrappers only.
- If AI-assisted stories imply vague autonomy, they hide authorship and review boundaries. Prefer controllable assistance and explicit human checkpoints.

## Deliverables

- `user-stories.md`
- canonical user stories grouped by capability area
- unique `US1.x` story identifiers for downstream traceability
- happy-path and boundary/failure stories where relevant
- explicit `TODO: Confirm` markers for unresolved story details
- optional persona or actor diagrams that add context without replacing canonical story blocks
- a draft ready for review before downstream artifact work

## Validation Checklist

- artifact filename is `user-stories.md`
- stories are grouped by capability area
- every final story has a unique `US1.x` story identifier
- every final story uses the canonical five-field contract
- stories are actor-first, behavior-focused, and value-bearing
- stories include observable results
- oversized stories are split into buildable slices
- relevant boundary and failure stories are included
- implementation strategy is not mixed into the artifact
- the artifact passes the shared user-stories validator

## Deterministic Validation

- `bash ../write-user-stories/scripts/validate_user_stories.sh <resolved-user-stories-path>`
