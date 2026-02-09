#!/bin/bash
# PostToolUseFailure hook for Bash: Feed fix instructions back to Claude
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE 'pytest|uv run pytest'; then
  echo "TESTS FAILED. Read the error output above carefully. Identify the failing test(s) and root cause. Fix the implementation code (not the tests) unless the tests themselves are wrong. Then re-run the failing tests to verify."
  exit 0
fi

if echo "$COMMAND" | grep -qE 'ruff check|uv run ruff'; then
  echo "LINT FAILED. Read the ruff errors above. Fix each violation in the reported files. Then re-run ruff check to verify."
  exit 0
fi

if echo "$COMMAND" | grep -qE 'mypy|uv run mypy'; then
  echo "TYPE CHECK FAILED. Read the mypy errors above. Fix the type annotations or logic causing the errors. Then re-run mypy to verify."
  exit 0
fi

exit 0
