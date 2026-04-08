# Effect Deep Modules

Use this reference when a gray-box module should be expressed with Effect v4 service patterns.

Effect mapping:

- Model the module boundary as a `Context.Service` with a small caller-visible interface.
- Implement the module behind a `Layer` so dependency wiring and lifecycle stay explicit but off the public surface.
- Use `Schema` for caller-visible data and typed errors when values cross meaningful boundaries.
- Keep refs, queues, streams, `RequestResolver`, retries, caches, `PubSub`, and helper services private unless callers truly depend on them.
- Treat `ManagedRuntime` as an integration bridge at the edge of the module or application, not as part of the core module contract.
- Use `LayerMap.Service` when one logical module owns keyed, scoped instances such as per-tenant or per-project resources.

Deep-module rules:

- Make the service contract smaller than the implementation depth it hides.
- Keep constructors, dependency acquisition, and teardown in the layer, not in caller code.
- Expose capability methods such as `load`, `plan`, `execute`, or `publish`, not transport or storage choreography.
- Expose `Stream` only when streaming is part of the caller-visible capability. Otherwise keep polling, chunking, and backpressure mechanics internal.
- Prefer one owned capability per service boundary. Split services only when responsibilities or lifecycles diverge.
- If the module boundary is weak and mostly mirrors helper structure, mark it `TODO: Confirm`.
