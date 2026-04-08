#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: validate_requirements.sh <requirements-file>" >&2
  exit 1
fi

FILE="$1"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROVENANCE_SCRIPT="$SCRIPT_DIR/../../document-traceability/scripts/validate_frontmatter_provenance.sh"

if [[ ! -f "$FILE" ]]; then
  echo "Requirements file not found: $FILE" >&2
  exit 1
fi

bash "$PROVENANCE_SCRIPT" requirements "$FILE"

required_sections=(
  "## Functional Requirements"
  "## Non-Functional Requirements"
  "## Technical Constraints"
  "## Data Requirements"
  "## Integration Requirements"
  "## Dependencies"
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

if ! grep -Eq '^[[:space:]]*-[[:space:]]+FR1\.[0-9]+:' "$FILE"; then
  echo "Missing at least one functional requirement with FR1.x numbering" >&2
  exit 1
fi

awk '
function fail(msg, line) {
  printf("%s at line %d\n", msg, line) > "/dev/stderr"
  exit 1
}
BEGIN {
  in_fr=0
  fr_line=0
  trace=0
}
/^[[:space:]]*-[[:space:]]+FR1\.[0-9]+:/ {
  if (in_fr && !trace) fail("Missing Story traceability for functional requirement", fr_line)
  in_fr=1
  fr_line=NR
  trace=0
  next
}
/^[[:space:]]*-[[:space:]]+(NFR2|TC3|DR4|IR5|DEP6)\.[0-9]+:/ {
  if (in_fr && !trace) fail("Missing Story traceability for functional requirement", fr_line)
  in_fr=0
  next
}
/^## / {
  if (in_fr && !trace) fail("Missing Story traceability for functional requirement", fr_line)
  in_fr=0
  next
}
in_fr && /^[[:space:]]+-[[:space:]]+Story traceability:[[:space:]]*(TODO: Confirm|.*US1\.[0-9]+.*)$/ {
  trace=1
  next
}
END {
  if (in_fr && !trace) fail("Missing Story traceability for functional requirement", fr_line)
}
' "$FILE"

echo "Requirements validation passed: $FILE"
