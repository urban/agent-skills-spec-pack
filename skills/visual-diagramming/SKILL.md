---
name: visual-diagramming
description: "Select and author Mermaid diagrams that clarify systems, behavior, relationships, or journeys. Use when an artifact needs a visual explanation grounded in the available evidence."
license: MIT
metadata:
  version: "0.2.0"
  author: "urban (https://github.com)"
  layer: foundational
---

## Rules

- Prefer diagrams when they communicate shape, behavior, or experience faster than prose because the work must stay legible to humans.
- Use prose to add constraints, assumptions, exceptions, tradeoffs, or details the diagram cannot carry; do not restate the diagram in sentence form.
- Choose the diagram that answers the main question with the least ambiguity, not the one that is most familiar.
- Use multiple small diagrams when one diagram would mix concerns such as structure, ordering, state, and data shape.
- Keep labels consistent with the surrounding artifact because renamed actors, components, or entities make the diagram unverifiable.
- In derived artifacts, keep every diagram evidence-based and mark weak inferences as `TODO: Confirm`.
- Omit a diagram type when it adds no clarity and say why instead of forcing decorative coverage.
- Prefer Mermaid syntax that renders in common markdown viewers unless the target renderer is known and the added feature materially improves clarity.
- Keep diagrams readable before making them attractive; styling may support meaning, but the diagram must remain understandable without decorative treatment.

## Authoring workflow

1. Identify the main question the artifact needs the diagram to answer.
2. Confirm the available evidence and note any uncertainty that must remain explicit.
3. Choose the smallest diagram type that answers that question clearly.
4. Extract only the actors, entities, states, steps, or touchpoints needed for that diagram.
5. Draft Mermaid with concise, renderer-safe labels.
6. Check completeness, readability, and compatibility with common Mermaid renderers.
7. Add only the prose the diagram cannot show, and mark weak inferences as `TODO: Confirm`.

## Mermaid syntax safety

- Keep node and state labels short, plain, and renderer-safe.
- Avoid `1. Text` patterns inside labels because some renderers parse them as markdown lists.
- Prefer stable subgraph IDs with display labels, and reference the IDs rather than the display text.
- Avoid emoji and punctuation-heavy labels unless they are necessary for correctness.
- Prefer simple syntax that is portable across GitHub, Obsidian, and similar markdown environments.
- Read [`references/syntax-safety.md`](./references/syntax-safety.md) when authoring or reviewing Mermaid labels, subgraphs, or parser-sensitive syntax.

## Prose-to-diagram extraction pattern

When the source material is prose, extract diagram structure before writing Mermaid:

- Nouns and named roles often become actors, participants, entities, systems, or states.
- Verbs and events often become transitions, messages, actions, or decision labels.
- Ordered steps often become `sequenceDiagram` or `flowchart` structure.
- Durable records and their links often become `erDiagram` entities and relationships.
- Conditions, modes, or lifecycle stages often become `stateDiagram-v2` states.
- Persona stages, touchpoints, and friction often become `journey` structure.

If the same prose suggests multiple diagram types, choose the one that answers the artifact's main question with the least ambiguity. Add a second focused diagram only when the remaining concern is important enough to justify it.

## Supported diagrams

- `journey`: use for persona stages, actions, touchpoints, and pain points. Best when the question is what the actor experiences over time.
  - Minimum completeness: identify the persona or actor, order the stages, and show the key touchpoints or friction.
- `sequenceDiagram`: use for ordered interactions between actors, components, or systems. Best when the question is who talks to whom and in what order.
  - Minimum completeness: name all participants, distinguish the key exchanges, and include alternate paths when they materially change the behavior.
  - Read [`references/sequence-diagram-conventions.md`](./references/sequence-diagram-conventions.md) when interaction ordering, participant naming, or alternate paths are central.
- `stateDiagram-v2`: use for lifecycle behavior and allowed transitions. Best when the question is how one entity, workflow, or process changes state.
  - Minimum completeness: states read like conditions, transitions read like triggers, and start or end states appear where relevant.
  - Read [`references/state-diagram-naming.md`](./references/state-diagram-naming.md) when authoring or reviewing state-diagram naming for states, transitions, actions, guards, parent states, or invoked actors.
- `flowchart`: use for process flow, decision flow, routing, and system context. Best when the question is how work moves through steps or how systems and boundaries relate without claiming sequence timing.
  - Minimum completeness: the starting point or boundary is clear, decisions or relationships are labeled explicitly, and the overall flow direction is coherent.
  - Read [`references/flowchart-conventions.md`](./references/flowchart-conventions.md) when a flowchart could be mistaken for state, sequence, architecture, or process structure.
- `erDiagram`: use for persistent entities and relationships. Best when the question is what durable records exist and how they relate.
  - Minimum completeness: entities are named, relationships are shown, and cardinality is supported by the available evidence.
  - Read [`references/erd-conventions.md`](./references/erd-conventions.md) when relationship cardinality, field inclusion, or conceptual versus implementation detail affects correctness.

## Output format

Use a compact documentation-first structure:

````markdown
## <Diagram Title>

```mermaid
<diagram>
```

Notes:
- <why this diagram type was chosen>
- <constraint, caveat, or assumption the diagram cannot show>
- `TODO: Confirm` for any weak inference
````

Omit the notes section only when the diagram is fully self-explanatory and there are no important caveats.

## Artifact guidance

### Technical design

- Use diagrams where they clarify architecture better than prose.
- Prefer `flowchart` for system context and major data or control flow.
- Prefer `sequenceDiagram` for interface orchestration and integration behavior.
- Prefer `stateDiagram-v2` for meaningful workflow or entity lifecycle rules.
- Prefer `erDiagram` when persistent data shape is central to correctness or implementation.

### Derived technical design

- Use the same diagram types as authored technical design, but only when code, tests, config, or existing documentation support them.
- If the repository shows behavior but not intent, diagram the observed behavior and mark uncertain design claims as `TODO: Confirm`.
- Do not clean up or idealize the architecture in diagrams beyond what the evidence supports.

### User stories

- Prefer `journey` for persona-centered stories because it keeps the focus on stages, touchpoints, and friction.
- Use `sequenceDiagram` only when interaction ordering is central to the story.
- Use `flowchart` only when branching paths or decision logic matter more than lived experience.
- Avoid technical diagrams that pull the artifact away from actor value.

## Readability and compatibility

- Prefer one primary story per diagram.
- Split diagrams when they mix concerns, need multiple legends, or grow beyond a readable scale.
- Prefer concise labels over sentence-length text.
- Default to `TD` or `LR` when direction needs to be explicit and no stronger layout cue exists.
- Use color only when it encodes meaning; the diagram must remain understandable without color.
- Avoid advanced Mermaid features unless the target renderer is known and the extra complexity materially improves clarity.

## Gotchas

- If you add a diagram and then paraphrase every node and arrow below it, the artifact gets longer without getting clearer. Add only the constraints or caveats the diagram cannot show.
- If you pick a sequence diagram for a state problem, reviewers see steps but miss the lifecycle rules. Use `stateDiagram-v2` when the real question is allowed transitions.
- If you force every artifact to include every diagram type, diagrams become ceremony and humans stop trusting them. Include only diagrams that remove ambiguity.
- If derived diagrams smooth over contradictions in the codebase, the artifact looks polished but becomes fiction. Diagram implemented reality and mark weak spots `TODO: Confirm`.
- If one diagram tries to show personas, orchestration, state, and entities at once, it becomes unreadable and nobody checks it. Split by concern.
- If labels in the diagram do not match names used elsewhere in the artifact, readers waste time translating instead of understanding. Reuse the same names everywhere.
- If a diagram depends on styling, animation, or a renderer-specific feature to make sense, the artifact becomes fragile. Prefer semantic labels and simple structure first.

## References

- [`references/syntax-safety.md`](./references/syntax-safety.md): Read when authoring or reviewing Mermaid labels, subgraphs, numbering, or parser-sensitive syntax.
- [`references/sequence-diagram-conventions.md`](./references/sequence-diagram-conventions.md): Read when participant roles, ordering, alternate paths, or message clarity matter.
- [`references/flowchart-conventions.md`](./references/flowchart-conventions.md): Read when a flowchart is carrying process, routing, or system-context meaning.
- [`references/erd-conventions.md`](./references/erd-conventions.md): Read when entity relationships, cardinality, or attribute scope affect correctness.
- [`references/state-diagram-naming.md`](./references/state-diagram-naming.md): Read when authoring or reviewing `stateDiagram-v2` naming for states, transitions, actions, guards, parent states, or invoked actors.

## Validation Checklist

- The chosen diagram answers the artifact's main question faster than prose.
- Prose adds constraints or detail not visible in the diagram and does not repeat it.
- Diagram type matches the concern: journey, interaction order, state, flow, or entity relationships.
- The diagram includes the minimum completeness required for its type.
- Mermaid labels and structure follow the syntax-safety rules needed for common renderers.
- Large or mixed concerns are split into multiple focused diagrams.
- Labels match the surrounding artifact terminology.
- Derived diagrams stay evidence-based and use `TODO: Confirm` for weak inferences.
- Output follows the standard documentation-first format unless there is a strong reason to simplify it.
- Omitted diagram types are omitted intentionally, with a short reason when omission might be surprising.
