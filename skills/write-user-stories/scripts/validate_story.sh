#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: scripts/validate_story.sh <story-file>" >&2
  echo "   or: cat story.md | scripts/validate_story.sh" >&2
}

story_input=""

if [[ $# -gt 1 ]]; then
  usage
  exit 1
fi

if [[ $# -eq 1 ]]; then
  if [[ ! -f "$1" ]]; then
    echo "Story file not found: $1" >&2
    exit 1
  fi
  story_input="$(cat "$1")"
elif [[ ! -t 0 ]]; then
  story_input="$(cat)"
else
  usage
  exit 1
fi

story_input="$(printf '%s\n' "$story_input" | tr -d '\r')"

if printf '%s\n' "$story_input" | grep -Eq '\[TODO:[^]]+\]|<[^>]+>'; then
  echo "Error: story contains unresolved placeholder tokens" >&2
  exit 1
fi

required_fields=("Story ID" "Actor" "Situation" "Action" "Outcome" "Observation")

if ! printf '%s\n' "$story_input" | grep -Eq '^### Story: .+'; then
  echo "Error: story must begin with '### Story: <short title>'" >&2
  exit 1
fi

for field in "${required_fields[@]}"; do
  line="$(printf '%s\n' "$story_input" | grep -E "^- ${field}:" | head -n 1 || true)"
  if [[ -z "$line" ]]; then
    echo "Error: missing required field '- ${field}:'" >&2
    exit 1
  fi

  value="$(printf '%s\n' "$line" | sed -E "s/^- ${field}:[[:space:]]*//")"
  if [[ -z "$value" ]]; then
    echo "Error: field '${field}' must not be empty" >&2
    exit 1
  fi
done

story_id_value="$(printf '%s\n' "$story_input" | sed -nE 's/^- Story ID:[[:space:]]*(.+)$/\1/p' | head -n 1)"
if [[ ! "$story_id_value" =~ ^US1\.[0-9]+$ ]]; then
  echo "Error: Story ID must use the format 'US1.x'" >&2
  exit 1
fi

action_value="$(printf '%s\n' "$story_input" | sed -nE 's/^- Action:[[:space:]]*(.+)$/\1/p' | head -n 1)"
outcome_value="$(printf '%s\n' "$story_input" | sed -nE 's/^- Outcome:[[:space:]]*(.+)$/\1/p' | head -n 1)"
observation_value="$(printf '%s\n' "$story_input" | sed -nE 's/^- Observation:[[:space:]]*(.+)$/\1/p' | head -n 1)"

if [[ "$action_value" == "$outcome_value" || "$action_value" == "$observation_value" ]]; then
  echo "Error: action, outcome, and observation should describe distinct parts of the story" >&2
  exit 1
fi

echo "Story validation passed."