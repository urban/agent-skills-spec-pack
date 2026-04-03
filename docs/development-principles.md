# Development principles

Use these principles when changing the pack.

## Preserve the layer model

Every skill must fit exactly one layer:

- foundational
- expertise
- orchestration

Store each skill under `skills/<skill-name>/` and declare its layer in `metadata.layer`.

Split mixed responsibilities instead of bending the dependency graph.

## Preserve reversibility

Any new authored artifact should either:

- have a reconstruction path, or
- state clearly why it is author-only

Do not add one-way structure casually.

## Keep contracts stable

Canonical artifact contracts are the center of the pack.

Prefer:

- stable section order
- stable naming
- explicit validation
- explicit uncertainty for reconstructed outputs
- spec-pack-relative artifact contracts over repeated full workflow paths in every expertise skill

Avoid silent drift between create and derive paths.

## Keep boundaries clear

Do not blur these roles:

- foundational skills define shared contracts
- expertise skills own one bounded job
- orchestration skills coordinate expertise skills only

For path and lineage ownership:

- foundational owns `<project-name>` derivation and normalization
- orchestration owns spec-pack root selection and canonical `source_artifacts` lineage expectations
- expertise owns artifact filenames and same-pack dependency guidance

## Keep dependency direction strict

Follow these rules:

- foundational -> no required skill dependencies
- expertise -> foundational only
- orchestration -> expertise required for artifact-producing work; selected foundational leaf contracts allowed only for workflow-wide coordination concerns

Examples of allowed orchestration-level foundational use include:

- naming needed to resolve one workflow-wide `<project-name>`
- spec-pack root selection
- provenance assembly support

Do not use foundational dependencies in orchestration to replace expertise artifact contracts.
Prefer local references over required dependencies for optional follow-on guidance.

## Optimize for agent use

Artifacts should be easy for agents to load and act on.

Prefer:

- deterministic filenames
- canonical provenance and `source_artifacts`
- explicit headings
- concise language
- direct traceability
- relocatable spec packs when workflows need alternate output roots

Do not duplicate `<project-name>` derivation outside foundational naming contracts.
Keep canonical `source_artifacts` lineage expectations in orchestration rather than foundational or expertise skills.

## Prefer explicit uncertainty

Reconstruction skills should mark uncertainty instead of inventing intent.

## Keep responsibilities narrow

Each skill should do one thing well.

## Preserve repository workflow

Changes should preserve:

- easy review in the repo
- clean diffs
- straightforward reuse by agents
