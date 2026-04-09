# Documentation map

This directory explains how `agent-skills-spec-pack` is organized, what it guarantees, and how to change it safely.

## Start here

Read these in order if you are new to the package:

1. [system-overview.md](./system-overview.md) — what the pack owns, how the layer model works, why the boundaries are strict, and how framing differs from context across layers
2. [layer-hierarchy.md](./layer-hierarchy.md) — a visual explanation of the 3-layer hierarchy with concrete examples from `technical-design`, `derive-technical-design`, and `write-technical-design`
3. [provenance.md](./provenance.md) — the canonical frontmatter contract, lineage rules, and validation flow
4. [skill-authoring.md](./skill-authoring.md) — how to structure a skill, where files go, and how framing and context should be described in skill guidance
5. [skill-descriptions.md](./skill-descriptions.md) — how to write stable `description` fields that remain useful as workflows and dependencies evolve

## Read by task

| Task | Read |
| --- | --- |
| Decide whether a new skill should exist | [skill-selection.md](./skill-selection.md) |
| Create or update `skills/<skill-name>/SKILL.md` | [skill-authoring.md](./skill-authoring.md), [skill-descriptions.md](./skill-descriptions.md) |
| Understand layer ownership, dependency direction, and concrete hierarchy examples | [system-overview.md](./system-overview.md), [layer-hierarchy.md](./layer-hierarchy.md) |
| Check provenance, lineage, and frontmatter | [provenance.md](./provenance.md) |
| Review a skill before shipping it | [review-checklist.md](./review-checklist.md) |

## Core rules

These rules appear throughout the docs. Keep them stable.

- All skills live under `skills/`.
- Every skill declares exactly one layer in `metadata.layer`.
- Layers are strict:
  - **foundational** — shared contracts, templates, validators, naming, provenance mechanics
  - **specialist** — one bounded artifact or bounded analysis/planning job built on foundational contracts
  - **coordination** — workflow-wide coordination across specialist skills
- Dependency direction is strict:
  - foundational -> no required skill dependencies
  - specialist -> foundational only
  - coordination -> specialist only for artifact-producing work, with selected foundational leaf contracts allowed only for workflow-wide coordination concerns
- Provenance and `source_artifacts` are part of the artifact contract.
- Authored and reconstructed artifacts should use the same contract when they represent the same artifact type.

## Design goal

The package should be understandable in two ways at once:

- a human maintainer can see what each skill owns and why
- an agent can load the smallest set of rules needed to do the job correctly

## Brief usage stories

### Human maintainer

A human uses `agent-skills-spec-pack` to understand what skills exist, what each one owns, how they compose, and how to change the package without breaking reversibility, provenance, or layer boundaries.

Typical goals:

- decide whether to add a new skill or split an existing one
- update a `SKILL.md` file without drifting from the layer model
- review whether a workflow still preserves canonical artifact contracts
- trace why an emitted artifact has the structure, provenance, and lineage it does

### LLM or coding agent

An LLM uses `agent-skills-spec-pack` as selective runtime guidance. It should be able to load only the package-wide rules and the small set of skills needed for the current task, then apply those contracts directly while producing or validating artifacts.

Typical goals:

- choose the right coordination, specialist, or foundational skill for the task
- apply foundational capabilities selectively during work without needing the full package graph
- produce artifacts that stay compatible with shared templates, validators, and provenance rules
- reconstruct or author specification artifacts while keeping framing, context, and lineage boundaries intact
