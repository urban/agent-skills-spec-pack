---
name: [TODO: artifact name in kebab-case]
created_at: [TODO: creation timestamp in UTC ISO 8601]
updated_at: [TODO: last-updated timestamp in UTC ISO 8601]
generated_by:
  root_skill: [TODO: orchestration skill]
  producing_skill: [TODO: expertise skill]
  skills_used:
    - [TODO: ordered participating skill]
  skill_graph:
    [TODO: skill-name]: []
source_artifacts:
  plan: docs/plans/[TODO: artifact-name]-plan.md
---

## Task Summary

- Parent plan: `docs/plans/[TODO: artifact-name]-plan.md`
- Scope: [TODO: summarize the implementation slice covered by these tasks]
- Tracking intent: [TODO: describe how this document should be used during implementation]
- Runtime-edge obligations: [TODO: preserved operator-facing runtime behavior or `None in parent plan`]

## Stream Groups

### [TODO: Stream name]

Objective: [TODO: what this stream delivers]

#### Task [TODO: TASK-ID]

- Title: [TODO: short task title]
- Status: [TODO: Not started | In progress | Blocked | Complete]
- Blocked by: [TODO: comma-separated task IDs or `None`]
- Plan references:
  - [TODO: stable anchor from parent plan]
- What to build: [TODO: smallest independently verifiable end-to-end behavior]
- Acceptance criteria:
  - [TODO: structural completion criterion]
  - [TODO: behavior-verifying completion criterion]
- Notes:
  - [TODO: coordination note or `None`]

## Dependency Map

- [TODO: TASK-ID] -> [TODO: TASK-ID or `None`]

## Tracking Notes

- Active stream: [TODO: current stream or `None`]
- Global blockers: [TODO: blocker summary or `None`]
- TODO: Confirm: [TODO: unresolved high-impact task boundary or `None`]
