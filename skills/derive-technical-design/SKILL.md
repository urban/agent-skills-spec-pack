---
name: derive-technical-design
description: "Reconstruct technical-design artifacts from repository evidence and reconstructed specification context. Use when a user needs as-built architecture, boundaries, and implementation strategy documented for an existing system."
license: MIT
metadata:
  version: "0.4.2"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - gray-box-modules
    - effect-technical-design
    - reconstruct-implementation-constraints
    - visual-diagramming
    - write-technical-design
---

## Purpose

Produce `technical-design.md` as as-built architecture documentation from repository evidence. Reconstruct current boundaries, runtime behavior, interfaces, operational concerns, and implementation strategy without redesigning the system.

## Boundaries

- Output filename: `technical-design.md`
- Source of truth: repository code, tests, config, manifests, entrypoints, and structure; reconstructed `./charter.md`, `./user-stories.md`, and `./requirements.md` are supporting context, and stronger repository evidence wins
- Artifact contract: follow `../write-technical-design/SKILL.md`
- In scope:
  - reconstruct architecture, subsystem responsibilities, interfaces, data flow, and operational concerns
  - recover composition root, runtime profile, boundary types, resource ownership, parser or validator seams, and error model when source-backed
  - translate reconstructed story behavior into observed interaction paths, state transitions, feedback, and failure handling when evidence supports it
  - document gray-box modules only when evidence shows a real caller-visible seam
  - back up an existing report before overwrite
- Out of scope:
  - redesigning the system or proposing a cleaner future state as if it already exists
  - speculative module boundaries or idealized abstraction-only rewrites
  - workflow-wide `source_artifacts` lineage policy
  - copying reconstructed story blocks into the design as substitute architecture content
- Ask only when ambiguity changes scope, destination, artifact shape, evidence threshold, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- repository source code
- repository tests, configuration, manifests, and project structure when present
- runtime entrypoints, schemas, parsers, validators, error types, and integrations when present
- optional scope paths from the user
- optional output destination from the user
- reconstructed `./charter.md`, `./user-stories.md`, and `./requirements.md` when present

## Output

- `technical-design.md`
- a timestamped backup in the same directory before overwrite when the destination already exists
- one as-built technical-design artifact downstream work can trust for current architecture, runtime behavior, and implementation strategy

## Workflow

1. Confirm analysis scope and destination; default to the full repository when the user does not narrow it.
2. Inspect code, tests, config, repo layout, and entrypoints for composition root, runtime profile, boundary types, resource ownership, and the observed error model.
3. Use `../reconstruct-implementation-constraints/SKILL.md` to inventory execution-relevant runtime, parser, validation, integration, lifecycle, dependency, packaging, and failure constraints.
4. Use reconstructed `./user-stories.md` and `./requirements.md` when present to preserve behavioral traceability; carry relevant `US1.x` or requirement IDs into traceability notes and component impact notes.
5. If Effect imports or `Layer` composition appear, load `../effect-technical-design/SKILL.md`; use `../gray-box-modules/SKILL.md` only when evidence shows a real caller-visible seam.
6. Fill the required diagram slots with evidence-backed Mermaid, `Not needed:`, or `TODO: Confirm`; add `### Interaction Diagram` only when participant choreography adds material clarity without overstating certainty.
7. If the destination already exists, create a timestamped backup in the same directory before overwrite.
8. Draft `technical-design.md` with the shared contract; separate observed facts from inferred rationale and keep stronger source-backed findings ready for requirement reconciliation.
9. Validate with `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`.
10. Deliver the result as as-built architecture documentation, not a cleanup proposal.

## Validation

- Run: `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`
- Confirm backup exists before overwrite when needed and filename is `technical-design.md`.
- Confirm section order and required diagram slots match the shared contract without overclaiming certainty.
- Confirm composition root, runtime profile, concrete boundaries, parser or validation seams, resource ownership, and error surfaces are documented when source-backed.
- Confirm relevant reconstructed `US1.x` or requirement IDs are carried forward, gray-box claims stay evidence-backed, and unresolved high-impact details stay `TODO: Confirm`.
- Confirm stronger technical findings are marked for requirement reconciliation when they exceed what `./requirements.md` currently captures.

## Approval-view focus

- architecture summary plus the evidence basis for the major claims
- inferred-versus-observed distinctions and confidence hotspots
- runtime, error, and resource-ownership seams most likely to affect later changes
- major risks, tradeoffs, and findings that pressure requirement reconciliation
- artifact approval profile owned here lives in `./assets/approval-view-profile.json`
- keep that profile aligned with this skill's review framing; do not rely on a generic template

## References

- [`./references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: deciding whether observed seams are strong enough to document as gray-box modules.
- [`./references/diagram-evidence.md`](./references/diagram-evidence.md): Read when: filling required diagram slots without overstating certainty.
