# Design rationale

This pack is contract-first because the same artifact shapes must work across authoring, reconstruction, and planning.

## Why the pack is layered

Each layer has one job:

- **foundational** — reusable contracts, templates, validators, naming rules
- **expertise** — one bounded application of those contracts
- **orchestration** — coordination across expertise skills

Every skill still lives under `skills/<skill-name>/` and declares its layer in `metadata.layer`.

This keeps dependencies simple and avoids duplicated contract logic.

## Why shared contracts matter

Authored and reconstructed artifacts should stay compatible when they represent the same artifact type.

That is why both paths reuse the same foundational contracts for charter, user stories, requirements, technical design, execution plans, and task tracking.

If those contracts drift, reconstructed artifacts stop being reliable inputs.

## Why spec-pack root ownership belongs to orchestration

A multi-artifact workflow needs one coordinated root directory so related artifacts stay together.
That directory is workflow context, so it belongs to orchestration.

Examples:

- authored spec-pack root: `.specs/<project-name>/`
- reconstructed spec-pack root: `.specs/<project-name>-research/`

Orchestration may choose or override the spec-pack root for a run, but it should not redefine expertise-owned artifact filenames.

## Why artifact filenames belong to expertise

An expertise skill owns one bounded artifact or bounded analysis output.
That ownership includes the artifact's filename and its expected relationships to sibling artifacts in the same spec pack.

Examples:

- `charter.md`
- `user-stories.md`
- `requirements.md`
- `technical-design.md`
- `execution-plan.md`
- `execution-tasks.md`

When an expertise skill refers to same-pack dependencies, it should describe them with pack-relative paths such as:

- `./charter.md`
- `./user-stories.md`

This keeps artifact identity stable even when a workflow chooses a different spec-pack root.

Expertise may describe local same-pack context, but it should not define canonical `source_artifacts` lineage expectations for the workflow.
Those expectations belong to orchestration because they describe cross-artifact coordination rather than one leaf artifact contract.

## Why `<project-name>` remains foundational

`<project-name>` resolution and normalization are shared naming concerns.
Orchestration should consume that value when selecting a spec-pack root, not reimplement naming logic.

That means orchestration may depend directly on selected foundational leaf contracts when the concern is workflow-wide coordination rather than artifact-specific authoring.
Using `artifact-naming` to resolve one workflow-wide `<project-name>` is valid.
Using foundational write contracts to bypass expertise artifact skills is not.

This keeps basename resolution stable across authoring, reconstruction, and planning workflows.

## Why authoring, reconstruction, and planning stay separate

These workflows start from different sources of truth:

- **authoring** — product intent and approved scope
- **reconstruction** — repository evidence and implemented behavior
- **planning** — approved specification artifacts

If one skill mixes them, it becomes unclear whether an artifact describes intent, reality, or sequencing.

## Why execution coordination is downstream

Execution plans and task tracking are coordination artifacts, not substitutes for requirements or technical design.

Keeping them downstream prevents:

- planning from redefining scope
- task generation from becoming issue-tracker boilerplate
- technical design from collapsing into sequencing notes

## Why execution state is local

Plans and tasks live in the repo so they stay:

- close to the code
- easy to review
- reloadable by agents
- usable without external tooling

## Why this split helps

Separating basename, spec-pack root, and artifact filename ownership:

- preserves narrow layer ownership
- keeps spec packs relocatable
- reduces repeated full-path declarations
- preserves stable artifact filenames
- lets orchestration control workflow placement without taking over artifact identity
