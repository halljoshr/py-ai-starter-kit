---
name: plan-feature
description: Create comprehensive feature plans with all context for one-pass implementation success.
disable-model-invocation: true
argument-hint: "{feature-name}"
allowed-tools: Read, Glob, Grep, Write, WebFetch, WebSearch, Bash(git:*), Bash(rg:*)
---

# Plan Feature Command

**Create comprehensive feature plans with all context for one-pass implementation success.**

---

## Arguments

```
/plan-feature {feature-name}
```

**Example:**
```
/plan-feature hubspot-webhook-validation
/plan-feature debt-assessment-agent
/plan-feature user-authentication
```

---

## Purpose

Generate a complete, comprehensive Plan that provides ALL necessary context for a Claude Code agent to implement the feature successfully in one pass.

**Philosophy:** "Context is King" - The more context, references, patterns, and gotchas you provide upfront, the higher the success rate.

---

## Five-Phase Planning Process

### Phase 1: Feature Understanding

- Read Feature Requirements
- Assess Complexity (small/medium/large)
- Map Affected Systems

### Phase 2: Codebase Intelligence

- Search for Similar Features
- Identify Files to Reference (with specific line numbers)
- Note Existing Conventions
- Check Test Patterns

### Phase 3: External Research

- Library Documentation (include specific URLs)
- Implementation Examples
- Best Practices
- Common Pitfalls

### Phase 4: Strategic Thinking

- Architecture Fit
- Dependency Analysis
- Edge Cases
- Performance Implications
- Security Concerns
- Maintainability

### Phase 5: Plan Generation

Using the plan template, include:
- ALL context from phases 1-4
- Complete code examples (not pseudocode)
- Context reference table with specific line numbers
- Atomic tasks with IMPLEMENT/PATTERN/IMPORTS/GOTCHA/VALIDATE structure
- Validation commands for each task
- Confidence score (1-10)

---

## Output Location

Save plan as: `.agents/plans/{feature-name}.md`

---

## Quality Checklist

Before considering plan complete:

- [ ] Feature Understanding section complete
- [ ] Context References table with specific line numbers
- [ ] Patterns section with real code examples
- [ ] All tasks follow IMPLEMENT/PATTERN/IMPORTS/GOTCHA/VALIDATE structure
- [ ] Complete code blocks (not pseudocode)
- [ ] Testing Strategy defined
- [ ] Gotchas documented
- [ ] Acceptance Criteria checklist
- [ ] Validation commands specified
- [ ] Confidence score >= 8/10
- [ ] Saved to `.agents/plans/{feature-name}.md`

---

## Confidence Score

- 8-10: High confidence, one-pass success likely
- 6-7: Medium confidence, minor iterations expected
- 4-5: Low confidence, significant unknowns remain
- 1-3: Very low confidence, needs more research

**If score < 8, improve by:**
- Adding more context references
- Including more code examples
- Researching unknowns
- Breaking down complex tasks further
- Documenting more gotchas

---

## Remember

**The goal is one-pass implementation success through comprehensive context.**

More context upfront = Fewer iterations during implementation = Faster delivery.
