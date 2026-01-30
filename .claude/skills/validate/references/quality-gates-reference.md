# Quality Gates Reference

Detailed information about each validation stage in the PIV-Swarm workflow.

## Stage 1: Code Formatting (ruff format)

**Purpose:** Ensure consistent code style across codebase

**Command:**
```bash
uv run ruff format . --check
```

**What it checks:**
- Line length (100 characters)
- Indentation (4 spaces)
- Quote style (double quotes)
- Trailing whitespace
- Import sorting

**Common failures:**
- Mixed tabs and spaces
- Inconsistent quote usage
- Lines exceeding 100 characters
- Improper import order

**Fix:**
```bash
uv run ruff format .  # Auto-fix formatting
```

---

## Stage 2: Linting (ruff check)

**Purpose:** Catch code quality issues and potential bugs

**Command:**
```bash
uv run ruff check .
```

**What it checks:**
- Unused imports and variables
- Undefined names
- F-string syntax errors
- Import conventions (PEP8)
- Naming conventions
- Code complexity

**Common failures:**
- `F401`: Imported but unused
- `E501`: Line too long
- `F841`: Variable assigned but never used
- `N806`: Variable should be lowercase

**Fix:**
```bash
uv run ruff check . --fix  # Auto-fix safe issues
```

---

## Stage 3: Type Checking (mypy)

**Purpose:** Verify type hints are correct and consistent

**Command:**
```bash
uv run mypy app/ src/
```

**What it checks:**
- Type annotation correctness
- Return type matches
- Argument types match function signature
- Optional/None handling
- Generic type usage

**Common failures:**
- Missing return type annotation
- Incompatible types in assignment
- Missing type hints on function parameters
- `Optional[T]` vs `T | None` inconsistency

**Fix:**
Add proper type hints:
```python
# Bad
def process_data(data):
    return data.upper()

# Good
def process_data(data: str) -> str:
    return data.upper()
```

---

## Stage 4: Unit Tests (pytest)

**Purpose:** Verify business logic works in isolation

**Command:**
```bash
uv run pytest tests/unit/ -v
```

**What it checks:**
- All unit tests pass
- No test failures or errors
- No skipped tests (unless intentional)
- Fast execution (< 1s per test)

**Common failures:**
- Assertion errors (expected vs actual mismatch)
- Fixture errors (setup/teardown issues)
- Import errors (missing dependencies)
- Timeout (test taking too long)

**Fix:**
- Check test assertion logic
- Verify mock/fixture setup
- Ensure test isolation (no shared state)

---

## Stage 5: Integration Tests (pytest)

**Purpose:** Verify service interactions work correctly

**Command:**
```bash
uv run pytest tests/integration/ -v
```

**What it checks:**
- Integration tests pass
- Database operations work
- API endpoints respond correctly
- External service integrations function

**Common failures:**
- Database connection errors
- API authentication failures
- Missing test data
- Network timeouts

**Fix:**
- Check database is running and accessible
- Verify test environment configuration
- Ensure test data fixtures are set up

---

## Stage 6: Coverage (pytest-cov)

**Purpose:** Ensure adequate test coverage (minimum 80%)

**Command:**
```bash
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80
```

**What it checks:**
- Overall coverage >= 80%
- Per-module coverage reported
- Missing lines identified

**Common failures:**
- New code added without tests
- Error handling branches not tested
- Edge cases not covered

**Fix:**
- Add tests for uncovered lines
- Test both success and failure paths
- Use parametrize for multiple cases

**Reading coverage report:**
```
app/services/user.py    78%    45-52, 67-71
                        ^^^    ^^^^^^^^^^^^
                       coverage  missing lines
```

Lines 45-52 and 67-71 are not covered by tests.

---

## PIV-Swarm Additional Stages

### Stage 7: Task-Specific Verification

**Purpose:** Run validation commands specified in task files

**What it checks:**
- Task marked as completed
- Verification commands from `task.yaml` pass
- Feature-specific validation

**Example task verification:**
```yaml
# .agents/tasks/task-001.yaml
verification:
  commands:
    - "uv run pytest tests/unit/test_user_auth.py"
    - "uv run python scripts/verify_api_endpoints.py"
```

### Stage 8: Feature Requirements

**Purpose:** Verify all acceptance criteria met

**What it checks:**
- All tasks marked completed
- Acceptance criteria from spec satisfied
- No blockers or open issues

---

## Troubleshooting

### All tests pass locally but fail in CI

**Causes:**
- Environment differences (Python version, OS)
- Missing dependencies in CI
- Tests depending on local state

**Solutions:**
- Match CI environment locally (use Docker)
- Check CI logs for specific errors
- Ensure tests are fully isolated

### Coverage dropped below 80%

**Causes:**
- New code added without tests
- Tests removed or commented out
- Coverage calculation changed

**Solutions:**
- Run `pytest --cov --cov-report=html` to see detailed report
- Identify uncovered lines in HTML report
- Add tests for new functionality

### mypy errors after dependency update

**Causes:**
- Dependency changed type signatures
- New type stubs available
- Stricter type checking enabled

**Solutions:**
- Update type hints to match new signatures
- Use `type: ignore` sparingly for third-party issues
- Check library documentation for type changes

---

## Best Practices

1. **Run validation frequently** - Don't wait until the end
2. **Fix issues early** - Easier to fix small batches
3. **Use auto-fix tools** - Let `ruff format` and `ruff check --fix` help
4. **Read error messages** - They usually tell you exactly what's wrong
5. **Keep tests fast** - Unit tests should be < 1 second each
6. **Maintain coverage** - Don't let it drop below 80%
