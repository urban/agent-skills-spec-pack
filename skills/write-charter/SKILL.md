---
name: write-charter
description: "Write and validate canonical charter artifacts. Use when a task creates, derives, reviews, or validates scope-baseline documentation for a specification pack."
license: MIT
metadata:
  version: "0.2.0"
  author: "urban (https://github.com)"
  layer: foundational
---

## Rules

- Keep this artifact focused on the approved scope baseline because user stories, requirements, and design each own downstream detail.
- Preserve canonical frontmatter shape and validate created artifacts with the shared provenance validator when the workflow stamps provenance.
- Make goals and non-goals explicit because downstream artifacts need clear scope boundaries.
- Keep personas and actors concrete because stories and requirements should inherit a stable user lens.
- Keep success criteria externally meaningful and measurable because later artifacts need a shared definition of done.
- Mark unresolved high-impact ambiguity as `TODO: Confirm` instead of guessing.

## Constraints

- Output must be one Markdown artifact.
- The shared charter contract does not define workflow-wide `source_artifacts` policy.
- Required sections must appear in canonical order.
- Success criteria identifiers must use the shared prefix `SC1.x`.
- Do not include implementation strategy, file paths, task breakdowns, or detailed functional requirements.
- If a required section has no confirmed items yet, keep the section and use `TODO: Confirm`.

## Requirements

A valid charter artifact must include these sections in this order:

1. `Goals`
2. `Non-Goals`
3. `Personas / Actors`
4. `Success Criteria`

Minimum content expectations:

- canonical frontmatter shape when provenance is stamped for the workflow
- at least one goal bullet
- at least one numbered `SC1.x` success criterion
- every success criterion is specific enough to verify
- unresolved or weakly supported details use `TODO: Confirm`

Inputs:

- user intent or source material defining the problem and desired outcomes
- known scope boundaries, users, stakeholders, and success measures

Output:

- one charter Markdown artifact that downstream stories, requirements, and design work can reference as the approved scope baseline

## Workflow

1. Draft from [`assets/charter-template.md`](./assets/charter-template.md) so canonical ordering stays intact.
2. Record goals and explicit non-goals before downstream artifacts start adding detail.
3. Identify the personas or actors who receive value or constrain scope.
4. Write measurable success criteria with `SC1.x` identifiers.
5. Replace unresolved high-impact details with `TODO: Confirm` instead of inventing specifics.
6. Validate the finished artifact with [`scripts/validate_charter.sh`](./scripts/validate_charter.sh).

## Gotchas

- If goals exist without non-goals, adjacent ideas quietly become scope in later artifacts. State what the work will not cover.
- If personas are vague placeholders, stories and requirements inherit weak actors and drift into filler. Name concrete actors or use `TODO: Confirm`.
- If success criteria are aspiration statements instead of measurable checks, downstream artifacts cannot tell what done means. Make `SC1.x` items verifiable.
- If the artifact starts listing behaviors or architecture, it duplicates downstream work and blurs ownership. Keep it on framing, actors, and success.
- If empty sections are deleted instead of marked unresolved, later skills cannot tell whether the category was considered or forgotten. Keep the section and use `TODO: Confirm`.
- If workflow lineage rules are embedded here, the foundational contract stops being reusable across authoring and reconstruction. Leave workflow-specific `source_artifacts` policy to coordination.

## Deliverables

- A Markdown charter artifact with canonical frontmatter shape and section order.
- Explicit goals, non-goals, personas / actors, and success criteria.
- Clear `TODO: Confirm` markers for unresolved high-impact details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation when the workflow stamps provenance.
- All required sections exist and are in the correct order.
- At least one goal bullet exists.
- At least one `SC1.x` success criterion exists.
- Goals and non-goals are explicit.
- Detailed requirements and implementation strategy are not mixed into the artifact.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_charter.sh <charter-file>`
