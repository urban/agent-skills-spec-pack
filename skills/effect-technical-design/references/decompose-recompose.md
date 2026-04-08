# Decompose And Recompose An Effect TypeScript System

Use this reference to turn a large TypeScript system into stable Effect modules, then wire those modules back into one architecture.

## Decomposition Heuristic

Split a system only when one of these boundaries is real:

1. **Capability ownership**: one area owns a durable job such as provider access, synchronization, extraction, proxying, background processing, or external orchestration.
2. **Lifecycle ownership**: one area starts, scopes, stops, retries, caches, or watches resources.
3. **Contract ownership**: one area defines canonical data or a stable caller-visible API.
4. **Observation seam**: one area exposes reusable reads or shared evolving state to callers.
5. **Runtime seam**: one area belongs to a distinct runtime such as browser, worker, CLI, server, or long-lived service process.

Do not split only because a file is large or a concept has a noun.

## Recommended Decomposition Order

Decompose in this order because later layers depend on earlier ownership choices:

1. **Domain contracts**
   - canonical schemas, entities, value objects, invariants
   - Keep shared meaning, transformations, and serialization close to the contract when multiple boundaries depend on the same data.
2. **Capability services**
   - external IO, hidden policy, retries, scoped resources, caching, orchestration of adapters
   - Use a service boundary when callers should depend on a stable capability instead of transport details.
3. **Persistence and read seams**
   - reusable reads over durable state, read composition, projections for callers
   - Use semantic reads to hide storage details from downstream consumers.
   - A read module here means a small read-only module for reusable semantic reads, not a first-class Effect type.
4. **Feature orchestration seams**
   - feature-local workflows that combine domain, services, and commits or mutations
   - Keep user-facing orchestration close to the feature when the boundary is primarily reactive or interactive.
5. **Runtime edges**
   - `HttpApi` handlers, CLI commands, worker entrypoints, TUI screens, browser boot files
   - Keep these thin; they should decode inputs and assemble the right runtime.

## Boundary Questions

For each candidate module, answer all of these:

- What capability or truth does it own?
- What does it explicitly not own?
- Who calls it and what stable contract do they see?
- Which dependencies does it compose internally versus receive from above?
- Does it own lifecycle or only pure transformation?
- Would callers break if internals were reorganized?

If you cannot answer these, the module is probably premature.

## Recomposition Heuristic

Once modules are real, wire them back together with explicit composition points.

### Recomposition Order

1. **Recompose domain contracts into boundary contracts**
   - domain types, DTO transforms, persistence shapes, tool schemas
2. **Recompose capabilities through `Layer`, `Context.Service`, `Context.Reference`, or `LayerMap.Service`**
   - one composition point per runtime or sub-runtime
3. **Recompose reads through read modules and `Atom`**
   - read module first, `Atom` second when a shared evolving read or UI command is needed
4. **Recompose feature workflows**
   - feature runtime combines local state or app layer, capability services, and feature-local commands
5. **Recompose app runtime**
   - browser root, CLI main, worker loop, server process, or handler module provides the final layers

### Where To Compose

Prefer one of these explicit composition sites:

- a static `.layer` on a `Context.Service` when the capability is broadly reusable
- an `Atom.runtime(...)` when a UI-facing feature needs a scoped runtime assembled from feature dependencies
- an app bootstrap file when the whole runtime is global
- a handler, command, or entrypoint module only for final decode-and-wire steps, not for durable business policy

## Reusable Pattern Rules

- When a module owns external resources, long-lived state, or cleanup, model it as a capability boundary with explicit lifecycle and composition.
- When state is user-facing and reactive, keep reads and commands close to the feature, but compose infrastructure behind a runtime seam instead of smearing it through components.
- Document the durable API that callers rely on, not the helper choreography that implements it.
- State exactly where the runtime is assembled. Avoid architecture descriptions that imply any caller can `provide` dependencies anywhere.

## Module Shape Checklist

A good Effect module usually has:

- one owned capability or truth
- a smaller public contract than internal machinery
- explicit lifecycle ownership when resources exist
- explicit dependency composition story
- tests that lock caller-visible behavior, not helper choreography

A weak module usually has:

- many nouns but no owned capability
- public methods that mirror internal steps
- hidden `provide` calls across unrelated call sites
- mixed domain meaning, persistence mechanics, and UI state with no seam

## Decision Summary

Use this quick router:

- pure invariant or entity meaning -> domain contract
- external IO with retries, caching, scoping, or hidden policy -> `Context.Service`
- reusable semantic read -> feature read module
- shared evolving UI-facing read or command surface -> `Atom`
- decode and wire edge -> runtime edge module
- feature-only orchestration -> feature module that may host local read modules and atoms
