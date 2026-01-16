# CHANGELOG Best Practices

Maintaining an up-to-date CHANGELOG is **mandatory** for all feature development and bug fixes. The CHANGELOG serves as the primary source of truth for what has changed between versions and provides critical context for internal developers.

---

## When to Update the CHANGELOG

### During PR Creation (REQUIRED)

- Before creating a pull request, you **must** add an entry to the `[Unreleased]` section of `CHANGELOG.md`
- The CHANGELOG entry should be part of your PR and reviewed alongside code changes
- Reviewers should verify that the CHANGELOG entry accurately describes the changes

### At Release Time

- When cutting a new release, move all `[Unreleased]` items to a new dated version section
- Update `pyproject.toml` with the new version number
- Add version comparison links at the bottom of CHANGELOG.md
- Commit with message format: `Release v0.X.0`

---

## What to Include

### ✅ DO Include

- New features and capabilities
- Changes to existing functionality
- Major bug fixes that affected team workflows
- Infrastructure changes (Lambda deployment, testing framework, CI/CD)
- Breaking API changes
- Security fixes
- Database schema changes
- Performance improvements with measurable impact
- New integrations with external services

### ❌ DO NOT Include

- Pure code refactoring with no functional impact
- Minor typo fixes in code comments
- Work-in-progress commits that were superseded by later work
- Documentation-only updates (unless significant, like API docs)
- Internal variable renames or code organization
- Dependency version bumps (unless they enable new features or fix bugs)

---

## How to Format Entries

### Category Structure

Use these categories in order:
- **Added** - New features and capabilities
- **Changed** - Changes to existing functionality
- **Fixed** - Bug fixes
- **Security** - Security-related changes
- **Infrastructure** - Deployment, CI/CD, testing framework changes
- **Developer Experience** - Tooling and DX improvements

### Entry Format

```markdown
### Category
- Brief outcome-focused description (PRO-XXX, #PR)
  - Sub-detail 1 (if complex feature)
  - Sub-detail 2
  - Sub-detail 3 (max 2-4 bullets)
```

### Key Formatting Rules

1. **Always include** both Linear ticket reference (PRO-XXX) **and** PR number (#X)
2. **Main line**: 1-2 sentence outcome-focused description
3. **Sub-bullets**: Optional, use only for complex features (max 2-4)
4. **Focus on "why" and "what it enables"**, not implementation details
5. **Be technical** - audience is 99% internal developers
6. **Keep it scannable** - reader should grasp changes quickly

---

## Good vs Bad Examples

### ✅ GOOD Examples

**Example 1: Feature with Context**
```markdown
### Added
- HubSpot webhook signature validation supporting v1, v2, and v3 formats (PRO-171, #5)
  - Validates signatures using SHA-256 HMAC with proper URI encoding
  - Integrates with AWS Secrets Manager for secure API key retrieval
  - Includes 15+ test cases covering all signature versions and edge cases
```
*Why it's good*: Outcome-focused, technical but clear, includes ticket and PR, explains what was built and why it matters.

**Example 2: Infrastructure Improvement**
```markdown
### Infrastructure
- Comprehensive pytest testing framework with tiered dataset validation (PRO-127, #4)
  - Smoke tests with mock data for fast CI checks (<1 second)
  - Sample dataset tests for development branch merges (1-30 seconds)
  - Golden dataset tests for production deployments (>30 seconds)
  - Achieved 90% code coverage with branch coverage enabled
```
*Why it's good*: Explains the impact, provides context about the testing tiers, quantifies the improvement.

**Example 3: Bug Fix**
```markdown
### Fixed
- Heron Data deal pulling logic that was incorrectly skipping test scenarios (PRO-127)
  - Resolved issue where deals with certain status codes were not being processed
  - Ensures all test cases now execute correctly
```
*Why it's good*: Describes the problem and the fix's impact, not just "fixed a bug".

---

### ❌ BAD Examples

**Example 1: Too Vague**
```markdown
### Added
- HubSpot webhooks (PRO-171)
```
*Why it's bad*: Doesn't explain what was added, why, or what it enables. No PR reference. Not scannable.

**Example 2: Too Granular (Commit-Level)**
```markdown
### Changed
- refs PRO-171 created the handler for the real hubspot webhook requests and changed from stageName to stageId
- refs PRO-171 I have the first version running in lambda with a SAM deployment
- refs PRO-171 Updated to use secrets manager and add the documentation. Currently the data is just logged
- refs PRO-171 Fixed warnings in pytest
```
*Why it's bad*: This is commit-level detail that should be grouped into one feature-level entry. Not outcome-focused.

**Example 3: Too Implementation-Focused**
```markdown
### Changed
- Refactored webhook validator class to use composition over inheritance
- Moved secret loading from request handler to __init__ method
- Renamed variable `sig` to `signature` for clarity
- Updated type hints to use pydantic BaseModel
```
*Why it's bad*: Pure implementation details with no explanation of impact or outcome. These shouldn't be in CHANGELOG.

**Example 4: Missing Context**
```markdown
### Fixed
- Fixed issue with Heron integration
```
*Why it's bad*: No ticket/PR reference, no detail about what was broken or how it was fixed.

---

## Workflow Integration

### During Development

```bash
# 1. Create feature branch
git checkout dev
git pull origin dev
git checkout -b feature/pro-xxx-your-feature

# 2. Develop and commit normally
# ... make changes ...
git add .
git commit -m "feat(webhooks): add signature validation"

# 3. Before creating PR: Update CHANGELOG
# Edit CHANGELOG.md and add entry under [Unreleased]
```

**CHANGELOG Entry Example**:
```markdown
## [Unreleased]

### Added
- HubSpot webhook signature validation supporting v1, v2, and v3 formats (PRO-171, #TBD)
  - Validates signatures using SHA-256 HMAC with proper URI encoding
  - Integrates with AWS Secrets Manager for secure API key management
```

```bash
# 4. Commit CHANGELOG update
git add CHANGELOG.md
git commit -m "docs: update CHANGELOG for webhook validation feature"

# 5. Push and create PR
git push origin feature/pro-xxx-your-feature
# Create PR via GitHub - add PR number to CHANGELOG entry after PR is created

# 6. Update CHANGELOG with PR number
# Edit CHANGELOG.md to replace #TBD with actual PR number
git add CHANGELOG.md
git commit -m "docs: add PR number to CHANGELOG"
git push
```

---

### At Release Time

```bash
# 1. Ensure you're on dev with all changes merged
git checkout dev
git pull origin dev

# 2. Edit CHANGELOG.md
# - Move [Unreleased] items to new [0.X.0] - YYYY-MM-DD section
# - Update version comparison links at bottom
# - Leave [Unreleased] section empty for future work

# 3. Update pyproject.toml version
# Change: version = "0.4.0" -> version = "0.5.0"

# 4. Commit release changes
git add CHANGELOG.md pyproject.toml
git commit -m "Release v0.5.0"

# 5. Merge to main and tag (if doing releases)
git push origin dev
# Create PR to main if needed, or merge directly depending on workflow
```

**Example Version Section After Release**:
```markdown
## [Unreleased]

## [0.5.0] - 2025-12-20

### Added
- HubSpot webhook signature validation supporting v1, v2, and v3 formats (PRO-171, #5)
  - Validates signatures using SHA-256 HMAC with proper URI encoding
  - Integrates with AWS Secrets Manager for secure API key retrieval

[Unreleased]: https://github.com/Newity-LLC/uw-portal-api/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/Newity-LLC/uw-portal-api/compare/v0.4.0...v0.5.0
```

---

## Grouping Related Commits

When multiple commits contribute to a single feature, group them into **one logical entry**:

**Multiple Commits** (from git log):
```
3ec3909 refs PRO-171 I have the first version running in lambda with SAM
4248a91 refs PRO-171 created the handler for real hubspot webhook requests
601841d refs PRO-171 Updated to use secrets manager and add documentation
661d117 refs PRO-171 Fixed warnings in pytest
```

**Single CHANGELOG Entry**:
```markdown
### Added
- HubSpot webhook integration with AWS Lambda deployment (PRO-171, #5)
  - Signature validation with AWS Secrets Manager integration
  - SAM deployment configuration
  - Comprehensive test coverage
```

---

## Tips for Writing Great Entries

1. **Use Active Voice**: "Add feature X" not "Feature X was added"
2. **Be Specific**: "Add HubSpot webhook validation" not "Add webhooks"
3. **Explain Impact**: What does this enable? What problem does it solve?
4. **Stay Technical**: Audience is developers - use proper terminology
5. **Link Everything**: Always include (PRO-XXX, #PR) references
6. **Think Features, Not Files**: Group related changes by user-facing feature
7. **Test Your Description**: If someone reads only this entry, would they understand the change?

---

## Checklist for PR Reviews

### For Authors
- [ ] CHANGELOG entry added to `[Unreleased]` section
- [ ] Entry includes both Linear ticket (PRO-XXX) and PR number (#X)
- [ ] Description is outcome-focused, not implementation-focused
- [ ] Related commits are grouped into single logical entry
- [ ] Entry is in the correct category (Added, Changed, Fixed, etc.)
- [ ] Sub-bullets used only for complex features (max 2-4)

### For Reviewers
- [ ] CHANGELOG entry exists and is in correct format
- [ ] Entry accurately describes the changes in the PR
- [ ] Ticket and PR references are present and correct
- [ ] Description would be clear to other developers
- [ ] Entry is appropriately detailed (not too vague, not too granular)

---

## Common Questions

**Q: Should I update CHANGELOG for every commit?**
A: No, only update when creating a PR. Group related commits into one entry.

**Q: What if I'm just refactoring code with no functional changes?**
A: Don't add to CHANGELOG unless it impacts performance, testing, or developer workflow.

**Q: How detailed should entries be?**
A: 1-2 line summary is usually enough. Add 2-4 sub-bullets only for complex features.

**Q: What if my PR fixes multiple unrelated issues?**
A: Add separate CHANGELOG entries for each distinct change, each with its own ticket reference.

**Q: When do we bump versions?**
A: Coordinate with team lead. Generally when releasing to a new environment or hitting a milestone.

**Q: Do I need to update CHANGELOG for documentation-only changes?**
A: Usually no, unless it's significant (like new API documentation or major README overhaul).

---

## Automated Version Check

GitHub Actions automatically enforces version bumps on PRs to `dev` and `main`:

- **Blocks merge** if version in `pyproject.toml` hasn't changed
- **Verifies CHANGELOG** contains the new version number
- **Can be bypassed** by adding `skip-version-check` label (use sparingly for WIP/docs PRs)

**If CI fails with "Version must be bumped":**
1. Update version in `pyproject.toml` (patch/minor/major)
2. Move `[Unreleased]` to `[X.X.X] - YYYY-MM-DD` in CHANGELOG.md
3. Push changes and CI will pass

**When to skip the check:**
- Work-in-progress PRs (not ready for merge)
- Documentation-only changes
- Repository configuration updates

To add the bypass label: Go to your PR → Labels → Add `skip-version-check`
