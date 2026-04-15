---
name: derive-charter
description: "Reconstruct charter artifacts from repository evidence. Use when a user needs implemented goals, boundaries, personas, and success criteria documented for an existing system with explicit uncertainty."
license: MIT
metadata:
  version: "0.2.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - write-charter
---

## Purpose

Produce `charter.md` from repository evidence. Reconstruct plausible goals, non-goals, personas, and success criteria from implemented behavior without inventing product history or pretending the recovered framing was historically approved.

## Boundaries

- Output filename: `charter.md`
- Source of truth: repository code and tests; stronger repository evidence wins over cleaner narrative
- Artifact contract: follow `../write-charter/SKILL.md`
- In scope:
  - reconstruct plausible goals, non-goals, personas, and success criteria from observable behavior and constraints
  - preserve explicit uncertainty where business framing cannot be proved confidently
  - back up an existing report before overwrite
- Out of scope:
  - presenting guessed strategy as recovered fact
  - reconstructing detailed requirements or technical design
  - using commit history, PR text, or external docs as primary evidence
- Ask only when ambiguity changes scope, destination, evidence threshold, artifact shape, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- repository source code
- repository tests when present
- optional user-provided scope paths
- optional user-provided output destination

## Output

- `charter.md`
- a timestamped backup in the same directory before overwrite when the destination already exists
- one reconstructed charter artifact downstream work can trust as evidence-bounded framing with explicit uncertainty

## Workflow

1. Confirm analysis scope and destination; default to the full repository when the user does not narrow it.
2. Inspect code and tests to inventory user-visible surfaces, constraints, role boundaries, and measurable outcomes.
3. Infer candidate goals, non-goals, personas, and success criteria only as far as the evidence supports.
4. If the destination already exists, create a timestamped backup in the same directory before overwrite.
5. Draft `charter.md` with the `write-charter` contract.
6. Add evidence-aware `TODO: Confirm` wherever framing remains weakly supported.
7. Validate with `bash ../write-charter/scripts/validate_charter.sh <resolved-charter-path>`.
8. Deliver the result as reconstructed framing grounded in implemented evidence, not speculative product history.

## Validation

- Run: `bash ../write-charter/scripts/validate_charter.sh <resolved-charter-path>`
- Confirm backup exists before overwrite when needed and filename is `charter.md`.
- Confirm section order and `SC1.x` numbering match the shared contract.
- Confirm goals, non-goals, personas, and success criteria are grounded in observable evidence rather than guessed intent.
- Confirm unresolved high-impact details stay `TODO: Confirm`.

## Approval-view focus

- highest-confidence framing and measurable outcomes
- weakly supported goals, non-goals, or personas
- evidence basis for success criteria and obvious scope boundaries
- any `TODO: Confirm` item that would distort downstream reconstruction if treated as settled
