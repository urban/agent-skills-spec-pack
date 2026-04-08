# Effect Boundary Contracts

Use this reference when defining the public contract of a gray-box module in Effect.

Contract rules:

- Define the caller-visible capability as a `Context.Service` interface with a small set of durable methods.
- Make inputs, outputs, and typed errors explicit in method signatures when they materially affect callers.
- Use `Schema` for boundary DTOs, command inputs, result payloads, and errors that must be validated or serialized.
- Use `Schema.TaggedErrorClass` for boundary-facing errors that callers should discriminate on.
- Keep lower-level causes wrapped behind domain or module errors instead of leaking transport, storage, or parsing details directly.
- Surface streaming return types, event feeds, or long-running handles only when they are part of the business capability, not just implementation convenience.

Invariant rules:

- State what the service preserves on success and failure, not just what it attempts.
- Put validation at the boundary when invalid inputs would otherwise leak deeper into the module.
- Keep policy defaults explicit through `Context.Reference` or config services rather than hidden magic constants.
- Keep reference-backed policy narrow and stable. Use it for defaults, feature flags, strictness, and thresholds, not to smuggle arbitrary internal state across the boundary.
- Separate stable contract promises from replaceable implementation choices.

What not to expose:

- concrete clients, repositories, refs, queues, caches, internal state transitions
- helper file layout or call order
- retry policy, batching shape, or concurrency mechanics unless callers depend on them
- `ManagedRuntime`, request batching internals, event bus topology, or background fiber orchestration unless the boundary explicitly owns those concepts
