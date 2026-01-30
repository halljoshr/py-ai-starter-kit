# Python AI Starter Kit

**A complete autonomous engineering workflow for Python projects using Claude Code.**

This starter kit provides a PIV-Swarm system - a collection of Claude Code skills that enable systematic, high-quality feature development with session persistence and multi-agent support.

---

## What is PIV-Swarm?

**PIV-Swarm** is a workflow methodology built on Claude Code skills:

```
Prime → Discuss → Spec → Plan → Execute → Validate → Commit
```

**Philosophy:** "Context is King" - Understand before acting, validate before proceeding, learn from every implementation.

---

## Quick Start

### 1. Clone This Repository

```bash
git clone <your-repo-url>
cd py-ai-starter-kit
```

### 2. Set Up Environment

```bash
# Create virtual environment
uv venv

# Install dependencies
uv sync
```

### 3. Start Building Features

```bash
# Start Claude Code in your project
claude

# Run the PIV workflow
/prime              # Understand codebase
/discuss feature-name  # Make design decisions
/spec feature-name     # Generate formal specification
/plan                  # Create task files
/execute               # Build with validation
/validate              # Final verification
/commit                # Semantic commit
```

---

## Core Workflow

### Prime: Understand the Codebase

```bash
/prime        # Standard context gathering
/prime-deep   # Deep analysis with cross-references
```

**What it does:**
- Analyzes project structure
- Identifies patterns and conventions
- Builds context for planning
- Captures technical decisions

### Discuss: Make Design Decisions

```bash
/discuss feature-name
```

**What it does:**
- Clarifies requirements
- Captures architectural decisions
- Reviews and improves existing skills
- Resolves ambiguities before planning
- Records decisions in `.agents/research/`

### Spec: Generate Formal Specification

```bash
/spec feature-name
```

**What it does:**
- Creates Anthropic XML specification
- Defines acceptance criteria
- Outlines implementation approach
- Saved to `.agents/specs/`

### Plan: Create Task Files

```bash
/plan
```

**What it does:**
- Converts spec into individual task files
- Creates `.agents/tasks/task-NNN.yaml` for each task
- Defines dependencies (blocked_by/blocks)
- Includes validation commands and skills per task
- Ready for multi-agent execution

### Execute: Build with Validation

```bash
/execute
```

**What it does:**
- Works through tasks sequentially
- Respects dependencies
- Runs validation commands after each task
- Invokes validation skills when specified
- Captures results in task files
- Updates session state

### Validate: Final Verification

```bash
/validate         # Auto-detect mode
/validate --quick # Quality gates only
/validate --full  # Include e2e + security
```

**What it does:**
- Verifies all tasks completed
- Runs task-specific verification commands
- Executes quality gates (ruff, mypy, pytest)
- Checks coverage (>= 80%)
- Generates validation report
- Updates session state

### Commit: Create Semantic Commit

```bash
/commit
```

**What it does:**
- Creates semantic commit message
- Follows conventional commits format
- Includes co-author attribution
- Runs pre-commit hooks

---

## Session Management

### Pause and Resume Work

```bash
/pause   # Checkpoint current state
# ... close session, come back later ...
/resume  # Restore and continue
```

**What it persists:**
- Current phase and progress
- Task status and results
- Design decisions
- Token usage
- Git state

### Check Progress

```bash
/status  # Show current feature status
```

**Shows:**
- Feature name and phase
- Tasks completed/remaining
- Token budget used
- Next recommended action

---

## Task Management

Work with individual tasks:

```bash
/task-list         # List all tasks
/task-create       # Create new task
/task-update       # Update task status
/task-complete     # Mark task done
```

**Task files** (`.agents/tasks/task-NNN.yaml`) include:
- Description and acceptance criteria
- Implementation steps
- Validation commands and skills
- Dependencies (blocked_by/blocks)
- Test results and token tracking

---

## Additional Skills

### Code Quality

```bash
/code-review              # Full codebase review
/code-review-since <ref>  # Review since commit
```

### Bug Workflow

```bash
/rca            # Root cause analysis
/implement-fix  # Implement bug fix
```

---

## Project Structure

```
your-project/
├── .claude/
│   ├── skills/              # 24 PIV-Swarm skills
│   ├── schemas/             # YAML schemas (task, session)
│   └── reference/           # Best practices docs
├── .agents/                 # Session state (created on first use)
│   ├── specs/               # Anthropic XML specifications
│   ├── tasks/               # Individual task-NNN.yaml files
│   ├── state/               # session.yaml, STATE.md
│   ├── research/            # Discussion and design notes
│   └── reports/             # Validation reports
├── src/                     # Your source code
├── tests/                   # Your tests
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── CLAUDE.md                # Instructions for Claude
├── README.md                # This file
└── pyproject.toml           # Project configuration
```

---

## Multi-Session Development

PIV-Swarm supports working on features across multiple sessions:

1. **Start Feature**: `/prime` → `/discuss` → `/spec` → `/plan`
2. **Work Session 1**: `/execute` (complete some tasks) → `/pause`
3. **Work Session 2**: `/resume` → `/execute` (continue) → `/pause`
4. **Final Session**: `/resume` → `/execute` → `/validate` → `/commit`

**State persists** in `.agents/` directory - commit it or use context handoff files.

---

## Multi-Agent "Swarm" Support

The system is designed for multiple agents to work collaboratively:

- **Individual task files** - Agents can claim specific tasks
- **Task dependencies** - blocked_by/blocks prevent conflicts
- **Task ownership** - Owner field tracks who's working on what
- **State persistence** - Shared state in `.agents/` directory
- **Token tracking** - Per-task budgets prevent overruns

---

## Customization

### Adjust for Your Stack

Edit `.claude/skills/` to match your project:
- Update validation commands in `/validate`
- Modify test structure in schemas
- Add custom skills for your workflow

### Extend the System

Create new skills in `.claude/skills/your-skill/SKILL.md`:

```yaml
---
name: your-skill
description: What your skill does
disable-model-invocation: true
allowed-tools: Read, Write, Bash
---

# Your Skill

Instructions for Claude...
```

---

## Best Practices

### Start Every Feature with /prime

**Don't skip priming** - it provides critical context for planning.

### Use /discuss for Ambiguity

**Resolve gray areas upfront** - saves time in implementation.

### Validate Frequently

```bash
/validate --quick  # During development
/validate          # After each task
/validate --full   # Before merging
```

### Commit Task Files

**Commit `.agents/` directory** to preserve state across sessions.

### Use /pause Between Sessions

**Checkpoint state** before closing Claude Code.

---

## Configuration

### CLAUDE.md

Contains instructions for Claude:
- Development philosophy (KISS, YAGNI)
- Code conventions and style
- Testing strategy
- When to read reference docs

**Edit CLAUDE.md** to match your project's conventions.

### Reference Documentation

15 best practice docs in `.claude/reference/`:
- FastAPI, Pydantic, Pytest patterns
- Security, performance, database standards
- Git workflow, changelog management
- And more

---

## Example Workflow

### Building a New Feature: User Authentication

```bash
# Session 1: Planning (15 minutes)
/prime
/discuss user-authentication
# → Decide: JWT tokens, email validation, rate limiting
/spec user-authentication
/plan
# → Creates 8 tasks in .agents/tasks/

/pause
# → Checkpoint state

# Session 2: Implementation (2 hours)
/resume
/status
# → Shows 8 tasks pending

/execute
# → Completes tasks 1-5, validates each
# → Task 6 blocked by external dependency

/pause
# → Checkpoint with 5/8 tasks done

# Session 3: Completion (1 hour)
/resume
/execute
# → Completes tasks 6-8

/validate
# → All checks pass, generates report

/commit
# → Creates semantic commit with all changes
```

---

## Troubleshooting

### Skills Not Loading

```bash
# Check skill structure
ls .claude/skills/*/SKILL.md

# Verify YAML frontmatter is valid
head -10 .claude/skills/prime/SKILL.md
```

### Session State Corrupted

```bash
# Inspect state
cat .agents/state/session.yaml

# Reset if needed (loses progress!)
rm -rf .agents/state/session.yaml
```

### Task Stuck/Blocked

```bash
/task-list              # See all tasks
/task-update task-003   # Manually update if needed
```

---

## Contributing

This starter kit is designed to evolve:

1. **Use PIV-Swarm to improve PIV-Swarm** (dogfooding)
2. **Share skill improvements** back to the community
3. **Add reference docs** for new patterns discovered
4. **Report issues** and suggest enhancements

---

## Philosophy

**PIV-Swarm Values:**

- **Context is King** - Always understand before acting
- **Decide Once, Execute Cleanly** - Resolve ambiguity upfront
- **Trust but Verify** - Validate at every stage
- **State Persistence** - Work across sessions seamlessly
- **Swarm-Ready** - Enable multi-agent collaboration
- **Smart Defaults** - Minimize user interaction

---

## License

MIT

---

## Getting Help

- Check `.claude/reference/` for best practices
- Review `.claude/skills/` for skill documentation
- Inspect `.agents/state/STATE.md` for current status
- Use `/status` to see progress
- Use `/help` to list all available skills

**Build better, faster, with AI assistance.**
