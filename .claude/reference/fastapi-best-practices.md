# FastAPI Best Practices

Reference guide for FastAPI patterns used in this project.

---

## Router Organization

### Standard Router Structure

```python
"""
{Module description}
"""

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from app.services.{service_name} import {ServiceName}
from app.models.{model_name} import {ModelName}
from app.schemas.{schema_name} import {SchemaCreate, SchemaUpdate, SchemaResponse}

router = APIRouter(prefix="/api/v1/{resource}", tags=["{resource}"])

# Dependency injection
def get_{service_name}() -> {ServiceName}:
    """Dependency injection for {ServiceName}."""
    return {ServiceName}()
```

**Key Points:**
- Prefix with `/api/v1/` for versioning
- Use tags for OpenAPI documentation grouping
- Dependency injection for services (not direct instantiation)
- Import models and schemas separately

---

## Dependency Injection

### Service Dependencies

```python
# ✅ GOOD: Dependency injection
@router.get("/{id}", response_model=DealResponse)
async def get_deal(
    id: str,
    service: DealService = Depends(get_deal_service)
) -> DealResponse:
    return await service.get_deal(id)

# ❌ BAD: Direct instantiation
@router.get("/{id}")
async def get_deal(id: str):
    service = DealService()  # Don't do this
    return await service.get_deal(id)
```

**Why:** Dependency injection enables testing, mocking, and lifecycle management.

---

## Async vs Sync Endpoints

### Use Async When:
- Calling external APIs (httpx)
- Database operations (async drivers)
- AWS services (aioboto3)
- File I/O (aiofiles)
- Multiple concurrent operations

```python
@router.get("/{deal_id}")
async def get_deal(
    deal_id: str,
    service: DealService = Depends(get_deal_service)
) -> DealResponse:
    """Async for external API call."""
    return await service.fetch_from_hubspot(deal_id)
```

### Use Sync When:
- Pure computation
- No I/O operations
- Quick transformations

```python
@router.post("/calculate")
def calculate_total(request: CalculationRequest) -> CalculationResponse:
    """Sync for pure computation."""
    total = sum(item.amount for item in request.items)
    return CalculationResponse(total=total)
```

---

## Response Models

### Always Use response_model

```python
# ✅ GOOD: Explicit response model
@router.get("/{id}", response_model=DealResponse)
async def get_deal(id: str, service: DealService = Depends(get_deal_service)):
    return await service.get_deal(id)

# ❌ BAD: No response model
@router.get("/{id}")
async def get_deal(id: str, service: DealService = Depends(get_deal_service)):
    return await service.get_deal(id)  # What structure is returned?
```

**Benefits:**
- Automatic validation
- OpenAPI documentation
- Type safety
- Response filtering

---

## Request/Response Schemas

### Separate Schemas for Different Operations

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# Base schema with common fields
class DealBase(BaseModel):
    """Base deal schema."""
    name: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0)
    stage: str

# Create schema (input)
class DealCreate(DealBase):
    """Schema for creating deals."""
    pass

# Update schema (partial input)
class DealUpdate(BaseModel):
    """Schema for updating deals - all fields optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0)
    stage: Optional[str] = None

# Response schema (output with DB fields)
class DealResponse(DealBase):
    """Schema for deal responses."""
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
```

**Pattern:**
- `{Model}Base` - Shared fields
- `{Model}Create` - Required fields for creation
- `{Model}Update` - Optional fields for updates
- `{Model}Response` - Complete model with DB fields

---

## Error Handling

### HTTP Exceptions

```python
from fastapi import HTTPException, status

@router.get("/{id}")
async def get_deal(id: str, service: DealService = Depends(get_deal_service)):
    try:
        return await service.get_deal(id)
    except EntityNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deal not found: {id}"
        )
    except ExternalAPIError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="External service unavailable"
        )
```

**Status Codes:**
- `200 OK` - Successful GET
- `201 CREATED` - Successful POST
- `204 NO_CONTENT` - Successful DELETE
- `400 BAD_REQUEST` - Validation error
- `404 NOT_FOUND` - Resource not found
- `422 UNPROCESSABLE_ENTITY` - Pydantic validation error (automatic)
- `500 INTERNAL_SERVER_ERROR` - Server error
- `503 SERVICE_UNAVAILABLE` - External service down

---

## Path Parameters vs Query Parameters

### Path Parameters: Resource Identifiers

```python
@router.get("/{deal_id}")  # Required identifier
async def get_deal(deal_id: str):
    pass

@router.get("/{deal_id}/contacts/{contact_id}")  # Nested resources
async def get_deal_contact(deal_id: str, contact_id: str):
    pass
```

### Query Parameters: Filters and Options

```python
@router.get("/")
async def list_deals(
    stage: Optional[str] = None,        # Optional filter
    skip: int = 0,                       # Pagination
    limit: int = 100,                    # Pagination
    sort_by: str = "created_at"          # Sorting
):
    pass
```

---

## Request Body Validation

```python
from pydantic import Field, field_validator

class WebhookPayload(BaseModel):
    event_type: str = Field(..., min_length=1)
    deal_id: str = Field(..., regex=r"^\d+$")
    timestamp: datetime

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        allowed = ['deal.created', 'deal.updated', 'deal.deleted']
        if v not in allowed:
            raise ValueError(f"Invalid event_type. Must be one of: {allowed}")
        return v

@router.post("/webhook")
async def receive_webhook(payload: WebhookPayload):  # Auto-validates
    return {"status": "received"}
```

---

## Background Tasks

```python
from fastapi import BackgroundTasks

async def send_notification(user_id: str, message: str):
    """Background task."""
    # Send notification logic
    pass

@router.post("/deals")
async def create_deal(
    deal: DealCreate,
    background_tasks: BackgroundTasks,
    service: DealService = Depends(get_deal_service)
):
    result = await service.create_deal(deal)
    background_tasks.add_task(send_notification, result.id, "Deal created")
    return result
```

---

## Middleware

### Add Logging/Timing Middleware

```python
import time
from fastapi import Request
import structlog

logger = structlog.get_logger()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing."""
    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time
    logger.info(
        "request_processed",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        duration=duration
    )

    return response
```

---

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],  # Specific origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

**Never use in production:**
```python
allow_origins=["*"]  # ❌ Security risk
```

---

## Startup and Shutdown Events

```python
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Application starting up")
    # Initialize database connections
    # Warm up caches
    # Verify external service connectivity

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Application shutting down")
    # Close database connections
    # Flush logs
```

---

## Lambda Integration (Mangum)

```python
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

# Add routes...

# Lambda handler
lambda_handler = Mangum(app, lifespan="off")
```

**Key Points:**
- Set `lifespan="off"` for Lambda (no persistent state)
- Environment variables via Lambda configuration
- Cold start optimization (minimize imports)

---

## Testing FastAPI Routes

### Unit Test with TestClient

```python
from fastapi.testclient import TestClient
from unittest.mock import Mock, patch

def test_get_deal():
    """Test GET /api/v1/deals/{id} endpoint."""
    # Arrange
    client = TestClient(app)
    mock_service = Mock()
    mock_service.get_deal.return_value = DealResponse(
        id="123",
        name="Test Deal",
        amount=Decimal("1000.00")
    )

    # Act
    with patch('app.routes.deals.get_deal_service', return_value=mock_service):
        response = client.get("/api/v1/deals/123")

    # Assert
    assert response.status_code == 200
    assert response.json()["name"] == "Test Deal"
```

---

## Common Patterns

### Pagination

```python
from typing import List, Generic, TypeVar

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    skip: int
    limit: int

@router.get("/", response_model=PaginatedResponse[DealResponse])
async def list_deals(skip: int = 0, limit: int = 100):
    items = await service.list_deals(skip=skip, limit=limit)
    total = await service.count_deals()
    return PaginatedResponse(items=items, total=total, skip=skip, limit=limit)
```

### Health Check

```python
@router.get("/health")
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC),
        "version": "0.6.2"
    }
```

---

## Anti-Patterns to Avoid

### ❌ Don't Return Dict Directly

```python
# ❌ BAD
@router.get("/{id}")
async def get_deal(id: str):
    return {"id": id, "name": "Deal"}  # Untyped

# ✅ GOOD
@router.get("/{id}", response_model=DealResponse)
async def get_deal(id: str) -> DealResponse:
    return DealResponse(id=id, name="Deal")
```

### ❌ Don't Catch All Exceptions

```python
# ❌ BAD
try:
    result = await service.get_deal(id)
except Exception:  # Too broad
    raise HTTPException(500, "Error")

# ✅ GOOD
try:
    result = await service.get_deal(id)
except EntityNotFoundError:
    raise HTTPException(404, f"Deal not found: {id}")
except ExternalAPIError as e:
    logger.error(f"API error: {e}")
    raise HTTPException(503, "Service unavailable")
```

### ❌ Don't Block Async Endpoints

```python
# ❌ BAD: Blocking in async endpoint
@router.get("/{id}")
async def get_deal(id: str):
    response = requests.get(url)  # Blocking call!
    return response.json()

# ✅ GOOD: Use async client
@router.get("/{id}")
async def get_deal(id: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    return response.json()
```

---

## Performance Tips

1. **Use async for I/O** - External APIs, databases, files
2. **Connection pooling** - Reuse HTTP clients when possible
3. **Caching** - Cache expensive computations
4. **Pagination** - Limit result sets
5. **Field selection** - Only return needed fields
6. **Compression** - Enable gzip middleware

---

## Security Checklist

- [ ] Input validation with Pydantic
- [ ] Authentication on protected routes
- [ ] CORS configured properly
- [ ] Rate limiting on public endpoints
- [ ] No secrets in code
- [ ] HTTPS only in production
- [ ] SQL injection prevention (use ORMs)
- [ ] XSS prevention (auto-escaped responses)

---

## References

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Models](https://docs.pydantic.dev/latest/)
- [Dependency Injection](https://fastapi.tiangolo.com/tutorial/dependencies/)
- [Testing](https://fastapi.tiangolo.com/tutorial/testing/)
