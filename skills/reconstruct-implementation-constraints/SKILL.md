---
name: reconstruct-implementation-constraints
description: "Recover source-backed implementation constraints that materially shape execution, accepted inputs, operator-visible behavior, or operational prerequisites. Use when a derived requirements or technical-design task needs a reusable constraint ledger from code, tests, manifests, or runtime wiring."
license: MIT
metadata:
  version: "0.1.0"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Rules

- Recover source-backed, execution-relevant constraints that materially change executable output, accepted inputs, safety behavior, or operational prerequisites.
- Treat package manifests, runtime entrypoints, command definitions, schemas, decoders, parser logic, error types, config, and tests as first-class evidence.
- Keep evidence traceable to concrete files and observed behavior when confidence is not obvious.
- Classify recovered constraints into stable buckets:
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
- Use `TODO: Confirm` only when the repository cannot prove the detail.

## Constraints

- This skill defines a reusable classification contract; it does not own the final requirements or technical-design artifact shape.
- Do not silently drop runtime, parser, integration, lifecycle, or packaging constraints because they feel “implementation-only” when they materially affect execution or operations.
- Do not turn architecture decomposition, commit sequencing, or task breakdown into constraint-ledger content.
- Do not promote every low-level library choice into a requirement when it does not materially affect execution, accepted inputs, interoperability, safety, or operations.
- Do not rewrite observed behavior into preferred future-state architecture.

## Requirements

Expected inputs:

- package manifests
- runtime entrypoints
- command definitions
- schemas and decoders
- parser functions
- error types
- tests
- config files
- repository code for the chosen scope

Outputs to the calling skill:

- one constraint ledger grouped by requirement and design category
- confidence notes where support is weak
- routing guidance for where each recovered constraint belongs in requirements versus technical design

In scope:

- recovering runtime and platform constraints
- recovering command grammar, aliases, and shared flag rules
- recovering schema, validation, and parsing constraints
- recovering integration, protocol, and tooling prerequisites
- recovering lifecycle, resource-ownership, and packaging assumptions
- recovering operator-visible no-op and failure behavior
- recovering observed error semantics, including typed and direct thrown failures

Out of scope:

- inventing original intent the code does not prove
- documenting full architecture decomposition
- turning every library import into a constraint
- replacing specialist artifact contracts

## Workflow

1. Confirm the scope to analyze and gather the manifests, entrypoints, commands, schemas, parsers, errors, tests, and config relevant to that scope.
2. Inventory candidate constraints that materially affect execution, accepted inputs, validation semantics, interoperability, safety behavior, or operational prerequisites.
3. Drop low-impact implementation facts that do not change executable behavior or operator obligations.
4. Classify each retained constraint into the shared buckets:
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
5. Map each recovered constraint to where it belongs downstream:
   - `requirements.md` for externally meaningful obligations and execution-relevant constraints
   - `technical-design.md` for composition roots, boundary types, resource ownership, runtime wiring, and detailed error or lifecycle seams
   - both when the same fact shapes an observable contract and an architectural boundary
6. Keep special attention on command aliases, shared flags, accepted source grammars, strict versus tolerant modes, fixed runtime or tool requirements, temp-resource ownership, and review or diff integrations.
7. Record packaging or path assumptions as `TODO: Confirm` when the code suggests them but does not fully prove them.
8. Deliver the constraint ledger with confidence notes and routing guidance for the calling skill.

## Gotchas

- If manifests or runtime entrypoints are ignored, runtime and dependency constraints vanish before requirements or design drafting even starts.
- If parser logic, schemas, or CLI tests are ignored, accepted input grammar and validation semantics disappear from the reconstructed contract.
- If every implementation fact is kept, the ledger turns into a code inventory. Keep only execution-relevant constraints.
- If observed no-op or failure behavior is dropped because it feels too small, operator-visible contract details disappear from downstream artifacts.
- If packaging or path assumptions are stated too confidently, downstream work inherits fiction. Use `TODO: Confirm` when support is partial.
- If a constraint is recovered but not mapped to requirements or technical design, later specialist outputs will drop it again.

## Deliverables

- a reusable implementation-constraint ledger for the chosen scope
- confidence notes for weakly supported details
- clear routing guidance for requirements versus technical design
- explicit `TODO: Confirm` markers where evidence is partial

## Validation Checklist

- recovered constraints are source-backed and execution-relevant
- runtime, parser, integration, lifecycle, dependency, and packaging constraints are considered explicitly
- low-impact implementation trivia is excluded
- operator-visible no-op and failure behavior is included when source-backed
- each recovered constraint is mapped to requirements, technical design, or both
- weakly supported details are marked `TODO: Confirm`
