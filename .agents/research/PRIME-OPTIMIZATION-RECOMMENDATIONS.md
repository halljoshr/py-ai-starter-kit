# Prime Command Token Optimization Recommendations

**Date:** 2026-01-23
**Issue:** Prime command consuming too many tokens on large codebases (uw-portal-api: 270 tracked files, 2724 Python files)
**Symptom:** Hitting compaction by Task 1.1 in Phase 1 during implement-plan execution
**Impact:** Loss of critical context, degraded implementation quality

---

## Current State Analysis

### uw-portal-api Project Size
- **Tracked files:** 270 files
- **Python files:** 2,724 files (including venv)
- **Core docs:** ~55KB (CLAUDE.md: 8.8KB, README.md: 25.7KB, PIV-LOOP.md: 20.8KB)
- **Average plan size:** ~5,000-6,700 words (~7,000-9,500 tokens each)
- **Plans directory:** 10 feature plans (~57K words total)

### Token Consumption Breakdown (Estimated)

**Current Prime Process:**
1. Read CLAUDE.md: ~3,000 tokens
2. Read README.md: ~8,500 tokens
3. Read PIV-LOOP.md: ~7,000 tokens
4. git ls-files output: ~500-1,000 tokens
5. Directory structure: ~300-500 tokens
6. Recent commits: ~200 tokens
7. Key file searches (rg commands): ~1,000-2,000 tokens
8. Architecture mapping: ~2,000-3,000 tokens
9. Recent plans listing: ~300 tokens
10. Context report generation: ~15,000-20,000 tokens

**Total Prime consumption: ~37,000-45,000 tokens**

**Context before implementation:**
- Prime context: 37-45K tokens
- Plan file read: 7-10K tokens
- System prompts + tools: ~10-15K tokens
- **TOTAL: ~54-70K tokens BEFORE any implementation work**

**Result:** With 200K context window, you're already at 27-35% capacity before writing a single line of code.

---

## Root Cause Analysis

### Problem 1: Reading Full Documentation Every Time
- CLAUDE.md, README.md, PIV-LOOP.md are **static** between features
- Re-reading 55KB of docs every prime is wasteful
- These docs change rarely (maybe 1-2 times per month)

### Problem 2: Over-Comprehensive Context Reports
- Context reports duplicate information from source docs
- Reports are 15-20K tokens of synthesized content
- Most information not immediately needed for implementation

### Problem 3: Exhaustive Code Searches
- Running multiple `rg` searches that return large result sets
- Searching entire codebase when focused search would suffice
- Pattern discovery across all files when you need specific examples

### Problem 4: Sequential Context Accumulation
- Prime → Read plan → Implement accumulates linearly
- No mechanism to "unload" Prime context after plan loading
- Plan contains all necessary references, making Prime context redundant

### Problem 5: No Layered Context Strategy
- All context loaded upfront regardless of need
- No "just-in-time" context loading
- No distinction between "always needed" vs "reference on demand"

---

## Recommended Solutions

### Strategy 1: Tiered Prime Modes (IMMEDIATE WIN)

Create three prime modes with different depths:

#### **Quick Prime** (Default for known codebases)
```bash
/prime --quick
```
**Token budget: ~8,000 tokens**

**Process:**
1. ✅ Read project structure (git ls-files | head -50)
2. ✅ Read current git state (branch, status, recent commits)
3. ✅ List recent plans (last 3-5 only)
4. ✅ Generate MINIMAL context summary (not full report)
5. ❌ Skip full doc reads (assume familiarity)
6. ❌ Skip exhaustive searches
7. ❌ Skip full architecture mapping

**Output:** `.agents/init-context/{project}-quick-{date}.md` (2-3K tokens max)

**Use case:** Daily work on familiar codebase, known patterns

---

#### **Standard Prime** (Current default, for periodic refresh)
```bash
/prime
```
**Token budget: ~20,000 tokens**

**Process:**
1. ✅ Read CLAUDE.md (skim for changes)
2. ✅ Read project structure
3. ✅ Read git state
4. ✅ Targeted searches (entry points, key patterns)
5. ✅ Recent plans (last 5)
6. ✅ Generate focused context report (8-10K tokens)
7. ❌ Skip README.md (reference on demand)
8. ❌ Skip PIV-LOOP.md (stable methodology)
9. ❌ Skip exhaustive architecture mapping

**Output:** `.agents/init-context/{project}-standard-{date}.md` (8-10K tokens)

**Use case:** Weekly refresh, new feature areas, team collaboration

---

#### **Deep Prime** (Comprehensive, for onboarding/major refactors)
```bash
/prime --deep
```
**Token budget: ~45,000 tokens**

**Process:** Current full prime process

**Use case:** First time on project, major refactors, onboarding, after long breaks

---

### Strategy 2: Reference-on-Demand Pattern (HIGH IMPACT)

**Instead of loading all docs upfront, reference them when needed.**

**Implementation:**
1. Prime generates a **reference index** (not full content)
2. During implementation, read specific sections as needed
3. Use `Read` tool with offset/limit for targeted access

**Example Reference Index:**
```markdown
# Context Reference Index

## Documentation
- CLAUDE.md: Development standards [Read on demand]
- README.md: Project overview [Read on demand]
- .claude/reference/fastapi-best-practices.md [Read on demand]

## Key Files (for this feature)
- app/agents/tax_analysis_agent.py:45-120 - Existing agent pattern
- app/services/alloy_service.py:67-89 - API client example
- tests/integration/test_alloy_integration.py - Test pattern

## Recent Patterns
- tax-transition.md - Similar agent implementation
- standardized-agent-event-output.md - Output format standard
```

**Token savings: ~30,000 tokens** (read 3K index instead of 33K docs)

---

### Strategy 3: Plan-Embedded Context (ARCHITECTURAL CHANGE)

**Problem:** Prime context becomes stale/redundant once plan is created.

**Solution:** Plans should be self-contained with all necessary context.

**Plan Enhancement:**
```markdown
# Tax Analysis Agent

## Quick Context (embedded)
- **Patterns to follow:** app/agents/debt_validation_agent.py:45-67
- **Test pattern:** tests/integration/test_debt_validation.py:12-34
- **API client:** app/services/alloy_service.py:78-92
- **Standards:** CLAUDE.md#Agent-Design-Principles (lines 145-167)

## Implementation Tasks
[Each task includes inline references instead of assuming context]
```

**Workflow change:**
1. Run lightweight `/prime --quick` (8K tokens)
2. Run `/plan-feature` (generates self-contained plan)
3. **DISCARD PRIME CONTEXT** (conversation can be closed)
4. **NEW CONVERSATION:** `/implement-plan {plan-file}` (only plan loaded, ~10K tokens)

**Token savings: ~30,000 tokens** (no prime context during implementation)

---

### Strategy 4: Context Caching with TTL (INFRASTRUCTURE)

**Leverage prompt caching for stable content.**

**Implementation:**
```python
# Cache stable documentation with 1-hour TTL
system_messages = [
    {
        "type": "text",
        "text": "You are Claude Code assistant...",
    },
    {
        "type": "text",
        "text": "<CLAUDE.md content>",
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    },
    {
        "type": "text",
        "text": "<Project structure context>",
        "cache_control": {"type": "ephemeral", "ttl": "1h"}
    }
]
```

**Benefits:**
- First prime: Pay 2x tokens for cache write
- Subsequent primes (within 1 hour): Pay 0.1x for cache hits
- **90% cost reduction** on repeated primes
- **60-90% latency reduction**

**When this helps:**
- Multiple features in same day
- Iterative development sessions
- Team working on same codebase

**Cost analysis:**
- First prime: 45K tokens × 2 = 90K token cost (cache write)
- Next 5 primes: 45K tokens × 0.1 = 4.5K token cost each (cache hits)
- **Total for 6 primes:** 90K + (5 × 4.5K) = 112.5K tokens
- **Without caching:** 6 × 45K = 270K tokens
- **Savings: 58% over 6 iterations**

---

### Strategy 5: Focused Context Queries (BEHAVIORAL)

**Instead of comprehensive architecture mapping, use targeted queries.**

**Current approach (wasteful):**
```bash
# Returns hundreds of results
rg "class.*BaseModel" --files-with-matches -g "*.py"
rg "Service\(\)" --files-with-matches -g "*.py"
rg "@router\.(get|post|put|delete)" -A 2 -g "*.py" | head -30
```

**Optimized approach (focused):**
```bash
# Only search in relevant directories for current work
rg "class.*Agent" app/agents/ --files-with-matches
rg "def test_" tests/integration/test_alloy*.py -n | head -10

# Or use Task tool with Explore agent for targeted discovery
```

**Guideline:** Only search for patterns you need for the current feature, not comprehensive discovery.

**Token savings: ~5,000-10,000 tokens**

---

### Strategy 6: Lazy Context Loading (NEW TOOL)

**Create a context management system that loads context progressively.**

**New command: `/load-context {type}`**

```bash
# Instead of one big prime, load context incrementally
/load-context structure    # Just directory/file structure (2K tokens)
/load-context recent       # Recent commits + plans (1K tokens)
/load-context standards    # CLAUDE.md principles (3K tokens)
/load-context architecture # Architecture patterns (5K tokens)
```

**Benefits:**
- Pay only for what you need
- Can unload/reload specific context layers
- More granular control over context window

---

## Recommended Implementation Plan

### Phase 1: Quick Wins (Implement Immediately)

**1.1: Add Prime Mode Flags**
```markdown
# Update .claude/commands/core_piv_loop/prime.md

Add parameter support:
- /prime --quick (or /prime -q)
- /prime (standard, default)
- /prime --deep (or /prime -d)
```

**Token savings: 15-25K per prime for daily work**

---

**1.2: Reference Index Instead of Full Context**
```markdown
Context report should be:
- Quick reference guide (3-5K tokens)
- File path references (not full content)
- "Read on demand" pointers

NOT:
- Full documentation reproduction
- Exhaustive code examples
- Comprehensive architecture diagrams
```

**Token savings: 10-15K per prime**

---

**1.3: Plan-Embedded Context Standard**
```markdown
Update /plan-feature to:
- Include all necessary file references inline
- Embed key pattern snippets in tasks
- Reference specific line numbers for lookups
- Make plans self-contained

Update /implement-plan to:
- NOT require prior prime context
- Work from plan alone
- Load additional context as needed during implementation
```

**Token savings: 30-40K during implementation (can skip prime entirely)**

---

### Phase 2: Infrastructure Improvements (Next)

**2.1: Implement Context Caching**
- Configure prompt caching for CLAUDE.md, README.md, PIV-LOOP.md
- Cache project structure for 1 hour
- Monitor cache hit rates

**2.2: Create Focused Search Patterns**
- Document targeted search strategies in reference docs
- Discourage exhaustive codebase scanning
- Use Task tool with Explore agent for discovery

**2.3: Context Unloading Strategy**
- Document when to close conversations (after planning)
- Establish pattern: plan in one conversation, implement in fresh conversation

---

### Phase 3: Advanced Optimization (Future)

**3.1: Lazy Context Loading**
- Implement /load-context command with granular options
- Create context layers that can be loaded/unloaded

**3.2: Context Compression**
- Summarize old conversation history more aggressively
- Preserve only critical decisions, not full implementation details

**3.3: PreCompact Hook Configuration**
- Configure to preserve plan content, task list, and critical errors
- Allow compaction of search results and exploratory work

---

## Immediate Action Items

### For Your Next Feature on uw-portal-api

**Option A: Minimal Prime (Recommended)**
1. Skip /prime entirely if you've primed recently (within same day)
2. Read plan file directly
3. During implementation, use `Read` tool to reference specific files as needed
4. **Estimated token savings: ~40K tokens**

**Option B: Quick Prime**
1. Only check: git status, git log -5, ls .agents/plans/ -lt | head -5
2. Generate 2-3 sentence context summary in your head (don't write report)
3. Proceed to /plan-feature or /implement-plan
4. **Estimated token savings: ~35K tokens**

**Option C: Plan-Then-New-Conversation**
1. **Conversation 1:** /prime → /plan-feature → close conversation
2. **Conversation 2 (fresh):** /implement-plan {plan-file} → implementation
3. Plan loads (~10K), prime context NOT loaded (~40K saved)
4. **Estimated token savings: ~30K tokens during implementation**

---

## Measurement & Validation

### Success Metrics

**Token Usage:**
- **Current:** ~45K tokens for prime, ~70K total before implementation
- **Target (Quick Prime):** ~8K tokens for prime, ~30K total before implementation
- **Target (No Prime):** 0K tokens for prime, ~20K total before implementation

**Context Retention:**
- Ability to reach Task 3+ in Phase 1 before compaction
- Completion of Phase 1 without hitting compaction
- Full feature implementation without context loss

**Quality Metrics:**
- Implementation still follows patterns correctly
- No increase in validation failures
- Code review scores remain high

---

## Risks & Mitigations

### Risk 1: Loss of Context Quality
**Mitigation:** Make plans more comprehensive with embedded references

### Risk 2: Developer Confusion
**Mitigation:** Document when to use each prime mode clearly

### Risk 3: Inconsistent Pattern Following
**Mitigation:** Plans must include complete code examples, not references to prime context

### Risk 4: More Developer Manual Work
**Mitigation:** Self-contained plans reduce need for manual context gathering

---

## Recommendation Summary

**For immediate relief on uw-portal-api:**

1. **Stop running full /prime before /implement-plan**
   - Plans are already comprehensive (~7-9K tokens)
   - Plans contain all necessary references
   - Prime context is redundant during implementation

2. **Use new conversation for implementation**
   - **Conversation 1:** Planning only
   - **Conversation 2:** Implementation only (fresh context)
   - Saves ~40K tokens

3. **Create Quick Prime variant**
   - Only for periodic refresh (weekly, not daily)
   - 8K tokens instead of 45K tokens
   - Reference index instead of full report

4. **Enhance plans with embedded context**
   - All necessary file references inline
   - Complete code patterns in tasks
   - Self-contained implementation guide

**Expected outcome:**
- Reduce pre-implementation token usage from 70K to 20K (71% reduction)
- Reach feature completion without hitting compaction
- Maintain code quality through comprehensive plans

---

## Next Steps

1. **Immediate:** Test Option C (plan-then-new-conversation) on next uw-portal-api feature
2. **Short-term:** Implement Quick Prime mode in prime.md command
3. **Medium-term:** Update plan-feature command to create self-contained plans
4. **Long-term:** Implement prompt caching for stable documentation

---

## Questions for Consideration

1. **How often does CLAUDE.md actually change?** If rarely, caching is highly valuable
2. **Are recent plans actually useful during implementation?** Or is only the current plan needed?
3. **Could we generate context reports AFTER implementation?** As documentation, not pre-work?
4. **Should /implement-plan automatically start fresh conversation?** Enforce pattern in tooling?

---

**Prepared by:** Claude Sonnet 4.5
**Document status:** Recommendations for review and validation
