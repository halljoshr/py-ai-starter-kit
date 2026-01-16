# PIV Loop Methodology

**Prime → Implement → Validate**

A systematic development methodology for high-quality, one-pass implementation success.

---

## Overview

The PIV Loop is a three-phase iterative development cycle that emphasizes:
- **Context-first development** - Understand before acting
- **Phase-gated execution** - Validate before proceeding
- **Continuous feedback** - Learn from each implementation
- **Institutional knowledge** - Preserve decisions in artifacts

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

---

## Phase 1: PRIME (Context Establishment)

**Command:** `/prime` or `.claude/commands/core_piv_loop/prime.md`

**Purpose:** Establish comprehensive codebase understanding BEFORE any planning or implementation work.

### When to Use Prime

- ✅ Start of new conversation
- ✅ Before planning major features
- ✅ After significant refactors
- ✅ When onboarding new team members
- ✅ After long breaks from the codebase

### Prime Process

1. **Analyze Project Structure**
   ```bash
   git ls-files                    # Enumerate all tracked files
   find . -type d -maxdepth 3      # Directory hierarchy
   ```

2. **Read Core Documentation**
   - CLAUDE.md (development standards)
   - README.md (project overview)
   - Recent plans in `.agents/plans/`
   - Package configuration (pyproject.toml)

3. **Identify Key Files**
   - Entry points (main.py, app entrypoints)
   - Configuration files (.env.example, configs/)
   - Data models (Pydantic models, schemas)
   - Service implementations (app/services/)
   - Test structure (tests/)

4. **Understand Current State**
   ```bash
   git status                      # Current branch and changes
   git log -10 --oneline          # Recent work
   git branch -a                   # Available branches
   ```

5. **Map Architecture**
   - Framework patterns (FastAPI routers, dependencies)
   - Data flow (request → services → agents → response)
   - External integrations (APIs, AWS services)
   - Testing approach (unit/integration/e2e)

### Prime Output

**Deliverable:** Context report saved to `.agents/init-context/{project-name}-context-{date}.md`

**Report Structure:**
```markdown
# {Project Name} Context Report

**Generated:** {Date}
**Branch:** {Current Branch}

## Project Overview
- **Purpose:** What the system does
- **Technologies:** Python, FastAPI, LangGraph, AWS Lambda, etc.
- **Version:** Current version from pyproject.toml

## Architecture
- **Pattern:** Event-driven, multi-agent workflow orchestration
- **Key Directories:**
  - app/ - Main application code
  - src/ - Source modules
  - tests/ - Test suite (unit/integration/e2e)
  - docs/ - Documentation and schemas

## Tech Stack
- **Language:** Python 3.9+
- **Frameworks:** FastAPI, LangGraph, Pydantic v2
- **AWS Services:** Bedrock, Secrets Manager, Lambda
- **Testing:** pytest, pytest-asyncio, pytest-cov
- **Tools:** UV, ruff, mypy, SAM CLI

## Core Principles (from CLAUDE.md)
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Dependency Inversion
- Single Responsibility
- Fail Fast

## Current State
- **Branch:** {branch name}
- **Recent Work:** {summary of last 5-10 commits}
- **Active Plans:** {any in-progress features}

## Key Patterns
- Database naming: entity-specific primary keys (session_id, lead_id)
- Repository pattern: BaseRepository with auto-derivation
- API routes: RESTful with consistent parameter naming
- Testing: 3-tier (unit/integration/e2e) with markers
- Validation: Multi-stage (linting, typing, tests, coverage)

## Observations
- {Any notable findings}
- {Areas that might need attention}
- {Patterns to follow}
```

### Benefits of Priming

- ✅ **Prevents assumptions** - Agent understands YOUR conventions
- ✅ **Reduces errors** - Fewer "I didn't know that existed" mistakes
- ✅ **Speeds up planning** - Context already gathered
- ✅ **Onboards conversations** - Each session starts with full context
- ✅ **Identifies patterns** - Recognizes existing solutions to follow

---

## Phase 2: IMPLEMENT (Execution with Validation)

**Command:** `/plan-feature` then `/implement-plan`

### Step 2.1: Planning

**Command:** `/plan-feature {feature-name}` or `.claude/commands/core_piv_loop/plan-feature.md`

**Purpose:** Create comprehensive feature plan with ALL context needed for one-pass implementation success.

#### Five-Phase Planning Process

**Phase 1: Feature Understanding**
- Extract core problems
- Identify user value
- Assess complexity
- Map affected systems

**Phase 2: Codebase Intelligence**
- Search for similar features/patterns
- Identify files to reference in plan
- Note existing conventions to follow
- Check test patterns for validation

**Phase 3: External Research**
- Library documentation (include specific URLs)
- Implementation examples (GitHub/StackOverflow)
- Best practices and common pitfalls
- Reference `.claude/reference/` docs

**Phase 4: Strategic Thinking**
- Consider architecture fit
- Identify dependencies between tasks
- Plan for edge cases
- Assess performance implications
- Evaluate security concerns
- Consider maintainability

**Phase 5: Plan Generation**
- Create structured markdown plan
- Include context reference tables
- Provide complete code examples
- Document gotchas explicitly
- Define atomic tasks with validation
- Score confidence (1-10)

#### Plan Document Structure

```markdown
# Feature Name

## Feature Understanding
- Problem statement
- User story
- Value proposition
- Complexity assessment

## Context References
| File | Purpose | Specific Lines |
|------|---------|----------------|
| app/services/example.py | Pattern to follow | Lines 45-67 |

## Patterns to Follow
[Extracted code examples from YOUR codebase]

## Implementation Tasks

### Task 1: [FILE PATH]
- **IMPLEMENT:** What to build
- **PATTERN:** Reference to existing code (file:line)
- **IMPORTS:** Required modules
- **GOTCHA:** Non-obvious pitfalls
- **VALIDATE:** Specific test command

```python
[Complete implementation code block]
```

### Task 2: [FILE PATH]
...

## Testing Strategy
- Unit tests: [Description]
- Integration tests: [Description]
- Coverage expectations: 80%+

## Acceptance Criteria
- [ ] Checkbox validation criteria
- [ ] Specific behaviors
- [ ] Expected outputs

## Confidence Score: X/10
[Rationale for score]
```

**Output:** `.agents/plans/{feature-name}.md`

---

### Step 2.2: Implementation

**Command:** `/implement-plan {plan-file}` or `.claude/commands/core_piv_loop/implement-plan.md`

**Purpose:** Execute plan systematically with validation at EVERY step.

#### Implementation Process

1. **Preparation**
   - Read ENTIRE plan document
   - Understand all dependencies
   - Note critical gotchas
   - Verify baseline (run tests before changes)

2. **Sequential Execution**
   - Implement each task in order
   - Follow patterns exactly as documented
   - Use complete code from plan (not pseudocode)

3. **Incremental Validation (After EACH Task)**
   ```bash
   # Run task-specific validation command
   ruff check {file}              # Syntax check
   mypy {file}                    # Type check
   pytest tests/unit/test_{file}  # Unit tests
   ```
   - ✅ If passes: Mark task complete, proceed
   - ❌ If fails: Debug and fix immediately, don't accumulate debt

4. **Deviation Tracking**
   - Document when implementation deviates from plan
   - Record TYPE: Added feature/Changed approach/Omitted task
   - Record RATIONALE: Why deviation was necessary
   - Record IMPACT: Effect on overall implementation

5. **Issue Resolution Loop**
   ```
   Implement → Validate → Pass?
                          ↓ No
                       Fix → Validate → Pass?
                                        ↓ Yes
                                     Proceed
   ```

6. **Progress Updates**
   - Update todo list after EACH task completion
   - Keep user informed of progress
   - Flag blockers immediately

#### Critical Rules

- ❌ NEVER skip validation steps
- ❌ NEVER proceed if validation fails
- ❌ NEVER accumulate multiple failures before fixing
- ✅ ALWAYS fix issues immediately
- ✅ ALWAYS document deviations from plan
- ✅ ALWAYS verify baseline before starting

#### Output

- ✅ Working implementation
- ✅ All tests passing
- ✅ Deviation notes (if any)
- ✅ Ready for Phase 3 (Validate)

---

## Phase 3: VALIDATE (Quality Gates)

**Command:** `/validate` or `.claude/commands/validation/validate.md`

**Purpose:** Comprehensive quality assurance through multi-stage validation before commit/merge.

### Validation Stages

#### Default Validation (4 Stages)

**Stage 1: Static Analysis (< 5 seconds)**
```bash
# Linting
ruff check app/ tests/

# Type checking
mypy app/
```
**Pass criteria:** 0 errors

---

**Stage 2: Unit Tests (< 30 seconds)**
```bash
uv run pytest tests/unit/ -v
```
**Pass criteria:** 100% unit tests passing

---

**Stage 3: Fast Integration Tests (< 2 minutes)**
```bash
uv run pytest tests/integration/ -m "not very_slow" -v
```
**Pass criteria:** All fast integration tests passing

---

**Stage 4: Coverage Analysis**
```bash
uv run pytest tests/unit/ tests/integration/ \
  --cov=app --cov=src \
  --cov-report=term-missing \
  --cov-fail-under=80
```
**Pass criteria:** 80%+ coverage, no regressions

---

#### Full Validation (6 Stages) - Use `--full` flag

**Stage 5: E2E Tests**
```bash
uv run pytest tests/e2e/ -v
```
**Pass criteria:** All end-to-end tests passing

---

**Stage 6: Security Checks (Optional)**
```bash
bandit -r app/ -ll
```
**Pass criteria:** No high/medium security issues

---

### Validation Output

```markdown
# Validation Report

## Stage 1: Static Analysis ✓
- Linting: ✓ (0 errors)
- Type checking: ✓ (0 errors)

## Stage 2: Unit Tests ✓
- Tests run: 259
- Passed: 259
- Failed: 0
- Duration: 12.3s

## Stage 3: Integration Tests ✓
- Tests run: 74
- Passed: 74
- Failed: 0
- Duration: 89.2s

## Stage 4: Coverage ✓
- Coverage: 87.2%
- Threshold: 80.0%
- Missing coverage: 5 files

## Overall Status: ✓ PASSED

All validation gates passed. Ready to commit.
```

### When to Validate

- ✅ After implementing each feature
- ✅ Before creating commits
- ✅ Before creating pull requests
- ✅ Before merging to dev/main
- ✅ After fixing bugs

---

## Supporting Workflows

### Code Review

**Command:** `/code-review` or `.claude/commands/validation/code-review.md`

**Purpose:** AI-driven code review before committing

**Five Evaluation Dimensions:**
1. **Logic** - Correctness, edge cases, error handling
2. **Security** - Vulnerabilities, secrets exposure
3. **Performance** - Efficiency, scalability
4. **Quality** - DRY, complexity, naming
5. **Standards** - CLAUDE.md adherence

**Output:** `.agents/code-reviews/{feature-name}-review.md`

---

### Execution Report

**Command:** `/execution-report {plan-file}` or `.claude/commands/validation/execution-report.md`

**Purpose:** Post-implementation feedback loop to improve future planning

**Report includes:**
- Metadata (plan, date, duration)
- Changes (files, lines)
- Validation results
- Successes (what went well)
- Difficulties (obstacles)
- Deviations (what changed)
- Recommendations (improvements)

**Output:** `.agents/execution-reports/{feature-name}-report.md`

**Why this matters:** Plans get better over time through feedback

---

### Root Cause Analysis (RCA)

**Command:** `/rca {issue-number}` or `.claude/commands/bug_fix/rca.md`

**Purpose:** Systematic bug investigation before fixing

**Six-Phase Process:**
1. Information Gathering
2. Code Investigation
3. Historical Analysis
4. Root Cause Determination
5. Impact Evaluation
6. Solution Design

**Output:** `.agents/rca/issue-{number}.md`

---

### Semantic Commits

**Command:** `/commit` or `.claude/commands/git/commit.md`

**Purpose:** Create semantic commits with proper formatting

**Format:**
```
<type>(<scope>): <subject>

<body>

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
```

**Types:** feat, fix, refactor, test, docs, chore

---

## Feedback Loops

The PIV Loop creates continuous improvement through feedback mechanisms:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│  Implementation                                     │
│       ↓                                            │
│  Execution Report                                  │
│       ↓                                            │
│  Identify:                                         │
│  - What worked well (patterns to reuse)           │
│  - What was difficult (planning gaps)             │
│  - What changed (unexpected complexities)         │
│       ↓                                            │
│  Improve Future Plans:                             │
│  - Add missing context                            │
│  - Document new gotchas                           │
│  - Update reference docs                          │
│  - Refine task breakdowns                         │
│       ↓                                            │
│  Better Next Implementation                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Institutional Knowledge

All PIV artifacts are preserved in `.agents/`:

- **Plans** - Feature implementation blueprints
- **Execution Reports** - Implementation feedback
- **Code Reviews** - Quality assessments
- **RCA Documents** - Bug analysis
- **Init Context** - Codebase snapshots

These artifacts create institutional knowledge that:
- ✅ Informs future implementations
- ✅ Prevents repeat mistakes
- ✅ Accelerates onboarding
- ✅ Documents architectural decisions
- ✅ Tracks system evolution

---

## Best Practices

### Do's ✅

- ✅ **Always Prime before planning** - Context is king
- ✅ **Include specific line numbers** - Make references precise
- ✅ **Document gotchas explicitly** - Prevent predictable errors
- ✅ **Validate after each task** - Catch issues early
- ✅ **Fix before proceeding** - Never accumulate debt
- ✅ **Track deviations** - Learn from changes
- ✅ **Generate execution reports** - Close feedback loop
- ✅ **Update reference docs** - Share patterns with team

### Don'ts ❌

- ❌ **Don't skip Prime phase** - Assumptions lead to errors
- ❌ **Don't use pseudocode in plans** - Provide complete code
- ❌ **Don't batch validations** - Validate incrementally
- ❌ **Don't ignore test failures** - Fix immediately
- ❌ **Don't skip execution reports** - Miss learning opportunities
- ❌ **Don't work without context** - Always establish baseline

---

## Success Metrics

### Planning Quality
- **Confidence score:** Target 8+/10 for one-pass success
- **Context completeness:** All necessary files referenced
- **Pattern reuse:** Existing code examples included
- **Gotcha documentation:** Non-obvious pitfalls flagged

### Implementation Quality
- **First-pass success rate:** % of tasks completed without revision
- **Deviation rate:** % of tasks that differed from plan
- **Validation pass rate:** % of tasks passing incremental validation
- **Time to completion:** Actual vs estimated duration

### Overall Quality
- **Test coverage:** Maintain 80%+ threshold
- **Code review issues:** Target < 5 per feature
- **Bug recurrence rate:** % of bugs that reappear
- **Team velocity:** Features completed per sprint

---

## CI/CD Integration

### PR to Dev Branch
```bash
/validate  # Stages 1-4 (fast validation)
```

### Merge to Main Branch
```bash
/validate --full  # All 6 stages including e2e
```

### Release Process
```bash
/validate --full  # Full validation
/execution-report {plan-file}  # Generate feedback
# Update CHANGELOG.md with changes
# Tag release
```

---

## Reference Documentation

Supporting best practices available in `.claude/reference/`:

- `fastapi-best-practices.md` - FastAPI patterns
- `pydantic-best-practices.md` - Pydantic v2 standards
- `pytest-best-practices.md` - Testing patterns
- `aws-lambda-best-practices.md` - Serverless patterns
- `security-best-practices.md` - Security standards
- `uv-package-manager.md` - UV usage patterns
- `git-workflow.md` - Git best practices
- `rg-search-patterns.md` - ripgrep usage

---

## Getting Started

### First Time Setup

1. **Prime the codebase:**
   ```
   /prime
   ```

2. **Review the context report:**
   ```
   Read .agents/init-context/{project-name}-context-{date}.md
   ```

3. **Plan your first feature:**
   ```
   /plan-feature {feature-name}
   ```

4. **Review and approve the plan:**
   ```
   Read .agents/plans/{feature-name}.md
   ```

5. **Implement the feature:**
   ```
   /implement-plan .agents/plans/{feature-name}.md
   ```

6. **Validate the implementation:**
   ```
   /validate
   ```

7. **Generate feedback:**
   ```
   /execution-report .agents/plans/{feature-name}.md
   ```

8. **Commit your changes:**
   ```
   /commit
   ```

### Daily Workflow

```bash
# Morning: Establish context
/prime

# Planning: Create feature plan
/plan-feature {feature-name}

# Development: Implement with validation
/implement-plan .agents/plans/{feature-name}.md

# Quality: Validate before commit
/validate

# Commit: Semantic commit
/commit

# Feedback: Generate report
/execution-report .agents/plans/{feature-name}.md
```

---

## Troubleshooting

### "Plan confidence score < 8"
**Solution:** More research needed
- Search codebase for similar patterns
- Review `.claude/reference/` docs
- Gather more external examples
- Break down complex tasks further

### "Validation failing repeatedly"
**Solution:** Review plan assumptions
- Check if patterns are outdated
- Verify dependencies are correct
- Review gotchas section for missed items
- Update plan and restart implementation

### "Implementation deviating significantly from plan"
**Solution:** Document and learn
- Track all deviations in execution report
- Update plan with new discoveries
- Add missing gotchas to reference docs
- Consider re-planning if > 50% deviation

### "Tests passing locally but failing in CI"
**Solution:** Environment differences
- Check environment variables
- Verify dependencies versions
- Review CI logs for clues
- Test with `/validate --full`

---

## Continuous Improvement

The PIV Loop is self-improving:

1. **Execution reports identify gaps** in planning
2. **Reference docs capture patterns** for reuse
3. **RCA documents prevent bugs** from recurring
4. **Code reviews maintain quality** standards
5. **Context reports accelerate** onboarding

**Result:** Each iteration improves the next.

---

## Summary

The PIV Loop methodology provides:

✅ **Systematic approach** - Clear phases with defined outputs
✅ **Quality gates** - Multi-stage validation before merge
✅ **Feedback loops** - Continuous improvement through reports
✅ **Institutional knowledge** - Preserved artifacts and patterns
✅ **One-pass success** - Comprehensive planning for fewer iterations
✅ **Team alignment** - Shared understanding through documentation

**Philosophy:** "Context is King" - Understand before acting, validate before proceeding, learn from every implementation.
