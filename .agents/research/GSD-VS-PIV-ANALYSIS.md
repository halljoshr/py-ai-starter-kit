# GSD vs PIV Loop Analysis

**Created:** 2026-01-26
**Purpose:** Compare GET SHIT DONE (GSD) framework against our PIV Loop methodology to inform adoption/integration decisions.

---

## Executive Summary

**GSD** (Get Shit Done) is a mature, battle-tested meta-prompting system that solves many of the problems we're building toward in our Priority 1 goals. It offers automatic context management, multi-agent orchestration, and session persistence out of the box.

**Key Finding:** GSD implements most of our Priority 1 goals (session management, multi-session architecture, token budgets) as built-in features. The question is whether to adopt GSD, borrow its concepts, or continue building PIV independently.

---

## Framework Overview

### GET SHIT DONE (GSD)

- **Link:** https://github.com/glittercowboy/get-shit-done
- **Install:** `npx get-shit-done-cc`
- **Philosophy:** "The complexity is in the system, not in your workflow"
- **Core Problem Solved:** "Context rot" - quality degradation as context window fills

### PIV Loop (Ours)

- **Location:** py-ai-starter-kit
- **Philosophy:** "Context is King, Sessions are Natural, Quality is Non-Negotiable"
- **Core Problem Solved:** Systematic, high-quality AI-assisted development

---

## Workflow Comparison

### GSD: 6-Stage Workflow

```
1. /gsd:new-project      → PROJECT.md, REQUIREMENTS.md, ROADMAP.md, STATE.md
2. /gsd:discuss-phase N  → {phase}-CONTEXT.md
3. /gsd:plan-phase N     → {phase}-RESEARCH.md, {phase}-{N}-PLAN.md
4. /gsd:execute-phase N  → {phase}-{N}-SUMMARY.md, {phase}-VERIFICATION.md
5. /gsd:verify-work N    → {phase}-UAT.md
6. /gsd:complete-milestone → Archive, tag release
```

### PIV Loop: 3-Phase Workflow

```
1. /prime           → .agents/init-context/{project}-context-{date}.md
2. /plan-feature    → .agents/plans/{feature}.md
   /implement-plan  → Working code + deviations
3. /validate        → Quality gates (lint, type, test, coverage)
   /code-review     → Review before commit
   /commit          → Semantic commit
```

### Mapping

| GSD Stage | PIV Equivalent | Notes |
|-----------|---------------|-------|
| new-project | /prime | GSD more structured (generates multiple docs) |
| discuss-phase | (manual with Opus) | GSD formalizes preference capture |
| plan-phase | /plan-feature | Similar purpose, different output format |
| execute-phase | /implement-plan | GSD uses fresh context per task |
| verify-work | /validate + manual | GSD has UAT workflow built-in |
| complete-milestone | /commit + manual | GSD automates release tagging |

---

## Feature Comparison

### Context Management

| Feature | GSD | PIV Loop |
|---------|-----|----------|
| Fresh context per task | ✅ Automatic (200k per executor) | ❌ Manual (user starts new conversation) |
| Context rot prevention | ✅ Built-in | ❌ Relies on user discipline |
| State persistence | ✅ STATE.md | ❌ Not implemented (Priority 1 goal) |
| Session pause/resume | ✅ /gsd:pause-work, /gsd:resume-work | ❌ Not implemented |
| Token budget tracking | ✅ Implicit (never fills) | ❌ Not implemented (Priority 1 goal) |

**Winner: GSD** - Solves context management automatically

### Multi-Agent Orchestration

| Feature | GSD | PIV Loop |
|---------|-----|----------|
| Parallel research | ✅ 4 agents (stack, features, architecture, pitfalls) | ❌ Single agent |
| Planning verification | ✅ Planner → Checker → iterate loop | ❌ Manual review |
| Parallel execution | ✅ Multiple executors with fresh contexts | ❌ Sequential single agent |
| Verification agents | ✅ Verifier + Debugger agents | ❌ /validate command (single agent) |

**Winner: GSD** - Native multi-agent support

### Artifact Structure

| Artifact Type | GSD Location | PIV Location |
|--------------|--------------|--------------|
| Project context | .planning/PROJECT.md | .agents/init-context/ |
| Requirements | .planning/REQUIREMENTS.md | (in plan files) |
| Roadmap | .planning/ROADMAP.md | (in GOALS.md) |
| State tracking | .planning/STATE.md | (not implemented) |
| Research | .planning/research/ | .agents/research/ |
| Plans | .planning/{phase}-{N}-PLAN.md | .agents/plans/ |
| Execution summaries | .planning/{phase}-{N}-SUMMARY.md | .agents/execution-reports/ |
| Verification | .planning/{phase}-VERIFICATION.md | (in /validate output) |

**Comparable** - Both preserve artifacts, different organization

### Task Specification

**GSD: XML Structure**
```xml
<task type="auto">
  <name>Create login endpoint</name>
  <files>src/app/api/auth/login/route.ts</files>
  <action>Specific implementation steps</action>
  <verify>Testable condition</verify>
  <done>Success criteria</done>
</task>
```

**PIV: Markdown Structure**
```markdown
### Task 1: [FILE PATH]
- **IMPLEMENT:** What to build
- **PATTERN:** Reference to existing code (file:line)
- **IMPORTS:** Required modules
- **GOTCHA:** Non-obvious pitfalls
- **VALIDATE:** Specific test command
```

**GSD Advantage:** XML is more parseable, `<verify>` and `<done>` enforce testability
**PIV Advantage:** Markdown more human-readable, includes PATTERN and GOTCHA fields

### Git Integration

| Feature | GSD | PIV Loop |
|---------|-----|----------|
| Automatic commits | ✅ Per task (atomic) | ❌ Manual /commit |
| Semantic versioning | ✅ Built-in | ✅ /commit command |
| Git bisect friendly | ✅ One commit per task | ⚠️ Depends on user discipline |
| Revert granularity | ✅ Task-level | ⚠️ Depends on user discipline |

**Winner: GSD** - Automatic atomic commits

### Commands

**GSD Commands (22+)**
```
Core: new-project, discuss-phase, plan-phase, execute-phase, verify-work, audit-milestone, complete-milestone, new-milestone
Navigation: progress, help, update
Phase Management: add-phase, insert-phase, remove-phase, list-phase-assumptions, plan-milestone-gaps
Session: pause-work, resume-work
Utilities: settings, set-profile, add-todo, check-todos, debug, quick
Brownfield: map-codebase
```

**PIV Commands (12)**
```
Core: prime, plan-feature, implement-plan
Validation: validate, code-review, code-review-since, execution-report
Bug Fix: rca, implement-fix
Git: commit
Spec: generate-prp, execute-prp
```

**GSD Advantage:** More comprehensive command set, better phase management
**PIV Advantage:** Simpler, less to learn

---

## Goal Alignment Analysis

### Priority 1 Goals (Foundation)

| Goal | PIV Status | GSD Solution |
|------|------------|--------------|
| Spec Creation Process | Research complete, tooling pending | `discuss-phase` + `plan-phase` workflow |
| Session Management System | Not started | `STATE.md` + `pause-work`/`resume-work` |
| Multi-Session Architecture | Not started | Fresh 200k context per task execution |
| Token Budget Management | Not started | Implicit - never fills context |

**Assessment:** GSD provides all Priority 1 features out of the box.

### Priority 2 Goals (Core Skills)

| Goal | PIV Status | GSD Solution |
|------|------------|--------------|
| Comprehensive Skills Tree | 12 commands | 22+ commands with better phase management |
| JSON Features Tracking | Not started | `ROADMAP.md` + progress tracking |
| TDD Culture Enforcement | Not started | `<verify>` tags in XML tasks |
| Standard Development Flow | Documented | 6-stage container pattern |
| Profiling & Optimization | Not started | Not built-in |

**Assessment:** GSD covers most Priority 2 goals except profiling.

### Priority 3 Goals (Quality)

| Goal | PIV Status | GSD Solution |
|------|------------|--------------|
| Language-Specific Standards | Python complete | Not built-in (methodology-agnostic) |
| Project Ownership | Not started | Not built-in |
| Configurable Autonomy | Not started | `mode: yolo | interactive` setting |
| Standard Folder Structures | Python complete | `.planning/` structure defined |

**Assessment:** PIV has better reference documentation; GSD has autonomy settings.

---

## Strengths & Weaknesses

### GSD Strengths

1. **Automatic context management** - No manual session handling needed
2. **Multi-agent orchestration** - Parallel research, planning, execution
3. **Battle-tested** - Used by engineers at Amazon, Google, Shopify, Webflow
4. **Atomic commits** - Clean git history without user discipline
5. **Quick mode** - `/gsd:quick` for ad-hoc tasks
6. **Active development** - Regular updates, Discord community
7. **Cross-platform install** - `npx get-shit-done-cc`

### GSD Weaknesses

1. **Opinionated structure** - Must use `.planning/` folder
2. **Less reference documentation** - No equivalent to `.claude/reference/`
3. **No code review workflow** - No `/code-review` or `/code-review-since`
4. **XML format** - Less human-readable than markdown
5. **External dependency** - Relies on npm package

### PIV Strengths

1. **Comprehensive reference docs** - 15 best practices documents
2. **Code review workflow** - `/code-review`, `/code-review-since`
3. **Customizable** - Can modify commands directly
4. **Human-readable plans** - Markdown with PATTERN and GOTCHA fields
5. **Bug fix workflow** - `/rca` and `/implement-fix`
6. **No external dependencies** - Just `.claude/` folder

### PIV Weaknesses

1. **Manual context management** - User must start new conversations
2. **Single agent** - No parallel execution
3. **No state persistence** - Can't pause/resume work
4. **No token tracking** - Risk of context rot
5. **Not battle-tested** - Still in development

---

## Integration Options

### Option 1: Adopt GSD Completely

**Action:** Replace PIV with GSD
```bash
npx get-shit-done-cc
```

**Keep from PIV:**
- `.claude/reference/` documentation (copy to project)
- `/code-review` and `/code-review-since` concepts (request as GSD feature)

**Pros:**
- Immediate access to all Priority 1 features
- Battle-tested, community supported
- Less development work

**Cons:**
- Lose custom methodology
- Different file structure
- External dependency

### Option 2: Borrow Concepts into PIV

**Action:** Implement GSD features in PIV commands

**Concepts to borrow:**
1. `STATE.md` - Add to `/implement-plan` for session persistence
2. Fresh context per task - Document as best practice
3. XML task format - Consider for `/plan-feature` output
4. Atomic commits - Integrate into `/implement-plan`
5. `<verify>` tags - Add to task structure
6. Pause/resume - Add `/pause-work` and `/resume-work` commands

**Pros:**
- Keep custom methodology
- Cherry-pick best features
- No external dependency

**Cons:**
- More development work
- Reinventing the wheel
- May miss GSD improvements

### Option 3: Hybrid Approach

**Action:** Use GSD for execution, PIV for planning/review

**Workflow:**
1. PIV `/prime` - Establish context
2. PIV planning discussion with Opus
3. GSD `/gsd:plan-phase` - Create executable plan
4. GSD `/gsd:execute-phase` - Run with fresh contexts
5. PIV `/code-review` - Review before merge
6. PIV `/code-review-since` - Pre-push validation

**Pros:**
- Best of both worlds
- Keep review workflow
- Leverage GSD execution

**Cons:**
- Two systems to maintain
- Context switching
- Potential conflicts

### Option 4: Wait and Watch

**Action:** Continue PIV development, monitor GSD evolution

**Rationale:**
- GSD may add code review features
- Claude Code may add native features (see claude-sneakpeek)
- More time to evaluate real-world usage

**Pros:**
- No commitment yet
- Learn from GSD community
- Flexibility

**Cons:**
- Delayed benefits
- Continued manual context management
- Priority 1 goals remain unimplemented

---

## Recommendation

### Short Term (Next 2 Weeks)

**Try GSD on a real project.**

1. Install: `npx get-shit-done-cc`
2. Use on a small-medium feature (not critical path)
3. Document experience in `.agents/research/GSD-TRIAL-NOTES.md`
4. Compare to PIV workflow

### Decision Point (After Trial)

Evaluate based on:
- Did GSD's context management improve quality?
- Did multi-agent orchestration speed up work?
- Did you miss PIV's code review workflow?
- Did the XML format feel natural?
- Did atomic commits improve git history?

### Long Term Options

Based on trial results:

| If... | Then... |
|-------|---------|
| GSD significantly better | Adopt GSD, port reference docs |
| GSD better but missing features | Adopt GSD, request code review feature |
| PIV workflow preferred | Borrow GSD concepts into PIV |
| Both have merits | Hybrid approach |
| Neither satisfying | Wait for Claude Code native features |

---

## Key Takeaways

1. **GSD solves our Priority 1 goals** - Session management, multi-session, token budgets
2. **PIV has unique strengths** - Reference docs, code review, bug fix workflow
3. **Not mutually exclusive** - Could use GSD execution with PIV review
4. **Trial before commitment** - Real-world experience will inform decision
5. **Active space** - Both GSD and Claude Code (sneakpeek) evolving rapidly

---

## References

- GSD Repository: https://github.com/glittercowboy/get-shit-done
- PIV Loop Documentation: `.claude/PIV-LOOP.md`
- GOALS.md: Strategic roadmap with Priority 1-4 goals
- claude-sneakpeek: https://github.com/mikekelly/claude-sneakpeek (native multi-agent)

---

## Action Items

- [ ] Install GSD: `npx get-shit-done-cc`
- [ ] Select trial project (small-medium feature)
- [ ] Run complete GSD cycle (all 6 stages)
- [ ] Document experience in `.agents/research/GSD-TRIAL-NOTES.md`
- [ ] Make adoption decision based on trial

---

*This analysis should be updated after GSD trial completion.*
