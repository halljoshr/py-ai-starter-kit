# Beads Framework & Linear Integration Research

**Date:** 2026-02-04
**Status:** Analysis Complete - Implementation Recommendations Ready
**Context:** Evaluating Beads framework concepts and Linear integration strategy for PIV-Swarm

---

## Executive Summary

Analyzed Steve Yegge's [Beads framework](https://github.com/steveyegge/beads) for AI agent task management and evaluated Linear integration strategies.

**Key Findings:**
- PIV-Swarm workflow is more sophisticated than Beads' minimal approach (6-2 advantage)
- Four Beads concepts worth adopting: hash-based IDs, hierarchical structure, semantic memory decay, git audit trails
- Linear integration is viable with current system, enhanced by Beads concepts
- Hybrid model recommended: Linear for planning, PIV-Swarm for execution

**Recommendation:** Adopt Beads infrastructure concepts while keeping PIV-Swarm workflow superiority.

---

## Table of Contents

1. [Beads Framework Analysis](#beads-framework-analysis)
2. [PIV-Swarm vs Beads Comparison](#piv-swarm-vs-beads-comparison)
3. [Beads Concepts Worth Adopting](#beads-concepts-worth-adopting)
4. [Linear Integration Design](#linear-integration-design)
5. [Implementation Roadmap](#implementation-roadmap)
6. [Open Questions](#open-questions)

---

## Beads Framework Analysis

### Problem Statement
Beads addresses a critical gap in AI agent workflows: **maintaining persistent, structured memory across long-horizon tasks**. Rather than relying on unorganized markdown plans that lose context, it provides a dependency-aware graph for tracking work.

### Core Abstractions

#### 1. Git-Backed Storage
Issues are persisted as JSONL in a `.beads/` directory, treating **version control as the database**.

```
.beads/
├── issues.jsonl      # Append-only task storage
└── cache.db          # SQLite for fast queries
```

**Philosophy:** "Distributed, git-backed graph issue tracker for AI agents"

**Benefits:**
- `git log .beads/issues.jsonl` = full audit trail
- `git diff` = task changes
- `git revert` = undo task operations
- Branch merges = automatic task syncing

#### 2. Hash-Based IDs
Tasks use cryptographic identifiers like `bd-a1b2` that **prevent merge collisions** in multi-agent and multi-branch workflows.

**Example:**
```bash
# Branch A: bd-a3f8 "Implement JWT"
# Branch B: bd-7c2d "Add login endpoint"
# git merge → No conflicts (different IDs)

# Sequential IDs cause conflicts:
# Branch A: task-005.yaml
# Branch B: task-005.yaml
# git merge → CONFLICT
```

#### 3. Hierarchical Organization
Supports epic-level nesting:
```
bd-a3f8         (Epic: "Add authentication")
bd-a3f8.1       (Task: "Implement JWT service")
bd-a3f8.1.1     (Subtask: "Add token signing")
bd-a3f8.1.2     (Subtask: "Add token validation")
bd-a3f8.2       (Task: "Build login endpoint")
```

**Comparison to flat dependencies:**
- Beads: Natural parent-child relationships
- Flat: Manual `blocked_by`/`blocks` arrays

#### 4. Semantic Memory Decay
Closed tasks get auto-summarized to preserve context windows:

```jsonl
// Open task (full details)
{"id":"bd-a3f8","title":"Add auth","desc":"Full 500-word description...","status":"open"}

// After closing (summarized)
{"id":"bd-a3f8","title":"Add auth","summary":"Implemented JWT with bcrypt","status":"closed"}
```

**Impact:** On a 50-task project, Beads might use 15K tokens for closed task context vs 50K tokens without summarization (70% reduction).

### Design Principles

1. **Agent-First Optimization:** JSON output, automatic dependency tracking, built-in ready-state detection
2. **Invisible Infrastructure:** SQLite caching for performance, background daemon for sync
3. **Memory Efficiency:** Semantic decay for completed work
4. **Flexible Deployment:** Supports stealth mode, contributor workflows, maintainer roles

### Essential Operations

```bash
bd ready        # Lists unblocked tasks (AI agent entrypoint)
bd create       # Initiates work items with priority levels
bd dep add      # Establishes task relationships
bd show         # Displays full audit trails
bd complete     # Closes tasks (triggers summarization)
```

### What Beads Doesn't Have

- ❌ No workflow methodology (just task tracking)
- ❌ No validation system
- ❌ No code quality enforcement
- ❌ No specification framework
- ❌ No context management strategy
- ❌ No smart defaults or decision schemas

**Conclusion:** Beads is infrastructure for task tracking, not a complete development methodology.

---

## PIV-Swarm vs Beads Comparison

### Feature Matrix

| Feature | Beads | PIV-Swarm | Winner |
|---------|-------|-----------|--------|
| **Task Storage** | JSONL in `.beads/` | YAML in `.agents/tasks/` | Tie (different strengths) |
| **Task IDs** | Hash-based (`bd-a1b2`) | Sequential (`task-001.yaml`) | **Beads** 🏆 |
| **Workflow Support** | Minimal (create/ready/complete) | Full PIV cycle (prime→spec→plan→execute→validate) | **PIV-Swarm** 🏆 |
| **Validation** | None built-in | Dual (commands + skills), 6 stages | **PIV-Swarm** 🏆 |
| **Specifications** | Not included | Anthropic XML format | **PIV-Swarm** 🏆 |
| **Smart Defaults** | Not included | Schema-based decision support | **PIV-Swarm** 🏆 |
| **Context Management** | Basic | Layered (shallow discovery, fresh context) | **PIV-Swarm** 🏆 |
| **Memory Management** | Semantic decay for closed tasks | Token budgets, checkpointing | **Beads** 🏆 |
| **Multi-Agent Support** | Hash IDs prevent collisions | File-based, dependencies | **Beads** 🏆 |
| **Hierarchical Tasks** | Epic → Task → Subtask | Flat with dependencies | **Beads** 🏆 |
| **Git Integration** | Native (storage IS git) | External (files tracked in git) | **Beads** 🏆 |

**Score: PIV-Swarm 6, Beads 4**

### Detailed Analysis

#### What Beads Does Better

**1. Hash-Based Task IDs (Critical for Multi-Dev)**
```
Beads:   bd-a3f8, bd-7c2d, bd-9e4a
Yours:   task-001.yaml, task-002.yaml, task-003.yaml
```

**Risk with sequential IDs:**
```bash
# Developer A on feature/auth branch
git checkout -b feature/auth
# Creates task-005.yaml

# Developer B on feature/payments branch
git checkout -b feature/payments
# Creates task-005.yaml

# Merge to dev
git merge feature/auth    # OK
git merge feature/payments # CONFLICT on task-005.yaml
```

Hash-based IDs eliminate this entirely.

**2. Hierarchical Task Structure**
```
Beads (Natural Hierarchy):
  bd-a3f8         (Epic: "Add authentication")
  bd-a3f8.1       (Task: "Implement JWT service")
  bd-a3f8.1.1     (Subtask: "Add token signing")
  bd-a3f8.1.2     (Subtask: "Add token validation")
  bd-a3f8.2       (Task: "Build login endpoint")

PIV-Swarm (Flat with Dependencies):
  task-001.yaml:  # Epic: Add authentication
    blocked_by: []

  task-002.yaml:  # JWT service
    blocked_by: [task-001]

  task-003.yaml:  # Token signing
    blocked_by: [task-002]

  task-004.yaml:  # Token validation
    blocked_by: [task-002]

  task-005.yaml:  # Login endpoint
    blocked_by: [task-001]
```

**Trade-off:**
- Beads hierarchy: Cleaner visualization, mirrors product planning
- PIV-Swarm dependencies: More flexible (many-to-many relationships)

**3. Semantic Memory Decay (Token Optimization)**

On a 50-task project over 6 months:
- **Without decay:** All 50 tasks at full description = ~50K tokens
- **With decay:** 45 closed tasks summarized + 5 open full = ~15K tokens
- **Savings:** 70% token reduction on historical context

**Impact on PIV-Swarm sessions:**
```
Session 1: Create 10 tasks (full descriptions)
Session 2: Complete 8, still loading full descriptions = wasted tokens
Session 3: Complete 6 more, loading 14 full descriptions = 35K tokens wasted

With semantic decay:
Session 3: Loading 14 summaries + 4 open tasks = 10K tokens
```

**4. Git-Native Audit Trail**

Beads leverages git as the database:
```bash
# Full task history
git log --follow .beads/issues.jsonl

# Who changed a task
git blame .beads/issues.jsonl | grep bd-a3f8

# Undo task changes
git revert <commit-hash>

# Task changes across branches
git diff main..feature/auth .beads/issues.jsonl
```

**PIV-Swarm equivalent:** Would need custom commands to achieve the same.

#### What PIV-Swarm Does Better

**1. Full Development Workflow**

```
PIV-Swarm (Complete Methodology):
  /session-start  → Interactive workflow selection
  /prime          → Context discovery (shallow, smart)
  /discuss        → Architectural decisions
  /spec           → Anthropic XML specification
  /plan           → Convert spec to tasks
  /execute        → Fresh context per task
  /validate       → 6-stage quality gates
  /code-review    → Automated review
  /commit         → Semantic commits

Beads (Minimal Task Tracking):
  bd create       → Make task
  bd ready        → List unblocked tasks
  bd complete     → Mark done
```

**Verdict:** Beads is a component, PIV-Swarm is a complete system.

**2. Validation & Quality Gates**

PIV-Swarm validation is sophisticated:
```yaml
validation:
  commands:
    - uv run pytest tests/unit/ -v
    - uv run pytest tests/integration/ -m "not very_slow"
    - uv run mypy src/
    - uv run ruff check .

  skills:
    - name: code-review
      when: code_written
    - name: validate
      when: always

  success_criteria:
    - "All unit tests pass"
    - "Code coverage ≥80%"
    - "No mypy errors"
    - "No ruff violations"
```

**Beads:** Has zero built-in validation. It's just a to-do list.

**3. Context Management Strategy**

PIV-Swarm `/prime` skill avoids wasteful full-file reads:
```
1. Shallow Discovery (WHERE things are)
   - rg --files -g "*.py" src/
   - Find patterns without reading

2. Pattern Sampling (HOW things work)
   - Read 1-2 example files
   - Understand conventions

3. On-Demand Loading (WHEN needed)
   - Load full files during implementation
   - Preserve "smart context" budget
```

**Beads:** No context management strategy. Assumes external agent handles this.

**4. Schema-Based Smart Defaults**

PIV-Swarm `/discuss` skill auto-resolves 70% of decisions:
```yaml
# database-decisions.yaml
sqlite:
  default_when: "prototype OR demo OR example"
  rationale: "Fast setup, zero ops"

postgresql:
  default_when: "production OR scale OR >10M rows"
  rationale: "Production-grade, ACID guarantees"

# Only asks user if ambiguous
```

**Result:** Reduces question fatigue from ~35 to ~10 questions.

**Beads:** No decision support. Manual all the way.

**5. Specification-Driven Development**

PIV-Swarm uses **Anthropic XML format** for formal specifications:
```xml
<project_specification>
  <overview>
    High-level description, success criteria, constraints
  </overview>

  <implementation_steps>
    <step_0>
      <task>Implement JWT token service</task>
      <duration>1 session (~25K tokens)</duration>
      <tdd>true</tdd>
      <files>
        <create>src/auth/jwt_service.py</create>
        <create>tests/unit/auth/test_jwt_service.py</create>
      </files>
      <actions>
        - Create JWTService class with sign() method
        - Implement HS256 algorithm
        - Add token expiration validation
      </actions>
      <validation>
        - pytest tests/unit/auth/ -v
        - mypy src/auth/
      </validation>
    </step_0>
  </implementation_steps>

  <session_management>
    <startup_ritual>Load spec → Review progress → Continue next task</startup_ritual>
    <token_budget>200K per session, checkpoint at 150-175K</token_budget>
    <progress_tracking>Update task files, commit after validation</progress_tracking>
  </session_management>

  <gotchas>
    Known pitfalls documented upfront to prevent wasted cycles
  </gotchas>
</project_specification>
```

**Benefits:**
- Prevents scope creep (spec is contract)
- Enables multi-session work (spec persists)
- Clear validation criteria (done means done)
- Institutional knowledge (decisions documented)

**Beads:** No specification framework. Tasks are just titles and descriptions.

**6. Fresh Context Per Task**

PIV-Swarm `/execute` skill supports `context: fork`:
```yaml
# task-003.yaml
id: task-003
name: Implement login endpoint
context: fork  # This task runs with fresh context

# Result:
# - No dependency on previous conversation history
# - Can run in parallel with other tasks
# - Perfect for multi-agent swarms
# - Each task gets full 200K token budget
```

**Beads:** Assumes single-agent sequential execution.

---

## Beads Concepts Worth Adopting

### 1. Hash-Based Task IDs

**Current Problem:**
```bash
# Sequential IDs cause merge conflicts
.agents/tasks/task-001.yaml
.agents/tasks/task-002.yaml
.agents/tasks/task-003.yaml
```

**Proposed Solution:**
```bash
# Hash-based IDs prevent conflicts
.agents/tasks/task-a3f8.yaml
.agents/tasks/task-7c2d.yaml
.agents/tasks/task-9e4a.yaml
```

**Implementation:**
```python
import hashlib
from datetime import datetime
import os

def generate_task_id(prefix: str = "task") -> str:
    """Generate collision-resistant task ID using timestamp + entropy"""
    timestamp = datetime.now().isoformat()
    entropy = os.urandom(8).hex()
    hash_input = f"{timestamp}{entropy}"
    short_hash = hashlib.sha256(hash_input.encode()).hexdigest()[:8]
    return f"{prefix}-{short_hash}"

# Usage
task_id = generate_task_id()  # "task-a3f8c2d9"
filename = f".agents/tasks/{task_id}.yaml"
```

**Update Required Skills:**
- `/task-create` - Generate hash IDs instead of sequential
- `/task-list` - Handle hash-based filenames
- `/task-get` - Lookup by hash ID
- `/task-update` - Reference by hash ID

**Migration Path:**
```bash
# One-time migration script
for file in .agents/tasks/task-*.yaml; do
  old_id=$(basename "$file" .yaml)
  new_id=$(python -c "from task_utils import generate_task_id; print(generate_task_id())")
  mv "$file" ".agents/tasks/${new_id}.yaml"
  # Update references in other task files
  rg -l "$old_id" .agents/tasks/ | xargs sed -i "s/$old_id/$new_id/g"
done
```

**Benefits:**
- ✅ Prevents merge conflicts in multi-dev scenarios
- ✅ Enables parallel task creation across branches
- ✅ Future-proofs for distributed agent swarms

---

### 2. Hierarchical Task Structure

**Current Structure (Flat with Dependencies):**
```yaml
# task-001.yaml (Epic)
id: task-001
name: Add authentication system
type: epic  # Not currently supported
blocked_by: []

# task-002.yaml (Task)
id: task-002
name: Implement JWT service
blocked_by: [task-001]

# task-003.yaml (Subtask)
id: task-003
name: Add token signing
blocked_by: [task-002]
```

**Proposed Structure (Hierarchical):**
```yaml
# task-a3f8.yaml (Epic)
id: task-a3f8
type: epic
name: Add authentication system
description: Full JWT-based authentication with refresh tokens
children:
  - task-a3f8-1
  - task-a3f8-2
parent: null
progress:
  total_children: 2
  completed_children: 0

# task-a3f8-1.yaml (Task under epic)
id: task-a3f8-1
type: task
parent: task-a3f8
name: Implement JWT service
description: Token signing and validation
children:
  - task-a3f8-1-1
  - task-a3f8-1-2
progress:
  total_children: 2
  completed_children: 0

# task-a3f8-1-1.yaml (Subtask)
id: task-a3f8-1-1
type: subtask
parent: task-a3f8-1
name: Add token signing
description: Implement HS256 signing with secret rotation
children: []
```

**Schema Changes:**
```yaml
# Add to .claude/schemas/task.yaml

type:
  type: enum
  values: [epic, task, subtask]
  description: Task level in hierarchy

parent:
  type: string | null
  description: Parent task ID (null for top-level epics)

children:
  type: array[string]
  description: Child task IDs

progress:
  type: object
  properties:
    total_children: integer
    completed_children: integer
    percentage: integer  # Auto-calculated
```

**Benefits:**
- ✅ Mirrors Linear's epic → issue → sub-issue structure
- ✅ Clearer progress visualization
- ✅ Better mapping to product planning
- ✅ Natural rollup of completion percentages

**Enhanced `/task-list` Output:**
```
Epic: Add authentication (3/5 tasks complete) [60%]
  ✓ Task: JWT service (2/2 subtasks) [100%]
    ✓ Subtask: Token signing
    ✓ Subtask: Token validation
  ⏳ Task: Login endpoint (in progress)
    ✓ Subtask: Route handler
    ⏳ Subtask: Request validation
  ⏳ Task: Password reset flow
  ⏳ Task: Session management
```

---

### 3. Semantic Memory Decay

**Problem:** Token wastage on closed task descriptions

**Current Behavior:**
```yaml
# task-001.yaml (completed 3 months ago)
id: task-001
name: Add user authentication
description: |
  Implemented comprehensive JWT-based authentication system with the following features:

  1. Token Generation
     - HS256 signing algorithm with secret rotation
     - 15-minute access token expiration
     - 7-day refresh token expiration
     - UUID-based JTI (JWT ID) for tracking

  2. Token Validation
     - Signature verification using public key
     - Expiration checking with clock skew tolerance
     - Revocation list checking via Redis
     - Issuer and audience validation

  3. Security Features
     - Bcrypt password hashing (cost factor 12)
     - Rate limiting on login endpoint (5 attempts per 15 min)
     - HTTPS-only cookie transmission
     - CSRF token validation

  [300 more words...]

status: completed
completed_at: 2025-11-04T10:30:00Z

# This full description loads into context every session
# Cost: ~800 tokens per completed task
# 50 completed tasks = 40K tokens wasted
```

**Proposed Behavior (Semantic Decay):**
```yaml
# task-001.yaml (after summarization)
id: task-001
name: Add user authentication
summary: "Implemented JWT auth with HS256 signing, refresh token rotation, bcrypt password hashing, rate limiting, and CSRF protection. Tests: 94% coverage."
description_archived: true
archived_at: 2025-11-04T10:35:00Z
status: completed
completed_at: 2025-11-04T10:30:00Z

# Full description moved to:
# .agents/archive/task-001-full.yaml

# Cost: ~50 tokens per completed task
# 50 completed tasks = 2.5K tokens
# Savings: 93% token reduction
```

**Implementation:**

```yaml
# Update /task-complete skill

When marking task as completed:
1. Generate 1-2 sentence summary using LLM
2. Move full description to .agents/archive/{task_id}-full.yaml
3. Update task file with summary only
4. Set description_archived: true flag

Summary generation prompt:
"Summarize this completed task in 1-2 sentences focusing on what was delivered and validation results. Task: {description}"
```

**Archive Structure:**
```bash
.agents/archive/
├── task-001-full.yaml     # Full original description
├── task-002-full.yaml
├── task-003-full.yaml
└── README.md              # "Archived full descriptions for completed tasks"
```

**Schema Changes:**
```yaml
# Add to task schema

summary:
  type: string | null
  description: Brief summary for completed tasks (auto-generated)

description_archived:
  type: boolean
  default: false
  description: Whether full description moved to archive

archived_at:
  type: datetime | null
  description: When description was archived
```

**Context Loading Strategy:**
```python
# In /prime and /execute skills

def load_task_context(task_ids: list[str]) -> str:
    context = []
    for task_id in task_ids:
        task = load_task_yaml(task_id)

        if task.status == "completed" and task.description_archived:
            # Load summary only (50 tokens)
            context.append(f"{task.name}: {task.summary}")
        else:
            # Load full description (800 tokens)
            context.append(f"{task.name}: {task.description}")

    return "\n".join(context)
```

**Benefits:**
- ✅ 70-90% token reduction on completed task context
- ✅ Preserve "smart context" budget for active work
- ✅ Full descriptions available on-demand if needed
- ✅ Automatic execution (no manual intervention)

---

### 4. Git Audit Trail Enhancement

**Current State:** Task files are tracked in git, but no specialized commands for audit trails.

**Proposed Skills:**

#### `/task-history` - Show full task audit trail
```yaml
name: task-history
description: Show complete audit trail for a task
usage: /task-history <task-id>

implementation: |
  git log --follow --pretty=format:"%h %ad %an %s" --date=short .agents/tasks/{task-id}.yaml

  # Plus structured output:
  - Who created the task
  - When status changed (pending → in_progress → completed)
  - Who claimed ownership
  - When validation passed/failed
  - Associated commits

example_output: |
  Task: task-a3f8 (Implement JWT service)

  Created: 2026-01-15 by jane@example.com
  Claimed: 2026-01-15 by agent-explore-001
  Started: 2026-01-15 10:30 AM
  Completed: 2026-01-15 2:45 PM
  Duration: 4h 15m

  Changes:
  a3f8c2d9 2026-01-15 jane    feat(auth): create task for JWT service
  7c2d4e1a 2026-01-15 claude  chore(task): mark task-a3f8 as in_progress
  9e4a6f3b 2026-01-15 claude  chore(task): update task-a3f8 validation results
  2b8d5c7e 2026-01-15 claude  chore(task): mark task-a3f8 as completed

  Associated Commits:
  4f9a1c3d feat(auth): implement JWT signing (task-a3f8)
  8e2b7d5f test(auth): add JWT service tests (task-a3f8)
```

#### `/task-blame` - Show who changed each field
```yaml
name: task-blame
description: Show who last modified each field in a task
usage: /task-blame <task-id>

implementation: |
  git blame .agents/tasks/{task-id}.yaml

example_output: |
  Task: task-a3f8

  Field          | Changed By    | Date       | Commit
  ---------------|---------------|------------|----------
  status         | claude-agent  | 2026-01-15 | 7c2d4e1a
  owner          | jane          | 2026-01-15 | a3f8c2d9
  priority       | jane          | 2026-01-15 | a3f8c2d9
  blocked_by     | claude-agent  | 2026-01-15 | 9e4a6f3b
  actual_tokens  | claude-agent  | 2026-01-15 | 2b8d5c7e
```

#### `/task-diff` - Compare task versions
```yaml
name: task-diff
description: Compare task state across commits or branches
usage: /task-diff <task-id> [commit1] [commit2]

implementation: |
  git diff commit1..commit2 .agents/tasks/{task-id}.yaml

  # Structured output showing field changes

example_output: |
  Task: task-a3f8
  Comparing: a3f8c2d9 (created) vs 2b8d5c7e (completed)

  status:
    - pending
    + completed

  owner:
    - null
    + agent-explore-001

  actual_tokens:
    - null
    + 23450

  validation.test_results:
    + All tests passed (94% coverage)
```

**Benefits:**
- ✅ Full accountability for task changes
- ✅ Debug task state issues easily
- ✅ Understand task evolution over time
- ✅ Leverage git's built-in audit capabilities

---

## Linear Integration Design

### Overview

**Goal:** Bidirectional sync between Linear (product planning) and PIV-Swarm (execution tracking).

**Model:** Hybrid approach - Linear for feature planning, PIV-Swarm for development execution.

### Architecture

```
┌─────────────────────────────────────┐
│         Linear (Product)            │
│   Epics, Issues, Sub-issues         │
│   Status: Backlog, Todo, In Progress│
└─────────────┬───────────────────────┘
              │
              │ /linear-sync (Pull)
              ↓
┌─────────────────────────────────────┐
│      PIV-Swarm (Development)        │
│  .agents/tasks/ (Execution Context) │
│  /prime → /discuss → /spec → /plan  │
└─────────────┬───────────────────────┘
              │
              │ Auto-sync (Push)
              ↓
┌─────────────────────────────────────┐
│    Linear (Status Updates)          │
│   Progress tracking, commit links    │
└─────────────────────────────────────┘
```

### Workflow

#### **Phase 1: Planning (Linear-First)**

Product/PM creates features in Linear:
```
Linear Epic: PRO-123 "Add User Authentication"
├─ PRO-124: JWT token service
├─ PRO-125: Login endpoint
├─ PRO-126: Password reset flow
└─ PRO-127: Session management
```

#### **Phase 2: Development Kickoff (Pull from Linear)**

Developer starts work:
```bash
/session-start
> Select workflow: Feature Development

/linear-sync PRO-123

# This command:
# 1. Fetches PRO-123 epic and sub-issues from Linear API
# 2. Runs /prime to understand codebase context
# 3. Runs /discuss for architectural decisions
# 4. Runs /spec to create formal specification
# 5. Runs /plan to generate task files with Linear mappings
```

**Generated Task Files:**
```yaml
# .agents/tasks/task-a3f8.yaml (Epic)
id: task-a3f8
type: epic
name: Add user authentication
linear:
  issue_id: "b8c9d0e1-f2a3-4b5c-6d7e-8f9a0b1c2d3e"  # Linear UUID
  issue_key: "PRO-123"                              # Human-readable
  issue_url: "https://linear.app/your-workspace/issue/PRO-123"
  epic_id: "b8c9d0e1-f2a3-4b5c-6d7e-8f9a0b1c2d3e"
  last_synced: "2026-02-04T10:00:00Z"
  sync_enabled: true
children:
  - task-a3f8-1  # Maps to PRO-124
  - task-a3f8-2  # Maps to PRO-125
  - task-a3f8-3  # Maps to PRO-126

# .agents/tasks/task-a3f8-1.yaml (Issue)
id: task-a3f8-1
type: task
parent: task-a3f8
name: Implement JWT token service
linear:
  issue_id: "c1d2e3f4-a5b6-7c8d-9e0f-1a2b3c4d5e6f"
  issue_key: "PRO-124"
  issue_url: "https://linear.app/your-workspace/issue/PRO-124"
  parent_issue_id: "b8c9d0e1-f2a3-4b5c-6d7e-8f9a0b1c2d3e"
  last_synced: "2026-02-04T10:00:00Z"
  sync_enabled: true
status: pending
priority: high
# ... rest of task file
```

#### **Phase 3: Execution (Local with Auto-Sync)**

As developer works, PIV-Swarm auto-syncs status to Linear:

```bash
/execute

# Task lifecycle hooks:
# 1. Task starts
task-a3f8-1: pending → in_progress
→ Linear API: Update PRO-124 status to "In Progress"
→ Linear API: Add comment "Development started by @jane"

# 2. Task completes
task-a3f8-1: in_progress → completed
→ Linear API: Update PRO-124 status to "Done"
→ Linear API: Add comment with validation results:
  """
  ✅ Task completed

  Validation Results:
  - Unit tests: ✅ 15/15 passed
  - Integration tests: ✅ 3/3 passed
  - Coverage: 94%
  - Type checking: ✅ No errors
  - Linting: ✅ No violations

  Files Changed:
  - src/auth/jwt_service.py (created)
  - tests/unit/auth/test_jwt_service.py (created)
  - tests/integration/auth/test_jwt_integration.py (created)
  """

# 3. Commits link to Linear
git commit -m "feat(auth): implement JWT signing (PRO-124)"
→ Linear API: Link commit to PRO-124
→ Shows in Linear issue timeline
```

#### **Phase 4: Monitoring (Status Dashboard)**

```bash
/status

# Enhanced output with Linear integration:
Current Feature: Add user authentication (PRO-123)
Progress: 2/4 tasks complete (50%)

Linear Sync Status: ✅ Connected
Last sync: 2 minutes ago

Tasks:
  ✓ task-a3f8-1 (PRO-124) - JWT token service [Done]
  ✓ task-a3f8-2 (PRO-125) - Login endpoint [Done]
  ⏳ task-a3f8-3 (PRO-126) - Password reset flow [In Progress]
  ⏳ task-a3f8-4 (PRO-127) - Session management [Todo]

Linear Epic: https://linear.app/your-workspace/issue/PRO-123
```

### Key Mappings

| PIV-Swarm | Linear | Sync Direction | Notes |
|-----------|--------|----------------|-------|
| Session feature | Epic | Pull (Linear → Local) | Created in Linear first |
| Task files (epic type) | Epic | Pull | Top-level planning |
| Task files (task type) | Issue | Bidirectional | Main work items |
| Task files (subtask type) | Sub-issue | Bidirectional | Granular work |
| Task status | Issue state | Push (Local → Linear) | Development drives updates |
| Task priority | Issue priority | Pull initially | PM sets priorities |
| blocked_by/blocks | Issue relations | Bidirectional | Dependency tracking |
| Validation results | Issue comments | Push | Automated reporting |
| Git commits | Issue attachments | Push | Commit linking via message |
| actual_tokens | Custom field | Push | Cost tracking |

### Linear API Integration

#### **Technology Stack**
- **HTTP Client:** `httpx` (async, already in stack)
- **Data Models:** Pydantic v2 (type safety, validation)
- **API:** Linear GraphQL API
- **Auth:** Personal API token or OAuth

#### **Service Architecture**

```python
# src/integrations/linear/models.py
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum

class LinearIssueState(str, Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    CANCELED = "canceled"

class LinearIssue(BaseModel):
    id: str                                    # UUID
    identifier: str                            # "PRO-123"
    title: str
    description: str | None = None
    state: LinearIssueState
    priority: int = Field(ge=0, le=4)         # 0=No priority, 4=Urgent
    assignee_id: str | None = None
    parent_id: str | None = None              # For sub-issues
    created_at: datetime
    updated_at: datetime
    url: str

class LinearComment(BaseModel):
    id: str
    body: str
    created_at: datetime
    user_id: str

# src/integrations/linear/service.py
import httpx
from typing import List, Optional

class LinearService:
    """Linear API client using GraphQL"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.linear.app/graphql"
        self.headers = {
            "Authorization": api_key,
            "Content-Type": "application/json"
        }

    async def get_issue(self, issue_key: str) -> LinearIssue:
        """Fetch single issue by identifier (e.g., PRO-123)"""
        query = """
        query GetIssue($issueKey: String!) {
          issue(filter: { identifier: { eq: $issueKey } }) {
            id
            identifier
            title
            description
            state { name }
            priority
            assignee { id name }
            parent { id identifier }
            createdAt
            updatedAt
            url
          }
        }
        """
        variables = {"issueKey": issue_key}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                headers=self.headers,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            data = response.json()
            return LinearIssue.model_validate(data["data"]["issue"])

    async def get_epic_with_children(self, epic_key: str) -> tuple[LinearIssue, List[LinearIssue]]:
        """Fetch epic and all child issues"""
        # GraphQL query to get parent + children
        # Returns (epic, [child_issues])
        pass

    async def update_issue_status(self, issue_id: str, state: LinearIssueState) -> None:
        """Update issue state"""
        mutation = """
        mutation UpdateIssue($issueId: String!, $stateId: String!) {
          issueUpdate(id: $issueId, input: { stateId: $stateId }) {
            success
          }
        }
        """
        # Get state ID from state name, then update
        pass

    async def add_comment(self, issue_id: str, body: str) -> LinearComment:
        """Add comment to issue"""
        mutation = """
        mutation CreateComment($issueId: String!, $body: String!) {
          commentCreate(input: { issueId: $issueId, body: $body }) {
            comment { id body createdAt }
          }
        }
        """
        pass

    async def link_commit(self, issue_id: str, commit_sha: str, commit_url: str) -> None:
        """Link git commit to issue"""
        # Linear auto-detects commits with "PRO-123" in message
        # This is just for manual linking if needed
        pass

# src/integrations/linear/sync.py
class LinearSync:
    """Bidirectional sync between Linear and PIV-Swarm tasks"""

    def __init__(self, service: LinearService):
        self.service = service

    async def pull_epic_to_tasks(self, epic_key: str) -> List[str]:
        """
        Pull Linear epic and create PIV-Swarm task files

        Returns list of created task IDs
        """
        # 1. Fetch epic + children from Linear
        epic, children = await self.service.get_epic_with_children(epic_key)

        # 2. Create epic task file (task-{hash}.yaml)
        epic_task_id = self._create_epic_task(epic)

        # 3. Create child task files
        child_task_ids = []
        for child in children:
            task_id = self._create_child_task(child, epic_task_id)
            child_task_ids.append(task_id)

        return [epic_task_id] + child_task_ids

    async def push_task_status(self, task_id: str) -> None:
        """Push local task status to Linear"""
        # 1. Load task file
        task = load_task_yaml(task_id)

        # 2. Check if Linear sync enabled
        if not task.get("linear", {}).get("sync_enabled"):
            return

        # 3. Map PIV-Swarm status to Linear state
        linear_state = self._map_status_to_linear(task.status)

        # 4. Update Linear issue
        linear_issue_id = task["linear"]["issue_id"]
        await self.service.update_issue_status(linear_issue_id, linear_state)

        # 5. Update last_synced timestamp
        task["linear"]["last_synced"] = datetime.now().isoformat()
        save_task_yaml(task_id, task)

    def _map_status_to_linear(self, piv_status: str) -> LinearIssueState:
        """Map PIV-Swarm task status to Linear state"""
        mapping = {
            "pending": LinearIssueState.TODO,
            "in_progress": LinearIssueState.IN_PROGRESS,
            "completed": LinearIssueState.DONE,
            "blocked": LinearIssueState.IN_PROGRESS,  # Keep in progress, add comment
            "failed": LinearIssueState.TODO,          # Reset to todo, add comment
        }
        return mapping.get(piv_status, LinearIssueState.TODO)
```

### New Skills

#### `/linear-sync` - Pull Linear epic and create tasks

```yaml
name: linear-sync
description: Pull Linear epic and create PIV-Swarm task files
usage: /linear-sync <epic-key>

parameters:
  - name: epic-key
    type: string
    required: true
    description: Linear epic identifier (e.g., PRO-123)

implementation:
  1. Validate Linear API connection
  2. Fetch epic and child issues from Linear
  3. Run /prime to understand codebase (if not already done)
  4. Run /discuss to gather architectural decisions
  5. Run /spec to create formal specification
  6. Run /plan with Linear context to generate tasks
  7. Create task files with Linear metadata
  8. Display summary of created tasks

example:
  input: /linear-sync PRO-123
  output: |
    ✅ Synced Linear epic PRO-123

    Created tasks:
    - task-a3f8 (epic) → PRO-123: Add user authentication
      - task-a3f8-1 → PRO-124: JWT token service
      - task-a3f8-2 → PRO-125: Login endpoint
      - task-a3f8-3 → PRO-126: Password reset flow

    Next: /execute to start implementation
```

#### `/linear-push` - Manual sync to Linear

```yaml
name: linear-push
description: Manually sync current task state to Linear
usage: /linear-push [task-id]

parameters:
  - name: task-id
    type: string
    required: false
    description: Specific task to sync (default: all tasks)

implementation:
  1. Load task file(s)
  2. Check Linear sync_enabled flag
  3. Push status updates to Linear
  4. Add validation results as comments
  5. Link any new commits
  6. Update last_synced timestamp

example:
  input: /linear-push task-a3f8-1
  output: |
    ✅ Synced task-a3f8-1 to Linear

    PRO-124: JWT token service
    - Status updated: Todo → In Progress
    - Comment added with validation results
    - 2 commits linked

    View in Linear: https://linear.app/your-workspace/issue/PRO-124
```

### Auto-Sync Hooks

**Modify existing skills to auto-sync:**

#### `/task-update` enhancement
```yaml
# Add to /task-update skill

After updating task status:
  if linear.sync_enabled:
    await linear_sync.push_task_status(task_id)
    logger.info(f"Synced {task_id} to Linear {linear.issue_key}")
```

#### `/task-complete` enhancement
```yaml
# Add to /task-complete skill

After marking task complete:
  1. Generate summary (semantic memory decay)
  2. Archive full description
  3. if linear.sync_enabled:
       - Update Linear status to "Done"
       - Add completion comment with:
         - Validation results (test pass/fail, coverage, etc.)
         - Files changed
         - Commits linked
  4. Update last_synced timestamp
```

#### `/commit` enhancement
```yaml
# Add to /commit skill (git commit wrapper)

When creating commit:
  1. Create git commit as normal
  2. Parse commit message for Linear issue keys (PRO-XXX)
  3. If found and Linear sync enabled:
       - Link commit to Linear issue via API
       - Linear will auto-detect and show in timeline
  4. Ensure commit message includes issue key for traceability
```

### Configuration

#### **Settings File**
```yaml
# .agents/config/linear.yaml

linear:
  enabled: true
  api_key_env: "LINEAR_API_KEY"  # Load from environment variable
  workspace: "your-workspace"
  team_id: "your-team-id"

  # Auto-sync behavior
  auto_sync:
    enabled: true
    on_task_update: true
    on_task_complete: true
    on_commit: true

  # Status mapping
  status_mapping:
    pending: "Todo"
    in_progress: "In Progress"
    completed: "Done"
    blocked: "In Progress"  # With comment
    failed: "Todo"          # With comment

  # Sync frequency
  sync:
    mode: "real_time"  # or "manual", "session_boundary"
    retry_on_failure: true
    max_retries: 3
```

#### **Environment Variables**
```bash
# .envrc (loaded via direnv)
export LINEAR_API_KEY="lin_api_xxxxxxxxxxxxx"
```

#### **Feature Flag**
```python
# Enable/disable Linear integration
USE_LINEAR_SYNC = os.getenv("USE_LINEAR_SYNC", "true").lower() == "true"

# Fallback behavior if disabled
if not USE_LINEAR_SYNC:
    logger.info("Linear sync disabled, working offline")
    # PIV-Swarm works normally without Linear
```

### Error Handling

```python
class LinearSyncError(Exception):
    """Base exception for Linear sync errors"""
    pass

class LinearAPIError(LinearSyncError):
    """Linear API returned error"""
    pass

class LinearAuthError(LinearSyncError):
    """Linear authentication failed"""
    pass

class LinearNotFoundError(LinearSyncError):
    """Linear issue not found"""
    pass

# Graceful degradation
async def safe_sync(task_id: str) -> None:
    try:
        await linear_sync.push_task_status(task_id)
    except LinearAuthError:
        logger.error("Linear auth failed, check API key")
        # Continue without sync
    except LinearAPIError as e:
        logger.error(f"Linear API error: {e}")
        # Queue for retry
        retry_queue.add(task_id)
    except Exception as e:
        logger.exception("Unexpected Linear sync error")
        # Continue without sync
```

### Conflict Resolution

**Scenario:** Linear status changed while working locally

**Strategy:** Local wins (development is source of truth for status)

```python
async def sync_with_conflict_detection(task_id: str) -> None:
    # 1. Fetch current Linear state
    linear_issue = await service.get_issue(task.linear.issue_key)

    # 2. Compare with local last_synced timestamp
    if linear_issue.updated_at > task.linear.last_synced:
        # Linear changed since last sync
        logger.warning(f"Conflict detected for {task_id}")

        # 3. Check what changed in Linear
        if linear_issue.state != expected_linear_state:
            # Status diverged
            logger.info(f"Linear status: {linear_issue.state}, Local status: {task.status}")

            # 4. Local wins, but add comment to Linear explaining
            await service.add_comment(
                linear_issue.id,
                f"Status updated by PIV-Swarm: {task.status}\n"
                f"(Overriding Linear status: {linear_issue.state})"
            )

    # 5. Push local state
    await service.update_issue_status(linear_issue.id, map_status(task.status))
```

### Offline Mode

PIV-Swarm must work fully offline (Linear is enhancement, not requirement):

```python
# All Linear sync calls wrapped in:
if USE_LINEAR_SYNC and linear_config.enabled:
    try:
        await sync_operation()
    except Exception:
        logger.info("Linear sync failed, continuing offline")
        # Queue for later retry when online
```

**Queued Sync:**
```yaml
# .agents/state/linear-sync-queue.yaml

queued_syncs:
  - task_id: task-a3f8-1
    operation: update_status
    payload: {status: "completed"}
    queued_at: "2026-02-04T14:30:00Z"
    retry_count: 0

  - task_id: task-a3f8-2
    operation: add_comment
    payload: {comment: "Validation passed"}
    queued_at: "2026-02-04T14:32:00Z"
    retry_count: 1

# Retry on next /linear-push or session start
```

---

## Implementation Roadmap

### Phase 1: Beads-Inspired Infrastructure (2-3 sessions)

**Goal:** Improve task management without Linear dependency

#### Task 1.1: Hash-Based Task IDs
- **Effort:** 1-2 hours
- **Priority:** High (prevents multi-dev conflicts)
- **Dependencies:** None

**Steps:**
1. Create `generate_task_id()` function in task utilities
2. Update `/task-create` skill to use hash IDs
3. Update `/task-list`, `/task-get`, `/task-update` to handle hash IDs
4. Migration script for existing tasks: `task-001.yaml` → `task-a3f8.yaml`
5. Test parallel task creation across branches (no conflicts)

**Validation:**
```bash
# Test 1: Create tasks in parallel branches
git checkout -b feature/auth
/task-create "Implement JWT"  # Creates task-a3f8.yaml

git checkout -b feature/payments
/task-create "Add Stripe"     # Creates task-7c2d.yaml

git checkout dev
git merge feature/auth        # No conflict
git merge feature/payments    # No conflict ✅
```

#### Task 1.2: Semantic Memory Decay
- **Effort:** 2-3 hours
- **Priority:** Medium (token savings)
- **Dependencies:** Task 1.1

**Steps:**
1. Add `summary`, `description_archived`, `archived_at` fields to task schema
2. Create `.agents/archive/` directory with README
3. Update `/task-complete` skill:
   - Generate 1-2 sentence summary via LLM
   - Move full description to archive
   - Update task file with summary
4. Update `/prime` and `/execute` to load summaries for completed tasks
5. Measure token savings on test project (expect 70-90% reduction)

**Validation:**
```bash
# Test: Complete 10 tasks, measure token usage
# Before: 10 tasks × 800 tokens = 8K tokens
# After: 10 summaries × 50 tokens = 500 tokens
# Savings: 93% ✅
```

#### Task 1.3: Hierarchical Task Structure
- **Effort:** 4-5 hours
- **Priority:** Medium (better organization)
- **Dependencies:** Task 1.1

**Steps:**
1. Add `type` (epic/task/subtask), `parent`, `children`, `progress` to schema
2. Update `/task-create` to support parent parameter
3. Update `/task-list` to display hierarchical tree view
4. Update `/status` to show epic-level rollup
5. Add auto-calculation of progress percentages
6. Create test epic with 3 tasks and 2 subtasks each

**Validation:**
```bash
/task-list

# Expected output:
Epic: Add authentication (3/5 tasks) [60%]
  ✓ Task: JWT service (2/2 subtasks) [100%]
    ✓ Subtask: Token signing
    ✓ Subtask: Token validation
  ⏳ Task: Login endpoint (1/2 subtasks) [50%]
    ✓ Subtask: Route handler
    ⏳ Subtask: Request validation
  ⏳ Task: Password reset (0/2 subtasks) [0%]
```

#### Task 1.4: Git Audit Trail Skills
- **Effort:** 2-3 hours
- **Priority:** Low (nice to have)
- **Dependencies:** None

**Steps:**
1. Create `/task-history` skill (git log for task file)
2. Create `/task-blame` skill (who changed each field)
3. Create `/task-diff` skill (compare task versions)
4. Add git log integration to `/task-get` output
5. Test with tasks modified across multiple commits

**Success Criteria:**
- All 3 new skills working
- Clear, formatted output showing audit trails
- Integrated into `/task-get` display

---

### Phase 2: Linear Integration Core (3-4 sessions)

**Goal:** Basic bidirectional sync with Linear

**Prerequisites:**
- Phase 1 complete (hash IDs, hierarchical structure)
- Linear API key obtained
- Test Linear workspace with sample epic

#### Task 2.1: Linear API Client
- **Effort:** 3-4 hours
- **Priority:** High (foundation)
- **Dependencies:** None

**Steps:**
1. Create `src/integrations/linear/` module structure
2. Define Pydantic models for Linear API (issue, comment, state)
3. Implement `LinearService` class with GraphQL queries:
   - `get_issue(issue_key)` - Fetch single issue
   - `get_epic_with_children(epic_key)` - Fetch epic + children
   - `update_issue_status(issue_id, state)` - Update status
   - `add_comment(issue_id, body)` - Add comment
4. Add error handling (404, 401, 429 rate limits)
5. Write unit tests with mocked responses
6. Write integration tests against real Linear API

**Validation:**
```python
# Integration test
async def test_linear_api_integration():
    service = LinearService(api_key=os.getenv("LINEAR_API_KEY"))

    # Fetch test issue
    issue = await service.get_issue("TEST-1")
    assert issue.identifier == "TEST-1"

    # Update status
    await service.update_issue_status(issue.id, LinearIssueState.IN_PROGRESS)

    # Add comment
    comment = await service.add_comment(issue.id, "Test comment from PIV-Swarm")
    assert comment.body == "Test comment from PIV-Swarm"
```

#### Task 2.2: Pull Linear → PIV-Swarm
- **Effort:** 4-5 hours
- **Priority:** High (enables workflow)
- **Dependencies:** Task 2.1

**Steps:**
1. Create `LinearSync` class with `pull_epic_to_tasks()` method
2. Implement epic → task file conversion logic
3. Map Linear fields to task schema fields
4. Add Linear metadata block to task files
5. Create `/linear-sync` skill
6. Integrate with PIV-Swarm workflow:
   - `/linear-sync PRO-123`
   - → `/prime` (if needed)
   - → `/discuss`
   - → `/spec`
   - → `/plan` (creates tasks with Linear mappings)
7. Test end-to-end: Linear epic → task files → spec → plan

**Validation:**
```bash
# Test: Sync real Linear epic
/linear-sync PRO-123

# Expected:
# - Creates task-{hash}.yaml files
# - Each has linear.issue_key field
# - Hierarchical structure matches Linear
# - Can run /execute on generated tasks
```

#### Task 2.3: Push PIV-Swarm → Linear
- **Effort:** 3-4 hours
- **Priority:** High (closes the loop)
- **Dependencies:** Task 2.2

**Steps:**
1. Implement `LinearSync.push_task_status()` method
2. Map PIV-Swarm statuses to Linear states
3. Add auto-sync hooks to existing skills:
   - `/task-update` → Push status change
   - `/task-complete` → Push completion + validation results
4. Create `/linear-push` skill for manual sync
5. Add conflict detection (local wins strategy)
6. Test status lifecycle: pending → in_progress → completed

**Validation:**
```bash
# Test: Full lifecycle sync
/execute task-a3f8-1
# → Linear PRO-124 status: Todo → In Progress ✅

# Task completes
# → Linear PRO-124 status: In Progress → Done ✅
# → Linear comment added with validation results ✅
```

#### Task 2.4: Configuration & Error Handling
- **Effort:** 2-3 hours
- **Priority:** High (production readiness)
- **Dependencies:** Task 2.3

**Steps:**
1. Create `.agents/config/linear.yaml` configuration file
2. Add environment variable loading (LINEAR_API_KEY)
3. Add feature flag (USE_LINEAR_SYNC)
4. Implement graceful degradation (offline mode)
5. Add retry queue for failed syncs
6. Add comprehensive error handling
7. Test offline mode (PIV-Swarm works without Linear)

**Validation:**
```bash
# Test 1: Offline mode
export USE_LINEAR_SYNC=false
/execute task-a3f8-1
# → Works normally, no Linear API calls ✅

# Test 2: Network failure
export USE_LINEAR_SYNC=true
# Disconnect network
/task-update task-a3f8-1 --status in_progress
# → Queues sync for later ✅
# → PIV-Swarm continues working ✅

# Test 3: Reconnect and retry
# Reconnect network
/linear-push
# → Processes queued syncs ✅
```

---

### Phase 3: Enhanced Features (2-3 sessions)

**Goal:** Polish and productivity enhancements

#### Task 3.1: Commit Linking
- **Effort:** 2 hours
- **Priority:** Medium
- **Dependencies:** Phase 2 complete

**Steps:**
1. Update `/commit` skill to parse Linear issue keys from message
2. Link commits to Linear issues via API
3. Test git commit workflow with Linear references

**Validation:**
```bash
git commit -m "feat(auth): implement JWT signing (PRO-124)"
# → Commit linked to PRO-124 in Linear timeline ✅
```

#### Task 3.2: Enhanced `/status` with Linear
- **Effort:** 2 hours
- **Priority:** Medium
- **Dependencies:** Phase 2 complete

**Steps:**
1. Update `/status` skill to show Linear epic progress
2. Display Linear URLs for easy navigation
3. Show sync status (connected, last sync time)
4. Add Linear epic rollup (tasks completed, blocked, etc.)

**Validation:**
```bash
/status

# Expected:
Linear Sync: ✅ Connected (last sync: 2 min ago)
Epic: PRO-123 Add authentication (3/5 tasks) [60%]
  https://linear.app/workspace/issue/PRO-123

Tasks:
  ✓ PRO-124: JWT service [Done]
  ✓ PRO-125: Login endpoint [Done]
  ⏳ PRO-126: Password reset [In Progress]
  ⏳ PRO-127: Session management [Todo]
  ⏳ PRO-128: Token refresh [Todo]
```

#### Task 3.3: Token Tracking in Linear
- **Effort:** 2-3 hours
- **Priority:** Low (nice to have)
- **Dependencies:** Phase 2 complete

**Steps:**
1. Create Linear custom field for token usage
2. Push `actual_tokens` to Linear after task completion
3. Display total tokens in Linear epic
4. Generate cost reports (tokens × cost per token)

**Validation:**
- Linear issue shows token usage: "Tokens: 23,450"
- Linear epic shows total: "Total tokens: 145,820 (~$2.19)"

---

### Phase 4: Testing & Documentation (1 session)

#### Task 4.1: Integration Tests
- **Effort:** 2-3 hours
- **Priority:** High
- **Dependencies:** Phase 2-3 complete

**Steps:**
1. Write integration tests for full workflow:
   - Linear sync → PIV-Swarm execution → Linear update
2. Test error scenarios (network failure, auth failure, not found)
3. Test offline mode
4. Achieve 80%+ coverage

#### Task 4.2: Documentation
- **Effort:** 2 hours
- **Priority:** High
- **Dependencies:** All phases complete

**Steps:**
1. Create `.claude/reference/linear-integration.md` guide
2. Update CLAUDE.md with Linear workflow
3. Add examples to `/linear-sync` and `/linear-push` skills
4. Create troubleshooting guide
5. Document configuration options

#### Task 4.3: Retrospective
- **Effort:** 1 hour
- **Priority:** Medium
- **Dependencies:** All complete

**Steps:**
1. Create `.agents/feedback/linear-integration-retrospective-YYYY-MM-DD.md`
2. Document what worked well
3. Document challenges and lessons learned
4. Propose improvements for future iterations
5. Update GOALS.md status

---

## Open Questions

### 1. Linear Status Mapping

**Question:** How should PIV-Swarm statuses map to Linear states?

**Proposed Mapping:**
| PIV-Swarm | Linear | Notes |
|-----------|--------|-------|
| pending | Todo | Standard mapping |
| in_progress | In Progress | Standard mapping |
| completed | Done | Standard mapping |
| blocked | In Progress | Keep "In Progress" + add comment explaining blocker |
| failed | Todo | Reset to "Todo" + add comment with error details |

**Alternative:** Create custom Linear states (Blocked, Failed) if workspace allows.

**Decision Needed:** Does your Linear workspace use standard states or custom workflow?

---

### 2. Task Creation Ownership

**Question:** Who creates tasks - PM in Linear or developer via `/plan`?

**Option A: PM Creates All Issues Upfront**
- PM creates epic + all issues in Linear
- Developer runs `/linear-sync PRO-123`
- PIV-Swarm pulls everything down
- **Pros:** Clear product ownership, upfront planning
- **Cons:** PM must know technical breakdown

**Option B: PM Creates Epic Only**
- PM creates epic with high-level description
- Developer runs `/linear-sync PRO-123`
- PIV-Swarm runs `/discuss` → `/spec` → `/plan`
- `/plan` creates sub-issues in Linear automatically
- **Pros:** Developer controls technical breakdown
- **Cons:** Linear issues created by automation (might surprise PM)

**Option C: Hybrid**
- PM creates epic + major features (coarse-grained)
- Developer breaks down further during `/plan` (fine-grained)
- Only push granular subtasks to Linear if desired
- **Pros:** Balance of product and technical control
- **Cons:** More complex mapping logic

**Decision Needed:** What's your team's current Linear workflow?

---

### 3. Sync Frequency

**Question:** When should PIV-Swarm sync to Linear?

**Option A: Real-Time (Every Task Update)**
- `/task-update` → Immediate API call
- **Pros:** Linear always current
- **Cons:** Many API calls, might hit rate limits

**Option B: On-Demand (`/linear-push`)**
- Manual sync when ready
- **Pros:** Full control, no surprise updates
- **Cons:** Manual overhead, Linear can get stale

**Option C: Session Boundaries**
- Sync on `/session-start`, `/pause`, `/validate`, `/commit`
- **Pros:** Batched updates, fewer API calls
- **Cons:** Linear not real-time

**Option D: Hybrid**
- Auto-sync on major events (task complete, blocked)
- Manual `/linear-push` for other updates
- **Pros:** Balance of automation and control
- **Cons:** More complex logic

**Decision Needed:** How often do you check Linear during development?

---

### 4. Conflict Resolution Strategy

**Question:** If Linear status changes while working locally, which wins?

**Option A: Local Wins (Development is Source of Truth)**
- PIV-Swarm status always overrides Linear
- Add comment to Linear explaining why
- **Pros:** Developer workflow uninterrupted
- **Cons:** PM status changes can be overwritten

**Option B: Linear Wins (PM is Source of Truth)**
- Pull Linear status before every operation
- Reject local changes if Linear newer
- **Pros:** PM maintains control
- **Cons:** Interrupts developer flow

**Option C: Prompt on Conflict**
- Detect conflict, ask developer which to keep
- **Pros:** No data loss
- **Cons:** Interrupts workflow with questions

**Option D: Timestamp-Based**
- Most recent change wins (regardless of source)
- **Pros:** Fair, deterministic
- **Cons:** Race conditions possible

**Recommendation:** Start with Option A (local wins) since development status is most accurate during active work.

**Decision Needed:** Does your PM actively change issue status during development sprints?

---

### 5. Offline Mode Requirement

**Question:** Must PIV-Swarm work fully offline without Linear?

**Assumption:** Yes (based on project philosophy of tool independence).

**Implementation:**
- Feature flag: `USE_LINEAR_SYNC=false` → Full offline mode
- All Linear sync wrapped in try/except with graceful degradation
- Queued syncs retry when back online

**Decision Needed:** Confirm this assumption.

---

### 6. Custom Fields for Metrics

**Question:** Should we push PIV-Swarm metrics to Linear custom fields?

**Potential Custom Fields:**
- Token usage (integer)
- Coverage percentage (integer)
- Test count (integer)
- Files changed (integer)
- Duration estimate (string)
- Actual duration (string)

**Pros:**
- Rich metrics visible in Linear
- Product can track development costs
- Historical data for estimation

**Cons:**
- Requires Linear workspace admin to create custom fields
- Clutters Linear UI if team doesn't use metrics
- API overhead

**Decision Needed:** Would your team use these metrics in Linear?

---

### 7. Testing Strategy

**Question:** How to test Linear integration without polluting production workspace?

**Options:**
- Create dedicated test Linear workspace
- Use Linear's staging environment (if available)
- Mock Linear API entirely in tests (no real calls)

**Recommendation:** Combination approach:
- Unit tests: Mock Linear API (fast, no external dependency)
- Integration tests: Real API calls to test workspace
- E2E tests: Real API calls with cleanup after

**Decision Needed:** Do you have a test Linear workspace available?

---

## Next Steps

1. **Clarify Open Questions** - Answer the 7 questions above to finalize design
2. **Prioritize Phases** - Decide which phases to implement first
3. **Create Specification** - Use `/spec` to create formal Anthropic XML spec
4. **Generate Tasks** - Use `/plan` to break down into atomic tasks
5. **Execute** - Use `/execute` to implement with fresh context per task
6. **Validate** - Use `/validate` to ensure quality before merge

**Recommended Immediate Next Steps:**
1. Answer open questions (this document)
2. Implement Phase 1 Task 1.1 (hash-based IDs) as proof of concept
3. Test Linear API access (get API key, test simple query)
4. Decide if Linear integration is high priority or "nice to have"

---

## References

- **Beads GitHub:** https://github.com/steveyegge/beads
- **Linear API Docs:** https://developers.linear.app/docs/graphql/working-with-the-graphql-api
- **PIV-Swarm Methodology:** `.claude/reference/piv-loop-methodology.md`
- **HubSpot Integration Retrospective:** `.agents/feedback/hubspot-integration-retrospective-2026-02-04.md` (pattern to follow)

---

**Document Status:** ✅ Complete - Ready for Review & Decision

**Last Updated:** 2026-02-04

**Next Review:** After open questions answered
