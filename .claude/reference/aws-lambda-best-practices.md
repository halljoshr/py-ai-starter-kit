# AWS Lambda Best Practices

Reference guide for AWS Lambda patterns in this project.

---

## Lambda Handler with Mangum

```python
from mangum import Mangum
from fastapi import FastAPI

app = FastAPI()

# Add routes...

# Lambda handler
lambda_handler = Mangum(app, lifespan="off")
```

**Key Setting:** `lifespan="off"` - Lambda has no persistent state between invocations.

---

## Environment Variables

```python
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    hubspot_api_key: str = os.getenv("HUBSPOT_API_KEY")
    aws_region: str = os.getenv("AWS_REGION", "us-east-1")
```

Configure in Lambda Console or template.

---

## AWS Secrets Manager Integration

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

# Usage
secrets = get_secret("prod/api-keys")
api_key = secrets["hubspot_api_key"]
```

---

## Cold Start Optimization

### Minimize Imports

```python
# ✅ GOOD: Import at top (loaded once)
import boto3
from app.services import DealService

def lambda_handler(event, context):
    service = DealService()
    return service.process(event)
```

### Connection Reuse

```python
# Initialize outside handler (reused across invocations)
import httpx

client = httpx.AsyncClient()

async def lambda_handler(event, context):
    # Reuse client
    response = await client.get(url)
    return response.json()
```

---

## Logging

```python
import logging
import json

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info(json.dumps({
        "event": "request_received",
        "request_id": context.request_id
    }))
```

**Use structured logging** for CloudWatch Logs Insights.

---

## Best Practices

✅ **DO:**
- Set `lifespan="off"` for Mangum
- Cache secrets (lru_cache)
- Reuse connections
- Use structured logging
- Handle errors gracefully

❌ **DON'T:**
- Import inside handler
- Create new clients per invocation
- Log sensitive data
- Use global state expecting persistence
