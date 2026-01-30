---
name: task-update
description: Update a task's details, status, or dependencies.
argument-hint: "[task-id]"
allowed-tools: Read, Write
---

# PIV-Swarm: Task Update

**Update a task's details, status, or dependencies.**

---

## Usage

```
/task-update task-003
/task-update task-003 --status in_progress
/task-update task-003 --priority critical
```

---

## Process

### Step 1: Load Task

Read `.agents/tasks/{task-id}.yaml`

Display current state:
```markdown
## Task: task-003

| Field | Current Value |
|-------|---------------|
| Name | Create Auth service |
| Status | pending |
| Priority | high |
| Owner | (none) |
| Blocked By | task-001 |

**What would you like to update?**
```

### Step 2: Apply Updates

Update the specified fields:

**Status transitions:**
- `pending` → `in_progress` (sets owner, started_at)
- `in_progress` → `completed` (sets completed_at)
- `in_progress` → `failed` (sets failed_at, notes)
- `in_progress` → `blocked` (sets blocker info)

**Other fields:**
- `priority`: critical, high, medium, low
- `blocked_by`: add/remove task IDs
- `blocks`: add/remove task IDs
- `action`: update description
- `verify`: update verification command
- `notes`: add notes

### Step 3: Update Task File

Write changes to `.agents/tasks/{task-id}.yaml`

### Step 4: Update Session State

If status changed, update `.agents/state/session.yaml`:
```yaml
tasks:
  pending: 2  # Decrement
  in_progress: 1  # Increment
  ids:
    pending: ["task-004", "task-005"]
    in_progress: ["task-003"]
```

### Step 5: Display Confirmation

```markdown
## Task Updated: task-003

| Field | Old | New |
|-------|-----|-----|
| Status | pending | in_progress |
| Owner | (none) | main |
| Started | - | 10:35 |

Task is now in progress.
```

---

## Quick Updates

```
/task-update task-003 --status completed
/task-update task-003 --add-blocked-by task-002
/task-update task-003 --notes "Waiting for API key"
```

---

## Notes

- Status changes are logged in history
- Completing a task unblocks dependent tasks
- Use `/task-complete` for full completion workflow
