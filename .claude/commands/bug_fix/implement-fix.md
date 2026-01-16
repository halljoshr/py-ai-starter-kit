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
# Run affected tests
uv run pytest tests/unit/test_{module}.py -v

# Run full test suite
/validate

# Verify issue is resolved
# Test manually if needed
```

### Step 6: Check for Similar Patterns

```bash
# Search for similar code patterns
# Fix all instances in same PR
rg "{similar_pattern}" app/ src/
```

### Step 7: Update Documentation

- Update security-best-practices.md if needed
- Update CLAUDE.md if needed
- Add to known-issues if pattern found elsewhere

---

## Output Format

```markdown
## Fix Implementation: Issue #{number}

**RCA:** .agents/rca/issue-{number}.md
**Implemented:** {Date}
**Branch:** fix/issue-{number}

### Files Modified
- app/services/webhook_service.py (+2, -1)
- app/services/api_auth.py (+2, -1)
- tests/unit/test_webhook_service.py (+15, -0)

### Fix Applied
{Description of what was fixed}

### Tests Added
- test_signature_validation_timing_safe
- test_token_validation_timing_safe

### Validation
- All tests passing: ✅
- Issue resolved: ✅
- Similar patterns fixed: ✅

### Ready for PR: YES
```

---

## Commit Message

```
fix(security): prevent timing attacks in signature validation

Fixes #{issue-number}

- Use secrets.compare_digest() for constant-time comparison
- Prevents timing attack vulnerabilities
- Applied fix to all similar patterns in codebase
- Added security tests

RCA: .agents/rca/issue-{number}.md

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Remember

"Fix the root cause, test the fix, prevent recurrence."
