---
name: write-approval-view
description: "Write and validate derived approval views for canonical package artifacts. Use when a workflow needs human approval of an exact canonical artifact snapshot through Markdown or HTML review surfaces."
license: MIT
metadata:
  version: "0.4.0"
  author: "urban (https://github.com)"
  layer: foundational
  internal: true
---

## Purpose

Own the shared approval-view framework: profile routing, scaffolding, HTML rendering, glance metrics, snapshot identity, visual carry-forward, and fail-closed validation for exact canonical snapshots.

## Contract

- Approval views are derived review surfaces, never canonical source-of-truth artifacts.
- Approval views may use only the in-scope canonical artifact bytes for the active review:
  - artifact review -> one canonical artifact
  - pack review -> the explicit canonical artifact set in that pack snapshot
- Output paths:
  - artifact -> `<spec-pack-root>/approval/<artifact-basename>.md` and `<spec-pack-root>/approval/<artifact-basename>.html`
  - pack -> `<spec-pack-root>/approval/pack.md` and `<spec-pack-root>/approval/pack.html`
- Ownership:
  - producing specialist skill owns artifact approval framing at `../<skill>/assets/approval-view-profile.json`
  - workflow coordinator owns pack approval framing at `../<root-skill>/assets/pack-approval-view-profile.json`
  - this skill owns the framework, shared renderer, shared validator, and generic fallbacks only
- Artifact profile routing order:
  1. canonical frontmatter `generated_by.producing_skill`
  2. basename fallback mapped to a specialist owner only
  3. built-in generic artifact fallback profile
- Pack profile routing order:
  1. unanimous canonical frontmatter `generated_by.root_skill` across the included artifact set
  2. matching coordinator-owned `../<root-skill>/assets/pack-approval-view-profile.json`
  3. built-in generic pack fallback profile
- Bad or missing `producing_skill` or `root_skill` must not block generation; fall back best-effort.
- Markdown contract:
  - no frontmatter
  - required top-level `##` sections must match the selected profile exactly, in order
  - revised views prepend `Change Summary`; `Snapshot Identity` remains the final top-level section
  - scaffold with `python3 ./scripts/scaffold_approval_view.py artifact <canonical-file>`, `artifact-revised <canonical-file>`, `pack [<canonical-file> ...]`, or `pack-revised [<canonical-file> ...]` unless the caller has an equivalent deterministic scaffold
  - carried-forward visuals stay inside required sections under `### Visual Evidence`
- Profile schema:
  - top level: `profile_id`, `display_name`, `subtitle`, `review_type`, optional `default_visual_section`, optional `revised`, `sections`, `glance_cards`
  - section fields: `key`, `title`, `kind`, `label`, `style`, `tone`, `emphasis`, `item_label`, `empty_state`, `why`
  - glance-card fields: `label`, `metric`, `section_title`, `hint`, `tone`, `source`, `extractor`
  - revised fields: `section_overrides`, `glance_cards`
- Supported section kinds:
  - `change-summary`
  - `summary`
  - `scope`
  - `cards`
  - `callouts`
  - `traceability`
  - `validator`
  - `timeline`
  - `snapshot`
  - `fragment`
  - `paired-lists`
  - `checklist`
  - `ledger`
  - `matrix`
  - `roster`
  - `diagram-led-summary`
- Unknown section kinds hard-fail.
- Visual carry-forward rules:
  - copy only in-scope visuals that materially affect approval
  - place them in `### Visual Evidence` inside the most relevant required section
  - if the profile sets `default_visual_section`, prefer that section and keep visuals there when present
  - precede each carried-forward visual with `- Source: <resolved canonical path> :: <exact heading>`
  - copy Mermaid fence contents exactly; do not redraw, rename, or reinterpret diagrams
- Glance metrics:
  - default source = approval Markdown
  - optional source = canonical artifact extraction when a profile requests it
- Traceability map rules:
  - every substantive claim uses this exact three-line block:
    - `- [Tn] Claim: <summary>`
    - `  - Source: <resolved canonical path> :: <exact heading>`
    - `  - Evidence quote: "<verbatim quote from that canonical section>"`
- Validator status rules:
  - include both `Canonical validator` and `Approval-view validator`
  - record command and result for each
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
- HTML rules:
  - one self-contained HTML file with inline CSS/JS; deterministic CDN fonts and Mermaid runtime are allowed
  - same section order and snapshot identity as Markdown
  - keep snapshot identity fields visible only in the final `Snapshot Identity` section, except for the required review-target title
  - include top-level `At a Glance` summary derived from the active profile's glance cards
  - add responsive section navigation when the page has 4+ top-level sections
  - render by section `kind`, with styling driven mainly by `kind`, `tone`, and `emphasis`
  - render section `why` subtly but visibly
  - keep `Snapshot Identity` visually recessed
- Reporting rules:
  - when presenting an HTML approval view in terminal/chat, include the resolved HTML filesystem path and matching absolute `file://` URI
- Do not add facts, repo analysis, or workflow policy not present in the canonical artifact or explicit pack snapshot.

## Inputs

- review mode: `artifact` | `artifact-revised` | `pack` | `pack-revised`
- one canonical artifact path or one explicit canonical artifact set
- resolved approval output paths
- selected approval profile or built-in fallback
- canonical validator command and result
- carried-forward visual evidence when in scope

## Outputs

- one Markdown approval view for the exact active snapshot
- one HTML approval view for the same snapshot
- deterministic scaffold, render, and validation helpers under `./scripts/`
- shared HTML shell under `./assets/approval-view-shell.html`

## Workflow

1. Confirm the canonical artifact or explicit pack snapshot already passed its validator.
2. Resolve the profile with the routing rules above.
3. Scaffold from `./scripts/scaffold_approval_view.py` when helpful.
4. Compute snapshot hashes from the exact canonical bytes.
5. Carry forward in-scope visuals into `### Visual Evidence` inside the relevant required section.
6. Write only claims backed by the active canonical snapshot and record exact traceability.
7. In revised mode, prepend `Change Summary` and keep `Snapshot Identity` last.
8. Render HTML with `python3 ./scripts/render_approval_view_html.py <approval-md> <approval-html>`.
9. Validate with the correct mode:
   - artifact: `bash ./scripts/validate_approval_view.sh artifact <canonical-file> <approval-md> <approval-html>`
   - artifact-revised: `bash ./scripts/validate_approval_view.sh artifact-revised <canonical-file> <approval-md> <approval-html>`
   - pack: `bash ./scripts/validate_approval_view.sh pack <approval-md> <approval-html> <canonical-file>...`
   - pack-revised: `bash ./scripts/validate_approval_view.sh pack-revised <approval-md> <approval-html> <canonical-file>...`
10. When handing the review over, report the resolved HTML path and matching absolute `file://` URI.
11. If validation fails, revise the approval view before using it for approval.

## Validation

- Confirm Markdown sections match the selected profile exactly, with `Snapshot Identity` last.
- Confirm revised views prepend `Change Summary` and include `Previous snapshot SHA-256:`.
- Confirm unsupported section kinds fail closed.
- Confirm carried-forward visuals stay inside required sections and respect `default_visual_section` when present.
- Confirm traceability headings and quotes resolve exactly against the in-scope canonical snapshot.
- Confirm snapshot hashes and `updated_at` fields match the current canonical bytes exactly.
- Confirm HTML and Markdown point at the same snapshot.
- Confirm HTML emits `data-section-tone` and `data-section-emphasis`, visible section `why`, section-kind markers, glance summary, and responsive navigation when required.
- Confirm glance cards can derive from approval Markdown or canonical extraction, according to the profile.
- Confirm pack review uses the coordinator-owned pack profile when root-skill routing resolves cleanly, else the built-in fallback.
- Run the shared validator before asking for approval.
