#!/usr/bin/env python3
"""
Compare different providers side-by-side.

Demonstrates:
- Provider switching with same code
- Performance comparison
- Cost comparison
- Output validation consistency

Dependencies:
    uv add pydantic-ai

Usage:
    # Requires ANTHROPIC_API_KEY
    uv run python examples/pydantic-ai-poc/provider_comparison.py
"""

import asyncio
import time
import os
from pydantic import BaseModel, Field
from pydantic_ai import Agent


class DataSummary(BaseModel):
    """Simplified data summary for testing"""
    total_value: float = Field(description="Total value from all sources")
    item_count: int = Field(description="Number of items")
    status: str = Field(pattern="^(valid|invalid|needs_review)$", description="Status assessment")


async def analyze_with_model(prompt: str, model: str, label: str) -> dict:
    """Analyze with specific model and return metrics"""
    print(f"\n{label}")
    print("-" * 70)

    try:
        start = time.time()

        agent = Agent(
            model=model,
            output_type=DataSummary,
            system_prompt="Extract data summary from provided information"
        )

        result = await agent.run(prompt)
        duration = time.time() - start

        print(f"   ✓ Duration: {duration:.2f}s")
        print(f"   Tokens: {result.usage().request_tokens} in, {result.usage().response_tokens} out")

        if hasattr(result.usage(), 'total_cost'):
            print(f"   Cost: ${result.usage().total_cost():.4f}")

        print(f"   Result:")
        print(f"      Total Value: ${result.output.total_value:,.2f}")
        print(f"      Items: {result.output.item_count}")
        print(f"      Status: {result.output.status}")

        return {
            "model": model,
            "label": label,
            "duration": duration,
            "input_tokens": result.usage().request_tokens,
            "output_tokens": result.usage().response_tokens,
            "cost": result.usage().total_cost() if hasattr(result.usage(), 'total_cost') else None,
            "output": result.output,
            "success": True
        }

    except Exception as e:
        print(f"   ❌ Error: {str(e)}")
        return {
            "model": model,
            "label": label,
            "success": False,
            "error": str(e)
        }


async def compare_providers():
    """Compare different providers"""
    prompt = """
    Data Summary:
    - Item 1 (ABC Corp): Value $45,000
    - Item 2 (XYZ LLC): Value $120,000
    - Item 3 (DEF Inc): Value $85,000
    - Total items: 3
    - Status: All items validated
    - Year: 2024
    """

    print("=" * 70)
    print("Provider Comparison POC")
    print("=" * 70)

    results = []

    # Test 1: Anthropic Direct API (fastest, cheapest)
    if os.getenv("ANTHROPIC_API_KEY"):
        result = await analyze_with_model(
            prompt,
            "anthropic:claude-sonnet-4-0",
            "1️⃣  Anthropic Direct API (Recommended)"
        )
        results.append(result)
    else:
        print("\n1️⃣  Anthropic Direct API")
        print("-" * 70)
        print("   ⚠️  Skipped: Set ANTHROPIC_API_KEY to test")

    # Test 2: OpenAI (alternative provider)
    if os.getenv("OPENAI_API_KEY"):
        result = await analyze_with_model(
            prompt,
            "openai:gpt-4",
            "2️⃣  OpenAI GPT-4"
        )
        results.append(result)
    else:
        print("\n2️⃣  OpenAI GPT-4")
        print("-" * 70)
        print("   ⚠️  Skipped: Set OPENAI_API_KEY to test")

    # Test 3: Bedrock (current production provider)
    # Note: Requires AWS credentials configured
    # Uncomment to test:
    # if os.getenv("AWS_PROFILE") or os.getenv("AWS_ACCESS_KEY_ID"):
    #     result = await analyze_with_model(
    #         prompt,
    #         "bedrock:anthropic.claude-3-sonnet-20240229-v1:0",
    #         "3️⃣  AWS Bedrock (Current Production)"
    #     )
    #     results.append(result)

    # Comparison
    if len([r for r in results if r.get("success")]) >= 2:
        print("\n" + "=" * 70)
        print("📊 Comparison Summary")
        print("=" * 70)

        successful = [r for r in results if r.get("success")]

        # Speed comparison
        fastest = min(successful, key=lambda x: x["duration"])
        print(f"\n🏎️  Fastest: {fastest['label']}")
        for r in successful:
            relative_speed = r["duration"] / fastest["duration"]
            print(f"   {r['label']}: {r['duration']:.2f}s ({relative_speed:.1f}x)")

        # Cost comparison
        with_cost = [r for r in successful if r.get("cost") is not None]
        if with_cost:
            cheapest = min(with_cost, key=lambda x: x["cost"])
            print(f"\n💰 Cost:")
            for r in with_cost:
                relative_cost = r["cost"] / cheapest["cost"] if cheapest["cost"] > 0 else 1.0
                print(f"   {r['label']}: ${r['cost']:.4f} ({relative_cost:.1f}x)")

        # Output consistency
        outputs = [r["output"] for r in successful]
        if all(o == outputs[0] for o in outputs):
            print(f"\n✓ Output Consistency: All providers returned identical results")
        else:
            print(f"\n⚠️  Output Consistency: Some variation in results")

    print("\n" + "=" * 70)
    print("Key Insights")
    print("=" * 70)
    print("• Same code works with ANY provider (just change env var)")
    print("• Pydantic validation ensures type safety across providers")
    print("• Easy A/B testing and cost optimization")
    print("• No vendor lock-in - switch providers anytime")


async def main():
    if not os.getenv("ANTHROPIC_API_KEY") and not os.getenv("OPENAI_API_KEY"):
        print("⚠️  No API keys found")
        print("\nSet at least one:")
        print("  export ANTHROPIC_API_KEY=your-key")
        print("  export OPENAI_API_KEY=your-key")
        print()
        return

    await compare_providers()


if __name__ == "__main__":
    asyncio.run(main())
