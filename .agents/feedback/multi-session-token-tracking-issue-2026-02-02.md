# Multi-Session Token Tracking Issue

**Date:** 2026-02-02
**Reporter:** User testing in `/home/jhall/Projects/starter-example`
**Status:** Critical design flaw identified

---

## Problem Summary

The PIV-Swarm multi-session system has a fundamental flaw in how it tracks token budgets across sessions, making it appear that tokens "carry over" when they shouldn't.

---

## What Happened (User Experience)

### Session 1
```bash
/execute
# Completed task-001 (~35K tokens)
# Completed task-002 (~58K tokens)
# Total session 1: ~93K tokens
# [User expected auto-checkpoint/pause here]
```

### Session 2 (New Conversation)
```bash
/execute
# User expected: Auto-resume from task-003 with fresh 0/200K budget
# What happened: Nothing - execute doesn't auto-resume

/resume-session
# Shows: "93,000 / 200,000 tokens used (46.5%)"
# User sees: "Wait, I'm starting a NEW session but it shows 93K used?"
```

**User's correct intuition:**
> "It feels like tokens are carrying over sessions like it is the total budget instead of just the context budget."

---

## Root Causes

### Issue 1: Token Budget Tracking Design Flaw

**Current implementation (`session.yaml`):**
```yaml
session:
  tokens_used: 93000      # Accumulates across ALL sessions
  tokens_budget: 200000   # Constant
```

**Visual displayed to user:**
```
93,000 / 200,000 tokens used (46.5%)
████████████████████░░░░░░░░░░░░░░░░░░░░ 46.5%
107,000 tokens remaining before warning threshold (150K)
```

**Why this is wrong:**
- The 200K budget is **per-conversation context window**, not cumulative
- Session 2 starts with a **fresh 0K / 200K budget**
- The 93K from Session 1 is **gone** (conversation ended)
- We should track cumulative cost separately for analytics ONLY

**What should be displayed in Session 2:**
```
Feature Total Cost: 93,000 tokens across 2 sessions
Current Session: 0 / 200,000 tokens (0%)
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%
200,000 tokens available for task-003
```

### Issue 2: Execute Doesn't Auto-Resume

**Current behavior:**
```bash
# New conversation, fresh context
/execute
# → Starts from scratch, ignores existing session.yaml
```

**Expected behavior:**
```bash
# New conversation, fresh context
/execute
# → Detects session.yaml exists with status: paused
# → Auto-loads session context
# → Continues from next_task: task-003
# → Shows: "Resuming feature: py-ai-starter-kit from task-003"
```

**Why this matters:**
- Users don't want to remember two commands (`/resume-session` then `/execute`)
- The `/execute` skill should be smart enough to know "am I resuming or starting fresh?"
- This is the "pit of success" design - make the right thing easy

### Issue 3: Checkpoint Recommendations vs Reality

**From `session.yaml`:**
```yaml
checkpoint_recommendations:
  - after_task: task-002
    reason: "After Spec creation (~90K tokens cumulative)"
    cumulative_tokens: 90000
```

**User completed task-002 at ~93K tokens.** The system should have:
1. Detected we hit the checkpoint recommendation
2. Auto-paused with message: "Checkpoint reached after task-002 (~93K tokens)"
3. Displayed resume instructions

**Instead:** Execution just... stopped? Or user manually paused? Unclear.

---

## Proposed Fixes

### Fix 1: Separate Token Tracking (CRITICAL)

**New `session.yaml` structure:**

```yaml
session:
  feature: py-ai-starter-kit
  phase: plan
  status: active               # or: paused
  created_at: "2026-02-02T00:00:00Z"
  last_updated: "2026-02-02T18:30:00Z"

  # Current session tracking (resets each conversation)
  current_session_number: 3
  current_session_tokens: 0           # Resets to 0 each new conversation
  current_session_budget: 200000      # Always 200K
  current_session_started: "2026-02-02T18:30:00Z"

  # Feature-level tracking (accumulates across all sessions)
  feature_total_tokens: 93000         # Sum of all completed sessions
  feature_total_cost_usd: 0.28        # At Sonnet 4 pricing

  # Session history
  session_history:
    - session: 1
      started: "2026-02-02T00:00:00Z"
      ended: "2026-02-02T10:30:00Z"
      tokens_used: 35000
      tasks_completed: [task-001]
      checkpoint_reason: "Checkpoint recommendation after task-001"

    - session: 2
      started: "2026-02-02T15:00:00Z"
      ended: "2026-02-02T18:18:30Z"
      tokens_used: 58000
      tasks_completed: [task-002]
      checkpoint_reason: "User-requested checkpoint for testing"

    - session: 3
      started: "2026-02-02T18:30:00Z"
      ended: null                     # Still active
      tokens_used: 0                  # Current session
      tasks_completed: []
      checkpoint_reason: null

  current_task: null
  next_task: task-003
```

**Display in Session 3:**
```markdown
## Session Resumed: py-ai-starter-kit

### Feature Progress
**Total Investment:** 93,000 tokens ($0.28 across 2 sessions)
**Completed:** task-001, task-002 (2/6 tasks)

### Current Session (Session 3)
**Budget:** 0 / 200,000 tokens (0%) - Fresh session
░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░ 0%

**Next Task:** task-003 (Session Management System)
**Est. Tokens:** ~60K (leaves 140K buffer)
**Checkpoint:** Recommended after this task (~150K cumulative feature cost)

### Ready to Continue?
Type `/execute` to proceed with task-003
```

### Fix 2: Make `/execute` Auto-Resume

**Add to `/execute` skill (Step 1: Startup Ritual):**

```markdown
### Step 1: Startup Ritual (ENHANCED)

**Check for existing session:**

1. Check if `.agents/state/session.yaml` exists
2. If exists:
   a. Read `session.status`
   b. If `status: paused`:
      - Display: "🔄 Resuming session for feature: {feature}"
      - Initialize current_session_tokens = 0 (fresh conversation)
      - Increment current_session_number
      - Update session.started timestamp
      - Continue to step 2 (load session context)
   c. If `status: active`:
      - Display: "✓ Continuing active session"
      - Continue to step 2
3. If not exists:
   - Display: "❌ No active session found. Run /plan first to create tasks."
   - Exit

**Load session context:**

1. Read `.agents/specs/{feature}-spec.txt` (understand context)
2. Read `.agents/state/session.yaml` (current progress)
3. Display session summary (see Fix 1 for format)
4. Run `git status && git log -3` (understand state)
5. Run `uv run pytest tests/unit/ -v --tb=short` (baseline validation)

Never start executing without startup ritual.
```

**Result:** Users just type `/execute` in new conversation and it "just works"

### Fix 3: Auto-Checkpoint on Recommendations

**Add to `/execute` skill (Step 16: Check Token Budget):**

```markdown
### Step 16: Check Token Budget (ENHANCED)

Calculate tokens used **in current session only**:
```yaml
current_session_tokens: session.current_session_tokens + task_actual_tokens
feature_total_tokens: session.feature_total_tokens + task_actual_tokens  # Separate!
```

**Check against checkpoint recommendations:**

```python
next_checkpoint = find_next_checkpoint_after_current_task(session.plan.checkpoint_recommendations)

if next_checkpoint and next_checkpoint.after_task == current_task_id:
    print(f"✓ Checkpoint recommendation reached after {current_task_id}")
    print(f"   Feature total: {feature_total_tokens}K tokens")
    print(f"   Recommendation: {next_checkpoint.reason}")
    print()
    print("💡 Consider pausing here to start fresh session for next phase.")
    print("   Continue? (y/n)")

    user_choice = input()
    if user_choice.lower() == 'n':
        run_pause_skill(reason=f"Checkpoint after {current_task_id}")
        return
```

**Token budget warning (per current session):**

- < 150K (75%): Continue to next task
- 150-175K (75-88%): ⚠️ Warning: "Current session at {tokens}K (75%). Consider checkpointing after current task."
- > 175K (88%): 🚨 **AUTO-CHECKPOINT:** Automatically run `/pause` skill

**Note:** These thresholds are for **current_session_tokens**, not feature_total_tokens.
```

---

## Impact Assessment

### User Confusion (HIGH)
- Users see "93K tokens used" in fresh session
- Creates impression tokens "carry over" (they don't)
- Makes 200K budget seem cumulative (it's not)
- **Fix priority:** CRITICAL - this breaks mental model

### Workflow Friction (MEDIUM)
- Users must remember `/resume-session` then `/execute`
- Two commands where one should suffice
- **Fix priority:** HIGH - usability issue

### Missed Checkpoints (LOW)
- System recommends checkpoints but doesn't enforce
- Users might blow past 150K in single session
- **Fix priority:** MEDIUM - nice-to-have

---

## Testing Plan

After implementing fixes:

### Test 1: Fresh Session Display
```bash
# Session 2, after task-002 completed in Session 1
/execute

# Expected output:
# Feature Total: 93,000 tokens ($0.28 across 2 sessions)
# Current Session: 0 / 200,000 (0%)
# Next: task-003
```

### Test 2: Auto-Resume
```bash
# New conversation, session.yaml exists with status: paused
/execute

# Expected: Auto-resumes without needing /resume-session
# Shows: "🔄 Resuming session for feature: py-ai-starter-kit"
```

### Test 3: Checkpoint Recommendation
```bash
# Complete task-003 (hits checkpoint recommendation at ~150K cumulative)
/execute

# Expected after task-003 completes:
# "✓ Checkpoint recommendation reached after task-003"
# "Feature total: 150K tokens"
# "Consider pausing here to start fresh session"
# "Continue? (y/n)"
```

### Test 4: Auto-Checkpoint
```bash
# In single session, approach 175K current session tokens
/execute

# Expected at 175K:
# "🚨 Token budget critical (175K / 200K)"
# "Auto-checkpointing for session health"
# [Runs /pause automatically]
```

---

## Breaking Changes

### For Users
- **session.yaml format changes** - Old sessions need migration
- **Token display changes** - Now shows two numbers (feature total vs current session)

### Migration Script Needed
```python
# migrate_session_yaml.py
def migrate_v1_to_v2(old_session):
    """Migrate old session.yaml format to new multi-session format."""
    return {
        'session': {
            'current_session_number': 2,  # Guess based on tasks completed
            'current_session_tokens': 0,
            'feature_total_tokens': old_session['tokens_used'],
            'session_history': [
                {
                    'session': 1,
                    'tokens_used': old_session['tokens_used'],
                    'tasks_completed': old_session['tasks']['ids']['completed'],
                    'ended': old_session['last_updated'],
                }
            ]
        }
    }
```

---

## Recommendation

**Implement in this order:**

1. **Fix 1 (Token Tracking)** - Critical, fixes user confusion
2. **Fix 2 (Auto-Resume)** - High priority, removes friction
3. **Fix 3 (Auto-Checkpoint)** - Medium priority, improves UX

**Timeline suggestion:**
- Fix 1: First Priority (breaks mental model)
- Fix 2: Second Priority (usability)
- Fix 3: Third Priority (nice-to-have)

**Backward compatibility:**
- Provide migration script for existing sessions
- Document breaking changes in CHANGELOG.md
- Consider this a "v2" of session management

---

## Additional Observations

### User's Intuition Was Correct
The user immediately identified the problem:
> "tokens are carrying over sessions like it is the total budget instead of just the context budget"

This shows the current design **violates the principle of least surprise**. Fix urgently.

### The "Resume" Command Is Redundant
With auto-resume in `/execute`, the `/resume-session` skill becomes:
- **Optional** - For viewing session state without executing
- **Alias** - Could just be `/status` with pretty formatting
- **Deprecated** - Most users would just use `/execute`

Consider making `/resume-session` an alias for `/status` after Fix 2 is implemented.

---

**Status:** Ready for implementation
**Assigned to:** (TBD)
**Tracking:** Link to task/issue when created
