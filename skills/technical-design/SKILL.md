---
name: technical-design
description: "Produce technical-design artifacts from approved specification context. Use when a user needs architecture, boundaries, interfaces, and implementation strategy documented before coding."
license: MIT
metadata:
  version: "0.3.5"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: design
  domain: specification-authoring
  dependencies:
    - effect-technical-design
    - gray-box-modules
    - visual-diagramming
    - write-technical-design
---

## Purpose

Produce `technical-design.md` from approved specification context. Translate approved behavior and obligations into architecture, boundaries, interfaces, data flow, operational concerns, and implementation strategy without re-owning requirements or planning.

## Boundaries

- Output filename: `technical-design.md`
- Source of truth: approved `./charter.md`, `./user-stories.md`, and `./requirements.md`; use repository evidence when existing implementation constrains the design
- Artifact contract: follow `../write-technical-design/SKILL.md`
- In scope:
  - define architecture, subsystem responsibilities, interfaces, and data flow
  - translate approved story behavior into interaction paths, state transitions, feedback, and failure handling
  - capture implementation strategy, testing strategy, risks, and tradeoffs
  - use gray-box module descriptions only when the seam is durable and caller-visible
- Out of scope:
  - redefining product framing, user stories, or requirements
  - generating execution tasks or commit sequencing
  - code changes
  - inventing module boundaries unsupported by approved scope or repository evidence
  - workflow-wide `source_artifacts` lineage policy
- Ask only when ambiguity changes scope, artifact shape, software quality, integrations, core data model, provenance or validator compatibility, or approval readiness.

## Inputs

- approved `./charter.md`
- approved `./user-stories.md`
- approved `./requirements.md`
- repository evidence when code, infrastructure, or integrations already constrain the design
- known constraints, integrations, operational expectations, and runtime model

## Output

- `technical-design.md`
- one technical-design artifact downstream planning and implementation can trust for architecture, boundaries, interfaces, and implementation strategy

## Workflow

1. Load approved `./charter.md`, `./user-stories.md`, and `./requirements.md`; inspect repo evidence only where implementation or integrations materially constrain the design.
2. Identify runtime model, composition root, components, interfaces, data flow, integration points, failure model, and operational seams needed to satisfy approved scope.
3. Translate stories and requirements into design consequences; carry relevant `US1.x` or requirement IDs into system-context traceability notes and component impact notes.
4. If the target uses Effect, load `../effect-technical-design/SKILL.md` before finalizing boundaries or code examples.
5. Use `../gray-box-modules/SKILL.md` only when a capability has durable caller-visible seams; otherwise describe the structure directly.
6. Fill the required diagram slots using shared Mermaid diagram guidance; add `### Interaction Diagram` only when ordered collaboration adds material clarity.
7. Draft `technical-design.md` with the `write-technical-design` contract; keep one orienting sentence per named component and add short stack-true code examples with supporting prose when they clarify a contract or seam.
8. Mark unresolved high-impact choices as `TODO: Confirm`.
9. Validate with `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`.
10. Deliver for approval before implementation.

## Validation

- Run: `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`
- Confirm filename is `technical-design.md`, section order matches the shared contract, and `### Process Flowchart` appears before `### Context Flowchart`.
- Confirm all required diagram slots are intentionally completed and any optional interaction diagram adds real clarity.
- Confirm at least one named component has an orienting sentence before bullets and at least one short non-Mermaid code block has supporting prose.
- Confirm architecture, implementation strategy, testing strategy, risks or tradeoffs, and relevant `US1.x` or requirement traceability are explicit.
- Confirm the artifact stays technical design, not copied requirements or a task list.

## Approval-view focus

- architecture summary, runtime model, and composition root
- key boundaries, interface contracts, and data-flow hotspots
- implementation-strategy consequences, operational seams, and major risks or tradeoffs
- any `TODO: Confirm` item that could mislead downstream implementation
- artifact approval profile owned here lives in `./assets/approval-view-profile.json`
- keep that profile aligned with this skill's review framing; do not rely on a generic template
