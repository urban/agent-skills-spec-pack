# System overview

`agent-skills-spec-pack` exists to make software specification artifacts usable in both directions:

- from product intent to implementation
- from an implemented system back to reusable specification artifacts

The package is contract-first. It tries to make the structure, lineage, and boundaries of each artifact explicit so later work does not depend on guesswork.

## What the pack owns

The pack covers skills for these artifact types and adjacent workflow steps:

- charter
- user stories
- requirements
- technical design
- execution plan
- task tracking

Those artifacts may be created in different workflows:

- **authoring** — starting from product intent and approved scope
- **reconstruction** — starting from repository evidence and implemented behavior
- **planning** — starting from approved specification artifacts

## The layer model

Every skill belongs to exactly one layer.

For a visual explanation with concrete examples from `write-technical-design`, `technical-design`, `derive-technical-design`, `specification-authoring`, and `specification-reconstruction`, read [layer-hierarchy.md](./layer-hierarchy.md).

| Layer | Owns | Must not own |
| --- | --- | --- |
| **foundational** | shared contracts, templates, validators, naming, metadata shape, provenance mechanics | workflow framing, artifact-specific filenames, parent workflow identity |
| **specialist** | one bounded artifact or one bounded analysis/planning output | workflow-wide coordination, spec-pack root ownership, canonical lineage policy for the full workflow |
| **coordination** | sequencing, workflow-wide defaults, root workflow identity, cross-artifact consistency, canonical lineage expectations | reusable leaf artifact contracts |

This split is strict because the same artifact contracts must survive across authoring, reconstruction, and planning.

## Framing versus context

Use these terms deliberately.

- **framing** means what a skill is responsible for describing or producing
- **context** means the upstream artifacts, local files, and evidence a skill uses while doing that job

This distinction matters because the pack separates workflow meaning from bounded artifact work.

### Who owns framing

- **coordination** owns **workflow framing**
  - what workflow is happening
  - what sequence of specialist steps applies
  - what the root workflow identity is
  - what lineage expectations apply across the workflow
- **specialist** owns **bounded artifact framing**
  - what one artifact or bounded analysis/planning output is for
  - what truth standard applies to that output
  - what it must not become
- **foundational** owns shared contracts and validation mechanics, not framing for a specific run

### How specialist skills use context

Specialist skills may use context such as:

- sibling artifacts like `./charter.md` or `./requirements.md`
- repository code, tests, and configuration
- approved upstream constraints or decisions

But using context does not transfer ownership of framing.

A specialist may read charter context without re-owning charter framing. It may read requirements context without re-owning requirements framing. It may read repository evidence without changing from authored work into reconstruction.

### Why this distinction exists

Without this distinction, skills start to absorb each other's responsibilities.

Typical failures:

- a specialist reads upstream artifacts as context, then rewrites their framing inside a downstream artifact
- a specialist starts defining workflow-wide lineage or approval rules because it sees the larger workflow around it
- a coordination skill starts restating artifact contracts instead of routing through specialists
- a reconstruction specialist turns evidence into imagined product intent instead of implemented reality

When that happens, artifacts drift, workflow boundaries blur, and reversibility weakens.

### Practical rule

- coordination defines **what workflow the run is in**
- specialist defines **what this one output is for**
- specialist consumes **context** from upstream artifacts and local evidence
- foundational defines **shared structure and validation**, not run-specific framing

## Dependency rules

Dependency direction is strict:

- **foundational** -> no required skill dependencies
- **specialist** -> foundational only
- **coordination** -> specialist only for artifact-producing work

Coordination may also use selected foundational leaf contracts when the concern is truly workflow-wide, such as:

- `<project-name>` resolution
- spec-pack root selection
- provenance assembly support

Coordination must not use foundational dependencies to bypass specialist artifact skills.

This leaf model also applies to prose, not just metadata.

Foundational skills should describe reusable capabilities and the triggers for using them, rather than routing to other foundational skills by exact package name. That keeps the architecture clean and also keeps foundational skills directly usable by an LLM or a human prompt without requiring package-graph knowledge.

In practice:

- foundational guidance should say what capability to apply and when
- specialist and coordination skills may still compose other skills by exact name when explicit package composition is the point
- exact foundational skill names are still appropriate in inventories, frontmatter, dependencies, file paths, and validator commands

## Ownership model for paths and names

Treat artifact location as three separate concerns.

| Concern | Example | Owner |
| --- | --- | --- |
| artifact basename | `<project-name>` | foundational |
| spec-pack root | `.specs/<project-name>/` or `.specs/<project-name>-reconstructed/` | coordination |
| artifact filename | `charter.md`, `requirements.md` | specialist |

This split keeps filenames stable while letting workflows choose different output roots.

### What each layer does with paths

- **foundational** may define naming and normalization rules for `<project-name>` and shared validation behavior
- **coordination** may choose or override the spec-pack root for one run
- **specialist** should define the filename of the artifact it produces and describe same-pack dependencies with pack-relative paths such as `./charter.md`

Specialist may describe local same-pack context, but it should not define workflow-level `source_artifacts` policy or hardcode the root workflow identity.

## Why the boundaries are strict

The package becomes less reliable when a skill tries to do more than one layer's job.

Typical failure modes:

- a foundational skill starts encoding workflow placement rules
- a specialist skill starts defining cross-workflow lineage policy
- a coordination skill starts copying the rules of a shared artifact contract
- a single skill mixes authoring, reconstruction, and planning into one vague flow

When that happens, artifacts drift, reuse drops, and reversibility weakens.

## Reversibility

Reversibility means the package can support both authored and reconstructed versions of the same artifact type without changing the contract.

That requires:

- stable naming
- stable section structure
- explicit provenance
- explicit uncertainty when reconstruction evidence is weak
- shared foundational contracts for artifact types that appear in multiple workflows

Do not add one-way structure casually. If a new authored artifact has no reconstruction path, say so clearly.

## Workflow boundaries

Keep these sources of truth separate:

- **authoring** describes intended scope and approved direction
- **reconstruction** describes implemented reality and evidence from the repo
- **planning** describes sequencing and execution coordination

Do not blur them. A plan is not a requirement. A requirement is not a design. A reconstruction should not invent intent.

This is also a framing rule:

- coordination owns the workflow framing that says whether the run is authoring, reconstruction, or planning
- specialist skills must keep their artifact framing inside that workflow instead of drifting into adjacent sources of truth
- upstream artifacts may be used as context, but their framing must not be re-owned downstream

## Why execution artifacts stay downstream and local

Execution plans and task tracking are coordination artifacts. They should stay downstream from requirements and technical design.

Keeping execution state in the repo makes it:

- easy to review
- easy for agents to reload
- usable without external tooling
- close to the code it coordinates

## Package defaults

When uncertain, prefer:

- shared contracts over duplicated rules
- composition over duplication
- explicit validation
- explicit uncertainty over guessed intent
- local references over optional required dependencies
- one bounded specialist skill over a multi-purpose skill
- coordination over cross-specialist coupling

These defaults keep the package predictable for both humans and agents.
