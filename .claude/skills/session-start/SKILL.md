---
name: session-start
description: Interactive session starter that guides you through PIV-Swarm workflow selection
disable-model-invocation: false
allowed-tools: Read, AskUserQuestion
---

# Session Start - Interactive Workflow Guide

**Purpose:** Help user choose the right workflow at the start of each Claude Code session.

---

## Process

### Step 1: Determine Work Type

Use `AskUserQuestion` to understand what the user wants to accomplish:

```
Question: "What type of work are you starting?"
Options:
1. "New feature or module" → Go to PIV Workflow
2. "Bug fix or investigation" → Go to Bug Workflow
3. "Quick refactor or cleanup (<50 lines)" → Proceed directly
4. "Documentation updates" → Proceed directly
5. "Exploration or research" → Use /explore or /discuss
```

### Step 2: Route to Appropriate Workflow

**For New Feature/Module:**
- Explain PIV workflow: `/prime → /discuss → /spec → /plan → /execute → /validate → /commit`
- Recommend: "Let's start with `/prime` to understand the codebase."
- Offer to run `/prime` for them

**For Bug Fix:**
- Explain Bug workflow: `/rca → /implement-fix → /validate → /commit`
- Ask: "What's the bug or error you're seeing?"
- Recommend starting with `/rca`

**For Quick Changes:**
- Confirm scope: "You mentioned quick refactor. Is this <50 lines and <30 minutes?"
- If YES: "Okay, proceeding without formal workflow. What needs to change?"
- If NO: "This sounds larger. Should we use PIV workflow?"

**For Documentation:**
- Ask: "Are you documenting a design decision or just updating existing docs?"
- If design decision: "Consider using `/discuss` to capture the reasoning."
- If updating: "Proceed directly. Which docs need updating?"

**For Exploration:**
- Ask: "Are you exploring to plan a feature, or just learning the codebase?"
- If planning: Recommend `/discuss feature-name` to capture insights
- If learning: Recommend `/explore` with specific question

### Step 3: Remind About Anti-Patterns

Show common mistakes to avoid:

```
🚫 Anti-Patterns to Avoid:
- "Let me just quickly build this" → Leads to scope creep
- Adding features mid-implementation → Use /discuss to lock scope first
- "I'll add tests later" → Use /execute with task-by-task validation
- Skipping documentation → Design decisions get lost

✅ PIV Best Practices:
- Prime first = understand before acting
- Discuss = lock requirements, prevent refactoring
- Spec = contract that prevents scope creep
- Plan = atomic tasks with clear validation
- Execute = task-by-task with tests
- Validate = automated quality gates
```

### Step 4: Offer to Start Workflow

Ask: "Would you like me to run [recommended workflow step] now?"

If YES: Execute the recommended skill (e.g., `/prime`)
If NO: "Okay, let me know when you're ready. Type `/session-start` anytime to see this guide again."

---

## Example Interaction

**User opens Claude Code and runs `/session-start`**

**Claude:**
```
🚀 Session Start - Workflow Guide

What type of work are you starting?

[Option 1] New feature or module
[Option 2] Bug fix or investigation
[Option 3] Quick refactor (<50 lines)
[Option 4] Documentation updates
[Option 5] Exploration or research
```

**User selects:** "New feature or module"

**Claude:**
```
Great! For new features, we'll use the PIV-Swarm workflow:

1. /prime - Understand codebase (5-10 min)
2. /discuss - Clarify requirements and design (10-15 min)
3. /spec - Generate formal specification (5-10 min)
4. /plan - Break into atomic tasks (10-15 min)
5. /execute - Implement with validation (varies)
6. /validate - Quality gates (5-10 min)
7. /commit - Semantic commit (2 min)

📝 Recent Lesson Learned:
Last session (hubspot-integration), skipping PIV led to:
- Scope creep (added global CLI mid-stream)
- Refactoring needed ("continue the full refactor")
- ~70k extra tokens spent

5 minutes of /discuss saves 30 minutes of refactoring.

Would you like me to run /prime now to understand the codebase?

[Yes, run /prime] [No, I'll run it manually]
```

---

## Success Criteria

- User makes informed choice about workflow
- Anti-patterns are surfaced upfront
- User doesn't start coding without considering PIV
- Workflow feels helpful, not restrictive

---

## Notes

- Keep interaction <2 minutes total
- Be enthusiastic but not preachy
- Reference concrete examples (hubspot-integration)
- Emphasize time savings, not process compliance
