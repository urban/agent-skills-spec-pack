# Agent Skills for Software Development

This package contains a contract-first skill pack for software specification work.

It provides:

- foundational skills for shared artifact contracts, templates, validators, and naming
- expertise skills that apply those contracts within one authoring, planning, design, or reconstruction responsibility
- orchestration skills that orchestrate multiple expertise skills into a full specification flow

## Package Boundary

`@urban/agent-skills-pack` owns specification artifacts and the workflows that create or reconstruct them.

## Canonical Layout

- `skills/`
  All package skills. Each skill declares its layer in `metadata.layer`.
- `docs/`
  Package guidance for purpose, boundaries, layering, and skill authoring.

Each skill keeps its own `assets/`, `scripts/`, and `references/` directories under `skills/<skill-name>/`.

Dependency direction for the layer model:

- foundational skills do not depend on other skills
- expertise skills may depend only on foundational skills
- orchestration skills may depend only on expertise skills

## Current Skill Inventory

### Foundational

- `artifact-naming`
  Deterministic artifact-name resolution reused across authored and planning artifacts.
- `write-charter`
  Canonical charter artifact contract, template, and validator.
- `write-user-stories`
  Canonical user-story sentence contract.
- `write-requirements`
  Canonical requirements artifact contract, numbering taxonomy, template, and validator.
- `write-technical-design`
  Canonical technical-design artifact contract, template, and validator.
- `write-execution-plan`
  Canonical execution-plan contract, template, and validator.
- `write-task-tracking`
  Canonical task-tracking contract, template, and validator.
- `gray-box-modules`
  Canonical bounded-capability contract for reusable module seams in technical design artifacts.

### Expertise

- `charter`
  Authoring expertise skill for `docs/specs/<project-name>/charter.md`.
- `user-story-authoring`
  Authoring expertise skill for `docs/specs/<project-name>/user-stories.md`.
- `requirements`
  Authoring expertise skill for `docs/specs/<project-name>/requirements.md`.
- `technical-design`
  Design expertise skill for `docs/specs/<project-name>/technical-design.md`.
- `execution-planning`
  Planning expertise skill for `docs/plans/<project-name>-plan.md`.
- `task-generation`
  Planning expertise skill for `docs/tasks/<project-name>-tasks.md`.
- `derive-charter`
  Reconstruction expertise skill for `docs/research/<project-name>/charter.md` by default.
- `derive-user-stories`
  Reconstruction expertise skill for `docs/research/<project-name>/user-stories.md` by default.
- `derive-requirements`
  Reconstruction expertise skill for `docs/research/<project-name>/requirements.md` by default.
- `derive-technical-design`
  Reconstruction expertise skill for `docs/research/<project-name>/technical-design.md` by default.

### Orchestrations

- `specification-authoring`
  Orchestrates `charter -> user-story-authoring -> requirements -> technical-design`.
- `specification-to-execution`
  Orchestrates `execution-planning -> task-generation` from approved specification artifacts.
- `specification-reconstruction`
  Orchestrates `derive-charter -> derive-user-stories -> derive-requirements -> derive-technical-design`.

All listed skills are stored at `skills/<skill-name>/SKILL.md`.

## Layer Model

Each layer has one job:

- foundational
  Define reusable contracts. No required skill dependencies.
- expertise
  Apply one foundational contract set inside one bounded responsibility.
- orchestration
  Coordinate multiple expertise skills without restating foundational rules.

Reversibility depends on authoring and reconstruction expertise skills targeting the same foundational contracts for shared artifact types.

## Artifact Flow

Greenfield path:

```text
idea / feature request
  -> specification-authoring
    -> docs/specs/<project-name>/charter.md
    -> docs/specs/<project-name>/user-stories.md
    -> docs/specs/<project-name>/requirements.md
    -> docs/specs/<project-name>/technical-design.md
      -> specification-to-execution
        -> docs/plans/<project-name>-plan.md
        -> docs/tasks/<project-name>-tasks.md
          -> implementation with Codex
```

Reverse-engineering path:

```text
existing codebase
  -> specification-reconstruction
    -> docs/research/<project-name>/charter.md
    -> docs/research/<project-name>/user-stories.md
    -> docs/research/<project-name>/requirements.md
    -> docs/research/<project-name>/technical-design.md
      -> specification-to-execution or execution-planning
        -> docs/plans/<project-name>-plan.md
        -> docs/tasks/<project-name>-tasks.md
          -> follow-on implementation with Codex
```

Typical greenfield workflow:

1. Use `specification-authoring` to create the authored spec pack.
   Outputs `docs/specs/<project-name>/charter.md`, `docs/specs/<project-name>/user-stories.md`, `docs/specs/<project-name>/requirements.md`, and `docs/specs/<project-name>/technical-design.md`.
   When authored technical design identifies a meaningful bounded capability, express it with the package's foundational `gray-box-modules` contract inside the design artifact.
2. Use `specification-to-execution` when you want an execution plan and local tasks created from the approved spec pack.
3. Use `execution-planning` or `task-generation` directly only when refreshing one downstream artifact instead of the full execution-coordination flow.
4. Implement from the combination of user stories, requirements, technical design, plan, and tasks.

Typical reverse-engineering workflow:

1. Use `specification-reconstruction` against an existing codebase.
   By default it writes `docs/research/<project-name>/charter.md`, `docs/research/<project-name>/user-stories.md`, `docs/research/<project-name>/requirements.md`, and `docs/research/<project-name>/technical-design.md`, but expertise skills may honor explicit user-provided destinations.
   When evidence shows a real bounded capability, let `derive-technical-design` apply the package's foundational `gray-box-modules` contract and mark uncertainty explicitly when the seam is weak.
2. Review the reconstructed charter, user stories, requirements, and technical design.
3. Use `specification-to-execution` if you want the full execution-coordination pack, or `execution-planning` if you only need a fresh plan for follow-on work.
4. Use `task-generation` directly only when an approved execution plan already exists and only local task tracking needs to be refreshed.

## Authoring Guidance

Read these docs when changing the pack:

- [`docs/purpose.md`](./docs/purpose.md)
- [`docs/design-rationale.md`](./docs/design-rationale.md)
- [`docs/development-principles.md`](./docs/development-principles.md)
- [`docs/skill-expertise-selection.md`](./docs/skill-expertise-selection.md)
- [`docs/skill-structure.md`](./docs/skill-structure.md)
- [`docs/composability-checklist.md`](./docs/composability-checklist.md)
- [`docs/progressive-disclosure.md`](./docs/progressive-disclosure.md)

## Recommended Prompts

Examples:

- `Use specification-authoring to define the spec for a new feature in @urban/dotai.`
- `Use specification-to-execution to turn the approved remote-skill-installation spec into an execution plan and local tasks.`
- `Use execution-planning to refresh docs/plans/remote-skill-installation-plan.md from the approved spec pack.`
- `Use task-generation to break docs/plans/remote-skill-installation-plan.md into local tasks.`
- `Use specification-reconstruction to derive the missing spec from this codebase.`
