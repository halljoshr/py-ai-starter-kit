# Goals: Building the Best Agentic Coding Experience

This document outlines the strategic goals for py-ai-starter-kit, organized by priority and with clear success criteria.

---

## Core Philosophy

**"Context is King, Sessions are Natural, Quality is Non-Negotiable"**

- Spend tokens wisely on context that matters
- Design for multi-session development from the start
- Never compromise quality for speed
- Learn from every implementation to improve the next
- Keep it simple until complexity proves its value (YAGNI + KISS)

---

## Priority 1: Foundation (Do This Month)

### 1. Spec Creation Process

**Status:** Research complete (2026-01-23), implementation pending

**What it is:**
- Systematic process to go from requirements document to implementation specification
- Follows Anthropic's XML-based spec format with session management built in
- Three workflow options: Full spec (2 days), Lightweight spec (4-5 hours), Iterative (not recommended)

**Research artifacts created:**
- ✅ [.agents/research/SPEC-CREATION-PROCESS.md](.agents/research/SPEC-CREATION-PROCESS.md) - Complete process documentation
- ✅ [.agents/specs/tax_analysis_spec.txt](.agents/specs/tax_analysis_spec.txt) - Example specification in proper format (from uw-portal-api project)
- ✅ [.agents/research/ANTHROPIC-HARNESS-COMPARISON.md](.agents/research/ANTHROPIC-HARNESS-COMPARISON.md) - Comparison of approaches

**Success criteria:**
- [x] Documented process from requirements → spec
- [x] Created example spec in Anthropic XML format
- [ ] **Built `/create-spec` command** - Interactive spec creation tool
- [ ] **Created spec templates** - API integration, data processing, UI components, refactoring
- [ ] **Integrated with `/plan-feature`** - Make planning consume specs as input
- [ ] **Validated on py-ai-starter-kit features** - Use for 2-3 real features in THIS project

**What's missing:**
1. **Tooling** - No `/create-spec` command to guide users through creation
2. **Templates** - No reusable templates for common patterns
3. **Integration** - `/plan-feature` doesn't load from or reference specs
4. **Validation** - Spec created for different project (uw-portal-api), not tested here
5. **Workflow bridge** - Missing spec → plan connection

**Next steps:**
- **Phase 1 (Week 1-2):** Build `/create-spec` command and spec validation
- **Phase 2 (Week 2-3):** Create spec templates library (4-5 common patterns)
- **Phase 3 (Week 3-4):** Integrate with `/plan-feature` workflow
- **Phase 4 (Month 2):** Use on 2-3 features in py-ai-starter-kit to validate

---

### 2. Session Management System

**Status:** Not started

**What it is:**
- Live progress tracking that survives conversation boundaries
- Automatic checkpointing at token thresholds
- Session startup rituals that establish context efficiently
- Health metrics visible during work

**Components:**

#### 2.1 Progress File System
```
.agents/progress/
├── current-session.txt          # Live progress, updated during work
├── feature-name-history.txt     # Complete session history for feature
└── session-metrics.json         # Token usage, tasks completed, time spent
```

**Format for current-session.txt:**
```
Feature: [Feature Name] ([Linear Ticket])
Plan: .agents/plans/[plan-file].md
Started: [Timestamp]
Current Session: [N]

COMPLETED:
✓ Phase 1, Task 1.1: [Task description] (Session 1, 18K tokens)
✓ Phase 1, Task 1.2: [Task description] (Session 1, 24K tokens)
✓ Phase 2, Task 2.1: [Task description] (Session 2, 22K tokens)

IN PROGRESS:
→ Phase 2, Task 2.3: [Task description] (45% complete)
  - Subtask 1: Done
  - Subtask 2: In progress
  - Subtask 3: Not started

REMAINING:
- Phase 2, Task 2.4: [Task description]
- Phase 3: Testing & Validation (4 tasks)
- Phase 4: Documentation (2 tasks)

SESSION METRICS:
Token usage: ~67K / 200K (34%)
Files modified: 8
Tests added: 12
Tests passing: 12/12
Last validation: All checks passed
Last commit: abc1234 "Implement Phase 2 Task 2.2"

BLOCKERS:
None

NOTES:
- API endpoint changed from /v1/tax to /v2/tax-analysis
- Added extra validation per code review feedback
```

#### 2.2 Session Startup Ritual

Add to all implementation commands:

**Session Startup Ritual (ALWAYS RUN FIRST)**

Before any implementation work:

1. **Verify location**
   ```bash
   pwd
   ls -la
   ```

2. **Read progress** (if exists)
   ```bash
   cat .agents/progress/current-session.txt
   ```

3. **Check git state**
   ```bash
   git status
   git log -5 --oneline
   git diff --stat
   ```

4. **Run baseline tests**
   ```bash
   uv run pytest tests/unit/ -v --tb=short
   ```

5. **Verify nothing broken before proceeding**
   - All tests must pass
   - No unexpected modified files
   - Branch is correct

6. **Load relevant context**
   - Read plan file for current phase
   - Read any blockers from previous session
   - Understand what's completed vs remaining

Never start coding without completing startup ritual.

#### 2.3 Automatic Checkpointing

Add to `/implement-plan` command:

**Token Budget Monitoring**

Track token usage throughout implementation:

- At 25% (50K tokens): Log: "Token budget: 50K used (25%), proceeding"
- At 50% (100K tokens): Log: "Token budget: 100K used (50%), halfway through budget"
- At 75% (150K tokens): WARNING: "Token budget: 150K used (75%) - Consider checkpointing soon" → Suggest: "Natural breakpoint: Complete current task, then checkpoint"
- At 88% (175K tokens): CRITICAL: "Token budget: 175K used (88%) - CHECKPOINT NOW" → Action: Automatic checkpoint procedure

**Checkpoint Procedure**

When reaching 75%+ token usage OR completing a major phase:

1. **Update progress file**
   - Mark completed tasks
   - Document current state (% complete for in-progress task)
   - Note any blockers or decisions made

2. **Run validation**
   ```bash
   uv run pytest tests/unit/ -v
   uv run ruff check .
   uv run mypy app/
   ```

3. **Commit work**
   ```bash
   git add [files]
   git commit -m "WIP: [Phase X.Y] - [What was completed]

   - Completed: [list tasks done]
   - In progress: [what's partially done]
   - Remaining: [what's left]

   Token checkpoint at [X]K tokens."
   ```

4. **Display resume instructions**
   ```
   ═══════════════════════════════════════════════════
   SESSION CHECKPOINT
   ═══════════════════════════════════════════════════

   Completed: [Phase X, Tasks Y-Z]
   Token usage: [N]K
   Tests: All passing

   TO RESUME (New conversation):
   1. cd [project-path]
   2. cat .agents/progress/current-session.txt
   3. git log -1
   4. Continue with: [Next task]

   ═══════════════════════════════════════════════════
   ```

5. **End session gracefully**
   - Do NOT start new major tasks
   - Return control to user

**Success criteria:**
- [ ] Progress files update automatically during implementation
- [ ] Session startup ritual runs at beginning of every session
- [ ] Token warnings display at 25%, 50%, 75%, 88%
- [ ] Automatic checkpoint at 88% tokens or phase completion
- [ ] Session metrics tracked and viewable
- [ ] Resume instructions display after checkpoint

**Timeline:** Week 1-2

---

### 3. Multi-Session Architecture by Default

**Status:** Not started

**What it is:**
- Workflow assumes multiple sessions from the start, not as fallback
- Plans broken into session-sized phases (target: 20-40K tokens per session)
- Natural breakpoints between phases
- Fresh context each session via file-based state

**Changes needed:**

#### 3.1 Update `/prime` Command

Add `--quick` mode as default for known codebases:

**Quick Prime (Default for known codebases)**

Usage: `/prime --quick`

Target: ~8K tokens
When: You've worked on this codebase in last 30 days

Process:
1. Read project structure (git ls-files | head -50)
2. Read current git state (branch, status, last 5 commits)
3. List recent plans (last 3 only)
4. Generate minimal context summary
5. Skip full documentation reads

**Full Prime (For new/unfamiliar codebases)**

Usage: `/prime --full`

Target: ~45K tokens
When: First time on codebase or major changes since last work

Process:
1. Complete project structure analysis
2. Full documentation reads (CLAUDE.md, README.md, etc.)
3. List all plans with summaries
4. Generate comprehensive context report
5. Save to .agents/init-context/

#### 3.2 Update `/plan-feature` Command

Add session-aware planning:

**Session-Aware Planning**

When creating plans, automatically break into session-sized chunks:

**Target per session:** 20-40K tokens
**Warning threshold:** 50K tokens
**Critical threshold:** 75K tokens

**Token estimation formula:**
- Reading 1 file: ~500 tokens (average)
- Writing 1 new file: ~1,000 tokens
- Modifying 1 file: ~800 tokens
- Running tests: ~500 tokens
- Debugging/iteration: +50% to estimates

**Phase sizing guidelines:**
- Phase with 3-5 tasks: Usually fits 1 session
- Phase with 6-10 tasks: Split across 2 sessions
- Phase with 10+ tasks: Break into sub-phases

**Output format:**
```
PHASE 1: Data Models (Session 1 target)
Estimated tokens: 35K
Tasks: 1.1, 1.2, 1.3
Natural breakpoint after this phase

PHASE 2: Service Layer (Sessions 2-3)
Estimated tokens: 65K (split into 2 sessions)
  Session 2: Tasks 2.1-2.3 (30K tokens)
  Session 3: Tasks 2.4-2.6 (35K tokens)
Natural breakpoint after Task 2.3
```

#### 3.3 Update `/implement-plan` Command

Add session selection:

**Single Phase (Recommended)**

Usage: `/implement-plan --phase 1`

Implements only Phase 1, then checkpoints.

**Multiple Phases (Use with caution)**

Usage: `/implement-plan --phases 1,2`

Only if phases are small (<30K tokens combined).

**Resume from Checkpoint**

Usage: `/implement-plan --resume`

Reads progress file, continues from last incomplete task.

**Success criteria:**
- [ ] `/prime --quick` is default, uses ~8K tokens
- [ ] `/plan-feature` estimates tokens per phase
- [ ] Plans automatically suggest session breaks
- [ ] `/implement-plan` defaults to single phase
- [ ] `--resume` flag reads progress and continues

**Timeline:** Week 2-3

---

### 4. Token Budget Management System

**Status:** Not started

**What it is:**
- Pre-flight estimation before starting work
- Real-time tracking during implementation
- Historical analysis for accuracy improvement
- Cost visibility (tokens → dollars)

**Components:**

#### 4.1 Pre-Flight Estimation

Add to `/plan-feature`:

After plan creation, display:

```
═══════════════════════════════════════════════════
TOKEN BUDGET ANALYSIS
═══════════════════════════════════════════════════

PLAN OVERVIEW:
  Total phases: 5
  Total tasks: 23
  Estimated tokens: ~142,000 tokens
  Estimated cost: ~$0.43 (using Sonnet 4)

SESSION BREAKDOWN:
  Session 1 (Phase 1): ~28K tokens → $0.08
  Session 2 (Phase 2): ~35K tokens → $0.11
  Session 3 (Phase 3): ~42K tokens → $0.13
  Session 4 (Phase 4): ~25K tokens → $0.08
  Session 5 (Phase 5): ~12K tokens → $0.04

RECOMMENDATIONS:
  ✓ Plan is well-sized for 5 sessions
  ✓ No session exceeds 50K token warning threshold
  ⚠ Phase 3 is close to 50K - consider splitting

═══════════════════════════════════════════════════
```

#### 4.2 Real-Time Tracking

Display during implementation:

```
[12:45:30] Token Budget: 23.5K / 200K (12%) ████░░░░░░░░░░░░░░░░
[12:47:15] Token Budget: 31.2K / 200K (16%) █████░░░░░░░░░░░░░░░
[12:52:40] Token Budget: 47.8K / 200K (24%) █████████░░░░░░░░░░░
```

#### 4.3 Historical Analysis

Track in `.agents/analytics/token-history.json`:

```json
{
  "features": [
    {
      "feature_id": "tax-analysis-agent",
      "estimated_tokens": 142000,
      "actual_tokens": 156000,
      "accuracy": "90%",
      "variance_reason": "Additional debugging in Phase 3",
      "sessions": 5,
      "total_cost": 0.47
    }
  ],
  "accuracy_trend": {
    "last_5_features": "88%",
    "last_10_features": "85%",
    "improving": true
  }
}
```

**Success criteria:**
- [ ] Pre-flight estimation shows tokens per session
- [ ] Real-time tracking visible during work
- [ ] Historical data tracks estimated vs actual
- [ ] Cost calculation included (tokens → dollars)
- [ ] Accuracy improves over time (feedback loop)

**Timeline:** Week 3-4

---

## Priority 2: Core Skills & Workflows (Do This Quarter)

### 5. Comprehensive Skills Tree

**Status:** Partially complete

**What it is:**
- Atomic skills that do one thing well
- Compound skills that chain atomic skills
- Custom workflows users can define
- Conditional logic for smart branching

**Current Skills (Implemented):**
- ✅ `/prime` - Establish codebase context
- ✅ `/plan-feature` - Create feature plan
- ✅ `/implement-plan` - Execute plan
- ✅ `/validate` - Multi-stage quality gates
- ✅ `/code-review` - AI-driven code review
- ✅ `/code-review-since` - Review changes since commit
- ✅ `/commit` - Semantic commit workflow
- ✅ `/rca` - Root cause analysis for bugs
- ✅ `/implement-fix` - Execute fix from RCA

**Planned Atomic Skills:**

#### 5.1 Context Skills
- `/prime --quick` - Minimal context (8K tokens)
- `/prime --full` - Complete context (45K tokens)
- `/context-refresh` - Update context mid-session
- `/context-prune` - Remove irrelevant context

#### 5.2 Planning Skills
- `/plan-feature` - Full feature plan
- `/plan-bugfix` - Focused bug fix plan
- `/plan-refactor` - Refactoring plan
- `/plan-spike` - Research/exploration plan

#### 5.3 Implementation Skills
- `/implement-plan` - Execute full plan
- `/implement-phase` - Execute single phase
- `/implement-task` - Execute single task
- `/quick-fix` - Immediate fix without planning

#### 5.4 Quality Skills
- `/validate` - All quality gates
- `/validate-unit` - Unit tests only
- `/validate-types` - Type checking only
- `/code-review` - Full code review
- `/code-review-since` - Review since commit

#### 5.5 Git Skills
- `/commit` - Interactive commit
- `/checkpoint` - Save progress + commit
- `/create-pr` - Create pull request with summary

#### 5.6 Analysis Skills
- `/rca` - Root cause analysis
- `/security-scan` - Security vulnerability scan
- `/dependency-audit` - Check for outdated/vulnerable deps

#### 5.7 Profiling & Optimization Skills
- `/profile` - Comprehensive performance profiling
- `/profile-memory` - Memory usage analysis
- `/profile-cpu` - CPU hotspot identification
- `/profile-io` - I/O bottleneck detection
- `/optimize` - Apply performance optimizations
- `/optimize-queries` - Database query optimization
- `/optimize-imports` - Python import optimization
- `/benchmark` - Create and run performance benchmarks
- `/compare-performance` - Before/after performance comparison

**Planned Compound Skills:**

**Compound Skills (Chains of atomic skills)**

**/quick-fix** - Fast bug fix workflow for small issues.

Steps:
1. /prime --quick
2. /rca (identify root cause)
3. /implement-fix
4. /validate-unit
5. /commit

Use when: Bug is small, fix is obvious, no architectural changes needed.

**/feature-full** - Complete feature development workflow.

Steps:
1. /prime --full
2. /plan-feature
3. /implement-phase (for each phase)
4. /validate
5. /code-review
6. /commit
7. /create-pr

Use when: New feature, multiple sessions expected, full quality gates needed.

**/refactor-safe** - Safe refactoring workflow with validation.

Steps:
1. /prime --quick
2. /validate (baseline - must pass)
3. /plan-refactor
4. /implement-plan
5. /validate (verify no regression)
6. /code-review
7. /commit

Use when: Code cleanup, no behavior changes, safety critical.

**/investigate** - Research workflow for unfamiliar code.

Steps:
1. /prime --full
2. /plan-spike
3. Document findings in .agents/research/
4. Create recommendations

Use when: Learning new codebase area, evaluating approaches, no implementation yet.

**/optimize-performance** - Systematic performance optimization workflow.

Steps:
1. /prime --quick
2. /benchmark (establish baseline performance)
3. /profile (identify bottlenecks: CPU, memory, I/O, database)
4. /plan-optimization (create targeted optimization plan)
5. /implement-plan (apply optimizations)
6. /benchmark (measure improvements)
7. /compare-performance (verify gains)
8. /validate (ensure no regressions)
9. /commit

Use when: Application is slow, need to improve performance, data-driven optimization required.

**Custom Workflows:**

Allow users to define their own:

```yaml
# .agents/workflows/my-workflow.yaml
name: my-api-endpoint
description: My team's standard API endpoint workflow

steps:
  - skill: /prime
    args: --quick

  - skill: /plan-feature
    args: --template api-endpoint

  - skill: /implement-phase
    args: --phase 1
    checkpoint_after: true

  - skill: /implement-phase
    args: --phase 2
    checkpoint_after: true

  - skill: /validate
    fail_fast: true

  - skill: /code-review
    auto_fix: minor_issues

  - skill: /commit
    args: --interactive false
```

**Success criteria:**
- [ ] All atomic skills documented and working
- [ ] 5+ compound skills defined and tested
- [ ] Custom workflow YAML format defined
- [ ] Workflow execution engine implemented
- [ ] Conditional logic support (if/else branches)

**Timeline:** Month 2

---

### 6. JSON Features Tracking System

**Status:** Not started (inspired by Anthropic's feature_list.json)

**What it is:**
- Single source of truth for all features
- Immutable test steps, mutable status
- Clear pass/fail criteria per feature
- Progress visualization

**File structure:**

```json
{
  "project": "py-ai-starter-kit",
  "version": "1.0.0",
  "features": [
    {
      "id": "feat-001",
      "name": "Session Management System",
      "description": "Live progress tracking, checkpointing, session metrics",
      "status": "in_progress",
      "priority": "high",
      "linear_ticket": "PRO-142",
      "plan_file": ".agents/plans/session-management.md",
      "spec_file": ".agents/specs/session-management.txt",
      "created": "2026-01-23",
      "started": "2026-01-24",
      "completed": null,
      "test_steps": [
        "Create progress file with IN PROGRESS task",
        "Run token budget warning at 75%",
        "Trigger automatic checkpoint at 88%",
        "Verify progress file updates correctly",
        "Resume from checkpoint in new conversation",
        "Verify session metrics JSON is correct"
      ],
      "passes": false,
      "phases": [
        {
          "phase": 1,
          "name": "Progress File System",
          "status": "completed",
          "sessions": 2,
          "tokens_used": 48000
        },
        {
          "phase": 2,
          "name": "Checkpoint Automation",
          "status": "in_progress",
          "sessions": 1,
          "tokens_used": 22000
        },
        {
          "phase": 3,
          "name": "Session Metrics",
          "status": "pending",
          "sessions": 0,
          "tokens_used": 0
        }
      ],
      "blockers": [],
      "notes": "Token budget monitoring working well, checkpoint automation needs testing"
    },
    {
      "id": "feat-002",
      "name": "Multi-Session Architecture",
      "description": "Default to multi-session workflow with phase-based planning",
      "status": "pending",
      "priority": "high",
      "linear_ticket": "PRO-143",
      "plan_file": null,
      "spec_file": null,
      "created": "2026-01-23",
      "started": null,
      "completed": null,
      "test_steps": [
        "Run /prime --quick and verify <10K tokens",
        "Create plan with token estimates per phase",
        "Implement single phase with /implement-plan --phase 1",
        "Checkpoint and verify progress saved",
        "Resume in new conversation with /implement-plan --resume",
        "Complete feature across 3+ sessions without compaction"
      ],
      "passes": false,
      "phases": [],
      "blockers": ["Blocked by feat-001 (Session Management)"],
      "notes": null
    }
  ],
  "summary": {
    "total_features": 2,
    "completed": 0,
    "in_progress": 1,
    "pending": 1,
    "pass_rate": "0%",
    "total_sessions": 3,
    "total_tokens_used": 70000
  }
}
```

**Commands:**

```bash
# View all features
/features list

# View specific feature
/features show feat-001

# Update feature status
/features update feat-001 --status completed --passes true

# Add new feature
/features add "Feature name" --priority high --ticket PRO-144

# Generate progress report
/features report
```

**Success criteria:**
- [ ] JSON schema defined and documented
- [ ] Commands to view/update features
- [ ] Auto-update from implementation sessions
- [ ] Progress reports generated
- [ ] Integrated with /implement-plan workflow

**Timeline:** Month 2

---

### 7. Test-Driven Development (TDD) Culture

**Status:** Partially implemented

**What it is:**
- Write tests first, implementation second
- Red-Green-Refactor cycle enforced
- Test coverage requirements
- Fast feedback loops

**Current state:**
- ✅ `/validate` command runs tests
- ✅ Coverage threshold set (80%)
- ❌ Tests not written BEFORE implementation
- ❌ No enforcement of TDD workflow

**Improvements needed:**

#### 7.1 TDD Workflow Enforcement

Update `/implement-plan` to enforce TDD:

**TDD Workflow (Red-Green-Refactor)**

For each task in the plan:

**Step 1: RED (Write failing test)**
1. Read task requirements
2. Write test(s) that verify the requirements
3. Run test - MUST FAIL (proves test is valid)
4. Commit: "test: Add failing test for [feature]"

**Step 2: GREEN (Make test pass)**
1. Implement minimal code to make test pass
2. Run test - MUST PASS
3. Commit: "feat: Implement [feature] to pass test"

**Step 3: REFACTOR (Improve code)**
1. Improve code quality without changing behavior
2. Run test - MUST STILL PASS
3. Commit: "refactor: Improve [aspect] of [feature]"

**Enforcement:**
- /implement-plan WILL NOT proceed to implementation without test
- Validation runs after each step
- Red-Green-Refactor cycle logged in progress file

#### 7.2 Test Templates

Provide templates for common test patterns:

```python
# .claude/templates/test-templates/

# API endpoint test
def test_api_endpoint_success():
    """Test [endpoint] returns [expected result] when [condition]."""
    # Arrange
    client = TestClient(app)
    payload = {...}

    # Act
    response = client.post("/api/endpoint", json=payload)

    # Assert
    assert response.status_code == 200
    assert response.json()["key"] == expected_value

# Service layer test
def test_service_method_with_mock():
    """Test [service method] calls [dependency] correctly."""
    # Arrange
    mock_dependency = Mock()
    service = Service(dependency=mock_dependency)

    # Act
    result = service.method(input_data)

    # Assert
    mock_dependency.method.assert_called_once_with(expected_args)
    assert result == expected_result

# Data model validation test
def test_model_validation_rejects_invalid():
    """Test [model] raises ValidationError when [invalid condition]."""
    # Arrange
    invalid_data = {...}

    # Act & Assert
    with pytest.raises(ValidationError) as exc_info:
        Model(**invalid_data)
    assert "expected error message" in str(exc_info.value)
```

#### 7.3 Coverage Reporting

Enhance validation to show coverage details:

```bash
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80

# Output enhanced with:
Coverage by module:
  app/models/: 92%
  app/services/: 87%
  app/api/: 78% ⚠️  (below 80% threshold)

Files needing coverage:
  app/api/endpoints.py: 78% (lines 45-52, 67-71 not covered)
```

**Success criteria:**
- [ ] /implement-plan enforces Red-Green-Refactor cycle
- [ ] Test templates available for common patterns
- [ ] Coverage reports show per-module breakdown
- [ ] CI fails if coverage drops below 80%
- [ ] TDD workflow documented in PIV-LOOP.md

**Timeline:** Month 2-3

---

### 8. Standard Development Flow (Container Pattern)

**Status:** Documented in [.agents/research/SPEC-CREATION-PROCESS.md](.agents/research/SPEC-CREATION-PROCESS.md)

**What it is:**
- Clear entry and exit points for every feature
- Consistent flow regardless of feature type
- Checkpoints and quality gates at predictable stages
- Artifacts produced at each stage

**Standard Flow:** See [.agents/research/SPEC-CREATION-PROCESS.md](.agents/research/SPEC-CREATION-PROCESS.md) for complete 7-stage flow:

```
Requirements → Technical Discovery → Spec Creation → Planning →
Implementation → Quality Assurance → Finalization → Feedback Loop
```

**Success criteria:**
- [x] Flow documented with clear entry/exit points
- [x] Commands defined for each stage
- [x] Quality gates specified
- [x] Artifacts list complete
- [ ] Tested on 3+ features (in progress)

**Timeline:** Already documented, refinement ongoing

---

### 9. Profiling & Optimization System

**Status:** Not started

**What it is:**
- Data-driven performance optimization workflow
- Automated profiling tools for Python (cProfile, memory_profiler, py-spy)
- Benchmark framework for before/after comparisons
- Performance regression detection
- Optimization recommendations based on profiling data

**Components:**

#### 9.1 Profiling Tools Integration

**CPU Profiling:**
```python
# /profile or /profile-cpu
# Uses cProfile + snakeviz for visualization

Output:
- Hotspot functions (top 20 by cumulative time)
- Call graphs showing where time is spent
- Recommendations for optimization targets
```

**Memory Profiling:**
```python
# /profile-memory
# Uses memory_profiler + tracemalloc

Output:
- Peak memory usage
- Memory growth over time
- Top memory consumers
- Potential memory leaks
```

**I/O Profiling:**
```python
# /profile-io
# Tracks file operations, network calls, database queries

Output:
- Slow queries (>100ms)
- N+1 query detection
- File I/O bottlenecks
- Network latency issues
```

#### 9.2 Benchmark Framework

Create standardized benchmarks:

```python
# .agents/benchmarks/benchmark_api.py

import pytest
import time
from app.main import app

@pytest.mark.benchmark
def test_api_endpoint_performance(benchmark):
    """Benchmark /api/users endpoint response time."""
    def make_request():
        response = client.get("/api/users")
        assert response.status_code == 200
        return response

    result = benchmark(make_request)
    # Target: <50ms p95 latency
    assert result.stats.get("mean") < 0.050

@pytest.mark.benchmark
def test_database_query_performance(benchmark, db_session):
    """Benchmark complex user query."""
    def run_query():
        return db_session.query(User).join(Profile).filter(...).all()

    result = benchmark(run_query)
    # Target: <100ms for complex query
    assert result.stats.get("mean") < 0.100
```

#### 9.3 Performance Comparison

Track performance over time:

```json
// .agents/analytics/performance-history.json
{
  "benchmarks": [
    {
      "name": "api_endpoint_performance",
      "baseline": {
        "mean": 0.085,
        "p95": 0.120,
        "date": "2026-01-20"
      },
      "current": {
        "mean": 0.042,
        "p95": 0.058,
        "date": "2026-01-23"
      },
      "improvement": "50.6% faster",
      "optimizations_applied": [
        "Added database query caching",
        "Optimized N+1 queries with eager loading",
        "Added connection pooling"
      ]
    }
  ]
}
```

#### 9.4 Optimization Workflow

**Automated optimization detection:**

```markdown
## /optimize Command

Analyzes profiling data and suggests optimizations:

PROFILING SUMMARY:
- CPU: High time in `calculate_tax()` (45% of runtime)
- Memory: 2GB peak, mostly in data loading
- I/O: 15 database queries per request (N+1 pattern detected)

RECOMMENDED OPTIMIZATIONS:
1. **High Impact** - Fix N+1 queries in user profile loading
   - Add eager loading: .options(joinedload(User.profile))
   - Expected improvement: 60% faster

2. **Medium Impact** - Cache `calculate_tax()` results
   - Use @lru_cache for repeated calculations
   - Expected improvement: 30% faster

3. **Low Impact** - Lazy load large datasets
   - Stream data instead of loading all at once
   - Expected improvement: 50% memory reduction

APPLY OPTIMIZATIONS? (y/n)
```

#### 9.5 Performance Regression Detection

Add to CI/CD:

```yaml
# .github/workflows/performance.yml
name: Performance Tests

on: [pull_request]

jobs:
  benchmark:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Run benchmarks
        run: uv run pytest tests/ -m benchmark --benchmark-only

      - name: Compare with baseline
        run: |
          # Fail if performance regresses >10%
          uv run python scripts/compare_benchmarks.py \
            --threshold 0.10 \
            --baseline .agents/analytics/performance-baseline.json \
            --current benchmark-results.json
```

**Success criteria:**
- [ ] `/profile` command runs cProfile and generates report
- [ ] `/profile-memory` tracks memory usage
- [ ] `/profile-io` detects slow queries and N+1 patterns
- [ ] `/benchmark` framework established with 5+ key benchmarks
- [ ] `/compare-performance` shows before/after metrics
- [ ] `/optimize` suggests data-driven improvements
- [ ] Performance regression detection in CI
- [ ] Optimization recommendations are actionable

**Key Metrics:**
- Benchmark baseline for critical paths
- Performance improvements tracked over time
- Zero performance regressions in CI
- Optimization impact measured and documented

**Timeline:** Month 2-3

---

## Priority 3: Quality & Conventions (Do This Quarter)

### 10. Language-Specific Coding Standards

**Status:** Python complete, expand as needed (YAGNI)

**What it is:**
- Comprehensive style guides per language
- Linting and formatting configurations
- Best practices and anti-patterns
- Framework-specific guidance

**Current Coverage:**

✅ **Python** (Complete in `.claude/reference/`)
- style-conventions.md
- fastapi-best-practices.md
- pydantic-best-practices.md
- pytest-best-practices.md
- aws-lambda-best-practices.md
- security-best-practices.md
- error-handling-patterns.md
- database-standards.md
- performance-optimization.md

**Future Languages:**

❌ **TypeScript/JavaScript** (When actively used)
- Planned: ESLint config, Prettier, React patterns, Node.js best practices

❌ **Go** (When actively used)
- Planned: gofmt, golangci-lint, standard project layout

**Philosophy:**
- Add languages ONLY when actively using them (YAGNI)
- Create language-agnostic template structure first
- Focus on patterns that transfer across languages
- Don't over-document - link to official style guides where possible

**Success criteria:**
- [x] Python standards complete
- [ ] Template structure for language guides created
- [ ] Add new language only when project uses it
- [ ] Cross-language patterns documented separately

**Timeline:** As needed (YAGNI)

---

### 11. Project Ownership & Documentation

**Status:** Not started

**What it is:**
- Clear ownership per module/feature
- Decision log (why we made choices)
- Architecture decision records (ADRs)
- Onboarding documentation

**Components:**

#### 10.1 OWNERS File

```yaml
# .github/OWNERS.yaml

ownership:
  - path: "app/models/"
    owners: ["@dev1", "@dev2"]
    description: "Data models and Pydantic schemas"

  - path: "app/api/"
    owners: ["@dev3"]
    description: "FastAPI endpoints and routing"

  - path: ".claude/"
    owners: ["@dev1"]
    description: "AI coding methodology and reference docs"
```

#### 10.2 Decision Log

```markdown
# .agents/decisions/DECISIONS.md

## Decision Log

### 2026-01-23: Use Anthropic XML format for specs
**Context:** Needed structured format for implementation specs
**Decision:** Adopt Anthropic's XML-based format with semantic tags
**Rationale:**
  - Proven to work at scale (Anthropic uses internally)
  - Machine-readable and human-readable
  - Better than markdown for complex nested structures
**Alternatives considered:**
  - Markdown (too unstructured)
  - JSON (not human-friendly)
  - YAML (ambiguous indentation)
**Status:** Adopted
**Owner:** @dev1
```

#### 10.3 Architecture Decision Records (ADRs)

```markdown
# .agents/architecture/adr/001-multi-session-architecture.md

# ADR 001: Multi-Session Architecture by Default

## Status
Proposed

## Context
Single-session development causes token exhaustion on large features.

## Decision
Design all workflows for multi-session development from the start.

## Consequences
- Eliminates compaction issues
- Predictable token usage
- Fresh context improves quality
- Requires session discipline

## Implementation
See [.agents/research/ANTHROPIC-HARNESS-COMPARISON.md](.agents/research/ANTHROPIC-HARNESS-COMPARISON.md) for detailed design.

## Date
2026-01-23
```

**Success criteria:**
- [ ] OWNERS file created
- [ ] Decision log established
- [ ] ADRs created for major choices
- [ ] Onboarding guide written

**Timeline:** Month 3

---

### 12. Configurable Autonomy Levels

**Status:** Not started

**What it is:**
- Users choose how much AI autonomy vs human oversight
- Different levels for different contexts (prod vs prototype)
- Clear escalation paths when AI gets stuck

**Autonomy Levels:**

**Level 0: Full Supervision (Learning Mode)**
- AI asks approval before EVERY action
- Best for: New users, critical systems

**Level 1: Approve Plans (Current Default)**
- AI creates plan, waits for approval
- Implements autonomously once approved
- Best for: Production development

**Level 2: Approve Phases (Multi-Session)**
- AI implements one phase at a time
- Asks approval before each new phase
- Best for: Large features, want checkpoints

**Level 3: Approve Before Commit Only**
- AI works autonomously
- Only asks approval before final commit
- Best for: Trusted features, time-sensitive work

**Level 4: Full Autonomy (Experimental)**
- AI works completely autonomously
- Creates PR, human reviews asynchronously
- Best for: Prototyping, personal projects

**Configuration:**

```yaml
# .agents/config/autonomy.yaml

default_level: 1

contexts:
  bugfix: 2
  refactor: 1
  feature: 1
  prototype: 3
  emergency: 4

escalation:
  test_failure_threshold: 3
  token_budget_exceeded: true
  security_scan_failure: true
  pattern_not_found: true
```

**Success criteria:**
- [ ] 5 autonomy levels implemented
- [ ] Configuration file format defined
- [ ] Context-specific overrides working
- [ ] Escalation triggers functional

**Timeline:** Month 4

---

### 13. Standard Folder Structures

**Status:** Python complete, expand as needed

**What it is:**
- Consistent project layout per language
- Similar structure across languages where possible
- Templates for new projects

**Current Structure (Python):**

```
py-ai-starter-kit/
├── .agents/                    # AI methodology artifacts
│   ├── plans/
│   ├── specs/
│   ├── init-context/
│   ├── execution-reports/
│   ├── progress/
│   ├── analytics/
│   ├── features/
│   ├── research/
│   ├── architecture/
│   └── decisions/
│
├── .claude/                    # Claude configuration
│   ├── reference/
│   ├── patterns/
│   ├── anti-patterns/
│   ├── templates/
│   ├── workflows/
│   └── config/
│
├── app/                        # Application code
│   ├── models/
│   ├── services/
│   ├── api/
│   ├── utils/
│   └── config.py
│
├── tests/                      # Test suite
│   ├── unit/
│   ├── integration/
│   └── e2e/
│
├── CLAUDE.md
├── GOALS.md
├── CHANGELOG.md
└── pyproject.toml
```

**Cross-language similarities:**
- `.agents/` structure identical
- `.claude/` structure identical
- `tests/` three-tier structure (unit/integration/e2e)
- `CLAUDE.md`, `GOALS.md`, `CHANGELOG.md` in root

**Success criteria:**
- [x] Python structure documented
- [ ] TypeScript structure defined (when needed)
- [ ] Templates for `piv init [language]`
- [ ] Migration guide for existing projects

**Timeline:** Month 4

---

## Priority 4: Advanced Features (Future)

### 14. Smart Context Management

**Status:** Research phase

**What it is:**
- Efficient, not minimal - spend tokens wisely
- Layered loading: start minimal, expand on-demand
- Context caching for stable docs
- Progressive detail

**Research needed:**
- Anthropic's prompt caching API capabilities
- Cost-benefit analysis of caching strategies
- Context pruning algorithms

**Timeline:** Month 6+

---

### 15. Cost Tracking & Optimization

**Status:** Not started

**What it is:**
- Track API costs per feature, session, project
- Budget alerts and spending limits
- Optimization suggestions

**Timeline:** Month 6+

---

### 16. Linear Integration (Optional)

**Status:** Exploring

**What it is:**
- Sync feature status to Linear tickets
- Auto-update ticket when feature completed
- Link commits/PRs to tickets

**Decision needed:** Is this valuable enough to build?

**Timeline:** TBD

---

### 17. Cross-Project Pattern Library

**Status:** Not started

**What it is:**
- Catalog of successful patterns across all projects
- Searchable by language, framework, problem type
- Anti-patterns database (what NOT to do)

**Timeline:** Month 6+

---

### 18. Feedback Loop Analytics

**Status:** Not started

**What it is:**
- Analyze execution reports for trends
- Identify patterns in successful vs difficult features
- Auto-improve token estimates
- Suggest process improvements

**Timeline:** Month 6+

---

### 19. Developer Onboarding System

**Status:** Not started

**What it is:**
- Interactive tutorial for new users
- Guided first feature implementation
- Video walkthroughs of PIV workflow

**Timeline:** Month 6+

---

### 20. Multi-Provider Abstraction

**Status:** Current: Anthropic only

**What it is:**
- Primary: Anthropic API (best for coding)
- Fallback: AWS Bedrock (reliability/compliance)
- Thin abstraction layer (pragmatic, not perfect)

**Philosophy:** "Pragmatic portability" - easy to switch, not perfectly agnostic

**Timeline:** Month 6+ (only if needed)

---

### 21. Advanced Context Optimization Patterns

**Status:** Research complete ([.agents/research/CONTEXT-OPTIMIZATION-RESEARCH.md](.agents/research/CONTEXT-OPTIMIZATION-RESEARCH.md))

**What it is:**
Production-grade optimization techniques from Anthropic for maximizing performance and minimizing costs:

1. **Prompt Caching** (60-90% cost reduction, 75-90% latency improvement)
   - Cache system prompts with 1-hour TTL
   - Cache large documents and codebases
   - Cache conversation history with 5-minute TTL
   - Speculative caching (warm cache while user types)

2. **Conversation Compaction** (50-60% token reduction)
   - Auto-compact at configurable thresholds
   - Use Haiku for summaries (cost optimization)
   - Custom summary prompts to preserve critical context

3. **PreCompact Hooks** (preserve context before summarization)
   - Archive full transcripts before compaction
   - Extract critical entities, decisions, file changes
   - Add custom context to summaries
   - Block compaction if conditions aren't met

4. **Combined Optimization Strategy**
   - Caching + Compaction + Hooks working together
   - Up to 68% cost savings combined
   - 5x effective throughput improvement

**Documentation:**
- Complete implementation guide: [CONTEXT-OPTIMIZATION-RESEARCH.md](CONTEXT-OPTIMIZATION-RESEARCH.md)
- Includes code examples, cost analysis, best practices
- Real-world results from Anthropic's production systems

**Implementation Phases:**

**Phase 1: Caching Patterns** (Month 6)
- Add `.claude/reference/prompt-caching-patterns.md`
- Implement system prompt caching
- Add cache monitoring to tools
- Target: 70%+ cache hit rate

**Phase 2: Auto-Compaction** (Month 7)
- Add `.claude/reference/conversation-compaction-patterns.md`
- Implement auto-compaction in long-running workflows
- Use Haiku for summaries
- Target: 50%+ token reduction in multi-session work

**Phase 3: PreCompact Hooks** (Month 8)
- Create `.claude/hooks/pre_compact.py`
- Archive transcripts before summarization
- Extract critical context preservation
- Integrate with session management system

**Phase 4: Combined Strategy** (Month 9)
- Integrate caching + compaction + hooks
- Add monitoring dashboard
- Document cost savings achieved
- Create optimization playbook

**Success Criteria:**
- [ ] Prompt caching implemented with 70%+ hit rate
- [ ] Auto-compaction reduces token usage by 50%+
- [ ] PreCompact hooks preserve 100% of critical context
- [ ] Combined strategy achieves 60%+ cost savings
- [ ] Monitoring metrics tracked and visualized
- [ ] Documentation complete with examples

**Key Metrics to Track:**
- Cache hit rate (target: 70%+)
- Cache read vs write tokens
- Compaction frequency and token savings
- Time-to-first-token improvements
- Cost per session (before/after optimization)
- Effective throughput (tokens/minute)

**Real-World Impact:**
- Chat with books: **79% latency reduction, 90% cost savings**
- Customer service workflow: **58.6% token reduction** with compaction
- Combined optimizations: **68% cost savings** vs baseline

**Prerequisites:**
- Token Budget Management System (Goal #4) implemented
- Session Management System (Goal #2) operational
- Basic monitoring and metrics in place

**Timeline:** Month 6-9 (research complete, ready for implementation)

---

## Success Metrics

**How we measure "best agentic coding experience":**

### Quality Metrics
- ✅ Test coverage: >80% across all projects
- ✅ Code review scores: >8/10 on all dimensions
- ✅ Zero security vulnerabilities on merge
- ✅ Type checking: 100% coverage

### Efficiency Metrics
- ✅ Token usage: Actual within 15% of estimated
- ✅ Session efficiency: <5% sessions hit compaction
- ✅ Planning accuracy: Specs cover 90%+ of requirements
- ✅ Rework rate: <10% of code rewritten after review

### Developer Experience Metrics
- ✅ Onboarding time: New dev productive in <1 day
- ✅ Feature velocity: Consistent, predictable timelines
- ✅ Context switches: Minimal cognitive load
- ✅ Confidence: Developers trust AI recommendations

### Process Metrics
- ✅ Adoption rate: Team uses PIV loop for 90%+ features
- ✅ Documentation coverage: Every feature has spec + plan + execution report
- ✅ Feedback loops: Execution reports reviewed and acted on
- ✅ Continuous improvement: Measurable process improvements quarterly

---

## Quarterly Goals

### Q1 2026 (Current) - Foundation
- ⬜ Spec creation process (research done, implementation pending)
- ⬜ Session management system
- ⬜ Multi-session architecture by default
- ⬜ Token budget management
- ⬜ Comprehensive skills tree

### Q2 2026 - Quality & Automation
- ⬜ JSON features tracking
- ⬜ TDD culture enforcement
- ⬜ Profiling & optimization system
- ⬜ Configurable autonomy levels
- ⬜ Pattern library (20+ patterns)

### Q3 2026 - Scale & Polish
- ⬜ Cross-project knowledge transfer
- ⬜ Advanced context management
- ⬜ Cost tracking & optimization
- ⬜ Developer onboarding system

### Q4 2026 - Innovation
- ⬜ Feedback loop analytics
- ⬜ Auto-improving systems
- ⬜ Advanced workflows

---

## Contributing

This goals document is living and should be updated as:
- Goals are completed (mark with ✅)
- New needs are discovered
- Priorities shift
- Learnings from implementation

**Update process:**
1. Discuss proposed changes
2. Document decision in DECISIONS.md
3. Update GOALS.md with rationale
4. Announce changes

**Review cadence:**
- Weekly: Check progress on Priority 1 goals
- Monthly: Reassess priorities, add/remove goals
- Quarterly: Major review and planning session

---

## Questions & Clarifications Needed

1. **Previous Goal "TOON":** What was meant by "Probably stop sending json instead of TOON"? (Typo for TOML? Plain text? Different format?)
2. **Linear Integration:** Do we actually need Linear integration or is manual linking sufficient?
3. **Multi-language priority:** Which language should we support next? TypeScript? Go?
4. **Autonomy defaults:** Should Level 1 (approve plans) remain default, or move to Level 2 (approve phases) for multi-session workflow?

---

_Last updated: 2026-01-23_
_Next review: 2026-02-01_
