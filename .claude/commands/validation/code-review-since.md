# Code Review Since Command

**Enhanced code review that accepts a git reference to review changes since a specific commit or branch.**

---

## Purpose

Perform comprehensive code review across five dimensions (Logic, Security, Performance, Quality, and Standards) for all changes since a specified git reference.

This is useful for:
- Reviewing entire feature branches before merging to dev/main
- Reviewing changes since the last release
- Reviewing work across multiple commits
- Pre-merge validation

---

## Usage

```bash
/code-review-since [git-ref]
```

**Parameters:**
- `git-ref` (optional): Git reference to compare against. Defaults to `origin/dev`

**Examples:**
```bash
/code-review-since origin/dev          # Review all changes since dev
/code-review-since main                # Review all changes since main
/code-review-since HEAD~3              # Review last 3 commits
/code-review-since abc123              # Review since specific commit
/code-review-since v1.2.0              # Review since tag
/code-review-since                     # Defaults to origin/dev
```

---

## Review Process

### Step 1: Parse Arguments and Establish Context

```bash
# Parse git reference (default: origin/dev)
GIT_REF="${1:-origin/dev}"

# Validate git reference exists
git rev-parse --verify "$GIT_REF" > /dev/null 2>&1

# Read core documentation
cat CLAUDE.md
cat README.md

# Get current branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
```

### Step 2: Identify Changed Files

```bash
# Get list of changed files since git reference
git diff --name-only "$GIT_REF"...HEAD

# Show summary statistics
echo "Reviewing changes from $GIT_REF to HEAD"
echo "Branch: $CURRENT_BRANCH"
echo "Files changed: $(git diff --name-only "$GIT_REF"...HEAD | wc -l)"
echo "Lines added: $(git diff --stat "$GIT_REF"...HEAD | tail -1)"
```

### Step 3: Analyze Full Files

For each changed file:
- Read the **complete current file** (not just diffs)
- Understand surrounding context
- Check imports and dependencies
- Verify function/class relationships
- Look for ripple effects

**Important:** Always read full files to understand context, not just the diff lines.

### Step 4: Analyze Diff Context

```bash
# Get the actual changes with context
git diff "$GIT_REF"...HEAD

# For each file, understand:
# - What was added (+ lines)
# - What was removed (- lines)
# - Why the change was made (commit messages)
```

### Step 5: Evaluate on Five Dimensions

#### 1. Logic ✅
- Correctness of algorithms
- Off-by-one errors
- Edge case handling
- Null/None checks
- Error handling completeness
- Race conditions
- Type conversion safety
- Conditional logic correctness

#### 2. Security 🔒 (CRITICAL flag for issues)
- SQL injection vulnerabilities
- XSS vulnerabilities
- Insecure data handling
- Exposed credentials/secrets
- Improper authentication/authorization
- Missing input validation
- Command injection risks
- Path traversal vulnerabilities

#### 3. Performance ⚡
- N+1 query problems
- Inefficient algorithms (O(n²) when O(n) possible)
- Memory leaks
- Unnecessary database calls
- Missing caching opportunities
- Blocking I/O in async code
- Large data structure copies
- Inefficient loops

#### 4. Quality 📊
- DRY violations (code duplication)
- Function complexity (cyclomatic complexity)
- Variable naming clarity
- Type annotations completeness
- Documentation/docstrings
- Code readability
- Magic numbers/strings
- Consistent patterns

#### 5. Standards 📏
- CLAUDE.md adherence
- Testing requirements met (80% coverage)
- Naming conventions (snake_case, PascalCase)
- File structure (max 500 lines)
- Function length (max 100 lines)
- Line length (max 100 characters)
- Error handling patterns
- Logging practices

---

## Output Format

Save to: `.agents/code-reviews/{feature-name}-since-{git-ref}-review-{date}.md`

```markdown
# Code Review: {Feature Name} (Since {git-ref})

**Reviewed:** {Date and Time}
**Branch:** {current branch}
**Comparing:** {git-ref}...HEAD
**Commits Reviewed:** {count}
**Reviewer:** Claude Sonnet 4.5

---

## Summary

**Git Range:** `{git-ref}...HEAD`
**Files Changed:** {count}
**Lines Added:** +{count}
**Lines Removed:** -{count}

**Issues Found:** {count}
- Critical: {count} 🔴
- High: {count} 🟠
- Medium: {count} 🟡
- Low: {count} 🟢

**Overall Assessment:** Approve ✅ / Request Changes ⚠️ / Reject ❌

---

## Commit History

{List of commits in range with one-line summaries}

```
abc123 Refs PRO-XXX Added prescreen_id validation
def456 Refs PRO-XXX Updated workflow manager
ghi789 Refs PRO-XXX Added tests for validation
```

---

## Files Changed

| File | +Lines | -Lines | Status |
|------|--------|--------|--------|
| src/nodes/validate_risk_data.py | +16 | -3 | ✅ Reviewed |
| src/graph/workflows.py | +10 | -2 | ✅ Reviewed |
| app/services/workflow_manager.py | +38 | -10 | ✅ Reviewed |
| tests/manual/test_risk_validation.py | +67 | -0 | ✅ Reviewed |

---

## Issues

{Same issue format as regular code-review}

### Issue 1: [CRITICAL] {Title}

**File:** {file}:{line}
**Severity:** CRITICAL 🔴
**Category:** Security

**Problem:**
{Description}

**Code:**
```python
{problematic code}
```

**Fix:**
```python
{corrected code}
```

**Impact:** {Impact description}

---

## Positive Observations

✅ {List of good practices found}

---

## Recommendations

### Must Fix (Before Merge)
- {Critical and High severity issues}

### Should Fix (This PR)
- {Medium severity issues}

### Nice to Have (Future)
- {Low severity improvements}

---

## Standards Compliance

**CLAUDE.md Adherence:**
- ✅ File length < 500 lines
- ✅ Function length < 100 lines
- ✅ Line length ≤ 100 characters
- ✅ Testing coverage ≥ 80%
- ✅ Proper naming conventions

**Git Commit Quality:**
- ✅ Semantic commit messages (feat/fix/docs/refactor)
- ✅ Linear ticket references (PRO-XXX)
- ✅ Logical commit grouping

---

## Testing Impact

**Test Files Modified:** {count}
**Test Coverage Change:** {before}% → {after}%

**Recommended Test Commands:**
```bash
# Run affected tests
uv run python scripts/run-relevant-tests.py {git-ref}...HEAD --branch=dev --coverage

# Run full test suite
uv run pytest --cov=app --cov=src --cov-fail-under=80
```

---

## Overall Assessment

**Recommendation:** {APPROVE / REQUEST CHANGES / REJECT}

**Rationale:**
{Explanation of decision}

**Confidence Level:** {1-10}/10

**Next Steps:**
1. {Action items}
2. {Required fixes}
3. {Testing commands}

---

## Review Metadata

**Git Reference Range:** `{git-ref}...HEAD`
**Commits in Range:** {commit hashes}
**Review Duration:** ~{estimated time}
**Lines of Code Reviewed:** {total lines}
```

---

## Implementation Notes

### How to Get Changed Files

```bash
# List files changed between git-ref and HEAD
git diff --name-only "$GIT_REF"...HEAD

# Get detailed diff
git diff "$GIT_REF"...HEAD

# Get stat summary
git diff --stat "$GIT_REF"...HEAD

# Get commit list
git log --oneline "$GIT_REF"..HEAD
```

### How to Read Full Files

For each changed file in the diff:

```bash
# Read the complete current file (HEAD version)
cat {file_path}

# Or use Read tool
Read(file_path)
```

### How to Handle Large Diffs

If the diff is very large (>20 files or >1000 lines):

1. **Group by category**: Review services, then nodes, then tests
2. **Prioritize critical paths**: Review security-sensitive code first
3. **Sample representative files**: Review 3-5 files thoroughly per category
4. **Summarize patterns**: Look for repeated issues across files

---

## Examples

### Example 1: Review Since Dev Branch

```bash
/code-review-since origin/dev
```

**Output:**
```
Reviewing changes from origin/dev to HEAD
Branch: feature/pro-266-create-queue-for-hubspot-triggers
Files changed: 4
Commits: 3
Lines added: +131, Lines removed: -15

Generating comprehensive code review...
✓ Read CLAUDE.md
✓ Identified 4 changed files
✓ Analyzed full files
✓ Checked logic, security, performance, quality, standards
✓ Saved review to .agents/code-reviews/webhook-queue-since-dev-review-2026-01-20.md

Assessment: APPROVE ✅
Issues found: 0 Critical, 0 High, 0 Medium, 2 Low
```

### Example 2: Review Last 3 Commits

```bash
/code-review-since HEAD~3
```

**Output:**
```
Reviewing changes from HEAD~3 to HEAD
Branch: feature/pro-284-risk-score-validation
Files changed: 2
Commits: 3
Lines added: +45, Lines removed: -8

Generating code review...
✓ Complete

Assessment: REQUEST CHANGES ⚠️
Issues found: 0 Critical, 1 High, 1 Medium, 0 Low
```

### Example 3: Review Since Specific Commit

```bash
/code-review-since abc123def
```

---

## Git Reference Examples

### Common References

| Reference | Description | Example |
|-----------|-------------|---------|
| `origin/dev` | Remote dev branch | `/code-review-since origin/dev` |
| `origin/main` | Remote main branch | `/code-review-since origin/main` |
| `dev` | Local dev branch | `/code-review-since dev` |
| `HEAD~3` | 3 commits ago | `/code-review-since HEAD~3` |
| `abc123` | Specific commit hash | `/code-review-since abc123` |
| `v1.2.0` | Git tag | `/code-review-since v1.2.0` |

### Three-dot vs Two-dot Syntax

```bash
# Three-dot (recommended): Changes on current branch since diverging
git diff origin/dev...HEAD

# Two-dot: All changes between two points
git diff origin/dev..HEAD
```

**Use three-dot (`...`) for branch comparisons** to see only the changes made on your branch.

---

## Checklist

Before completing review:

- [ ] Validated git reference exists
- [ ] Read CLAUDE.md and README
- [ ] Identified all changed files
- [ ] Read complete files (not just diffs)
- [ ] Reviewed commit messages
- [ ] Checked logic correctness
- [ ] Checked security vulnerabilities
- [ ] Checked performance issues
- [ ] Checked code quality
- [ ] Checked standards compliance
- [ ] Documented all issues with severity
- [ ] Provided specific fix recommendations
- [ ] Calculated test coverage impact
- [ ] Saved review to `.agents/code-reviews/`
- [ ] Provided clear next steps

---

## Success Criteria

A successful code review:

✅ **Comprehensive** - Reviews all changed files and their context
✅ **Actionable** - Provides specific fixes with code examples
✅ **Prioritized** - Issues are categorized by severity
✅ **Objective** - Based on standards, not opinions
✅ **Constructive** - Highlights positives and negatives
✅ **Complete** - Includes next steps and testing recommendations

---

## Remember

- **Read full files, not just diffs** - Context matters
- **Understand the "why"** - Check commit messages
- **Be thorough but practical** - Focus on high-impact issues
- **Provide examples** - Show both problem and solution
- **Think like a reviewer** - Would you approve this PR?

"Code review is not about finding every tiny issue. It's about ensuring the code is correct, secure, maintainable, and meets standards."
