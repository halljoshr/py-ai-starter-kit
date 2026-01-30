---
name: task-complete
description: Mark a task as complete with verification.
argument-hint: "[task-id]"
allowed-tools: Read, Write, Bash
---

# PIV-Swarm: Task Complete

**Mark a task as complete with verification.**

---

## Usage

```
/task-complete task-003
```

---

## Process

### Step 1: Load Task

Read `.agents/tasks/{task-id}.yaml`

Verify task is in `in_progress` status.

### Step 2: Run Verification

Execute the task's verify command:

```bash
{verify command from task}
```

**If verification passes:** Continue to Step 3

**If verification fails:**
```markdown
## Verification Failed

**Command:** {verify}
**Output:**
{error output}

**Options:**
1. Fix and retry
2. Mark complete anyway (not recommended)
3. Cancel
```

### Step 3: Update Task Status

```yaml
status: completed
completed_at: "2026-01-26T10:45:00Z"
verification_output: "{output from verify command}"
actual_tokens: {estimate}
```

### Step 4: Update Session State

```yaml
tasks:
  in_progress: 0  # Decrement
  completed: 3  # Increment
  ids:
    in_progress: []
    completed: ["task-001", "task-002", "task-003"]
```

### Step 5: Check Unblocked Tasks

Find tasks that were blocked by this one:

```markdown
## Unblocked Tasks

The following tasks are now ready:
- task-004: Create Login endpoint
- task-005: Add integration tests
```

### Step 6: Update STATE.md

Move task to completed section:

```markdown
### Completed
- [x] task-001: Create User model
- [x] task-002: Create User repository
- [x] task-003: Create Auth service  <-- NEW

### Pending (Ready)
- [ ] task-004: Create Login endpoint  <-- Now ready
```

### Step 7: Display Confirmation

```markdown
## Task Completed: task-003

**Name:** Create Auth service
**Duration:** 15 minutes
**Verification:** PASSED

### Unblocked
- task-004: Create Login endpoint

### Progress
Completed: 3/5 tasks (60%)
[████████████░░░░░░░░]
```

---

## Notes

- Always runs verification before marking complete
- Automatically unblocks dependent tasks
- Updates all state files
- Commit changes separately with git
