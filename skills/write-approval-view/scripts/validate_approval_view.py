#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass
from datetime import datetime
from html import unescape
from pathlib import Path

from approval_profiles import glance_cards_for_mode, load_review_profile, section_spec_by_kind, section_specs


USAGE = """Usage:
  validate_approval_view.py artifact <canonical-file> <approval-md> <approval-html>
  validate_approval_view.py artifact-revised <canonical-file> <approval-md> <approval-html>
  validate_approval_view.py pack <approval-md> <approval-html> <canonical-file>...
  validate_approval_view.py pack-revised <approval-md> <approval-html> <canonical-file>...
"""

MERMAID_FENCE_PATTERN = re.compile(r"^```mermaid\s*$", re.IGNORECASE | re.MULTILINE)
MARKDOWN_TABLE_SEPARATOR_PATTERN = re.compile(r"^\|?(\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$")


@dataclass
class TraceEntry:
    claim_id: str
    claim: str
    source_path: str
    heading: str
    evidence_quote: str


@dataclass
class CanonicalSnapshot:
    path: str
    text: str


def fail(message: str) -> None:
    raise ValueError(message)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_iso8601_z(value: str, field_name: str) -> None:
    if not value.endswith("Z"):
        fail(f"{field_name} must end with Z: {value}")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        fail(f"{field_name} must be valid UTC ISO 8601: {value}")


def parse_frontmatter_updated_at(markdown_text: str, path: Path) -> str:
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        fail(f"Canonical artifact missing frontmatter: {path}")

    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^updated_at:\s*(.+)$", line)
        if match:
            updated_at = match.group(1).strip()
            parse_iso8601_z(updated_at, f"updated_at in {path}")
            return updated_at

    fail(f"Canonical artifact missing updated_at in frontmatter: {path}")


def trim_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def parse_sections(markdown_text: str) -> list[tuple[str, list[str]]]:
    sections: list[tuple[str, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in markdown_text.splitlines():
        if line.startswith("## "):
            if current_title is not None:
                sections.append((current_title, trim_blank_lines(current_lines)))
            current_title = line[3:].strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections.append((current_title, trim_blank_lines(current_lines)))

    return sections


def section_map(markdown_text: str) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = {}
    for title, lines in parse_sections(markdown_text):
        if title in mapping:
            fail(f"Duplicate approval-view section: {title}")
        mapping[title] = lines
    return mapping


def require_sections(markdown_text: str, expected_specs: list[dict[str, object]]) -> list[str]:
    sections = parse_sections(markdown_text)
    titles = [title for title, _ in sections]
    expected = [str(spec["title"]) for spec in expected_specs]
    if titles != expected:
        fail(
            "Approval-view sections must match the selected approval profile exactly. "
            f"Expected {expected}; found {titles}"
        )
    return titles


def nonempty_section(lines: list[str], title: str) -> None:
    if not any(line.strip() for line in lines):
        fail(f"Section is empty: {title}")


def extract_bullet_value(lines: list[str], label: str) -> str:
    pattern = re.compile(rf"^- {re.escape(label)}:\s*(.+)$")
    for line in lines:
        match = pattern.match(line)
        if match:
            return match.group(1).strip()
    fail(f"Missing snapshot field: {label}")


def parse_snapshot_identity_artifact(lines: list[str], canonical_path: Path, revised: bool) -> dict[str, str]:
    for required in [
        "Review type",
        "Approval mode",
        "Canonical artifact",
        "Snapshot SHA-256",
        "Canonical updated_at",
        "Approval view generated_at",
    ]:
        extract_bullet_value(lines, required)

    data = {
        "review_type": extract_bullet_value(lines, "Review type"),
        "approval_mode": extract_bullet_value(lines, "Approval mode"),
        "canonical_artifact": extract_bullet_value(lines, "Canonical artifact"),
        "snapshot_sha256": extract_bullet_value(lines, "Snapshot SHA-256"),
        "canonical_updated_at": extract_bullet_value(lines, "Canonical updated_at"),
        "approval_view_generated_at": extract_bullet_value(lines, "Approval view generated_at"),
    }

    expected_mode = "Revised" if revised else "Initial"
    if data["review_type"] != "Artifact":
        fail(f"Review type must be Artifact, found: {data['review_type']}")
    if data["approval_mode"] != expected_mode:
        fail(f"Approval mode must be {expected_mode}, found: {data['approval_mode']}")
    if Path(data["canonical_artifact"]).resolve() != canonical_path.resolve():
        fail("Canonical artifact path in approval view does not match validator input")
    if not re.fullmatch(r"[0-9a-f]{64}", data["snapshot_sha256"]):
        fail("Snapshot SHA-256 must be 64 lowercase hex characters")
    parse_iso8601_z(data["canonical_updated_at"], "Canonical updated_at")
    parse_iso8601_z(data["approval_view_generated_at"], "Approval view generated_at")
    return data


def parse_pack_root(lines: list[str]) -> str:
    return extract_bullet_value(lines, "Spec-pack root")


def parse_included_snapshots(lines: list[str]) -> list[dict[str, str]]:
    included_snapshots: list[dict[str, str]] = []
    in_snapshot_list = False

    for line in lines:
        if line == "- Included snapshots:":
            in_snapshot_list = True
            continue
        if in_snapshot_list and re.match(r"^- [^ ]", line):
            break
        if not in_snapshot_list:
            continue
        match = re.match(r"^  - (.+?) \| SHA-256: ([0-9a-f]{64}) \| updated_at: (.+)$", line)
        if match:
            path_value, sha_value, updated_at = match.groups()
            parse_iso8601_z(updated_at.strip(), "Included snapshot updated_at")
            included_snapshots.append(
                {
                    "path": path_value.strip(),
                    "sha256": sha_value.strip(),
                    "updated_at": updated_at.strip(),
                }
            )

    if not included_snapshots:
        fail("Snapshot Identity must include one or more Included snapshots entries")

    return included_snapshots


def compute_pack_snapshot_hash(canonical_paths: list[Path]) -> tuple[str, list[dict[str, str]], str]:
    normalized = sorted(path.resolve() for path in canonical_paths)
    records: list[dict[str, str]] = []
    aggregate_lines: list[str] = []

    for path in normalized:
        text = read_text(path)
        file_hash = sha256_file(path)
        updated_at = parse_frontmatter_updated_at(text, path)
        resolved = str(path)
        aggregate_lines.append(f"{resolved}\t{file_hash}\n")
        records.append({"path": resolved, "sha256": file_hash, "updated_at": updated_at})

    aggregate_hash = hashlib.sha256("".join(aggregate_lines).encode("utf-8")).hexdigest()
    root = str(Path(os.path.commonpath([str(path.parent) for path in normalized])).resolve())
    return aggregate_hash, records, root


def parse_snapshot_identity_pack(lines: list[str], canonical_paths: list[Path], revised: bool) -> dict[str, object]:
    for required in [
        "Review type",
        "Approval mode",
        "Spec-pack root",
        "Pack snapshot SHA-256",
        "Approval view generated_at",
    ]:
        extract_bullet_value(lines, required)

    included_snapshots = parse_included_snapshots(lines)
    data: dict[str, object] = {
        "review_type": extract_bullet_value(lines, "Review type"),
        "approval_mode": extract_bullet_value(lines, "Approval mode"),
        "spec_pack_root": parse_pack_root(lines),
        "pack_snapshot_sha256": extract_bullet_value(lines, "Pack snapshot SHA-256"),
        "approval_view_generated_at": extract_bullet_value(lines, "Approval view generated_at"),
        "included_snapshots": included_snapshots,
    }

    expected_mode = "Revised" if revised else "Initial"
    if data["review_type"] != "Pack":
        fail(f"Review type must be Pack, found: {data['review_type']}")
    if data["approval_mode"] != expected_mode:
        fail(f"Approval mode must be {expected_mode}, found: {data['approval_mode']}")
    if not re.fullmatch(r"[0-9a-f]{64}", str(data["pack_snapshot_sha256"])):
        fail("Pack snapshot SHA-256 must be 64 lowercase hex characters")
    parse_iso8601_z(str(data["approval_view_generated_at"]), "Approval view generated_at")

    expected_hash, expected_records, expected_root = compute_pack_snapshot_hash(canonical_paths)
    if str(data["spec_pack_root"]) != expected_root:
        fail("Spec-pack root in approval view does not match canonical artifact set")
    if str(data["pack_snapshot_sha256"]) != expected_hash:
        fail("Pack snapshot SHA-256 does not match canonical artifact set")

    actual_records = [
        {
            "path": str(Path(record["path"]).resolve()),
            "sha256": record["sha256"],
            "updated_at": record["updated_at"],
        }
        for record in included_snapshots
    ]
    if actual_records != expected_records:
        fail("Included snapshots block does not match the canonical artifact set exactly")

    return data


def validate_change_summary(lines: list[str]) -> None:
    previous_hash = extract_bullet_value(lines, "Previous snapshot SHA-256")
    if not re.fullmatch(r"[0-9a-f]{64}", previous_hash):
        fail("Previous snapshot SHA-256 must be 64 lowercase hex characters")

    delta_lines = [line for line in lines if line.startswith("- ") and not line.startswith("- Previous snapshot SHA-256:")]
    if not delta_lines:
        fail("Change Summary must include at least one delta bullet or '- None'")


def validate_scope(lines: list[str]) -> None:
    if "- In scope:" not in lines:
        fail("Scope section must include '- In scope:'")
    if "- Out of scope:" not in lines:
        fail("Scope section must include '- Out of scope:'")


def group_top_level_bullets(lines: list[str]) -> list[list[str]]:
    groups: list[list[str]] = []
    current: list[str] | None = None
    in_code = False

    for line in lines:
        if line.startswith("```"):
            if current is not None:
                current.append(line)
            in_code = not in_code
            continue
        if in_code:
            if current is not None:
                current.append(line)
            continue
        if line.startswith("- "):
            if current is not None:
                groups.append(trim_blank_lines(current))
            current = [line]
        elif current is not None:
            current.append(line)

    if current is not None:
        groups.append(trim_blank_lines(current))

    return [group for group in groups if group]


def bullet_text(group: list[str]) -> str:
    if not group:
        return ""
    return re.sub(r"^-\s+", "", group[0]).strip()


def count_meaningful_groups(lines: list[str]) -> int:
    groups = group_top_level_bullets(lines)
    meaningful = [group for group in groups if bullet_text(group).lower() != "none"]
    return len(meaningful)


def validate_list_like_section(lines: list[str], title: str) -> None:
    if count_meaningful_groups(lines) == 0 and "- None" not in lines:
        fail(f"{title} must contain one or more top-level bullets or '- None'")


def validate_paired_lists(lines: list[str], title: str) -> None:
    if count_meaningful_groups(lines) < 2:
        fail(f"{title} must contain at least two contrasted top-level list groups")


def has_markdown_table(lines: list[str]) -> bool:
    for index in range(len(lines) - 1):
        if lines[index].strip().startswith("|") and MARKDOWN_TABLE_SEPARATOR_PATTERN.match(lines[index + 1].strip()):
            return True
    return False


def validate_matrix(lines: list[str], title: str) -> None:
    if has_markdown_table(lines):
        return
    if count_meaningful_groups(lines) == 0:
        fail(f"{title} must contain a Markdown table or a deterministic bullet-row fallback")


def parse_traceability(lines: list[str]) -> list[TraceEntry]:
    entries: list[TraceEntry] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        claim_match = re.match(r"^- \[([^\]]+)\] Claim: (.+)$", line)
        if not claim_match:
            fail(f"Invalid Traceability Map entry: {line}")
        if i + 2 >= len(lines):
            fail(f"Incomplete Traceability Map entry for {claim_match.group(1).strip()}")
        source_match = re.match(r"^  - Source: (.+?) :: (.+)$", lines[i + 1])
        quote_match = re.match(r'^  - Evidence quote: "(.*)"$', lines[i + 2])
        if not source_match:
            fail(f"Traceability entry {claim_match.group(1).strip()} missing valid Source line")
        if not quote_match:
            fail(f"Traceability entry {claim_match.group(1).strip()} missing valid Evidence quote line")
        entries.append(
            TraceEntry(
                claim_id=claim_match.group(1).strip(),
                claim=claim_match.group(2).strip(),
                source_path=source_match.group(1).strip(),
                heading=source_match.group(2).strip(),
                evidence_quote=quote_match.group(1),
            )
        )
        i += 3

    if not entries:
        fail("Traceability Map must include at least one substantive claim")

    return entries


def parse_heading_blocks(markdown_text: str) -> dict[str, str]:
    lines = markdown_text.splitlines()
    headings: list[tuple[int, int, str]] = []
    blocks: dict[str, str] = {}

    for index, line in enumerate(lines):
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            headings.append((index, len(match.group(1)), match.group(2).strip()))

    for idx, (start_index, level, title) in enumerate(headings):
        if title in blocks:
            fail(f"Canonical artifact contains duplicate heading title: {title}")
        end_index = len(lines)
        for next_index in range(idx + 1, len(headings)):
            candidate_index, candidate_level, _ = headings[next_index]
            if candidate_level <= level:
                end_index = candidate_index
                break
        blocks[title] = "\n".join(lines[start_index:end_index])

    return blocks


def validate_traceability(entries: list[TraceEntry], allowed_paths: set[str], canonical_texts: dict[str, str]) -> None:
    heading_cache = {path: parse_heading_blocks(text) for path, text in canonical_texts.items()}
    for entry in entries:
        resolved_source = str(Path(entry.source_path).resolve())
        if resolved_source not in allowed_paths:
            fail(f"Traceability entry {entry.claim_id} references an out-of-scope canonical artifact")
        heading_blocks = heading_cache[resolved_source]
        if entry.heading not in heading_blocks:
            fail(f"Traceability entry {entry.claim_id} references missing heading '{entry.heading}' in {resolved_source}")
        if entry.evidence_quote not in heading_blocks[entry.heading]:
            fail(
                f"Traceability entry {entry.claim_id} quote not found in heading '{entry.heading}' of {resolved_source}"
            )


def validate_validator_status(lines: list[str], mode: str) -> None:
    text = "\n".join(lines)
    canonical_block = re.search(r"- Canonical validator:\n  - Command: (.+)\n  - Result: (.+)", text)
    approval_block = re.search(r"- Approval-view validator:\n  - Command: (.+)\n  - Result: (.+)", text)
    if not canonical_block:
        fail("Validator Status must include Canonical validator command and result")
    if not approval_block:
        fail("Validator Status must include Approval-view validator command and result")

    canonical_result = canonical_block.group(2).strip()
    approval_command = approval_block.group(1).strip()
    approval_result = approval_block.group(2).strip()

    if canonical_result != "Passed":
        fail("Canonical validator result must be Passed")
    if approval_result != "Passed":
        fail("Approval-view validator result must be Passed")
    if "validate_approval_view.sh" not in approval_command:
        fail("Approval-view validator command must call validate_approval_view.sh")
    if mode not in approval_command:
        fail(f"Approval-view validator command must include the current mode: {mode}")


def validate_placeholders(markdown_text: str) -> None:
    if re.search(r"\[(?:TODO|todo):[^\]]+\]", markdown_text):
        fail("Approval view still contains unresolved [TODO: ...] placeholders")
    if re.search(r"<[^>\n]+>", markdown_text):
        fail("Approval view still contains unresolved <...> placeholders")


def extract_html_metadata(html_text: str) -> dict[str, object]:
    match = re.search(r'<script id="approval-view-metadata" type="application/json">(.*?)</script>', html_text, re.DOTALL)
    if not match:
        fail("HTML approval view missing approval-view-metadata JSON block")
    try:
        return json.loads(unescape(match.group(1)))
    except json.JSONDecodeError:
        fail("HTML approval view metadata JSON is invalid")


def approval_view_title(review_type: str, canonical_artifact: str | None = None, spec_pack_root: str | None = None) -> str:
    if review_type == "Artifact":
        if canonical_artifact:
            artifact_name = Path(canonical_artifact).name or canonical_artifact
            return f"Artifact Approval View: {artifact_name}"
        return "Artifact Approval View"
    if review_type == "Pack":
        if spec_pack_root:
            pack_name = Path(spec_pack_root).name or spec_pack_root
            return f"Pack Approval View: {pack_name}"
        return "Pack Approval View"
    fail(f"Unsupported review type for HTML title: {review_type}")


def extract_html_value(html_text: str, pattern: str, error_message: str) -> str:
    match = re.search(pattern, html_text, re.DOTALL)
    if not match:
        fail(error_message)
    return unescape(match.group(1)).strip()


def parse_headings(markdown_text: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for line in markdown_text.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if match:
            headings.append((len(match.group(1)), match.group(2).strip()))
    return headings


def count_heading_prefix(canonical_snapshots: list[CanonicalSnapshot], extractor: dict[str, object]) -> int:
    heading_level = int(extractor.get("heading_level") or 3)
    prefix = str(extractor.get("heading_prefix") or "")
    count = 0
    for snapshot in canonical_snapshots:
        for level, title in parse_headings(snapshot.text):
            if level != heading_level:
                continue
            if prefix and not title.startswith(prefix):
                continue
            count += 1
    return count


def count_visual_evidence_items(markdown_text: str) -> int:
    return len(re.findall(r"^- Source: ", markdown_text, re.MULTILINE))


def snapshot_canonical_sources(review_type: str, canonical_files: list[Path]) -> list[CanonicalSnapshot]:
    return [CanonicalSnapshot(path=str(path.resolve()), text=read_text(path)) for path in canonical_files]


def glance_metric_value(
    card: dict[str, object],
    markdown_text: str,
    sections: dict[str, list[str]],
    expected_specs: list[dict[str, object]],
    canonical_snapshots: list[CanonicalSnapshot],
) -> int:
    metric = str(card.get("metric") or "groups")
    source = str(card.get("source") or "approval")
    section_title = str(card.get("section_title") or "")

    if source == "canonical":
        extractor = dict(card.get("extractor") or {})
        if metric == "count-heading-prefix":
            return count_heading_prefix(canonical_snapshots, extractor)
        return 0

    if metric == "groups":
        return count_meaningful_groups(sections.get(section_title, []))
    if metric == "traceability_claims":
        lines = sections.get(section_title, []) if section_title else []
        if not lines:
            traceability_spec = next(spec for spec in expected_specs if spec["kind"] == "traceability")
            lines = sections[str(traceability_spec["title"])]
        return len(parse_traceability(lines))
    if metric == "validator_checks":
        lines = sections.get(section_title, []) if section_title else []
        if not lines:
            validator_spec = next(spec for spec in expected_specs if spec["kind"] == "validator")
            lines = sections[str(validator_spec["title"])]
        return len(re.findall(r"^  - Result: Passed$", "\n".join(lines), re.MULTILINE))
    if metric == "visuals":
        return count_visual_evidence_items(markdown_text)
    return 0


def derive_expected_rich_metadata(
    markdown_text: str,
    expected_specs: list[dict[str, object]],
    sections: dict[str, list[str]],
    profile: dict[str, object],
    revised: bool,
    canonical_files: list[Path],
) -> dict[str, object]:
    canonical_snapshots = snapshot_canonical_sources(str(profile["review_type"]), canonical_files)
    glance = {}
    for raw_card in glance_cards_for_mode(profile, revised):
        card = dict(raw_card)
        glance[str(card.get("label") or "Review")] = str(
            glance_metric_value(card, markdown_text, sections, expected_specs, canonical_snapshots)
        )
    return {
        "sections": [
            {
                "id": f"section-{spec['key']}",
                "key": spec["key"],
                "title": spec["title"],
                "kind": spec["kind"],
                "tone": spec["tone"],
                "emphasis": spec["emphasis"],
            }
            for spec in expected_specs
        ],
        "glance": glance,
        "has_mermaid": bool(MERMAID_FENCE_PATTERN.search(markdown_text)),
        "has_toc": len(expected_specs) >= 4,
    }


def unique_preserving_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    output: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        output.append(value)
    return output


def validate_visual_placement(sections: dict[str, list[str]], expected_specs: list[dict[str, object]], profile: dict[str, object]) -> None:
    default_key = str(profile.get("default_visual_section") or "").strip()
    if not default_key:
        return

    visual_titles = [title for title, lines in sections.items() if any(line.startswith("- Source: ") for line in lines)]
    if not visual_titles:
        return

    matching_spec = next((spec for spec in expected_specs if str(spec["key"]) == default_key), None)
    if matching_spec is None:
        fail(f"default_visual_section '{default_key}' not found in expected specs")

    expected_title = str(matching_spec["title"])
    if any(title != expected_title for title in visual_titles):
        fail(f"Visual Evidence must appear in the preferred default_visual_section '{expected_title}' when visuals are present")


def validate_html(
    html_text: str,
    markdown_text: str,
    expected_specs: list[dict[str, object]],
    sections: dict[str, list[str]],
    expected_metadata: dict[str, object],
    expected_title: str,
    review_type: str,
    profile: dict[str, object],
    revised: bool,
    canonical_files: list[Path],
) -> None:
    metadata = extract_html_metadata(html_text)
    for key, value in expected_metadata.items():
        if metadata.get(key) != value:
            fail(f"HTML metadata mismatch for {key}")

    if metadata.get("profile_id") != profile.get("profile_id"):
        fail("HTML metadata mismatch for profile_id")
    if metadata.get("profile_source") != profile.get("source"):
        fail("HTML metadata mismatch for profile_source")

    derived = metadata.get("derived")
    if not isinstance(derived, dict):
        fail("HTML metadata missing derived rich-view metadata")

    expected_derived = derive_expected_rich_metadata(markdown_text, expected_specs, sections, profile, revised, canonical_files)
    for key, value in expected_derived.items():
        if derived.get(key) != value:
            fail(f"HTML derived metadata mismatch for {key}")

    page_title = extract_html_value(html_text, r"<title>(.*?)</title>", "HTML approval view missing <title>")
    if page_title != expected_title:
        fail(f"HTML <title> must be '{expected_title}', found '{page_title}'")

    header_title = extract_html_value(html_text, r"<h1>(.*?)</h1>", "HTML approval view missing page title <h1>")
    if header_title != expected_title:
        fail(f"HTML page title must be '{expected_title}', found '{header_title}'")

    if 'data-approval-view="rich-v1"' not in html_text:
        fail("HTML approval view must use the rich approval layout marker")
    if 'id="approval-glance"' not in html_text or 'data-approval-glance' not in html_text:
        fail("HTML approval view missing top-level glance summary")
    if html_text.count('data-glance-card') < len(expected_derived["glance"]):
        fail("HTML approval view missing one or more glance summary cards")

    section_markup = re.findall(
        r'<section[^>]+id="([^"]+)"[^>]+data-section-role="([^"]+)"[^>]+data-section-kind="([^"]+)"[^>]+data-section-style="([^"]+)"[^>]+data-section-tone="([^"]+)"[^>]+data-section-emphasis="([^"]+)"',
        html_text,
    )
    expected_section_markup = [
        (f"section-{spec['key']}", spec["key"], spec["kind"], spec["style"], spec["tone"], spec["emphasis"])
        for spec in expected_specs
    ]
    if section_markup != expected_section_markup:
        fail(
            "HTML section order or section markers do not match the selected approval profile. "
            f"Expected {expected_section_markup}; found {section_markup}"
        )

    for spec in expected_specs:
        title = str(spec["title"])
        if title not in html_text:
            fail(f"HTML approval view missing section title: {title}")
        why = str(spec.get("why") or "").strip()
        if why and why not in html_text:
            fail(f"HTML approval view missing visible section why text for {title}")

    if sum(1 for spec in expected_specs if str(spec.get("why") or "").strip()) > html_text.count('data-section-why'):
        fail("HTML approval view missing one or more visible section why markers")

    if expected_derived["has_toc"]:
        if 'id="approval-toc"' not in html_text:
            fail("HTML approval view missing responsive section navigation")
        toc_links = re.findall(r'<a[^>]+href="#([^"]+)"[^>]+data-toc-link', html_text)
        unique_links = unique_preserving_order(toc_links)
        expected_ids = [f"section-{spec['key']}" for spec in expected_specs]
        if unique_links != expected_ids:
            fail("HTML approval view TOC links do not match the selected approval profile")

    for spec in expected_specs:
        kind = str(spec["kind"])
        key = str(spec["key"])
        title = str(spec["title"])
        if kind == "change-summary" and f'data-change-summary="{key}"' not in html_text:
            fail(f"HTML approval view missing change-summary layout for {title}")
        if kind == "scope" and f'data-scope-grid="{key}"' not in html_text:
            fail(f"HTML approval view missing scope split layout for {title}")
        if kind == "validator":
            if f'data-validator-grid="{key}"' not in html_text or html_text.count('data-validator-card') < 2:
                fail(f"HTML approval view missing validator status cards for {title}")
        if kind == "timeline" and f'data-timeline="{key}"' not in html_text:
            fail(f"HTML approval view missing timeline layout for {title}")
        if kind == "snapshot" and f'data-snapshot-panel="{key}"' not in html_text:
            fail(f"HTML approval view missing recessed snapshot panel for {title}")
        if kind == "traceability":
            traceability_count = len(parse_traceability(sections[title]))
            if f'data-traceability-list="{key}"' not in html_text or html_text.count('data-traceability-item') < traceability_count:
                fail(f"HTML approval view missing traceability accordions for {title}")
        if kind == "cards" and f'data-card-grid="{key}"' not in html_text and count_meaningful_groups(sections[title]) > 0:
            fail(f"HTML approval view missing card grid for {title}")
        if kind == "callouts" and f'data-callout-stack="{key}"' not in html_text and count_meaningful_groups(sections[title]) > 0:
            fail(f"HTML approval view missing callout stack for {title}")
        if kind == "summary" and f'data-summary-section="{key}"' not in html_text:
            fail(f"HTML approval view missing summary layout for {title}")
        if kind == "diagram-led-summary" and f'data-diagram-led-summary="{key}"' not in html_text:
            fail(f"HTML approval view missing diagram-led-summary layout for {title}")
        if kind == "paired-lists" and f'data-paired-lists="{key}"' not in html_text:
            fail(f"HTML approval view missing paired-lists layout for {title}")
        if kind == "checklist" and f'data-checklist="{key}"' not in html_text:
            fail(f"HTML approval view missing checklist layout for {title}")
        if kind == "ledger" and f'data-ledger="{key}"' not in html_text:
            fail(f"HTML approval view missing ledger layout for {title}")
        if kind == "matrix" and f'data-matrix="{key}"' not in html_text:
            fail(f"HTML approval view missing matrix layout for {title}")
        if kind == "roster" and f'data-roster="{key}"' not in html_text:
            fail(f"HTML approval view missing roster layout for {title}")

    if review_type == "Pack" and 'data-snapshot-table' not in html_text:
        fail("Pack approval HTML must render included snapshots as a semantic table")

    if expected_derived["has_mermaid"]:
        for marker in [
            'data-mermaid-shell',
            'data-mermaid-source',
            'data-mermaid-source-detail',
            'language-mermaid',
            'cdn.jsdelivr.net/npm/mermaid@11',
            'data-zoom-action',
        ]:
            if marker not in html_text:
                fail(f"HTML approval view missing Mermaid rich-render marker: {marker}")


def validate_common_sections(
    sections: dict[str, list[str]],
    mode: str,
    expected_specs: list[dict[str, object]],
    profile: dict[str, object],
) -> list[TraceEntry]:
    traceability: list[TraceEntry] = []

    for spec in expected_specs:
        title = str(spec["title"])
        kind = str(spec["kind"])
        lines = sections[title]
        nonempty_section(lines, title)

        if kind == "change-summary":
            validate_change_summary(lines)
        elif kind == "scope":
            validate_scope(lines)
        elif kind == "paired-lists":
            validate_paired_lists(lines, title)
        elif kind in {"checklist", "ledger", "roster", "cards", "callouts", "timeline"}:
            validate_list_like_section(lines, title)
        elif kind == "matrix":
            validate_matrix(lines, title)
        elif kind == "traceability":
            traceability = parse_traceability(lines)
        elif kind == "validator":
            validate_validator_status(lines, mode)

    validate_visual_placement(sections, expected_specs, profile)
    return traceability


def validate_artifact_mode(mode: str, canonical_file: Path, approval_md: Path, approval_html: Path, revised: bool) -> None:
    if not canonical_file.is_file():
        fail(f"Canonical artifact not found: {canonical_file}")
    if not approval_md.is_file():
        fail(f"Approval Markdown not found: {approval_md}")
    if not approval_html.is_file():
        fail(f"Approval HTML not found: {approval_html}")

    canonical_text = read_text(canonical_file)
    approval_md_text = read_text(approval_md)
    approval_html_text = read_text(approval_html)
    validate_placeholders(approval_md_text)

    profile = load_review_profile("artifact", canonical_path=canonical_file)
    expected_specs = section_specs(profile, revised)
    require_sections(approval_md_text, expected_specs)
    sections = section_map(approval_md_text)
    snapshot_title = str(section_spec_by_kind(profile, revised)["snapshot"]["title"])
    snapshot = parse_snapshot_identity_artifact(sections[snapshot_title], canonical_file, revised)

    expected_hash = sha256_file(canonical_file)
    expected_updated_at = parse_frontmatter_updated_at(canonical_text, canonical_file)
    if snapshot["snapshot_sha256"] != expected_hash:
        fail("Snapshot SHA-256 does not match canonical artifact bytes")
    if snapshot["canonical_updated_at"] != expected_updated_at:
        fail("Canonical updated_at does not match canonical artifact frontmatter")

    traceability = validate_common_sections(sections, mode, expected_specs, profile)
    allowed_path = str(canonical_file.resolve())
    validate_traceability(traceability, {allowed_path}, {allowed_path: canonical_text})

    expected_metadata = {
        "review_type": "Artifact",
        "approval_mode": snapshot["approval_mode"],
        "canonical_artifact": snapshot["canonical_artifact"],
        "snapshot_sha256": snapshot["snapshot_sha256"],
        "canonical_updated_at": snapshot["canonical_updated_at"],
        "approval_view_generated_at": snapshot["approval_view_generated_at"],
        "profile_id": profile["profile_id"],
        "profile_source": profile["source"],
    }
    expected_title = approval_view_title("Artifact", canonical_artifact=snapshot["canonical_artifact"])
    validate_html(
        approval_html_text,
        approval_md_text,
        expected_specs,
        sections,
        expected_metadata,
        expected_title,
        "Artifact",
        profile,
        revised,
        [canonical_file],
    )


def validate_pack_mode(mode: str, approval_md: Path, approval_html: Path, canonical_files: list[Path], revised: bool) -> None:
    if not canonical_files:
        fail("Pack mode requires one or more canonical files")
    for canonical_file in canonical_files:
        if not canonical_file.is_file():
            fail(f"Canonical artifact not found: {canonical_file}")
    if not approval_md.is_file():
        fail(f"Approval Markdown not found: {approval_md}")
    if not approval_html.is_file():
        fail(f"Approval HTML not found: {approval_html}")

    approval_md_text = read_text(approval_md)
    approval_html_text = read_text(approval_html)
    validate_placeholders(approval_md_text)

    profile = load_review_profile("pack", canonical_paths=canonical_files)
    expected_specs = section_specs(profile, revised)
    require_sections(approval_md_text, expected_specs)
    sections = section_map(approval_md_text)
    snapshot_title = str(section_spec_by_kind(profile, revised)["snapshot"]["title"])
    snapshot = parse_snapshot_identity_pack(sections[snapshot_title], canonical_files, revised)
    traceability = validate_common_sections(sections, mode, expected_specs, profile)

    canonical_texts = {str(path.resolve()): read_text(path) for path in canonical_files}
    validate_traceability(traceability, set(canonical_texts.keys()), canonical_texts)

    expected_metadata = {
        "review_type": "Pack",
        "approval_mode": snapshot["approval_mode"],
        "spec_pack_root": snapshot["spec_pack_root"],
        "pack_snapshot_sha256": snapshot["pack_snapshot_sha256"],
        "approval_view_generated_at": snapshot["approval_view_generated_at"],
        "included_snapshots": snapshot["included_snapshots"],
        "profile_id": profile["profile_id"],
        "profile_source": profile["source"],
    }
    expected_title = approval_view_title("Pack", spec_pack_root=str(snapshot["spec_pack_root"]))
    validate_html(
        approval_html_text,
        approval_md_text,
        expected_specs,
        sections,
        expected_metadata,
        expected_title,
        "Pack",
        profile,
        revised,
        canonical_files,
    )


def main() -> int:
    try:
        if len(sys.argv) < 5:
            print(USAGE, file=sys.stderr)
            return 1

        mode = sys.argv[1]
        if mode not in {"artifact", "artifact-revised", "pack", "pack-revised"}:
            print(USAGE, file=sys.stderr)
            return 1

        revised = mode.endswith("-revised")
        if mode.startswith("artifact"):
            if len(sys.argv) != 5:
                print(USAGE, file=sys.stderr)
                return 1
            canonical_file = Path(sys.argv[2]).resolve()
            approval_md = Path(sys.argv[3]).resolve()
            approval_html = Path(sys.argv[4]).resolve()
            validate_artifact_mode(mode, canonical_file, approval_md, approval_html, revised)
        else:
            if len(sys.argv) < 5:
                print(USAGE, file=sys.stderr)
                return 1
            approval_md = Path(sys.argv[2]).resolve()
            approval_html = Path(sys.argv[3]).resolve()
            canonical_files = [Path(arg).resolve() for arg in sys.argv[4:]]
            validate_pack_mode(mode, approval_md, approval_html, canonical_files, revised)

        print("Validation passed.")
        return 0
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
