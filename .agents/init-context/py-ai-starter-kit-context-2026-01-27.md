# py-ai-starter-kit Context Report

**Generated:** 2026-01-27
**Branch:** main
**Agent:** Claude Sonnet 4.5
**Git Status:** Clean working tree (main branch)

---

## Project Overview

**Purpose:** Python AI Starter Kit - A comprehensive methodology framework for systematic AI-assisted software development using the PIV (Prime → Implement → Validate) Loop. This is NOT a deployable application but a toolkit of commands, workflows, reference documentation, and best practices for high-quality AI-driven development.

**Version:** N/A (Methodology framework)

**Technologies:**
- **Language:** Python (methodology designed for Python projects)
- **Development Methodology:** PIV Loop (Prime → Implement → Validate)
- **Package Manager:** UV (blazing-fast Python package/environment management)
- **Quality Tools:**
  - ruff (linting & formatting, replaces Black/flake8)
  - mypy (type checking)
  - pytest (testing framework with coverage)
- **VCS:** Git with GitHub Flow workflow
- **Documentation Format:** Markdown with Claude Code skills system

**Key Capabilities:**
- Complete development workflow commands (12 commands across 5 categories)
- Context-first development philosophy ("Context is King")
- Multi-tier testing strategy (unit/integration/e2e)
- Institutional knowledge preservation through `.agents/` artifacts
- AI-assisted code review and root cause analysis
- Comprehensive reference documentation (15 best practices documents)
- Research-backed approach (6 research documents analyzing Anthropic patterns)
- Strategic roadmap (21 major goals in GOALS.md)

---

## Architecture

**Pattern:** Methodology and command framework (not a traditional application architecture)

**Core Philosophy:** "Context is King, Sessions are Natural, Quality is Non-Negotiable"

### Directory Structure

```
py-ai-starter-kit/
├── .agents/                      # PIV Loop artifact storage
│   ├── init-context/            # Context reports from /prime (3 existing)
│   ├── plans/                   # Feature plans from /plan-feature (empty)
│   ├── execution-reports/       # Post-implementation feedback (empty)
│   ├── research/                # Research documents (6 files)
│   │   ├── SPEC-CREATION-PROCESS.md
│   │   ├── ANTHROPIC-HARNESS-COMPARISON.md
│   │   ├── TAX-ANALYSIS-SESSION-COMPARISON.md
│   │   ├── CONTEXT-OPTIMIZATION-RESEARCH.md
│   │   ├── PRIME-OPTIMIZATION-RECOMMENDATIONS.md
│   │   └── RESEARCH-ANALYSIS.md
│   ├── specs/                   # Implementation specifications
│   │   ├── UW-PORTAL-TAX-ANALYSIS-SPEC.md (example from other project)
│   │   └── tax_analysis_spec.txt
│   ├── analytics/               # Token tracking, metrics (empty - future)
│   ├── architecture/            # Architecture Decision Records (empty - future)
│   ├── decisions/               # Decision log (empty - future)
│   ├── features/                # Feature tracking (empty - future)
│   └── progress/                # Session progress tracking (empty - future)
│
├── .claude/                      # Claude Code configuration
│   ├── commands/                # Skill implementations (12 commands)
│   │   ├── core_piv_loop/       # prime.md, plan-feature.md, implement-plan.md
│   │   ├── validation/          # validate.md, code-review.md, code-review-since.md, execution-report.md
│   │   ├── bug_fix/             # rca.md, implement-fix.md
│   │   └── git/                 # commit.md
│   ├── reference/               # Best practices documentation (15 files)
│   │   ├── piv-loop-methodology.md
│   │   ├── style-conventions.md
│   │   ├── fastapi-best-practices.md
│   │   ├── pydantic-best-practices.md
│   │   ├── pytest-best-practices.md
│   │   ├── aws-lambda-best-practices.md
│   │   ├── database-standards.md
│   │   ├── security-best-practices.md
│   │   ├── error-handling-patterns.md
│   │   ├── performance-optimization.md
│   │   ├── uv-package-manager.md
│   │   ├── git-workflow.md
│   │   ├── rg-search-patterns.md
│   │   ├── changelog-best-practices.md
│   │   └── habit-tracker-example.md
│   ├── schemas/                 # Schema definitions (untracked)
│   ├── skills/                  # Skill metadata (12 SKILL.md files)
│   └── PIV-LOOP.md              # Core methodology documentation (763 lines)
│
├── piv-swarm-example/           # Example project structure
│   ├── .agents/state/           # Agent state files (3 yaml files)
│   ├── .claude/commands/        # Agent commands (orchestrator, agents, state, tasks)
│   ├── src/                     # Source code (main.py, api/, models/, services/)
│   ├── tests/                   # Test suite (unit/, integration/)
│   ├── CLAUDE.md                # Project-specific guidelines
│   └── pyproject.toml           # Project configuration
│
├── piv-swarm/                   # PIV Swarm workspace (in development)
│   └── examples/                # Examples directory
│
├── research/                    # User research directory
├── tmp/                         # Temporary files
│
├── CLAUDE.md                    # PRIMARY development guidelines (394 lines)
├── CLAUDE_OG.md                 # Original version (archival reference)
├── CLAUDE-TEMPLATE.md           # Template for new projects
├── GOALS.md                     # Strategic roadmap (1656 lines, 21 major goals)
├── my-current-process.md        # User's documented workflow (18 lines)
├── FEEDBACK_IDEAS.md            # Improvement tracking (15 lines)
├── notes.md                     # General notes
├── .gitignore                   # Git ignore rules
└── (no pyproject.toml)          # Framework itself has no dependencies
```

---

## Command Inventory

**12 Commands Available** (organized by category)

### Core PIV Loop (3 commands)

| Command | File | Purpose | Output |
|---------|------|---------|--------|
| `/prime` | core_piv_loop/prime.md | Establish comprehensive codebase context | `.agents/init-context/{project}-context-{date}.md` |
| `/plan-feature {name}` | core_piv_loop/plan-feature.md | Create detailed implementation plan with patterns | `.agents/plans/{feature-name}.md` |
| `/implement-plan {file}` | core_piv_loop/implement-plan.md | Execute plan with incremental validation | Working code + deviations log |

### Validation (4 commands)

| Command | File | Purpose | Output |
|---------|------|---------|--------|
| `/validate` | validation/validate.md | Multi-stage quality gates (lint, type, test, coverage) | Validation report |
| `/code-review` | validation/code-review.md | AI-driven 5-dimension code review | `.agents/code-reviews/{feature}-review.md` |
| `/code-review-since {ref}` | validation/code-review-since.md | Review changes since commit/branch | Review report for delta |
| `/execution-report {plan}` | validation/execution-report.md | Post-implementation feedback loop | `.agents/execution-reports/{feature}-report.md` |

### Bug Fix (2 commands)

| Command | File | Purpose | Output |
|---------|------|---------|--------|
| `/rca {issue}` | bug_fix/rca.md | 6-phase root cause analysis | `.agents/rca/issue-{number}.md` |
| `/implement-fix` | bug_fix/implement-fix.md | Execute fix from RCA document | Bug fix + tests |

### Git (1 command)

| Command | File | Purpose | Output |
|---------|------|---------|--------|
| `/commit` | git/commit.md | Semantic commit with proper formatting | Git commit with Co-Authored-By |

### Spec/PRP (2 commands)

| Command | File | Purpose | Output |
|---------|------|---------|--------|
| `/generate-prp` | generate-prp.md | Create Product Requirements Plan | PRP document |
| `/execute-prp` | execute-prp.md | Execute BASE PRP | Implementation |

---

## Tech Stack Details

### Package Management: UV

**Why UV:**
- 10-100x faster than pip
- Unified tool (replaces pip, pip-tools, virtualenv, pipx)
- Deterministic resolution
- Lockfile support

**Key Commands:**
```bash
uv venv                    # Create virtual environment
uv sync                    # Sync dependencies from lockfile
uv add requests            # Add package (updates pyproject.toml)
uv add --dev pytest        # Add dev dependency
uv run python script.py    # Run in environment
uv run pytest              # Run tests in environment
```

**NEVER manually edit pyproject.toml** - always use `uv add`

### Code Quality Tools

**Ruff** (Linting & Formatting)
- Replaces Black, flake8, isort
- 10-100x faster than Black
- Line length: 100 characters
- Double quotes enforced

```bash
uv run ruff format .       # Format code
uv run ruff check .        # Lint code
```

**Mypy** (Type Checking)
- Type hints required for ALL functions
- Pydantic v2 integration

```bash
uv run mypy app/           # Type check
```

**Pytest** (Testing)
- Three-tier structure: unit/integration/e2e
- Coverage threshold: 80% minimum
- Markers for test classification

```bash
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -m "not very_slow" -v
uv run pytest --cov=app --cov-fail-under=80
```

---

## Core Principles (from CLAUDE.md)

### Development Philosophy

**KISS (Keep It Simple, Stupid)**
- Choose straightforward solutions over complex ones
- Simple solutions are easier to understand, maintain, debug

**YAGNI (You Aren't Gonna Need It)**
- Implement features only when needed
- Don't build on speculation

**Design Principles**
- **Dependency Inversion:** High-level modules depend on abstractions
- **Open/Closed Principle:** Open for extension, closed for modification
- **Single Responsibility:** Each function/class/module has one clear purpose
- **Fail Fast:** Check errors early, raise exceptions immediately

### Code Standards

**Structure:**
- File length: **Max 500 lines** (refactor if exceeding)
- Function length: **Max 100 lines** (single responsibility)
- Line length: **100 characters** (enforced by ruff)

**Type Hints:**
- **Required everywhere** - function signatures, class attributes
- Use `pydantic` v2 for data validation

**Naming Conventions:**
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private attributes/methods: `_leading_underscore`
- Database primary keys: Entity-specific (`session_id`, `lead_id`, NOT `id`)

**Imports:**
- Follow PEP8
- Use double quotes for strings
- Format with `ruff format`

### Testing Strategy

**Three-Tier Structure:**

1. **Unit Tests** (`tests/unit/`)
   - Purpose: Test business logic in isolation
   - Speed: < 1 second per test
   - Mocking: All I/O operations mocked
   - When: Every commit, during development

2. **Integration Tests** (`tests/integration/`)
   - Purpose: Test service interactions, API integrations
   - Speed: 1-30 seconds
   - Mocking: Minimal - prefer real dependencies
   - When: Before PR, during CI

3. **E2E Tests** (`tests/e2e/`)
   - Purpose: Test complete user workflows
   - Speed: > 30 seconds
   - Mocking: None - real system behavior
   - When: Before merge to main, before releases

**Coverage Requirements:**
- Target: 80% minimum
- Branch coverage enabled
- CI fails if < 80%

---

## PIV Loop Methodology

### The Three Phases

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   PRIME                 IMPLEMENT              VALIDATE │
│   ↓                     ↓                      ↓        │
│   Context ──────────→   Execution ─────────→   Quality │
│   Establishment         with                   Gates    │
│                        Incremental                      │
│                        Validation                       │
│                                                         │
│   ↓                     ↓                      ↓        │
│   Context Report ───→   Working Code ──────→   Ready   │
│                        + Deviations            to       │
│                                               Commit    │
│                                                         │
└─────────────────────────────────────────────────────────┘
                            │
                            ↓
                    Execution Report
                    (Feedback Loop)
```

### Phase 1: PRIME (Context Establishment)

**Purpose:** Understand codebase BEFORE planning/implementation

**Process:**
1. Analyze project structure (`git ls-files`, `find`)
2. Read core documentation (CLAUDE.md, README.md, PIV-LOOP.md)
3. Identify key files (entry points, models, services, tests)
4. Understand current state (`git status`, `git log`)
5. Map architecture (patterns, data flow, integrations)
6. Review recent plans (if any)

**Output:** `.agents/init-context/{project}-context-{date}.md`

### Phase 2: IMPLEMENT (Execution with Validation)

**Step 2.1: Planning** (`/plan-feature`)

Five-phase planning process:
1. **Feature Understanding** - Extract core problems, user value
2. **Codebase Intelligence** - Find similar patterns, conventions
3. **External Research** - Library docs, examples, best practices
4. **Strategic Thinking** - Architecture fit, dependencies, edge cases
5. **Plan Generation** - Structured markdown with complete code examples

**Output:** `.agents/plans/{feature-name}.md`

**Step 2.2: Implementation** (`/implement-plan`)

Sequential execution with incremental validation:
1. Preparation - Read plan, verify baseline
2. Task-by-task execution following patterns exactly
3. Validation after EACH task (ruff, mypy, pytest)
4. Deviation tracking (type, rationale, impact)
5. Issue resolution loop (never accumulate failures)
6. Progress updates

**Critical Rules:**
- ❌ NEVER skip validation steps
- ❌ NEVER proceed if validation fails
- ❌ NEVER accumulate multiple failures
- ✅ ALWAYS fix issues immediately
- ✅ ALWAYS document deviations
- ✅ ALWAYS verify baseline before starting

### Phase 3: VALIDATE (Quality Gates)

**Command:** `/validate` or `/validate --full`

**Default Validation (4 stages):**
1. **Static Analysis** - ruff check, mypy (< 5 seconds)
2. **Unit Tests** - pytest tests/unit/ (< 30 seconds)
3. **Fast Integration Tests** - pytest tests/integration/ -m "not very_slow" (< 2 minutes)
4. **Coverage Analysis** - pytest with --cov, --cov-fail-under=80

**Full Validation (6 stages, use --full):**
5. **E2E Tests** - pytest tests/e2e/
6. **Security Checks** - bandit -r app/ -ll (optional)

**Pass Criteria:** All stages must pass (0 errors, 80%+ coverage, all tests passing)

---

## Reference Documentation

**15 Documents in `.claude/reference/`**

### Core Methodology
- `piv-loop-methodology.md` - Complete 763-line PIV Loop guide

### Code Standards
- `style-conventions.md` - Naming, docstrings, imports, organization
- `fastapi-best-practices.md` - API patterns, dependencies, async
- `pydantic-best-practices.md` - Validation, V2 syntax, settings
- `pytest-best-practices.md` - Test organization, fixtures, mocking

### Infrastructure
- `aws-lambda-best-practices.md` - Serverless patterns, cold starts, Secrets Manager
- `database-standards.md` - Naming conventions, repository patterns, models

### Quality & Security
- `security-best-practices.md` - Input validation, secrets, SQL injection, OWASP
- `error-handling-patterns.md` - Custom exceptions, logging, retry patterns
- `performance-optimization.md` - Profiling, caching, async I/O, query optimization

### Tools & Workflow
- `uv-package-manager.md` - UV usage, dependency management, lockfiles
- `git-workflow.md` - Branching strategy (GitHub Flow), semantic commits
- `rg-search-patterns.md` - Ripgrep patterns (NEVER use grep/find!)
- `changelog-best-practices.md` - Version management, PR workflow

### Examples
- `habit-tracker-example.md` - Example CLAUDE.md structure for habit tracker app

---

## Research Artifacts

**6 Research Documents in `.agents/research/`**

| Document | Lines | Key Insights |
|----------|-------|--------------|
| `SPEC-CREATION-PROCESS.md` | - | Process from requirements → implementation spec (Anthropic XML format) |
| `ANTHROPIC-HARNESS-COMPARISON.md` | - | Analysis of Anthropic's multi-session architecture patterns |
| `TAX-ANALYSIS-SESSION-COMPARISON.md` | - | Real-world comparison of single-session vs multi-session workflows |
| `CONTEXT-OPTIMIZATION-RESEARCH.md` | - | Prompt caching, conversation compaction, PreCompact hooks (60-90% savings) |
| `PRIME-OPTIMIZATION-RECOMMENDATIONS.md` | - | Token-efficient priming strategies |
| `RESEARCH-ANALYSIS.md` | - | General research analysis documentation |
| `GSD-VS-PIV-ANALYSIS.md` | - | Comparison with "Get Shit Done" approach |

**Key Research Findings:**
- Multi-session architecture prevents token exhaustion
- Prompt caching can save 60-90% costs with 1-hour TTL
- Conversation compaction achieves 50-60% token reduction
- Anthropic uses XML-based specs for implementation
- Session management with checkpointing is critical

---

## Strategic Roadmap (from GOALS.md)

**1656 lines, 21 major goals organized by priority**

### Priority 1: Foundation (This Month)

1. **Spec Creation Process** (Status: Research complete, implementation pending)
   - Build `/create-spec` command
   - Create spec templates (API, data processing, UI, refactoring)
   - Integrate with `/plan-feature`
   - Validate on 2-3 real features

2. **Session Management System** (Status: Not started)
   - Live progress tracking (`.agents/progress/current-session.txt`)
   - Session startup rituals (verify location, read progress, check git, run tests)
   - Automatic checkpointing at 75-88% token usage
   - Session metrics (tokens, tasks, time)

3. **Multi-Session Architecture by Default** (Status: Not started)
   - `/prime --quick` mode (~8K tokens for known codebases)
   - `/prime --full` mode (~45K tokens for new/unfamiliar)
   - Session-aware planning (20-40K tokens per session)
   - Phase-based implementation with breakpoints

4. **Token Budget Management System** (Status: Not started)
   - Pre-flight estimation before work starts
   - Real-time tracking with progress bars
   - Historical analysis for accuracy improvement
   - Cost visibility (tokens → dollars)
   - Token warnings at 25%, 50%, 75%, 88%

### Priority 2: Core Skills & Workflows (This Quarter)

5. **Comprehensive Skills Tree** (Status: Partially complete - 12 commands exist)
   - Atomic skills (context, planning, implementation, quality, git, analysis)
   - Compound skills (quick-fix, feature-full, refactor-safe, investigate)
   - Custom workflows (YAML-defined)
   - Profiling & optimization skills (`/profile`, `/benchmark`, `/optimize`)

6. **JSON Features Tracking System** (Status: Not started)
   - `feature_list.json` as single source of truth
   - Immutable test steps, mutable status
   - Progress visualization
   - Integration with implementation workflow

7. **Test-Driven Development (TDD) Culture** (Status: Partially implemented)
   - Enforce Red-Green-Refactor cycle in `/implement-plan`
   - Test templates for common patterns
   - Coverage reporting with per-module breakdown

8. **Standard Development Flow** (Status: Documented)
   - 7-stage container pattern documented in `SPEC-CREATION-PROCESS.md`
   - Requirements → Discovery → Spec → Planning → Implementation → QA → Finalization

9. **Profiling & Optimization System** (Status: Not started)
   - CPU profiling (`/profile-cpu` with cProfile + snakeviz)
   - Memory profiling (`/profile-memory` with memory_profiler)
   - I/O profiling (`/profile-io` for queries, N+1 detection)
   - Benchmark framework with performance regression detection
   - Automated optimization recommendations

### Priority 3: Quality & Conventions (This Quarter)

10. **Language-Specific Coding Standards** (Status: Python complete)
11. **Project Ownership & Documentation** (Status: Not started - OWNERS, ADRs, decision log)
12. **Configurable Autonomy Levels** (Status: Not started - 5 levels from supervised to autonomous)
13. **Standard Folder Structures** (Status: Python complete)

### Priority 4: Advanced Features (Future - Month 6+)

14. Smart Context Management
15. Cost Tracking & Optimization
16. Linear Integration (Optional)
17. Cross-Project Pattern Library
18. Feedback Loop Analytics
19. Developer Onboarding System
20. Multi-Provider Abstraction
21. Advanced Context Optimization Patterns (Research complete)

---

## Current State

**Branch:** main

**Git Status:**
- Working tree: Clean
- Untracked: `.claude/schemas/`, `.claude/skills/plan/`, `.claude/skills/spec/`

**Recent Commits (last 10):**
```
c90ea98 (HEAD -> main, origin/main) Adding template instructions.
7e2502f Testing a few renditions of claude skills and building the best workflow.
d562fbe Updated research and structure as well as Goals. Still working out the idea for the final product but getting close.
c0604ae Michael made me write out my current process so I figured I would document that somewhere.
64cca90 Added gsd link.
af3260b Added a feedback & ideas file to track all my thoughts on things that can be improved.
72002af Added the code-review-since feature.
ae9e9ba Added info about pre-compacting rules and when we should do certain actions, research.
a1b1cce Building out an analysis of the best way to use claude code in python. This is not finished just a starting place.
3715afe Create execute-prp.md
```

**Recent Focus:**
- Template instructions for new projects (CLAUDE-TEMPLATE.md)
- Testing different skill renditions for optimal workflow
- Research into Anthropic patterns and multi-session architecture
- User workflow documentation (my-current-process.md)
- Adding code-review-since command for pre-push validation

**Active Plans:** None (`.agents/plans/` is empty)

**Active Specs:**
- `.agents/specs/UW-PORTAL-TAX-ANALYSIS-SPEC.md` - Example spec from uw-portal-api project (reference only)
- `.agents/specs/tax_analysis_spec.txt` - Text format version

---

## User's Current Workflow

**Documented in `my-current-process.md` (18 lines)**

1. **Planning Phase** (Opus conversation)
   - Discuss feature idea with context about input/output data formats
   - Mention TDD (Test Driven Development)
   - Ask/answer clarifying questions
   - Use `/plan-feature` in same context to create plan.md
   - Manual review (sometimes ask new context to critique plan)

2. **Implementation Phase** (New context)
   - Run `/implement-plan plan.md` (note: usually runs `/prime` first, but not this time)
   - Watch for plan adherence (newer command, may need refinement)
   - Verify all tests pass
   - Manual testing: run server, check functionality

3. **Code Review Phase** (New context)
   - Run `/prime` then `/code-review`
   - Fix critical findings in same context
   - Manual review (run server, check functionality)
   - Commit changes

4. **Pre-Push Review** (New context)
   - Run `/prime` then `/code-review-since <ref>` (ref = commit or dev/main branch point)

**Key Observations:**
- User prefers **fresh contexts** between major phases
- Strong **TDD emphasis** in planning
- Manual testing includes **running server** and functional checks
- **Code-review-since** used as quality gate before pushing to main
- Note that `/implement-plan` is "newer rendition" and may need work

---

## Feedback & Ideas

**From `FEEDBACK_IDEAS.md` (15 lines)**

**Improvement Areas:**
1. Full tests-first deployment workflow
2. More efficient prime function for large codebases

**Company/Team Issues:**
- Everyone using AI differently, no consistency
- Need for similar systems across developers

**Referenced Solution:**
- https://github.com/glittercowboy/get-shit-done - Alternative approach for comparison

---

## Example Projects

### piv-swarm-example/

**Purpose:** Example project structure showing PIV methodology applied to a simple Todo API

**Tech Stack:**
- Python 3.11+
- FastAPI
- Pydantic v2
- pytest

**Structure:**
```
piv-swarm-example/
├── .agents/state/           # State management (agents.yaml, messages.yaml, session.yaml)
├── .claude/commands/        # Agent-specific commands
│   ├── agents/             # debugger, executor, researcher, reviewer
│   ├── orchestrator/       # discuss, execute, plan, prime, validate
│   ├── state/              # assign, pause, resume, status
│   └── tasks/              # complete, create, list, update
├── src/
│   ├── main.py             # FastAPI app
│   ├── api/                # Route handlers
│   ├── models/             # Pydantic models
│   └── services/           # Business logic
├── tests/
│   ├── unit/               # Unit tests
│   └── integration/        # API tests
├── CLAUDE.md               # Project-specific guidelines (51 lines)
└── pyproject.toml          # Dependencies and config
```

**Key Differences from Main:**
- Contains actual Python code (main.py exists)
- Has agent orchestration system (state management, swarm commands)
- Simpler CLAUDE.md (51 lines vs 394 lines in main)
- Line length: 100 (matches main standards)

---

## Key Patterns to Follow

### 1. PIV Loop Discipline

**Always follow the sequence:**
```
PRIME (Context) → IMPLEMENT (Execution) → VALIDATE (Quality) → Feedback Loop
```

**Never skip steps:**
- Don't plan without priming
- Don't implement without planning
- Don't commit without validating
- Don't move on without execution reports

### 2. Search Commands - CRITICAL

**ALWAYS use `rg` (ripgrep), NEVER `grep` or `find`:**

```bash
# ✅ CORRECT
rg "pattern"                      # Search content
rg --files -g "*.py"             # Find files
rg "pattern" -g "*.py"           # Search in specific files
rg "pattern" -A 3 -B 3           # Context lines

# ❌ WRONG - DON'T USE THESE
grep -r "pattern" .              # Use rg instead
find . -name "*.py"              # Use rg --files -g "*.py"
```

**Why:** Documented in `.claude/reference/rg-search-patterns.md`

### 3. Artifact Preservation

**Save all PIV outputs to `.agents/` for institutional knowledge:**

| Artifact Type | Directory | Format |
|---------------|-----------|--------|
| Context reports | `.agents/init-context/` | `{project}-context-{YYYY-MM-DD}.md` |
| Feature plans | `.agents/plans/` | `{feature-name}.md` |
| Execution reports | `.agents/execution-reports/` | `{feature-name}-report.md` |
| Code reviews | `.agents/code-reviews/` | `{feature-name}-review.md` |
| RCA documents | `.agents/rca/` | `issue-{number}.md` |
| Research | `.agents/research/` | `{TOPIC}.md` |
| Specs | `.agents/specs/` | `{FEATURE}-SPEC.md` or `.txt` |

### 4. Validation After Each Task

**Incremental validation prevents debt accumulation:**

```bash
# After EACH implementation task:
ruff check {file}              # Syntax check (< 1 second)
mypy {file}                    # Type check (< 5 seconds)
pytest tests/unit/test_{file}  # Unit tests (< 30 seconds)

# If any fail:
# 1. STOP immediately
# 2. Fix the issue
# 3. Re-run validation
# 4. Only proceed when ALL pass
```

**Never batch validate** - catch issues early when context is fresh.

### 5. Session Management (Future Pattern)

**Research indicates moving toward:**

```
.agents/progress/current-session.txt format:

Feature: [Feature Name] ([Linear Ticket])
Plan: .agents/plans/{plan-file}.md
Started: [Timestamp]
Current Session: [N]

COMPLETED:
✓ Phase 1, Task 1.1: [Task description] (Session 1, 18K tokens)

IN PROGRESS:
→ Phase 2, Task 2.3: [Task description] (45% complete)

REMAINING:
- Phase 2, Task 2.4: [Task description]
- Phase 3: Testing & Validation (4 tasks)

SESSION METRICS:
Token usage: ~67K / 200K (34%)
Tests passing: 12/12
Last commit: abc1234

BLOCKERS:
None
```

**Token Budget Monitoring:**
- 25% (50K): Log progress
- 50% (100K): Halfway notice
- 75% (150K): Warning - consider checkpoint
- 88% (175K): Critical - automatic checkpoint NOW

### 6. Git Workflow

**GitHub Flow pattern:**
```
main (protected) ← PR ← release/your-release from dev
                           ↑
                         dev ← PR ← feature/your-feature
```

**Daily workflow:**
1. `git checkout dev && git pull origin dev`
2. `git checkout -b feature/new-feature`
3. Make changes + tests
4. `git push origin feature/new-feature`
5. Create PR → Review → Merge to dev

**Commit format:**
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude <noreply@anthropic.com>
```

Types: feat, fix, docs, style, refactor, test, chore

**NEVER include "claude code" or "written by claude code" in commit messages**

### 7. Code Review Dimensions

**5-dimension evaluation:**
1. **Logic** - Correctness, edge cases, error handling
2. **Security** - Vulnerabilities, secrets exposure, OWASP issues
3. **Performance** - Efficiency, scalability, bottlenecks
4. **Quality** - DRY, complexity, naming, readability
5. **Standards** - CLAUDE.md adherence, conventions

**Score each dimension 1-10, target average: 8+**

---

## Critical Rules & Anti-Patterns

### DO ✅

- ✅ **Always Prime before planning** - Context is king
- ✅ **Include specific line numbers** in plans - Make references precise
- ✅ **Document gotchas explicitly** - Prevent predictable errors
- ✅ **Validate after each task** - Catch issues early
- ✅ **Fix before proceeding** - Never accumulate technical debt
- ✅ **Track deviations** - Learn from plan changes
- ✅ **Generate execution reports** - Close feedback loop
- ✅ **Update reference docs** - Share patterns with team
- ✅ **Use `rg` for search** - Never grep/find
- ✅ **Follow TDD** - Write tests first, watch them fail, make them pass
- ✅ **Keep files under 500 lines** - Refactor when exceeding
- ✅ **Type hints everywhere** - No function without types

### DON'T ❌

- ❌ **Don't skip Prime phase** - Assumptions lead to errors
- ❌ **Don't use pseudocode in plans** - Provide complete code examples
- ❌ **Don't batch validations** - Validate incrementally after each task
- ❌ **Don't ignore test failures** - Fix immediately before proceeding
- ❌ **Don't skip execution reports** - Miss learning opportunities
- ❌ **Don't work without context** - Always establish baseline
- ❌ **Don't use grep/find** - Use `rg` (ripgrep)
- ❌ **Don't manually edit pyproject.toml** - Use `uv add`
- ❌ **Don't commit without validation** - Run `/validate` first
- ❌ **Don't create files > 500 lines** - Refactor into modules
- ❌ **Don't accumulate multiple failures** - Fix immediately

---

## Observations & Recommendations

### Strengths

- ✅ **Comprehensive methodology** with clear phases and outputs
- ✅ **Extensive strategic planning** (GOALS.md: 1656 lines, 21 major goals)
- ✅ **Strong research foundation** (6 research documents analyzing Anthropic patterns)
- ✅ **User workflow documented** (my-current-process.md) for iteration
- ✅ **15 reference documents** cover Python best practices comprehensively
- ✅ **12 commands** cover full development lifecycle
- ✅ **Context-first philosophy** well articulated ("Context is King")
- ✅ **Example project** (piv-swarm-example) shows methodology in practice
- ✅ **Research-backed approach** (Anthropic patterns studied)

### Current Status

**What This Project IS:**
- Methodology framework and toolkit
- Command system for AI-assisted development
- Best practices documentation library
- Research on optimal AI development workflows

**What This Project IS NOT:**
- Deployable application
- Python codebase with business logic
- Library or package to install

**Artifact Status:**
- `.agents/init-context/` - 3 context reports (2026-01-23, 2026-01-26, 2026-01-27)
- `.agents/plans/` - Empty (no active feature plans)
- `.agents/execution-reports/` - Empty (no implementation feedback yet)
- `.agents/research/` - 6 documents (comprehensive research complete)
- `.agents/specs/` - 2 example specs (from different project)
- Other `.agents/` subdirectories - Empty (future systems)

### Gaps vs Strategic Goals

**Priority 1 Goals Status:**
1. ⬜ Spec Creation Process - Research done, `/create-spec` command pending
2. ⬜ Session Management System - Not started (progress files, checkpointing)
3. ⬜ Multi-Session Architecture - Not started (`/prime --quick`, phase-based planning)
4. ⬜ Token Budget Management - Not started (estimation, tracking, warnings)

**Priority 2 Goals Status:**
5. 🟡 Comprehensive Skills Tree - 12 commands exist, compound skills + custom workflows pending
6. ⬜ JSON Features Tracking - Not started (feature_list.json system)
7. 🟡 TDD Culture - `/validate` exists, Red-Green-Refactor enforcement pending
8. ✅ Standard Development Flow - Documented in research
9. ⬜ Profiling & Optimization - Not started (`/profile`, `/benchmark`, `/optimize`)

### Patterns to Continue

Based on user's documented workflow:

1. **Fresh contexts between phases** - User starts new conversation for prime/implement/review
2. **TDD emphasis** - Always mention test-driven development in planning
3. **Manual testing included** - Run server, check functionality (not just automated tests)
4. **Code-review-since before main** - Quality gate before pushing to protected branch
5. **Incremental validation** - After each task, not at end
6. **Plan critique optional** - Sometimes ask new context to review plan for complex features

### Recommended Next Actions

**Immediate (This Week):**
1. Use this context to work on features following existing PIV methodology
2. Generate execution reports after implementations to build feedback loop
3. Consider which Priority 1 goal to tackle first

**Short-term (This Month):**
1. Build `/create-spec` command (research already complete)
2. Implement session management progress files
3. Add token budget monitoring to existing commands
4. Test `/prime --quick` vs `/prime --full` patterns

**Medium-term (This Quarter):**
1. Expand skills tree with compound skills
2. Build profiling & optimization commands
3. Implement JSON features tracking
4. Add TDD enforcement to `/implement-plan`

---

## Success Metrics

### Planning Quality
- **Confidence score:** Target 8+/10 for one-pass success
- **Context completeness:** All necessary files referenced with line numbers
- **Pattern reuse:** Existing code examples included in plan
- **Gotcha documentation:** Non-obvious pitfalls explicitly flagged

### Implementation Quality
- **First-pass success rate:** % of tasks completed without revision
- **Deviation rate:** % of tasks that differed from plan (track and learn)
- **Validation pass rate:** % of tasks passing incremental validation first try
- **Time to completion:** Actual vs estimated (improve estimates over time)

### Overall Quality
- **Test coverage:** Maintain 80%+ threshold
- **Code review issues:** Target < 5 per feature
- **Bug recurrence rate:** % of bugs that reappear (should decrease)
- **Team velocity:** Features completed per sprint (should increase)

### Token Efficiency (Future)
- **Token usage accuracy:** Actual within 15% of estimated
- **Session efficiency:** < 5% sessions hit compaction
- **Cache hit rate:** 70%+ (when caching implemented)
- **Cost per feature:** Track and optimize over time

---

## Next Steps

Based on this context, you are now ready to:

### 1. Plan Features
```bash
/plan-feature {feature-name}
```
- Reference patterns in `.claude/reference/`
- Follow 5-phase planning process
- Include complete code examples
- Score confidence (target 8+/10)

### 2. Implement Features
```bash
/implement-plan .agents/plans/{feature-name}.md
```
- Sequential execution with validation after EACH task
- Track deviations from plan (type, rationale, impact)
- Fix issues immediately before proceeding
- Update todo list after each completion

### 3. Validate Code
```bash
/validate              # Default 4-stage validation
/validate --full       # Full 6-stage validation
```
- Stage 1: Static analysis (ruff, mypy)
- Stage 2: Unit tests
- Stage 3: Integration tests (fast)
- Stage 4: Coverage (80%+ required)
- Stage 5: E2E tests (--full only)
- Stage 6: Security (--full only)

### 4. Review Code
```bash
/code-review                           # Review all uncommitted changes
/code-review-since {commit/branch}     # Review since reference
```
- 5-dimension evaluation (logic, security, performance, quality, standards)
- Each dimension scored 1-10
- Actionable recommendations
- Use before main push

### 5. Generate Feedback
```bash
/execution-report .agents/plans/{feature-name}.md
```
- Close feedback loop
- Document what worked well
- Identify difficulties
- Recommend improvements
- Improve future planning

### 6. Commit Changes
```bash
/commit
```
- Semantic commit format
- Proper type and scope
- Co-Authored-By: Claude

---

## Validation Checklist

Prime completion checklist:

- [x] Read CLAUDE.md completely (394 lines)
- [x] Read PIV-LOOP.md (763 lines)
- [x] Read GOALS.md (1656 lines, 21 major goals)
- [x] Analyzed directory structure (root + piv-swarm-example)
- [x] Identified key files (12 commands, 15 reference docs, 6 research docs)
- [x] Reviewed recent commits (last 10)
- [x] Checked current branch and status (main, clean)
- [x] Understood methodology patterns (PIV Loop)
- [x] Reviewed user's current workflow (my-current-process.md)
- [x] Reviewed feedback and improvement ideas (FEEDBACK_IDEAS.md)
- [x] Reviewed research artifacts (6 comprehensive documents)
- [x] Extracted naming conventions and standards
- [x] Mapped command inventory (12 commands across 5 categories)
- [x] Understood three-tier testing strategy
- [x] Documented critical search command rules (rg not grep)
- [x] Generated comprehensive context report (this document)
- [x] Saved report to `.agents/init-context/py-ai-starter-kit-context-2026-01-27.md`

---

## Summary

**Project Type:** Python AI development methodology framework (starter kit)

**Core Philosophy:** "Context is King, Sessions are Natural, Quality is Non-Negotiable"

**Primary Use Case:** Systematic, high-quality AI-assisted software development using PIV Loop

**Current State:**
- Methodology comprehensively documented (CLAUDE.md, PIV-LOOP.md, GOALS.md)
- 12 commands implemented and operational
- 15 reference documents provide Python best practices
- 6 research documents inform strategic direction
- Strategic roadmap defined (21 major goals across 4 priorities)
- No Python application code (this IS the framework)
- Example project (piv-swarm-example) demonstrates methodology

**Key Differentiators:**
- Phase-gated development with validation at every step
- Institutional knowledge preservation through `.agents/` artifacts
- Research-backed approach (Anthropic patterns studied and documented)
- Multi-session architecture being designed (based on real-world learnings)
- Comprehensive documentation (15 best practices docs)
- User workflow documented for continuous improvement

**Ready for:**
1. Feature planning using `/plan-feature`
2. Implementation using `/implement-plan`
3. Validation using `/validate` or `/validate --full`
4. Code review using `/code-review` or `/code-review-since`
5. Feedback generation using `/execution-report`
6. Building Priority 1 goals (spec creation, session management, multi-session architecture, token budget)

**Token Efficiency Note:**
- This Prime report: ~52K tokens
- Future `/prime --quick` target: ~8K tokens (for known codebases)
- Future `/prime --full` target: ~45K tokens (for new/unfamiliar codebases)
- Current approach is comprehensive but will be optimized

---

**Context established. Ready to execute PIV Loop methodology.**
