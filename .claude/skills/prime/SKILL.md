---
name: prime
description: Establish comprehensive codebase context before planning or implementation. Use at the start of new features or conversations.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(ls:*), Bash(pwd), Bash(find:*)
---

# Prime Command

**Establish comprehensive codebase context before planning or implementation.**

---

## Purpose

The Prime command establishes a complete understanding of the codebase, its patterns, conventions, and current state BEFORE any planning or implementation work begins.

**Philosophy:** "Context is King" - Understanding the system prevents assumptions, reduces errors, and accelerates development.

---

## When to Use Prime

Use Prime at the beginning of:
- **New conversations** - Start with full context
- **Major features** - Understand before planning
- **Refactoring work** - Know what exists before changing
- **Bug investigation** - Understand the system state
- **Team onboarding** - Accelerate new developer ramp-up
- **After long breaks** - Refresh understanding of codebase

---

## Prime Process

### Step 1: Analyze Project Structure

```bash
# Enumerate all tracked files
git ls-files | head -100

# Visualize directory hierarchy
find . -type d -maxdepth 3 ! -path "*/\.*" ! -path "*/node_modules/*" ! -path "*/venv_linux/*" | sort

# Count files by type
git ls-files | rg "\.(py|md|json|yaml|toml)$" | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

**Extract:**
- Project layout (app/, src/, tests/, docs/)
- Module organization (services, models, schemas, agents)
- Configuration locations (.env.example, pyproject.toml, configs/)
- Documentation structure (docs/, README.md, CLAUDE.md)

### Step 2: Read Core Documentation

Priority order:
1. CLAUDE.md - Development standards and conventions
2. README.md - Project overview and setup
3. .claude/PIV-LOOP.md - Development methodology
4. pyproject.toml - Dependencies and configuration
5. .env.example - Required environment variables

### Step 3: Identify Key Files

**Entry Points:**
```bash
rg "if __name__ == .__main__.:" --files-with-matches
rg "FastAPI\(" --files-with-matches
```

**Data Models:**
```bash
rg "class.*BaseModel" --files-with-matches -g "*.py"
```

**Services:**
```bash
ls -la app/services/ src/services/ 2>/dev/null
```

### Step 4: Understand Current State

```bash
git branch --show-current
git status
git log -10 --oneline --decorate
```

### Step 5: Map Architecture

- FastAPI routers
- Dependency injection patterns
- Pydantic validators
- Data flow
- External integrations

### Step 6: Review Recent Plans

```bash
ls -lt .agents/plans/*.md 2>/dev/null | head -5
ls -lt .agents/execution-reports/*.md 2>/dev/null | head -5
```

---

## Output: Context Report

Generate a comprehensive context report saved to:
```
.agents/init-context/{project-name}-context-{YYYY-MM-DD}.md
```

---

## Checklist

Before completing Prime, verify:

- [ ] Read CLAUDE.md completely
- [ ] Read README.md
- [ ] Analyzed directory structure
- [ ] Identified key files (entry points, models, services)
- [ ] Reviewed recent commits (last 10)
- [ ] Checked current branch and status
- [ ] Mapped architecture patterns
- [ ] Understood testing structure
- [ ] Reviewed recent plans (if any)
- [ ] Extracted naming conventions
- [ ] Generated context report
- [ ] Saved report to `.agents/init-context/`

---

## Success Criteria

A successful Prime produces a context report that:

- **Comprehensive** - Covers all major aspects of the codebase
- **Actionable** - Provides specific file references and line numbers
- **Current** - Reflects the actual state of the code
- **Scannable** - Easy to reference during planning/implementation
- **Preserved** - Saved for future reference and onboarding

**Result:** You understand the codebase well enough to plan features that align with existing patterns and conventions.
