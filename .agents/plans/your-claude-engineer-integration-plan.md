# Implementation Plan: Your Claude Engineer Pattern Integration

**Feature ID:** yce-integration-001
**Created:** 2026-02-02
**Spec:** [.agents/specs/your-claude-engineer-integration-spec.txt](.agents/specs/your-claude-engineer-integration-spec.txt)
**Analysis:** [.agents/research/your-claude-engineer-analysis-2026-02-02.md](.agents/research/your-claude-engineer-analysis-2026-02-02.md)

---

## Overview

Integrate proven patterns from [Your Claude Engineer](https://github.com/coleam00/your-claude-engineer) to achieve:
- **30-40% cost reduction** through multi-model optimization
- **Fix token tracking bug** (critical user confusion)
- **Enforce quality gates** (prevent regressions)
- **Improve session context** (better resumption)

---

## Phase Summary

| Phase | Duration | Tokens Est. | Priority | Dependencies |
|-------|----------|-------------|----------|--------------|
| Phase 1: Multi-Model Cost Optimization | 2-3 weeks | ~80K | CRITICAL | None |
| Phase 2: Token Tracking Fix | 1-2 weeks | ~60K | CRITICAL | None |
| Phase 3: Quality Gates | 1-2 weeks | ~50K | HIGH | Phase 2 |
| Phase 4: Session Context | 1 week | ~30K | HIGH | Phase 2 |
| Phase 5: Auto-Resume & Checkpoint | 1 week | ~35K | MEDIUM | Phase 2, 4 |
| Phase 6: Documentation & Validation | 3-5 days | ~20K | HIGH | All phases |

**Total Estimated Effort:** 6-9 weeks
**Total Estimated Tokens:** ~275K tokens (split across multiple sessions)

---

## Session Plan

### Session 1: Research & Phase 1 Start (~40K tokens)
- Research Claude Code model selection (Task 1.1)
- Design skill model selection mechanism (Task 1.2)
- Add model field to skill YAML schema (Task 1.3)
- Update first 10 skills with model assignments (Task 1.4 partial)

**Checkpoint after:** Research complete, schema designed, 10 skills updated

### Session 2: Phase 1 Completion (~40K tokens)
- Update remaining 14 skills with model assignments (Task 1.4 complete)
- Implement token tracking by model (Task 1.5)
- Create test feature for measurement (Task 1.6 start)

**Checkpoint after:** All skills updated, token tracking in place

### Session 3: Phase 1 Validation & Phase 2 Start (~50K tokens)
- Complete test feature and measure savings (Task 1.6 complete)
- Document multi-model optimization (Task 1.7)
- Design session.yaml v2 schema (Task 2.1)
- Implement session state manager (Task 2.2)

**Checkpoint after:** Phase 1 complete, Phase 2 started

### Session 4: Phase 2 Completion (~45K tokens)
- Update /execute to reset tokens (Task 2.3)
- Update /resume-session display (Task 2.4)
- Add session_history array (Task 2.5)
- Create migration script (Task 2.6)

**Checkpoint after:** Token tracking fixed, migration ready

### Session 5: Phase 2 Testing & Phase 3 Start (~40K tokens)
- Test multi-session workflow (Task 2.7)
- Update CHANGELOG (Task 2.8)
- Design task YAML v2 with gates (Task 3.1-3.2)
- Update /execute for gates (Task 3.3 start)

**Checkpoint after:** Phase 2 tested, gates designed

### Session 6: Phase 3 & 4 (~40K tokens)
- Complete gate enforcement (Task 3.3-3.5)
- Add gates to templates (Task 3.6)
- Document gates (Task 3.7)
- Extend session_history (Task 4.1-4.3)

**Checkpoint after:** Gates working, session context started

### Session 7: Phase 4, 5, 6 (~40K tokens)
- Complete session context (Task 4.4-4.7)
- Implement auto-resume (Task 5.1-5.3)
- Test auto features (Task 5.4-5.6)
- Begin documentation updates (Task 6.1-6.3)

**Checkpoint after:** All features implemented

### Session 8: Final Validation (~20K tokens)
- Complete documentation (Task 6.4)
- Test on 2-3 real features (Task 6.5)
- Measure outcomes (Task 6.6)
- Create migration guide (Task 6.7)

**Completion:** All phases done, validated, documented

---

## PHASE 1: Multi-Model Cost Optimization

**Goal:** 30-40% cost reduction through Haiku/Sonnet model mixing
**Duration:** 2-3 weeks
**Estimated Tokens:** ~80K (across 2 sessions)
**Priority:** CRITICAL

### Tasks

#### Task 1.1: Research Claude Code Model Selection
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours

**Actions:**
1. Read Claude Code CLI documentation
2. Check if skills can specify model in YAML
3. Test manual model switching in Claude Code
4. Document findings and limitations
5. Determine implementation approach

**Acceptance Criteria:**
- [ ] Documented Claude Code model selection capabilities
- [ ] Identified implementation approach (native vs. workaround)
- [ ] Risks and limitations documented

**Validation:**
- Document findings in `.agents/research/claude-code-model-research.md`

#### Task 1.2: Design Skill Model Selection Mechanism
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours

**Actions:**
1. Design skill YAML frontmatter extension
2. Create skill model assignment strategy
3. Design token tracking schema
4. Design cost calculation logic
5. Review with team

**Acceptance Criteria:**
- [ ] Skill YAML schema extended with `model` field
- [ ] Model assignment strategy documented
- [ ] Token tracking schema designed
- [ ] Cost calculation formula defined

**Validation:**
- Schema documented in `.claude/schemas/skill-v2.yaml`

**Files:**
- Create: `.claude/schemas/skill-v2.yaml`
- Create: `.agents/research/skill-model-selection-design.md`

#### Task 1.3: Add Model Field to Skill YAML Schema
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Update `.claude/schemas/skill.yaml` with `model` field
2. Add `estimated_tokens` field for planning
3. Document field meanings
4. Update example skill
5. Validate schema changes

**Acceptance Criteria:**
- [ ] Schema includes `model: haiku|sonnet|opus` field
- [ ] Schema includes `estimated_tokens: int` field
- [ ] Default model is `sonnet` for backward compatibility
- [ ] Example skill updated

**Validation:**
- Schema parses correctly
- Example skill valid

**Files:**
- Modify: `.claude/schemas/skill.yaml`
- Create: `.claude/schemas/examples/skill-with-model.md`

#### Task 1.4: Update All 24 Skills with Model Assignments
**Estimated Tokens:** ~30K
**Duration:** 1 day
**TDD:** false

**Actions:**
For each skill in `.claude/skills/`:
1. Add `model` field to YAML frontmatter
2. Add `estimated_tokens` field
3. Assign appropriate model:
   - **Haiku:** prime, prime-deep, discuss, spec, plan, plan-feature, validate, pause, resume-session, status, explore, task-list, task-create, task-update, task-complete
   - **Sonnet:** implement-plan, execute, implement-fix, code-review, code-review-since, execution-report, rca, generate-prp, execute-prp
4. Test that skills still load correctly

**Model Assignment Rationale:**

**Haiku Skills (Lightweight):**
- Context gathering (prime, explore)
- Planning and organization (discuss, spec, plan, plan-feature)
- Status and task management (status, task-*)
- Quality checks (validate - runs commands, not deep analysis)
- Session management (pause, resume-session)

**Sonnet Skills (Heavy Lifting):**
- Implementation (implement-plan, execute, implement-fix)
- Deep analysis (code-review, rca)
- Report generation (execution-report)
- PRP operations (generate-prp, execute-prp)

**Acceptance Criteria:**
- [ ] All 24 skills have `model` field
- [ ] All 24 skills have `estimated_tokens` field
- [ ] Assignments follow rationale
- [ ] Skills still load without errors

**Validation:**
- Load each skill and verify YAML parses
- Check no syntax errors

**Files:**
- Modify: `.claude/skills/*/SKILL.md` (all 24 skills)

#### Task 1.5: Implement Token Tracking by Model
**Estimated Tokens:** ~20K
**Duration:** 1 day
**TDD:** true

**Actions:**
1. Write tests for token tracking logic
2. Create token tracking helper script
3. Update session.yaml to track per-model tokens
4. Implement cost calculation by model
5. Test token accumulation

**Acceptance Criteria:**
- [ ] Unit tests for token tracking (pass)
- [ ] session.yaml tracks haiku_tokens, sonnet_tokens, opus_tokens
- [ ] session.yaml tracks haiku_cost, sonnet_cost, opus_cost
- [ ] Cost calculated using correct pricing
- [ ] Tests pass

**Validation Commands:**
```bash
uv run pytest tests/unit/test_token_tracking.py -v
uv run pytest tests/unit/test_cost_calculation.py -v
```

**Files:**
- Create: `tests/unit/test_token_tracking.py`
- Create: `tests/unit/test_cost_calculation.py`
- Create: `.agents/scripts/token_tracker.py`
- Modify: `.agents/schemas/session-v2.yaml`

**Patterns:**
- `.claude/reference/pytest-best-practices.md`
- `.claude/reference/pydantic-best-practices.md`

#### Task 1.6: Test on Real Features and Measure Savings
**Estimated Tokens:** ~15K
**Duration:** 2-3 days (spread across feature development)
**TDD:** false

**Actions:**
1. Select 3 representative features for testing
2. Baseline: Estimate cost if all-Sonnet
3. Actual: Run with multi-model optimization
4. Compare: Calculate cost savings percentage
5. Document: Record findings

**Test Features:**
- Simple feature (mostly planning): Prime optimization improvement
- Medium feature (balanced): Session state management
- Complex feature (heavy implementation): Multi-session architecture

**Acceptance Criteria:**
- [ ] 3 features tested with multi-model approach
- [ ] Baseline all-Sonnet cost calculated
- [ ] Actual multi-model cost measured
- [ ] Cost savings >= 30%
- [ ] Findings documented

**Validation:**
- Compare actual costs vs. baseline
- Verify 30%+ savings achieved

**Files:**
- Create: `.agents/analytics/model-cost-analysis.md`

#### Task 1.7: Document Multi-Model Optimization
**Estimated Tokens:** ~5K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Create reference doc: multi-model-optimization.md
2. Document model selection rationale
3. Document cost savings achieved
4. Provide examples
5. Update CLAUDE.md with guidance
6. Update README.md with cost section

**Acceptance Criteria:**
- [ ] Reference doc created
- [ ] Model selection rationale documented
- [ ] Cost savings data included
- [ ] Examples provided
- [ ] CLAUDE.md updated
- [ ] README.md updated

**Files:**
- Create: `.claude/reference/multi-model-optimization.md`
- Modify: `CLAUDE.md`
- Modify: `README.md`

### Phase 1 Success Criteria

- [x] All 24 skills have `model` field assigned
- [x] Token usage tracked by model in session.yaml
- [x] Cost calculation implemented and accurate
- [x] 30%+ cost reduction measured on 3 real features
- [x] Documentation complete
- [x] No quality degradation (Haiku adequate for assigned tasks)

---

## PHASE 2: Token Tracking Fix

**Goal:** Fix critical token budget tracking across sessions
**Duration:** 1-2 weeks
**Estimated Tokens:** ~60K (across 1-2 sessions)
**Priority:** CRITICAL

### Tasks

#### Task 2.1: Design Session YAML v2 Schema
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours

**Actions:**
1. Design new session.yaml structure
2. Separate current_session vs. feature_total tokens
3. Add session_history array
4. Add per-model tracking
5. Document schema
6. Get feedback

**Acceptance Criteria:**
- [ ] Schema includes current_session_tokens (resets)
- [ ] Schema includes feature_total_tokens (accumulates)
- [ ] Schema includes session_history array
- [ ] Schema includes tokens_by_model
- [ ] Schema includes cost_by_model
- [ ] Schema documented

**Files:**
- Create: `.agents/schemas/session-v2.yaml`
- Create: `.agents/research/session-v2-design.md`

#### Task 2.2: Implement Session State Manager
**Estimated Tokens:** ~20K
**Duration:** 1 day
**TDD:** true

**Actions:**
1. Write tests for session manager
2. Create SessionStateManager class
3. Implement read_session() method
4. Implement write_session() method
5. Implement new_session() method
6. Implement resume_session() method
7. Test all methods

**Acceptance Criteria:**
- [ ] Unit tests for SessionStateManager (pass)
- [ ] Can read session.yaml v2 format
- [ ] Can write session.yaml v2 format
- [ ] new_session() initializes correctly
- [ ] resume_session() increments session number
- [ ] resume_session() resets current_session_tokens to 0

**Validation Commands:**
```bash
uv run pytest tests/unit/test_session_manager.py -v
uv run mypy .agents/scripts/session_manager.py
uv run ruff check .agents/scripts/
```

**Files:**
- Create: `tests/unit/test_session_manager.py`
- Create: `.agents/scripts/session_manager.py`

**Patterns:**
- `.claude/reference/pytest-best-practices.md`
- `.claude/reference/pydantic-best-practices.md`

#### Task 2.3: Update /execute to Reset Session Tokens
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Read current /execute skill
2. Add session detection logic
3. On resume: reset current_session_tokens to 0
4. On resume: increment current_session_number
5. Update session.yaml on start
6. Test multi-session workflow

**Acceptance Criteria:**
- [ ] /execute detects paused sessions
- [ ] current_session_tokens resets to 0 on resume
- [ ] current_session_number increments on resume
- [ ] session.yaml updated correctly
- [ ] Multi-session test passes

**Files:**
- Modify: `.claude/skills/execute/SKILL.md`

#### Task 2.4: Update /resume-session Display
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Read current /resume-session skill
2. Update display to show both token counts:
   - Feature Total: X tokens ($Y across N sessions)
   - Current Session: 0 / 200K (0%)
3. Test display format
4. Verify clarity

**Acceptance Criteria:**
- [ ] Display shows feature_total_tokens
- [ ] Display shows current_session_tokens (0 on start)
- [ ] Display shows cost in USD
- [ ] Display shows session count
- [ ] Format is clear and not confusing

**Files:**
- Modify: `.claude/skills/resume-session/SKILL.md`

#### Task 2.5: Add Session History Array
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** true

**Actions:**
1. Write tests for session history
2. Extend SessionStateManager with history methods
3. add_session_to_history() method
4. get_last_session() method
5. Test history operations

**Acceptance Criteria:**
- [ ] Tests for session history (pass)
- [ ] Can add session to history
- [ ] Can retrieve last session
- [ ] History persists across sessions
- [ ] Tests pass

**Validation Commands:**
```bash
uv run pytest tests/unit/test_session_history.py -v
```

**Files:**
- Create: `tests/unit/test_session_history.py`
- Modify: `.agents/scripts/session_manager.py`

#### Task 2.6: Create Migration Script
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** true

**Actions:**
1. Write tests for migration
2. Create migrate_session_yaml.py script
3. Detect old format (tokens_used field)
4. Convert to new format
5. Backup old file before migration
6. Test migration on sample files

**Acceptance Criteria:**
- [ ] Tests for migration (pass)
- [ ] Detects old format correctly
- [ ] Converts to new format correctly
- [ ] Backups old file (session.yaml.backup)
- [ ] Preserves all data
- [ ] Logs migration actions

**Validation Commands:**
```bash
uv run pytest tests/unit/test_session_migration.py -v
uv run python .agents/scripts/migrate_session_yaml.py --dry-run
```

**Files:**
- Create: `tests/unit/test_session_migration.py`
- Create: `.agents/scripts/migrate_session_yaml.py`
- Create: `.agents/fixtures/session-v1-example.yaml`

#### Task 2.7: Test Multi-Session Workflow
**Estimated Tokens:** ~10K
**Duration:** 3-4 hours
**TDD:** false

**Actions:**
1. Create test feature spanning 3 sessions
2. Session 1: Complete 2 tasks (~40K tokens)
3. Pause and checkpoint
4. Session 2: Resume, complete 2 tasks (~45K tokens)
5. Pause and checkpoint
6. Session 3: Resume, complete 1 task (~20K tokens)
7. Verify token tracking correct
8. Verify no confusion in display

**Acceptance Criteria:**
- [ ] 3-session workflow completes successfully
- [ ] current_session_tokens resets each session
- [ ] feature_total_tokens accumulates correctly
- [ ] session_history has 3 entries
- [ ] Display is clear and accurate

**Validation:**
- Manually verify session.yaml after each session
- Check token counts match expectations

**Files:**
- Create: `tests/integration/test_multi_session_workflow.py`

#### Task 2.8: Update CHANGELOG
**Estimated Tokens:** ~3K
**Duration:** 30 minutes
**TDD:** false

**Actions:**
1. Add breaking changes section to CHANGELOG.md
2. Document session.yaml format change
3. Link to migration script
4. Provide migration instructions
5. Commit CHANGELOG

**Acceptance Criteria:**
- [ ] CHANGELOG.md updated
- [ ] Breaking changes documented
- [ ] Migration instructions clear
- [ ] Links to migration script provided

**Files:**
- Modify: `CHANGELOG.md`

### Phase 2 Success Criteria

- [x] session.yaml v2 schema designed and documented
- [x] SessionStateManager implemented and tested
- [x] current_session_tokens resets to 0 on resume
- [x] feature_total_tokens accumulates correctly
- [x] session_history tracks all sessions
- [x] Migration script works on old sessions
- [x] 3-session workflow tested successfully
- [x] CHANGELOG updated with breaking changes
- [x] User confusion eliminated

---

## PHASE 3: Quality Gates

**Goal:** Enforce quality gates to prevent regressions
**Duration:** 1-2 weeks
**Estimated Tokens:** ~50K (across 1 session)
**Priority:** HIGH
**Dependencies:** Phase 2 (token tracking must work)

### Tasks

#### Task 3.1: Design Task YAML v2 with Gates
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours

**Actions:**
1. Design gates section for task YAML
2. Define gate types: pre_implementation, post_implementation, completion_verification
3. Define failure actions: block, warn
4. Create example task with gates
5. Document schema

**Acceptance Criteria:**
- [ ] Gates section designed
- [ ] Gate types documented
- [ ] Failure actions defined
- [ ] Example task created
- [ ] Schema documented

**Files:**
- Create: `.agents/schemas/task-v2.yaml`
- Create: `.agents/schemas/examples/task-with-gates.yaml`
- Create: `.agents/research/quality-gates-design.md`

#### Task 3.2: Update Task Schema
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Update `.agents/schemas/task.yaml` with gates section
2. Add validation for gate structure
3. Test schema parsing
4. Validate example tasks

**Acceptance Criteria:**
- [ ] Schema includes gates section
- [ ] Schema validates gate structure
- [ ] Example tasks parse correctly
- [ ] Backward compatible (gates optional)

**Files:**
- Modify: `.agents/schemas/task.yaml`

#### Task 3.3: Update /execute Skill to Enforce Gates
**Estimated Tokens:** ~20K
**Duration:** 1 day
**TDD:** false

**Actions:**
1. Read current /execute skill
2. Add pre_implementation gate check
3. Add post_implementation gate check
4. Add completion_verification gate check
5. Implement block vs. warn behavior
6. Track gate results in task file

**Gate Enforcement Logic:**

**Pre-Implementation Gate:**
```
1. Read task.validation.gates.pre_implementation
2. If required == true:
   a. Run all commands
   b. If any fail:
      - If failure_action == "block":
        * Display error
        * Exit without starting task
      - If failure_action == "warn":
        * Display warning
        * Ask user to continue (y/n)
3. Record gate results
```

**Post-Implementation Gate:**
```
1. After implementation complete
2. Read task.validation.gates.post_implementation
3. If required == true:
   a. Run all commands and skills
   b. If any fail:
      - If failure_action == "block":
        * Display error
        * Mark task failed
        * Do not commit
      - If failure_action == "warn":
        * Display warning
        * Ask user to continue (y/n)
4. Record gate results
```

**Completion Verification Gate:**
```
1. After post_implementation gate passes
2. Read task.validation.gates.completion_verification
3. If required == true:
   a. Run all commands
   b. If any fail:
      - If failure_action == "block":
        * Display error
        * Mark task incomplete
        * Do not mark completed
      - If failure_action == "warn":
        * Display warning
        * Proceed to completion
4. Record gate results
```

**Acceptance Criteria:**
- [ ] Pre-implementation gates enforced
- [ ] Post-implementation gates enforced
- [ ] Completion verification gates enforced
- [ ] Block action prevents progression
- [ ] Warn action displays warning but allows continuation
- [ ] Gate results tracked in task file

**Files:**
- Modify: `.claude/skills/execute/SKILL.md`

#### Task 3.4: Implement Gate Result Tracking
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** true

**Actions:**
1. Write tests for gate result tracking
2. Extend task file schema with gate_results
3. Implement gate result writing
4. Test gate result persistence

**Gate Results Format:**
```yaml
gate_results:
  pre_implementation:
    executed: true
    passed: true
    commands:
      - command: pytest tests/unit/ -v
        exit_code: 0
        passed: true
    failure_action: block

  post_implementation:
    executed: true
    passed: false
    commands:
      - command: pytest tests/integration/ -v
        exit_code: 1
        passed: false
        output: "2 tests failed"
    skills:
      - skill: validate
        passed: false
        issues: "Coverage below 80%"
    failure_action: block

  completion_verification:
    executed: false
    passed: null
```

**Acceptance Criteria:**
- [ ] Tests for gate result tracking (pass)
- [ ] gate_results written to task file
- [ ] All gate types tracked
- [ ] Command results captured
- [ ] Skill results captured
- [ ] Tests pass

**Validation Commands:**
```bash
uv run pytest tests/unit/test_gate_tracking.py -v
```

**Files:**
- Create: `tests/unit/test_gate_tracking.py`
- Modify: `.agents/schemas/task.yaml` (add gate_results)

#### Task 3.5: Test Gate Blocking Behavior
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Create test task with failing pre_implementation gate
2. Run /execute, verify blocked
3. Create test task with failing post_implementation gate
4. Run /execute, verify task marked failed
5. Create test task with passing gates
6. Run /execute, verify completes normally

**Acceptance Criteria:**
- [ ] Pre-implementation gate failure blocks task start
- [ ] Post-implementation gate failure blocks commit
- [ ] Completion verification gate failure blocks completion
- [ ] Passing gates allow normal progression
- [ ] Error messages are clear

**Files:**
- Create: `tests/integration/test_gate_enforcement.py`
- Create: `.agents/fixtures/task-with-failing-gate.yaml`
- Create: `.agents/fixtures/task-with-passing-gates.yaml`

#### Task 3.6: Add Gates to Task Templates
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Create task templates with sensible gate defaults
2. API endpoint template (pre: unit tests, post: validate, completion: integration tests)
3. Service template (pre: unit tests, post: validate, completion: unit tests)
4. Bug fix template (pre: regression test, post: validate, completion: regression test)
5. Document when to use each template

**Acceptance Criteria:**
- [ ] 3+ task templates with gates
- [ ] Gates appropriate for task type
- [ ] Templates documented
- [ ] Examples provided

**Files:**
- Create: `.claude/templates/tasks/api-endpoint-task.yaml`
- Create: `.claude/templates/tasks/service-task.yaml`
- Create: `.claude/templates/tasks/bugfix-task.yaml`
- Create: `.claude/reference/task-templates.md`

#### Task 3.7: Document Gate Patterns
**Estimated Tokens:** ~6K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Create reference doc: quality-gates-reference.md
2. Document gate types and when to use
3. Document failure actions (block vs. warn)
4. Provide examples
5. Document best practices
6. Update CLAUDE.md with gate guidance

**Acceptance Criteria:**
- [ ] Reference doc created
- [ ] All gate types documented
- [ ] Examples provided
- [ ] Best practices documented
- [ ] CLAUDE.md updated

**Files:**
- Create: `.claude/reference/quality-gates-reference.md`
- Modify: `CLAUDE.md`

### Phase 3 Success Criteria

- [x] Task YAML schema includes gates section
- [x] /execute enforces all gate types
- [x] Block action prevents progression
- [x] Warn action displays warning
- [x] Gate results tracked in task files
- [x] Task templates with gates created
- [x] Documentation complete
- [x] Integration tests pass

---

## PHASE 4: Session Context Preservation

**Goal:** Improve resumption with rich session context
**Duration:** 1 week
**Estimated Tokens:** ~30K (across 1 session)
**Priority:** HIGH
**Dependencies:** Phase 2 (session_history must exist)

### Tasks

#### Task 4.1: Extend Session History with Summary/Decisions/Blockers
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** true

**Actions:**
1. Write tests for extended session history
2. Update session_history schema
3. Add fields: summary, decisions, blockers
4. Update SessionStateManager
5. Test persistence

**Session History Entry Format:**
```yaml
session_history:
  - session: 1
    started: "2026-02-02T00:00:00Z"
    ended: "2026-02-02T10:30:00Z"
    tokens_used: 35000
    tasks_completed: [task-001]
    summary: |
      Implemented Prime optimization. Reduced token usage from 45K to 10K
      by using shallow discovery pattern. All tests passing.
    decisions:
      - "Use Haiku for prime skill to reduce cost"
      - "Skip reading reference docs until needed"
    blockers: []
```

**Acceptance Criteria:**
- [ ] Tests for extended history (pass)
- [ ] Schema includes summary, decisions, blockers
- [ ] SessionStateManager updated
- [ ] Tests pass

**Validation Commands:**
```bash
uv run pytest tests/unit/test_session_history_extended.py -v
```

**Files:**
- Create: `tests/unit/test_session_history_extended.py`
- Modify: `.agents/schemas/session-v2.yaml`
- Modify: `.agents/scripts/session_manager.py`

#### Task 4.2: Update /pause to Prompt for Summary
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Read current /pause skill
2. Add summary prompt at end of session
3. Prompt: "Session Summary (1-3 sentences, what was accomplished):"
4. Store summary in session_history
5. Test prompt flow

**Acceptance Criteria:**
- [ ] /pause prompts for summary
- [ ] Summary stored in session_history
- [ ] Prompt is clear and concise
- [ ] Can skip prompt with --no-prompt flag

**Files:**
- Modify: `.claude/skills/pause/SKILL.md`

#### Task 4.3: Update /pause to Prompt for Decisions
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. After summary prompt, add decisions prompt
2. Prompt: "Key Decisions Made (comma-separated, press enter to skip):"
3. Parse comma-separated decisions
4. Store in session_history
5. Test prompt flow

**Acceptance Criteria:**
- [ ] /pause prompts for decisions
- [ ] Decisions parsed and stored
- [ ] Can skip with empty input
- [ ] Multiple decisions supported

**Files:**
- Modify: `.claude/skills/pause/SKILL.md`

#### Task 4.4: Update /pause to Prompt for Blockers
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. After decisions prompt, add blockers prompt
2. Prompt: "Any Blockers? (comma-separated, press enter to skip):"
3. Parse comma-separated blockers
4. Store in session_history
5. Test prompt flow

**Acceptance Criteria:**
- [ ] /pause prompts for blockers
- [ ] Blockers parsed and stored
- [ ] Can skip with empty input
- [ ] Multiple blockers supported

**Files:**
- Modify: `.claude/skills/pause/SKILL.md`

#### Task 4.5: Update /resume-session to Display Last Session Context
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Read current /resume-session skill
2. Get last session from session_history
3. Display formatted summary:
   - Last session summary
   - Decisions made
   - Blockers encountered
4. Test display format

**Display Format:**
```
## Resuming Session: py-ai-starter-kit

### Last Session (Session 2)
**Ended:** 2026-02-02 18:18:30
**Tokens:** 58K tokens used
**Completed:** task-002

**Summary:**
Implemented Spec creation process. Created /spec skill with
Anthropic XML format. Added validation for required sections.

**Decisions Made:**
- Use XML format vs. markdown for better structure
- Require acceptance_criteria section in all specs

**Blockers:**
None

### Current Session (Session 3)
Ready to start task-003 (Session Management System)
```

**Acceptance Criteria:**
- [ ] Last session context displayed
- [ ] Format is clear and scannable
- [ ] Works when no prior session
- [ ] Decisions and blockers optional

**Files:**
- Modify: `.claude/skills/resume-session/SKILL.md`

#### Task 4.6: Test Multi-Session with Rich Context
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Run 3-session workflow with prompts
2. Session 1: Complete tasks, provide summary/decisions/blockers
3. Session 2: Resume, verify context displayed
4. Session 2: Complete tasks, provide summary/decisions/blockers
5. Session 3: Resume, verify context displayed
6. Validate context helps resumption

**Acceptance Criteria:**
- [ ] 3-session workflow with prompts completes
- [ ] Context displayed on each resume
- [ ] Context is accurate and helpful
- [ ] No confusion about prior work

**Files:**
- Create: `tests/integration/test_session_context.py`

#### Task 4.7: Document Session Summary Best Practices
**Estimated Tokens:** ~4K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Create reference doc: session-context-best-practices.md
2. Document what makes a good summary
3. Document how to capture decisions
4. Document when to note blockers
5. Provide examples
6. Update CLAUDE.md

**Acceptance Criteria:**
- [ ] Reference doc created
- [ ] Best practices documented
- [ ] Examples provided
- [ ] CLAUDE.md updated

**Files:**
- Create: `.claude/reference/session-context-best-practices.md`
- Modify: `CLAUDE.md`

### Phase 4 Success Criteria

- [x] session_history includes summary, decisions, blockers
- [x] /pause prompts for context (skippable)
- [x] /resume-session displays last session context
- [x] 3-session workflow tested with rich context
- [x] Context is helpful for resumption
- [x] Documentation complete

---

## PHASE 5: Auto-Resume and Checkpointing

**Goal:** Seamless multi-session workflow with auto-resume
**Duration:** 1 week
**Estimated Tokens:** ~35K (across 1 session)
**Priority:** MEDIUM
**Dependencies:** Phase 2 (token tracking), Phase 4 (session context)

### Tasks

#### Task 5.1: Update /execute with Auto-Resume Detection
**Estimated Tokens:** ~10K
**Duration:** 3-4 hours
**TDD:** false

**Actions:**
1. Read current /execute skill
2. Add session detection at startup
3. If session.yaml exists and status == "paused":
   - Display: "🔄 Resuming session for feature: {feature}"
   - Run resume logic (reset tokens, increment session)
   - Display session summary
   - Continue from next_task
4. If no session or status != "paused":
   - Display: "❌ No active session. Run /plan first."
5. Test auto-resume

**Acceptance Criteria:**
- [ ] /execute detects paused sessions
- [ ] Auto-resumes without /resume-session
- [ ] Displays resumption message
- [ ] Session summary shown
- [ ] Works seamlessly

**Files:**
- Modify: `.claude/skills/execute/SKILL.md`

#### Task 5.2: Implement Checkpoint Recommendation Detection
**Estimated Tokens:** ~10K
**Duration:** 3-4 hours
**TDD:** false

**Actions:**
1. Read current /execute skill
2. After task completion, check plan.checkpoint_recommendations
3. Find next checkpoint after current task
4. If checkpoint recommendation matched:
   - Display: "✓ Checkpoint recommendation reached after {task}"
   - Display: "Feature total: {feature_total_tokens}K tokens"
   - Display: "Recommendation: {reason}"
   - Prompt: "Continue or pause? (c/p)"
5. If pause chosen, run /pause automatically
6. Test checkpoint detection

**Acceptance Criteria:**
- [ ] Checkpoint recommendations detected
- [ ] User prompted at checkpoints
- [ ] Auto-pause on 'p' choice
- [ ] Continue on 'c' choice
- [ ] Checkpoint logged in history

**Files:**
- Modify: `.claude/skills/execute/SKILL.md`

#### Task 5.3: Implement Auto-Checkpoint at 88% Tokens
**Estimated Tokens:** ~8K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. During /execute, track current_session_tokens
2. After each task, check: current_session_tokens > 175K (88% of 200K)
3. If threshold exceeded:
   - Display: "🚨 Token budget critical (175K / 200K)"
   - Display: "Auto-checkpointing for session health"
   - Run /pause automatically
   - Exit gracefully
4. Test auto-checkpoint

**Acceptance Criteria:**
- [ ] Auto-checkpoint triggers at 175K current session tokens
- [ ] /pause runs automatically
- [ ] Checkpoint reason logged
- [ ] User informed clearly

**Files:**
- Modify: `.claude/skills/execute/SKILL.md`

#### Task 5.4: Test Auto-Resume Across Conversations
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Session 1: Run /execute, complete tasks, pause manually
2. Close conversation
3. Session 2: New conversation, run /execute (no /resume-session)
4. Verify auto-resumes correctly
5. Verify session summary displayed
6. Complete more tasks

**Acceptance Criteria:**
- [ ] /execute auto-resumes in new conversation
- [ ] No /resume-session needed
- [ ] Session summary displayed
- [ ] Works seamlessly

**Files:**
- Create: `tests/e2e/test_auto_resume.py`

#### Task 5.5: Test Auto-Checkpoint Triggers
**Estimated Tokens:** ~5K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Create feature with checkpoint recommendations
2. Run /execute, complete tasks until checkpoint
3. Verify prompt displayed
4. Test both continue and pause choices
5. Create feature that hits 88% token threshold
6. Verify auto-checkpoint triggers

**Acceptance Criteria:**
- [ ] Checkpoint recommendations trigger prompt
- [ ] Continue choice works
- [ ] Pause choice works
- [ ] 88% threshold triggers auto-checkpoint
- [ ] All checkpoints logged

**Files:**
- Create: `tests/integration/test_auto_checkpoint.py`

#### Task 5.6: Document Auto-Resume Behavior
**Estimated Tokens:** ~4K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Update README.md with auto-resume section
2. Document /execute auto-detection
3. Document checkpoint recommendations
4. Document auto-checkpoint threshold
5. Provide examples
6. Update CLAUDE.md

**Acceptance Criteria:**
- [ ] README.md updated
- [ ] Auto-resume documented
- [ ] Checkpointing documented
- [ ] Examples provided
- [ ] CLAUDE.md updated

**Files:**
- Modify: `README.md`
- Modify: `CLAUDE.md`

### Phase 5 Success Criteria

- [x] /execute auto-resumes paused sessions
- [x] /resume-session becomes optional (for viewing only)
- [x] Checkpoint recommendations prompt user
- [x] Auto-checkpoint at 88% current session tokens
- [x] E2E test passes across conversations
- [x] Documentation complete

---

## PHASE 6: Documentation and Validation

**Goal:** Complete documentation and validate all features
**Duration:** 3-5 days
**Estimated Tokens:** ~20K (across 1 session)
**Priority:** HIGH
**Dependencies:** All phases (1-5 complete)

### Tasks

#### Task 6.1: Update CLAUDE.md with Multi-Model Guidance
**Estimated Tokens:** ~4K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Add section: Multi-Model Cost Optimization
2. Document when to use Haiku vs. Sonnet
3. Document cost savings achieved
4. Provide model selection guidelines
5. Update development commands section

**Acceptance Criteria:**
- [ ] CLAUDE.md includes multi-model section
- [ ] Guidelines clear
- [ ] Cost savings documented
- [ ] Examples provided

**Files:**
- Modify: `CLAUDE.md`

#### Task 6.2: Update README.md with Cost Optimization Section
**Estimated Tokens:** ~4K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Add section: Cost Optimization
2. Document 30-40% savings achieved
3. Explain model selection strategy
4. Provide usage examples
5. Link to reference docs

**Acceptance Criteria:**
- [ ] README.md includes cost optimization section
- [ ] Savings documented with examples
- [ ] Model strategy explained
- [ ] Links to reference docs

**Files:**
- Modify: `README.md`

#### Task 6.3: Create Multi-Model Optimization Reference Doc
**Estimated Tokens:** ~5K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Create .claude/reference/multi-model-optimization.md
2. Document model selection rationale
3. Document per-skill model assignments
4. Provide cost analysis examples
5. Document best practices

**Acceptance Criteria:**
- [ ] Reference doc created
- [ ] All 24 skills documented with rationale
- [ ] Cost analysis included
- [ ] Best practices documented

**Files:**
- Create: `.claude/reference/multi-model-optimization.md`

#### Task 6.4: Update CHANGELOG.md
**Estimated Tokens:** ~3K
**Duration:** 30-60 minutes
**TDD:** false

**Actions:**
1. Add all changes to CHANGELOG.md
2. Document breaking changes
3. Document new features
4. Document improvements
5. Link to migration guide

**Acceptance Criteria:**
- [ ] CHANGELOG.md updated
- [ ] All phases documented
- [ ] Breaking changes highlighted
- [ ] Migration guide linked

**Files:**
- Modify: `CHANGELOG.md`

#### Task 6.5: Test Complete Workflow on 2-3 Real Features
**Estimated Tokens:** ~10K
**Duration:** 2-3 days
**TDD:** false

**Actions:**
1. Select 2-3 real features for end-to-end testing:
   - Feature 1: Simple (mostly planning)
   - Feature 2: Medium (balanced)
   - Feature 3: Complex (heavy implementation)
2. Run complete workflow:
   - /prime (Haiku)
   - /discuss (Haiku)
   - /spec (Haiku)
   - /plan (Haiku)
   - /execute (Sonnet for implementation)
   - /validate (Haiku)
   - /commit (Sonnet for review)
3. Track token usage by model
4. Calculate cost savings
5. Test multi-session flow
6. Test quality gates
7. Verify session context
8. Document results

**Acceptance Criteria:**
- [ ] 2-3 features tested end-to-end
- [ ] All new features used
- [ ] Token tracking accurate
- [ ] Cost savings measured
- [ ] Quality gates work
- [ ] Session context helpful
- [ ] Results documented

**Files:**
- Create: `.agents/analytics/integration-test-results.md`

#### Task 6.6: Measure Cost Savings and Quality Improvements
**Estimated Tokens:** ~5K
**Duration:** 2-3 hours
**TDD:** false

**Actions:**
1. Analyze results from Task 6.5
2. Calculate actual cost savings percentage
3. Compare quality metrics:
   - Regressions prevented by gates
   - Session resumption success rate
   - User confusion eliminated (survey)
4. Document findings
5. Create summary report

**Acceptance Criteria:**
- [ ] Cost savings calculated (target: 30%+)
- [ ] Quality metrics measured
- [ ] Comparison to baseline
- [ ] Findings documented
- [ ] Summary report created

**Files:**
- Create: `.agents/analytics/cost-savings-report.md`
- Create: `.agents/analytics/quality-metrics-report.md`

#### Task 6.7: Create Migration Guide
**Estimated Tokens:** ~4K
**Duration:** 1-2 hours
**TDD:** false

**Actions:**
1. Create migration guide for existing users
2. Document breaking changes
3. Provide step-by-step migration steps
4. Link to migration script
5. Include FAQs

**Migration Steps:**
1. Backup `.agents/state/session.yaml`
2. Run migration script: `uv run python .agents/scripts/migrate_session_yaml.py`
3. Verify session.yaml converted correctly
4. Update all task files to include gates (optional)
5. Review new token tracking display
6. Test multi-session workflow

**Acceptance Criteria:**
- [ ] Migration guide created
- [ ] Steps clear and complete
- [ ] FAQs included
- [ ] Tested on real migration

**Files:**
- Create: `.agents/docs/migration-guide-v2.md`

### Phase 6 Success Criteria

- [x] CLAUDE.md updated with all new features
- [x] README.md updated with cost optimization
- [x] Reference docs complete
- [x] CHANGELOG.md updated
- [x] 2-3 real features tested successfully
- [x] Cost savings validated (30%+)
- [x] Quality improvements measured
- [x] Migration guide published

---

## Risk Management

### Critical Risks

**R-001: Claude Code CLI may not support per-skill model selection**
- **Impact:** HIGH - Cannot implement Phase 1 as designed
- **Mitigation:** Research first (Task 1.1), have fallback plan
- **Fallback:** Use environment variables or separate sessions per model

**R-002: Breaking changes to session.yaml may break workflows**
- **Impact:** MEDIUM - Users with active sessions cannot resume
- **Mitigation:** Provide migration script, auto-detect old format
- **Backup:** Create `.agents/state/session.yaml.backup` before migration

### Medium Risks

**R-003: Token tracking accuracy**
- **Impact:** MEDIUM - Cost calculations may be off
- **Mitigation:** Validate against actual billing, refine over time
- **Monitoring:** Compare estimated vs. actual monthly

**R-004: Quality gates too restrictive**
- **Impact:** MEDIUM - Users may disable or avoid gates
- **Mitigation:** Make gates optional by default, allow customization
- **User control:** `required: false` default, users opt-in to strict mode

### Low Risks

**R-005: Session context prompts slow workflow**
- **Impact:** LOW - Users may skip prompts
- **Mitigation:** Quick prompts, pre-filled defaults, --no-prompt flag
- **Monitoring:** Track prompt skip rate

---

## Success Metrics

### Cost Reduction
- **Target:** 30-40% reduction
- **Measurement:** Compare before/after on 3 features
- **Baseline:** All-Sonnet execution
- **Actual:** Mixed Haiku/Sonnet

### Token Tracking Accuracy
- **Target:** 100% user understanding
- **Measurement:** User survey after multi-session
- **Question:** "Do you understand your token budget?"
- **Pass:** 100% "yes" responses

### Quality Improvement
- **Target:** 0 regressions with gates
- **Measurement:** Track regression rate
- **Baseline:** Historical rate (if known)
- **Target:** 0 in gated features

### Session Resumption Success
- **Target:** 95% completion rate
- **Measurement:** Multi-session features (3+ sessions)
- **Baseline:** Current rate (if known)
- **Target:** 95%+ without manual intervention

### Documentation Completeness
- **Target:** 100% checklist
- **Measurement:**
  - [ ] CLAUDE.md updated
  - [ ] README.md updated
  - [ ] Reference docs created
  - [ ] CHANGELOG.md updated
  - [ ] Migration guide published

---

## Next Steps

1. **Review this plan** with team/stakeholders
2. **Answer open questions** (see spec)
3. **Create task files** for each phase
4. **Begin Phase 1** (Multi-Model Cost Optimization)
5. **Track progress** in session.yaml

---

## Notes

- **Phases can run partially in parallel** after dependencies met
- **Token estimates are approximate** - may vary based on implementation
- **Sessions should checkpoint** at phase boundaries
- **Test frequently** - don't accumulate untested changes
- **Document as you go** - don't defer to end

---

_Plan created: 2026-02-02_
_Estimated completion: 6-9 weeks_
_Total estimated tokens: ~275K (across 8+ sessions)_
