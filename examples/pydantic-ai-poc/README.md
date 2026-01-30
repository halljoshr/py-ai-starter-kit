# Pydantic AI POC Examples

**Purpose:** Demonstrate provider-agnostic agent architecture for document processing applications.

---

## Quick Start

### 1. Install Dependencies

```bash
cd /home/jhall/Projects/py-ai-starter-kit
uv add pydantic-ai
```

### 2. Set API Key

```bash
# For Anthropic (recommended)
export ANTHROPIC_API_KEY=your-key-here

# Optional: For provider comparison
export OPENAI_API_KEY=your-openai-key
```

### 3. Run Examples

```bash
# Example 1: Document processing agent POC
uv run python examples/pydantic-ai-poc/document_agent_poc.py

# Example 2: Provider comparison
uv run python examples/pydantic-ai-poc/provider_comparison.py

# Example 3: Abstract interface demo
uv run python examples/pydantic-ai-poc/abstract_interface_demo.py
```

---

## Examples

### 1. document_agent_poc.py

**Demonstrates:**
- Document analysis with structured data extraction
- Type-safe output with Pydantic validation
- Provider switching via environment variable

**Key Features:**
- 6x faster than OCR preprocessing (no Textract needed)
- Direct PDF ingestion (shown with text for POC)
- Same code works with Anthropic, Bedrock, OpenAI, Ollama

**Usage:**
```bash
# Default: Anthropic Claude Sonnet 4
uv run python examples/pydantic-ai-poc/document_agent_poc.py

# Switch to different provider
MODEL="openai:gpt-4" uv run python examples/pydantic-ai-poc/document_agent_poc.py

# Local development with Ollama (no API key needed)
MODEL="ollama:llama3" uv run python examples/pydantic-ai-poc/document_agent_poc.py
```

**Expected Output:**
```
🧪 POC: Document Analysis with Pydantic AI
   Model: anthropic:claude-sonnet-4-0

📄 Analyzing sample document data...

✓ Analysis complete
   Input tokens: 245
   Output tokens: 67
   Total cost: $0.0012

📊 Extracted Data:
   Entity: Sample Corporation LLC
   ID: 12-3456789
   Field 1: $120,450.00
   Field 2: $45,230.00
   Confidence: 95.5%
```

---

### 2. provider_comparison.py

**Demonstrates:**
- Side-by-side provider comparison
- Performance metrics (speed, cost, tokens)
- Output consistency validation

**Key Features:**
- Same prompt to multiple providers
- Quantitative comparison (speed, cost)
- Validates output consistency

**Usage:**
```bash
# Requires ANTHROPIC_API_KEY and/or OPENAI_API_KEY
uv run python examples/pydantic-ai-poc/provider_comparison.py
```

**Expected Output:**
```
1️⃣  Anthropic Direct API (Recommended)
----------------------------------------------------------------------
   ✓ Duration: 1.23s
   Tokens: 187 in, 45 out
   Cost: $0.0009
   Result:
      Total Value: $250,000.00
      Items: 3
      Status: valid

2️⃣  OpenAI GPT-4
----------------------------------------------------------------------
   ✓ Duration: 2.45s
   Tokens: 195 in, 52 out
   Cost: $0.0015
   Result:
      Total Value: $250,000.00
      Items: 3
      Status: valid

📊 Comparison Summary
----------------------------------------------------------------------
🏎️  Fastest: Anthropic Direct API (Recommended)
   Anthropic: 1.23s (1.0x)
   OpenAI: 2.45s (2.0x)

💰 Cost:
   Anthropic: $0.0009 (1.0x)
   OpenAI: $0.0015 (1.7x)

✓ Output Consistency: All providers returned identical results
```

---

### 3. abstract_interface_demo.py

**Demonstrates:**
- Abstract provider interface (AgentProvider)
- Multiple implementations (Pydantic AI, mock Bedrock)
- Provider-agnostic application code
- Feature flag control

**Key Features:**
- Same interface for all providers
- Easy testing with mock providers
- Feature flag rollout strategy
- Zero vendor lock-in

**Usage:**
```bash
# Works with or without API key (uses mock for demo)
uv run python examples/pydantic-ai-poc/abstract_interface_demo.py
```

**Expected Output:**
```
Test 1: Pydantic AI Provider
----------------------------------------------------------------------
🚀 Using Pydantic AI provider

📊 Analyzing data with PydanticAIProvider
   ✓ Analysis complete
   Tokens: 232

Result: total_value=250450.0 item_count=3 status='valid'

Test 2: Bedrock Provider (Mock)
----------------------------------------------------------------------
🚀 Using Bedrock provider (mock)

📊 Analyzing data with MockBedrockProvider
   [Mock Bedrock] Invoking agent...
   ✓ Analysis complete
   Tokens: 150

Result: total_value=250450.0 item_count=3 status='valid'

Key Benefits
----------------------------------------------------------------------
✅ Application code is provider-agnostic
✅ Same interface for all providers (AgentProvider)
✅ Easy testing (mock providers)
✅ Feature flag control (gradual rollout)
✅ No vendor lock-in (switch providers anytime)

   This is the migration architecture pattern!
```

---

## Architecture Pattern

### Abstract Interface

```python
class AgentProvider(ABC, Generic[OutputT, DepsT]):
    """Provider-agnostic interface"""

    @abstractmethod
    async def invoke(
        self,
        prompt: str,
        dependencies: DepsT,
        session_id: str | None = None,
        **kwargs: Any
    ) -> AgentResult[OutputT]:
        pass
```

### Implementations

**Pydantic AI:**
```python
class PydanticAIProvider(AgentProvider):
    def __init__(self, model: str, output_type: type[OutputT]):
        self.agent = Agent(model=model, output_type=output_type)

    async def invoke(self, prompt, dependencies, session_id):
        result = await self.agent.run(prompt, deps=dependencies)
        return AgentResult(output=result.output)
```

**Bedrock (Wrapper):**
```python
class BedrockAgentProvider(AgentProvider):
    def __init__(self, agent_id: str, output_type: type[OutputT]):
        self.bedrock_service = BedrockAgentService()

    async def invoke(self, prompt, dependencies, session_id):
        response = await self.bedrock_service.invoke_bedrock_agent(...)
        return AgentResult(output=parse_response(response))
```

### Application Code

```python
class DocumentProcessingService:
    def __init__(self, provider: AgentProvider):
        self.provider = provider  # Works with ANY provider

    async def process(self, data: str):
        result = await self.provider.invoke(data, deps, session_id)
        return result.output
```

**Key:** Application code depends on interface, not implementations.

---

## Benefits vs Current Bedrock Approach

### Textract OCR (Current)

```python
# 1. Download PDF from S3
pdf_bytes = await download_from_s3(s3_key)

# 2. Convert PDF → PNG (Textract requirement)
images = await convert_pdf_to_images(pdf_bytes)  # 5MB limit per page

# 3. OCR with Textract
text = await extract_text_with_textract(images)  # 30-60 seconds

# 4. Invoke Bedrock agent with text
result = await bedrock_service.invoke_agent(text)
```

**Issues:**
- ❌ 30-60 second processing time
- ❌ 5MB page limit (must split large PDFs)
- ❌ Quality loss (OCR errors, formatting loss)
- ❌ Extra AWS costs (Textract + S3 storage)

### Vision Model (Pydantic AI)

```python
# 1. Download PDF from S3
pdf_bytes = await download_from_s3(s3_key)

# 2. Invoke with direct PDF ingestion
result = await provider.invoke(
    prompt="Extract data from document",
    files=[(pdf_bytes, "application/pdf")]  # Direct PDF!
)  # 5-10 seconds
```

**Benefits:**
- ✅ 6x faster (5-10s vs 30-60s)
- ✅ No file size limits
- ✅ Preserves visual formatting
- ✅ No Textract costs
- ✅ Higher accuracy (sees actual document)

---

## Provider Flexibility

### Switch Providers Instantly

```python
# Development: Local Ollama (no API costs)
provider = PydanticAIProvider(model="ollama:llama3")

# Staging: OpenAI (fast iteration)
provider = PydanticAIProvider(model="openai:gpt-4")

# Production: Anthropic direct (fastest, cheapest)
provider = PydanticAIProvider(model="anthropic:claude-sonnet-4-0")

# OR: Bedrock (if AWS required)
provider = PydanticAIProvider(model="bedrock:anthropic.claude-3-sonnet")
```

**Same application code for all!**

---

## Next Steps

### For Application Migration

1. **Copy these examples to your project:**
   ```bash
   cp -r examples/pydantic-ai-poc /path/to/your/project/examples/
   ```

2. **Add pydantic-ai to dependencies:**
   ```bash
   cd /path/to/your/project
   uv add pydantic-ai
   ```

3. **Test with real documents:**
   ```bash
   # Modify document_agent_poc.py to load actual PDF
   uv run python examples/pydantic-ai-poc/document_agent_poc.py samples/document.pdf
   ```

4. **Implement Foundation:**
   - Create `app/services/agent_provider.py`
   - Create `app/services/pydantic_ai_provider.py`
   - Create `app/services/bedrock_agent_provider.py`
   - Add feature flags to settings

5. **Implement First Agent:**
   - Create parallel endpoint for testing
   - A/B test Bedrock vs Pydantic AI
   - Gradual rollout with feature flag

---

## Related Documents

- **Migration Plan:** `.agents/research/bedrock-converse-migration-plan-sanitized-2026-01-30.md`
- **Decision Summary:** `.agents/research/migration-decision-summary-sanitized-2026-01-30.md`

---

## Support

For questions or issues:
1. Check migration plan for detailed roadmap
2. Review decision summary for option comparison
3. Test POC examples to understand patterns
