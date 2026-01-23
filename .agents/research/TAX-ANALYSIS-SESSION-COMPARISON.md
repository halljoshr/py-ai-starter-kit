# Tax Analysis Implementation: Session Strategy Comparison

**Feature:** Tax Analysis Agent (PRO-142)
**Plan:** tax-analysis-complete.md (1,669 lines, ~9,500 tokens)
**Context:** uw-portal-api-context-2026-01-23.md (~45,000 tokens)

---

## Current Approach (Your PIV Loop)

### Session Structure

**Single Mega-Session:**
```
Session 1: Prime → Plan → Implement All Phases
├── Prime (45K tokens)
├── Read Plan (10K tokens)
├── Phase 1: Tax Reconciliation (5 tasks)
│   ├── Task 1.1: Models (read context, implement, test) → +15K tokens
│   ├── Task 1.2: TOD Service (read demo-tax, migrate, test) → +12K tokens
│   ├── Task 1.3: Heron Service (research API, implement, test) → +18K tokens
│   ├── Task 1.4: TOD Node (implement, test) → +8K tokens
│   ├── Task 1.5: Heron Node (implement, test) → +8K tokens
│   └── [COMPACTION HITS HERE ~118K tokens] ⚠️
└── ❌ FAILURE: Context lost, can't complete remaining tasks
```

**Token Accumulation:**
```
Start:        0K
After Prime:  45K (22.5%)
After Plan:   55K (27.5%)
Task 1.1:     70K (35%)
Task 1.2:     82K (41%)
Task 1.3:    100K (50%)
Task 1.4:    108K (54%)
Task 1.5:    116K (58%)
Task 1.6:    ⚠️ COMPACTION at ~120K (60%)
```

**Problems:**
- ❌ Never completes Phase 1 before hitting compaction
- ❌ Context loss = forgot plan details, patterns, gotchas
- ❌ Have to restart session, re-prime, re-load context
- ❌ Frustration and time waste
- ❌ Inconsistent implementation (patterns forgotten)

---

## Anthropic Harness Approach

### Session Structure

**Multi-Session with File-Based State:**

#### Session 0: Planning Only (Separate from Implementation)
```
Session 0: Prime → Plan → Save → Close
├── Prime (45K tokens - but only once)
├── Plan creation (10K tokens)
└── Save plan, close conversation
Total: 55K tokens, 1 session
```

#### Session 1: Phase 1 - Models & Services Setup
```
[FRESH CONTEXT - 0 tokens]
├── Read progress file (.agents/progress/tax-current.txt) → 2K tokens
├── Read plan Phase 1 section → 3K tokens
├── git log -5 → 0.5K tokens
├── Implement Task 1.1: Models → 10K tokens
├── Implement Task 1.2: TOD Service → 8K tokens
├── Update progress file
├── Commit work
└── Close session
Total: ~23.5K tokens, well under limit
```

#### Session 2: Phase 1 - Heron Service
```
[FRESH CONTEXT - 0 tokens]
├── Read progress file → 2K tokens
├── Read plan Phase 1 section → 3K tokens
├── git diff → 1K tokens
├── Implement Task 1.3: Heron Service → 15K tokens
├── Update progress file
├── Commit work
└── Close session
Total: ~21K tokens, well under limit
```

#### Session 3: Phase 1 - Nodes
```
[FRESH CONTEXT - 0 tokens]
├── Read progress file → 2K tokens
├── Read plan Phase 1 section → 3K tokens
├── Implement Task 1.4: TOD Node → 6K tokens
├── Implement Task 1.5: Heron Node → 6K tokens
├── Update progress file
├── Commit work
└── Close session
Total: ~17K tokens, well under limit
```

#### Session 4: Phase 1 - Bedrock & Workflow
```
[FRESH CONTEXT - 0 tokens]
├── Read progress file → 2K tokens
├── Read plan Phase 1 section → 3K tokens
├── Implement Task 1.6: Bedrock Node → 8K tokens
├── Implement Task 1.7: Workflow → 10K tokens
├── Update progress file
├── Commit work
└── Close session
Total: ~23K tokens, well under limit
```

#### Session 5: Phase 1 - Integration & Tests
```
[FRESH CONTEXT - 0 tokens]
├── Read progress file → 2K tokens
├── Read plan Phase 1 section → 3K tokens
├── Implement Task 1.8-1.11: Config, manager, router, tests → 20K tokens
├── Run validation → 5K tokens
├── Update progress file
├── Final commit
└── Close session
Total: ~30K tokens, well under limit
```

**Continue similarly for Phases 2-5...**

**Token Usage per Session:**
- Average: 20-30K tokens per session
- Max: Never exceeds 50K tokens
- ✅ NEVER hits compaction
- ✅ Each session completes cleanly

**Progress File (.agents/progress/tax-current.txt):**
```txt
Feature: Tax Analysis Agent (PRO-142)
Plan: .agents/plans/tax-analysis-complete.md
Branch: feature/pro-142-tax-build-agent
Started: 2026-01-23 09:00 AM
Last Updated: 2026-01-23 14:30 PM

COMPLETED SESSIONS:
✓ Session 1 (Jan 23 09:00-10:15): Phase 1 Models & Services
✓ Session 2 (Jan 23 10:30-11:45): Phase 1 Heron Service
✓ Session 3 (Jan 23 13:00-14:00): Phase 1 Nodes
✓ Session 4 (Jan 23 14:00-14:30): Phase 1 Bedrock & Workflow

IN PROGRESS:
→ Session 5: Phase 1 Integration & Tests (50% done)

COMPLETED TASKS:
✓ Phase 1, Task 1.1: Reconciliation models (app/models/schemas.py +120 lines)
✓ Phase 1, Task 1.2: TOD Filing service (app/services/tod_filing_service.py, migrated from demo-tax)
✓ Phase 1, Task 1.3: Heron tax service (app/services/heron_tax_service.py +180 lines)
✓ Phase 1, Task 1.4: TOD Filing node (src/nodes/tod_filing.py +90 lines)
✓ Phase 1, Task 1.5: Heron tax node (src/nodes/heron_tax.py +85 lines)
✓ Phase 1, Task 1.6: Tax Bedrock node (src/nodes/tax_bedrock.py +110 lines)
✓ Phase 1, Task 1.7: Tax workflow (src/graph/workflows.py +150 lines)

CURRENT TASK:
→ Phase 1, Task 1.8-1.11: Config, workflow manager, router, comprehensive tests

REMAINING:
- Phase 2: Tax Compliance Verification (5 tasks)
- Phase 3: Entity Identification (4 tasks)
- Phase 4: Affiliate Discovery (5 tasks)
- Phase 5: Implied Debt Analysis (4 tasks)

VALIDATION STATUS:
- Last validation: Session 4 end - All tests passing
- Coverage: 87.3% (target: 80%+)
- Linting: Clean (ruff check)
- Type checking: Clean (mypy)

GIT STATUS:
- Commits: 4 WIP commits (one per session)
- Files modified: 8 new files, 3 modified
- Branch status: Up to date with dev

TOKEN USAGE (Sessions 1-4):
- Session 1: 23.5K / 200K (12%)
- Session 2: 21K / 200K (10%)
- Session 3: 17K / 200K (8.5%)
- Session 4: 23K / 200K (11.5%)
- Average: 21K per session
- ZERO compactions ✅
```

**Advantages:**
- ✅ Each session completes successfully
- ✅ Never hits compaction (20-30K per session)
- ✅ Natural checkpoints (commit after each session)
- ✅ Progress tracked in file (survives conversation ends)
- ✅ Can pause/resume work easily
- ✅ Less cognitive load (focus on 1-2 tasks per session)

**Disadvantages:**
- ⚠️ More sessions required (5 sessions for Phase 1 vs attempting 1)
- ⚠️ Context switching between sessions
- ⚠️ Must manually read progress file each time
- ⚠️ No rich context report (just progress file + plan)
- ⚠️ Less institutional knowledge per session

---

## Your PIV Loop Approach (Current)

### Session Structure

**What Actually Happens:**
```
Session 1: Prime + Plan
├── Prime (45K tokens)
├── Plan creation (10K tokens)
└── Close conversation (optional, rarely done)
Total: 55K tokens

Session 2: Implement All at Once (PROBLEM)
├── Read plan (10K tokens)
├── [No prime context - start fresh? Or carry over?]
├── Phase 1 Tasks 1-11 → Attempts to do all
├── COMPACTION hits mid-implementation
└── ❌ FAILURE: Context lost, incomplete work

Restart Session 3: Resume attempt
├── Read plan again (10K)
├── git diff to see what was done (5K)
├── Try to continue from where left off
├── May hit compaction again
└── Frustration cycle
```

**Actual Token Flow (Current Problem):**
```
Session 1 (Planning):
- Prime: 45K
- Plan: 10K
- Total: 55K ✅ (No problem here)

Session 2 (Implementation - THE PROBLEM):
- Start: 0K (if fresh) or 55K (if same session)
- Read plan: +10K
- Task 1.1: +15K
- Task 1.2: +12K
- Task 1.3: +18K (now at 55-100K depending on starting point)
- Task 1.4: +8K
- Task 1.5: +8K
- [COMPACTION at ~120K] ⚠️
- Task 1.6: Can't complete (context lost)
```

**Why It Fails:**
1. **No progress tracking** - If compaction hits, don't know what's done
2. **No session boundaries** - Try to do everything at once
3. **Large plan stays in context** - 10K tokens not needed during implementation
4. **No intermediate commits** - All-or-nothing approach
5. **Context report not used during implementation** - 45K prime wasted

---

## Hybrid Approach (Recommended)

### Session Structure

**Combines best of both:**

#### Session 0: Quick Prime + Planning
```
Session 0: Quick Prime → Plan → Close
├── Quick Prime (8K tokens using --quick flag)
│   - Skip full docs reads
│   - Just structure + git state + recent plans
│   - Generate minimal context reference index
├── Plan creation (10K tokens)
│   - Self-contained plan with embedded context
│   - File references with line numbers
│   - Complete code examples inline
└── Save plan, close conversation
Total: 18K tokens (saves 37K vs full prime!)
```

#### Session 1: Phase 1.1 - Data Models
```
[FRESH CONTEXT - 0 tokens]
├── Read progress file (.agents/progress/tax-current.txt) → 2K tokens
├── Read plan Phase 1.1 section → 2K tokens
├── git log -5 → 0.5K tokens
├── Baseline validation (run existing tests) → 1K tokens
├── Implement Task 1.1: Models
│   ├── Write tests first (TDD) → 5K tokens
│   ├── Implement models → 5K tokens
│   ├── Run tests → 2K tokens
│   └── Validation (ruff, mypy) → 1K tokens
├── Update progress file
├── Commit work
└── Close session
Total: ~18.5K tokens

Validation checkpoint:
✓ Tests passing
✓ Linting clean
✓ Coverage threshold met
```

#### Session 2: Phase 1.2 - TOD Filing Service
```
[FRESH CONTEXT - 0 tokens]
├── Startup ritual:
│   ├── Read progress file → 2K
│   ├── Read plan Phase 1.2 section → 2K
│   ├── git status → 0.5K
│   ├── Run baseline tests → 1K
│   └── Verify nothing broken → 0.5K
├── Implementation:
│   ├── Write service tests → 4K
│   ├── Migrate TOD service from demo-tax → 6K
│   ├── Update imports and config → 2K
│   ├── Run tests → 2K
│   └── Validation (ruff, mypy) → 1K
├── Update progress file → 0.5K
├── Commit with WIP message → 0.5K
└── Close session
Total: ~22K tokens

TOKEN BUDGET CHECK:
Current: 22K / 200K (11%)
Status: ✅ GREEN - Safe to continue
```

#### Session 3: Phase 1.3 - Heron Tax Service (CRITICAL TASK)
```
[FRESH CONTEXT - 0 tokens]
├── Startup ritual → 6K tokens
├── Implementation:
│   ├── Research Heron API (read docs, examples) → 8K
│   ├── Write service tests → 5K
│   ├── Implement HeronTaxService → 10K
│   ├── Run tests → 2K
│   ├── Validation → 1K
│   └── [TOKEN CHECK: 32K / 200K (16%)] ✅
├── Update progress file → 0.5K
├── Commit → 0.5K
└── Close session
Total: ~33K tokens

CRITICAL TASK HANDLING:
- Heron API uncertainty = more exploratory work
- Kept in one session but monitored token usage
- Would split if approaching 50K tokens
```

#### Session 4: Phase 1.4-1.5 - Workflow Nodes
```
[FRESH CONTEXT - 0 tokens]
├── Startup ritual → 6K
├── Task 1.4: TOD Node → 8K
├── Task 1.5: Heron Node → 8K
├── Both tasks related, small enough to batch
├── Tests for both → 4K
├── Validation → 2K
├── Update progress + commit → 1K
└── Close session
Total: ~29K tokens
```

#### Session 5: Phase 1.6-1.7 - Bedrock & Workflow
```
[FRESH CONTEXT - 0 tokens]
├── Startup ritual → 6K
├── Task 1.6: Bedrock analysis node → 10K
├── Task 1.7: Workflow creation → 12K
├── Integration tests → 6K
├── Validation → 2K
├── Update progress + commit → 1K
└── Close session
Total: ~37K tokens

TOKEN BUDGET CHECK:
Current: 37K / 200K (18.5%)
Status: ✅ GREEN - Well under threshold
```

#### Session 6: Phase 1.8-1.11 - Integration & Testing
```
[FRESH CONTEXT - 0 tokens]
├── Startup ritual → 6K
├── Config updates → 4K
├── Workflow manager integration → 6K
├── Agent router updates → 4K
├── Comprehensive tests → 12K
├── Full validation suite → 5K
├── Update progress + commit → 1K
├── Phase 1 COMPLETE marker in progress file
└── Close session
Total: ~38K tokens
```

#### Session 7: Phase 1 Review & Phase 2 Kickoff
```
[FRESH CONTEXT - 0 tokens]
├── Startup ritual → 6K
├── Run full test suite for Phase 1 → 4K
├── Code review findings (if any) → 5K
├── Fix critical issues → 8K
├── Final Phase 1 commit (clean, squashed) → 2K
├── Read plan Phase 2 section → 3K
├── Update progress file for Phase 2 start
└── Close session
Total: ~28K tokens
```

**Continue for Phases 2-5 following same pattern...**

### Progress File Enhanced (.agents/progress/tax-current.txt)

```txt
Feature: Tax Analysis Agent (PRO-142)
Plan: .agents/plans/tax-analysis-complete.md (self-contained, embedded context)
Branch: feature/pro-142-tax-build-agent
Context Index: .agents/init-context/context-reference-index.md (read on demand)
Started: 2026-01-23 09:00 AM
Last Updated: 2026-01-23 16:45 PM

=== PHASE 1: TAX RETURN RECONCILIATION ===
Status: ✅ COMPLETE (6 sessions, 0 compactions)

Session History:
1. [09:00-09:45] Models (18.5K tokens) ✓
2. [10:00-10:45] TOD Service (22K tokens) ✓
3. [11:00-12:00] Heron Service (33K tokens) ✓ [CRITICAL]
4. [13:00-13:45] Nodes (29K tokens) ✓
5. [14:00-14:50] Bedrock & Workflow (37K tokens) ✓
6. [15:00-16:00] Integration & Tests (38K tokens) ✓
7. [16:00-16:45] Review & Fixes (28K tokens) ✓

Completed Files:
✓ app/models/schemas.py (+120 lines: ReconciliationVariance, YearReconciliation, ReconciliationResult)
✓ app/services/tod_filing_service.py (migrated from demo-tax, 350 lines)
✓ app/services/heron_tax_service.py (new, 180 lines)
✓ src/nodes/tod_filing.py (new, 90 lines)
✓ src/nodes/heron_tax.py (new, 85 lines)
✓ src/nodes/tax_bedrock.py (new, 110 lines)
✓ src/graph/workflows.py (+150 lines: create_tax_analysis_workflow)
✓ app/core/config.py (+20 lines: TOD & Bedrock config)
✓ app/services/workflow_manager.py (+80 lines: TAX_ANALYSIS case)
✓ app/core/agent_router.py (+15 lines: AgentType.TAX_ANALYSIS)
✓ tests/unit/models/test_tax_models.py (new, 120 lines)
✓ tests/unit/services/test_tod_filing_service.py (new, 180 lines)
✓ tests/unit/services/test_heron_tax_service.py (new, 150 lines)
✓ tests/unit/nodes/test_tod_filing_node.py (new, 100 lines)
✓ tests/unit/nodes/test_heron_tax_node.py (new, 95 lines)
✓ tests/unit/nodes/test_tax_bedrock_node.py (new, 110 lines)
✓ tests/integration/test_tax_workflow.py (new, 200 lines)

Validation Results:
✓ All unit tests passing (259 → 319 tests, +60)
✓ All integration tests passing (74 → 75 tests, +1)
✓ Coverage: 87.3% (up from 86.1%, threshold: 80%)
✓ Linting: Clean (ruff check)
✓ Type checking: Clean (mypy)
✓ No merge conflicts with dev

Git Commits:
- 7c8a1f2 WIP: Phase 1 models
- 9d4e3b1 WIP: Phase 1 TOD service
- 2f1a8c4 WIP: Phase 1 Heron service
- 6b9d2e3 WIP: Phase 1 nodes
- 4a7f1d5 WIP: Phase 1 Bedrock & workflow
- 8e2c9f6 WIP: Phase 1 integration
- 1d3a4b7 feat(tax): Complete Phase 1 - Tax Return Reconciliation

=== PHASE 2: TAX COMPLIANCE VERIFICATION ===
Status: 🔄 IN PROGRESS (Session 8 active)

Next Session Plan:
→ Session 8: Compliance models & TOD enhancement (estimated 25K tokens)
→ Session 9: Compliance logic (estimated 20K tokens)
→ Session 10: Tests & validation (estimated 30K tokens)

=== PHASES 3-5: PENDING ===

=== TOKEN USAGE ANALYTICS ===
Total sessions: 7
Total tokens used: 205.5K (across 7 fresh sessions)
Average per session: 29.4K tokens
Max session: 38K tokens (Session 6)
Min session: 18.5K tokens (Session 1)
Compactions: 0 ✅
Success rate: 100% ✅

=== DEVIATIONS FROM PLAN ===
1. Session 3 took longer than estimated due to Heron API uncertainty
   - Mitigation: Monitored tokens, stayed under 50K
2. Batched Tasks 1.4-1.5 together (small, related tasks)
   - Reason: Both were node implementations, similar patterns
3. Added Session 7 for review not in original plan
   - Reason: Best practice to validate before moving to Phase 2

=== LEARNINGS ===
- Quick prime (8K) was sufficient, didn't need full prime
- Self-contained plans work well (no need for context report during implementation)
- Session checkpoints every 30-40K tokens optimal
- File-based progress tracking essential for multi-session work
- Token monitoring every 10K tokens prevents surprises
```

### Key Hybrid Features

**1. Quick Prime Mode:**
```bash
/prime --quick

Output: Context Reference Index (3-5K tokens)
Instead of: Full context report (15-20K tokens)

Savings: ~15K tokens per prime
```

**2. Self-Contained Plans:**
- All necessary code examples embedded
- File references with specific line numbers
- No dependency on prime context during implementation
- Plan acts as complete implementation guide

**3. Progress File as Single Source of Truth:**
- Updated after EVERY session
- Tracks completed work, current task, remaining work
- Includes validation status
- Token usage analytics
- Deviation tracking
- Git commit log

**4. Session Startup Ritual:**
```
1. Read progress file (2K tokens)
2. Read relevant plan section (2-3K tokens)
3. git status / git log (0.5K tokens)
4. Run baseline tests (1K tokens)
5. Proceed with implementation
```

**5. Session Checkpointing:**
- Natural breaks every 30-40K tokens
- Commit work at end of each session
- Update progress file
- Close conversation (free up resources)

**6. Token Budget Monitoring:**
```
Every 10K tokens, check:
- Current usage
- Remaining budget
- Estimated remaining work

If approaching 75K:
- Checkpoint now
- Commit work
- Close session
- Resume in next session
```

**7. Validation Gates:**
```
After EACH task within session:
✓ ruff check {file}
✓ mypy {file}
✓ pytest tests/unit/{module}/ -v

After EACH session:
✓ All tests passing
✓ Coverage maintained
✓ No linting errors
✓ Commit clean state
```

---

## Token Comparison: Full Implementation

### Anthropic Harness (Multi-Session)

**Phase 1 Only (11 tasks):**
```
Session 0: Plan                     18K tokens
Session 1: Models                   20K tokens
Session 2: TOD Service              22K tokens
Session 3: Heron Service            30K tokens
Session 4: Nodes                    28K tokens
Session 5: Bedrock & Workflow       35K tokens
Session 6: Integration              38K tokens
Session 7: Testing                  25K tokens
Session 8: Review                   20K tokens

Total: 236K tokens across 9 sessions
Average: 26.2K per session
Max: 38K (Session 6)
Compactions: 0 ✅
Success: 100% ✅
```

### Your Current PIV (Single Session Attempt)

**Phase 1 Only (11 tasks):**
```
Session 0: Prime + Plan             55K tokens
Session 1: Implement All
├── Start                            0K (or 55K if same session)
├── Read plan                       10K
├── Tasks 1.1-1.3                   45K
├── COMPACTION                      [Lost context]
├── Tasks 1.4-1.6                   ❌ Can't complete
└── Session ends incomplete

Session 2: Resume attempt
├── Re-read plan                    10K
├── git diff                         5K
├── Continue where left off         40K
├── COMPACTION again                [More context loss]
└── ❌ Still incomplete

Session 3: Final attempt
├── Re-read everything              15K
├── Complete remaining              50K
├── Testing                         15K
└── ✅ Finally done (frustration high)

Total: ~245K tokens across 3 frustrated sessions
Compactions: 2-3 ⚠️
Success: Eventually, with pain
Developer experience: Poor
```

### Hybrid Approach (Optimal)

**Phase 1 Only (11 tasks):**
```
Session 0: Quick Prime + Plan        18K tokens
Session 1: Models                    18.5K tokens
Session 2: TOD Service               22K tokens
Session 3: Heron Service             33K tokens
Session 4: Nodes                     29K tokens
Session 5: Bedrock & Workflow        37K tokens
Session 6: Integration               38K tokens
Session 7: Review                    28K tokens

Total: 223.5K tokens across 8 sessions
Average: 27.9K per session
Max: 38K (Session 6)
Compactions: 0 ✅
Success: 100% ✅
Developer experience: Excellent
```

**Savings vs Current:**
- 21.5K tokens saved (9.6% reduction)
- 0 compactions vs 2-3
- Much better developer experience
- Predictable, reliable progress

---

## Recommendations for Your Tax Analysis Implementation

### Immediate Actions

**1. Create Progress File Template:**

```bash
mkdir -p .agents/progress
touch .agents/progress/tax-current.txt
```

**2. Implement Quick Prime:**

Update `.claude/commands/core_piv_loop/prime.md` to add `--quick` flag:
```markdown
## Quick Prime (Default for Known Codebases)

When: Daily work, familiar codebase, recent prime exists

Process:
1. Read project structure (git ls-files | head -50)
2. Read git state (status, log -5, branch)
3. List recent plans (last 3-5)
4. Generate minimal context reference index

Output: .agents/init-context/{project}-quick-{date}.md (2-3K tokens)
```

**3. Break Tax Analysis into Session-Sized Phases:**

Instead of trying to do all of Phase 1 in one session:

```
Session 1: Phase 1.1 - Data Models Only (Tasks 1.1)
Session 2: Phase 1.2 - TOD Filing Service (Task 1.2)
Session 3: Phase 1.3 - Heron Tax Service (Task 1.3)
Session 4: Phase 1.4-1.5 - Workflow Nodes (Tasks 1.4-1.5)
Session 5: Phase 1.6-1.7 - Bedrock & Workflow (Tasks 1.6-1.7)
Session 6: Phase 1.8-1.11 - Integration & Tests (Tasks 1.8-1.11)
```

**4. Update Plan with Session Breaks:**

Add to tax-analysis-complete.md:
```markdown
## Session Breakdown (Hybrid Approach)

### Session 1: Phase 1.1 - Data Models
**Token Budget:** ~20K tokens
**Tasks:** 1.1
**Deliverables:**
- ReconciliationVariance model
- YearReconciliation model
- ReconciliationResult model
- Unit tests passing

### Session 2: Phase 1.2 - TOD Filing Service
**Token Budget:** ~25K tokens
**Tasks:** 1.2
**Deliverables:**
- Migrated TOD Filing service
- Service tests passing
- Config updated

[Continue for all sessions...]
```

### Modified Workflow for Next Feature

**Before starting implementation:**

1. **Skip /prime if you primed recently (same day)**
2. **Or use /prime --quick** (saves 37K tokens)
3. **Create self-contained plan** (all context embedded)
4. **Initialize progress file** (.agents/progress/{feature}-current.txt)
5. **Close planning conversation**

**During implementation:**

1. **Session 1:**
   ```bash
   # New conversation
   Read: .agents/progress/{feature}-current.txt
   Read: .agents/plans/{feature}.md (relevant section only)
   git status && git log -5
   Implement: First logical chunk (aim for 20-30K tokens)
   Validate: Tests pass, linting clean
   Update: Progress file
   Commit: WIP commit
   Close: Conversation
   ```

2. **Session 2+:**
   ```bash
   # Repeat same pattern
   # Each session: 20-40K tokens max
   # Checkpoint if approaching 75K
   ```

3. **Monitor tokens every 10K:**
   ```python
   # Add this awareness to your process
   if current_tokens > 75000:
       checkpoint_and_close_session()
   ```

### Expected Improvement

**Before (Current Pain):**
- ❌ Compaction by Task 1.1 in Phase 1
- ❌ Can't complete features
- ❌ Have to restart multiple times
- ❌ Frustration and time waste

**After (Hybrid Approach):**
- ✅ Complete Phase 1 in 6-7 sessions
- ✅ ZERO compactions
- ✅ Each session completes cleanly
- ✅ Predictable, reliable progress
- ✅ Better code quality (focused sessions)
- ✅ Progress tracked in files (can pause/resume anytime)

---

## Summary: Which Approach for Tax Analysis?

### For Your uw-portal-api Tax Feature

**Recommended: Hybrid Approach**

**Rationale:**
1. **Saves tokens** (18K quick prime vs 45K full prime)
2. **Prevents compaction** (sessions naturally limited to 20-40K)
3. **Better than Anthropic's** (keep your quality gates)
4. **Institutional knowledge preserved** (progress files + plan artifacts)
5. **Can pause/resume** (progress file tracks state)

**Implementation Plan:**

```
Day 1:
- Session 0: Quick Prime + Plan Tax Analysis (30 min, 18K tokens)

Day 2:
- Session 1: Phase 1.1 - Models (1 hour, 20K tokens)
- Session 2: Phase 1.2 - TOD Service (1 hour, 25K tokens)

Day 3:
- Session 3: Phase 1.3 - Heron Service (1.5 hours, 33K tokens)
- Session 4: Phase 1.4-1.5 - Nodes (1 hour, 29K tokens)

Day 4:
- Session 5: Phase 1.6-1.7 - Bedrock & Workflow (1.5 hours, 37K tokens)
- Session 6: Phase 1.8-1.11 - Integration (1.5 hours, 38K tokens)

Day 5:
- Session 7: Phase 1 Review & Fixes (1 hour, 28K tokens)
- Phase 1 Complete ✅

Continue Phases 2-5 similarly...
```

**Expected Timeline:**
- Phase 1: 5-7 sessions (~2 days)
- Phase 2: 3-4 sessions (~1 day)
- Phase 3: 3-4 sessions (~1 day)
- Phase 4: 4-5 sessions (~1.5 days)
- Phase 5: 3-4 sessions (~1 day)
- **Total: ~20-28 sessions (~7-10 days)**

vs Current Approach:
- **Total: Unknown (keeps hitting compaction, restarting, frustration)**

**The hybrid approach is predictable, reliable, and prevents the pain you're currently experiencing.**
