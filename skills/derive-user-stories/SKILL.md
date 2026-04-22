---
name: derive-user-stories
description: "Reconstruct user-stories artifacts from repository evidence. Use when a user needs implemented user-visible behavior and capability areas documented for an existing system."
license: MIT
metadata:
  version: "0.3.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - write-user-stories
---

## Purpose

Produce `user-stories.md` from repository evidence. Reconstruct implemented user-visible behavior, actors, and capability areas without inventing product history or forcing technical-only internals into stories.

## Boundaries

- Output filename: `user-stories.md`
- Source of truth: repository code and tests; reconstructed `./charter.md` is supporting context, and stronger repository evidence wins
- Artifact contract: use canonical story blocks compatible with `../write-user-stories/SKILL.md`
- Report shape:
  - draft from `./assets/report-template.md`
  - output one Markdown artifact with these sections, in order:
    1. `Executive Summary`
    2. `Stakeholder-Ready Product Narratives`
    3. `Capability Map`
    4. `Coverage Gaps`
    5. `Additional Notes`
  - `Capability Map` must include at least one `## Capability Area:` section and at least one canonical story block
  - every story must include:
    - unique `US1.x` story identifier
    - canonical `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`
    - `Confidence: High|Medium|Low`
    - `Rationale`
    - `Code Evidence` with at least one `path:line` reference
    - `Test Evidence` or `No direct test evidence`
    - `TODO: Confirm` for unresolved story details when needed
- In scope:
  - infer implemented user-visible outcomes and evidence-based capability areas
  - document coverage gaps for code areas without clear user-facing mapping
  - keep confidence tied to evidence depth
  - back up an existing report before overwrite
- Out of scope:
  - technical-only stories with no user-visible outcome
  - speculative product history or roadmap intent
  - multi-file output
  - PR descriptions, commit history, issue trackers, or external docs as primary evidence
  - workflow-wide `source_artifacts` lineage policy
- Ask only when ambiguity changes scope, destination, evidence threshold, artifact shape, confidence assignment, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- repository source code
- repository tests when present
- optional user-provided scope paths or modules
- optional user-provided output destination
- reconstructed `./charter.md` when present

## Output

- `user-stories.md`
- a timestamped backup in the same directory before overwrite when the destination already exists
- one derived user-stories artifact with executive summary, stakeholder narratives, capability map, coverage gaps, and evidence-backed story blocks ready for downstream requirements work

## Workflow

1. Confirm analysis scope and destination; default to the full repository when the user does not narrow it.
2. Inventory user-facing surfaces such as UI routes, API endpoints, CLI commands, workflows, and integrations.
3. Trace those surfaces into handlers, services, and domain logic; collect concrete `path:line` evidence and use tests to strengthen or weaken confidence.
4. Identify evidence-based actors and capability areas; use reconstructed `./charter.md` only as supporting context.
5. Draft from `./assets/report-template.md`; write one canonical story block per user-visible outcome in `Capability Map`, assign unique `US1.x` identifiers, and add confidence, rationale, code evidence, and test evidence.
6. Put technically important but not clearly user-visible areas in `Coverage Gaps` instead of forcing them into stories.
7. Include ambiguous but plausible user-visible outcomes with lower confidence and `TODO: Confirm` instead of dropping them.
8. If the destination already exists, create a timestamped backup in the same directory before overwrite.
9. Validate with `bash ./scripts/validate_report.sh <resolved-user-stories-path>`.
10. Deliver the result as reconstructed implemented user outcomes, not speculative product strategy.

## Validation

- Run: `bash ./scripts/validate_report.sh <resolved-user-stories-path>`
- Confirm backup exists before overwrite when needed and required report sections are present in order.
- Confirm every story has a unique `US1.x` identifier, canonical five fields, confidence label, rationale, code evidence, and test evidence or `No direct test evidence`.
- Confirm evidence is traceable to concrete file paths and lines, and no template placeholders remain.
- Confirm technical-only areas stay in `Coverage Gaps` instead of being forced into stories.
- Confirm ambiguous stories use lower confidence or `TODO: Confirm` instead of overclaiming certainty.

## Approval-view focus

- capability map and highest-value recovered stories
- coverage gaps and evidence weakness around likely user-facing behavior
- low-confidence stories and inferred-versus-observed pressure points
- any story or ambiguity that would mislead downstream requirements if treated as settled
- artifact approval profile owned here lives in `./assets/approval-view-profile.json`
- keep that profile aligned with this skill's review framing; do not rely on a generic template
