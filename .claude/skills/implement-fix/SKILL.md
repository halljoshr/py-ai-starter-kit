---
name: implement-fix
description: Execute bug fix based on RCA document with proper testing and validation.
disable-model-invocation: true
argument-hint: "{rca-file}"
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# Implement Fix Command

**Execute bug fix based on RCA document.**

---

## Arguments

```
/implement-fix {rca-file}
```

**Example:**
```
/implement-fix .agents/rca/issue-42-2025-01-14.md
```

---

## Purpose

Implement bug fix systematically based on root cause analysis, following the solution design from RCA.

---

## Process

### Step 1: Review RCA

- Read complete RCA document
- Understand root cause
- Note all files to modify
- Review testing strategy
- Check for similar patterns

### Step 2: Verify Issue

```bash
# Reproduce the bug if possible
# Run existing tests to confirm failure
uv run pytest tests/unit/test_{affected_module}.py -v
```

### Step 3: Implement Fix

Follow solution design from RCA exactly:
- Modify specified files
- Follow recommended approach
- Add inline comments explaining fix
- Reference issue number in comments

### Step 4: Add Tests

- Add tests that would have caught this bug
- Test the fix works
- Test edge cases
- Add regression test

### Step 5: Verify Fix

```bash
uv run pytest tests/unit/test_{module}.py -v
/validate
```

### Step 6: Check for Similar Patterns

```bash
rg "{similar_pattern}" app/ src/
```

Fix all instances in same PR.

### Step 7: Update Documentation

- Update security-best-practices.md if needed
- Update CLAUDE.md if needed
- Add to known-issues if pattern found elsewhere

---

## Commit Message Format

```
fix(security): prevent timing attacks in signature validation

Fixes #{issue-number}

- Use secrets.compare_digest() for constant-time comparison
- Prevents timing attack vulnerabilities
- Applied fix to all similar patterns in codebase
- Added security tests

RCA: .agents/rca/issue-{number}.md

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

## Remember

"Fix the root cause, test the fix, prevent recurrence."
