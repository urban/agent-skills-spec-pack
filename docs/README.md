# Documentation map

This directory explains how `agent-skills-pack` is organized, what it guarantees, and how to change it safely.

## Start here

Read these in order if you are new to the package:

1. [system-overview.md](./system-overview.md) — what the pack owns, how the layer model works, why the boundaries are strict, and how framing differs from context across layers
2. [provenance.md](./provenance.md) — the canonical frontmatter contract, lineage rules, and validation flow
3. [skill-authoring.md](./skill-authoring.md) — how to structure a skill, where files go, and how framing and context should be described in skill guidance

## Read by task

| Task | Read |
| --- | --- |
| Decide whether a new skill should exist | [skill-selection.md](./skill-selection.md) |
| Create or update `skills/<skill-name>/SKILL.md` | [skill-authoring.md](./skill-authoring.md) |
| Understand layer ownership, workflow framing, and specialist context | [system-overview.md](./system-overview.md) |
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
