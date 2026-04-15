# Provenance and traceability

Provenance is part of the artifact contract. The package only stays reversible if every created artifact records how it was produced and which upstream artifacts shaped it.

A valid artifact should answer these questions:

- What produced this file?
- Which skills participated?
- Which upstream artifacts shaped it?
- When was it created and last updated?
- Can a downstream skill trust it as input?

## Owning skill

The shared provenance contract is owned by:

- `skills/document-traceability/SKILL.md`

Use it whenever a skill creates or validates one of the package's canonical artifacts.

## Canonical frontmatter

Created artifacts must begin with this shape:

```yaml
---
name: <artifact-name>
created_at: <UTC ISO 8601 timestamp>
updated_at: <UTC ISO 8601 timestamp>
generated_by:
  root_skill: <top-level coordination skill>
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

Rules:

- Use UTC ISO 8601 timestamps with a trailing `Z`.
- Keep `generated_by` and `source_artifacts` separate.
- `generated_by` records how the artifact was produced.
- `source_artifacts` records which upstream artifacts shaped the result.
- Skill contracts may describe same-pack dependencies with pack-relative paths, but canonical provenance must record resolved artifact paths in `source_artifacts`.

## Ownership of lineage policy

Lineage policy has separate owners.

| Concern | Owner |
| --- | --- |
| frontmatter shape | foundational provenance contract |
| provenance assembly mechanics | foundational provenance contract |
| direct production step | specialist |
| root workflow identity | coordination |
| canonical `source_artifacts` expectations for a workflow | coordination |

Follow these rules:

- coordination owns the canonical lineage map for artifacts in its workflow
- specialist may use same-pack sibling artifacts as local context, but should not define workflow-wide lineage policy
- foundational provenance defines the metadata shape and validation flow, not which artifact kinds require which source artifact types
- specialist should not hardcode `generated_by.root_skill`

Do not add extra source artifact types casually.

## Provenance assembly rules

Build provenance from the producing branch only.

Include:

- the root coordination skill
- the direct producing skill
- participating foundational skills from that branch

Exclude:

- sibling specialist branches that did not participate

Traversal order:

1. root skill first
2. then depth-first in declared dependency order
3. remove duplicates from `skills_used`

Derive `skill_graph` from the same participating set.

Fail closed on:

- missing skill files
- missing declared dependencies
- malformed metadata
- dependency cycles

## Workflow for creating an artifact

When a skill creates an artifact:

1. identify the artifact kind
2. identify the root workflow and direct producing skill
3. collect dependencies from the producing branch
4. stamp canonical frontmatter before final validation
5. record exactly the required `source_artifacts` keys
6. run the shared provenance validator
7. do not emit the artifact if validation fails

## Validation

Shared validator:

- `skills/document-traceability/scripts/validate_frontmatter_provenance.sh`

Usage:

```bash
bash skills/document-traceability/scripts/validate_frontmatter_provenance.sh <artifact-kind> <artifact-file>
```

Most `write-*` validators already call it.

## Where the contract applies

Apply canonical provenance and traceability to:

- authored artifacts under `.specs/<project-name>/`
- execution artifacts under `.specs/<project-name>/`
- reconstructed artifacts under `.specs/<project-name>-reconstructed/` when created through the package's canonical contracts

Do not apply this frontmatter contract to derived approval views under `<spec-pack-root>/approval/`. Approval views are secondary review surfaces with no canonical frontmatter; validate them with the shared approval-view contract instead. See [approval-views.md](./approval-views.md).

If a skill creates one of these artifacts, it should either:

- depend on `document-traceability`, or
- use a lower-layer contract that already enforces the canonical frontmatter and validator

## Typical lineage expectations

Workflow-specific lineage belongs to coordination, but these examples show the common pattern:

- charter -> `{}`
- user stories -> `charter`
- requirements -> `charter`, `user_stories`
- technical design -> `charter`, `user_stories`, `requirements`
- execution plan -> `charter`, `user_stories`, `requirements`, `technical_design`
- execution tasks -> `plan`

Treat this as a common shape, not a reason to move lineage ownership out of coordination.
