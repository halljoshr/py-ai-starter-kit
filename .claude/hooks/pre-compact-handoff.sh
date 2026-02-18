#!/bin/bash
# Pre-compact hook: instructs Claude to perform handoff before compaction
# Stdout goes to Claude, stderr goes to user only

# Read hook input from stdin
INPUT=$(cat)
TRIGGER=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('trigger','unknown'))" 2>/dev/null || echo "unknown")
TRANSCRIPT=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('transcript_path',''))" 2>/dev/null || echo "")

# Log to stderr (user sees this)
echo "[pre-compact] Trigger: $TRIGGER" >&2

# Write breadcrumb to confirm hook fired
echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) trigger=$TRIGGER transcript=$TRANSCRIPT" >> /tmp/imp-precompact.log

# Check if handoff was already done this session (marker file)
MARKER="/tmp/.imp-handoff-done-$$"
if [ -f "$MARKER" ]; then
    echo "[pre-compact] Handoff already completed, proceeding with compaction." >&2
    exit 0
fi

# Stdout goes to Claude — this is the instruction
cat <<'EOF'
IMPORTANT: Context compaction is about to occur. Before compaction proceeds, you MUST perform a session handoff:

1. Update HANDOFF.md with current state and next task
2. Update MEMORY.md conversation log with this session's summary
3. Create a conversation log in conversation-logs/ with sequential numbering
4. Write a marker file to /tmp/.imp-handoff-done to signal completion

Do this NOW before responding to any other requests. Use the /handoff skill if available, otherwise do it manually.
EOF

exit 0
