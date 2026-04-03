---
name: specification-reconstruction
description: Orchestrate reconstruction of a specification pack from an existing codebase. Use when a user wants charter, user stories, requirements, and technical design recovered from implemented software.
metadata:
  version: 0.1.0
  layer: orchestration
  dependencies:
    - artifact-naming
    - derive-charter
    - derive-user-stories
    - derive-requirements
    - derive-technical-design
---

## Rules

- Treat repository evidence as the primary source of truth because this workflow reconstructs implemented reality, not intended history.
- Keep this workflow at the orchestration layer because expertise skills own artifact-specific reconstruction methods and validation.
- Use `artifact-naming` to resolve one stable `<project-name>` for the workflow because reconstructed artifacts must align to one reconstruction spec-pack root.
- Use `.specs/<project-name>-research/` as the default reconstruction spec-pack root unless the user provides explicit destinations.
- Establish `generated_by.root_skill` as `specification-reconstruction` for every artifact emitted from this workflow.
- Keep uncertainty explicit with `TODO: Confirm` whenever the codebase cannot prove original intent.
- Run reconstruction in order because derived charter captures recoverable framing, derived stories capture user-visible behavior, derived requirements capture the contract, and derived design explains the implementation.
- Use local gray-box routing only when repository evidence suggests an architectural seam that needs bounded follow-on analysis outside this workflow.

## Constraints

- This workflow coordinates reconstruction; it does not replace underlying expertise or foundational contracts.
- Final output must include reconstructed `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md`.
- Orchestration must use expertise skills for artifact-producing work and may use `artifact-naming` only for workflow-wide naming and placement coordination.
- If a user asks for a reconstructed execution plan, frame it as current-state guidance rather than pretending to recover the original authored plan.
- Every reconstructed artifact must carry deterministic provenance rooted in this workflow plus the canonical `source_artifacts` lineage required by this workflow.

## Source Artifact Lineage

Use exactly these `source_artifacts` roles in this workflow:

- `charter.md` -> `{}`
- `user-stories.md` -> `charter`
- `requirements.md` -> `charter`, `user_stories`
- `technical-design.md` -> `charter`, `user_stories`, `requirements`

Do not add extra lineage roles casually.

## Requirements

Inputs:

- repository source code
- tests, configs, and docs when present
- optional user-provided analysis scope
- optional user-provided output destinations
- optional explicit artifact slug or preferred basename
- clarification only when the requested scope or output shape is ambiguous

Default outputs when the user does not provide explicit destinations:

- `.specs/<project-name>-research/charter.md`
- `.specs/<project-name>-research/user-stories.md`
- `.specs/<project-name>-research/requirements.md`
- `.specs/<project-name>-research/technical-design.md`

Additional outputs:

- one reconstructed pack grounded in repository evidence
- explicit uncertainty markers where the codebase cannot prove original intent

In scope:

- resolving one workflow-wide `<project-name>` with `artifact-naming`
- selecting and preserving one reconstruction spec-pack root for the workflow
- orchestrating expertise entry skills for reconstruction
- checking that derived artifacts support each other
- establishing root workflow provenance and canonical `source_artifacts` lineage for every reconstructed artifact
- routing bounded gray-box follow-on discovery when needed

Out of scope:

- inventing business intent the repository does not support
- presenting guesses as recovered facts
- replacing expertise-level reconstruction contracts with workflow prose
- treating current-state recommendations as the original plan

## Workflow

1. Confirm the repository scope to analyze, defaulting to the whole repository when the user does not narrow it.
2. Resolve `<project-name>` once with `artifact-naming`, honoring an explicit artifact slug or preferred basename when provided.
3. Resolve the reconstruction spec-pack root once for the full run, defaulting to `.specs/<project-name>-research/` unless the user provides explicit destinations.
4. Establish `root_skill = specification-reconstruction` for all reconstructed artifacts in this run.
5. Inspect repository evidence relevant to the chosen scope, prioritizing source, tests, configs, and existing docs.
6. Run `derive-charter`, write the result to `<spec-pack-root>/charter.md`, and review whether the inferred goals, non-goals, personas, and success criteria stay within what the codebase can plausibly support.
7. Run `derive-user-stories`, write the result to `<spec-pack-root>/user-stories.md`, and review whether the inferred outcomes reflect observable behavior rather than desired future behavior.
8. Run `derive-requirements`, write the result to `<spec-pack-root>/requirements.md`, and confirm the reconstructed contract stays supported by repository evidence and does not silently re-own charter content.
9. Run `derive-technical-design`, write the result to `<spec-pack-root>/technical-design.md`, and confirm the as-built design explains the derived requirements without speculating beyond the codebase.
10. Read [`references/gray-box-routing.md`](./references/gray-box-routing.md) only when the reconstruction pass finds a probable architectural seam that needs bounded follow-on analysis.
11. Perform a cross-artifact consistency pass:
   - derived `charter.md` is supported by observable behavior and constraints
   - derived `user-stories.md` fits the derived personas and implied scope boundaries
   - derived `requirements.md` is supported by repository evidence and aligns to derived stories
   - derived `technical-design.md` explains the implemented system
   - every reconstructed artifact carries canonical provenance and the `source_artifacts` roles required by this workflow
   - weakly supported conclusions remain marked `TODO: Confirm`
12. Deliver the reconstructed pack for documentation recovery, planning, or future implementation work.

## Gotchas

- If you start from stale docs or stakeholder memory instead of the repository, the “reconstructed” pack quietly becomes a rewrite of intent rather than a description of what exists. Start from code, tests, configs, and observable behavior first.
- If derived charter content sounds cleaner than the evidence, later artifacts inherit invented framing. Keep goals, non-goals, personas, and success criteria bounded by what the codebase can support and mark weak points explicitly.
- If derived stories describe what the product should do instead of what it demonstrably does, every downstream artifact inherits aspiration as fact. Rewrite those stories to match implemented behavior and mark gaps explicitly.
- If requirements are reconstructed from naming conventions alone, they sound plausible while drifting from real system guarantees. Tie each important requirement back to concrete repository evidence.
- If you hide uncertainty to make the pack read cleanly, future teams cannot tell which parts are proven and which are inferred. Keep `TODO: Confirm` markers where evidence is weak or conflicting.
- If technical design explanation outruns what the codebase shows, architecture diagrams become fiction with the credibility of recovered documentation. Stop at the evidence boundary and label hypotheses.
- If you write defaults as if they were mandatory output paths, users lose the ability to direct reconstruction where they need it. Treat the listed `.specs/...-research/` locations as defaults only.
- If `<project-name>` is re-derived mid-workflow, the reconstructed pack can fork into multiple roots even when the artifact content still aligns. Resolve naming once and preserve it for the full run.
- If you skip the consistency pass, contradictions between inferred charter, stories, requirements, and design survive until someone tries to use the pack for change planning. Reconcile or surface those conflicts before delivery.
- If gray-box discovery turns into a substitute for careful repository reading, the workflow becomes an excuse to speculate about architecture. Use the gray-box handoff only for bounded seams that the main reconstruction pass cannot explain confidently.

## Deliverables

- one reconstructed specification pack grounded in repository evidence
- `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` written to the chosen reconstruction spec-pack root
- deterministic provenance and source-artifact lineage on every reconstructed artifact
- explicit `TODO: Confirm` markers for unsupported or weakly supported conclusions
- a pack ready for documentation recovery, planning, or downstream change work

## References

- [`references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: reconstruction finds a probable architectural seam that needs bounded gray-box follow-on analysis.

## Validation Checklist

- `artifact-naming` was used to resolve one stable `<project-name>` for the workflow
- default workflow output paths match the reconstruction role defaults when the user does not override them
- derived `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` all exist at the chosen destinations
- every reconstructed artifact records `generated_by.root_skill = specification-reconstruction`
- every reconstructed artifact records the `source_artifacts` roles required by this workflow
- derived charter and stories reflect observed behavior rather than desired future intent
- derived requirements and design are supported by repository evidence
- weakly supported conclusions are marked explicitly with `TODO: Confirm`
- contradictions across derived artifacts are resolved or surfaced for review
