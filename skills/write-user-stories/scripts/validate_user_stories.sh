#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: validate_user_stories.sh <user-stories-file>" >&2
  exit 1
fi

FILE="$1"
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
PROVENANCE_SCRIPT="$SCRIPT_DIR/../../document-traceability/scripts/validate_frontmatter_provenance.sh"

if [[ ! -f "$FILE" ]]; then
  echo "User stories file not found: $FILE" >&2
  exit 1
fi

bash "$PROVENANCE_SCRIPT" user-stories "$FILE"

if grep -Eq '\[TODO:[^]]+\]|<[^>]+>' "$FILE"; then
  echo "User stories artifact contains unresolved placeholder tokens" >&2
  exit 1
fi

if ! grep -Eq '^# User Stories$' "$FILE"; then
  echo "User stories artifact must include '# User Stories'" >&2
  exit 1
fi

capability_count="$(grep -Ec '^## Capability Area: .+' "$FILE" || true)"
if (( capability_count == 0 )); then
  echo "User stories artifact must include at least one capability area" >&2
  exit 1
fi

story_count="$(grep -Ec '^### Story: .+' "$FILE" || true)"
if (( story_count == 0 )); then
  echo "User stories artifact must include at least one story block" >&2
  exit 1
fi

story_id_count="$(grep -Ec '^- Story ID:[[:space:]]*US1\.[0-9]+$' "$FILE" || true)"
if (( story_id_count != story_count )); then
  echo "Every story must include a valid '- Story ID: US1.x' line" >&2
  exit 1
fi

duplicate_story_ids="$(grep -E '^- Story ID:[[:space:]]*US1\.[0-9]+$' "$FILE" | sed -E 's/^- Story ID:[[:space:]]*//' | sort | uniq -d)"
if [[ -n "$duplicate_story_ids" ]]; then
  echo "Duplicate story IDs found:" >&2
  printf '%s\n' "$duplicate_story_ids" >&2
  exit 1
fi

awk '
function fail(msg, line) {
  printf("%s at line %d\n", msg, line) > "/dev/stderr"
  exit 1
}
BEGIN {
  in_story=0
  story_line=0
}
/^### Story: / {
  if (in_story) {
    if (!storyid) fail("Missing - Story ID: in story block", story_line)
    if (!actor) fail("Missing - Actor: in story block", story_line)
    if (!situation) fail("Missing - Situation: in story block", story_line)
    if (!action) fail("Missing - Action: in story block", story_line)
    if (!outcome) fail("Missing - Outcome: in story block", story_line)
    if (!observation) fail("Missing - Observation: in story block", story_line)
  }
  in_story=1
  story_line=NR
  storyid=actor=situation=action=outcome=observation=0
  next
}
/^## Capability Area: / {
  if (in_story) {
    if (!storyid) fail("Missing - Story ID: in story block", story_line)
    if (!actor) fail("Missing - Actor: in story block", story_line)
    if (!situation) fail("Missing - Situation: in story block", story_line)
    if (!action) fail("Missing - Action: in story block", story_line)
    if (!outcome) fail("Missing - Outcome: in story block", story_line)
    if (!observation) fail("Missing - Observation: in story block", story_line)
    in_story=0
  }
  next
}
in_story && /^- Story ID:[[:space:]]*US1\.[0-9]+$/ { storyid=1; next }
in_story && /^- Actor:[[:space:]]*.+/ { actor=1; next }
in_story && /^- Situation:[[:space:]]*.+/ { situation=1; next }
in_story && /^- Action:[[:space:]]*.+/ { action=1; next }
in_story && /^- Outcome:[[:space:]]*.+/ { outcome=1; next }
in_story && /^- Observation:[[:space:]]*.+/ { observation=1; next }
END {
  if (in_story) {
    if (!storyid) fail("Missing - Story ID: in story block", story_line)
    if (!actor) fail("Missing - Actor: in story block", story_line)
    if (!situation) fail("Missing - Situation: in story block", story_line)
    if (!action) fail("Missing - Action: in story block", story_line)
    if (!outcome) fail("Missing - Outcome: in story block", story_line)
    if (!observation) fail("Missing - Observation: in story block", story_line)
  }
}
' "$FILE"

echo "User stories validation passed: $FILE"