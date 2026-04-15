---
name: user-story-authoring
description: "Produce user-stories artifacts from approved product framing. Use when a user needs user-visible behavior captured before detailed requirements, technical design, or execution planning."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: specification-authoring
  dependencies:
    - write-user-stories
    - visual-diagramming
---

## Purpose

Produce `user-stories.md` from approved product framing. Capture user-visible behavior, value, and observable outcomes in canonical story blocks without re-owning requirements, technical design, or execution planning.

## Boundaries

- Output filename: `user-stories.md`
- Source of truth: approved `./charter.md` and other approved framing; use repository evidence only when existing behavior or integrations materially change the story set
- Artifact contract: follow `../write-user-stories/SKILL.md`
- In scope:
  - identify real actors and user-visible capability areas
  - draft canonical stories with unique `US1.x` identifiers plus `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`
  - split oversized stories into buildable slices
  - add boundary and failure stories for visible errors, forbidden actions, review gates, safety boundaries, trust boundaries, and controllability limits when relevant
  - add persona or actor-flow diagrams only when they clarify stages, touchpoints, or branching paths
- Out of scope:
  - redefining approved goals, non-goals, personas, or success criteria
  - detailed functional requirements
  - technical design, engineering tasks, or code changes
  - workflow-wide `source_artifacts` lineage policy
- Ask only when ambiguity changes actors, situations, actions, outcomes, observations, scope, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- approved `./charter.md` or equivalent product framing
- desired outcomes and known users or stakeholders
- goals, non-goals, and scope boundaries when available
- repository evidence when existing behavior affects the story set

## Output

- `user-stories.md`
- one user-stories artifact downstream requirements, design, and planning can trust for user-visible behavior and stable story anchors

## Workflow

1. Load approved framing from `./charter.md` and available inputs; inspect repo evidence only where existing behavior or integrations materially change the story set.
2. Determine the system purpose in user-facing terms and identify or prioritize real actors before drafting stories.
3. Identify user-visible capability areas.
4. Draft `user-stories.md` with the shared contract; assign unique `US1.x` identifiers in artifact order and keep each story actor-first with `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`.
5. Split oversized or multi-behavior stories so each story maps cleanly to acceptance criteria and implementation slices.
6. Add boundary and failure stories for invalid inputs, visible errors, forbidden writes, review gates, provenance needs, controllability limits, and other visible trust boundaries when relevant; for AI-assisted systems include reviewability, provenance, controllability, and human-authored versus machine-generated boundaries when they affect users.
7. Use `../visual-diagramming/SKILL.md` only when persona journeys, actor touchpoints, or branching paths are clearer visually than prose.
8. Review against `../write-user-stories/references/story-quality-checklist.md` and `../write-user-stories/references/anti-patterns.md`.
9. Validate with `bash ../write-user-stories/scripts/validate_user_stories.sh <resolved-user-stories-path>`; use `bash ../write-user-stories/scripts/validate_story.sh <story-file-or-stdin>` for single-story debugging when needed.
10. Deliver for approval before downstream requirements, design, or planning.

## Validation

- Run: `bash ../write-user-stories/scripts/validate_user_stories.sh <resolved-user-stories-path>`
- Confirm stories are grouped by capability area and every final story has a unique `US1.x` identifier plus the canonical five fields.
- Confirm stories are actor-first, behavior-focused, value-bearing, and externally observable.
- Confirm oversized stories are split and relevant boundary or failure coverage is present.
- Confirm requirements, architecture, and task detail are not mixed into the artifact.
- Confirm optional diagrams add context without replacing canonical story blocks.

## Approval-view focus

- capability areas and primary actors
- highest-value story anchors and observable outcomes
- boundary and failure coverage that protects downstream requirements quality
- story gaps or `TODO: Confirm` items that would distort later requirements if left vague
