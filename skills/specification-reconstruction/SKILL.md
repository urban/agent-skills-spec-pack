---
name: specification-reconstruction
description: "Orchestrate reconstruction of a specification pack from repository evidence. Use when a user needs charter, user-stories, requirements, and technical-design artifacts recovered from an existing system."
license: MIT
metadata:
  version: "0.3.0"
  author: "urban (https://github.com)"
  layer: coordination
  dependencies:
    - document-traceability
    - artifact-naming
    - derive-charter
    - derive-user-stories
    - derive-requirements
    - derive-technical-design
---

## Rules

- Treat repository evidence as the primary source of truth because this workflow reconstructs implemented reality, not intended history.
- Keep this workflow at the coordination layer because specialist skills own artifact-specific reconstruction methods and validation.
- Use `artifact-naming` to resolve one stable `<project-name>` for the workflow because reconstructed artifacts must align to one reconstruction spec-pack root.
- Use `.specs/<project-name>-reconstructed/` as the default reconstruction spec-pack root unless the user provides explicit destinations.
- Establish `generated_by.root_skill` as `specification-reconstruction` for every artifact emitted from this workflow.
- Keep uncertainty explicit with `TODO: Confirm` whenever the codebase cannot prove original intent.
- Build two working inventories before deriving downstream artifacts:
  - one user-visible behavior inventory
  - one implementation-constraint inventory
- Treat package manifests, runtime entrypoints, command definitions, schema definitions, parser logic, tagged errors, integration clients, and tests as first-class evidence for implementation constraints.
- Reconcile downstream artifacts when `derive-technical-design` recovers stronger source-backed constraints than `derive-requirements` captured.
- Make exclusions explicit when implemented surfaces stay outside the chosen reconstruction scope.
- Run reconstruction in order because derived charter captures recoverable framing, derived stories capture user-visible behavior, derived requirements capture the contract, and derived design explains the implementation.
- Use local gray-box routing only when repository evidence suggests an architectural seam that needs bounded follow-on analysis outside this workflow.

## Constraints

- This workflow coordinates reconstruction; it does not replace underlying specialist or foundational contracts.
- Final output must include reconstructed `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md`.
- Coordination must use specialist skills for artifact-producing work and may use `artifact-naming` only for workflow-wide naming and placement coordination.
- Reconstructed requirements and technical design must account for high-impact implementation constraints that change execution, accepted inputs, safety behavior, operator-visible output, or operational prerequisites.
- Specialist outputs must not silently drop proven runtime, parser, integration, or lifecycle constraints as “mere implementation detail”.
- If a user asks for a reconstructed execution plan, frame it as current-state guidance rather than pretending to recover the original authored plan.
- Every reconstructed artifact must carry deterministic provenance rooted in this workflow plus the canonical `source_artifacts` lineage required by this workflow.

## Source Artifact Lineage

This workflow owns the canonical `source_artifacts` lineage map for reconstructed artifacts.

Use exactly these `source_artifacts` artifact-type keys in this workflow:

- `charter.md` -> `source_artifacts: {}`
- `user-stories.md` -> `charter`
- `requirements.md` -> `charter`, `user_stories`
- `technical-design.md` -> `charter`, `user_stories`, `requirements`

Resolved reconstructed paths should normally be:

- `charter` -> `<spec-pack-root>/charter.md`
- `user_stories` -> `<spec-pack-root>/user-stories.md`
- `requirements` -> `<spec-pack-root>/requirements.md`

For reconstructed user stories specifically:

- `derive-user-stories` produces `user-stories.md`
- the shared `write-user-stories` contract defines the story structure
- this workflow defines that reconstructed `user-stories.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md`

Do not add extra source artifact-types casually.

## Requirements

Inputs:

- repository source code
- tests, configs, and docs when present
- package manifests, runtime entrypoints, command definitions, schema definitions, parser logic, runtime wiring, and tests when present
- optional user-provided analysis scope
- optional user-provided output destinations
- optional explicit artifact slug or preferred basename
- clarification only when the requested scope or output shape is ambiguous

Default outputs when the user does not provide explicit destinations:

- `.specs/<project-name>-reconstructed/charter.md`
- `.specs/<project-name>-reconstructed/user-stories.md`
- `.specs/<project-name>-reconstructed/requirements.md`
- `.specs/<project-name>-reconstructed/technical-design.md`

Additional outputs:

- one reconstructed pack grounded in repository evidence
- one explicit user-visible behavior inventory used during reconstruction
- one explicit implementation-constraint inventory used to reconcile requirements and technical design
- explicit uncertainty markers where the codebase cannot prove original intent

In scope:

- resolving one workflow-wide `<project-name>` with `artifact-naming`
- selecting and preserving one reconstruction spec-pack root for the workflow
- orchestrating specialist entry skills for reconstruction
- building and reconciling user-visible behavior and implementation-constraint inventories
- checking that derived artifacts support each other
- establishing root workflow provenance and canonical `source_artifacts` lineage for every reconstructed artifact
- routing bounded gray-box follow-on discovery when needed
- making implemented-but-excluded surfaces explicit when the analysis scope omits them

Out of scope:

- inventing business intent the repository does not support
- presenting guesses as recovered facts
- replacing specialist-level reconstruction contracts with workflow prose
- treating current-state recommendations as the original plan

## Workflow

1. Confirm the user needs reconstruction of a specification pack from repository evidence, then confirm the scope to analyze, defaulting to the whole repository when the user does not narrow it.
2. Resolve `<project-name>` once with `artifact-naming`, honoring an explicit artifact slug or preferred basename when provided.
3. Resolve the reconstruction spec-pack root once for the full run, defaulting to `.specs/<project-name>-reconstructed/` unless the user provides explicit destinations.
4. Establish `root_skill = specification-reconstruction` for all reconstructed artifacts in this run.
5. Inspect repository evidence relevant to the chosen scope, prioritizing source, tests, configs, package manifests, runtime entrypoints, command definitions, schemas, parser logic, and existing docs.
6. Build a user-visible behavior inventory from code and tests.
7. Build an implementation-constraint inventory from manifests, entrypoints, command definitions, schemas, parsers, tagged errors, integrations, lifecycle code, and tests.
8. Classify recovered implementation constraints into these buckets:
   - runtime/platform
   - command grammar and CLI surface
   - validation and schema
   - data shape and parsing
   - integration and protocol
   - lifecycle and resource ownership
   - dependency and tooling prerequisites
   - operator-visible error and no-op behavior
   - packaging and path assumptions
9. Run `derive-charter`, write the result to `<spec-pack-root>/charter.md`, and review whether the inferred goals, non-goals, personas, and success criteria stay within what the codebase can plausibly support.
10. Run `derive-user-stories`, write the result to `<spec-pack-root>/user-stories.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md`, and review whether the inferred outcomes reflect observable behavior rather than desired future behavior.
11. Run `derive-requirements`, write the result to `<spec-pack-root>/requirements.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md` and `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, and confirm the reconstructed contract accounts for source-backed implementation constraints without collapsing into architecture prose.
12. Run `derive-technical-design`, write the result to `<spec-pack-root>/technical-design.md`, stamp `source_artifacts.charter = <spec-pack-root>/charter.md`, `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, and `source_artifacts.requirements = <spec-pack-root>/requirements.md`, and confirm the as-built design names the composition root, boundary types, validation seams, resource ownership, and error model when the code proves them.
13. Reconcile `technical-design.md` back into `requirements.md` when stronger source-backed constraints appear in technical design:
   - compare the implementation-constraint inventory with the drafted requirements
   - backfill missing `NFR`, `TC`, `DR`, `IR`, or `DEP` items
   - keep architecture decomposition in technical design rather than moving it into requirements
14. Read [`references/gray-box-routing.md`](./references/gray-box-routing.md) only when the reconstruction pass finds a probable architectural seam that needs bounded follow-on analysis.
15. Perform a cross-artifact consistency pass:
   - derived `charter.md` is supported by observable behavior and constraints
   - derived `user-stories.md` fits the derived personas and implied scope boundaries and uses the shared five-field story contract
   - derived `requirements.md` is supported by repository evidence, aligns to derived stories, and captures high-impact implementation constraints in the right requirement families
   - derived `technical-design.md` explains the implemented system, including source-backed runtime, parser, validation, lifecycle, and failure constraints
   - excluded implemented surfaces are called out explicitly when they were left outside the chosen scope
   - every reconstructed artifact carries canonical provenance and the `source_artifacts` artifact-type keys required by this workflow
   - weakly supported conclusions remain marked `TODO: Confirm`
16. Deliver the reconstructed specification pack for documentation recovery, planning, or future implementation work.

## Gotchas

- If you start from stale docs or stakeholder memory instead of the repository, the “reconstructed” pack quietly becomes a rewrite of intent rather than a description of what exists. Start from code, tests, configs, and observable behavior first.
- If the workflow stays purely story-first, package manifests, runtime wiring, parser rules, and operational constraints disappear from downstream artifacts. Build both inventories before drafting requirements or design.
- If derived charter content sounds cleaner than the evidence, later artifacts inherit invented framing. Keep goals, non-goals, personas, and success criteria bounded by what the codebase can support and mark weak points explicitly.
- If derived stories describe what the product should do instead of what it demonstrably does, every downstream artifact inherits aspiration as fact. Rewrite those stories to match implemented behavior and mark gaps explicitly.
- If requirements are reconstructed from naming conventions alone, they sound plausible while drifting from real system guarantees. Tie each important requirement back to concrete repository evidence.
- If technical design discovers stronger constraints than requirements and you fail to reconcile them, the pack becomes internally inconsistent. Backfill the right non-FR sections before delivery.
- If you hide uncertainty to make the pack read cleanly, future teams cannot tell which parts are proven and which are inferred. Keep `TODO: Confirm` markers where evidence is weak or conflicting.
- If technical design explanation outruns what the codebase shows, architecture diagrams become fiction with the credibility of recovered documentation. Stop at the evidence boundary and label hypotheses.
- If implemented surfaces are excluded from scope without explanation, the pack misstates what the repository actually contains. Call exclusions out explicitly.
- If you write defaults as if they were mandatory output paths, users lose the ability to direct reconstruction where they need it. Treat the listed `.specs/...-reconstructed/` locations as defaults only.
- If `<project-name>` is re-derived mid-workflow, the reconstructed pack can fork into multiple roots even when the artifact content still aligns. Resolve naming once and preserve it for the full run.
- If you skip the consistency pass, contradictions between inferred charter, stories, requirements, and design survive until someone tries to use the pack for change planning. Reconcile or surface those conflicts before delivery.
- If gray-box discovery turns into a substitute for careful repository reading, the workflow becomes an excuse to speculate about architecture. Use the gray-box handoff only for bounded seams that the main reconstruction pass cannot explain confidently.

## Deliverables

- one reconstructed specification pack grounded in repository evidence
- `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` written to the chosen reconstruction spec-pack root
- deterministic provenance and source-artifact lineage on every reconstructed artifact
- one explicit implementation-constraint inventory used to reconcile requirements and technical design
- explicit `TODO: Confirm` markers for unsupported or weakly supported conclusions
- a pack ready for documentation recovery, planning, or downstream change work

## References

- [`references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: reconstruction finds a probable architectural seam that needs bounded gray-box follow-on analysis.

## Validation Checklist

- `artifact-naming` was used to resolve one stable `<project-name>` for the workflow
- default workflow output paths match the reconstruction role defaults when the user does not override them
- an explicit implementation-constraint inventory exists during reconstruction
- derived `charter.md`, `user-stories.md`, `requirements.md`, and `technical-design.md` all exist at the chosen destinations
- every reconstructed artifact records `generated_by.root_skill = specification-reconstruction`
- reconstructed `user-stories.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md`
- reconstructed `requirements.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md` and `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`
- reconstructed `technical-design.md` records exactly `source_artifacts.charter = <spec-pack-root>/charter.md`, `source_artifacts.user_stories = <spec-pack-root>/user-stories.md`, and `source_artifacts.requirements = <spec-pack-root>/requirements.md`
- derived charter and stories reflect observed behavior rather than desired future intent
- high-impact runtime, parser, integration, and lifecycle constraints appear in `requirements.md` or `technical-design.md`
- stronger technical-design findings are reconciled back into requirements when needed
- excluded implemented surfaces are called out explicitly when they stay out of scope
- weakly supported conclusions are marked explicitly with `TODO: Confirm`
- contradictions across derived artifacts are resolved or surfaced for review
