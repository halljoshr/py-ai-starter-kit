---
name: prime-deep
description: Establish deep codebase context by reading actual implementation files. Use when you need comprehensive understanding of the code itself.
disable-model-invocation: true
allowed-tools: Read, Glob, Grep, Bash(git:*), Bash(ls:*), Bash(pwd), Bash(find:*)
---

# Prime Deep Command

**Establish comprehensive understanding of actual implementation code.**

---

## Purpose

Prime Deep reads the actual codebase files to build complete context of implementation details, patterns in practice, and code architecture. Unlike `/prime` (which samples), this reads most key files.

**Philosophy:** "Deep context for deep work" - When planning major features or refactoring, understanding the full codebase prevents conflicts and ensures consistency.

**Trade-off:** Higher context cost (50K+ tokens) for comprehensive code understanding.

---

## When to Use Prime Deep

Use Prime Deep when:
- **Major refactoring** - Need to understand all affected areas
- **Complex feature** - Touches multiple modules
- **Architecture decisions** - Need full picture before designing
- **Initial deep dive** - First time working with unfamiliar codebase
- **System-wide changes** - Authentication, logging, error handling patterns

**Don't use for:**
- Simple bug fixes
- Single-file changes
- Continuing existing work (context already established)

---

## Prime Deep Process

### Step 1: Read Core Documentation

**Core project files:**
```bash
# Read these directly
cat README.md
cat CLAUDE.md
cat pyproject.toml
cat .env.example 2>/dev/null || echo "No .env.example"
```

### Step 2: Analyze Structure

```bash
# Get comprehensive directory structure
find . -type d -maxdepth 4 \
  ! -path "*/\.*" \
  ! -path "*/node_modules/*" \
  ! -path "*/venv*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  | sort

# Count files by type
git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

### Step 3: Read Source Code

**CRITICAL EXCLUSIONS:**
- **SKIP `.claude/` directory** - Reference docs and skills load on-demand
- **SKIP `venv*/` directories** - Virtual environments
- **SKIP `node_modules/`** - Dependencies
- **SKIP `__pycache__/`, `*.pyc`** - Compiled files
- **SKIP `dist/`, `build/`** - Build artifacts

**Read application code:**
```bash
# Find all Python source files (excluding .claude/)
find . -name "*.py" -type f \
  ! -path "*/.claude/*" \
  ! -path "*/venv*" \
  ! -path "*/__pycache__/*" \
  ! -path "*/node_modules/*" \
  ! -path "*/dist/*" \
  ! -path "*/build/*" \
  | head -50
```

**Read in priority order:**
1. Entry points (`main.py`, `app.py`, `__main__.py`)
2. Core services (`app/services/**/*.py`, `src/services/**/*.py`)
3. Data models (`app/models/**/*.py`, `**/schemas/**/*.py`)
4. API routes (`app/routes/**/*.py`, `app/routers/**/*.py`)
5. Configuration (`config/*.py`, `app/config.py`)
6. Utilities (`app/utils/**/*.py`, `src/utils/**/*.py`)

### Step 4: Read Tests

**Test files (sample, don't read all):**
```bash
# Read representative tests from each tier
find tests/unit -name "test_*.py" | head -3
find tests/integration -name "test_*.py" | head -2
find tests/e2e -name "test_*.py" | head -1
```

### Step 5: Configuration Files

```bash
# Read configuration
cat pyproject.toml
cat setup.py 2>/dev/null || echo "No setup.py"
cat pytest.ini 2>/dev/null || echo "No pytest.ini"
cat .github/workflows/*.yml 2>/dev/null | head -1 || echo "No GH workflows"
```

### Step 6: Review Git State

```bash
git branch --show-current
git status --short
git log -10 --oneline --decorate --graph
```

---

## Output: Deep Context Report

Generate a comprehensive report saved to:
```
.agents/init-context/{project-name}-deep-context-{YYYY-MM-DD}.md
```

**Report sections:**
1. **Project Overview** - From README/CLAUDE.md
2. **Architecture Map** - Complete module structure
3. **Code Patterns Observed** - Common patterns in actual code
4. **Key Dependencies** - From pyproject.toml
5. **Test Coverage** - Testing structure and patterns
6. **Recent Changes** - Git history insights
7. **File Reference Index** - Quick lookup of where things are

---

## Checklist

Before completing Prime Deep, verify:

- [ ] Read CLAUDE.md and README.md fully
- [ ] Read pyproject.toml and configuration files
- [ ] Analyzed complete directory structure
- [ ] Read ALL entry points
- [ ] Read MOST service files (app/services/, src/services/)
- [ ] Read MOST model/schema files
- [ ] Read MOST API route files
- [ ] Read representative tests (3 unit, 2 integration, 1 e2e)
- [ ] Read core utility files
- [ ] Reviewed git status and recent commits
- [ ] **CONFIRMED skipped `.claude/` directory** (no reference docs or skills)
- [ ] **CONFIRMED skipped venv/node_modules/cache directories**
- [ ] Generated comprehensive context report
- [ ] Saved report to `.agents/init-context/`

---

## Success Criteria

A successful Prime Deep produces:

- **Comprehensive code understanding** - Know implementation details across modules
- **Pattern recognition** - See how conventions are applied consistently
- **Architectural clarity** - Understand data flow and dependencies
- **Context efficiency** - Avoided meta-documentation (.claude/) that loads on-demand
- **Actionable knowledge** - Can plan complex features without additional reads

**Context cost:** 50-80K tokens (significant but necessary for major work)

**Result:** Complete understanding of actual implementation code, ready for complex planning or system-wide changes.

---

## When to Use Each Prime Command

| Command | Context Cost | When to Use |
|---------|--------------|-------------|
| `/prime` | 10-18K tokens | Daily work, feature planning, continuation |
| `/prime-deep` | 50-80K tokens | Major refactoring, complex features, initial deep dive |

**Rule of thumb:** Start with `/prime`. Use `/prime-deep` only when planning reveals you need broader code context.
