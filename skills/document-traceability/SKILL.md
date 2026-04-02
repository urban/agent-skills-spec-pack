---
name: document-traceability
description: Define canonical authored-document frontmatter, deterministic skill provenance, source artifact lineage, and shared provenance validation for authored spec-pack artifacts. Use when a skill writes or validates charter, user stories, requirements, technical design, execution plans, or task-tracking artifacts.
metadata:
  version: 0.1.0
  layer: foundational
---

## Rules

- Use one canonical frontmatter contract for authored spec-pack artifacts because downstream validation and feedback depend on deterministic metadata.
- Keep skill provenance separate from source artifact lineage because one explains how the artifact was produced and the other explains what approved inputs it used.
- Compute provenance only from the artifact-producing skill branch because sibling orchestration branches are not part of one artifact's generation path.
- Treat provenance failures as hard failures because partial or guessed metadata breaks traceability.
- Use UTC ISO 8601 timestamps with a trailing `Z` because authored artifacts need stable machine-checkable time values.

## Canonical Frontmatter

Every authored spec-pack artifact must begin with:

```yaml
---
name: <artifact-name>
created_at: <UTC ISO 8601 timestamp>
updated_at: <UTC ISO 8601 timestamp>
generated_by:
  root_skill: <top-level orchestration skill>
  producing_skill: <direct artifact-producing skill>
  skills_used:
    - <ordered participating skills>
  skill_graph:
    <skill-name>:
      - <declared dependency>
source_artifacts:
  <role>: <path>
---
```

For charter artifacts, use `source_artifacts: {}`.

## Provenance Assembly

- `root_skill` is the orchestration skill that initiated authored generation.
- `producing_skill` is the direct role skill responsible for the artifact.
- `skills_used` is the ordered, deduplicated skill list from the producing branch only.
- `skill_graph` is the adjacency map derived from each participating skill's declared `metadata.dependencies`.
- traversal order is deterministic: root skill first, then depth-first traversal in declared dependency order.
- include participating foundational skills such as `artifact-naming`, `document-traceability`, and the relevant `write-*` contract skill.
- exclude sibling role branches that did not participate in the specific artifact.
- fail closed on missing skill files, missing declared dependencies, malformed metadata, or dependency cycles.

## Source Artifact Roles

Required `source_artifacts` roles by artifact kind:

- `charter`: `{}`
- `user-stories`: `charter`
- `requirements`: `charter`, `user_stories`
- `technical-design`: `charter`, `user_stories`, `requirements`
- `plan`: `charter`, `user_stories`, `requirements`, `technical_design`
- `tasks`: `plan`

## Workflow

1. Identify the artifact kind and its direct producing skill.
2. Establish the `root_skill` from the authored workflow that initiated the run.
3. Walk the producing skill branch from `SKILL.md` metadata dependencies only.
4. Build `skills_used` in deterministic traversal order with duplicates removed.
5. Build `skill_graph` from the same participating skills.
6. Record only the required `source_artifacts` roles for the artifact kind.
7. Stamp canonical frontmatter before final validation.
8. Validate with [`scripts/validate_frontmatter_provenance.sh`](./scripts/validate_frontmatter_provenance.sh).
9. If validation fails, stop and do not emit the artifact.

## Gotchas

- If source artifact lineage is copied into `generated_by`, provenance stops explaining the skill chain and becomes noisy. Keep the two concerns separate.
- If sibling orchestration branches appear in `skills_used`, the metadata becomes non-deterministic across artifact kinds. Keep traversal on the producing branch only.
- If timestamps use date-only values or local time, machines cannot tell whether metadata is canonical. Use UTC ISO 8601 with `Z`.
- If charter uses an empty multiline map instead of `source_artifacts: {}`, validators cannot distinguish deliberate emptiness from omission. Use the explicit empty map form.
- If a skill is used but missing from `skill_graph`, downstream reviewers cannot reconstruct provenance deterministically. Keep `skills_used` and `skill_graph` aligned.

## Deliverables

- canonical authored-document frontmatter contract
- deterministic provenance assembly rules
- required source-artifact role map by artifact kind
- shared provenance validator script

## Deterministic Validation

- `bash scripts/validate_frontmatter_provenance.sh <artifact-kind> <artifact-file>`
