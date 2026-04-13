---
name: write-technical-design
description: "Write and validate canonical technical-design artifacts. Use when a task creates, derives, reviews, or validates architecture and implementation strategy documentation that must stay compatible across workflows."
license: MIT
metadata:
  version: "0.5.2"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Rules

- Keep technical design separate from product requirements and execution task breakdowns because architecture should explain solution shape, not product scope or local sequencing.
- Preserve canonical frontmatter shape and validate created artifacts with the shared provenance validator when the workflow stamps provenance.
- Treat the approved charter, user stories, and requirements as the source of truth for scope, user-visible behavior, and obligations; reference them instead of restating them in the design.
- When canonical user stories are available, use their `US1.x` identifiers in design traceability notes and component impact notes so downstream planning can link back to stable story anchors.
- Use Mermaid diagram-authoring guidance when a Mermaid diagram communicates structure, interaction, behavior, or data relationships faster than prose because technical design is for humans making implementation decisions.
- Add an interaction diagram only when ordered collaboration between named participants explains the system more clearly than the process flowchart, context flowchart, and surrounding prose.
- Describe the system in terms of responsibilities, boundaries, interactions, and tradeoffs because component lists without relationships do not guide implementation.
- Start each named component subsection with one orienting sentence immediately below the heading and before any bullets so readers can understand the component before scanning structured detail.
- Include short representative code examples when they explain a contract, schema, result family, persisted shape, or composition seam better than prose alone.
- Surround code examples with supporting prose that explains what the example is illustrating and why that shape matters.
- When the design targets a known library, framework, or platform, write code examples that fit the chosen stack, using its current names and following its conventions, idioms, and best practices instead of generic pseudocode or outdated APIs.
- Keep interfaces, data flow, and operational concerns concrete enough to implement because vague design prose fails downstream.
- When observable, name the composition root, runtime profile, boundary types, resource ownership, and error model explicitly.
- For derived design, record the actual abstractions and runtime escape hatches the code uses, even when they differ from preferred style.
- Interface sections should include accepted grammars, validation rules, and boundary errors when they materially shape callers.
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
- Include at least one short non-Mermaid fenced code block somewhere in the artifact; code examples must stay short and cannot replace architectural explanation.
- Under `Components and Responsibilities`, each named component subsection must contain a one-sentence definition paragraph directly below the `###` heading and before the structured bullet list.
- Under `System Context`, `### Process Flowchart` must appear before `### Context Flowchart`.
- The artifact must explicitly address four required diagram slots: process flowchart, context flowchart, behavior state diagram, and entity relationship diagram.
- Each required diagram slot must contain either a Mermaid diagram of the expected type, a `Not needed:` rationale, or `TODO: Confirm` when applicability is still unresolved.
- `### Interaction Diagram` is optional and should be added only when ordered collaboration between participants adds material clarity beyond the process flowchart, context flowchart, and surrounding prose.
- When an optional `### Interaction Diagram` subsection is included, it must contain either a `sequenceDiagram`, a `Not needed:` rationale, or `TODO: Confirm`.
- If a required section is not yet confirmed, keep the section and mark it `TODO: Confirm`.
- Do not copy charter framing, five-field story blocks, or requirement lists into the design as substitute content.

## Requirements

A valid technical-design artifact must include these sections in this order:

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
- a concrete architecture summary that names the runtime model and composition root when observable
- at least one named component or subsystem
- each named component begins with a one-sentence definition paragraph directly below its heading
- at least one short non-Mermaid fenced code block illustrates a contract, schema, result family, persisted shape, or composition seam
- named components include concrete boundary types when observable
- interfaces and contracts include accepted grammars, validation rules, and error surfaces when they materially affect callers
- failure and recovery includes typed versus thrown failures, degraded modes, and operator-visible recovery paths when present
- implementation strategy explains recomposition sites and ownership, not only rollout prose
- traceability notes use relevant `US1.x` story IDs or requirement IDs where those anchors clarify design scope
- explicit testing strategy
- explicit risks and tradeoffs
- a `### Process Flowchart` subsection using `flowchart`, `Not needed:`, or `TODO: Confirm`
- a `### Context Flowchart` subsection using `flowchart`, `Not needed:`, or `TODO: Confirm`, placed after `### Process Flowchart`
- a `### Behavior State Diagram` subsection using `stateDiagram-v2`, `Not needed:`, or `TODO: Confirm`
- a `### Entity Relationship Diagram` subsection using `erDiagram`, `Not needed:`, or `TODO: Confirm`
- if present, a `### Interaction Diagram` subsection using `sequenceDiagram`, `Not needed:`, or `TODO: Confirm`
- `TODO: Confirm` where a high-impact design detail is unresolved or weakly supported

Inputs:

- approved requirements or repository evidence for derived design
- approved or reconstructed user stories that define user-visible behavior
- known architecture boundaries, integrations, operational concerns, and implementation constraints
- visual explanation needs such as process flow, context, interactions, state behavior, persona flow, or persistent entity relationships when diagrams would add clarity

Output:

- one technical design Markdown artifact that downstream planning and implementation work can use directly

## Workflow

1. Identify the approved charter, user stories, requirements, or implemented behavior the design must satisfy and use them as referenced scope anchors.
2. Draft from [`assets/technical-design-template.md`](./assets/technical-design-template.md) so canonical ordering stays intact.
3. Translate upstream behavior into design consequences:
   - carry forward relevant story `US1.x` identifiers into design traceability notes and component impact notes
   - user-story `Actor` and `Action` shape primary interfaces and interaction paths
   - user-story `Situation` shapes triggers, lifecycle entry points, and boundary conditions
   - user-story `Outcome` shapes success criteria the architecture must preserve
   - user-story `Observation` shapes externally visible signals, state transitions, or interaction feedback that design must support
   - requirements shape explicit obligations, constraints, and contracts
4. Distinguish runtime edges, domain or service boundaries, parser or decoder boundaries, validator boundaries, and integration adapters before filling sections.
5. Define major components or subsystems and state their responsibilities, boundary types, ownership, and interactions.
6. For each named component subsection, write one sentence directly below the heading that orients the reader before the structured bullets begin.
7. Add one or more short representative code examples when they clarify contracts, schemas, result families, persisted shapes, or composition seams better than prose alone.
8. If the target uses a known library, framework, or platform, make those examples fit the chosen stack, using its current names and following its conventions, idioms, and best practices.
9. Use Mermaid diagram-authoring guidance to fill the required process, context, state, and entity diagram slots with either the right Mermaid diagram, a `Not needed:` rationale, or `TODO: Confirm` when applicability is unresolved, and add an interaction diagram only when participant choreography adds material explanatory value.
10. Describe data flow, interfaces, integration points, grammars, validation rules, and failure handling in enough detail to guide implementation.
11. Record security, reliability, performance, implementation strategy, resource ownership, and testing strategy decisions.
12. Surface risks, tradeoffs, and unresolved questions rather than burying them in narrative.
13. For derived design, separate observed architecture from inferred intent and use `TODO: Confirm` for weak conclusions.
14. Validate the finished artifact with [`scripts/validate_technical_design.sh`](./scripts/validate_technical_design.sh).

## Gotchas

- If the document repeats charter, user-story, or requirements content instead of explaining boundaries and interactions, implementers still have to invent the architecture. Reference upstream artifacts, then spend the document on solution shape.
- If components are listed without boundary type, owned capability, or ownership, the design becomes a directory tour rather than a system model. Name what each component owns and how it interacts with others.
- If the first line under a component heading is a bullet list, the section becomes harder to skim and reviewers have to infer the component's purpose from fragments. Start with one orienting sentence, then move into the bullets.
- If a technical design that would benefit from examples contains no code blocks, readers have to reconstruct types and contracts from prose alone. Include short representative examples where they materially improve understanding.
- If code examples appear without supporting explanation, the document gains syntax but not clarity. Introduce or follow each example with prose that explains what it is illustrating.
- If code examples use outdated framework or library patterns, the artifact teaches the wrong implementation style while appearing authoritative. Use current names and best practices for the target stack.
- If interfaces omit accepted grammars, validation rules, or boundary errors, important contracts stay implicit and change risk hides until coding. Make those seams explicit when they matter.
- If interfaces and data flow stay vague, teams discover incompatible assumptions only during coding. Make boundary contracts and major data movement explicit.
- If you add a diagram and then repeat it in prose, the document gets longer without adding signal. Use the surrounding text for constraints, caveats, and decisions the diagram cannot show.
- If you silently skip a required process, context, state, or entity diagram slot because the system seems simple, validation will fail and reviewers will not know whether the omission was intentional. Fill every required slot with a diagram, `Not needed:`, or `TODO: Confirm`.
- If an interaction diagram only restates the process flowchart or nearby prose, it adds ceremony instead of understanding. Add it only when participant choreography, handoffs, or commit boundaries need the extra view.
- If implementation strategy ignores composition roots, dependency-wiring sites, or resource ownership, layered and multi-boundary designs become too vague to guide change work. Name recomposition and ownership explicitly.
- If implementation strategy turns into a task list, planning gets duplicated and the design ages badly. Explain rollout approach and sequencing constraints, not every work item.
- If design traceability relies on story titles instead of canonical `US1.x` IDs, later story renames break downstream references. Use story IDs whenever stories are available.
- If derived design smooths over contradictions in the codebase, later planning treats speculation as architecture fact. Report implemented reality and mark weak seams `TODO: Confirm`.
- If failure and recovery strategy is skipped, reliability bugs get deferred until production because no one owned them in design. Capture degraded modes, typed and thrown failures, and recovery paths explicitly.
- If risks and tradeoffs are generic, reviewers cannot challenge the real decision points. Record the concrete tensions this design is actually choosing between.
- If workflow lineage rules are embedded here, the foundational contract stops being reusable across authoring and reconstruction. Leave workflow-specific `source_artifacts` policy to coordination.
- If design ignores story `Situation` or `Observation`, the architecture may satisfy happy-path behavior while missing triggers, feedback, and boundary handling. Carry those signals forward.

## Deliverables

- A Markdown technical-design artifact with canonical frontmatter shape and section order.
- Traceability notes that reference canonical `US1.x` story IDs or requirement IDs where relevant.
- Explicit architecture, component responsibilities, data flow, interfaces, operational concerns, and implementation strategy.
- The four required diagram slots completed with Mermaid diagrams, `Not needed:` rationales, or `TODO: Confirm`, chosen with Mermaid diagram-authoring guidance.
- An optional interaction diagram only when ordered participant collaboration adds explanatory value, using `sequenceDiagram`, `Not needed:`, or `TODO: Confirm` when included.
- A concrete testing strategy plus explicit risks and tradeoffs.
- One or more short representative code examples with supporting prose.
- Clear `TODO: Confirm` markers for unresolved high-impact design details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation when the workflow stamps provenance.
- All required sections exist and are in the correct order.
- Architecture and implementation strategy are both present.
- Runtime model and composition root are present when observable.
- At least one component or subsystem is named explicitly.
- Each named component begins with one orienting sentence directly below its heading.
- At least one short non-Mermaid fenced code block appears in the artifact.
- Code examples are explained by surrounding prose rather than dropped in without context.
- Named components include boundary type and owned capability when observable.
- Validation and error seams are explicit when source-backed.
- Resource and lifecycle ownership is explicit when it materially affects behavior.
- Testing strategy and risks or tradeoffs are explicit.
- All four required diagram slots exist, `### Process Flowchart` appears before `### Context Flowchart`, and each required slot uses the expected Mermaid type, `Not needed:`, or `TODO: Confirm`.
- If an `### Interaction Diagram` subsection is present, it adds explanatory value and uses `sequenceDiagram`, `Not needed:`, or `TODO: Confirm`.
- Traceability notes use relevant `US1.x` story IDs or requirement IDs where those anchors clarify the design.
- User-story behavior influences interfaces, triggers, state, or feedback where relevant rather than being copied verbatim.
- Mermaid diagrams are chosen to clarify rather than decorate and their prose does not simply restate them.
- The artifact remains technical design rather than a task list or code dump.
- Direct runtime escape hatches are documented when relevant.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_technical_design.sh <technical-design-file>`
