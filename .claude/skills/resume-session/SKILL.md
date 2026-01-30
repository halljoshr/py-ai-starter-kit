---
name: resume-session
description: Resume a paused PIV session from saved state.
disable-model-invocation: true
allowed-tools: Read, Write, Glob
---

# PIV-Swarm: Resume Session

**Resume a paused PIV session from saved state.**

**Usage:** `/resume-session`

---

## Process

### Step 1: Load State

Read `.agents/state/session.yaml` to get:
- Feature name
- Current phase
- Task progress
- Last activity

### Step 2: Verify State

Check that state is valid:
- Session exists
- Status is `paused` or `active`
- Phase is known
- Task files exist

### Step 3: Update Session Status

```yaml
session:
  status: active
  resumed_at: "2026-01-26T14:00:00Z"
```

### Step 4: Display Session Summary

```markdown
## Session Resumed

**Feature:** {feature-name}
**Phase:** {phase}
**Status:** active

### Progress

| Status | Count |
|--------|-------|
| Completed | {n} |
| In Progress | {n} |
| Pending | {n} |

### Last Activity
{last event from history}

### Current Task
{task-id}: {task-name}

### Next Action

Based on phase:
- **prime:** Continue context gathering
- **discuss:** Continue decision capture
- **plan:** Continue task creation
- **execute:** Continue task execution
- **validate:** Continue verification
```

### Step 5: Continue Workflow

Based on current phase, suggest next action:

- If `execute` phase with pending tasks: Show next task details
- If `validate` phase: Show remaining verifications
- If blocked: Show blocker details

---

## Recovery

If state is corrupted or missing:

```markdown
## State Recovery Needed

The session state appears incomplete.

**Options:**
1. Start fresh with `/prime`
2. Manually fix state files
3. Check git history for previous state

**Missing/Invalid:**
- {list issues}
```

---

## Notes

- Resume loads all context from files
- No conversation history is preserved
- State files are the source of truth
