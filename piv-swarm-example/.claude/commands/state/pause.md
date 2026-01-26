# PIV-Swarm: Pause Command

**Save state and pause work for later resumption.**

---

## Usage

```bash
/piv:pause
```

---

## Process

### Step 1: Save Current Task State

If a task is in progress:

```yaml
# Update .agents/tasks/{current-task}.yaml
status: in_progress  # Keep as in_progress
notes: |
  Paused at: 2026-01-26T10:30:00Z
  Progress: ~60% complete
  Last action: Created login endpoint, working on tests
```

### Step 2: Update Session State

```yaml
# Update .agents/state/session.yaml
session:
  status: paused
  paused_at: "2026-01-26T10:30:00Z"

tokens:
  used: 45000  # Record current usage
```

### Step 3: Commit Any Pending Changes

```bash
# If there are uncommitted changes
git status

# Stage and commit WIP
git add .
git commit -m "WIP: Pause point for {feature}

- Current task: {task-id}
- Progress: ~{N}% complete
- Tokens used: {N}K

Session paused for later resumption."
```

### Step 4: Update STATE.md

```markdown
## Status: PAUSED ⏸️

**Paused:** 2026-01-26 10:30
**Current Task:** task-003 (in progress, ~60%)
**Tokens Used:** 45K

### To Resume

In a new conversation:
```bash
/piv:resume
```

The session will continue from task-003.
```

### Step 5: Log Pause Event

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: session_pause
  content: |
    Session paused.
    Current task: task-003 (~60% complete)
    Tokens used: 45K
    Resume with: /piv:resume
```

### Step 6: Display Resume Instructions

```markdown
═══════════════════════════════════════════════════════════════
                     SESSION PAUSED
═══════════════════════════════════════════════════════════════

## Progress Saved

| Field | Value |
|-------|-------|
| Feature | user-authentication |
| Current Task | task-003: Create Auth service |
| Task Progress | ~60% complete |
| Tokens Used | 45K |
| Tasks Completed | 2 / 5 |

## Changes Committed

Commit: abc1234
Message: "WIP: Pause point for user-authentication"

## To Resume

Start a new conversation and run:

```bash
/piv:resume
```

The session will:
1. Load saved state
2. Continue from task-003
3. Pick up where you left off

═══════════════════════════════════════════════════════════════
```

---

## When to Pause

- End of work session
- Need to switch to different task
- Token budget getting high (approaching 150K)
- Waiting for external input/blocker resolution

---

## What Gets Saved

- Session state (feature, phase, status)
- Token usage
- Task statuses
- Current task progress notes
- All decisions from discuss phase
- Message history

---

## Output

1. Updated session.yaml with paused status
2. Updated STATE.md with resume instructions
3. WIP commit if uncommitted changes
4. Message logged
5. Resume instructions displayed
