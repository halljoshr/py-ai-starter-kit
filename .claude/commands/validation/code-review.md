# Code Review Command

**AI-driven code review before committing.**

---

## Purpose

Perform comprehensive code review across five dimensions: Logic, Security, Performance, Quality, and Standards.

---

## Usage

```
/code-review
```

---

## Review Process

### Step 1: Establish Context
```bash
# Read core documentation
cat CLAUDE.md
cat README.md

# Identify changed files
git status
git diff HEAD --name-only
```

### Step 2: Analyze Full Files
- Read complete files (not just diffs)
- Understand surrounding context
- Check for ripple effects

### Step 3: Evaluate on Five Dimensions

#### 1. Logic
- Correctness of algorithms
- Off-by-one errors
- Edge case handling
- Null/None checks
- Error handling completeness
- Race conditions

#### 2. Security (CRITICAL flag for issues)
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure data handling
- Exposed credentials/secrets
- Improper authentication
- Missing input validation

#### 3. Performance
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Unnecessary database calls
- Missing caching opportunities
- Blocking I/O in async code

#### 4. Quality
- DRY violations
- Function complexity
- Variable naming clarity
- Type annotations completeness
- Documentation/docstrings
- Code duplication

#### 5. Standards
- CLAUDE.md adherence
- Testing requirements met
- Naming conventions
- File structure
- Error handling patterns

---

## Output Format

Save to: `.agents/code-reviews/{feature-name}-review-{date}.md`

```markdown
# Code Review: {Feature Name}

**Reviewed:** {Date}
**Branch:** {branch name}
**Reviewer:** Claude Sonnet 4.5

---

## Summary

**Files Reviewed:** {count}
**Issues Found:** {count}
- Critical: {count}
- High: {count}
- Medium: {count}
- Low: {count}

**Overall Assessment:** Approve / Request Changes / Reject

---

## Issues

### Issue 1: [CRITICAL] Exposed API key in code

**File:** app/services/webhook_service.py:45
**Severity:** CRITICAL
**Category:** Security

**Problem:**
API key hardcoded in source code instead of using environment variable.

**Code:**
```python
self.api_key = "sk-live-abc123def456"  # CRITICAL: Hardcoded secret
```

**Fix:**
```python
from app.config.settings import get_settings

self.api_key = get_settings().api_key  # Use environment variable
```

**Impact:** High - Exposes credentials if code is committed to repository.

---

### Issue 2: [HIGH] Missing error handling

**File:** app/services/webhook_service.py:67
**Severity:** HIGH
**Category:** Logic

**Problem:**
No error handling for HTTP request failures. Will crash on network errors.

**Code:**
```python
response = await client.get(url)
data = response.json()  # Crashes if response is not JSON
```

**Fix:**
```python
try:
    response = await client.get(url)
    response.raise_for_status()
    data = response.json()
except httpx.HTTPStatusError as e:
    logger.error(f"HTTP error: {e}")
    raise
except httpx.RequestError as e:
    logger.error(f"Request error: {e}")
    raise
```

**Impact:** Medium - Service crashes on API failures instead of graceful handling.

---

### Issue 3: [MEDIUM] N+1 query pattern

**File:** app/services/deal_service.py:123
**Severity:** MEDIUM
**Category:** Performance

**Problem:**
Loading related records in a loop causes N+1 queries.

**Code:**
```python
for deal in deals:
    deal.owner = await get_owner(deal.owner_id)  # N+1 query
```

**Fix:**
```python
# Fetch all owners in one query
owner_ids = [deal.owner_id for deal in deals]
owners = await get_owners_bulk(owner_ids)
owner_map = {o.id: o for o in owners}

for deal in deals:
    deal.owner = owner_map.get(deal.owner_id)
```

**Impact:** Low - Performance degrades with large datasets.

---

### Issue 4: [LOW] Missing type hints

**File:** app/utils/helpers.py:34
**Severity:** LOW
**Category:** Quality

**Problem:**
Function lacks type hints making it harder to understand expected types.

**Code:**
```python
def calculate_total(items):  # Missing type hints
    return sum(i.amount for i in items)
```

**Fix:**
```python
from typing import List
from app.models import Item

def calculate_total(items: List[Item]) -> Decimal:
    """Calculate total amount from items."""
    return sum(i.amount for i in items)
```

**Impact:** Very Low - Reduces code clarity but doesn't affect functionality.

---

## Positive Observations

✅ **Good test coverage** - All new code has corresponding tests
✅ **Clear naming** - Variables and functions use descriptive names
✅ **Proper async usage** - Correctly using async/await patterns
✅ **Pydantic v2 syntax** - Models use correct v2 validators

---

## Recommendations

### Must Fix (Before Merge)
- Issue 1: Remove hardcoded API key (CRITICAL)
- Issue 2: Add error handling to HTTP requests (HIGH)

### Should Fix (This PR)
- Issue 3: Optimize N+1 query pattern (MEDIUM)

### Nice to Have (Future)
- Issue 4: Add type hints to utility functions (LOW)

---

## Standards Compliance

**CLAUDE.md Adherence:**
- ✅ File length < 500 lines
- ✅ Function length < 100 lines
- ✅ Line length ≤ 100 characters
- ✅ Testing coverage ≥ 80%
- ✅ Proper naming conventions
- ❌ Missing docstrings on some functions (Issue 5)

---

## Overall Assessment

**Recommendation:** REQUEST CHANGES

**Rationale:**
- 1 CRITICAL security issue must be fixed
- 1 HIGH severity logic issue should be fixed
- Otherwise code quality is good with proper testing

**Next Steps:**
1. Fix Critical and High severity issues
2. Re-run validation: `/validate`
3. Request re-review if needed
```

---

## Review Checklist

- [ ] Established context (read CLAUDE.md, README)
- [ ] Identified all changed files
- [ ] Read complete files (not just diffs)
- [ ] Checked for logic errors
- [ ] Checked for security vulnerabilities
- [ ] Checked for performance issues
- [ ] Checked for quality problems
- [ ] Checked standards compliance
- [ ] Documented all issues with severity
- [ ] Provided specific fix recommendations
- [ ] Saved review to `.agents/code-reviews/`

---

## Remember

"The best code is often the code you don't write" - Simplicity over cleverness.
