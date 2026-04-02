# Skill Structure

Use this document when creating or updating a skill directory in this package.

## Required Layout

The canonical package layout is:

- `skills/<skill-name>/`

Every package skill lives under `skills/`. Use `metadata.layer` to declare whether it is foundational, role, or orchestration.

Choose one layer only:

- foundational for reusable contracts, templates, validators, and naming rules
- role for one role-specific entry skill that applies foundational contracts
- orchestration for a coordinating skill that depends on role skills only

Each skill lives in its own directory:

- `skills/<skill-name>/SKILL.md`

Add these only when needed:

- `skills/<skill-name>/assets/`
- `skills/<skill-name>/scripts/`
- `skills/<skill-name>/references/`

Use:

- `assets/` for templates, regexes, or scaffolds the skill directly uses
- `scripts/` for deterministic validators or helper scripts
- `references/` for short guidance docs the skill should consult on demand

## Required Frontmatter

Every `SKILL.md` must define:

- `name`
- `description`
- `metadata.layer`

Add `metadata.dependencies` when the skill composes other skills or relies on shared contracts.

Add `metadata.archetype` and `metadata.domain` only for role skills.

Example:

```yaml
---
name: example-skill
description: One-sentence description of the reusable workflow this skill owns.
metadata:
  layer: foundational
  dependencies:
    - write-requirements
    - artifact-naming
---
```

## Dependency Direction Rules

- foundational skills must not depend on other skills
- role skills may depend only on foundational skills
- orchestration skills may depend only on role skills

## Validation Expectations

If you add or change a skill:

- verify the `SKILL.md` is internally consistent
- verify every linked asset, script, or reference path exists
- run any deterministic validator scripts you introduce
- keep examples and output paths aligned with package terminology
