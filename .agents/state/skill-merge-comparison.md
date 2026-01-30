# Skill Merge Comparison: tmp-piv → py-ai-starter-kit

**Date:** 2026-01-28

---

## Summary

### NEW Skills in tmp-piv (Need to copy - 7 skills)
| Skill | Lines | Purpose |
|-------|-------|---------|
| pause | 84 | Checkpoint session state mid-feature |
| resume | 107 | Restore session and continue work |
| status | 80 | Show current feature progress |
| task-complete | 124 | Mark task as complete with results |
| task-create | 130 | Create individual task-NNN.yaml files |
| task-list | 92 | List all tasks with status |
| task-update | 109 | Update task status and metadata |

**Action:** Copy all 7 skills directly.

---

### IDENTICAL Skills (No action needed - 3 skills)
| Skill | Lines | Status |
|-------|-------|--------|
| plan | 419 | Exact match - no differences |
| execute | 491 | Exact match - no differences |
| spec | 559 | Exact match - no differences |

**Action:** Keep as-is.

---

### KEEP py-ai-starter-kit Version (Better/Updated - 3 skills)
| Skill | py-ai Lines | tmp-piv Lines | Reason |
|-------|-------------|---------------|--------|
| **prime** | 187 | 119 | **Just updated by user - DO NOT OVERWRITE** |
| **prime-deep** | 192 | n/a | **Just updated by user - DO NOT OVERWRITE** |
| **discuss** | 433 | 142 | py-ai version has extensive skill improvement framework, meta phase, evaluation criteria. Much more comprehensive. |

**Action:** Keep current versions.

---

### DECISION NEEDED: validate (Different approaches)

#### Current py-ai-starter-kit (122 lines)
**Type:** Generic quality gates
**Focus:** Standalone validation tool
**Features:**
- Arguments: `--full`, `--coverage`
- 4 stages: linting, type check, unit tests, coverage
- Optional 6 stages with `--full`: + e2e tests, security
- Independent - doesn't use PIV-Swarm state
- Good for: Daily dev, quick checks, pre-commit

**Philosophy:** "Catch issues early" - Quality gates

#### tmp-piv Version (201 lines)
**Type:** PIV-Swarm integrated validation
**Focus:** End-of-feature verification
**Features:**
- Loads session.yaml state
- Checks all tasks completed
- Runs verify command from each task file
- Quality checks (ruff, mypy, pytest, coverage)
- Requirements verification from discuss phase
- Generates validation report
- Updates session state
- Good for: End of execute phase, final validation

**Philosophy:** "Trust but verify" - Systematic confirmation

---

## Recommendation

### Option 1: Replace validate (Keep one)
Replace py-ai-starter-kit validate with tmp-piv version since PIV-Swarm needs state-aware validation.

**Pros:** Single validate skill, integrated with workflow
**Cons:** Lose standalone quick validation

### Option 2: Keep both (Rename one)
- Keep py-ai-starter-kit as `/validate` (quick checks)
- Copy tmp-piv as `/validate-feature` or `/validate-piv` (end-of-cycle)

**Pros:** Both use cases covered
**Cons:** Two similar skills, potential confusion

### Option 3: Merge capabilities
Create single validate skill that:
- Accepts `--quick` for standalone checks
- Accepts `--feature` for PIV-Swarm integrated validation
- Auto-detects if session.yaml exists

**Pros:** Best of both worlds
**Cons:** More complex, needs implementation

---

## Recommended Action Plan

1. **Copy NEW skills from tmp-piv** (7 skills)
   ```bash
   cp -r /home/jhall/Projects/tmp-piv/.claude/skills/{pause,resume,status,task-*} \
         /home/jhall/Projects/py-ai-starter-kit/.claude/skills/
   ```

2. **Keep existing skills** unchanged:
   - prime (just updated)
   - prime-deep (just updated)
   - discuss (more comprehensive)
   - plan, execute, spec (identical)

3. **Decide on validate approach** (User choice):
   - [ ] Option 1: Replace with tmp-piv version
   - [ ] Option 2: Keep both (rename tmp-piv to validate-feature)
   - [ ] Option 3: Merge into unified skill

---

## Files Not in Comparison

**py-ai-starter-kit only** (Keep - not in tmp-piv):
- code-review (106 lines)
- code-review-since (102 lines)
- commit (107 lines)
- execute-prp (48 lines)
- execution-report (91 lines)
- generate-prp (74 lines)
- implement-fix (111 lines)
- implement-plan (127 lines)
- plan-feature (125 lines)
- rca (131 lines)

These are additional skills for the starter kit. Keep all.

---

## Next Steps

1. User decides on validate approach
2. Execute copy commands for NEW skills
3. Verify all skills load correctly
4. Test skill invocation
5. Update CLAUDE.md if needed
