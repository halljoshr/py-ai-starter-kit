# Feedback: /discuss and /spec Skill Improvements

**Date:** 2026-01-28
**Source:** Dogfooding session - First use of /discuss and /spec on py-ai-starter-kit
**Context:** After completing full PIV workflow (prime → discuss → spec) on overall project
**Related:** [FEEDBACK_IDEAS.md](../../FEEDBACK_IDEAS.md) - General improvement ideas

---

## Overview

This document captures lessons learned from the first real usage of /discuss and /spec skills. These improvements will be implemented when building the skills themselves (Priority 1, Goal #2).

**Key Insight:** Timeline assumptions biased decisions. AI development is hours/days, not months/years.

---

## Critical Issue: Timeline Bias

### Problem

I (Claude) framed discussions using human development timelines:
- "Week 1-2 for Prime optimization"
- "Priority 2 = Q2 2026 (months away)"
- "Defer to 2027+"

This led to **unnecessary deferrals**:
- "Goal #6? Not critical for Q1, defer"
- "Goal #11? Team will grow later, defer"
- "Goals #17-19? Way in the future, defer"

### Reality

With AI-assisted development using PIV:
- Goal #6 (JSON tracking) = 2-3 hours, not months
- Goal #11 (formalization) = 1 hour to structure
- Templates, patterns, docs = Days, not quarters

### Fix

**For /discuss skill:**
1. ❌ Remove ALL timeline assumptions (no "Week 1-2", no "Q2 2026")
2. ❌ Don't say "Priority X = time period Y"
3. ✅ Frame as "now vs later", not "this quarter vs next year"
4. ✅ Ask user about timing: "When do you need this?"
5. ✅ Treat everything as potentially doable now

**For /spec skill:**
1. ❌ Remove timeline estimates from implementation steps
2. ✅ Assume building whole project in one go (even if multi-day)
3. ✅ For feature specs: Always assume single sitting

**Exception:** User explicitly states timeline → Use their timeline, don't invent

**✅ IMPLEMENTED (2026-01-30):** Added "Timeline & Estimation Policy" section to CLAUDE.md. All future agents will read this during /prime.

---

## 10 Improvement Areas

### 1. Question Volume & Efficiency ✅

**Observation:** 35 AskUserQuestion interactions during discussion

**Problem:** Asking questions already answered in research/references

**Solution:**
- /discuss should read research + reference docs early (use more tokens upfront)
- Add decision guidance to YAML schemas (`.claude/schemas/database-decisions.yaml`)
- Start with 2-3 strategic questions, apply smart defaults from schemas
- Only ask what's NOT already documented

**Example Smart Defaults (from schemas):**
```yaml
# .claude/schemas/database-decisions.yaml
database_choice:
  sqlite:
    use_when:
      - "Project is demo, example, or prototype"
      - "< 5 models, < 10 endpoints"
  postgresql:
    use_when:
      - "10M+ rows mentioned"
      - "Production environment"
      - "Complex queries needed"

fastapi_patterns:
  always_use:
    - "Pydantic v2 (not v1)"
    - "Async/await (not blocking I/O)"
    - "httpx for external APIs (not requests)"
```

**Implementation:**
- Build schema guidance files (Priority 1, alongside /discuss)
- /discuss reads research + schemas before asking
- Reduces 35 questions → ~10 questions

---

### 2. Research Timing ✅

**Observation:** Asked "have you looked at swarm info?" before reading it myself

**Problem:** Asking about things I should read first

**Solution:**
- /discuss reads research/references when needed for clarity
- If unclear what we're discussing → read relevant docs first, then ask informed questions
- Not "always read everything" but "read what's needed to understand context"

**Example:**
- ❌ BAD: "How should skills coordinate?" (vague, no context)
- ✅ GOOD: Read piv-swarm-example/, understand design, then ask "The swarm example shows orchestrator + executors. Build now or defer automation?"

---

### 3. Premature Implementation Detail ✅

**Observation:** During /discuss, we decided exact Python script structure for `/optimize`

**Initial hypothesis:** Too detailed for /discuss (should be /spec)

**Actual decision:** /discuss IS the right place for implementation details

**Problem:** We got sidetracked into meta-discussions about skill system itself

**Solution:**
- /discuss should iron out ALL details (strategic + implementation) for the feature
- /spec is clean writeup of those decisions in Anthropic XML format
- **Rule:** /discuss for feature X → Discuss feature X only
- Don't meta-discuss "how should skills work in general" unless that's the feature

**What happened:**
- Feature: /optimize skill
- Got sidetracked: "How should skills use helper scripts in general?"
- Should have: Stayed focused on /optimize, used existing patterns

---

### 4. Decision Granularity ✅

**Observation:** 35 numbered decisions - is that too many?

**Decision:** **Flexibility over rigid structure**

**Solution:**
- Large/complex projects → More decisions (35, 50, 100+ if needed)
- Simple projects → Fewer decisions
- Don't artificially limit decision count
- **Primary metric: Completeness** (did we capture everything?)
- Organize however makes them clear and referenceable
- Group if helpful (Decision #3 with 3a, 3b, 3c) or separate if distinct

---

### 5. Discussion Structure ✅

**Observation:** Went through goals 1-21 sequentially, caused cognitive switches

**Problem:** Jumping between unrelated topics (token mgmt → testing → autonomy → back to tokens)

**Solution:** /discuss should create thematic agenda BEFORE asking questions

**Example Agenda:**
```markdown
## Discussion Agenda for py-ai-starter-kit

**Session 1: Token & Context Management** (30-40 min)
- Prime optimization (Goal #1)
- Token budgeting (Goal #4)
- Context management (Goal #14)
- Cost tracking (Goal #15)

**Session 2: State & Workflow** (40-50 min)
- Session management (Goal #3)
- Multi-session architecture (Goal #4)
- Swarm coordination

**Session 3: Quality & Testing** (30-40 min)
- TDD culture (Goal #7)
- Validation strategy
- Coverage enforcement

Approve this agenda? Or reorder?
```

**Implementation:** /discuss has "agenda creation" step before questions

---

### 6. Clarification Loops ✅

**Observation:** Multiple times user said "clarify this" and I re-asked

**Problem:** Questions weren't clear enough upfront

**Solution:** Add more context/rationale for each option, especially WHY that option exists

**Example:**

**WEAK (current):**
```
Options:
1. Single-agent first
2. Build for swarm from day one
3. Swarm-lite
```

**STRONG (improved):**
```
Options:
1. Single-agent first (Recommended for clarity)
   Description: Work in single-agent mode for Priority 1
   Why this exists: Simpler to build and test, proves workflow first before adding complexity

2. Build for swarm from day one
   Description: Implement full agent spawning and coordination now
   Why this exists: Avoids refactoring later, but significantly more complex upfront

3. Swarm-lite (What we chose)
   Description: Build state structure now, add automation later
   Why this exists: Gets state right immediately, defers complex orchestration until workflow proven
```

**Key:** Each option explains its rationale, not just what it is

---

### 7. Validation of Consistency ✅

**Observation:** Made 35 decisions but didn't check if they all work together

**Problem:** Potential conflicts undetected (strict TDD + atomic commits + phase-based = too much overhead?)

**Solution:** After all decisions made, run consistency check

**Example:**
```markdown
## Final Step: Consistency Validation

Checking if all 35 decisions work together...

✅ No conflicts found between:
- Swarm-lite architecture + YAML state
- Atomic commits per task + phase-based execution
- Strict TDD + user approval opt-outs

⚠️ Potential tension identified:
- Decision #17: Validate after each task (comprehensive)
- Decision #16: Execute one phase at a time (fresh context)
- Concern: Running all unit tests after each task might be slow if test suite is large

Recommendation: Keep as-is, monitor during dogfooding. If tests become slow (>2 min),
consider caching test results or smarter test selection.
```

---

### 8. Spec Generation Timing ✅

**Observation:** Generated spec at the very end (all discussion → then spec)

**Decision:** **Clean separation is correct**

**Rationale:**
- Allows flexibility: Some discussions conclude "don't build this" or "too simple for spec"
- /discuss can end with "cancel feature" or "skip spec, go straight to implementation"
- Only generate spec when discussion confirms we're moving forward

**Flow:**
```
/discuss feature
  → Decision: Build it (proceed to /spec)
  → Decision: Don't build it (stop, document why)
  → Decision: Too simple (skip to /plan or direct implementation)
```

---

### 9. Token Efficiency in Discussion ✅

**Observation:** Used 137K tokens for discussion + spec (68% of budget)

**Decision:** **Verbosity is correct**

**Rationale:**
- Pay tokens upfront in /discuss to save implementation rework
- Better to spend 100K discussing + 50K implementing than 50K discussing + 100K fixing
- Thorough discussion prevents agent rabbit holes and unwanted features
- **Principle:** "Expensive planning, cheap implementation" beats "cheap planning, expensive fixes"

**Token investment philosophy:** Front-load planning → smooth implementation

---

### 10. User Fatigue ✅

**Observation:** Long discussions might be exhausting

**Decision:** Discussion length scales with scope, offer breaks between sections

**Solution:**
- Small feature (3 goals) = short discussion
- Large project (21 goals) = long discussion, offer breaks
- After each thematic section completes: offer optional break
- **CRITICAL:** Save all decisions to `.agents/research/{feature}-discussion-{date}.md` BEFORE any break
- User chooses to continue or pause

**Example:**
```markdown
## Session 1 Complete: Token & Context Management ✓

Decisions captured:
- Decision #1: Prime optimization
- Decision #2: Token thresholds
- Decision #3: Caching strategy

**Saved to:** .agents/research/py-ai-starter-kit-discussion-2026-01-28.md

---

**Next:** Session 2 - State & Workflow (5 topics, ~40 min estimated)

Continue now or take a break?
- Continue → Move to Session 2
- Pause → Save progress, resume later with /resume-discuss
```

**Safety:** All decisions written incrementally, never lost if context ends

---

## New Skill Required: /explore

### Discovery

During feedback, realized there are TWO types of discussion phases:

**Level 1: Project Exploration (New)**
- Scenario: "I have a vague idea, not sure if feasible, scope unclear"
- Purpose: Explore problem space, understand feasibility, clarify goals
- Style: Free-form, exploratory, lots of "what if?"
- Output: Research document for /discuss to consume

**Level 2: Feature Discussion (Existing /discuss)**
- Scenario: "I know what I'm building, need to make decisions"
- Purpose: Apply research, use patterns, make implementation decisions
- Style: Structured, pattern-based, strategic questions
- Output: Decision document with rationale

### Skill: /explore

**Name:** `/explore` (chosen over /research, /discover, /shape)

**Priority:** Priority 1 (build early, needed for workflow)

**Purpose:** Early-stage project exploration before /discuss

**Actions:**
1. Ask open-ended questions about the problem
2. Research similar solutions (web search if needed)
3. Explore feasibility and complexity
4. Discuss trade-offs at high level
5. Help user articulate goals clearly
6. Capture findings in `.agents/research/{project}-exploration-{date}.md`

**Output Format:**
```markdown
# Project Exploration: {name}

## Problem Statement
[What user is trying to solve]

## Goals & Success Criteria
[What success looks like]

## Similar Solutions Researched
[What exists, pros/cons]

## Feasibility Assessment
[Can we build this? Complexity?]

## Recommended Approach
[High-level direction based on exploration]

## Open Questions for /discuss Phase
[Specific architectural decisions needed]

## Research Artifacts
[Links to docs, examples, references found]
```

**Integration:** /discuss reads this exploration document and focuses questions on "Open Questions" section

**Complete Flow:**
```
/explore project-idea     → Early exploration, create research doc
   ↓
/prime (or /prime-deep)  → Codebase context
   ↓
/discuss feature         → Read exploration + research, make decisions (smart defaults)
   ↓
/spec                    → Formal specification
   ↓
/plan → /execute → ...
```

**User Note:** "I think it was a combination of that plan and previous research conversations that resulted in the research documents. I am making this up on the fly a bit still."

**Implementation Priority:** Build /explore in Priority 1 alongside /discuss and /spec

---

## Implementation Checklist

When building /discuss and /spec skills (Priority 1, Goal #2):

**For /discuss:**
- [ ] Remove all timeline assumptions and references
- [ ] Create thematic agenda before asking questions
- [ ] Read research + reference docs early in phase
- [ ] Build YAML schema guidance files (`.claude/schemas/`)
- [ ] Add context/rationale to each question option (WHY it exists)
- [ ] Implement consistency validation at end
- [ ] Offer breaks between thematic sections
- [ ] Save decisions incrementally to `.agents/research/`
- [ ] Stay focused on feature being discussed (no meta-discussions)

**For /spec:**
- [ ] Remove timeline estimates from implementation steps
- [ ] Assume single sitting for features, multi-day for projects
- [ ] Only generate spec when /discuss confirms "build it"
- [ ] Clean writeup of decisions in Anthropic XML format
- [ ] Reference all decisions made in /discuss

**For /explore (new):**
- [ ] Build skill in Priority 1
- [ ] Output format that /discuss expects
- [ ] Open-ended question style
- [ ] Feasibility assessment
- [ ] Generate research document with "Open Questions" section

---

## Related Documents

**This Document:**
- `.agents/feedback/discuss-spec-improvements-2026-01-28.md`

**References:**
- [FEEDBACK_IDEAS.md](../../FEEDBACK_IDEAS.md) - General improvement ideas and company issues
- [.agents/research/overall-project-discussion-2026-01-28.md](../research/overall-project-discussion-2026-01-28.md) - Full discussion transcript with 35 decisions
- [.agents/specs/py-ai-starter-kit-spec.txt](../specs/py-ai-starter-kit-spec.txt) - Specification generated from discussion
- [.agents/research/SPEC-CREATION-PROCESS.md](../research/SPEC-CREATION-PROCESS.md) - Original spec creation research

**Bi-directional Links:**
- FEEDBACK_IDEAS.md should reference this document
- This document references FEEDBACK_IDEAS.md
- Discussion transcript references this feedback
- Spec references discussion decisions

---

## Success Metrics

**These improvements are successful when:**
- /discuss uses <50% tokens of current usage (via research reading + smart defaults)
- Clarification loops reduced by 80% (better question context)
- User fatigue reduced (thematic grouping + breaks)
- No timeline bias in discussions
- Consistency validation catches conflicts
- /explore → /discuss → /spec flow works smoothly on first dogfooding feature

---

**Next Steps:**
1. Update FEEDBACK_IDEAS.md to reference this document
2. Implement /explore, /discuss, /spec skills using these improvements (Priority 1, Goal #2)
3. Test on first dogfooding feature (probably /status or /optimize skill)
4. Capture additional feedback and iterate

---

*Captured: 2026-01-28*
*Source: Dogfooding session with user feedback*
*Status: Ready for implementation*
