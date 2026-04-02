# AGENTS.md

## Purpose

This package contains composable skills for a reversible specification system.

All skills in this package live under `skills/`. Use `metadata.layer` to declare whether a skill is foundational, expertise, or orchestration.

Optimize for these outcomes:

- preserve reversibility between authored and derived/reconstructed spec packs
- keep shared artifact contracts in foundational skills
- keep expertise entry skills narrow and single-purpose
- keep orchestration separate from expertise and contract logic

## Layer Rules

New or changed skills must fit exactly one layer:

- foundational skills define reusable contracts, templates, validators, or naming rules
- expertise skills apply foundational contracts within one role or domain boundary
- orchestration skills orchestrate multiple expertise skills to complete a larger flow

Dependency direction is strict:

- foundational -> no required skill dependencies
- expertise -> foundational only
- orchestrations -> expertise only

If a proposed skill crosses layers, split it before adding or moving it.

Expertise skills must define:

- `metadata.archetype`
- `metadata.domain`

Use expertise-local `references/` for situational routing guidance.

Skill-local support files stay inside the owning skill directory:

- `assets/` for templates or scaffolds used directly by the skill
- `scripts/` for deterministic validators or helpers
- `references/` for on-demand supporting docs

When writing relative paths inside a skill, treat the installed skills directory as the runtime layout:

- keep skill-local references relative to the skill itself, like `./assets/...`, `./scripts/...`, and `./references/...`
- write cross-skill references as sibling-skill paths in the flat installed directory, like `../write-requirements/...`
- do not write cross-skill paths relative to the source, like `../../skills/...`

Prefer:

- shared contracts over duplicated rules
- composition over duplication
- deterministic filenames and validation
- explicit uncertainty instead of guessed intent

Do not create a new skill just to hold project-specific content or one-off analysis.

## Read First

Read these package docs before changing skills:

- [`docs/purpose.md`](./docs/purpose.md)
- [`docs/design-rationale.md`](./docs/design-rationale.md)
- [`docs/development-principles.md`](./docs/development-principles.md)
- [`docs/skill-structure.md`](./docs/skill-structure.md)

## Skill Authoring Routes

Load only what matches the current task:

| Task                                  | Read first                                                             |
| ------------------------------------- | ---------------------------------------------------------------------- |
| Decide whether to add a new skill     | [`docs/skill-expertise-selection.md`](./docs/skill-expertise-selection.md)       |
| Create or update `SKILL.md` structure | [`docs/skill-structure.md`](./docs/skill-structure.md)                 |
| Preserve composability and reuse      | [`docs/composability-checklist.md`](./docs/composability-checklist.md) |
| Split guidance across files well      | [`docs/progressive-disclosure.md`](./docs/progressive-disclosure.md)   |
| Check design boundaries               | [`docs/design-rationale.md`](./docs/design-rationale.md)               |
| Check development rules               | [`docs/development-principles.md`](./docs/development-principles.md)   |

Use [`docs/skill-structure.md`](./docs/skill-structure.md) for the canonical `skills/` layout and skill-local file placement rules.

## Default Bias

When uncertain, prefer:

- foundational reuse over restating rules
- one bounded expertise skill over a multi-purpose layer entry
- orchestration over cross-expertise coupling
- explicit validation
- explicit uncertainty
- composition over duplication
