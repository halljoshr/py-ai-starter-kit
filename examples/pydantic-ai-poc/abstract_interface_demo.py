#!/usr/bin/env python3
"""
Demonstrate abstract interface pattern for provider-agnostic agents.

Shows how to:
- Define provider-agnostic interface
- Implement multiple providers (Pydantic AI, mock Bedrock)
- Switch providers transparently
- Feature flag control

This is the architecture pattern for migration.

Dependencies:
    uv add pydantic-ai

Usage:
    uv run python examples/pydantic-ai-poc/abstract_interface_demo.py
"""

import asyncio
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Any, Dict
from dataclasses import dataclass
from pydantic import BaseModel, Field
from pydantic_ai import Agent


# ============================================================================
# PART 1: Abstract Interface (Provider-Agnostic)
# ============================================================================

OutputT = TypeVar("OutputT", bound=BaseModel)
DepsT = TypeVar("DepsT")


@dataclass
class AgentResult(Generic[OutputT]):
    """Standardized agent result"""
    output: OutputT
    raw_response: str | None = None
    usage: Dict[str, int] | None = None
    session_id: str | None = None


class AgentProvider(ABC, Generic[OutputT, DepsT]):
    """
    Abstract base for agent providers.

    Both Bedrock and Pydantic AI implement this interface.
    Application code only depends on this interface, not specific providers.
    """

    @abstractmethod
    async def invoke(
        self,
        prompt: str,
        dependencies: DepsT,
        session_id: str | None = None,
        **kwargs: Any
    ) -> AgentResult[OutputT]:
        """Invoke the agent with a prompt"""
        pass


# ============================================================================
# PART 2: Concrete Implementations
# ============================================================================

class PydanticAIProvider(AgentProvider[OutputT, DepsT]):
    """Pydantic AI implementation"""

    def __init__(
        self,
        model: str,
        output_type: type[OutputT],
        system_prompt: str | None = None
    ):
        self.model = model
        self.output_type = output_type
        self.agent = Agent(
            model=model,
            output_type=output_type,
            system_prompt=system_prompt or "You are a helpful assistant."
        )

    async def invoke(
        self,
        prompt: str,
        dependencies: DepsT,
        session_id: str | None = None,
        **kwargs: Any
    ) -> AgentResult[OutputT]:
        """Invoke Pydantic AI agent"""
        result = await self.agent.run(prompt, **kwargs)

        return AgentResult(
            output=result.output,
            raw_response=result.all_messages()[-1].content if result.all_messages() else None,
            usage={
                "input_tokens": result.usage().request_tokens,
                "output_tokens": result.usage().response_tokens,
                "total_tokens": result.usage().total_tokens,
            },
            session_id=session_id,
        )


class MockBedrockProvider(AgentProvider[OutputT, DepsT]):
    """
    Mock Bedrock implementation for demonstration.

    In production, this would wrap the real bedrock_service.py:
        response = bedrock_agent_runtime.invoke_agent(...)
        return AgentResult(output=parse_response(response))
    """

    def __init__(self, output_type: type[OutputT]):
        self.output_type = output_type

    async def invoke(
        self,
        prompt: str,
        dependencies: DepsT,
        session_id: str | None = None,
        **kwargs: Any
    ) -> AgentResult[OutputT]:
        """Mock Bedrock invocation"""
        print(f"   [Mock Bedrock] Invoking agent...")

        # In production, this would call actual Bedrock API
        # For demo, return mock data matching output type
        mock_data = {
            "total_value": 250450.0,
            "item_count": 3,
            "status": "valid"
        }

        return AgentResult(
            output=self.output_type(**mock_data),
            raw_response="[Mock Bedrock response]",
            usage={"input_tokens": 100, "output_tokens": 50, "total_tokens": 150},
            session_id=session_id,
        )


# ============================================================================
# PART 3: Application Code (Provider-Agnostic)
# ============================================================================

class DataSummary(BaseModel):
    """Data analysis output schema"""
    total_value: float
    item_count: int
    status: str = Field(pattern="^(valid|invalid|needs_review)$")


class DataAnalysisService:
    """
    Data analysis service that works with ANY provider.

    Application code depends on AgentProvider interface,
    not specific implementations.
    """

    def __init__(self, provider: AgentProvider[DataSummary, None]):
        self.provider = provider

    async def analyze_data(self, data: str, session_id: str) -> DataSummary:
        """
        Analyze data using configured provider.

        This method doesn't know or care which provider is used.
        Works identically with Bedrock, Pydantic AI, or any future provider.
        """
        print(f"\n📊 Analyzing data with {self.provider.__class__.__name__}")

        result = await self.provider.invoke(
            prompt=f"Analyze this data:\n\n{data}",
            dependencies=None,
            session_id=session_id
        )

        print(f"   ✓ Analysis complete")
        print(f"   Tokens: {result.usage['total_tokens']}" if result.usage else "")

        return result.output


# ============================================================================
# PART 4: Factory & Feature Flags
# ============================================================================

class AgentConfig:
    """Configuration with feature flags"""
    USE_PYDANTIC_AI = True  # Feature flag
    PYDANTIC_AI_MODEL = "anthropic:claude-sonnet-4-0"


def create_analysis_agent(config: AgentConfig) -> AgentProvider[DataSummary, None]:
    """
    Factory to create agent based on configuration.

    In production, this reads from environment variables:
        USE_PYDANTIC_AI = os.getenv("USE_PYDANTIC_AI", "false").lower() == "true"
    """
    if config.USE_PYDANTIC_AI:
        print("🚀 Using Pydantic AI provider")
        return PydanticAIProvider(
            model=config.PYDANTIC_AI_MODEL,
            output_type=DataSummary,
            system_prompt="Extract data summary from provided information"
        )
    else:
        print("🚀 Using Bedrock provider (mock)")
        return MockBedrockProvider(output_type=DataSummary)


# ============================================================================
# PART 5: Demo
# ============================================================================

async def demo_provider_switching():
    """Demonstrate switching providers with feature flag"""

    data = """
    Data Summary:
    - Item 1: Value $45,000
    - Item 2: Value $120,000
    - Item 3: Value $85,450
    - Total: $250,450
    """

    print("=" * 70)
    print("Abstract Interface Demo: Provider Switching")
    print("=" * 70)

    # Test 1: With Pydantic AI
    print("\n" + "=" * 70)
    print("Test 1: Pydantic AI Provider")
    print("=" * 70)

    config_pydantic = AgentConfig()
    config_pydantic.USE_PYDANTIC_AI = True

    provider_pydantic = create_analysis_agent(config_pydantic)
    service_pydantic = DataAnalysisService(provider_pydantic)

    try:
        result_pydantic = await service_pydantic.analyze_data(data, "session-123")
        print(f"\nResult: {result_pydantic}")
    except Exception as e:
        print(f"\n⚠️  Error: {e}")
        print("   (Set ANTHROPIC_API_KEY to test with real API)")
        result_pydantic = None

    # Test 2: With mock Bedrock
    print("\n" + "=" * 70)
    print("Test 2: Bedrock Provider (Mock)")
    print("=" * 70)

    config_bedrock = AgentConfig()
    config_bedrock.USE_PYDANTIC_AI = False

    provider_bedrock = create_analysis_agent(config_bedrock)
    service_bedrock = DataAnalysisService(provider_bedrock)

    result_bedrock = await service_bedrock.analyze_data(data, "session-456")
    print(f"\nResult: {result_bedrock}")

    # Summary
    print("\n" + "=" * 70)
    print("Key Benefits")
    print("=" * 70)
    print("✅ Application code (DataAnalysisService) is provider-agnostic")
    print("✅ Same interface for all providers (AgentProvider)")
    print("✅ Easy testing (mock providers)")
    print("✅ Feature flag control (gradual rollout)")
    print("✅ No vendor lock-in (switch providers anytime)")
    print("\n   This is the migration architecture pattern!")


async def main():
    import os

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("ℹ️  Tip: Set ANTHROPIC_API_KEY to test with real Anthropic API")
        print("   Otherwise, demo will use mock Bedrock provider\n")

    await demo_provider_switching()


if __name__ == "__main__":
    asyncio.run(main())
