# Purpose

`@urban/agent-skills-pack` exists to make software specifications usable in both directions:

- from product intent to implementation
- from an implemented codebase back to reusable specification artifacts

It does that with a layered skill system stored under `skills/`:

- foundational skills
  Shared contracts, naming rules, templates, and validators.
- role skills
  Authoring, reconstruction, and planning entry points that apply those contracts.
- orchestration skills
  Orchestration across multiple role skills.

Each skill declares its layer with `metadata.layer`.

## What The Pack Owns

The pack focuses on the skills needed to create, reconstruct, and operationalize specification artifacts:

- canonical contracts for charter, user stories, requirements, technical design, execution plans, and task tracking
- authoring workflows for new work
- derivation workflows for existing systems
- planning workflows that turn an approved spec pack into implementable work
- orchestration workflows that assemble coherent multi-artifact flows

## Why This Matters

Without stable specification artifacts, an implementation agent has to infer missing product and architecture context from partial inputs. That usually causes:

- scope drift
- architecture drift
- weaker traceability from intent to code
- weaker follow-on work on existing systems

This pack reduces that ambiguity by making artifact contracts explicit, reusable, and machine-friendly across both the authoring and reconstruction paths.
