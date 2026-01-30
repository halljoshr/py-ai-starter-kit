# Security Checklist for Code Review

OWASP-aligned security checks for Python code review.

## 1. Input Validation

### SQL Injection Prevention

**❌ Never:**
```python
# String concatenation
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**✅ Always:**
```python
# Parameterized queries
query = "SELECT * FROM users WHERE id = %s"
cursor.execute(query, (user_id,))

# Or with SQLAlchemy
user = session.query(User).filter(User.id == user_id).first()
```

### Command Injection Prevention

**❌ Never:**
```python
# Shell=True with user input
os.system(f"ls {user_directory}")
subprocess.run(f"cat {filename}", shell=True)
```

**✅ Always:**
```python
# Pass arguments as list, no shell
subprocess.run(["ls", user_directory])
subprocess.run(["cat", filename])
```

### Path Traversal Prevention

**❌ Never:**
```python
# Direct path concatenation
file_path = os.path.join(BASE_DIR, user_filename)
with open(file_path) as f:
    content = f.read()
```

**✅ Always:**
```python
# Validate path stays within allowed directory
file_path = (Path(BASE_DIR) / user_filename).resolve()
if not file_path.is_relative_to(BASE_DIR):
    raise ValueError("Path traversal attempt detected")

with open(file_path) as f:
    content = f.read()
```

---

## 2. Authentication & Authorization

### Password Storage

**❌ Never:**
```python
# Plain text
user.password = password

# Simple hash (MD5, SHA1)
user.password = hashlib.md5(password.encode()).hexdigest()
```

**✅ Always:**
```python
# Use bcrypt or argon2
from passlib.hash import bcrypt

user.password_hash = bcrypt.hash(password)

# Verify
if bcrypt.verify(password, user.password_hash):
    # Success
```

### JWT Token Security

**❌ Never:**
```python
# Weak secret
SECRET_KEY = "secret123"

# No expiration
token = jwt.encode(payload, SECRET_KEY)

# Algorithm manipulation vulnerability
jwt.decode(token, SECRET_KEY)  # Allows "none" algorithm
```

**✅ Always:**
```python
# Strong secret (use secrets module)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")  # From environment

# Set expiration
payload = {
    "user_id": user.id,
    "exp": datetime.utcnow() + timedelta(minutes=30)
}
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Verify with algorithm restriction
jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
```

### API Key Storage

**❌ Never:**
```python
# Hardcoded
API_KEY = "sk_live_abc123"

# In code comments
# API_KEY = "sk_live_abc123"  # Don't forget to rotate!
```

**✅ Always:**
```python
# Environment variables
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY environment variable required")

# Use secrets management (AWS Secrets Manager, etc.)
```

---

## 3. Data Exposure

### Sensitive Data in Logs

**❌ Never:**
```python
logger.info(f"User login: {username}, password: {password}")
logger.debug(f"Credit card: {credit_card_number}")
logger.info(f"API key: {api_key}")
```

**✅ Always:**
```python
# Mask sensitive data
logger.info(f"User login: {username}")  # No password
logger.debug(f"Credit card: ****{credit_card_number[-4:]}")
logger.info(f"API key: {api_key[:8]}***")
```

### Error Messages

**❌ Never:**
```python
# Expose internal details
except Exception as e:
    return {"error": str(e)}  # May expose SQL, file paths, etc.
```

**✅ Always:**
```python
# Generic error messages in production
except ValueError as e:
    logger.error(f"Validation error: {e}", exc_info=True)
    return {"error": "Invalid input provided"}

except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    return {"error": "Internal server error"}
```

---

## 4. API Security

### Rate Limiting

**Check for:**
- Rate limiting on authentication endpoints
- Rate limiting on public APIs
- Proper 429 status codes with Retry-After header

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/login")
@limiter.limit("5/minute")  # 5 attempts per minute
async def login(credentials: Credentials):
    ...
```

### CORS Configuration

**❌ Never:**
```python
# Allow all origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Dangerous!
    allow_credentials=True,
)
```

**✅ Always:**
```python
# Specific origins
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # ["https://example.com"]
    allow_credentials=True,
)
```

### Request Size Limits

**Check for:**
```python
# Limit request body size to prevent DoS
app.add_middleware(
    RequestSizeLimitMiddleware,
    max_size=1_000_000  # 1MB
)
```

---

## 5. Dependency Security

### Known Vulnerabilities

**Check:**
```bash
# Scan dependencies for known vulnerabilities
uv run pip-audit

# Or use safety
uv run safety check
```

### Outdated Dependencies

**❌ Never:**
```toml
# Unpinned versions
dependencies = [
    "fastapi",  # Could pull vulnerable version
    "pydantic",
]
```

**✅ Always:**
```toml
# Pinned versions with minimum
dependencies = [
    "fastapi>=0.109.0",  # Known secure version
    "pydantic>=2.5.0",
]

# Use lock file
uv lock  # Creates uv.lock with exact versions
```

---

## 6. Cryptography

### Random Number Generation

**❌ Never:**
```python
# Predictable random
import random
token = random.randint(1000, 9999)  # Not cryptographically secure
```

**✅ Always:**
```python
# Cryptographically secure random
import secrets
token = secrets.token_urlsafe(32)
verification_code = secrets.randbelow(1000000)  # 0-999999
```

### Encryption

**❌ Never:**
```python
# Weak or custom encryption
encrypted = base64.b64encode(data.encode())  # Not encryption!

# Or rolling your own crypto
```

**✅ Always:**
```python
# Use established libraries
from cryptography.fernet import Fernet

# Generate key (do once, store securely)
key = Fernet.generate_key()
cipher = Fernet(key)

# Encrypt
encrypted = cipher.encrypt(data.encode())

# Decrypt
decrypted = cipher.decrypt(encrypted).decode()
```

---

## 7. File Upload Security

### Validation

**❌ Never:**
```python
# Trust user-provided filename
file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)
with open(file_path, "wb") as f:
    f.write(uploaded_file.file.read())
```

**✅ Always:**
```python
# Validate filename, extension, size, content type
import uuid
from pathlib import Path

ALLOWED_EXTENSIONS = {".jpg", ".png", ".pdf"}
MAX_SIZE = 10 * 1024 * 1024  # 10MB

# Check size
if uploaded_file.size > MAX_SIZE:
    raise ValueError("File too large")

# Check extension
file_ext = Path(uploaded_file.filename).suffix.lower()
if file_ext not in ALLOWED_EXTENSIONS:
    raise ValueError("File type not allowed")

# Generate safe filename
safe_filename = f"{uuid.uuid4()}{file_ext}"
file_path = Path(UPLOAD_DIR) / safe_filename

# Verify it's actually an image (if expecting image)
from PIL import Image
try:
    Image.open(uploaded_file.file).verify()
except:
    raise ValueError("Invalid image file")
```

---

## 8. Session Management

### Session Security

**Check for:**
- Secure cookie flags (HttpOnly, Secure, SameSite)
- Session expiration
- Session regeneration after login
- Logout functionality

```python
from fastapi import Response

# Set secure cookies
response.set_cookie(
    key="session",
    value=session_token,
    httponly=True,  # Prevent JavaScript access
    secure=True,    # HTTPS only
    samesite="lax", # CSRF protection
    max_age=3600    # 1 hour expiration
)
```

---

## 9. Common Vulnerabilities

### XML External Entity (XXE)

**If parsing XML:**
```python
import defusedxml.ElementTree as ET  # Use defusedxml, not xml

tree = ET.parse(xml_file)  # Safe from XXE
```

### Server-Side Request Forgery (SSRF)

**❌ Never:**
```python
# Allow arbitrary URLs
url = request.json["url"]
response = httpx.get(url)  # Can access internal services!
```

**✅ Always:**
```python
# Validate URL against allowlist
ALLOWED_DOMAINS = ["api.example.com", "cdn.example.com"]

parsed = urlparse(url)
if parsed.hostname not in ALLOWED_DOMAINS:
    raise ValueError("URL not allowed")

response = httpx.get(url)
```

---

## Review Checklist

For each code review, verify:

- [ ] No hardcoded secrets or credentials
- [ ] SQL queries use parameterization
- [ ] User input is validated
- [ ] Sensitive data is not logged
- [ ] Passwords are hashed (bcrypt/argon2)
- [ ] File paths prevent traversal
- [ ] API has rate limiting
- [ ] CORS configured properly
- [ ] Dependencies are pinned and audited
- [ ] Error messages don't expose internals
- [ ] Cryptographic operations use `secrets` module
- [ ] File uploads are validated
- [ ] Sessions use secure cookies
- [ ] No shell injection vulnerabilities
