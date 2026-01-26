---
name: commit
description: Semantic commit workflow with proper message formatting and Co-Authored-By attribution.
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Commit Command

**Semantic commit workflow with proper formatting.**

---

## Purpose

Create well-formatted git commits following semantic conventions with proper attribution.

---

## Process

### Step 1: Review Changes

```bash
git status
git diff HEAD --name-only
git diff --stat
```

### Step 2: Analyze Changes

Determine:
- Type of change (feat, fix, docs, style, refactor, test, chore)
- Scope (which module/feature affected)
- Summary of what changed and why

### Step 3: Create Commit Message

Format:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes bug nor adds feature
- `test`: Adding tests
- `chore`: Maintenance tasks

### Step 4: Stage and Commit

```bash
git add <specific-files>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Rules

- **NEVER** include "claude code" or "written by claude code" in messages
- **ALWAYS** add Co-Authored-By footer
- **ALWAYS** use specific file staging (not `git add -A`)
- **NEVER** commit secrets or credentials
- **NEVER** skip pre-commit hooks unless explicitly requested

---

## Example

```bash
git commit -m "$(cat <<'EOF'
feat(webhooks): add signature validation for HubSpot webhooks

- Implement HMAC signature verification
- Add timing-safe comparison to prevent attacks
- Include comprehensive test coverage

Refs PRO-123

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

---

## Remember

- Focus on the "why" not just the "what"
- Keep subject line under 72 characters
- Separate subject from body with blank line
- Reference issue/ticket numbers in footer
