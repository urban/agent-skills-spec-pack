#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from approval_profiles import glance_cards_for_mode, load_review_profile, section_spec_by_title

INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
INLINE_STRONG_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
INLINE_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BULLET_PATTERN = re.compile(r"^(\s*)-\s+(.*)$")
SUBHEADING_PATTERN = re.compile(r"^(#{3,6})\s+(.+)$")
TRACEABILITY_PATTERN = re.compile(r"^- \[([^\]]+)\] Claim: (.+)$")
SOURCE_PATTERN = re.compile(r"^  - Source: (.+?) :: (.+)$")
QUOTE_PATTERN = re.compile(r'^  - Evidence quote: "(.*)"$')
MERMAID_FENCE_PATTERN = re.compile(r"^```mermaid\s*$", re.IGNORECASE | re.MULTILINE)
MARKDOWN_TABLE_SEPARATOR_PATTERN = re.compile(r"^\|?(\s*:?-{3,}:?\s*\|)+\s*:?-{3,}:?\s*\|?$")

MERMAID_COUNTER = 0


@dataclass
class Section:
    title: str
    lines: list[str]


@dataclass
class TraceEntry:
    claim_id: str
    claim: str
    source_path: str
    heading: str
    evidence_quote: str


@dataclass
class ValidatorEntry:
    label: str
    command: str
    result: str


@dataclass
class ListItem:
    text: str
    continuation: list[str]
    children: list["ListItem"]


@dataclass
class SnapshotRecord:
    path: str
    sha256: str
    updated_at: str


@dataclass
class CanonicalSnapshot:
    path: str
    text: str


def usage() -> None:
    print("Usage: render_approval_view_html.py <approval-md> <approval-html>", file=sys.stderr)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def trim_blank_lines(lines: list[str]) -> list[str]:
    start = 0
    end = len(lines)
    while start < end and not lines[start].strip():
        start += 1
    while end > start and not lines[end - 1].strip():
        end -= 1
    return lines[start:end]


def parse_sections(markdown_text: str) -> list[Section]:
    sections: list[Section] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in markdown_text.splitlines():
        if line.startswith("## "):
            if current_title is not None:
                sections.append(Section(current_title, trim_blank_lines(current_lines)))
            current_title = line[3:].strip()
            current_lines = []
        elif current_title is not None:
            current_lines.append(line)

    if current_title is not None:
        sections.append(Section(current_title, trim_blank_lines(current_lines)))

    return sections


def extract_markdown_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Approval View"


def first_h1_removed(markdown_text: str) -> str:
    lines = markdown_text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).lstrip("\n")
    return markdown_text


def normalize_label(label: str) -> str:
    normalized = label.strip().lower().replace(" ", "_").replace("-", "_")
    normalized = normalized.replace("sha_256", "sha256")
    return normalized


def parse_snapshot_fields(lines: list[str]) -> tuple[list[tuple[str, str]], list[SnapshotRecord]]:
    fields: list[tuple[str, str]] = []
    records: list[SnapshotRecord] = []

    for line in lines:
        included_match = re.match(r"^  - (.+?) \| SHA-256: ([0-9a-f]{64}) \| updated_at: (.+)$", line)
        if included_match:
            records.append(
                SnapshotRecord(
                    path=included_match.group(1).strip(),
                    sha256=included_match.group(2).strip(),
                    updated_at=included_match.group(3).strip(),
                )
            )
            continue

        bullet_match = re.match(r"^- ([^:]+):\s*(.+)$", line)
        if bullet_match:
            fields.append((bullet_match.group(1).strip(), bullet_match.group(2).strip()))

    return fields, records


def extract_snapshot_metadata(sections: list[Section]) -> dict[str, object]:
    metadata: dict[str, object] = {}
    if not sections:
        return metadata

    fields, records = parse_snapshot_fields(sections[-1].lines)
    for label, value in fields:
        metadata[normalize_label(label)] = value.strip()
    if records:
        metadata["included_snapshots"] = [
            {"path": record.path, "sha256": record.sha256, "updated_at": record.updated_at}
            for record in records
        ]
    return metadata


def approval_view_title(markdown_text: str, metadata: dict[str, object]) -> str:
    review_type = str(metadata.get("review_type", "")).strip()
    if review_type == "Artifact":
        canonical_artifact = str(metadata.get("canonical_artifact", "")).strip()
        if canonical_artifact:
            artifact_name = Path(canonical_artifact).name or canonical_artifact
            return f"Artifact Approval View: {artifact_name}"
        return "Artifact Approval View"
    if review_type == "Pack":
        spec_pack_root = str(metadata.get("spec_pack_root", "")).strip()
        if spec_pack_root:
            pack_name = Path(spec_pack_root).name or spec_pack_root
            return f"Pack Approval View: {pack_name}"
        return "Pack Approval View"
    return extract_markdown_title(markdown_text)


def approval_view_subtitle(profile: dict[str, object]) -> str:
    return str(
        profile.get("subtitle")
        or "Glance-first approval surface with traceable evidence, structured review gates, and final snapshot metadata."
    )


def resolve_review_profile(metadata: dict[str, object]) -> tuple[dict[str, object], bool, list[Path]]:
    review_type_value = str(metadata.get("review_type", "")).strip()
    revised = str(metadata.get("approval_mode", "")).strip() == "Revised"

    if review_type_value == "Artifact":
        canonical_artifact = str(metadata.get("canonical_artifact", "")).strip()
        canonical_paths = [Path(canonical_artifact).resolve()] if canonical_artifact else []
        canonical_path = canonical_paths[0] if canonical_paths else None
        return load_review_profile("artifact", canonical_path=canonical_path), revised, canonical_paths

    if review_type_value == "Pack":
        canonical_paths: list[Path] = []
        for record in metadata.get("included_snapshots", []):
            if isinstance(record, dict) and record.get("path"):
                canonical_paths.append(Path(str(record["path"])).resolve())
        return load_review_profile("pack", canonical_paths=canonical_paths), revised, canonical_paths

    return load_review_profile("artifact"), revised, []


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = INLINE_LINK_PATTERN.sub(r'<a href="\2">\1</a>', escaped)
    escaped = INLINE_STRONG_PATTERN.sub(r"<strong>\1</strong>", escaped)
    escaped = INLINE_CODE_PATTERN.sub(r"<code>\1</code>", escaped)
    return escaped


def parse_list_items(lines: list[str], start: int = 0, indent: int = 0) -> tuple[list[ListItem], int]:
    items: list[ListItem] = []
    current_item: ListItem | None = None
    index = start

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            if current_item is not None:
                current_item.continuation.append("")
            index += 1
            continue

        match = BULLET_PATTERN.match(line)
        if match:
            current_indent = len(match.group(1))
            if current_indent < indent:
                break
            if current_indent > indent:
                if current_item is None:
                    break
                children, index = parse_list_items(lines, index, current_indent)
                current_item.children.extend(children)
                continue
            current_item = ListItem(match.group(2).strip(), [], [])
            items.append(current_item)
            index += 1
            continue

        if current_item is None:
            break

        required_prefix = " " * (indent + 2)
        if line.startswith(required_prefix):
            current_item.continuation.append(line[indent + 2 :])
        else:
            current_item.continuation.append(line.strip())
        index += 1

    return items, index


def render_list_items(items: list[ListItem], depth: int = 0) -> str:
    if not items:
        return ""

    output = [f'<ul class="rich-list rich-list--depth-{depth}">']
    for item in items:
        output.append("<li>")
        output.append(f'<div class="rich-list__text">{render_inline(item.text)}</div>')
        continuation_lines = trim_blank_lines(item.continuation)
        if continuation_lines:
            output.append(f'<div class="rich-list__detail">{render_fragment(continuation_lines, heading_level=5)}</div>')
        if item.children:
            output.append(render_list_items(item.children, depth + 1))
        output.append("</li>")
    output.append("</ul>")
    return "\n".join(output)


def next_mermaid_id() -> str:
    global MERMAID_COUNTER
    MERMAID_COUNTER += 1
    return f"approval-mermaid-{MERMAID_COUNTER}"


def render_mermaid_shell(code: str) -> str:
    shell_id = next_mermaid_id()
    escaped_code = html.escape(code)
    return f'''
<div class="diagram-shell mermaid-shell" data-mermaid-shell id="{shell_id}">
  <div class="diagram-shell__head">
    <div class="diagram-shell__label">Visual Evidence · Mermaid</div>
    <div class="zoom-controls" aria-label="Mermaid controls">
      <button type="button" data-zoom-action="out" aria-label="Zoom out">−</button>
      <button type="button" data-zoom-action="in" aria-label="Zoom in">+</button>
      <button type="button" data-zoom-action="reset" aria-label="Reset zoom">Reset</button>
      <button type="button" data-zoom-action="fit" aria-label="Fit diagram">Fit</button>
      <button type="button" data-zoom-action="expand" aria-label="Open expanded diagram">⛶</button>
    </div>
  </div>
  <div class="mermaid-wrap">
    <div class="mermaid-viewport" data-mermaid-viewport>
      <div class="mermaid-canvas" data-mermaid-canvas></div>
    </div>
  </div>
  <pre class="mermaid-source" data-mermaid-source hidden>{escaped_code}</pre>
  <details class="detail-panel source-detail" data-mermaid-source-detail>
    <summary>Raw Mermaid source</summary>
    <pre class="code-block"><code class="language-mermaid">{escaped_code}</code></pre>
  </details>
</div>
'''.strip()


def render_code_block(language: str, code: str) -> str:
    normalized_language = language.strip().lower()
    if normalized_language == "mermaid":
        return render_mermaid_shell(code)

    label = normalized_language or "text"
    return f'''
<div class="code-file">
  <div class="code-file__header">{html.escape(label)}</div>
  <pre class="code-block"><code class="language-{html.escape(label)}">{html.escape(code)}</code></pre>
</div>
'''.strip()


def render_fragment(lines: list[str], heading_level: int = 4) -> str:
    output: list[str] = []
    paragraph_lines: list[str] = []
    index = 0

    def flush_paragraph() -> None:
        nonlocal paragraph_lines
        if not paragraph_lines:
            return
        paragraph = " ".join(line.strip() for line in paragraph_lines if line.strip())
        if paragraph:
            output.append(f"<p>{render_inline(paragraph)}</p>")
        paragraph_lines = []

    while index < len(lines):
        raw_line = lines[index]

        if raw_line.startswith("```"):
            flush_paragraph()
            language = raw_line[3:].strip()
            code_lines: list[str] = []
            index += 1
            while index < len(lines) and not lines[index].startswith("```"):
                code_lines.append(lines[index])
                index += 1
            output.append(render_code_block(language, "\n".join(code_lines)))
            if index < len(lines) and lines[index].startswith("```"):
                index += 1
            continue

        heading_match = SUBHEADING_PATTERN.match(raw_line)
        if heading_match:
            flush_paragraph()
            level = min(heading_level, 6)
            output.append(f'<h{level} class="subheading">{html.escape(heading_match.group(2).strip())}</h{level}>')
            index += 1
            continue

        if BULLET_PATTERN.match(raw_line):
            flush_paragraph()
            list_lines = [raw_line]
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if candidate.startswith("```") or SUBHEADING_PATTERN.match(candidate):
                    break
                if not candidate.strip() or BULLET_PATTERN.match(candidate) or candidate.startswith(" "):
                    list_lines.append(candidate)
                    index += 1
                    continue
                break
            first_match = next((BULLET_PATTERN.match(line) for line in list_lines if BULLET_PATTERN.match(line)), None)
            indent = len(first_match.group(1)) if first_match else 0
            items, _ = parse_list_items(list_lines, 0, indent)
            output.append(render_list_items(items))
            continue

        if not raw_line.strip():
            flush_paragraph()
            index += 1
            continue

        paragraph_lines.append(raw_line)
        index += 1

    flush_paragraph()
    return "\n".join(output).strip()


def split_subsections(lines: list[str]) -> list[tuple[str | None, list[str]]]:
    sections: list[tuple[str | None, list[str]]] = []
    current_title: str | None = None
    current_lines: list[str] = []

    for line in lines:
        if line.startswith("### "):
            sections.append((current_title, trim_blank_lines(current_lines)))
            current_title = line[4:].strip()
            current_lines = []
        else:
            current_lines.append(line)

    sections.append((current_title, trim_blank_lines(current_lines)))
    return [(title, chunk) for title, chunk in sections if title is not None or chunk]


def partition_section_lines(lines: list[str]) -> tuple[list[str], list[tuple[str, list[str]]], list[str]]:
    main_lines: list[str] = []
    extra_subsections: list[tuple[str, list[str]]] = []
    visual_lines: list[str] = []

    for title, chunk in split_subsections(lines):
        if title is None:
            main_lines.extend(chunk)
        elif title == "Visual Evidence":
            visual_lines.extend(chunk)
        else:
            extra_subsections.append((title, chunk))

    return trim_blank_lines(main_lines), extra_subsections, trim_blank_lines(visual_lines)


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


def is_none_group(group: list[str]) -> bool:
    return bullet_text(group).lower() == "none"


def count_meaningful_groups(lines: list[str]) -> int:
    groups = group_top_level_bullets(lines)
    meaningful = [group for group in groups if not is_none_group(group)]
    return len(meaningful)


def render_extra_subsections(subsections: list[tuple[str, list[str]]]) -> str:
    if not subsections:
        return ""

    cards = []
    for title, chunk in subsections:
        cards.append(
            f'''
<article class="mini-panel">
  <h4>{html.escape(title)}</h4>
  <div class="mini-panel__body">{render_fragment(chunk, heading_level=5)}</div>
</article>
'''.strip()
        )

    return f'<div class="mini-panel-grid">{"".join(cards)}</div>'


def render_empty_state(message: str) -> str:
    return f'<div class="empty-state">{render_inline(message)}</div>'


def render_visual_evidence(lines: list[str]) -> str:
    if not lines:
        return ""

    items: list[tuple[str | None, str | None, list[str]]] = []
    current_source: str | None = None
    current_heading: str | None = None
    current_lines: list[str] = []

    for line in lines:
        match = re.match(r"^- Source: (.+?) :: (.+)$", line)
        if match:
            if current_source is not None or current_lines:
                items.append((current_source, current_heading, trim_blank_lines(current_lines)))
            current_source = match.group(1).strip()
            current_heading = match.group(2).strip()
            current_lines = []
            continue
        current_lines.append(line)

    if current_source is not None or current_lines:
        items.append((current_source, current_heading, trim_blank_lines(current_lines)))

    cards: list[str] = []
    for source_path, heading, chunk in items:
        source_html = ""
        if source_path is not None and heading is not None:
            source_html = f'''
<div class="evidence-source">
  <span class="evidence-source__label">Source</span>
  <code>{html.escape(source_path)}</code>
  <span class="evidence-source__sep">::</span>
  <code>{html.escape(heading)}</code>
</div>
'''.strip()
        body_html = render_fragment(chunk, heading_level=5) if chunk else render_empty_state("No additional visual notes.")
        cards.append(
            f'''
<article class="visual-card">
  {source_html}
  <div class="visual-card__body">{body_html}</div>
</article>
'''.strip()
        )

    return f'''
<div class="visual-evidence" data-visual-evidence>
  <div class="visual-evidence__label">Visual Evidence</div>
  <div class="visual-evidence__grid">{"".join(cards)}</div>
</div>
'''.strip()


def render_summary_points(groups: list[list[str]]) -> str:
    if not groups:
        return ""

    cards = []
    for index, group in enumerate(groups, start=1):
        cards.append(
            f'''
<article class="summary-point">
  <div class="summary-point__index">{index:02d}</div>
  <div class="summary-point__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
        )
    return f'<div class="summary-points">{"".join(cards)}</div>'


def render_change_summary(lines: list[str], section_key: str) -> str:
    groups = group_top_level_bullets(lines)
    previous_hash = "Unknown"
    deltas: list[list[str]] = []

    for group in groups:
        text = bullet_text(group)
        if text.startswith("Previous snapshot SHA-256:"):
            previous_hash = text.split(":", 1)[1].strip()
        else:
            deltas.append(group)

    if not deltas:
        deltas = [["- None"]]

    delta_cards = []
    for index, group in enumerate(deltas, start=1):
        delta_cards.append(
            f'''
<article class="delta-card">
  <div class="delta-card__label">Delta {index:02d}</div>
  <div class="delta-card__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
        )

    return f'''
<div class="hero-stack" data-hero-section data-change-summary="{html.escape(section_key)}">
  <div class="hero-note">
    <span class="hero-note__label">Previous snapshot</span>
    <code>{html.escape(previous_hash)}</code>
  </div>
  <div class="delta-grid" data-change-grid>
    {"".join(delta_cards)}
  </div>
</div>
'''.strip()


def render_summary_like(lines: list[str], section_key: str, empty_state: str, visual_first: bool = False) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    intro_lines: list[str] = []
    bullet_lines: list[str] = []
    seen_bullet = False

    for line in main_lines:
        if not seen_bullet and line.startswith("- "):
            seen_bullet = True
        if seen_bullet:
            bullet_lines.append(line)
        else:
            intro_lines.append(line)

    summary_points = render_summary_points(group_top_level_bullets(bullet_lines))
    intro_html = render_fragment(trim_blank_lines(intro_lines), heading_level=5) if trim_blank_lines(intro_lines) else ""
    extra_html = render_extra_subsections(extra_subsections)
    text_html = "".join(part for part in [intro_html, summary_points, extra_html] if part) or render_empty_state(empty_state)
    visuals_html = render_visual_evidence(visual_lines)

    if visual_first and visuals_html:
        return f'''
<div class="diagram-led" data-diagram-led-summary="{html.escape(section_key)}">
  <div class="diagram-led__visual">{visuals_html}</div>
  <div class="diagram-led__text">{text_html}</div>
</div>
'''.strip()

    if visuals_html:
        marker = "data-diagram-led-summary" if visual_first else "data-summary-section"
        return f'''
<div class="split-hero" {marker}="{html.escape(section_key)}">
  <div class="split-hero__main">{text_html}</div>
  <div class="split-hero__visual">{visuals_html}</div>
</div>
'''.strip()

    if visual_first:
        return f'<div class="hero-stack" data-hero-section data-diagram-led-summary="{html.escape(section_key)}">{text_html}</div>'
    return f'<div class="hero-stack" data-hero-section data-summary-section="{html.escape(section_key)}">{text_html}</div>'


def parse_scope(lines: list[str]) -> tuple[list[str], list[str]]:
    in_scope: list[str] = []
    out_scope: list[str] = []
    current: str | None = None

    for line in lines:
        if line == "- In scope:":
            current = "in"
            continue
        if line == "- Out of scope:":
            current = "out"
            continue
        if current == "in":
            in_scope.append(line)
        elif current == "out":
            out_scope.append(line)

    return trim_blank_lines(in_scope), trim_blank_lines(out_scope)


def render_scope(lines: list[str], section_key: str) -> str:
    in_scope, out_scope = parse_scope(lines)
    return f'''
<div class="scope-grid" data-scope-grid="{html.escape(section_key)}">
  <article class="scope-card scope-card--in">
    <div class="scope-card__label">In scope</div>
    <div class="scope-card__body">{render_fragment(in_scope, heading_level=5) if in_scope else render_empty_state("None")}</div>
  </article>
  <article class="scope-card scope-card--out">
    <div class="scope-card__label">Out of scope</div>
    <div class="scope-card__body">{render_fragment(out_scope, heading_level=5) if out_scope else render_empty_state("None")}</div>
  </article>
</div>
'''.strip()


def render_cards(lines: list[str], label_prefix: str, section_key: str, empty_state: str, marker: str, variant: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]

    if not groups:
        content_html = render_empty_state(empty_state)
    else:
        cards = []
        for index, group in enumerate(groups, start=1):
            cards.append(
                f'''
<article class="review-card review-card--{variant}">
  <div class="review-card__label">{html.escape(label_prefix)} {index:02d}</div>
  <div class="review-card__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        content_html = f'<div class="review-card-grid review-card-grid--{variant}" {marker}="{html.escape(section_key)}">{"".join(cards)}</div>'

    return "".join(
        part
        for part in [content_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def parse_named_panels(lines: list[str]) -> list[ListItem]:
    items, _ = parse_list_items(lines, 0, 0)
    return items


def render_paired_lists(lines: list[str], section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    panels = parse_named_panels(main_lines)

    if not panels:
        panels_html = render_empty_state(empty_state)
    else:
        rendered_panels = []
        for item in panels:
            panel_body_parts: list[str] = []
            continuation = trim_blank_lines(item.continuation)
            if continuation:
                panel_body_parts.append(render_fragment(continuation, heading_level=5))
            if item.children:
                panel_body_parts.append(render_list_items(item.children, depth=0))
            panel_body = "".join(panel_body_parts) or render_empty_state("None")
            rendered_panels.append(
                f'''
<article class="paired-panel">
  <h3>{html.escape(item.text.rstrip(':'))}</h3>
  <div class="paired-panel__body">{panel_body}</div>
</article>
'''.strip()
            )
        panels_html = f'<div class="paired-grid" data-paired-lists="{html.escape(section_key)}">{"".join(rendered_panels)}</div>'

    return "".join(
        part
        for part in [panels_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def render_checklist(lines: list[str], section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]

    if not groups:
        checklist_html = render_empty_state(empty_state)
    else:
        items = []
        for index, group in enumerate(groups, start=1):
            items.append(
                f'''
<li class="checklist-item">
  <div class="checklist-item__marker">{index:02d}</div>
  <div class="checklist-item__body">{render_fragment(group, heading_level=5)}</div>
</li>
'''.strip()
            )
        checklist_html = f'<ol class="checklist" data-checklist="{html.escape(section_key)}">{"".join(items)}</ol>'

    return "".join(
        part
        for part in [checklist_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def render_ledger(lines: list[str], section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]

    if not groups:
        ledger_html = render_empty_state(empty_state)
    else:
        rows = []
        for index, group in enumerate(groups, start=1):
            rows.append(
                f'''
<article class="ledger-row">
  <div class="ledger-row__index">{index:02d}</div>
  <div class="ledger-row__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        ledger_html = f'<div class="ledger" data-ledger="{html.escape(section_key)}">{"".join(rows)}</div>'

    return "".join(
        part
        for part in [ledger_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def render_roster(lines: list[str], section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]

    if not groups:
        roster_html = render_empty_state(empty_state)
    else:
        entries = []
        for group in groups:
            title = bullet_text(group)
            details = render_fragment(group[1:], heading_level=5) if len(group) > 1 else ""
            entries.append(
                f'''
<article class="roster-entry">
  <h3>{render_inline(title)}</h3>
  <div class="roster-entry__body">{details or render_empty_state("No additional role detail.")}</div>
</article>
'''.strip()
            )
        roster_html = f'<div class="roster" data-roster="{html.escape(section_key)}">{"".join(entries)}</div>'

    return "".join(
        part
        for part in [roster_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def split_table_row(line: str) -> list[str]:
    trimmed = line.strip().strip("|")
    return [cell.strip() for cell in trimmed.split("|")]


def extract_markdown_table(lines: list[str]) -> tuple[list[str], list[str], list[list[str]], list[str]]:
    for index in range(len(lines) - 1):
        if not lines[index].strip().startswith("|"):
            continue
        if not MARKDOWN_TABLE_SEPARATOR_PATTERN.match(lines[index + 1].strip()):
            continue
        end = index + 2
        while end < len(lines) and lines[end].strip().startswith("|"):
            end += 1
        headers = split_table_row(lines[index])
        rows = [split_table_row(line) for line in lines[index + 2 : end]]
        before = trim_blank_lines(lines[:index])
        after = trim_blank_lines(lines[end:])
        return before, headers, rows, after
    return trim_blank_lines(lines), [], [], []


def render_matrix(lines: list[str], section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    intro_lines, headers, rows, after_lines = extract_markdown_table(main_lines)

    intro_html = render_fragment(intro_lines, heading_level=5) if intro_lines else ""
    trailing_html = render_fragment(after_lines, heading_level=5) if after_lines else ""

    if headers:
        header_html = "".join(f"<th>{render_inline(header)}</th>" for header in headers)
        row_html = []
        for row in rows:
            padded = row + [""] * max(0, len(headers) - len(row))
            row_html.append("<tr>" + "".join(f"<td>{render_inline(cell)}</td>" for cell in padded[: len(headers)]) + "</tr>")
        matrix_html = f'''
<div class="table-wrap" data-matrix="{html.escape(section_key)}">
  <table class="matrix-table">
    <thead><tr>{header_html}</tr></thead>
    <tbody>{"".join(row_html)}</tbody>
  </table>
</div>
'''.strip()
    else:
        groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]
        if not groups:
            matrix_html = render_empty_state(empty_state)
        else:
            rows_html = []
            for index, group in enumerate(groups, start=1):
                rows_html.append(
                    f'''
<article class="matrix-fallback-row">
  <div class="matrix-fallback-row__index">{index:02d}</div>
  <div class="matrix-fallback-row__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
                )
            matrix_html = f'<div class="matrix-fallback" data-matrix="{html.escape(section_key)}">{"".join(rows_html)}</div>'

    return "".join(
        part
        for part in [intro_html, matrix_html, trailing_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def render_callout_section(lines: list[str], label_prefix: str, section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]

    if not groups:
        stack_html = render_empty_state(empty_state)
    else:
        callouts = []
        for index, group in enumerate(groups, start=1):
            callouts.append(
                f'''
<article class="callout callout--warning">
  <div class="callout__label">{html.escape(label_prefix)} {index:02d}</div>
  <div class="callout__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        stack_html = f'<div class="callout-stack" data-callout-stack="{html.escape(section_key)}">{"".join(callouts)}</div>'

    return "".join(
        part
        for part in [stack_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def render_timeline_section(lines: list[str], section_key: str, empty_state: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = [group for group in group_top_level_bullets(main_lines) if not is_none_group(group)]

    if not groups:
        timeline_html = render_empty_state(empty_state)
    else:
        items = []
        for index, group in enumerate(groups, start=1):
            items.append(
                f'''
<article class="timeline-item">
  <div class="timeline-item__marker">{index:02d}</div>
  <div class="timeline-item__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        timeline_html = f'<div class="impact-timeline" data-timeline="{html.escape(section_key)}">{"".join(items)}</div>'

    return "".join(
        part
        for part in [timeline_html, render_extra_subsections(extra_subsections), render_visual_evidence(visual_lines)]
        if part
    )


def parse_traceability(lines: list[str]) -> list[TraceEntry]:
    entries: list[TraceEntry] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue
        claim_match = TRACEABILITY_PATTERN.match(line)
        if not claim_match or index + 2 >= len(lines):
            index += 1
            continue
        source_match = SOURCE_PATTERN.match(lines[index + 1])
        quote_match = QUOTE_PATTERN.match(lines[index + 2])
        if not source_match or not quote_match:
            index += 1
            continue
        entries.append(
            TraceEntry(
                claim_id=claim_match.group(1).strip(),
                claim=claim_match.group(2).strip(),
                source_path=source_match.group(1).strip(),
                heading=source_match.group(2).strip(),
                evidence_quote=quote_match.group(1),
            )
        )
        index += 3
    return entries


def render_traceability(lines: list[str], section_key: str) -> str:
    entries = parse_traceability(lines)
    if not entries:
        return render_empty_state("No traceability claims.")

    parts = []
    for index, entry in enumerate(entries, start=1):
        open_attr = " open" if index == 1 else ""
        parts.append(
            f'''
<details class="traceability-item" data-traceability-item{open_attr}>
  <summary>
    <span class="traceability-item__id">{html.escape(entry.claim_id)}</span>
    <span class="traceability-item__claim">{render_inline(entry.claim)}</span>
  </summary>
  <div class="traceability-item__body">
    <div class="traceability-meta">
      <span class="traceability-meta__label">Source</span>
      <code>{html.escape(entry.source_path)}</code>
      <span class="traceability-meta__sep">::</span>
      <code>{html.escape(entry.heading)}</code>
    </div>
    <blockquote>{html.escape(entry.evidence_quote)}</blockquote>
  </div>
</details>
'''.strip()
        )

    return f'<div class="traceability-list" data-traceability-list="{html.escape(section_key)}">{"".join(parts)}</div>'


def parse_validator_entries(lines: list[str]) -> list[ValidatorEntry]:
    text = "\n".join(lines)
    entries: list[ValidatorEntry] = []
    for label in ("Canonical validator", "Approval-view validator"):
        pattern = re.compile(rf"- {re.escape(label)}:\n  - Command: (.+)\n  - Result: (.+)")
        match = pattern.search(text)
        if match:
            entries.append(ValidatorEntry(label=label, command=match.group(1).strip(), result=match.group(2).strip()))
    return entries


def render_validator_status(lines: list[str], section_key: str) -> str:
    entries = parse_validator_entries(lines)
    cards = []
    for entry in entries:
        tone = "passed" if entry.result == "Passed" else "unknown"
        cards.append(
            f'''
<article class="validator-card validator-card--{tone}" data-validator-card>
  <div class="validator-card__top">
    <div class="validator-card__label">{html.escape(entry.label)}</div>
    <span class="status-pill status-pill--{tone}">{html.escape(entry.result)}</span>
  </div>
  <details class="detail-panel" data-command-details>
    <summary>Validator command</summary>
    <pre class="code-block"><code>{html.escape(entry.command)}</code></pre>
  </details>
</article>
'''.strip()
        )
    return f'<div class="validator-grid" data-validator-grid="{html.escape(section_key)}">{"".join(cards)}</div>'


def render_snapshot_identity(lines: list[str], section_key: str) -> str:
    fields, records = parse_snapshot_fields(lines)
    rows = []
    mono_labels = {"Snapshot SHA-256", "Pack snapshot SHA-256", "Canonical artifact", "Spec-pack root", "Approval view generated_at", "Canonical updated_at"}
    for label, value in fields:
        value_class = "snapshot-grid__value snapshot-grid__value--mono" if label in mono_labels else "snapshot-grid__value"
        rows.append(
            f'''
<div class="snapshot-grid__row">
  <dt>{html.escape(label)}</dt>
  <dd class="{value_class}">{html.escape(value)}</dd>
</div>
'''.strip()
        )
    table_html = ""
    if records:
        table_rows = []
        for record in records:
            table_rows.append(
                f'''
<tr>
  <td><code>{html.escape(record.path)}</code></td>
  <td><code>{html.escape(record.sha256)}</code></td>
  <td><code>{html.escape(record.updated_at)}</code></td>
</tr>
'''.strip()
            )
        table_html = f'''
<details class="detail-panel snapshot-detail" data-snapshot-details>
  <summary>Included snapshots ({len(records)})</summary>
  <div class="table-wrap">
    <table class="snapshot-table" data-snapshot-table>
      <thead>
        <tr>
          <th>Canonical artifact</th>
          <th>SHA-256</th>
          <th>updated_at</th>
        </tr>
      </thead>
      <tbody>
        {"".join(table_rows)}
      </tbody>
    </table>
  </div>
</details>
'''.strip()

    return f'''
<div class="snapshot-panel" data-snapshot-panel="{html.escape(section_key)}">
  <dl class="snapshot-grid">{"".join(rows)}</dl>
  {table_html}
</div>
'''.strip()


def fallback_section_spec(title: str) -> dict[str, object]:
    for review_type in ("artifact", "pack"):
        profile = load_review_profile(review_type)
        mapping = section_spec_by_title(profile, False)
        spec = mapping.get(title)
        if spec is not None:
            return spec
    return {
        "key": slugify(title),
        "title": title,
        "kind": "fragment",
        "label": title,
        "style": "default",
        "tone": "neutral",
        "emphasis": "standard",
        "item_label": "Item",
        "empty_state": "None",
        "why": "",
    }


def profile_section_spec(profile: dict[str, object], revised: bool, title: str) -> dict[str, object]:
    return section_spec_by_title(profile, revised).get(title) or fallback_section_spec(title)


def render_section(section: Section, index: int, profile: dict[str, object], revised: bool) -> str:
    spec = profile_section_spec(profile, revised, section.title)
    title = section.title
    role = str(spec["key"])
    kind = str(spec["kind"])
    style = str(spec.get("style") or "default")
    tone = str(spec.get("tone") or "neutral")
    emphasis = str(spec.get("emphasis") or "standard")
    label = str(spec.get("label") or title)
    item_label = str(spec.get("item_label") or "Item")
    empty_state = str(spec.get("empty_state") or "None")
    why = str(spec.get("why") or "").strip()

    if kind == "change-summary":
        body_html = render_change_summary(section.lines, role)
    elif kind == "summary":
        body_html = render_summary_like(section.lines, role, empty_state, visual_first=False)
    elif kind == "diagram-led-summary":
        body_html = render_summary_like(section.lines, role, empty_state, visual_first=True)
    elif kind == "scope":
        body_html = render_scope(section.lines, role)
    elif kind == "cards":
        body_html = render_cards(section.lines, item_label, role, empty_state, "data-card-grid", role)
    elif kind == "paired-lists":
        body_html = render_paired_lists(section.lines, role, empty_state)
    elif kind == "checklist":
        body_html = render_checklist(section.lines, role, empty_state)
    elif kind == "ledger":
        body_html = render_ledger(section.lines, role, empty_state)
    elif kind == "matrix":
        body_html = render_matrix(section.lines, role, empty_state)
    elif kind == "roster":
        body_html = render_roster(section.lines, role, empty_state)
    elif kind == "callouts":
        body_html = render_callout_section(section.lines, item_label, role, empty_state)
    elif kind == "traceability":
        body_html = render_traceability(section.lines, role)
    elif kind == "validator":
        body_html = render_validator_status(section.lines, role)
    elif kind == "timeline":
        body_html = render_timeline_section(section.lines, role, empty_state)
    elif kind == "snapshot":
        body_html = render_snapshot_identity(section.lines, role)
    else:
        body_html = render_fragment(section.lines, heading_level=5)

    why_html = f'<p class="section-why" data-section-why>{render_inline(why)}</p>' if why else ""
    return f'''
<section class="approval-section approval-section--{role}" id="section-{role}" data-section-role="{role}" data-section-kind="{kind}" data-section-style="{style}" data-section-tone="{tone}" data-section-emphasis="{emphasis}" style="--section-index:{index}">
  <div class="section-top">
    <div class="section-heading">
      <div class="section-kicker">
        <span class="section-number">{index:02d}</span>
        <span>{html.escape(label)}</span>
      </div>
      <h2>{html.escape(title)}</h2>
      {why_html}
    </div>
  </div>
  <div class="section-content">{body_html}</div>
</section>
'''.strip()


def validator_pass_count(lines: list[str]) -> int:
    return len(re.findall(r"^  - Result: Passed$", "\n".join(lines), re.MULTILINE))


def count_visual_evidence_items(sections: Iterable[Section]) -> int:
    count = 0
    for section in sections:
        count += len(re.findall(r"^- Source: ", "\n".join(section.lines), re.MULTILINE))
    return count


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


def snapshot_canonical_sources(metadata: dict[str, object]) -> list[CanonicalSnapshot]:
    snapshots: list[CanonicalSnapshot] = []
    review_type = str(metadata.get("review_type") or "").strip()
    paths: list[str] = []
    if review_type == "Artifact":
        canonical_path = str(metadata.get("canonical_artifact") or "").strip()
        if canonical_path:
            paths.append(canonical_path)
    else:
        for record in metadata.get("included_snapshots", []):
            if isinstance(record, dict) and record.get("path"):
                paths.append(str(record["path"]))

    for raw_path in paths:
        path = Path(raw_path).resolve()
        if not path.is_file():
            continue
        snapshots.append(CanonicalSnapshot(path=str(path), text=read_text(path)))
    return snapshots


def glance_metric_value(
    card: dict[str, object],
    section_map: dict[str, list[str]],
    sections: list[Section],
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
        return count_meaningful_groups(section_map.get(section_title, []))
    if metric == "traceability_claims":
        traceability_lines = section_map.get(section_title, []) if section_title else []
        if not traceability_lines:
            for section in sections:
                if fallback_section_spec(section.title)["kind"] == "traceability":
                    traceability_lines = section.lines
                    break
        return len(parse_traceability(traceability_lines))
    if metric == "validator_checks":
        validator_lines = section_map.get(section_title, []) if section_title else []
        if not validator_lines:
            for section in sections:
                if fallback_section_spec(section.title)["kind"] == "validator":
                    validator_lines = section.lines
                    break
        return validator_pass_count(validator_lines)
    if metric == "visuals":
        return count_visual_evidence_items(sections)
    return 0


def derive_glance_cards(profile: dict[str, object], revised: bool, sections: list[Section], metadata: dict[str, object]) -> list[dict[str, str]]:
    section_map = {section.title: section.lines for section in sections}
    canonical_snapshots = snapshot_canonical_sources(metadata)
    cards: list[dict[str, str]] = []
    for raw_card in glance_cards_for_mode(profile, revised):
        card = dict(raw_card)
        cards.append(
            {
                "label": str(card.get("label") or "Review"),
                "value": str(glance_metric_value(card, section_map, sections, canonical_snapshots)),
                "hint": str(card.get("hint") or ""),
                "tone": str(card.get("tone") or "info"),
                "source": str(card.get("source") or "approval"),
            }
        )
    return cards


def render_glance_cards(cards: list[dict[str, str]]) -> str:
    rendered = []
    for card in cards:
        rendered.append(
            f'''
<article class="glance-card glance-card--{html.escape(card["tone"])}" data-glance-card data-glance-source="{html.escape(card.get("source", "approval"))}">
  <div class="glance-card__label">{html.escape(card["label"])}</div>
  <div class="glance-card__value">{html.escape(card["value"])}</div>
  <p>{html.escape(card["hint"])}</p>
</article>
'''.strip()
        )
    return "".join(rendered)


def render_toc(sections: list[Section], profile: dict[str, object], revised: bool) -> str:
    links = []
    for index, section in enumerate(sections, start=1):
        spec = profile_section_spec(profile, revised, section.title)
        section_id = f"section-{spec['key']}"
        links.append(
            f'<a href="#{section_id}" data-toc-link><span class="toc-index">{index:02d}</span><span>{html.escape(section.title)}</span></a>'
        )
    return "".join(links)


def build_metadata(
    markdown_text: str,
    sections: list[Section],
    profile: dict[str, object],
    revised: bool,
    snapshot_metadata: dict[str, object],
) -> dict[str, object]:
    metadata = dict(snapshot_metadata)
    metadata["profile_id"] = profile.get("profile_id")
    metadata["profile_source"] = profile.get("source")

    derived_sections = []
    for section in sections:
        spec = profile_section_spec(profile, revised, section.title)
        derived_sections.append(
            {
                "id": f"section-{spec['key']}",
                "key": spec["key"],
                "title": section.title,
                "kind": spec["kind"],
                "tone": spec.get("tone"),
                "emphasis": spec.get("emphasis"),
            }
        )

    glance = derive_glance_cards(profile, revised, sections, snapshot_metadata)
    metadata["derived"] = {
        "sections": derived_sections,
        "glance": {card["label"]: card["value"] for card in glance},
        "has_mermaid": bool(MERMAID_FENCE_PATTERN.search(markdown_text)),
        "has_toc": len(sections) >= 4,
    }
    return metadata


def main() -> int:
    if len(sys.argv) != 3:
        usage()
        return 1

    source_path = Path(sys.argv[1]).resolve()
    output_path = Path(sys.argv[2]).resolve()
    shell_path = Path(__file__).resolve().parent.parent / "assets" / "approval-view-shell.html"

    if not source_path.is_file():
        print(f"Approval Markdown not found: {source_path}", file=sys.stderr)
        return 1
    if not shell_path.is_file():
        print(f"HTML shell template not found: {shell_path}", file=sys.stderr)
        return 1

    markdown_text = read_text(source_path)
    shell_text = read_text(shell_path)
    markdown_body = first_h1_removed(markdown_text)
    sections = parse_sections(markdown_body)
    snapshot_metadata = extract_snapshot_metadata(sections)
    profile, revised, _ = resolve_review_profile(snapshot_metadata)
    metadata = build_metadata(markdown_body, sections, profile, revised, snapshot_metadata)
    title = approval_view_title(markdown_text, metadata)
    subtitle = approval_view_subtitle(profile)
    view_label = str(profile.get("display_name") or "Approval View")
    toc_html = render_toc(sections, profile, revised)
    glance_html = render_glance_cards(derive_glance_cards(profile, revised, sections, snapshot_metadata))
    body_html = "\n".join(render_section(section, index, profile, revised) for index, section in enumerate(sections, start=1))

    html_text = (
        shell_text.replace("{{TITLE}}", html.escape(title))
        .replace("{{VIEW_LABEL}}", html.escape(view_label))
        .replace("{{SUBTITLE}}", html.escape(subtitle))
        .replace("{{TOC}}", toc_html)
        .replace("{{GLANCE}}", glance_html)
        .replace("{{METADATA_JSON}}", html.escape(json.dumps(metadata, indent=2, sort_keys=True)))
        .replace("{{BODY}}", body_html)
    )

    write_text(output_path, html_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
