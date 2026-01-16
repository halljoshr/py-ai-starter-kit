# Database Naming Standards

Comprehensive database naming conventions for tables, fields, repositories, models, and API routes.

---

## Entity-Specific Primary Keys

All database tables use entity-specific primary keys for clarity and consistency:

```sql
-- ✅ STANDARDIZED: Entity-specific primary keys
sessions.session_id UUID PRIMARY KEY
leads.lead_id UUID PRIMARY KEY
messages.message_id UUID PRIMARY KEY
daily_metrics.daily_metric_id UUID PRIMARY KEY
agencies.agency_id UUID PRIMARY KEY
```

**Why entity-specific?**
- Self-documenting: `lead_id` is clearer than generic `id`
- Prevents ambiguity in joins and foreign keys
- Makes SQL queries more readable
- Consistent across the entire schema

---

## Field Naming Conventions

### Primary Keys
```sql
-- Pattern: {entity}_id
session_id, lead_id, message_id, agency_id
```

### Foreign Keys
```sql
-- Pattern: {referenced_entity}_id
session_id REFERENCES sessions(session_id)
agency_id REFERENCES agencies(agency_id)
lead_id REFERENCES leads(lead_id)
```

**Always match the referenced table's primary key name.**

### Timestamps
```sql
-- Pattern: {action}_at
created_at    -- When record was created
updated_at    -- When record was last modified
started_at    -- When process/session started
expires_at    -- When record/session expires
completed_at  -- When process completed
deleted_at    -- For soft deletes
```

### Booleans
```sql
-- Pattern: is_{state}
is_connected   -- Connection status
is_active      -- Active/inactive status
is_qualified   -- Qualification status
is_verified    -- Verification status
has_errors     -- Error presence
```

### Counts
```sql
-- Pattern: {entity}_count
message_count       -- Number of messages
lead_count          -- Number of leads
notification_count  -- Number of notifications
attempt_count       -- Number of attempts
```

### Durations
```sql
-- Pattern: {property}_{unit}
duration_seconds   -- Duration in seconds
timeout_minutes    -- Timeout in minutes
interval_hours     -- Interval in hours
retention_days     -- Retention period in days
```

### Status Fields
```sql
-- Pattern: {entity}_status
lead_status        -- Status of lead (e.g., 'qualified', 'disqualified')
session_status     -- Status of session (e.g., 'active', 'ended')
payment_status     -- Status of payment (e.g., 'pending', 'completed')
```

---

## Repository Pattern Auto-Derivation

The enhanced BaseRepository automatically derives table names and primary keys from the model class name.

### Convention-Based Repositories

```python
from app.repositories.base import BaseRepository
from app.models import Lead, AvatarSession, Message

# ✅ STANDARDIZED: Convention-based repositories
class LeadRepository(BaseRepository[Lead]):
    def __init__(self):
        super().__init__()  # Auto-derives "leads" and "lead_id"

class SessionRepository(BaseRepository[AvatarSession]):
    def __init__(self):
        super().__init__()  # Auto-derives "sessions" and "session_id"

class MessageRepository(BaseRepository[Message]):
    def __init__(self):
        super().__init__()  # Auto-derives "messages" and "message_id"
```

### Derivation Rules

1. **Table Name**: Pluralize model class name, convert to snake_case
   - `Lead` → `leads`
   - `AvatarSession` → `avatar_sessions`
   - `DailyMetric` → `daily_metrics`

2. **Primary Key**: Snake_case model name + `_id`
   - `Lead` → `lead_id`
   - `AvatarSession` → `avatar_session_id`
   - `DailyMetric` → `daily_metric_id`

### Benefits

- ✅ Self-documenting schema
- ✅ Clear foreign key relationships
- ✅ Eliminates repository method overrides
- ✅ Consistent with entity naming patterns
- ✅ No manual configuration needed

---

## Model-Database Alignment

Models mirror database fields exactly to eliminate field mapping complexity.

### Exact Field Matching

```python
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from datetime import datetime, UTC

# ✅ STANDARDIZED: Models mirror database exactly
class Lead(BaseModel):
    lead_id: UUID = Field(default_factory=uuid4)  # Matches DB column
    session_id: UUID                               # Matches DB column
    agency_id: str                                 # Matches DB column
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    is_qualified: bool = False
    lead_status: str = "new"

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
        alias_generator=None  # Use exact field names (no camelCase conversion)
    )
```

### Why Exact Matching?

- ✅ No field mapping layer needed
- ✅ What you see in Python is what's in the database
- ✅ Simpler debugging (field names match everywhere)
- ✅ No confusion between `leadId` (API) and `lead_id` (DB)
- ✅ Direct ORM mapping with `from_attributes=True`

---

## API Route Standards

RESTful endpoints with consistent parameter naming.

### Standard CRUD Routes

```python
from fastapi import APIRouter, HTTPException, Depends
from uuid import UUID

router = APIRouter(prefix="/api/v1/leads", tags=["leads"])

# Collection endpoints
@router.get("/")
async def list_leads() -> list[LeadResponse]:
    """List all leads"""
    pass

@router.post("/", status_code=201)
async def create_lead(lead: LeadCreate) -> LeadResponse:
    """Create a new lead"""
    pass

# Resource endpoints (use {entity}_id pattern)
@router.get("/{lead_id}")
async def get_lead(lead_id: UUID) -> LeadResponse:
    """Get a specific lead"""
    pass

@router.put("/{lead_id}")
async def update_lead(lead_id: UUID, lead: LeadUpdate) -> LeadResponse:
    """Update a specific lead"""
    pass

@router.delete("/{lead_id}", status_code=204)
async def delete_lead(lead_id: UUID):
    """Delete a specific lead"""
    pass
```

### Sub-Resource Routes

```python
# Sub-resources: /{parent_id}/{sub_resource}
@router.get("/{lead_id}/messages")
async def list_lead_messages(lead_id: UUID) -> list[MessageResponse]:
    """Get all messages for a lead"""
    pass

# Filter by foreign key: /resource?{foreign_key}_id={value}
@router.get("/")
async def list_leads(agency_id: str | None = None) -> list[LeadResponse]:
    """List leads, optionally filtered by agency"""
    pass

# Alternative filter route: /{foreign_key}/{value}
@router.get("/agency/{agency_id}")
async def list_leads_by_agency(agency_id: str) -> list[LeadResponse]:
    """Get all leads for an agency"""
    pass
```

### Path Parameter Naming

**Always use the same name as the database field:**

```python
# ✅ GOOD: Matches database field
@router.get("/{lead_id}")
async def get_lead(lead_id: UUID):
    pass

# ❌ BAD: Doesn't match database
@router.get("/{id}")  # Too generic
async def get_lead(id: UUID):
    pass
```

---

## Complete Example

### Database Schema

```sql
CREATE TABLE leads (
    lead_id UUID PRIMARY KEY,
    session_id UUID NOT NULL REFERENCES sessions(session_id),
    agency_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP,
    is_qualified BOOLEAN DEFAULT FALSE,
    lead_status VARCHAR(50) DEFAULT 'new',
    qualification_score INTEGER
);
```

### Pydantic Model

```python
from pydantic import BaseModel, Field, ConfigDict
from uuid import UUID, uuid4
from datetime import datetime, UTC

class Lead(BaseModel):
    lead_id: UUID = Field(default_factory=uuid4)
    session_id: UUID
    agency_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime | None = None
    is_qualified: bool = False
    lead_status: str = "new"
    qualification_score: int | None = None

    model_config = ConfigDict(from_attributes=True)
```

### Repository

```python
class LeadRepository(BaseRepository[Lead]):
    def __init__(self):
        super().__init__()  # Auto-derives table="leads", pk="lead_id"

    async def find_by_agency(self, agency_id: str) -> list[Lead]:
        """Find all leads for an agency."""
        query = "SELECT * FROM leads WHERE agency_id = $1"
        return await self.fetch_all(query, agency_id)
```

### API Route

```python
router = APIRouter(prefix="/api/v1/leads", tags=["leads"])

@router.get("/{lead_id}")
async def get_lead(
    lead_id: UUID,
    repo: LeadRepository = Depends(get_lead_repository)
) -> LeadResponse:
    """Get a specific lead by ID."""
    lead = await repo.find_by_id(lead_id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadResponse.model_validate(lead)

@router.get("/agency/{agency_id}")
async def list_leads_by_agency(
    agency_id: str,
    repo: LeadRepository = Depends(get_lead_repository)
) -> list[LeadResponse]:
    """Get all leads for an agency."""
    leads = await repo.find_by_agency(agency_id)
    return [LeadResponse.model_validate(lead) for lead in leads]
```

---

## Quick Reference

### Naming Patterns

| Type | Pattern | Example |
|------|---------|---------|
| Table | `{entities}` | `leads`, `sessions`, `messages` |
| Primary Key | `{entity}_id` | `lead_id`, `session_id` |
| Foreign Key | `{referenced_entity}_id` | `session_id`, `agency_id` |
| Timestamp | `{action}_at` | `created_at`, `updated_at` |
| Boolean | `is_{state}` | `is_active`, `is_qualified` |
| Count | `{entity}_count` | `message_count`, `lead_count` |
| Duration | `{property}_{unit}` | `duration_seconds`, `timeout_minutes` |
| Status | `{entity}_status` | `lead_status`, `session_status` |

### Path Parameters

| Route | Parameter | Type |
|-------|-----------|------|
| `/api/v1/leads/{lead_id}` | `lead_id` | UUID |
| `/api/v1/sessions/{session_id}` | `session_id` | UUID |
| `/api/v1/leads/agency/{agency_id}` | `agency_id` | str |

---

## See Also

- [NAMING_CONVENTIONS.md](../../NAMING_CONVENTIONS.md) - Complete naming standards
- [fastapi-best-practices.md](./fastapi-best-practices.md) - API endpoint patterns
- [pydantic-best-practices.md](./pydantic-best-practices.md) - Model validation
