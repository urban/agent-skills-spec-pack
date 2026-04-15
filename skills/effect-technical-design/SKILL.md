---
name: effect-technical-design
description: "Define shared Effect-specific technical-design guidance for TypeScript systems. Use when a technical-design task targets an Effect application and needs ownership, boundary, or recomposition guidance."
license: MIT
metadata:
  version: "0.2.2"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own reusable Effect-specific technical-design guidance for TypeScript systems: decomposition, recomposition, abstraction selection, observed-architecture recovery, and current Effect-native example shape. This skill complements the shared technical-design contract; it does not replace it.

## Contract

- Start from owned capabilities, read seams, lifecycle boundaries, and runtime composition points before naming an Effect abstraction.
- Choose the smallest stable abstraction that protects the boundary:
  - helper before schema-backed contract
  - schema-backed contract before read module
  - read module before `Atom`
  - feature module before `Context.Service`
  - `Context.Service` before a wider layer graph
- Treat a read module as a design role: a small read-only module that exposes reusable semantic reads, hides storage and projection details, and does not own write policy, retries, resource lifecycle, or runtime wiring.
- Separate capability ownership from observation ownership; services and layers own infrastructure, while read modules and `Atom` expose reads and feature-facing state.
- Name concrete recomposition sites; avoid vague "just provide the layers" guidance and ad hoc `provide` chains.
- In derived design, document the Effect abstractions actually in use before suggesting alternatives.
- Keep direct Node or Bun APIs, direct child-process calls, direct thrown errors, and other runtime escape hatches explicit when the implementation uses them.
- When examples clarify the design, use current Effect names and practices such as `Context.Service`, `Context.Reference`, `Schema.Struct`, `Schema.TaggedStruct`, `Schema.Union`, `Schema.TaggedErrorClass`, `Effect.gen`, `Effect.fn`, and `Layer.effect` when those are the right fit.
- Do not teach generic Effect syntax here and do not use outdated pre-`Context` aliases.
- Mark weakly supported architectural claims as `TODO: Confirm`.

## Inputs

- approved requirements or repository evidence
- runtime profile: CLI, server, browser, worker, or mixed
- known integrations, persistence model, and UI or reactive state needs
- unresolved boundary questions that need explicit decisions

## Outputs

- Effect-specific decomposition guidance
- Effect-specific recomposition guidance
- abstraction-selection rationale tied to ownership and lifecycle
- observed-architecture notes for derived design
- short current Effect-native examples when they materially clarify a boundary
- `TODO: Confirm` markers for unresolved high-impact seams

## Workflow

1. Confirm the task is for a TypeScript system using Effect.
2. Inspect imports, runtime wiring, and entrypoints before proposing abstractions.
3. Identify the job: decomposition, recomposition, abstraction selection, or derived-architecture recovery.
4. Resolve the key design decisions before finalizing guidance:
   - reactive and background state profile
   - persistence contract shape
   - runtime profile
   - multi-runtime breakdown when relevant
5. Load `./references/decompose-recompose.md` for module and recomposition decisions.
6. Load `./references/abstraction-selection.md` for boundary-level abstraction choice.
7. Load `./references/pattern-notes.md` only when a reusable pattern reminder is needed to support or reject a design choice.
8. For derived design, classify observed abstractions by ownership, lifecycle, caller visibility, recomposition site, and escape hatches.
9. Return guidance in ownership and observed-architecture terms first; add improvement notes only after the current architecture is clear.
10. Use `TODO: Confirm` for unresolved high-impact seams.

## Validation

- Confirm this skill stays foundational and does not own the final artifact contract.
- Confirm guidance is framed in ownership, lifecycle, and recomposition terms.
- Confirm derived guidance names the abstractions actually in use when the repository shows them.
- Confirm deviations from preferred Effect practice are documented as observed facts rather than erased.
- Confirm services, `Atom`, read modules, runtime edges, and schema contracts are not used interchangeably.
- Confirm weak seams remain explicit as `TODO: Confirm`.

## References

- [`./references/decompose-recompose.md`](./references/decompose-recompose.md): Read when: breaking a system into Effect modules or deciding how they should wire back together.
- [`./references/abstraction-selection.md`](./references/abstraction-selection.md): Read when: choosing between `Schema.Class`, plain `Schema`, `Context.Service`, `Context.Reference`, `Layer`, `LayerMap.Service`, a feature read module, `Atom`, a runtime edge module, a toolkit, or a feature-local helper.
- [`./references/pattern-notes.md`](./references/pattern-notes.md): Read when: a reusable Effect pattern reminder would help support or reject a design choice.
