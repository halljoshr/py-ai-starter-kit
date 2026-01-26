# PIV-Swarm: Plan Command

**Generate atomic tasks from discussion decisions.**

---

## Purpose

The Plan command transforms discussion decisions into a set of atomic, executable tasks. Each task is:
- Self-contained (can be executed independently)
- Verifiable (has clear success criteria)
- Ownable (can be assigned to an agent)

**Philosophy:** "Tasks as the atomic unit" - Small, clear, verifiable units of work.

---

## Process

### Step 1: Load Context

```yaml
# Read from .agents/state/session.yaml
- feature name
- all decisions from discuss phase
- any constraints
```

### Step 2: Update State

```yaml
# Update .agents/state/session.yaml
session:
  phase: plan
```

### Step 3: Identify Required Tasks

Based on feature and decisions, identify all tasks needed:

1. **Setup Tasks**
   - File creation
   - Configuration changes
   - Dependency additions

2. **Model Tasks**
   - Data models
   - Schemas
   - Validators

3. **Service Tasks**
   - Business logic
   - External integrations
   - Utilities

4. **API Tasks**
   - Endpoints
   - Request/response handling
   - Authentication/authorization

5. **Test Tasks**
   - Unit tests
   - Integration tests
   - Fixtures

6. **Documentation Tasks**
   - Code comments
   - API docs
   - README updates

### Step 4: Order Tasks by Dependency

Create dependency graph:
- Which tasks block others?
- Which can run in parallel?
- What's the critical path?

### Step 5: Create Task Files

For each task, create `.agents/tasks/task-{NNN}.yaml`:

```yaml
id: "task-001"
name: "Create User model"
status: pending
owner: null
phase: implementation
priority: high

files:
  - "src/models/user.py"
  - "tests/unit/test_user_model.py"

action: |
  Create User Pydantic model with fields:
  - id: UUID (auto-generated)
  - email: EmailStr (unique)
  - hashed_password: str
  - created_at: datetime
  - is_active: bool (default True)

  Include validators:
  - Email format validation
  - Password not stored in plain text

  Follow pattern from: src/models/base.py

verify: "uv run pytest tests/unit/test_user_model.py -v"
done: "User model validates email format and stores hashed passwords"

blocked_by: []
blocks:
  - "task-002"
  - "task-003"

created_at: "2026-01-26T10:00:00Z"
estimated_tokens: 10000
```

### Step 6: Generate Task Summary

Create task overview:

```markdown
## Task Plan: {feature-name}

**Total Tasks:** {N}
**Estimated Tokens:** {total}K
**Estimated Sessions:** {N} (at 40K per session)

### Dependency Graph

```
task-001 (User model)
    ├── task-002 (User repository)
    │   └── task-004 (Login endpoint)
    └── task-003 (Auth service)
        └── task-004 (Login endpoint)
            └── task-005 (Tests)
```

### Task List

| ID | Name | Priority | Blocked By | Est. Tokens |
|----|------|----------|------------|-------------|
| task-001 | Create User model | high | - | 10K |
| task-002 | Create User repository | high | task-001 | 12K |
| task-003 | Create Auth service | high | task-001 | 15K |
| task-004 | Create Login endpoint | high | task-002, task-003 | 15K |
| task-005 | Add integration tests | medium | task-004 | 10K |

**Total:** 62K tokens (~2 sessions)
```

### Step 7: Update Session State

```yaml
# .agents/state/session.yaml
tasks:
  total: 5
  pending: 5
  in_progress: 0
  completed: 0
  ids:
    pending: ["task-001", "task-002", "task-003", "task-004", "task-005"]
```

### Step 8: Update STATE.md

```markdown
## Tasks

### Pending
- [ ] task-001: Create User model (high)
- [ ] task-002: Create User repository (high, blocked by task-001)
- [ ] task-003: Create Auth service (high, blocked by task-001)
- [ ] task-004: Create Login endpoint (high, blocked by task-002, task-003)
- [ ] task-005: Add integration tests (medium, blocked by task-004)

### Progress
```
Planned: 5 tasks
Ready to execute: 1 (task-001)
```
```

### Step 9: Log Message

```yaml
# .agents/state/messages.yaml
- from: orchestrator
  to: all
  type: status_update
  content: |
    Planning complete for: user-authentication
    Tasks created: 5
    Estimated tokens: 62K
    Ready for execution.
```

---

## Task Quality Checklist

For each task, verify:

- [ ] **Atomic** - Single responsibility, completable in one session
- [ ] **Clear** - Unambiguous action description
- [ ] **Verifiable** - Has verify command and done criteria
- [ ] **Sized** - Under 20K token estimate
- [ ] **Dependent** - Dependencies explicitly listed
- [ ] **Pattern** - References existing code patterns where applicable

---

## Output

1. Individual task files in `.agents/tasks/`
2. Task summary in STATE.md
3. Updated session.yaml with task tracking
4. Message logged

---

## Completion Criteria

- [ ] All required tasks identified
- [ ] Tasks ordered by dependency
- [ ] Each task has verify and done criteria
- [ ] Task files created
- [ ] Session state updated
- [ ] STATE.md shows task list
- [ ] Total estimate reasonable (<100K for single feature)

---

## Next Command

After Plan, proceed to:
- `/piv:execute` - Execute tasks

---

## Token Budget

**Target:** 10-20K tokens
**Warning:** If planning exceeds 25K, task list may be too large - consider splitting feature

---

## Single-Agent vs Swarm

| Mode | Behavior |
|------|----------|
| Single | Orchestrator creates all tasks |
| Swarm | Could spawn planner + checker agents for verification |

Current mode: **Single Agent**
