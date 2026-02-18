#!/bin/bash
# SessionStart hook: Load PIV session state if it exists
SESSION_FILE="${CLAUDE_PROJECT_DIR:-.}/.agents/state/session.yaml"
if [ -f "$SESSION_FILE" ]; then
  echo "PIV session found:"
  head -20 "$SESSION_FILE"
fi
exit 0
