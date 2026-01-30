---
name: task-create
description: Create a new task in the current PIV session.
argument-hint: "[task-name]"
allowed-tools: Read, Write, Glob
---

# PIV-Swarm: Task Create

**Create a new task.**

---

## Usage

```
/task-create "Add password reset endpoint"
```

---

## Process

### Step 1: Generate Task ID

Find next available ID by checking `.agents/tasks/`:
```
task-001.yaml exists
task-002.yaml exists
Next: task-003
```

### Step 2: Gather Task Details

Ask for required information:

```markdown
## New Task: $ARGUMENTS

**Files affected:**
> (list files this task will create/modify)

**Action description:**
> (what should be done)

**Verification command:**
> (command to verify completion)

**Done criteria:**
> (how to know it's complete)

**Priority:** [critical/high/medium/low]

**Blocked by:** (task IDs, or none)
```

### Step 3: Create Task File

Create `.agents/tasks/task-{NNN}.yaml`:

```yaml
id: "task-003"
name: "$ARGUMENTS"
status: pending
owner: null
priority: medium

files:
  - "src/api/auth/reset.py"
  - "tests/unit/test_reset.py"

action: |
  (action description from user)

verify: "uv run pytest tests/unit/test_reset.py -v"
done: "(done criteria from user)"

blocked_by: []
blocks: []

created_at: "(current timestamp)"
estimated_tokens: 12000
```

### Step 4: Update Session State

Update `.agents/state/session.yaml`:
```yaml
tasks:
  total: 4  # Increment
  pending: 3  # Increment
  ids:
    pending:
      - "task-001"
      - "task-002"
      - "task-003"  # Add new
```

### Step 5: Display Confirmation

```markdown
## Task Created

| Field | Value |
|-------|-------|
| ID | task-003 |
| Name | $ARGUMENTS |
| Status | pending |
| Priority | medium |

Task added to queue.
```

---

## Quick Create

For simple tasks with inline details:

```
/task-create "Fix login error" --files "src/api/auth/login.py" --priority high
```

---

## Notes

- Tasks are stored as individual YAML files
- Each task must have verify and done criteria
- Dependencies can be added later with `/task-update`
