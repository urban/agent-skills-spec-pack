---
name: write-requirements
description: Write and validate canonical requirements artifacts. Use when a task creates, derives, reviews, or validates product obligations that must stay stable for downstream design and planning.
metadata:
  version: 0.4.0
  layer: foundational
---

## Rules

- Keep this artifact focused on product obligations and constraints because product framing and success criteria belong in the charter.
- Preserve canonical frontmatter shape and validate created artifacts with the shared provenance validator when the workflow stamps provenance.
- Use deterministic requirement identifiers because design, planning, and review need stable references.
- When canonical user stories are available, use their story IDs in requirement traceability notes so downstream artifacts can link back to one source of truth for story intent.
- Ground functional requirements in canonical user-story behavior, especially `Actor`, `Situation`, `Action`, `Outcome`, and `Observation`, because requirements should formalize approved behavior rather than replace it.
- Keep requirements externally meaningful and testable because vague statements cannot be validated.
- In derived requirements, concrete runtime, framework, protocol, parser, and tooling names are allowed when the implementation hard-wires them and replacing them would change executable behavior, accepted inputs, validation semantics, or operational prerequisites.
- Command aliases, shared flag semantics, accepted source grammars, and explicit validation rules belong in requirements when they are part of the observable contract.
- Mark unresolved high-impact ambiguity as `TODO: Confirm` instead of guessing.
- When deriving from code, describe implemented reality rather than imagined original intent.

## Constraints

- Output must be one Markdown artifact.
- The shared requirements contract does not define workflow-wide `source_artifacts` policy.
- Required sections must appear in canonical order.
- Requirement identifiers must use the shared prefixes:
  - `FR1.x` for Functional Requirements
  - `NFR2.x` for Non-Functional Requirements
  - `TC3.x` for Technical Constraints
  - `DR4.x` for Data Requirements
  - `IR5.x` for Integration Requirements
  - `DEP6.x` for Dependencies
- Do not include goals, non-goals, persona catalogs, success-criterion sections, file paths, code snippets, commit sequencing, or task breakdowns as requirements content.
- Implementation-enforced constraints are allowed when phrased as stable obligations rather than as a code tour.
- If a required section has no confirmed items yet, keep the section and use `TODO: Confirm`.
- Do not copy user stories verbatim into the requirements artifact; translate them into verifiable obligations while preserving behavioral traceability.

## Requirements

A valid requirements artifact must include these sections in this order:

1. `Functional Requirements`
2. `Non-Functional Requirements`
3. `Technical Constraints`
4. `Data Requirements`
5. `Integration Requirements`
6. `Dependencies`
7. `Further Notes`

Minimum content expectations:

- canonical frontmatter shape when provenance is stamped for the workflow
- at least one numbered `FR1.x` requirement
- every functional requirement includes a `Story traceability` note that references one or more `US1.x` story IDs or `TODO: Confirm`
- every requirement is specific enough to verify
- source-backed, execution-relevant implementation constraints appear in the right non-FR sections when they materially shape behavior or operations
- unresolved or weakly supported details use `TODO: Confirm`

Inputs:

- approved product framing, approved stories, repository evidence, or other source material defining the behavior and constraints
- known constraints, integrations, data rules, and dependencies

Output:

- one requirements Markdown artifact that downstream design, planning, and review work can reference directly

## Workflow

1. Draft from [`assets/requirements-template.md`](./assets/requirements-template.md) so canonical ordering stays intact.
2. Start from approved user stories or evidence-backed behavior before adding detailed constraints.
3. Translate each relevant user-story behavior into verifiable obligations:
   - carry forward the story ID so the requirement can point back to the canonical story block
   - `Actor` and `Action` usually shape functional behavior
   - `Situation` often shapes preconditions, triggers, or edge-case obligations
   - `Outcome` clarifies the value-bearing result that the requirement must preserve
   - `Observation` helps make the requirement testable and externally checkable
4. Write numbered functional requirements with `FR1.x` identifiers and include `Story traceability` notes that reference the relevant `US1.x` story IDs.
5. Translate source-backed implementation facts into the correct requirement family instead of forcing everything into `FR` or dropping it as detail.
6. Capture quality expectations, constraints, data rules, integrations, and dependencies with the shared identifier taxonomy.
7. Keep scope framing and success checks in the charter instead of duplicating them here.
8. Replace unresolved high-impact details with `TODO: Confirm` instead of inventing specifics.
9. Validate the finished artifact with [`scripts/validate_requirements.sh`](./scripts/validate_requirements.sh).

## Gotchas

- If requirements merely restate the five-field stories without sharpening them into obligations, the artifact adds format but not precision. Convert behavior into verifiable requirements.
- If requirements ignore `Situation` or `Observation`, edge conditions and verifiability often disappear. Preserve triggers and visible checks where they matter.
- If hard-wired runtime, protocol, parser, or tooling choices are stripped out of derived requirements, the artifact stops matching execution-relevant constraints. Keep them when the code proves they matter.
- If command grammar or aliases are omitted because they feel too technical, the executable interface becomes incomplete. Keep observable contract rules in the right sections.
- If requirements include technical design choices, later architecture work becomes fake because the solution was smuggled in as scope. Keep requirements focused on externally meaningful obligations and constraints.
- If goals, personas, or success criteria are copied into this artifact, the pack drifts into redundancy and later edits split across files. Leave product framing to the charter.
- If numbering is ad hoc, design and plan documents cannot reference requirements stably across revisions. Use the shared prefix taxonomy every time.
- If requirement traceability points to story titles instead of canonical story IDs, downstream references become fragile when titles change. Use `US1.x` IDs whenever stories are available.
- If derived requirements describe what the system probably meant to do, you create a cleaner story than the code actually supports. Document implemented reality and mark weak inferences with `TODO: Confirm`.
- If empty sections are deleted instead of marked unresolved, downstream skills cannot tell whether the category was considered or forgotten. Keep the section and use `TODO: Confirm`.
- If functional requirements are written as tasks or file edits, planning inherits implementation trivia instead of product obligations. State behavior and constraints, not commit steps.
- If workflow lineage rules are embedded here, the foundational contract stops being reusable across authoring and reconstruction. Leave workflow-specific `source_artifacts` policy to coordination.

## Deliverables

- A Markdown requirements artifact with canonical frontmatter shape and section order.
- Deterministic identifiers across all requirement categories.
- Functional requirement traceability that references canonical `US1.x` story IDs when stories are available.
- Explicit functional requirements, non-functional requirements, constraints, integrations, data requirements, and dependencies.
- Clear `TODO: Confirm` markers for unresolved high-impact details.

## Validation Checklist

- Canonical frontmatter passes shared provenance validation when the workflow stamps provenance.
- All required sections exist and are in the correct order.
- At least one `FR1.x` requirement exists.
- Every functional requirement includes a `Story traceability` note with one or more `US1.x` story IDs or `TODO: Confirm`.
- Functional requirements trace to user-story behavior rather than copying story blocks verbatim.
- Concrete runtime, protocol, parser, and tooling constraints are included when source-backed and execution-relevant.
- Command aliases, shared flag semantics, accepted source forms, and explicit validation rules are captured when they affect the executable interface.
- Product framing and success-criterion sections are not mixed into the artifact.
- Architecture-only decomposition and task-level detail are not mixed into the artifact.
- Unknown high-impact details are marked `TODO: Confirm`.

## Deterministic Validation

- `bash scripts/validate_requirements.sh <requirements-file>`
