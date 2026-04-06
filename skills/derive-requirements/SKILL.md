---
name: derive-requirements
description: Reconstruct requirements artifacts from repository evidence and reconstructed user-visible behavior. Use when a user needs implemented product obligations documented for an existing system.
metadata:
  version: 0.3.0
  layer: specialist
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - reconstruct-implementation-constraints
    - write-requirements
---

## Rules

- Treat repository code and tests as the primary evidence because this role documents implemented reality, not remembered intent.
- Produce the artifact as `requirements.md`.
- Use the `write-requirements` contract so the derived artifact stays compatible with authored requirements.
- Keep functional requirements user-visible and behavior-led.
- Capture code-enforced runtime, validation, parsing, integration, dependency, and operational constraints in non-functional requirements, technical constraints, data requirements, integration requirements, or dependencies when they materially shape execution, accepted inputs, safety behavior, interoperability, or operator-visible output.
- Use `reconstruct-implementation-constraints` to recover source-backed constraints from package manifests, runtime entrypoints, command definitions, schemas, tagged errors, parser logic, config, and tests.
- If a concrete runtime, framework, protocol, parser rule, or tool is hard-wired by the implementation and changing it would change executable behavior or operational prerequisites, record it in the right non-FR category instead of dropping it.
- Keep evidence traceable to concrete file paths and line references when support is thin or disputed.
- Use context from `./charter.md` and `./user-stories.md` when they exist because reconstructed requirements should stay aligned to reconstructed framing and outcomes.
- Use `TODO: Confirm` when the repository cannot prove the actor, rationale, intended scope boundary, or verification expectation.
- Do not define workflow-wide `source_artifacts` lineage policy here.

## Constraints

- Output must be one Markdown artifact named `requirements.md`.
- The artifact must stay compatible with the `write-requirements` contract.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not claim original product framing that is not supported by repository evidence.
- Do not treat runtime or platform dependencies, parser grammar, validation rules, shared flag semantics, or CLI grammar as fake “internal plumbing” when they are part of the executable contract.
- Do not move architecture decomposition into requirements, but do capture implementation-enforced obligations and constraints.
- Derive requirements from the reconstructed five-field user-story contract rather than from old sentence-only story assumptions.

## Requirements

Inputs:

- repository source code
- repository tests when present
- package manifests, runtime entrypoints, command definitions, schemas, parsers, error types, config, and tests when present
- optional user-provided scope paths
- optional user-provided output destination

Output:

- one derived requirements artifact named `requirements.md`

In scope:

- reconstructing implemented requirements, constraints, and dependencies
- reconstructing code-enforced runtime, validation, parsing, integration, and operational constraints
- deriving explicit dependencies from manifests and runtime integrations
- recording operator-visible no-op and failure guarantees when they affect externally checkable behavior
- preserving explicit uncertainty where business rationale cannot be proved
- backing up an existing report before overwrite
- aligning requirements to reconstructed story behavior when `./user-stories.md` is available

Out of scope:

- reconstructing unsupported goals, non-goals, personas, or success criteria as facts
- rewriting the system to match cleaner imagined intent
- producing technical design or execution tasks
- using commit history, PR text, or external docs as primary evidence

## Workflow

1. Confirm the user needs requirements artifacts reconstructed from repository evidence, then confirm analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inventory user-visible behavior from code and tests.
3. Use `reconstruct-implementation-constraints` to inventory source-backed implementation constraints from manifests, entrypoints, command definitions, schemas, parser logic, error types, config, and tests.
4. Classify each recovered fact into the right requirement family:
   - `FR` for user-visible commands, actions, outcomes, aliases, and operator-visible behavior
   - `NFR` for runtime model, logging behavior, ordering guarantees, tolerant versus strict behavior, staging behavior, safety behavior, and other quality constraints
   - `TC` for accepted grammars, shared flag semantics, validation rules, framework constraints, metadata variants, path or layout assumptions, and compatibility rules
   - `DR` for data shape, required metadata, schema variants, parsing strictness, and source-classification rules
   - `IR` for filesystem, network, source archive download, version-control diff, child-process, or other protocol and adapter constraints
   - `DEP` for required runtimes, package managers, version-control tools, network access, packaged assets, or fixed runtime integrations required for operation
5. Use reconstructed stories from `./user-stories.md` when available to preserve behavioral traceability.
6. Infer missing rationale only as far as the evidence supports and mark weak points as `TODO: Confirm`.
7. Resolve the chosen destination path.
8. If the destination artifact already exists, create a timestamped backup in the same directory before overwrite.
9. Draft the artifact with the `write-requirements` contract.
10. Translate reconstructed story behavior into requirements:
   - use `Actor` and `Action` to identify the implemented obligation
   - use `Situation` to capture preconditions and edge conditions supported by the code
   - use `Outcome` to preserve the visible result
   - use `Observation` to preserve how the implemented behavior can be checked
11. Translate implementation-enforced facts into the right non-FR sections instead of forcing them into functional requirements or dropping them as trivia.
12. When a reconstructed `technical-design.md` is available in the same run, compare it against the drafted requirements and backfill missing high-impact `NFR`, `TC`, `DR`, `IR`, or `DEP` items before final delivery.
13. Write `requirements.md` to the chosen destination.
14. Add evidence-aware `TODO: Confirm` markers anywhere actor intent, benefit, scope rationale, or verification framing remains unprovable.
15. Validate with `bash ../write-requirements/scripts/validate_requirements.sh <resolved-requirements-path>`.
16. Deliver the artifact as reconstructed implemented requirements, not as speculative product history.

## Gotchas

- If you describe what the product probably meant to do instead of what the code proves, the report becomes cleaner than reality and misleads future design work. Stay anchored to implemented behavior.
- If package manifests, runtime wiring, or command definitions are ignored, runtime and dependency constraints vanish from the reconstructed contract. Treat them as first-class evidence.
- If tests proving CLI grammar, shared flag placement, no-op output, or failure formatting are ignored, requirements understate the executable contract. Use those tests.
- If implementation constraints are treated as design trivia, the output stops matching source-backed execution behavior. Put them in the right non-FR sections.
- If every internal subsystem gets promoted into a requirement, the artifact turns into a technical inventory instead of a product contract. Keep the report externally meaningful and verifiable.
- If you only reconstruct actions and ignore situations or observations, you lose the implementation's boundary behavior and testability. Preserve those signals when evidence exists.
- If weak evidence is omitted entirely, reviewers read silence as certainty. Keep ambiguous items and mark them `TODO: Confirm`.
- If you overwrite an existing research report without a backup, later reviewers lose the ability to compare interpretations across passes. Create the timestamped backup first.
- If tests contradict code paths and you smooth over the mismatch, the artifact hides the most important uncertainty in the repo. Record the implemented evidence and note the ambiguity explicitly.
- If file and line evidence is not traceable, disagreements collapse into opinion instead of inspection. Keep support concrete when confidence is not obvious.

## Deliverables

- `requirements.md`
- a timestamped backup when overwriting an existing artifact
- evidence-based reconstructed requirements with explicit uncertainty handling
- high-impact implementation constraints captured in the right requirement families
- validation passing via the shared requirements validator

## Validation Checklist

- artifact filename is `requirements.md`
- existing artifact backup is created before overwrite when needed
- section order and numbering follow the `write-requirements` contract
- requirements describe implemented behavior rather than guessed original intent
- requirements stay compatible with reconstructed user-story behavior when user stories are available
- high-impact implementation constraints are captured in non-FR sections when they materially shape execution or operations
- aliases, shared flag semantics, accepted source forms, validation rules, URL grammar, and tool or runtime prerequisites are not dropped when source-backed
- requirements remain externally meaningful and verifiable instead of becoming an architecture tour
- unresolved high-impact details are marked `TODO: Confirm`
- validation passes with the shared script

## Deterministic Validation

- `bash ../write-requirements/scripts/validate_requirements.sh <resolved-requirements-path>`
