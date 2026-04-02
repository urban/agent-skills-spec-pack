---
name: technical-design
description: Produce technical design artifacts from approved charter, requirements, and repository evidence. Use when a user wants architecture, boundaries, and implementation strategy defined before coding.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: design
  domain: specification-authoring
  dependencies:
    - artifact-naming
    - document-traceability
    - effect-technical-design
    - gray-box-modules
    - visual-diagramming
    - write-technical-design
---

## Rules

- Keep this role focused on technical design because approved scope, actors, and success criteria belong in the charter, requirements own product obligations, and execution sequencing belongs in planning.
- Use `artifact-naming` to resolve and preserve `<project-name>` because skill-pack file paths must stay aligned.
- Use `document-traceability` to stamp canonical provenance plus `source_artifacts.charter`, `source_artifacts.user_stories`, and `source_artifacts.requirements` because design depends on the approved upstream specification.
- Use the `write-technical-design` contract for section order and content boundaries because downstream planning expects that canonical shape.
- Use `visual-diagramming` to choose Mermaid diagrams when architecture, interactions, behavior, or data relationships will be understood faster visually than through prose alone.
- Ground the design in approved charter, approved requirements, approved stories, and repository evidence because architecture without scope alignment becomes speculative.
- Apply `gray-box-modules` only when the system exposes meaningful bounded capabilities with durable caller-visible seams.
- If the target system uses Effect, load `../effect-technical-design/SKILL.md` and apply its decomposition, recomposition, and abstraction-selection guidance instead of inventing ad hoc Effect architecture rules.
- Mark unresolved high-impact design choices as `TODO: Confirm` instead of smoothing them over.

## Constraints

- Output must be one Markdown artifact at `.specs/<project-name>/technical-design.md`.
- The artifact must stay compatible with the `write-technical-design` contract.
- The artifact must record `source_artifacts.charter`, `source_artifacts.user_stories`, and `source_artifacts.requirements`.
- Include architecture, interfaces, data flow, operational concerns, implementation strategy, and testing strategy.
- The artifact must explicitly address the four required diagram slots from `write-technical-design`: context flowchart, behavior state diagram, entity relationship diagram, and interaction diagram.
- Use diagrams to support understanding, then use prose to add detail the diagrams cannot show without repeating them.
- Do not collapse the design into requirements restatement, a file inventory, or a flat task list.
- Do not invent module boundaries that are not supported by approved scope and repository evidence.

## Requirements

Inputs:

- approved charter
- approved user stories
- approved requirements artifact
- repository evidence when code, infrastructure, or integrations already exist
- known constraints, integrations, operational expectations, and runtime model

Output:

- one complete technical design artifact at `.specs/<project-name>/technical-design.md`

In scope:

- defining architecture and subsystem responsibilities
- documenting boundaries, interfaces, and data flow
- capturing implementation strategy, testing strategy, risks, and tradeoffs
- using gray-box module descriptions when evidence supports them
- using the Effect-specific foundational guidance when the target system is built with Effect
- stamping deterministic authored-document provenance and source-artifact lineage

Out of scope:

- redefining product framing, user stories, or requirements
- generating execution tasks
- code changes

## Workflow

1. Confirm the user wants a technical design artifact and gather the approved charter, user stories, and requirements context.
2. Resolve `<project-name>` with `artifact-naming` and keep it stable for the run.
3. Capture `root_skill` from the active authored workflow and set `producing_skill = technical-design`.
4. Inspect repository structure, code, and integration boundaries when existing implementation constrains the design.
5. Identify major components, responsibilities, interfaces, operational seams, and runtime surfaces needed to satisfy the approved scope.
6. If the target system uses Effect, load `../effect-technical-design/SKILL.md` before finalizing boundaries so decomposition, recomposition, and abstraction choices stay consistent with the shared Effect guidance.
7. Use `visual-diagramming` to fill the four required diagram slots with either the expected Mermaid diagram, a `Not needed:` rationale, or `TODO: Confirm` when applicability is unresolved.
8. Apply `gray-box-modules` only to capabilities with durable caller-visible boundaries; otherwise describe the observed structure without forcing the pattern.
9. Draft `.specs/<project-name>/technical-design.md` using the `write-technical-design` contract.
10. Stamp canonical provenance with `source_artifacts.charter`, `source_artifacts.user_stories`, and `source_artifacts.requirements`.
11. Record implementation strategy, testing strategy, risks, tradeoffs, and `TODO: Confirm` markers for unresolved high-impact design decisions.
12. Validate with `bash ../write-technical-design/scripts/validate_technical_design.sh .specs/<project-name>/technical-design.md`.
13. Deliver the draft and request approval before implementation proceeds.

## Gotchas

- If the artifact mostly restates the charter or requirements, implementers still have to invent the architecture from scratch. Use upstream artifacts as scope anchors, then spend the document on boundaries and interactions.
- If components are named without owned responsibilities, the design becomes a directory tour instead of a system model. State what each component owns and how it interacts with others.
- If you force every design into gray-box modules, weak seams get documented as facts and later work ossifies around speculation. Use the pattern only when evidence supports a real boundary.
- If data flow and interface contracts stay vague, integration bugs show up during coding when assumptions finally collide. Make boundary shape explicit before handing the design downstream.
- If implementation strategy turns into a task list, execution planning gets duplicated and the design becomes noisy fast. Capture rollout shape and sequencing constraints, not every work item.
- If the target system uses Effect and you skip the shared Effect guidance, abstraction choices drift toward personal preference and later designs stop being comparable. Reuse the foundational Effect pattern skill instead of improvising.
- If provenance omits any upstream spec artifact, execution planning cannot prove what design commitments came from where. Keep all required source-artifact roles explicit.
- If unresolved design choices are hidden behind confident prose, planners treat guesses as settled architecture. Use `TODO: Confirm` where the decision is still open or weakly supported.

## Deliverables

- `.specs/<project-name>/technical-design.md`
- architecture aligned to approved charter, user stories, and requirements
- explicit components, interfaces, data flow, implementation strategy, testing strategy, risks, and tradeoffs
- deterministic provenance plus required source-artifact lineage
- the four required diagram slots completed with the expected Mermaid diagrams, `Not needed:` rationales, or `TODO: Confirm`, aligned with `visual-diagramming`
- validation passing via the shared technical-design validator

## Validation Checklist

- artifact path is `.specs/<project-name>/technical-design.md`
- section order follows the `write-technical-design` contract
- required source-artifact roles are present
- architecture and implementation strategy are both present
- at least one component or subsystem is named explicitly
- testing strategy and risks/tradeoffs are explicit
- all four required diagram slots are present and intentionally completed
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-technical-design/scripts/validate_technical_design.sh .specs/<project-name>/technical-design.md`
