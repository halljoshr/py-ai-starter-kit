---
name: task-list
description: List all tasks in the current PIV session with their status.
allowed-tools: Read, Glob
---

# PIV-Swarm: Task List

**List all tasks in the current session.**

---

## Process

### Step 1: Load Tasks

Read all task files from `.agents/tasks/*.yaml`

### Step 2: Display Task List

```markdown
## Tasks

### Summary

| Status | Count |
|--------|-------|
| Completed | 2 |
| In Progress | 1 |
| Pending | 3 |
| Blocked | 1 |
| Failed | 0 |
| **Total** | **7** |

### Completed

| ID | Name | Completed |
|----|------|-----------|
| task-001 | Create User model | 10:15 |
| task-002 | Create User repository | 10:30 |

### In Progress

| ID | Name | Owner | Started |
|----|------|-------|---------|
| task-003 | Create Auth service | main | 10:35 |

### Pending (Ready)

| ID | Name | Priority |
|----|------|----------|
| task-004 | Create Login endpoint | high |

### Pending (Blocked)

| ID | Name | Blocked By |
|----|------|------------|
| task-005 | Add integration tests | task-003, task-004 |

### Failed

(none)

---

## Dependency Graph

task-001 (done)
├── task-002 (done)
│   └── task-004 (ready)
│       └── task-005 (blocked)
└── task-003 (in progress)
    └── task-004 (ready)
```

---

## Filters

Show specific status:
```
/task-list --status pending
/task-list --status blocked
```

---

## Notes

- Tasks ordered by dependency and priority
- "Ready" means all blockers completed
- Use `/status` for session overview
