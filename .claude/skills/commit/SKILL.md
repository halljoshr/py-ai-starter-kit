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

### Step 3: Extract Ticket Reference from Branch Name

Run `git branch --show-current` and extract the ticket number from the branch name.

**Pattern:** Look for a ticket identifier in the branch name — typically a prefix followed by a number, separated by hyphens or slashes.

**Examples:**
- `feature/pro-60-module-7-loan-calculator` → `Refs PRO-60`
- `hotfix/JIRA-1234-fix-login` → `Refs JIRA-1234`
- `feature/ticket-99-add-search` → `Refs TICKET-99`
- `fix/gh-42-typo` → `Refs GH-42`

**Rule:** Extract the first segment that matches `<letters>-<digits>` and uppercase the prefix. If no ticket pattern is found, omit the Refs footer and ask the user if they want to add one.

### Step 4: Create Commit Message

Format:
```
<type>(<scope>): <subject>

<body>

Refs <TICKET-NUMBER>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation only
- `style`: Formatting, no code change
- `refactor`: Code change that neither fixes bug nor adds feature
- `test`: Adding tests
- `chore`: Maintenance tasks

**Subject line:**
- Imperative mood ("add", "fix", "update" — not "added", "fixes", "updates")
- Under 72 characters
- Lowercase after the colon
- No period at the end

**Body:**
- Focus on the "why" not just the "what"
- Explain what changed and what problem it solves
- Use bullet points for multiple changes (prefix with `- `)
- Wrap at 100 characters

### Step 5: Stage and Commit

```bash
git add <specific-files>
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

Refs <TICKET-NUMBER>
EOF
)"
```

---

## Rules

- **NEVER** include "claude code", "AI-generated", "written by claude code", or any AI attribution in messages
- **NEVER** add `Co-Authored-By` footer for AI — the developer is the sole author
- **ALWAYS** use specific file staging (not `git add -A` or `git add .`)
- **NEVER** commit secrets, credentials, `.env` files, or API keys
- **NEVER** skip pre-commit hooks unless explicitly requested
- **ALWAYS** extract ticket reference from branch name when available
- **ALWAYS** use HEREDOC syntax for multi-line commit messages
- **REMEMBER**: AI is a tool like an IDE or linter — it assists but does not author code

---

## Example

Given branch `feature/pro-123-hubspot-webhooks`:

```bash
git add src/webhooks/validate.ts src/webhooks/validate.test.ts
git commit -m "$(cat <<'EOF'
feat(webhooks): add signature validation for HubSpot webhooks

Implement HMAC signature verification to ensure webhook payloads
are authentic and untampered.

Changes:
- Add HMAC signature verification using timing-safe comparison
- Reject requests with missing or invalid signatures
- Add comprehensive test coverage for valid/invalid/missing cases

Refs PRO-123
EOF
)"
```

---

## Remember

- Focus on the "why" not just the "what"
- Keep subject line under 72 characters
- Separate subject from body with blank line
- The `Changes:` section is optional but useful for multi-file commits
- If pre-commit hooks fail, fix the issue and create a NEW commit (never amend)
