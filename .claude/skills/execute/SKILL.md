---
name: execute
description: Execute tasks with fresh context per task. Runs validation commands AND skills.
disable-model-invocation: true
context: fork
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, Skill
---

# PIV-Swarm: Execute

**Execute tasks with fresh context per task. Automatically runs validation and quality gates.**

**Philosophy:** "Fresh context, clean execution" - Each task gets full attention with comprehensive validation.

---

## Process

### Step 1: Startup Ritual

Every execution session begins with:
1. Read `.agents/specs/{feature}-spec.txt` (understand context)
2. Read `.agents/state/session.yaml` (current progress)
3. `git status && git log -3` (understand state)
4. `uv run pytest tests/unit/ -v --tb=short` (baseline validation)

Never start executing without startup ritual.

### Step 2: Find Next Task

Identify next executable task:
1. Status is `pending`
2. All `blocked_by` tasks are `completed` with `test_results.status: pass`
3. Highest priority among available

If no tasks available:
- Check for blockers (failed tests on dependencies)
- Check if all tasks complete
- Display status and exit

### Step 3: Load Task

Read task file: `.agents/tasks/{task-id}.yaml`

Display:
```markdown
## Executing: task-003

**Name:** Implement ingestion service
**Phase:** services
**Priority:** high
**Duration:** ~25K tokens
**TDD:** true

**Files to Create:**
- src/services/ingestion.py
- tests/unit/services/test_ingestion.py

**Actions:**
1. Write unit tests with mocked database
2. Implement single event insert method
3. Implement bulk insert with executemany()
4. Add error handling for duplicates
5. Add transaction management

**Patterns:**
- .claude/reference/fastapi-best-practices.md
- .claude/reference/error-handling-patterns.md

**Validation:**
Commands:
  - uv run pytest tests/unit/services/test_ingestion.py -v
  - mypy src/services/ingestion.py
  - ruff check src/services/ingestion.py

Skills:
  - code-review (when: code_written)
  - validate (when: always)
```

### Step 4: Update Task Status

Update task file:
```yaml
status: in_progress
owner: main
started_at: "2026-01-27T18:45:00Z"
```

Update session state:
```yaml
tasks:
  in_progress: 1
  current_task: "task-003"
```

### Step 5: Read Pattern References

Read all files in `patterns` section:
```bash
cat .claude/reference/fastapi-best-practices.md
cat .claude/reference/error-handling-patterns.md
```

Understand conventions before implementing.

### Step 6: Execute Task Actions

**Follow the task's actions exactly, in order.**

For TDD tasks:
1. Write tests first (action 1)
2. Run tests (should fail)
3. Implement code (actions 2-N)
4. Run tests (should pass)

For non-TDD tasks:
1. Implement according to actions
2. Write code following patterns
3. Add docstrings and type hints

### Step 7: Run Validation Commands

**Execute each command in `validation.commands`:**

For each command:
1. Capture start time
2. Run command via Bash tool
3. Capture exit code, output, duration
4. Record passed = (exit_code == 0)

Example:
```yaml
command_results:
  - command: uv run pytest tests/unit/services/test_ingestion.py -v
    exit_code: 0
    duration_seconds: 1.23
    output: |
      ===== test session starts =====
      tests/unit/services/test_ingestion.py::test_insert_event PASSED
      tests/unit/services/test_ingestion.py::test_bulk_insert PASSED
      ===== 2 passed in 1.23s =====
    passed: true

  - command: mypy src/services/ingestion.py
    exit_code: 0
    duration_seconds: 0.45
    output: "Success: no issues found in 1 source file"
    passed: true

  - command: ruff check src/services/ingestion.py
    exit_code: 0
    duration_seconds: 0.12
    output: "All checks passed!"
    passed: true
```

**If any command fails:**
- Analyze error output
- Fix the issue
- Re-run validation
- Max 3 attempts before marking task failed

### Step 8: Invoke Validation Skills

**For each skill in `validation.skills`:**

Check `when` condition:
- `always` → Always run
- `code_written` → Run if `files.create` or `files.modify` not empty
- `tests_written` → Run if any test files in `files`
- `api_created` → Run if `endpoints` not empty

If condition met, invoke skill:
```bash
# Example: /code-review for code written
Skill tool: code-review {args}
```

Capture results:
```yaml
skill_results:
  - skill: code-review
    invoked_at: "2026-01-27T18:50:00Z"
    passed: true
    summary: "0 critical, 0 high, 2 medium, 1 low issues found"
    issues_found:
      critical: 0
      high: 0
      medium: 2
      low: 1
    details: |
      ## Code Review: ingestion.py

      ### Medium Issues
      - Line 45: Consider adding retry logic for database errors
      - Line 67: Magic number 1000 should be a constant

      ### Low Issues
      - Line 23: Docstring could be more detailed

  - skill: validate
    invoked_at: "2026-01-27T18:52:00Z"
    passed: true
    summary: "All validation stages passed"
    issues_found:
      critical: 0
      high: 0
      medium: 0
      low: 0
    details: |
      Stage 1: Static Analysis - PASS
      Stage 2: Unit Tests - PASS (2 tests, 100% coverage)
      Stage 3: Type Checking - PASS
      Stage 4: Coverage - PASS (85%)
```

**Passing criteria for skills:**
- `validate`: All stages pass
- `code-review`: 0 critical, 0 high issues
- `code-review-since`: 0 critical, 0 high issues

### Step 9: Evaluate Overall Result

Determine if task passes:

```python
overall_passed = (
    all(cmd.passed for cmd in command_results) AND
    all(skill.passed for skill in skill_results)
)
```

Update task file:
```yaml
test_results:
  status: pass  # or fail
  last_run: "2026-01-27T18:52:00Z"
  command_results: [...]  # From step 7
  skill_results: [...]    # From step 8
  overall_passed: true    # or false
  failure_reason: null    # or "pytest failed: 2 tests failing"
```

### Step 10: Handle Pass/Fail

**If overall_passed = true:**
- Continue to Step 11 (commit)

**If overall_passed = false:**
- Analyze failure_reason
- Fix issues
- Re-run validation (back to Step 7)
- Max 3 attempts
- If still failing after 3 attempts:
  - Mark task status: `failed`
  - Add note with details
  - Move to next task

### Step 11: Commit Changes

**Only if overall_passed = true:**

Create atomic commit:
```bash
git add {files from task}
git commit -m "feat({phase}): {task name}

{Brief description of what was implemented}

Task: {task-id}
Validation: All tests passing
Coverage: {coverage}%

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 12: Update Task to Completed

```yaml
status: completed
completed_at: "2026-01-27T18:53:00Z"
actual_tokens: 24500
```

### Step 13: Unblock Dependent Tasks

Find tasks with `blocked_by: [current-task-id]`:
- Check if all their blockers are now complete
- If yes, they become available for next execution

### Step 14: Update Session State

```yaml
tasks:
  completed: 3
  in_progress: 0
  pending: 17
  ids:
    completed: ["task-001", "task-002", "task-003"]
    pending: ["task-004", ...]

tokens:
  used: 65000
```

### Step 15: Update STATE.md

```markdown
### Completed (3)
- [x] task-001: Setup project structure ✓
- [x] task-002: Database connection ✓
- [x] task-003: Implement ingestion service ✓ (0 critical, 2 medium issues)

### Pending (Ready - 2)
- [ ] task-004: Implement query service (ready, high priority)
- [ ] task-005: Create API endpoints (ready, high priority)

### Pending (Blocked - 15)
- [ ] task-006: ... (blocked by task-004)
```

### Step 16: Check Token Budget

Calculate tokens used this session:
- Read from session.yaml: `tokens.used`
- Add estimated tokens for this task

**Decision:**
- < 150K (75%): Continue to next task (Step 2)
- 150-175K (75-88%): ⚠️ Warning, suggest checkpoint after current task
- > 175K (88%): 🚨 Checkpoint required, run `/pause`

### Step 17: Loop or Complete

**Continue if:**
- Tokens < 150K AND
- Tasks remaining AND
- No unresolved blockers

**Checkpoint if:**
- Tokens >= 150K OR
- User requests it

**Complete if:**
- All tasks completed OR
- All remaining tasks blocked

---

## Checkpoint Process

When token budget exceeded:

1. Display checkpoint summary
2. Update all state files
3. Commit any pending changes
4. Display resume instructions

```markdown
## Checkpoint

**Session Summary:**
- Tasks completed: 8/20
- Tokens used: 156K / 200K (78%)
- Next task: task-009

**Quality Metrics:**
- All completed tasks: PASSING ✓
- Test coverage: 85% average
- Code review: 0 critical issues

**To Resume:**
```bash
# New conversation, fresh context
cd /path/to/project
/resume
```

**Next task will be:** task-009 (Create aggregation service)
```

---

## Error Handling

### Validation Command Fails

1. Analyze error output
2. Determine root cause
3. Fix issue
4. Re-run validation.commands
5. If fixed, continue
6. If not fixed after 3 attempts:
   - Mark task `failed`
   - Capture detailed error in `test_results.failure_reason`
   - Move to next task

### Validation Skill Fails

1. Read skill output in `skill_results.details`
2. Address critical/high issues
3. Re-run validation.skills
4. If fixed, continue
5. If not fixed after 3 attempts:
   - Mark task `failed`
   - Capture details
   - Move to next task

### Blocker Detected

If no tasks are available (all blocked):
1. Identify which tasks are blocking
2. Check their test_results
3. Display blocker report
4. Exit (human intervention needed)

---

## Completion Criteria

Execution session complete when:
- [ ] All tasks completed with `test_results.status: pass`, OR
- [ ] Token budget exceeded (checkpoint created), OR
- [ ] Unresolved blocker encountered

---

## Task Status Transitions

```
pending → in_progress → completed (if overall_passed = true)
pending → in_progress → failed (if validation fails 3x)
pending → blocked (if dependency fails)
```

---

## Example Task Execution Output

```markdown
## Task Complete: task-003

**Status:** ✓ PASSED
**Duration:** 24,500 tokens
**Time:** 15 minutes

### Validation Results

**Commands:** 3/3 passed
  ✓ pytest (2 tests, 1.23s)
  ✓ mypy (0 issues)
  ✓ ruff (clean)

**Skills:** 2/2 passed
  ✓ code-review (0 critical, 0 high, 2 medium, 1 low)
  ✓ validate (all stages passed, 85% coverage)

### Files Modified
- src/services/ingestion.py (+180 lines)
- tests/unit/services/test_ingestion.py (+95 lines)

### Git Commit
- Commit: abc1234
- Message: "feat(services): Implement ingestion service"

### Next Task
- task-004: Implement query service (ready)
```

---

## Remember

**Validation is NOT optional:**
- Every task MUST run validation.commands
- Every task with code SHOULD run validation.skills
- Tasks only marked `completed` if `overall_passed = true`
- This ensures quality at every step

**Fresh context per task:**
- Each task execution can run in fresh session (context: fork)
- Task file has ALL context needed
- No dependency on conversation history
- Perfect for multi-session work

**Quality over speed:**
- Don't skip validation to save tokens
- Fix issues immediately, don't accumulate debt
- Code review catches issues early
- Test results prove correctness
