#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: validate_frontmatter_provenance.sh <artifact-kind> <artifact-file>" >&2
  exit 1
fi

artifact_kind="$1"
artifact_file="$2"

case "$artifact_kind" in
  charter|user-stories|requirements|technical-design|plan|tasks)
    ;;
  *)
    echo "Unsupported artifact kind: $artifact_kind" >&2
    exit 1
    ;;
esac

if [[ ! -f "$artifact_file" ]]; then
  echo "Artifact file not found: $artifact_file" >&2
  exit 1
fi

if [[ "$(head -n1 "$artifact_file")" != "---" ]]; then
  echo "Missing opening YAML frontmatter delimiter" >&2
  exit 1
fi

if [[ "$(grep -n '^---$' "$artifact_file" | wc -l | tr -d ' ')" -lt 2 ]]; then
  echo "Missing closing YAML frontmatter delimiter" >&2
  exit 1
fi

frontmatter="$({
  awk 'NR == 1 && $0 == "---" { in_frontmatter = 1; next }
       in_frontmatter && $0 == "---" { exit }
       in_frontmatter { print }' "$artifact_file"
} || true)"

if [[ -z "$frontmatter" ]]; then
  echo "Frontmatter is empty" >&2
  exit 1
fi

extract_value() {
  local key="$1"
  printf '%s\n' "$frontmatter" | sed -nE "s/^${key}: (.+)$/\1/p" | head -n1
}

extract_top_level_block() {
  local key="$1"
  printf '%s\n' "$frontmatter" | awk -v key="$key" '
    $0 == key ":" { in_block = 1; next }
    in_block && $0 ~ /^[^[:space:]]/ { exit }
    in_block { print }
  '
}

name_value="$(extract_value name)"
created_at="$(extract_value created_at)"
updated_at="$(extract_value updated_at)"

if [[ -z "$name_value" ]] || [[ ! "$name_value" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "Missing or invalid frontmatter field: name" >&2
  exit 1
fi

iso_utc_pattern='^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$'
if [[ -z "$created_at" ]] || [[ ! "$created_at" =~ $iso_utc_pattern ]]; then
  echo "Missing or invalid frontmatter field: created_at (expected UTC ISO 8601)" >&2
  exit 1
fi
if [[ -z "$updated_at" ]] || [[ ! "$updated_at" =~ $iso_utc_pattern ]]; then
  echo "Missing or invalid frontmatter field: updated_at (expected UTC ISO 8601)" >&2
  exit 1
fi
if [[ "$created_at" > "$updated_at" ]]; then
  echo "created_at must be less than or equal to updated_at" >&2
  exit 1
fi

generated_by_block="$(extract_top_level_block generated_by)"
if [[ -z "$generated_by_block" ]]; then
  echo "Missing frontmatter block: generated_by" >&2
  exit 1
fi

root_skill="$(printf '%s\n' "$generated_by_block" | sed -nE 's/^  root_skill: (.+)$/\1/p' | head -n1)"
producing_skill="$(printf '%s\n' "$generated_by_block" | sed -nE 's/^  producing_skill: (.+)$/\1/p' | head -n1)"
skill_name_pattern='^[a-z0-9]+(-[a-z0-9]+)*$'

if [[ -z "$root_skill" ]] || [[ ! "$root_skill" =~ $skill_name_pattern ]]; then
  echo "Missing or invalid generated_by.root_skill" >&2
  exit 1
fi
if [[ -z "$producing_skill" ]] || [[ ! "$producing_skill" =~ $skill_name_pattern ]]; then
  echo "Missing or invalid generated_by.producing_skill" >&2
  exit 1
fi

skills_used_block="$(printf '%s\n' "$generated_by_block" | awk '
  $0 == "  skills_used:" { in_block = 1; next }
  in_block && $0 ~ /^  [a-z_]+:/ { exit }
  in_block { print }
')"
mapfile -t skills_used < <(printf '%s\n' "$skills_used_block" | sed -nE 's/^    - ([a-z0-9-]+)$/\1/p')
if (( ${#skills_used[@]} == 0 )); then
  echo "generated_by.skills_used must include at least one skill" >&2
  exit 1
fi
if [[ "${skills_used[0]}" != "$root_skill" ]]; then
  echo "generated_by.skills_used must start with root_skill" >&2
  exit 1
fi

seen_skills=""
for skill in "${skills_used[@]}"; do
  if [[ ! "$skill" =~ $skill_name_pattern ]]; then
    echo "Invalid skill name in generated_by.skills_used: $skill" >&2
    exit 1
  fi
  if [[ " $seen_skills " == *" $skill "* ]]; then
    echo "Duplicate skill in generated_by.skills_used: $skill" >&2
    exit 1
  fi
  seen_skills+=" $skill"
done

if [[ " $seen_skills " != *" $producing_skill "* ]]; then
  echo "generated_by.producing_skill must appear in generated_by.skills_used" >&2
  exit 1
fi

skill_graph_block="$(printf '%s\n' "$generated_by_block" | awk '
  $0 == "  skill_graph:" { in_block = 1; next }
  in_block && $0 ~ /^  [a-z_]+:/ { exit }
  in_block { print }
')"
if [[ -z "$skill_graph_block" ]]; then
  echo "generated_by.skill_graph must not be empty" >&2
  exit 1
fi

mapfile -t skill_graph_keys < <(printf '%s\n' "$skill_graph_block" | sed -nE 's/^    ([a-z0-9-]+):( \[\])?$/\1/p')
if (( ${#skill_graph_keys[@]} == 0 )); then
  echo "generated_by.skill_graph must include at least one skill entry" >&2
  exit 1
fi

for skill in "${skills_used[@]}"; do
  if [[ ! " ${skill_graph_keys[*]} " =~ (^|[[:space:]])${skill}($|[[:space:]]) ]]; then
    echo "generated_by.skill_graph is missing entry for skill: $skill" >&2
    exit 1
  fi
done

current_graph_skill=""
while IFS= read -r line; do
  if [[ "$line" =~ ^[[:space:]]{4}([a-z0-9-]+):([[:space:]]\[\])?$ ]]; then
    current_graph_skill="${BASH_REMATCH[1]}"
    continue
  fi
  if [[ "$line" =~ ^[[:space:]]{6}-[[:space:]]([a-z0-9-]+)$ ]]; then
    dependency="${BASH_REMATCH[1]}"
    if [[ -z "$current_graph_skill" ]]; then
      echo "generated_by.skill_graph dependency appears before a skill key" >&2
      exit 1
    fi
    if [[ ! " $seen_skills " =~ (^|[[:space:]])${dependency}($|[[:space:]]) ]]; then
      echo "generated_by.skill_graph dependency is not listed in generated_by.skills_used: $dependency" >&2
      exit 1
    fi
    continue
  fi
  if [[ -n "$line" ]]; then
    echo "Invalid generated_by.skill_graph line: $line" >&2
    exit 1
  fi
done <<< "$skill_graph_block"

source_artifacts_line="$(printf '%s\n' "$frontmatter" | sed -nE 's/^source_artifacts: (.+)$/\1/p' | head -n1)"
source_artifacts_block="$(extract_top_level_block source_artifacts)"

if [[ "$artifact_kind" == "charter" ]]; then
  if [[ "$source_artifacts_line" != "{}" ]]; then
    echo "Charter artifacts must use 'source_artifacts: {}'" >&2
    exit 1
  fi
else
  if [[ -n "$source_artifacts_line" ]]; then
    echo "source_artifacts must use an expanded mapping for artifact kind: $artifact_kind" >&2
    exit 1
  fi
  if [[ -z "$source_artifacts_block" ]]; then
    echo "Missing frontmatter block: source_artifacts" >&2
    exit 1
  fi

  mapfile -t source_artifact_entries < <(printf '%s\n' "$source_artifacts_block" | sed -nE 's/^  ([a-z_]+): (.+)$/\1\t\2/p')
  if (( ${#source_artifact_entries[@]} == 0 )); then
    echo "source_artifacts must include at least one artifact path for artifact kind: $artifact_kind" >&2
    exit 1
  fi

  declare -A seen_artifact_types=()
  for entry in "${source_artifact_entries[@]}"; do
    artifact_type="${entry%%$'\t'*}"
    path_value="${entry#*$'\t'}"

    if [[ -n "${seen_artifact_types[$artifact_type]:-}" ]]; then
      echo "Duplicate source_artifacts artifact-type: $artifact_type" >&2
      exit 1
    fi
    seen_artifact_types[$artifact_type]=1

    if [[ ! "$artifact_type" =~ ^[a-z_]+$ ]]; then
      echo "Invalid source_artifacts artifact-type: $artifact_type" >&2
      exit 1
    fi
    if [[ ! "$path_value" =~ ^\.specs/.+\.md$ ]]; then
      echo "Invalid source_artifacts path for artifact-type ${artifact_type}: $path_value" >&2
      exit 1
    fi
  done
fi

echo "Frontmatter provenance validation passed: $artifact_file"
