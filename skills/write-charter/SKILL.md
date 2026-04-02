---
name: write-charter
description: Write and validate canonical charter artifacts. Use when a task creates, reviews, or validates the goals, non-goals, personas, and success criteria that define the approved scope baseline for an authored specification pack.
metadata:
  version: 0.1.0
  layer: foundational
  dependencies:
    - document-traceability
---

## Rules

- Keep this artifact focused on the approved scope baseline because user stories, requirements, and design each own downstream detail.
- Use the `document-traceability` contract for canonical frontmatter, timestamps, provenance, and shared validation.
- Make goals and non-goals explicit because downstream artifacts need clear scope boundaries.
- Keep personas and actors concrete because stories and requirements should inherit a stable user lens.
- Keep success criteria externally meaningful and measurable because later artifacts need a shared definition of done.
- Mark unresolved high-impact ambiguity as `TODO: Confirm` instead of guessing.

## Constraints

- Output must be one Markdown artifact.
- Frontmatter must use canonical authored-document fields from `document-traceability`.
- Required sections must appear in canonical order.
- Success criteria identifiers must use the shared prefix `SC1.x`.
- `source_artifacts` must be `source_artifacts: {}`.
- Do not include implementation strategy, file paths, task breakdowns, or detailed functional requirements.
- If a required section has no confirmed items yet, keep the section and use `TODO: Confirm`.

## Requirements

A valid charter artifact must include these sections in this order:

1. `Goals`
2. `Non-Goals`
3. `Personas / Actors`
4. `Success Criteria`

Minimum content expectations:

- canonical provenance and timestamp frontmatter
- at least one goal bullet
- at least one numbered `SC1.x` success criterion
- every success criterion is specific enough to verify
- unresolved or weakly supported details use `TODO: Confirm`

Inputs:

- user intent or source material defining the problem and desired outcomes
- known scope boundaries, users, stakeholders, and success measures
- root orchestration context needed to stamp `generated_by`

Output:

- one charter Markdown artifact that downstream stories, requirements, and design work can reference as the approved scope baseline

## Workflow

1. Draft from [`assets/charter-template.md`](./assets/charter-template.md) so canonical ordering stays intact.
2. Stamp canonical frontmatter from `document-traceability`, including `source_artifacts: {}`.
3. Record goals and explicit non-goals before downstream artifacts start adding detail.
4. Identify the personas or actors who receive value or constrain scope.
5. Write measurable success criteria with `SC1.x` identifiers.
6. Replace unresolved high-impact details with `TODO: Confirm` instead of inventing specifics.
7. Validate the finished artifact with [`scripts/validate_charter.sh`](./scripts/validate_charter.sh).

## Gotchas

- If provenance is missing because charter has no upstream artifact, the root authored document still becomes untraceable. Keep the full `generated_by` block.
- If goals exist without non-goals, adjacent ideas quietly become scope in later artifacts. State what the work will not cover.
- If personas are vague placeholders, stories and requirements inherit weak actors and drift into filler. Name concrete actors or use `TODO: Confirm`.
- If success criteria are aspiration statements instead of measurable checks, downstream artifacts cannot tell what done means. Make `SC1.x` items verifiable.
- If the artifact starts listing behaviors or architecture, it duplicates downstream work and blurs ownership. Keep it on framing, actors, and success.
- If empty sections are deleted instead of marked unresolved, later skills cannot tell whether the category was considered or forgotten. Keep the section and use `TODO: Confirm`.

## Deliverables

- A Markdown charter artifact with canonical frontmatter and section order.
- Explicit goals, non-goals, personas / actors, and success criteria.
- Clear `TODO: Confirm` markers for unresolved high-impact details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation.
- All required sections exist and are in the correct order.
- `source_artifacts: {}` is present.
- At least one goal bullet exists.
- At least one `SC1.x` success criterion exists.
- Goals and non-goals are explicit.
- Detailed requirements and implementation strategy are not mixed into the artifact.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_charter.sh <charter-file>`
