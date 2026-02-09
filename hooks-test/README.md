# Claude Code Hooks: Research, Testing, and Implementation Guide

## Purpose of This Directory

This directory exists as a **proof-of-concept and testing ground** for Claude Code hook scripts. It was created during a session where we built out a comprehensive `.claude/settings.local.json` configuration and needed a controlled environment to verify that each hook actually works before deploying them globally.

The core problem we were solving: **Claude Code hooks receive data via stdin as JSON, not environment variables.** Our first implementation used `$CLAUDE_FILE_PATH` and `$CLAUDE_TOOL_INPUT` — variables that don't exist. Every hook silently failed. This test directory let us isolate, debug, and verify each hook independently before trusting them in production workflows.

---

## What We Learned (The Hard Way)

### 1. Hooks Receive Data via stdin, Not Environment Variables

This is the single most important thing to know. Every hook of type `"command"` receives a JSON payload on stdin. The only environment variable reliably available is `$CLAUDE_PROJECT_DIR` (the project root).

**Wrong (will silently fail):**
```bash
# These variables DO NOT EXIST
uv run ruff format "$CLAUDE_FILE_PATH"
if echo "$CLAUDE_TOOL_INPUT" | grep -q 'git commit'; then ...
```

**Correct:**
```bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')
```

**Dependency:** All hook scripts require `jq` to parse the JSON stdin. Verify with `which jq` before deploying.

### 2. The JSON Schema Varies by Hook Event and Tool

Each hook event type sends a different JSON structure. Here are the ones we tested:

**PostToolUse / PreToolUse for Edit/Write:**
```json
{
  "session_id": "abc123",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/absolute/path/to/file.py",
    "content": "file contents here"
  },
  "tool_response": {
    "filePath": "/absolute/path/to/file.py",
    "success": true
  }
}
```

**PostToolUse / PreToolUse for Bash:**
```json
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "uv run pytest tests/ -v",
    "description": "Run test suite",
    "timeout": 120000
  }
}
```

**PostToolUseFailure for Bash:**
```json
{
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "uv run pytest tests/ -v"
  },
  "error": "Command exited with non-zero status code 1"
}
```

**SessionStart:**
```json
{
  "session_id": "abc123",
  "hook_event_name": "SessionStart"
}
```

### 3. Hook Exit Codes Have Meaning

- **Exit 0:** Hook succeeded. stdout is fed back to Claude as context.
- **Exit 2:** Hook wants to **block** the tool use (PreToolUse only). stderr becomes the error message shown to Claude.
- **Any other non-zero exit:** Hook failed. Claude Code may log it but continues.

This is critical for the pre-commit lint gate: `exit 2` prevents the commit from happening.

### 4. Settings Changes Require a New Session

Modifying `.claude/settings.local.json` or `~/.claude/settings.json` mid-session does **not** reload hooks. You must start a new Claude Code session for hook changes to take effect. This is why we tested hooks manually with piped stdin rather than relying on live Claude Code invocation.

### 5. Hook stdout is Fed Back to Claude as Context

Whatever a hook prints to stdout gets injected into Claude's context as a `<user-prompt-submit-hook>` or similar system message. This is the mechanism that makes the auto-fix loop work: when pytest fails, the PostToolUseFailure hook prints instructions telling Claude to fix the code and re-run tests. Claude sees those instructions and acts on them.

### 6. The `statusMessage` Property Does Not Exist

The JSON schema for hook configuration does not include `statusMessage`. Our first version included it and the schema validator flagged it. Only these properties are valid on a hook entry: `type`, `command`, `timeout`.

---

## Architecture of the Hook System

### File Layout

```
~/.claude/
├── settings.json              # Global settings (permissions, env, hooks)
└── hooks/                     # Global hook scripts
    ├── post-edit-format.sh    # Auto-format Python files after Edit/Write
    ├── post-commit-confirm.sh # Show git log after commits
    ├── post-failure-autofix.sh # Feed fix instructions on test/lint/type failures
    ├── pre-commit-lint.sh     # Block commits if ruff check fails
    ├── session-start-piv.sh   # Load PIV session state on startup
    └── notify-permission.sh   # macOS notification on permission prompts

<project>/.claude/
├── settings.local.json        # Project-specific overrides (gitignored)
├── settings.json              # Shared project settings (committed)
└── hooks/                     # Project-specific hook scripts
    └── (project-specific hooks here)
```

### Settings Precedence (Highest to Lowest)

1. Managed settings (system-level, IT-controlled)
2. Command-line arguments
3. Local project settings (`.claude/settings.local.json`)
4. Shared project settings (`.claude/settings.json`)
5. User settings (`~/.claude/settings.json`)

Hooks from **all levels are merged**, not overridden. A global PostToolUse hook and a project-level PostToolUse hook both fire.

### Hook Execution Flow

```
Claude decides to use a tool (e.g., Write)
    │
    ├─→ PreToolUse hooks fire (can block with exit 2)
    │       │
    │       └─→ If blocked: tool does NOT execute, stderr shown to Claude
    │
    ├─→ Tool executes
    │       │
    │       ├─→ Success: PostToolUse hooks fire
    │       │       └─→ stdout fed to Claude as context
    │       │
    │       └─→ Failure: PostToolUseFailure hooks fire
    │               └─→ stdout fed to Claude as context (auto-fix instructions)
    │
    └─→ Claude continues with hook feedback in context
```

---

## The Six Hooks We Built

### 1. post-edit-format.sh (PostToolUse → Edit|Write)

**Purpose:** Auto-format Python files immediately after Claude writes or edits them.

**Why it matters:** Claude sometimes produces code with minor formatting inconsistencies. Running ruff format + ruff check --fix after every write ensures code is always clean without Claude spending tokens on formatting.

**Graceful degradation:** Tries `uv run ruff` first, falls back to bare `ruff`, skips entirely if neither is available. Only processes `.py` files.

**Testing method:**
```bash
echo '{"tool_input": {"file_path": "/path/to/ugly_file.py"}}' | ~/.claude/hooks/post-edit-format.sh
# Then inspect the file - should be formatted
```

### 2. post-commit-confirm.sh (PostToolUse → Bash)

**Purpose:** After a git commit, echo `git log --oneline -1` to confirm what was committed.

**Why it matters:** Provides immediate visual confirmation in Claude's context that the commit landed.

**Testing method:**
```bash
echo '{"tool_input": {"command": "git commit -m \"feat: add feature\""}}' | ~/.claude/hooks/post-commit-confirm.sh
# Should output the latest commit hash and message
```

### 3. post-failure-autofix.sh (PostToolUseFailure → Bash)

**Purpose:** When pytest, ruff, or mypy fails, inject targeted fix instructions into Claude's context.

**Why it matters:** This creates a self-correcting loop. Without it, Claude sees the error but may not immediately act on it. With the hook, Claude receives explicit instructions like "Read the error output above. Fix the implementation code. Re-run to verify." This dramatically reduces the number of turns needed to resolve failures.

**Pattern matching:**
- `pytest` or `uv run pytest` → test fix instructions
- `ruff check` or `uv run ruff` → lint fix instructions
- `mypy` or `uv run mypy` → type check fix instructions
- Anything else → silent (exit 0, no output)

**Testing method:**
```bash
echo '{"tool_input": {"command": "uv run pytest tests/ -v"}}' | ~/.claude/hooks/post-failure-autofix.sh
# Should output: "TESTS FAILED. Read the error output above..."

echo '{"tool_input": {"command": "ls -la"}}' | ~/.claude/hooks/post-failure-autofix.sh
# Should output nothing (silent pass-through)
```

### 4. pre-commit-lint.sh (PreToolUse → Bash)

**Purpose:** Block `git commit` if `ruff check .` finds violations.

**Why it matters:** Prevents committing code with lint errors. Acts as a pre-commit hook but at the Claude Code level rather than git level. The advantage over git hooks is that Claude sees the lint errors in context and can fix them before retrying.

**Blocking mechanism:** Exits with code 2 and sends ruff output to stderr, which Claude Code interprets as "block this tool use."

**Testing method:**
```bash
# Create a file with lint errors first, then:
echo '{"tool_input": {"command": "git commit -m \"test\""}}' | ~/.claude/hooks/pre-commit-lint.sh
echo "Exit code: $?"
# Should output lint errors to stderr and exit with code 2
```

### 5. session-start-piv.sh (SessionStart → startup)

**Purpose:** On session startup, check for an active PIV session and display its state.

**Why it matters:** When resuming work across sessions, this immediately shows Claude where the previous session left off — which phase, how many tasks completed, what's pending. Enables seamless `/piv:resume` workflows.

**Graceful degradation:** Only outputs if `.agents/state/session.yaml` exists. Silent otherwise (no "No active PIV session" noise for non-PIV projects).

**Testing method:**
```bash
# Create a test session file:
mkdir -p /tmp/test-project/.agents/state
echo -e "session:\n  phase: execute\n  feature: user-auth" > /tmp/test-project/.agents/state/session.yaml

echo '{}' | CLAUDE_PROJECT_DIR="/tmp/test-project" ~/.claude/hooks/session-start-piv.sh
# Should output the session state
```

### 6. notify-permission.sh (Notification → permission_prompt)

**Purpose:** Send a macOS notification when Claude Code is waiting for a permission decision.

**Why it matters:** If you tab away while Claude is working, you won't see the permission prompt. This hook sends a native macOS notification so you know to come back. Especially useful during long agent team runs where permission prompts can stall the entire pipeline.

**Platform-specific:** Uses `osascript` (macOS only). On Linux, replace with `notify-send`. Fails silently on unsupported platforms.

**Testing method:**
```bash
echo '{}' | ~/.claude/hooks/notify-permission.sh
# Should display a macOS notification
```

---

## How to Adapt This for Your Project

### Step 1: Identify Your Tool Chain

The hooks we built assume a Python/ruff/mypy/pytest stack. Map your project's tools:

| Our Hook | Python Stack | Node/TS Equivalent | Go Equivalent | Rust Equivalent |
|----------|-------------|-------------------|---------------|-----------------|
| Auto-format | `ruff format` | `prettier --write` | `gofmt -w` | `rustfmt` |
| Auto-lint | `ruff check --fix` | `eslint --fix` | `golangci-lint run` | `clippy --fix` |
| Test failure | `pytest` | `jest`, `vitest` | `go test` | `cargo test` |
| Type check | `mypy` | `tsc --noEmit` | (built-in) | (built-in) |
| Pre-commit lint | `ruff check .` | `eslint .` | `golangci-lint run` | `cargo clippy` |

### Step 2: Create Your Hook Scripts

Use this template for any PostToolUse hook on file changes:

```bash
#!/bin/bash
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Guard: skip if no file path or wrong file type
if [[ -z "$FILE_PATH" || "$FILE_PATH" != *.<your-extension> ]]; then
  exit 0
fi

# Guard: skip if tool not available
if ! command -v <your-tool> &>/dev/null; then
  exit 0
fi

# Do the thing
<your-tool> "$FILE_PATH"
exit 0
```

Use this template for PostToolUseFailure auto-fix hooks:

```bash
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if echo "$COMMAND" | grep -qE '<your-test-command>'; then
  echo "TESTS FAILED. <Your specific instructions for Claude to fix the issue.>"
  exit 0
fi

exit 0
```

### Step 3: Decide Global vs Project-Level

**Put in `~/.claude/hooks/` (global) if:**
- The hook is tool-agnostic (git commit confirm, notifications)
- The hook gracefully no-ops when its tool isn't available
- You want it in every project

**Put in `<project>/.claude/hooks/` (project-level) if:**
- The hook is specific to this project's unique workflow
- The hook references project-specific paths or configs
- The hook should be shared with the team (committed to git)

### Step 4: Test Before Deploying

**Never trust a hook you haven't tested manually.** Use the stdin piping pattern:

```bash
# Simulate Claude writing a file
echo '{"tool_input": {"file_path": "/path/to/file.py"}}' | ./your-hook.sh

# Simulate a failed test run
echo '{"tool_input": {"command": "npm test"}}' | ./your-hook.sh

# Check exit codes for blocking hooks
echo '{"tool_input": {"command": "git commit -m test"}}' | ./your-hook.sh 2>/dev/null
echo "Exit code: $?"  # Should be 2 if blocking, 0 if allowing
```

---

## Advanced Patterns (Theory)

### Pattern: Cascading Auto-Fix Loop

The PostToolUseFailure hook creates a feedback loop:

```
Claude runs tests → Tests fail → Hook injects "fix it" instructions →
Claude reads errors + instructions → Claude fixes code → Claude re-runs tests →
Tests pass (or loop repeats)
```

This can be extended to create multi-stage validation:

```bash
# In post-failure-autofix.sh, add cascading instructions:
if echo "$COMMAND" | grep -qE 'pytest'; then
  echo "TESTS FAILED."
  echo "1. Fix the failing test(s) based on the error output above."
  echo "2. After fixing, run: uv run ruff check . --quiet"
  echo "3. After lint passes, run: uv run mypy src/ --quiet"
  echo "4. After type check passes, re-run the original test command."
  exit 0
fi
```

### Pattern: Context-Aware Hooks

Hooks can read project configuration to adapt behavior:

```bash
#!/bin/bash
INPUT=$(cat)
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"

# Check if this is a Python project
if [ -f "$PROJECT_DIR/pyproject.toml" ]; then
  # Python formatting
  ...
elif [ -f "$PROJECT_DIR/package.json" ]; then
  # Node formatting
  ...
elif [ -f "$PROJECT_DIR/go.mod" ]; then
  # Go formatting
  ...
fi
```

### Pattern: Agent Team Coordination

For PIV-Swarm or agent team workflows, hooks can coordinate state:

```bash
#!/bin/bash
# PostToolUse hook: Log agent activity to shared state
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
PROJECT_DIR="${CLAUDE_PROJECT_DIR:-.}"
STATE_FILE="$PROJECT_DIR/.agents/state/activity.log"

if [ -d "$PROJECT_DIR/.agents" ]; then
  echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $TOOL_NAME used" >> "$STATE_FILE"
fi
exit 0
```

### Pattern: Conditional PreToolUse Gates

Beyond lint checking, PreToolUse hooks can enforce project policies:

```bash
#!/bin/bash
# Block writes to protected files
INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name')
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

if [[ "$TOOL_NAME" == "Write" || "$TOOL_NAME" == "Edit" ]]; then
  # Block modifications to migration files
  if echo "$FILE_PATH" | grep -q '/migrations/'; then
    echo "BLOCKED: Migration files should not be modified directly. Create a new migration instead." >&2
    exit 2
  fi

  # Block modifications to generated files
  if echo "$FILE_PATH" | grep -q '/generated/'; then
    echo "BLOCKED: Generated files should not be modified. Update the generator instead." >&2
    exit 2
  fi
fi
exit 0
```

---

## Test Results from This Directory

All hooks were verified manually by piping simulated JSON stdin:

| # | Hook | Event | Test | Result |
|---|------|-------|------|--------|
| 1 | post-edit-format.sh | PostToolUse (Edit\|Write) | Ugly Python → auto-formatted, unused imports removed | PASS |
| 2 | post-failure-autofix.sh | PostToolUseFailure (pytest) | Outputs test fix instructions | PASS |
| 3 | post-failure-autofix.sh | PostToolUseFailure (ruff) | Outputs lint fix instructions | PASS |
| 4 | post-failure-autofix.sh | PostToolUseFailure (mypy) | Outputs type check fix instructions | PASS |
| 5 | post-failure-autofix.sh | PostToolUseFailure (other) | Silent for non-matching commands | PASS |
| 6 | pre-commit-lint.sh | PreToolUse (git commit) | Blocks commit with exit 2 on lint errors | PASS |
| 7 | pre-commit-lint.sh | PreToolUse (non-commit) | Silent pass-through | PASS |
| 8 | post-commit-confirm.sh | PostToolUse (git commit) | Shows git log --oneline -1 | PASS |
| 9 | session-start-piv.sh | SessionStart (no session) | Silent (no output) | PASS |
| 10 | session-start-piv.sh | SessionStart (with session) | Prints session YAML state | PASS |
| 11 | notify-permission.sh | Notification | Sends macOS notification | PASS |

---

## Files in This Directory

```
hooks-test/
├── README.md              # This file
├── pyproject.toml         # Minimal Python project config (ruff, mypy, pytest)
├── src/
│   ├── __init__.py
│   └── math_utils.py     # Simple module used for hook testing
└── tests/
    ├── __init__.py
    └── test_math.py       # Tests including a deliberate failure for hook testing
```

This directory can be safely deleted once the hooks are verified in a real project. Its value is as a reference and testing sandbox, not as production code.
