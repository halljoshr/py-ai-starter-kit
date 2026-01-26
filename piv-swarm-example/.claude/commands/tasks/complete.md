# PIV-Swarm: Task Complete Command

**Mark a task as completed with verification.**

---

## Usage

```bash
/piv:task:complete {task-id}
```

Example:
```bash
/piv:task:complete task-003
```

---

## Process

### Step 1: Load Task

```yaml
# Read .agents/tasks/{task-id}.yaml
id: task-003
name: Create Auth service
status: in_progress
verify: "uv run pytest tests/unit/test_auth_service.py -v"
done: "Auth service generates valid JWT tokens"
```

### Step 2: Run Verification

Execute the task's verify command:

```bash
uv run pytest tests/unit/test_auth_service.py -v
```

**Capture output for task record.**

### Step 3: Check Verification Result

**If passes:**
```markdown
## Verification Passed ✓

```
tests/unit/test_auth_service.py::test_token_generation PASSED
tests/unit/test_auth_service.py::test_token_validation PASSED
tests/unit/test_auth_service.py::test_refresh_token PASSED

3 passed in 0.42s
```

Proceeding to mark complete...
```

**If fails:**
```markdown
## Verification Failed ✗

```
tests/unit/test_auth_service.py::test_token_generation FAILED

E   AssertionError: Expected token to contain user_id
```

Options:
1. Fix the issue and try again
2. Mark as failed
3. Cancel completion

Your choice?
```

### Step 4: Update Task

```yaml
# Update .agents/tasks/{task-id}.yaml
status: completed
completed_at: "2026-01-26T10:30:00Z"
actual_tokens: 15000
verification_output: |
  3 passed in 0.42s
```

### Step 5: Create Commit

```bash
git add {task files}
git commit -m "feat(auth): Create Auth service

- Implement JWT token generation
- Add token validation
- Add refresh token support
- Add unit tests

Task: task-003
Verify: 3 tests passed

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 6: Update Session State

```yaml
# Update .agents/state/session.yaml
tasks:
  completed: 3  # Increment
  in_progress: 0  # Decrement
  ids:
    completed:
      - task-001
      - task-002
      - task-003  # Add
```

### Step 7: Check for Unblocked Tasks

```yaml
# Check if any tasks were blocked by this one
# task-004 blocked_by: [task-003]
# task-003 now complete → task-004 unblocked
```

```markdown
## Tasks Unblocked

The following tasks are now ready:
- task-004: Create Login endpoint
```

### Step 8: Log Completion

```yaml
# .agents/state/messages.yaml
- from: main
  to: orchestrator
  type: task_completed
  content: "Completed task-003: Create Auth service"
  task_id: "task-003"
  metadata:
    tokens_used: 15000
    verification_output: "3 passed in 0.42s"
    commit_sha: "def5678"
```

### Step 9: Display Summary

```markdown
═══════════════════════════════════════════════════════════════
                    TASK COMPLETED
═══════════════════════════════════════════════════════════════

## task-003: Create Auth service

| Field | Value |
|-------|-------|
| Status | ✓ Completed |
| Verification | 3 tests passed |
| Tokens | 15K |
| Commit | def5678 |

## Progress

```
Completed: 3 / 5 [████████████░░░░░░░░] 60%
```

## Next Task

**task-004:** Create Login endpoint
- Status: pending (was blocked, now ready)
- Priority: high

Continue with `/piv:execute` or `/piv:task:complete task-004` after implementing.

═══════════════════════════════════════════════════════════════
```

---

## Skip Verification

For manual verification (not recommended):

```bash
/piv:task:complete task-003 --skip-verify
```

Will prompt for confirmation.

---

## Output

1. Verification run
2. Task file updated
3. Git commit created
4. Session state updated
5. Blocked tasks unblocked
6. Message logged
7. Summary displayed
