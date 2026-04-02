---
name: specification-reconstruction
description: Orchestrate reconstruction of a specification pack from an existing codebase. Use when a user wants charter, user stories, requirements, and technical design recovered from implemented software.
metadata:
  version: 0.1.0
  layer: orchestration
  dependencies:
    - derive-charter
    - derive-user-stories
    - derive-requirements
    - derive-technical-design
---

## Rules

- Treat repository evidence as the primary source of truth because this workflow reconstructs implemented reality, not intended history.
- Keep this workflow at the orchestration layer because expertise skills own artifact-specific reconstruction methods and validation.
- Use default research output locations unless the user provides explicit destinations.
- Keep uncertainty explicit with `TODO: Confirm` whenever the codebase cannot prove original intent.
- Run reconstruction in order because derived charter captures recoverable framing, derived stories capture user-visible behavior, derived requirements capture the contract, and derived design explains the implementation.
- Use local gray-box routing only when repository evidence suggests an architectural seam that needs bounded follow-on analysis outside this workflow.

## Constraints

- This workflow coordinates reconstruction; it does not replace underlying expertise or foundational contracts.
- Final output must include reconstructed charter, user stories, requirements, and technical design.
- Orchestration dependencies stay limited to expertise entry skills; do not name foundational contract skills here.
- If a user asks for a reconstructed execution plan, frame it as current-state guidance rather than pretending to recover the original authored plan.

## Requirements

Inputs:

- repository source code
- tests, configs, and docs when present
- optional user-provided analysis scope
- optional user-provided output destinations
- clarification only when the requested scope or output shape is ambiguous

Default outputs when the user does not provide explicit destinations:

- `docs/research/<project-name>/charter.md`
- `docs/research/<project-name>/user-stories.md`
- `docs/research/<project-name>/requirements.md`
- `docs/research/<project-name>/technical-design.md`

Additional outputs:

- one reconstructed pack grounded in repository evidence
- explicit uncertainty markers where the codebase cannot prove original intent

In scope:

- orchestrating expertise entry skills for reconstruction
- preserving consistent `<project-name>` defaults across derived artifacts
- checking that derived artifacts support each other
- routing bounded gray-box follow-on discovery when needed

Out of scope:

- inventing business intent the repository does not support
- presenting guesses as recovered facts
- replacing expertise-level reconstruction contracts with workflow prose
- treating current-state recommendations as the original plan

## Workflow

1. Confirm the repository scope to analyze, defaulting to the whole repository when the user does not narrow it.
2. Resolve one stable `<project-name>` for default output locations unless the user provides explicit destinations.
3. Inspect repository evidence relevant to the chosen scope, prioritizing source, tests, configs, and existing docs.
4. Run `derive-charter` and review whether the inferred goals, non-goals, personas, and success criteria stay within what the codebase can plausibly support.
5. Run `derive-user-stories` and review whether the inferred outcomes reflect observable behavior rather than desired future behavior.
6. Run `derive-requirements` and confirm the reconstructed contract stays supported by repository evidence and does not silently re-own charter content.
7. Run `derive-technical-design` and confirm the as-built design explains the derived requirements without speculating beyond the codebase.
8. Read [`references/gray-box-routing.md`](./references/gray-box-routing.md) only when the reconstruction pass finds a probable architectural seam that needs bounded follow-on analysis.
9. Perform a cross-artifact consistency pass:
   - derived charter is supported by observable behavior and constraints
   - derived stories fit the derived personas and implied scope boundaries
   - derived requirements are supported by repository evidence and align to derived stories
   - derived technical design explains the implemented system
   - weakly supported conclusions remain marked `TODO: Confirm`
10. Deliver the reconstructed pack for documentation recovery, planning, or future implementation work.

## Gotchas

- If you start from stale docs or stakeholder memory instead of the repository, the “reconstructed” pack quietly becomes a rewrite of intent rather than a description of what exists. Start from code, tests, configs, and observable behavior first.
- If derived charter content sounds cleaner than the evidence, later artifacts inherit invented framing. Keep goals, non-goals, personas, and success criteria bounded by what the codebase can support and mark weak points explicitly.
- If derived stories describe what the product should do instead of what it demonstrably does, every downstream artifact inherits aspiration as fact. Rewrite those stories to match implemented behavior and mark gaps explicitly.
- If requirements are reconstructed from naming conventions alone, they sound plausible while drifting from real system guarantees. Tie each important requirement back to concrete repository evidence.
- If you hide uncertainty to make the pack read cleanly, future teams cannot tell which parts are proven and which are inferred. Keep `TODO: Confirm` markers where evidence is weak or conflicting.
- If technical design explanation outruns what the codebase shows, architecture diagrams become fiction with the credibility of recovered documentation. Stop at the evidence boundary and label hypotheses.
- If you write defaults as if they were mandatory output paths, users lose the ability to direct reconstruction where they need it. Treat the listed `docs/research/...` locations as defaults only.
- If you skip the consistency pass, contradictions between inferred charter, stories, requirements, and design survive until someone tries to use the pack for change planning. Reconcile or surface those conflicts before delivery.
- If gray-box discovery turns into a substitute for careful repository reading, the workflow becomes an excuse to speculate about architecture. Use the gray-box handoff only for bounded seams that the main reconstruction pass cannot explain confidently.

## Deliverables

- one reconstructed specification pack grounded in repository evidence
- charter, user stories, requirements, and technical design artifacts written to the chosen destinations
- explicit `TODO: Confirm` markers for unsupported or weakly supported conclusions
- a pack ready for documentation recovery, planning, or downstream change work

## References

- [`references/gray-box-routing.md`](./references/gray-box-routing.md): Read when: reconstruction finds a probable architectural seam that needs bounded gray-box follow-on analysis.

## Validation Checklist

- default workflow output paths match the reconstruction role defaults when the user does not override them
- derived charter, user stories, requirements, and technical design artifacts all exist at the chosen destinations
- orchestration dependencies stay limited to expertise entry skills
- derived charter and stories reflect observed behavior rather than desired future intent
- derived requirements and design are supported by repository evidence
- weakly supported conclusions are marked explicitly with `TODO: Confirm`
- contradictions across derived artifacts are resolved or surfaced for review
