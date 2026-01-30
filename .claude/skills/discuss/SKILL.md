---
name: discuss
description: Interactive discussion phase for architectural decisions, skill improvements, and design exploration
disable-model-invocation: true
argument-hint: "[feature-name]"
allowed-tools: Read, Write, Glob, Grep, AskUserQuestion, Bash
---

# Discuss: Interactive Design Phase

**Collaborative discussion to make architectural decisions, explore skill improvements, and clarify requirements before writing the spec.**

**Philosophy:** "Decide together, implement autonomously" - All ambiguous decisions happen here through discussion.

---

## Purpose

Bridge the gap between priming (understanding) and spec (formal plan) through structured discussion:
1. **Clarify ambiguous requirements** from ticket/README
2. **Make architectural decisions** with user input
3. **Review and improve existing skills** based on examples and best practices
4. **Explore design alternatives** and trade-offs
5. **Capture all decisions** for the spec phase

---

## Arguments

```
/discuss [feature-name]
```

**Examples:**
```
/discuss analytics-pipeline
/discuss authentication-system
/discuss
```

If no feature name, infers from README.md or asks.

---

## Process

### Step 1: Load Context

**Read priming artifacts:**
```bash
cat .agents/state/prime-context.md  # Codebase understanding
cat README.md                        # Requirements
cat .agents/piv-feedback.md         # Previous learnings (if exists)
```

**Understand:**
- What feature is being requested
- What already exists in codebase
- What patterns/conventions are established
- What pain points exist from previous cycles

---

### Step 2: Load Decision Schemas

**Read schema library for smart defaults:**

```bash
# Load relevant decision schemas
cat .claude/schemas/database-decisions.yaml
cat .claude/schemas/api-patterns.yaml
cat .claude/schemas/testing-strategies.yaml
cat .claude/schemas/architecture-patterns.yaml
cat .claude/schemas/deployment-options.yaml
```

**Apply heuristics from schemas:**

Each schema contains:
- `use_when`: Conditions for auto-selecting this option
- `default_when`: Heuristic rules for automatic selection
- `always_use`: Patterns to apply without asking
- `never_do`: Anti-patterns to avoid

**Example heuristic application:**

```yaml
# From database-decisions.yaml
database_choice:
  sqlite:
    default_when: "prototype OR demo"
  postgresql:
    default_when: "production OR scale"
```

**Decision flow:**
1. Check if context matches `default_when` conditions
2. If match → Auto-select, document in decisions
3. If no match or ambiguous → Add to discussion topics
4. Always apply `always_use` patterns without asking

**Result:** Reduce question volume by 70% through smart defaults (35 → ~10 questions)

**See:** `.claude/schemas/README.md` for detailed schema usage patterns

---

### Step 3: Identify Discussion Topics

**Analyze requirements and extract:**

1. **Ambiguous Requirements**
   - Vague descriptions ("make it fast", "user-friendly")
   - Missing acceptance criteria
   - Unclear scope boundaries

2. **Architectural Decisions Needed**
   - Database choice (if not specified)
   - Caching strategy (if performance critical)
   - Auth mechanism (if needed)
   - Async vs sync patterns
   - External service integrations

3. **Skill Improvement Opportunities**
   - Read all skills in `.claude/skills/*/SKILL.md`
   - Compare against user-provided examples
   - Identify gaps, inconsistencies, or improvement areas
   - Look for missing skills referenced in workflow

4. **Design Trade-offs**
   - Simplicity vs flexibility
   - Performance vs maintainability
   - Time-to-market vs technical debt

**Output:** Discussion agenda with topics grouped

---

### Step 4: Skill Review & Improvement

**This is the META phase - improving our own tools!**

1. **Read all current skills:**
   ```bash
   ls .claude/skills/*/SKILL.md
   ```

2. **For each skill, evaluate:**
   - Is the process clear and actionable?
   - Does it have all necessary steps?
   - Are there example outputs?
   - Does it reference schemas correctly?
   - Is it consistent with other skills?

3. **Ask user for examples:**
   ```
   "I see we have [skill-name]. Do you have any examples or
   reference implementations that could improve it?"
   ```

4. **Capture improvement ideas:**
   - Add missing steps
   - Clarify ambiguous instructions
   - Add code examples
   - Improve validation criteria
   - Better error handling

5. **Update skills immediately if changes are clear:**
   - Edit SKILL.md files
   - Add examples to `.claude/reference/`
   - Update schemas in `.claude/schemas/`

**Example discussion:**
```markdown
## Skill Improvement: /execute

**Current state:** Has validation command execution but skill invocation is unclear
**Issue:** Doesn't show exactly how to use the Skill tool
**Example needed:** Show concrete invocation of /code-review and /validate
**Proposed improvement:** Add Step 8 with explicit Skill tool usage and result capture
```

---

### Step 5: Architectural Discussion

**For each decision point, present options:**

**IMPORTANT:** Only ask about decisions not auto-resolved by schemas in Step 2.

Use AskUserQuestion with:
- Clear options (2-4 choices)
- Trade-offs explained for each
- Recommendation based on context (from schemas when available)
- "Other" always available

**Example:**
```
Question: "Which database for 10M+ row analytics?"
Options:
1. PostgreSQL (Recommended)
   - Best for 10M+ rows
   - Excellent indexing
   - ACID guarantees
   Trade-off: Requires separate service

2. SQLite
   - Simple setup
   - No external dependencies
   Trade-off: Performance issues at 10M+ scale

3. MongoDB
   - Flexible JSON schema
   - Horizontal scaling
   Trade-off: Eventual consistency, overkill for structured data
```

**Capture each decision with rationale:**
```yaml
- question: "Database choice?"
  answer: "PostgreSQL"
  rationale: "10M+ rows requirement needs proper indexing and ACID"
  auto_selected: false  # User was asked
  timestamp: "2026-01-28T..."
```

**Example with schema auto-selection:**
```markdown
## Decision: API Framework

**Schema Match:** api-patterns.yaml → always_use: "Pydantic v2 for validation"
**Auto-Selected:** FastAPI with Pydantic v2
**Rationale:** Matches project context (Python, REST API), schema default applied
**Status:** ✓ No user question needed
```

---

### Step 6: Requirement Clarification

**For vague requirements, drill down:**

| Vague | Clarified |
|-------|-----------|
| "Fast queries" | "< 500ms p95 at 10M rows" |
| "Good test coverage" | "80% minimum, critical paths 100%" |
| "Scalable" | "Handle 1K requests/sec, horizontal scaling via load balancer" |
| "User-friendly API" | "OpenAPI docs, consistent error responses, examples for each endpoint" |

Use AskUserQuestion to get specifics.

---

### Step 7: Design Alternatives

**Present multiple approaches when valid:**

Example: Background job processing
```
Option 1: APScheduler (Recommended for v1)
- Pros: Built into Python, no external deps, good for periodic tasks
- Cons: Single-process, not distributed
- Best for: < 100 jobs/hour, simple scheduling

Option 2: Celery + Redis
- Pros: Distributed, battle-tested, scales horizontally
- Cons: Complex setup, more moving parts
- Best for: > 1000 jobs/hour, multiple workers needed

Option 3: AWS Lambda + EventBridge
- Pros: Serverless, infinite scale, pay-per-use
- Cons: Cloud vendor lock-in, cold starts
- Best for: Unpredictable load, cloud-native architecture
```

**Capture chosen approach and why.**

---

### Step 8: Update Feedback Log

**If `.agents/piv-feedback.md` exists:**
- Review previous issues encountered
- Discuss how to avoid them
- Update skills/references to prevent recurrence

**Example:**
```markdown
## Previous Issue
Feature: User authentication (2026-01-15)
Problem: Validation skill missed insecure password hashing
Learning: Need security-focused validation step

## Resolution
- Updated /validate skill to include security checks
- Added .claude/reference/security-best-practices.md
- Added security checklist to code-review skill
```

---

### Step 9: Create Discussion Summary

**Save to:** `.agents/research/{feature}-discussion-{date}.md`

```markdown
# Feature Discussion: {feature-name}
Date: {timestamp}

## Schema-Based Auto-Decisions

(List decisions made automatically from schema heuristics in Step 2)

## Requirements Clarified

| Original | Clarified |
|----------|-----------|
| "Fast" | < 500ms p95 |
| "Scalable" | 1K req/sec |

## Architectural Decisions

1. **Database: PostgreSQL**
   - Rationale: 10M+ rows, ACID needed
   - Alternative considered: MongoDB (rejected - structured data better in SQL)

2. **Caching: Redis**
   - Rationale: Distributed, persistent, < 100ms target
   - Alternative considered: In-memory (rejected - not shared across instances)

## Skill Improvements Made

1. **Enhanced /execute skill**
   - Added explicit Skill tool invocation in Step 8
   - Added test_results capture structure
   - Added retry logic documentation

2. **Created /discuss skill**
   - New skill for interactive design phase
   - Includes skill improvement review
   - Captures decisions with rationale

## Design Decisions

- Background jobs: APScheduler (v1), migrate to Celery if > 100 jobs/hour
- API versioning: /api/v1/ prefix
- Error responses: RFC 7807 Problem Details
- Logging: structlog with JSON output

## Open Questions

(None - all clarified)

## Next Steps

Run `/spec {feature-name}` to generate formal specification.
```

---

### Step 10: Update Session State

**Update `.agents/state/session.yaml`:**
```yaml
session:
  phase: discuss
  status: completed

decisions: [...]  # All captured decisions

discuss:
  completed_at: "2026-01-28T..."
  topics_discussed: 7
  skills_improved: 2
  decisions_made: 9
```

---

### Step 11: Prompt Next Phase

```markdown
## Discussion Complete ✓

**Summary:**
- Requirements clarified: 5
- Decisions made: 9
- Skills improved: 2
- Alternatives evaluated: 3

**Captured in:** .agents/research/{feature}-discussion-{date}.md

**Next Step:**
```bash
/spec {feature-name}
```

This will generate the formal Anthropic XML specification using all decisions made during discussion.
```

---

## Discussion Topics Checklist

Discuss phase is complete when:
- [ ] All vague requirements clarified with specific targets
- [ ] All architectural decisions made with rationale
- [ ] All existing skills reviewed for improvements
- [ ] All design alternatives evaluated
- [ ] User has provided any reference examples they want incorporated
- [ ] All decisions captured in discussion summary
- [ ] Session state updated

---

## Skill Improvement Framework

**When reviewing skills, check:**

1. **Completeness**
   - [ ] Has clear purpose/philosophy
   - [ ] Step-by-step process
   - [ ] Input/output examples
   - [ ] Error handling
   - [ ] Completion criteria

2. **Actionability**
   - [ ] Each step is concrete (not vague)
   - [ ] Tool usage specified (Bash vs Read vs Skill)
   - [ ] File paths are specific
   - [ ] Commands are copy-pasteable

3. **Integration**
   - [ ] References correct schemas
   - [ ] Consistent with other skills
   - [ ] Updates session state correctly
   - [ ] Fits in overall workflow

4. **Examples**
   - [ ] Has example inputs
   - [ ] Has example outputs
   - [ ] Shows error cases
   - [ ] References real implementations

**Improvement sources:**
- User-provided examples
- Anthropic research docs
- Other workflow implementations
- Previous PIV feedback
- Industry best practices

---

## Example Skill Improvement Session

```
Assistant: "I'm reviewing the /execute skill. I see it runs validation
commands but the skill invocation section could be clearer.

Do you have any examples of how validation skills should be invoked
and how results should be captured?"

User: "Yes, check the Anthropic example in research docs."

Assistant: [Reads research docs, finds explicit examples]

"I see Anthropic captures skill results with passed/failed status and
issue counts. Let me update /execute to show exactly how to invoke
the Skill tool and capture these results."

[Updates /execute skill with Step 8: Invoke Validation Skills]
```

---

## Remember

**Discuss before spec:**
- Spec writes decisions, discuss makes them
- All ambiguity resolved here
- User input captured, not guessed
- Skill improvements happen iteratively

**Output quality:**
- Every decision has rationale
- Every alternative is considered
- Every improvement is captured
- Ready for autonomous implementation

---

## Next Skill

After `/discuss` completes: `/spec {feature-name}` to generate formal specification
