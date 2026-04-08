# Effect Abstraction Selection

Use this reference after you know the boundary you are designing.

## Choose The Smallest Stable Abstraction

Pick the first abstraction whose ownership rules match the module. Do not skip ahead to heavier abstractions for aesthetics.

## Selection Matrix

### `Schema.Class`

Use when:

- the module defines canonical data meaning
- invariants, parsing, encoding, or descriptive annotations matter
- callers need one shared contract across boundaries

Why:

- keeps business meaning and validation together
- supports decoding and encoding at edges without turning the model into infrastructure

Do not use when:

- the type exists only as one feature-local intermediate
- the shape is purely adapter-specific and not part of canonical meaning

### plain `Schema`

Use when:

- the contract needs runtime validation or codec behavior, but a class adds no value
- the shape is structural, local, or adapter-facing
- constructors, methods, or nominal identity would be noise

Why:

- keeps runtime validation explicit without forcing class semantics
- works well for DTOs, edge payloads, config shapes, and persistence records

Do not use when:

- the system benefits from one named canonical class-based contract
- callers materially rely on a richer domain type with shared meaning

### `Context.Service`

Use when:

- the boundary owns external IO, retries, caches, resource scoping, background coordination, or runtime substitution
- callers should depend on a capability contract rather than implementation details
- dependency composition matters and should stay explicit

Why:

- gives the capability a stable seam
- makes lifecycle and dependency wiring visible
- keeps infrastructure out of runtime edges and reactive UI state

Do not use when:

- the code is pure, feature-local, and has no owned lifecycle or IO
- you only want a namespace for helper functions

### `Context.Reference`

Use when:

- the boundary is configuration-like rather than capability-like
- the system needs a service with a default value and straightforward overrides
- feature flags, tunables, or environment-derived values should stay injectable

Why:

- matches the v4 service pattern for defaultable values
- avoids inventing a heavier service just to carry configuration

Do not use when:

- the boundary owns behavior, lifecycle, or external resources
- the value is not meaningfully shared through the runtime

### `LayerMap.Service`

Use when:

- the design needs keyed, dynamic resource provisioning
- one stable boundary must build scoped services per tenant, key, or environment slice
- the runtime owns memoization and cleanup for those keyed resources

Why:

- makes dynamic resource ownership explicit
- keeps per-key layer construction out of ad hoc caller code

Do not use when:

- one static layer is enough
- the key-based lifecycle is not real

### `Layer`

Use when:

- the design needs to explain how capability modules recompose
- runtime provisioning, substitution, or merging materially affects correctness
- one runtime assembles multiple services or adapters

Why:

- keeps wiring explicit
- documents where dependencies are provided and where they stop

Do not use when:

- the design is only naming a pure module with no runtime composition concern
- each caller would still provide dependencies ad hoc with no stable composition point

### feature read modules

A feature read module is a design role, not a specific Effect abstraction. It is a small read-only module that exposes reusable semantic reads, hides storage and projection details, and does not own write policy, retries, resource lifecycle, or runtime wiring.

Use when:

- multiple callers need the same semantic read
- the read should stay stable even if storage details evolve
- the module does not own long-lived mutable runtime state

Why:

- separates observation semantics from capability ownership
- avoids re-encoding filters, joins, or projections across features
- keeps reusable reads from being over-modeled as services when no capability seam exists

Do not use when:

- the read is one-off and local to a component or service method
- the module actually owns writes, retries, or background lifecycle
- callers really depend on an infrastructure capability, in which case use `Context.Service`

### `Atom` and `Atom.runtime`

Use when:

- the system needs shared evolving state, feature commands, or reactive read models for UI/runtime consumers
- a feature needs a local runtime seam to bind reads, commits, and services together

Why:

- gives callers ergonomic reactive access without turning components into wiring sites
- keeps UI-facing orchestration close to the feature

Do not use when:

- the boundary primarily owns infrastructure or external capability lifecycle
- the state is not shared, not evolving, or not caller-facing

### runtime edge modules

Use when:

- the module decodes inputs, chooses a feature runtime, and renders or executes
- the boundary is an `HttpApi` handler, CLI command, worker entrypoint, TUI screen, or similar edge

Why:

- keeps edges thin and lets deeper modules own durable policy

Do not use when:

- the edge becomes the only home for business rules or retry policy

### `Toolkit.make` and tool contracts

Use when:

- a module exposes a structured capability surface to an AI or tool caller
- parameter and result schemas are part of the public contract

Why:

- formalizes the boundary between orchestration and callable actions
- keeps tool IO shape explicit and testable

Do not use when:

- the module has no external tool-caller boundary
- a normal service or read-module contract would suffice

## Escalation Triggers

Promote a helper only when one of these appears:

- canonical shared meaning -> `Schema.Class`
- runtime-validated structural contract -> plain `Schema`
- reusable semantic read -> feature read module
- shared evolving read or UI command surface -> `Atom`
- owned IO, lifecycle, caching, retries, or substitution -> `Context.Service`
- defaultable shared configuration -> `Context.Reference`
- explicit keyed resource assembly point -> `LayerMap.Service`
- explicit runtime assembly point -> `Layer`
- AI or tool boundary -> toolkit contract

## Anti-Patterns

- service as folder-organizer
- `Atom` as infrastructure container
- `Layer` as architecture diagram decoration
- `Schema.Class` as default for every type
- read module mixed with write-side policy
- runtime edge mixed with durable business logic
