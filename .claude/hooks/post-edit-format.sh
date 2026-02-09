#!/bin/bash
# PostToolUse hook for Edit|Write: Auto-format and lint-fix Python files
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE_PATH" || "$FILE_PATH" != *.py ]]; then
  exit 0
fi

uv run ruff format --quiet "$FILE_PATH" 2>/dev/null
uv run ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
exit 0
