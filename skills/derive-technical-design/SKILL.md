---
name: derive-technical-design
description: Reconstruct technical design artifacts from repository code, tests, and system structure. Use when a user wants the as-built architecture and implementation strategy documented for an existing project.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - gray-box-modules
    - visual-diagramming
    - write-technical-design
---

## Rules

- Treat code, tests, configuration, and repository structure as the primary evidence because this role documents the system that exists today.
- Use the `write-technical-design` contract so the derived artifact stays compatible with authored technical design.
- Use `visual-diagramming` to choose Mermaid diagrams when observed architecture, interactions, behavior, or data relationships will be understood faster visually than through prose alone.
- Distinguish observed architecture from inferred rationale because code often shows structure more clearly than intent.
- Apply `gray-box-modules` only when repository evidence supports a real bounded capability with a caller-visible seam.
- Use `TODO: Confirm` when rationale, ownership, or boundary strength cannot be proved from the repository.

## Constraints

- Output must be one Markdown report at the user-specified destination or, by default, `docs/research/<project-name>/technical-design.md`.
- The artifact must stay compatible with the `write-technical-design` contract.
- The artifact must explicitly address the four required diagram slots from `write-technical-design`: context flowchart, behavior state diagram, entity relationship diagram, and interaction diagram.
- Diagrams must stay evidence-based and support the observed system instead of proposing a cleaner future state.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not recommend future-state improvements as if they were the current architecture.
- Do not invent gray-box modules from naming, directory layout, or ideal decomposition alone.

## Requirements

Inputs:

- repository source code
- repository tests when present
- repository configuration and project structure
- optional user-provided scope paths
- optional user-provided output destination

Output:

- one derived technical design report at the user-specified destination or, when no destination is provided, `docs/research/<project-name>/technical-design.md`

In scope:

- reconstructing architecture, subsystem responsibilities, interfaces, data flow, and operational concerns
- describing implementation strategy and testing strategy implied by the codebase
- documenting evidence-backed gray-box modules when the seam is real
- backing up an existing report before overwrite

Out of scope:

- redesigning the system
- rewriting requirements from scratch
- presenting speculative module boundaries as observed fact

## Workflow

1. Confirm analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inspect code, tests, configuration, and repo layout for architecture signals.
3. Inventory major modules, interfaces, data flow, integrations, failure handling, and test surfaces.
4. Evaluate whether any bounded capability meets the gray-box evidence threshold before documenting it as a module boundary.
5. Use `visual-diagramming` to fill the four required diagram slots with either the expected Mermaid diagram, a `Not needed:` rationale, or `TODO: Confirm` when applicability is unresolved, while avoiding claims the evidence cannot support.
6. Load `references/diagram-evidence.md` when diagram wording, slot applicability, or evidence thresholds are unclear.
7. Resolve the destination path from user input when provided; otherwise resolve `<project-name>` from the nearest package or repository name and use `docs/research/<project-name>/technical-design.md`.
8. If the destination report already exists, create a timestamped backup in the same directory before overwrite.
9. Draft the chosen destination with the `write-technical-design` contract.
10. Mark inferred rationale, weak seams, or ambiguous ownership as `TODO: Confirm` rather than upgrading them to confident design facts.
11. Validate with `bash ../write-technical-design/scripts/validate_technical_design.sh <destination-path>`.
12. Deliver the report as as-built architecture documentation, not as a cleanup proposal.

## Gotchas

- If you document the architecture you wish the repo had, later planning starts from fiction and misses the real constraints. Describe the system that exists today.
- If directory names alone are treated as module boundaries, gray-box documentation looks tidy but collapses under inspection. Require evidence of caller-visible seams, ownership, or boundary tests.
- If inferred rationale is written in the same voice as observed structure, reviewers cannot tell fact from interpretation. Separate the two and use `TODO: Confirm` for weak conclusions.
- If data flow is skipped because the codebase is large, the final document names parts without explaining how the system actually works. Trace the important paths end to end.
- If contradictory evidence between tests, config, and implementation is smoothed over, the report hides the repo's real design risk. Preserve the ambiguity instead of cleaning it up.
- If a derived diagram explains more than the repository proves, readers trust a picture that the evidence cannot support. Keep diagrams anchored to observed behavior and mark weak spots `TODO: Confirm`.
- If an existing report is overwritten without backup, future review loses the history of how understanding changed. Create the timestamped backup first.

## Deliverables

- the chosen technical-design report destination
- a timestamped backup when overwriting an existing report
- as-built architecture, implementation-strategy, and testing-strategy documentation
- the four required diagram slots completed with evidence-backed Mermaid diagrams, `Not needed:` rationales, or `TODO: Confirm`
- validation passing via the shared technical-design validator

## References

- [`references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: deciding whether observed repository seams are strong enough to document as gray-box modules.
- [`references/diagram-evidence.md`](./references/diagram-evidence.md): Read when: filling required diagram slots for a derived technical design without overstating certainty.

## Validation Checklist

- report path is the user-specified destination or the default `docs/research/<project-name>/technical-design.md`
- existing report backup is created before overwrite when needed
- section order follows the `write-technical-design` contract
- named components, interfaces, testing strategy, and risks/tradeoffs are explicit
- all four required diagram slots are present and completed without overstating certainty
- gray-box module claims are tied to concrete repository evidence
- unresolved high-impact details are marked `TODO: Confirm`
- validation passes with the shared script

## Deterministic Validation

- `bash ../write-technical-design/scripts/validate_technical_design.sh <destination-path>`
