# Agent skills for software development

`agent-skills-pack` is a contract-first skill pack for software specification work.

It supports both directions:

- from product intent to implementation
- from an existing codebase back to reusable specification artifacts

## Package model

The pack has three layers:

- **Foundational** — shared contracts, templates, validators, naming, provenance
- **Expertise** — one bounded authoring, reconstruction, design, or planning job
- **Orchestration** — multi-step flows across expertise skills

Each skill declares its layer in `metadata.layer`.

## Why it exists

Without stable artifacts, agents infer too much from prompts and repository clues. That leads to:

- scope drift
- architecture drift
- weak traceability
- weaker follow-on work

This pack makes artifact structure, provenance, and lineage explicit.

## Package boundary

The package owns specification artifacts and the workflows that create, reconstruct, and operationalize them:

- charter
- user stories
- requirements
- technical design
- execution plan
- task tracking

## Repository layout

- `skills/` — all package skills
- `docs/` — package guidance

Each skill lives at `skills/<skill-name>/SKILL.md` and may also include:

- `assets/` — templates and scaffolds
- `scripts/` — validators and helpers
- `references/` — optional guidance

## Layer rules

Dependency direction is strict:

- foundational -> no required skill dependencies
- expertise -> foundational only
- orchestration -> expertise only

Reversibility depends on authored and reconstructed artifacts sharing the same foundational contracts for the same artifact type.

## Current skill inventory

### Foundational

- `artifact-naming` — deterministic artifact naming
- `document-traceability` — canonical provenance and source-artifact lineage
- `write-charter` — charter contract, template, validator
- `write-user-stories` — user story sentence contract
- `write-requirements` — requirements contract, numbering, template, validator
- `write-technical-design` — technical design contract, template, validator
- `write-execution-plan` — execution plan contract, template, validator
- `write-task-tracking` — task tracking contract, template, validator
- `gray-box-modules` — bounded capability contract for technical design artifacts
- `visual-diagramming` — diagram selection guidance for Mermaid-backed visuals
- `effect-technical-design` — Effect-specific technical design guidance for TypeScript systems

### Expertise

- `charter` — writes `.specs/<project-name>/charter.md`
- `user-story-authoring` — writes `.specs/<project-name>/user-stories.md`
- `requirements` — writes `.specs/<project-name>/requirements.md`
- `technical-design` — writes `.specs/<project-name>/technical-design.md`
- `execution-planning` — writes `.specs/<project-name>/execution-plan.md`
- `task-generation` — writes `.specs/<project-name>/execution-tasks.md`
- `derive-charter` — reconstructs `.specs/<project-name>-research/charter.md` by default
- `derive-user-stories` — reconstructs `.specs/<project-name>-research/user-stories.md` by default
- `derive-requirements` — reconstructs `.specs/<project-name>-research/requirements.md` by default
- `derive-technical-design` — reconstructs `.specs/<project-name>-research/technical-design.md` by default

### Orchestration

- `specification-authoring` — `charter -> user-story-authoring -> requirements -> technical-design`
- `specification-to-execution` — `execution-planning -> task-generation`
- `specification-reconstruction` — `derive-charter -> derive-user-stories -> derive-requirements -> derive-technical-design`

## Artifact flows

### Greenfield

```text
idea / feature request
  -> specification-authoring
    -> .specs/<project-name>/charter.md
    -> .specs/<project-name>/user-stories.md
    -> .specs/<project-name>/requirements.md
    -> .specs/<project-name>/technical-design.md
      -> specification-to-execution
        -> .specs/<project-name>/execution-plan.md
        -> .specs/<project-name>/execution-tasks.md
          -> implementation
```

### Reconstruction

```text
existing codebase
  -> specification-reconstruction
    -> .specs/<project-name>-research/charter.md
    -> .specs/<project-name>-research/user-stories.md
    -> .specs/<project-name>-research/requirements.md
    -> .specs/<project-name>-research/technical-design.md
      -> specification-to-execution or execution-planning
        -> .specs/<project-name>/execution-plan.md
        -> .specs/<project-name>/execution-tasks.md
          -> follow-on implementation
```

## Provenance and traceability

Created artifacts should use the canonical frontmatter from `document-traceability`.

That frontmatter records:

- artifact name
- creation and update timestamps
- root workflow and producing skill
- participating skills in the producing branch
- upstream artifacts used to create the document

Keep these separate:

- `generated_by` — how the artifact was produced
- `source_artifacts` — which inputs shaped it

Typical lineage:

- charter -> `{}`
- user stories -> `charter`
- requirements -> `charter`, `user_stories`
- technical design -> `charter`, `user_stories`, `requirements`
- plan -> `charter`, `user_stories`, `requirements`, `technical_design`
- tasks -> `plan`

See [`docs/provenance.md`](./docs/provenance.md) for the full contract.

## Typical workflows

### Author a new spec pack

1. Run `specification-authoring`.
2. Review the charter, user stories, requirements, and technical design.
3. Run `specification-to-execution` if you want a plan and tasks.
4. Implement from the approved artifacts.

### Reconstruct a spec pack from code

1. Run `specification-reconstruction`.
2. Review the reconstructed artifacts and mark uncertainty where evidence is weak.
3. Run `specification-to-execution` or `execution-planning` for follow-on work.
4. Use `task-generation` only when a plan already exists and tasks need refresh.

## Docs for maintainers

- [`docs/README.md`](./docs/README.md)
- [`docs/purpose.md`](./docs/purpose.md)
- [`docs/provenance.md`](./docs/provenance.md)
- [`docs/design-rationale.md`](./docs/design-rationale.md)
- [`docs/development-principles.md`](./docs/development-principles.md)
- [`docs/skill-expertise-selection.md`](./docs/skill-expertise-selection.md)
- [`docs/skill-structure.md`](./docs/skill-structure.md)
- [`docs/composability-checklist.md`](./docs/composability-checklist.md)
- [`docs/progressive-disclosure.md`](./docs/progressive-disclosure.md)

## Example prompts

- `Use specification-authoring to define the spec for a new feature in @urban/dotai.`
- `Use specification-to-execution to turn the approved remote-skill-installation spec into an execution plan and local tasks.`
- `Use execution-planning to refresh .specs/remote-skill-installation/execution-plan.md from the approved spec pack.`
- `Use task-generation to break .specs/remote-skill-installation/execution-plan.md into local tasks.`
- `Use specification-reconstruction to derive the missing spec from this codebase.`
