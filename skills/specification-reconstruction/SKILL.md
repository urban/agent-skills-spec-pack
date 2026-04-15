---
name: specification-reconstruction
description: "Orchestrate reconstruction of a specification pack from repository evidence. Use when a user needs charter, user-stories, requirements, and technical-design artifacts recovered from an existing system."
license: MIT
metadata:
  version: "0.3.2"
  author: "urban (https://github.com)"
  layer: coordination
  dependencies:
    - document-traceability
    - artifact-naming
    - write-approval-view
    - derive-charter
    - derive-user-stories
    - derive-requirements
    - derive-technical-design
---

## Purpose

Coordinate reconstruction of a specification pack from repository evidence into one stable reconstruction root. Keep evidence-first workflow order, provenance, lineage, constraint reconciliation, uncertainty handling, and pack-level consistency explicit while specialist skills own the artifact contracts.

## Workflow rules

- Root workflow identity: `specification-reconstruction`
- Workflow source of truth: repository code, tests, configs, manifests, entrypoints, schemas, parsers, runtime wiring, and other in-scope evidence; stronger repository evidence wins over reconstructed framing
- Resolve one stable `<project-name>` and one stable reconstruction spec-pack root for the full run; default root: `.specs/<project-name>-reconstructed/`
- Use specialist skills in this order: `derive-charter` -> `derive-user-stories` -> `derive-requirements` -> `derive-technical-design`
- Build two working inventories before downstream derivation: one user-visible behavior inventory and one implementation-constraint inventory
- Reconcile stronger source-backed findings from technical design back into requirements when needed
- Make exclusions explicit when implemented surfaces stay outside the chosen scope
- Keep deterministic provenance and the workflow-owned `source_artifacts` map on every reconstructed artifact
- This workflow coordinates reconstruction; it does not replace child reconstruction contracts
- Ask when ambiguity changes scope, destination, artifact shape, evidence threshold, lineage, approval rules, or another blocking category

## Source artifact lineage

Use this exact workflow-owned `source_artifacts` map:

- `charter.md` -> `{}`
- `user-stories.md` -> `charter`
- `requirements.md` -> `charter`, `user_stories`
- `technical-design.md` -> `charter`, `user_stories`, `requirements`

Resolved reconstructed paths normally are:

- `charter` -> `<spec-pack-root>/charter.md`
- `user_stories` -> `<spec-pack-root>/user-stories.md`
- `requirements` -> `<spec-pack-root>/requirements.md`

Do not add extra source-artifact keys casually.

## Inputs

- repository source code
- tests, configs, manifests, runtime entrypoints, command definitions, schemas, parsers, runtime wiring, and docs when present
- optional user-provided analysis scope
- optional user-provided output destinations
- optional explicit artifact slug or preferred basename
- clarification only when ambiguity materially changes reconstruction

## Outputs

- default canonical outputs at `.specs/<project-name>-reconstructed/{charter.md,user-stories.md,requirements.md,technical-design.md}` when the user does not override destinations
- derived approval views under `<spec-pack-root>/approval/` for requested review checkpoints and final pack review, in Markdown and HTML
- one reconstructed specification pack grounded in repository evidence
- one explicit user-visible behavior inventory and one explicit implementation-constraint inventory used during reconstruction
- explicit uncertainty and confidence markers where the evidence stays weak

## Workflow

1. Confirm the user needs reconstruction from repository evidence, then resolve analysis scope, one `<project-name>`, and one reconstruction spec-pack root for the full run.
2. Establish `generated_by.root_skill = specification-reconstruction` and the workflow-owned approval output location under `<spec-pack-root>/approval/`.
3. Inspect in-scope repository evidence, prioritizing code, tests, configs, manifests, entrypoints, command surfaces, schemas, parser logic, runtime wiring, integrations, and lifecycle behavior.
4. Build a user-visible behavior inventory and an implementation-constraint inventory before deriving downstream artifacts.
5. Run `derive-charter`, write `<spec-pack-root>/charter.md`, validate, and review whether the recovered framing stays inside the evidence boundary.
6. Run `derive-user-stories`, write `<spec-pack-root>/user-stories.md`, stamp `source_artifacts.charter`, validate, and review whether stories reflect observable behavior rather than desired future behavior.
7. Run `derive-requirements`, write `<spec-pack-root>/requirements.md`, stamp `source_artifacts.charter` and `source_artifacts.user_stories`, validate, and confirm the reconstructed contract captures high-impact implementation constraints without collapsing into architecture prose.
8. Run `derive-technical-design`, write `<spec-pack-root>/technical-design.md`, stamp `source_artifacts.charter`, `source_artifacts.user_stories`, and `source_artifacts.requirements`, validate, and confirm the as-built design names source-backed runtime, boundary, validation, lifecycle, and failure constraints.
9. Reconcile stronger technical-design findings back into `requirements.md` when the implementation-constraint inventory shows missing high-impact `NFR`, `TC`, `DR`, `IR`, or `DEP` items.
10. Run the final cross-artifact consistency pass across evidence support, reconstructed framing, story behavior, requirement families, design fidelity, exclusions, provenance, lineage, confidence, and remaining uncertainty.
11. Generate and validate requested per-artifact approval views, and always generate and validate the final pack approval view under `<spec-pack-root>/approval/pack.{md,html}` for review.
12. Deliver the reconstructed pack for documentation recovery, planning, or downstream change work.

## Approval flow

- When this run includes human approval checkpoints, generate or refresh the per-artifact approval view for the exact current canonical snapshot before asking for approval.
- Always generate the final pack approval view after the consistency pass.
- Approval of a derived approval view counts as approval of the exact canonical snapshot it was derived from.
- Any canonical artifact change invalidates prior approval for that artifact and requires a regenerated approval view.
- Approval is whole-artifact only.
- No artifact may be approved while any `TODO: Confirm` remains.
- If a checkpointed artifact is not approved, revise that canonical artifact, regenerate its approval view, and rerun any affected downstream consistency checks before treating it as approved.
- If final pack review fails, revise the affected canonical artifact(s), rerun consistency checks, and regenerate the affected approval views plus the final pack approval view.
- Approval views must derive from the canonical artifact only, persist under `<spec-pack-root>/approval/` in Markdown and HTML, and trace substantive claims back to exact canonical locations.
- When asking for approval on an HTML review surface in the terminal, include the resolved HTML path and the matching absolute `file://` URI for that file.
- Reconstruction approval views must surface overall confidence, low-confidence claims, weak evidence, and inferred-versus-observed distinctions prominently.

## Validation

- Confirm one stable `<project-name>` and one stable reconstruction spec-pack root are used across the pack.
- Confirm the user-visible behavior inventory and implementation-constraint inventory exist during reconstruction.
- Confirm derived `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` exist at the chosen destinations.
- Confirm every reconstructed artifact records `generated_by.root_skill = specification-reconstruction`.
- Confirm exact `source_artifacts` keys and resolved paths match this workflow's lineage map.
- Confirm high-impact runtime, parser, validation, integration, lifecycle, dependency, and operator-visible constraints appear in `requirements.md` or `technical-design.md`, and stronger technical-design findings are reconciled back into requirements when needed.
- Confirm excluded implemented surfaces are called out explicitly when they stay out of scope.
- Confirm requested approval checkpoints use fresh approval views for the current canonical snapshots, and final pack review has a fresh pack approval view.
- Confirm each approval view passed `bash ../write-approval-view/scripts/validate_approval_view.sh ...` with the correct mode.
- Confirm weakly supported conclusions remain explicit through confidence markers or `TODO: Confirm`, and contradictions across derived artifacts are resolved or surfaced.

## References

- [`./references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: reconstruction finds a probable architectural seam that needs bounded gray-box follow-on analysis.
