# Skill structure

Use this guide when creating or updating a skill.

## Canonical layout

Every skill lives under:

- `skills/<skill-name>/`

Each skill must include:

- `skills/<skill-name>/SKILL.md`

Add these only when needed:

- `skills/<skill-name>/assets/`
- `skills/<skill-name>/scripts/`
- `skills/<skill-name>/references/`

Use them like this:

- `assets/` — templates, regexes, scaffolds
- `scripts/` — deterministic validators or helpers
- `references/` — short optional guidance

## Required frontmatter

Every `SKILL.md` must define:

- `name`
- `description`
- `metadata.layer`

Add `metadata.dependencies` when the skill composes other skills or relies on shared contracts.

Expertise skills must also define:

- `metadata.archetype`
- `metadata.domain`

If a skill creates or validates a package artifact, prefer an explicit dependency on `document-traceability` unless a lower-layer skill handles provenance.

Example:

```yaml
---
name: example-skill
description: One-sentence description of the workflow this skill owns.
metadata:
  layer: foundational
  dependencies:
    - write-requirements
    - artifact-naming
---
```

## Layer rules

Choose exactly one layer:

- **foundational** — reusable contracts, templates, validators, naming, provenance
- **expertise** — one bounded skill built on foundational contracts
- **orchestration** — a coordinating skill built on expertise skills and, when needed, selected foundational leaf contracts for workflow-wide coordination

Dependency direction is strict:

- foundational must not depend on other skills
- expertise may depend only on foundational skills
- orchestration must depend on expertise skills for artifact-producing work
- orchestration may also depend on selected foundational leaf contracts only when they serve workflow-wide coordination concerns such as naming, spec-pack root selection, or provenance assembly support
- orchestration must not use foundational dependencies to replace expertise artifact contracts

## Path ownership

Treat artifact location as three separate concerns:

- **artifact basename** — `<project-name>`
  Owned by foundational naming contracts.
- **spec-pack root** — workflow-level artifact directory such as `.specs/<project-name>/` or `.specs/<project-name>-research/`
  Owned by orchestration.
- **artifact filename** — artifact-specific file such as `charter.md` or `requirements.md`
  Owned by expertise.

Apply these rules:

- foundational skills may define naming and normalization rules for `<project-name>`, but not workflow-specific spec-pack roots
- orchestration skills may choose or override one spec-pack root for a run, but should not redefine expertise-owned artifact filenames
- orchestration skills own canonical `source_artifacts` lineage expectations for artifacts in their workflow
- expertise skills should define the filename of the artifact they produce
- when expertise skills refer to sibling artifacts in the same spec pack, they should use pack-relative paths such as `./charter.md`
- expertise skills may describe same-pack context, but should not define workflow-level lineage policy
- validators may still operate on fully resolved runtime paths, but the skill contract should describe pack-local placement when appropriate

Use this split when writing or revising path guidance in `SKILL.md` files.
Prefer filename and pack-relative dependency guidance in expertise skills over repeating full workflow paths in every expertise contract.

## Validation checklist

When you add or change a skill:

- verify `SKILL.md` is internally consistent
- verify linked assets, scripts, and references exist
- run any validator scripts you add
- verify emitted artifacts use canonical provenance and the correct `source_artifacts` roles
- keep examples and output paths aligned with package terminology and layer ownership
