# py-ai-starter-kit Context Report

**Generated:** 2026-02-04
**Branch:** main
**Last Commit:** cc04cc3 - more thoughts and feedbak.

---

## Executive Summary

**py-ai-starter-kit** is a comprehensive PIV-Swarm (Prime-Implement-Validate) autonomous engineering workflow system for Python projects using Claude Code. It provides a systematic, high-quality feature development methodology with session persistence and multi-agent support through 24+ Claude Code skills.

**Core Philosophy:** "Context is King" - Understand before acting, validate before proceeding, learn from every implementation.

**Current Status:** Active development with extensive skills library and two example projects (piv-swarm-example and hubspot-integration). Repository has uncommitted changes to commit skill and thoughts document, plus new untracked hubspot-integration directory.

---

## Project Structure

### Top-Level Organization

```
py-ai-starter-kit/
├── .agents/              # AI methodology artifacts (session state, research)
├── .claude/              # Claude Code configuration (skills, reference docs, schemas)
│   ├── skills/           # 24 PIV-Swarm skills
│   ├── reference/        # 15 best practice docs
│   ├── schemas/          # YAML schemas (task, session, architecture)
│   └── PIV-LOOP.md       # PIV methodology overview
├── examples/             # POC examples (pydantic-ai)
├── piv-swarm/            # Core PIV-Swarm documentation
├── piv-swarm-example/    # Example Todo API implementation (FastAPI)
├── hubspot-integration/  # HubSpot Python client module (NEW, untracked)
├── research/             # (empty - likely archived)
├── tmp/                  # Temporary files
├── CLAUDE.md             # Development standards and conventions
├── GOALS.md              # Strategic roadmap with 21 goals
├── README.md             # User-facing documentation
├── thoughts.md           # User feedback and improvement ideas (MODIFIED)
└── FEEDBACK_IDEAS.md     # User feedback tracking
```

### File Type Distribution

- **Markdown (131 files):** Primary documentation format
- **Python (12 files):** Implementation code in examples and hubspot-integration
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
- `commit` - Semantic commits with co-author attribution (MODIFIED)

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
- `pre-commit-hooks-guide.md` - Pre-commit hook patterns

### 3. Session State Management (.agents/)

**Directory Structure:**

```
.agents/
├── init-context/        # Context reports from /prime (2 existing)
├── specs/               # Anthropic XML specifications (2 specs)
├── tasks/               # Individual task-NNN.yaml files (empty)
├── state/               # session.yaml, STATE.md (3 state files)
├── research/            # 12 research documents (see below)
├── feedback/            # 4 feedback analysis documents
├── plans/               # Feature plans (1 plan: your-claude-engineer-integration)
├── execution-reports/   # Validation reports (empty currently)
├── progress/            # Progress tracking (empty)
├── analytics/           # Token usage, metrics (empty)
├── features/            # Feature tracking (empty)
├── architecture/        # ADRs (empty)
└── decisions/           # Decision log (empty)
```

**Recent Research & Feedback:**
- `your-claude-engineer-analysis-2026-02-02.md` - Analysis of YCE integration
- `methodology-synthesis-analysis-2026-02-02.md` - Methodology synthesis
- `linus-mode-brutal-feedback-2026-02-03.md` - Brutal critique feedback
- `hyper-critical-thoughts-analysis-2026-02-02.md` - Critical analysis
- `multi-session-token-tracking-issue-2026-02-02.md` - Token tracking issues
- `CONTEXT-OPTIMIZATION-RESEARCH.md` - Prompt caching, compaction patterns
- `GSD-VS-PIV-ANALYSIS.md` - Workflow comparison

### 4. Example Implementations

#### A. piv-swarm-example/ - Minimal Todo API

**Purpose:** Demonstrate PIV-Swarm patterns with minimal FastAPI app

**Structure:**
- **Framework:** FastAPI 0.109.0+
- **Python:** 3.11+
- **Entry Point:** `src/main.py` - Simple health check endpoint
- **Directories:**
  - `src/api/` - API endpoints (currently empty)
  - `src/models/` - Pydantic models (currently empty)
  - `src/services/` - Business logic (currently empty)
  - `tests/` - Three-tier tests (unit/integration/e2e, currently empty)
- **Dev Tools:** pytest, ruff, mypy, httpx
- **Status:** Minimal skeleton, ready for feature implementation

**Pattern Observed:** Clean FastAPI structure with type hints and docstrings.

#### B. hubspot-integration/ - HubSpot Python Client (NEW)

**Purpose:** Modular Python client for HubSpot API integration (untracked, in development)

**Structure:**
- **Main Code:** `src/hubspot_integration/`
  - `models.py` - Pydantic models for HubSpot objects (142 lines)
    - Models: HubSpotDeal, HubSpotCompany, HubSpotContact, HubSpotAssociation
    - Search models: DealSearchResult, CompanyWithDeals, SearchResults
    - Uses Pydantic v2 with Field descriptions and Config
  - `config.py` - Configuration management
  - `cli.py` - CLI interface
  - `setup_cli.py` - Setup CLI
- **Tests:** Three-tier structure (unit/, integration/, __pycache__)
  - `tests/unit/test_service.py` - Service tests
  - `tests/conftest.py` - pytest fixtures
  - Coverage: 82% (.coverage file present)
- **Examples:** `examples/basic_usage.py` and several demo scripts
- **Documentation:**
  - `README.md` - Main documentation
  - `QUICKSTART.md` - Quick start guide
  - `ARCHITECTURE.md` - Architecture overview
  - `ADAPTING.md` - Adaptation guide
  - `INSTALL.md` - Installation instructions
  - `GLOBAL_CLI_GUIDE.md` - CLI reference
  - `CLI_QUICK_REFERENCE.md` - CLI quick ref
  - `SEARCH_OPTIONS_GUIDE.md` - Search guide
  - `FINAL_DECISION.md` - Design decisions
- **Demo Scripts:**
  - `test_connection.py` - Connection testing
  - `interactive_test.py` - Interactive testing
  - `smart_search_demo.py` - Smart search demo
  - `quick_search.py` - Quick search
  - `compare_options.py` - Option comparison
  - `demo_search_options.py` - Search options demo
  - `example_option2.py` - Option 2 example
- **Dev Environment:**
  - `.venv/` - Virtual environment
  - `.env` - Environment variables (contains secrets, gitignored)
  - `.env.example` - Example environment variables
  - `.gitignore` - Git ignore rules
  - `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` - Tool caches
  - `htmlcov/` - Coverage HTML report
- **Status:** Active development, comprehensive docs, 82% test coverage

**Pattern Observed:** Mature Python project structure following PIV best practices:
- Pydantic v2 models with type hints and field descriptions
- Three-tier testing with good coverage (82%)
- Comprehensive documentation
- CLI tooling
- Multiple example implementations

---

## Development Standards (from CLAUDE.md)

### Philosophy

**KISS (Keep It Simple):** Choose straightforward solutions over complex ones.
**YAGNI (You Aren't Gonna Need It):** Build features only when needed, not speculatively.
**Design Principles:** Dependency Inversion, Open/Closed, Single Responsibility, Fail Fast.

### Critical Policy: NO Timeline Predictions

**NEVER use:**
- Timeline language ("Week 1-2", "Q2 2026", "30-60 minutes")
- Duration predictions ("This will take X days/weeks/months")
- Time-based priorities ("Priority 1 = this quarter")
- Phrases like "defer to next quarter/year"

**ALWAYS use:**
- Priority framing ("First Priority", "High/Medium/Low Priority")
- "When do you need this?" or "What's urgent?"
- "Now vs later" not "this quarter vs next year"
- Assume AI-assisted development speed (fast iteration)

**Rationale:** AI-assisted development moves faster than traditional estimates. Features that seem "months away" can be completed in days. Let users determine urgency.

**Exception:** Technical performance metrics (e.g., "API responds in 5-10 seconds") are facts, not predictions.

### Code Structure Rules

- **Max file length:** 500 lines
- **Max function length:** 100 lines
- **Line length:** 100 characters (enforced by ruff)
- **Single Responsibility:** One clear purpose per function/class/module
- **Type hints:** Required for all function signatures and class attributes
- **Format with ruff:** Not Black (faster alternative)
- **Pydantic v2:** For data validation and settings

### Package Management (UV)

This project uses UV for blazing-fast Python package management.

**Key Commands:**
```bash
uv venv                    # Create virtual environment
uv sync                    # Install dependencies
uv add <package>           # Add package (NEVER edit pyproject.toml manually!)
uv add --dev <package>     # Add dev dependency
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
/plan-feature       # Create task files
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

1. **cc04cc3** (HEAD) - more thoughts and feedbak.
2. **f517509** - Working closer to what I actually want. Tried the current run through with some issues today and have built out some ideas to make that work better.
3. **f62a040** - Built out a bunch of skills not tested yet.
4. **610850a** - working on skills not finished.
5. **c90ea98** - Adding template instructions.
6. **7e2502f** - Testing a few renditions of claude skills and building best workflow
7. **d562fbe** - Updated research and structure as well as Goals
8. **c0604ae** - Michael made me write out my current process
9. **64cca90** - Added gsd link
10. **af3260b** - Added a feedback & ideas file

**Pattern:** Active skill development, methodology refinement, and practical testing with real projects (hubspot-integration). Recent focus on improving workflow based on hands-on experience.

---

## User Feedback Themes (from thoughts.md)

**Key improvement areas identified by user:**

1. **Autonomous Error Handling:** AI should find and fix errors by running tests independently, not requiring user babysitting
2. **Smart Context Usage:** Work within smart context window (<120k tokens), reset often, avoid wasting context on unnecessary reads
3. **Process Cleanup:** Kill subprocesses automatically to avoid blocking
4. **Orchestrator + Specialized Agents:** Need orchestrator + specialized agents (code review, documentation, etc.)
5. **Server Monitoring:** Always run as server when applicable to monitor errors
6. **Remove Timeline Language:** Completely eliminate timing/estimation from AI responses (already in CLAUDE.md)
7. **Meaningful Metrics:** Track tickets completed, code quality, first-time-right rate
8. **Documentation System:** Show commands and context used for each stage
9. **Early Design Conversations:** Review ideas/plans before implementation, not just code
10. **Tool Definitions & SOPs:** Document external tools (Linear, Sentry, AWS) and coding patterns
11. **Data Schema Knowledge:** Know how data is accessed and structured
12. **Strict Testing Standards:** Define expected data in tests, catch breaking changes
13. **Code Review Before Complete:** Always run code review before marking feature done
14. **Process Optimization:** Optimize workflow after validating correctness
15. **Scale Testing:** Build at-scale tests with faker data matching real schemas
16. **Platform Agnostic:** Build for ideas, not specific teams/platforms
17. **Data Caching:** Cache test data, validate with unseen subset
18. **Strict Validation:** Use strictest standards to reduce refactoring
19. **Failure Loop Detection:** Document failures and stop to avoid token waste
20. **Interaction Analysis:** Categorize AI interactions to improve workflow
21. **Model Optimization:** Use right model for task (opus=research, haiku=updates, sonnet=implementation)
22. **Skills with Code:** Build executable code into skills instead of markdown instructions
23. **Daily Reporting:** Output reports showing tickets/code/research completed
24. **Iterative Workflow:** Improve after every project, ask what could be better
25. **Logging:** Nice logging throughout
26. **Auditable Logs:** Track data sent to/from agents for scenario recreation
27. **Fast CI/CD:** GH Actions should not take an hour
28. **Coverage Granularity:** Check file-by-file coverage, not full suite
29. **Multi-language Support:** Use Rust, Go, C++ when best for task
30. **Post-completion Hooks:** Use hooks to run checks after AI thinks it's done
31. **Mermaid Diagrams:** Use mermaid for visual documentation
32. **Deep Think for Deadlocks:** Use deep think models when stuck, export conversation, revert code
33. **Multi-model Voting:** Use multiple models for consensus on code changes
34. **HubSpot Module Example:** Building modular HubSpot integration as proof-of-concept (hubspot-integration/)

---

## Current Project State

**Branch:** main
**Git Status:**
- Modified: `.claude/skills/commit/SKILL.md`
- Modified: `thoughts.md`
- Untracked: `hubspot-integration/` (entire directory)

**Recent Work:**
- User has been testing PIV workflow with real project (hubspot-integration)
- Documenting feedback and improvements based on hands-on experience
- Modifying commit skill based on learnings
- Building modular Python package following PIV best practices

**Active Plans:**
- `.agents/plans/your-claude-engineer-integration-plan.md` - Plan for YCE integration

**Ready for:**
- Committing hubspot-integration work
- Testing and refining 24 skills based on real project experience
- Implementing feedback from thoughts.md
- Goal implementation from GOALS.md

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

### Example Dependencies

- **pydantic-ai:** Multi-provider agent abstraction (in examples/)
- **HubSpot API:** Custom client implementation (in hubspot-integration/)

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

## Patterns Observed in Example Projects

### From piv-swarm-example/src/main.py:
- Clean FastAPI instantiation with title, description, version
- Type hints on return types (`dict[str, str]`)
- Docstrings on endpoints
- Health check pattern

### From hubspot-integration/src/hubspot_integration/models.py:
- Pydantic v2 with Field descriptions
- Flexible schema pattern (properties: dict[str, Any])
- Alias support (createdAt → created_at)
- Config with populate_by_name
- Rich models with computed properties (@property)
- Multiple data representation options (flat vs grouped)
- Search result models with convenience methods
- Comprehensive docstrings explaining model purpose

---

## Read More (On-Demand Reference Docs)

When working on specific areas, refer to these documents:

| Topic | Document |
|-------|----------|
| Development workflow, PIV loop | `.claude/reference/piv-loop-methodology.md` |
| Code style, naming, imports | `.claude/reference/style-conventions.md` |
| API endpoints, dependencies | `.claude/reference/fastapi-best-practices.md` |
| Data validation, settings | `.claude/reference/pydantic-best-practices.md` |
| Test patterns, fixtures, mocking | `.claude/reference/pytest-best-practices.md` |
| Lambda handlers, cold starts | `.claude/reference/aws-lambda-best-practices.md` |
| Security, input validation | `.claude/reference/security-best-practices.md` |
| Exception handling, logging | `.claude/reference/error-handling-patterns.md` |
| Database conventions, repos | `.claude/reference/database-standards.md` |
| Profiling, caching, async I/O | `.claude/reference/performance-optimization.md` |
| CHANGELOG format, PRs | `.claude/reference/changelog-best-practices.md` |
| UV package management | `.claude/reference/uv-package-manager.md` |
| Git branching, commits | `.claude/reference/git-workflow.md` |
| ripgrep search patterns | `.claude/reference/rg-search-patterns.md` |
| Example CLAUDE.md | `.claude/reference/habit-tracker-example.md` |
| Pre-commit hooks | `.claude/reference/pre-commit-hooks-guide.md` |

---

## Important Conventions

### From CLAUDE.md:

1. **Never assume or guess** - Ask for clarification
2. **Always verify file paths** before use
3. **Test your code** - No feature complete without tests
4. **Document decisions** - Future developers will thank you
5. **Keep CLAUDE.md updated** - Living document
6. **NO timeline language** - Use priority framing instead

### From README.md:

1. **Start every feature with /prime** - Context is critical
2. **Use /discuss for ambiguity** - Resolve gray areas upfront
3. **Validate frequently** - After each task, before merge
4. **Commit task files** - Preserve state in `.agents/` directory
5. **Use /pause between sessions** - Checkpoint before closing

### From Prime Skill:

1. **Shallow discovery** - Build map of WHERE things are, not WHAT they contain
2. **Read files on-demand** - When planning/implementation requires them
3. **Use --files-with-matches** - For locating, not reading
4. **Sample patterns** - Read 1-2 examples to see conventions applied
5. **Generate reports** - Save context for future reference

### From User Feedback (thoughts.md):

1. **Autonomous validation** - Run tests and fix errors without prompting
2. **Smart context usage** - Stay under 120k tokens, reset often
3. **Code review before done** - Always run /code-review before marking complete
4. **File-level coverage** - Check changed files individually, not full suite
5. **Multi-model strategy** - Use right model for task (opus/haiku/sonnet)

---

## Next Steps (Recommendations)

Based on current state, user feedback, and recent activity:

### High Priority:
1. **Commit hubspot-integration** - User has working module ready to commit
2. **Review and commit thoughts.md** - Capture user feedback improvements
3. **Update commit skill** - Changes in `.claude/skills/commit/SKILL.md` need review
4. **Document hubspot-integration learnings** - What worked well in PIV workflow?

### Medium Priority:
5. **Implement autonomous error detection** - Top feedback from thoughts.md
6. **Add file-level coverage skill** - Stop checking full suite unnecessarily
7. **Build post-completion hook system** - Auto-run checks after implementation
8. **Add process cleanup** - Kill subprocesses automatically

### Lower Priority:
9. **Test 24 skills systematically** - Use hubspot-integration as test case
10. **Multi-model voting experiment** - Proof of concept for consensus
11. **Daily output reporting** - Track tickets/code/research completed

---

## Checklist: Prime Completion

- [x] Read CLAUDE.md fully (noted reference docs for later)
- [x] Read README.md
- [x] No pyproject.toml in root (found in piv-swarm-example/)
- [x] Analyzed directory structure
- [x] Located key files using search patterns
- [x] Read example files (main.py, models.py from both projects)
- [x] Reviewed recent commits (last 10)
- [x] Checked current branch and status
- [x] Mapped architecture patterns (24 skills, 15 reference docs)
- [x] Understood testing structure (three-tier)
- [x] Listed recent research and feedback
- [x] Extracted naming conventions from CLAUDE.md
- [x] Analyzed user feedback from thoughts.md
- [x] Reviewed active plan (your-claude-engineer-integration)
- [x] Inspected new hubspot-integration project
- [x] Generated context report with actionable pointers
- [x] Saved report to `.agents/init-context/`

---

## Success Criteria: ✅ PASSED

This context report is:

- **Comprehensive** - Covers structure, conventions, patterns, user feedback, and active projects
- **Actionable** - Specific next steps based on current state and user priorities
- **Current** - Reflects actual state (main branch, cc04cc3, uncommitted changes, new project)
- **Scannable** - Clear sections, tables, and hierarchical organization
- **Balanced** - High-level overview with pointers to detailed docs
- **Preserved** - Saved to `.agents/init-context/py-ai-starter-kit-context-2026-02-04.md`

**Result:** Comprehensive understanding of py-ai-starter-kit achieved, including user feedback themes and real-world project example. Ready to plan features aligned with existing patterns and user priorities.

---

_Generated by /prime command • 2026-02-04_
