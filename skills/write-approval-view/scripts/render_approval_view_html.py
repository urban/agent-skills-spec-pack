#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path


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


def extract_markdown_title(markdown_text: str) -> str:
    for line in markdown_text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return "Approval View"


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


INLINE_CODE_PATTERN = re.compile(r"`([^`]+)`")
INLINE_STRONG_PATTERN = re.compile(r"\*\*([^*]+)\*\*")
INLINE_LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def render_inline(text: str) -> str:
    escaped = html.escape(text)
    escaped = INLINE_LINK_PATTERN.sub(r'<a href="\2">\1</a>', escaped)
    escaped = INLINE_STRONG_PATTERN.sub(r"<strong>\1</strong>", escaped)
    escaped = INLINE_CODE_PATTERN.sub(r"<code>\1</code>", escaped)
    return escaped


LIST_PATTERN = re.compile(r"^(\s*)-\s+(.*)$")
HEADING_PATTERN = re.compile(r"^(#{2,3})\s+(.+)$")


def markdown_to_html(markdown_text: str) -> str:
    output: list[str] = []
    paragraph_lines: list[str] = []
    list_stack: list[int] = []
    in_code_block = False
    code_lines: list[str] = []
    code_language = ""
    current_section_open = False

    def close_paragraph() -> None:
        nonlocal paragraph_lines
        if paragraph_lines:
            paragraph = " ".join(line.strip() for line in paragraph_lines)
            output.append(f"      <p>{render_inline(paragraph)}</p>")
            paragraph_lines = []

    def close_lists(target_depth: int = 0) -> None:
        nonlocal list_stack
        while len(list_stack) > target_depth:
            output.append("      " + "  " * (len(list_stack) - 1) + "</ul>")
            list_stack.pop()

    def close_section() -> None:
        nonlocal current_section_open
        if current_section_open:
            close_paragraph()
            close_lists(0)
            output.append("    </section>")
            current_section_open = False

    for raw_line in markdown_text.splitlines():
        if raw_line.startswith("```"):
            close_paragraph()
            close_lists(0)
            if not in_code_block:
                in_code_block = True
                code_language = raw_line[3:].strip()
                code_lines = []
            else:
                class_attr = f' class="language-{html.escape(code_language)}"' if code_language else ""
                output.append(
                    "      <pre><code" + class_attr + ">" + html.escape("\n".join(code_lines)) + "</code></pre>"
                )
                in_code_block = False
                code_lines = []
                code_language = ""
            continue

        if in_code_block:
            code_lines.append(raw_line)
            continue

        heading_match = HEADING_PATTERN.match(raw_line)
        if heading_match:
            close_paragraph()
            close_lists(0)
            level = len(heading_match.group(1))
            title = heading_match.group(2).strip()
            if level == 2:
                close_section()
                output.append(f'    <section class="section">')
                output.append(f'      <h2 id="{slugify(title)}">{html.escape(title)}</h2>')
                current_section_open = True
            else:
                output.append(f'      <h3 id="{slugify(title)}">{html.escape(title)}</h3>')
            continue

        list_match = LIST_PATTERN.match(raw_line)
        if list_match:
            close_paragraph()
            indent, item = list_match.groups()
            depth = len(indent) // 2 + 1
            while len(list_stack) < depth:
                output.append("      " + "  " * len(list_stack) + "<ul>")
                list_stack.append(depth)
            close_lists(depth)
            output.append("      " + "  " * depth + f"<li>{render_inline(item.strip())}</li>")
            continue

        if raw_line.strip() == "":
            close_paragraph()
            close_lists(0)
            continue

        paragraph_lines.append(raw_line)

    close_paragraph()
    close_lists(0)
    close_section()

    return "\n".join(output).rstrip() + "\n"


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
    metadata = extract_snapshot_metadata(markdown_text)
    title = approval_view_title(markdown_text, metadata)
    generated_at = str(metadata.get("approval_view_generated_at", "Unknown"))
    body_html = markdown_to_html(first_h1_removed(markdown_text))

    html_text = (
        shell_text.replace("{{TITLE}}", html.escape(title))
        .replace("{{GENERATED_AT}}", html.escape(generated_at))
        .replace("{{METADATA_JSON}}", html.escape(json.dumps(metadata, indent=2, sort_keys=True)))
        .replace("{{BODY}}", body_html.rstrip())
    )

    write_text(output_path, html_text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
