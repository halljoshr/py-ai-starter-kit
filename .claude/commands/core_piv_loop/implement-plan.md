# Implement Plan Command

**Execute plan documents systematically with validation at every step.**

---

## Arguments

```
/implement-plan {plan-file}
```

**Example:**
```
/implement-plan .agents/plans/hubspot-webhook-validation.md
/implement-plan .agents/plans/debt-assessment-agent.md
```

---

## Purpose

Execute a comprehensive Plan document systematically, with incremental validation after EACH task to ensure quality and catch issues early.

**Philosophy:** "Validate Early, Validate Often" - Don't accumulate technical debt by skipping validation steps.

---

## Pre-Implementation Checklist

Before starting implementation:

- [ ] Read ENTIRE plan document
- [ ] Understand all task dependencies
- [ ] Note all critical gotchas
- [ ] Verify baseline (run tests before changes)
- [ ] Confirm environment setup (API keys, dependencies)

---

## Implementation Process

### Step 1: Preparation

**Read and Parse Plan:**
```markdown
1. Load plan file from .agents/plans/
2. Extract:
   - Feature understanding
   - Context references
   - Implementation tasks
   - Testing strategy
   - Acceptance criteria
   - Gotchas
   - Validation commands
```

**Verify Baseline:**
```bash
# Ensure starting from clean state
git status

# Run existing tests to confirm baseline
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -m "not very_slow" -v

# Check coverage baseline
uv run pytest --cov=app --cov=src --cov-report=term
```

**Document Baseline:**
- Tests passing: X / Y
- Coverage: Z%
- Branch: {branch name}
- Last commit: {commit hash}

---

### Step 2: Sequential Task Execution

**For EACH task in order:**

#### 2.1: Review Task Details

Read the task completely:
- **IMPLEMENT:** What to build
- **PATTERN:** Reference code to follow
- **IMPORTS:** Required modules
- **GOTCHA:** Pitfalls to avoid
- **VALIDATE:** Command to run

#### 2.2: Check Dependencies

- Is this task dependent on previous tasks?
- Are all prerequisites complete?
- Are required files created?

#### 2.3: Implement Task

- Follow the pattern exactly as documented
- Use the complete code from plan (not pseudocode)
- Reference the specified files and line numbers
- Pay attention to gotchas
- Add inline comments where logic is non-obvious

#### 2.4: Incremental Validation (CRITICAL)

**Run task-specific validation immediately:**

```bash
# Syntax check
ruff check {file}

# Type check
mypy {file}

# Unit tests (if applicable)
uv run pytest tests/unit/test_{name}.py -v
```

**Validation Decision Tree:**
```
Run Validation
    ↓
Pass? ──Yes──→ Mark task complete, proceed to next task
    ↓
    No
    ↓
Debug & Fix
    ↓
Run Validation Again
    ↓
Pass? ──Yes──→ Mark task complete, proceed to next task
    ↓
    No
    ↓
Try alternative approach or ask user for guidance
```

#### 2.5: Update Progress

```markdown
- [x] Task N: {Description}
  - ✅ Validation passed
  - Duration: X minutes
  - Notes: {Any observations}
```

**Update TodoWrite immediately after completing each task.**

---

### Step 3: Deviation Tracking

**If implementation must deviate from plan, document:**

```markdown
## Deviation: Task N

**Type:** Added feature / Changed approach / Omitted task

**Reason:** {Why deviation was necessary}
- {Detailed explanation}
- {What was discovered during implementation}

**Impact:**
- {Effect on other tasks}
- {Changes to overall design}
- {Testing implications}

**Alternative Considered:**
- {What was in the plan}
- {Why it didn't work}
```

**Common deviation types:**
- **Added feature:** Discovered need for additional functionality
- **Changed approach:** Original approach had issues/limitations
- **Omitted task:** Task no longer needed or covered by other changes
- **Reordered tasks:** Dependencies different than expected

---

### Step 4: Issue Resolution Loop

**When validation fails:**

```
Attempt 1: Implement as planned
    ↓
    Validation fails
    ↓
Attempt 2: Debug error, review gotchas, fix issue
    ↓
    Validation fails
    ↓
Attempt 3: Try alternative approach from context references
    ↓
    Validation fails
    ↓
Ask user for guidance (provide detailed error info)
```

**NEVER:**
- ❌ Skip validation when it fails
- ❌ Proceed to next task with failing tests
- ❌ Accumulate multiple failures before fixing
- ❌ Assume "it will work in production"

**ALWAYS:**
- ✅ Fix issues immediately
- ✅ Re-run validation after fix
- ✅ Document what was fixed and why
- ✅ Update tests if needed

---

### Step 5: Continuous Testing

**After every 2-3 tasks, run broader validation:**

```bash
# All unit tests
uv run pytest tests/unit/ -v

# Fast integration tests
uv run pytest tests/integration/ -m "not very_slow" -v

# Coverage check
uv run pytest --cov=app --cov=src --cov-report=term
```

**Purpose:**
- Catch regressions early
- Verify integration between tasks
- Monitor coverage trends
- Ensure overall system health

---

### Step 6: Final Validation

**After all tasks complete:**

```bash
# Full validation suite
/validate

# Or manually:
ruff check app/ tests/
mypy app/
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -m "not very_slow" -v
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80
```

**Verify Acceptance Criteria:**
- [ ] Go through plan's acceptance criteria checklist
- [ ] Verify each criterion met
- [ ] Document any criteria not met and why

---

## Progress Reporting

**Keep user informed throughout:**

### Start of Implementation
```markdown
## Starting Implementation: {Feature Name}

**Plan:** .agents/plans/{feature-name}.md
**Tasks:** {total count}
**Estimated Duration:** {if known}

**Baseline:**
- Tests passing: X / Y
- Coverage: Z%
- Branch: {branch}
```

### During Implementation
```markdown
**Progress:** Task N / M complete

**Current Task:** {Task description}
**Status:** In progress / Validating / Complete

**Recent Completions:**
- [x] Task N-2: {Description} ✅
- [x] Task N-1: {Description} ✅
```

### After Each Task
```markdown
**Completed:** Task N - {Description}
**Validation:** ✅ Passed
**Duration:** X minutes
**Next:** Task N+1 - {Description}
```

### Issues Encountered
```markdown
**Issue:** Task N validation failed
**Error:** {Error message}
**Attempts:** {count}
**Status:** Debugging / Fixed / Seeking guidance
```

---

## Deviation Documentation

**Track ALL deviations from plan:**

### Deviation Log Template

```markdown
## Implementation Deviations

### Deviation 1: Task 3 - Changed approach

**Original Plan:**
- Use httpx.get() synchronously
- Parse JSON manually

**Actual Implementation:**
- Used httpx.AsyncClient() asynchronously
- Let Pydantic parse JSON automatically

**Reason:**
- Endpoint requires async for performance
- Pydantic validation is more robust

**Impact:**
- Task 4 tests needed async fixtures
- Minor change to test patterns
- Better error handling

**Improvement for Next Plan:**
- Check if endpoint is async before planning
- Default to Pydantic parsing for JSON APIs

---

### Deviation 2: Task 5 - Added task not in plan

**Added:**
- Error logging middleware

**Reason:**
- Discovered need during integration testing
- Required for debugging production issues

**Impact:**
- Added 30 minutes to implementation
- Added tests for middleware

**Improvement for Next Plan:**
- Always consider logging/observability upfront
```

---

## Success Criteria

Implementation is complete when:

✅ **All tasks executed**
- Every task in plan implemented or explicitly omitted with reason

✅ **All validations pass**
- Linting: 0 errors
- Type checking: 0 errors
- Unit tests: 100% passing
- Integration tests: 100% passing (not very_slow)
- Coverage: ≥ 80%

✅ **All acceptance criteria met**
- Each checkbox in plan verified

✅ **Deviations documented**
- Any changes from plan explained

✅ **Tests updated**
- New features have tests
- Coverage maintained or improved

✅ **Documentation updated**
- Docstrings complete
- CHANGELOG.md entry added (if applicable)

---

## Final Output

### Execution Summary

```markdown
## Execution Summary: {Feature Name}

**Plan:** .agents/plans/{feature-name}.md
**Completed:** {Date and Time}
**Duration:** {Total time}

### Tasks Completed: X / Y

- [x] Task 1: Create data model
  - ✅ Validation passed
  - Duration: 5 minutes

- [x] Task 2: Create service
  - ✅ Validation passed
  - Duration: 15 minutes

- [x] Task 3: Create API route
  - ❌ Validation failed (attempt 1)
  - 🔧 Fixed: Changed sync to async
  - ✅ Validation passed (attempt 2)
  - Duration: 20 minutes

- [x] Task 4: Create unit tests
  - ✅ Validation passed
  - Duration: 10 minutes

- [x] Task 5: Create integration tests
  - ✅ Validation passed
  - Duration: 15 minutes

### Final Validation Results

- [x] Linting: ✅ 0 errors
- [x] Type checking: ✅ 0 errors
- [x] Unit tests: ✅ 25/25 passing
- [x] Integration tests: ✅ 8/8 passing
- [x] Coverage: ✅ 87.2% (threshold: 80%)

### Files Changed

**Added:**
- app/models/webhook_payload.py (95 lines)
- app/services/webhook_service.py (120 lines)
- app/routes/webhooks.py (85 lines)
- tests/unit/test_webhook_service.py (150 lines)
- tests/integration/test_webhooks.py (100 lines)

**Modified:**
- app/main.py (+5 lines, -0 lines) - Added webhook router

### Acceptance Criteria

- [x] All data models created with Pydantic v2
- [x] Service implementation with async/await
- [x] API routes with dependency injection
- [x] Unit tests with 100% method coverage
- [x] Integration tests for happy/error paths
- [x] All tests passing
- [x] Coverage ≥ 80%
- [x] Linting passes
- [x] Type checking passes
- [x] No secrets in code

### Deviations from Plan

**Count:** 2 deviations

1. **Task 3:** Changed from sync to async (reason: performance requirements)
2. **Added:** Error logging middleware (reason: debugging needs)

See detailed deviation log above.

### Summary

Successfully implemented webhook validation feature with comprehensive test coverage. Two minor deviations from plan, both documented with rationale. All acceptance criteria met. Ready for code review and commit.
```

---

## Next Steps After Implementation

1. **Run full validation:**
   ```bash
   /validate
   ```

2. **Generate execution report:**
   ```bash
   /execution-report .agents/plans/{feature-name}.md
   ```

3. **Code review (optional):**
   ```bash
   /code-review
   ```

4. **Commit changes:**
   ```bash
   /commit
   ```

5. **Update CHANGELOG.md:**
   - Add entry under [Unreleased]
   - Include PRO-XXX ticket reference

---

## Troubleshooting

### "Validation keeps failing"
**Solution:**
1. Review gotchas section of plan
2. Check context references for missed patterns
3. Review error message carefully
4. Try alternative approach
5. Ask user for guidance after 3 attempts

### "Test coverage dropped"
**Solution:**
1. Run coverage with missing lines: `pytest --cov-report=term-missing`
2. Identify uncovered lines
3. Add tests for uncovered code
4. Verify edge cases covered

### "Integration test requires API key"
**Solution:**
1. Check .env.example for required variables
2. Verify environment setup
3. Use mocks if API unavailable
4. Mark test with `@pytest.mark.requires_api`

### "Type checking fails with cryptic error"
**Solution:**
1. Check import statements
2. Verify Pydantic model types
3. Add explicit type hints
4. Review mypy error location carefully

---

## Critical Rules

### NEVER:
- ❌ Skip validation when it fails
- ❌ Proceed with failing tests
- ❌ Ignore type errors
- ❌ Skip documentation
- ❌ Commit secrets
- ❌ Modify tests to pass without fixing code

### ALWAYS:
- ✅ Validate after each task
- ✅ Fix issues immediately
- ✅ Document deviations
- ✅ Update todo list
- ✅ Keep user informed
- ✅ Maintain or improve coverage

---

## Remember

**The goal is working, tested, validated code - not just code that "looks right".**

Validation after every task prevents:
- Accumulating technical debt
- Hard-to-debug integration issues
- Regression in test coverage
- Merge conflicts and refactoring

**"Trust but verify" - Validate everything, every time.**
