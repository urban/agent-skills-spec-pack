---
name: charter
description: "Produce charter artifacts from approved product framing. Use when a user needs approved scope, goals, non-goals, personas, and success criteria captured for specification work."
license: MIT
metadata:
  version: "0.2.1"
  author: "urban (https://github.com)"
  layer: specialist
  archetype: planning
  domain: specification-authoring
  dependencies:
    - write-charter
---

## Purpose

Produce `charter.md` from approved product framing. Capture the approved scope baseline, actors, and measurable success criteria without re-owning user stories, requirements, technical design, or planning.

## Boundaries

- Output filename: `charter.md`
- Source of truth: approved product intent, problem statement, and scope framing; use repository evidence only when existing behavior, integrations, or platform constraints materially affect scope or success criteria
- Artifact contract: follow `../write-charter/SKILL.md`
- In scope:
  - define goals and non-goals
  - name personas and actors
  - record measurable success criteria
  - preserve explicit uncertainty where needed
- Out of scope:
  - detailed user stories
  - detailed requirements
  - technical architecture
  - implementation task planning
  - code changes
- Ask only when ambiguity changes goals, non-goals, actors, success criteria, scope, software quality, provenance or validator compatibility, or approval readiness.

## Inputs

- product idea, feature request, or approved problem statement
- desired outcomes, goals, and scope boundaries
- known actors, stakeholders, and success measures
- repository evidence when existing behavior affects framing

## Output

- `charter.md`
- one charter artifact downstream user stories, requirements, and design can trust as the approved scope baseline

## Workflow

1. Load approved framing and gather goals, non-goals, actors, and success signals; inspect repo evidence only where existing behavior or constraints materially affect framing.
2. Draft `charter.md` with the `write-charter` contract.
3. Make goals and non-goals explicit before downstream artifacts add behavior or solution detail.
4. Keep personas or actors concrete and write measurable `SC1.x` success criteria.
5. Move user-visible behaviors, detailed obligations, and design ideas out of the charter.
6. Mark unresolved high-impact details as `TODO: Confirm`.
7. Validate with `bash ../write-charter/scripts/validate_charter.sh <resolved-charter-path>`.
8. Deliver for approval before user stories, requirements, or technical design proceed.

## Validation

- Run: `bash ../write-charter/scripts/validate_charter.sh <resolved-charter-path>`
- Confirm filename is `charter.md`, section order matches the shared contract, and success criteria use `SC1.x`.
- Confirm goals and non-goals are explicit, and at least one success criterion exists.
- Confirm detailed user stories, requirements, and implementation strategy are not mixed into the artifact.
- Confirm unresolved high-impact details stay `TODO: Confirm`.

## Approval-view focus

- goals and non-goals that set scope edges
- personas or actors that will shape downstream stories
- measurable success criteria and obvious scope risks
- any `TODO: Confirm` item that would distort downstream artifacts if treated as settled
