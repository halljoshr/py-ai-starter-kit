# Security Best Practices

Security patterns for this project.

---

## Input Validation

**Always use Pydantic for input validation:**

```python
from pydantic import BaseModel, Field, field_validator

class WebhookPayload(BaseModel):
    event_type: str = Field(..., min_length=1, max_length=100)
    deal_id: str = Field(..., regex=r"^\d+$")

    @field_validator('event_type')
    @classmethod
    def validate_event_type(cls, v: str) -> str:
        allowed = ['deal.created', 'deal.updated', 'deal.deleted']
        if v not in allowed:
            raise ValueError(f"Invalid event_type: {v}")
        return v
```

---

## Secrets Management

### AWS Secrets Manager

```python
import boto3
import json
from functools import lru_cache

@lru_cache()
def get_secret(secret_name: str) -> dict:
    """Get secret from AWS Secrets Manager (cached)."""
    client = boto3.client('secretsmanager')
    response = client.get_secret_value(SecretId=secret_name)
    return json.loads(response['SecretString'])
```

### Environment Variables

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    api_key: str  # Load from environment
    database_url: str

    model_config = SettingsConfigDict(env_file=".env")
```

**NEVER:**
- ❌ Hardcode secrets in code
- ❌ Commit .env files
- ❌ Log secrets
- ❌ Expose secrets in error messages

---

## Signature Validation

### Webhook Signatures (Timing-Safe Comparison)

```python
import hmac
import hashlib
import secrets

def validate_signature(payload: str, signature: str, secret: str) -> bool:
    """Validate webhook signature (timing-attack safe)."""
    expected = hmac.new(
        secret.encode(),
        payload.encode(),
        hashlib.sha256
    ).hexdigest()

    # ✅ GOOD: Constant-time comparison
    return secrets.compare_digest(expected, signature)

    # ❌ BAD: Timing attack vulnerable
    # return expected == signature
```

**Why:** `==` comparison leaks timing information that can be used to brute-force signatures.

---

## SQL Injection Prevention

**Use parameterized queries (never string concatenation):**

```python
# ✅ GOOD: Parameterized query
cursor.execute("SELECT * FROM deals WHERE id = ?", (deal_id,))

# ❌ BAD: String concatenation (SQL injection!)
cursor.execute(f"SELECT * FROM deals WHERE id = '{deal_id}'")
```

**Even better: Use ORMs that handle this automatically.**

---

## XSS Prevention

FastAPI automatically escapes JSON responses, but be careful with:

```python
from fastapi.responses import HTMLResponse

# ❌ BAD: Raw HTML without escaping
@router.get("/profile")
def get_profile(name: str):
    return HTMLResponse(f"<h1>Welcome {name}</h1>")  # XSS!

# ✅ GOOD: Use templates with auto-escaping or return JSON
@router.get("/profile", response_model=ProfileResponse)
def get_profile(name: str):
    return ProfileResponse(name=name)
```

---

## Authentication Patterns

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Verify JWT token."""
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

@router.get("/protected")
async def protected_route(user: dict = Depends(verify_token)):
    return {"user": user}
```

---

## CORS Configuration

```python
from fastapi.middleware.cors import CORSMiddleware

# ✅ GOOD: Specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://app.example.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# ❌ BAD: Allow all origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Security risk!
)
```

---

## Rate Limiting

```python
from fastapi import Request, HTTPException
from collections import defaultdict
import time

# Simple in-memory rate limiter (use Redis for production)
request_counts = defaultdict(list)

def rate_limit(max_requests: int = 100, window: int = 60):
    """Rate limit decorator."""
    def decorator(func):
        async def wrapper(request: Request, *args, **kwargs):
            ip = request.client.host
            now = time.time()

            # Clean old requests
            request_counts[ip] = [
                req_time for req_time in request_counts[ip]
                if now - req_time < window
            ]

            if len(request_counts[ip]) >= max_requests:
                raise HTTPException(status_code=429, detail="Too many requests")

            request_counts[ip].append(now)
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
```

---

## Password Hashing

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain, hashed)
```

---

## Security Checklist

- [ ] All input validated with Pydantic
- [ ] No secrets in code
- [ ] Use AWS Secrets Manager for production secrets
- [ ] Webhook signatures use `secrets.compare_digest()`
- [ ] Parameterized queries (no SQL injection)
- [ ] CORS configured (no allow_origins=["*"])
- [ ] HTTPS only in production
- [ ] Rate limiting on public endpoints
- [ ] Passwords hashed with bcrypt
- [ ] Error messages don't leak sensitive data

---

## References

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Secrets Management](https://docs.aws.amazon.com/secretsmanager/)
