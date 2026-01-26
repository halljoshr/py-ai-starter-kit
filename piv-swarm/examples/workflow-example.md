# PIV-Swarm Workflow Example

This document shows a complete workflow from feature request to completion.

---

## Feature: User Authentication

**Request:** "Add user authentication with JWT tokens"

---

## Session 1: Prime & Discuss

### Step 1: Prime

```bash
/piv:prime
```

**Output:** Context established, codebase analyzed.

- Found existing security.py with JWT helpers
- No existing auth endpoints
- User model needs to be created

### Step 2: Discuss

```bash
/piv:discuss user-authentication
```

**Questions & Decisions:**

| Question | Decision |
|----------|----------|
| Auth method? | JWT with refresh tokens |
| Token duration? | 15min access, 7 day refresh |
| Password storage? | bcrypt hashing |
| Session storage? | Stateless (no server-side storage) |

**Saved to:** `session.yaml` decisions field

---

## Session 1: Plan

### Step 3: Plan

```bash
/piv:plan
```

**Generated Tasks:**

| ID | Name | Priority | Blocked By | Est. Tokens |
|----|------|----------|------------|-------------|
| task-001 | Create User model | high | - | 10K |
| task-002 | Create User repository | high | task-001 | 12K |
| task-003 | Create Auth service | high | task-001 | 15K |
| task-004 | Create Login endpoint | high | task-002, task-003 | 15K |
| task-005 | Add integration tests | medium | task-004 | 10K |

**Total estimate:** 62K tokens (~2 sessions)

**Files created:**
- `.agents/tasks/task-001.yaml`
- `.agents/tasks/task-002.yaml`
- `.agents/tasks/task-003.yaml`
- `.agents/tasks/task-004.yaml`
- `.agents/tasks/task-005.yaml`

---

## Session 1: Execute (Tasks 1-2)

### Step 4: Execute

```bash
/piv:execute
```

**Task 001: Create User model**

1. Read existing patterns
2. Write tests first (TDD)
3. Implement User model
4. Run verification: ✓ PASSED
5. Commit: "feat(models): Create User model"

**Task 002: Create User repository**

1. Read existing repository pattern
2. Write tests first
3. Implement UserRepository
4. Run verification: ✓ PASSED
5. Commit: "feat(repo): Create User repository"

**Token usage:** 45K / 200K

### Step 5: Pause

```bash
/piv:pause
```

**Checkpoint created:**
- Tasks completed: 2/5
- Tokens used: 45K
- Next task: task-003
- Commit: "WIP: Pause point for user-authentication"

---

## Session 2: Resume & Complete

### Step 6: Resume

```bash
/piv:resume
```

**Loaded state:**
- Feature: user-authentication
- Completed: task-001, task-002
- Next: task-003

**Baseline tests:** ✓ All passing

### Step 7: Continue Execution

```bash
/piv:execute
```

**Task 003: Create Auth service**
- Implemented AuthService
- ✓ PASSED
- Commit: "feat(auth): Create Auth service"

**Task 004: Create Login endpoint**
- Implemented POST /auth/login
- ✓ PASSED
- Commit: "feat(api): Create Login endpoint"

**Task 005: Add integration tests**
- Wrote integration tests
- ✓ PASSED
- Commit: "test(auth): Add integration tests"

**All tasks complete!**

---

## Session 2: Validate

### Step 8: Validate

```bash
/piv:validate
```

**Results:**

| Stage | Status |
|-------|--------|
| Task Verification | ✓ 5/5 passed |
| Linting | ✓ 0 errors |
| Type Check | ✓ 0 errors |
| Unit Tests | ✓ 47 passed |
| Integration Tests | ✓ 12 passed |
| Coverage | ✓ 87% |

**Verdict:** ✓ PASSED - Ready for deployment

---

## Summary

| Metric | Value |
|--------|-------|
| Total Sessions | 2 |
| Total Tokens | ~95K |
| Tasks Completed | 5 |
| Tests Written | 17 |
| Coverage | 87% |
| Time | ~2 hours |

**Files Created:**
- `src/models/user.py`
- `src/repositories/user.py`
- `src/services/auth.py`
- `src/api/auth/routes.py`
- `src/api/auth/schemas.py`
- `tests/unit/test_user_model.py`
- `tests/unit/test_user_repository.py`
- `tests/unit/test_auth_service.py`
- `tests/unit/test_login_endpoint.py`
- `tests/integration/test_auth_flow.py`

**Commits:**
1. feat(models): Create User model
2. feat(repo): Create User repository
3. feat(auth): Create Auth service
4. feat(api): Create Login endpoint
5. test(auth): Add integration tests

---

## Key Learnings

1. **Fresh contexts work** - No context rot across sessions
2. **Task atomicity matters** - Each task independently verifiable
3. **Pause/resume seamless** - State perfectly preserved
4. **TDD enforced quality** - Tests written before code
5. **Atomic commits clean** - Easy to review and bisect
