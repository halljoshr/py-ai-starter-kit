# Commit Command

**Create semantic commits with proper formatting.**

---

## Purpose

Create well-formatted, semantic commits that:
- Follow conventional commits format
- Have clear, descriptive messages
- Reference related issues/PRs
- Credit Claude appropriately
- Follow project git workflow

---

## Process

### Step 1: Gather Changes

```bash
# See current status
git status

# See detailed diff
git diff HEAD

# See recent commit style for consistency
git log -5 --oneline
```

---

### Step 2: Analyze Changes

- Read FULL files that changed (not just diffs)
- Understand the PURPOSE of changes
- Identify the type of change (feat/fix/refactor/etc.)
- Check for any secrets in staged files

---

### Step 3: Draft Commit Message

**Format:**
```
<type>(<scope>): <subject>

<body>

<footer>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring (no functional changes)
- `test` - Adding or updating tests
- `docs` - Documentation only
- `chore` - Maintenance (dependencies, configs)
- `style` - Formatting (no code changes)
- `perf` - Performance improvements

**Scope:** Module/feature affected (optional but recommended)

**Subject:** Short description (50 chars max, no period)

**Body:** Detailed explanation (optional, wrap at 72 chars)
- What changed
- Why it changed
- Any important details

**Footer:** Issue references, breaking changes
- `Fixes #123`
- `Closes PRO-456`
- `BREAKING CHANGE: ...`

---

### Step 4: Verify No Secrets

```bash
# Check for common secret patterns
git diff --cached | rg "(api_key|secret|password|token)"

# Warn if found
```

**NEVER commit:**
- API keys
- Passwords
- Tokens
- Private keys
- .env files (unless .env.example)
- credentials.json
- secrets.yaml

---

### Step 5: Create Commit

```bash
# Add files
git add {files}

# Commit with heredoc for proper formatting
git commit -m "$(cat <<'EOF'
<type>(<scope>): <subject>

<body>

<footer>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"

# Verify commit
git status
git log -1
```

---

## Example Commits

### Feature Addition

```
feat(webhooks): add HubSpot signature validation

- Implement signature validation supporting v1, v2, v3 formats
- Use SHA-256 HMAC with proper URI encoding
- Integrate AWS Secrets Manager for API key retrieval
- Add comprehensive test coverage (25 unit + 8 integration tests)

Closes PRO-171

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

### Bug Fix

```
fix(security): prevent timing attacks in signature validation

- Use secrets.compare_digest() for constant-time comparison
- Applied fix to all similar patterns in codebase
- Add security tests documenting timing attack prevention

Fixes #42

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

### Refactoring

```
refactor(services): extract common HTTP client logic

- Create BaseHTTPService with shared client configuration
- Update webhook_service and hubspot_service to extend base
- Reduce code duplication by 150 lines
- No functional changes

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

### Test Addition

```
test(webhooks): add integration tests for error scenarios

- Add tests for invalid signatures
- Add tests for malformed payloads
- Add tests for timeout scenarios
- Increase coverage from 82% to 91%

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

### Documentation

```
docs(api): update webhook endpoint documentation

- Add signature validation requirements
- Include example payloads
- Document error responses
- Add troubleshooting section

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## Commit Checklist

- [ ] Ran `/validate` and all checks passed
- [ ] Reviewed git diff for accuracy
- [ ] Checked for secrets in staged files
- [ ] Chose appropriate commit type
- [ ] Wrote clear, concise subject line
- [ ] Added body with context (if needed)
- [ ] Referenced issue/PR if applicable
- [ ] Added Co-Authored-By tag
- [ ] Followed conventional commits format
- [ ] Verified commit with `git log -1`

---

## Important Notes

### DO:
- ✅ Follow conventional commits format
- ✅ Reference issues (Fixes #123)
- ✅ Keep subject line under 50 chars
- ✅ Wrap body at 72 chars
- ✅ Use imperative mood ("add" not "added")
- ✅ Include Co-Authored-By tag
- ✅ Validate before committing

### DON'T:
- ❌ Commit secrets or API keys
- ❌ Commit without running `/validate`
- ❌ Use vague messages ("fix stuff")
- ❌ Combine unrelated changes
- ❌ Include "Claude Code" or "written by Claude" in message
- ❌ Push to remote (unless user explicitly requests)

---

## After Committing

1. **Verify commit:**
   ```bash
   git log -1
   git show HEAD
   ```

2. **Update CHANGELOG.md** (separate commit):
   - Add entry under [Unreleased]
   - Include PRO-XXX reference
   - Describe user-facing changes

3. **DO NOT push** unless user explicitly requests

---

## Remember

"Clear commits = clear history" - Future developers (including you) will thank you.
