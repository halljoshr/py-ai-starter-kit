# PIV-Swarm: Task Create Command

**Create a new task.**

---

## Usage

```bash
/piv:task:create "{task-name}"
```

Example:
```bash
/piv:task:create "Add password reset endpoint"
```

---

## Process

### Step 1: Generate Task ID

```bash
# Find next available ID
ls .agents/tasks/
# task-001.yaml, task-002.yaml, task-003.yaml
# Next: task-004
```

### Step 2: Gather Task Details

Ask for required information:

```markdown
## New Task: Add password reset endpoint

**Files affected:**
> (list files this task will create/modify)

**Action description:**
> (what should be done)

**Verification command:**
> (command to verify completion)

**Done criteria:**
> (how to know it's complete)

**Priority:** [critical/high/medium/low]
>

**Blocked by:** (task IDs, or none)
>
```

### Step 3: Create Task File

```yaml
# .agents/tasks/task-004.yaml
id: "task-004"
name: "Add password reset endpoint"
status: pending
owner: null
phase: implementation
priority: medium

files:
  - "src/api/auth/reset.py"
  - "tests/unit/test_reset.py"

action: |
  Create POST /auth/reset-password endpoint that:
  1. Accepts email address
  2. Generates reset token
  3. Sends reset email
  4. Returns success message

verify: "uv run pytest tests/unit/test_reset.py -v"
done: "POST /auth/reset-password sends reset email and returns 200"

blocked_by: []
blocks: []

created_at: "2026-01-26T11:00:00Z"
started_at: null
completed_at: null
estimated_tokens: 12000
actual_tokens: null
notes: null
verification_output: null
```

### Step 4: Update Session State

```yaml
# Update .agents/state/session.yaml
tasks:
  total: 4  # Increment
  pending: 2  # Increment
  ids:
    pending:
      - "task-003"
      - "task-004"  # Add new
```

### Step 5: Display Confirmation

```markdown
## Task Created

| Field | Value |
|-------|-------|
| ID | task-004 |
| Name | Add password reset endpoint |
| Status | pending |
| Priority | medium |
| Est. Tokens | 12K |

Task added to queue.
```

---

## Quick Create

For simple tasks, provide inline:

```bash
/piv:task:create "Fix login error" --files "src/api/auth/login.py" --priority high
```

---

## Output

1. New task file in `.agents/tasks/`
2. Updated session.yaml
3. Confirmation displayed
