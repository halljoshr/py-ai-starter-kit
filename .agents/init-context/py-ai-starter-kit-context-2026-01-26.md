# py-ai-starter-kit Context Report

**Generated:** 2026-01-26
**Branch:** main
**Agent:** Claude Opus 4.5
**Git Status:** Clean (2 untracked files: context report, `which` file)

---

## Project Overview

**Purpose:** Python AI Starter Kit - A methodology framework and reference implementation for systematic AI-assisted software development using the PIV (Prime → Implement → Validate) Loop approach. This is NOT an application but a comprehensive toolkit of commands, workflows, and documentation for high-quality AI-driven development.

**Version:** N/A (Methodology framework, not deployable application)

**Technologies:**
- Language: Python (methodology designed for Python projects)
- Development Methodology: PIV Loop (Prime → Implement → Validate)
- Package Manager: UV (fast Python package management)
- Quality Tools: ruff (linting/formatting), mypy (type checking), pytest (testing)
- VCS: Git with GitHub Flow workflow

**Key Capabilities:**
- Complete development workflow commands (prime, plan-feature, implement-plan, validate, commit)
- Context-first development philosophy ("Context is King")
- Multi-tier testing strategy (unit/integration/e2e)
- Institutional knowledge preservation through `.agents/` artifacts
- AI-assisted code review and root cause analysis
- Comprehensive reference documentation (15 best practices docs)
- Research on context optimization and session management

---

## Architecture

**Pattern:** Methodology and command framework (not a traditional application architecture)

**Directory Structure:**
```
py-ai-starter-kit/
├── .agents/                    # PIV Loop artifact storage
│   ├── init-context/          # Context reports from /prime
│   ├── plans/                 # Feature plans from /plan-feature
│   ├── execution-reports/     # Implementation feedback
│   ├── research/              # Research documents (6 files)
│   ├── specs/                 # Implementation specifications
│   ├── analytics/             # (Empty - future token tracking)
│   ├── architecture/          # (Empty - future ADRs)
│   ├── decisions/             # (Empty - future decision log)
│   ├── features/              # (Empty - future feature tracking)
│   └── progress/              # (Empty - future session progress)
│
├── .claude/                    # Claude Code configuration
│   ├── commands/              # Skill implementations (12 commands)
│   │   ├── core_piv_loop/    # prime, plan-feature, implement-plan
│   │   ├── validation/       # validate, code-review, code-review-since, execution-report
│   │   ├── bug_fix/          # rca, implement-fix
│   │   └── git/              # commit
│   ├── reference/             # Best practices (15 documents)
│   └── PIV-LOOP.md           # Core methodology documentation
│
├── research/                   # User research directory
├── tmp/                        # Temporary files
│
├── CLAUDE.md                   # Primary development guidelines
├── CLAUDE_OG.md               # Original version (archival)
├── GOALS.md                   # Strategic roadmap (1600+ lines)
├── my-current-process.md      # User's workflow documentation
├── FEEDBACK_IDEAS.md          # Improvement tracking
└── .gitignore
```

**Key Artifact Directories:**
- `.agents/research/` - Contains 6 research documents on methodology optimization
- `.agents/specs/` - Contains UW-PORTAL-TAX-ANALYSIS-SPEC.md example
- `.agents/init-context/` - Previous context report from 2026-01-23

---

## Command Inventory

**12 Commands Available in `.claude/commands/`:**

### Core PIV Loop (3)
| Command | Purpose |
|---------|---------|
| `/prime` | Establish comprehensive codebase context |
| `/plan-feature {name}` | Create detailed implementation plan |
| `/implement-plan {file}` | Execute plan with incremental validation |

### Validation (4)
| Command | Purpose |
|---------|---------|
| `/validate` | Multi-stage quality gates (lint, type, test, coverage) |
| `/code-review` | AI-driven 5-dimension code review |
| `/code-review-since {ref}` | Review changes since commit/branch |
| `/execution-report {plan}` | Generate post-implementation feedback |

### Bug Fix (2)
| Command | Purpose |
|---------|---------|
| `/rca {issue}` | 6-phase root cause analysis |
| `/implement-fix` | Execute fix from RCA |

### Git (1)
| Command | Purpose |
|---------|---------|
| `/commit` | Semantic commit with proper formatting |

### Spec/PRP (2)
| Command | Purpose |
|---------|---------|
| `/generate-prp` | Create PRP (Product Requirements Plan) |
| `/execute-prp` | Execute BASE PRP |

---

## Reference Documentation

**15 Documents in `.claude/reference/`:**

### Core Methodology
- `piv-loop-methodology.md` - Complete PIV Loop guide (mirrors .claude/PIV-LOOP.md)

### Code Standards
- `style-conventions.md` - Naming, docstrings, imports, organization
- `fastapi-best-practices.md` - API patterns, dependencies, async
- `pydantic-best-practices.md` - Validation, V2 syntax, settings
- `pytest-best-practices.md` - Test organization, fixtures, mocking

### Infrastructure
- `aws-lambda-best-practices.md` - Serverless patterns, cold starts
- `database-standards.md` - Naming conventions, repository patterns

### Quality & Security
- `security-best-practices.md` - Input validation, secrets, OWASP
- `error-handling-patterns.md` - Exceptions, logging, retries
- `performance-optimization.md` - Profiling, caching, async I/O

### Tools & Workflow
- `uv-package-manager.md` - UV usage, dependency management
- `git-workflow.md` - Branching strategy, semantic commits
- `rg-search-patterns.md` - Ripgrep patterns (NEVER use grep/find)
- `changelog-best-practices.md` - Version management, PR workflow

### Examples
- `habit-tracker-example.md` - Example CLAUDE.md structure

---

## Research Artifacts

**6 Research Documents in `.agents/research/`:**

| Document | Purpose |
|----------|---------|
| `SPEC-CREATION-PROCESS.md` | Process from requirements → implementation spec |
| `ANTHROPIC-HARNESS-COMPARISON.md` | Analysis of Anthropic's multi-session approach |
| `TAX-ANALYSIS-SESSION-COMPARISON.md` | Real-world session analysis |
| `CONTEXT-OPTIMIZATION-RESEARCH.md` | Prompt caching, compaction strategies |
| `PRIME-OPTIMIZATION-RECOMMENDATIONS.md` | Token-efficient priming |
| `RESEARCH-ANALYSIS.md` | General analysis documentation |

---

## Core Principles (from CLAUDE.md)

**Development Philosophy:**
- **KISS** - Choose straightforward solutions over complex ones
- **YAGNI** - Implement features only when needed
- **Dependency Inversion** - High-level modules depend on abstractions
- **Open/Closed Principle** - Open for extension, closed for modification
- **Single Responsibility** - Each unit has one clear purpose
- **Fail Fast** - Check errors early, raise exceptions immediately

**Code Standards:**
- Line length: **100 characters**
- File length: **Max 500 lines**
- Function length: **Max 100 lines**
- Coverage threshold: **80% minimum**
- Type hints: **Required everywhere**
- String style: **Double quotes**

**Naming Conventions:**
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private: `_leading_underscore`
- Database PKs: Entity-specific (`session_id`, `lead_id`)

---

## Current State

**Branch:** main

**Status:**
- Working tree clean
- 2 untracked files (this context report, `which` file)

**Recent Commits (last 10):**
```
d562fbe (HEAD -> main, origin/main) Updated research and structure as well as Goals
c0604ae Michael made me write out my current process
64cca90 Added gsd link
af3260b Added feedback & ideas file
72002af Added the code-review-since feature
ae9e9ba Added info about pre-compacting rules research
a1b1cce Building out analysis of Python usage (incomplete)
3715afe Create execute-prp.md
dc14347 Create generate-prp.md
7545b70 Create CLAUDE.md
```

**Recent Focus:**
- Research into Anthropic's spec-driven development approach
- Documenting comprehensive GOALS.md (1600+ lines, 21 major goals)
- Adding session management and multi-session architecture research
- User's current workflow documentation (my-current-process.md)
- Code-review-since feature for pre-push validation

**Active Plans:** None (`.agents/plans/` empty)

**Active Specs:**
- `.agents/specs/UW-PORTAL-TAX-ANALYSIS-SPEC.md` - Example spec from uw-portal-api project

---

## Strategic Roadmap (from GOALS.md)

### Priority 1: Foundation (This Month)
1. **Spec Creation Process** - `/create-spec` command, templates, integration
2. **Session Management System** - Progress tracking, checkpointing, metrics
3. **Multi-Session Architecture** - `/prime --quick`, phase-based planning
4. **Token Budget Management** - Pre-flight estimation, real-time tracking

### Priority 2: Core Skills (This Quarter)
5. **Comprehensive Skills Tree** - Atomic and compound skills, custom workflows
6. **JSON Features Tracking** - feature_list.json for progress tracking
7. **TDD Culture Enforcement** - Red-Green-Refactor workflow
8. **Standard Development Flow** - 7-stage container pattern
9. **Profiling & Optimization** - `/profile`, `/benchmark`, `/optimize`

### Priority 3: Quality (This Quarter)
10. **Language-Specific Standards** - Python complete, expand as needed
11. **Project Ownership** - OWNERS file, decision log, ADRs
12. **Configurable Autonomy** - 5 levels from full supervision to full autonomy
13. **Standard Folder Structures** - Templates for `piv init [language]`

### Priority 4: Advanced (Future)
14. Smart Context Management
15. Cost Tracking & Optimization
16. Linear Integration
17. Cross-Project Pattern Library
18. Feedback Loop Analytics
19. Developer Onboarding System
20. Multi-Provider Abstraction
21. Advanced Context Optimization Patterns

---

## User's Current Workflow (from my-current-process.md)

**Documented Process:**
1. **Planning** - Talk to Opus about feature, mention TDD, clarify questions
2. **Plan Creation** - Use `/plan-feature` in same context
3. **Manual Review** - Review plan, optionally ask new context to critique
4. **Implementation** - New context, run `/implement-plan plan.md`
5. **Verification** - Watch for plan adherence, verify tests pass
6. **Manual Testing** - Run server, check functionality
7. **Code Review** - New context, `/prime` then `/code-review`
8. **Commit** - Fix critical findings, commit
9. **Pre-Push Review** - `/prime` then `/code-review-since <ref>` before main

**Key Observations:**
- User prefers fresh contexts between phases
- TDD emphasis in planning
- Manual review includes running server
- Code-review-since used before pushing to main
- Notes that `/implement-plan` is "newer rendition" and may need work

---

## Feedback & Ideas (from FEEDBACK_IDEAS.md)

**Improvement Areas:**
1. Full tests-first deployment workflow
2. More efficient prime function for large codebases

**Company Issues:**
- Everyone using AI differently, no consistency
- Developers should use similar systems

**Referenced Solution:**
- https://github.com/glittercowboy/get-shit-done

---

## Key Patterns to Follow

### PIV Loop Methodology
```
PRIME (Context) → IMPLEMENT (Execution) → VALIDATE (Quality) → Feedback Loop
```

**Critical Rules:**
- ❌ NEVER skip validation steps
- ❌ NEVER proceed if validation fails
- ❌ NEVER accumulate multiple failures
- ✅ ALWAYS fix issues immediately
- ✅ ALWAYS document deviations
- ✅ ALWAYS verify baseline before starting

### Search Commands
**CRITICAL:** Always use `rg` (ripgrep), NEVER `grep` or `find`:
```bash
# ✅ Correct
rg "pattern"
rg --files -g "*.py"

# ❌ Wrong
grep -r "pattern" .
find . -name "*.py"
```

### Artifact Preservation
Save all PIV outputs to `.agents/` for institutional knowledge:
- Context reports → `.agents/init-context/`
- Feature plans → `.agents/plans/`
- Execution reports → `.agents/execution-reports/`
- Research → `.agents/research/`
- Specs → `.agents/specs/`

### Session Management (Future)
Research indicates moving toward:
- Progress tracking files (current-session.txt)
- Token budget monitoring (25%, 50%, 75%, 88% thresholds)
- Automatic checkpointing
- Session startup rituals

---

## Observations & Recommendations

**Strengths:**
- ✅ Comprehensive methodology with clear phases and outputs
- ✅ Extensive GOALS.md provides strategic direction (21 major goals)
- ✅ Strong research foundation (6 research documents)
- ✅ User has documented real-world workflow for iteration
- ✅ 15 reference documents cover most Python patterns
- ✅ 12 commands cover full development lifecycle
- ✅ Context-first philosophy well articulated

**Areas of Note:**
- This is a **methodology framework**, not a deployable application
- No Python code exists - this is structure and documentation only
- `.agents/` largely empty - artifacts will accumulate with use
- GOALS.md is extensive (1600+ lines) - consider breaking into phases
- Session management system not yet implemented (Priority 1 goal)

**Current Status vs Goals:**
- Spec Creation: Research complete, tooling pending
- Session Management: Not started
- Multi-Session Architecture: Not started
- Token Budget Management: Not started
- Skills Tree: Partially complete (12 commands exist)

**Patterns to Continue:**
- Prime before planning: Always run `/prime` at conversation start
- Sequential validation: After EACH implementation task
- Artifact preservation: Save to `.agents/`
- Fresh contexts: User prefers between prime/implement/review
- Code-review-since before main push

---

## Next Steps

Based on this context, you are now ready to:

1. **Plan features** using `/plan-feature {name}`
   - Reference patterns in `.claude/reference/`
   - Follow 5-phase planning process
   - Include code examples

2. **Implement features** using `/implement-plan {plan-file}`
   - Sequential execution with validation after each task
   - Track deviations from plan
   - Fix issues immediately

3. **Validate code** using `/validate`
   - 4-stage default: linting, types, unit tests, coverage
   - 6-stage full: adds e2e and security

4. **Review code** using `/code-review` or `/code-review-since`
   - 5-dimension evaluation
   - Use code-review-since before main push

5. **Generate feedback** using `/execution-report {plan-file}`
   - Close feedback loop
   - Improve future planning

**Priority Implementation Work:**
Based on GOALS.md Priority 1, the next features to build are:
1. `/create-spec` command (spec templates, validation)
2. Session Management System (progress files, checkpointing)
3. `/prime --quick` mode for token efficiency
4. Token budget monitoring and warnings

---

## Validation Checklist

Prime completion checklist:

- [x] Read CLAUDE.md completely
- [x] Read PIV-LOOP.md
- [x] Read GOALS.md (comprehensive strategic roadmap)
- [x] Analyzed directory structure
- [x] Identified key files (commands, reference docs, research)
- [x] Reviewed recent commits (last 10)
- [x] Checked current branch and status
- [x] Understood methodology patterns (PIV Loop)
- [x] Reviewed user's current workflow (my-current-process.md)
- [x] Reviewed feedback and improvement ideas
- [x] Reviewed research artifacts (6 documents)
- [x] Extracted naming conventions and standards
- [x] Generated context report
- [x] Saved report to `.agents/init-context/`

---

## Summary

**Project Type:** Python AI development methodology framework (starter kit)

**Core Philosophy:** "Context is King, Sessions are Natural, Quality is Non-Negotiable"

**Primary Use Case:** Systematic, high-quality AI-assisted software development using PIV Loop

**Current State:**
- Methodology well-documented
- 12 commands implemented
- 15 reference documents available
- 6 research documents inform future direction
- GOALS.md provides extensive roadmap (21 major goals)
- No actual Python code yet - this is the framework itself

**Key Differentiators:**
- Phase-gated development with validation at every step
- Institutional knowledge preservation through artifacts
- Research-informed approach (Anthropic patterns studied)
- Multi-session architecture being designed
- Comprehensive documentation for Python best practices

**Ready for:** Feature planning, implementation, and validation following PIV Loop methodology
