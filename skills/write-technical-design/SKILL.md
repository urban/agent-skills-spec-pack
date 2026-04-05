---
name: write-technical-design
description: Write and validate canonical software technical design artifacts. Use when a task creates, derives, reviews, or validates architecture and implementation-strategy documentation that must stay compatible across authoring and reconstruction.
metadata:
  version: 0.2.0
  layer: foundational
---

## Rules

- Keep technical design separate from product requirements and execution task breakdowns because architecture should explain solution shape, not product scope or local sequencing.
- Preserve canonical frontmatter shape and validate created artifacts with the shared provenance validator when the workflow stamps provenance.
- Treat the approved charter, user stories, and requirements as the source of truth for scope, user-visible behavior, and obligations; reference them instead of restating them in the design.
- Use `visual-diagramming` when a Mermaid diagram communicates structure, interaction, behavior, or data relationships faster than prose because technical design is for humans making implementation decisions.
- Describe the system in terms of responsibilities, boundaries, interactions, and tradeoffs because component lists without relationships do not guide implementation.
- Keep interfaces, data flow, and operational concerns concrete enough to implement because vague design prose fails downstream.
- Use prose around diagrams to add constraints, assumptions, exceptions, and tradeoffs; do not paraphrase the diagram.
- Capture risks and tradeoffs explicitly because those decisions are part of the design contract.
- Mark unresolved high-impact details as `TODO: Confirm` instead of filling gaps with optimism.
- When deriving design from code, document the architecture that exists rather than the architecture that would be cleaner.
- Translate approved or reconstructed user-story behavior into design consequences rather than copying story blocks verbatim.

## Constraints

- Output must be one Markdown artifact.
- The shared technical-design contract does not define workflow-wide `source_artifacts` policy.
- Required sections must appear in canonical order.
- Include architecture and implementation strategy, but do not expand into commit sequencing or atomic task lists.
- Code snippets are optional and must stay short; they cannot replace architectural explanation.
- The artifact must explicitly address four diagram slots: context flowchart, behavior state diagram, entity relationship diagram, and interaction diagram.
- Each diagram slot must contain either a Mermaid diagram of the expected type, a `Not needed:` rationale, or `TODO: Confirm` when applicability is still unresolved.
- If a required section is not yet confirmed, keep the section and mark it `TODO: Confirm`.
- Do not copy charter framing, five-field story blocks, or requirement lists into the design as substitute content.

## Requirements

A valid technical design artifact must include these sections in this order:

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

Minimum content expectations:

- canonical frontmatter shape when provenance is stamped for the workflow
- a concrete architecture summary
- at least one named component or subsystem
- explicit testing strategy
- explicit risks and tradeoffs
- a `### Context Flowchart` subsection using `flowchart`, `Not needed:`, or `TODO: Confirm`
- a `### Behavior State Diagram` subsection using `stateDiagram-v2`, `Not needed:`, or `TODO: Confirm`
- a `### Entity Relationship Diagram` subsection using `erDiagram`, `Not needed:`, or `TODO: Confirm`
- a `### Interaction Diagram` subsection using `sequenceDiagram`, `Not needed:`, or `TODO: Confirm`
- `TODO: Confirm` where a high-impact design detail is unresolved or weakly supported

Inputs:

- approved requirements or repository evidence for derived design
- approved or reconstructed user stories that define user-visible behavior
- known architecture boundaries, integrations, operational concerns, and implementation constraints
- visual explanation needs such as context, interactions, state behavior, persona flow, or persistent entity relationships when diagrams would add clarity

Output:

- one technical design Markdown artifact that downstream planning and implementation work can use directly

## Workflow

1. Identify the approved charter, user stories, requirements, or implemented behavior the design must satisfy and use them as referenced scope anchors.
2. Draft from [`assets/technical-design-template.md`](./assets/technical-design-template.md) so canonical ordering stays intact.
3. Translate upstream behavior into design consequences:
   - user-story `Actor` and `Action` shape primary interfaces and interaction paths
   - user-story `Situation` shapes triggers, lifecycle entry points, and boundary conditions
   - user-story `Outcome` shapes success criteria the architecture must preserve
   - user-story `Observation` shapes externally visible signals, state transitions, or interaction feedback that design must support
   - requirements shape explicit obligations, constraints, and contracts
4. Define major components or subsystems and state their responsibilities and interactions.
5. Use `visual-diagramming` to fill the required diagram slots with either the right Mermaid diagram, a `Not needed:` rationale, or `TODO: Confirm` when applicability is unresolved.
6. Describe data flow, interfaces, integration points, and failure handling in enough detail to guide implementation.
7. Record security, reliability, performance, implementation strategy, and testing strategy decisions.
8. Surface risks, tradeoffs, and unresolved questions rather than burying them in narrative.
9. For derived design, separate observed architecture from inferred intent and use `TODO: Confirm` for weak conclusions.
10. Validate the finished artifact with [`scripts/validate_technical_design.sh`](./scripts/validate_technical_design.sh).

## Gotchas

- If the document repeats charter, user-story, or requirements content instead of explaining boundaries and interactions, implementers still have to invent the architecture. Reference upstream artifacts, then spend the document on solution shape.
- If components are listed without owned responsibilities, the design becomes a directory tour rather than a system model. Name what each component owns and how it interacts with others.
- If interfaces and data flow stay vague, teams discover incompatible assumptions only during coding. Make boundary contracts and major data movement explicit.
- If you add a diagram and then repeat it in prose, the document gets longer without adding signal. Use the surrounding text for constraints, caveats, and decisions the diagram cannot show.
- If you silently skip a required diagram slot because the system seems simple, validation will fail and reviewers will not know whether the omission was intentional. Fill every slot with a diagram, `Not needed:`, or `TODO: Confirm`.
- If implementation strategy turns into a task list, planning gets duplicated and the design ages badly. Explain rollout approach and sequencing constraints, not every work item.
- If derived design smooths over contradictions in the codebase, later planning treats speculation as architecture fact. Report implemented reality and mark weak seams `TODO: Confirm`.
- If failure and recovery strategy is skipped, reliability bugs get deferred until production because no one owned them in design. Capture degraded modes, error handling, and recovery paths explicitly.
- If risks and tradeoffs are generic, reviewers cannot challenge the real decision points. Record the concrete tensions this design is actually choosing between.
- If workflow lineage rules are embedded here, the foundational contract stops being reusable across authoring and reconstruction. Leave workflow-specific `source_artifacts` policy to coordination.
- If design ignores story `Situation` or `Observation`, the architecture may satisfy happy-path behavior while missing triggers, feedback, and boundary handling. Carry those signals forward.

## Deliverables

- A Markdown technical design artifact with canonical frontmatter shape and section order.
- Explicit architecture, component responsibilities, data flow, interfaces, operational concerns, and implementation strategy.
- The four required diagram slots completed with Mermaid diagrams, `Not needed:` rationales, or `TODO: Confirm`, chosen with `visual-diagramming`.
- A concrete testing strategy plus explicit risks and tradeoffs.
- Clear `TODO: Confirm` markers for unresolved high-impact design details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation when the workflow stamps provenance.
- All required sections exist and are in the correct order.
- Architecture and implementation strategy are both present.
- At least one component or subsystem is named explicitly.
- Testing strategy and risks/tradeoffs are explicit.
- All four required diagram slots exist and each uses the expected Mermaid type, `Not needed:`, or `TODO: Confirm`.
- User-story behavior influences interfaces, triggers, state, or feedback where relevant rather than being copied verbatim.
- Mermaid diagrams are chosen to clarify rather than decorate and their prose does not simply restate them.
- The artifact remains technical design rather than a task list or code dump.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_technical_design.sh <technical-design-file>`
