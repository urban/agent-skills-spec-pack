---
name: write-technical-design
description: "Define and validate canonical technical-design artifacts. Use when a workflow creates, derives, reviews, or validates architecture and implementation strategy documentation that must stay compatible across workflows."
license: MIT
metadata:
  version: "0.5.3"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared technical-design artifact contract: canonical section order, minimum content, diagram-slot rules, template shape, and deterministic validation. Keep authored and derived technical-design artifacts compatible without owning workflow-wide lineage policy.

## Contract

- Artifact shape:
  - one Markdown artifact
  - canonical frontmatter when the workflow stamps provenance
  - keep every required section even when unresolved; use `TODO: Confirm` instead of deleting sections
  - required sections, in order:
    1. `Architecture Summary`
    2. `System Context`
    3. `Components and Responsibilities`
    4. `Data Model and Data Flow`
    5. `Interfaces and Contracts`
    6. `Integration Points`
    7. `Failure and Recovery Strategy`
    8. `Security, Reliability, and Performance`
    9. `Implementation Strategy`
    10. `Testing Strategy`
    11. `Risks and Tradeoffs`
    12. `Further Notes`
- Scope boundary:
  - technical design explains solution shape, runtime behavior, boundaries, interactions, and tradeoffs
  - reference charter, user stories, and requirements as scope anchors instead of copying them into the design
  - do not turn the artifact into requirements restatement, commit sequencing, or task breakdown
  - this skill does not own workflow-wide `source_artifacts` policy
- Diagram slots:
  - `## System Context` must contain `### Process Flowchart` before `### Context Flowchart`
  - `## Components and Responsibilities` must contain `### Behavior State Diagram`
  - `## Data Model and Data Flow` must contain `### Entity Relationship Diagram`
  - `### Interaction Diagram` is optional under `## Interfaces and Contracts`
  - each required slot must contain the expected Mermaid type, `Not needed:`, or `TODO: Confirm`
  - expected types: `flowchart`, `flowchart`, `stateDiagram-v2`, `erDiagram`, and optional `sequenceDiagram`
- Minimum content:
  - concrete architecture summary; name runtime model and composition root when observable
  - at least one named component or subsystem
  - each named component subsection starts with one orienting sentence directly below the `###` heading and before bullets
  - traceability notes use relevant `US1.x` story IDs or requirement IDs in system context or component impact notes when they clarify scope
  - interfaces include accepted grammars, validation rules, and boundary errors when they materially affect callers
  - failure and recovery cover degraded modes and typed versus thrown failures when present
  - implementation strategy names recomposition sites, resource ownership, and direct runtime escape hatches when observable
  - explicit testing strategy, risks, and tradeoffs
  - at least one short non-Mermaid fenced code block, with surrounding prose, to clarify a contract, schema, persisted shape, result family, or composition seam
  - when the target stack is known, code examples use its current names, conventions, idioms, and best practices
  - use shared Mermaid diagram guidance when diagrams explain structure, interaction, behavior, or data relationships faster than prose
  - use `TODO: Confirm` for unresolved high-impact details instead of optimistic filler

## Inputs

- approved charter, user stories, and requirements when authoring
- repository evidence when deriving as-built design
- known runtime boundaries, integrations, operational concerns, and implementation constraints
- visual explanation needs when a diagram adds clarity faster than prose

## Outputs

- one canonical technical-design Markdown artifact compatible across authoring, derivation, review, and downstream planning
- the shared template at `./assets/technical-design-template.md`
- deterministic validation via `./scripts/validate_technical_design.sh`

## Workflow

1. Start from `./assets/technical-design-template.md`.
2. Carry approved or reconstructed behavior forward as design consequences; use relevant `US1.x` or requirement IDs as traceability anchors.
3. Define runtime edges, components, ownership, interfaces, data flow, integration points, failure model, and operational qualities concretely enough to implement.
4. Fill the required diagram slots with the expected Mermaid type, `Not needed:`, or `TODO: Confirm`; add an interaction diagram only when participant choreography adds material clarity.
5. Add short representative code examples only when they explain a contract or seam faster than prose, and explain what each example shows.
6. Keep unresolved or weakly supported high-impact details explicit as `TODO: Confirm`.
7. Validate with `bash ./scripts/validate_technical_design.sh <technical-design-file>`.

## Validation

- Run: `bash ./scripts/validate_technical_design.sh <technical-design-file>`
- Confirm the artifact stays technical design, not copied requirements or a task list.
- Confirm required diagram slots, component-definition rule, traceability anchors, and non-Mermaid code-example rule are satisfied.
- Confirm canonical frontmatter is valid when the workflow stamps provenance.
