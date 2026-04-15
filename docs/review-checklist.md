# Review checklist

Use this checklist before shipping a new or changed skill.

## 1. Runtime composition

Confirm that:

- the `description` makes the skill easy to select at runtime
- the `description` states stable ownership rather than today's workflow implementation details
- runtime use does not depend on the reader already knowing the full package graph
- the skill has clear boundaries
- another agent could choose it without reading unrelated skills first
- helper or support skills that should not appear in skill installers are marked `metadata.internal: true`
- `metadata.internal: true` is not described as changing dependency resolution, packaging, or runtime behavior
- the `description` follows [skill-descriptions.md](./skill-descriptions.md)

## 2. Layer and boundary checks

Confirm that:

- the skill fits exactly one layer
- foundational skills define reusable leaf contracts and validation
- specialist skills apply those contracts within one bounded artifact or analysis/planning job
- coordination skills own workflow-wide coordination without restating shared contract rules
- child skills do not know parent workflow framing
- planning does not redefine requirements
- requirements do not become technical design
- reconstruction does not invent intent

## 3. Contract checks

If the skill works with a shared artifact type, confirm that:

- section order matches the canonical contract
- naming matches the canonical contract
- validation matches the canonical contract
- canonical provenance and `source_artifacts` are applied on create
- workflow-level lineage expectations come from coordination rather than foundational or specialist contracts
- uncertainty is explicit for reconstruction outputs
- workflows with approval checkpoints generate approval views from canonical artifacts only
- approval views live under `<spec-pack-root>/approval/`, are validated, and are regenerated after canonical changes
- approved artifacts do not still contain `TODO: Confirm`

Prefer reusing a `write-*` skill over copying its rules.

## 4. Path and ownership checks

Confirm that:

- foundational owns `<project-name>` derivation and normalization
- coordination owns spec-pack root selection and workflow-wide output defaults
- specialist owns the artifact filename for the output it produces
- same-pack dependencies in specialist skills use pack-relative paths when appropriate
- specialist does not hardcode root workflow identity

## 5. Reuse checks

Confirm that:

- the skill has one clear responsibility
- the owned output is explicit
- install-time dependencies are declared when packaging requires them
- another coordination could reuse the skill unchanged

## 6. Agent-use checks

Prefer:

- deterministic filenames
- canonical frontmatter for created artifacts
- explicit headings
- concise instructions
- direct workflow order
- local validation commands

Avoid vague prose, hidden assumptions, and formats that require structure inference.

## 7. Reconstruction checks

For reconstruction-heavy skills, confirm that:

- code, tests, config, and repo structure are primary evidence
- implemented reality is described instead of imagined intent
- weak conclusions are marked explicitly
- approval views surface low-confidence claims, weak evidence, and inferred-versus-observed distinctions when the workflow uses approval checkpoints
- compatibility with the authored contract is preserved when the artifact type is shared

## 8. Final decision

A skill is usually ready to ship when:

- its ownership is narrow
- its dependencies respect the layer model
- its artifact contract is stable
- its provenance is valid
- another human or agent could use it without private context
