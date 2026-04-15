#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


SECTION_STYLES = {
    "Change Summary": "hero",
    "Executive Summary": "hero",
    "Scope": "elevated",
    "Decisions Required for Approval": "default",
    "Risks and Tradeoffs": "default",
    "Blockers and Unresolved Items": "elevated",
    "Traceability Map": "default",
    "Validator Status": "elevated",
    "Downstream Impact if Approved": "default",
    "Snapshot Identity": "recessed",
}

SECTION_LABELS = {
    "Change Summary": "Revision Delta",
    "Executive Summary": "Approval Brief",
    "Scope": "Boundary",
    "Decisions Required for Approval": "Decision Gate",
    "Risks and Tradeoffs": "Risk Review",
    "Blockers and Unresolved Items": "Open Issues",
    "Traceability Map": "Evidence",
    "Validator Status": "Validation",
    "Downstream Impact if Approved": "Impact",
    "Snapshot Identity": "Snapshot",
}

INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
INLINE_STRONG_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
INLINE_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
BULLET_PATTERN = re.compile(r"^(\s*)-\s+(.*)$")
SUBHEADING_PATTERN = re.compile(r"^(#{3,6})\s+(.+)$")
TRACEABILITY_PATTERN = re.compile(r"^- \[([^\]]+)\] Claim: (.+)$")
SOURCE_PATTERN = re.compile(r"^  - Source: (.+?) :: (.+)$")
QUOTE_PATTERN = re.compile(r'^  - Evidence quote: "(.*)"$')
MERMAID_FENCE_PATTERN = re.compile(r"^```mermaid\s*$", re.IGNORECASE | re.MULTILINE)

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


def extract_snapshot_metadata(markdown_text: str) -> dict[str, object]:
    metadata: dict[str, object] = {}
    lines = markdown_text.splitlines()
    in_snapshot = False
    included_snapshots: list[dict[str, str]] = []

    for line in lines:
        if line == "## Snapshot Identity":
            in_snapshot = True
            continue
        if in_snapshot and line.startswith("## "):
            break
        if not in_snapshot:
            continue

        bullet_match = re.match(r"^- ([^:]+):\s*(.+)$", line)
        if bullet_match:
            label, value = bullet_match.groups()
            metadata[normalize_label(label)] = value.strip()
            continue

        included_match = re.match(
            r"^  - (.+?) \| SHA-256: ([0-9a-f]{64}) \| updated_at: (.+)$",
            line,
        )
        if included_match:
            path_value, sha_value, updated_at = included_match.groups()
            included_snapshots.append(
                {
                    "path": path_value.strip(),
                    "sha256": sha_value.strip(),
                    "updated_at": updated_at.strip(),
                }
            )

    if included_snapshots:
        metadata["included_snapshots"] = included_snapshots

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


def approval_view_subtitle() -> str:
    return "Glance-first approval surface with traceable evidence, structured review gates, and final snapshot metadata."


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

        stripped = line
        required_prefix = " " * (indent + 2)
        if line.startswith(required_prefix):
            stripped = line[indent + 2 :]
        else:
            stripped = line.strip()
        current_item.continuation.append(stripped)
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
            output.append(f"<h{level} class=\"subheading\">{html.escape(heading_match.group(2).strip())}</h{level}>")
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


def render_change_summary(lines: list[str]) -> str:
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
<div class="hero-stack" data-hero-section>
  <div class="hero-note">
    <span class="hero-note__label">Previous snapshot</span>
    <code>{html.escape(previous_hash)}</code>
  </div>
  <div class="delta-grid" data-change-grid>
    {"".join(delta_cards)}
  </div>
</div>
'''.strip()


def render_executive_summary(lines: list[str]) -> str:
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
    text_html = "".join(part for part in [intro_html, summary_points, extra_html] if part)
    if not text_html:
        text_html = render_empty_state("Add 1–3 concise bullets or a short lead paragraph for approvers.")

    visuals_html = render_visual_evidence(visual_lines)
    if visuals_html:
        return f'''
<div class="split-hero">
  <div class="split-hero__main">{text_html}</div>
  <div class="split-hero__visual">{visuals_html}</div>
</div>
'''.strip()

    return f'<div class="hero-stack" data-hero-section>{text_html}</div>'


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


def render_scope(lines: list[str]) -> str:
    in_scope, out_scope = parse_scope(lines)
    return f'''
<div class="scope-grid" data-scope-grid>
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


def render_card_grid_section(lines: list[str], label_prefix: str, grid_class: str) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = group_top_level_bullets(main_lines)
    meaningful_groups = [group for group in groups if not is_none_group(group)]

    if not meaningful_groups:
        cards_html = render_empty_state("None")
    else:
        cards = []
        for index, group in enumerate(meaningful_groups, start=1):
            cards.append(
                f'''
<article class="review-card review-card--{grid_class}">
  <div class="review-card__label">{html.escape(label_prefix)} {index:02d}</div>
  <div class="review-card__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        cards_html = f'<div class="review-card-grid review-card-grid--{grid_class}" data-card-grid="{html.escape(grid_class)}">{"".join(cards)}</div>'

    extras_html = render_extra_subsections(extra_subsections)
    visuals_html = render_visual_evidence(visual_lines)
    return "".join(part for part in [cards_html, extras_html, visuals_html] if part)


def render_blockers(lines: list[str]) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = group_top_level_bullets(main_lines)
    meaningful_groups = [group for group in groups if not is_none_group(group)]

    if not meaningful_groups:
        stack_html = render_empty_state("None")
    else:
        callouts = []
        for index, group in enumerate(meaningful_groups, start=1):
            callouts.append(
                f'''
<article class="callout callout--warning">
  <div class="callout__label">Blocker {index:02d}</div>
  <div class="callout__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        stack_html = f'<div class="callout-stack">{"".join(callouts)}</div>'

    extras_html = render_extra_subsections(extra_subsections)
    visuals_html = render_visual_evidence(visual_lines)
    return "".join(part for part in [stack_html, extras_html, visuals_html] if part)


def render_downstream_impact(lines: list[str]) -> str:
    main_lines, extra_subsections, visual_lines = partition_section_lines(lines)
    groups = group_top_level_bullets(main_lines)
    meaningful_groups = [group for group in groups if not is_none_group(group)]

    if not meaningful_groups:
        timeline_html = render_empty_state("None")
    else:
        items = []
        for index, group in enumerate(meaningful_groups, start=1):
            items.append(
                f'''
<article class="timeline-item">
  <div class="timeline-item__marker">{index:02d}</div>
  <div class="timeline-item__body">{render_fragment(group, heading_level=5)}</div>
</article>
'''.strip()
            )
        timeline_html = f'<div class="impact-timeline" data-impact-timeline>{"".join(items)}</div>'

    extras_html = render_extra_subsections(extra_subsections)
    visuals_html = render_visual_evidence(visual_lines)
    return "".join(part for part in [timeline_html, extras_html, visuals_html] if part)


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


def render_traceability(lines: list[str]) -> str:
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

    return f'<div class="traceability-list" data-traceability-list>{"".join(parts)}</div>'


def parse_validator_entries(lines: list[str]) -> list[ValidatorEntry]:
    text = "\n".join(lines)
    entries: list[ValidatorEntry] = []
    for label in ("Canonical validator", "Approval-view validator"):
        pattern = re.compile(rf"- {re.escape(label)}:\n  - Command: (.+)\n  - Result: (.+)")
        match = pattern.search(text)
        if match:
            entries.append(ValidatorEntry(label=label, command=match.group(1).strip(), result=match.group(2).strip()))
    return entries


def render_validator_status(lines: list[str]) -> str:
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
    return f'<div class="validator-grid" data-validator-grid>{"".join(cards)}</div>'


def parse_snapshot_fields(lines: list[str]) -> tuple[list[tuple[str, str]], list[SnapshotRecord]]:
    fields: list[tuple[str, str]] = []
    records: list[SnapshotRecord] = []
    in_included = False

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
        if not bullet_match:
            continue
        label, value = bullet_match.groups()
        label = label.strip()
        value = value.strip()
        if label == "Included snapshots":
            in_included = True
            continue
        if in_included and label:
            in_included = False
        fields.append((label, value))

    return fields, records


def render_snapshot_identity(lines: list[str]) -> str:
    fields, records = parse_snapshot_fields(lines)
    rows = []
    for label, value in fields:
        value_class = "snapshot-grid__value snapshot-grid__value--mono" if "SHA-256" in label or label.endswith("artifact") or label.endswith("root") or label.endswith("generated_at") or label.endswith("updated_at") else "snapshot-grid__value"
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
<div class="snapshot-panel" data-snapshot-panel>
  <dl class="snapshot-grid">{"".join(rows)}</dl>
  {table_html}
</div>
'''.strip()


def render_section(section: Section, index: int) -> str:
    title = section.title
    role = slugify(title)
    style = SECTION_STYLES.get(title, "default")
    label = SECTION_LABELS.get(title, title)

    if title == "Change Summary":
        body_html = render_change_summary(section.lines)
    elif title == "Executive Summary":
        body_html = render_executive_summary(section.lines)
    elif title == "Scope":
        body_html = render_scope(section.lines)
    elif title == "Decisions Required for Approval":
        body_html = render_card_grid_section(section.lines, "Decision", "decision")
    elif title == "Risks and Tradeoffs":
        body_html = render_card_grid_section(section.lines, "Risk", "risk")
    elif title == "Blockers and Unresolved Items":
        body_html = render_blockers(section.lines)
    elif title == "Traceability Map":
        body_html = render_traceability(section.lines)
    elif title == "Validator Status":
        body_html = render_validator_status(section.lines)
    elif title == "Downstream Impact if Approved":
        body_html = render_downstream_impact(section.lines)
    elif title == "Snapshot Identity":
        body_html = render_snapshot_identity(section.lines)
    else:
        body_html = render_fragment(section.lines, heading_level=5)

    return f'''
<section class="approval-section approval-section--{role}" id="section-{role}" data-section-role="{role}" data-section-style="{style}" style="--section-index:{index}">
  <div class="section-top">
    <div class="section-heading">
      <div class="section-kicker">
        <span class="section-number">{index:02d}</span>
        <span>{html.escape(label)}</span>
      </div>
      <h2>{html.escape(title)}</h2>
    </div>
  </div>
  <div class="section-content">{body_html}</div>
</section>
'''.strip()


def validator_pass_count(lines: list[str]) -> int:
    return len(re.findall(r"^  - Result: Passed$", "\n".join(lines), re.MULTILINE))


def count_visual_evidence_items(sections: list[Section]) -> int:
    count = 0
    for section in sections:
        count += len(re.findall(r"^- Source: ", "\n".join(section.lines), re.MULTILINE))
    return count


def derive_glance_cards(sections: list[Section]) -> list[dict[str, str]]:
    section_map = {section.title: section.lines for section in sections}
    return [
        {
            "label": "Decisions",
            "value": str(count_meaningful_groups(section_map.get("Decisions Required for Approval", []))),
            "hint": "Approval calls requiring an explicit yes/no.",
            "tone": "accent",
        },
        {
            "label": "Risks",
            "value": str(count_meaningful_groups(section_map.get("Risks and Tradeoffs", []))),
            "hint": "Tradeoffs or material concerns to scan fast.",
            "tone": "muted",
        },
        {
            "label": "Blockers",
            "value": str(count_meaningful_groups(section_map.get("Blockers and Unresolved Items", []))),
            "hint": "Open items that can stall or limit approval.",
            "tone": "warning",
        },
        {
            "label": "Evidence claims",
            "value": str(len(parse_traceability(section_map.get("Traceability Map", [])))),
            "hint": "Trace-linked claims backed by verbatim source quotes.",
            "tone": "info",
        },
        {
            "label": "Validator checks",
            "value": str(validator_pass_count(section_map.get("Validator Status", []))),
            "hint": "Recorded validator passes carried from the review inputs.",
            "tone": "success",
        },
        {
            "label": "Visuals",
            "value": str(count_visual_evidence_items(sections)),
            "hint": "Carried-forward visual evidence sections in this review.",
            "tone": "info",
        },
    ]


def render_glance_cards(cards: list[dict[str, str]]) -> str:
    rendered = []
    for card in cards:
        rendered.append(
            f'''
<article class="glance-card glance-card--{html.escape(card["tone"])}" data-glance-card>
  <div class="glance-card__label">{html.escape(card["label"])}</div>
  <div class="glance-card__value">{html.escape(card["value"])}</div>
  <p>{html.escape(card["hint"])}</p>
</article>
'''.strip()
        )
    return "".join(rendered)


def render_toc(sections: list[Section]) -> str:
    links = []
    for index, section in enumerate(sections, start=1):
        section_id = f"section-{slugify(section.title)}"
        links.append(
            f'<a href="#{section_id}" data-toc-link><span class="toc-index">{index:02d}</span><span>{html.escape(section.title)}</span></a>'
        )
    return "".join(links)


def build_metadata(markdown_text: str, sections: list[Section]) -> dict[str, object]:
    metadata = extract_snapshot_metadata(markdown_text)
    section_map = {section.title: section.lines for section in sections}
    metadata["derived"] = {
        "sections": [{"id": f"section-{slugify(section.title)}", "title": section.title} for section in sections],
        "glance": {
            "decisions": count_meaningful_groups(section_map.get("Decisions Required for Approval", [])),
            "risks": count_meaningful_groups(section_map.get("Risks and Tradeoffs", [])),
            "blockers": count_meaningful_groups(section_map.get("Blockers and Unresolved Items", [])),
            "traceability_claims": len(parse_traceability(section_map.get("Traceability Map", []))),
            "validator_checks_passed": validator_pass_count(section_map.get("Validator Status", [])),
            "visual_evidence_items": count_visual_evidence_items(sections),
        },
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
    metadata = build_metadata(markdown_body, sections)
    title = approval_view_title(markdown_text, metadata)
    subtitle = approval_view_subtitle()
    toc_html = render_toc(sections)
    glance_html = render_glance_cards(derive_glance_cards(sections))
    body_html = "\n".join(render_section(section, index) for index, section in enumerate(sections, start=1))

    html_text = (
        shell_text.replace("{{TITLE}}", html.escape(title))
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
