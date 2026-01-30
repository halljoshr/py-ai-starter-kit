---
name: code-review
description: AI-driven code review before committing. Reviews logic, security, performance, quality, and standards.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Write, Bash(git:*)
---

# Code Review Command

**AI-driven code review before committing.**

---

## Purpose

Perform comprehensive code review across five dimensions: Logic, Security, Performance, Quality, and Standards.

---

## Review Process

### Step 1: Establish Context

```bash
cat CLAUDE.md
cat README.md
git status
git diff HEAD --name-only
```

### Step 2: Analyze Full Files

- Read complete files (not just diffs)
- Understand surrounding context
- Check for ripple effects

### Step 3: Run Complexity Analysis

```bash
# Analyze code complexity metrics
uv run python .claude/skills/code-review/scripts/analyze_complexity.py app/ src/
```

This provides:
- Cyclomatic complexity per function
- Functions exceeding complexity thresholds (>10, >15)
- File length warnings (>500 lines)
- Import count analysis
- Refactoring recommendations

Review the output to identify high-complexity code requiring special attention.

### Step 4: Evaluate on Five Dimensions

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

**Comprehensive Security Review:** Consult `references/security-checklist.md` for OWASP-aligned security patterns, including:
- Input validation patterns
- Authentication/Authorization best practices
- Password storage, JWT security, API key management
- Path traversal prevention
- Error message security
- CORS configuration
- Cryptography best practices
- File upload validation

#### 3. Performance
- N+1 query problems
- Inefficient algorithms
- Memory leaks
- Unnecessary database calls
- Missing caching opportunities
- Blocking I/O in async code

#### 4. Quality
- DRY violations
- Function complexity (review complexity analysis results from Step 3)
- Variable naming clarity
- Type annotations completeness
- Documentation/docstrings
- Code duplication

**Note:** Use complexity analysis output from Step 3 to identify functions requiring refactoring (complexity > 10).

#### 5. Standards
- CLAUDE.md adherence
- Testing requirements met
- Naming conventions
- File structure
- Error handling patterns

---

## Output Format

Save to: `.agents/code-reviews/{feature-name}-review-{date}.md`

Include:
- Summary with issue counts by severity
- Detailed issues with file:line, severity, category
- Problematic code and fix examples
- Positive observations
- Recommendations (Must Fix / Should Fix / Nice to Have)
- Standards compliance checklist
- Overall assessment (Approve / Request Changes / Reject)

---

## Severity Levels

- **CRITICAL**: Security vulnerabilities, data loss risks
- **HIGH**: Logic errors, missing error handling
- **MEDIUM**: Performance issues, code quality
- **LOW**: Style issues, minor improvements

---

## Remember

"The best code is often the code you don't write" - Simplicity over cleverness.
