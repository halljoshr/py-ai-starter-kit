# Git Workflow

Git best practices and workflow for this project.

---

## Branch Strategy

```
main (protected) ←── PR ←── dev ←── PR ←── feature/your-feature
```

**Branches:**
- `main` - Production-ready code
- `dev` - Integration branch for features
- `feature/*` - New features (e.g., `feature/pro-266-webhook-validation`)
- `fix/*` - Bug fixes (e.g., `fix/issue-42-timing-attack`)

---

## Daily Workflow

```bash
# 1. Start from dev
git checkout dev
git pull origin dev

# 2. Create feature branch
git checkout -b feature/pro-XXX-feature-name

# 3. Make changes + tests
# ... develop ...

# 4. Commit (use /commit command)
/commit

# 5. Push
git push origin feature/pro-XXX-feature-name

# 6. Create PR to dev
gh pr create --base dev
```

---

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:**
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code restructuring
- `test` - Adding tests
- `docs` - Documentation
- `chore` - Maintenance

**Example:**
```
feat(webhooks): add signature validation

- Implement v1, v2, v3 signature support
- Use AWS Secrets Manager for API keys
- Add comprehensive test coverage

Closes PRO-171

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

---

## CHANGELOG.md Maintenance

### When to Update

**During PR Creation (REQUIRED):**
- Add entry to `[Unreleased]` section
- Include PRO-XXX ticket reference
- Describe user-facing changes

**At Release:**
- Move `[Unreleased]` items to new version section
- Update version in pyproject.toml

### Format

```markdown
## [Unreleased]

### Added
- HubSpot webhook signature validation (PRO-171, #5)
  - Supports v1, v2, v3 signature formats
  - AWS Secrets Manager integration

### Fixed
- Timing attack vulnerability in signature comparison (PRO-172, #6)
```

---

## Pull Request Workflow

```bash
# Create PR to dev
gh pr create --base dev --title "feat: add webhook validation" --body "..."

# After approval, merge (squash or merge commit)
# GitHub will auto-close with "Fixes #123" in commits

# Delete branch after merge
git branch -d feature/pro-XXX-feature-name
git push origin --delete feature/pro-XXX-feature-name
```

---

## Common Commands

```bash
# Status
git status

# See changes
git diff
git diff --staged

# Recent commits
git log -10 --oneline

# Undo uncommitted changes
git checkout -- file.py

# Amend last commit (if not pushed)
git commit --amend

# Stash changes
git stash
git stash pop
```

---

## Best Practices

✅ **DO:**
- Pull dev before creating branch
- Commit frequently with clear messages
- Run `/validate` before committing
- Update CHANGELOG.md
- Squash fixup commits before PR
- Delete branches after merge

❌ **DON'T:**
- Commit secrets
- Force push to main/dev
- Commit without validation
- Use vague messages ("fix stuff")
- Push directly to main

---

## References

- [Conventional Commits](https://www.conventionalcommits.org/)
- [Git Best Practices](https://git-scm.com/book/en/v2)
