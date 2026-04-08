#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
report_path="${1:-}"

required_sections=(
  "Executive Summary"
  "Stakeholder-Ready Product Narratives"
  "Capability Map"
  "Coverage Gaps"
  "Additional Notes"
)

if [[ -z "${report_path}" ]]; then
  echo "Usage: scripts/validate_report.sh <report-path>" >&2
  exit 1
fi

if [[ ! -f "${report_path}" ]]; then
  echo "Error: report not found: ${report_path}" >&2
  exit 1
fi

story_validator="${script_dir}/../../write-user-stories/scripts/validate_story.sh"
provenance_validator="${script_dir}/../../document-traceability/scripts/validate_frontmatter_provenance.sh"

if [[ ! -x "${story_validator}" ]]; then
  echo "Error: write-user-stories validator not found or not executable" >&2
  exit 1
fi

if [[ ! -x "${provenance_validator}" ]]; then
  echo "Error: document-traceability validator not found or not executable" >&2
  exit 1
fi

errors=0
declare -A seen_story_ids=()
fail() {
  echo "ERROR: $1" >&2
  errors=$((errors + 1))
}

if ! bash "${provenance_validator}" user-stories "${report_path}" >/dev/null; then
  fail "Canonical provenance validation failed"
fi

if grep -Eq '\[TODO:[^]]+\]|<[^>]+>' "${report_path}"; then
  fail "Report still contains unresolved template placeholders ([TODO: ...] or legacy <...> tokens)"
fi

if ! grep -Eq '^# User Stories$' "${report_path}"; then
  fail "First artifact heading must be '# User Stories'"
fi

prev_line=0
for section in "${required_sections[@]}"; do
  line="$(grep -n -m1 "^## ${section}$" "${report_path}" | cut -d: -f1 || true)"
  if [[ -z "$line" ]]; then
    fail "Missing required section: ## ${section}"
    continue
  fi
  if (( line <= prev_line )); then
    fail "Section out of order: ## ${section}"
  fi
  prev_line="$line"
done

if ! grep -Eq '^## Capability Area: .+' "${report_path}"; then
  fail "Capability Map must include at least one capability area"
fi

story_blocks="$(awk '
/^### Story: / {
  if (block != "") {
    print block
    print "__PI_STORY_BREAK__"
  }
  block = $0 ORS
  next
}
block != "" {
  if ($0 ~ /^## / && $0 !~ /^## Capability Area: /) {
    print block
    print "__PI_STORY_BREAK__"
    block = ""
  } else {
    block = block $0 ORS
  }
}
END {
  if (block != "") print block
}
' "${report_path}")"

story_count=0
current_block=""
while IFS= read -r line || [[ -n "$line" ]]; do
  if [[ "$line" == "__PI_STORY_BREAK__" ]]; then
    if [[ -n "$current_block" ]]; then
      story_count=$((story_count + 1))
      if ! printf '%s\n' "$current_block" | bash "$story_validator" >/dev/null; then
        fail "Invalid canonical story block near story ${story_count}"
      fi
      story_id="$(printf '%s\n' "$current_block" | sed -nE 's/^- Story ID:[[:space:]]*(US1\.[0-9]+)$/\1/p' | head -n 1)"
      if [[ -z "$story_id" ]]; then
        fail "Story ${story_count} must include '- Story ID: US1.x'"
      elif [[ -n "${seen_story_ids[$story_id]:-}" ]]; then
        fail "Duplicate story ID '${story_id}'"
      else
        seen_story_ids[$story_id]=1
      fi
      if ! printf '%s\n' "$current_block" | grep -Eq '^- Confidence: (High|Medium|Low)$'; then
        fail "Story ${story_count} must include '- Confidence: High|Medium|Low'"
      fi
      if ! printf '%s\n' "$current_block" | grep -Eq '^- Rationale: .+'; then
        fail "Story ${story_count} must include '- Rationale:'"
      fi
      if ! printf '%s\n' "$current_block" | grep -Eq '^- Code Evidence:$'; then
        fail "Story ${story_count} must include '- Code Evidence:'"
      fi
      if ! printf '%s\n' "$current_block" | grep -Eq '^  - .+'; then
        fail "Story ${story_count} must include at least one evidence bullet"
      fi
      if ! printf '%s\n' "$current_block" | grep -Eq '^- Test Evidence:$'; then
        fail "Story ${story_count} must include '- Test Evidence:'"
      fi
    fi
    current_block=""
  else
    current_block+="$line"$'\n'
  fi
done <<< "$story_blocks"

if (( story_count == 0 )); then
  fail "Capability Map requires at least one story"
fi

if (( errors > 0 )); then
  echo
  echo "Validation failed with ${errors} error(s)." >&2
  exit 1
fi

echo "Validation passed."