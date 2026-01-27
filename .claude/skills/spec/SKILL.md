---
name: spec
description: Build comprehensive app specification in Anthropic XML format. Smart defaults, minimal questions.
disable-model-invocation: true
argument-hint: "[ticket-file]"
allowed-tools: Read, Write, Glob, AskUserQuestion, Grep
---

# App Specification Builder

**Build comprehensive app specification in Anthropic XML format with smart defaults and minimal questions.**

---

## Purpose

Create a formal application specification that serves as the source of truth for `/plan` and `/execute`. Makes smart architectural decisions based on context, only asks when truly ambiguous.

**Philosophy:** "Decide once, implement deterministically" - All decisions happen in spec phase, implementation follows spec exactly.

**Output Format:** Anthropic-style XML specification with machine-readable implementation steps

---

## Process

### Step 1: Read Requirements

Read the ticket/requirements file (README.md or specified file):
- Feature description
- Requirements list
- Acceptance criteria
- Performance targets
- Scope boundaries

### Step 2: Extract Explicit Decisions

Identify what's **already specified** in the ticket and extract decisions:

| Ticket Says | Decision |
|-------------|----------|
| "10M+ rows" | PostgreSQL (performance required) |
| "Use Faker" | Faker library for data generation |
| "Query < 500ms" | Indexing + caching required |
| "Demo/test/example" | SQLite, no auth |
| "Production" | Postgres, Redis, auth |

**Do not ask about anything explicitly stated.**

### Step 3: Apply Smart Defaults

**Database:**
```
IF "demo" OR "test" OR "example" OR "prototype"
  → SQLite
ELSE IF "10M+ rows" OR "production" OR "scale"
  → PostgreSQL
ELSE IF < 5 models AND < 10 endpoints
  → SQLite
ELSE
  → Ask user
```

**Caching:**
```
IF perf < 100ms AND multiple reads
  → Ask about Redis
ELSE IF perf < 500ms
  → In-memory LRU cache
ELSE
  → No caching (v1)
```

**Auth:**
```
IF "demo" OR "test" OR "internal"
  → No auth (v1)
ELSE IF "public API" OR "user accounts"
  → Ask: JWT, API keys, or session?
ELSE
  → No auth
```

**Async:**
```
IF "webhooks" OR "external API" OR "third-party"
  → Async (FastAPI + httpx)
ELSE IF perf < 100ms OR high concurrency
  → Async
ELSE
  → Sync
```

### Step 4: Ask Questions (Only When Needed)

Use AskUserQuestion for:
- Not specified in ticket
- No clear smart default
- Critical architectural decision

### Step 5: Generate Anthropic XML Spec

Output specification in Anthropic XML format.

**Save to:** `.agents/specs/{feature-name}-spec.txt`

---

## Anthropic XML Format

```xml
<project_specification>

<project_name>
{Feature Name}
</project_name>

<overview>
{2-3 sentence description of what this builds}
</overview>

<technology_stack>
  <framework>
    - FastAPI 0.115.0+ (Web framework)
    - Pydantic v2 (Data validation)
    - SQLAlchemy 2.0+ (ORM if database)
  </framework>

  <database>
    - PostgreSQL 15+ (chosen because: 10M+ rows, performance)
    OR
    - SQLite (chosen because: demo project, simple)
  </database>

  <external_dependencies>
    - Faker (realistic test data)
    - httpx (async HTTP)
  </external_dependencies>

  <testing>
    - pytest 8.0+ (testing framework)
    - pytest-asyncio (async tests)
    - pytest-cov (coverage, 80% minimum)
  </testing>

  <quality_tools>
    - ruff (linting/formatting)
    - mypy (type checking)
    - UV (package management)
  </quality_tools>
</technology_stack>

<core_features>
  <feature_group_1>
    - Bullet point of what this feature does
    - Another key capability
    - Success criteria
  </feature_group_1>

  <feature_group_2>
    - More features
  </feature_group_2>
</core_features>

<data_models>
  <model_name>
    ClassName:
    - field_name: type (description)
    - another_field: type
    - computed_field: type (computed via validator)

    Validation:
    - Rule 1
    - Rule 2

    Indexes (if database):
    - field_name
    - (composite_field_1, composite_field_2)
  </model_name>
</data_models>

<api_endpoints>
  <endpoint_group>
    POST /api/v1/resource
    - Purpose: What it does
    - Request: RequestModel
    - Response: ResponseModel
    - Performance: < 100ms
    - Validation: Rules

    GET /api/v1/resource/{id}
    - Purpose: Retrieve resource
    - etc.
  </endpoint_group>
</api_endpoints>

<services_to_implement>
  <service_name>
    File: src/services/service_name.py

    Purpose: What this service does

    Methods:
    - async def method_name(param: Type) -> ReturnType
      Purpose: What it does
      Errors: What exceptions it raises

    Dependencies:
    - DatabaseConnection
    - ExternalAPIClient

    Patterns to follow:
    - .claude/reference/fastapi-best-practices.md
  </service_name>
</services_to_implement>

<database_schema>
  <table_name>
    CREATE TABLE table_name (
        id UUID PRIMARY KEY,
        field1 VARCHAR(255) NOT NULL,
        field2 TIMESTAMP,
        field3 JSONB,
        created_at TIMESTAMP DEFAULT NOW()
    );

    CREATE INDEX idx_field1 ON table_name(field1);
    CREATE INDEX idx_field2_field1 ON table_name(field2, field1);

    Why these indexes:
    - field1: Filtered in 80% of queries
    - Composite: Supports time-range + filter queries
  </table_name>
</database_schema>

<testing_strategy>
  <unit_tests>
    Location: tests/unit/
    Purpose: Test business logic in isolation
    Coverage: All service methods, validators, models
    Mocking: All I/O (database, HTTP, filesystem)
    Speed: < 1s total
    Command: uv run pytest tests/unit/ -v
  </unit_tests>

  <integration_tests>
    Location: tests/integration/
    Purpose: Test API endpoints with real dependencies
    Coverage: All API routes, database interactions
    Mocking: Minimal (real database, mock external APIs)
    Speed: 1-30s
    Command: uv run pytest tests/integration/ -v
  </integration_tests>

  <performance_tests>
    Location: tests/performance/
    Purpose: Validate performance targets with scale
    Coverage: 10M row queries, bulk inserts, concurrent requests
    Speed: > 30s
    Command: uv run pytest tests/performance/ -v
  </performance_tests>

  <coverage_requirements>
    Target: 80% minimum
    Command: uv run pytest --cov=src --cov-fail-under=80
  </coverage_requirements>
</testing_strategy>

<implementation_steps>
  <step_0>
    Task: Setup project structure and configuration
    Duration: 1 session (~15K tokens)

    Files:
    - pyproject.toml (create dependencies)
    - src/config/settings.py (Pydantic settings)
    - src/main.py (FastAPI app)
    - tests/conftest.py (pytest fixtures)

    Actions:
    - Initialize UV project with dependencies
    - Create Pydantic settings with env var support
    - Setup FastAPI app with CORS, routes
    - Create basic pytest configuration
    - Add test fixtures for database/client

    Patterns:
    - .claude/reference/fastapi-best-practices.md
    - .claude/reference/pydantic-best-practices.md

    Validation:
    - uv sync works
    - uv run uvicorn src.main:app runs
    - pytest discovers tests
    - ruff check passes
  </step_0>

  <step_1>
    Task: Implement data models
    Duration: 1 session (~20K tokens)
    TDD: Write tests first

    Files:
    - src/models/event.py (new)
    - tests/unit/models/test_event.py (new)

    Models:
    - Event (with field validators)
    - TimeSeriesAggregation

    Actions:
    - Write test cases for valid/invalid events
    - Implement Event model with Pydantic v2
    - Add field validators (timestamp range, event_type enum)
    - Add computed fields if needed
    - Test validation logic

    Patterns:
    - .claude/reference/pydantic-best-practices.md (v2 syntax)

    Validation:
    - uv run pytest tests/unit/models/ -v
    - All validators working
    - mypy passes
    - 100% test coverage for models
  </step_1>

  <step_2>
    Task: Database setup and connection
    Duration: 1 session (~20K tokens)

    Files:
    - src/db/connection.py (async engine)
    - src/db/models.py (SQLAlchemy models)
    - src/db/migrations/ (Alembic setup)
    - tests/unit/db/test_connection.py

    Actions:
    - Create async SQLAlchemy engine
    - Define ORM models matching Pydantic models
    - Setup connection pooling
    - Create indexes as specified
    - Setup Alembic migrations
    - Test connection and CRUD operations

    Patterns:
    - .claude/reference/database-standards.md

    Validation:
    - Connection pool works
    - Models create tables correctly
    - Indexes exist (check with SQL)
    - Tests pass with test database
  </step_2>

  <step_3>
    Task: Implement ingestion service
    Duration: 1 session (~25K tokens)
    TDD: Write tests first

    Files:
    - src/services/ingestion.py (new)
    - tests/unit/services/test_ingestion.py (new)

    Methods:
    - async def insert_event(event: Event) -> Event
    - async def insert_batch(events: List[Event]) -> BatchResult

    Actions:
    - Write unit tests with mocked database
    - Implement single event insert
    - Implement bulk insert with executemany()
    - Add error handling
    - Add transaction management
    - Test edge cases (duplicates, invalid data)

    Patterns:
    - .claude/reference/fastapi-best-practices.md (async patterns)
    - .claude/reference/error-handling-patterns.md

    Validation:
    - uv run pytest tests/unit/services/ -v
    - All methods tested
    - Error handling verified
    - Performance benchmarked (mock timing)
  </step_3>

  <step_4>
    Task: Implement API endpoints - Ingestion
    Duration: 1 session (~20K tokens)

    Files:
    - src/api/ingest.py (new)
    - tests/integration/test_ingest_api.py (new)

    Endpoints:
    - POST /api/v1/events
    - POST /api/v1/events/batch

    Actions:
    - Create FastAPI router
    - Implement endpoints with dependency injection
    - Add request validation
    - Add response models
    - Write integration tests with TestClient
    - Test error cases (422, 500)

    Patterns:
    - .claude/reference/fastapi-best-practices.md

    Validation:
    - uv run pytest tests/integration/test_ingest_api.py -v
    - All endpoints working
    - Validation errors handled correctly
    - Performance meets targets
  </step_4>

  ... (continue for all features)
</implementation_steps>

<session_management>
  <startup_ritual>
    Every session begins with:
    1. Read .agents/specs/{feature}-spec.txt (this file)
    2. Read .agents/state/session.yaml (current progress)
    3. git status && git log -3 (understand state)
    4. uv run pytest tests/unit/ -v --tb=short (baseline)
    5. Identify current step from session state

    Never start implementing without startup ritual.
  </startup_ritual>

  <token_budgeting>
    Target per session: 20-40K tokens
    Warning threshold: 50K tokens
    Critical threshold: 75K tokens

    If approaching 50K:
    - Complete current step
    - Update session state
    - Commit work
    - Run /pause

    Never exceed 75K tokens in single session.
  </token_budgeting>

  <progress_tracking>
    After each step:
    - Update .agents/state/session.yaml:
      - Mark step complete
      - Add completion timestamp
      - Note any blockers
      - Update token usage
    - Commit work: "feat(step-N): {description}"
    - Run validation suite
  </progress_tracking>

  <validation_gates>
    After each step:
    - ruff check {modified files}
    - mypy {modified files}
    - pytest {relevant tests} -v
    - Never commit failing tests
    - Never end session with broken code
  </validation_gates>
</session_management>

<success_criteria>
  Feature complete when:
  - All implementation steps completed
  - All tests passing (unit, integration, performance)
  - 80%+ code coverage
  - All validation gates passed
  - All acceptance criteria met (from requirements)
  - Performance targets achieved
  - Documentation complete
</success_criteria>

<constraints>
  - Line length: 100 characters max
  - File length: 500 lines max
  - Function length: 100 lines max
  - Type hints: Required on all functions
  - Pydantic: v2 syntax only
  - Async: Use async/await, not blocking I/O
</constraints>

<gotchas>
  <pydantic_v2_syntax>
    Issue: Pydantic v2 changed validator syntax
    Impact: @validator decorator no longer works
    Solution: Use @field_validator and @model_validator
    Example: .claude/reference/pydantic-best-practices.md
  </pydantic_v2_syntax>

  <async_patterns>
    Issue: Must use httpx, not requests
    Impact: requests is blocking, breaks async
    Solution: Use httpx.AsyncClient with async with
    Example: .claude/reference/fastapi-best-practices.md
  </async_patterns>

  <database_performance>
    Issue: 10M rows requires proper indexing
    Impact: Queries will be slow without indexes
    Solution: Create indexes on filtered/sorted columns
    Example: See <database_schema> section
  </database_performance>
</gotchas>

</project_specification>
```

---

## Key Points

### Implementation Steps Structure

Each step MUST include:
1. **Task**: What to build
2. **Duration**: Token estimate
3. **TDD**: If tests-first approach
4. **Files**: Exact files to create/modify
5. **Actions**: Step-by-step what to do
6. **Patterns**: Which reference docs to follow
7. **Validation**: How to verify completion

### Smart Defaults Applied

Document WHY each decision was made:
- "PostgreSQL (chosen because: 10M+ rows requirement)"
- "In-memory cache (chosen because: < 500ms target, no external deps needed)"

### Session Management

Include Anthropic's session discipline:
- Startup ritual
- Token budgets
- Progress tracking
- Validation gates

---

## Output Location

`.agents/specs/{feature-name}-spec.txt`

---

## Remember

The spec quality determines implementation quality. More details = more autonomous execution.

- Include exact file paths
- Specify which patterns to follow
- Document gotchas upfront
- Make token estimates realistic
- Break into session-sized steps (20-40K)
