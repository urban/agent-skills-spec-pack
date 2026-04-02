---
name: derive-charter
description: Reconstruct charter-form artifacts from repository code and tests. Use when a user wants goals, non-goals, personas, and success criteria recovered from implemented software with explicit uncertainty handling.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - write-charter
---

## Rules

- Treat repository code and tests as the primary evidence because this role documents implemented reality, not remembered product strategy.
- Use the `write-charter` contract so the derived artifact stays compatible with authored charter artifacts while remaining explicit that it is reconstructed, not historically approved.
- Infer goals, non-goals, personas, and success criteria only as far as repository evidence supports them because business framing is often only partially observable in code.
- Keep evidence traceable to concrete file paths and line references when support is thin or disputed.
- Use `TODO: Confirm` when the repository cannot prove framing details strongly enough.

## Constraints

- Output must be one Markdown report at the user-specified destination or, by default, `docs/research/<project-name>/charter.md`.
- The artifact must stay compatible with the `write-charter` contract.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not claim original intent, non-goals, or success measures that are not supportable from repository evidence.
- Do not turn low-level implementation details into fake goals or personas just to fill sections.

## Requirements

Inputs:

- repository source code
- repository tests when present
- optional user-provided scope paths
- optional user-provided output destination

Output:

- one derived charter report at the user-specified destination or, when no destination is provided, `docs/research/<project-name>/charter.md`

In scope:

- reconstructing plausible goals, non-goals, personas, and success criteria from implemented behavior and constraints
- preserving explicit uncertainty where business framing cannot be proved confidently
- backing up an existing report before overwrite

Out of scope:

- presenting guessed strategy as recovered fact
- reconstructing detailed requirements or technical design
- using commit history, PR text, or external docs as primary evidence

## Workflow

1. Confirm analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inventory user-visible surfaces, constraints, role boundaries, and measurable outcomes from code and tests.
3. Infer candidate goals, non-goals, personas, and success criteria only as far as the evidence supports and mark weak conclusions as `TODO: Confirm`.
4. Resolve the destination path from user input when provided; otherwise resolve `<project-name>` from the nearest package or repository name and use `docs/research/<project-name>/charter.md`.
5. If the destination report already exists, create a timestamped backup in the same directory before overwrite.
6. Draft the chosen destination with the `write-charter` contract.
7. Add evidence-aware `TODO: Confirm` markers anywhere framing remains weakly supported.
8. Validate with `bash ../write-charter/scripts/validate_charter.sh <destination-path>`.
9. Deliver the report as reconstructed charter-form scope grounded in implemented evidence, not as speculative product history or proof of historical approval.

## Gotchas

- If you treat naming or UI labels as proof of business goals, the artifact becomes cleaner than the evidence allows. Keep weak framing explicit with `TODO: Confirm`.
- If you infer personas from internal module names alone, later stories inherit invented actors. Use observable entry points, permissions, workflows, or tests to support actor claims.
- If code constraints are rewritten as product goals, the charter artifact misstates why the system exists. Separate inferred purpose from implementation necessity.
- If success criteria are guessed from optimism instead of measurable signals in the codebase, future planning inherits fake definitions of done. Keep success claims concrete or mark them unresolved.
- If weak evidence is omitted entirely, reviewers read silence as certainty. Keep ambiguous framing and mark it clearly.
- If you overwrite an existing research report without a backup, later reviewers lose the ability to compare interpretations across passes. Create the timestamped backup first.

## Deliverables

- the chosen charter report destination
- a timestamped backup when overwriting an existing report
- evidence-based reconstructed framing with explicit uncertainty handling
- validation passing via the shared charter validator

## Validation Checklist

- report path is the user-specified destination or the default `docs/research/<project-name>/charter.md`
- existing report backup is created before overwrite when needed
- section order follows the `write-charter` contract
- goals, non-goals, personas, and success criteria are derived from observable evidence rather than guessed product history
- unresolved high-impact details are marked `TODO: Confirm`
- validation passes with the shared script

## Deterministic Validation

- `bash ../write-charter/scripts/validate_charter.sh <destination-path>`
