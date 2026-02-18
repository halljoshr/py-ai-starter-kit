#!/bin/bash
# PostToolUse hook for Bash: Show commit confirmation after git commit
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -q 'git commit'; then
  git log --oneline -1 2>/dev/null
fi
exit 0
