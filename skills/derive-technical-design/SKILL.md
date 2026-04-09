---
name: derive-technical-design
description: Reconstruct technical-design artifacts from repository evidence and reconstructed specification context. Use when a user needs as-built architecture, boundaries, and implementation strategy documented for an existing system.
metadata:
  version: 0.4.1
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

## Rules

- Treat code, tests, configuration, and repository structure as the primary evidence because this role documents the system that exists today.
- Produce the artifact as `technical-design.md`.
- Use the `write-technical-design` contract so the derived artifact stays compatible with authored technical design.
- Use `visual-diagramming` to choose and author Mermaid diagrams when observed architecture, interactions, behavior, or data relationships will be understood faster visually than through prose alone.
- Add an interaction diagram only when observed ordered collaboration between named participants explains the implemented system more clearly than the process flowchart, context flowchart, and surrounding prose.
- When diagram wording, syntax safety, or slot-specific completeness is unclear, load the relevant `visual-diagramming` references instead of inventing local conventions.
- Upstream reconstructed artifacts help, but source code wins when it proves stronger runtime, validation, lifecycle, or failure constraints.
- Identify and document the composition root, runtime profile, layer or service graph, parser boundaries, validation seams, tagged error surfaces, resource ownership, and direct runtime escape hatches when the repository shows them.
- When Effect imports or `Layer` composition are present, load `effect-technical-design` to recover the actual abstractions in use and their recomposition seams.
- Apply `gray-box-modules` only when repository evidence supports a real bounded capability with a caller-visible seam.
- Recover the observed error model, including direct thrown errors or direct host-runtime API usage, instead of rewriting the implementation into a preferred future-state style.
- Distinguish observed architecture from inferred rationale because code often shows structure more clearly than intent.
- Use context from `./charter.md`, `./user-stories.md`, and `./requirements.md` when they exist because reconstructed design should stay aligned to reconstructed framing, outcomes, and obligations.
- When reconstructed stories include canonical `US1.x` identifiers, use those IDs in design traceability notes so downstream plans can anchor on stable reconstructed story references.
- Use `TODO: Confirm` when rationale, ownership, boundary strength, or visible behavior cannot be proved from the repository.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `technical-design.md`.
- The artifact must stay compatible with the `write-technical-design` contract.
- Under `System Context`, `### Process Flowchart` must appear before `### Context Flowchart`.
- The artifact must explicitly address the four required diagram slots from `write-technical-design`: process flowchart, context flowchart, behavior state diagram, and entity relationship diagram.
- `### Interaction Diagram` is optional and should be added only when observed ordered collaboration between participants adds material clarity beyond the process flowchart, context flowchart, and surrounding prose.
- Diagrams must stay evidence-based and support the observed system instead of proposing a cleaner future state.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not recommend future-state improvements as if they were the current architecture.
- Do not stop at generic “CLI + service” descriptions when the code shows concrete boundary types and runtime wiring.
- Do not rewrite direct host-runtime APIs or direct thrown-error usage into idealized abstraction-only architecture in derived design.
- Do not invent gray-box modules from naming, directory layout, or ideal decomposition alone.
- Do not copy reconstructed five-field story blocks into the design as substitute architecture content.

## Requirements

Inputs:

- repository source code
- repository tests when present
- repository configuration and project structure
- package manifests, runtime entrypoints, command definitions, schemas, parsers, error types, config, and tests when present
- optional user-provided scope paths
- optional user-provided output destination

Output:

- one derived technical-design artifact named `technical-design.md`

In scope:

- reconstructing architecture, subsystem responsibilities, interfaces, data flow, and operational concerns
- describing implementation strategy and testing strategy implied by the codebase
- describing composition root and runtime profile when observable
- documenting service, layer, parser, validator, and adapter boundaries when source-backed
- documenting parser or validator seams, resource and lifecycle ownership, and error surfaces when source-backed
- translating reconstructed story behavior into observed interaction paths, state transitions, feedback surfaces, and failure handling when supported by evidence
- documenting evidence-backed gray-box modules when the seam is real
- backing up an existing report before overwrite

Out of scope:

- redesigning the system
- rewriting requirements from scratch
- presenting speculative module boundaries as observed fact

## Workflow

1. Confirm the user needs technical-design artifacts reconstructed from repository evidence and specification context, then confirm analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inspect code, tests, configuration, repo layout, and runtime entrypoints for architecture signals.
3. Detect the runtime profile and composition root.
4. Use `reconstruct-implementation-constraints` to inventory execution-relevant runtime, parser, validation, integration, lifecycle, dependency, packaging, and failure constraints.
5. Inventory boundary types and their owned capabilities:
   - command handlers or other entrypoints
   - services and layers
   - parser or decoder modules
   - validators
   - integration adapters
6. Inventory resource ownership and mutation sites such as temp directories, child processes, scoped resources, long-lived services, and filesystem write paths.
7. Inventory the observed error model, including tagged errors, schema errors, platform errors, direct thrown errors, degraded modes, and operator-visible recovery behavior.
8. Use reconstructed stories from `./user-stories.md` and requirements from `./requirements.md` when available to preserve behavioral traceability.
9. Translate observed upstream behavior into as-built design consequences:
   - use story `US1.x` identifiers to anchor design traceability notes and component impact notes
   - use story `Actor` and `Action` to identify observed entry points and interaction surfaces
   - use story `Situation` to capture triggers, boundary conditions, and lifecycle entry points visible in the code
   - use story `Outcome` to identify the result the implementation is trying to produce
   - use story `Observation` to identify visible outputs, status changes, review points, or feedback mechanisms
   - use reconstructed requirements to anchor obligations and constraints the code appears to implement
10. If Effect imports or `Layer` composition are present, load `effect-technical-design` to document the actual Effect abstractions, composition sites, and runtime escape hatches in use.
11. Evaluate whether any bounded capability meets the gray-box evidence threshold before documenting it as a module boundary.
12. Use `visual-diagramming` to fill the required process, context, state, and entity diagram slots with either the expected Mermaid diagram, a `Not needed:` rationale, or `TODO: Confirm` when applicability is unresolved, while avoiding claims the evidence cannot support, and add an interaction diagram only when participant choreography adds material explanatory value.
13. Load the relevant `visual-diagramming` references when syntax safety, interaction sequencing, flowchart mode, ERD scope, or state naming is unclear.
14. Load `references/diagram-evidence.md` when diagram wording, slot applicability, or evidence thresholds are unclear.
15. Resolve the chosen destination path.
16. If the destination artifact already exists, create a timestamped backup in the same directory before overwrite.
17. Draft the artifact with the `write-technical-design` contract.
18. Write `technical-design.md` to the chosen destination.
19. Mark inferred rationale, weak seams, ambiguous ownership, or unresolved packaging assumptions as `TODO: Confirm` rather than upgrading them to confident design facts.
20. When stronger source-backed constraints emerge than `requirements.md` captured, mark them for requirement reconciliation before final delivery.
21. Validate with `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`.
22. Deliver the artifact as as-built architecture documentation, not as a cleanup proposal.

## Gotchas

- If you document the architecture you wish the repo had, later planning starts from fiction and misses the real constraints. Describe the system that exists today.
- If you stop at generic “CLI + service” prose, the design misses the composition root, layer graph, parser boundaries, and other concrete seams that guide change work. Name those seams when the code proves them.
- If direct thrown errors, direct host-runtime APIs, or other runtime escape hatches are normalized away, the report stops matching the implementation. Record observed facts first.
- If directory names alone are treated as module boundaries, gray-box documentation looks tidy but collapses under inspection. Require evidence of caller-visible seams, ownership, or boundary tests.
- If inferred rationale is written in the same voice as observed structure, reviewers cannot tell fact from interpretation. Separate the two and use `TODO: Confirm` for weak conclusions.
- If design traceability relies on story titles instead of canonical `US1.x` IDs, downstream planning loses stable reconstructed anchors when titles change. Carry the story IDs forward.
- If you only reconstruct action flows and ignore situations or observations, the design misses triggers, boundary handling, and visible feedback behavior. Preserve those signals when evidence supports them.
- If data flow is skipped because the codebase is large, the final document names parts without explaining how the system actually works. Trace the important paths end to end.
- If contradictory evidence between tests, config, and implementation is smoothed over, the report hides the repo's real design risk. Preserve the ambiguity instead of cleaning it up.
- If a derived diagram explains more than the repository proves, readers trust a picture that the evidence cannot support. Keep diagrams anchored to observed behavior and mark weak spots `TODO: Confirm`.
- If an interaction diagram only repeats the process flowchart or nearby prose, it makes the artifact busier without improving understanding. Add it only when participant choreography, handoffs, or commit boundaries need the extra evidence-backed view.
- If the composition root is omitted, the runtime architecture stays too vague to guide later changes. Name the entrypoint and recomposition sites when observable.
- If an existing report is overwritten without backup, future review loses the history of how understanding changed. Create the timestamped backup first.

## Deliverables

- `technical-design.md`
- a timestamped backup when overwriting an existing artifact
- as-built architecture, implementation-strategy, and testing-strategy documentation
- traceability notes that reference relevant reconstructed `US1.x` story IDs or requirement IDs
- explicit composition-root, runtime-profile, boundary, resource-ownership, and error-model coverage when source-backed
- the four required diagram slots completed with evidence-backed Mermaid diagrams, `Not needed:` rationales, or `TODO: Confirm`
- an optional interaction diagram only when ordered participant collaboration adds explanatory value, using `sequenceDiagram`, `Not needed:`, or `TODO: Confirm` when included
- validation passing via the shared technical-design validator

## References

- [`references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: deciding whether observed repository seams are strong enough to document as gray-box modules.
- [`references/diagram-evidence.md`](./references/diagram-evidence.md): Read when: filling required diagram slots and deciding whether an optional interaction diagram adds value in a derived technical design without overstating certainty.

## Validation Checklist

- artifact filename is `technical-design.md`
- existing artifact backup is created before overwrite when needed
- section order follows the `write-technical-design` contract
- composition root and runtime profile are named when observable
- named components include concrete boundary types when observable
- parser, validation, resource, and error boundaries are documented when source-backed
- named components, interfaces, testing strategy, and risks or tradeoffs are explicit
- design traceability uses relevant reconstructed `US1.x` story IDs or requirement IDs where those anchors clarify scope
- all four required diagram slots are present, `### Process Flowchart` appears before `### Context Flowchart`, and the required slots are completed without overstating certainty
- if an `### Interaction Diagram` subsection is present, it adds explanatory value and stays evidence-backed
- reconstructed story behavior influences observed interfaces, state, feedback, or failure handling where relevant
- gray-box module claims are tied to concrete repository evidence
- stronger technical findings are marked for requirement reconciliation when needed
- unresolved high-impact details are marked `TODO: Confirm`
- validation passes with the shared script

## Deterministic Validation

- `bash ../write-technical-design/scripts/validate_technical_design.sh <resolved-technical-design-path>`
