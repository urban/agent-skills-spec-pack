---
name: technical-design
description: Produce technical-design artifacts from approved specification context and repository evidence. Use when a user needs architecture, boundaries, interfaces, and implementation strategy documented before coding.
metadata:
  version: 0.3.4
  layer: specialist
  archetype: design
  domain: specification-authoring
  dependencies:
    - effect-technical-design
    - gray-box-modules
    - visual-diagramming
    - write-technical-design
---

## Rules

- Keep this role focused on technical design because approved scope, actors, and success criteria belong in the charter, requirements own product obligations, and execution sequencing belongs in planning.
- Produce the artifact as `technical-design.md`.
- Use the `write-technical-design` contract for section order, content boundaries, shared validation, diagram slot requirements, traceability expectations, component-definition formatting, and representative code-example expectations because downstream planning expects that canonical shape.
- Under each named component heading, write one orienting sentence before any bullet list so readers can understand the component at a glance before scanning its structured details.
- Include short representative code examples when they clarify a contract, schema, result family, persisted shape, or composition seam faster than prose alone, and surround them with prose that explains what the example is illustrating.
- If the target system uses a known library, framework, or platform, the representative code examples should fit the chosen stack, using its current names and following its conventions, idioms, and best practices rather than generic placeholders or outdated APIs.
- When `./user-stories.md` includes canonical story IDs, carry those `US1.x` identifiers into design traceability notes instead of relying on story titles alone.
- Use `visual-diagramming` to choose and author Mermaid diagrams when architecture, interactions, behavior, or data relationships will be understood faster visually than through prose alone.
- Add an interaction diagram only when ordered collaboration between named participants explains the system more clearly than the process flowchart, context flowchart, and surrounding prose.
- When diagram wording, syntax safety, or slot-specific completeness is unclear, load the relevant `visual-diagramming` references instead of improvising local conventions.
- Ground the design in approved charter, approved requirements, approved stories, and repository evidence because architecture without scope alignment becomes speculative.
- Use approved upstream context from `./charter.md`, `./user-stories.md`, and `./requirements.md`.
- Apply `gray-box-modules` only when the system exposes meaningful bounded capabilities with durable caller-visible seams.
- If the target system uses Effect, load `../effect-technical-design/SKILL.md` and apply its decomposition, recomposition, and abstraction-selection guidance instead of inventing ad hoc Effect architecture rules.
- Mark unresolved high-impact design choices as `TODO: Confirm` instead of smoothing them over.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `technical-design.md`.
- The artifact must stay compatible with the `write-technical-design` contract.
- Include architecture, interfaces, data flow, operational concerns, implementation strategy, and testing strategy.
- Under `System Context`, `### Process Flowchart` must appear before `### Context Flowchart`.
- The artifact must explicitly address the four required diagram slots from `write-technical-design`: process flowchart, context flowchart, behavior state diagram, and entity relationship diagram.
- `### Interaction Diagram` is optional and should be added only when ordered collaboration between participants adds material clarity beyond the process flowchart, context flowchart, and surrounding prose.
- Use diagrams to support understanding, then use prose to add detail the diagrams cannot show without repeating them.
- Do not collapse the design into requirements restatement, copied five-field story blocks, a file inventory, or a flat task list.
- Do not invent module boundaries that are not supported by approved scope and repository evidence.
- For each named component subsection, place the one-sentence definition directly below the heading and before the structured bullets.
- Include at least one short non-Mermaid fenced code block somewhere in the artifact when it materially clarifies the technical design.

## Requirements

Inputs:

- approved charter
- approved user stories
- approved requirements artifact
- repository evidence when code, infrastructure, or integrations already exist
- known constraints, integrations, operational expectations, and runtime model

Output:

- one complete technical-design artifact named `technical-design.md`

In scope:

- defining architecture and subsystem responsibilities
- documenting boundaries, interfaces, and data flow
- translating approved story behavior into interaction paths, state transitions, visible feedback, and failure handling
- capturing implementation strategy, testing strategy, risks, and tradeoffs
- using gray-box module descriptions when evidence supports them
- using the Effect-specific foundational guidance when the target system is built with Effect

Out of scope:

- redefining product framing, user stories, or requirements
- generating execution tasks
- code changes

## Workflow

1. Confirm the user needs technical-design artifacts from approved specification context and repository evidence, then gather the approved charter, user stories, and requirements context.
2. Inspect repository structure, code, and integration boundaries when existing implementation constrains the design.
3. Identify major components, responsibilities, interfaces, operational seams, and runtime surfaces needed to satisfy the approved scope.
4. Translate approved upstream behavior into design consequences:
   - use story `US1.x` identifiers to anchor design traceability notes and component impact notes
   - use story `Actor` and `Action` to identify interaction surfaces and owned responsibilities
   - use story `Situation` to preserve triggers, lifecycle entry points, and boundary conditions
   - use story `Outcome` to preserve the value-bearing result the design must support
   - use story `Observation` to preserve externally visible signals, feedback, or review points
   - use requirements to formalize contracts, constraints, and implementation obligations
5. If the target system uses Effect, load `../effect-technical-design/SKILL.md` before finalizing boundaries so decomposition, recomposition, and abstraction choices stay consistent with the shared Effect guidance.
6. Use `visual-diagramming` to fill the required process, context, state, and entity diagram slots with either the expected Mermaid diagram, a `Not needed:` rationale, or `TODO: Confirm` when applicability is unresolved, and add an interaction diagram only when participant choreography adds material explanatory value.
7. Load the relevant `visual-diagramming` references when syntax safety, interaction sequencing, flowchart mode, ERD scope, or state naming is unclear.
8. Apply `gray-box-modules` only to capabilities with durable caller-visible boundaries; otherwise describe the observed structure without forcing the pattern.
9. Draft `technical-design.md` using the `write-technical-design` contract.
10. For each named component subsection, add a one-sentence definition immediately below the heading before listing boundary type, owned capability, hidden depth, inputs, outputs, and impact notes.
11. Add one or more short representative code examples where they clarify the design better than prose alone, especially for contracts, schemas, result families, persisted shapes, or composition seams.
12. When the target system uses a known library, framework, or platform, ensure those code examples fit the chosen stack, using its current names and following its conventions, idioms, and best practices; if the system uses Effect, keep them aligned with `effect-technical-design`.
13. Record implementation strategy, testing strategy, risks, tradeoffs, and `TODO: Confirm` markers for unresolved high-impact design decisions.
14. Validate with `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`.
15. Deliver the draft and request approval before implementation proceeds.

## Gotchas

- If the artifact mostly restates the charter or requirements, implementers still have to invent the architecture from scratch. Use upstream artifacts as scope anchors, then spend the document on boundaries and interactions.
- If the first line under a component heading is a bullet list, readers have to infer the component's purpose from fragments and the section becomes harder to skim. Start each component with one orienting sentence before the bullets.
- If code examples are omitted from a design that would be clearer with one, the artifact forces implementers to reverse-engineer types and contracts from prose. Add short representative examples where they carry meaning faster than paragraphs.
- If code examples appear without surrounding explanation, reviewers can read the syntax but still miss why the example matters. Introduce or follow each example with prose that names what it is illustrating.
- If code examples use outdated or non-idiomatic patterns for the chosen stack, they teach the wrong architecture while appearing precise. Use that stack's current names, conventions, idioms, and best practices.
- If components are named without owned responsibilities, the design becomes a directory tour instead of a system model. State what each component owns and how it interacts with others.
- If you force every design into gray-box modules, weak seams get documented as facts and later work ossifies around speculation. Use the pattern only when evidence supports a real boundary.
- If design traceability relies on story titles instead of canonical `US1.x` IDs, later story renames break downstream planning anchors. Carry story IDs forward.
- If you only carry story actions forward and ignore situations or observations, the design misses triggers, feedback, and edge behavior. Preserve those signals.
- If data flow and interface contracts stay vague, integration bugs show up during coding when assumptions finally collide. Make boundary shape explicit before handing the design downstream.
- If an interaction diagram only repeats the process flowchart or nearby prose, it consumes attention without adding understanding. Use it only when participant choreography, handoffs, or commit boundaries need the extra view.
- If implementation strategy turns into a task list, execution planning gets duplicated and the design becomes noisy fast. Capture rollout shape and sequencing constraints, not every work item.
- If the target system uses Effect and you skip the shared Effect guidance, abstraction choices drift toward personal preference and later designs stop being comparable. Reuse the foundational Effect pattern skill instead of improvising.
- If unresolved design choices are hidden behind confident prose, planners treat guesses as settled architecture. Use `TODO: Confirm` where the decision is still open or weakly supported.

## Deliverables

- `technical-design.md`
- architecture aligned to approved charter, user stories, and requirements
- traceability notes that reference relevant `US1.x` story IDs or requirement IDs
- explicit components, each introduced by a one-sentence definition before their structured bullets, plus interfaces, data flow, implementation strategy, testing strategy, risks, and tradeoffs
- one or more short representative code examples with supporting prose, aligned to the chosen stack's current names, conventions, idioms, and best practices when the stack is known
- the four required diagram slots completed with the expected Mermaid diagrams, `Not needed:` rationales, or `TODO: Confirm`, aligned with `visual-diagramming`
- an optional interaction diagram only when ordered participant collaboration adds explanatory value, using `sequenceDiagram`, `Not needed:`, or `TODO: Confirm` when included
- validation passing via the shared technical-design validator

## Validation Checklist

- artifact filename is `technical-design.md`
- section order follows the `write-technical-design` contract
- architecture and implementation strategy are both present
- at least one component or subsystem is named explicitly and begins with a one-sentence definition before its bullets
- at least one short non-Mermaid fenced code block appears where it clarifies the design
- code examples are accompanied by prose that explains what they illustrate
- testing strategy and risks/tradeoffs are explicit
- all four required diagram slots are present, `### Process Flowchart` appears before `### Context Flowchart`, and each required slot is intentionally completed
- if an `### Interaction Diagram` subsection is present, it adds explanatory value and is intentionally completed
- design traceability uses relevant `US1.x` story IDs or requirement IDs where those anchors clarify scope
- approved story behavior influences interaction paths, state, feedback, or failure handling where relevant
- unresolved high-impact details are marked `TODO: Confirm`

## Deterministic Validation

- `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`
