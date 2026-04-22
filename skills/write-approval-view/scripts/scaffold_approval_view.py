#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

from approval_profiles import glance_cards_for_mode, load_review_profile, section_specs


USAGE = """Usage:
  scaffold_approval_view.py artifact <canonical-file>
  scaffold_approval_view.py artifact-revised <canonical-file>
  scaffold_approval_view.py pack [<canonical-file> ...]
  scaffold_approval_view.py pack-revised [<canonical-file> ...]
"""


def infer_paired_labels(title: str) -> tuple[str, str]:
    normalized = title.replace("/", " and ")
    for separator in (" and ", " vs ", " versus "):
        if separator in normalized:
            left, right = [part.strip(" :") for part in normalized.split(separator, 1)]
            if left and right:
                return left, right
    return ("First list", "Second list")


def wants_visual_placeholder(spec: dict[str, str], profile: dict[str, object]) -> bool:
    default_visual_section = str(profile.get("default_visual_section") or "").strip()
    if default_visual_section:
        return str(spec["key"]) == default_visual_section
    return spec["kind"] in {"summary", "diagram-led-summary"}


def visual_placeholder_block(spec: dict[str, str], profile: dict[str, object]) -> str:
    if not wants_visual_placeholder(spec, profile):
        return ""
    return (
        "\n\n### Visual Evidence\n\n"
        "- Source: [TODO: resolved canonical path] :: [TODO: exact heading]\n"
        "- [TODO: copy in-scope Mermaid or other visual content here exactly; delete this subsection if none are in scope]"
    )


def section_template(spec: dict[str, str], mode: str, review_type: str, profile: dict[str, object]) -> str:
    title = spec["title"]
    kind = spec["kind"]
    item_label = spec.get("item_label", "Item")
    empty_state = spec.get("empty_state", "None")

    if kind == "change-summary":
        return (
            f"## {title}\n\n"
            "- Previous snapshot SHA-256: [TODO: previous approved snapshot hash]\n"
            "- [TODO: one delta per bullet; use `- None` only when no substantive change exists]"
        )

    if kind == "summary":
        return (
            f"## {title}\n\n"
            "- [TODO: 1-3 concise bullets aligned to this artifact's review focus]"
            f"{visual_placeholder_block(spec, profile)}"
        )

    if kind == "diagram-led-summary":
        return (
            f"## {title}\n\n"
            "- [TODO: concise architecture or runtime framing bullets]\n"
            f"{visual_placeholder_block(spec, profile)}\n\n"
            "### Review Notes\n\n"
            "- [TODO: note the seams, boundaries, or claims the reviewer should inspect first]"
        )

    if kind == "scope":
        return (
            f"## {title}\n\n"
            "- In scope:\n"
            "  - [TODO: what this review settles]\n"
            "- Out of scope:\n"
            "  - [TODO: what this review does not settle]"
        )

    if kind == "paired-lists":
        left_label, right_label = infer_paired_labels(title)
        return (
            f"## {title}\n\n"
            f"- {left_label}:\n"
            "  - [TODO: first contrasted item]\n"
            f"- {right_label}:\n"
            "  - [TODO: second contrasted item]"
        )

    if kind == "cards":
        return f"## {title}\n\n- [TODO: one {item_label.lower()} per bullet; start with the reviewable point]"

    if kind == "checklist":
        return (
            f"## {title}\n\n"
            f"- [TODO: one {item_label.lower()} or checkpoint per bullet]\n"
            "  - [TODO: optional nested detail]\n"
            f"- [TODO: another {item_label.lower()}]"
        )

    if kind == "ledger":
        return (
            f"## {title}\n\n"
            f"- [TODO: one {item_label.lower()} row per bullet; keep the row label terse]\n"
            "  - [TODO: nested supporting detail when needed]"
        )

    if kind == "matrix":
        return (
            f"## {title}\n\n"
            "| Focus | Detail | Notes |\n"
            "| --- | --- | --- |\n"
            "| [TODO] | [TODO] | [TODO] |\n\n"
            "- If a Markdown table is not practical, use one top-level bullet per row with nested `Column: value` details."
        )

    if kind == "roster":
        return (
            f"## {title}\n\n"
            f"- [TODO: named {item_label.lower()} or actor]\n"
            "  - Role: [TODO]\n"
            "  - Relevance: [TODO]"
        )

    if kind == "callouts":
        return f"## {title}\n\n- [TODO: one {item_label.lower()} or unresolved item per bullet; use `- {empty_state}` when clear]"

    if kind == "timeline":
        return f"## {title}\n\n- [TODO: one {item_label.lower()} per bullet; order by sequence, dependency, or impact]"

    if kind == "traceability":
        return (
            f"## {title}\n\n"
            "- [T1] Claim: [TODO: substantive claim]\n"
            "  - Source: [TODO: resolved canonical path] :: [TODO: exact heading]\n"
            '  - Evidence quote: "[TODO: verbatim quote from the canonical section]"'
        )

    if kind == "validator":
        approval_command = "bash ./scripts/validate_approval_view.sh"
        if review_type == "artifact":
            approval_command = f"{approval_command} {mode} <canonical-file> <approval-md> <approval-html>"
        else:
            approval_command = f"{approval_command} {mode} <approval-md> <approval-html> <canonical-file>..."
        return (
            f"## {title}\n\n"
            "- Canonical validator:\n"
            "  - Command: [TODO: canonical validator command]\n"
            "  - Result: Passed\n"
            "- Approval-view validator:\n"
            f"  - Command: [TODO: {approval_command}]\n"
            "  - Result: Passed"
        )

    if kind == "snapshot":
        if review_type == "artifact":
            approval_mode = "Revised" if mode == "artifact-revised" else "Initial"
            return (
                f"## {title}\n\n"
                "- Review type: Artifact\n"
                f"- Approval mode: {approval_mode}\n"
                "- Canonical artifact: [TODO: resolved canonical path]\n"
                "- Snapshot SHA-256: [TODO: SHA-256 of canonical artifact bytes]\n"
                "- Canonical updated_at: [TODO: updated_at from canonical frontmatter]\n"
                "- Approval view generated_at: [TODO: UTC ISO 8601 timestamp]"
            )
        approval_mode = "Revised" if mode == "pack-revised" else "Initial"
        return (
            f"## {title}\n\n"
            "- Review type: Pack\n"
            f"- Approval mode: {approval_mode}\n"
            "- Spec-pack root: [TODO: resolved spec-pack root]\n"
            "- Pack snapshot SHA-256: [TODO: aggregate SHA-256 of sorted path + file-hash pairs]\n"
            "- Approval view generated_at: [TODO: UTC ISO 8601 timestamp]\n"
            "- Included snapshots:\n"
            "  - [TODO: resolved canonical path] | SHA-256: [TODO: file hash] | updated_at: [TODO: updated_at]"
        )

    return f"## {title}\n\n- [TODO: fill this section from the canonical artifact only]"


def main() -> int:
    if len(sys.argv) < 2:
        print(USAGE, file=sys.stderr)
        return 1

    mode = sys.argv[1]
    if mode not in {"artifact", "artifact-revised", "pack", "pack-revised"}:
        print(USAGE, file=sys.stderr)
        return 1

    review_type = "artifact" if mode.startswith("artifact") else "pack"
    revised = mode.endswith("revised")

    canonical_path = None
    canonical_paths: list[Path] | None = None
    if review_type == "artifact":
        if len(sys.argv) != 3:
            print(USAGE, file=sys.stderr)
            return 1
        canonical_path = Path(sys.argv[2]).resolve()
    else:
        canonical_paths = [Path(arg).resolve() for arg in sys.argv[2:]]

    profile = load_review_profile(review_type, canonical_path=canonical_path, canonical_paths=canonical_paths)
    _ = glance_cards_for_mode(profile, revised)

    lines = ["# Approval View", ""]
    for index, spec in enumerate(section_specs(profile, revised)):
        if index > 0:
            lines.append("")
        lines.append(section_template(spec, mode, review_type, profile))

    print("\n".join(lines))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
