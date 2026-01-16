# Root Cause Analysis (RCA) Command

**Systematic bug investigation before fixing.**

---

## Arguments

```
/rca {issue-number}
```

**Example:**
```
/rca 42
/rca PRO-266
```

---

## Purpose

Perform comprehensive root cause analysis before attempting to fix a bug. Understanding WHY something broke prevents repeat issues and enables better fixes.

---

## Six-Phase RCA Process

### Phase 1: Information Gathering

**Collect all available information:**
- Issue description
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Environment (dev/staging/prod)
- When it started occurring
- User reports

**If using GitHub Issues:**
```bash
gh issue view {issue-number}
```

---

### Phase 2: Code Investigation

**Search for relevant code:**
```bash
# Find error messages
rg "exact error message" app/ src/

# Find related functions
rg "function_name" app/ src/ -A 5

# Find file modifications
rg "problematic_variable" app/ src/
```

**Read relevant files completely** (not just grep results)

---

### Phase 3: Historical Analysis

**Review recent changes:**
```bash
# Find commits affecting relevant files
git log --oneline -- path/to/file.py | head -20

# See what changed recently
git log --since="2 weeks ago" --oneline --grep="relevant_keyword"

# Check specific commit
git show {commit-hash}
```

---

### Phase 4: Root Cause Determination

**Identify the actual cause:**
- Input validation failure?
- Unhandled edge case?
- Race condition?
- Missing error handling?
- Incorrect business logic?
- External service failure?
- Data migration issue?

---

### Phase 5: Impact Evaluation

**Assess scope:**
- How many users affected?
- What features broken?
- Data integrity issues?
- Security implications?

---

### Phase 6: Solution Design

**Plan the fix:**
- What files need modification?
- What tests need to be added?
- How to prevent recurrence?
- Rollback plan if needed?

---

## Output Format

Save to: `.agents/rca/issue-{number}-{date}.md`

```markdown
# Root Cause Analysis: {Issue Title}

**Issue:** #{number} or PRO-{number}
**Analyzed:** {Date}
**Analyzer:** Claude Sonnet 4.5
**Severity:** Critical / High / Medium / Low

---

## Issue Summary

**Reporter:** {username}
**Reported:** {date}
**Environment:** Production / Staging / Development

**Description:**
{Clear description of the problem}

**Steps to Reproduce:**
1. {step 1}
2. {step 2}
3. {step 3}

**Expected Behavior:**
{what should happen}

**Actual Behavior:**
{what actually happens}

**Error Messages:**
```
{stack trace or error output}
```

---

## Investigation

### Code Analysis

**Relevant Files:**
- app/services/webhook_service.py:67 - Where error occurs
- app/models/webhook_payload.py:34 - Related validation
- app/routes/webhooks.py:45 - Entry point

**Problematic Code:**
```python
# app/services/webhook_service.py:67
async def validate_signature(self, payload: str, signature: str) -> bool:
    expected = hmac.new(
        self.secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    return expected == signature  # BUG: Timing attack vulnerable
```

### Historical Context

**Recent Changes:**
```
commit abc1234 (2025-01-10)
Author: Developer
"feat(webhooks): add signature validation"

This commit introduced the validation logic but used simple == comparison
instead of secure comparison.
```

**Related Issues:**
- Similar security issue fixed in PR #123 (authentication module)
- Pattern exists elsewhere that should also be reviewed

---

## Root Cause

**Category:** Security Vulnerability

**Cause:** Timing attack vulnerability in signature comparison

**Details:**
The code uses standard `==` comparison for signature validation, which is vulnerable to timing attacks. An attacker can measure response times to determine if signatures are partially correct, eventually brute-forcing the valid signature.

**Why It Happened:**
- Developer unaware of timing attack risks
- No security review before merge
- Similar vulnerable code exists in codebase
- Missing security testing

**First Introduced:**
- Commit: abc1234
- Date: 2025-01-10
- PR: #45

---

## Impact Assessment

### Scope
- **Affected Users:** All webhook integrations (~50 customers)
- **Affected Features:** Webhook signature validation
- **Data Integrity:** No data corruption
- **Security:** HIGH - Signatures can be brute-forced

### Severity: HIGH

**Justification:**
- Security vulnerability
- Affects production
- Actively exploitable
- No authentication bypass yet, but possible

### Urgency: HIGH

**Recommended Timeline:** Fix within 24 hours

---

## Solution Design

### Fix Strategy

**Approach:** Use `secrets.compare_digest()` for constant-time comparison

**Files to Modify:**
1. app/services/webhook_service.py:67
2. tests/unit/test_webhook_service.py (add security test)

**Implementation:**
```python
import secrets

async def validate_signature(self, payload: str, signature: str) -> bool:
    expected = hmac.new(
        self.secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()
    # Use constant-time comparison to prevent timing attacks
    return secrets.compare_digest(expected, signature)
```

### Testing Strategy

**New Tests Required:**
1. Unit test for correct signature validation
2. Unit test for incorrect signature validation
3. Security test documenting timing attack prevention

**Regression Tests:**
- Verify existing webhook tests still pass
- Add integration test with real webhook payloads

### Prevention Strategy

**Immediate:**
- Fix this instance
- Search codebase for similar patterns
- Add security test

**Long-term:**
- Add to security-best-practices.md
- Include in code review checklist
- Add linter rule if possible
- Security training for team

---

## Related Issues

**Similar Patterns in Codebase:**
```bash
# Search for other unsafe comparisons
rg "signature.*==" app/ src/
rg "token.*==" app/ src/
```

**Found:**
- app/services/api_auth.py:89 - Also needs fixing
- app/utils/validators.py:45 - Also needs fixing

**Recommendation:** Fix all instances in same PR

---

## Recommendations

### Immediate Actions
1. Implement fix using `secrets.compare_digest()`
2. Add security tests
3. Search for similar patterns
4. Create hotfix PR
5. Deploy to production ASAP

### Follow-up Actions
1. Update security-best-practices.md
2. Add to code review checklist
3. Security audit of authentication code
4. Team training on timing attacks

### Process Improvements
1. Require security review for authentication changes
2. Add security-focused linter rules
3. Include timing attack tests in template
4. Document in CLAUDE.md

---

## Fix Plan

**See:** `.agents/plans/fix-issue-{number}.md`

**Tasks:**
1. Fix webhook_service.py signature comparison
2. Fix api_auth.py token comparison
3. Fix validators.py secret comparison
4. Add security tests
5. Update security-best-practices.md
6. Run full security audit

**Estimated Duration:** 2 hours

**Priority:** HIGH

---

## Approval

**RCA Complete:** ✅
**Root Cause Identified:** ✅
**Solution Designed:** ✅
**Prevention Plan:** ✅

**Ready to implement fix:** YES

**Next Step:** `/implement-fix .agents/rca/issue-{number}.md`
```

---

## RCA Checklist

- [ ] Gathered all issue information
- [ ] Reproduced the issue (if possible)
- [ ] Investigated relevant code
- [ ] Reviewed recent changes (git log)
- [ ] Identified root cause
- [ ] Assessed impact and severity
- [ ] Designed solution
- [ ] Identified similar patterns
- [ ] Planned prevention strategy
- [ ] Documented in `.agents/rca/`
- [ ] Ready to implement fix

---

## Remember

"Fix the cause, not the symptom" - Understanding WHY prevents repeat issues.
