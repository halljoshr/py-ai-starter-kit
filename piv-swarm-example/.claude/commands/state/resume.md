# PIV-Swarm: Resume Command

**Resume a paused session from saved state.**

---

## Usage

```bash
/piv:resume
```

---

## Process

### Step 1: Load Session State

```yaml
# Read .agents/state/session.yaml
session:
  status: paused  # Verify was paused
  feature: user-authentication
  phase: execute
  paused_at: "2026-01-26T10:30:00Z"
```

### Step 2: Display Loaded State

```markdown
═══════════════════════════════════════════════════════════════
                    RESUMING SESSION
═══════════════════════════════════════════════════════════════

## Session Found

| Field | Value |
|-------|-------|
| Feature | user-authentication |
| Phase | execute |
| Paused | 2026-01-26 10:30 |
| Current Task | task-003 |

## Progress

- Tasks Completed: 2 / 5
- Tokens Used: 45K (previous session)

## Loading Context...
```

### Step 3: Run Startup Ritual

```bash
# Verify location
pwd
ls -la

# Check git state
git status
git log -3 --oneline

# Verify no unexpected changes
git diff --stat
```

### Step 4: Run Baseline Tests

```bash
# Verify nothing broken
uv run pytest tests/unit/ -v --tb=short
```

**If tests fail:**
```markdown
⚠️ WARNING: Baseline tests failing

Some tests are failing before we start:
- test_user_model.py::test_validation - FAILED

Options:
1. Fix failing tests first
2. Continue anyway (not recommended)
3. Abort resume

Your choice?
```

### Step 5: Load Current Task

```yaml
# Read .agents/tasks/task-003.yaml
id: task-003
name: Create Auth service
status: in_progress
notes: |
  Paused at: 2026-01-26T10:30:00Z
  Progress: ~60% complete
  Last action: Created login endpoint, working on tests
```

### Step 6: Display Task Context

```markdown
## Current Task: task-003

**Name:** Create Auth service
**Status:** In Progress (~60%)
**Last Action:** Created login endpoint, working on tests

**Remaining Work:**
- Complete auth service tests
- Add token refresh logic

**Files:**
- src/services/auth.py (exists)
- tests/unit/test_auth_service.py (partial)

Ready to continue?
```

### Step 7: Update Session State

```yaml
# Update .agents/state/session.yaml
session:
  status: active
  resumed_at: "2026-01-26T14:00:00Z"

tokens:
  used: 0  # Reset for new session (previous was 45K)
```

### Step 8: Log Resume Event

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: session_resume
  content: |
    Session resumed.
    Continuing from: task-003
    Previous progress: 45K tokens, 2/5 tasks
```

### Step 9: Update STATE.md

```markdown
## Status: ACTIVE ▶️

**Resumed:** 2026-01-26 14:00
**Continuing:** task-003 (in progress)

### Session History
- Session 1: 45K tokens, completed task-001, task-002
- Session 2: (current) continuing from task-003
```

### Step 10: Ready to Continue

```markdown
═══════════════════════════════════════════════════════════════
                    SESSION RESUMED
═══════════════════════════════════════════════════════════════

## Ready to Continue

| Field | Value |
|-------|-------|
| Feature | user-authentication |
| Current Task | task-003: Create Auth service |
| Previous Progress | 2/5 tasks, 45K tokens |
| Baseline Tests | ✓ Passing |

## Next Steps

Continue with task-003:
- Complete auth service tests
- Add token refresh logic

Or run `/piv:status` to see full state.

═══════════════════════════════════════════════════════════════
```

---

## Error Handling

### No Paused Session

```markdown
⚠️ No paused session found.

The session.yaml shows status: idle

Options:
1. Start new session with /piv:prime
2. Check if correct directory

Your choice?
```

### State Files Missing

```markdown
⚠️ State files incomplete.

Missing: .agents/state/session.yaml

This may be a new project or corrupted state.

Options:
1. Start fresh with /piv:prime
2. Attempt to reconstruct from tasks/

Your choice?
```

---

## Output

1. Loaded and displayed session state
2. Ran startup ritual (pwd, git, tests)
3. Updated session.yaml (status: active)
4. Message logged
5. Ready to continue execution
