---
name: derive-user-stories
description: Reconstruct evidence-based user stories, epic groupings, and stakeholder narratives from an existing codebase. Use when a user wants implemented user-facing outcomes inferred from repository code and tests.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - write-user-stories
---

## Rules

- Treat repository code as the primary evidence and use tests to strengthen confidence because this role reconstructs implemented outcomes, not roadmap intent.
- Focus on user-visible behavior because technical plumbing without user value belongs in coverage gaps, not in stories.
- Use the canonical user-story sentence contract for every derived story because the output must stay compatible with downstream story consumers.
- Keep evidence traceable to concrete file paths and line references because confidence must be reviewable.
- Use `TODO: Confirm` for unsupported actor, action, or benefit fields instead of guessing.
- Assign story confidence from evidence strength, not from how plausible the narrative sounds.

## Constraints

- Output must be one Markdown report at the user-specified destination or, by default, `docs/research/<project-name>/user-stories.md`.
- Always draft from `./assets/report-template.md`.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not use PR descriptions, commit history, issue trackers, or external docs as primary evidence.
- Do not omit ambiguous stories when they still reflect likely user-visible behavior; include them with lower confidence and `TODO: Confirm` markers.

## Requirements

Inputs:

- repository source code
- repository tests when present
- optional user-provided scope paths or modules
- optional user-provided output destination

Output:

- one derived user-stories report at the user-specified destination or, when no destination is provided, `docs/research/<project-name>/user-stories.md`

Required report sections, in order:

1. `Executive Summary`
2. `Stakeholder-Ready Product Narratives`
3. `Epic Map`
4. `Coverage Gaps`
5. `Additional Notes`

Per-story requirements:

- one canonical actor-action-benefit story sentence
- confidence label: `High`, `Medium`, or `Low`
- confidence rationale
- at least one code evidence reference
- test evidence or explicit `No direct test evidence`
- `TODO: Confirm` for unresolved actor, action, or benefit fields

In scope:

- inferring implemented user-visible outcomes
- grouping stories into evidence-based epics or features
- documenting coverage gaps for code areas without clear user-facing mapping
- backing up an existing report before overwrite

Out of scope:

- technical-only stories with no user-visible outcome
- speculative product history
- multi-file output

## Workflow

1. Define analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inventory user-facing surfaces such as UI routes, API endpoints, CLI commands, workflows, and integrations.
3. Trace those surfaces into handlers, services, and domain logic and collect `path:line` evidence.
4. Use tests to strengthen or weaken confidence about each inferred outcome.
5. Cluster related outcomes into concise inferred epics or features.
6. Draft the report from `./assets/report-template.md`, then replace placeholders with actual content.
7. Write one canonical story per user-visible outcome and use `TODO: Confirm` for unsupported actor, action, or benefit fields.
8. Assign `High`, `Medium`, or `Low` confidence based on evidence strength and completeness.
9. Record non-mapped code areas in `Coverage Gaps` and unresolved ambiguity in `Additional Notes`.
10. Resolve the destination path from user input when provided; otherwise resolve `<project-name>` from user input, the nearest relevant `package.json`, or the repository directory name, normalize it to lowercase kebab-case, and use `docs/research/<project-name>/user-stories.md`.
11. If the destination report already exists, create a timestamped backup in the same directory before overwrite.
12. Validate with `bash ./scripts/validate_report.sh <destination-path>`.
13. Deliver the report as reconstructed implemented user outcomes, not as speculative product strategy.

## Gotchas

- If story benefits are guessed from naming alone, the report sounds polished but overstates what the code actually proves. Keep the story and mark unsupported fields `TODO: Confirm`.
- If technical capabilities that users never experience are forced into stories, the epic map fills with implementation trivia and loses stakeholder value. Put those areas in `Coverage Gaps` instead.
- If confidence is assigned by narrative coherence instead of evidence depth, weak stories get treated as facts downstream. Base confidence on code and test support only.
- If ambiguous stories are dropped entirely, the report falsely suggests complete understanding of the product surface. Include plausible user-visible outcomes with lower confidence and clear uncertainty.
- If the template placeholders survive into the final report, validation may catch them late and the artifact becomes harder to trust. Draft from the template, then clear every placeholder deliberately.
- If evidence references are not concrete, reviewers cannot challenge or refine the derivation without redoing the whole pass. Keep `path:line` support on every story.
- If an existing report is overwritten without backup, previous interpretations disappear and review loses context. Create the timestamped backup first.

## Deliverables

- the chosen user-stories report destination
- a timestamped backup when overwriting an existing report
- stakeholder narratives, epic map, coverage gaps, and additional notes
- user stories with confidence, rationale, and evidence references
- validation passing via `./scripts/validate_report.sh`

## Validation Checklist

- report path is the user-specified destination or the default `docs/research/<project-name>/user-stories.md`
- existing report backup is created before overwrite when needed
- all five required sections exist in order
- every story follows the canonical actor-action-benefit contract
- every story includes confidence, rationale, and evidence references
- unresolved story fields are marked `TODO: Confirm`
- no template placeholders remain

## Deterministic Validation

- `bash ./scripts/validate_report.sh <destination-path>`
