# PIV-Swarm: Status Command

**Display current session state.**

---

## Usage

```bash
/piv:status
```

---

## Process

### Step 1: Read State Files

```bash
# Read all state files
cat .agents/state/session.yaml
cat .agents/state/agents.yaml
cat .agents/state/STATE.md
```

### Step 2: Display Summary

```markdown
═══════════════════════════════════════════════════════════════
                      PIV-SWARM STATUS
═══════════════════════════════════════════════════════════════

## Session

| Field | Value |
|-------|-------|
| Feature | user-authentication |
| Phase | execute |
| Status | active |
| Started | 2026-01-26 10:00 |

## Token Budget

```
Used:     45K / 200K [████████░░░░░░░░░░░░░░░░░░░░░░] 22%
Warning:  150K (75%)
Critical: 175K (88%)
```

## Agents

| Agent | Role | Status | Task |
|-------|------|--------|------|
| main | orchestrator | active | task-003 |

## Tasks

| Status | Count |
|--------|-------|
| Completed | 2 |
| In Progress | 1 |
| Pending | 2 |
| Blocked | 0 |
| Failed | 0 |

### Current Task
**task-003:** Create Auth service
- Status: in_progress
- Owner: main
- Started: 10:15

### Task Queue
1. task-004: Create Login endpoint (blocked by task-003)
2. task-005: Add integration tests (blocked by task-004)

## Recent Activity

| Time | Event |
|------|-------|
| 10:15 | Started task-003 |
| 10:10 | Completed task-002 |
| 10:05 | Completed task-001 |
| 10:00 | Session started |

## Blockers

None

═══════════════════════════════════════════════════════════════
```

---

## Output

Formatted status display showing:
- Session info
- Token budget with visual bar
- Agent status
- Task counts and queue
- Recent activity
- Any blockers

---

## Notes

- Read-only command (doesn't modify state)
- Quick overview for orientation
- Use `/piv:task:list` for detailed task view
