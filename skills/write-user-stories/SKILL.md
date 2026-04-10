---
name: write-user-stories
description: "Write and validate canonical user-stories artifacts. Use when a task creates, derives, reviews, or validates user-visible behavior documentation that must stay compatible across workflows."
license: MIT
metadata:
  version: "0.3.0"
  author: "urban (https://github.com)"
  layer: foundational
---

## Rules

- Use the shared five-field story schema for every canonical story:
  - `Actor`
  - `Situation`
  - `Action`
  - `Outcome`
  - `Observation`
- Group stories under capability areas because downstream requirements and planning work need stable behavioral clustering.
- Use deterministic story identifiers because downstream requirements, design, planning, and review need stable references back to canonical story blocks.
- Keep each story focused on one meaningful user-visible behavior because oversized stories hide scope and break acceptance slicing.
- Make success externally observable because invisible success claims are weak inputs for review, testing, and requirements.
- Prefer user-visible behavior and value over implementation detail.
- Keep uncertainty explicit with `TODO: Confirm` rather than guessing unsupported actors, triggers, outcomes, or observations.
- Treat boundary and failure behavior as first-class story material when it is user-visible, operator-visible, review-visible, or safety-relevant.
- Preserve canonical frontmatter shape and validate created artifacts with the shared provenance validator when the workflow stamps provenance.

## Constraints

- Output must be one Markdown artifact.
- The shared user-stories contract does not define workflow-wide `source_artifacts` policy.
- Story identifiers must use the shared prefix `US1.x`.
- The contract does not require a single sentence form such as `As a / I want / so that`.
- Every canonical story must appear inside a capability area and include a unique story identifier plus all five required fields.
- Optional fields may add context, but must not replace the five required fields.
- Do not encode architecture, services, libraries, storage choices, adapters, or internal implementation patterns unless they are directly user-visible.

## Requirements

A valid canonical user-stories artifact must include:

- canonical frontmatter shape when provenance is stamped for the workflow
- `# User Stories`
- at least one `## Capability Area: <name>` section
- at least one `### Story: <short title>` block per artifact
- for each story, these required fields in list form:
  - `- Story ID:` using `US1.x`
  - `- Actor:`
  - `- Situation:`
  - `- Action:`
  - `- Outcome:`
  - `- Observation:`
- unresolved details expressed as `TODO: Confirm` inline when needed

Allowed optional additions:

- `- Rationale:`
- `- Priority:`
- `- Related constraints:`
- `- Traceability links:`
- workflow-specific evidence or confidence fields when a specialist contract requires them

Inputs:

- project concept, charter, PRD, design notes, codebase analysis, or other source material that describes user-visible behavior
- known actors, situations, constraints, and value signals when available

Output:

- one or more canonical user stories grouped by capability area and ready for downstream requirements, design, and planning work

## Workflow

1. Draft from [`assets/user-stories-template.md`](./assets/user-stories-template.md) when a full artifact scaffold helps.
2. Identify real actors before drafting stories.
3. Identify user-visible capability areas.
4. Draft each story with [`assets/story-template.md`](./assets/story-template.md).
5. Assign deterministic `US1.x` story identifiers in artifact order and keep them attached to the canonical story blocks.
6. Keep one meaningful behavior per story and split bundled stories with [`references/split-or-keep.md`](./references/split-or-keep.md).
7. Ensure every story states why the behavior matters through `Outcome` and how success is verified through `Observation`.
8. Add boundary and failure stories when they are visible, reviewable, controllable, or safety-relevant.
9. Review the artifact against [`references/story-quality-checklist.md`](./references/story-quality-checklist.md) and [`references/anti-patterns.md`](./references/anti-patterns.md).
10. Validate the artifact with [`scripts/validate_user_stories.sh`](./scripts/validate_user_stories.sh) and use [`scripts/validate_story.sh`](./scripts/validate_story.sh) for single-story debugging.

## Gotchas

- If the story starts from a feature label instead of a real actor, the output drifts toward backlog taxonomy instead of behavior. Name the actor first.
- If `Situation` is missing, the trigger stays implicit and the story becomes hard to test or scope. State the trigger or context clearly.
- If story IDs are missing, duplicated, or ad hoc, downstream requirements and plans fall back to fragile title matching. Keep one unique `US1.x` identifier on every canonical story.
- If `Observation` is vague, the story may sound valuable while still hiding how anyone would verify success. Name a visible sign.
- If one story contains multiple actions or outcomes, it reads like an epic and downstream work cannot slice it cleanly. Split it.
- If implementation details dominate the story, requirements and design inherit architecture decisions too early. Rewrite in user-visible terms.
- If happy-path stories exist without boundary or failure coverage, important constraints stay unstated until too late. Add visible edge behavior.
- If capability areas are missing, related stories become harder to navigate, trace, and refine. Keep grouping explicit.
- If workflow lineage rules are embedded here, the foundational contract stops being reusable across authoring and reconstruction. Leave workflow-specific `source_artifacts` policy to coordination.

## Deliverables

- Canonical user-stories artifact structure shared across workflows.
- Deterministic story identifiers for downstream traceability.
- Canonical story template and artifact template.
- Reusable story quality checklist, anti-pattern guidance, and split guidance.
- Deterministic validation for one story or one artifact.

## Validation Checklist

- Artifact has `# User Stories`.
- Artifact has at least one `## Capability Area:` section.
- Every story block has a `### Story:` title.
- Every story has a unique `US1.x` Story ID.
- Every story contains `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`.
- Optional fields do not replace required fields.
- Story IDs are concrete, and the other required fields are concrete or explicitly marked `TODO: Confirm`.
- Stories stay behavior-focused and user-visible.
- Stories are small enough to map to acceptance criteria and implementation slices.

## Deterministic Validation

- `bash scripts/validate_user_stories.sh <user-stories-file>`
- `bash scripts/validate_story.sh <story-file-or-stdin>`
