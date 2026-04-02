---
name: derive-requirements
description: Reconstruct software requirements artifacts from repository code and tests. Use when a user wants implemented product behavior documented as requirements for an existing project.
metadata:
  version: 0.1.0
  layer: expertise
  archetype: research
  domain: specification-reconstruction
  dependencies:
    - write-requirements
---

## Rules

- Treat repository code and tests as the primary evidence because this role documents implemented reality, not remembered intent.
- Use the `write-requirements` contract so the derived artifact stays compatible with authored requirements.
- Prefer user-visible behavior and explicit constraints over internal plumbing because the output is still a requirements artifact.
- Keep evidence traceable to concrete file paths and line references when support is thin or disputed.
- Use `TODO: Confirm` when the repository cannot prove the actor, rationale, or intended scope boundary.

## Constraints

- Output must be one Markdown report at the user-specified destination or, by default, `docs/research/<project-name>/requirements.md`.
- The artifact must stay compatible with the `write-requirements` contract.
- If the destination file already exists, create a timestamped backup before overwrite.
- Do not claim original product framing that is not supported by repository evidence.
- Do not turn technical plumbing into fake user-facing requirements just to fill sections.

## Requirements

Inputs:

- repository source code
- repository tests when present
- optional user-provided scope paths
- optional user-provided output destination

Output:

- one derived requirements report at the user-specified destination or, when no destination is provided, `docs/research/<project-name>/requirements.md`

In scope:

- reconstructing implemented requirements, constraints, and dependencies
- preserving explicit uncertainty where business rationale cannot be proved
- backing up an existing report before overwrite

Out of scope:

- reconstructing unsupported goals, non-goals, personas, or success criteria as facts
- rewriting the system to match cleaner imagined intent
- producing technical design or execution tasks
- using commit history, PR text, or external docs as primary evidence

## Workflow

1. Confirm analysis scope, defaulting to the full repository when the user does not narrow it.
2. Inventory user-visible behaviors, interfaces, constraints, and dependencies from code and tests.
3. Infer missing rationale only as far as the evidence supports and mark weak points as `TODO: Confirm`.
4. Resolve the destination path from user input when provided; otherwise resolve `<project-name>` from the nearest package or repository name and use `docs/research/<project-name>/requirements.md`.
5. If the destination report already exists, create a timestamped backup in the same directory before overwrite.
6. Draft the chosen destination with the `write-requirements` contract.
7. Add evidence-aware `TODO: Confirm` markers anywhere actor intent, benefit, or scope rationale remains unprovable.
8. Validate with `bash ../write-requirements/scripts/validate_requirements.sh <destination-path>`.
9. Deliver the report as reconstructed implemented requirements, not as speculative product history.

## Gotchas

- If you describe what the product probably meant to do instead of what the code proves, the report becomes cleaner than reality and misleads future design work. Stay anchored to implemented behavior.
- If every internal subsystem gets promoted into a requirement, the artifact turns into a technical inventory instead of a product contract. Keep the report user-visible unless a constraint clearly belongs in requirements.
- If weak evidence is omitted entirely, reviewers read silence as certainty. Keep ambiguous items and mark them `TODO: Confirm`.
- If you overwrite an existing research report without a backup, later reviewers lose the ability to compare interpretations across passes. Create the timestamped backup first.
- If tests contradict code paths and you smooth over the mismatch, the artifact hides the most important uncertainty in the repo. Record the implemented evidence and note the ambiguity explicitly.
- If file and line evidence is not traceable, disagreements collapse into opinion instead of inspection. Keep support concrete when confidence is not obvious.

## Deliverables

- the chosen requirements report destination
- a timestamped backup when overwriting an existing report
- evidence-based reconstructed requirements with explicit uncertainty handling
- validation passing via the shared requirements validator

## Validation Checklist

- report path is the user-specified destination or the default `docs/research/<project-name>/requirements.md`
- existing report backup is created before overwrite when needed
- section order and numbering follow the `write-requirements` contract
- requirements describe implemented behavior rather than guessed original intent
- unresolved high-impact details are marked `TODO: Confirm`
- validation passes with the shared script

## Deterministic Validation

- `bash ../write-requirements/scripts/validate_requirements.sh <destination-path>`
