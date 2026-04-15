---
name: artifact-naming
description: "Resolve and normalize stable artifact basenames. Use when a workflow or skill needs deterministic naming without taking ownership of placement, filenames, or authoring."
license: MIT
metadata:
  version: "0.1.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own basename resolution only. Return one stable, filesystem-safe basename the caller can reuse across revisions without taking ownership of path selection, placement, filenames, or authoring.

## Contract

- Resolution order:
  1. explicit user-provided artifact slug or basename
  2. existing related artifact basename when continuing or revising prior work
  3. concise basename derived from the approved problem statement
- Normalize to lowercase kebab-case before any caller-owned suffix is added.
- Preserve semantic tokens that disambiguate artifact intent.
- Reuse the same basename across revisions of the same artifact family.
- Do not silently rename published or already-linked artifacts.
- Do not derive names from implementation details, branch names, or transient ticket text when an approved problem statement exists.
- This skill owns basename resolution only; it does not own path selection, placement, filename selection, suffix policy, or artifact authoring.

## Inputs

- explicit artifact slug or preferred basename when available
- related prior artifact filename when revising existing work
- approved problem statement or concise artifact title
- target artifact type when the caller needs the right suffix later

## Outputs

- one deterministic basename
- one short source note: `explicit`, `reused`, or `derived`
- one normalized result ready for caller-owned composition

## Workflow

1. Check for an explicit artifact slug or basename.
2. If none exists, reuse the established basename when the task is a continuation or revision.
3. If no prior basename exists, derive a concise name from the approved problem statement.
4. Normalize the chosen value to lowercase kebab-case.
5. Return the basename plus its source and reuse that same basename for future revisions.

## Validation

- Confirm higher-precedence naming sources were checked before fallback derivation.
- Confirm the returned basename is lowercase kebab-case and filesystem-safe.
- Confirm revisions preserve the existing basename.
- Confirm no path, placement, filename, suffix, or authoring rules were mixed into this contract.
