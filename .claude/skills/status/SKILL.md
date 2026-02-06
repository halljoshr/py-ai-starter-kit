---
name: status
description: Display current PIV session state including tasks, agents, and context budget.
allowed-tools: Read
---

# PIV-Swarm: Status

**Display current session state.**

---

## Process

### Step 1: Read State Files

Read:
- `.agents/state/session.yaml`
- `.agents/state/STATE.md`

### Step 2: Display Summary

```markdown
═══════════════════════════════════════════════════════════════
                      PIV-SWARM STATUS
═══════════════════════════════════════════════════════════════

## Session

| Field | Value |
|-------|-------|
| Feature | {feature-name} |
| Phase | {phase} |
| Status | {status} |
| Started | {timestamp} |

## Context Budget

Used:     45K / 200K [████████░░░░░░░░░░░░░░░░░░░░░░] 22%
Warning:  150K (75%)
Critical: 175K (88%)

Note: This tracks context window usage for THIS session only.
Each new session starts fresh with full ~200K capacity.

## Agents

| Agent | Role | Status | Task |
|-------|------|--------|------|
| main | orchestrator | active | {task-id} |

## Tasks

| Status | Count |
|--------|-------|
| Completed | {n} |
| In Progress | {n} |
| Pending | {n} |
| Blocked | {n} |

### Current Task
**{task-id}:** {task-name}
- Status: in_progress
- Started: {time}

### Task Queue
1. {next-task}: {name} (blocked by ...)
2. ...

## Blockers

{blockers or "None"}

═══════════════════════════════════════════════════════════════
```

---

## Notes

- Read-only command (doesn't modify state)
- Quick overview for orientation
- Use `/task-list` for detailed task view
