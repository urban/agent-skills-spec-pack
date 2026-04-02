# Progressive Disclosure

Use progressive disclosure so an agent loads only the guidance needed for the current task.

This package should separate always-on local rules, required workflow instructions, and optional deep detail instead of placing everything in one file.

## Loading Model

Use these layers:

- `AGENTS.md`
  Always-on package rules, pack boundaries, and routing to deeper docs.
- `SKILL.md`
  The required workflow for one skill and the minimum rules needed to execute it correctly.
- `docs/`, `references/`, `assets/`, and `scripts/`
  On-demand support material, templates, validation helpers, and deeper guidance.

All package skills live under `skills/`. Package docs live under `docs/`. Skill-local support files stay under `skills/<skill-name>/`.

## What Stays In AGENTS.md

Keep `AGENTS.md` short and authoritative.

It should hold:

- pack-wide invariants
- non-negotiable boundaries
- the skill-expertise model
- routing to deeper documents

It should not hold every situational authoring rule or every example.

## What Stays In SKILL.md

Keep `SKILL.md` focused on what an agent must do when that skill is triggered.

It should hold:

- purpose
- workflow
- constraints
- required deliverables
- validation checklist
- links to deeper resources when needed

It should not become a dumping ground for every optional explanation, edge case, or reference document.

## What Moves To Supporting Docs

Move detail into `docs/` or `references/` when it is:

- situational rather than always required
- shared by multiple skills
- long enough to distract from the main workflow
- useful mainly during authoring or maintenance rather than execution

Examples:

- expertise-selection guidance
- skill-structure conventions
- composability review criteria
- progressive disclosure rules themselves

## Navigation Rules

When splitting material across files:

- link, do not duplicate
- give each rule one authoritative location
- add explicit routing near the decision point
- use specific link labels so the agent does not guess what to read

Prefer one lightweight routing table over scattered loose links.

## Anti-Patterns

Avoid:

- putting all guidance into `AGENTS.md`
- putting all detail into `SKILL.md`
- duplicating the same rule across `AGENTS.md`, `SKILL.md`, and supporting docs
- linking vaguely without saying when a document should be read
- creating deep reference trees that an agent has to explore blindly

## Practical Rule

When adding new guidance, ask:

1. Must every agent see this before touching any skill in this package?
   If yes, it belongs in `AGENTS.md`.
2. Must every agent running one specific skill see this?
   If yes, it belongs in that skill's `SKILL.md`.
3. Is it optional, situational, shared, or deeper explanation?
   If yes, it belongs in `docs/` or `references/` and should be linked from the right entry point.
