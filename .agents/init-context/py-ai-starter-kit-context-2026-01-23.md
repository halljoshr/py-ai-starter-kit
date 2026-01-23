# py-ai-starter-kit Context Report

**Generated:** 2026-01-23 13:43 UTC
**Branch:** main
**Agent:** Claude Sonnet 4.5
**Git Status:** Modified my-current-process.md (uncommitted)

---

## Project Overview

**Purpose:** This is a Python AI Starter Kit repository designed to establish best practices, workflows, and command structures for systematic AI-assisted software development. It serves as a methodology framework and reference implementation for the PIV (Prime → Implement → Validate) Loop development approach.

**Version:** N/A (Methodology framework, not a deployable application)

**Technologies:**
- Language: Python (inferred from conventions)
- Development Methodology: PIV Loop (Prime → Implement → Validate)
- Package Manager: UV (fast Python package management)
- Quality Tools: ruff (linting/formatting), mypy (type checking), pytest (testing)
- VCS: Git with GitHub Flow workflow

**Key Capabilities:**
- Systematic development workflow commands (prime, plan-feature, implement-plan, validate, commit)
- Context-first development approach
- Multi-tier testing strategy (unit/integration/e2e)
- Institutional knowledge preservation through artifacts
- AI-assisted code review and root cause analysis
- Comprehensive reference documentation for Python best practices

---

## Architecture

**Pattern:** Methodology and command framework (not a traditional application architecture)

**Directory Structure:**
```
py-ai-starter-kit/
├── .agents/                    # Artifact storage for PIV Loop outputs
│   ├── init-context/          # Context reports from /prime command
│   ├── plans/                 # Feature plans from /plan-feature command
│   ├── execution-reports/     # Implementation feedback from /execution-report
│   ├── code-reviews/          # Code review outputs from /code-review
│   └── rca/                   # Root cause analysis documents from /rca
├── .claude/                    # Claude Code command definitions
│   ├── commands/              # Skill command implementations
│   │   ├── core_piv_loop/    # Prime, plan-feature, implement-plan
│   │   ├── validation/       # Validate, code-review, execution-report, code-review-since
│   │   ├── bug_fix/          # RCA, implement-fix
│   │   └── git/              # Commit command
│   ├── reference/             # Best practices documentation
│   │   ├── piv-loop-methodology.md
│   │   ├── style-conventions.md
│   │   ├── fastapi-best-practices.md
│   │   ├── pydantic-best-practices.md
│   │   ├── pytest-best-practices.md
│   │   ├── aws-lambda-best-practices.md
│   │   ├── security-best-practices.md
│   │   ├── error-handling-patterns.md
│   │   ├── database-standards.md
│   │   ├── performance-optimization.md
│   │   ├── changelog-best-practices.md
│   │   ├── uv-package-manager.md
│   │   ├── git-workflow.md
│   │   ├── rg-search-patterns.md
│   │   └── habit-tracker-example.md
│   └── PIV-LOOP.md            # Core methodology documentation
├── CLAUDE.md                   # Main development guidelines (primary doc)
├── CLAUDE_OG.md               # Original version (archival)
├── my-current-process.md       # User's current workflow documentation
├── FEEDBACK_IDEAS.md           # Improvement tracking
├── CONTEXT-OPTIMIZATION-RESEARCH.md  # Token optimization research
└── RESEARCH-ANALYSIS.md        # Analysis documentation
```

**Workflow Flow:**
1. `/prime` → Establish comprehensive codebase context
2. `/plan-feature {name}` → Create detailed implementation plan
3. `/implement-plan {plan-file}` → Execute plan with incremental validation
4. `/validate` → Multi-stage quality gates (linting, types, tests, coverage)
5. `/code-review` → AI-driven code review before commit
6. `/commit` → Semantic commit with proper formatting
7. `/execution-report {plan-file}` → Generate feedback for continuous improvement

---

## Tech Stack Details

**Methodology Framework (Not a Python application):**
This repository contains:
- Development workflow commands (executed by Claude Code CLI)
- Best practices documentation
- Reference patterns for Python projects

**Expected Target Stack (for projects using this methodology):**
- **Language:** Python 3.9+
- **Frameworks:** FastAPI (web), LangGraph (agents), Pydantic v2 (validation)
- **AWS Services:** Bedrock, Lambda, Secrets Manager
- **Testing:** pytest, pytest-asyncio, pytest-cov
- **Tools:** UV, ruff, mypy, SAM CLI

**Key Dependencies (typical projects using this framework):**
- langgraph - Workflow orchestration
- fastapi - Web framework
- pydantic >= 2.0 - Data validation
- boto3 - AWS SDK
- httpx - HTTP client
- pytest - Testing framework

---

## Core Principles (from CLAUDE.md)

**Development Philosophy:**
- **KISS (Keep It Simple, Stupid)** - Choose straightforward solutions over complex ones
- **YAGNI (You Aren't Gonna Need It)** - Implement features only when needed
- **Dependency Inversion** - High-level modules depend on abstractions, not low-level modules
- **Open/Closed Principle** - Software entities open for extension, closed for modification
- **Single Responsibility** - Each function/class/module has one clear purpose
- **Fail Fast** - Check for errors early, raise exceptions immediately

**Code Standards:**
- Line length: **100 characters** (enforced by ruff)
- File length: **Max 500 lines** (refactor if approaching limit)
- Function length: **Max 100 lines** with single responsibility
- Coverage threshold: **80% minimum** (CI fails below threshold)
- Type hints: **Required** for all function signatures and class attributes
- String style: **Double quotes**
- Naming: `snake_case` (variables/functions), `PascalCase` (classes), `UPPER_SNAKE_CASE` (constants)

**Testing Strategy:**
- **3-tier structure:** unit / integration / e2e
- **Unit tests** (`tests/unit/`) - < 1 second, all I/O mocked
- **Integration tests** (`tests/integration/`) - 1-30 seconds, minimal mocking
- **E2E tests** (`tests/e2e/`) - > 30 seconds, no mocking
- **Markers** for categorization (speed, services, features, dependencies)
- **Test-driven development** encouraged

**Git Workflow:**
- **Branch strategy:** main (production) ← dev (integration) ← feature/* (development)
- **Commit format:** Semantic commits (type(scope): subject)
- **CHANGELOG:** Mandatory updates before PR
- **Never include:** "claude code" or "written by claude code" in commits
- **Co-authored:** Always credit Claude in commit footer

---

## Current State

**Branch:** main

**Status:**
- Modified: my-current-process.md (17 insertions, 15 deletions)
- Clean working tree otherwise

**Recent Work (last 10 commits):**
```
c0604ae - Michael made me write out my current process (HEAD -> main, origin/main)
64cca90 - Added gsd link
af3260b - Added feedback & ideas file
72002af - Added code-review-since feature
ae9e9ba - Added pre-compacting rules research
a1b1cce - Building out analysis of Python usage (incomplete)
3715afe - Create execute-prp.md
dc14347 - Create generate-prp.md
7545b70 - Create CLAUDE.md
```

**Recent Focus:**
- Documenting user's current development process (my-current-process.md)
- Adding code-review-since validation feature for reviewing changes before pushing to main
- Research into context optimization and prompt caching strategies
- Gathering feedback and improvement ideas
- Establishing core methodology documentation

**Active Plans:**
No in-progress feature plans found in `.agents/plans/` (directory structure created but empty)

**Uncommitted Changes:**
- my-current-process.md: User's workflow documentation updated with TDD emphasis and manual review steps

---

## Key Patterns Observed

### PIV Loop Methodology

**Three-Phase Cycle:**
1. **PRIME** - Context establishment before any work
2. **IMPLEMENT** - Execution with incremental validation after each task
3. **VALIDATE** - Multi-stage quality gates before commit

**Critical Rules:**
- ❌ NEVER skip validation steps
- ❌ NEVER proceed if validation fails
- ❌ NEVER accumulate multiple failures before fixing
- ✅ ALWAYS fix issues immediately
- ✅ ALWAYS document deviations from plan
- ✅ ALWAYS verify baseline before starting

### Command Structure

Commands are defined in `.claude/commands/` as markdown files:
- **core_piv_loop/**: prime.md, plan-feature.md, implement-plan.md
- **validation/**: validate.md, code-review.md, execution-report.md, code-review-since.md
- **bug_fix/**: rca.md, implement-fix.md
- **git/**: commit.md

### Artifact Preservation

All PIV outputs saved to `.agents/` for institutional knowledge:
- Context reports → `.agents/init-context/`
- Feature plans → `.agents/plans/`
- Execution reports → `.agents/execution-reports/`
- Code reviews → `.agents/code-reviews/`
- RCA documents → `.agents/rca/`

### User's Current Process (from my-current-process.md)

1. **Original planning** with Opus - discuss feature, mention TDD, clarify questions
2. **Run /plan-feature** to create formatted plan.md
3. **Manual review** of plan (sometimes ask new context to critique)
4. **New context: /implement-plan** (note: user sometimes runs /prime before this)
5. **Monitor implementation** - watch for plan adherence, verify tests pass
6. **Manual review** - run server, check functionality against checklist
7. **New context: /prime then /code-review** - fix critical findings
8. **Commit** changes
9. **Before pushing to main: /prime then /code-review-since <commit_code>**

### Search Patterns

**CRITICAL:** Always use `rg` (ripgrep), never `grep` or `find`:
```bash
# ✅ Correct
rg "pattern"
rg --files -g "*.py"

# ❌ Wrong
grep -r "pattern" .
find . -name "*.py"
```

---

## Testing Architecture

**Test Organization (Typical Structure):**
- `tests/unit/` - Pure unit tests, < 1 second, no APIs
- `tests/integration/` - API tests, 1-30 seconds, minimal mocking
- `tests/e2e/` - Full workflows, > 30 seconds, no mocking
- `tests/manual/` - Manual testing scripts (not in CI)

**Active Markers (Typical):**
- **Speed:** `fast`, `slow`, `very_slow`
- **Services:** `hubspot`, `bedrock`, `heron`, `alloy`
- **Features:** `flag_validation`, `business_risks`, `debt_validation`
- **Dependencies:** `requires_api`, `requires_secrets`

**Coverage:** Target 80% minimum (enforced by `--cov-fail-under=80`)

**Test Commands:**
```bash
# All tests
uv run pytest

# Unit tests only
uv run pytest tests/unit/ -v

# Integration (exclude very slow)
uv run pytest tests/integration/ -m "not very_slow" -v

# With coverage
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## External Integrations (Typical)

**AWS Services:**
- Bedrock - AI/ML model access
- Secrets Manager - Production secrets
- Lambda - Serverless compute

**Development Tools:**
- UV - Package management
- ruff - Linting and formatting
- mypy - Type checking
- pytest - Testing
- gh CLI - GitHub operations

---

## Configuration Management

**Environment Variables:**
- Production: AWS Secrets Manager
- Local development: .env file
- Settings: Pydantic BaseSettings for configuration
- Example: .env.example for required variables

**Package Management:**
```bash
uv venv               # Create virtual environment
uv sync               # Sync dependencies
uv add package        # Add package (NEVER edit pyproject.toml directly!)
uv add --dev pytest   # Add dev dependency
uv run python script  # Run in environment
```

---

## Reference Documentation

**Available in `.claude/reference/` (16 documents):**

### Core Methodology
- [piv-loop-methodology.md](.claude/reference/piv-loop-methodology.md) - Complete PIV Loop guide

### Code Standards
- [style-conventions.md](.claude/reference/style-conventions.md) - Naming, docstrings, imports
- [fastapi-best-practices.md](.claude/reference/fastapi-best-practices.md) - API patterns
- [pydantic-best-practices.md](.claude/reference/pydantic-best-practices.md) - Validation patterns
- [pytest-best-practices.md](.claude/reference/pytest-best-practices.md) - Testing patterns

### Infrastructure
- [aws-lambda-best-practices.md](.claude/reference/aws-lambda-best-practices.md) - Serverless patterns
- [database-standards.md](.claude/reference/database-standards.md) - DB naming, repository patterns

### Quality & Security
- [security-best-practices.md](.claude/reference/security-best-practices.md) - Input validation, secrets
- [error-handling-patterns.md](.claude/reference/error-handling-patterns.md) - Exceptions, logging
- [performance-optimization.md](.claude/reference/performance-optimization.md) - Profiling, caching

### Tools & Workflow
- [uv-package-manager.md](.claude/reference/uv-package-manager.md) - Package management
- [git-workflow.md](.claude/reference/git-workflow.md) - Branching, commits
- [rg-search-patterns.md](.claude/reference/rg-search-patterns.md) - Ripgrep usage
- [changelog-best-practices.md](.claude/reference/changelog-best-practices.md) - Version management

### Examples
- [habit-tracker-example.md](.claude/reference/habit-tracker-example.md) - Example CLAUDE.md structure

---

## Observations & Recommendations

**Strengths:**
- ✅ Comprehensive methodology with clear phases and deliverables
- ✅ Strong emphasis on context-first development ("Context is King")
- ✅ Validation at every step prevents error accumulation
- ✅ Institutional knowledge preservation through artifact storage
- ✅ Detailed reference documentation for common patterns
- ✅ User has documented real-world process for iteration
- ✅ Feedback loop through execution reports

**Areas of Note:**
- This is a **methodology framework**, not a deployable application
- No actual Python code exists yet - this is the starter kit structure
- `.agents/` directory exists but is empty (no artifacts generated yet)
- User tracks feedback/ideas in FEEDBACK_IDEAS.md for continuous improvement
- Context optimization research indicates awareness of token usage challenges

**Patterns to Follow:**
- Prime before planning: Always run `/prime` at conversation start
- Sequential validation: Validate after EACH implementation task, not at the end
- Artifact preservation: Save all plans, reports, and reviews to `.agents/`
- Incremental fixes: Fix validation failures immediately, never accumulate debt
- New context for phases: User preference for fresh context between prime/implement/review

**Recent Changes:**
- c0604ae: Added user's current process documentation showing real-world workflow
- 72002af: Added code-review-since feature for pre-push validation
- af3260b: Created feedback tracking system
- ae9e9ba: Researching context optimization and pre-compacting strategies

---

## Identified Improvement Opportunities (from FEEDBACK_IDEAS.md)

1. **Test-first deployment** - Building out full tests-first workflow that knows required tests before commit
2. **Prime function optimization** - More efficient token usage for large codebases (currently "pretty rough")
3. **Team alignment** - Need consistent AI usage patterns across developers
4. **Possible solution reference:** https://github.com/glittercowboy/get-shit-done

---

## User's Workflow Insights (from my-current-process.md)

**Key practices:**
- Emphasizes TDD (Test Driven Development)
- Uses new contexts between phases (planning → implementation → review)
- Manual review includes running server and using checklist for critical functionality
- Sometimes uses new context to critique plan for complex features
- Always runs /code-review-since before pushing to main branch
- Notes that /implement-plan is "newer rendition" and may need work

**Validation points:**
- Tests must pass after implementation
- Manual server run to verify functionality
- Code review findings must be fixed before commit
- Additional review before pushing to main

---

## Context Optimization Research Highlights

From CONTEXT-OPTIMIZATION-RESEARCH.md:

**Prompt Caching Benefits:**
- 60-90% cost reduction for repeated context
- 5-minute cache (1.25x write cost, 0.1x read cost)
- 1-hour cache (2x write cost, 0.1x read cost)
- Cache hierarchies: tools → system → messages
- Minimum cacheable: 1024 tokens (Sonnet), 4096 tokens (Opus/Haiku)

**PreCompact Hook:**
- Intercept automatic conversation compaction
- Preserve critical context before summarization
- Configure in Claude Code settings

---

## Next Steps

Based on this context, you are now ready to:

1. **Plan features** using `/plan-feature {name}`
   - Comprehensive 5-phase planning process
   - Include code examples from this methodology
   - Reference patterns in `.claude/reference/` docs

2. **Implement features** using `/implement-plan {plan-file}`
   - Sequential execution with incremental validation
   - Track deviations from plan
   - Fix issues immediately

3. **Validate code** using `/validate`
   - 4-stage default: linting, types, unit tests, coverage
   - 6-stage full: adds e2e and security checks
   - Must pass 80% coverage threshold

4. **Review code** using `/code-review` or `/code-review-since`
   - AI-driven 5-dimension evaluation
   - Fix critical findings before commit
   - Use code-review-since before pushing to main

5. **Generate feedback** using `/execution-report {plan-file}`
   - Close feedback loop after implementation
   - Document successes, difficulties, deviations
   - Improve future planning through learning

**Refer back to this context report** throughout development to ensure consistency with project conventions and methodology.

---

## Validation Checklist

Prime completion checklist:

- [x] Read CLAUDE.md completely
- [x] Read PIV-LOOP.md
- [x] Analyzed directory structure
- [x] Identified key files (command definitions, reference docs)
- [x] Reviewed recent commits (last 10)
- [x] Checked current branch and status (main, my-current-process.md modified)
- [x] Understood methodology patterns (PIV Loop)
- [x] Reviewed user's current workflow (my-current-process.md)
- [x] Extracted naming conventions and standards
- [x] Reviewed feedback and improvement ideas
- [x] Generated context report
- [x] Saved report to `.agents/init-context/`

---

## Summary

**Project Type:** Python AI development methodology framework (starter kit)

**Core Philosophy:** "Context is King" - Understand before acting, validate before proceeding, learn from every implementation

**Primary Use Case:** Systematic, high-quality AI-assisted software development using the PIV Loop methodology

**Key Differentiators:**
- Phase-gated development with validation at every step
- Institutional knowledge preservation through artifact storage
- Comprehensive reference documentation
- Test-driven development emphasis
- Continuous improvement through execution reports

**Current Status:** Active methodology development, user iterating on workflow based on real-world usage

**Ready for:** Feature planning, implementation, and validation following PIV Loop methodology
