# Skill expertise selection

Use this guide when deciding whether a new skill should exist and which layer it belongs to.

## Create a new skill only when needed

Create a new skill only if at least one of these is true:

- a new artifact needs its own stable contract or validator
- a reusable orchestration is needed across repositories or parent skills
- an existing skill is doing more than one job and should be split
- a missing layer would make the pack less reversible or less composable

Do not create a new skill just to hold:

- project-specific content
- one-off analysis
- logic that belongs in an existing skill

## Choose one layer

Every skill belongs to exactly one layer and lives under `skills/<skill-name>/`.
Declare the layer in `metadata.layer`.

### Foundational

Use this layer for shared contracts, templates, naming, validators, or provenance rules.

Examples:

- `artifact-naming`
- `write-charter`
- `write-user-stories`
- `write-requirements`
- `write-technical-design`
- `write-execution-plan`
- `write-task-tracking`
- `gray-box-modules`

Foundational skills may own shared naming and normalization such as `<project-name>` resolution, but not workflow-specific spec-pack roots.

### Expertise

Use this layer when the skill applies foundational contracts within one bounded responsibility.

Examples:

- `charter`
- `user-story-authoring`
- `requirements`
- `derive-charter`
- `derive-requirements`
- `technical-design`
- `derive-technical-design`
- `execution-planning`
- `task-generation`

Expertise skills must:

- own one output or one bounded analysis/planning job
- depend only on foundational skills
- declare `metadata.archetype` and `metadata.domain`
- keep optional routing guidance in local `references/`

Expertise skills should own the artifact filename for that output and describe same-pack dependency expectations relative to the spec-pack root when appropriate.
Expertise skills should not define workflow-level `source_artifacts` lineage policy.

### Orchestration

Use this layer when the skill coordinates multiple expertise skills into one larger flow.

Examples:

- `specification-authoring`
- `specification-to-execution`
- `specification-reconstruction`

Orchestration skills must:

- depend on expertise skills for artifact-producing work
- preserve one end-to-end flow
- avoid restating foundational contract rules

Orchestration skills may also depend on selected foundational leaf contracts when the concern is workflow-wide coordination rather than artifact-specific authoring.
Examples include:

- naming needed to resolve one workflow-wide `<project-name>`
- spec-pack root selection
- provenance assembly support

Orchestration skills must not use foundational dependencies to replace expertise artifact contracts.
Orchestration skills may own workflow-wide spec-pack root selection, destination overrides for a run, and canonical `source_artifacts` lineage expectations for artifacts in that workflow, but should not redefine expertise-owned artifact filenames.

## Selection checks

Before creating a skill, confirm that:

- it owns one clear output or coordination outcome
- it does not redefine adjacent artifacts
- it can declare dependencies instead of inlining their rules
- it fits exactly one layer

## Split signals

Split a skill instead of expanding it when:

- it both defines a reusable contract and performs expertise execution
- it needs dependencies from both foundational and orchestration layers
- it tries to own multiple artifact types
- it mixes authoring, reconstruction, and planning sources of truth
