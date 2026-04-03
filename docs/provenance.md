# Provenance and traceability

Provenance and traceability are core parts of `agent-skills-pack`.

The pack only stays reversible when every created artifact says:

- what produced it
- which skills participated
- which upstream artifacts it used
- when it was created and updated

## Why this matters

Without canonical provenance and lineage:

- artifacts cannot be validated consistently
- downstream skills cannot reliably check inputs
- reviewers cannot reconstruct how a document was produced
- reversibility degrades because relationships become implicit
- plans and tasks lose their link to approved scope and design

In this pack, provenance and traceability are part of the artifact contract.

## Foundational skill

This contract is owned by:

- `skills/document-traceability/SKILL.md`

Use it whenever a skill creates or validates a charter, user stories, requirements, technical design, execution plan, or task-tracking artifact.

## Canonical frontmatter

Created artifacts must begin with this shape:

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

Use UTC ISO 8601 timestamps with a trailing `Z`.

Keep these separate:

- `generated_by` — how the artifact was produced
- `source_artifacts` — which upstream artifacts shaped it

Skill contracts may describe same-pack dependencies using pack-relative paths, but canonical provenance must continue recording resolved artifact paths in `source_artifacts`.

## Required lineage ownership

Canonical provenance must record the exact `source_artifacts` roles required by the active orchestration workflow.

Use these rules:

- orchestration owns canonical lineage expectations for artifacts in its workflow
- expertise may use same-pack sibling artifacts as local context, but should not define workflow-level lineage policy
- foundational provenance defines the metadata shape and validation flow, not which artifact kinds require which lineage roles

Do not add extra lineage roles casually.

## Provenance assembly rules

Build provenance from the producing branch only:

- include the root orchestration skill
- include the direct producing skill
- include participating foundational skills from that branch
- exclude sibling expertise branches that did not participate

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

## Workflow expectation

When creating an artifact:

1. identify the artifact kind
2. identify the root workflow and direct producing skill
3. collect dependencies from the producing branch
4. stamp canonical frontmatter before final validation
5. record exactly the required `source_artifacts` roles
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

## Where this applies

Apply provenance and traceability to:

- authored artifacts under `.specs/<project-name>/`
- execution artifacts under `.specs/<project-name>/`
- reconstructed artifacts under `.specs/<project-name>-research/` when created through the pack's canonical contracts

If a skill creates one of these artifacts, it should either:

- depend on `document-traceability`, or
- use a foundational contract that already requires the canonical frontmatter and validator

Prefer the explicit dependency when the skill itself stamps or validates provenance.

## Design intent

A valid artifact should answer:

- Where did this come from?
- Which workflow created it?
- Which shared contracts shaped it?
- Which upstream artifacts did it use?
- Can the next skill trust it as input?

If it cannot, the pack has lost one of its core guarantees.
