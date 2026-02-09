#!/bin/bash
# PreToolUse hook for Bash: Block git commit if ruff check fails
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -q 'git commit'; then
  OUTPUT=$(uv run ruff check . --quiet 2>&1)
  if [[ $? -ne 0 ]]; then
    echo "$OUTPUT" >&2
    exit 2
  fi
fi
exit 0
