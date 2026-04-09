# Agent Skills Spec Pack

`agent-skills-spec-pack` is a contract-first skill pack for software specification work.

It supports both directions:

- from product intent to implementation
- from an existing codebase back to reusable specification artifacts

The package is designed to be legible to both humans and agents. Each skill has a narrow job, artifact contracts stay stable, and provenance is part of the output rather than an afterthought.

## What this pack covers

The pack owns the artifacts and workflows around:

- charter
- user stories
- requirements
- technical design
- execution plan
- task tracking

Those artifacts appear in three kinds of workflows:

- **authoring** — define a spec from product intent
- **reconstruction** — derive a spec from an existing codebase
- **planning** — turn approved spec artifacts into execution artifacts

## The layer model

Every skill belongs to exactly one layer and declares it in `metadata.layer`.

| Layer | Purpose | Typical ownership |
| --- | --- | --- |
| **foundational** | shared reusable contracts | templates, validators, naming, provenance, shared artifact rules |
| **specialist** | one bounded artifact or analysis/planning job | writing one artifact, deriving one artifact, producing one bounded output |
| **coordination** | workflow-wide coordination | sequencing specialist skills, approvals, workflow defaults, lineage expectations |

### Dependency rules

Dependency direction is strict:

- foundational -> no required skill dependencies
- specialist -> foundational only
- coordination -> specialist only for artifact-producing work

Coordination may also use selected foundational leaf contracts for workflow-wide concerns such as naming, spec-pack root selection, or provenance assembly support.

## Ownership model

The package keeps naming, placement, and artifact identity separate.

| Concern | Example | Owner |
| --- | --- | --- |
| artifact basename | `<project-name>` | foundational |
| spec-pack root | `.specs/<project-name>/` | coordination |
| artifact filename | `requirements.md` | specialist |

This keeps artifact filenames stable while still allowing different workflows to choose different output roots.

## Why this exists

Without stable contracts, agents infer too much from prompts and repository clues. That usually leads to:

- scope drift
- architecture drift
- weak traceability
- weaker follow-on work

This pack reduces that drift by making structure, provenance, and lineage explicit.

## Repository layout

- `skills/` — all package skills
- `docs/` — package documentation for maintainers and contributors

Each skill lives at:

- `skills/<skill-name>/SKILL.md`

A skill may also include:

- `assets/` — templates and scaffolds
- `scripts/` — validators and helpers
- `references/` — optional supporting guidance

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

### Specialist

- `charter` — writes `charter.md`
- `user-story-authoring` — writes `user-stories.md`
- `requirements` — writes `requirements.md`
- `technical-design` — writes `technical-design.md`
- `execution-planning` — writes `execution-plan.md`
- `task-generation` — writes `execution-tasks.md`
- `derive-charter` — reconstructs `charter.md`
- `derive-user-stories` — reconstructs `user-stories.md`
- `derive-requirements` — reconstructs `requirements.md`
- `derive-technical-design` — reconstructs `technical-design.md`

By default, authored artifacts live under `.specs/<project-name>/` and reconstructed artifacts live under `.specs/<project-name>-reconstructed/`.

### Coordination

- `specification-authoring` — `charter -> user-story-authoring -> requirements -> technical-design`
- `specification-to-execution` — `execution-planning -> task-generation`
- `specification-reconstruction` — `derive-charter -> derive-user-stories -> derive-requirements -> derive-technical-design`

## Typical artifact flows

### Greenfield authoring flow

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

### Reconstruction flow

```text
existing codebase
  -> specification-reconstruction
    -> .specs/<project-name>-reconstructed/charter.md
    -> .specs/<project-name>-reconstructed/user-stories.md
    -> .specs/<project-name>-reconstructed/requirements.md
    -> .specs/<project-name>-reconstructed/technical-design.md
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

Typical lineage shape:

- charter -> `{}`
- user stories -> `charter`
- requirements -> `charter`, `user_stories`
- technical design -> `charter`, `user_stories`, `requirements`
- execution plan -> `charter`, `user_stories`, `requirements`, `technical_design`
- execution tasks -> `plan`

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

## Maintainer docs

Start with:

- [`docs/README.md`](./docs/README.md)
- [`docs/system-overview.md`](./docs/system-overview.md)
- [`docs/provenance.md`](./docs/provenance.md)
- [`docs/skill-authoring.md`](./docs/skill-authoring.md)
- [`docs/skill-selection.md`](./docs/skill-selection.md)
- [`docs/review-checklist.md`](./docs/review-checklist.md)

## Example prompts

- `Use specification-authoring to define the spec for a new feature in @urban/dotai.`
- `Use specification-to-execution to turn the approved remote-skill-installation spec into an execution plan and local tasks.`
- `Use execution-planning to refresh .specs/remote-skill-installation/execution-plan.md from the approved spec pack.`
- `Use task-generation to break .specs/remote-skill-installation/execution-plan.md into local tasks.`
- `Use specification-reconstruction to derive the missing spec from this codebase.`
