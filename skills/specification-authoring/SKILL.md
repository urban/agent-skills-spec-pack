---
name: specification-authoring
description: "Orchestrate authored specification packs from approved product framing. Use when a user needs a coordinated charter, user-stories, requirements, and technical-design pack created for a new product or major feature."
license: MIT
metadata:
  version: "0.2.2"
  author: "urban (https://github.com)"
  layer: coordination
  dependencies:
    - document-traceability
    - artifact-naming
    - write-approval-view
    - charter
    - user-story-authoring
    - requirements
    - technical-design
---

## Purpose

Coordinate authored specification work from approved product framing into one stable spec-pack root. Keep workflow order, approval gates, provenance, lineage, and pack-level consistency explicit while specialist skills own the artifact contracts.

## Workflow rules

- Root workflow identity: `specification-authoring`
- Workflow source of truth: approved product framing, then the approved upstream canonical artifacts produced earlier in this workflow
- Resolve one stable `<project-name>` and one stable authored spec-pack root for the full run; default root: `.specs/<project-name>/`
- Use specialist skills in this order: `charter` -> `user-story-authoring` -> `requirements` -> `technical-design`
- Downstream canonical artifacts may not be emitted or presented before upstream approval
- Keep deterministic provenance and the workflow-owned `source_artifacts` map on every authored artifact
- This workflow coordinates artifacts; it does not replace child artifact contracts
- Ask when ambiguity changes scope, artifact shape, lineage, approval rules, software quality, or another blocking category

## Source artifact lineage

Use this exact workflow-owned `source_artifacts` map:

- `charter.md` -> `{}`
- `user-stories.md` -> `charter`
- `requirements.md` -> `charter`, `user_stories`
- `technical-design.md` -> `charter`, `user_stories`, `requirements`

Resolved authored paths normally are:

- `charter` -> `<spec-pack-root>/charter.md`
- `user_stories` -> `<spec-pack-root>/user-stories.md`
- `requirements` -> `<spec-pack-root>/requirements.md`

Do not add extra source-artifact keys casually.

## Inputs

- product idea, feature request, or approved problem statement
- desired outcomes, goals, and scope boundaries
- repository context when existing code, integrations, or constraints matter
- optional explicit authored destination root
- optional explicit artifact slug or preferred basename
- clarification only when ambiguity materially changes the pack

## Outputs

- `<spec-pack-root>/charter.md`
- `<spec-pack-root>/user-stories.md`
- `<spec-pack-root>/requirements.md`
- `<spec-pack-root>/technical-design.md`
- derived approval views under `<spec-pack-root>/approval/` for each artifact checkpoint and the final pack, in Markdown and HTML
- one authored specification pack ready for approval or downstream coordination

## Workflow

1. Confirm the user needs authored specification work, then resolve one `<project-name>` and one authored spec-pack root for the full run.
2. Establish `generated_by.root_skill = specification-authoring` and the workflow-owned approval output location under `<spec-pack-root>/approval/`.
3. Co-create or confirm goals, non-goals, actors, success criteria, and scope boundaries needed for the charter.
4. Run `charter`, write `<spec-pack-root>/charter.md`, validate provenance and artifact contract, generate and validate the derived approval view, and wait for explicit approval of that snapshot before continuing.
5. Run `user-story-authoring`, write `<spec-pack-root>/user-stories.md`, stamp `source_artifacts.charter`, validate, generate and validate the derived approval view, and wait for explicit approval before continuing.
6. Run `requirements`, write `<spec-pack-root>/requirements.md`, stamp `source_artifacts.charter` and `source_artifacts.user_stories`, validate, generate and validate the derived approval view, and wait for explicit approval before continuing.
7. Run `technical-design`, write `<spec-pack-root>/technical-design.md`, stamp `source_artifacts.charter`, `source_artifacts.user_stories`, and `source_artifacts.requirements`, validate, generate and validate the derived approval view, and wait for explicit approval before continuing.
8. Run the final cross-artifact consistency pass across scope, actors, stories, requirements, design, provenance, lineage, and remaining uncertainty.
9. Generate and validate the final pack approval view under `<spec-pack-root>/approval/pack.{md,html}`.
10. Deliver the authored pack for final review or downstream coordination.

## Approval flow

- Approval must be explicit in the conversation.
- Silence, implied satisfaction, or a request to keep going does not count as approval.
- Approval of a derived approval view counts as approval of the exact canonical snapshot it was derived from.
- Any canonical artifact change invalidates prior approval for that artifact and requires a regenerated approval view.
- Approval is whole-artifact only.
- No artifact may be approved while any `TODO: Confirm` remains.
- If an artifact is not approved, revise that canonical artifact, regenerate its approval view, and repeat the same gate before continuing downstream.
- If final pack review fails, revise the affected canonical artifact(s), rerun consistency checks, and regenerate the affected approval views plus the final pack approval view.
- Persist per-artifact approval views and the final pack approval view under `<spec-pack-root>/approval/` in both Markdown and HTML.
- When asking for approval on an HTML review surface in the terminal, include the resolved HTML path and the matching absolute `file://` URI for that file.
- Approval views must derive from the canonical artifact only and trace substantive claims back to exact canonical locations.

## Validation

- Confirm one stable `<project-name>` and one stable authored spec-pack root are used across the pack.
- Confirm `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` exist in the chosen root.
- Confirm every authored artifact records `generated_by.root_skill = specification-authoring`.
- Confirm exact `source_artifacts` keys and resolved paths match this workflow's lineage map.
- Confirm each artifact passed its validator before its approval view was generated.
- Confirm each approval view passed `bash ../write-approval-view/scripts/validate_approval_view.sh ...` with the correct mode.
- Confirm each approval checkpoint used a fresh approval view for the current canonical snapshot and no approved artifact still contains `TODO: Confirm`.
- Confirm charter scope and actors support the stories, stories support requirements, requirements support design, and contradictions are resolved or surfaced.
