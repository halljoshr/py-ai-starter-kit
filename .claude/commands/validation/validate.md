# Validate Command

**Multi-stage quality gates before commits and PRs.**

---

## Arguments

```
/validate              # Default validation (stages 1-4)
/validate --full       # Full validation including e2e (stages 1-6)
/validate --coverage   # Coverage analysis only
```

---

## Purpose

Run comprehensive multi-stage validation to ensure code quality before committing or merging.

**Philosophy:** "Catch issues early" - Multiple quality gates prevent defects from reaching production.

---

## Default Validation (4 Stages)

### Stage 1: Static Analysis (< 5 seconds)

**Linting:**
```bash
ruff check app/ tests/
```
**Pass criteria:** 0 errors

**Type Checking:**
```bash
mypy app/
```
**Pass criteria:** 0 type errors

**Why this matters:**
- Catches syntax errors
- Enforces code style consistency
- Prevents type-related bugs
- Fast feedback loop

---

### Stage 2: Unit Tests (< 30 seconds)

```bash
uv run pytest tests/unit/ -v --tb=short
```

**Pass criteria:**
- 100% unit tests passing
- No skipped tests (unless marked intentionally)
- Execution time < 30 seconds

**Why this matters:**
- Validates business logic
- Tests edge cases
- Fast enough for frequent runs
- Foundation of test pyramid

---

### Stage 3: Fast Integration Tests (< 2 minutes)

```bash
uv run pytest tests/integration/ -m "not very_slow" -v --tb=short
```

**Pass criteria:**
- 100% fast integration tests passing
- No timeout errors
- No external API failures (or properly mocked)

**Why this matters:**
- Validates service interactions
- Tests API contracts
- Catches integration bugs
- Reasonable execution time for CI

---

### Stage 4: Coverage Analysis

```bash
uv run pytest tests/unit/ tests/integration/ \
  --cov=app --cov=src \
  --cov-report=term-missing \
  --cov-fail-under=80
```

**Pass criteria:**
- Coverage ≥ 80%
- No significant coverage regressions
- Critical paths covered

**Why this matters:**
- Ensures comprehensive testing
- Identifies untested code
- Prevents coverage regressions
- Quality insurance

---

## Full Validation (6 Stages)

Use `--full` flag for comprehensive validation before releases.

### Stage 5: E2E Tests

```bash
uv run pytest tests/e2e/ -v --tb=short
```

**Pass criteria:**
- 100% e2e tests passing
- Complete workflows validated
- Production-like scenarios tested

**When to run:**
- Before merging to main
- Before releases
- Weekly CI runs

---

### Stage 6: Security Checks (Optional)

```bash
bandit -r app/ -ll
```

**Pass criteria:**
- No high-severity issues
- No medium-severity issues (or documented exceptions)

**When to run:**
- Before releases
- After security-related changes
- Monthly security audits

---

## Output Format

### Success Output

```markdown
# Validation Report

**Date:** 2025-01-14 11:30:00
**Branch:** feature/pro-XXX-feature-name
**Commit:** abc1234

---

## Stage 1: Static Analysis ✓

### Linting
**Status:** ✓ PASSED
**Command:** ruff check app/ tests/
**Result:** 0 errors
**Duration:** 1.2s

### Type Checking
**Status:** ✓ PASSED
**Command:** mypy app/
**Result:** 0 type errors
**Duration:** 3.8s

---

## Stage 2: Unit Tests ✓

**Status:** ✓ PASSED
**Command:** uv run pytest tests/unit/ -v
**Tests Run:** 259
**Passed:** 259
**Failed:** 0
**Skipped:** 0
**Duration:** 12.3s

---

## Stage 3: Integration Tests ✓

**Status:** ✓ PASSED
**Command:** uv run pytest tests/integration/ -m "not very_slow" -v
**Tests Run:** 74
**Passed:** 74
**Failed:** 0
**Skipped:** 0
**Duration:** 89.2s

---

## Stage 4: Coverage Analysis ✓

**Status:** ✓ PASSED
**Command:** pytest --cov=app --cov=src --cov-report=term-missing
**Coverage:** 87.2%
**Threshold:** 80.0%
**Missing Coverage:** 5 files (see details below)

**Coverage by Module:**
- app/services/: 92.5%
- app/routes/: 88.3%
- app/models/: 95.1%
- app/agents/: 82.7%
- src/: 79.8% ⚠️ (below 80%, but overall passing)

---

## Overall Status: ✓ PASSED

All validation gates passed. Code is ready to commit.

**Next Steps:**
1. Review any warnings above
2. Commit changes: `/commit`
3. Update CHANGELOG.md
4. Create PR
```

---

### Failure Output

```markdown
# Validation Report

**Date:** 2025-01-14 11:30:00
**Branch:** feature/pro-XXX-feature-name
**Commit:** abc1234

---

## Stage 1: Static Analysis ✗

### Linting
**Status:** ✗ FAILED
**Command:** ruff check app/ tests/
**Errors:** 3 errors found

**Details:**
```
app/services/webhook_service.py:45:1: F401 'httpx' imported but unused
app/services/webhook_service.py:67:80: E501 line too long (105 > 100 characters)
tests/unit/test_webhook.py:12:1: F811 redefinition of unused 'mock_client'
```

**Fix:**
```bash
ruff check --fix app/ tests/  # Auto-fix what's possible
# Then manually fix remaining issues
```

---

### Type Checking
**Status:** ✗ FAILED
**Command:** mypy app/
**Errors:** 2 type errors

**Details:**
```
app/services/webhook_service.py:89: error: Incompatible return value type (got "str", expected "WebhookPayload")
app/routes/webhooks.py:34: error: Missing return statement
```

**Fix:**
- Review type hints
- Add explicit return types
- Fix incompatible types

---

## Overall Status: ✗ FAILED

Validation failed at Stage 1. Fix issues above and run `/validate` again.

**DO NOT proceed with commit until all stages pass.**
```

---

## Coverage-Only Mode

```bash
/validate --coverage
```

**Output:**
```markdown
# Coverage Analysis Report

**Command:** pytest --cov=app --cov=src --cov-report=term-missing --cov-report=html

## Overall Coverage: 87.2%

**Threshold:** 80.0% ✓

## Coverage by Module

| Module | Coverage | Status |
|--------|----------|--------|
| app/services/ | 92.5% | ✓ |
| app/routes/ | 88.3% | ✓ |
| app/models/ | 95.1% | ✓ |
| app/agents/ | 82.7% | ✓ |
| src/ | 79.8% | ⚠️ |

## Missing Coverage (< 80%)

### src/utils/helper.py: 65.2%
**Missing lines:** 45-52, 89-95, 120-125

**Recommendations:**
- Add unit tests for helper functions
- Test edge cases on lines 45-52
- Add error handling tests

### app/services/legacy_service.py: 45.0%
**Missing lines:** 12-45, 67-89

**Note:** Legacy code, consider refactoring or deprecating

## HTML Report

Open `htmlcov/index.html` in browser for detailed coverage report.
```

---

## Usage Scenarios

### Daily Development
```bash
/validate  # Quick validation before commit (stages 1-4)
```

### Before PR Creation
```bash
/validate  # Ensure quality gates pass
```

### Before Merging to Dev
```bash
/validate --full  # Include e2e tests
```

### Before Release
```bash
/validate --full  # Full validation including security
```

### Coverage Check Only
```bash
/validate --coverage  # Just check test coverage
```

---

## CI/CD Integration

### PR to Dev Branch
```yaml
- name: Validate (Fast)
  run: |
    ruff check app/ tests/
    mypy app/
    uv run pytest tests/unit/ -v
    uv run pytest tests/integration/ -m "not very_slow" -v
    uv run pytest --cov=app --cov=src --cov-fail-under=80
```

### Merge to Main Branch
```yaml
- name: Validate (Full)
  run: |
    ruff check app/ tests/
    mypy app/
    uv run pytest tests/unit/ -v
    uv run pytest tests/integration/ -v
    uv run pytest tests/e2e/ -v
    uv run pytest --cov=app --cov=src --cov-fail-under=80
    bandit -r app/ -ll
```

---

## Troubleshooting

### "Linting fails with many errors"
**Solution:**
```bash
# Auto-fix what's possible
ruff check --fix app/ tests/

# Then manually fix remaining
ruff check app/ tests/
```

### "Type checking fails"
**Solution:**
1. Review error messages carefully
2. Add explicit type hints
3. Check Pydantic model types
4. Verify import statements

### "Tests pass locally but fail in CI"
**Solution:**
1. Check environment variables
2. Verify dependency versions match
3. Check for file system dependencies
4. Review CI logs for clues

### "Coverage is below threshold"
**Solution:**
```bash
# See missing lines
uv run pytest --cov=app --cov=src --cov-report=term-missing

# Generate HTML report for details
uv run pytest --cov=app --cov=src --cov-report=html
open htmlcov/index.html
```

### "Integration tests timeout"
**Solution:**
1. Check external API availability
2. Increase timeout in pytest.ini
3. Use mocks for unreliable services
4. Mark as `@pytest.mark.very_slow` if needed

---

## Quality Thresholds

### Linting
- **Target:** 0 errors
- **Tool:** ruff
- **Config:** pyproject.toml [tool.ruff]

### Type Checking
- **Target:** 0 errors
- **Tool:** mypy
- **Config:** pyproject.toml [tool.mypy]

### Unit Tests
- **Target:** 100% passing
- **Speed:** < 30 seconds
- **Location:** tests/unit/

### Integration Tests
- **Target:** 100% passing (fast tests)
- **Speed:** < 2 minutes
- **Location:** tests/integration/

### E2E Tests
- **Target:** 100% passing
- **Speed:** < 5 minutes
- **Location:** tests/e2e/

### Coverage
- **Target:** ≥ 80%
- **Tool:** pytest-cov
- **Config:** pyproject.toml [tool.coverage]

---

## Best Practices

### Run Validation Frequently
- ✅ After implementing each feature
- ✅ Before committing
- ✅ Before creating PR
- ✅ After fixing bugs

### Fix Issues Immediately
- ✅ Don't accumulate validation failures
- ✅ Fix linting before moving on
- ✅ Fix failing tests before adding more code
- ✅ Maintain coverage threshold

### Use Appropriate Level
- 🏃 **Daily dev:** `/validate` (fast)
- 📋 **PR creation:** `/validate` (fast)
- 🔀 **Merge to dev:** `/validate --full` (comprehensive)
- 🚀 **Release:** `/validate --full` (comprehensive)

### Monitor Trends
- 📊 Track coverage over time
- 📉 Investigate coverage drops
- 📈 Celebrate coverage improvements
- 🎯 Aim for 90%+ on new code

---

## Success Criteria

Validation is successful when:

✅ **Stage 1:** 0 linting errors, 0 type errors
✅ **Stage 2:** 100% unit tests passing
✅ **Stage 3:** 100% fast integration tests passing
✅ **Stage 4:** Coverage ≥ 80%
✅ **Overall:** All stages passed

**Result:** Code is ready to commit and create PR.

---

## Remember

**Quality gates exist to catch issues before they reach production.**

- Validation is not optional
- All stages must pass
- Fix issues immediately
- Don't skip validation "just this once"

**"Measure twice, cut once" - Validate thoroughly, commit confidently.**
