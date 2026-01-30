# Context Handoff: PIV-Swarm Development

**Date**: 2026-01-28
**Project**: py-ai-starter-kit
**Feature**: Complete PIV-Swarm workflow development
**Session**: Continuing from skill design and architecture phase

---

## Current State

### What We're Building
**PIV-Swarm**: A complete autonomous engineering workflow for Python projects using Claude Code skills.

**Workflow**: Prime → Discuss → Spec → Plan → Execute → Validate → Resume

**Goal**: Create a "starter kit" that developers can clone to get:
- Complete skill-based workflow
- Session state management
- Task-based execution with validation
- Multi-session feature development
- Smart defaults with minimal interaction

---

## What Exists Now

### Skills Created (16 total)

**In py-ai-starter-kit/.claude/skills/:**
- ✅ `spec/` - Generate Anthropic XML specifications
- ✅ `plan/` - Convert spec to individual task YAML files
- ✅ `execute/` - Execute tasks with validation (commands + skills)
- ✅ `validate/` - Multi-stage quality gates
- ✅ `prime/` - Codebase context gathering
- ✅ `discuss/` - Just created (partial, needs completion)
- ✅ `code-review/`, `code-review-since/` - Code quality
- ✅ `commit/` - Git workflow
- ✅ `rca/`, `implement-fix/` - Bug workflow
- ✅ Other validation and reporting skills

**In tmp-piv/.claude/skills/ (reference implementation):**
- ✅ `discuss/` - Complete interactive design phase with skill improvement
- ✅ `pause/`, `resume/`, `status/` - Session management
- ✅ `task-create/`, `task-update/`, `task-list/`, `task-complete/` - Task management
- ✅ More polished versions of prime, execute, plan, spec, validate

### Schemas Created

**In .claude/schemas/:**
- ✅ `task.yaml` - Complete task structure with:
  - test_results (command_results + skill_results)
  - validation.commands and validation.skills
  - blocked_by/blocks dependencies
  - Token estimates and actuals

### Reference Documentation (15 files)

**In .claude/reference/:**
- All copied to both repos
- fastapi, pydantic, pytest, security, performance, etc.
- Best practices and patterns

---

## Key Design Decisions Made

### 1. Skills: Local vs Global
**Decision**: Keep PIV-Swarm skills LOCAL (in project .claude/skills/)
**Rationale**:
- Only YAML frontmatter loads initially (minimal context)
- Full content loads only when skill invoked
- Part of the product (starter kit deliverable)
- Should be versioned with project

### 2. Task Architecture
**Decision**: Individual task-NNN.yaml files (not single JSON like Anthropic)
**Rationale**: "Swarm-ready" - multiple agents can claim tasks independently

### 3. Validation Strategy
**Decision**: Both commands AND skills in validation
**Example**:
```yaml
validation:
  commands:
    - uv run pytest tests/unit/ -v
    - mypy src/
  skills:
    - name: code-review
      when: code_written
    - name: validate
      when: always
```

### 4. State Persistence
**Files that enable resume**:
- `.agents/specs/{feature}-spec.txt` - Anthropic XML spec
- `.agents/tasks/task-NNN.yaml` - Individual task files with ALL context
- `.agents/state/session.yaml` - Machine-readable state
- `.agents/state/STATE.md` - Human-readable overview
- `.agents/research/{feature}-discussion.md` - Discussion decisions

### 5. Session Management
**Token budgets**:
- 200K total per session
- 150K warning (75%)
- 175K critical (88%) - checkpoint required

**Checkpoint strategy**: Between tasks when possible, mid-task if emergency

---

## What Needs to Happen Next

### Immediate Task: Merge Skills

**From tmp-piv → py-ai-starter-kit, copy improved versions:**

1. `discuss/SKILL.md` - Enhanced with skill improvement framework
2. `pause/SKILL.md` - Session checkpoint
3. `resume/SKILL.md` - Session restoration
4. `status/SKILL.md` - Progress reporting
5. `task-*` skills - Task management (create, update, list, complete)

**Compare and merge:**
- `execute/` - tmp-piv has validation.skills invocation
- `plan/` - tmp-piv generates task files with validation.skills
- `spec/` - Check for differences
- `validate/` - Compare approaches

### Next: Dogfood PIV-Swarm

**Use our own system to build itself!**

```bash
# 1. Copy skills from tmp-piv
# 2. Run workflow
/prime          # Understand current state
/discuss        # Review skills, make decisions
/spec piv-swarm # Generate formal spec
/plan           # Create task files
/execute        # Build with validation
```

---

## Important Files to Review

### Current Directory Structure
```
/home/jhall/Projects/py-ai-starter-kit/
├── .claude/
│   ├── skills/           # 16 skills (some need updating)
│   ├── schemas/          # task.yaml complete
│   └── reference/        # 15 best practice docs
├── .agents/
│   └── state/            # No active session yet
├── CLAUDE.md             # Full project instructions
└── CLAUDE-TEMPLATE.md    # Template for new projects
```

### Reference Implementation
```
/home/jhall/Projects/tmp-piv/
├── .claude/skills/       # 13 polished skills
├── .agents/
│   ├── specs/            # (no spec file yet)
│   ├── tasks/            # task-001 through task-020
│   ├── state/            # session.yaml, STATE.md
│   └── research/         # discussion notes
└── Feature: analytics-project (20 tasks planned, 0 completed)
```

---

## Context You Have Available

### What User Has Provided
- Complete PIV-Swarm vision and requirements
- Anthropic research examples
- Smart defaults philosophy
- Swarm-ready architecture requirement
- Session state persistence needs
- Multi-session workflow support

### What We Discovered Together
- Skills load frontmatter only (context efficient)
- Need /discuss phase for skill improvement
- Test results capture is critical
- Validation skills must be invoked automatically
- Task files need ALL context for fresh agents
- Dependencies tracked via blocked_by/blocks

---

## User's Next Question/Request

User asked: "could you write a context switch example right now so I can try this in a different agent?"

**This file IS that example!**

---

## Instructions for New Agent

1. **Read this file** (you just did!)
2. **Verify current state**:
   ```bash
   cd /home/jhall/Projects/py-ai-starter-kit
   git status
   ls .claude/skills/*/SKILL.md
   ls .agents/
   ```

3. **Compare with reference**:
   ```bash
   ls /home/jhall/Projects/tmp-piv/.claude/skills/
   diff .claude/skills/execute/SKILL.md /home/jhall/Projects/tmp-piv/.claude/skills/execute/SKILL.md
   ```

4. **Ask user**:
   - "I've reviewed the context. We need to copy improved skills from tmp-piv. Should I proceed?"
   - Or: "What would you like to work on first?"
   - Or: "Ready to run /prime to kick off the PIV-Swarm build?"

---

## Questions a New Agent Might Have

**Q: What's the difference between tmp-piv and py-ai-starter-kit?**
A: tmp-piv is a test implementation (analytics project). py-ai-starter-kit is the "product" - the starter kit that users will clone.

**Q: Which skills are "correct"?**
A: tmp-piv has more refined versions from actual usage. Copy those, then enhance through /discuss.

**Q: Should I start executing tasks?**
A: No - no spec/plan exists yet for PIV-Swarm feature. Run the workflow: prime → discuss → spec → plan → execute.

**Q: What if the user wants to improve skills first?**
A: Perfect! That's what /discuss is for. Review skills, get user examples, make improvements.

**Q: What's in .agents/state/session.yaml format?**
A: See tmp-piv version as reference. Machine-readable YAML with tokens, tasks, decisions, git state.

---

## Success Criteria

PIV-Swarm is complete when py-ai-starter-kit has:
- [ ] All core skills working (prime, discuss, spec, plan, execute, validate, pause, resume)
- [ ] All task management skills (create, update, list, complete, status)
- [ ] Complete schemas (task.yaml and session.yaml)
- [ ] Session state management working
- [ ] Multi-session resume working
- [ ] Validation with both commands and skills
- [ ] Comprehensive documentation
- [ ] CLAUDE.md and CLAUDE-TEMPLATE.md ready
- [ ] Can dogfood itself (use PIV-Swarm to build features)

---

## Conversation Continuity

You're continuing a conversation where:
- We converted commands to skills
- Built out tmp-piv as a test
- Designed complete PIV-Swarm workflow
- Created discuss skill with skill improvement
- Decided skills should be local
- User wants to test context switching

**Next natural action**: Copy improved skills from tmp-piv, then either:
1. Improve skills through discussion + user examples, OR
2. Run full workflow to build PIV-Swarm formally

---

**Ready to continue!** What's your first move?
