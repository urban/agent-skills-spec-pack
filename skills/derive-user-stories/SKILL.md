---
name: derive-user-stories
description: Reconstruct user-stories artifacts from repository evidence. Use when a user needs implemented user-visible behavior and capability areas inferred from an existing system.
metadata:
  version: 0.3.0
  layer: specialist
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - write-user-stories
---

## Rules

- Treat repository code as the primary evidence and use tests to strengthen confidence because this role reconstructs implemented outcomes, not roadmap intent.
- Produce the artifact as `user-stories.md`.
- Use the shared `write-user-stories` contract for canonical story structure, story identifiers, capability grouping, quality checks, and validation.
- Focus on user-visible behavior because technical plumbing without stakeholder-visible value belongs in coverage gaps, not in stories.
- Keep evidence traceable to concrete file paths and line references because confidence must be reviewable.
- Use context from `./charter.md` when it exists because reconstructed goals, actors, and success framing can sharpen the story set.
- Use `TODO: Confirm` for unsupported actor, situation, action, outcome, or observation details instead of guessing.
- Assign confidence from evidence strength, not from how plausible the narrative sounds.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `user-stories.md`.
- Always draft from `./assets/report-template.md`.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not use PR descriptions, commit history, issue trackers, or external docs as primary evidence.
- Do not omit ambiguous stories when they still reflect likely user-visible behavior; include them with lower confidence and explicit uncertainty.

## Requirements

Inputs:

- repository source code
- repository tests when present
- optional user-provided scope paths or modules
- optional user-provided output destination

Output:

- one derived user-stories artifact named `user-stories.md`

Required report sections, in order:

1. `Executive Summary`
2. `Stakeholder-Ready Product Narratives`
3. `Capability Map`
4. `Coverage Gaps`
5. `Additional Notes`

Per-story requirements:

- one canonical story block compatible with `write-user-stories`
- one unique `US1.x` story identifier per story
- confidence label: `High`, `Medium`, or `Low`
- confidence rationale
- at least one code evidence reference
- test evidence or explicit `No direct test evidence`
- `TODO: Confirm` for unresolved story details

In scope:

- inferring implemented user-visible outcomes
- grouping stories into evidence-based capability areas
- documenting coverage gaps for code areas without clear user-facing mapping
- backing up an existing report before overwrite

Out of scope:

- technical-only stories with no user-visible outcome
- speculative product history
- multi-file output

## Workflow

1. Confirm the user needs user-stories artifacts reconstructed from repository evidence, then define analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inventory user-facing surfaces such as UI routes, API endpoints, CLI commands, workflows, and integrations.
3. Trace those surfaces into handlers, services, and domain logic and collect `path:line` evidence.
4. Use tests to strengthen or weaken confidence about each inferred outcome.
5. Identify evidence-based actors and capability areas.
6. Draft the report from `./assets/report-template.md`, then replace placeholders with actual content.
7. Write one canonical story block per user-visible outcome using `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`.
8. Assign unique `US1.x` story identifiers in artifact order so downstream requirements can trace back to canonical reconstructed stories.
9. Add confidence, rationale, code evidence, and test evidence for each story.
10. Record non-mapped code areas in `Coverage Gaps` and unresolved ambiguity in `Additional Notes`.
11. Write `user-stories.md` to the chosen destination.
12. If the destination artifact already exists, create a timestamped backup in the same directory before overwrite.
13. Validate with `bash ./scripts/validate_report.sh <resolved-user-stories-path>`.
14. Deliver the artifact as reconstructed implemented user outcomes, not speculative product strategy.

## Gotchas

- If actor or outcome fields are guessed from naming alone, the report sounds polished but overstates what the code proves. Keep uncertainty explicit.
- If technical capabilities that users never experience are forced into stories, the capability map fills with implementation trivia. Put those areas in `Coverage Gaps` instead.
- If confidence is assigned by narrative coherence instead of evidence depth, weak stories get treated as facts downstream. Base confidence on code and test support only.
- If ambiguous stories are dropped entirely, the report falsely suggests complete understanding of the product surface. Include plausible user-visible outcomes with lower confidence and clear uncertainty.
- If story IDs are missing, duplicated, or unstable, downstream requirements lose a reliable traceability anchor. Keep one unique `US1.x` identifier on every reconstructed story.
- If story blocks drift away from the shared five-field contract, reconstruction and authoring stop being reversible. Keep the shared structure intact.
- If an existing report is overwritten without backup, previous interpretations disappear and review loses context. Create the timestamped backup first.

## Deliverables

- `user-stories.md`
- a timestamped backup when overwriting an existing artifact
- stakeholder narratives, capability map, coverage gaps, and additional notes
- user story blocks with unique `US1.x` identifiers, confidence, rationale, evidence references, and canonical frontmatter
- validation passing via `./scripts/validate_report.sh`

## Validation Checklist

- artifact filename is `user-stories.md`
- existing artifact backup is created before overwrite when needed
- all five required sections exist in order
- every story has a unique `US1.x` story identifier
- every story follows the canonical five-field contract
- every story includes confidence, rationale, and evidence references
- unresolved story details are marked `TODO: Confirm`
- no template placeholders remain

## Deterministic Validation

- `bash ./scripts/validate_report.sh <resolved-user-stories-path>`
