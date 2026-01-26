---
name: code-review-since
description: Enhanced code review for changes since a specific git reference (commit, branch, or tag).
disable-model-invocation: true
argument-hint: "[git-ref]"
allowed-tools: Read, Glob, Grep, Write, Bash(git:*)
---

# Code Review Since Command

**Enhanced code review for changes since a specific git reference.**

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

## Purpose

Perform comprehensive code review for all changes since a specified git reference. Useful for:
- Reviewing entire feature branches before merging
- Reviewing changes since the last release
- Reviewing work across multiple commits
- Pre-merge validation

---

## Review Process

### Step 1: Identify Changed Files

```bash
git diff --name-only "$GIT_REF"...HEAD
git diff --stat "$GIT_REF"...HEAD
git log --oneline "$GIT_REF"..HEAD
```

### Step 2: Analyze Full Files

For each changed file, read the **complete current file** (not just diffs).

### Step 3: Evaluate on Five Dimensions

Same as `/code-review`:
1. Logic
2. Security (CRITICAL flag)
3. Performance
4. Quality
5. Standards

---

## Output Format

Save to: `.agents/code-reviews/{feature-name}-since-{git-ref}-review-{date}.md`

Includes:
- Git range summary (files changed, lines added/removed)
- Commit history in range
- Issues by severity
- Positive observations
- Standards compliance
- Testing impact
- Overall assessment

---

## Git Reference Examples

| Reference | Description |
|-----------|-------------|
| `origin/dev` | Remote dev branch |
| `origin/main` | Remote main branch |
| `HEAD~3` | 3 commits ago |
| `abc123` | Specific commit |
| `v1.2.0` | Git tag |

---

## Remember

- **Read full files, not just diffs** - Context matters
- **Understand the "why"** - Check commit messages
- **Be thorough but practical** - Focus on high-impact issues
