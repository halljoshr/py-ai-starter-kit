# Style & Conventions

Python coding standards, naming conventions, and documentation patterns for consistent, maintainable code.

---

## Python Style Guide

### PEP 8 Compliance

Follow [PEP 8](https://pep8.org/) with these project-specific choices:

- **Line length:** 100 characters (enforced by ruff in pyproject.toml)
- **String quotes:** Double quotes `"` (not single quotes)
- **Trailing commas:** Use in multi-line structures
- **Imports:** Absolute imports preferred, grouped by stdlib/third-party/local
- **Blank lines:** 2 between top-level definitions, 1 between methods

### Code Formatting

```python
# ✅ GOOD: Follows style guide
from typing import List, Optional
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models import User
from app.services import PaymentService


class Payment(BaseModel):
    """Payment transaction model."""

    amount: Decimal = Field(..., gt=0, decimal_places=2)
    currency: str = Field(default="USD", max_length=3)
    user_id: int
    description: Optional[str] = None
    tags: List[str] = []


def process_payment(
    amount: Decimal,
    user_id: int,
    description: Optional[str] = None,
) -> Payment:
    """
    Process a payment transaction.

    Args:
        amount: Payment amount in specified currency
        user_id: ID of user making payment
        description: Optional payment description

    Returns:
        Created payment record

    Raises:
        ValueError: If amount is invalid
        PaymentError: If processing fails
    """
    if amount <= 0:
        raise ValueError("Amount must be positive")

    payment = Payment(
        amount=amount,
        user_id=user_id,
        description=description,
        tags=["processed", "validated"],
    )

    return payment
```

### Automatic Formatting

Use `ruff format` (faster alternative to Black):

```bash
# Format all files
uv run ruff format .

# Check formatting without changes
uv run ruff format --check .

# Format specific file
uv run ruff format app/services/payment.py
```

---

## Type Hints

### Always Use Type Hints

Type hints are **mandatory** for:
- Function signatures (parameters and return values)
- Class attributes
- Module-level variables

```python
from typing import List, Dict, Optional, Union
from decimal import Decimal
from datetime import datetime

# ✅ GOOD: Full type hints
def calculate_total(
    items: List[Dict[str, Union[str, Decimal]]],
    tax_rate: Decimal,
    discount: Optional[Decimal] = None,
) -> Decimal:
    """Calculate total with tax and optional discount."""
    subtotal = sum(item["price"] for item in items)
    tax = subtotal * tax_rate

    if discount:
        subtotal -= discount

    return subtotal + tax


# ✅ GOOD: Class with typed attributes
class Order:
    """Order with line items."""

    order_id: int
    created_at: datetime
    items: List[Dict[str, Union[str, Decimal]]]
    total: Decimal

    def __init__(
        self,
        order_id: int,
        items: List[Dict[str, Union[str, Decimal]]],
    ) -> None:
        self.order_id = order_id
        self.items = items
        self.created_at = datetime.now()
        self.total = self._calculate_total()

    def _calculate_total(self) -> Decimal:
        """Calculate order total."""
        return sum(item["price"] for item in self.items)


# ❌ BAD: No type hints
def process(data, config):
    result = transform(data)
    return result
```

### Type Checking

Use `mypy` for static type checking:

```bash
# Check all files
uv run mypy app/

# Check specific file
uv run mypy app/services/payment.py

# Strict mode
uv run mypy --strict app/
```

---

## Naming Conventions

### General Rules

| Type | Convention | Example |
|------|-----------|---------|
| Variables and functions | `snake_case` | `user_count`, `calculate_total()` |
| Classes | `PascalCase` | `PaymentService`, `UserModel` |
| Constants | `UPPER_SNAKE_CASE` | `MAX_RETRIES`, `API_TIMEOUT` |
| Private attributes/methods | `_leading_underscore` | `_internal_state`, `_validate()` |
| Type aliases | `PascalCase` | `UserId`, `PaymentResult` |
| Enum values | `UPPER_SNAKE_CASE` | `Status.PENDING`, `Role.ADMIN` |

### Examples

```python
from enum import Enum
from typing import TypeAlias

# Constants
MAX_RETRIES: int = 3
API_TIMEOUT: int = 30
DEFAULT_CURRENCY: str = "USD"

# Type aliases
UserId: TypeAlias = int
PaymentAmount: TypeAlias = Decimal

# Enums
class PaymentStatus(str, Enum):
    """Payment status values."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

# Classes
class PaymentProcessor:
    """Process payment transactions."""

    # Public attributes
    max_retries: int
    timeout: int

    # Private attributes
    _api_key: str
    _session: Optional[Session] = None

    def __init__(self, api_key: str) -> None:
        self.max_retries = MAX_RETRIES
        self.timeout = API_TIMEOUT
        self._api_key = api_key

    # Public methods
    def process_payment(self, amount: PaymentAmount) -> PaymentResult:
        """Process a payment transaction."""
        return self._execute_payment(amount)

    # Private methods
    def _execute_payment(self, amount: PaymentAmount) -> PaymentResult:
        """Internal payment execution logic."""
        pass
```

### Database Naming

See [database-standards.md](./database-standards.md) for database-specific naming conventions:
- Primary keys: `{entity}_id`
- Foreign keys: `{referenced_entity}_id`
- Timestamps: `{action}_at`
- Booleans: `is_{state}`

---

## Docstring Standards

### Google-Style Docstrings

Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings) for all public functions, classes, and modules.

#### Function Docstrings

```python
def calculate_discount(
    price: Decimal,
    discount_percent: float,
    min_amount: Decimal = Decimal("0.01"),
) -> Decimal:
    """
    Calculate the discounted price for a product.

    Applies percentage discount to the original price and ensures
    the final price doesn't go below the minimum allowed amount.

    Args:
        price: Original price of the product
        discount_percent: Discount percentage (0-100)
        min_amount: Minimum allowed final price

    Returns:
        Final price after applying discount

    Raises:
        ValueError: If discount_percent is not between 0 and 100
        ValueError: If final price would be below min_amount

    Example:
        >>> calculate_discount(Decimal("100"), 20)
        Decimal('80.00')
        >>> calculate_discount(Decimal("100"), 95, Decimal("10"))
        Decimal('10.00')
    """
    if not 0 <= discount_percent <= 100:
        raise ValueError("Discount percent must be between 0 and 100")

    discount_amount = price * (discount_percent / 100)
    final_price = price - discount_amount

    if final_price < min_amount:
        raise ValueError(f"Final price {final_price} below minimum {min_amount}")

    return final_price
```

#### Class Docstrings

```python
class PaymentProcessor:
    """
    Process payment transactions through external gateway.

    Handles payment processing, retry logic, and error handling for
    transactions through the payment gateway API. Supports multiple
    payment methods and currencies.

    Attributes:
        gateway_url: Base URL for payment gateway API
        max_retries: Maximum number of retry attempts
        timeout: Request timeout in seconds

    Example:
        >>> processor = PaymentProcessor(api_key="secret")
        >>> result = processor.process_payment(
        ...     amount=Decimal("100.00"),
        ...     currency="USD"
        ... )
        >>> print(result.status)
        'completed'
    """

    def __init__(self, api_key: str, timeout: int = 30) -> None:
        """
        Initialize payment processor.

        Args:
            api_key: Authentication key for payment gateway
            timeout: Request timeout in seconds (default: 30)
        """
        self.gateway_url = "https://api.payment-gateway.com"
        self.max_retries = 3
        self.timeout = timeout
        self._api_key = api_key
```

#### Module Docstrings

```python
"""
Payment processing services.

This module provides services for processing payment transactions
through external payment gateways. It includes retry logic, error
handling, and support for multiple payment methods.

Typical usage example:

    processor = PaymentProcessor(api_key=settings.PAYMENT_API_KEY)
    result = processor.process_payment(
        amount=Decimal("100.00"),
        currency="USD",
        payment_method="card"
    )
"""

from decimal import Decimal
from typing import Optional

# ... rest of module
```

### Docstring Sections

Use these sections in order (skip sections that don't apply):

1. **Summary** - One-line description (required)
2. **Extended Description** - Multi-line explanation (optional)
3. **Args** - Parameter descriptions (required for functions with params)
4. **Returns** - Return value description (required if returns something)
5. **Raises** - Exception descriptions (required if raises exceptions)
6. **Yields** - For generators (required for generators)
7. **Example** - Usage examples (recommended)
8. **Note** - Additional notes (optional)
9. **Warning** - Important warnings (optional)

---

## Code Comments

### When to Comment

```python
# ✅ GOOD: Complex logic explained
def calculate_risk_score(factors: Dict[str, float]) -> float:
    """Calculate risk score from multiple factors."""
    # Weight factors by importance (business requirement from PRO-123)
    weights = {
        "credit_score": 0.4,
        "debt_ratio": 0.3,
        "payment_history": 0.3,
    }

    # Normalize scores to 0-100 scale
    normalized = {
        key: value * 100 for key, value in factors.items()
    }

    # Calculate weighted average
    score = sum(
        normalized[key] * weights[key]
        for key in weights
    )

    return score


# ✅ GOOD: Non-obvious workaround explained
def fetch_user_data(user_id: int) -> dict:
    """Fetch user data from API."""
    # API returns 404 for deleted users, but we need 200 with deleted flag
    # See: https://github.com/vendor/api/issues/123
    try:
        return api.get(f"/users/{user_id}")
    except NotFoundError:
        return {"id": user_id, "deleted": True}


# ❌ BAD: Obvious comment
def get_user_count() -> int:
    """Get the number of users."""
    # Return the count of users
    return User.objects.count()


# ❌ BAD: Commented-out code (delete instead)
def process_payment(amount: Decimal) -> Payment:
    """Process payment."""
    # old_method(amount)
    # legacy_validation(amount)
    return new_method(amount)
```

### Inline Comments

```python
# ✅ GOOD: Explains "why", not "what"
timeout = 60  # Increased from 30s due to slow API response times

# ❌ BAD: States the obvious
timeout = 60  # Set timeout to 60
```

### TODO Comments

```python
# ✅ GOOD: Actionable TODO with ticket reference
def calculate_score(data: dict) -> float:
    """Calculate risk score."""
    # TODO(PRO-456): Add support for international credit scores
    score = data.get("credit_score", 0)
    return score


# ❌ BAD: Vague TODO without context
def calculate_score(data: dict) -> float:
    """Calculate risk score."""
    # TODO: improve this
    score = data.get("credit_score", 0)
    return score
```

---

## Import Organization

### Import Order

1. Standard library imports
2. Third-party imports
3. Local application imports

Separate each group with a blank line.

```python
# ✅ GOOD: Organized imports
# Standard library
import json
import logging
from datetime import datetime
from typing import Optional, List

# Third-party
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select

# Local
from app.config import settings
from app.models import User, Payment
from app.services.payment import PaymentService
from app.utils.validators import validate_email


# ❌ BAD: Mixed import groups
from app.models import User
import json
from fastapi import APIRouter
from datetime import datetime
from app.config import settings
```

### Import Formatting

```python
# ✅ GOOD: Explicit imports
from app.models import User, Payment, Order

# ✅ GOOD: Multi-line for readability (when > 3 imports)
from app.services import (
    PaymentService,
    UserService,
    NotificationService,
    EmailService,
)

# ❌ BAD: Star imports (exception: __init__.py)
from app.models import *
```

---

## Code Organization

### File Structure

```python
"""Module docstring here."""

# Imports
import standard_library
from third_party import something
from app.local import module

# Constants
MAX_RETRIES = 3
API_TIMEOUT = 30

# Type aliases
UserId = int

# Exceptions
class CustomError(Exception):
    """Custom exception."""
    pass

# Classes
class MyClass:
    """Class docstring."""
    pass

# Functions
def my_function() -> None:
    """Function docstring."""
    pass

# Main execution (if script)
if __name__ == "__main__":
    main()
```

### Function Length

- **Target:** < 50 lines
- **Maximum:** 100 lines
- **If longer:** Extract helper functions

```python
# ✅ GOOD: Broken into smaller functions
def process_order(order: Order) -> OrderResult:
    """Process an order through all stages."""
    validated_order = _validate_order(order)
    payment_result = _process_payment(validated_order)
    inventory_result = _update_inventory(validated_order)
    notification = _send_confirmation(validated_order)

    return OrderResult(
        order=validated_order,
        payment=payment_result,
        inventory=inventory_result,
        notification=notification,
    )

def _validate_order(order: Order) -> Order:
    """Validate order details."""
    # Validation logic
    return order

def _process_payment(order: Order) -> PaymentResult:
    """Process payment for order."""
    # Payment logic
    return result


# ❌ BAD: 200+ line monolithic function
def process_order(order: Order) -> OrderResult:
    """Process order."""
    # 200 lines of validation, payment, inventory, notifications...
    pass
```

### File Length

- **Target:** < 300 lines
- **Maximum:** 500 lines
- **If longer:** Split into multiple modules

---

## Pydantic Models

### Use Pydantic V2

This project uses **Pydantic V2**. See [pydantic-best-practices.md](./pydantic-best-practices.md) for comprehensive patterns.

```python
from pydantic import BaseModel, Field, ConfigDict
from decimal import Decimal
from datetime import datetime

class Product(BaseModel):
    """Product model with validation."""

    name: str = Field(..., min_length=1, max_length=255)
    price: Decimal = Field(..., gt=0, decimal_places=2)
    description: str | None = None
    tags: list[str] = []

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        use_enum_values=True,
    )
```

---

## Error Messages

### User-Facing Messages

```python
# ✅ GOOD: Clear, actionable error message
raise ValueError(
    "Price must be positive. Received: -10.00"
)

# ✅ GOOD: Helpful context
raise ValidationError(
    f"Invalid email format: '{email}'. "
    f"Expected format: user@domain.com"
)

# ❌ BAD: Vague error
raise ValueError("Invalid input")

# ❌ BAD: Technical jargon for users
raise ValueError("NoneType object has no attribute 'price'")
```

### Internal Error Messages

```python
# ✅ GOOD: Detailed context for debugging
raise PaymentError(
    f"Payment gateway timeout after {retry_count} retries. "
    f"Transaction ID: {transaction_id}, "
    f"Amount: {amount}, "
    f"Gateway: {gateway_name}"
)

# ❌ BAD: No context
raise PaymentError("Payment failed")
```

---

## String Formatting

### Use f-strings

```python
# ✅ GOOD: f-string (Python 3.6+)
message = f"User {user_id} paid {amount}"

# ✅ GOOD: Multi-line f-string
message = (
    f"Order {order_id} processed:\n"
    f"  Amount: {amount}\n"
    f"  Tax: {tax}\n"
    f"  Total: {total}"
)

# ❌ BAD: .format()
message = "User {} paid {}".format(user_id, amount)

# ❌ BAD: % formatting
message = "User %s paid %s" % (user_id, amount)
```

---

## Boolean Expressions

### Explicit Comparisons

```python
# ✅ GOOD: Explicit None check
if value is not None:
    process(value)

# ✅ GOOD: Explicit empty check
if len(items) > 0:
    process_items(items)

# ✅ GOOD: Boolean attribute
if user.is_active:
    send_notification(user)

# ❌ BAD: Implicit truthiness (when None is valid)
if value:  # Could be 0, "", [], etc.
    process(value)
```

---

## Quick Reference Checklist

### Before Committing

- [ ] Code formatted with `ruff format`
- [ ] No linting errors (`ruff check`)
- [ ] Type hints on all functions
- [ ] Type checking passes (`mypy`)
- [ ] Docstrings on public functions/classes
- [ ] Imports organized (stdlib, third-party, local)
- [ ] No commented-out code
- [ ] No hardcoded secrets
- [ ] Functions < 100 lines
- [ ] Files < 500 lines

---

## See Also

- [pydantic-best-practices.md](./pydantic-best-practices.md) - Pydantic V2 patterns
- [database-standards.md](./database-standards.md) - Database naming conventions
- [fastapi-best-practices.md](./fastapi-best-practices.md) - API endpoint patterns
- [pytest-best-practices.md](./pytest-best-practices.md) - Testing conventions
