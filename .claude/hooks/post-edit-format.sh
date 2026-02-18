#!/bin/bash
# PostToolUse hook for Edit|Write: Auto-format and lint-fix Python files
# Gracefully no-ops if ruff is not available in the project
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ -z "$FILE_PATH" || "$FILE_PATH" != *.py ]]; then
  exit 0
fi

# Try uv run ruff first, fall back to bare ruff, skip if neither exists
if command -v uv &>/dev/null && uv run ruff --version &>/dev/null; then
  uv run ruff format --quiet "$FILE_PATH" 2>/dev/null
  uv run ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
elif command -v ruff &>/dev/null; then
  ruff format --quiet "$FILE_PATH" 2>/dev/null
  ruff check --fix --quiet "$FILE_PATH" 2>/dev/null
fi
exit 0
