# Plan Feature Command

**Create comprehensive feature plans with all context for one-pass implementation success.**

---

## Arguments

```
/plan-feature {feature-name}
```

**Example:**
```
/plan-feature hubspot-webhook-validation
/plan-feature debt-assessment-agent
/plan-feature user-authentication
```

---

## Purpose

Generate a complete, comprehensive Plan (formerly PRP) that provides ALL necessary context for a Claude Code agent to implement the feature successfully in one pass.

**Philosophy:** "Context is King" - The more context, references, patterns, and gotchas you provide upfront, the higher the success rate.

---

## Five-Phase Planning Process

### Phase 1: Feature Understanding

**Goal:** Deeply understand the problem before designing a solution.

**Process:**
1. **Read Feature Requirements**
   - If a feature file exists, read it completely
   - Extract user stories and acceptance criteria
   - Identify core problems to solve
   - Understand user value proposition

2. **Assess Complexity**
   - Estimate scope (small/medium/large)
   - Identify dependencies on other systems
   - Flag potential challenges
   - Determine if phased approach needed

3. **Map Affected Systems**
   - Which services need changes?
   - Which data models affected?
   - Which APIs involved?
   - Which tests need updates?

**Output:** Clear problem statement and complexity assessment

---

### Phase 2: Codebase Intelligence

**Goal:** Find existing patterns to follow and files to reference.

**Process:**

1. **Search for Similar Features**
   ```bash
   # Find similar implementations
   rg "similar_feature_name" --files-with-matches

   # Find similar patterns
   rg "class.*Service" app/services/ -l
   rg "@router\.(get|post)" app/routes/ -l
   ```

2. **Identify Files to Reference**
   - Service implementations: `app/services/example_service.py`
   - Data models: `app/models/example.py`
   - API routes: `app/routes/example.py`
   - Test patterns: `tests/integration/test_example.py`

   **Document specific line numbers:**
   - "Lines 45-67: Webhook signature validation pattern"
   - "Lines 120-145: Error handling approach"
   - "Lines 89-110: Pydantic model with validators"

3. **Note Existing Conventions**
   - From CLAUDE.md
   - From `.claude/reference/` docs
   - From recent plans in `.agents/plans/`
   - From similar existing code

4. **Check Test Patterns**
   ```bash
   # Find test patterns for similar features
   rg "def test_.*webhook" tests/ -A 5
   rg "@pytest.mark" tests/ | head -20
   ```

**Output:** Context reference table with file paths and specific line numbers

---

### Phase 3: External Research

**Goal:** Gather documentation, examples, and best practices from external sources.

**Process:**

1. **Library Documentation**
   - Official docs for frameworks/libraries used
   - **Include specific URLs with anchors**
   - Example: `https://docs.pydantic.dev/latest/concepts/validators/#field-validators`

2. **Implementation Examples**
   - GitHub repositories with similar features
   - StackOverflow solutions (vetted and recent)
   - Blog posts with working examples
   - **Include URLs for agent to reference**

3. **Best Practices**
   - Security considerations (OWASP if relevant)
   - Performance patterns
   - Error handling strategies
   - Testing approaches

4. **Common Pitfalls**
   - Known issues with libraries/versions
   - Edge cases to handle
   - Performance gotchas
   - Security vulnerabilities to avoid

**Output:** Curated list of URLs and documentation references

---

### Phase 4: Strategic Thinking

**Goal:** Design the implementation approach considering all constraints.

**Process:**

1. **Architecture Fit**
   - Does this fit existing patterns?
   - Does it violate any principles?
   - Will it scale appropriately?
   - Is it maintainable?

2. **Dependency Analysis**
   - What must be implemented first?
   - What can be done in parallel?
   - What external dependencies needed?
   - What new packages required?

3. **Edge Cases**
   - What inputs might be invalid?
   - What external services might fail?
   - What race conditions possible?
   - What security vulnerabilities exist?

4. **Performance Implications**
   - Will this be fast enough?
   - Any N+1 query risks?
   - Caching needed?
   - Async vs sync considerations?

5. **Security Concerns**
   - Input validation needed?
   - Authentication/authorization?
   - Secrets management?
   - Rate limiting required?

6. **Maintainability**
   - Is the design simple?
   - Is it testable?
   - Is it documented?
   - Can others understand it?

**Output:** Strategic decisions documented with rationale

---

### Phase 5: Plan Generation

**Goal:** Create structured, complete plan document ready for implementation.

**Process:**

1. **Use Plan Template** (see below)
2. **Include ALL context** from phases 1-4
3. **Write complete code examples** (not pseudocode)
4. **Create context reference table** with specific line numbers
5. **Define atomic tasks** with full task structure
6. **Document gotchas explicitly**
7. **Specify validation commands** for each task
8. **Score confidence** (1-10 for one-pass success)

---

## Plan Document Template

```markdown
# Feature Name

**Plan ID:** {feature-name}
**Created:** {Date}
**Confidence Score:** X/10

---

## Feature Understanding

### Problem Statement
{Clear 2-3 sentence description of the problem}

### User Value
{What value does this provide? Who benefits?}

### Complexity Assessment
- **Scope:** Small / Medium / Large
- **Dependencies:** {List systems/services affected}
- **Challenges:** {Potential difficulties}
- **Approach:** {Single-phase or multi-phase}

---

## Context References

**Files to reference during implementation:**

| File | Purpose | Specific Lines | Reason |
|------|---------|----------------|--------|
| app/services/example_service.py | Service pattern | Lines 45-67 | Shows standard service structure |
| app/routes/example.py | Route pattern | Lines 23-45 | Shows FastAPI router setup |
| app/models/example.py | Model pattern | Lines 89-110 | Shows Pydantic model with validators |
| tests/integration/test_example.py | Test pattern | Lines 120-145 | Shows integration test structure |

**Reference Documentation:**
- [FastAPI Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Pydantic V2 Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [pytest-asyncio Usage](https://pytest-asyncio.readthedocs.io/en/latest/)

**Internal Reference Docs:**
- `.claude/reference/fastapi-best-practices.md` - Router organization
- `.claude/reference/pydantic-best-practices.md` - Model validation
- `.claude/reference/pytest-best-practices.md` - Testing patterns

---

## Patterns to Follow

### Example 1: Service Pattern

From `app/services/hubspot_service.py:45-67`:

```python
class HubSpotService:
    """Service for HubSpot API interactions."""

    def __init__(self):
        self.api_key = get_settings().hubspot_api_key
        self.base_url = "https://api.hubapi.com"

    async def get_deal(self, deal_id: str) -> Dict[str, Any]:
        """Retrieve deal from HubSpot."""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/crm/v3/objects/deals/{deal_id}",
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()
            return response.json()
```

**Why this pattern:** Standard service structure with dependency injection, async/await, proper error handling.

### Example 2: Pydantic Model with Validators

From `app/models/webhook.py:89-110`:

```python
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class WebhookPayload(BaseModel):
    """Webhook payload validation."""

    event_type: str = Field(..., min_length=1)
    timestamp: datetime
    deal_id: Optional[str] = None

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        allowed = ['deal.created', 'deal.updated', 'deal.deleted']
        if v not in allowed:
            raise ValueError(f"Invalid event_type: {v}")
        return v

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True
    )
```

**Why this pattern:** Pydantic v2 syntax, explicit validation, clear error messages.

---

## Implementation Tasks

### Task Dependencies
- Task 2 depends on Task 1 (data model must exist before service)
- Tasks 3-4 can be done in parallel (independent)
- Task 5 depends on all previous tasks (testing after implementation)

---

### Task 1: Create Data Model

**File:** `app/models/{model_name}.py`

- **IMPLEMENT:** Create Pydantic model for {feature} with validation
- **PATTERN:** Follow `app/models/webhook.py:89-110` (field validators, ConfigDict)
- **IMPORTS:** `from pydantic import BaseModel, Field, field_validator`
- **GOTCHA:** Use Pydantic v2 syntax (`field_validator` not `validator`), `ConfigDict` not `Config`
- **VALIDATE:** `ruff check app/models/{model_name}.py && mypy app/models/{model_name}.py`

```python
"""
{Model description}
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from datetime import datetime

class {ModelName}(BaseModel):
    """
    {Model docstring}

    Attributes:
        field1: Description
        field2: Description
    """

    field1: str = Field(..., min_length=1, max_length=255)
    field2: Optional[datetime] = None

    @field_validator('field1')
    @classmethod
    def validate_field1(cls, v: str) -> str:
        """Validate field1 meets business rules."""
        if not v.strip():
            raise ValueError("field1 cannot be empty")
        return v.strip()

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        str_strip_whitespace=True
    )
```

---

### Task 2: Create Service Implementation

**File:** `app/services/{service_name}.py`

- **IMPLEMENT:** Create service class for {feature} business logic
- **PATTERN:** Follow `app/services/hubspot_service.py:45-67` (async methods, error handling)
- **IMPORTS:** `import httpx`, `from app.models.{model} import {Model}`
- **GOTCHA:** Always use `async with httpx.AsyncClient()` for async requests, handle rate limiting
- **VALIDATE:** `uv run pytest tests/unit/test_{service_name}.py -v`

```python
"""
{Service description}
"""

import httpx
from typing import Dict, Any
from app.config.settings import get_settings
from app.models.{model_name} import {ModelName}

class {ServiceName}:
    """
    {Service docstring}

    Handles {description of responsibilities}.
    """

    def __init__(self):
        """Initialize service with configuration."""
        self.settings = get_settings()
        self.api_url = self.settings.{api_url_setting}

    async def {method_name}(self, param: str) -> {ModelName}:
        """
        {Method description}

        Args:
            param: Description

        Returns:
            {ModelName} instance with validated data

        Raises:
            httpx.HTTPStatusError: If API request fails
            ValidationError: If response data invalid
        """
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.api_url}/{param}",
                headers={"Authorization": f"Bearer {self.settings.api_key}"},
                timeout=30.0
            )
            response.raise_for_status()
            data = response.json()
            return {ModelName}(**data)
```

---

### Task 3: Create API Route

**File:** `app/routes/{route_name}.py`

- **IMPLEMENT:** Create FastAPI router with endpoints for {feature}
- **PATTERN:** Follow `app/routes/example.py:23-45` (router setup, dependency injection)
- **IMPORTS:** `from fastapi import APIRouter, Depends, HTTPException`
- **GOTCHA:** Use dependency injection for services, not direct instantiation
- **VALIDATE:** `ruff check app/routes/{route_name}.py`

```python
"""
{Route description}
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.{service_name} import {ServiceName}
from app.models.{model_name} import {ModelName}

router = APIRouter(prefix="/api/v1/{resource}", tags=["{resource}"])

def get_{service_name}() -> {ServiceName}:
    """Dependency injection for {ServiceName}."""
    return {ServiceName}()

@router.get("/{id}", response_model={ModelName})
async def get_{resource}(
    id: str,
    service: {ServiceName} = Depends(get_{service_name})
) -> {ModelName}:
    """
    Retrieve {resource} by ID.

    Args:
        id: {Resource} identifier
        service: Injected service instance

    Returns:
        {ModelName} data

    Raises:
        HTTPException: 404 if not found, 500 if service error
    """
    try:
        return await service.{method_name}(id)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{resource} not found: {id}"
            )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Service error"
        )
```

---

### Task 4: Create Unit Tests

**File:** `tests/unit/test_{service_name}.py`

- **IMPLEMENT:** Unit tests for {service} with mocked dependencies
- **PATTERN:** Follow `tests/unit/test_example.py:50-80` (fixtures, mocking)
- **IMPORTS:** `import pytest`, `from unittest.mock import AsyncMock, patch`
- **GOTCHA:** Use `AsyncMock` for async methods, not `Mock`
- **VALIDATE:** `uv run pytest tests/unit/test_{service_name}.py -v`

```python
"""
Unit tests for {ServiceName}.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.services.{service_name} import {ServiceName}
from app.models.{model_name} import {ModelName}

@pytest.fixture
def service():
    """Fixture for {ServiceName} instance."""
    return {ServiceName}()

@pytest.fixture
def mock_response_data():
    """Fixture for mock API response data."""
    return {
        "field1": "test_value",
        "field2": "2025-01-14T12:00:00Z"
    }

@pytest.mark.unit
@pytest.mark.fast
@pytest.mark.asyncio
async def test_{method_name}_success(service, mock_response_data):
    """Test successful {method_name} call."""
    # Arrange
    mock_response = MagicMock()
    mock_response.json.return_value = mock_response_data
    mock_response.raise_for_status = MagicMock()

    # Act
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        result = await service.{method_name}("test_id")

    # Assert
    assert isinstance(result, {ModelName})
    assert result.field1 == "test_value"

@pytest.mark.unit
@pytest.mark.fast
@pytest.mark.asyncio
async def test_{method_name}_not_found(service):
    """Test {method_name} with 404 response."""
    # Arrange
    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "Not found", request=MagicMock(), response=mock_response
    )

    # Act & Assert
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        with pytest.raises(httpx.HTTPStatusError):
            await service.{method_name}("invalid_id")
```

---

### Task 5: Create Integration Tests

**File:** `tests/integration/test_{feature_name}.py`

- **IMPLEMENT:** Integration tests calling real API routes
- **PATTERN:** Follow `tests/integration/test_full_workflow.py:100-130` (TestClient, real dependencies)
- **IMPORTS:** `from fastapi.testclient import TestClient`
- **GOTCHA:** Integration tests require valid API keys in environment
- **VALIDATE:** `uv run pytest tests/integration/test_{feature_name}.py -v -m "not very_slow"`

```python
"""
Integration tests for {feature} feature.
"""

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.requires_api
def test_{feature}_end_to_end():
    """Test complete {feature} workflow."""
    # Arrange
    test_data = {
        "field1": "test_value",
        "field2": "2025-01-14T12:00:00Z"
    }

    # Act
    response = client.post("/api/v1/{resource}", json=test_data)

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["field1"] == test_data["field1"]
    assert "id" in data

@pytest.mark.integration
@pytest.mark.fast
def test_{feature}_validation_error():
    """Test {feature} with invalid data."""
    # Arrange
    invalid_data = {"field1": ""}  # Empty field should fail validation

    # Act
    response = client.post("/api/v1/{resource}", json=invalid_data)

    # Assert
    assert response.status_code == 422  # Validation error
    assert "field1" in response.json()["detail"][0]["loc"]
```

---

## Testing Strategy

### Unit Tests
- **Location:** `tests/unit/test_{service_name}.py`
- **Coverage:** All service methods, all validators, all edge cases
- **Mocking:** httpx.AsyncClient, external APIs, database calls
- **Markers:** `@pytest.mark.unit`, `@pytest.mark.fast`
- **Expected:** < 1 second total execution time

### Integration Tests
- **Location:** `tests/integration/test_{feature_name}.py`
- **Coverage:** End-to-end workflows, API routes, real dependencies
- **Markers:** `@pytest.mark.integration`, `@pytest.mark.slow`, `@pytest.mark.requires_api`
- **Expected:** 1-30 seconds execution time

### Coverage Expectations
- **Target:** 80%+ code coverage
- **Command:** `uv run pytest --cov=app --cov-report=term-missing --cov-fail-under=80`
- **Focus:** All business logic, validators, error handling

---

## Gotchas & Common Pitfalls

### Pydantic V2 Syntax
- ❌ OLD: `@validator('field')` → ✅ NEW: `@field_validator('field')`
- ❌ OLD: `class Config:` → ✅ NEW: `model_config = ConfigDict(...)`
- ❌ OLD: `orm_mode = True` → ✅ NEW: `from_attributes = True`

### Async/Await
- ❌ Don't use `requests` library (blocking) → ✅ Use `httpx.AsyncClient` (async)
- ❌ Don't forget `async with` context manager → ✅ Always use for resource cleanup
- ❌ Don't use `Mock` for async → ✅ Use `AsyncMock` from unittest.mock

### Testing
- ❌ Don't test implementation details → ✅ Test behavior and outcomes
- ❌ Don't use real API keys in tests → ✅ Mock external calls in unit tests
- ❌ Don't skip markers → ✅ Always add appropriate `@pytest.mark.*` decorators

### FastAPI
- ❌ Don't instantiate services in routes → ✅ Use dependency injection with `Depends()`
- ❌ Don't return dict directly → ✅ Use `response_model` with Pydantic models
- ❌ Don't catch all exceptions → ✅ Let FastAPI handle HTTPException, catch specific errors

### Security
- ❌ Don't commit secrets → ✅ Use environment variables or AWS Secrets Manager
- ❌ Don't trust user input → ✅ Validate all inputs with Pydantic
- ❌ Don't expose internal errors → ✅ Return generic 500 errors to clients

---

## Acceptance Criteria

- [ ] All data models created with Pydantic v2 syntax
- [ ] Service implementation with async/await
- [ ] API routes with dependency injection
- [ ] Unit tests with 100% method coverage
- [ ] Integration tests for happy path and error cases
- [ ] All tests passing (`uv run pytest`)
- [ ] Code coverage ≥ 80%
- [ ] Linting passes (`ruff check`)
- [ ] Type checking passes (`mypy app/`)
- [ ] No secrets in code
- [ ] Documentation in docstrings
- [ ] CHANGELOG.md updated

---

## Validation Commands

**After each task:**
```bash
# Syntax and style
ruff check {file}

# Type checking
mypy {file}

# Unit tests
uv run pytest tests/unit/test_{name}.py -v
```

**Before commit:**
```bash
# Full validation
/validate

# Or manually:
ruff check app/ tests/
mypy app/
uv run pytest tests/unit/ -v
uv run pytest tests/integration/ -m "not very_slow" -v
uv run pytest --cov=app --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## Confidence Score: X/10

**Rationale:**
- [+1] Clear problem statement and requirements
- [+1] Comprehensive context references with line numbers
- [+1] Complete code examples (not pseudocode)
- [+1] Explicit gotchas documented
- [+1] Atomic tasks with validation commands
- [+1] Testing strategy defined
- [+1] Similar patterns exist in codebase
- [+1] External documentation referenced
- [+1] Dependencies clearly identified
- [+1] Security and edge cases considered

**Score interpretation:**
- 8-10: High confidence, one-pass success likely
- 6-7: Medium confidence, minor iterations expected
- 4-5: Low confidence, significant unknowns remain
- 1-3: Very low confidence, needs more research

**If score < 8, improve by:**
- Adding more context references
- Including more code examples
- Researching unknowns
- Breaking down complex tasks further
- Documenting more gotchas

---

## Output Location

Save plan as: `.agents/plans/{feature-name}.md`

---

## Next Steps

After plan is complete and approved:

1. **Review plan with user** - Get approval before implementation
2. **Execute plan:** `/implement-plan .agents/plans/{feature-name}.md`
3. **Validate:** `/validate`
4. **Generate report:** `/execution-report .agents/plans/{feature-name}.md`
5. **Commit:** `/commit`

---

## Quality Checklist

Before considering plan complete:

- [ ] Feature Understanding section complete
- [ ] Context References table with specific line numbers
- [ ] Patterns section with real code examples
- [ ] All tasks follow IMPLEMENT/PATTERN/IMPORTS/GOTCHA/VALIDATE structure
- [ ] Complete code blocks (not pseudocode)
- [ ] Testing Strategy defined
- [ ] Gotchas documented
- [ ] Acceptance Criteria checklist
- [ ] Validation commands specified
- [ ] Confidence score ≥ 8/10
- [ ] Saved to `.agents/plans/{feature-name}.md`

---

## Remember

**The goal is one-pass implementation success through comprehensive context.**

More context upfront = Fewer iterations during implementation = Faster delivery.
