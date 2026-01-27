---
name: plan
description: Generate atomic task files from XML spec. Converts implementation steps to machine-readable tasks.
disable-model-invocation: true
argument-hint: "[spec-file]"
allowed-tools: Read, Write, Bash, Glob
---

# Plan: Generate Task Files from Spec

**Convert XML spec implementation steps into individual YAML task files.**

---

## Purpose

Read the Anthropic XML spec and generate individual task files for each `<step_N>` in `<implementation_steps>`. Each task becomes an independently executable unit with all context needed.

**Philosophy:** "Spec to tasks" - The XML spec defines WHAT to build, tasks define HOW to execute.

---

## Arguments

```
/plan [spec-file]
```

**Examples:**
```
/plan .agents/specs/analytics-pipeline-spec.txt
/plan
```

If no file specified, looks for most recent spec in `.agents/specs/`

---

## Process

### Step 1: Read Spec File

Load the XML specification:
- Find spec file (argument or latest in `.agents/specs/`)
- Parse `<implementation_steps>` section
- Extract all `<step_N>` blocks

### Step 2: Extract Step Information

For each `<step_N>`, extract:
- Task name (from `Task:` line)
- Duration estimate (from `Duration:` line)
- TDD flag (from `TDD:` line if present)
- Files to create/modify (from `Files:` section)
- Models/endpoints/methods (from structured sections)
- Actions list (from `Actions:` section)
- Patterns to follow (from `Patterns:` section)
- Validation commands (from `Validation:` section)

### Step 3: Determine Dependencies

Analyze steps to identify dependencies:
- Step 0 (setup) blocks nothing, blocked by nothing
- Step 1 (models) blocked by step 0
- Step 2 (database) blocked by step 1
- Step 3 (services) blocked by step 2
- etc.

**General rules:**
- Setup → Models → Database → Services → APIs → Tests
- Within same layer, tasks can be parallel

### Step 4: Create Task Files

Create `.agents/tasks/` directory if needed.

For each step, create `.agents/tasks/task-{NNN}.yaml`:

```yaml
id: task-001
name: {Task name from spec}
status: pending
owner: null
phase: {setup|models|services|api|tests}
priority: {high|medium|low}

duration_estimate: {from spec}
tdd: {true|false}

files:
  create:
    - {new files from spec}
  modify:
    - {existing files to modify}

models: {if specified in step}
  - ModelName
  - AnotherModel

endpoints: {if API step}
  - POST /api/v1/resource
  - GET /api/v1/resource/{id}

actions:
  - {action 1 from spec}
  - {action 2 from spec}
  - {action 3 from spec}

patterns:
  - {pattern reference 1}
  - {pattern reference 2}

validation:
  commands:
    - {validation command 1}
    - {validation command 2}
  skills:
    - name: code-review
      when: code_written
      args: null
    - name: validate
      when: always
      args: null
  success_criteria:
    - {criterion 1 from spec}
    - {criterion 2 from spec}

blocked_by: {list of task IDs}
blocks: {list of task IDs}

created_at: {current timestamp}
started_at: null
completed_at: null
estimated_tokens: {from duration estimate}
actual_tokens: null
notes: null

test_results:
  status: null
  last_run: null
  command_results: []
  skill_results: []
  overall_passed: null
  failure_reason: null
```

### Step 5: Calculate Totals

Sum up:
- Total tasks
- Total estimated tokens
- Tokens per phase
- Identify checkpoint boundaries (every 120-150K tokens)

### Step 6: Update Session State

Update `.agents/state/session.yaml`:

```yaml
session:
  phase: plan
  status: active

plan:
  spec_file: .agents/specs/analytics-pipeline-spec.txt
  total_tasks: 20
  total_estimated_tokens: 215000
  phases:
    - name: setup
      tasks: [task-001]
      tokens: 15000
    - name: models
      tasks: [task-002, task-003]
      tokens: 40000
    - name: services
      tasks: [task-004, task-005, task-006]
      tokens: 65000
  checkpoint_recommendations:
    - After task-008 (~140K tokens used)
    - After task-015 (~175K tokens used)

tasks:
  total: 20
  pending: 20
  in_progress: 0
  completed: 0
  ids:
    pending: [task-001, task-002, ...]
    in_progress: []
    completed: []
```

### Step 7: Update STATE.md

```markdown
## Tasks

### Pending (20)
- [ ] task-001: Setup project structure (setup, 15K tokens)
- [ ] task-002: Implement data models (models, 20K tokens)
- [ ] task-003: Database setup (database, 20K tokens)
...

### Task Summary
- Total: 20 tasks
- Estimated: 215K tokens (spans 2-3 sessions)
- Checkpoints recommended after: task-008, task-015

### Dependency Graph
```
task-001 (setup)
  └─> task-002, task-003 (models)
        └─> task-004 (database)
              └─> task-005, task-006, task-007 (services)
```
```

### Step 8: Display Summary

```markdown
## Plan Generated

**Spec:** analytics-pipeline-spec.txt
**Tasks Created:** 20
**Estimated Tokens:** 215K (2-3 sessions)

### Breakdown by Phase
| Phase | Tasks | Tokens |
|-------|-------|--------|
| Setup | 1 | 15K |
| Models | 2 | 40K |
| Services | 3 | 65K |
| APIs | 6 | 55K |
| Tests | 8 | 40K |

### Checkpoint Strategy
- **Checkpoint 1:** After task-008 (~140K used)
- **Checkpoint 2:** After task-015 (~175K used)
- **Final Session:** task-016 to task-020 (~50K)

### Next Steps
1. Review task files in `.agents/tasks/`
2. Run `/execute` to start implementation
3. Tasks execute in dependency order
4. System auto-pauses at checkpoints
```

---

## Task File Naming

- `task-001.yaml` through `task-NNN.yaml`
- Zero-padded to 3 digits for sorting
- Maps 1:1 with spec steps (step_0 = task-001, step_1 = task-002, etc.)

---

## Task Phases

| Phase | Purpose | Example Tasks |
|-------|---------|---------------|
| setup | Project structure, config | pyproject.toml, settings.py |
| models | Data models, schemas | Pydantic models, enums |
| database | DB setup, migrations | SQLAlchemy models, indexes |
| services | Business logic | Service classes, integrations |
| api | API endpoints | FastAPI routes, dependencies |
| tests | Testing | Unit, integration, performance |
| docs | Documentation | Docstrings, README updates |

---

## Priority Calculation

```
IF phase == "setup"
  → priority: high (blocks everything)
ELSE IF blocks > 3 other tasks
  → priority: high (critical path)
ELSE IF blocks 1-3 tasks
  → priority: medium
ELSE
  → priority: low (leaf task)
```

---

## Token Budget Planning

**Per-session budget:** 200K tokens
**Warning threshold:** 150K tokens
**Critical threshold:** 175K tokens

**Checkpoint recommendations:**
- Calculate cumulative token usage
- Suggest `/pause` at natural boundaries near 140-150K
- Ensure each session has clear start/stop points

**Example:**
```
Tasks 1-8: 140K tokens → Pause after task-008
Tasks 9-15: 145K tokens → Pause after task-015
Tasks 16-20: 50K tokens → Final session
```

---

## Validation

Plan is valid when:
- [ ] All spec steps converted to task files
- [ ] Each task has verify command
- [ ] Dependencies correctly identified
- [ ] Token estimates reasonable (10-40K per task)
- [ ] Checkpoint strategy defined
- [ ] Session state updated
- [ ] STATE.md shows all tasks

---

## Example Task File

```yaml
id: task-003
name: Implement ingestion service
status: pending
owner: null
phase: services
priority: high

duration_estimate: "1 session (~25K tokens)"
tdd: true

files:
  create:
    - src/services/ingestion.py
    - tests/unit/services/test_ingestion.py
  modify: []

models: []
endpoints: []

actions:
  - Write unit tests with mocked database
  - Implement single event insert method
  - Implement bulk insert with executemany()
  - Add error handling for duplicates
  - Add transaction management
  - Test edge cases (invalid data, rollback)

patterns:
  - .claude/reference/fastapi-best-practices.md
  - .claude/reference/error-handling-patterns.md

validation:
  commands:
    - uv run pytest tests/unit/services/test_ingestion.py -v
    - mypy src/services/ingestion.py
    - ruff check src/services/ingestion.py
  skills:
    - name: code-review
      when: code_written
      args: null
    - name: validate
      when: always
      args: null
  success_criteria:
    - All service methods tested
    - Error handling verified
    - 100% coverage for ingestion service
    - Type checking passes
    - 0 critical issues in code review

blocked_by: [task-002]
blocks: [task-004, task-005]

created_at: "2026-01-27T16:30:00Z"
started_at: null
completed_at: null
estimated_tokens: 25000
actual_tokens: null
notes: null

test_results:
  status: null
  last_run: null
  command_results: []
  skill_results: []
  overall_passed: null
  failure_reason: null
```

---

## Completion Criteria

- [ ] All `<step_N>` from spec converted to task-NNN.yaml
- [ ] Task files created in `.agents/tasks/`
- [ ] Dependencies correctly mapped
- [ ] Session state updated with task list
- [ ] STATE.md shows full task breakdown
- [ ] Checkpoint strategy documented
- [ ] Summary displayed to user

---

## Next Skill

After `/plan` completes: `/execute` to start implementation

---

## Notes

- One task file per implementation step
- Task files are independently executable
- All context for execution in the task file
- No need to re-read full spec during execution
- Supports pause/resume at task boundaries
- Ready for swarm-mode parallelization
