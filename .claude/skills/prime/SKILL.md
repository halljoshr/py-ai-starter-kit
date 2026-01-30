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

**Approach:** Shallow discovery, not deep reading. Build a map of WHERE things are, not WHAT they contain. Read specific files only when planning/implementation requires them.

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

**IMPORTANT:** Read ONLY these files. DO NOT read referenced documentation in `.claude/reference/` or `.claude/skills/` - those load on-demand when needed.

Priority order:
1. CLAUDE.md - Development standards and conventions (note reference files, don't read them)
2. README.md - Project overview and setup
3. pyproject.toml - Dependencies and configuration
4. .env.example - Required environment variables

**Explicitly SKIP:**
- `.claude/reference/**/*.md` - Reference docs (load on-demand)
- `.claude/skills/**/*.md` - Skill files (load on-invocation)
- `docs/**` - Full documentation (reference when needed)

### Step 3: Identify Key Files

**Entry Points (locate, don't read yet):**
```bash
rg "if __name__ == .__main__.:" --files-with-matches
rg "FastAPI\(" --files-with-matches
```

**Data Models (locate only):**
```bash
rg "class.*BaseModel" --files-with-matches -g "*.py"
```

**Services (locate only):**
```bash
ls -la app/services/ src/services/ 2>/dev/null
```

### Step 3.5: Sample Code Patterns (Read 1-2 examples)

**Read ONE entry point example (if exists):**
```bash
# Read the main application file to understand patterns
rg "FastAPI\(|if __name__" --files-with-matches -g "*.py" | head -1
```

**Read ONE service example (if services exist):**
```bash
# Read one service to see dependency injection, error handling patterns
ls app/services/*.py src/services/*.py 2>/dev/null | head -1
```

**Read ONE test example (if tests exist):**
```bash
# Read one test to understand testing patterns
find tests/unit -name "test_*.py" -type f 2>/dev/null | head -1
```

**Purpose:** Understand patterns in action without reading entire codebase. CLAUDE.md tells you conventions; these examples show them applied.

### Step 4: Understand Current State

```bash
git branch --show-current
git status
git log -10 --oneline --decorate
```

### Step 5: Map Architecture

**Use search patterns, NOT full file reads:**

```bash
# Find routers (don't read them yet)
rg "APIRouter|@app\.(get|post|put|delete)" --files-with-matches -g "*.py"

# Find Pydantic models (don't read them yet)
rg "class.*\(BaseModel\)" --files-with-matches -g "*.py"

# Find services (list only)
ls app/services/ src/services/ 2>/dev/null || echo "No services directory"
```

**Goal:** Build a mental map of WHERE things are, not WHAT they contain. Read specific files only when planning requires it.

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

- [ ] Read CLAUDE.md fully (note reference docs for later, don't read them now)
- [ ] Read README.md
- [ ] Read pyproject.toml
- [ ] Analyzed directory structure (using ls/find)
- [ ] Located key files using search patterns (--files-with-matches)
- [ ] Read 1-2 example files (entry point, service, or test) to see patterns
- [ ] Reviewed recent commits (last 10)
- [ ] Checked current branch and status
- [ ] Mapped architecture patterns (file locations + sampled examples)
- [ ] Understood testing structure (directory layout + one test example)
- [ ] Listed recent plans (if any exist)
- [ ] Extracted naming conventions from CLAUDE.md
- [ ] Generated context report with "read more" pointers
- [ ] Saved report to `.agents/init-context/`

---

## Success Criteria

A successful Prime produces a context report that:

- **Comprehensive** - Covers structure, conventions, and key patterns
- **Actionable** - Provides specific file references for deeper reading when needed
- **Current** - Reflects the actual state of the code
- **Scannable** - Easy to reference during planning/implementation
- **Balanced** - Enough context to start planning, not everything upfront
- **Preserved** - Saved for future reference and onboarding

**Result:** You understand the codebase well enough to plan features that align with existing patterns. For complex features, you know which reference docs to read for deeper context.
