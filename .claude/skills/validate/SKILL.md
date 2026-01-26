---
name: validate
description: Multi-stage quality gates before commits and PRs. Runs linting, type checking, tests, and coverage.
disable-model-invocation: true
argument-hint: "[--full|--coverage]"
allowed-tools: Bash
---

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

```bash
ruff check app/ tests/
mypy app/
```
**Pass criteria:** 0 errors

### Stage 2: Unit Tests (< 30 seconds)

```bash
uv run pytest tests/unit/ -v --tb=short
```
**Pass criteria:** 100% passing

### Stage 3: Fast Integration Tests (< 2 minutes)

```bash
uv run pytest tests/integration/ -m "not very_slow" -v --tb=short
```
**Pass criteria:** 100% passing

### Stage 4: Coverage Analysis

```bash
uv run pytest tests/unit/ tests/integration/ \
  --cov=app --cov=src \
  --cov-report=term-missing \
  --cov-fail-under=80
```
**Pass criteria:** Coverage >= 80%

---

## Full Validation (--full)

Adds:
- **Stage 5:** E2E Tests
- **Stage 6:** Security Checks (bandit)

---

## Quality Thresholds

| Check | Target | Tool |
|-------|--------|------|
| Linting | 0 errors | ruff |
| Type Checking | 0 errors | mypy |
| Unit Tests | 100% passing | pytest |
| Integration Tests | 100% passing | pytest |
| Coverage | >= 80% | pytest-cov |

---

## Usage Scenarios

- **Daily Development:** `/validate` (fast)
- **Before PR Creation:** `/validate`
- **Before Merging to Dev:** `/validate --full`
- **Before Release:** `/validate --full`
- **Coverage Check Only:** `/validate --coverage`

---

## Success Criteria

Validation is successful when:

- Stage 1: 0 linting errors, 0 type errors
- Stage 2: 100% unit tests passing
- Stage 3: 100% fast integration tests passing
- Stage 4: Coverage >= 80%
- Overall: All stages passed

**Result:** Code is ready to commit and create PR.

---

## Remember

**Quality gates exist to catch issues before they reach production.**

- Validation is not optional
- All stages must pass
- Fix issues immediately
- Don't skip validation "just this once"

**"Measure twice, cut once" - Validate thoroughly, commit confidently.**
