# AGENTS.md

## Purpose

This package contains composable skills for a reversible specification system.

All skills live under `skills/` and must declare one layer in `metadata.layer`.

Optimize for:

- reversibility between authored and reconstructed spec packs
- shared artifact contracts in foundational skills
- narrow expertise entry skills
- orchestration separated from expertise and contract logic
- explicit provenance and source-artifact lineage for created artifacts

## Layer rules

Every skill must fit exactly one layer:

- **foundational** — shared contracts, templates, validators, naming, provenance
- **expertise** — one bounded application of foundational contracts within one role or domain
- **orchestration** — coordination across expertise skills only

Dependency direction is strict:

- foundational -> no required skill dependencies
- expertise -> foundational only
- orchestration -> expertise only

If a skill crosses layers, split it.

Expertise skills must define:

- `metadata.archetype`
- `metadata.domain`

## Skill-local files

Keep support files inside the owning skill directory:

- `assets/` — templates and scaffolds
- `scripts/` — deterministic validators or helpers
- `references/` — optional routing or supporting guidance

When writing relative paths inside a skill, use installed runtime layout:

- skill-local paths: `./assets/...`, `./scripts/...`, `./references/...`
- cross-skill paths: `../write-requirements/...`
- never source-relative paths like `../../skills/...`

## Package defaults

Prefer:

- shared contracts over duplicated rules
- composition over duplication
- deterministic filenames and validation
- explicit uncertainty over guessed intent
- local references over optional required dependencies

Do not create a new skill for project-specific content or one-off analysis.

## Read first

Read these before changing skills:

- [`docs/README.md`](./docs/README.md)
- [`docs/purpose.md`](./docs/purpose.md)
- [`docs/provenance.md`](./docs/provenance.md)
- [`docs/design-rationale.md`](./docs/design-rationale.md)
- [`docs/development-principles.md`](./docs/development-principles.md)
- [`docs/skill-structure.md`](./docs/skill-structure.md)

## Read by task

| Task | Read first |
| --- | --- |
| Decide whether to add a skill | [`docs/skill-expertise-selection.md`](./docs/skill-expertise-selection.md) |
| Create or update `SKILL.md` | [`docs/skill-structure.md`](./docs/skill-structure.md) |
| Check reuse and boundaries | [`docs/composability-checklist.md`](./docs/composability-checklist.md) |
| Split guidance across files | [`docs/progressive-disclosure.md`](./docs/progressive-disclosure.md) |
| Check provenance rules | [`docs/provenance.md`](./docs/provenance.md) |
| Check design boundaries | [`docs/design-rationale.md`](./docs/design-rationale.md) |
| Check development rules | [`docs/development-principles.md`](./docs/development-principles.md) |

Use [`docs/skill-structure.md`](./docs/skill-structure.md) as the canonical source for `skills/` layout and skill-local file placement.

## Default bias

When uncertain, prefer:

- foundational reuse over restating rules
- one bounded expertise skill over a multi-purpose skill
- orchestration over cross-expertise coupling
- explicit validation
- explicit uncertainty
- composition over duplication
