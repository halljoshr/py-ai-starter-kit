#!/bin/bash
# Notification hook: macOS notification when permission prompt appears
osascript -e 'display notification "Claude Code needs your attention" with title "Permission Required"' 2>/dev/null
exit 0
