# py-ai-starter-kit Context Report

**Generated:** 2026-02-02
**Branch:** main
**Last Commit:** f62a040 - Built out a bunch of skills not tested yet.

---

## Executive Summary

**py-ai-starter-kit** is a comprehensive PIV-Swarm (Prime-Implement-Validate) autonomous engineering workflow system for Python projects using Claude Code. It provides a systematic, high-quality feature development methodology with session persistence and multi-agent support through 24+ Claude Code skills.

**Core Philosophy:** "Context is King" - Understand before acting, validate before proceeding, learn from every implementation.

**Current Status:** Active development with extensive skills library. Recently completed major skill build-out (commit f62a040). Repository is clean with no uncommitted changes.

---

## Project Structure

### Top-Level Organization

```
py-ai-starter-kit/
├── .agents/              # AI methodology artifacts (session state, research)
├── .claude/              # Claude Code configuration (skills, reference docs, schemas)
├── examples/             # POC examples (pydantic-ai)
├── piv-swarm/            # Core PIV-Swarm documentation
├── piv-swarm-example/    # Example Todo API implementation
├── research/             # (empty - likely archived)
├── tmp/                  # Temporary files
├── CLAUDE.md             # Development standards and conventions
├── GOALS.md              # Strategic roadmap with 21 goals
├── README.md             # User-facing documentation
└── FEEDBACK_IDEAS.md     # User feedback tracking
```

### File Type Distribution

- **Markdown (122 files):** Primary documentation format
- **Python (12 files):** Implementation code, mostly in examples/
- **YAML (15 files):** Schemas, configurations
- **JSON (3 files):** Data/config files
- **TOML (1 file):** Python project configuration

---

## Core Components

### 1. Claude Code Skills (.claude/skills/)

**24 Skills Implemented:**

**Context & Planning:**
- `prime` - Establish comprehensive codebase context
- `prime-deep` - Deep analysis with cross-references
- `discuss` - Design decision conversations
- `spec` - Generate formal Anthropic XML specifications
- `plan` - Create task files from specs
- `plan-feature` - Feature planning workflow
- `explore` - Codebase exploration

**Implementation:**
- `execute` - Execute task files
- `implement-plan` - Implement feature plans
- `implement-fix` - Execute bug fixes

**Validation:**
- `validate` - Multi-stage quality gates
- `code-review` - Full codebase review
- `code-review-since` - Review changes since commit
- `execution-report` - Generate validation reports

**Bug Workflow:**
- `rca` - Root cause analysis
- `implement-fix` - Fix implementation

**Session Management:**
- `pause` - Checkpoint session state
- `resume-session` - Restore session
- `status` - Display current state

**Task Management:**
- `task-list` - List all tasks
- `task-create` - Create new task
- `task-update` - Update task
- `task-complete` - Mark task done

**Git Operations:**
- `commit` - Semantic commits with co-author attribution

**PRP (Planning & Reporting):**
- `generate-prp` - Create PRP
- `execute-prp` - Execute BASE PRP

### 2. Reference Documentation (.claude/reference/)

**15 Best Practice Documents:**

- `piv-loop-methodology.md` - Development workflow
- `style-conventions.md` - Naming, docstrings, imports
- `fastapi-best-practices.md` - API patterns
- `pydantic-best-practices.md` - Data validation (v2)
- `pytest-best-practices.md` - Three-tier testing
- `aws-lambda-best-practices.md` - Serverless patterns
- `security-best-practices.md` - OWASP Top 10 prevention
- `error-handling-patterns.md` - Exception handling
- `database-standards.md` - Repository patterns
- `performance-optimization.md` - Profiling & caching
- `changelog-best-practices.md` - Version management
- `uv-package-manager.md` - Fast Python package management
- `git-workflow.md` - Branching strategy
- `rg-search-patterns.md` - ripgrep usage
- `habit-tracker-example.md` - Example CLAUDE.md

### 3. Session State Management (.agents/)

**Directory Structure:**

```
.agents/
├── specs/               # Anthropic XML specifications
├── tasks/               # Individual task-NNN.yaml files
├── state/               # session.yaml, STATE.md
├── research/            # 10 research documents (see below)
├── plans/               # Feature plans (empty - no active plans)
├── execution-reports/   # Validation reports (empty currently)
├── progress/            # Progress tracking (empty)
├── analytics/           # Token usage, metrics (empty)
├── features/            # Feature tracking (empty)
├── architecture/        # ADRs (empty)
└── decisions/           # Decision log (empty)
```

**Recent Research (Last 10 days):**
1. `migration-decision-summary-sanitized-2026-01-30.md` - Migration decisions
2. `bedrock-converse-migration-plan-sanitized-2026-01-30.md` - AWS Bedrock migration
3. `session-summary-2026-01-30.md` - Session recap
4. `explore-skill-build-complete-2026-01-30.md` - Skill building completion
5. `skill-enhancement-progress-2026-01-30.md` - Enhancement tracking
6. `skill-building-implementation-2026-01-30.md` - Implementation notes
7. `overall-project-discussion-2026-01-28.md` - Project direction
8. `GSD-VS-PIV-ANALYSIS.md` - Workflow comparison
9. `RESEARCH-ANALYSIS.md` - General research
10. `CONTEXT-OPTIMIZATION-RESEARCH.md` - Prompt caching, compaction patterns

### 4. Example Implementation (piv-swarm-example/)

**Minimal Todo API demonstrating PIV-Swarm patterns:**

- **Framework:** FastAPI 0.109.0+
- **Python:** 3.11+
- **Structure:**
  - `src/main.py` - Entry point with health check endpoint
  - `src/api/` - API endpoints (currently empty)
  - `src/models/` - Pydantic models (currently empty)
  - `src/services/` - Business logic (currently empty)
  - `tests/` - Three-tier tests (unit/integration/e2e)
- **Dev Tools:** pytest, ruff, mypy, httpx
- **Status:** Minimal skeleton, ready for feature implementation

---

## Development Standards (from CLAUDE.md)

### Philosophy

**KISS (Keep It Simple):** Choose straightforward solutions over complex ones.
**YAGNI (You Aren't Gonna Need It):** Build features only when needed, not speculatively.
**Design Principles:** Dependency Inversion, Open/Closed, Single Responsibility, Fail Fast.

### Critical Policy: NO Timeline Predictions

**NEVER use:**
- Timeline language ("Week 1-2", "Q2 2026")
- Duration predictions ("This will take X days")
- Time-based priorities ("Priority 1 = this quarter")

**ALWAYS use:**
- Priority framing ("First Priority", "High/Medium/Low")
- "When do you need this?" or "What's urgent?"
- "Now vs later" not "this quarter vs next year"

**Rationale:** AI-assisted development moves faster than traditional estimates. Let users determine urgency.

### Code Structure Rules

- **Max file length:** 500 lines
- **Max function length:** 100 lines
- **Line length:** 100 characters (enforced by ruff)
- **Single Responsibility:** One clear purpose per function/class/module

### Package Management (UV)

This project uses UV for blazing-fast Python package management.

**Key Commands:**
```bash
uv venv                    # Create virtual environment
uv sync                    # Install dependencies
uv add <package>           # Add package (NEVER edit pyproject.toml manually!)
uv run pytest              # Run tests
uv run ruff format .       # Format code
uv run ruff check .        # Lint
uv run mypy app/           # Type checking
```

### Testing Strategy (Three-Tier)

1. **Unit Tests** (`tests/unit/`) - < 1 second, all I/O mocked
2. **Integration Tests** (`tests/integration/`) - 1-30 seconds, minimal mocking
3. **E2E Tests** (`tests/e2e/`) - > 30 seconds, no mocking

**Coverage Requirement:** 80% minimum (enforced in CI)

### Style Conventions

- **PEP8** with 100 char line length
- **Double quotes** for strings
- **Type hints** for all function signatures
- **Format with ruff** (not Black)
- **Pydantic v2** for validation

**Naming:**
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`

### Git Workflow

**Branches:**
- `main` - Production-ready
- `dev` - Integration branch
- `feature/*` - New features
- `hotfix/*` - Bug fixes

**Commit Format:**
```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

**NEVER include:** "claude code" or "written by claude code" in commit messages

### Search Requirements

**CRITICAL:** Always use `rg` (ripgrep) instead of `grep` or `find`:

```bash
# ✅ Correct
rg "pattern"
rg --files -g "*.py"

# ❌ Wrong
grep -r "pattern" .
find . -name "*.py"
```

---

## PIV-Swarm Workflow

### Standard Flow

```
Prime → Discuss → Spec → Plan → Execute → Validate → Commit
```

**Commands:**
```bash
/prime              # Understand codebase
/discuss <name>     # Make design decisions
/spec <name>        # Generate formal specification
/plan               # Create task files
/execute            # Build with validation
/validate           # Final verification
/commit             # Semantic commit
```

### Session Persistence

**Pause/Resume:**
```bash
/pause    # Checkpoint current state
/resume   # Restore and continue
/status   # Show current progress
```

**Persists:**
- Current phase and progress
- Task status and results
- Design decisions
- Token usage
- Git state

### Multi-Agent "Swarm" Support

- Individual task files - Agents claim specific tasks
- Task dependencies - `blocked_by`/`blocks` prevent conflicts
- Task ownership - Track who's working on what
- Shared state in `.agents/` directory
- Per-task token budgets

---

## Recent Activity (Last 10 Commits)

1. **f62a040** - Built out a bunch of skills not tested yet
2. **610850a** - working on skills not finished
3. **c90ea98** - Adding template instructions
4. **7e2502f** - Testing a few renditions of claude skills and building best workflow
5. **d562fbe** - Updated research and structure as well as Goals
6. **c0604ae** - Michael made me write out my current process
7. **64cca90** - Added gsd link
8. **af3260b** - Added a feedback & ideas file
9. **72002af** - Added the code-review-since feature
10. **ae9e9ba** - Added info about pre-compacting rules and research

**Pattern:** Active skill development and methodology refinement. Focus on building comprehensive skill library.

---

## Strategic Goals (from GOALS.md)

### Core Philosophy

"Context is King, Sessions are Natural, Quality is Non-Negotiable"

- Spend tokens wisely on context that matters
- Design for multi-session development from the start
- Never compromise quality for speed
- Learn from every implementation
- KISS + YAGNI principles

### Priority 1 Goals (Current Focus)

1. **Spec Creation Process** - Systematic requirements → specification workflow
2. **Session Management System** - Live progress tracking, checkpointing, metrics
3. **Multi-Session Architecture** - Default to multi-session with phase-based planning
4. **Token Budget Management** - Pre-flight estimation, real-time tracking, cost visibility

### Priority 2 Goals

5. **Comprehensive Skills Tree** - Atomic + compound skills (currently 24 implemented)
6. **JSON Features Tracking** - Single source of truth inspired by Anthropic's approach
7. **TDD Culture** - Enforce Red-Green-Refactor cycle
8. **Standard Development Flow** - Clear entry/exit points, consistent artifacts
9. **Profiling & Optimization System** - Data-driven performance improvements

### Priority 3 Goals

10. **Language-Specific Standards** - Python complete, expand as needed (YAGNI)
11. **Project Ownership & Docs** - OWNERS file, decision log, ADRs
12. **Configurable Autonomy Levels** - 5 levels from full supervision to full autonomy
13. **Standard Folder Structures** - Consistent layout across languages

### Priority 4 Goals (Future)

14. **Smart Context Management** - Efficient loading, prompt caching, progressive detail
15. **Cost Tracking & Optimization** - API costs per feature/session/project
16. **Linear Integration** - Optional ticket sync
17. **Cross-Project Pattern Library** - Searchable patterns/anti-patterns
18. **Feedback Loop Analytics** - Auto-improve from execution reports
19. **Developer Onboarding** - Interactive tutorials
20. **Multi-Provider Abstraction** - Anthropic primary, AWS Bedrock fallback
21. **Advanced Context Optimization** - Caching, compaction, PreCompact hooks (research complete)

---

## Key Technologies

### Core Stack

- **Python:** 3.11+
- **Package Manager:** UV (blazing-fast alternative to pip/poetry)
- **API Framework:** FastAPI 0.109.0+
- **Validation:** Pydantic v2.5.0+
- **ASGI Server:** Uvicorn 0.27.0+

### Development Tools

- **Testing:** pytest 8.0.0+, pytest-asyncio, httpx
- **Linting:** ruff 0.1.0+ (replaces Black + flake8 + isort)
- **Type Checking:** mypy 1.8.0+ (strict mode)
- **Coverage:** pytest-cov (80% minimum threshold)

### AI/ML Dependencies (examples/)

- **pydantic-ai:** Used in POC examples for multi-provider agent abstraction

---

## Architecture Patterns

### Skill Structure

**Skills use YAML frontmatter:**
```yaml
---
name: skill-name
description: What the skill does
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Skill Documentation
Instructions for Claude...
```

### Task File Schema

**Task YAML structure (.agents/tasks/task-NNN.yaml):**
- Description and acceptance criteria
- Implementation steps
- Validation commands and skills
- Dependencies (`blocked_by`/`blocks`)
- Test results and token tracking
- Owner field for multi-agent coordination

### Session State Schema

**Session YAML (.agents/state/session.yaml):**
- Feature name and phase
- Tasks completed/remaining
- Token budget used
- Next recommended action
- Git state snapshot

---

## Read More (On-Demand Reference Docs)

When working on specific areas, refer to these documents:

| Topic | Document |
|-------|----------|
| Development workflow, PIV loop | [.claude/reference/piv-loop-methodology.md](.claude/reference/piv-loop-methodology.md) |
| Code style, naming, imports | [.claude/reference/style-conventions.md](.claude/reference/style-conventions.md) |
| API endpoints, dependencies | [.claude/reference/fastapi-best-practices.md](.claude/reference/fastapi-best-practices.md) |
| Data validation, settings | [.claude/reference/pydantic-best-practices.md](.claude/reference/pydantic-best-practices.md) |
| Test patterns, fixtures, mocking | [.claude/reference/pytest-best-practices.md](.claude/reference/pytest-best-practices.md) |
| Lambda handlers, cold starts | [.claude/reference/aws-lambda-best-practices.md](.claude/reference/aws-lambda-best-practices.md) |
| Security, input validation | [.claude/reference/security-best-practices.md](.claude/reference/security-best-practices.md) |
| Exception handling, logging | [.claude/reference/error-handling-patterns.md](.claude/reference/error-handling-patterns.md) |
| Database conventions, repos | [.claude/reference/database-standards.md](.claude/reference/database-standards.md) |
| Profiling, caching, async I/O | [.claude/reference/performance-optimization.md](.claude/reference/performance-optimization.md) |
| CHANGELOG format, PRs | [.claude/reference/changelog-best-practices.md](.claude/reference/changelog-best-practices.md) |
| UV package management | [.claude/reference/uv-package-manager.md](.claude/reference/uv-package-manager.md) |
| Git branching, commits | [.claude/reference/git-workflow.md](.claude/reference/git-workflow.md) |
| ripgrep search patterns | [.claude/reference/rg-search-patterns.md](.claude/reference/rg-search-patterns.md) |
| Example CLAUDE.md | [.claude/reference/habit-tracker-example.md](.claude/reference/habit-tracker-example.md) |

---

## Important Conventions Extracted

### From CLAUDE.md:

1. **Never assume or guess** - Ask for clarification
2. **Always verify file paths** before use
3. **Test your code** - No feature complete without tests
4. **Document decisions** - Future developers will thank you
5. **Keep CLAUDE.md updated** - Living document

### From README.md:

1. **Start every feature with /prime** - Context is critical
2. **Use /discuss for ambiguity** - Resolve gray areas upfront
3. **Validate frequently** - After each task, before merge
4. **Commit task files** - Preserve state in `.agents/` directory
5. **Use /pause between sessions** - Checkpoint before closing

### From Skills:

1. **Shallow discovery** - Build map of WHERE things are, not WHAT they contain
2. **Read files on-demand** - When planning/implementation requires them
3. **Use --files-with-matches** - For locating, not reading
4. **Sample patterns** - Read 1-2 examples to see conventions applied
5. **Generate reports** - Save context for future reference

---

## Current Project State

**Branch:** main
**Status:** Clean working directory (no uncommitted changes)
**Last Activity:** Skill development and testing (f62a040)

**No Active Work:**
- No pending plans in `.agents/plans/`
- No execution reports in `.agents/execution-reports/`
- No in-progress tasks

**Ready for:**
- New feature planning
- Skill testing and refinement
- Example implementation in piv-swarm-example/
- Goal implementation from GOALS.md Priority 1

---

## Next Steps (Recommendations)

Based on current state and GOALS.md:

1. **Test Recent Skills** - 24 skills built but not tested (commit message: "not tested yet")
2. **Spec Creation Tooling** - Build `/create-spec` command (Goal #1, Phase 1)
3. **Session Management Implementation** - Begin Goal #2 (Progress File System)
4. **Token Budget System** - Implement Goal #4 (Pre-flight estimation)
5. **Expand piv-swarm-example** - Use as testing ground for workflows

---

## Checklist: Prime Completion

- [x] Read CLAUDE.md fully (noted reference docs for later)
- [x] Read README.md
- [x] Attempted to read pyproject.toml (doesn't exist in root, found in piv-swarm-example/)
- [x] Analyzed directory structure (using ls/find)
- [x] Located key files using search patterns
- [x] Read 1-2 example files (piv-swarm-example/src/main.py, pyproject.toml)
- [x] Reviewed recent commits (last 10)
- [x] Checked current branch and status
- [x] Mapped architecture patterns (24 skills, 15 reference docs)
- [x] Understood testing structure (three-tier in piv-swarm-example)
- [x] Listed recent research (10 documents from last 2 weeks)
- [x] Extracted naming conventions from CLAUDE.md
- [x] Generated context report with "read more" pointers
- [x] Saved report to `.agents/init-context/`

---

## Success Criteria: ✅ PASSED

This context report is:

- **Comprehensive** - Covers structure, conventions, key patterns, and strategic goals
- **Actionable** - Provides specific file references for deeper reading when needed
- **Current** - Reflects actual state of code (main branch, commit f62a040, clean status)
- **Scannable** - Organized with clear sections and tables
- **Balanced** - Enough context to start planning, pointers for deep dives
- **Preserved** - Saved to `.agents/init-context/py-ai-starter-kit-context-2026-02-02.md`

**Result:** Comprehensive understanding of py-ai-starter-kit achieved. Ready to plan features that align with existing patterns and strategic goals.

---

_Generated by /prime command • 2026-02-02_
