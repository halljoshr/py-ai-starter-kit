# PIV-Swarm: Assign Command

**Assign a task to an agent.**

---

## Usage

```bash
/piv:assign {task-id} {agent-id}
```

Example:
```bash
/piv:assign task-003 main
/piv:assign task-004 executor-1  # Future swarm mode
```

---

## Process

### Step 1: Validate Task

```yaml
# Read .agents/tasks/{task-id}.yaml
# Verify:
# - Task exists
# - Status is pending or assigned
# - Not blocked by incomplete tasks
```

### Step 2: Validate Agent

```yaml
# Read .agents/state/agents.yaml
# Verify:
# - Agent exists
# - Agent is idle or can take more tasks
```

### Step 3: Check Dependencies

```yaml
# Verify blocked_by tasks are completed
blocked_by:
  - task-001  # Must be completed
  - task-002  # Must be completed
```

**If blocked:**
```markdown
⚠️ Cannot assign task-003

Blocked by incomplete tasks:
- task-001: pending
- task-002: pending

Complete blocking tasks first.
```

### Step 4: Update Task

```yaml
# Update .agents/tasks/{task-id}.yaml
status: assigned
owner: "{agent-id}"
```

### Step 5: Update Agent

```yaml
# Update .agents/state/agents.yaml
agents:
  - id: "{agent-id}"
    current_task: "{task-id}"
    status: active
```

### Step 6: Log Assignment

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: "{agent-id}"
  type: task_assignment
  content: "Assigned task-003: Create Auth service"
  task_id: "task-003"
```

### Step 7: Display Confirmation

```markdown
## Task Assigned

| Field | Value |
|-------|-------|
| Task | task-003: Create Auth service |
| Agent | main |
| Status | assigned |

Agent main can now work on this task.
```

---

## Single-Agent Mode

In single-agent mode, assignment is automatic:
- Only agent is `main`
- `/piv:execute` auto-assigns to main

Manual assignment rarely needed.

---

## Future Swarm Mode

With multiple agents:
```bash
# Assign to specific executor
/piv:assign task-003 executor-1
/piv:assign task-004 executor-2

# Auto-assign to any available
/piv:assign task-003 auto
```

---

## Output

1. Updated task file (owner, status)
2. Updated agent registry
3. Message logged
4. Confirmation displayed
