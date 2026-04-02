# Composability Checklist

Use this document before finalizing a new or updated skill.

## Runtime Composition Checks

Confirm:

- the skill can be selected at runtime from its `description`, especially its `Use when ...` trigger
- runtime use does not depend on `metadata.dependencies`
- the skill has clear boundaries without tightly coupling itself to one workflow
- another agent can choose this skill without already knowing the rest of the package graph

Prefer loose composition through strong descriptions, bounded outputs, and explicit contracts.

Avoid using install-time dependencies as runtime routing hints.

## Boundary Checks

Confirm the skill keeps these responsibilities separate:

- foundational skills define shared contracts and validation
- role skills apply those contracts within one bounded responsibility
- orchestration skills orchestrate role entry skills without restating contract rules

Planning must not redefine requirements.
Requirements must not become technical design.
Reconstruction must not silently invent intent.

## Contract Checks

If the skill participates in a shared artifact type, confirm:

- section order matches the canonical contract
- naming rules match the canonical contract
- validation rules match the canonical contract
- uncertainty handling is explicit where reconstruction is involved

Prefer building or reusing a `write-*` contract skill instead of duplicating rules.

## Reuse Checks

Confirm:

- the foundational skill has one clear responsibility
- the owned output is explicit
- install-time dependencies are declared instead of inlined when packaging truly requires them
- another orchestration could reuse it without modification

Do not use `metadata.dependencies` to force runtime composition. Runtime composition should come from skill descriptions and clear scope.

## Agent-Use Checks

Prefer:

- deterministic filenames
- explicit headings
- concise instructions
- direct workflow order
- local validation commands

Avoid vague prose, hidden assumptions, and output formats that require an LLM to infer structure.

## Reconstruction Checks

For reconstruction or inference-heavy skills, confirm:

- code, tests, config, and repository structure are treated as primary evidence
- implemented reality is described instead of imagined original intent
- weakly supported conclusions are marked explicitly
- compatibility with the authored artifact contract is preserved where the artifact type is shared
