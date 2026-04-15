# Approval views

Approval views are derived review surfaces for canonical package artifacts. They reduce human review cost without creating a second source of truth.

## Terms

Use these terms deliberately:

- **canonical artifact** — a Markdown artifact under the spec-pack root that carries canonical frontmatter and remains the source of truth
- **derived approval view** — a Markdown or HTML review surface generated from one canonical artifact snapshot or one full-pack snapshot
- **approval snapshot** — the exact canonical bytes a derived approval view represents
- **working notes** — non-canonical scratch work allowed during drafting but not emitted as workflow artifacts

## One-source-of-truth rule

- canonical Markdown artifacts remain the single source of truth
- approval views may use only the in-scope canonical artifact bytes for the active review
- approval views do not replace canonical artifacts and do not use canonical frontmatter
- approval views must stay secondary to the canonical artifact they summarize

## Ownership split

| Concern | Owner |
| --- | --- |
| shared approval-view contract, rendering, and validation | foundational `write-approval-view` |
| when approval views are generated | coordination |
| artifact-specific review emphasis | specialist |

## Output paths

Approval views live under `<spec-pack-root>/approval/`.

Default paths:

- per-artifact review -> `<spec-pack-root>/approval/<artifact-basename>.md` and `<spec-pack-root>/approval/<artifact-basename>.html`
- full-pack review -> `<spec-pack-root>/approval/pack.md` and `<spec-pack-root>/approval/pack.html`

## Approval rules

- approval must be explicit in the conversation
- approval of a derived approval view counts as approval of the exact snapshot it represents
- any canonical artifact change invalidates prior approval for that artifact
- approval is whole-artifact or whole-pack only
- no artifact may be treated as approved while any `TODO: Confirm` remains
- revised review requires a fresh approval view for the new snapshot before re-approval

## Required Markdown structure

Markdown approval views have no frontmatter.

Required sections, in order:

1. `Snapshot Identity`
2. `Change Summary` when the view is revised
3. `Executive Summary`
4. `Scope`
5. `Decisions Required for Approval`
6. `Risks and Tradeoffs`
7. `Blockers and Unresolved Items`
8. `Traceability Map`
9. `Validator Status`
10. `Downstream Impact if Approved`

Revised views are diff-first:

- `Change Summary` appears immediately after `Snapshot Identity`
- `Change Summary` includes `Previous snapshot SHA-256:`
- `Change Summary` includes at least one delta bullet or `- None`

## Snapshot identity

Artifact views record:

- `Review type: Artifact`
- `Approval mode: Initial | Revised`
- `Canonical artifact: <resolved path>`
- `Snapshot SHA-256: <hash of canonical bytes>`
- `Canonical updated_at: <updated_at from canonical frontmatter>`
- `Approval view generated_at: <UTC ISO 8601 timestamp>`

Pack views record:

- `Review type: Pack`
- `Approval mode: Initial | Revised`
- `Spec-pack root: <resolved root>`
- `Pack snapshot SHA-256: <aggregate hash of sorted path + file-hash pairs>`
- `Approval view generated_at: <UTC ISO 8601 timestamp>`
- `Included snapshots:` with one bullet per canonical artifact in this exact form:
  - `<resolved path> | SHA-256: <hash> | updated_at: <timestamp>`

## Traceability and validator status

Every substantive claim in `Traceability Map` uses this exact three-line block:

```text
- [Tn] Claim: <summary>
  - Source: <resolved canonical path> :: <exact heading>
  - Evidence quote: "<verbatim quote from that canonical section>"
```

Rules:

- source headings must match the canonical artifact exactly
- evidence quotes must appear verbatim in the referenced section
- `Validator Status` must include both `Canonical validator` and `Approval-view validator`
- record the command and result for each validator

## HTML companion

Every Markdown approval view has a matching self-contained HTML companion for the same snapshot.

The HTML view must:

- keep the same section order and snapshot identity as the Markdown view
- be rendered deterministically from the Markdown view
- validate against the same snapshot metadata

## Validation commands

Use the shared validator from repo root:

```bash
bash skills/write-approval-view/scripts/validate_approval_view.sh artifact <canonical-file> <approval-md> <approval-html>
bash skills/write-approval-view/scripts/validate_approval_view.sh artifact-revised <canonical-file> <approval-md> <approval-html>
bash skills/write-approval-view/scripts/validate_approval_view.sh pack <approval-md> <approval-html> <canonical-file>...
bash skills/write-approval-view/scripts/validate_approval_view.sh pack-revised <approval-md> <approval-html> <canonical-file>...
```

Fail closed on:

- missing required sections or wrong order
- snapshot hash mismatch
- stale `updated_at` metadata
- unresolved traceability headings or quotes
- missing `Change Summary` for revised views
- HTML and Markdown snapshot mismatch
- unresolved template placeholders

## Workflow defaults

Current coordination workflows use approval views like this:

- `specification-authoring` — per-artifact approval after each canonical artifact, then final pack review
- `specification-reconstruction` — requested per-artifact checkpoints, then final pack review
- `specification-to-execution` — when execution approval is requested or already required

Use `skills/write-approval-view/SKILL.md` as the exact contract when implementing or validating approval-view behavior.
