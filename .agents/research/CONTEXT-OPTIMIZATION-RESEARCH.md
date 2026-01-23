# Context Management, Caching & Compaction Strategies

## Overview

This document covers critical patterns for optimizing token usage, reducing costs, and managing long-running conversations through three key mechanisms:

1. **Prompt Caching** - Cache stable content (system prompts, documents) to reduce processing time and costs
2. **Conversation Compaction** - Automatically summarize conversation history when it grows too large
3. **PreCompact Hook** - Intercept compaction to preserve critical context before summarization

---

## 1. Prompt Caching (60-90% Cost Reduction)

### How It Works

Prompt caching allows you to cache frequently used context between API calls, dramatically reducing both costs and latency:

1. System checks if prompt prefix (up to cache breakpoint) is already cached
2. If found, uses cached version (90% cost reduction)
3. Otherwise, processes full prompt and caches the prefix for future use

### Cache Durations (TTL)

**Two options:**

| Duration | Syntax | Cache Write Cost | Best For |
|----------|--------|------------------|----------|
| **5 minutes** (default) | `{"type": "ephemeral"}` or `{"type": "ephemeral", "ttl": "5m"}` | 1.25x base input | Rapid iterations, same session |
| **1 hour** | `{"type": "ephemeral", "ttl": "1h"}` | 2x base input | Longer sessions, recurring queries |

**Important**: TTL resets each time cached content is reused (at no additional cost for 5-minute cache)

### Pricing Impact

| Model | Base Input | 5m Cache Write | 1h Cache Write | Cache Hit | Output |
|-------|-----------|----------------|----------------|-----------|--------|
| **Sonnet 4.5** | $3/MTok | $3.75/MTok (1.25x) | $6/MTok (2x) | **$0.30/MTok (0.1x)** | $15/MTok |
| **Opus 4.5** | $5/MTok | $6.25/MTok (1.25x) | $10/MTok (2x) | **$0.50/MTok (0.1x)** | $25/MTok |
| **Haiku 4.5** | $1/MTok | $1.25/MTok (1.25x) | $2/MTok (2x) | **$0.10/MTok (0.1x)** | $5/MTok |

**Real-world results:**
- Chat with books (100K tokens): **79% latency reduction, 90% cost savings**
- Many-shot prompting: **31% faster, 86% cheaper**
- Multi-turn conversations: **75% latency improvement, 53% cost reduction**

### Cache Breakpoints

**Key principles:**
- **Cumulative cache keys**: Each cache block depends on all content before it
- **Backward sequential checking**: System checks up to 20 blocks before each explicit breakpoint
- **Up to 4 breakpoints** can be defined per request

**Cache hierarchy**: `tools` → `system` → `messages`

**Implementation example:**
```python
import anthropic

client = anthropic.Anthropic()

# Cache system instructions and large documents
response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert Python developer...",
        },
        {
            "type": "text",
            "text": "<Entire codebase context or large document>",
            "cache_control": {"type": "ephemeral", "ttl": "1h"}  # 1-hour cache
        }
    ],
    messages=[{"role": "user", "content": "Analyze this code"}]
)

# Monitor cache performance
print(f"Cache hits: {response.usage.cache_read_input_tokens}")
print(f"Cache writes: {response.usage.cache_creation_input_tokens}")
print(f"Uncached: {response.usage.input_tokens}")
```

### Minimum Cacheable Lengths

| Model | Minimum Tokens |
|-------|----------------|
| Claude Opus 4.5 | 4096 tokens |
| Claude Sonnet 4.5 | 1024 tokens |
| Claude Haiku 4.5 | 4096 tokens |

### Cache Invalidation

| Change | Tools Cache | System Cache | Messages Cache |
|--------|-------------|--------------|----------------|
| Tool definitions modified | ❌ Invalidated | ❌ Invalidated | ❌ Invalidated |
| Web search toggle | ✅ Preserved | ❌ Invalidated | ❌ Invalidated |
| Tool choice parameter | ✅ Preserved | ✅ Preserved | ❌ Invalidated |
| Images added/removed | ✅ Preserved | ✅ Preserved | ❌ Invalidated |
| Thinking parameters | ✅ Preserved | ✅ Preserved | ❌ Invalidated |

### Best Practices for Caching

1. **Place stable content first**: System instructions, tool definitions, large documents
2. **Use single breakpoint at end**: System automatically checks previous 20 blocks
3. **Add breakpoints for >20 blocks**: Ensure all content can be cached
4. **Multi-turn conversations**: Mark final message with `cache_control`
5. **Monitor cache performance**: Track `cache_read_input_tokens` vs `cache_creation_input_tokens`
6. **Cache large reference docs with 1-hour TTL**: System prompts, codebases, knowledge bases
7. **Cache conversation history with 5-minute TTL**: Rapid back-and-forth interactions

### Speculative Caching Pattern (90% Latency Reduction)

Reduce time-to-first-token by warming the cache while user types:

```python
import asyncio
from anthropic import AsyncAnthropic

client = AsyncAnthropic()

async def speculative_caching():
    # Start cache warming with minimal request while user types
    cache_task = asyncio.create_task(
        client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1,  # Probe request - just warm the cache
            system=[{
                "type": "text",
                "text": large_context_string,
                "cache_control": {"type": "ephemeral"}
            }],
            messages=[{"role": "user", "content": "warmup"}]
        )
    )

    # Simulate user typing (3 seconds)
    await asyncio.sleep(3)
    await cache_task  # Ensure cache is warm

    # Actual request now hits warm cache - near instant
    response = await client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        system=[{
            "type": "text",
            "text": large_context_string,
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[{"role": "user", "content": actual_user_message}]
    )

    return response

# Result: 20.87s → 1.94s time-to-first-token (90.7% reduction)
```

---

## 2. Conversation Compaction (50-60% Token Reduction)

### How It Works

Automatically compresses conversation history when token usage exceeds threshold:

1. **Monitor** token usage per turn
2. **Inject summary prompt** when threshold exceeded
3. **Generate summary** wrapped in `<summary>` tags
4. **Clear history** and discard verbose tool results
5. **Resume** with compressed context

### Implementation (SDK Beta Feature)

```python
from anthropic import Anthropic

client = Anthropic()

# Using tool runner with auto-compaction
runner = client.beta.messages.tool_runner(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    tools=tools,
    messages=messages,
    compaction_control={
        "enabled": True,
        "context_token_threshold": 100000,  # Default: 100K tokens
        "model": "claude-haiku-4-5",  # Use cheaper model for summaries
        "summary_prompt": "Custom summary instructions..."  # Optional
    }
)

for message in runner:
    # Process messages - compaction happens automatically
    pass
```

### Configuration Parameters

| Parameter | Type | Default | Purpose |
|-----------|------|---------|---------|
| `enabled` | bool | Required | Enable auto-compaction |
| `context_token_threshold` | int | 100,000 | Token count triggering compaction |
| `model` | str | Main model | Model for generating summaries (use Haiku to save costs) |
| `summary_prompt` | str | Default | Custom instructions for summarization |

### Threshold Guidelines

| Threshold | Use Case | Characteristics |
|-----------|----------|----------------|
| **5K-20K** | Frequent compaction | Iterative tasks, minimal context needed |
| **50K-100K** | Balanced approach | Multi-phase workflows, moderate history |
| **100K-150K** | Maximum context | Tasks requiring substantial conversation history |
| **Default (100K)** | General purpose | Good balance for most applications |

### Real-World Results

**Customer service workflow (5 tickets, 35 tool calls):**

| Metric | Without Compaction | With Compaction | Savings |
|--------|-------------------|-----------------|---------|
| Turns | 37 | 26 | - |
| Compactions | 0 | 2 | - |
| Input tokens | 204,416 | 82,171 | **58.6%** |
| Output tokens | 4,422 | 4,275 | - |
| **Total tokens** | **208,838** | **86,446** | **122,392 (58.6%)** |

### What Gets Preserved vs. Discarded

✅ **Retained in summaries:**
- Entity IDs and names
- Categories and priorities
- Key decisions and routing logic
- Overall progress status
- Critical patterns discovered
- Next steps and pending actions

❌ **Discarded:**
- Full article/document text
- Complete response drafts
- Detailed reasoning chains
- Verbose tool results
- Redundant confirmations

### Manual Compaction Implementation

If you're not using the SDK beta feature, implement manual compaction:

```python
from anthropic import Anthropic

client = Anthropic()
COMPACTION_THRESHOLD = 75000  # 75K tokens
messages = []

SUMMARY_PROMPT = """Write a continuation summary including:

1. **Task Overview** - Core request and success criteria
2. **Current State** - Completed work, files created/modified
3. **Important Discoveries** - Technical constraints, key decisions made
4. **Next Steps** - Specific actions needed to complete the task
5. **Context to Preserve** - User preferences, domain-specific details

Wrap your summary in <summary></summary> tags."""

# Conversation loop
while True:
    user_input = input("User: ")
    messages.append({"role": "user", "content": user_input})

    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=2048,
        messages=messages
    )

    messages.append({"role": "assistant", "content": response.content})

    # Check if compaction needed
    total_tokens = (
        response.usage.input_tokens +
        (response.usage.cache_read_input_tokens or 0) +
        response.usage.output_tokens
    )

    if total_tokens > COMPACTION_THRESHOLD:
        print("[Compacting conversation history...]")

        # Generate summary using cheaper model
        summary_response = client.messages.create(
            model="claude-haiku-4-5",  # Cheaper for summarization
            max_tokens=4096,
            messages=messages + [{"role": "user", "content": SUMMARY_PROMPT}]
        )

        # Extract summary text
        summary_text = "".join(
            block.text for block in summary_response.content
            if block.type == "text"
        )

        # Replace entire history with summary
        messages = [{"role": "user", "content": summary_text}]
        print(f"[Compacted to {len(summary_text)} characters]")
```

### Use Cases

✅ **Ideal for:**
- Sequential processing (ticket workflows, data pipelines)
- Multi-phase workflows with natural checkpoints
- Iterative data processing
- Extended analysis sessions
- Batch operations where history accumulates

❌ **Avoid for:**
- Short tasks (<50K-100K tokens total)
- Tasks requiring complete audit trails
- Highly iterative refinement needing exact conversation details
- Legal/compliance scenarios requiring full history

---

## 3. PreCompact Hook (Preserve Critical Context)

### What It Does

The `PreCompact` hook fires **before** conversation compaction occurs, allowing you to:
- Archive full transcript before summarization
- Extract and preserve critical information
- Add custom context to the summary
- Block compaction if conditions aren't met
- Log compaction events for monitoring

### Hook Input Data

```python
{
    "hook_event_name": "PreCompact",
    "session_id": "abc123",
    "transcript_path": "/path/to/transcript.json",
    "cwd": "/working/directory",
    "trigger": "auto",  # or "manual"
    "custom_instructions": "Additional summary guidance..."  # optional
}
```

### Implementation (Python SDK)

```python
from claude_agent_sdk import query, ClaudeAgentOptions, HookMatcher
import json
import shutil
from datetime import datetime

async def preserve_before_compaction(input_data, tool_use_id, context):
    """Archive transcript and extract key information before compaction."""

    if input_data['hook_event_name'] != 'PreCompact':
        return {}

    transcript_path = input_data['transcript_path']
    session_id = input_data['session_id']

    # 1. Archive full transcript before it's compacted
    archive_path = f".agents/transcripts/{session_id}-{datetime.now().isoformat()}.json"
    shutil.copy(transcript_path, archive_path)
    print(f"[PreCompact] Archived transcript to {archive_path}")

    # 2. Extract critical information
    with open(transcript_path, 'r') as f:
        transcript = json.load(f)

    # Parse transcript for important entities, decisions, etc.
    critical_info = extract_critical_context(transcript)

    # 3. Add preservation instructions to summary
    preservation_note = f"""
CRITICAL CONTEXT TO PRESERVE:
- Entity IDs: {', '.join(critical_info['entity_ids'])}
- Key Decisions: {'; '.join(critical_info['decisions'])}
- Files Modified: {', '.join(critical_info['files'])}
- User Preferences: {critical_info['preferences']}
"""

    return {
        'systemMessage': preservation_note,
        'hookSpecificOutput': {
            'hookEventName': 'PreCompact',
            'additionalContext': preservation_note
        }
    }

def extract_critical_context(transcript):
    """Extract critical information from transcript."""
    # Implement your extraction logic
    return {
        'entity_ids': ['user-123', 'project-456'],
        'decisions': ['Use FastAPI', 'SQLite for development'],
        'files': ['src/main.py', 'tests/test_api.py'],
        'preferences': 'Prefers verbose logging in development'
    }

# Use the hook
async for message in query(
    prompt="Long-running task with compaction",
    options=ClaudeAgentOptions(
        hooks={
            'PreCompact': [HookMatcher(hooks=[preserve_before_compaction])]
        },
        # Enable compaction
        compaction_control={
            "enabled": True,
            "context_token_threshold": 50000
        }
    )
):
    print(message)
```

### Hook Configuration (Settings File)

For persistent hook configuration across sessions:

```json
{
  "hooks": {
    "PreCompact": [
      {
        "matcher": "auto",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/pre_compact_hook.py",
            "timeout": 60
          }
        ]
      }
    ]
  }
}
```

### Hook Script Example

```python
#!/usr/bin/env python3
"""PreCompact hook script for standalone execution."""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

def main():
    # Read hook input from stdin
    input_data = json.load(sys.stdin)

    if input_data.get('hook_event_name') != 'PreCompact':
        sys.exit(0)  # Not our hook, allow to proceed

    # Archive transcript
    transcript_path = Path(input_data['transcript_path'])
    archive_dir = Path('.agents/transcripts')
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    archive_path = archive_dir / f"session_{timestamp}.json"
    shutil.copy(transcript_path, archive_path)

    # Output preservation instructions
    output = {
        'systemMessage': f'Transcript archived to {archive_path}',
        'hookSpecificOutput': {
            'hookEventName': 'PreCompact',
            'additionalContext': 'Preserve entity IDs and key decisions in summary'
        }
    }

    print(json.dumps(output))
    sys.exit(0)  # Success

if __name__ == '__main__':
    main()
```

### Exit Codes for Hooks

| Exit Code | Meaning | Behavior |
|-----------|---------|----------|
| **0** | Success | Allow compaction to proceed (stdout shown in verbose mode) |
| **2** | Blocking error | Prevent compaction from happening |
| **Other** | Non-blocking error | Log error but allow compaction to proceed |

### Use Cases for PreCompact Hook

1. **Compliance & Audit**: Archive full transcripts before summarization for regulatory requirements
2. **Debug & Analysis**: Preserve detailed execution traces for troubleshooting
3. **Context Preservation**: Extract and inject critical entities/decisions into summary
4. **Custom Summarization**: Add domain-specific instructions to the summary prompt
5. **Monitoring**: Track compaction frequency and trigger alerts
6. **Conditional Compaction**: Block compaction if certain conditions aren't met

---

## 4. Combined Optimization Strategy

### The Ultimate Pattern: Caching + Compaction + Hooks

Combine all three mechanisms for maximum efficiency:

```python
from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, HookMatcher
from anthropic import Anthropic

async def optimized_conversation():
    client = Anthropic()

    # 1. Cache stable system prompts and documents (1-hour TTL)
    system_with_cache = [
        {
            "type": "text",
            "text": "You are an expert Python developer. Follow best practices...",
            "cache_control": {"type": "ephemeral", "ttl": "1h"}
        },
        {
            "type": "text",
            "text": large_codebase_context,  # Entire codebase or reference docs
            "cache_control": {"type": "ephemeral", "ttl": "1h"}
        }
    ]

    # 2. Enable auto-compaction with Haiku for summaries
    compaction_config = {
        "enabled": True,
        "context_token_threshold": 75000,  # 75K tokens
        "model": "claude-haiku-4-5",  # Cheaper model for summarization
        "summary_prompt": """Preserve these in your summary:
        - All entity IDs and names
        - Key architectural decisions
        - Files created or modified
        - Next action items
        - User preferences discovered"""
    }

    # 3. Add PreCompact hook for transcript archival
    hooks = {
        'PreCompact': [HookMatcher(hooks=[archive_transcript_hook])]
    }

    # Execute with combined optimizations
    async with ClaudeSDKClient(options=ClaudeAgentOptions(
        system_prompt=system_with_cache,
        compaction_control=compaction_config,
        hooks=hooks
    )) as client:
        await client.query("Long-running development task")

        async for message in client.receive_response():
            # Cache hits: 90% cost reduction
            # Compaction: 50-60% token reduction
            # Hook: Full history preserved
            process_message(message)
```

### Cost Impact Analysis

**Baseline (no optimization):**
- 10 turns conversation
- 150K input tokens per turn (codebase + history)
- Total: 1.5M input tokens
- Cost (Sonnet 4.5): 1.5M × $3/MTok = **$4.50**

**With caching only:**
- Turn 1: 150K tokens (cache write @ $3.75/MTok) = $0.56
- Turns 2-10: 150K tokens (cache hit @ $0.30/MTok) = $0.045 × 9 = $0.405
- Total cost: **$0.97** (78% savings)

**With compaction only:**
- Compaction at turn 5 and 8
- Average tokens reduced by 58%
- Total: 630K input tokens
- Cost: 630K × $3/MTok = **$1.89** (58% savings)

**With BOTH caching + compaction:**
- Turn 1: Cache write = $0.56
- Turns 2-4: Cache hits = $0.135
- Turn 5: Compaction + cache write = $0.28
- Turns 6-7: Cache hits = $0.09
- Turn 8: Compaction + cache write = $0.28
- Turns 9-10: Cache hits = $0.09
- Total cost: **$1.44** (68% savings)

### Rate Limit Optimization

**Cache-aware input tokens per minute (ITPM):**

```
Effective throughput = ITPM / (1 - cache_hit_rate)

Example with 2M ITPM and 80% cache hit rate:
Effective throughput = 2M / 0.2 = 10M tokens/minute (5x improvement)
```

**Compaction impact:**
- Reduces conversation growth rate
- Extends time before hitting context limits
- Reduces ITPM consumption on subsequent turns

### Monitoring Metrics

Track these metrics to optimize your strategy:

```python
# After each API call
metrics = {
    # Caching metrics
    "cache_hit_rate": cache_read / (cache_read + cache_creation + uncached),
    "cache_read_tokens": response.usage.cache_read_input_tokens,
    "cache_write_tokens": response.usage.cache_creation_input_tokens,
    "uncached_tokens": response.usage.input_tokens,

    # Compaction metrics
    "compaction_savings": (baseline_tokens - compacted_tokens) / baseline_tokens,
    "compaction_count": total_compactions,
    "avg_tokens_per_turn": total_input_tokens / turn_count,

    # Performance metrics
    "time_to_first_token": ttft_ms,
    "effective_throughput": actual_tokens / (time_seconds / 60),
    "cost_per_turn": estimated_cost_usd
}

# Log and analyze
logger.info("Optimization metrics", extra=metrics)
```

---

## 5. Recommendations for Your Starter Kit

### Phase 1: Add Caching Patterns Reference

Create `.claude/reference/prompt-caching-patterns.md`:

```markdown
# Prompt Caching Patterns

## System Prompt Caching (1-hour TTL)
- Cache system instructions that rarely change
- Use 1-hour TTL for stability
- Monitor cache hit rates

## Document Caching
- Cache large codebases, knowledge bases, reference docs
- Place at end of system array with cache_control
- Minimum 1024 tokens (Sonnet) or 4096 tokens (Opus/Haiku)

## Conversation History Caching (5-minute TTL)
- Mark final user message with cache_control
- Good for rapid back-and-forth
- TTL resets on each use

## Speculative Caching
- Warm cache while user types
- 90% latency reduction
- Ideal for user-facing applications

## Monitoring
Track cache_read_input_tokens vs cache_creation_input_tokens
```

### Phase 2: Add Compaction Patterns Reference

Create `.claude/reference/conversation-compaction-patterns.md`:

```markdown
# Conversation Compaction Patterns

## Auto-Compaction Setup
- Enable in SDK with compaction_control
- Set threshold based on use case (50K-150K)
- Use Haiku for summaries to save costs

## Custom Summary Prompts
Define what to preserve:
- Entity IDs and names
- Key decisions and rationale
- Files created/modified
- Next action items
- User preferences

## Manual Compaction
- Implement for non-SDK usage
- Inject summary prompt at threshold
- Replace history with summary

## Use Cases
- Sequential workflows (best fit)
- Multi-phase projects
- Extended analysis sessions
```

### Phase 3: Add PreCompact Hook Example

Create `.claude/hooks/pre_compact.py`:

```python
#!/usr/bin/env python3
"""Archive transcripts before compaction."""

import json
import sys
import shutil
from pathlib import Path
from datetime import datetime

def main():
    input_data = json.load(sys.stdin)

    if input_data.get('hook_event_name') != 'PreCompact':
        sys.exit(0)

    # Archive transcript
    transcript_path = Path(input_data['transcript_path'])
    archive_dir = Path('.agents/transcripts')
    archive_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    session_id = input_data.get('session_id', 'unknown')
    archive_path = archive_dir / f"{session_id}_{timestamp}.json"

    shutil.copy(transcript_path, archive_path)

    output = {
        'systemMessage': f'Transcript archived to {archive_path}. Preserve entity IDs and decisions in summary.',
        'hookSpecificOutput': {
            'hookEventName': 'PreCompact'
        }
    }

    print(json.dumps(output))
    sys.exit(0)

if __name__ == '__main__':
    main()
```

### Phase 4: Update CLAUDE.md with Context Management

Add section to your main CLAUDE.md:

```markdown
## Context Management & Optimization

### Prompt Caching
- Cache system prompts with 1-hour TTL
- Cache large documents and codebases
- Monitor cache hit rates (target 70%+)
- See: `.claude/reference/prompt-caching-patterns.md`

### Conversation Compaction
- Auto-compact at 75K token threshold
- Use Haiku for summaries (cost optimization)
- Preserve entity IDs, decisions, file changes
- See: `.claude/reference/conversation-compaction-patterns.md`

### PreCompact Hook
- Archive full transcripts before summarization
- Extract critical context for preservation
- Located: `.claude/hooks/pre_compact.py`
```

### Phase 5: Add to Validation Command

Update `/validate` command to check for token efficiency:

```markdown
## Stage 7: Token Efficiency (Optional)

Check optimization opportunities:
- [ ] System prompts marked with cache_control
- [ ] Large documents use 1-hour TTL caching
- [ ] Conversation loops implement compaction
- [ ] PreCompact hook configured for archival
- [ ] Cache hit rates logged and monitored
```

---

## Key Takeaways

1. **Caching is critical**: 60-90% cost reduction, 75-90% latency improvement for cached content
2. **Compaction enables long sessions**: 50-60% token reduction, extends context window usage
3. **PreCompact preserves history**: Archive transcripts, extract critical context before summarization
4. **Combine all three**: Maximize cost savings and performance
5. **Monitor metrics**: Track cache hits, compaction frequency, token usage
6. **Use cheaper models for summaries**: Haiku for compaction summaries saves significant costs
7. **Speculative caching**: 90% latency reduction for user-facing applications

**Implementation Priority**: HIGH - These patterns are essential for production-grade Claude applications.
