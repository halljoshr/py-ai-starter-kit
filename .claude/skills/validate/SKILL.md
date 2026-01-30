---
name: validate
description: Multi-stage validation with PIV-Swarm integration. Verifies tasks, quality gates, and feature completion.
disable-model-invocation: true
argument-hint: "[--quick|--full]"
allowed-tools: Read, Bash, Glob, Grep
---

# PIV-Swarm: Validate

**Final verification that all tasks complete and feature works.**

**Philosophy:** "Trust but verify" - Systematic confirmation with granular quality gates.

---

## Arguments

```
/validate           # Full PIV-Swarm validation (if session exists) or quality gates only
/validate --quick   # Quality gates only (skip state/tasks checking)
/validate --full    # Complete validation including e2e tests and security
```

---

## Process

### Mode Detection

**Auto-detect mode based on context:**
- If `.agents/state/session.yaml` exists → **PIV-Swarm Mode**
- If no session.yaml or `--quick` flag → **Standalone Mode**
- If `--full` flag → Add e2e tests and security checks

---

## PIV-Swarm Mode (Default when session.yaml exists)

### Step 1: Load State

Read from `.agents/state/session.yaml`:
- feature name
- task list and status
- decisions from discuss phase
- validation requirements

### Step 2: Update Phase

```yaml
session:
  phase: validate
  started_at: "2026-01-28T10:00:00Z"
```

### Step 3: Task Completion Check

Verify all tasks completed:

```yaml
tasks:
  total: 5
  completed: 5  # Must equal total
  failed: 0     # Must be zero
  blocked: 0    # Must be zero
```

**If incomplete tasks exist:**
- List incomplete tasks with status
- Ask user: "3 tasks incomplete. Fix now, skip, or abort?"

### Step 4: Task-Specific Verification

Execute verify command from each task file:

```bash
# Read each .agents/tasks/task-*.yaml
# Extract validation.commands section
# Run each command

# Example from task-001.yaml:
uv run pytest tests/unit/test_user_model.py -v
```

Track results:
```markdown
## Task Verification Results

| Task | Command | Result |
|------|---------|--------|
| task-001 | pytest tests/unit/test_user_model.py | ✓ PASS |
| task-002 | mypy src/user/ | ✓ PASS |
| task-003 | pytest tests/integration/test_api.py | ✗ FAIL |
```

**If task verification fails:**
- Show failure details
- Offer to re-run after fix
- Option to proceed with warning

---

## Quality Gates (All Modes)

**Comprehensive documentation:** All quality gates are documented in detail in `references/quality-gates-reference.md`, including common failures, troubleshooting, and best practices.

### Stage 1: Static Analysis (< 5 seconds)

**Linting:**
```bash
uv run ruff check .
```
**Pass criteria:** 0 errors

**Type Checking:**
```bash
uv run mypy src/ app/
```
**Pass criteria:** 0 errors

---

### Stage 2: Unit Tests (< 30 seconds)

```bash
uv run pytest tests/unit/ -v --tb=short
```

**Pass criteria:** 100% passing

---

### Stage 3: Integration Tests (< 2 minutes)

```bash
uv run pytest tests/integration/ -m "not very_slow" -v --tb=short
```

**Pass criteria:** 100% passing

---

### Stage 4: Coverage Analysis

```bash
# Run pytest with JSON coverage report
uv run pytest tests/unit/ tests/integration/ \
  --cov=app --cov=src \
  --cov-report=json:coverage.json \
  --cov-report=term-missing \
  --cov-fail-under=80
```

**Pass criteria:** Coverage >= 80%

**Detailed Analysis:**
```bash
# Use coverage script for detailed analysis of files below threshold
uv run python .claude/skills/validate/scripts/check_coverage.py coverage.json 80
```

This script provides:
- Per-file coverage breakdown
- Files below threshold with missing line ranges
- Actionable recommendations

**For troubleshooting:** See `references/quality-gates-reference.md` for detailed guidance on each stage.

---

### Stage 5: E2E Tests (--full only)

```bash
uv run pytest tests/e2e/ -v --tb=short
```

**Pass criteria:** 100% passing

---

### Stage 6: Security Checks (--full only)

```bash
uv run bandit -r src/ app/ -ll
```

**Pass criteria:** No medium/high severity issues

---

## PIV-Swarm Mode: Additional Steps

### Step 5: Feature Requirements Verification

Review decisions from `.agents/research/{feature}-discussion.md`:

```markdown
## Requirements Verification

| # | Requirement | Status | Evidence |
|---|-------------|--------|----------|
| 1 | JWT authentication | ✓ Implemented | tests/test_auth.py:45 |
| 2 | Email validation | ✓ Implemented | src/validators.py:12 |
| 3 | Rate limiting | ✓ Implemented | app/middleware.py:89 |
```

### Step 6: Generate Validation Report

Create `.agents/reports/validation-{timestamp}.md`:

```markdown
# Validation Report: {feature-name}

**Date:** 2026-01-28T10:30:00Z
**Status:** PASSED
**Duration:** 3m 45s

## Task Verification
- Total tasks: 5
- Completed: 5
- Verified: 5
- Failed: 0

## Quality Gates
| Gate | Status | Details |
|------|--------|---------|
| Linting | ✓ PASS | 0 errors |
| Type Check | ✓ PASS | 0 errors |
| Unit Tests | ✓ PASS | 47 passed in 12s |
| Integration | ✓ PASS | 23 passed in 1m 34s |
| Coverage | ✓ PASS | 87% (threshold: 80%) |

## Requirements
All 3 requirements verified and implemented.

## Summary
Feature is complete and ready for deployment.

## Next Steps
- Create commit
- Create PR to dev branch
- Update CHANGELOG.md
```

### Step 7: Update Session State

```yaml
session:
  phase: validate
  status: completed

validation:
  status: passed
  completed_at: "2026-01-28T10:30:00Z"
  duration_seconds: 225
  report_path: .agents/reports/validation-20260128-103000.md
```

### Step 8: Update STATE.md

```markdown
## Status: VALIDATED ✓

**Validation completed:** 2026-01-28 10:30:00

All tasks completed and verified.
All quality gates passed.
All requirements met.

Feature ready for deployment.
```

---

## Standalone Mode (--quick or no session)

**Execute only quality gates:**
1. Stage 1: Static Analysis
2. Stage 2: Unit Tests
3. Stage 3: Integration Tests
4. Stage 4: Coverage
5. (Optional) Stage 5-6 with --full

**No state interaction, no reporting.**

**Use cases:**
- Daily development validation
- Pre-commit checks
- Quick quality verification

---

## Handling Failures

### Task Verification Fails

```markdown
## Task Verification Failed: task-003

**Command:** pytest tests/integration/test_api.py
**Exit code:** 1
**Error:** AssertionError: Expected 200, got 500

**Options:**
1. Fix the issue and re-run /validate
2. Mark as known issue (add to session.yaml)
3. Abort validation
```

### Quality Gate Fails

```markdown
## Quality Gate Failed: Coverage

**Result:** 72% (threshold: 80%)
**Missing coverage:**
- src/utils/helpers.py: 45%
- src/models/user.py: 68%

**Options:**
1. Add tests for missing coverage
2. Lower threshold temporarily (update pyproject.toml)
3. Proceed with warning (not recommended)
```

### Requirements Not Met

```markdown
## Requirement Not Verified: Rate Limiting

**Expected:** Rate limiting middleware implemented
**Found:** No rate limiting in codebase

**Options:**
1. Implement missing requirement
2. Update requirements (was it descoped?)
3. Mark as follow-up task
```

---

## Success Criteria

### PIV-Swarm Mode
- [ ] All tasks completed
- [ ] All task verifications passed
- [ ] All quality gates passed
- [ ] All requirements verified
- [ ] Validation report generated
- [ ] Session state updated

### Standalone Mode
- [ ] Static analysis: 0 errors
- [ ] Unit tests: 100% passing
- [ ] Integration tests: 100% passing
- [ ] Coverage: >= 80%
- [ ] (--full) E2E tests: 100% passing
- [ ] (--full) Security: No issues

---

## Quality Thresholds

| Check | Target | Tool |
|-------|--------|------|
| Linting | 0 errors | ruff |
| Type Checking | 0 errors | mypy |
| Unit Tests | 100% passing | pytest |
| Integration Tests | 100% passing | pytest |
| E2E Tests | 100% passing | pytest |
| Coverage | >= 80% | pytest-cov |
| Security | No medium/high | bandit |

---

## Usage Scenarios

| Scenario | Command | Duration |
|----------|---------|----------|
| Daily dev check | `/validate --quick` | < 1 minute |
| End of task | `/validate` | 2-3 minutes |
| End of feature (PIV) | `/validate` | 3-5 minutes |
| Pre-PR full check | `/validate --full` | 5-10 minutes |
| Before release | `/validate --full` | 5-10 minutes |

---

## Next Steps

**After successful validation:**

**PIV-Swarm Mode:**
- Run `/commit` to create semantic commit
- Update CHANGELOG.md
- Create PR with validation report
- Run `/pause` if continuing later

**Standalone Mode:**
- Commit changes
- Create PR
- Merge when approved

---

## Token Budget

**Standalone:** 2-5K tokens
**PIV-Swarm:** 10-20K tokens (includes reporting)

---

## Remember

**Quality gates exist to catch issues before they reach production.**

- Validation is not optional
- All stages must pass
- Fix issues immediately
- Don't skip validation "just this once"
- Use --quick during development, full validation before completion

**"Measure twice, cut once" - Validate thoroughly, commit confidently.**
