# Error Handling Patterns

Best practices for exception handling, custom exceptions, logging, and error recovery in Python applications.

---

## Custom Exception Hierarchy

Create domain-specific exceptions for better error handling and debugging.

### Base Exception Pattern

```python
class PaymentError(Exception):
    """Base exception for payment-related errors."""
    pass

class InsufficientFundsError(PaymentError):
    """Raised when account has insufficient funds."""
    def __init__(self, required: Decimal, available: Decimal):
        self.required = required
        self.available = available
        super().__init__(
            f"Insufficient funds: required {required}, available {available}"
        )

class PaymentGatewayError(PaymentError):
    """Raised when payment gateway returns an error."""
    def __init__(self, gateway: str, error_code: str, message: str):
        self.gateway = gateway
        self.error_code = error_code
        super().__init__(f"{gateway} error {error_code}: {message}")
```

### Benefits of Custom Exceptions

- ✅ **Specific error handling**: Catch and handle different error types differently
- ✅ **Rich error context**: Include relevant data (amounts, IDs, etc.)
- ✅ **Better logging**: Log errors with full context
- ✅ **Clear error hierarchy**: Base exceptions for broad categories

---

## Exception Handling Best Practices

### Specific Exception Handling

```python
import logging

logger = logging.getLogger(__name__)

def process_payment(amount: Decimal, account_id: str) -> PaymentResult:
    """Process a payment with comprehensive error handling."""
    try:
        account = get_account(account_id)
        validate_amount(amount)

        if account.balance < amount:
            raise InsufficientFundsError(
                required=amount,
                available=account.balance
            )

        result = charge_account(account, amount)
        logger.info(
            "Payment processed",
            account_id=account_id,
            amount=amount,
            result_id=result.id
        )
        return PaymentResult(success=True, transaction_id=result.id)

    except InsufficientFundsError as e:
        # Expected error - log as warning
        logger.warning(
            "Payment failed: insufficient funds",
            account_id=account_id,
            required=e.required,
            available=e.available
        )
        return PaymentResult(
            success=False,
            reason="insufficient_funds",
            message=str(e)
        )

    except PaymentGatewayError as e:
        # Gateway error - log with gateway context
        logger.error(
            "Payment gateway error",
            gateway=e.gateway,
            error_code=e.error_code,
            account_id=account_id,
            amount=amount
        )
        return PaymentResult(
            success=False,
            reason="gateway_error",
            message=str(e)
        )

    except PaymentError as e:
        # Catch-all for payment errors
        logger.error(
            "Payment error",
            error_type=type(e).__name__,
            account_id=account_id,
            amount=amount,
            exc_info=True
        )
        return PaymentResult(
            success=False,
            reason="payment_error",
            message="An error occurred processing your payment"
        )

    except Exception as e:
        # Unexpected error - log full traceback
        logger.exception(
            "Unexpected error processing payment",
            account_id=account_id,
            amount=amount
        )
        # Don't expose internal errors to user
        return PaymentResult(
            success=False,
            reason="internal_error",
            message="An unexpected error occurred"
        )
```

### Exception Handling Guidelines

1. **Catch specific exceptions first**: Most specific → most general
2. **Log with context**: Include relevant IDs, amounts, etc.
3. **Don't expose internal details**: User-facing messages should be generic
4. **Use exc_info=True**: Log full traceback for unexpected errors
5. **Return structured errors**: Use result objects, not raw exceptions

---

## Context Managers for Resource Management

Use context managers to ensure resources are properly cleaned up.

### Database Transaction Pattern

```python
from contextlib import contextmanager
from typing import Generator
import logging

logger = logging.getLogger(__name__)

@contextmanager
def database_transaction(
    connection
) -> Generator[Connection, None, None]:
    """
    Provide a transactional scope for database operations.

    Automatically commits on success, rolls back on error.
    """
    trans = connection.begin_transaction()
    try:
        logger.debug("Starting database transaction")
        yield connection
        trans.commit()
        logger.debug("Transaction committed")
    except Exception as e:
        trans.rollback()
        logger.warning(
            "Transaction rolled back",
            error=str(e),
            exc_info=True
        )
        raise
    finally:
        connection.close()

# Usage
def transfer_funds(from_account: str, to_account: str, amount: Decimal):
    """Transfer funds between accounts with transactional safety."""
    conn = get_connection()

    with database_transaction(conn) as db:
        # All operations in this block are transactional
        debit_account(db, from_account, amount)
        credit_account(db, to_account, amount)
        log_transfer(db, from_account, to_account, amount)
    # Transaction automatically committed or rolled back
```

### File Handling Pattern

```python
from contextlib import contextmanager
import tempfile
import os

@contextmanager
def temp_file(suffix: str = ".tmp"):
    """Create a temporary file that's automatically cleaned up."""
    fd, path = tempfile.mkstemp(suffix=suffix)
    try:
        os.close(fd)  # Close file descriptor
        yield path
    finally:
        # Clean up even if exception occurred
        if os.path.exists(path):
            os.remove(path)

# Usage
with temp_file(suffix=".json") as temp_path:
    # Write to temp file
    with open(temp_path, "w") as f:
        json.dump(data, f)

    # Process the file
    process_file(temp_path)
# File automatically deleted
```

---

## Logging Strategy

### Structured Logging with Context

```python
import logging
from functools import wraps
from typing import Callable, Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

def log_execution(func: Callable) -> Callable:
    """
    Decorator to log function entry, exit, and errors.

    Use for debugging important functions.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        func_name = func.__name__
        logger.debug(f"Entering {func_name}", extra={"args": args, "kwargs": kwargs})

        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting {func_name} successfully")
            return result

        except Exception as e:
            logger.exception(
                f"Error in {func_name}",
                extra={"error_type": type(e).__name__}
            )
            raise

    return wrapper

# Usage
@log_execution
def calculate_risk_score(deal_id: str, factors: dict) -> float:
    """Calculate risk score for a deal."""
    # Complex calculation
    return score
```

### Logging Levels

```python
import logging

logger = logging.getLogger(__name__)

# DEBUG: Detailed diagnostic information
logger.debug("Processing deal", deal_id=deal_id, factors=factors)

# INFO: General informational messages
logger.info("Risk score calculated", deal_id=deal_id, score=score)

# WARNING: Something unexpected but recoverable
logger.warning("Deal missing optional field", deal_id=deal_id, field="tax_id")

# ERROR: Error occurred but application continues
logger.error("Failed to fetch external data", deal_id=deal_id, service="heron")

# CRITICAL: Serious error, application may not continue
logger.critical("Database connection lost", database_url=db_url)
```

### Logging Best Practices

1. **Use structured logging**: Include key-value pairs for context
2. **Log at appropriate levels**: Don't log everything as ERROR
3. **Include correlation IDs**: Track requests across services
4. **Don't log sensitive data**: PII, passwords, API keys
5. **Log exceptions with exc_info=True**: Includes full traceback

---

## FastAPI Exception Handling

### Custom Exception Handler

```python
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

class BusinessRuleViolation(Exception):
    """Raised when a business rule is violated."""
    def __init__(self, rule: str, details: str):
        self.rule = rule
        self.details = details
        super().__init__(f"Business rule violation: {rule}")

@app.exception_handler(BusinessRuleViolation)
async def business_rule_handler(
    request: Request,
    exc: BusinessRuleViolation
) -> JSONResponse:
    """Handle business rule violations with proper status code."""
    logger.warning(
        "Business rule violation",
        rule=exc.rule,
        details=exc.details,
        path=request.url.path
    )
    return JSONResponse(
        status_code=422,  # Unprocessable Entity
        content={
            "error": "business_rule_violation",
            "rule": exc.rule,
            "message": exc.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Catch-all handler for unexpected exceptions."""
    logger.exception(
        "Unhandled exception",
        path=request.url.path,
        method=request.method
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "An unexpected error occurred"
        }
    )
```

---

## Error Recovery Patterns

### Retry with Exponential Backoff

```python
import time
import logging
from typing import TypeVar, Callable
from functools import wraps

logger = logging.getLogger(__name__)

T = TypeVar('T')

def retry_with_backoff(
    max_retries: int = 3,
    base_delay: float = 1.0,
    max_delay: float = 60.0,
    exponential_base: float = 2.0
):
    """
    Retry a function with exponential backoff.

    Args:
        max_retries: Maximum number of retry attempts
        base_delay: Initial delay between retries (seconds)
        max_delay: Maximum delay between retries (seconds)
        exponential_base: Base for exponential backoff calculation
    """
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> T:
            delay = base_delay

            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)

                except Exception as e:
                    if attempt == max_retries:
                        logger.error(
                            f"Failed after {max_retries} retries",
                            function=func.__name__,
                            error=str(e)
                        )
                        raise

                    logger.warning(
                        f"Attempt {attempt + 1} failed, retrying",
                        function=func.__name__,
                        error=str(e),
                        retry_in=delay
                    )

                    time.sleep(delay)
                    delay = min(delay * exponential_base, max_delay)

        return wrapper
    return decorator

# Usage
@retry_with_backoff(max_retries=3, base_delay=1.0)
def fetch_external_data(api_url: str) -> dict:
    """Fetch data from external API with automatic retry."""
    response = requests.get(api_url, timeout=10)
    response.raise_for_status()
    return response.json()
```

### Circuit Breaker Pattern

```python
from enum import Enum
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered

class CircuitBreaker:
    """
    Circuit breaker to prevent cascading failures.

    Opens after threshold failures, closes after recovery.
    """
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        success_threshold: int = 2
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.success_threshold = success_threshold

        self.failure_count = 0
        self.success_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED

    def call(self, func: Callable, *args, **kwargs):
        """Execute function through circuit breaker."""
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
                logger.info("Circuit breaker entering half-open state")
            else:
                raise Exception("Circuit breaker is OPEN")

        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result

        except Exception as e:
            self._on_failure()
            raise

    def _on_success(self):
        """Handle successful call."""
        self.failure_count = 0

        if self.state == CircuitState.HALF_OPEN:
            self.success_count += 1
            if self.success_count >= self.success_threshold:
                self.state = CircuitState.CLOSED
                self.success_count = 0
                logger.info("Circuit breaker closed")

    def _on_failure(self):
        """Handle failed call."""
        self.failure_count += 1
        self.last_failure_time = datetime.now()
        self.success_count = 0

        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            logger.warning(
                "Circuit breaker opened",
                failure_count=self.failure_count
            )

    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt reset."""
        return (
            self.last_failure_time and
            datetime.now() - self.last_failure_time
            > timedelta(seconds=self.recovery_timeout)
        )

# Usage
breaker = CircuitBreaker(failure_threshold=5, recovery_timeout=60)

def call_external_service(data: dict) -> dict:
    """Call external service through circuit breaker."""
    return breaker.call(external_api.post, "/endpoint", json=data)
```

---

## Quick Reference

### Exception Handling Checklist

- [ ] Create custom exceptions for domain errors
- [ ] Catch specific exceptions before general ones
- [ ] Log errors with full context (IDs, values)
- [ ] Don't expose internal details to users
- [ ] Use `exc_info=True` for unexpected errors
- [ ] Return structured error responses
- [ ] Clean up resources with context managers
- [ ] Implement retry logic for transient failures
- [ ] Use circuit breakers for external services

### Logging Checklist

- [ ] Use appropriate log levels (DEBUG/INFO/WARNING/ERROR/CRITICAL)
- [ ] Include structured context (key-value pairs)
- [ ] Add correlation IDs for request tracking
- [ ] Don't log sensitive data (PII, secrets)
- [ ] Log exceptions with full tracebacks
- [ ] Use decorators for consistent logging

---

## See Also

- [fastapi-best-practices.md](./fastapi-best-practices.md) - API error handling
- [security-best-practices.md](./security-best-practices.md) - Secure error messages
