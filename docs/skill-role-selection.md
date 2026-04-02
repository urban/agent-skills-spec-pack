# Skill Role Selection

Use this document when deciding whether a new skill should exist and which layer it belongs in.

## Create A New Skill Only When Needed

Create a new skill only when at least one of these is true:

- a new artifact needs its own stable contract or validator
- an orchestration skill is reusable across multiple repositories or multiple parent skills
- a current skill is doing more than one job and should be split
- a missing layer prevents the pack from staying reversible or composable

Do not create a new skill just to hold:

- project-specific content
- one-off analysis
- logic that belongs inside an existing skill

## Choose One Layer

Every skill should fit one clear layer.

All skills are stored under `skills/<skill-name>/`. The chosen layer is declared in `metadata.layer`.

### Foundational

Use this layer when the pack needs a shared artifact contract, template, naming rule, or validator.

Examples:

- `artifact-naming`
- `write-charter`
- `write-user-stories`
- `write-requirements`
- `write-technical-design`
- `write-execution-plan`
- `write-task-tracking`
- `gray-box-modules`

### Role

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

Role skills should:

- own one output or one bounded analysis/planning responsibility
- depend only on foundational skills
- declare `metadata.archetype` and `metadata.domain`
- keep optional routing guidance in local `references/`

### Orchestration

Use this layer when the skill coordinates multiple role entry skills into one larger flow.

Examples:

- `specification-authoring`
- `specification-to-execution`
- `specification-reconstruction`

Orchestration skills should:

- depend only on role skills
- preserve one end-to-end flow
- avoid restating foundational contract rules

## Selection Checks

Before creating the skill, confirm:

- it owns one clear output or coordination outcome
- it does not redefine adjacent artifacts
- it can declare its dependencies instead of inlining their rules
- it fits exactly one layer

## Split Signals

Split a skill instead of expanding it when:

- it both defines a reusable contract and performs role-specific execution
- it needs dependencies from both foundational and orchestration layers
- it tries to own multiple artifact types
- it mixes authoring, reconstruction, and planning sources of truth
