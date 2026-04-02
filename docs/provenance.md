# Provenance And Traceability

Provenance and traceability are core concepts in `@urban/agent-skills-pack`.

The pack is designed to make specification artifacts reusable in both directions:

- from intent to implementation
- from an implemented system back to reusable specification artifacts

That only works when every created artifact carries deterministic metadata that explains:

- what produced it
- which supporting skills participated
- which upstream artifacts it depends on
- when it was created and updated

## Why Provenance And Traceability Matter

Without canonical provenance and lineage:

- artifacts cannot be validated consistently
- downstream skills cannot reliably determine whether inputs are complete
- reviewers cannot reconstruct how a document was produced
- reversibility degrades because artifact relationships become implicit or conversational
- plan and task artifacts lose their link back to approved scope and design

In this pack, provenance and traceability are not optional annotations. They are part of the artifact contract.

## The Foundational Skill

The foundational skill that owns this contract is:

- `skills/document-traceability/SKILL.md`

Use it whenever a skill creates or validates a charter, user stories, requirements, technical design, execution plan, or task-tracking artifact.

## Canonical Frontmatter

Created skill-pack artifacts must begin with canonical frontmatter:

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

Keep two concepts separate:

- `generated_by`
  How the artifact was produced.
- `source_artifacts`
  Which approved or inspected upstream artifacts it used.

## Required Lineage By Artifact Kind

Use exactly these `source_artifacts` roles:

- `charter`
  - `source_artifacts: {}`
- `user-stories`
  - `charter`
- `requirements`
  - `charter`
  - `user_stories`
- `technical-design`
  - `charter`
  - `user_stories`
  - `requirements`
- `plan`
  - `charter`
  - `user_stories`
  - `requirements`
  - `technical_design`
- `tasks`
  - `plan`

Do not add extra lineage roles casually. Determinism matters.

## Provenance Assembly Rules

Build provenance from the producing branch only.

That means:

- include the root orchestration skill
- include the direct producing skill
- include participating foundational skills from that branch
- exclude sibling expertise branches that did not participate in the specific artifact

Deterministic traversal order is:

1. root skill first
2. then depth-first traversal in declared dependency order
3. with duplicates removed from `skills_used`

`skill_graph` should be derived from the same participating set of skills.

Fail closed on:

- missing skill files
- missing declared dependencies
- malformed metadata
- dependency cycles

## Workflow Expectation

When creating an artifact:

1. identify the artifact kind
2. identify the root workflow and direct producing skill
3. collect the producing branch skill dependencies
4. stamp canonical frontmatter before final validation
5. record exactly the required `source_artifacts` roles
6. run the shared provenance validator
7. do not emit the artifact if provenance validation fails

## Validation

The shared validator is:

- `skills/document-traceability/scripts/validate_frontmatter_provenance.sh`

Usage:

```bash
bash skills/document-traceability/scripts/validate_frontmatter_provenance.sh <artifact-kind> <artifact-file>
```

Most `write-*` validators in the pack already invoke this shared provenance validator.

## Where This Should Be Enforced

Provenance and traceability should be applied across:

- authored specification artifacts under `.specs/<project-name>/`
- execution coordination artifacts under `.specs/<project-name>/`
- reconstructed research artifacts under `.specs/<project-name>-research/` whenever they are created through the pack's canonical artifact contracts

If a skill creates one of these artifacts, it should either:

- depend on `document-traceability`, or
- use a foundational contract that explicitly requires the canonical frontmatter and validator

Prefer the explicit dependency when the skill itself stamps or validates provenance.

## Design Intent

This repo optimizes for reversible specification systems. Provenance and traceability are what let a reviewer or another agent answer:

- Where did this artifact come from?
- Which workflow created it?
- Which shared contracts shaped it?
- Which upstream artifacts did it depend on?
- Can this artifact be trusted as a valid input for the next stage?

If those questions cannot be answered from the artifact itself, the pack has lost one of its core guarantees.
