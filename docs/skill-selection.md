# Deciding whether a skill should exist

Use this guide before adding a new skill or splitting an existing one.

## Create a new skill only when needed

Create a new skill only if at least one of these is true:

- a new artifact needs its own stable contract or validator
- a reusable coordination is needed across repositories or parent skills
- an existing skill is doing more than one job and should be split
- a missing layer would make the package less reversible or less composable

Do not create a new skill just to hold:

- project-specific content
- one-off analysis
- logic that belongs in an existing skill

## Pick exactly one layer

Every skill belongs to exactly one layer and lives under `skills/<skill-name>/`.

### Foundational

Use this layer for generic shared contracts, templates, naming, validators, metadata, or provenance mechanics.

Typical examples:

- `artifact-naming`
- `write-charter`
- `write-user-stories`
- `write-requirements`
- `write-technical-design`
- `write-execution-plan`
- `write-task-tracking`
- `write-approval-view`
- `gray-box-modules`

Foundational skills should be reusable leaves. They may own shared naming and normalization such as `<project-name>` resolution, shared metadata shape, validators, templates, and provenance assembly mechanics. They must not own workflow-specific spec-pack roots, specialist-owned filenames, or workflow-level lineage policy.

When writing foundational guidance, describe the capability or trigger rather than routing to another foundational skill by exact name. This keeps foundational skills usable as standalone capability contracts that an LLM can apply selectively during work.

The literal names in the example list above are still appropriate here because this document is classifying package structure, not teaching foundational prose style.

### Specialist

Use this layer when the skill applies foundational contracts within one bounded responsibility.

Typical examples:

- `charter`
- `user-story-authoring`
- `requirements`
- `derive-charter`
- `derive-requirements`
- `technical-design`
- `derive-technical-design`
- `execution-planning`
- `task-generation`

Specialist skills must:

- own one output or one bounded analysis/planning job
- behave like leaves relative to coordination
- depend only on foundational skills
- declare `metadata.archetype` and `metadata.domain`

Specialist skills should own the artifact filename for that output, describe same-pack dependency expectations relative to the spec-pack root when needed, and define the local validation invocation shape when useful.

They should not define:

- workflow-level `source_artifacts` lineage policy
- spec-pack root placement
- `<project-name>`
- root workflow identity

### Coordination

Use this layer when the skill coordinates multiple specialist skills into one larger flow.

Typical examples:

- `specification-authoring`
- `specification-to-execution`
- `specification-reconstruction`

Coordination skills must:

- depend on specialist skills for artifact-producing work
- preserve one end-to-end flow
- avoid restating foundational contract rules
- own workflow-wide coordination such as sequencing, approvals, root workflow provenance, and cross-artifact consistency checks

They may also depend on selected foundational leaf contracts when the concern is workflow-wide coordination rather than artifact-specific authoring. Common cases:

- naming needed to resolve one workflow-wide `<project-name>`
- spec-pack root selection
- provenance assembly support
- approval-view generation and validation support

They must not use foundational dependencies to replace specialist artifact contracts.

## Selection checks

Before creating a skill, confirm that:

- it owns one clear output or coordination outcome
- it does not redefine adjacent artifacts
- it can declare dependencies instead of copying their rules
- it fits exactly one layer
- `metadata.internal: true` is set when the skill is a helper or support dependency that should be hidden from skill installers

## Split signals

Split a skill instead of expanding it when:

- it both defines a reusable contract and performs specialist execution
- it needs dependencies from both foundational and coordination layers
- it tries to own multiple artifact types
- it mixes authoring, reconstruction, and planning sources of truth

## Default bias

When uncertain, prefer:

- foundational reuse over restating rules
- one bounded specialist skill over a multi-purpose skill
- coordination over cross-specialist coupling
- explicit validation
- explicit uncertainty
- composition over duplication
