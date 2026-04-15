---
name: write-approval-view
description: "Write and validate derived approval views for canonical package artifacts. Use when a workflow needs human approval of an exact canonical artifact snapshot through Markdown or HTML review surfaces."
license: MIT
metadata:
  version: "0.1.0"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared approval-view contract: derived Markdown and HTML review surfaces for exact canonical artifact snapshots or full-pack snapshot sets, including snapshot identity, traceability, rendering, and fail-closed validation.

## Contract

- Approval views are derived review surfaces, not canonical source-of-truth artifacts.
- Approval views may use only the in-scope canonical artifact bytes for the active review:
  - per-artifact review -> one canonical artifact
  - pack review -> the explicit canonical artifact set in that pack snapshot
- Output paths:
  - per-artifact -> `<spec-pack-root>/approval/<artifact-basename>.md` and `<spec-pack-root>/approval/<artifact-basename>.html`
  - pack -> `<spec-pack-root>/approval/pack.md` and `<spec-pack-root>/approval/pack.html`
- Markdown contract:
  - no frontmatter
  - required sections, in order:
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
- Snapshot identity:
  - artifact view fields:
    - `Review type: Artifact`
    - `Approval mode: Initial | Revised`
    - `Canonical artifact: <resolved path>`
    - `Snapshot SHA-256: <hash of canonical bytes>`
    - `Canonical updated_at: <updated_at from canonical frontmatter>`
    - `Approval view generated_at: <UTC ISO 8601 timestamp>`
  - pack view fields:
    - `Review type: Pack`
    - `Approval mode: Initial | Revised`
    - `Spec-pack root: <resolved root>`
    - `Pack snapshot SHA-256: <aggregate hash of sorted path + file-hash pairs>`
    - `Approval view generated_at: <UTC ISO 8601 timestamp>`
    - `Included snapshots:` with one bullet per canonical artifact in this exact form:
      - `<resolved path> | SHA-256: <hash> | updated_at: <timestamp>`
- Revised view rules:
  - `Change Summary` must appear immediately after `Snapshot Identity`
  - revised views are diff-first, then full current summary
  - `Change Summary` must include `Previous snapshot SHA-256:` and at least one delta bullet or `- None`
- Traceability map rules:
  - every substantive claim uses this exact three-line block:
    - `- [Tn] Claim: <summary>`
    - `  - Source: <resolved canonical path> :: <exact heading>`
    - `  - Evidence quote: "<verbatim quote from that canonical section>"`
  - source headings must match the canonical artifact exactly
  - evidence quotes must appear verbatim in the referenced canonical section
- Validator status rules:
  - include both `Canonical validator` and `Approval-view validator`
  - record the command and result for each
- HTML rules:
  - self-contained HTML
  - same section order and snapshot identity as the Markdown view
  - render from the Markdown view with `python3 ./scripts/render_approval_view_html.py <approval-md> <approval-html>` unless the caller has an equivalent deterministic renderer
- Reporting rules:
  - when presenting an HTML approval view in terminal/chat, include the resolved HTML filesystem path and the absolute `file://` URI for that same file
  - emit the `file://` URI as plain text so terminal URL detection can make it clickable
  - do not rewrite Markdown-internal links solely for terminal clickability; relative links inside approval artifacts may remain relative
- Do not add facts, repo analysis, or workflow policy not present in the canonical artifact or explicit pack snapshot.

## Inputs

- review mode: `artifact` | `artifact-revised` | `pack` | `pack-revised`
- one canonical artifact path or an explicit canonical artifact set
- resolved approval output paths
- artifact-specific review emphasis, decisions, risks, blockers, and downstream impact derived from the canonical artifact or pack snapshot
- canonical validator command and result

## Outputs

- one Markdown approval view
- one HTML approval view for the same snapshot
- templates under `./assets/`
- deterministic rendering and validation helpers under `./scripts/`

## Workflow

1. Confirm the canonical artifact or explicit pack snapshot already passed its validator.
2. Choose the matching Markdown template under `./assets/`.
3. Compute snapshot hashes from the exact canonical bytes:
   - artifact view -> SHA-256 of the canonical file
   - pack view -> SHA-256 of the sorted `<resolved-path><TAB><file-sha>` list
4. Copy only claims backed by the canonical artifact or pack snapshot; record each substantive claim in `Traceability Map` with an exact heading and verbatim evidence quote.
5. If the view is revised, add `Change Summary` immediately after `Snapshot Identity` and anchor it to the previous approved snapshot hash.
6. Render the HTML companion with `python3 ./scripts/render_approval_view_html.py <approval-md> <approval-html>`.
7. Validate with the correct mode:
   - artifact: `bash ./scripts/validate_approval_view.sh artifact <canonical-file> <approval-md> <approval-html>`
   - revised artifact: `bash ./scripts/validate_approval_view.sh artifact-revised <canonical-file> <approval-md> <approval-html>`
   - pack: `bash ./scripts/validate_approval_view.sh pack <approval-md> <approval-html> <canonical-file>...`
   - revised pack: `bash ./scripts/validate_approval_view.sh pack-revised <approval-md> <approval-html> <canonical-file>...`
8. When handing the approval view to the user for review, report the resolved HTML path and the absolute `file://` URI for that HTML file.
9. If validation fails, revise the approval view and do not use it for approval.

## Validation

- Confirm the Markdown view contains the required sections in order.
- Confirm snapshot hash fields match the current canonical bytes exactly.
- Confirm `updated_at` values match canonical frontmatter exactly.
- Confirm revised modes include `Change Summary` with `Previous snapshot SHA-256:`.
- Confirm every traceability entry resolves to an exact heading and verbatim quote in the referenced canonical artifact.
- Confirm HTML and Markdown point to the same snapshot.
- Confirm any user-facing HTML review reference includes the resolved HTML path and the matching absolute `file://` URI.
- Confirm unresolved template placeholders do not remain.
- Run the shared validator with the correct mode before asking for approval.
