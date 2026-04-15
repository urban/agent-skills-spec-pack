---
name: write-approval-view
description: "Write and validate derived approval views for canonical package artifacts. Use when a workflow needs human approval of an exact canonical artifact snapshot through Markdown or HTML review surfaces."
license: MIT
metadata:
  version: "0.2.0"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared approval-view contract: derived Markdown and HTML review surfaces for exact canonical artifact snapshots or full-pack snapshot sets, including snapshot identity, traceability, visual carry-forward, glance-first rendering, and fail-closed validation.

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
    1. `Change Summary` when the view is revised; otherwise omit
    2. `Executive Summary`
    3. `Scope`
    4. `Decisions Required for Approval`
    5. `Risks and Tradeoffs`
    6. `Blockers and Unresolved Items`
    7. `Traceability Map`
    8. `Validator Status`
    9. `Downstream Impact if Approved`
    10. `Snapshot Identity`
  - keep the top-level `##` section order exact; `Snapshot Identity` must be the final top-level section. Place carried-forward visuals inside the relevant required section as subsections or fenced blocks, not as new top-level sections
- Visual carry-forward rules:
  - when the canonical artifact or pack snapshot contains in-scope diagrams or other visual sections that materially affect approval, copy them into the Markdown approval view
  - place carried-forward visuals in a `### Visual Evidence` subsection inside the most relevant required section; for technical-design artifact approvals, default to `## Executive Summary` unless another required section is a better fit
  - precede each carried-forward visual with `- Source: <resolved canonical path> :: <exact heading>` so approvers can match the visual to the canonical section
  - copy Mermaid fence contents exactly; do not redraw, rename, or reinterpret the diagram
  - for technical-design artifact approvals, carry forward every required diagram slot present in the canonical artifact and any populated optional `Interaction Diagram`
  - if a technical-design diagram slot says `Not needed:` or `TODO: Confirm`, carry that exact status forward instead of inventing a diagram
  - in pack review, include only the visuals needed to approve the explicit included snapshot set
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
  - `Change Summary` must be the first required section, immediately before `Executive Summary`
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
  - one self-contained HTML file with inline CSS/JS; deterministic CDN fonts and Mermaid runtime are allowed when needed for rendering
  - same section order and snapshot identity as the Markdown view
  - do not repeat snapshot identity fields elsewhere in visible HTML; keep them in the final `## Snapshot Identity` section, except for the required review-target title
  - surface a top-of-page `At a Glance` summary derived from approval content without repeating full snapshot identity fields there
  - when the page has 4+ top-level sections, include responsive section navigation: sticky desktop TOC and sticky horizontal mobile nav
  - use section-specific presentation patterns, not visually identical cards:
    - `Change Summary` -> hero delta panel
    - `Executive Summary` -> hero summary with dominant first-paint treatment
    - `Scope` -> split `In scope` / `Out of scope` panels
    - `Decisions Required for Approval` -> numbered decision cards
    - `Risks and Tradeoffs` -> scan-friendly risk cards
    - `Blockers and Unresolved Items` -> warning callouts
    - `Traceability Map` -> details/accordion claim entries
    - `Validator Status` -> side-by-side validator status cards
    - `Downstream Impact if Approved` -> ordered impact timeline or impact cards
    - `Snapshot Identity` -> visually recessed final metadata panel
  - use depth tiers so primary sections dominate and reference sections recede: hero / elevated / default / recessed
  - include all carried-forward visuals from the Markdown view
  - when a required section contains `### Visual Evidence`, prefer a split or otherwise clearly separated layout so prose and visual review can happen side by side or with strong visual separation
  - render structured row/column content as semantic tables when that improves scanability; for pack review, `Included snapshots` defaults to an HTML table
  - use `<details>/<summary>` for secondary evidence, long validator commands, long evidence quotes, raw Mermaid source, or verbose included-snapshot listings
  - preserve Mermaid blocks in HTML as rendered Mermaid visual shells with zoom / pan / expand controls while also preserving the underlying Mermaid source in the HTML; do not redraw, rename, or reinterpret the diagram
  - surface the review target in both the HTML `<title>` and the visible page title:
    - artifact view -> `Artifact Approval View: <artifact-basename>`
    - pack view -> `Pack Approval View: <spec-pack-name>` where `<spec-pack-name>` is the basename of `Spec-pack root`
  - avoid generic approval-view styling: no Inter-as-primary body font, no emoji section headers, no indigo/violet gradient accents, no glowing cards, no visually uniform section chrome
  - render from the Markdown view and snapshot identity with `python3 ./scripts/render_approval_view_html.py <approval-md> <approval-html>` unless the caller has an equivalent deterministic renderer
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
- canonical diagram or visual sections, or explicit confirmation that none are in scope
- canonical validator command and result

## Outputs

- one Markdown approval view, including carried-forward visuals when in scope
- one HTML approval view for the same snapshot, preserving the same carried-forward visuals and using the shared glance-first review layout
- templates under `./assets/`
- deterministic rendering and validation helpers under `./scripts/`

## Workflow

1. Confirm the canonical artifact or explicit pack snapshot already passed its validator.
2. Choose the matching Markdown template under `./assets/`.
3. Compute snapshot hashes from the exact canonical bytes:
   - artifact view -> SHA-256 of the canonical file
   - pack view -> SHA-256 of the sorted `<resolved-path><TAB><file-sha>` list
4. Identify any in-scope diagrams or other visual sections in the canonical artifact or pack snapshot. When present, carry them forward into a `### Visual Evidence` subsection inside the most relevant required section, preceding each with `- Source: <resolved canonical path> :: <exact heading>`.
5. For technical-design artifact approvals, include every required diagram slot and any populated optional `Interaction Diagram`; if a slot is `Not needed:` or `TODO: Confirm`, copy that exact slot status instead of inventing a diagram.
6. Copy only claims backed by the canonical artifact or pack snapshot; record each substantive claim in `Traceability Map` with an exact heading and verbatim evidence quote.
7. If the view is revised, add `Change Summary` as the first required section, immediately before `Executive Summary`, and anchor it to the previous approved snapshot hash.
8. Render the HTML companion with `python3 ./scripts/render_approval_view_html.py <approval-md> <approval-html>`, making sure the HTML `<title>` and page title surface the approved artifact basename or pack name, the page includes glance summary + responsive nav + section-specific layout treatments, and carried-forward Mermaid blocks survive as rendered interactive shells plus preserved source in HTML.
9. Validate with the correct mode:
   - artifact: `bash ./scripts/validate_approval_view.sh artifact <canonical-file> <approval-md> <approval-html>`
   - revised artifact: `bash ./scripts/validate_approval_view.sh artifact-revised <canonical-file> <approval-md> <approval-html>`
   - pack: `bash ./scripts/validate_approval_view.sh pack <approval-md> <approval-html> <canonical-file>...`
   - revised pack: `bash ./scripts/validate_approval_view.sh pack-revised <approval-md> <approval-html> <canonical-file>...`
10. When handing the approval view to the user for review, report the resolved HTML path and the absolute `file://` URI for that HTML file.
11. If validation fails, revise the approval view and do not use it for approval.

## Validation

- Confirm the Markdown view contains the required sections in order, with `Snapshot Identity` last.
- Confirm any carried-forward visuals stay inside required top-level sections and use a `### Visual Evidence` subsection when present.
- Confirm snapshot hash fields match the current canonical bytes exactly.
- Confirm `updated_at` values match canonical frontmatter exactly.
- Confirm revised modes include `Change Summary` with `Previous snapshot SHA-256:`.
- Confirm every traceability entry resolves to an exact heading and verbatim quote in the referenced canonical artifact.
- Confirm any in-scope visual sections from the canonical artifact or pack snapshot appear in the approval Markdown without semantic drift.
- Confirm technical-design artifact approvals carry forward every required diagram slot and any populated optional `Interaction Diagram`, or the exact `Not needed:` or `TODO: Confirm` slot text.
- Confirm HTML and Markdown point to the same snapshot.
- Confirm HTML includes a top-of-page glance summary derived from the approval content.
- Confirm approval pages with 4+ sections include responsive section navigation.
- Confirm section-specific HTML layouts are present and `Snapshot Identity` is visually recessed in the final section.
- Confirm HTML preserves the same carried-forward visual content as the Markdown view, including Mermaid blocks.
- Confirm Mermaid visual evidence renders in an interactive shell and still preserves raw Mermaid source in the HTML.
- Confirm semantic tables are used where row/column scanning materially improves review speed, including pack `Included snapshots`.
- Confirm visible HTML does not repeat snapshot identity fields outside the final section, other than the required review-target title.
- Confirm visible HTML uses collapsible details for secondary evidence, long validator commands, long quotes, raw Mermaid source, or verbose snapshot listings.
- Confirm the HTML `<title>` and visible page title surface the approved artifact basename for artifact review or the pack name for pack review.
- Confirm the HTML hierarchy is obvious before reading every sentence.
- Confirm the HTML avoids generic approval-view styling: no Inter-as-primary, no emoji headers, no indigo/violet gradient accents, no glowing cards, and no uniform card treatment for every section.
- Confirm any user-facing HTML review reference includes the resolved HTML path and the matching absolute `file://` URI.
- Confirm unresolved template placeholders do not remain.
- Run the shared validator with the correct mode before asking for approval.
