---
name: rca
description: Root Cause Analysis - Systematic bug investigation before fixing.
disable-model-invocation: true
argument-hint: "{issue-number}"
allowed-tools: Read, Glob, Grep, Write, Bash(git:*), Bash(gh:*)
---

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

Collect all available information:
- Issue description
- Steps to reproduce
- Expected vs actual behavior
- Error messages/stack traces
- Environment (dev/staging/prod)
- When it started occurring

```bash
gh issue view {issue-number}
```

### Phase 2: Code Investigation

```bash
rg "exact error message" app/ src/
rg "function_name" app/ src/ -A 5
```

Read relevant files completely (not just grep results).

### Phase 3: Historical Analysis

```bash
git log --oneline -- path/to/file.py | head -20
git log --since="2 weeks ago" --oneline --grep="relevant_keyword"
git show {commit-hash}
```

### Phase 4: Root Cause Determination

Identify the actual cause:
- Input validation failure?
- Unhandled edge case?
- Race condition?
- Missing error handling?
- Incorrect business logic?
- External service failure?
- Data migration issue?

### Phase 5: Impact Evaluation

Assess scope:
- How many users affected?
- What features broken?
- Data integrity issues?
- Security implications?

### Phase 6: Solution Design

Plan the fix:
- What files need modification?
- What tests need to be added?
- How to prevent recurrence?
- Rollback plan if needed?

---

## Output Format

Save to: `.agents/rca/issue-{number}-{date}.md`

Include:
- Issue Summary
- Investigation details
- Root Cause analysis
- Impact Assessment
- Solution Design
- Prevention Strategy
- Related Issues
- Fix Plan

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
