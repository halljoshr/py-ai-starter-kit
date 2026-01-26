# PIV-Swarm: Swarm-Ready Development Framework

**Version:** 0.1.0 (Prototype)
**Status:** In Development
**Parent Project:** py-ai-starter-kit

---

## Overview

PIV-Swarm is a next-generation development framework designed to work with single-agent Claude Code today and multi-agent swarm mode in the future. It extends the PIV Loop methodology with:

- **Task-centric architecture** - Everything is a task with explicit ownership
- **Agent registry** - Track agents (one today, many tomorrow)
- **Message passing** - Communication patterns ready for swarm
- **State persistence** - Never lose progress between sessions

## Design Philosophy

```
"Design the abstraction now, swap the implementation later."
```

The same commands, state files, and workflow work in both modes:

| Today (Single Agent) | Future (Swarm Mode) |
|---------------------|---------------------|
| Sequential task execution | Parallel task execution |
| One agent in registry | Multiple agents |
| Messages logged | Messages sent between agents |
| Same interface | Same interface |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      ORCHESTRATOR                            │
│                                                              │
│   /prime ──→ /discuss ──→ /plan ──→ /execute ──→ /validate  │
│      │          │           │           │            │       │
│      ▼          ▼           ▼           ▼            ▼       │
│   context    decisions    tasks      results     approval    │
└─────────────────────────────────────────────────────────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │RESEARCHER│  │RESEARCHER│  │RESEARCHER│
        └──────────┘  └──────────┘  └──────────┘
              │              │              │
              └──────────────┼──────────────┘
                             ▼
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
        ┌──────────┐  ┌──────────┐  ┌──────────┐
        │ EXECUTOR │  │ EXECUTOR │  │ EXECUTOR │
        └──────────┘  └──────────┘  └──────────┘
                             │
                             ▼
                      ┌──────────┐
                      │ REVIEWER │
                      └──────────┘
```

---

## Directory Structure

```
piv-swarm/
├── README.md                     # This file
│
├── .agents/                      # State and artifacts
│   ├── state/
│   │   ├── STATE.md             # Human-readable current state
│   │   ├── session.yaml         # Machine-readable session data
│   │   ├── agents.yaml          # Agent registry
│   │   └── messages.yaml        # Message log
│   │
│   ├── tasks/                   # Individual task files
│   │   └── {task-id}.yaml       # One file per task
│   │
│   ├── plans/                   # Feature plans
│   │   └── {feature}-plan.md
│   │
│   ├── research/                # Research outputs
│   │   └── {topic}.md
│   │
│   └── execution-reports/       # Execution summaries
│       └── {feature}-report.md
│
├── .claude/
│   ├── commands/
│   │   ├── orchestrator/        # Main workflow commands
│   │   │   ├── prime.md
│   │   │   ├── discuss.md
│   │   │   ├── plan.md
│   │   │   ├── execute.md
│   │   │   └── validate.md
│   │   │
│   │   ├── agents/              # Agent role prompts
│   │   │   ├── researcher.md
│   │   │   ├── executor.md
│   │   │   ├── reviewer.md
│   │   │   └── debugger.md
│   │   │
│   │   ├── state/               # State management
│   │   │   ├── pause.md
│   │   │   ├── resume.md
│   │   │   ├── status.md
│   │   │   └── assign.md
│   │   │
│   │   └── tasks/               # Task management
│   │       ├── create.md
│   │       ├── update.md
│   │       ├── complete.md
│   │       └── list.md
│   │
│   └── schemas/                 # YAML schemas
│       ├── task.yaml
│       └── message.yaml
│
└── examples/                    # Example files
    ├── task-example.yaml
    └── workflow-example.md
```

---

## Core Concepts

### 1. Tasks

Everything is a **task** with explicit ownership and verification criteria.

```yaml
id: task-001
name: "Implement login endpoint"
status: pending
owner: null
phase: implementation
files:
  - src/api/auth/login.py
action: |
  Create POST /auth/login endpoint that accepts
  email and password, validates credentials,
  and returns a JWT token.
verify: "uv run pytest tests/unit/test_login.py"
done: "POST /auth/login returns valid JWT on success"
```

**Key fields:**
- `owner` - Which agent owns this task (null = unassigned)
- `verify` - Command to verify completion
- `done` - Human-readable success criteria

### 2. Agents

Agents are registered in `agents.yaml`:

```yaml
agents:
  - id: main
    role: orchestrator
    status: active
```

**Today:** One agent (main)
**Future:** Multiple agents (researcher-1, executor-1, etc.)

### 3. Messages

All communication logged for debugging and future swarm:

```yaml
messages:
  - from: orchestrator
    to: executor-1
    type: task_assignment
    content: "Assigned task-001"
```

### 4. State

`STATE.md` provides human-readable snapshot:

```markdown
# Current State

## Session
- Feature: user-authentication
- Phase: implementation
- Started: 2026-01-26

## Progress
- [x] Task 1: Create user model
- [ ] Task 2: Implement login endpoint  ← IN PROGRESS (owner: main)
- [ ] Task 3: Add JWT middleware

## Blockers
None
```

---

## Workflow

### Single-Agent Mode (Current)

```bash
# 1. Establish context
/piv:prime

# 2. Capture preferences
/piv:discuss "user authentication feature"

# 3. Generate tasks
/piv:plan

# 4. Execute tasks (sequential)
/piv:execute

# 5. Verify and review
/piv:validate
```

### Swarm Mode (Future)

Same commands, but `/piv:execute` spawns parallel agents:

```bash
/piv:execute --parallel
# Spawns: executor-1, executor-2, executor-3
# Each takes tasks from queue
# Orchestrator monitors progress
```

---

## Commands Reference

### Orchestrator Commands

| Command | Purpose |
|---------|---------|
| `/piv:prime` | Establish codebase context |
| `/piv:discuss {feature}` | Capture implementation preferences |
| `/piv:plan` | Generate tasks from discussion |
| `/piv:execute` | Run tasks (sequential now, parallel future) |
| `/piv:validate` | Verify all tasks complete and correct |

### State Commands

| Command | Purpose |
|---------|---------|
| `/piv:status` | Show current state |
| `/piv:pause` | Save state and pause work |
| `/piv:resume` | Resume from saved state |
| `/piv:assign {task} {agent}` | Assign task to agent |

### Task Commands

| Command | Purpose |
|---------|---------|
| `/piv:task:create {name}` | Create new task |
| `/piv:task:list` | List all tasks |
| `/piv:task:update {id} {status}` | Update task status |
| `/piv:task:complete {id}` | Mark task complete |

---

## State Files

### STATE.md

Human-readable current state. Updated automatically by commands.

### session.yaml

Machine-readable session data:

```yaml
feature: user-authentication
phase: implementation
started: 2026-01-26T10:00:00Z
current_task: task-002
token_estimate: 45000
tokens_used: 12000
```

### agents.yaml

Agent registry:

```yaml
agents:
  - id: main
    role: orchestrator
    status: active
    current_task: task-002
```

### messages.yaml

Communication log:

```yaml
messages:
  - id: msg-001
    timestamp: 2026-01-26T10:05:00Z
    from: orchestrator
    to: main
    type: task_assignment
    content: "Starting task-002: Implement login endpoint"
```

---

## Swarm Integration Plan

When swarm mode becomes available:

1. **Agent Spawning**
   - Replace sequential loop with TeammateTool
   - Spawn researcher/executor agents as needed

2. **Parallel Execution**
   - Multiple executors work simultaneously
   - Each agent claims tasks from queue

3. **Message Passing**
   - Messages sent to real agents (not just logged)
   - Agents can ask questions, report blockers

4. **Coordination**
   - Orchestrator monitors all agents
   - Handles task dependencies
   - Resolves conflicts

---

## Development Roadmap

### Phase 1: Foundation ✅
- [x] Directory structure
- [x] README documentation
- [ ] Task YAML schema
- [ ] STATE.md template
- [ ] Session/agents/messages YAML templates

### Phase 2: State Commands
- [ ] `/piv:status` command
- [ ] `/piv:pause` command
- [ ] `/piv:resume` command

### Phase 3: Task Commands
- [ ] `/piv:task:create` command
- [ ] `/piv:task:list` command
- [ ] `/piv:task:update` command
- [ ] `/piv:task:complete` command

### Phase 4: Orchestrator Commands
- [ ] `/piv:prime` command
- [ ] `/piv:discuss` command
- [ ] `/piv:plan` command
- [ ] `/piv:execute` command
- [ ] `/piv:validate` command

### Phase 5: Agent Prompts
- [ ] Researcher agent prompt
- [ ] Executor agent prompt
- [ ] Reviewer agent prompt
- [ ] Debugger agent prompt

### Phase 6: Swarm Integration
- [ ] TeammateTool integration
- [ ] Parallel execution
- [ ] Agent-to-agent messaging

---

## Contributing

This is a prototype within py-ai-starter-kit. Once stable, it may replace the current PIV Loop implementation.

**To test:**
1. Copy `piv-swarm/.claude/commands/` to your project's `.claude/commands/piv/`
2. Copy `piv-swarm/.agents/` structure to your project
3. Run commands with `/piv:` prefix

---

## References

- Parent: [py-ai-starter-kit](../)
- Research: [GSD-VS-PIV-ANALYSIS.md](../.agents/research/GSD-VS-PIV-ANALYSIS.md)
- Swarm Info: [claude-sneakpeek](https://github.com/mikekelly/claude-sneakpeek)
- GSD: [get-shit-done](https://github.com/glittercowboy/get-shit-done)
