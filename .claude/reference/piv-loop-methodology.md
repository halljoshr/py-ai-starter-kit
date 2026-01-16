# PIV Loop Methodology

The **Prime → Implement → Validate** (PIV) methodology is a three-phase iterative development cycle emphasizing context-first development, phase-gated execution, and continuous feedback.

---

## Overview

```
PRIME (Context) → IMPLEMENT (Execution) → VALIDATE (Quality) → Feedback Loop
```

**Philosophy:** "Context is King" - Understand before acting, validate before proceeding, learn from every implementation.

---

## Phase 1: PRIME (Context Establishment)

**Command:** `/prime` or reference `.claude/commands/core_piv_loop/prime.md`

**Purpose:** Establish comprehensive codebase understanding BEFORE planning or implementation.

### When to Use

- Start of new conversation
- Before planning major features
- After significant refactors
- When onboarding new team members

### Process

1. **Analyze project structure** - Use git ls-files, directory hierarchy
2. **Read core documentation** - CLAUDE.md, README.md, architecture docs
3. **Identify key files** - Entry points, models, services, tests
4. **Understand current state** - git status, recent commits, branch state
5. **Map architecture** - Patterns, data flow, integrations, dependencies

### Output

Context report saved to `.agents/init-context/{project-name}-context-{date}.md`

### Benefits

- ✅ Prevents assumptions and reduces errors
- ✅ Speeds up planning with gathered context
- ✅ Onboards conversations with full understanding
- ✅ Creates reusable codebase snapshot

---

## Phase 2: IMPLEMENT (Execution with Validation)

### Step 2.1: Planning

**Command:** `/plan-feature {feature-name}` or reference `.claude/commands/core_piv_loop/plan-feature.md`

**Purpose:** Create comprehensive feature plans with ALL context for one-pass implementation success.

#### Five-Phase Planning Process

1. **Feature Understanding**
   - Problem statement
   - User value and impact
   - Complexity assessment
   - Success criteria

2. **Codebase Intelligence**
   - Search for similar patterns
   - Identify reference files
   - Find relevant tests
   - Map dependencies

3. **External Research**
   - Library documentation
   - Code examples
   - Best practices
   - **Include URLs** for future reference

4. **Strategic Thinking**
   - Architecture fit
   - Dependencies and risks
   - Edge cases and error handling
   - Security considerations
   - Performance implications

5. **Plan Generation**
   - Structured markdown format
   - Complete code examples
   - Step-by-step implementation
   - Validation checkpoints

#### Plan Structure

```markdown
# Feature: {name}

## Feature Understanding
- Problem statement
- User value
- Complexity: Low/Medium/High

## Context References
| File | Lines | Purpose |
|------|-------|---------|
| app/services/foo.py | 42-89 | Similar pattern for reference |

## Patterns to Follow
[Extracted code examples from YOUR codebase]

## Implementation Tasks

### Task 1: {Description}
**IMPLEMENT:**
- Step-by-step instructions
- File paths and line numbers

**PATTERN:**
[Code example showing the pattern]

**IMPORTS:**
```python
from app.models import Foo
```

**GOTCHA:**
- Watch out for X
- Remember to Y

**VALIDATE:**
- Run: uv run pytest tests/unit/test_foo.py
- Expect: All tests pass

## Testing Strategy
- Unit tests for business logic
- Integration tests for API interactions
- E2E tests for workflows

## Acceptance Criteria
- [ ] Feature works as described
- [ ] Tests pass
- [ ] Coverage > 80%
- [ ] Documentation updated

## Confidence Score: 8/10
Reasoning: Pattern exists in codebase, well-understood domain
```

#### Output

Plan saved to `.agents/plans/{feature-name}.md`

---

### Step 2.2: Implementation

**Command:** `/implement-plan {plan-file}` or reference `.claude/commands/core_piv_loop/implement-plan.md`

**Purpose:** Execute plan systematically with validation at EVERY step.

#### Process

1. **Preparation**
   - Read entire plan
   - Verify baseline (tests pass, no existing errors)
   - Set up todo list tracking

2. **Sequential Execution**
   - Implement each task in order
   - Follow patterns exactly as documented
   - Use todo list to track progress

3. **Incremental Validation** ⚠️ CRITICAL
   - After EACH task, run validation
   - Verify tests pass
   - Check for regressions
   - Fix issues immediately

4. **Deviation Tracking**
   - Document changes from plan
   - Record reasons for deviations
   - Update plan if needed

5. **Issue Resolution Loop**
   - Fix immediately, don't accumulate debt
   - Update todo list with blockers
   - Create new tasks if needed

6. **Progress Updates**
   - Mark tasks complete as you finish
   - Keep user informed of progress
   - Flag any blockers early

#### Critical Rules

- ❌ **NEVER skip validation when it fails**
- ❌ **NEVER proceed to next task with failures**
- ❌ **NEVER accumulate technical debt**
- ✅ **ALWAYS fix issues immediately**
- ✅ **ALWAYS document deviations**
- ✅ **ALWAYS run validation after each task**

#### Output

- Working implementation
- Deviation notes (if any)
- Updated todo list
- All tests passing

---

## Phase 3: VALIDATE (Quality Gates)

**Command:** `/validate` or reference `.claude/commands/validation/validate.md`

**Purpose:** Comprehensive quality assurance before commit/merge.

### Default Validation (4 Stages)

#### Stage 1: Static Analysis (< 5s)
```bash
ruff check app/ tests/
mypy app/
```

**Pass Criteria:**
- No linting errors
- No type errors
- Code follows style guide

#### Stage 2: Unit Tests (< 30s)
```bash
uv run pytest tests/unit/ -v
```

**Pass Criteria:**
- All unit tests pass
- Business logic validated in isolation

#### Stage 3: Fast Integration Tests (< 2min)
```bash
uv run pytest tests/integration/ -m "not very_slow" -v
```

**Pass Criteria:**
- Service interactions work
- API integrations validated
- No test failures

#### Stage 4: Coverage Analysis
```bash
uv run pytest tests/unit/ tests/integration/ --cov=app --cov=src --cov-fail-under=80
```

**Pass Criteria:**
- Coverage ≥ 80%
- Critical paths covered
- No untested business logic

### Full Validation (`--full` flag)

#### Stage 5: E2E Tests
```bash
uv run pytest tests/e2e/ -v
```

**Pass Criteria:**
- Complete workflows validated
- Production-like scenarios pass

#### Stage 6: Security Checks
```bash
# Dependency vulnerabilities
uv run pip-audit

# Secret detection
rg -i "api[_-]?key|secret|password" --type py
```

**Pass Criteria:**
- No known vulnerabilities
- No hardcoded secrets
- Input validation in place

### Validation Output

**On Success:**
```
✅ Stage 1: Static Analysis - PASSED
✅ Stage 2: Unit Tests - PASSED (24 tests, 0.8s)
✅ Stage 3: Integration Tests - PASSED (12 tests, 45s)
✅ Stage 4: Coverage - PASSED (87% coverage)

🎉 All validation stages passed! Ready to commit.
```

**On Failure:**
```
✅ Stage 1: Static Analysis - PASSED
❌ Stage 2: Unit Tests - FAILED (2 tests failed)

Validation failed at Stage 2. Fix issues before proceeding.

Failed tests:
- tests/unit/test_foo.py::test_bar - AssertionError
- tests/unit/test_foo.py::test_baz - ValueError
```

---

## Supporting Workflows

### Code Review

**Command:** `/code-review`

**Purpose:** AI-driven review before creating PR

**Evaluation Areas:**
- **Logic**: Correctness, edge cases, error handling
- **Security**: Input validation, secrets, SQL injection
- **Performance**: Efficiency, caching, database queries
- **Quality**: Readability, maintainability, documentation
- **Standards**: Style guide, naming conventions, patterns

**Output:** `.agents/code-reviews/{feature-name}-review-{date}.md`

---

### Execution Report

**Command:** `/execution-report {plan-file}`

**Purpose:** Post-implementation feedback to improve future planning

**Analysis:**
- What went well
- What could be improved
- Deviations from plan
- Lessons learned
- Plan quality score

**Output:** `.agents/execution-reports/{feature-name}-report-{date}.md`

**Benefits:**
- Improves future plan quality
- Identifies patterns in deviations
- Creates institutional knowledge
- Accelerates team learning

---

### Root Cause Analysis

**Command:** `/rca {issue-number}`

**Purpose:** Systematic bug investigation before fixing

**Process:**
1. Reproduce the issue
2. Analyze symptoms
3. Trace root cause
4. Identify contributing factors
5. Propose fix strategy

**Output:** `.agents/rca/issue-{number}-rca-{date}.md`

---

### Semantic Commits

**Command:** `/commit`

**Purpose:** Create properly formatted commits with Co-Authored-By tags

**Process:**
1. Review changes (git status, git diff)
2. Analyze commit message style from git log
3. Draft commit message following conventions
4. Add Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
5. Execute commit

---

## Agent Commands Reference

### Core PIV Loop
- `/prime` - Establish codebase context
- `/plan-feature {name}` - Create comprehensive feature plan
- `/implement-plan {plan-file}` - Execute plan with validation

### Quality Assurance
- `/validate` - Multi-stage quality gates (default: stages 1-4)
- `/validate --full` - Include e2e and security checks
- `/code-review` - AI-driven code review
- `/execution-report {plan-file}` - Post-implementation analysis

### Bug Workflow
- `/rca {issue-number}` - Root cause analysis
- `/implement-fix {rca-file}` - Fix bug systematically

### Git Workflow
- `/commit` - Semantic commit workflow

---

## Feedback Loops and Institutional Knowledge

All PIV artifacts are preserved in `.agents/`:

- **Plans** (`.agents/plans/`) - Feature implementation blueprints
- **Execution Reports** (`.agents/execution-reports/`) - Implementation feedback
- **Code Reviews** (`.agents/code-reviews/`) - Quality assessments
- **RCA Documents** (`.agents/rca/`) - Bug analysis
- **Init Context** (`.agents/init-context/`) - Codebase snapshots
- **Decisions** (`.agents/decisions/`) - Architectural decisions

### Benefits of Institutional Knowledge

- ✅ Informs future implementations
- ✅ Prevents repeat mistakes
- ✅ Accelerates onboarding
- ✅ Documents architectural decisions
- ✅ Tracks system evolution
- ✅ Improves plan quality over time
- ✅ Identifies patterns in issues

---

## Daily PIV Workflow

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

## Success Metrics

- **Plan Confidence Score:** Target 8+/10
- **First-Time Validation Pass:** 80%+ of tasks
- **Test Coverage:** Maintain 80%+
- **Deviation Rate:** < 20% of planned tasks
- **Bug Recurrence:** < 5% of fixed bugs

---

## Best Practices

### Planning

1. **Always prime first** - Don't plan without context
2. **Research thoroughly** - Include external docs and URLs
3. **Extract patterns** - Use examples from your codebase
4. **Think strategically** - Consider architecture, security, performance
5. **Be specific** - Complete code examples, not pseudocode

### Implementation

1. **Read entire plan** - Understand the full scope before starting
2. **Validate incrementally** - After every task, not just at the end
3. **Fix immediately** - Don't accumulate technical debt
4. **Document deviations** - Record why you diverged from plan
5. **Communicate progress** - Keep user informed with todo updates

### Validation

1. **Never skip stages** - Run all validation stages
2. **Fix before proceeding** - Don't commit with failures
3. **Check coverage** - Ensure new code is tested
4. **Review security** - Validate input, check for secrets
5. **Test edge cases** - Don't just test happy path

---

## Common Pitfalls

### ❌ Skipping Prime
**Problem:** Implementing without understanding context
**Impact:** Wrong patterns, missed dependencies, rework
**Solution:** Always `/prime` at start of conversation

### ❌ Incomplete Planning
**Problem:** Plans missing context, patterns, or edge cases
**Impact:** Low confidence score, implementation struggles
**Solution:** Follow 5-phase planning process thoroughly

### ❌ Skipping Validation
**Problem:** Proceeding to next task with test failures
**Impact:** Accumulated technical debt, hard-to-debug issues
**Solution:** Run validation after EVERY task

### ❌ Ignoring Deviations
**Problem:** Not documenting why you diverged from plan
**Impact:** Lost lessons, repeat mistakes, poor feedback loop
**Solution:** Track all deviations with reasons

### ❌ No Execution Reports
**Problem:** Not generating post-implementation feedback
**Impact:** Plan quality doesn't improve, repeat issues
**Solution:** Always run `/execution-report` after implementation

---

## Advanced Usage

### Multi-Feature Projects

For large projects with multiple related features:

1. **Prime once** - Establish context for entire project
2. **Plan all features** - Create plans for each feature
3. **Implement sequentially** - One feature at a time with validation
4. **Generate reports** - After each feature completion

### Refactoring Workflow

For large refactoring tasks:

1. **Prime** - Understand current architecture
2. **Plan refactor** - Document current state, target state, migration path
3. **Implement incrementally** - Small changes with validation
4. **Validate frequently** - Ensure no regressions
5. **Document decisions** - Save architectural decisions to `.agents/decisions/`

### Bug Fix Workflow

For systematic bug fixing:

1. **/rca {issue-number}** - Investigate root cause
2. **/plan-feature bug-fix-{number}** - Plan the fix
3. **/implement-plan** - Execute fix with validation
4. **/validate** - Comprehensive testing
5. **/execution-report** - Document lessons learned

---

## See Also

- [.claude/PIV-LOOP.md](.claude/PIV-LOOP.md) - Original detailed PIV Loop documentation
- [.agents/PIV-LOOP-QUICKSTART.md](.agents/PIV-LOOP-QUICKSTART.md) - Quick start guide with examples
- [.claude/commands/core_piv_loop/](.claude/commands/core_piv_loop/) - Command implementations
- [habit-tracker-example.md](./habit-tracker-example.md) - Example CLAUDE.md structure
