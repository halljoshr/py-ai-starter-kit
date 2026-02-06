---
name: commit
description: Semantic commit workflow with proper message formatting.
disable-model-invocation: true
allowed-tools: Bash(git:*)
---

# Commit Command

**Semantic commit workflow with proper formatting.**

---

## Purpose

Create well-formatted git commits following semantic conventions. AI is a tool that assists you - the developer retains full authorship and responsibility for all code changes.

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

<footer>
EOF
)"
```

---

## Rules

- **NEVER** include "claude code", "AI-generated", "written by claude code", or any AI attribution in messages
- **NEVER** add Co-Authored-By footer for AI - the developer is the sole author
- **ALWAYS** use specific file staging (not `git add -A`)
- **NEVER** commit secrets or credentials
- **NEVER** skip pre-commit hooks unless explicitly requested
- **REMEMBER**: AI is a tool like an IDE or linter - it assists but does not author code

---

## Example

```bash
git commit -m "$(cat <<'EOF'
feat(webhooks): add signature validation for HubSpot webhooks

- Implement HMAC signature verification
- Add timing-safe comparison to prevent attacks
- Include comprehensive test coverage

Refs PRO-123
EOF
)"
```

---

## Remember

- Focus on the "why" not just the "what"
- Keep subject line under 72 characters
- Separate subject from body with blank line
- Reference issue/ticket numbers in footer
