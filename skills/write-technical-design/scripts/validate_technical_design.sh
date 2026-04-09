#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: validate_technical_design.sh <technical-design-file>" >&2
  exit 1
fi

FILE="$1"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROVENANCE_SCRIPT="$SCRIPT_DIR/../../document-traceability/scripts/validate_frontmatter_provenance.sh"

if [[ ! -f "$FILE" ]]; then
  echo "Technical design file not found: $FILE" >&2
  exit 1
fi

bash "$PROVENANCE_SCRIPT" technical-design "$FILE"

required_sections=(
  "## Architecture Summary"
  "## System Context"
  "## Components and Responsibilities"
  "## Data Model and Data Flow"
  "## Interfaces and Contracts"
  "## Integration Points"
  "## Failure and Recovery Strategy"
  "## Security, Reliability, and Performance"
  "## Implementation Strategy"
  "## Testing Strategy"
  "## Risks and Tradeoffs"
  "## Further Notes"
)

prev_line=0
for section in "${required_sections[@]}"; do
  line="$(grep -nF "$section" "$FILE" | head -n1 | cut -d: -f1 || true)"
  if [[ -z "$line" ]]; then
    echo "Missing required section: $section" >&2
    exit 1
  fi
  if (( line <= prev_line )); then
    echo "Section out of order: $section" >&2
    exit 1
  fi
  prev_line=$line
done

component_count="$({
  awk '
    /^## Components and Responsibilities$/ { in_components = 1; next }
    in_components && /^## / { exit }
    in_components && /^### / && $0 != "### Behavior State Diagram" { count++ }
    END { print count + 0 }
  ' "$FILE"
} || true)"
if (( component_count < 1 )); then
  echo "Missing at least one named component subsection under Components and Responsibilities" >&2
  exit 1
fi

non_mermaid_code_block_count="$({
  awk '
    !in_block && /^```/ {
      in_block = 1
      lang = substr($0, 4)
      if (lang != "mermaid") {
        count++
      }
      next
    }
    in_block && /^```$/ {
      in_block = 0
      next
    }
  END { print count + 0 }
  ' "$FILE"
} || true)"
if (( non_mermaid_code_block_count < 1 )); then
  echo "Technical design must include at least one short non-Mermaid fenced code block" >&2
  exit 1
fi

if ! awk '
  function fail(msg, line) {
    printf("%s at line %d\n", msg, line) > "/dev/stderr"
    exit 1
  }
  /^## Components and Responsibilities$/ { in_components = 1; next }
  in_components && /^## / {
    if (expecting_definition) {
      fail("Component subsection must include a one-sentence definition before bullets", heading_line)
    }
    exit 0
  }
  in_components && /^### Behavior State Diagram$/ {
    expecting_definition = 0
    next
  }
  in_components && /^### / {
    if (expecting_definition) {
      fail("Component subsection must include a one-sentence definition before bullets", heading_line)
    }
    expecting_definition = 1
    heading_line = NR
    next
  }
  expecting_definition {
    if ($0 ~ /^[[:space:]]*$/) {
      next
    }
    if ($0 ~ /^[[:space:]]*-/ || $0 ~ /^```/) {
      fail("Component subsection must start with a one-sentence definition paragraph before bullets or code blocks", heading_line)
    }
    expecting_definition = 0
    next
  }
  END {
    if (expecting_definition) {
      fail("Component subsection must include a one-sentence definition before bullets", heading_line)
    }
  }
' "$FILE"; then
  exit 1
fi

traceability_pattern='US1\.[0-9]+|FR1\.[0-9]+|NFR2\.[0-9]+|TC3\.[0-9]+|DR4\.[0-9]+|IR5\.[0-9]+|DEP6\.[0-9]+'

extract_heading_block() {
  local heading="$1"
  awk -v heading="$heading" '
    $0 == heading { in_block = 1; next }
    in_block && ($0 ~ /^## / || $0 ~ /^### /) { exit }
    in_block { print }
  ' "$FILE"
}

extract_section_block() {
  local heading="$1"
  awk -v heading="$heading" '
    $0 == heading { in_block = 1; next }
    in_block && /^## / { exit }
    in_block { print }
  ' "$FILE"
}

heading_line() {
  local heading="$1"
  grep -nFx "$heading" "$FILE" | head -n1 | cut -d: -f1 || true
}

assert_heading_order() {
  local earlier="$1"
  local later="$2"
  local earlier_line
  local later_line

  earlier_line="$(heading_line "$earlier")"
  later_line="$(heading_line "$later")"

  if [[ -z "$earlier_line" || -z "$later_line" ]]; then
    echo "Cannot verify heading order without both headings: $earlier / $later" >&2
    exit 1
  fi

  if (( earlier_line >= later_line )); then
    echo "Heading must appear before later subsection: $earlier -> $later" >&2
    exit 1
  fi
}

validate_diagram_slot() {
  local heading="$1"
  local diagram_type="$2"
  local block

  if ! grep -Fxq "$heading" "$FILE"; then
    echo "Missing required diagram subsection: $heading" >&2
    exit 1
  fi

  block="$(extract_heading_block "$heading")"
  if [[ -z "$block" ]]; then
    echo "Diagram subsection is empty: $heading" >&2
    exit 1
  fi

  if grep -Eq "^[[:space:]]*-[[:space:]]+Not needed: " <<<"$block"; then
    return 0
  fi

  if grep -Eq 'TODO: Confirm' <<<"$block"; then
    return 0
  fi

  if ! grep -Eq '```mermaid' <<<"$block"; then
    echo "Diagram subsection must include a Mermaid block or 'Not needed:' rationale: $heading" >&2
    exit 1
  fi

  if ! grep -Eq "^[[:space:]]*${diagram_type}( |$)" <<<"$block"; then
    echo "Diagram subsection must use Mermaid type '${diagram_type}': $heading" >&2
    exit 1
  fi
}

validate_optional_diagram_slot() {
  local heading="$1"
  local diagram_type="$2"
  local block

  if ! grep -Fxq "$heading" "$FILE"; then
    return 0
  fi

  block="$(extract_heading_block "$heading")"
  if [[ -z "$block" ]]; then
    echo "Diagram subsection is empty: $heading" >&2
    exit 1
  fi

  if grep -Eq "^[[:space:]]*-[[:space:]]+Not needed: " <<<"$block"; then
    return 0
  fi

  if grep -Eq 'TODO: Confirm' <<<"$block"; then
    return 0
  fi

  if ! grep -Eq '```mermaid' <<<"$block"; then
    echo "Optional diagram subsection must include a Mermaid block or 'Not needed:' rationale: $heading" >&2
    exit 1
  fi

  if ! grep -Eq "^[[:space:]]*${diagram_type}( |$)" <<<"$block"; then
    echo "Optional diagram subsection must use Mermaid type '${diagram_type}': $heading" >&2
    exit 1
  fi
}

system_context_block="$(extract_heading_block '## System Context')"
if ! grep -Eq "^[[:space:]]*-[[:space:]]+Story or requirements traceability:[[:space:]]*(TODO: Confirm|.*(${traceability_pattern}).*)$" <<<"$system_context_block"; then
  echo "System Context must include story or requirements traceability with one or more US1.x or requirement IDs, or TODO: Confirm" >&2
  exit 1
fi

components_block="$(extract_section_block '## Components and Responsibilities')"
if ! grep -Eq "^[[:space:]]*-[[:space:]]+Story impact:[[:space:]]*(TODO: Confirm|.*(${traceability_pattern}).*)$" <<<"$components_block"; then
  echo "Components and Responsibilities must include at least one Story impact line with one or more US1.x or requirement IDs, or TODO: Confirm" >&2
  exit 1
fi

validate_diagram_slot '### Process Flowchart' 'flowchart'
validate_diagram_slot '### Context Flowchart' 'flowchart'
assert_heading_order '### Process Flowchart' '### Context Flowchart'
validate_diagram_slot '### Behavior State Diagram' 'stateDiagram-v2'
validate_diagram_slot '### Entity Relationship Diagram' 'erDiagram'
validate_optional_diagram_slot '### Interaction Diagram' 'sequenceDiagram'

echo "Technical design validation passed: $FILE"
