# Docs overview

These docs explain what `agent-skills-pack` owns and how to change it safely.

Core rules:

- all skills live under `../skills/`
- every skill declares one layer in `metadata.layer`
- provenance and traceability are part of the artifact contract
- authored and reconstructed artifacts should share the same structure when they represent the same artifact type

## Read first

- [purpose.md](./purpose.md) — scope and goals
- [provenance.md](./provenance.md) — frontmatter, lineage, validation
- [design-rationale.md](./design-rationale.md) — why the layer model is strict
- [development-principles.md](./development-principles.md) — rules for package changes

## Read by task

- [skill-expertise-selection.md](./skill-expertise-selection.md) — decide whether a skill should exist and which layer it belongs to
- [skill-structure.md](./skill-structure.md) — create or update a skill directory and `SKILL.md`
- [composability-checklist.md](./composability-checklist.md) — final review before shipping a skill
- [progressive-disclosure.md](./progressive-disclosure.md) — split guidance across `AGENTS.md`, `SKILL.md`, and support files
