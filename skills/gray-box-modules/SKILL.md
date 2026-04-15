---
name: gray-box-modules
description: "Define the shared contract for describing bounded gray-box modules in technical design. Use when a technical-design task needs durable module boundaries, contracts, invariants, or lifecycle ownership described."
license: MIT
metadata:
  version: "0.2.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own a reusable contract for describing gray-box modules in technical design: what the module owns, what callers can rely on, what complexity it hides, and what evidence is strong enough to claim the boundary.

## Contract

- Describe a module by:
  - boundary statement
  - owned capability
  - caller-visible contract shape
  - invariants and failure handling
  - dependency composition and lifecycle ownership
  - hidden implementation depth
  - boundary-test expectations
- Keep the public contract smaller and more stable than the hidden implementation.
- Name what the module owns and excludes.
- Name what complexity the module hides; without hidden depth, the boundary is usually just grouping.
- In authored design, prefer gray-box modules only when the system has real bounded capabilities.
- In derived design, claim a gray-box module only when repository evidence shows a real caller-visible seam.
- Separate observed evidence from inference and mark weak seams as `TODO: Confirm`.
- Do not treat every directory, package, or large file as a module by default.
- Do not expose helper layout, storage choreography, queue topology, or library-specific mechanics unless callers materially depend on them.

## Inputs

- authored design boundary question or repository evidence for a derived claim
- caller-visible contract needs
- invariants, failure, dependency, and lifecycle concerns
- Effect-specific boundary questions when relevant

## Outputs

- reusable gray-box module contract for technical-design work
- evidence threshold for authored versus derived module claims
- explicit expectations for ownership, contract, invariants, lifecycle, and hidden internals
- optional Effect-specific support through local references when needed

## Workflow

1. State the bounded capability and the seam that contains it.
2. Name what the module owns, what it does not own, and what complexity it hides.
3. Define the smallest durable public contract callers should rely on.
4. Record invariants, validation, failure handling, dependency composition, and lifecycle ownership that materially affect that boundary.
5. Describe boundary-test expectations that lock caller-visible behavior without freezing helper choreography.
6. In authored design, push toward gray-box modules only where the capability and lifecycle are durable.
7. In derived design, verify the module claim with concrete evidence such as stable entrypoints, composition-root registration, explicit wiring, tagged errors, dedicated tests, or isolated lifecycle control.
8. Mark any weak seam or uncertain intent as `TODO: Confirm`.
9. Load the Effect references only for Effect-specific boundary, lifecycle, testing, or deep-module questions.

## Validation

- Confirm the output reads as a foundational contract, not a role-specific workflow.
- Confirm boundary, ownership, contract, invariants, dependency composition, lifecycle ownership, and hidden depth are explicit.
- Confirm derived module claims cite caller-visible seams and supporting evidence rather than folder layout.
- Confirm boundary contracts include methods, inputs, outputs, and errors when they materially shape callers.
- Confirm weakly supported claims stay `TODO: Confirm`.

## References

- [`./references/effect-deep-modules.md`](./references/effect-deep-modules.md): Read when: mapping a gray-box module onto Effect service and layer patterns.
- [`./references/effect-boundary-contracts.md`](./references/effect-boundary-contracts.md): Read when: defining caller-visible methods, DTOs, invariants, or boundary errors in Effect.
- [`./references/effect-composition-lifecycle.md`](./references/effect-composition-lifecycle.md): Read when: assigning dependency composition or lifecycle ownership in Effect layers.
- [`./references/effect-boundary-testing.md`](./references/effect-boundary-testing.md): Read when: testing an Effect module boundary without freezing internal choreography.
