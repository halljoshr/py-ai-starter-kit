---
name: explore
description: Early-stage discovery for vague ideas. Research best practices, existing solutions, and feasibility before /discuss.
disable-model-invocation: true
argument-hint: "[topic]"
allowed-tools: Read, Glob, Grep, WebFetch, WebSearch, Write, Bash
---

# Explore: Discovery & Research Phase

**Transform vague ideas into actionable research for informed discussions.**

**Philosophy:** "Research first, decide later" - Understand the problem space before committing to solutions.

---

## Purpose

Early-stage exploration when you have:
- A vague idea but no clear direction
- Questions about best practices
- Uncertainty about existing solutions
- Need to understand implementation complexity
- Want to research before architectural decisions

**Output:** Comprehensive research document ready for `/discuss` phase

---

## Arguments

```
/explore [topic]
/explore authentication-patterns
/explore real-time-notifications
```

If no topic provided, extracts from README.md or asks user.

---

## When to Use

**✅ Use `/explore` when:**
- Idea is vague ("add real-time features", "improve security")
- Don't know if solutions already exist
- Need to research best practices
- Want to compare multiple approaches
- Unsure about implementation complexity

**❌ Skip `/explore` when:**
- Requirements are already clear and specific
- Solution is well-defined
- Just need to implement known patterns
- Direct to `/discuss` with clear architectural decisions

---

## Process

### Phase 1: Discovery

**Goal:** Understand what we're actually trying to build

**Questions to ask user:**
```
1. What problem are you trying to solve?
2. What's your current approach (if any)?
3. What's not working or missing?
4. What scale/complexity are you targeting?
5. Any constraints (time, tech stack, budget)?
```

**Use AskUserQuestion for structured discovery:**
- Keep questions focused (1-4 at a time)
- Build context progressively
- Clarify terminology
- Identify success criteria

**Output:** Clear problem statement

**Reference:** See `references/exploration-strategies.md` for question patterns

---

### Phase 2: Research

**Goal:** Find what already exists and learn from it

**Research sources:**

1. **Documentation & Standards**
   ```bash
   # Search for official docs
   # Use WebFetch for authoritative sources
   ```
   - Framework documentation
   - RFC specifications
   - Industry standards (OWASP, NIST, etc.)

2. **Existing Solutions**
   ```bash
   # Search GitHub for implementations
   # Look for popular libraries
   ```
   - npm/PyPI packages
   - Open source projects
   - Reference implementations

3. **Best Practices**
   ```bash
   # Search for guides and patterns
   ```
   - Architectural patterns
   - Design patterns
   - Anti-patterns to avoid

4. **Community Knowledge**
   - Blog posts from experts
   - Conference talks
   - Discussion threads (Stack Overflow, Reddit)

**WebFetch Strategy:**
- Start with official documentation
- Look for authoritative sources (not random blogs)
- Capture key concepts and code snippets
- Document sources with URLs

**Reference:** See `references/web-search-patterns.md` for effective research strategies

---

### Phase 3: Analysis

**Goal:** Evaluate and compare options

**For each solution found:**

```markdown
## Option: [Solution Name]

**What it is:** Brief description

**Pros:**
- Key benefits
- Use cases where it excels

**Cons:**
- Limitations
- Trade-offs

**When to use:**
- Specific scenarios
- Scale requirements
- Team expertise needed

**Resources:**
- [Official docs](url)
- [Example implementation](url)
- [Tutorial](url)
```

**Comparison criteria:**
- Complexity (simple → complex)
- Maturity (experimental → battle-tested)
- Community support (niche → mainstream)
- Performance (slow → fast)
- Maintenance burden (low → high)

**Create comparison table:**

| Solution | Complexity | Maturity | Performance | Best For |
|----------|-----------|----------|-------------|----------|
| Option A | Low | High | Medium | Small-medium projects |
| Option B | High | Medium | High | Large-scale systems |

---

### Phase 4: Feasibility Assessment

**Goal:** Understand implementation complexity

**Run complexity analysis on similar codebases:**

```bash
# If we have local examples, analyze them
uv run python .claude/skills/explore/scripts/estimate_complexity.py [codebase-path]
```

**Assess:**

1. **Code Complexity**
   - How many files/modules needed?
   - Dependencies required?
   - Integration points with existing code?

2. **Learning Curve**
   - New technologies to learn?
   - Team expertise level?
   - Documentation quality?

3. **Risk Assessment**
   - Security implications?
   - Performance concerns?
   - Maintenance burden?

4. **Implementation Estimate**
   - Small (1-3 files, < 500 LOC)
   - Medium (4-10 files, 500-2000 LOC)
   - Large (10+ files, > 2000 LOC)

**Reference:** See `references/feasibility-assessment.md` for complexity rubrics

---

### Phase 5: Synthesis

**Goal:** Create actionable research document

**Generate:** `.agents/research/{topic}-exploration-{date}.md`

```markdown
# Exploration: {Topic}

**Date:** {timestamp}
**Status:** Research Complete

---

## Problem Statement

What we're trying to solve and why.

---

## Research Findings

### Existing Solutions

1. **[Solution A]**
   - Description
   - Pros/Cons
   - When to use
   - Resources: [links]

2. **[Solution B]**
   - Description
   - Pros/Cons
   - When to use
   - Resources: [links]

### Best Practices

Key patterns and recommendations from research.

### Anti-Patterns

What to avoid based on community knowledge.

---

## Comparison Analysis

| Solution | Complexity | Maturity | Performance | Best For |
|----------|-----------|----------|-------------|----------|
| ... | ... | ... | ... | ... |

---

## Feasibility Assessment

**Complexity:** Small/Medium/Large
**Learning Curve:** Low/Medium/High
**Risk Level:** Low/Medium/High

**Estimated Scope:**
- Files to create/modify: X
- New dependencies: [list]
- Integration points: [list]

---

## Recommendations

**Primary Recommendation:** [Solution name]
- Rationale: Why this is the best fit
- Trade-offs accepted
- Risk mitigation

**Alternative:** [Solution name]
- When to consider this instead

---

## Open Questions for /discuss

1. [Question requiring architectural decision]
2. [Question requiring user input]
3. [Question about priorities]

---

## Code Examples

```python
# Runnable example demonstrating key concept
```

---

## Resources

### Documentation
- [Link with description]

### Example Implementations
- [Link with description]

### Tutorials
- [Link with description]

---

## Next Steps

Ready for `/discuss {topic}` to make architectural decisions based on this research.
```

---

## Success Criteria

Exploration is complete when:
- [ ] Problem statement is clear and specific
- [ ] Multiple solutions researched (2-4 options)
- [ ] Each solution has pros/cons documented
- [ ] Comparison table created
- [ ] Feasibility assessed with complexity estimate
- [ ] Resources documented with URLs
- [ ] Code examples included (where applicable)
- [ ] Primary recommendation with rationale
- [ ] Open questions identified for `/discuss`
- [ ] Research document generated

---

## Progressive Disclosure Pattern

**Level 1 (Loaded now):** This SKILL.md

**Level 2 (Load when needed):**
- `references/exploration-strategies.md` - Question patterns for discovery
- `references/web-search-patterns.md` - Effective research strategies
- `references/feasibility-assessment.md` - Complexity estimation rubrics

**Level 3 (Execute when needed):**
- `scripts/estimate_complexity.py` - Analyze codebase statistics

---

## Example Usage

### Scenario: "We need real-time notifications"

**Phase 1: Discovery**
```
Q: What type of notifications?
A: User activity updates, like GitHub notifications

Q: Scale?
A: 100K users, notifications every few minutes

Q: Existing infrastructure?
A: FastAPI backend, React frontend
```

**Phase 2: Research**
- WebSockets (Socket.io, native WebSocket API)
- Server-Sent Events (SSE)
- Polling strategies
- Third-party services (Pusher, Ably)

**Phase 3: Analysis**
| Solution | Complexity | Latency | Best For |
|----------|-----------|---------|----------|
| WebSocket | High | <100ms | Bi-directional, high frequency |
| SSE | Low | ~1s | Server→Client, moderate frequency |
| Polling | Very Low | 5-30s | Simple, low frequency |

**Phase 4: Feasibility**
- WebSocket: Medium complexity (5-7 files, need Redis for scaling)
- SSE: Low complexity (2-3 files, built-in browser support)
- Polling: Very low (1 file, use existing API)

**Phase 5: Synthesis**
**Recommendation:** Start with SSE
- Rationale: Simpler, meets frequency requirements, easier to maintain
- Trade-off: One-way only (acceptable for notification use case)
- Upgrade path: Can add WebSocket later if bi-directional needed

**Output:** `.agents/research/real-time-notifications-exploration-2026-01-30.md`

---

## Integration with PIV Workflow

```
/prime              # Understand codebase
    ↓
/explore [topic]    # Research vague idea ← YOU ARE HERE
    ↓
/discuss [feature]  # Make architectural decisions using research
    ↓
/spec [feature]     # Write formal specification
    ↓
...
```

**Key:** `/explore` transforms unknowns into informed choices for `/discuss`

---

## Token Budget

**Typical exploration:** 15-30K tokens
- Discovery: 2-5K
- Research: 8-15K (WebFetch heavy)
- Analysis: 3-5K
- Feasibility: 2-3K
- Synthesis: 2-5K

---

## Tips

**Effective Research:**
- Start with official documentation
- Look for production-grade examples
- Prioritize recent content (last 2 years)
- Check GitHub stars/downloads for popularity
- Read issue trackers for gotchas

**Avoid:**
- Over-researching (3-4 options is enough)
- Analysis paralysis (perfect is enemy of good)
- Ignoring existing codebase patterns
- Skipping feasibility assessment
- Forgetting to document sources

---

## Remember

**"Research doesn't mean we know everything, it means we know enough to decide intelligently."**

- Exploration reduces risk
- Multiple options reveal trade-offs
- Feasibility prevents overcommitment
- Documentation enables future review
- Research artifacts outlast memory

---

## Next Command

After `/explore` completes: `/discuss {topic}` with research document as context
