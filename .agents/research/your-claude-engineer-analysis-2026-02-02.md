# Your Claude Engineer Analysis

**Project:** https://github.com/coleam00/your-claude-engineer
**Author:** Cole Medin (coleam00)
**License:** MIT
**Date Analyzed:** 2026-02-02

---

## Executive Summary

**Your Claude Engineer** is a multi-agent orchestration system using the Claude Agent SDK to build full-stack applications autonomously. It demonstrates production-grade patterns for:

1. **Multi-agent coordination** with specialized roles
2. **External state management** (Linear as source of truth)
3. **Model-per-role cost optimization** (Haiku for orchestration, Sonnet for coding)
4. **Pull-based resumption** (query remote state vs. replay local logs)
5. **Quality gates** enforced before task progression

**Key Differentiation from py-ai-starter-kit:**
- **External state** (Linear) vs. **Local state** (YAML files)
- **Multi-agent orchestrator** vs. **Single-agent with skills**
- **Runtime system** (Python SDK) vs. **Methodology system** (Claude Code skills)

---

## Architecture Overview

### Core Components

```
┌─────────────────────────────────────────────────────┐
│            Orchestrator Agent (Haiku)               │
│  • Reads .linear_project.json (checkpoint)          │
│  • Queries Linear for current state                 │
│  • Routes work to specialized agents                │
│  • Enforces quality gates                           │
└──────────────────┬──────────────────────────────────┘
                   │
       ┌───────────┴───────────┐
       │                       │
   ┌───▼────┐           ┌──────▼──────┐
   │ Linear │           │   Coding    │
   │ Agent  │           │   Agent     │
   │(Haiku) │           │  (Sonnet)   │
   └───┬────┘           └──────┬──────┘
       │                       │
   ┌───▼────┐           ┌──────▼──────┐
   │ GitHub │           │    Slack    │
   │ Agent  │           │    Agent    │
   │(Haiku) │           │   (Haiku)   │
   └────────┘           └─────────────┘
```

### Agent Responsibilities

| Agent | Model | Role |
|-------|-------|------|
| **Orchestrator** | Haiku | Routing, decision-making, quality gates |
| **Coding** | Sonnet | Feature implementation, testing, debugging |
| **Linear** | Haiku | Issue management, status updates |
| **GitHub** | Haiku | Repository operations, PR creation |
| **Slack** | Haiku | Notifications, team updates |

**Key Pattern:** Lightweight model (Haiku) for orchestration, powerful model (Sonnet) only when needed.

---

## State Management Strategy

### Their Approach: External Source of Truth

**`.linear_project.json` (Checkpoint File):**
```json
{
  "team_id": "team_abc123",
  "project_id": "project_xyz789",
  "meta_issue_id": "issue_meta_456"
}
```

**How Resumption Works:**

1. **Session Start:** Read `.linear_project.json` from project directory
2. **Context Fetch:** Query Linear API for:
   - All issues in project (status, descriptions)
   - META issue comments (session history)
   - Next task to work on
3. **Decision:** Orchestrator decides what to do based on remote state
4. **Execution:** Delegate to specialized agent
5. **Update:** Agent writes results back to Linear
6. **Loop:** Repeat until project complete

**Benefits:**
- No local state corruption
- Multi-user collaboration possible (Linear is shared)
- Session resumption survives network failures, agent crashes
- Audit trail in Linear issue comments

**Drawbacks:**
- Requires Linear account and API access
- Network dependency for every operation
- Slower than local file reads
- Vendor lock-in (Linear-specific)

### Our Approach: Local YAML State

**`.agents/state/session.yaml` (Current):**
```yaml
session:
  feature: py-ai-starter-kit
  status: paused
  tokens_used: 93000  # ← Problem: accumulates incorrectly

tasks:
  completed: [task-001, task-002]
  pending: [task-003, task-004, task-005, task-006]
```

**How Resumption Works:**

1. **Session Start:** Read `session.yaml` from `.agents/state/`
2. **Context Load:** All state in local files
3. **Decision:** Single agent decides what to do
4. **Execution:** Agent executes via Claude Code skills
5. **Update:** Write results to `session.yaml` and task YAML files
6. **Loop:** Repeat until feature complete

**Benefits:**
- No external dependencies
- Fast (local file I/O)
- Works offline
- User owns all data

**Drawbacks:**
- State corruption possible (file edits, merge conflicts)
- Single-user only (no collaboration)
- Resumption requires careful state management
- No built-in audit trail

---

## Token Budget & Context Management

### Their Approach: Model-per-Role Optimization

**Cost Reduction Strategy:**

```python
# agents/definitions.py (conceptual)
agents = {
    "orchestrator": {
        "model": "haiku",        # $0.25 per 1M input tokens
        "role": "decision-making"
    },
    "coding": {
        "model": "sonnet",       # $3 per 1M input tokens
        "role": "implementation"
    },
    "linear": {
        "model": "haiku",        # $0.25 per 1M input tokens
        "role": "status updates"
    }
}
```

**Token Usage Pattern:**

```
Orchestrator (Haiku): ~5K tokens/decision
  ├─> Coding Agent (Sonnet): ~50K tokens/feature
  ├─> Linear Agent (Haiku): ~2K tokens/update
  └─> GitHub Agent (Haiku): ~3K tokens/commit

Total: ~60K tokens, but only 50K on expensive model
Cost: (10K × $0.25/1M) + (50K × $3/1M) = $0.0025 + $0.15 = $0.1525
```

**vs. Single Agent (Sonnet only):**
```
Single Agent (Sonnet): ~60K tokens
Cost: 60K × $3/1M = $0.18
```

**Savings:** ~15% cost reduction through model mixing.

**Context Management:**

- **Orchestrator:** Minimal context (project state, next task)
- **Coding Agent:** Full context (spec, patterns, prior work)
- **Support Agents:** Task-specific context only

Each agent gets a **fresh context window** on invocation. No compaction needed.

### Our Approach: Single Agent with Skills

**Current Model:**

```
Claude Code (Sonnet): ~150K tokens/session
  ├─> /prime skill: ~45K tokens
  ├─> /plan skill: ~30K tokens
  ├─> /implement-plan: ~65K tokens
  └─> /validate: ~10K tokens

Total: ~150K tokens, all on Sonnet
Cost: 150K × $3/1M = $0.45
```

**Context Accumulation:**

- All skills run in **same conversation**
- Context **accumulates** across skills
- Approaches 200K limit on large features
- Compaction required for multi-session work

**Potential Optimization:**

Could adopt their pattern:

```python
# Use Haiku for planning, Sonnet for implementation
skills = {
    "/prime": "haiku",       # Context gathering (lightweight)
    "/discuss": "haiku",     # Design decisions
    "/plan": "haiku",        # Task breakdown
    "/implement-plan": "sonnet",  # Heavy lifting
    "/validate": "haiku",    # Quality checks
    "/code-review": "sonnet" # Deep analysis
}
```

**Estimated Savings:** 30-40% cost reduction on typical feature.

---

## Workflow Patterns

### Their Workflow: Orchestrator-Driven State Machine

**Mandatory Serial Flow:**

```
1. Verification Gate
   ├─> Run regression tests (Coding Agent)
   ├─> PASS → Continue
   └─> FAIL → Fix, re-test, block new work

2. Feature Implementation
   ├─> Coding Agent implements next Linear issue
   ├─> Write tests (TDD)
   ├─> Implement code
   └─> Validate locally

3. Commit & Push
   ├─> GitHub Agent creates commit
   ├─> Push to remote
   └─> Update Linear issue status

4. Screenshot Validation
   ├─> Playwright MCP captures UI
   ├─> Verify feature works visually
   └─> Attach to Linear issue

5. Mark Done
   ├─> Update Linear issue → Done
   ├─> Add META comment (session log)
   └─> Slack notification

6. Check Completion
   ├─> Query Linear: done count vs. total
   ├─> Complete → End
   └─> Remaining → Loop to step 1
```

**Key Characteristics:**

- **Quality gates enforced** by orchestrator (can't skip verification)
- **External state updates** after each step (Linear, GitHub)
- **Visual validation** required (screenshots)
- **Explicit completion signal** (done count = total issues)

### Our Workflow: Skill-Driven PIV Loop

**Flexible User-Directed Flow:**

```
1. /prime
   └─> Establish context (~45K tokens)

2. /discuss (optional)
   └─> Make design decisions

3. /spec
   └─> Generate Anthropic XML specification

4. /plan
   └─> Create task-NNN.yaml files

5. /execute
   ├─> For each task:
   │   ├─> Read task file
   │   ├─> Implement (TDD)
   │   ├─> Run validation commands
   │   ├─> Run validation skills
   │   ├─> Commit if passing
   │   └─> Update task status
   └─> Loop until token budget or completion

6. /validate
   └─> Final quality gates

7. /commit
   └─> Semantic commit message
```

**Key Characteristics:**

- **User-driven progression** (user chooses when to run each skill)
- **Local state only** (YAML files)
- **Flexible quality gates** (can skip if needed)
- **Single conversation context** (accumulates tokens)

---

## Resumption Mechanisms

### Their Approach: Pull-Based Resumption

**How It Works:**

```python
# Simplified conceptual flow
def resume_session(project_dir):
    # 1. Read checkpoint file
    checkpoint = read_json(f"{project_dir}/.linear_project.json")

    # 2. Query remote state
    linear_client = LinearClient(api_key)
    issues = linear_client.get_issues(checkpoint["project_id"])
    meta_comment = linear_client.get_latest_comment(checkpoint["meta_issue_id"])

    # 3. Determine next action
    completed = [i for i in issues if i.status == "Done"]
    next_task = [i for i in issues if i.status == "Todo"][0]

    # 4. Provide context to orchestrator
    orchestrator_prompt = f"""
    Project: {checkpoint['project_id']}
    Progress: {len(completed)}/{len(issues)} done
    Last session: {meta_comment}
    Next task: {next_task.title}
    """

    # 5. Continue from next task
    orchestrator.run(orchestrator_prompt)
```

**Benefits:**
- **Always fresh state** (no stale local data)
- **Session-agnostic** (any conversation can resume any project)
- **Multi-session native** (designed for this from day 1)

**Drawbacks:**
- **Network dependency** (can't resume offline)
- **API rate limits** (Linear API calls on every resume)
- **Vendor lock-in** (Linear-specific implementation)

### Our Approach: File-Based Resumption

**How It Works (Current):**

```python
# Simplified conceptual flow
def resume_session():
    # 1. Read local state
    session = read_yaml(".agents/state/session.yaml")

    # 2. Load task files
    next_task_id = session["next_task"]
    next_task = read_yaml(f".agents/tasks/{next_task_id}.yaml")

    # 3. Provide context to agent
    resume_prompt = f"""
    Feature: {session['feature']}
    Completed: {session['tasks']['completed']}
    Next: {next_task_id} - {next_task['name']}
    """

    # 4. Continue from next task
    execute_skill(next_task)
```

**Benefits:**
- **Fast** (local file reads)
- **Offline-capable** (no network needed)
- **Vendor-agnostic** (works anywhere)

**Drawbacks:**
- **State corruption possible** (manual edits, merge conflicts)
- **Token tracking broken** (current bug we identified)
- **Single-user only** (no collaboration support)

---

## Key Learnings for py-ai-starter-kit

### 1. Multi-Model Cost Optimization (HIGH VALUE)

**What They Do:**
- Haiku for lightweight tasks (orchestration, status updates)
- Sonnet for heavy lifting (coding, deep analysis)
- **15-40% cost savings** depending on task mix

**How We Could Adopt:**

```yaml
# .claude/config/skill-models.yaml
skills:
  prime:
    model: haiku          # Context gathering (lightweight)
    estimated_tokens: 10000

  discuss:
    model: haiku          # Design decisions
    estimated_tokens: 8000

  plan:
    model: haiku          # Task breakdown
    estimated_tokens: 12000

  implement-plan:
    model: sonnet         # Implementation (heavy)
    estimated_tokens: 60000

  validate:
    model: haiku          # Quality checks
    estimated_tokens: 8000

  code-review:
    model: sonnet         # Deep analysis
    estimated_tokens: 15000
```

**Implementation Path:**
1. Add `model` parameter to skill YAML frontmatter
2. Update skill executor to respect model selection
3. Track tokens separately per model for cost analysis
4. Measure actual savings on real features

**Expected Impact:** 30-40% cost reduction on typical feature development.

### 2. External State as Source of Truth (MEDIUM VALUE)

**What They Do:**
- Linear issues are the **single source of truth**
- `.linear_project.json` is just a **pointer** (team ID, project ID)
- Resume by **querying remote state**, not reading local logs

**Benefits:**
- No state corruption
- Multi-user collaboration
- Survives local file deletion

**How We Could Adopt (Optional):**

```yaml
# .agents/config/state-backend.yaml
backend: linear  # or: local, github-issues, jira

linear:
  api_key: ${LINEAR_API_KEY}
  team_id: team_abc123
  project_prefix: "PIV-"

local:
  state_dir: .agents/state/
  backup_on_write: true
```

**Implementation Path:**
1. Create abstraction: `StateBackend` interface
2. Implement: `LocalStateBackend` (current YAML)
3. Implement: `LinearStateBackend` (optional)
4. Allow users to choose via config

**Priority:** Lower (local state works fine for single-user)

### 3. Deterministic State Machine Workflow (HIGH VALUE)

**What They Do:**
- **Mandatory gates:** Verification before implementation, screenshot before marking done
- **Serial progression:** Can't skip steps
- **Explicit completion signal:** Query remote for done count vs. total

**How We Could Adopt:**

```yaml
# task-003.yaml
validation:
  gates:
    - type: pre_implementation
      required: true
      commands:
        - uv run pytest tests/unit/ -v
      failure_action: block

    - type: post_implementation
      required: true
      skills:
        - validate
      failure_action: block

    - type: completion_verification
      required: true
      commands:
        - uv run pytest tests/integration/ -v
      failure_action: block
```

**Benefits:**
- **Quality enforced, not suggested**
- **Clear pass/fail criteria**
- **No skipping validation**

**Implementation Path:**
1. Extend task YAML schema with `gates` section
2. Update `/execute` skill to enforce gates
3. Block progression on gate failures
4. Track gate results in task files

**Expected Impact:** Higher quality, fewer regressions, clearer failure points.

### 4. Session Context Preservation (HIGH VALUE)

**What They Do:**
- META issue has **session comments** (what was done, decisions made)
- Each agent appends to audit trail
- Resumption reads last comment for context

**How We Could Adopt:**

```yaml
# .agents/state/session.yaml
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
    blockers: null

  - session: 2
    started: "2026-02-02T15:00:00Z"
    ended: "2026-02-02T18:18:30Z"
    tokens_used: 58000
    tasks_completed: [task-002]
    summary: |
      Implemented Spec creation process. Created /spec skill with
      Anthropic XML format. Added validation for required sections.
    decisions:
      - "Use XML format vs. markdown for better structure"
      - "Require acceptance_criteria section in all specs"
    blockers: null
```

**Benefits:**
- **Rich context on resume** (not just "task-002 done")
- **Decisions preserved** (why we did things)
- **Blockers tracked** (what needs attention)

**Implementation Path:**
1. Extend `session.yaml` with `session_history` array
2. Update `/pause` skill to prompt for summary
3. Update `/resume-session` to display last session summary
4. Track decisions and blockers explicitly

**Expected Impact:** Better context on resume, fewer "why did we do this?" moments.

### 5. Prompt-Driven Architecture (MEDIUM VALUE)

**What They Do:**
- Orchestration logic lives in **prompt files** (`.md`)
- Agent definitions in **YAML/Python config**
- Specifications as **data** (`.txt` files)

**Benefits:**
- Rapid iteration (change prompt, no code deploy)
- Versioned prompts (git diff shows changes)
- Clear separation: prompts (what to do) vs. code (infrastructure)

**How We Already Do This:**
- Skills defined in `SKILL.md` (prompt-driven ✓)
- Reference docs in `.claude/reference/` (data-driven ✓)
- Specs in `.agents/specs/` (data-driven ✓)

**We're already aligned here!**

### 6. Specialized Agent Delegation (LOW VALUE for us)

**What They Do:**
- Orchestrator delegates to specialized agents (Linear, Coding, GitHub, Slack)
- Each agent is a separate Claude instance

**Why Lower Value for Us:**
- Our model is **single agent with skills** (simpler)
- Claude Code skills already provide modularity
- Multi-agent orchestration adds complexity
- Their approach needs runtime system (Python SDK)

**Our Equivalent:**
- Skills = Specialized agents
- Single Claude instance = Lower token cost (no inter-agent context passing)
- Claude Code handles orchestration

**Decision:** Stick with single-agent + skills model. Simpler and works well.

---

## What to Adopt (Priority Order)

### Priority 1: Multi-Model Cost Optimization

**Impact:** 30-40% cost savings
**Effort:** Medium (add model selection to skills)
**Blockers:** None

**Action Items:**
1. Add `model` field to skill YAML frontmatter
2. Update skill executor to spawn correct model
3. Track per-model token usage
4. Measure savings on real features
5. Document in CLAUDE.md

### Priority 2: Fix Token Tracking (Already Identified)

**Impact:** Fixes user confusion, correct resumption
**Effort:** High (breaking change to session.yaml)
**Blockers:** None

**Action Items:**
1. Implement separate `current_session_tokens` vs. `feature_total_tokens`
2. Add `session_history` array
3. Create migration script for old sessions
4. Update `/execute` and `/resume-session` skills
5. Test multi-session workflow

### Priority 3: Deterministic Quality Gates

**Impact:** Higher quality, fewer regressions
**Effort:** Medium (extend task schema, update /execute)
**Blockers:** None

**Action Items:**
1. Add `gates` section to task YAML schema
2. Update `/execute` skill to enforce gates
3. Block task completion on gate failures
4. Track gate results in task files
5. Document gate patterns in reference docs

### Priority 4: Session Context Preservation

**Impact:** Better resumption context
**Effort:** Low (extend session.yaml, update /pause)
**Blockers:** Priority 2 (token tracking fix)

**Action Items:**
1. Extend `session.yaml` with `session_history.summary`
2. Update `/pause` skill to prompt for summary
3. Update `/resume-session` to display last summary
4. Add `decisions` and `blockers` tracking

### Priority 5: External State Backend (Optional)

**Impact:** Enables collaboration, prevents corruption
**Effort:** Very High (abstraction layer, Linear integration)
**Blockers:** None, but lower ROI

**Action Items:**
1. Create `StateBackend` interface
2. Implement `LocalStateBackend` (current)
3. Implement `LinearStateBackend` (optional)
4. Add configuration to choose backend
5. Document trade-offs

**Decision:** Defer to Priority 4 unless collaboration becomes critical need.

---

## Comparison Matrix

| Feature | Your Claude Engineer | py-ai-starter-kit | Winner |
|---------|---------------------|-------------------|--------|
| **Multi-Agent Coordination** | ✓ Orchestrator + Specialists | ✗ Single agent + skills | Tie (different models) |
| **Cost Optimization** | ✓ Model-per-role | ✗ Single model (Sonnet) | **Them** |
| **State Management** | ✓ External (Linear) | ✓ Local (YAML) | Tie (trade-offs) |
| **Resumption** | ✓ Pull-based (query remote) | ✓ File-based (read local) | Tie (trade-offs) |
| **Quality Gates** | ✓ Enforced by orchestrator | ~ Suggested by skills | **Them** |
| **Session History** | ✓ META comments | ✗ Minimal tracking | **Them** |
| **Collaboration** | ✓ Multi-user (Linear shared) | ✗ Single-user only | **Them** |
| **Offline Capability** | ✗ Requires Linear API | ✓ Fully offline | **Us** |
| **Simplicity** | ✗ Complex (5 agents) | ✓ Simple (1 agent) | **Us** |
| **Vendor Lock-in** | ✗ Linear-dependent | ✓ Vendor-agnostic | **Us** |
| **Documentation** | ✓ Comprehensive README | ✓ Extensive reference docs | Tie |
| **Testing Strategy** | ✓ Playwright visual validation | ✓ Three-tier pytest | Tie |

**Overall Assessment:**
- **Their strengths:** Cost optimization, collaboration, quality enforcement
- **Our strengths:** Simplicity, offline, vendor-agnostic, comprehensive methodology
- **Best path:** Adopt their cost optimization and quality gates, keep our single-agent model

---

## Recommended Implementation Plan

### Phase 1: Cost Optimization (Month 1)

**Goal:** 30-40% cost reduction on feature development

**Tasks:**
1. Add `model` field to skill YAML schema
2. Update Claude Code skill executor to spawn correct model
3. Assign models to skills:
   - Haiku: prime, discuss, plan, validate
   - Sonnet: implement-plan, code-review, rca
4. Track per-model token usage in session.yaml
5. Measure actual savings on 3 real features
6. Document findings and adjust model assignments

**Success Criteria:**
- [ ] All skills support model selection
- [ ] 30%+ cost reduction measured on real features
- [ ] No quality degradation (Haiku adequate for assigned tasks)

### Phase 2: Token Tracking Fix (Month 1)

**Goal:** Fix token budget confusion across sessions

**Tasks:**
1. Implement `current_session_tokens` vs. `feature_total_tokens` separation
2. Add `session_history` array to session.yaml
3. Update `/execute` skill to reset session tokens on resume
4. Update `/resume-session` to display correct budget
5. Create migration script for old session files
6. Test multi-session workflow (3+ sessions on one feature)

**Success Criteria:**
- [ ] Session 2+ shows "0 / 200K tokens" on start
- [ ] Feature total tracked separately for analytics
- [ ] Users understand budget correctly
- [ ] Old sessions migrated successfully

### Phase 3: Quality Gates (Month 2)

**Goal:** Enforce quality, prevent regressions

**Tasks:**
1. Extend task YAML schema with `gates` section
2. Update `/execute` skill to enforce pre/post gates
3. Block task completion on gate failures
4. Add gate result tracking to task files
5. Document gate patterns in reference docs
6. Test on 3 features with enforced gates

**Success Criteria:**
- [ ] Gates defined in task YAML
- [ ] Execution blocks on gate failures (no skipping)
- [ ] Gate results tracked in task files
- [ ] Zero regressions in tested features

### Phase 4: Session Context (Month 2)

**Goal:** Better resumption with rich context

**Tasks:**
1. Add `summary`, `decisions`, `blockers` to session_history
2. Update `/pause` skill to prompt for summary
3. Update `/resume-session` to display last session context
4. Test multi-session workflow with rich context
5. Document session summary best practices

**Success Criteria:**
- [ ] Each session has summary + decisions + blockers
- [ ] Resume displays last session context
- [ ] Users report better resumption experience
- [ ] Decisions preserved across sessions

---

## Conclusion

**Your Claude Engineer** demonstrates production-grade patterns we should adopt:

✅ **Adopt:**
1. Multi-model cost optimization (Priority 1)
2. Deterministic quality gates (Priority 3)
3. Session context preservation (Priority 4)

✅ **Already Good:**
1. Single-agent simplicity (keep it)
2. Offline capability (keep it)
3. Vendor-agnostic (keep it)
4. Prompt-driven skills (keep it)

❌ **Don't Adopt:**
1. External state backend (optional, lower priority)
2. Multi-agent orchestration (adds complexity we don't need)

**Expected Outcomes:**
- 30-40% cost reduction from model optimization
- Higher quality from enforced gates
- Better resumption from session context
- Maintained simplicity and offline capability

**Next Step:** Implement Phase 1 (Cost Optimization) to prove value before committing to other phases.

---

_Analysis completed: 2026-02-02_
_Repository: https://github.com/coleam00/your-claude-engineer_
_License: MIT (can adopt patterns freely)_
