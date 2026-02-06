# CLAUDE.md

This file provides comprehensive guidance to Claude Code when working with Python code in this repository.

---

## Core Development Philosophy

### KISS (Keep It Simple, Stupid)

Simplicity should be a key goal in design. Choose straightforward solutions over complex ones whenever possible. Simple solutions are easier to understand, maintain, and debug.

### YAGNI (You Aren't Gonna Need It)

Avoid building functionality on speculation. Implement features only when they are needed, not when you anticipate they might be useful in the future.

### Design Principles

- **Dependency Inversion**: High-level modules should not depend on low-level modules. Both should depend on abstractions.
- **Open/Closed Principle**: Software entities should be open for extension but closed for modification.
- **Single Responsibility**: Each function, class, and module should have one clear purpose.
- **Fail Fast**: Check for potential errors early and raise exceptions immediately when issues occur.

---

## ⏱️ Timeline & Estimation Policy

**CRITICAL: Never make timeline assumptions or predictions.**

AI-assisted development moves at different speeds than traditional development. Timelines biased toward human-only development lead to unnecessary deferrals and poor prioritization decisions.

### Rules

**❌ NEVER:**
- Use timeline language: "Week 1-2", "This month", "Q2 2026", "30-60 minutes"
- Make duration predictions: "This will take X days/weeks/months"
- Frame priorities as time periods: "Priority 1 = this quarter"
- Estimate implementation time unless explicitly asked
- Say "defer to next quarter/year"

**✅ ALWAYS:**
- Frame as priorities: "First Priority", "Second Priority", "High/Medium/Low Priority"
- Ask: "When do you need this?" or "What's urgent?"
- Use "now vs later", not "this quarter vs next year"
- Assume AI-assisted development speed (fast iteration)
- Let user determine urgency and timeline

### Examples

**❌ Bad:**
- "Phase 1 will take 1-2 weeks"
- "This is a Q2 2026 goal"
- "Exploration completes in 30-60 minutes"
- "Not critical for Q1, defer to 2027"

**✅ Good:**
- "Phase 1: Core abstractions (First Priority)"
- "When do you need this capability?"
- "Exploration scope: focused vs comprehensive"
- "Is this high priority or can it wait?"

### Rationale

With AI assistance:
- Features that seem "months away" can be days
- "Week 1-2" estimates assume human-only development
- Timeline bias causes artificial deferrals
- User knows their urgency better than AI can predict

**Exception:** Technical performance metrics (e.g., "API responds in 5-10 seconds") are facts, not predictions.

---

## 🧱 Code Structure & Modularity

- **Never create a file longer than 500 lines of code**. If approaching this limit, refactor by splitting into modules.
- **Functions should be under 100 lines** with a single, clear responsibility.
- **Organize code into clearly separated modules**, grouped by feature or responsibility.
- **Line length should be max 100 characters** (enforced by ruff in pyproject.toml)

---

## 🛠️ Development Environment

### UV Package Management

This project uses UV for blazing-fast Python package and environment management.

```bash
# Create virtual environment
uv venv

# Sync dependencies
uv sync

# Add a package (NEVER update pyproject.toml directly!)
uv add requests

# Add development dependency
uv add --dev pytest ruff mypy

# Run commands in the environment
uv run python script.py
uv run pytest
uv run ruff check .
```

### Development Commands

```bash
# Run all tests
uv run pytest

# Run specific test tier
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -m "not very_slow" -v

# Run tests with coverage
uv run pytest --cov=app --cov=src --cov-fail-under=80

# Format code
uv run ruff format .

# Check linting
uv run ruff check .

# Type checking
uv run mypy app/
```

---

## 📋 Style & Conventions

- **Follow PEP8** with line length: 100 characters
- Use double quotes for strings
- **Always use type hints** for function signatures and class attributes
- **Format with `ruff format`** (faster alternative to Black)
- **Use `pydantic` v2** for data validation and settings management

### Naming Conventions

- **Variables and functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private attributes/methods**: `_leading_underscore`

For detailed style guide, see [.claude/reference/style-conventions.md](.claude/reference/style-conventions.md)

---

## 🧪 Testing Strategy

### Three-Tier Test Structure

#### Unit Tests (`tests/unit/`)
- **Purpose:** Test business logic in isolation
- **Speed:** < 1 second per test
- **Mocking:** All I/O operations mocked
- **When to Run:** Every commit, during development

```bash
uv run pytest tests/unit/ -v
```

#### Integration Tests (`tests/integration/`)
- **Purpose:** Test service interactions and API integrations
- **Speed:** 1-30 seconds
- **Mocking:** Minimal - prefer real dependencies where possible
- **When to Run:** Before PR, during CI

```bash
uv run pytest tests/integration/ -m "not very_slow" -v
```

#### E2E Tests (`tests/e2e/`)
- **Purpose:** Test complete user workflows end-to-end
- **Speed:** > 30 seconds
- **Mocking:** None - real system behavior
- **When to Run:** Before merge to main, before releases

```bash
uv run pytest tests/e2e/ -v
```

### Coverage Requirements

- **Target:** 80% minimum code coverage
- **Measurement:** Branch coverage enabled
- **Threshold:** CI fails if coverage < 80%

```bash
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80
```

For comprehensive testing patterns, see [.claude/reference/pytest-best-practices.md](.claude/reference/pytest-best-practices.md)

---

## 🔄 Git Workflow

### Branch Strategy

- `main` - Production-ready code
- `dev` - Integration branch for features
- `feature/*` - New features
- `hotfix/*` - Bug fixes

### Commit Message Format

Never include "claude code" or "written by claude code" in commit messages.

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

### CHANGELOG Maintenance

**Mandatory:** Update `CHANGELOG.md` before creating a PR.

**Quick reference:**
- Add entry to `[Unreleased]` section before PR
- Include both Linear ticket (PRO-XXX) and PR number (#X)
- Focus on "why" and "what it enables", not implementation details
- Use categories: Added, Changed, Fixed, Security, Infrastructure

For detailed guidelines, see [.claude/reference/changelog-best-practices.md](.claude/reference/changelog-best-practices.md)

---

## 📚 Reference Documentation

Read these documents when working on specific areas:

| Document | When to Read |
|----------|--------------|
| [piv-loop-methodology.md](.claude/reference/piv-loop-methodology.md) | Understanding development workflow, commands, feedback loops |
| [style-conventions.md](.claude/reference/style-conventions.md) | Naming, docstrings, imports, code organization |
| [fastapi-best-practices.md](.claude/reference/fastapi-best-practices.md) | Building API endpoints, dependencies, async patterns |
| [pydantic-best-practices.md](.claude/reference/pydantic-best-practices.md) | Data validation, settings, V1→V2 migration |
| [pytest-best-practices.md](.claude/reference/pytest-best-practices.md) | Test organization, fixtures, mocking, parametrization |
| [aws-lambda-best-practices.md](.claude/reference/aws-lambda-best-practices.md) | Lambda handlers, cold starts, Secrets Manager |
| [security-best-practices.md](.claude/reference/security-best-practices.md) | Input validation, secrets, SQL injection prevention |
| [error-handling-patterns.md](.claude/reference/error-handling-patterns.md) | Custom exceptions, logging, retry patterns |
| [database-standards.md](.claude/reference/database-standards.md) | Naming conventions, repository patterns, models |
| [performance-optimization.md](.claude/reference/performance-optimization.md) | Profiling, caching, async I/O, database queries |
| [changelog-best-practices.md](.claude/reference/changelog-best-practices.md) | Version management, PR workflow, formatting |
| [uv-package-manager.md](.claude/reference/uv-package-manager.md) | Package management, dependency updates |
| [git-workflow.md](.claude/reference/git-workflow.md) | Branching strategy, commit conventions |
| [rg-search-patterns.md](.claude/reference/rg-search-patterns.md) | Search patterns, file filtering |
| [habit-tracker-example.md](.claude/reference/habit-tracker-example.md) | Example CLAUDE.md structure |

---

## ⚠️ Important Notes

- **NEVER ASSUME OR GUESS** - When in doubt, ask for clarification
- **Always verify file paths and module names** before use
- **Keep CLAUDE.md updated** when adding new patterns or dependencies
- **Test your code** - No feature is complete without tests
- **Document your decisions** - Future developers (including yourself) will thank you

---

## 🧠 Context Budget (Not Token Budget)

**Important distinction:** The PIV-Swarm system manages *context budget*, not *token budget*.

| Term | What It Implies | Reality |
|------|-----------------|---------|
| **Token budget** | Tracking API tokens spent (billing) | ❌ Not what we track |
| **Context budget** | Managing context window capacity | ✅ What we actually manage |

### How It Works

- Each Claude Code session gets a **fresh ~200K context window**
- Context doesn't accumulate across sessions - it **resets** with each new session
- The pause/resume system captures **state** so work can continue, not tokens
- When skills reference "context_used", this tracks consumption within the current session

### Why This Matters

```
Session 1: Uses 80K context → /pause → state saved
Session 2: Starts fresh with 200K → /resume → loads state (minimal context)
```

The checkpoint system exists to:
1. Save progress before hitting context limits
2. Allow work to continue in fresh sessions
3. Preserve decisions and task status (not token counts)

**Bottom line:** Think "context window management" not "token accounting."

---

## 🔍 Search Command Requirements

**CRITICAL**: Always use `rg` (ripgrep) instead of traditional `grep` and `find` commands:

```bash
# ❌ Don't use grep
grep -r "pattern" .

# ✅ Use rg instead
rg "pattern"

# ❌ Don't use find with name
find . -name "*.py"

# ✅ Use rg with file filtering
rg --files -g "*.py"
```

---

## 🚀 GitHub Flow Workflow

```
main (protected) ←── PR ←── release/your-release from dev
↓ ↑
deploy    dev ←── PR ←── feature/your-feature
```

### Daily Workflow

1. `git checkout dev && git pull origin dev`
2. `git checkout -b feature/new-feature`
3. Make changes + tests
4. `git push origin feature/new-feature`
5. Create PR → Review → Merge to dev

---

_This document is a living guide. Update it as the project evolves and new patterns emerge._
