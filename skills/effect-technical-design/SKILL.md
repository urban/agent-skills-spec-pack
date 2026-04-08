---
name: effect-technical-design
description: Define Effect-specific technical design guidance for TypeScript systems. Use when a technical-design task targets an Effect application and needs shared architecture and boundary conventions.
metadata:
  version: 0.2.0
  layer: foundational
---

## Rules

- Treat this skill as the Effect-specific companion to technical design, not as a replacement for the canonical technical-design artifact contract.
- Focus on architecture decisions that are not already obvious from referencing the Effect source code, because this skill should redirect boundary choices, not restate Effect syntax or API basics.
- Start from owned capabilities, read seams, lifecycle boundaries, and runtime composition points before naming an Effect abstraction, because premature abstraction causes most Effect design drift.
- Choose the smallest stable abstraction that protects the boundary: helper before schema-backed contract, schema-backed contract before read module, read module before `Atom`, feature module before `Context.Service`, and `Context.Service` before wider layer graphs.
- Treat a read module as a design role, not an Effect API: a small read-only module that exposes reusable semantic reads, hides storage and projection details, and does not own write policy, retries, resource lifecycle, or runtime wiring.
- Separate capability ownership from observation ownership, because services and layers own infrastructure while read modules and `Atom` expose reads and feature-facing state.
- Recompose modules through a small number of explicit runtime seams, because ad hoc `provide` chains hide the real architecture.
- In derived design, describe the Effect abstractions actually used before recommending alternatives.
- Recover concrete Effect architecture details such as `Layer.mergeAll`, `Layer.provideMerge`, `Context.Service`, `Schema.TaggedErrorClass`, `effect/unstable/cli`, scoped resources, and runtime helpers when the repository shows them.
- Capture where the implementation uses direct Node or Bun APIs, direct child-process calls, or direct thrown errors instead of idealized Effect-only boundaries.
- Mark weakly supported design claims as `TODO: Confirm` instead of turning hunches into architecture.

## Constraints

- This skill defines reusable Effect technical-design guidance; it does not own the final artifact shape.
- Do not duplicate generic Effect implementation advice already covered by referencing the Effect source code.
- Do not recommend services, `Atom`, layers, or schema-backed contracts by default.
- Do not collapse domain contracts, capability boundaries, and reactive read seams into one module category.
- Do not mirror repository folders as architecture unless the caller-visible boundary is real.
- Do not describe recomposition as “just provide the layers”; name concrete composition points and ownership.
- Do not rewrite a derived architecture into the preferred architecture if the code proves a different implementation.

## Requirements

Use this skill to supply:

- decomposition rules for breaking a TypeScript + Effect system into stable modules
- recomposition rules for wiring those modules into one runtime architecture
- abstraction-selection guidance for `Schema.Class`, plain `Schema`, `Context.Service`, `Context.Reference`, `Layer`, `LayerMap.Service`, feature read modules, `Atom`, runtime edge modules, toolkits, and helpers
- guardrails that keep technical designs focused on ownership instead of library enthusiasm
- derived-design guidance that names the abstractions, runtime wiring, and escape hatches actually in use

Inputs expected from the calling skill or task:

- approved requirements or repo evidence
- runtime context: CLI, server, browser, worker, or mixed
- known integrations, persistence model, and UI or reactive state needs
- unresolved boundary questions that need explicit decisions

Outputs to the calling skill:

- Effect-specific module decomposition guidance
- Effect-specific recomposition guidance
- abstraction rationale tied to ownership and lifecycle
- observed architecture notes for derived design
- `TODO: Confirm` markers for unresolved high-impact seams

In scope:

- Effect-aware technical design authoring guidance
- Effect-aware technical design reconstruction guidance
- boundary selection for common Effect abstractions
- translating implementation evidence into reusable architecture rules

Out of scope:

- generic Effect syntax or API tutorials
- implementation code generation
- product requirements authoring
- execution planning

Routing guidance:

| Task                                                | Read first                                                                     |
| --------------------------------------------------- | ------------------------------------------------------------------------------ |
| Break a system into stable Effect modules           | [`references/decompose-recompose.md`](./references/decompose-recompose.md)     |
| Choose the right Effect abstraction for a boundary  | [`references/abstraction-selection.md`](./references/abstraction-selection.md) |
| Ground the design in reusable architecture patterns | [`references/pattern-notes.md`](./references/pattern-notes.md)                 |

## Required Decision Table

Resolve these before finalizing guidance. If evidence is missing, keep the item as `TODO: Confirm` in the downstream design artifact.

| Decision                              | Confirm options                                                                                                                              | Architecture impact                                                                                                                                                                                                                             |
| ------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reactive and background state profile | no shared reactive state; UI-facing reactive state; long-lived background work; both UI-facing reactive state and long-lived background work | UI-facing reactive state may justify feature read modules and `Atom`; background work strengthens `Context.Service` and lifecycle ownership guidance; both require an explicit seam between observation and infrastructure ownership         |
| Persistence contract shape            | `Schema.Class`; plain `Schema`; existing external DTOs; mixed by boundary                                                                    | `Schema.Class` fits canonical shared domain meaning; plain `Schema` fits structural runtime-validated contracts; external DTOs fit adapter-facing boundaries; mixed should name which boundaries own canonical contracts versus borrowed shapes |
| Runtime profile                       | browser-only; server-only; CLI-only; worker-only; multi-runtime                                                                              | runtime profile sets the real recomposition seams, runtime edge modules, and where layers or feature runtimes assemble                                                                                                                          |
| Multi-runtime breakdown               | browser + server; CLI + worker; browser + worker; server + worker; other explicit combination                                                | multi-runtime designs must name which modules are shared versus runtime-specific, and where each runtime composes dependencies                                                                                                                  |

## Workflow

1. Confirm the technical-design task is for a TypeScript system using Effect.
2. Inspect imports, runtime wiring, and entrypoints before proposing abstractions.
3. Identify the decision type: decomposition, recomposition, abstraction selection, or derived-architecture recovery.
4. For decomposition or recomposition work, load [`references/decompose-recompose.md`](./references/decompose-recompose.md) to break the system into candidate modules by owned capability, lifecycle, contract, and runtime seam.
5. For abstraction selection work, load [`references/abstraction-selection.md`](./references/abstraction-selection.md) to choose the smallest stable abstraction for each candidate boundary.
6. Load [`references/pattern-notes.md`](./references/pattern-notes.md) only when you need reusable pattern reminders to support or reject a design choice.
7. For derived design, identify the actual abstractions and runtime composition in use, including services, layers, scoped resources, schema types, CLI wiring, and runtime helpers.
8. Classify each observed abstraction by ownership, lifecycle, visibility to callers, and recomposition site.
9. Note where the implementation bypasses preferred Effect conventions through direct Node or Bun APIs, direct thrown errors, or other escape hatches.
10. Return guidance in observed-architecture and ownership terms first: what the module owns, what it hides, what callers rely on, how it recomposes, and why a heavier or lighter abstraction would be wrong.
11. Add optional improvement notes only after the observed architecture is documented clearly.
12. Mark unresolved high-impact seams as `TODO: Confirm`.

## Gotchas

- If this skill starts teaching `Effect.gen`, `Effect.fn`, or basic service syntax, it duplicates information in the Effect source-code and wastes context right when the agent needs architecture guidance. Keep this skill on boundary and recomposition decisions.
- If you pick a `Context.Service` because a module looks important, the design grows infrastructure seams without any protected capability. Ask what the module owns before recommending a service.
- If you pick an `Atom` because a value is shared, you can accidentally move retries, provider setup, or worker lifecycle into reactive state and make cleanup invisible. Keep infrastructure below the observation seam.
- If you use read module, schema contract, service, and runtime edge as interchangeable labels, the design reads organized but gives implementers no ownership map. Assign one primary boundary role per module.
- If decomposition follows current folders instead of stable contracts, the design freezes accidents from today's repo and blocks cleaner recomposition later. Name modules by capability, lifecycle, and caller-visible contract.
- If recomposition is vague, implementers scatter `Layer.provide` calls through runtime edges, atoms, and helpers until the runtime graph is unreadable. Name the few real composition sites explicitly.
- If derived guidance rewrites the implementation into preferred architecture, reconstruction becomes fiction. Describe the abstractions actually in use before suggesting alternatives.
- If direct runtime escape hatches are omitted, downstream planning misses real constraints around lifecycle, failure handling, and portability. Keep those escape hatches visible.

## Deliverables

- reusable Effect-specific decomposition guidance for technical design work
- reusable Effect-specific recomposition guidance for technical design work
- a clear abstraction-selection guide for common Effect boundaries
- observed-architecture notes for derived Effect designs
- pattern notes for common Effect architectures
- explicit `TODO: Confirm` handling for weak seams

## References

- [`references/decompose-recompose.md`](./references/decompose-recompose.md): Read when: breaking a complex system into modules or deciding how those modules should wire back together.
- [`references/abstraction-selection.md`](./references/abstraction-selection.md): Read when: choosing between `Schema.Class`, plain `Schema`, `Context.Service`, `Context.Reference`, `Layer`, `LayerMap.Service`, a feature read module, `Atom`, a runtime edge module, a toolkit, or a feature-local helper.
- [`references/pattern-notes.md`](./references/pattern-notes.md): Read when: you need reusable, pattern reminders before finalizing the design.

## Validation Checklist

- the skill stays foundational and does not own the final artifact contract
- guidance is framed in ownership, lifecycle, and recomposition terms
- generic Effect syntax guidance is excluded in favor of referencing the Effect source code directly
- derived guidance names the abstractions actually in use when the repository shows them
- deviations from preferred Effect practice are documented as observed facts rather than silently erased
- services, `Atom`, read modules, runtime edges, and schema contracts are not used interchangeably
- missing high-impact evidence is marked `TODO: Confirm`
