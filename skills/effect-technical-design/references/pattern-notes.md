# Effect Technical Design Pattern Notes

Use this reference when you need reusable reminders about common Effect architecture shapes.

## Pattern 1: Capability boundaries are lifecycle-heavy

Observed reusable rule:

- modules that own external resources, clients, caches, watchers, background work, or cleanup need explicit lifecycle ownership
- callers should depend on a compact capability contract, not on setup choreography
- concurrency control and scoped cleanup belong inside the capability boundary, not at the edge

Design implication:

When a module owns process lifecycle, filesystem watch, API-client setup, cache lifetime, or scoped cleanup, model it as a `Context.Service` boundary and document lifecycle ownership explicitly.

## Pattern 2: Internal helpers stay hidden behind capability seams

Observed reusable rule:

- stable modules expose a narrow public API
- retry policy, caching, transport hooks, helper sequencing, and provider-specific details stay internal

Design implication:

Document the durable API that callers rely on, not the helper choreography that implements it.

## Pattern 3: Domain contracts should centralize shared meaning

Observed reusable rule:

- when the same shape crosses persistence, UI, AI, import/export, or integration boundaries, one schema-backed domain contract prevents drift
- encoding, decoding, defaults, and invariants stay near the contract instead of being repeatedly redefined

Design implication:

When business meaning is canonical across multiple boundaries, centralize it in a schema-backed domain contract before designing higher-level modules.

## Pattern 4: Observation and orchestration are often feature-local

Observed reusable rule:

- read modules capture reusable reads; here, “read module” means a small read-only module for reusable semantic reads, not a dedicated Effect abstraction
- feature atoms expose user-facing state and commands
- writes happen through focused feature workflows instead of generic global stores
- runtime assembly is often feature-local when the feature owns the user-facing seam

Design implication:

When a module mainly serves one feature's reactive read and command surface, keep it feature-local and recompose infrastructure behind a local runtime rather than lifting everything into app-global services.

## Pattern 5: Recomposition should happen through a few visible seams

Observed reusable rule:

- strong architectures have a small number of obvious composition points
- capability layers, feature runtimes, and app boot files make wiring visible
- if every caller can `provide` dependencies ad hoc, the runtime graph stops being legible

Design implication:

State exactly where the runtime is assembled. Avoid architecture descriptions that imply any caller can `provide` dependencies anywhere.

## Pattern 6: Caller contracts should be smaller than implementation depth

Observed reusable rule:

- callers depend on a narrow contract
- internals may include caches, event choreography, retries, cleanup, and helpers that should remain replaceable

Design implication:

Design gray-box modules: the contract should be what callers rely on; internal policy should stay hidden unless callers materially depend on it.

## Pattern 7: Reactive state and capability state are separate concerns

Observed reusable rule:

- reactive state is for observation and feature-facing commands
- capability state is for infrastructure ownership, retries, scoped resources, and hidden policy
- mixing them blurs cleanup ownership and makes abstractions harder to test

Design implication:

If the design mixes these concerns, split the module or explain why the runtime forces them together.

## Design Questions Before Reusing A Pattern

- Is this pattern solving lifecycle ownership, reactive feature state, canonical contracts, or runtime assembly?
- Does the target system actually share the runtime assumptions needed for this pattern?
- Can the same caller-visible contract be preserved with a smaller abstraction?
- Is the proposed module hiding real complexity or only moving code around?

## Safe Reuse Summary

Prefer these rules when the target system has:

- CLI, worker, or service-process lifecycles -> emphasize `Context.Service` boundaries and explicit lifecycle ownership
- browser or app-style reactive state -> emphasize feature-local reads, commands, and runtime seams
- schema-first entities shared across boundaries -> emphasize central domain contracts
- multiple external integrations or adapters -> emphasize narrow capability contracts and visible composition points

Use this runtime-fit check before reusing a pattern:

| Decision                              | Confirm options                                                                               | Pattern impact                                                                                                                                              |
| ------------------------------------- | --------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Reactive and background state profile | no shared reactive state; UI-facing reactive state; long-lived background work; both          | reactive patterns only fit when callers need shared evolving reads or commands; background-work patterns only fit when one module owns long-lived lifecycle |
| Runtime profile                       | browser-only; server-only; CLI-only; worker-only; multi-runtime                               | runtime-specific pattern guidance should only be reused when the target system matches the same runtime seam                                                |
| Multi-runtime breakdown               | browser + server; CLI + worker; browser + worker; server + worker; other explicit combination | mixed-runtime patterns must name what is shared, what is runtime-specific, and where recomposition happens                                                  |
| Persistence contract shape            | `Schema.Class`; plain `Schema`; existing external DTOs; mixed by boundary                     | schema-centric patterns only fit when the target system actually owns canonical contracts instead of borrowing adapter DTOs                                 |

Mark `TODO: Confirm` when the target system does not clearly fit the selected profile.
