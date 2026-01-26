# PIV-Swarm: Discuss Command

**Capture implementation preferences and decisions before planning.**

---

## Purpose

The Discuss command gathers all decisions and preferences needed for implementation BEFORE creating the plan. This prevents mid-implementation questions and ensures the plan is complete.

**Philosophy:** "Decide once, execute cleanly" - All gray areas resolved upfront.

---

## Usage

```bash
/piv:discuss {feature-name}
```

Example:
```bash
/piv:discuss user-authentication
```

---

## Process

### Step 1: Update State

```yaml
# Update .agents/state/session.yaml
session:
  feature: "{feature-name}"
  phase: discuss
```

### Step 2: Feature Analysis

Analyze the feature request to identify:
- Core requirements
- Affected systems
- Potential approaches
- Gray areas needing decisions

### Step 3: Identify Question Categories

Based on feature type, ask relevant questions:

**For API Features:**
- Authentication method?
- Request/response format?
- Error handling approach?
- Rate limiting needed?

**For Data Features:**
- Storage mechanism?
- Validation rules?
- Migration strategy?
- Caching approach?

**For UI Features:**
- Component library?
- State management?
- Responsive requirements?
- Accessibility level?

**For Infrastructure:**
- Deployment target?
- Scaling requirements?
- Monitoring approach?
- Rollback strategy?

### Step 4: Ask Questions

For each gray area, ask a clear question with options:

```markdown
## Decision Needed: [Topic]

**Question:** [Clear question]

**Options:**
1. [Option A] - [Pros/cons]
2. [Option B] - [Pros/cons]
3. [Option C] - [Pros/cons]

**Recommendation:** [If you have one]

**Your choice?**
```

### Step 5: Record Decisions

For each decision, record in session.yaml:

```yaml
# .agents/state/session.yaml
decisions:
  - question: "Which authentication method?"
    answer: "JWT with refresh tokens"
    timestamp: "2026-01-26T10:30:00Z"
    rationale: "Stateless, scalable, already used in codebase"

  - question: "Session duration?"
    answer: "15 minutes access, 7 days refresh"
    timestamp: "2026-01-26T10:31:00Z"
    rationale: "Balance security and UX"
```

### Step 6: Log Messages

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: status_update
  content: |
    Discussion complete for: user-authentication
    Decisions made: 5
    Ready for planning.
```

### Step 7: Update STATE.md

```markdown
## Discussion Decisions

| # | Question | Decision |
|---|----------|----------|
| 1 | Authentication method | JWT with refresh tokens |
| 2 | Session duration | 15min access, 7d refresh |
| 3 | ... | ... |
```

---

## Question Framework

### Must-Ask Questions

1. **Scope Boundaries**
   - What's in scope for v1?
   - What's explicitly out of scope?

2. **Quality Requirements**
   - Test coverage expectations?
   - Performance requirements?
   - Security requirements?

3. **Integration Points**
   - Which existing systems affected?
   - Any external APIs to integrate?

4. **Constraints**
   - Timeline constraints?
   - Technology constraints?
   - Backward compatibility needs?

### Feature-Specific Questions

Generate based on feature type and codebase patterns.

---

## Output

**Stored in session for planning phase:**

1. Feature name and description
2. All decisions with rationale
3. Scope boundaries (in/out)
4. Quality requirements
5. Integration points
6. Constraints

---

## Completion Criteria

- [ ] Feature analyzed for gray areas
- [ ] All questions asked and answered
- [ ] Decisions recorded in session.yaml
- [ ] STATE.md updated with decisions
- [ ] No remaining ambiguity

---

## Next Command

After Discuss, proceed to:
- `/piv:plan` - Generate tasks from decisions

---

## Token Budget

**Target:** 5-15K tokens (mostly Q&A)
**Warning:** If discussion exceeds 20K, checkpoint and continue

---

## Single-Agent vs Swarm

| Mode | Behavior |
|------|----------|
| Single | Orchestrator asks questions directly |
| Swarm | Could spawn researcher to find answers in codebase |

Current mode: **Single Agent**
