# Anthropic Harness vs PIV Loop Comparison

**Date:** 2026-01-23
**Article:** https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
**Your System:** PIV Loop Methodology

---

## Executive Summary

**TLDR:** Their approach and yours are solving **similar problems** but at **different scales and use cases**.

- **Anthropic's Harness:** Multi-session, fully autonomous agents building entire applications across days/weeks
- **Your PIV Loop:** Single-session to multi-session, human-supervised development with quality gates

**Verdict:** Their system is **more extreme autonomy**, yours is **more quality-focused**. Neither is strictly "better" - they serve different needs.

---

## Side-by-Side Comparison

| Dimension | Anthropic Harness | Your PIV Loop | Winner |
|-----------|-------------------|---------------|--------|
| **Session Model** | Multi-session with fresh context each time | Primarily single-session with optional multi-session | **TIE** (different use cases) |
| **Autonomy Level** | Fully autonomous across sessions | Human-supervised with validation gates | **Anthropic** (more autonomous) |
| **Context Management** | File-based state (init.sh, claude-progress.txt) | Artifact-based + conversation context | **PIV** (richer context) |
| **Quality Assurance** | E2E tests via Puppeteer MCP | Multi-stage validation (linting, types, tests, coverage) | **PIV** (more comprehensive) |
| **Token Efficiency** | Session resets naturally limit token use | Growing context risk (your main pain point) | **Anthropic** (better by design) |
| **Institutional Knowledge** | JSON feature lists + progress logs | Plans, execution reports, context reports, RCA docs | **PIV** (more thorough) |
| **Work Granularity** | 1 feature per session (small increments) | Full feature implementation in one session | **Anthropic** (better for large projects) |
| **Human Oversight** | Minimal (progress checks between sessions) | Continuous (validation after each phase) | **Anthropic** (less human time) |
| **Recoverability** | High (session state in files) | Medium (conversation-based, compaction risk) | **Anthropic** (more resilient) |
| **Developer Experience** | Set-and-forget for hours/days | Active participation throughout | **Depends** (preference) |

---

## What They Do Better

### 1. Token Efficiency Through Session Resets ⭐⭐⭐

**Their approach:**
- Each new session starts **fresh** (no accumulated context)
- Agent reads state from files: `claude-progress.txt`, feature JSON, git log
- Only loads what's needed for current feature
- Natural context limits: 1 feature = 1 session

**Why it works:**
```
Session 1: Fix login bug (0→200K tokens, ends)
Session 2: Add dashboard (starts at 0 tokens again)
Session 3: Optimize performance (starts at 0 tokens again)
```

**Your current problem:**
```
Session 1: /prime (45K) → /plan (10K) → /implement (starts at 55K)
Task 1.1: reads files (+10K = 65K)
Task 1.2: writes code (+15K = 80K)
Task 1.3: debugging (+20K = 100K)
Task 2.1: COMPACTION TRIGGERED (lost context)
```

**Lesson for you:** Multi-session by default, not as a fallback.

---

### 2. Incremental Progress Over Perfection ⭐⭐

**Their approach:**
- 1 feature per session (explicit limit)
- Focus on "code quality suitable for immediate merging"
- Feature list tracks pass/fail (not "partially complete")
- No half-finished features bleeding into next session

**Your approach:**
- Complete feature in one session (ambitious)
- Can lead to context exhaustion mid-feature
- Deviations tracked but feature completion expected

**Example difference:**
```
# Anthropic Harness
Session 1: Implement User.login() method + test ✓
Session 2: Implement User.logout() method + test ✓
Session 3: Add session timeout logic + test ✓

# Your PIV Loop
Session 1: Implement entire auth system (login, logout, sessions, tokens, middleware, tests)
Result: Context exhaustion at middleware implementation
```

**Lesson for you:** Break features into session-sized chunks proactively.

---

### 3. File-Based State Persistence ⭐⭐⭐

**Their key files:**

**`init.sh`** - Session startup script
```bash
#!/bin/bash
# Loads environment, runs tests, displays recent changes
git log -5 --oneline
npm test
cat claude-progress.txt
```

**`claude-progress.txt`** - Agent work log
```
2024-01-20 10:45: Implemented User.login() - tests passing
2024-01-20 14:22: Added password hashing with bcrypt
2024-01-21 09:15: Working on User.logout() - session cleanup needed
```

**`features.json`** - Feature tracking
```json
{
  "features": [
    {"id": 1, "name": "User login", "status": "pass"},
    {"id": 2, "name": "User logout", "status": "pass"},
    {"id": 3, "name": "Session timeout", "status": "fail"},
    {"id": 200, "name": "Admin dashboard", "status": "fail"}
  ]
}
```

**Why this works:**
- **Self-documenting:** Next session reads files to understand state
- **Git-trackable:** All state is versioned
- **Human-readable:** Developer can inspect between sessions
- **Claude-friendly:** Structured format easy to parse

**Your approach:**
- Context reports (`.agents/init-context/`) - written once, rarely updated
- Plans (`.agents/plans/`) - static after creation
- Execution reports (`.agents/execution-reports/`) - post-mortem, not live state
- No "current progress" file that updates during work

**Lesson for you:** Add live progress tracking file that updates during implementation.

---

### 4. Session Startup Ritual ⭐⭐

**Their pattern:**
```
New session starts →
1. Run init.sh (loads environment)
2. Read claude-progress.txt (understand recent work)
3. Check git log -5 (see commits)
4. Run baseline tests (verify nothing broken)
5. Load features.json (identify next failing feature)
6. Work on ONE feature
7. Update claude-progress.txt
8. Mark feature pass/fail
9. Commit
10. END SESSION
```

**Your pattern:**
```
New session starts →
1. /prime (massive context load)
2. /plan-feature (create plan)
3. /implement-plan (execute entire plan in same session)
4. Hope you don't hit compaction
```

**Lesson for you:** Formalize session startup/shutdown protocols.

---

### 5. Explicit E2E Testing via Puppeteer MCP ⭐

**Their approach:**
- Agents instructed to use browser automation for E2E testing
- Prevents "false completion" (agent claims done without verifying)
- Tests actual user-facing behavior, not just unit tests

**Your approach:**
- 3-tier testing (unit/integration/e2e)
- E2E tests exist but may not be run every implementation
- Coverage focused, not always behavior-focused

**Lesson for you:** E2E tests should be mandatory per feature, not optional.

---

## What You Do Better

### 1. Comprehensive Quality Gates ⭐⭐⭐

**Your /validate command:**
```
Stage 1: Linting (ruff check)
Stage 2: Type checking (mypy)
Stage 3: Unit tests (pytest tests/unit/)
Stage 4: Integration tests (pytest tests/integration/)
Stage 5: Coverage analysis (80% threshold)
Stage 6: E2E tests (pytest tests/e2e/)
Stage 7: Security checks (bandit)
```

**Their approach:**
- Run tests (pass/fail)
- E2E via Puppeteer
- No explicit linting, type checking, or coverage requirements

**Winner:** You. Multi-stage validation catches more issues.

---

### 2. Institutional Knowledge Preservation ⭐⭐⭐

**Your artifacts:**
- **Context reports** - Comprehensive codebase understanding
- **Feature plans** - Detailed implementation blueprints with patterns
- **Execution reports** - Post-implementation feedback loops
- **Code reviews** - AI-driven 5-dimension quality assessment
- **RCA documents** - Root cause analysis for bugs

**Their artifacts:**
- progress.txt - Work log
- features.json - Feature tracking
- Git commits - Code history

**Winner:** You. More comprehensive institutional knowledge.

**Why it matters:**
- Your artifacts help future developers understand WHY decisions were made
- Their artifacts track WHAT was done
- Your approach better for long-term maintainability

---

### 3. Human Oversight & Collaboration ⭐⭐

**Your approach:**
- Human reviews plans before implementation
- Human can intervene during implementation
- Human approves before commit
- Validation gates prevent bad code from landing

**Their approach:**
- Fully autonomous (human checks between sessions only)
- Agent self-validates with tests
- Less human time required

**Winner:** Depends on use case
- **Your approach:** Better for production systems, compliance, learning
- **Their approach:** Better for prototyping, experimentation, speed

---

### 4. Pattern Reuse & Convention Following ⭐⭐

**Your planning phase:**
- Searches codebase for similar patterns
- Extracts existing code examples
- Embeds patterns in plan
- Ensures consistency across codebase

**Their approach:**
- Agent rediscovers patterns each session
- Less explicit pattern guidance
- More emergent behavior

**Winner:** You. Better for maintaining consistent codebases.

---

### 5. Feedback Loops for Continuous Improvement ⭐⭐

**Your execution reports:**
- What worked well (patterns to reuse)
- What was difficult (planning gaps)
- What changed (unexpected complexities)
- Recommendations for future features

**Their approach:**
- No explicit feedback loop
- Learning happens implicitly through feature list evolution

**Winner:** You. Systematic improvement over time.

---

## What's Missing in Both Systems

### 1. Neither Has Smart Context Pruning

**The problem:**
- You: Load everything upfront, hit compaction during work
- Them: Start fresh each session (works but loses rich context)

**What would be better:**
- **Layered context loading:** Load minimal baseline, expand as needed
- **Smart caching:** Cache stable docs, reload conversation context only
- **Progressive detail:** High-level map initially, dive deep on demand

---

### 2. Neither Has Adaptive Session Sizing

**The problem:**
- You: Try to do entire feature in one session (often too much)
- Them: One feature per session (works but arbitrary limit)

**What would be better:**
- **Token-aware planning:** Estimate token usage, break into sessions proactively
- **Natural breakpoints:** Pause at logical boundaries (e.g., after Phase 1)
- **Dynamic adjustment:** If hitting 75% context, checkpoint and continue next session

---

### 3. Neither Has Real-Time Progress Tracking

**The problem:**
- You: Todo lists in conversation (lost on compaction)
- Them: progress.txt (manual updates, not real-time)

**What would be better:**
- **Live progress file:** Auto-updated as tasks complete
- **Token usage tracking:** Visible remaining budget
- **Session health metrics:** "70% context used, consider checkpointing"

---

## Synthesis: A Hybrid Approach

### Best of Both Worlds

**Adopt from Anthropic Harness:**

1. **Session-First Design**
   - Default to multi-session workflow
   - 1 phase = 1 session (not 1 feature = 1 session)
   - Natural token limits

2. **File-Based State**
   - `claude-progress.txt` equivalent for live progress
   - Feature tracking JSON
   - Session startup ritual (read state, run tests)

3. **Incremental Progress**
   - Break features into session-sized chunks
   - No half-finished features

**Keep from Your PIV Loop:**

1. **Quality Gates**
   - Multi-stage validation
   - Type checking, linting, coverage
   - Human oversight at critical points

2. **Institutional Knowledge**
   - Comprehensive plans
   - Execution reports
   - Code reviews and RCA

3. **Pattern Reuse**
   - Search for existing patterns
   - Embed in plans
   - Maintain consistency

---

## Concrete Recommendations for Your System

### Immediate (Fix Token Problem Today)

**1. Add Session Checkpointing to /implement-plan**

```markdown
## Session Checkpointing (Auto at 75K tokens)

When token usage reaches 75K during implementation:
1. Write progress to `.agents/progress/current-session.txt`
2. Commit work completed so far
3. Update plan with remaining tasks
4. END SESSION (user starts fresh session to continue)

Resume workflow:
1. New conversation
2. Read `.agents/progress/current-session.txt`
3. Read git diff to see completed work
4. Continue from next task
```

**2. Create Live Progress File**

```bash
# .agents/progress/current-session.txt
Feature: Tax Analysis Agent
Plan: .agents/plans/tax-analysis-complete.md
Started: 2024-01-23 10:30 AM

COMPLETED:
✓ Phase 1, Task 1.1: Create TaxAnalysisInput model
✓ Phase 1, Task 1.2: Create TaxAnalysisOutput model
✓ Phase 1, Task 1.3: Add validation tests

IN PROGRESS:
→ Phase 1, Task 1.4: Implement TaxAnalysisAgent class (30% done)

REMAINING:
- Phase 1, Task 1.5: Add agent configuration
- Phase 2: Integration with Alloy API (6 tasks)
- Phase 3: Testing (4 tasks)

TOKEN USAGE: ~65K / 200K (33%)
VALIDATION STATUS: All tests passing
GIT STATUS: 4 files modified, 2 tests added
```

**3. Add Session Startup Ritual to /implement-plan**

```markdown
## Before Starting Implementation

1. Read progress file (`.agents/progress/current-session.txt`)
2. Check git status and recent commits
3. Run baseline tests (`pytest tests/unit/ -v`)
4. Verify nothing broken before proceeding
5. Continue from last incomplete task
```

---

### Short-Term (This Week)

**1. Multi-Session by Default**

Change workflow from:
```
/prime → /plan-feature → /implement-plan (all in one session)
```

To:
```
Session 1: /prime → /plan-feature
Session 2: /implement-plan Phase 1
Session 3: /implement-plan Phase 2
Session 4: /validate → /code-review → /commit
```

**2. Phase-Sized Planning**

Update `/plan-feature` to break work into phases that fit in one session:
- Target: < 50K tokens per phase
- Each phase = 3-5 tasks max
- Natural breakpoints between phases

**3. Add Token Budget Warnings**

During implementation, monitor and warn:
```
[Token Budget] 50K / 200K used (25%) - proceeding
[Token Budget] 100K / 200K used (50%) - halfway through budget
[Token Budget] 150K / 200K used (75%) - WARNING: Consider checkpointing
[Token Budget] 175K / 200K used (88%) - CRITICAL: Checkpoint now or risk compaction
```

---

### Medium-Term (Next Sprint)

**1. Implement Feature Tracking System**

Create `.agents/features/project-features.json`:
```json
{
  "project": "uw-portal-api",
  "features": [
    {
      "id": "tax-analysis-agent",
      "name": "Tax Analysis Agent with Alloy Integration",
      "status": "in_progress",
      "plan": ".agents/plans/tax-analysis-complete.md",
      "phases": [
        {"phase": 1, "name": "Data Models", "status": "completed"},
        {"phase": 2, "name": "Agent Implementation", "status": "in_progress"},
        {"phase": 3, "name": "Testing", "status": "pending"}
      ],
      "sessions": [
        {"session": 1, "date": "2024-01-22", "work": "Planning", "tokens": 35000},
        {"session": 2, "date": "2024-01-23", "work": "Phase 1", "tokens": 45000},
        {"session": 3, "date": "2024-01-23", "work": "Phase 2", "tokens": 52000}
      ],
      "created": "2024-01-22",
      "last_updated": "2024-01-23"
    }
  ]
}
```

**2. Add Session Metrics Tracking**

Track per session:
- Tokens used
- Tasks completed
- Validations passed/failed
- Time spent
- Context window utilization

**3. Create `/checkpoint` Command**

Explicit checkpointing command:
```bash
/checkpoint

Actions:
1. Update progress file with current state
2. Commit work completed so far (WIP commit)
3. Update feature tracking JSON
4. Generate session summary
5. Save conversation state
6. Display resume instructions
```

---

## Final Verdict: Better or Worse?

**For your use case (uw-portal-api production development):**

| Aspect | Winner | Reasoning |
|--------|--------|-----------|
| **Token efficiency** | **Anthropic** | Session resets solve your main pain point |
| **Quality assurance** | **You** | Multi-stage validation catches more issues |
| **Developer productivity** | **Anthropic** | Less human time per feature |
| **Code quality** | **You** | More thorough validation and oversight |
| **Long-term maintenance** | **You** | Better institutional knowledge |
| **Learning & collaboration** | **You** | Human oversight improves team knowledge |
| **Speed (prototyping)** | **Anthropic** | Fully autonomous is faster |
| **Safety (production)** | **You** | Validation gates prevent bad code |

**Recommendation:** **Adopt their session model, keep your quality gates**

### Ideal Hybrid for uw-portal-api

```
Session 1 (Planning): /prime --quick → /plan-feature
↓
Session 2 (Phase 1): /implement-plan Phase 1 → /validate
↓
Session 3 (Phase 2): /implement-plan Phase 2 → /validate
↓
Session 4 (Phase 3): /implement-plan Phase 3 → /validate
↓
Session 5 (Quality): /code-review → fix issues → /commit
```

**Benefits:**
- ✅ Never hit compaction (sessions naturally limited)
- ✅ Maintain quality gates (validate after each phase)
- ✅ Progress tracked in files (readable between sessions)
- ✅ Human oversight at phase boundaries
- ✅ Institutional knowledge preserved
- ✅ Token-efficient (fresh context each session)

---

## Action Items

### High Priority (Do This Week)

1. **Add live progress file tracking** to /implement-plan
2. **Break features into phases** (max 50K tokens per phase)
3. **Test multi-session workflow** on next feature
4. **Add token usage warnings** during implementation

### Medium Priority (Next Sprint)

1. **Create feature tracking system** (JSON file)
2. **Implement /checkpoint command**
3. **Add session startup ritual** (read state, run tests)
4. **Update PIV-LOOP.md** with multi-session patterns

### Low Priority (Future)

1. **Metrics dashboard** (token usage, session efficiency)
2. **Automated session sizing** (estimate tokens, suggest breaks)
3. **Smart context pruning** (layered loading)
4. **Resume automation** (one-command session continuation)

---

## Summary

**Their system:** Better token efficiency through session resets, good for autonomous work
**Your system:** Better quality assurance and institutional knowledge, good for production

**Best approach:** Combine both
- Use their session model to solve your token problem
- Keep your validation and quality processes
- Add live progress tracking for multi-session continuity

**You're not behind, you're solving different problems.** They optimize for autonomous prototyping, you optimize for production quality. The hybrid approach gets you both.
