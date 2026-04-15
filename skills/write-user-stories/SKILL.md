---
name: write-user-stories
description: "Define and validate canonical user-stories artifacts. Use when a workflow creates, derives, reviews, or validates user-visible behavior documentation that must stay compatible across workflows."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared user-stories artifact contract: canonical story shape, `US1.x` identifiers, capability-area grouping, template shape, and deterministic validation. Keep authored and derived user-stories artifacts compatible without owning workflow-wide lineage policy.

## Contract

- Artifact shape:
  - one Markdown artifact
  - canonical frontmatter when the workflow stamps provenance
  - `# User Stories`
  - at least one `## Capability Area: <name>` section
  - at least one `### Story: <short title>` block
  - every canonical story appears inside a capability area
- Story contract:
  - each story has one unique `US1.x` identifier
  - required fields, in list form:
    - `- Story ID:`
    - `- Actor:`
    - `- Situation:`
    - `- Action:`
    - `- Outcome:`
    - `- Observation:`
  - the contract does not require `As a / I want / so that`
  - optional fields may add context but must not replace the five required fields
  - workflow-specific evidence or confidence fields are allowed when a specialist contract requires them
- Scope boundary:
  - keep stories user-visible, value-bearing, and behavior-focused
  - keep one meaningful behavior per story
  - treat visible boundary and failure behavior as first-class story material when relevant
  - do not encode architecture, services, libraries, storage choices, adapters, or internal implementation patterns unless they are directly user-visible
  - this skill does not own workflow-wide `source_artifacts` policy
- Quality rules:
  - group stories under capability areas for stable downstream clustering
  - make success externally observable
  - use `TODO: Confirm` instead of guessing unsupported actors, triggers, outcomes, or observations

## Inputs

- project concept, charter, PRD, design notes, codebase analysis, or other source material that describes user-visible behavior
- known actors, situations, constraints, and value signals when available

## Outputs

- one canonical user-stories Markdown artifact compatible across authoring, derivation, review, and downstream requirements or planning
- the shared templates at `./assets/user-stories-template.md` and `./assets/story-template.md`
- deterministic validation via `./scripts/validate_user_stories.sh` and `./scripts/validate_story.sh`

## Workflow

1. Start from `./assets/user-stories-template.md` when a full scaffold helps and `./assets/story-template.md` for individual stories.
2. Identify real actors before drafting stories.
3. Identify user-visible capability areas.
4. Draft one meaningful behavior per story with `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`.
5. Assign deterministic `US1.x` identifiers in artifact order.
6. Split bundled stories with `./references/split-or-keep.md` when one story contains multiple behaviors or outcomes.
7. Add visible boundary and failure stories when they are reviewable, controllable, operator-visible, or safety-relevant.
8. Review against `./references/story-quality-checklist.md` and `./references/anti-patterns.md`.
9. Validate with `bash ./scripts/validate_user_stories.sh <user-stories-file>` and use `bash ./scripts/validate_story.sh <story-file-or-stdin>` for single-story debugging.

## Validation

- Run: `bash ./scripts/validate_user_stories.sh <user-stories-file>`
- Run: `bash ./scripts/validate_story.sh <story-file-or-stdin>`
- Confirm every story has a unique `US1.x` identifier and all five required fields.
- Confirm stories stay actor-first, behavior-focused, externally observable, and small enough to map to acceptance criteria and implementation slices.
- Confirm optional fields do not replace required fields and canonical frontmatter is valid when the workflow stamps provenance.

## References

- [`./references/split-or-keep.md`](./references/split-or-keep.md): Read when: deciding whether one story should be split into smaller slices.
- [`./references/story-quality-checklist.md`](./references/story-quality-checklist.md): Read when: reviewing whether stories are actor-first, value-bearing, and observable.
- [`./references/anti-patterns.md`](./references/anti-patterns.md): Read when: a story drifts into implementation detail, generic boilerplate, or bundled behavior.
