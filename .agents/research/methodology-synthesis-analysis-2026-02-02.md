# Methodology Synthesis Analysis: PIV, RPI, SWARM & Beyond

**Date:** 2026-02-02
**Purpose:** Comparative analysis of coding methodologies to design optimal system
**Status:** Research & Synthesis Phase

---

## Executive Summary

After analyzing **PIV (Prime → Implement → Validate)**, **RPI (Research → Plan → Implement)**, **SWARM (multi-agent architecture)**, and **Your Claude Engineer** patterns, this document provides:

1. **Comparative strengths and limitations** of each methodology
2. **Integration opportunities** where methodologies complement each other
3. **Synthesis framework** for an optimal coding system
4. **Experimentation strategy** to iterate and improve
5. **Actionable next steps** for implementation

**Key Finding:** No single methodology is complete. The optimal system synthesizes:
- **RPI's documentation discipline** (research before planning)
- **PIV's validation rigor** (quality gates at every step)
- **SWARM's task architecture** (agent-ready from day 1)
- **Your Claude Engineer's cost optimization** (model-per-role)
- **HumanLayer's context engineering** (strategic token management)

---

## Methodology Comparison Matrix

| Dimension | PIV (Current) | RPI (HumanLayer) | SWARM (Future) | Your Claude Engineer |
|-----------|---------------|------------------|----------------|----------------------|
| **Phase Structure** | Prime → Implement → Validate | Research → Plan → Implement | Prime → Discuss → Plan → Execute → Validate | Orchestrator-driven state machine |
| **Documentation Philosophy** | Plan-first | Research-first, document-only agents | Task-first | External state (Linear) |
| **Quality Gates** | Suggested at end | Enforced at plan stage | Enforced per-task | Enforced by orchestrator |
| **Session Management** | Multi-session capable | Multi-session native | Multi-session ready | Multi-session via remote state |
| **Agent Architecture** | Single agent + skills | Specialized sub-agents (parallel) | Multi-agent ready | Multi-agent orchestrator |
| **Context Strategy** | Load everything upfront | Layered: minimal → expand | Task-specific context | Model-per-role optimization |
| **Token Optimization** | Single model (Sonnet) | Model-per-agent (Haiku/Sonnet) | Task-level model selection | Multi-model optimization (15-40% savings) |
| **State Persistence** | Local YAML files | External (Linear) + local thoughts/ | Local task files + registry | Remote (Linear) + checkpoint |
| **Resumption** | File-based, manual | Pull-based, query remote | State-based, automatic | Pull-based, external source |
| **Collaboration** | Single-user only | Multi-user (Linear shared) | Agent collaboration | Multi-user native |
| **Validation** | Manual run | Plan-stage review | Per-task gates | Mandatory screenshot validation |
| **Timeline Awareness** | ❌ Makes estimates | ❌ Phases with time | ✅ Priority-based (no time) | ✅ State-driven (no predictions) |
| **Complexity** | Low (simple) | Medium (orchestration) | High (multi-agent) | High (5 agents + Linear) |
| **Offline Capable** | ✅ Fully offline | ⚠️ Needs network for resumption | ✅ Fully offline | ❌ Requires Linear API |
| **Vendor Lock-in** | ✅ None | ⚠️ Linear-dependent | ✅ None | ❌ Linear-dependent |

---

## Methodology Deep Dive

### 1. PIV (Prime → Implement → Validate)

**Your Current System**

#### Strengths ✅

1. **Simplicity** - Single agent, easy to understand
2. **Comprehensive validation** - Multi-stage quality gates (static analysis, tests, coverage, security)
3. **Offline-first** - No external dependencies
4. **Vendor-agnostic** - Works with any Claude provider
5. **Rich reference docs** - Extensive `.claude/reference/` library
6. **Skills-based modularity** - Reusable, composable skills
7. **Feedback loops** - Execution reports improve future plans

#### Limitations ❌

1. **No research phase** - Jumps straight to planning without systematic discovery
2. **Quality gates optional** - Can be skipped, not enforced
3. **Single-model only** - No cost optimization via model mixing
4. **Context loaded upfront** - `/prime` loads everything (45K tokens)
5. **Token tracking broken** - Multi-session tracking accumulates incorrectly
6. **No session summaries** - Resume lacks rich context from previous sessions
7. **Timeline predictions** - Makes duration estimates instead of priorities

#### Best Use Cases 🎯

- Small to medium features (<5 files changed)
- Well-understood domains (familiar codebase areas)
- Single-developer projects
- Offline development environments
- When cost optimization is not critical

---

### 2. RPI (Research → Plan → Implement)

**HumanLayer's Production System**

#### Strengths ✅

1. **Research-first discipline** - Systematic discovery before planning
2. **Documentation-only agents** - No premature recommendations, just facts
3. **Plan-stage review** - Catch issues BEFORE implementation (faster than PR review)
4. **Specialized sub-agents** - Parallel research (locator, analyzer, pattern-finder, thoughts-locator)
5. **Model optimization** - Haiku for research/coordination, Sonnet for implementation (15-40% cost savings)
6. **External state** - Linear as source of truth (collaboration, corruption-proof)
7. **Session preservation** - META comments track decisions, blockers, context
8. **Thoughts system** - Separate repo for knowledge management across projects
9. **Resume validation** - Always verify codebase state matches handoff state
10. **No timeline predictions** - Priority-driven, not time-driven

#### Limitations ❌

1. **Network dependency** - Requires Linear API for resumption
2. **Vendor lock-in** - Tightly coupled to Linear
3. **Complexity** - Multi-agent orchestration adds cognitive overhead
4. **Setup cost** - Requires Linear project, API keys, configuration
5. **Slower iteration** - External API calls on every state query
6. **Keyboard-first UX** - Optimized for power users, steeper learning curve

#### Best Use Cases 🎯

- Large codebases (100K+ lines)
- Unfamiliar domains (new languages, frameworks)
- Multi-developer teams (Linear shared state)
- Long-running features (weeks/months)
- When cost optimization is critical
- Production systems with high collaboration needs

---

### 3. SWARM (Multi-Agent Architecture)

**Your Future-Ready Prototype**

#### Strengths ✅

1. **Agent-ready from day 1** - Same interface works in single or multi-agent mode
2. **Task-centric design** - Everything is a task with explicit ownership
3. **Message passing** - Communication patterns ready for swarm
4. **State persistence** - Agent registry, task queue, message log
5. **Gradual transition** - Single agent today, parallel agents tomorrow
6. **Clear ownership** - Tasks explicitly owned by agents
7. **Verification criteria** - Every task has `verify` and `done` fields
8. **Role specialization** - Researcher, Executor, Reviewer, Debugger agents

#### Limitations ❌

1. **Not production-ready** - Prototype phase, untested
2. **No actual swarm** - TeammateTool integration pending
3. **Added complexity** - More files, more state to manage
4. **Uncertain benefits** - Swarm mode may not justify complexity
5. **Learning curve** - New concepts (task ownership, message passing)
6. **Overhead** - Extra state files even in single-agent mode

#### Best Use Cases 🎯

- Highly parallelizable work (multiple independent tasks)
- Large features (10+ tasks)
- When team wants to test swarm mode
- Projects with clear task breakdown
- When preparing for future swarm capabilities

---

### 4. Your Claude Engineer

**Cole Medin's Multi-Agent Production System**

#### Strengths ✅

1. **Orchestrator pattern** - Haiku routes work, Sonnet implements (15% cost savings)
2. **External state (Linear)** - Pull-based resumption, corruption-proof
3. **Deterministic gates** - Can't skip verification, screenshot validation
4. **Model-per-role** - Optimal model for each agent type
5. **Session-agnostic** - Any conversation can resume any project
6. **Multi-user native** - Linear shared state enables collaboration
7. **Explicit completion** - Query done count vs. total issues

#### Limitations ❌

1. **Linear lock-in** - Completely dependent on Linear API
2. **Network dependency** - Can't work offline
3. **High complexity** - 5 agents (Orchestrator, Coding, Linear, GitHub, Slack)
4. **Runtime requirement** - Needs Claude Agent SDK (Python) running
5. **Less flexible** - Rigid state machine workflow
6. **API costs** - Linear API calls on every operation

#### Best Use Cases 🎯

- Teams already using Linear
- Production systems needing collaboration
- When cost optimization is critical
- Long-running autonomous agent workflows
- Multi-repository projects

---

## Integration Opportunities

### High-Value Adoptions (Implement First)

#### 1. RPI Research Phase ⭐⭐⭐⭐⭐

**What to adopt:**
- Add `/research` skill BEFORE `/plan`
- Specialized research agents (codebase-locator, analyzer, pattern-finder)
- Documentation-only constraint (no recommendations until asked)
- Save research to `.agents/research/`

**Integration with PIV:**
```
OLD: /prime → /plan-feature → /implement-plan → /validate
NEW: /prime → /research → /plan-feature → /implement-plan → /validate
```

**Benefits:**
- Better plans (based on facts, not assumptions)
- Fewer rework cycles (discovered issues upfront)
- Reusable research (saved for future reference)
- Parallel research (faster discovery)

**Effort:** Medium (2-3 days to implement)

---

#### 2. Model-per-Skill Optimization ⭐⭐⭐⭐⭐

**What to adopt:**
- Assign model (Haiku/Sonnet) per skill based on complexity
- Track per-model token usage
- Measure actual cost savings

**Model Assignment:**
```yaml
# .claude/config/skill-models.yaml
skills:
  prime:        haiku   # Context gathering (lightweight)
  research:     haiku   # Documentation only (lightweight)
  discuss:      haiku   # Design decisions (lightweight)
  plan:         haiku   # Task breakdown (lightweight)
  implement:    sonnet  # Heavy lifting (complex)
  validate:     haiku   # Quality checks (lightweight)
  code-review:  sonnet  # Deep analysis (complex)
  rca:          sonnet  # Root cause analysis (complex)
```

**Expected Savings:** 30-40% cost reduction

**Effort:** High (requires multi-model support, 5-7 days)

---

#### 3. Plan-Stage Review Gates ⭐⭐⭐⭐

**What to adopt:**
- Review and alignment at PLAN stage (not PR stage)
- Mandatory approval before implementation
- Catch issues early (design flaws, missed edge cases)

**Integration:**
```
/plan-feature → Generate plan → USER REVIEWS PLAN → /implement-plan
                                       ↓
                          (Iterate on plan until approved)
```

**Benefits:**
- Faster iteration (fix plan, not code)
- Less rework (alignment before implementation)
- Better plans (user feedback incorporated)

**Effort:** Low (1 day to add approval step)

---

#### 4. Session Context Preservation ⭐⭐⭐⭐

**What to adopt:**
- Session history with summaries
- Decisions tracking (why we did things)
- Blockers tracking (what needs attention)

**Schema:**
```yaml
# .agents/state/session.yaml
session_history:
  - session: 1
    started: "2026-02-02T10:00:00Z"
    ended: "2026-02-02T15:30:00Z"
    tokens_used: 35000
    tasks_completed: [task-001, task-002]
    summary: |
      Implemented authentication system. Added JWT middleware,
      login endpoint, and refresh token rotation. All tests passing.
    decisions:
      - "Use JWT instead of sessions for stateless API"
      - "Refresh tokens rotate on use for security"
    blockers: null
```

**Benefits:**
- Rich context on resume (not just task IDs)
- Preserved decisions (why we chose approach)
- Tracked blockers (what needs attention)

**Effort:** Medium (2-3 days)

---

#### 5. Deterministic Quality Gates ⭐⭐⭐⭐

**What to adopt:**
- Mandatory gates (can't skip validation)
- Pre-implementation verification (baseline tests pass)
- Post-implementation verification (new tests pass)
- Completion verification (full validation)

**Task Schema:**
```yaml
# task-001.yaml
validation:
  gates:
    - type: pre_implementation
      required: true
      commands: ["uv run pytest tests/unit/ -v"]
      failure_action: block

    - type: post_implementation
      required: true
      commands: ["uv run pytest tests/unit/ -v"]
      failure_action: block

    - type: completion
      required: true
      skills: ["validate"]
      failure_action: block
```

**Benefits:**
- Quality enforced (not suggested)
- No regressions (baseline tests required)
- Clear pass/fail (no ambiguity)

**Effort:** Medium (3-4 days)

---

### Medium-Value Adoptions (Consider)

#### 6. External State Backend (Optional) ⭐⭐⭐

**What to adopt:**
- Abstraction layer (StateBackend interface)
- Local implementation (current YAML)
- Linear implementation (optional)
- User chooses via config

**Benefits:**
- Corruption-proof (remote state)
- Collaboration (shared state)
- Flexibility (choose backend)

**Drawbacks:**
- High complexity (abstraction layer)
- Network dependency (Linear option)
- Maintenance burden (multiple backends)

**Decision:** Defer to later (Priority 3)

**Effort:** Very High (1-2 weeks)

---

#### 7. SWARM Task Architecture ⭐⭐⭐

**What to adopt:**
- Task-centric design (everything is a task)
- Agent registry (track ownership)
- Message passing (communication log)

**Benefits:**
- Swarm-ready (future-proof)
- Clear ownership (task → agent)
- Debugging (message log)

**Drawbacks:**
- Added complexity (more state files)
- Uncertain ROI (swarm not available)
- Learning curve (new patterns)

**Decision:** Monitor swarm availability, implement when concrete

**Effort:** High (1 week)

---

### Low-Value Adoptions (Don't Adopt)

#### 8. Linear Integration ⭐

**Why not:**
- Adds vendor lock-in
- Network dependency
- High maintenance cost
- Current local state works fine

**Alternative:** Keep local state, optionally sync to Linear if user wants

---

#### 9. Multi-Agent Orchestration ⭐

**Why not:**
- High complexity (5+ agents)
- Runtime dependency (Claude SDK)
- Current single-agent + skills works well
- Diminishing returns for single-developer use case

**Alternative:** Use SWARM architecture when TeammateTool available

---

## Synthesis Framework: The Optimal System

### Proposed Methodology: **RPIV (Research → Plan → Implement → Validate)**

Combines best elements of all methodologies:

```
┌─────────────────────────────────────────────────────────────────┐
│                    RPIV Methodology Flow                         │
└─────────────────────────────────────────────────────────────────┘

PHASE 1: RESEARCH (NEW)
├─ /prime (Haiku) - Minimal context (8K tokens)
├─ /research (Haiku) - Parallel discovery
│  ├─ Codebase-locator agent (find files/patterns)
│  ├─ Codebase-analyzer agent (understand implementation)
│  ├─ Pattern-finder agent (identify conventions)
│  └─ Save to .agents/research/
└─ Output: Research document (facts only, no recommendations)

PHASE 2: PLAN (ENHANCED)
├─ /discuss (Haiku) - Capture user preferences
├─ /plan-feature (Haiku) - Generate plan with token estimates
├─ USER REVIEWS PLAN ← NEW: Mandatory approval
└─ Output: Approved plan (.agents/plans/)

PHASE 3: IMPLEMENT (ENHANCED)
├─ Pre-implementation gate ← NEW: Baseline tests must pass
├─ /implement-plan (Sonnet) - Execute with TDD
│  ├─ Red-Green-Refactor per task
│  ├─ Validation after EVERY task
│  ├─ Checkpoint at 88% tokens ← NEW: Automatic
│  └─ Session summary on pause ← NEW: Capture decisions
└─ Output: Working code, tests passing, checkpoints saved

PHASE 4: VALIDATE (ENHANCED)
├─ Post-implementation gates ← NEW: Mandatory
├─ /validate (Haiku) - Multi-stage quality gates
├─ /code-review (Sonnet) - Deep analysis
└─ Output: Quality report, ready for PR

FEEDBACK LOOP:
└─ /execution-report - Improve future iterations
```

---

### Key Principles

1. **Research Before Planning** - No assumptions, gather facts first
2. **Plan-Stage Review** - Catch issues before implementation
3. **Quality Gates Enforced** - Can't skip validation
4. **Model Optimization** - Haiku for lightweight, Sonnet for complex
5. **Session Discipline** - Checkpoints, summaries, decisions tracked
6. **Priority-Driven** - No timeline predictions, user decides urgency
7. **Offline-First** - No external dependencies required
8. **Swarm-Ready** - Task architecture supports future agents
9. **Fail Fast** - Validate after every task, not at end

---

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      USER (Product Owner)                     │
│               Approves plans, sets priorities                 │
└─────────────────────────┬────────────────────────────────────┘
                          │
┌─────────────────────────▼────────────────────────────────────┐
│                  ORCHESTRATOR (You)                          │
│           Runs skills, tracks state, enforces gates           │
└─────────────────────────┬────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ RESEARCH      │  │ PLANNING      │  │ IMPLEMENTATION│
│ (Haiku)       │  │ (Haiku)       │  │ (Sonnet)      │
│               │  │               │  │               │
│ Parallel      │  │ Token         │  │ TDD           │
│ agents        │  │ estimation    │  │ Incremental   │
│               │  │               │  │ validation    │
└───────────────┘  └───────────────┘  └───────────────┘

STATE PERSISTENCE (Local YAML):
├─ .agents/state/session.yaml (session history, decisions, blockers)
├─ .agents/tasks/*.yaml (task definitions with gates)
├─ .agents/research/ (discovery artifacts)
├─ .agents/plans/ (approved plans)
└─ .agents/execution-reports/ (feedback loop)
```

---

## Experimentation & Iteration Strategy

### Phase 1: Foundation (Week 1-2)

**Goal:** Implement high-value adoptions without breaking current system

**Tasks:**
1. Add `/research` skill (Haiku model)
   - Implement codebase-locator pattern
   - Implement codebase-analyzer pattern
   - Save research to `.agents/research/`

2. Add model-per-skill configuration
   - Create `skill-models.yaml` config
   - Update skill executor to respect model setting
   - Track per-model token usage

3. Add plan-stage review gate
   - Modify `/plan-feature` to require approval
   - Display plan and wait for user confirmation
   - Allow iteration until approved

4. Fix token tracking
   - Separate `current_session_tokens` vs. `feature_total_tokens`
   - Add `session_history` array
   - Reset session tokens on resume

**Success Criteria:**
- [ ] `/research` skill works and produces useful artifacts
- [ ] Model-per-skill reduces cost by 20%+ on test feature
- [ ] Plan approval gate catches at least 1 issue before implementation
- [ ] Token tracking correct across 3+ sessions

**Measurement:**
- Cost per feature (before/after model optimization)
- Plan iteration count (how many times plan revised)
- Issues caught at plan stage vs. PR stage

---

### Phase 2: Quality Gates (Week 3-4)

**Goal:** Enforce quality, prevent regressions

**Tasks:**
1. Add deterministic quality gates
   - Extend task YAML schema with `gates` section
   - Implement pre/post/completion gates
   - Block progression on failures

2. Add session context preservation
   - Extend `session.yaml` with summary/decisions/blockers
   - Update `/pause` skill to prompt for summary
   - Update `/resume-session` to display last session

3. Add automatic checkpointing
   - Monitor token usage during implementation
   - Trigger checkpoint at 88% threshold
   - Save progress and display resume instructions

**Success Criteria:**
- [ ] Gates enforce quality (can't skip)
- [ ] Zero regressions in 5 test features
- [ ] Session summaries improve resume experience
- [ ] Automatic checkpoints prevent token exhaustion

**Measurement:**
- Regression count (before/after gates)
- Resume context quality (user feedback)
- Token exhaustion incidents (before/after checkpoints)

---

### Phase 3: Validation & Refinement (Week 5-8)

**Goal:** Test on real features, measure improvements

**Tasks:**
1. Run RPIV on 5 diverse features:
   - Small bugfix (1-2 files)
   - Medium feature (3-5 files)
   - Large feature (10+ files)
   - Refactoring task
   - Performance optimization

2. Collect metrics:
   - Cost per feature
   - Plan iteration count
   - Issues caught at plan stage
   - Rework rate (code changed after review)
   - Token accuracy (estimated vs. actual)
   - Time to first issue caught

3. Iterate based on findings:
   - Adjust model assignments if needed
   - Refine research patterns
   - Improve gate definitions
   - Optimize checkpoint thresholds

**Success Criteria:**
- [ ] 30%+ cost reduction (model optimization)
- [ ] 50%+ reduction in PR rework (plan-stage review)
- [ ] 90%+ token estimate accuracy
- [ ] Zero token exhaustion incidents
- [ ] User satisfaction (qualitative feedback)

**Measurement:**
- Before/after comparison across all metrics
- Feature complexity vs. cost/time correlation
- User feedback surveys

---

### Phase 4: Documentation & Rollout (Week 9-10)

**Goal:** Document RPIV, train team, prepare for wider adoption

**Tasks:**
1. Create comprehensive RPIV documentation
   - Update CLAUDE.md with RPIV workflow
   - Create RPIV quick-start guide
   - Document common patterns and anti-patterns
   - Record video walkthroughs

2. Create skill templates
   - Research skill templates (5+ common patterns)
   - Plan templates (API, data processing, UI, refactor)
   - Task templates (with gates)

3. Prepare for team rollout
   - Conduct training sessions
   - Create onboarding checklist
   - Set up feedback channels
   - Monitor adoption metrics

**Success Criteria:**
- [ ] Documentation complete and reviewed
- [ ] 3+ team members successfully use RPIV
- [ ] Templates cover 80%+ of common use cases
- [ ] Positive feedback from early adopters

---

### Phase 5: Advanced Features (Month 3+)

**Goal:** Explore advanced optimizations

**Potential enhancements:**
1. **Prompt caching** (70%+ latency reduction)
2. **Conversation compaction** (50%+ token reduction)
3. **SWARM integration** (when TeammateTool available)
4. **Cross-project pattern library**
5. **Feedback loop analytics** (auto-improving system)
6. **Developer onboarding system**

**Decision point:** Prioritize based on Phase 3 learnings

---

## Measurement Framework

### Primary Metrics

**Cost Efficiency:**
- Cost per feature (before/after RPIV)
- Token usage per phase
- Model mix (% Haiku vs. Sonnet)

**Quality:**
- Issues caught at plan stage vs. PR stage
- Regression count
- Test coverage
- Code review scores

**Efficiency:**
- Plan iteration count (fewer = better plan-stage review)
- Rework rate (% code changed after review)
- Token estimate accuracy
- Time to first issue caught

**Developer Experience:**
- User satisfaction (surveys)
- Onboarding time (time to first feature)
- Context switch pain (qualitative)
- Confidence in AI recommendations

### Secondary Metrics

**Process Adoption:**
- RPIV usage rate (% features using RPIV)
- Skill usage frequency
- Documentation coverage

**Knowledge Management:**
- Research artifacts created
- Pattern library size
- Cross-reference usage

**Session Management:**
- Checkpoint frequency
- Resume success rate
- Session summary quality

---

## Decision Framework

### When to Use Which Methodology

**Use RPIV (Proposed) for:**
- ✅ Most features (default choice)
- ✅ Unfamiliar domains (research phase helps)
- ✅ Medium to large features (benefits from research)
- ✅ When cost optimization matters

**Use PIV (Current) for:**
- ✅ Very small fixes (<5 min work)
- ✅ Emergency hotfixes (skip research)
- ✅ Well-understood trivial changes

**Consider SWARM for:**
- ⚠️ Highly parallelizable work (when TeammateTool available)
- ⚠️ Very large features (10+ independent tasks)
- ⚠️ Experimental projects (testing swarm mode)

**Don't use multi-agent orchestration:**
- ❌ Single-developer projects (unnecessary complexity)
- ❌ Small to medium features (overhead not justified)
- ❌ When offline capability required

---

## Risks & Mitigations

### Risk 1: Increased Complexity

**Risk:** RPIV adds research phase, gates, model selection → higher cognitive load

**Mitigation:**
- Create clear quickstart guide
- Provide templates for common patterns
- Make research optional for small features
- Gradual rollout (train team incrementally)

---

### Risk 2: Model Optimization May Not Deliver Savings

**Risk:** Multi-model support is complex, savings may not justify effort

**Mitigation:**
- Measure before committing (run cost analysis on 5 features)
- Start with simple model assignment (Haiku for all but implement/review)
- Track actual savings vs. estimated
- Abort if savings <15%

---

### Risk 3: Plan-Stage Review Slows Velocity

**Risk:** Mandatory approval adds friction, slows iteration

**Mitigation:**
- Make review async (user can review later if busy)
- Provide "quick approve" for trusted patterns
- Time-box review (if no response in X hours, auto-approve)
- Measure: does plan-stage review reduce PR rework?

---

### Risk 4: Session Context May Become Bloated

**Risk:** Summaries, decisions, blockers → large session files

**Mitigation:**
- Prompt for concise summaries (3-5 sentences)
- Archive old sessions after completion
- Implement session compaction after N sessions
- Monitor session file sizes

---

### Risk 5: RPIV May Not Fit All Use Cases

**Risk:** One-size-fits-all methodology may not work

**Mitigation:**
- Support multiple workflows (RPIV, PIV, quick-fix)
- Allow users to customize (skip research if desired)
- Collect feedback and iterate
- Document "when to use which" decision tree

---

## Actionable Next Steps

### Immediate (This Week)

1. **Decision:** Approve RPIV framework and experimentation plan
2. **Prototype:** Implement `/research` skill (Haiku)
3. **Prototype:** Add model-per-skill configuration
4. **Test:** Run RPIV on 1 small feature to validate

### Short-Term (Next 2 Weeks)

1. **Implement:** Phase 1 tasks (research skill, model optimization, plan approval, token tracking fix)
2. **Measure:** Cost savings, plan iteration count, token tracking correctness
3. **Iterate:** Adjust based on findings
4. **Document:** Create RPIV quickstart guide

### Medium-Term (Next Month)

1. **Implement:** Phase 2 tasks (quality gates, session context, checkpoints)
2. **Validate:** Test RPIV on 5 diverse features
3. **Measure:** All primary metrics
4. **Refine:** Adjust thresholds, patterns, templates

### Long-Term (Quarter 1)

1. **Document:** Complete RPIV documentation
2. **Train:** Onboard team to RPIV
3. **Monitor:** Adoption metrics and feedback
4. **Decide:** Advanced features (caching, compaction, SWARM)

---

## Open Questions

### For Discussion

1. **Model optimization priority:** Implement Phase 1 (research skill) first, or model optimization first?
   - Recommendation: Research skill first (validates RPIV flow)

2. **Plan approval UX:** Synchronous (block until user approves) or asynchronous (user reviews later)?
   - Recommendation: Synchronous with timeout (auto-approve after 24h)

3. **SWARM investment:** Commit to SWARM architecture now, or wait for TeammateTool release?
   - Recommendation: Wait for concrete swarm availability

4. **External state:** Invest in Linear integration for collaboration, or stay local-only?
   - Recommendation: Stay local, optionally sync to Linear if user wants

5. **Timeline policy:** Strictly enforce "no timeline predictions" across all docs/skills?
   - Recommendation: Yes, use priority levels instead

6. **Validation rigor:** Mandatory gates for all features, or optional for small fixes?
   - Recommendation: Mandatory for medium/large, optional for trivial fixes

---

## Conclusion

**Optimal system is a synthesis, not adoption of one methodology.**

**Key synthesis:**
- **RPI's research discipline** → Add `/research` phase
- **RPI's plan-stage review** → Approve plans before implementation
- **Your Claude Engineer's cost optimization** → Model-per-skill
- **Your Claude Engineer's deterministic gates** → Enforce quality
- **PIV's simplicity** → Keep single-agent + skills
- **PIV's offline-first** → No external dependencies required
- **SWARM's architecture** → Prepare for future, don't over-invest now

**Next step:** Approve experimentation plan and begin Phase 1 prototyping.

---

**Document Status:** Draft for review
**Decision Required:** Approve RPIV framework and experimentation plan
**Owner:** Product team
**Timeline:** Review by 2026-02-03, begin Phase 1 implementation 2026-02-04
