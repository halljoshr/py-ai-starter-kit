---
name: execution-report
description: Post-implementation feedback loop to improve future planning. Documents successes, difficulties, and deviations.
disable-model-invocation: true
argument-hint: "{plan-file}"
allowed-tools: Read, Write, Glob, Grep, Bash(git:*)
---

# Execution Report Command

**Post-implementation feedback loop to improve future planning.**

---

## Arguments

```
/execution-report {plan-file}
```

**Example:**
```
/execution-report .agents/plans/hubspot-webhook-validation.md
```

---

## Purpose

Generate comprehensive report after implementing a plan to:
- Document what worked well
- Identify what was difficult
- Track deviations from plan
- Recommend improvements for future planning

**Philosophy:** "Learn from every implementation" - Feedback loops improve planning quality over time.

---

## Report Structure

Save to: `.agents/execution-reports/{feature-name}-report-{date}.md`

### Sections

1. **Metadata** - Feature, plan confidence score, actual success, dates
2. **Changes Summary** - Files added/modified/deleted, line counts
3. **Validation Results** - Final validation status, test results, coverage
4. **Task Execution** - Status of each task, duration, issues
5. **Successes** - What went well
6. **Difficulties** - What was challenging, time lost, lessons
7. **Deviations from Plan** - Type, what changed, reason, impact
8. **Recommendations** - For future planning, implementation, documentation
9. **Metrics** - Plan accuracy, quality metrics, time metrics
10. **Overall Assessment** - Plan quality score, one-pass success

---

## Metrics to Track

### Plan Accuracy
- Tasks as planned vs actual
- Number of deviations
- Unexpected issues
- Time estimation accuracy

### Quality Metrics
- First-time validation pass rate
- Coverage achieved
- Tests added
- Code quality (linting/typing)

### Time Metrics
- Planned vs actual duration
- Breakdown (implementation, debugging, validation)
- Variance percentage

---

## When to Generate Report

- After completing feature implementation
- After all validation passes
- Before creating PR
- After fixing bugs (for bug-fix plans)

---

## Remember

"Every implementation teaches us how to plan better" - Close the feedback loop.
