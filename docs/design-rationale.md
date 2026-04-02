# Design Rationale

The skill pack uses a contract-first layer model because the same artifact shapes need to work across authoring, reconstruction, and downstream planning.

## Why The Pack Is Layered

Each layer has one responsibility:

- foundational skills define reusable contracts, templates, validators, and naming rules
- expertise skills apply those contracts inside one bounded responsibility
- orchestration skills orchestrate multiple expertise skills without restating lower-layer rules

The layers are conceptual. Every skill is stored under `skills/<skill-name>/` and declares its layer in `metadata.layer`.

This keeps dependencies directional and makes the pack easier to extend without duplicating artifact contracts.

## Why Shared Contracts Matter

Authored and reconstructed artifacts should remain structurally compatible whenever they represent the same artifact type.

That is why authored and reconstructed paths route through the same foundational skills whenever they target the same artifact type:

- `write-charter` for authored charter artifacts
- `write-user-stories`
- `write-requirements`
- `write-technical-design`
- `write-execution-plan` when planning is needed after either path
- `write-task-tracking` when plan work is decomposed into local tasks

That constraint keeps the system reversible:

- authored artifacts can guide implementation
- derived artifacts can guide later changes to existing systems
- downstream execution skills can consume either spec-pack variant

If the contracts drift, the reverse path stops being useful because reconstructed artifacts no longer behave like first-class inputs.

## Why Authoring, Reconstruction, And Planning Stay Separate

The workflows serve different sources of truth and should not blur together:

- authoring starts from product intent and approved scope
- reconstruction starts from repository evidence and implemented behavior
- planning starts from approved specification artifacts and produces coordination outputs

If one skill mixes those responsibilities, downstream users cannot tell whether an artifact represents intent, implemented reality, or implementation sequencing.

## Why Execution Coordination Is Downstream

Execution planning and task tracking are downstream coordination artifacts, not substitutes for requirements or technical design.

They stay in this package because they depend on specification artifacts, but they remain expertise-level consumers of foundational contracts instead of becoming their own ad hoc process model.

This separation prevents:

- planning from redefining scope
- task generation from becoming issue-tracker boilerplate
- technical design from collapsing into sequencing notes

## Why Execution State Is Local

The execution coordination pack writes plan and task artifacts into the repository because implementation work needs a local, inspectable coordination surface.

That keeps execution state:

- close to the code
- reviewable in the same workspace
- usable without external issue trackers
- easy for an agent to reload on later turns
