---
name: visual-diagramming
description: "Define shared Mermaid diagram-selection and authoring guidance. Use when an artifact needs a visual explanation grounded in the available evidence."
license: MIT
metadata:
  version: "0.2.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own reusable Mermaid guidance for choosing diagram type, extracting only the needed structure, writing renderer-safe syntax, and keeping prose complementary rather than repetitive.

## Contract

- Choose the smallest diagram that answers the artifact's main question with the least ambiguity; split mixed concerns instead of forcing one large diagram.
- Use prose to add constraints, assumptions, exceptions, tradeoffs, or weak-evidence notes the diagram cannot show; do not paraphrase the diagram.
- Keep labels consistent with the surrounding artifact and readable in common Mermaid renderers.
- In derived artifacts, keep diagrams evidence-based and mark weak inferences as `TODO: Confirm`.
- Omit a diagram type when it adds no clarity and say why when omission could be surprising.
- Diagram selection:
  - `journey` for persona stages, touchpoints, and friction
  - `sequenceDiagram` for ordered interactions between named participants
  - `stateDiagram-v2` for lifecycle states and allowed transitions
  - `flowchart` for process flow, routing, or system context without claiming timing
  - `erDiagram` for durable entities and relationships when the evidence supports cardinality
- Minimum completeness:
  - `journey`: actor or persona, ordered stages, key touchpoints or friction
  - `sequenceDiagram`: all key participants, key exchanges, alternate paths when material
  - `stateDiagram-v2`: meaningful states, meaningful triggers, start or end states when relevant
  - `flowchart`: clear start or boundary, explicit decisions or relationships, coherent direction
  - `erDiagram`: named entities, relationships, and evidence-backed cardinality
- Syntax safety:
  - keep labels short and renderer-safe
  - avoid markdown-like numbering inside labels
  - prefer stable subgraph IDs with display labels
  - avoid renderer-specific complexity unless the target renderer is known and the gain is material
- Default output shape:
  - heading
  - Mermaid block
  - short notes only when the diagram needs caveats, rationale, or `TODO: Confirm`

## Inputs

- the main question the artifact needs the diagram to answer
- the available source evidence and any uncertainty that must stay explicit
- surrounding artifact terminology
- target renderer when known

## Outputs

- one or more Mermaid diagram sections that answer the target question faster than prose
- reusable diagram-type, syntax-safety, and prose-to-diagram guidance for the calling skill

## Workflow

1. Identify the main question and the evidence boundary.
2. Choose the smallest diagram type that answers that question clearly.
3. Extract only the actors, entities, states, steps, or touchpoints needed for that view.
4. Draft Mermaid with concise, renderer-safe labels.
5. Check type-specific completeness, readability, and common-renderer compatibility.
6. Add only the prose the diagram cannot show, and keep weak inferences explicit as `TODO: Confirm`.

## Validation

- Confirm the chosen diagram answers the main question faster than prose.
- Confirm type and minimum completeness match the concern.
- Confirm labels match the surrounding artifact terminology.
- Confirm large or mixed concerns are split into focused diagrams.
- Confirm derived diagrams stay evidence-based and weak inferences remain explicit.

## References

- [`./references/syntax-safety.md`](./references/syntax-safety.md): Read when: authoring or reviewing Mermaid labels, subgraphs, numbering, or parser-sensitive syntax.
- [`./references/sequence-diagram-conventions.md`](./references/sequence-diagram-conventions.md): Read when: participant roles, ordering, alternate paths, or message clarity matter.
- [`./references/flowchart-conventions.md`](./references/flowchart-conventions.md): Read when: a flowchart is carrying process, routing, or system-context meaning.
- [`./references/erd-conventions.md`](./references/erd-conventions.md): Read when: entity relationships, cardinality, or attribute scope affect correctness.
- [`./references/state-diagram-naming.md`](./references/state-diagram-naming.md): Read when: authoring or reviewing `stateDiagram-v2` naming for states, transitions, actions, guards, parent states, or invoked actors.
