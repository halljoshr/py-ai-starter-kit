#!/bin/bash
# PreToolUse hook for Bash: Block git commit if ruff check fails
# Gracefully skips if ruff is not available in the project
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -q 'git commit'; then
  if command -v uv &>/dev/null && uv run ruff --version &>/dev/null; then
    OUTPUT=$(uv run ruff check . --quiet 2>&1)
    if [[ $? -ne 0 ]]; then
      echo "$OUTPUT" >&2
      exit 2
    fi
  elif command -v ruff &>/dev/null; then
    OUTPUT=$(ruff check . --quiet 2>&1)
    if [[ $? -ne 0 ]]; then
      echo "$OUTPUT" >&2
      exit 2
    fi
  fi
fi
exit 0
