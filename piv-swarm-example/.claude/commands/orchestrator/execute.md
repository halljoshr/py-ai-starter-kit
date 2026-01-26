# PIV-Swarm: Execute Command

**Execute tasks with fresh context per task.**

---

## Purpose

The Execute command runs tasks from the plan, ensuring:
- Fresh context for each task (prevents context rot)
- Verification after each task
- Atomic commits per task
- State persistence for resume

**Philosophy:** "Fresh context, clean execution" - Each task gets full attention.

---

## Process

### Step 1: Load State

```yaml
# Read from .agents/state/session.yaml
- current phase
- task list and status
- any blockers
```

### Step 2: Update State

```yaml
# Update .agents/state/session.yaml
session:
  phase: execute
```

### Step 3: Find Next Task

Identify next executable task:
1. Status is `pending`
2. All `blocked_by` tasks are `completed`
3. Highest priority among available

```yaml
# Update session.yaml
tasks:
  current_task: "task-001"
  next_task: "task-002"  # (or null if task-001 blocks others)
```

### Step 4: Load Task

Read task file: `.agents/tasks/{task-id}.yaml`

Display task details:
```markdown
## Executing: task-001

**Name:** Create User model
**Priority:** high
**Files:** src/models/user.py, tests/unit/test_user_model.py
**Blocked by:** (none)
**Blocks:** task-002, task-003

**Action:**
Create User Pydantic model with fields...

**Verify:** uv run pytest tests/unit/test_user_model.py -v
**Done:** User model validates email format and stores hashed passwords
```

### Step 5: Update Task Status

```yaml
# Update .agents/tasks/task-001.yaml
status: in_progress
owner: main
started_at: "2026-01-26T10:00:00Z"
```

### Step 6: Log Task Start

```yaml
# .agents/state/messages.yaml
- from: main
  to: orchestrator
  type: task_started
  content: "Starting task-001: Create User model"
  task_id: "task-001"
```

### Step 7: Execute Task

**Follow the task's action description exactly.**

For code tasks:
1. Read referenced pattern files
2. Implement according to action
3. Write tests if specified
4. Run verify command

### Step 8: Verify Task

Run the task's verify command:
```bash
# Example
uv run pytest tests/unit/test_user_model.py -v
```

**If verification passes:**
- Continue to Step 9

**If verification fails:**
- Debug and fix
- Re-run verification
- If stuck after 3 attempts, mark as blocked and move on

### Step 9: Commit Changes

Create atomic commit for this task:
```bash
git add {files from task}
git commit -m "feat(models): Create User model

- Add User Pydantic model with email validation
- Add password hashing support
- Add unit tests

Task: task-001

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 10: Update Task Status

```yaml
# Update .agents/tasks/task-001.yaml
status: completed
completed_at: "2026-01-26T10:15:00Z"
actual_tokens: 12000
verification_output: "5 passed in 0.42s"
```

### Step 11: Log Task Completion

```yaml
# .agents/state/messages.yaml
- from: main
  to: orchestrator
  type: task_completed
  content: "Completed task-001: Create User model"
  task_id: "task-001"
  metadata:
    tokens_used: 12000
    files_modified:
      - "src/models/user.py"
      - "tests/unit/test_user_model.py"
    commit_sha: "abc1234"
```

### Step 12: Update Session State

```yaml
# .agents/state/session.yaml
tasks:
  completed: 1
  pending: 4
  ids:
    completed: ["task-001"]
    pending: ["task-002", "task-003", "task-004", "task-005"]
```

### Step 13: Update STATE.md

```markdown
## Tasks

### Completed
- [x] task-001: Create User model ✓

### In Progress
(none)

### Pending
- [ ] task-002: Create User repository (ready)
- [ ] task-003: Create Auth service (ready)
- [ ] task-004: Create Login endpoint (blocked)
- [ ] task-005: Add integration tests (blocked)
```

### Step 14: Check Token Budget

```yaml
# Check tokens used
tokens:
  used: 12000
  budget: 200000
```

**If under 75% (150K):** Continue to next task
**If over 75%:** Warn and suggest checkpoint
**If over 88% (175K):** Force checkpoint (see Step 15)

### Step 15: Checkpoint (if needed)

If token budget exceeded or session ending:

1. Update all state files
2. Commit any pending changes
3. Log checkpoint message
4. Display resume instructions:

```markdown
## Checkpoint

**Tasks Completed:** 3/5
**Tokens Used:** 156K
**Next Task:** task-004

### To Resume

In a new conversation:
```bash
/piv:resume
```

The session will continue from task-004.
```

### Step 16: Loop

Repeat Steps 3-15 until:
- All tasks completed, OR
- Token budget exceeded, OR
- Blocker encountered

---

## Error Handling

### Verification Fails

1. Analyze error output
2. Fix the issue
3. Re-run verification
4. If fails 3 times:
   - Mark task as `failed`
   - Log blocker
   - Move to next task (if any)

### Unexpected Error

1. Log error details
2. Save current state
3. Create checkpoint
4. Ask user for guidance

---

## Output

After each task:
- Updated task file (status, tokens, verification)
- Git commit with changes
- Updated session state
- Updated STATE.md
- Message logged

After all tasks or checkpoint:
- Summary of completed tasks
- Resume instructions if incomplete

---

## Completion Criteria

Session complete when:
- [ ] All tasks completed, OR
- [ ] Token budget exceeded (checkpoint created), OR
- [ ] Unresolved blocker (user intervention needed)

---

## Next Command

After Execute completes all tasks:
- `/piv:validate` - Final verification

After checkpoint:
- `/piv:resume` - Continue execution

---

## Token Budget

**Per task:** 10-30K tokens (varies by complexity)
**Session total:** 150K soft limit, 175K hard limit
**Checkpoint:** Automatic at 175K

---

## Single-Agent vs Swarm

| Mode | Behavior |
|------|----------|
| Single | Main agent executes tasks sequentially |
| Swarm | Spawn executor agents for parallel execution |

Current mode: **Single Agent**

### Future Swarm Mode

```
/piv:execute --parallel

Spawns:
- executor-1: task-002
- executor-2: task-003
(Both unblocked after task-001)

Orchestrator monitors progress, handles completions.
```
