---
name: pause
description: Pause current session and save state for later resume.
disable-model-invocation: true
allowed-tools: Read, Write, Bash(git:*)
---

# PIV-Swarm: Pause

**Pause current session and save state for later resume.**

---

## Process

### Step 1: Save Current State

Ensure all state files are current:
- `.agents/state/session.yaml`
- `.agents/state/STATE.md`
- All task files in `.agents/tasks/`

### Step 2: Update Session Status

```yaml
# .agents/state/session.yaml
session:
  status: paused
  paused_at: "2026-01-26T12:00:00Z"
```

### Step 3: Commit State (Optional)

If there are uncommitted changes:

```bash
git add .agents/
git commit -m "chore: checkpoint session state

Phase: {phase}
Tasks completed: {n}/{total}

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 4: Display Resume Instructions

```markdown
## Session Paused

**Feature:** {feature-name}
**Phase:** {phase}
**Progress:** {completed}/{total} tasks

### State Saved
- Session: .agents/state/session.yaml
- Tasks: .agents/tasks/
- Commit: {sha} (if committed)

### To Resume

In a new conversation:
/resume

The session will continue from where you left off.
```

---

## What Gets Saved

1. **Session Info** - Feature, phase, timestamps
2. **Task Status** - All task states and progress
3. **Decisions** - All discuss phase decisions
4. **Progress Metrics** - Tasks completed, phases finished
5. **History** - Event log

**Note:** Context doesn't carry over between sessions - each session starts fresh.
We save *state* (what was done) not *context* (conversation history).

---

## Notes

- Always pause before ending a long session
- State is preserved in YAML files
- Can resume in same or new conversation
