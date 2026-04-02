# Development Principles

Changes to this skill pack should follow these principles.

## Preserve The Layer Model

Every skill should fit exactly one layer:

- foundational
- expertise
- orchestration

Store every skill under `skills/<skill-name>/` and declare the layer with `metadata.layer`.

Split mixed responsibilities instead of adding exceptions to the dependency graph.

## Preserve Reversibility

Any new authored artifact should have a clear story for reconstruction, or an explicit reason it is author-only.

Do not add authored-only structure casually. Every one-way artifact makes the system less reusable.

## Keep Contracts Stable

Canonical artifact contracts are the center of the pack.

Prefer:

- stable section order
- stable naming
- explicit validation rules
- explicit uncertainty handling for reconstructed outputs

Avoid silent contract drift between create and derive paths.

## Keep Pack Boundaries Clear

Do not blur these responsibilities:

- foundational skills define shared artifact contracts
- expertise skills own one bounded authoring, planning, or reconstruction responsibility
- orchestration skills orchestrate expertise entry skills only

If a skill mixes those roles, the outputs get harder to trust and harder to compose.

## Keep Dependency Direction Strict

Follow the package dependency rules:

- foundational -> no required skill dependencies
- expertises -> foundational only
- orchestrations -> expertise only

If a skill needs behavior from a lower layer, declare the dependency. If it needs guidance from another package or an optional follow-on path, prefer a local reference doc over a required dependency.

## Optimize For Agent Use

Artifacts should be easy for an implementation agent to load, compare, and act on.

Prefer:

- deterministic filenames
- explicit section headings
- concise language
- direct traceability between artifacts

Avoid prose that sounds good to humans but hides the actual contract.

## Prefer Explicit Uncertainty

Reconstruction skills should mark uncertainty instead of inventing original intent.

A precise unknown is more useful than a confident guess.

## Narrow Responsibilities

Each skill should do one thing well.

Prefer adding a small composable foundational contract or expertise skill over making one orchestration skill absorb unrelated responsibilities.

## Keep Repository Workflow In Mind

The pack is meant to be used inside a live repository with local planning and task artifacts.

Changes should preserve:

- compatibility with repository-based review
- easy diffing of generated artifacts
- straightforward reuse by agents
