# 🚀 PIV-Swarm Session Checklist

**BEFORE YOU START CODING - RUN THE WORKFLOW!**

---

## Quick Decision Tree

```
New feature or task?
│
├─ YES → Follow PIV Workflow (below)
│
└─ NO → Quick fix/exploration → Proceed directly
```

---

## PIV-Swarm Workflow

**Copy/paste these commands as you work:**

```bash
# 1. PRIME - Understand codebase (5-10 min)
/prime

# 2. DISCUSS - Clarify requirements (10-15 min)
/discuss feature-name

# 3. SPEC - Generate formal specification (5-10 min)
/spec feature-name

# 4. PLAN - Break into tasks (10-15 min)
/plan-feature

# 5. EXECUTE - Implement with validation (varies)
/execute

# 6. VALIDATE - Quality gates (5-10 min)
/validate --full

# 7. COMMIT - Semantic commit (2 min)
/commit
```

---

## Common Mistakes to Avoid

❌ **"Let me just quickly build this..."** → Scope creep, refactoring, wasted tokens
❌ **"I'll add docs later..."** → Design decisions lost forever
❌ **"Tests can wait..."** → Bugs slip through, coverage drops
❌ **"One more feature..."** → Never-ending session, unclear what's done

✅ **"Let me /prime first"** → Understand context, follow patterns
✅ **"/discuss before coding"** → Lock down requirements, prevent scope creep
✅ **"Task-by-task with /execute"** → Clear progress, can pause/resume
✅ **"/validate before /commit"** → Confidence in quality

---

## When to Skip PIV

**Skip for:**
- Bug fixes (use /rca → /implement-fix instead)
- Documentation updates
- Tiny refactors (<50 lines)
- Experiments/spikes (mark as such)

**Always use PIV for:**
- New features
- New modules/services
- API changes
- Refactoring >100 lines

---

## Token Budget Awareness

- **Prime:** ~20k tokens
- **Discuss:** ~30k tokens
- **Spec:** ~10k tokens
- **Plan:** ~15k tokens
- **Execute:** ~20k-40k per task
- **Validate:** ~10k tokens
- **Commit:** ~5k tokens

**Typical feature:** 100k-200k tokens with PIV
**Without PIV:** 200k-350k tokens (scope creep + refactoring)

---

## Last Session Reminder

**What you built:** hubspot-integration/
**What went wrong:** Skipped PIV → scope creep (global CLI) → "full refactor" needed
**Lesson learned:** 5 minutes of /discuss saves 30 minutes of refactoring

---

**Need help?** Run `/help` or read `.claude/reference/piv-loop-methodology.md`
