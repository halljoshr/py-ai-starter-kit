# PIV-Swarm: Task List Command

**List all tasks with status.**

---

## Usage

```bash
/piv:task:list
/piv:task:list --status pending
/piv:task:list --status completed
```

---

## Process

### Step 1: Read All Tasks

```bash
# Read all task files
ls .agents/tasks/*.yaml
```

### Step 2: Display Task List

```markdown
═══════════════════════════════════════════════════════════════
                       TASK LIST
═══════════════════════════════════════════════════════════════

## Summary

| Status | Count |
|--------|-------|
| Completed | 2 |
| In Progress | 1 |
| Pending | 2 |
| Blocked | 0 |
| Failed | 0 |
| **Total** | **5** |

---

## Completed ✓

| ID | Name | Tokens |
|----|------|--------|
| task-001 | Create User model | 10K |
| task-002 | Create User repository | 12K |

---

## In Progress ▶

| ID | Name | Owner | Started |
|----|------|-------|---------|
| task-003 | Create Auth service | main | 10:15 |

---

## Pending ○

| ID | Name | Priority | Blocked By |
|----|------|----------|------------|
| task-004 | Create Login endpoint | high | task-003 |
| task-005 | Add integration tests | medium | task-004 |

---

## Dependency Graph

```
task-001 ✓
├── task-002 ✓
│   └── task-004 ○ (waiting)
└── task-003 ▶ (in progress)
    └── task-004 ○ (waiting)
        └── task-005 ○ (waiting)
```

═══════════════════════════════════════════════════════════════
```

---

## Filter Options

### By Status

```bash
/piv:task:list --status pending
```

Shows only pending tasks.

### By Priority

```bash
/piv:task:list --priority high
```

Shows only high priority tasks.

### Ready to Execute

```bash
/piv:task:list --ready
```

Shows tasks that are pending with no blockers.

---

## Output

Formatted task list with:
- Summary counts
- Tasks grouped by status
- Dependency graph
- Blocking information
