---
name: implement-plan
description: Execute plan documents systematically with validation at every step.
disable-model-invocation: true
argument-hint: "{plan-file}"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

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

- Load plan file from .agents/plans/
- Extract context references, tasks, testing strategy
- Verify baseline tests pass

### Step 2: Sequential Task Execution

For EACH task in order:

1. **Review Task Details** - IMPLEMENT, PATTERN, IMPORTS, GOTCHA, VALIDATE
2. **Check Dependencies** - Are prerequisites complete?
3. **Implement Task** - Follow pattern exactly
4. **Incremental Validation** - Run task-specific validation immediately
5. **Update Progress** - Mark task complete

### Step 3: Deviation Tracking

If implementation must deviate from plan, document:
- Type (Added feature / Changed approach / Omitted task)
- Reason
- Impact
- Alternative Considered

### Step 4: Issue Resolution Loop

```
Attempt 1: Implement as planned
    ↓ Validation fails
Attempt 2: Debug error, review gotchas, fix issue
    ↓ Validation fails
Attempt 3: Try alternative approach
    ↓ Validation fails
Ask user for guidance
```

### Step 5: Continuous Testing

After every 2-3 tasks:
```bash
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -m "not very_slow" -v
```

### Step 6: Final Validation

```bash
/validate
```

---

## Critical Rules

### NEVER:
- Skip validation when it fails
- Proceed with failing tests
- Ignore type errors
- Skip documentation
- Commit secrets
- Modify tests to pass without fixing code

### ALWAYS:
- Validate after each task
- Fix issues immediately
- Document deviations
- Update todo list
- Keep user informed
- Maintain or improve coverage

---

## Remember

**The goal is working, tested, validated code - not just code that "looks right".**

"Trust but verify" - Validate everything, every time.
