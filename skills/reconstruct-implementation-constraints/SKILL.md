---
name: reconstruct-implementation-constraints
description: "Recover source-backed implementation constraints that materially shape execution, accepted inputs, operator-visible behavior, or operational prerequisites. Use when a derived requirements or technical-design task needs a reusable constraint ledger from code, tests, manifests, or runtime wiring."
license: MIT
metadata:
  version: "0.1.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own a reusable contract for recovering and classifying implementation constraints that materially affect execution. Return a constraint ledger plus routing guidance so derived requirements and technical design do not drop high-impact facts.

## Contract

- Recover only source-backed, execution-relevant constraints that materially change executable output, accepted inputs, validation semantics, interoperability, safety behavior, or operational prerequisites.
- Treat manifests, runtime entrypoints, command definitions, schemas, decoders, parser logic, error types, config, and tests as first-class evidence.
- Classify retained constraints into stable buckets:
  - runtime and platform
  - command grammar and aliases
  - validation and schema
  - data shape and parsing
  - integration and protocol
  - lifecycle and resource ownership
  - dependency and tooling prerequisites
  - error semantics
  - packaging and path assumptions
  - operator-visible no-op and failure behavior
- Phrase constraints as stable obligations or observed design facts, not as a code tour.
- Map each recovered constraint downstream to `requirements.md`, `technical-design.md`, or both.
- Do not silently drop runtime, parser, integration, lifecycle, or packaging constraints because they feel implementation-only.
- Do not turn architecture decomposition, commit sequencing, or task breakdown into constraint-ledger content.
- Do not rewrite observed behavior into preferred future-state architecture.
- Use `TODO: Confirm` only when the repository cannot prove the detail.

## Inputs

- package manifests
- runtime entrypoints
- command definitions
- schemas and decoders
- parser functions
- error types
- tests
- config files
- repository code for the chosen scope

## Outputs

- one reusable implementation-constraint ledger for the chosen scope
- confidence notes for weakly supported details
- routing guidance for `requirements.md` versus `technical-design.md`
- explicit `TODO: Confirm` markers where evidence is partial

## Workflow

1. Confirm the scope and gather the manifests, entrypoints, commands, schemas, parsers, errors, tests, config, and code relevant to that scope.
2. Inventory candidate constraints that materially affect execution, accepted inputs, validation semantics, interoperability, safety behavior, or operational prerequisites.
3. Drop low-impact implementation facts that do not change executable behavior or operator obligations.
4. Classify each retained constraint into the shared buckets.
5. Map each recovered constraint to `requirements.md`, `technical-design.md`, or both.
6. Keep special attention on aliases, shared flags, accepted source grammars, strict versus tolerant modes, fixed runtime or tool requirements, temp-resource ownership, and review or diff integrations.
7. Record packaging or path assumptions as `TODO: Confirm` when the code suggests them but does not fully prove them.
8. Deliver the constraint ledger with confidence notes and routing guidance.

## Validation

- Confirm recovered constraints are source-backed and execution-relevant.
- Confirm runtime, parser, integration, lifecycle, dependency, and packaging constraints were considered explicitly.
- Confirm low-impact implementation trivia was excluded.
- Confirm operator-visible no-op and failure behavior is included when source-backed.
- Confirm each recovered constraint is mapped to requirements, technical design, or both.
- Confirm weakly supported details stay `TODO: Confirm`.
