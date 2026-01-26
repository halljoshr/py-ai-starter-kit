# PIV-Swarm: Prime Command

**Establish comprehensive codebase context before any planning or implementation.**

---

## Purpose

The Prime command establishes a complete understanding of the codebase, its patterns, conventions, and current state. This context enables high-quality planning and execution.

**Philosophy:** "Context is King" - Understanding the system prevents assumptions and reduces errors.

---

## Process

### Step 1: Initialize Session

```bash
# Check if session exists
cat .agents/state/session.yaml

# If no active session, initialize
# Update session.yaml with:
#   status: active
#   phase: prime
#   created_at: (current timestamp)
```

### Step 2: Verify Environment

```bash
# Verify working directory
pwd
ls -la

# Check git state
git branch --show-current
git status --short
git log -5 --oneline
```

### Step 3: Read Core Documentation

Priority order:
1. `CLAUDE.md` - Development standards
2. `README.md` - Project overview
3. `pyproject.toml` - Dependencies and configuration
4. `.env.example` - Required environment variables

### Step 4: Analyze Project Structure

```bash
# List tracked files
git ls-files | head -100

# Directory structure
find . -type d -maxdepth 3 -not -path "*/\.*" -not -path "*/venv*" | sort

# File types
git ls-files | sed 's/.*\.//' | sort | uniq -c | sort -rn | head -10
```

### Step 5: Identify Key Files

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

**Tests:**
```bash
find tests -name "test_*.py" 2>/dev/null | wc -l
```

### Step 6: Map Architecture

- Framework patterns (FastAPI routers, dependencies)
- Data flow (request → services → response)
- External integrations (APIs, databases)
- Testing approach (unit/integration/e2e)

### Step 7: Update State

```yaml
# Update .agents/state/session.yaml
session:
  phase: prime
  status: active

tokens:
  by_phase:
    prime: (tokens used)

# Update .agents/state/STATE.md
# - Session info
# - Current phase: Prime
```

### Step 8: Log Message

```yaml
# Add to .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: session_start
  content: "Prime complete. Codebase context established."
```

---

## Output

Generate context summary including:

1. **Project Overview** - Purpose, technologies, version
2. **Architecture** - Directory structure, patterns
3. **Key Files** - Entry points, models, services
4. **Current State** - Branch, recent commits, status
5. **Conventions** - Naming, testing, quality standards

Store summary in session for subsequent commands.

---

## Completion Criteria

- [ ] Session initialized in session.yaml
- [ ] Core documentation read
- [ ] Project structure analyzed
- [ ] Key files identified
- [ ] Architecture mapped
- [ ] State updated
- [ ] Message logged

---

## Next Command

After Prime, proceed to:
- `/piv:discuss {feature}` - Capture implementation preferences

---

## Token Budget

**Target:** 15-25K tokens
**Warning:** If exceeding 30K, summarize and checkpoint

---

## Single-Agent vs Swarm

| Mode | Behavior |
|------|----------|
| Single | Main agent performs all analysis |
| Swarm | Could spawn researcher agents for parallel analysis |

Current mode: **Single Agent**
