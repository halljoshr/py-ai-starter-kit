# Performance Optimization

Guidelines and patterns for optimizing Python application performance.

---

## Golden Rule: Profile First

**Never optimize without profiling.** Measure before and after changes to ensure you're actually improving performance.

---

## Profiling Tools

### cProfile (Built-in)

```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()

    # Code to profile
    result = expensive_function()

    profiler.disable()

    # Print stats
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')
    stats.print_stats(20)  # Top 20 functions

    return result
```

### py-spy (Sampling Profiler)

```bash
# Install
uv add --dev py-spy

# Profile running process
py-spy top --pid <pid>

# Generate flamegraph
py-spy record -o profile.svg -- python script.py
```

### line_profiler (Line-by-Line Profiling)

```bash
# Install
uv add --dev line-profiler

# Decorate function
@profile
def slow_function():
    # code here
    pass

# Run
kernprof -l -v script.py
```

---

## Caching Strategies

### Function Result Caching with lru_cache

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def expensive_calculation(n: int) -> int:
    """
    Cache results of expensive calculations.

    lru_cache stores the last 1000 unique (n) values.
    """
    # Expensive computation
    result = sum(i ** 2 for i in range(n))
    return result

# First call: slow
result1 = expensive_calculation(1000)

# Second call with same input: instant (cached)
result2 = expensive_calculation(1000)
```

**When to use:**
- Pure functions (same input → same output)
- Expensive computations called repeatedly
- Limited unique input combinations

**When NOT to use:**
- Functions with side effects
- Functions that return large objects
- Unbounded unique inputs (memory leak risk)

### Manual Caching with TTL

```python
from datetime import datetime, timedelta
from typing import Any, Optional
import asyncio

class TTLCache:
    """Simple cache with time-to-live expiration."""

    def __init__(self, ttl_seconds: int = 300):
        self.ttl_seconds = ttl_seconds
        self.cache: dict[str, tuple[Any, datetime]] = {}

    def get(self, key: str) -> Optional[Any]:
        """Get value if not expired."""
        if key not in self.cache:
            return None

        value, expiry = self.cache[key]
        if datetime.now() > expiry:
            del self.cache[key]
            return None

        return value

    def set(self, key: str, value: Any):
        """Set value with expiration."""
        expiry = datetime.now() + timedelta(seconds=self.ttl_seconds)
        self.cache[key] = (value, expiry)

# Usage
cache = TTLCache(ttl_seconds=300)  # 5 minute TTL

async def get_deal(deal_id: str) -> Deal:
    """Get deal with caching."""
    cached = cache.get(f"deal:{deal_id}")
    if cached:
        return cached

    deal = await fetch_deal_from_db(deal_id)
    cache.set(f"deal:{deal_id}", deal)
    return deal
```

---

## Memory-Efficient Patterns

### Generators for Large Datasets

```python
from typing import Iterator, AsyncIterator
import asyncio
import aiofiles

def read_large_file(filepath: str) -> Iterator[dict]:
    """
    Read large file line-by-line without loading into memory.

    Yields one record at a time instead of returning a list.
    """
    with open(filepath, 'r') as f:
        for line in f:
            data = json.loads(line)
            yield process_record(data)

# Usage: Process without loading entire file
for record in read_large_file('huge_file.jsonl'):
    save_to_database(record)


async def read_large_file_async(filepath: str) -> AsyncIterator[dict]:
    """Async version for I/O-bound operations."""
    async with aiofiles.open(filepath, mode='r') as f:
        async for line in f:
            data = json.loads(line)
            yield process_record(data)

# Usage with async
async for record in read_large_file_async('huge_file.jsonl'):
    await save_to_database_async(record)
```

### Generator Expressions vs List Comprehensions

```python
# ❌ BAD: Creates entire list in memory
numbers = [i ** 2 for i in range(1_000_000)]
total = sum(numbers)  # Holds 1M numbers in memory

# ✅ GOOD: Generator - processes one at a time
numbers = (i ** 2 for i in range(1_000_000))
total = sum(numbers)  # Memory-efficient

# ✅ EVEN BETTER: Don't materialize at all
total = sum(i ** 2 for i in range(1_000_000))
```

---

## Async I/O for Concurrent Operations

### When to Use asyncio

**Use asyncio for:**
- Multiple API calls
- Database queries in parallel
- File I/O operations
- Network requests

**Don't use asyncio for:**
- CPU-bound tasks (use multiprocessing instead)
- Single sequential operations
- Code that's already fast enough

### Async API Calls

```python
import asyncio
import aiohttp

async def fetch_deal(session: aiohttp.ClientSession, deal_id: str) -> dict:
    """Fetch a single deal."""
    async with session.get(f"/api/deals/{deal_id}") as response:
        return await response.json()

async def fetch_all_deals(deal_ids: list[str]) -> list[dict]:
    """
    Fetch multiple deals concurrently.

    Async allows all requests to run in parallel instead of sequentially.
    """
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_deal(session, deal_id) for deal_id in deal_ids]
        return await asyncio.gather(*tasks)

# Usage
deal_ids = ["123", "456", "789"]
deals = asyncio.run(fetch_all_deals(deal_ids))

# Sequential: 3 × 1s = 3 seconds
# Concurrent: max(1s, 1s, 1s) = ~1 second
```

### Async Database Queries

```python
import asyncpg

async def fetch_multiple_records(ids: list[str]) -> list[dict]:
    """Fetch records concurrently with connection pool."""
    conn = await asyncpg.connect(DATABASE_URL)

    try:
        # Execute queries concurrently
        tasks = [
            conn.fetchrow("SELECT * FROM deals WHERE id = $1", id)
            for id in ids
        ]
        results = await asyncio.gather(*tasks)
        return [dict(r) for r in results if r]

    finally:
        await conn.close()
```

---

## CPU-Bound Optimization

### Multiprocessing for Parallel Computation

```python
from multiprocessing import Pool
from typing import List

def expensive_computation(n: int) -> int:
    """CPU-intensive task."""
    return sum(i ** 2 for i in range(n))

def process_in_parallel(numbers: List[int]) -> List[int]:
    """
    Process numbers in parallel using multiple CPU cores.

    Useful for CPU-bound tasks like image processing,
    data transformation, or complex calculations.
    """
    with Pool() as pool:
        results = pool.map(expensive_computation, numbers)
    return results

# Usage
numbers = [1_000_000, 2_000_000, 3_000_000, 4_000_000]
results = process_in_parallel(numbers)

# Sequential: 4 × 5s = 20 seconds
# Parallel (4 cores): ~5 seconds
```

**When to use multiprocessing:**
- CPU-bound tasks (computation-heavy)
- Multiple independent operations
- Available CPU cores > 1

**When NOT to use:**
- I/O-bound tasks (use asyncio instead)
- Tasks with high inter-process communication overhead
- Small tasks (overhead > benefit)

---

## Database Query Optimization

### Index Your Queries

```sql
-- ❌ BAD: Full table scan
SELECT * FROM deals WHERE agency_id = '123';

-- ✅ GOOD: Create index
CREATE INDEX idx_deals_agency_id ON deals(agency_id);

-- ✅ Composite index for multi-column queries
CREATE INDEX idx_deals_agency_status
ON deals(agency_id, status);
```

### Batch Inserts

```python
# ❌ BAD: Individual inserts
for record in records:
    await conn.execute(
        "INSERT INTO deals (id, name) VALUES ($1, $2)",
        record['id'], record['name']
    )
# 100 records = 100 round-trips

# ✅ GOOD: Batch insert
await conn.executemany(
    "INSERT INTO deals (id, name) VALUES ($1, $2)",
    [(r['id'], r['name']) for r in records]
)
# 100 records = 1 round-trip
```

### Query Only What You Need

```python
# ❌ BAD: Fetch all columns
deals = await conn.fetch("SELECT * FROM deals WHERE status = 'active'")

# ✅ GOOD: Fetch only needed columns
deals = await conn.fetch(
    "SELECT id, name, agency_id FROM deals WHERE status = 'active'"
)

# ❌ BAD: Fetch all, filter in Python
all_deals = await conn.fetch("SELECT * FROM deals")
active_deals = [d for d in all_deals if d['status'] == 'active']

# ✅ GOOD: Filter in database
active_deals = await conn.fetch(
    "SELECT id, name FROM deals WHERE status = 'active'"
)
```

---

## API Response Optimization

### Pagination

```python
from fastapi import Query

@router.get("/deals")
async def list_deals(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000)
) -> list[DealResponse]:
    """
    List deals with pagination.

    Prevents loading thousands of records at once.
    """
    deals = await deal_repo.find_all(skip=skip, limit=limit)
    return [DealResponse.model_validate(d) for d in deals]
```

### Response Compression

```python
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware

app = FastAPI()

# Compress responses > 1KB
app.add_middleware(GZipMiddleware, minimum_size=1000)
```

### Field Selection

```python
@router.get("/deals/{deal_id}")
async def get_deal(
    deal_id: str,
    fields: list[str] = Query(None)
) -> dict:
    """
    Get deal with optional field selection.

    Example: GET /deals/123?fields=id,name,status
    Returns only requested fields instead of full object.
    """
    deal = await deal_repo.find_by_id(deal_id)

    if fields:
        return {k: v for k, v in deal.dict().items() if k in fields}

    return deal.dict()
```

---

## Quick Performance Checklist

### Before Optimizing
- [ ] Profile to identify bottlenecks
- [ ] Measure current performance
- [ ] Set performance targets

### Common Optimizations
- [ ] Add `@lru_cache` to pure functions
- [ ] Use generators for large datasets
- [ ] Use asyncio for I/O-bound operations
- [ ] Use multiprocessing for CPU-bound tasks
- [ ] Add database indexes for frequent queries
- [ ] Batch database operations
- [ ] Implement response pagination
- [ ] Cache frequently accessed data

### After Optimizing
- [ ] Profile again to verify improvement
- [ ] Compare before/after metrics
- [ ] Document optimization decisions

---

## Performance Anti-Patterns

### ❌ Premature Optimization

```python
# DON'T spend time optimizing before you know it's slow
def process_data(data: list[dict]) -> list[dict]:
    # This is fine for small datasets
    return [transform(item) for item in data]

# Only optimize when profiling shows it's a bottleneck
```

### ❌ Over-Caching

```python
# DON'T cache everything
@lru_cache(maxsize=None)  # Unlimited cache = memory leak
def get_user_data(user_id: str, timestamp: str):  # timestamp changes every call
    pass
```

### ❌ Inappropriate async

```python
# DON'T use async for CPU-bound tasks
async def calculate_fibonacci(n: int) -> int:  # Won't benefit from async
    if n <= 1:
        return n
    return await calculate_fibonacci(n-1) + await calculate_fibonacci(n-2)
```

---

## See Also

- [aws-lambda-best-practices.md](./aws-lambda-best-practices.md) - Lambda-specific optimizations
- [fastapi-best-practices.md](./fastapi-best-practices.md) - API performance
