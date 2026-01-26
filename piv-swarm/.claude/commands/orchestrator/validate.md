# PIV-Swarm: Validate Command

**Final verification that all tasks complete and feature works.**

---

## Purpose

The Validate command performs comprehensive verification:
- All tasks completed
- All tests passing
- Code quality checks pass
- Feature requirements met

**Philosophy:** "Trust but verify" - Systematic confirmation before completion.

---

## Process

### Step 1: Load State

```yaml
# Read from .agents/state/session.yaml
- feature name
- task list and status
- decisions from discuss phase
```

### Step 2: Update State

```yaml
# Update .agents/state/session.yaml
session:
  phase: validate
```

### Step 3: Task Completion Check

Verify all tasks completed:

```yaml
# Check .agents/state/session.yaml
tasks:
  total: 5
  completed: 5  # Must equal total
  failed: 0     # Must be zero
  blocked: 0    # Must be zero
```

**If incomplete tasks exist:**
- List incomplete tasks
- Ask user to resolve or skip

### Step 4: Run All Verifications

Execute verify command for each task:

```bash
# For each task in .agents/tasks/*.yaml
# Run the verify command

# task-001
uv run pytest tests/unit/test_user_model.py -v

# task-002
uv run pytest tests/unit/test_user_repository.py -v

# ... etc
```

**Track results:**
```markdown
## Verification Results

| Task | Verify Command | Result |
|------|----------------|--------|
| task-001 | pytest test_user_model.py | ✓ PASS |
| task-002 | pytest test_user_repository.py | ✓ PASS |
| task-003 | pytest test_auth_service.py | ✓ PASS |
| task-004 | pytest test_login_endpoint.py | ✓ PASS |
| task-005 | pytest tests/integration/ | ✓ PASS |
```

### Step 5: Code Quality Checks

Run standard quality gates:

**Stage 1: Linting**
```bash
uv run ruff check app/ src/ tests/
```

**Stage 2: Type Checking**
```bash
uv run mypy app/ src/
```

**Stage 3: All Tests**
```bash
uv run pytest tests/unit/ tests/integration/ -v
```

**Stage 4: Coverage**
```bash
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80
```

### Step 6: Feature Requirements Check

Review decisions from discuss phase:

```markdown
## Requirements Verification

| # | Requirement | Status |
|---|-------------|--------|
| 1 | JWT authentication | ✓ Implemented |
| 2 | 15min access token | ✓ Configured |
| 3 | 7 day refresh token | ✓ Configured |
| 4 | Email validation | ✓ Implemented |
| 5 | Password hashing | ✓ Implemented |
```

### Step 7: Generate Validation Report

```markdown
# Validation Report: {feature-name}

**Date:** 2026-01-26
**Status:** ✓ PASSED

## Task Verification

| Task | Status |
|------|--------|
| task-001 | ✓ PASS |
| task-002 | ✓ PASS |
| task-003 | ✓ PASS |
| task-004 | ✓ PASS |
| task-005 | ✓ PASS |

## Quality Gates

| Gate | Status |
|------|--------|
| Linting | ✓ 0 errors |
| Type Check | ✓ 0 errors |
| Unit Tests | ✓ 47 passed |
| Integration | ✓ 12 passed |
| Coverage | ✓ 87% (threshold: 80%) |

## Requirements

All 5 requirements verified.

## Summary

Feature ready for deployment.

## Git Status

- Branch: feature/user-auth
- Commits: 5 (one per task)
- Files changed: 12
```

### Step 8: Update State

```yaml
# .agents/state/session.yaml
session:
  phase: validate
  status: completed

# If validation passed
validation:
  status: passed
  completed_at: "2026-01-26T11:00:00Z"
  report: ".agents/execution-reports/{feature}-validation.md"
```

### Step 9: Update STATE.md

```markdown
## Status: VALIDATED ✓

All tasks completed and verified.
All quality gates passed.
Feature ready for deployment.
```

### Step 10: Log Completion

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: status_update
  content: |
    Validation complete for: user-authentication
    Status: PASSED
    All 5 tasks verified.
    All quality gates passed.
    Feature ready for deployment.
```

---

## Handling Failures

### Task Verification Fails

```markdown
## Verification Failed: task-003

**Command:** uv run pytest tests/unit/test_auth_service.py -v
**Output:**
```
FAILED test_auth_service.py::test_token_generation - AssertionError
```

**Options:**
1. Fix the issue and re-run validation
2. Mark as known issue and proceed
3. Revert to checkpoint

**Your choice?**
```

### Quality Gate Fails

```markdown
## Quality Gate Failed: Coverage

**Result:** 72% (threshold: 80%)

**Missing Coverage:**
- src/api/auth/login.py: lines 45-52
- src/services/auth.py: lines 78-85

**Options:**
1. Add tests for missing coverage
2. Lower threshold temporarily
3. Proceed with warning

**Your choice?**
```

---

## Output

1. Validation report in `.agents/execution-reports/`
2. Updated session state
3. Updated STATE.md
4. Completion message

---

## Completion Criteria

Validation passes when:
- [ ] All tasks verified (verify commands pass)
- [ ] Linting passes (0 errors)
- [ ] Type checking passes (0 errors)
- [ ] All tests pass
- [ ] Coverage meets threshold (80%+)
- [ ] All requirements verified

---

## Next Steps

After successful validation:
- Merge to target branch
- Create PR if needed
- Clean up feature branch

---

## Token Budget

**Target:** 10-20K tokens
**Note:** Mostly running commands, not generating code

---

## Single-Agent vs Swarm

| Mode | Behavior |
|------|----------|
| Single | Main agent runs all verifications |
| Swarm | Could spawn reviewer agent for parallel checks |

Current mode: **Single Agent**
