# Pydantic V2 Best Practices

Reference guide for Pydantic v2 patterns used in this project.

---

## ⚠️ V2 Migration - Key Changes

### Syntax Changes (V1 → V2)

```python
# ❌ V1 SYNTAX (Don't use)
from pydantic import BaseModel, validator

class User(BaseModel):
    name: str

    @validator('name')
    def validate_name(cls, v):
        return v.strip()

    class Config:
        orm_mode = True

# ✅ V2 SYNTAX (Use this)
from pydantic import BaseModel, field_validator, ConfigDict

class User(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()

    model_config = ConfigDict(from_attributes=True)
```

**Key Changes:**
- `@validator` → `@field_validator`
- `class Config:` → `model_config = ConfigDict(...)`
- `orm_mode = True` → `from_attributes = True`
- Must add `@classmethod` decorator
- Must add type hints to validators

---

## Model Structure

### Base Model Pattern

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal

class DealBase(BaseModel):
    """Base schema with common fields."""
    name: str = Field(..., min_length=1, max_length=255)
    amount: Decimal = Field(..., gt=0, decimal_places=2)
    stage: str

class DealCreate(DealBase):
    """Schema for creating deals - only required fields."""
    pass

class DealUpdate(BaseModel):
    """Schema for updates - all fields optional."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    amount: Optional[Decimal] = Field(None, gt=0, decimal_places=2)
    stage: Optional[str] = None

class Deal(DealBase):
    """Complete model with DB fields."""
    id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM model to dict
        use_enum_values=True,  # Serialize enums as values
        populate_by_name=True  # Allow field_name or alias
    )
```

---

## Field Validation

### Field Constraints

```python
from pydantic import Field, EmailStr
from typing import Optional

class User(BaseModel):
    # String constraints
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr  # Built-in email validation

    # Numeric constraints
    age: int = Field(..., ge=0, le=150)  # 0 <= age <= 150
    salary: Decimal = Field(..., gt=0, decimal_places=2)

    # Pattern matching
    phone: str = Field(..., pattern=r"^\+?1?\d{9,15}$")

    # Optional with default
    role: str = Field(default="user")
    active: bool = Field(default=True)
```

**Common Constraints:**
- `min_length` / `max_length` - String length
- `ge` / `gt` - Greater than or equal / greater than
- `le` / `lt` - Less than or equal / less than
- `pattern` - Regex pattern
- `decimal_places` - Decimal precision

---

## Custom Validators

### Field Validator (V2)

```python
from pydantic import field_validator

class WebhookPayload(BaseModel):
    event_type: str
    deal_id: str

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        """Validate event_type is allowed."""
        allowed = ['deal.created', 'deal.updated', 'deal.deleted']
        if v not in allowed:
            raise ValueError(f"event_type must be one of: {allowed}")
        return v.lower()

    @field_validator('deal_id')
    @classmethod
    def validate_deal_id(cls, v: str) -> str:
        """Validate deal_id is numeric string."""
        if not v.isdigit():
            raise ValueError("deal_id must be numeric")
        return v
```

**Key Points:**
- Use `@field_validator('field_name')`
- Must add `@classmethod`
- Must have type hints
- Return the (possibly modified) value
- Raise `ValueError` for validation errors

---

### Model Validator (Cross-Field Validation)

```python
from pydantic import model_validator

class DateRange(BaseModel):
    start_date: datetime
    end_date: datetime

    @model_validator(mode='after')
    @classmethod
    def validate_date_range(cls, model):
        """Ensure end_date is after start_date."""
        if model.end_date <= model.start_date:
            raise ValueError("end_date must be after start_date")
        return model
```

**When to use:**
- Validating relationships between fields
- Computing derived fields
- Complex business logic validation

---

## Configuration Options

### ConfigDict Settings

```python
from pydantic import ConfigDict

class Deal(BaseModel):
    id: str
    name: str
    stage: DealStage  # Enum

    model_config = ConfigDict(
        # ORM/Database
        from_attributes=True,      # Allow ORM models (SQLAlchemy, etc.)

        # Enum handling
        use_enum_values=True,      # Serialize enums as values not names

        # Aliases
        populate_by_name=True,     # Accept both field_name and alias

        # Validation
        str_strip_whitespace=True, # Auto-strip strings
        validate_assignment=True,  # Validate on assignment after creation

        # JSON
        json_encoders={            # Custom JSON serialization
            datetime: lambda v: v.isoformat(),
            Decimal: str
        },

        # Other
        extra='forbid'             # Forbid extra fields (strict)
    )
```

**Common Settings:**
- `from_attributes=True` - Convert ORM models to Pydantic
- `use_enum_values=True` - Serialize enums properly
- `populate_by_name=True` - Flexible field naming
- `str_strip_whitespace=True` - Auto-trim strings
- `extra='forbid'` - Reject unexpected fields

---

## JSON Serialization

### Model Dump (V2)

```python
# ✅ V2 SYNTAX
user = User(name="John", email="john@example.com")

# To dict
user_dict = user.model_dump()

# To JSON string
user_json = user.model_dump_json()

# Exclude fields
user_dict = user.model_dump(exclude={'password'})

# Include only specific fields
user_dict = user.model_dump(include={'name', 'email'})
```

```python
# ❌ V1 SYNTAX (Don't use)
user.dict()  # Deprecated
user.json()  # Deprecated
```

---

## Nested Models

```python
class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str

class Contact(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class Deal(BaseModel):
    id: str
    name: str
    amount: Decimal
    contact: Contact          # Nested model
    billing_address: Address  # Nested model

# Usage
deal = Deal(
    id="123",
    name="Big Deal",
    amount=Decimal("50000"),
    contact={
        "name": "John Doe",
        "email": "john@example.com"
    },
    billing_address={
        "street": "123 Main St",
        "city": "Seattle",
        "state": "WA",
        "zip_code": "98101"
    }
)
```

---

## Settings Management

### BaseSettings Pattern

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings from environment variables."""

    # App config
    app_name: str = "UW Portal API"
    debug: bool = False

    # Database
    database_url: str

    # AWS
    aws_region: str = "us-east-1"
    aws_access_key_id: str
    aws_secret_access_key: str

    # External APIs
    hubspot_api_key: str
    heron_api_key: str

    # Optional with defaults
    log_level: str = "INFO"
    max_connections: int = 100

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # Allow HUBSPOT_API_KEY or hubspot_api_key
        extra="ignore"         # Ignore extra env vars
    )

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()

# Usage
settings = get_settings()
print(settings.hubspot_api_key)
```

---

## Union Types and Discriminators

```python
from typing import Literal, Union

class DealCreated(BaseModel):
    event_type: Literal["deal.created"]
    deal_id: str
    name: str

class DealUpdated(BaseModel):
    event_type: Literal["deal.updated"]
    deal_id: str
    changes: dict

class DealDeleted(BaseModel):
    event_type: Literal["deal.deleted"]
    deal_id: str

WebhookEvent = Union[DealCreated, DealUpdated, DealDeleted]

# Pydantic automatically discriminates based on event_type
```

---

## Validation Errors

### Handling Validation Errors

```python
from pydantic import ValidationError

try:
    user = User(name="", email="invalid")
except ValidationError as e:
    print(e.errors())
    # [
    #     {
    #         'type': 'string_too_short',
    #         'loc': ('name',),
    #         'msg': 'String should have at least 1 character',
    #         'input': ''
    #     },
    #     {
    #         'type': 'value_error',
    #         'loc': ('email',),
    #         'msg': 'value is not a valid email address',
    #         'input': 'invalid'
    #     }
    # ]
```

---

## Testing with Pydantic

```python
import pytest
from pydantic import ValidationError

def test_user_validation_success():
    """Test valid user creation."""
    user = User(name="John Doe", email="john@example.com")
    assert user.name == "John Doe"
    assert user.email == "john@example.com"

def test_user_validation_invalid_email():
    """Test invalid email raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        User(name="John", email="not-an-email")

    errors = exc_info.value.errors()
    assert len(errors) == 1
    assert errors[0]['loc'] == ('email',)
    assert 'email' in errors[0]['msg'].lower()

def test_user_validation_empty_name():
    """Test empty name raises ValidationError."""
    with pytest.raises(ValidationError) as exc_info:
        User(name="", email="john@example.com")

    errors = exc_info.value.errors()
    assert errors[0]['loc'] == ('name',)
```

---

## Common Patterns

### Optional Fields with None Default

```python
class User(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None  # Optional, defaults to None
    age: Optional[int] = None
```

### Required vs Optional

```python
# Required (no default)
name: str = Field(...)  # Ellipsis means required

# Optional with default
role: str = Field(default="user")

# Optional with None
phone: Optional[str] = Field(default=None)
```

---

## Anti-Patterns

### ❌ Don't Use V1 Syntax

```python
# ❌ BAD - V1 syntax
class User(BaseModel):
    @validator('name')
    def validate_name(cls, v):
        return v

    class Config:
        orm_mode = True

# ✅ GOOD - V2 syntax
class User(BaseModel):
    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v

    model_config = ConfigDict(from_attributes=True)
```

### ❌ Don't Forget Type Hints in Validators

```python
# ❌ BAD - Missing type hints
@field_validator('name')
@classmethod
def validate_name(cls, v):  # Missing type hints!
    return v.strip()

# ✅ GOOD - With type hints
@field_validator('name')
@classmethod
def validate_name(cls, v: str) -> str:
    return v.strip()
```

### ❌ Don't Use .dict() or .json()

```python
# ❌ BAD - Deprecated V1 methods
user.dict()
user.json()

# ✅ GOOD - V2 methods
user.model_dump()
user.model_dump_json()
```

---

## Migration Checklist

Migrating from Pydantic V1 to V2:

- [ ] Replace `@validator` with `@field_validator`
- [ ] Add `@classmethod` to all validators
- [ ] Add type hints to validator parameters and returns
- [ ] Replace `class Config:` with `model_config = ConfigDict(...)`
- [ ] Replace `orm_mode = True` with `from_attributes = True`
- [ ] Replace `.dict()` with `.model_dump()`
- [ ] Replace `.json()` with `.model_dump_json()`
- [ ] Test all validation logic
- [ ] Update tests for new error formats

---

## References

- [Pydantic V2 Documentation](https://docs.pydantic.dev/latest/)
- [Migration Guide](https://docs.pydantic.dev/latest/migration/)
- [Field Validators](https://docs.pydantic.dev/latest/concepts/validators/)
- [Settings Management](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
