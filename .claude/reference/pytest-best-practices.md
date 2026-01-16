# Pytest Best Practices

Reference guide for pytest patterns in this project.

---

## Test Structure (3-Tier)

### Unit Tests (`tests/unit/`)
- No external dependencies
- Mock all I/O (API calls, database, files)
- Fast (< 1 second per test)
- Test business logic in isolation

### Integration Tests (`tests/integration/`)
- Test service interactions
- Real or stubbed external APIs
- Database operations
- 1-30 seconds execution time

### E2E Tests (`tests/e2e/`)
- Complete user workflows
- Full system integration
- > 30 seconds execution time
- Run less frequently

---

## Markers

```python
# Speed markers
@pytest.mark.fast          # < 1 second
@pytest.mark.slow          # 1-30 seconds
@pytest.mark.very_slow     # > 30 seconds

# Service markers
@pytest.mark.hubspot
@pytest.mark.bedrock
@pytest.mark.heron

# Feature markers
@pytest.mark.flag_validation
@pytest.mark.business_risks
@pytest.mark.debt_validation

# Dependency markers
@pytest.mark.requires_api
@pytest.mark.requires_secrets

# Async tests
@pytest.mark.asyncio       # For async test functions
```

---

## Fixtures

### conftest.py Pattern

```python
# tests/conftest.py
import pytest
from app.services.deal_service import DealService

@pytest.fixture
def sample_deal_id():
    """Sample deal ID for tests."""
    return "49648948002"

@pytest.fixture
def deal_service():
    """DealService instance."""
    return DealService()

@pytest.fixture
def mock_deal_data():
    """Mock deal data."""
    return {
        "id": "123",
        "name": "Test Deal",
        "amount": "50000.00"
    }
```

---

## Unit Test Patterns

### Mocking External APIs

```python
from unittest.mock import AsyncMock, Mock, patch
import httpx

@pytest.mark.unit
@pytest.mark.fast
@pytest.mark.asyncio
async def test_get_deal_success():
    """Test successful deal retrieval."""
    # Arrange
    service = DealService()
    mock_response = Mock()
    mock_response.json.return_value = {"id": "123", "name": "Deal"}
    mock_response.raise_for_status = Mock()

    # Act
    with patch('httpx.AsyncClient') as mock_client:
        mock_client.return_value.__aenter__.return_value.get = AsyncMock(
            return_value=mock_response
        )
        result = await service.get_deal("123")

    # Assert
    assert result.id == "123"
    assert result.name == "Deal"
```

### Mocking AWS Services

```python
from unittest.mock import patch, MagicMock

@pytest.mark.unit
@pytest.mark.fast
def test_get_secret():
    """Test secrets manager retrieval."""
    mock_client = MagicMock()
    mock_client.get_secret_value.return_value = {
        'SecretString': '{"api_key": "test_key"}'
    }

    with patch('boto3.client', return_value=mock_client):
        secret = get_secret("my-secret")

    assert secret["api_key"] == "test_key"
```

---

## Integration Test Patterns

```python
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.mark.integration
@pytest.mark.slow
@pytest.mark.requires_api
def test_create_deal_integration():
    """Test deal creation with real API."""
    payload = {
        "name": "Test Deal",
        "amount": "50000.00",
        "stage": "qualification"
    }

    response = client.post("/api/v1/deals", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Deal"
    assert "id" in data
```

---

## Async Test Patterns

```python
@pytest.mark.asyncio
@pytest.mark.unit
@pytest.mark.fast
async def test_async_function():
    """Test async function."""
    result = await some_async_function()
    assert result is not None
```

**Common Issues:**
- Missing `@pytest.mark.asyncio` → "no running event loop"
- Using `Mock` instead of `AsyncMock` for async → fails
- Not awaiting async calls in tests → fails

---

## Parametrization

```python
@pytest.mark.parametrize("input,expected", [
    ("deal.created", True),
    ("deal.updated", True),
    ("deal.deleted", True),
    ("invalid.event", False),
])
def test_event_validation(input, expected):
    """Test event type validation."""
    result = is_valid_event(input)
    assert result == expected
```

---

## Exception Testing

```python
import pytest
from pydantic import ValidationError

def test_invalid_email_raises_error():
    """Test invalid email raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        User(email="not-an-email")

    assert "email" in str(exc_info.value)
```

---

## Coverage

```bash
# Run with coverage
uv run pytest --cov=app --cov=src --cov-report=term-missing

# Fail if below threshold
uv run pytest --cov=app --cov=src --cov-fail-under=80

# HTML report
uv run pytest --cov=app --cov=src --cov-report=html
open htmlcov/index.html
```

**Threshold:** 80% minimum

---

## Test Organization

```python
"""
Test module for Deal Service.

Tests cover deal retrieval, creation, and validation.
"""

import pytest
from app.services.deal_service import DealService

# Fixtures at top
@pytest.fixture
def service():
    return DealService()

# Group related tests
class TestDealRetrieval:
    """Tests for deal retrieval methods."""

    def test_get_deal_success(self, service):
        """Test successful deal retrieval."""
        pass

    def test_get_deal_not_found(self, service):
        """Test deal not found raises error."""
        pass

class TestDealCreation:
    """Tests for deal creation methods."""

    def test_create_deal_success(self, service):
        """Test successful deal creation."""
        pass
```

---

## Best Practices

✅ **DO:**
- Use descriptive test names
- One assertion focus per test
- Arrange-Act-Assert pattern
- Mock external dependencies in unit tests
- Add markers (`@pytest.mark.unit`)
- Use fixtures for common setup
- Test edge cases and error paths

❌ **DON'T:**
- Test implementation details
- Have tests depend on each other
- Use real API keys in tests
- Skip error case testing
- Forget `@pytest.mark.asyncio` for async
- Use blocking calls in async tests

---

## References

- [Pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
