#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Iterable, Sequence


SUPPORTED_SECTION_KINDS = {
    "change-summary",
    "summary",
    "scope",
    "cards",
    "callouts",
    "traceability",
    "validator",
    "timeline",
    "snapshot",
    "fragment",
    "paired-lists",
    "checklist",
    "ledger",
    "matrix",
    "roster",
    "diagram-led-summary",
}

STYLE_BY_KIND = {
    "change-summary": "hero",
    "summary": "hero",
    "scope": "elevated",
    "cards": "default",
    "callouts": "elevated",
    "traceability": "default",
    "validator": "elevated",
    "timeline": "default",
    "snapshot": "recessed",
    "fragment": "default",
    "paired-lists": "elevated",
    "checklist": "elevated",
    "ledger": "default",
    "matrix": "elevated",
    "roster": "default",
    "diagram-led-summary": "hero",
}

TONE_BY_KIND = {
    "change-summary": "accent",
    "summary": "accent",
    "scope": "info",
    "cards": "neutral",
    "callouts": "warning",
    "traceability": "info",
    "validator": "success",
    "timeline": "info",
    "snapshot": "neutral",
    "fragment": "neutral",
    "paired-lists": "accent",
    "checklist": "success",
    "ledger": "neutral",
    "matrix": "info",
    "roster": "accent",
    "diagram-led-summary": "accent",
}

EMPHASIS_BY_STYLE = {
    "hero": "dominant",
    "elevated": "standard",
    "default": "standard",
    "recessed": "recessed",
}

VALID_STYLES = {"hero", "elevated", "default", "recessed"}
VALID_TONES = {"accent", "info", "success", "warning", "neutral"}
VALID_EMPHASIS = {"dominant", "standard", "recessed"}
VALID_REVIEW_TYPES = {"artifact", "pack"}
VALID_GLANCE_SOURCES = {"approval", "canonical"}
VALID_GLANCE_METRICS = {
    "groups",
    "traceability_claims",
    "validator_checks",
    "visuals",
    "count-heading-prefix",
}

LEGACY_TONE_MAP = {
    "muted": "neutral",
}

GENERIC_ARTIFACT_PROFILE: dict[str, Any] = {
    "profile_id": "artifact-generic-approval-v2",
    "display_name": "Artifact Approval",
    "subtitle": "Glance-first artifact review with traceable evidence and final snapshot metadata.",
    "review_type": "artifact",
    "sections": [
        {
            "key": "executive-summary",
            "title": "Executive Summary",
            "kind": "summary",
            "label": "Approval Brief",
            "style": "hero",
            "tone": "accent",
            "emphasis": "dominant",
            "why": "Lead with the shortest possible approval read before deeper review.",
        },
        {
            "key": "scope",
            "title": "Scope",
            "kind": "scope",
            "label": "Boundary",
            "style": "elevated",
            "tone": "info",
            "why": "Separate settled scope from excluded scope before approval decisions.",
        },
        {
            "key": "decisions-required-for-approval",
            "title": "Decisions Required for Approval",
            "kind": "cards",
            "label": "Decision Gate",
            "style": "default",
            "item_label": "Decision",
            "tone": "neutral",
            "why": "Make explicit approval calls scannable.",
        },
        {
            "key": "risks-and-tradeoffs",
            "title": "Risks and Tradeoffs",
            "kind": "callouts",
            "label": "Risk Review",
            "style": "elevated",
            "item_label": "Risk",
            "tone": "warning",
            "why": "Surface tradeoffs before approval locks in direction.",
        },
        {
            "key": "blockers-and-unresolved-items",
            "title": "Blockers and Unresolved Items",
            "kind": "callouts",
            "label": "Open Issues",
            "style": "elevated",
            "item_label": "Blocker",
            "tone": "warning",
            "why": "Keep unresolved items visible so approval is not mistaken for completeness.",
        },
        {
            "key": "traceability-map",
            "title": "Traceability Map",
            "kind": "traceability",
            "label": "Evidence",
            "style": "default",
            "tone": "info",
            "why": "Tie substantive approval claims to exact canonical evidence.",
        },
        {
            "key": "validator-status",
            "title": "Validator Status",
            "kind": "validator",
            "label": "Validation",
            "style": "elevated",
            "tone": "success",
            "why": "Show both canonical and approval-view validation status.",
        },
        {
            "key": "downstream-impact-if-approved",
            "title": "Downstream Impact if Approved",
            "kind": "timeline",
            "label": "Impact",
            "style": "default",
            "item_label": "Impact",
            "tone": "info",
            "why": "Clarify what approval enables next.",
        },
        {
            "key": "snapshot-identity",
            "title": "Snapshot Identity",
            "kind": "snapshot",
            "label": "Snapshot",
            "style": "recessed",
            "tone": "neutral",
            "emphasis": "recessed",
            "why": "End with exact snapshot identity and provenance fields.",
        },
    ],
    "glance_cards": [
        {
            "label": "Decisions",
            "section_title": "Decisions Required for Approval",
            "metric": "groups",
            "hint": "Approval calls requiring an explicit yes or no.",
            "tone": "accent",
            "source": "approval",
        },
        {
            "label": "Open issues",
            "section_title": "Blockers and Unresolved Items",
            "metric": "groups",
            "hint": "Open items that can stall or limit approval.",
            "tone": "warning",
            "source": "approval",
        },
        {
            "label": "Evidence claims",
            "metric": "traceability_claims",
            "hint": "Trace-linked claims backed by verbatim source quotes.",
            "tone": "info",
            "source": "approval",
        },
        {
            "label": "Validator checks",
            "metric": "validator_checks",
            "hint": "Recorded validator passes carried from the review inputs.",
            "tone": "success",
            "source": "approval",
        },
        {
            "label": "Visuals",
            "metric": "visuals",
            "hint": "Carried-forward visual evidence sections in this review.",
            "tone": "info",
            "source": "approval",
        },
    ],
}

PACK_PROFILE: dict[str, Any] = {
    "profile_id": "pack-generic-approval-v2",
    "display_name": "Pack Approval",
    "subtitle": "Glance-first pack review with cross-artifact evidence, decision gates, and final snapshot metadata.",
    "review_type": "pack",
    "sections": [
        {
            "key": "executive-summary",
            "title": "Executive Summary",
            "kind": "summary",
            "label": "Approval Brief",
            "style": "hero",
            "tone": "accent",
            "emphasis": "dominant",
            "why": "Lead with the pack-level approval read before detailed review.",
        },
        {
            "key": "scope",
            "title": "Scope",
            "kind": "scope",
            "label": "Boundary",
            "style": "elevated",
            "tone": "info",
            "why": "Show what this pack review covers and excludes.",
        },
        {
            "key": "decisions-required-for-approval",
            "title": "Decisions Required for Approval",
            "kind": "cards",
            "label": "Decision Gate",
            "style": "default",
            "item_label": "Decision",
            "tone": "neutral",
            "why": "Keep cross-artifact approval calls explicit.",
        },
        {
            "key": "risks-and-tradeoffs",
            "title": "Risks and Tradeoffs",
            "kind": "callouts",
            "label": "Risk Review",
            "style": "elevated",
            "item_label": "Risk",
            "tone": "warning",
            "why": "Surface pack-level risks and tradeoffs.",
        },
        {
            "key": "traceability-map",
            "title": "Traceability Map",
            "kind": "traceability",
            "label": "Evidence",
            "style": "default",
            "tone": "info",
            "why": "Tie pack claims to exact artifact evidence.",
        },
        {
            "key": "validator-status",
            "title": "Validator Status",
            "kind": "validator",
            "label": "Validation",
            "style": "elevated",
            "tone": "success",
            "why": "Show pack validator results clearly.",
        },
        {
            "key": "downstream-impact-if-approved",
            "title": "Downstream Impact if Approved",
            "kind": "timeline",
            "label": "Impact",
            "style": "default",
            "item_label": "Impact",
            "tone": "info",
            "why": "Clarify what pack approval enables next.",
        },
        {
            "key": "snapshot-identity",
            "title": "Snapshot Identity",
            "kind": "snapshot",
            "label": "Snapshot",
            "style": "recessed",
            "tone": "neutral",
            "emphasis": "recessed",
            "why": "End with exact pack snapshot identity.",
        },
    ],
    "glance_cards": [
        {
            "label": "Decisions",
            "section_title": "Decisions Required for Approval",
            "metric": "groups",
            "hint": "Pack-level approval calls.",
            "tone": "accent",
            "source": "approval",
        },
        {
            "label": "Risks",
            "section_title": "Risks and Tradeoffs",
            "metric": "groups",
            "hint": "Cross-artifact tradeoffs or concerns.",
            "tone": "warning",
            "source": "approval",
        },
        {
            "label": "Evidence claims",
            "metric": "traceability_claims",
            "hint": "Pack claims backed by verbatim artifact quotes.",
            "tone": "info",
            "source": "approval",
        },
        {
            "label": "Validator checks",
            "metric": "validator_checks",
            "hint": "Validator passes recorded for this review.",
            "tone": "success",
            "source": "approval",
        },
        {
            "label": "Visuals",
            "metric": "visuals",
            "hint": "Visual evidence carried into the pack review.",
            "tone": "info",
            "source": "approval",
        },
    ],
}

CHANGE_SUMMARY_SECTION: dict[str, Any] = {
    "key": "change-summary",
    "title": "Change Summary",
    "kind": "change-summary",
    "label": "Revision Delta",
    "style": "hero",
    "tone": "accent",
    "emphasis": "dominant",
    "item_label": "Delta",
    "empty_state": "None",
    "why": "Lead revised approvals with exact deltas from the last approved snapshot.",
}

FALLBACK_SKILL_BY_BASENAME = {
    "charter.md": "charter",
    "user-stories.md": "user-story-authoring",
    "requirements.md": "requirements",
    "technical-design.md": "technical-design",
    "execution-plan.md": "execution-planning",
    "execution-tasks.md": "task-generation",
}


def _search_repo_root(start: Path) -> Path | None:
    start = start.resolve()
    anchor = start if start.is_dir() else start.parent
    for candidate in [anchor, *anchor.parents]:
        if (candidate / "skills").is_dir():
            return candidate
    return None


def repo_root(hint: Path | None = None) -> Path:
    candidates: list[Path] = []
    if hint is not None:
        candidates.append(hint)
    candidates.append(Path.cwd())
    candidates.append(Path(__file__).resolve())

    for candidate in candidates:
        resolved = _search_repo_root(candidate)
        if resolved is not None:
            return resolved

    return Path.cwd().resolve()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def _normalize_tone(value: Any, fallback: str) -> str:
    if value is None or str(value).strip() == "":
        candidate = fallback
    else:
        candidate = LEGACY_TONE_MAP.get(str(value).strip(), str(value).strip())
    if candidate not in VALID_TONES:
        raise ValueError(f"Unsupported approval profile tone '{candidate}'")
    return candidate


def _normalize_style(value: Any, kind: str) -> str:
    candidate = str(value).strip() if value is not None and str(value).strip() else STYLE_BY_KIND[kind]
    if candidate not in VALID_STYLES:
        raise ValueError(f"Unsupported approval profile style '{candidate}'")
    return candidate


def _normalize_emphasis(value: Any, style: str) -> str:
    candidate = str(value).strip() if value is not None and str(value).strip() else EMPHASIS_BY_STYLE.get(style, "standard")
    if candidate not in VALID_EMPHASIS:
        raise ValueError(f"Unsupported approval profile emphasis '{candidate}'")
    return candidate


def _normalize_section(section: dict[str, Any], source: str) -> dict[str, Any]:
    title = str(section.get("title") or "").strip()
    if not title:
        raise ValueError(f"Approval profile section missing title: {source}")

    kind = str(section.get("kind") or "fragment").strip()
    if kind not in SUPPORTED_SECTION_KINDS:
        raise ValueError(f"Unsupported approval profile section kind '{kind}' in {source}")

    key = str(section.get("key") or slugify(title)).strip()
    if not key:
        raise ValueError(f"Approval profile section missing key: {source}")

    style = _normalize_style(section.get("style"), kind)
    tone = _normalize_tone(section.get("tone"), TONE_BY_KIND[kind])
    emphasis = _normalize_emphasis(section.get("emphasis"), style)

    normalized = {
        "key": key,
        "title": title,
        "kind": kind,
        "label": str(section.get("label") or title).strip(),
        "style": style,
        "tone": tone,
        "emphasis": emphasis,
        "item_label": str(section.get("item_label") or "Item").strip(),
        "empty_state": str(section.get("empty_state") or "None").strip(),
        "why": str(section.get("why") or "").strip(),
    }
    if "glance" in section:
        normalized["glance"] = section["glance"]
    return normalized


def _normalize_glance_card(card: dict[str, Any], source: str) -> dict[str, Any]:
    metric = str(card.get("metric") or "groups").strip()
    if metric not in VALID_GLANCE_METRICS:
        raise ValueError(f"Unsupported glance metric '{metric}' in {source}")

    tone = _normalize_tone(card.get("tone"), "info")
    glance_source = str(card.get("source") or "approval").strip()
    if glance_source not in VALID_GLANCE_SOURCES:
        raise ValueError(f"Unsupported glance-card source '{glance_source}' in {source}")

    extractor = card.get("extractor")
    if extractor is not None and not isinstance(extractor, dict):
        raise ValueError(f"Glance-card extractor must be an object in {source}")

    normalized = {
        "label": str(card.get("label") or "Review").strip(),
        "metric": metric,
        "section_title": str(card.get("section_title") or "").strip(),
        "hint": str(card.get("hint") or "").strip(),
        "tone": tone,
        "source": glance_source,
        "extractor": dict(extractor or {}),
    }
    return normalized


def _normalize_revised_config(raw_revised: Any, source: str) -> dict[str, Any]:
    if raw_revised is None:
        return {"section_overrides": {}, "glance_cards": []}
    if not isinstance(raw_revised, dict):
        raise ValueError(f"Approval profile revised config must be an object: {source}")

    section_overrides: dict[str, dict[str, Any]] = {}
    for key, value in dict(raw_revised.get("section_overrides") or {}).items():
        if not isinstance(value, dict):
            raise ValueError(f"Approval profile revised.section_overrides['{key}'] must be an object in {source}")
        normalized_override: dict[str, Any] = {}
        if "style" in value:
            normalized_override["style"] = _normalize_style(value.get("style"), "fragment")
        if "tone" in value:
            normalized_override["tone"] = _normalize_tone(value.get("tone"), "neutral")
        if "emphasis" in value:
            normalized_override["emphasis"] = _normalize_emphasis(value.get("emphasis"), normalized_override.get("style", "default"))
        for field in ("label", "item_label", "empty_state", "why"):
            if field in value:
                normalized_override[field] = str(value.get(field) or "").strip()
        section_overrides[str(key).strip()] = normalized_override

    glance_cards = [
        _normalize_glance_card(card, f"{source} :: revised.glance_cards[{index}]")
        for index, card in enumerate(list(raw_revised.get("glance_cards") or []), start=1)
    ]
    return {"section_overrides": section_overrides, "glance_cards": glance_cards}


def normalize_profile(raw_profile: dict[str, Any], source: str) -> dict[str, Any]:
    sections = [_normalize_section(section, source) for section in raw_profile.get("sections", [])]
    if not sections:
        raise ValueError(f"Approval profile has no sections: {source}")

    seen_titles: set[str] = set()
    seen_keys: set[str] = set()
    kinds = [section["kind"] for section in sections]
    for section in sections:
        if section["title"] in seen_titles:
            raise ValueError(f"Duplicate approval profile section title '{section['title']}' in {source}")
        if section["key"] in seen_keys:
            raise ValueError(f"Duplicate approval profile section key '{section['key']}' in {source}")
        seen_titles.add(section["title"])
        seen_keys.add(section["key"])

    if kinds.count("traceability") != 1:
        raise ValueError(f"Approval profile must define exactly one traceability section: {source}")
    if kinds.count("validator") != 1:
        raise ValueError(f"Approval profile must define exactly one validator section: {source}")
    if kinds.count("snapshot") != 1:
        raise ValueError(f"Approval profile must define exactly one snapshot section: {source}")
    if sections[-1]["kind"] != "snapshot":
        raise ValueError(f"Approval profile snapshot section must be final: {source}")

    review_type = str(raw_profile.get("review_type") or "artifact").strip()
    if review_type not in VALID_REVIEW_TYPES:
        raise ValueError(f"Unsupported approval profile review_type '{review_type}' in {source}")

    default_visual_section = raw_profile.get("default_visual_section")
    if default_visual_section is not None:
        default_visual_section = str(default_visual_section).strip()
        if default_visual_section not in {section["key"] for section in sections}:
            raise ValueError(f"default_visual_section '{default_visual_section}' not found in {source}")

    glance_cards = [
        _normalize_glance_card(card, f"{source} :: glance_cards[{index}]")
        for index, card in enumerate(list(raw_profile.get("glance_cards") or []), start=1)
    ]
    revised = _normalize_revised_config(raw_profile.get("revised"), source)

    return {
        "profile_id": str(raw_profile.get("profile_id") or slugify(str(source))).strip(),
        "display_name": str(raw_profile.get("display_name") or "Approval View").strip(),
        "subtitle": str(raw_profile.get("subtitle") or GENERIC_ARTIFACT_PROFILE["subtitle"]).strip(),
        "review_type": review_type,
        "sections": sections,
        "glance_cards": glance_cards,
        "revised": revised,
        "source": source,
        "default_visual_section": default_visual_section,
    }


def frontmatter_lines(markdown_text: str) -> list[str]:
    lines = markdown_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return []
    collected: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            return collected
        collected.append(line)
    return []


def _parse_generated_by_field(markdown_text: str, field_name: str) -> str | None:
    lines = frontmatter_lines(markdown_text)
    if not lines:
        return None

    in_generated_by = False
    for line in lines:
        if line.strip() == "generated_by:":
            in_generated_by = True
            continue
        if in_generated_by:
            if re.match(r"^[^\s#-]", line):
                break
            match = re.match(rf"^\s{{2}}{re.escape(field_name)}:\s*(.+)$", line)
            if match:
                return match.group(1).strip()
    return None


def parse_producing_skill(markdown_text: str) -> str | None:
    return _parse_generated_by_field(markdown_text, "producing_skill")


def parse_root_skill(markdown_text: str) -> str | None:
    return _parse_generated_by_field(markdown_text, "root_skill")


def profile_path_for_skill(skill_name: str, root: Path | None = None) -> Path:
    return repo_root(root) / "skills" / skill_name / "assets" / "approval-view-profile.json"


def pack_profile_path_for_skill(skill_name: str, root: Path | None = None) -> Path:
    return repo_root(root) / "skills" / skill_name / "assets" / "pack-approval-view-profile.json"


def load_profile_file(path: Path) -> dict[str, Any]:
    data = json.loads(read_text(path))
    return normalize_profile(data, str(path.resolve()))


def _artifact_profile_candidates(canonical_path: Path, canonical_text: str | None) -> list[Path]:
    candidates: list[Path] = []
    root = repo_root(canonical_path)
    producing_skill = parse_producing_skill(canonical_text or "") if canonical_text is not None else None
    if producing_skill:
        candidates.append(profile_path_for_skill(producing_skill, root))

    fallback_skill = FALLBACK_SKILL_BY_BASENAME.get(canonical_path.name)
    if fallback_skill:
        fallback_path = profile_path_for_skill(fallback_skill, root)
        if fallback_path not in candidates:
            candidates.append(fallback_path)
    return candidates


def _validated_profile(path: Path, expected_review_type: str) -> dict[str, Any]:
    profile = load_profile_file(path)
    if profile["review_type"] != expected_review_type:
        raise ValueError(
            f"Approval profile at {path.resolve()} has review_type '{profile['review_type']}', expected '{expected_review_type}'"
        )
    return profile


def load_artifact_profile(canonical_path: Path) -> dict[str, Any]:
    canonical_path = canonical_path.resolve()
    canonical_text = read_text(canonical_path) if canonical_path.is_file() else None
    for candidate in _artifact_profile_candidates(canonical_path, canonical_text):
        if candidate.is_file():
            return _validated_profile(candidate, "artifact")
    return normalize_profile(GENERIC_ARTIFACT_PROFILE, "built-in artifact fallback")


def _resolved_root_skills(canonical_paths: Sequence[Path]) -> set[str]:
    skills: set[str] = set()
    for canonical_path in canonical_paths:
        if not canonical_path.is_file():
            return set()
        root_skill = parse_root_skill(read_text(canonical_path))
        if not root_skill:
            return set()
        skills.add(root_skill)
    return skills


def load_pack_profile(canonical_paths: Sequence[Path] | None = None) -> dict[str, Any]:
    normalized_paths = [Path(path).resolve() for path in list(canonical_paths or [])]
    if normalized_paths:
        root_skills = _resolved_root_skills(normalized_paths)
        if len(root_skills) == 1:
            root_skill = next(iter(root_skills))
            candidate = pack_profile_path_for_skill(root_skill, normalized_paths[0])
            if candidate.is_file():
                return _validated_profile(candidate, "pack")
    return normalize_profile(PACK_PROFILE, "built-in pack fallback")


def load_review_profile(
    review_type: str,
    canonical_path: Path | None = None,
    canonical_paths: Sequence[Path] | None = None,
) -> dict[str, Any]:
    if review_type == "artifact":
        if canonical_path is None:
            return normalize_profile(GENERIC_ARTIFACT_PROFILE, "built-in artifact fallback")
        return load_artifact_profile(canonical_path)
    if review_type == "pack":
        return load_pack_profile(canonical_paths)
    raise ValueError(f"Unsupported review type: {review_type}")


def _apply_section_override(section: dict[str, Any], override: dict[str, Any] | None) -> dict[str, Any]:
    merged = dict(section)
    if not override:
        return merged

    if "style" in override:
        merged["style"] = _normalize_style(override["style"], str(merged["kind"]))
    if "tone" in override:
        merged["tone"] = _normalize_tone(override["tone"], str(merged["tone"]))
    else:
        merged["tone"] = _normalize_tone(merged.get("tone"), TONE_BY_KIND[str(merged["kind"])])
    if "emphasis" in override:
        merged["emphasis"] = _normalize_emphasis(override["emphasis"], str(merged["style"]))
    else:
        merged["emphasis"] = _normalize_emphasis(merged.get("emphasis"), str(merged["style"]))
    for field in ("label", "item_label", "empty_state", "why"):
        if field in override:
            merged[field] = override[field]
    return merged


def section_specs(profile: dict[str, Any], revised: bool) -> list[dict[str, Any]]:
    overrides = dict(profile.get("revised", {}).get("section_overrides", {})) if revised else {}
    specs = [
        _apply_section_override(
            dict(spec),
            overrides.get(str(spec["key"])) or overrides.get(str(spec["title"])),
        )
        for spec in profile["sections"]
    ]
    if not revised:
        return specs
    change_summary = _apply_section_override(
        dict(CHANGE_SUMMARY_SECTION),
        overrides.get("change-summary") or overrides.get("Change Summary"),
    )
    return [change_summary] + specs


def glance_cards_for_mode(profile: dict[str, Any], revised: bool) -> list[dict[str, Any]]:
    if revised:
        revised_cards = list(profile.get("revised", {}).get("glance_cards") or [])
        if revised_cards:
            return [dict(card) for card in revised_cards]
    return [dict(card) for card in profile.get("glance_cards", [])]


def section_spec_by_title(profile: dict[str, Any], revised: bool) -> dict[str, dict[str, Any]]:
    return {spec["title"]: spec for spec in section_specs(profile, revised)}


def section_spec_by_kind(profile: dict[str, Any], revised: bool) -> dict[str, dict[str, Any]]:
    return {spec["kind"]: spec for spec in section_specs(profile, revised)}
