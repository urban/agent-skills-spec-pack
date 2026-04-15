---
name: document-traceability
description: "Define canonical provenance and source-artifact lineage for package artifacts. Use when a skill creates or validates a package artifact that must carry deterministic frontmatter metadata."
license: MIT
metadata:
  version: "0.2.1"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared frontmatter contract for package artifacts: canonical provenance fields, deterministic provenance assembly, `source_artifacts` field shape, and fail-closed validation.

## Contract

- Every package artifact begins with canonical frontmatter containing:
  - `name`
  - `created_at`
  - `updated_at`
  - `generated_by.root_skill`
  - `generated_by.producing_skill`
  - `generated_by.skills_used`
  - `generated_by.skill_graph`
  - `source_artifacts`
- Timestamps use UTC ISO 8601 with trailing `Z`.
- Keep skill provenance separate from source-artifact lineage.
- Provenance assembly rules:
  - `root_skill` is the coordination skill that initiated the run
  - `producing_skill` is the direct artifact-producing skill
  - `skills_used` is the ordered, deduplicated skill list from the producing branch only
  - `skill_graph` is the adjacency map from each participating skill's declared `metadata.dependencies`
  - traversal order is deterministic: root first, then depth-first in declared dependency order
  - include only participating skills from the producing branch
  - fail closed on missing skill files, missing declared dependencies, malformed metadata, or dependency cycles
- `source_artifacts` rules:
  - this skill defines field shape and validation expectations
  - coordination owns which artifact-type keys must be present for each workflow
  - use `source_artifacts: {}` when the active workflow requires an empty lineage map

## Inputs

- artifact kind
- direct producing skill
- root coordination skill
- participating skill metadata from the producing branch
- workflow-owned `source_artifacts` keys and resolved paths

## Outputs

- canonical frontmatter contract for package artifacts
- deterministic provenance assembly rules
- canonical `source_artifacts` field shape
- shared validator at `./scripts/validate_frontmatter_provenance.sh`

## Workflow

1. Identify the artifact kind and direct producing skill.
2. Establish the `root_skill` from the coordination workflow that initiated the run.
3. Walk the producing branch from declared `metadata.dependencies` only.
4. Build `skills_used` in deterministic traversal order with duplicates removed.
5. Build `skill_graph` from the same participating skills.
6. Record the `source_artifacts` keys required by the active coordination workflow.
7. Stamp canonical frontmatter before final validation.
8. Validate with `bash ./scripts/validate_frontmatter_provenance.sh <artifact-kind> <artifact-file>`.
9. If validation fails, stop and do not emit the artifact.

## Validation

- Run: `bash ./scripts/validate_frontmatter_provenance.sh <artifact-kind> <artifact-file>`
- Confirm provenance is computed from the producing branch only.
- Confirm `skills_used` and `skill_graph` stay aligned.
- Confirm timestamps use UTC ISO 8601 with `Z`.
- Confirm `source_artifacts` keys come from coordination, and `{}` is used only when the workflow requires explicit emptiness.
