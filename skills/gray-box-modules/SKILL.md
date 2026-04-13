---
name: gray-box-modules
description: "Define the shared contract for describing bounded gray-box modules in technical design. Use when a technical-design task needs durable module boundaries, contracts, invariants, or lifecycle ownership described."
license: MIT
metadata:
  version: "0.2.0"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Rules

- Describe a module by owned capability, boundary, contract, invariants, dependency composition, and hidden implementation depth because gray-box modules are about what callers can rely on, not how internals are arranged.
- Keep the public contract smaller and more stable than the hidden implementation because callers should depend on durable capabilities only.
- Name what complexity the module hides because a boundary without hidden depth is usually just a grouping label.
- In authored design, prefer gray-box modules when the system has real bounded capabilities because that gives implementation durable seams.
- In derived design, claim a gray-box module only when repository evidence shows a real boundary because convenient grouping is not enough.
- Mark weakly supported intent or uncertain seams as `TODO: Confirm` because reconstruction must not invent architectural confidence.

## Constraints

- This skill defines a reusable module contract; it does not replace the calling role's workflow.
- Do not treat every directory, package, or large file as a module by default.
- Do not expose helper layout, storage choreography, queue topology, or library-specific mechanics unless callers materially depend on them.
- Do not describe a boundary without stating what it owns and what it does not own.
- Do not freeze private implementation flow in tests, contracts, or design language.

## Requirements

The caller should use this contract to capture:

1. boundary statement
2. owned capability
3. caller-visible contract shape
4. invariants and failure handling
5. dependency composition and lifecycle ownership
6. hidden implementation depth
7. boundary-test expectations
8. reconstruction evidence threshold

Minimum output expectations:

- the boundary states what the module owns and excludes
- the contract lists caller-visible methods, inputs, outputs, and errors when they matter
- invariants explain what stays true across success and failure paths
- dependency composition explains what the module relies on and where wiring responsibility lives
- lifecycle ownership is explicit when resources, workers, subscriptions, or scoped cleanup matter
- reconstruction claims separate observed evidence from inference
- derived module claims cite evidence such as composition-root registration, explicit layer provisioning, stable public methods, tagged errors, dedicated tests, distinct tolerant versus strict modes, or isolated lifecycle and resource ownership when those signals exist

Use the bundled references only when the task specifically needs Effect guidance. Do not load them for non-Effect technical design work.

## Workflow

1. State the bounded capability and the seam that contains it.
2. Name what the module owns, what it does not own, and what complexity it hides.
3. Define the smallest durable public contract callers should rely on.
4. Record invariants, validation, failure handling, dependency composition, and lifecycle ownership that materially affect that boundary.
5. Describe boundary-test expectations that lock caller-visible behavior without locking helper choreography.
6. If the design is authored, push toward gray-box modules only where the capability and lifecycle are durable.
7. If the design is derived, verify the module claim with concrete evidence such as stable entrypoints, composition-root registration, explicit layer provisioning, stable public methods, tagged errors, dedicated tests, distinct tolerant versus strict paths, isolated lifecycle control, cohesive ownership, or explicit wiring.
8. Mark any weak seam or uncertain intent as `TODO: Confirm`.
9. Load the Effect references only for Effect-specific boundary, lifecycle, testing, or deep-module questions.

## Gotchas

- If you label every directory a module, the design looks structured but says nothing about capability ownership. Only claim a module when callers can rely on a real boundary.
- If the public contract mirrors internal helper flow, refactors become breaking changes on paper even when callers do not care. Keep the contract smaller than the implementation it hides.
- If authored design skips invariants and lifecycle ownership, implementers guess where cleanup, retries, or background work live and the boundary rots immediately. State those responsibilities up front.
- If derived design infers module intent from naming alone, you end up documenting an architecture that never really existed. Require evidence like dedicated tests, stable entrypoints, or explicit wiring.
- If tolerant and strict paths are merged into one vague boundary, important caller-visible contracts disappear. Keep materially different modes explicit.
- If service interfaces are named without public methods or error contracts, the module claim stays too weak to guide change work. Name the callable seam and failure model.
- If tests assert queue names, batching groups, or helper call order, they freeze internals and block replacement. Test caller-visible behavior and critical invariants instead.
- If you say a module exists but never name the complexity it hides, the boundary is probably just a convenience grouping. Explain the hidden policy, workflow, or lifecycle depth.
- If uncertainty gets polished into confident prose, later skills treat speculation as fact and compound the error. Use `TODO: Confirm` for weak seams.

## Deliverables

- A reusable contract for describing gray-box modules in technical-design artifacts.
- Explicit expectations for boundary, contract, invariants, lifecycle ownership, and hidden internals.
- Evidence rules for authored versus derived module claims.
- On-demand Effect references for tasks that need implementation-specific guidance.

## References

- [`references/effect-deep-modules.md`](./references/effect-deep-modules.md): Read when: mapping a gray-box module onto Effect service and layer patterns.
- [`references/effect-boundary-contracts.md`](./references/effect-boundary-contracts.md): Read when: defining caller-visible methods, DTOs, invariants, or boundary errors in Effect.
- [`references/effect-composition-lifecycle.md`](./references/effect-composition-lifecycle.md): Read when: assigning dependency composition or lifecycle ownership in Effect layers.
- [`references/effect-boundary-testing.md`](./references/effect-boundary-testing.md): Read when: testing an Effect module boundary without freezing internal choreography.

## Validation Checklist

- The output reads as a foundational contract, not as a role-specific workflow.
- Boundary, owned capability, contract, invariants, lifecycle, and dependency composition are all explicit.
- Authored technical design guidance pushes toward real bounded capabilities, not generic decomposition.
- Derived module claims cite caller-visible seams and supporting evidence rather than folder layout.
- Boundary contracts include methods, inputs, outputs, and errors when they materially shape callers.
- Resource and lifecycle ownership is explicit when present.
- Weakly supported claims are marked `TODO: Confirm`.
- Effect-specific details remain in references instead of bloating the main contract.
