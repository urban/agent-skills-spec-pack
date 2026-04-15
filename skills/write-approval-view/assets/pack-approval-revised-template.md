# Approval View

## Snapshot Identity

- Review type: Pack
- Approval mode: Revised
- Spec-pack root: [TODO: resolved spec-pack root]
- Pack snapshot SHA-256: [TODO: aggregate SHA-256 of sorted path + file-hash pairs]
- Approval view generated_at: [TODO: UTC ISO 8601 timestamp]
- Included snapshots:
  - [TODO: resolved canonical path] | SHA-256: [TODO: file hash] | updated_at: [TODO: updated_at]

## Change Summary

- Previous snapshot SHA-256: [TODO: prior approved pack snapshot hash]
- [TODO: delta summary bullet or None]

## Executive Summary

- [TODO: concise pack summary for approvers]

## Scope

- In scope:
  - [TODO: artifacts or decisions covered by this pack review]
- Out of scope:
  - [TODO: excluded artifacts, later phases, or unresolved follow-on work]

## Decisions Required for Approval

- [TODO: decision or None]

## Risks and Tradeoffs

- [TODO: risk, tradeoff, or None]

## Blockers and Unresolved Items

- [TODO: blocker, unresolved item, or None]

## Traceability Map

- [T1] Claim: [TODO: substantive pack-level claim]
  - Source: [TODO: resolved canonical path] :: [TODO: exact heading]
  - Evidence quote: "[TODO: verbatim quote from the canonical section]"

## Validator Status

- Canonical validator:
  - Command: [TODO: canonical validator commands summarized for this pack]
  - Result: Passed
- Approval-view validator:
  - Command: [TODO: bash ./scripts/validate_approval_view.sh pack-revised <approval-md> <approval-html> <canonical-file>...]
  - Result: Passed

## Downstream Impact if Approved

- [TODO: downstream effect of pack approval]
