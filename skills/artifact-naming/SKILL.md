---
name: artifact-naming
description: "Resolve and normalize stable artifact basenames. Use when a workflow or skill needs deterministic naming without taking ownership of placement, filenames, or authoring."
license: MIT
metadata:
  version: "0.1.0"
  author: "urban (https://github.com)"
  layer: foundational
---

## Rules

- Resolve one stable basename per artifact family and reuse it across revisions because rename drift breaks cross-artifact linking.
- Prefer explicit user-provided slugs first because caller intent outranks inferred naming.
- Reuse an existing related basename when continuing prior work because revisions should not fork naming history.
- Derive a new name from the approved problem statement only when no stronger source exists because derived names are fallback behavior.
- Normalize to lowercase kebab-case before adding any artifact-type suffix because downstream skills should not each invent cleanup logic.
- Preserve semantic tokens that disambiguate artifact intent because over-shortening causes collisions.

## Constraints

- This skill owns basename resolution only.
- It does not own path selection, artifact placement, artifact filename selection, or artifact authoring.
- Output must stay filesystem-safe: lowercase letters, numbers, and single hyphens only.
- Do not silently rename published or already-linked artifacts.
- Do not derive names from implementation details, branch names, or transient ticket text when an approved problem statement exists.
- Do not add type suffixes that conflict with the caller's canonical artifact contract.

## Requirements

Inputs the caller should provide when available:

- explicit artifact slug or preferred basename
- related prior artifact filename when revising existing work
- approved problem statement or concise artifact title
- target artifact type so the correct suffix can be applied by the calling contract

Output contract:

- one documented basename
- source of that name: explicit, reused, or derived
- normalized result ready for caller-owned composition

Resolution order:

1. explicit user-provided artifact name or slug
2. existing related artifact basename when continuing or revising prior work
3. concise title derived from the approved problem statement

Normalization requirements:

- convert to lowercase
- convert spaces and underscores to hyphens
- remove unsupported punctuation
- collapse repeated separators to one hyphen
- trim leading and trailing separators

## Workflow

1. Check for an explicit artifact slug or basename from the user or caller.
2. If none exists, inspect related artifacts and reuse the established basename when the task is a continuation or revision.
3. If no prior basename exists, derive a concise name from the approved problem statement.
4. Normalize the chosen value to lowercase kebab-case.
5. Return the basename plus its source so the caller can compose the final artifact name according to its own contract.
6. Reuse that same basename for future revisions of the same artifact family.

## Gotchas

- If you derive a fresh name for a revision instead of reusing the existing basename, links across stories, requirements, design, and plan files drift even though the work is the same. Reuse the prior basename first.
- If you pull the name from branch names or ticket IDs, you preserve tooling noise instead of problem meaning. Use explicit slug, then prior basename, then approved problem statement.
- If you strip too aggressively, distinct artifacts collapse into the same basename and later files overwrite each other semantically. Keep disambiguating tokens that carry intent.
- If you let each caller normalize differently, one artifact becomes `foo_bar`, another `foo-bar`, and a third `FooBar`. Normalize once with this contract before any suffix is added.
- If you silently rename an established artifact because a newer title sounds better, downstream references break and reviewers lose history. Preserve published names unless the user explicitly requests a rename migration.
- If you mix basename resolution with path, placement, or authoring decisions, callers start treating this skill as a document-placement workflow and duplicate naming logic elsewhere. Return the basename only.

## Deliverables

- A deterministic basename.
- A short note naming the source used: explicit, reused, or derived.
- A normalized value suitable for caller-owned composition.

## Validation Checklist

- Higher-precedence naming sources were checked before fallback derivation.
- The returned basename is lowercase kebab-case.
- Existing artifact basenames were preserved for revisions.
- The basename remains stable across the same artifact family.
- No path, placement, filename-selection, suffix, or authoring rules were mixed into this contract.
