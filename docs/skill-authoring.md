# Skill authoring guide

Use this guide when creating or updating a skill.

## Canonical layout

Every skill lives under:

- `skills/<skill-name>/`

Every skill must include:

- `skills/<skill-name>/SKILL.md`

Add these only when needed:

- `skills/<skill-name>/assets/`
- `skills/<skill-name>/scripts/`
- `skills/<skill-name>/references/`

Use them like this:

| Path | Use for |
| --- | --- |
| `assets/` | templates, regexes, scaffolds |
| `scripts/` | deterministic validators or helpers |
| `references/` | short optional guidance or routing help |

## Required `SKILL.md` frontmatter

Every `SKILL.md` must define:

- `name`
- `description`
- `metadata.layer`

Write `description` as stable routing metadata rather than a mini workflow summary. Follow [`skill-descriptions.md`](./skill-descriptions.md) when creating or revising the one-line description.

Add `metadata.dependencies` when the skill composes other skills or relies on shared contracts.

Use `metadata.internal: true` for helper or support skills that should be hidden from skill installers. Internal skills are not shown in installer selection surfaces, but they can still be installed automatically when another skill depends on them. This flag only affects installer visibility; dependency resolution, packaging, and runtime behavior stay the same.

Specialist skills must also define:

- `metadata.archetype`
- `metadata.domain`

If a skill creates or validates a package artifact, prefer an explicit dependency on `document-traceability` unless a lower-layer contract already handles provenance.

Example:

```yaml
---
name: example-skill
description: One-sentence description of the workflow this skill owns.
metadata:
  layer: foundational
  internal: true
  dependencies:
    - write-requirements
    - artifact-naming
---
```

## Layer rules

Choose exactly one layer:

- **foundational** — reusable leaf contracts, templates, validators, naming, metadata, provenance mechanics
- **specialist** — one bounded leaf skill built on foundational contracts that produces one artifact or bounded analysis/planning output
- **coordination** — workflow-wide coordination across specialist skills

Dependency direction is strict:

- foundational must not depend on other skills
- specialist may depend only on foundational skills
- coordination must depend on specialist skills for artifact-producing work
- coordination may also use selected foundational leaf contracts only for workflow-wide coordination concerns such as naming, spec-pack root selection, or provenance assembly support
- coordination must not use foundational dependencies to replace specialist artifact contracts

## Foundational reference rule

Treat foundational skills as reusable capability contracts, not as prose routers for other foundational skills.

That rule exists for two reasons:

- architectural clarity — foundational skills should stay leaf contracts in both `metadata.dependencies` and instructional prose
- runtime agency — foundational skills should remain directly useful to an LLM or user prompt without requiring package-graph knowledge

When foundational guidance refers to behavior that may also be owned by another foundational skill, describe:

- the capability being used, or
- the trigger for using that capability

Do not write foundational prose as named-skill chaining such as:

- `Use \`visual-diagramming\` when ...`
- `Load \`document-traceability\` to ...`
- `Use the \`artifact-naming\` skill for ...`

Prefer wording like:

- `Use Mermaid diagram-authoring guidance when a diagram explains the system faster than prose.`
- `Validate canonical frontmatter with the shared provenance validator when the workflow stamps provenance.`
- `Apply the shared artifact naming rules when one stable <project-name> is needed.`

This keeps foundational skills useful in three ways at once:

- specialist skills can depend on them as shared contracts
- coordination skills can use them for workflow-wide concerns
- an LLM can apply them selectively during work because the skill explains the capability and its trigger, not just an internal package name

Exact foundational skill names are still allowed where they are part of package structure rather than routing prose, such as:

- frontmatter `name`
- `metadata.dependencies`
- exact file paths
- validator commands
- package inventories and architecture docs

## Framing and context rules

Use these distinctions when writing a skill.

- **framing** = what the skill is responsible for producing, describing, or deciding
- **context** = the upstream artifacts, local files, and evidence the skill reads while doing that job

### Ownership by layer

- **coordination** owns **workflow framing**
  - what workflow is happening
  - what order specialist steps run in
  - what root workflow identity and lineage expectations apply
- **specialist** owns **bounded artifact framing**
  - what one artifact or bounded analysis/planning output is for
  - what source of truth standard applies to it
  - what it must not become
- **foundational** owns shared contracts, templates, validators, naming, and provenance mechanics rather than framing for a specific run

### Why this matters

This distinction protects the layer model.

If framing and context are confused:

- specialist skills start rewriting upstream artifact intent instead of using it as input
- specialist skills start defining workflow-wide lineage or approval logic
- coordination skills start copying artifact contracts instead of routing through specialists
- reconstruction skills start inventing intended scope from weak evidence

The result is drift, weaker reuse, and poorer reversibility.

### Authoring rule of thumb

When writing a specialist skill:

- define the artifact framing it owns
- name the context it may read
- do not let context become reframed ownership

Examples:

- a requirements specialist may use `./charter.md` and `./user-stories.md` as context, but should not re-own charter framing
- a technical-design specialist may use requirements and repo evidence as context, but should not become requirements or execution planning
- a reconstruction specialist may use repo evidence as context, but must keep reconstruction framing instead of inventing approved intent

## Path and filename ownership

Treat location as three separate concerns.

| Concern | Owner | Example |
| --- | --- | --- |
| artifact basename | foundational | `<project-name>` |
| spec-pack root | coordination | `.specs/<project-name>/` |
| artifact filename | specialist | `requirements.md` |

Use that split when writing skill instructions.

### Practical rules

- foundational skills may define naming rules, metadata shape, validators, templates, and provenance assembly mechanics
- coordination skills may choose or override one spec-pack root for a run
- specialist skills should define the filename of the artifact they produce
- when specialist skills refer to sibling artifacts in the same pack, use pack-relative paths such as `./charter.md`
- specialist skills may describe same-pack context and local validation commands, but should not define workflow-level lineage policy or hardcode root workflow identity
- validators may operate on fully resolved runtime paths, but the skill contract should describe pack-local placement when that is the real contract
- when describing specialist inputs, label upstream artifacts as context unless the specialist truly owns that framing
- when describing coordination behavior, keep workflow framing at coordination rather than leaking it into child specialist rules

## Description writing

Treat the `description` field as the stable identity of the skill.

It should make the skill easy to select at runtime without requiring the reader to know the whole package graph.

Prefer descriptions that state:

- what the skill owns
- what source of truth or framing it works from when that matters
- when to use it

Avoid putting these in the one-line description:

- exact child routing or workflow order
- current dependency composition
- validator or template names
- optional helper guidance
- full current consumer lists unless that boundary is intrinsic to the skill

Use the layer-specific rules and examples in [`skill-descriptions.md`](./skill-descriptions.md) as the canonical guide.

## Current `SKILL.md` body shape

The current repo keeps `SKILL.md` files short and runtime-oriented.

Use these defaults:

- keep only runtime-useful guidance in `SKILL.md`
- move long examples, anti-pattern catalogs, and maintenance detail into `references/`, `assets/`, or `scripts/`
- keep local validation explicit
- use runtime-relative paths
- do not restate a dependency's contract when that dependency already owns it
- prefer short bullets over long prose blocks
- keep section intros to one or two sentences

### Default section collapse

When refactoring or cleaning up a heavy `SKILL.md`, prefer this collapse:

- `Rules` + `Constraints` -> one tighter ownership section such as `Contract`, `Boundaries`, or `Workflow rules`
- `Requirements` -> split into `Inputs` plus owned `Output`/`Outputs` or contract bullets
- `Deliverables` -> merge into `Output`/`Outputs`
- `Validation Checklist` + `Deterministic Validation` -> `Validation`
- `Gotchas` -> drop by default; keep only when a small set of failure modes still changes runtime behavior
- long rationale prose -> move to support files only when it still adds value

### Default section stacks by layer

These are defaults, not hard requirements.

| Layer | Default sections |
| --- | --- |
| foundational | `Purpose`, `Contract`, `Inputs`, `Outputs`, `Workflow`, `Validation`, optional `References` |
| specialist | `Purpose`, `Boundaries`, `Inputs`, `Output`, `Workflow`, `Validation`, optional `Approval-view focus`, optional `References` |
| coordination | `Purpose`, `Workflow rules`, `Source artifact lineage`, `Inputs`, `Outputs`, `Workflow`, `Approval flow`, `Validation`, optional `References` |

Use `Approval-view focus` only when the artifact family has stable human-review emphasis worth surfacing for the shared approval-view contract.

## Progressive disclosure

Write documentation so an agent can load only what it needs.

Use these layers:

| File | Put this there |
| --- | --- |
| `AGENTS.md` | package-wide invariants, routing, non-negotiable boundaries |
| `SKILL.md` | what the agent must do when that skill is selected |
| `docs/`, `references/`, `assets/`, `scripts/` | optional detail, templates, validators, and deeper maintenance guidance |

### Good defaults

Put this in `AGENTS.md`:

- package-wide rules
- the layer model
- links to the canonical docs

Put this in `SKILL.md`:

- purpose
- workflow
- constraints
- required deliverables
- validation steps
- links to deeper resources when needed

Put this in support files:

- situational detail
- long explanations
- shared maintenance guidance
- templates and validators

### Avoid

- putting every rule in `AGENTS.md`
- turning `SKILL.md` into a maintenance dump
- duplicating the same rule across files
- vague links that do not say when to read them

Give each rule one home, then link to it.

## Writing guidance for humans and agents

Prefer:

- deterministic filenames
- explicit headings
- concise instructions
- direct workflow order
- local validation commands
- explicit uncertainty instead of guessed intent

Avoid:

- vague prose
- hidden assumptions
- repeated copies of the same contract
- path guidance that mixes basename, root, and filename ownership

## Validation checklist for authors

When you add or change a skill:

- verify `SKILL.md` is internally consistent
- verify linked assets, scripts, and references exist
- run any validator scripts you add
- verify emitted artifacts use canonical provenance and the correct `source_artifacts` keys
- keep examples and output paths aligned with package terminology and layer ownership
