# PIV-Swarm: Task Update Command

**Update a task's status or details.**

---

## Usage

```bash
/piv:task:update {task-id} --status {status}
/piv:task:update {task-id} --priority {priority}
/piv:task:update {task-id} --notes "{notes}"
```

Examples:
```bash
/piv:task:update task-003 --status in_progress
/piv:task:update task-003 --priority critical
/piv:task:update task-003 --notes "Blocked on API key"
```

---

## Valid Status Transitions

```
pending → assigned → in_progress → completed
                  ↘            ↗
                    → blocked →
                  ↘            ↗
                    → failed  →
```

| From | Can Go To |
|------|-----------|
| pending | assigned, in_progress |
| assigned | in_progress, pending |
| in_progress | completed, blocked, failed |
| blocked | in_progress |
| failed | in_progress |
| completed | in_progress (reopen) |

---

## Process

### Step 1: Load Task

```yaml
# Read .agents/tasks/{task-id}.yaml
```

### Step 2: Validate Transition

Check if status transition is valid.

### Step 3: Update Task

```yaml
# Update .agents/tasks/{task-id}.yaml
status: "{new-status}"

# Add timestamps as appropriate
started_at: "2026-01-26T10:00:00Z"  # When in_progress
completed_at: "2026-01-26T10:30:00Z"  # When completed
```

### Step 4: Update Session State

```yaml
# Update .agents/state/session.yaml
tasks:
  in_progress: 1  # Adjust counts
  pending: 2
```

### Step 5: Log Change

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: status_update
  content: "Task task-003 status changed: pending → in_progress"
  task_id: "task-003"
```

### Step 6: Display Confirmation

```markdown
## Task Updated

| Field | Old | New |
|-------|-----|-----|
| Status | pending | in_progress |

Task task-003 is now in progress.
```

---

## Updating Notes

Add context or blockers:

```bash
/piv:task:update task-003 --notes "Waiting for API credentials from DevOps"
```

---

## Batch Update

Update multiple tasks:

```bash
/piv:task:update task-001,task-002 --status completed
```

---

## Output

1. Updated task file
2. Updated session state
3. Message logged
4. Confirmation displayed
