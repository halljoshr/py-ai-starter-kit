#!/bin/bash
# Stop hook: checks real token usage from transcript and triggers handoff
# before context runs out. Fires after every assistant turn.
# Exit code 2 = block + feed stderr to Claude.

INPUT=$(cat)

# Parse JSON input
TRANSCRIPT=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('transcript_path',''))" 2>/dev/null || echo "")
STOP_HOOK_ACTIVE=$(echo "$INPUT" | python3 -c "import sys,json; print(json.load(sys.stdin).get('stop_hook_active',False))" 2>/dev/null || echo "False")

# CRITICAL: prevent infinite loop
if [ "$STOP_HOOK_ACTIVE" = "True" ] || [ "$STOP_HOOK_ACTIVE" = "true" ]; then
    exit 0
fi

# If handoff already done this session, don't nag
MARKER="/tmp/.imp-handoff-done"
if [ -f "$MARKER" ]; then
    exit 0
fi

# No transcript? Nothing to check
if [ -z "$TRANSCRIPT" ] || [ ! -f "$TRANSCRIPT" ]; then
    exit 0
fi

# Threshold = 80% of the autocompact point
# Autocompact fires at: (context_window - max_output_tokens) * autocompact_pct
# Default values match settings.json: 200k window, 32k output reserved, 95% autocompact
CONTEXT_WINDOW="${IMP_CONTEXT_WINDOW:-200000}"
MAX_OUTPUT_TOKENS="${CLAUDE_CODE_MAX_OUTPUT_TOKENS:-32000}"
AUTOCOMPACT_PCT="${CLAUDE_AUTOCOMPACT_PCT_OVERRIDE:-95}"
WARN_FRACTION="${IMP_WARN_FRACTION:-80}"  # warn at this % of the compaction point

# Parse real token usage from the last assistant message in the transcript
TOKEN_INFO=$(python3 -c "
import json, sys

transcript = '$TRANSCRIPT'
last_usage = None
try:
    with open(transcript) as f:
        for line in f:
            obj = json.loads(line)
            if obj.get('type') == 'assistant':
                msg = obj.get('message', {})
                usage = msg.get('usage', {})
                if usage:
                    last_usage = usage
except Exception:
    pass

if last_usage:
    total = (last_usage.get('input_tokens', 0) +
             last_usage.get('cache_creation_input_tokens', 0) +
             last_usage.get('cache_read_input_tokens', 0) +
             last_usage.get('output_tokens', 0))
    print(total)
else:
    print(0)
" 2>/dev/null || echo "0")

# Compute warn threshold: 80% of compaction point
COMPACTION_TOKENS=$(( (CONTEXT_WINDOW - MAX_OUTPUT_TOKENS) * AUTOCOMPACT_PCT / 100 ))
THRESHOLD_TOKENS=$(( COMPACTION_TOKENS * WARN_FRACTION / 100 ))

if [ "$TOKEN_INFO" -gt "$THRESHOLD_TOKENS" ] 2>/dev/null; then
    PCT_USED=$(( TOKEN_INFO * 100 / CONTEXT_WINDOW ))
    PCT_TO_COMPACT=$(( TOKEN_INFO * 100 / COMPACTION_TOKENS ))

    # Log for debugging
    echo "$(date -u +%Y-%m-%dT%H:%M:%SZ) TRIGGERED tokens=${TOKEN_INFO} warn_threshold=${THRESHOLD_TOKENS} compaction_at=${COMPACTION_TOKENS} pct_to_compact=${PCT_TO_COMPACT}% transcript=$TRANSCRIPT" >> /tmp/imp-context-check.log

    cat >&2 <<EOF
CONTEXT BUDGET WARNING: You have used ${PCT_TO_COMPACT}% of the way to autocompaction (${TOKEN_INFO} / ${COMPACTION_TOKENS} tokens). Compaction fires around ${COMPACTION_TOKENS} tokens.

You MUST perform a session handoff NOW before context runs out:

1. Update HANDOFF.md with current state and next task
2. Update MEMORY.md conversation log with this session's summary
3. Create a conversation log in conversation-logs/ with sequential numbering
4. Write a marker file: touch /tmp/.imp-handoff-done

Use the /handoff skill. Do this NOW — do not continue other work until handoff is complete.
EOF
    exit 2
fi

exit 0
