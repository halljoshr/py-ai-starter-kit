#!/usr/bin/env python3
"""
Coverage validation script for /validate skill

Parses pytest coverage output and provides detailed analysis:
- Overall coverage percentage
- Per-file coverage breakdown
- Files below threshold
- Missing line ranges

Usage:
    uv run python .claude/skills/validate/scripts/check_coverage.py coverage.json

Returns:
    0 if coverage >= threshold
    1 if coverage < threshold
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple


def parse_coverage_report(report_path: Path, threshold: float = 80.0) -> Dict:
    """
    Parse pytest coverage JSON report

    Args:
        report_path: Path to coverage.json file
        threshold: Minimum required coverage percentage

    Returns:
        Dictionary with coverage analysis
    """
    if not report_path.exists():
        return {
            "error": f"Coverage report not found: {report_path}",
            "total_coverage": 0.0,
            "passed": False,
        }

    try:
        with open(report_path) as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        return {
            "error": f"Invalid JSON in coverage report: {e}",
            "total_coverage": 0.0,
            "passed": False,
        }

    # Extract total coverage
    total_coverage = data["totals"]["percent_covered"]

    # Extract per-file coverage
    by_file = {}
    below_threshold = []

    for file_path, file_data in data["files"].items():
        coverage = file_data["summary"]["percent_covered"]
        by_file[file_path] = coverage

        if coverage < threshold:
            # Find missing line ranges
            missing_lines = file_data["missing_lines"]
            below_threshold.append({
                "file": file_path,
                "coverage": coverage,
                "missing_lines": missing_lines,
            })

    # Sort files below threshold by coverage (worst first)
    below_threshold.sort(key=lambda x: x["coverage"])

    return {
        "total_coverage": total_coverage,
        "threshold": threshold,
        "passed": total_coverage >= threshold,
        "by_file": by_file,
        "below_threshold": below_threshold,
        "num_files": len(by_file),
        "num_below_threshold": len(below_threshold),
    }


def format_missing_lines(missing_lines: List[int]) -> str:
    """
    Convert list of line numbers to compact range notation

    Example: [1, 2, 3, 5, 7, 8, 9] -> "1-3, 5, 7-9"
    """
    if not missing_lines:
        return "none"

    ranges = []
    start = missing_lines[0]
    end = missing_lines[0]

    for line in missing_lines[1:]:
        if line == end + 1:
            end = line
        else:
            if start == end:
                ranges.append(str(start))
            else:
                ranges.append(f"{start}-{end}")
            start = end = line

    # Add final range
    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ", ".join(ranges)


def print_coverage_report(result: Dict) -> None:
    """Print formatted coverage report to stdout"""

    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return

    # Overall status
    total = result["total_coverage"]
    threshold = result["threshold"]
    passed = result["passed"]

    status_icon = "✅" if passed else "❌"
    print(f"\n{status_icon} Overall Coverage: {total:.1f}% (threshold: {threshold}%)")

    if passed:
        print(f"   All {result['num_files']} files meet coverage requirements")
    else:
        print(f"   Coverage is {threshold - total:.1f}% below threshold")

    # Files below threshold
    if result["below_threshold"]:
        print(f"\n⚠️  {result['num_below_threshold']} files below {threshold}% coverage:\n")

        for item in result["below_threshold"]:
            file_path = item["file"]
            coverage = item["coverage"]
            missing = format_missing_lines(item["missing_lines"])

            print(f"   {file_path}")
            print(f"      Coverage: {coverage:.1f}%")
            print(f"      Missing lines: {missing}\n")

    # Summary
    print("\nTo increase coverage:")
    print("   1. Run: uv run pytest --cov --cov-report=html")
    print("   2. Open: htmlcov/index.html in browser")
    print("   3. Add tests for uncovered lines")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python check_coverage.py <coverage.json>")
        print("\nExample:")
        print("   uv run pytest --cov --cov-report=json:coverage.json")
        print("   uv run python .claude/skills/validate/scripts/check_coverage.py coverage.json")
        sys.exit(1)

    report_path = Path(sys.argv[1])
    threshold = float(sys.argv[2]) if len(sys.argv) > 2 else 80.0

    result = parse_coverage_report(report_path, threshold)
    print_coverage_report(result)

    # Exit code 0 if passed, 1 if failed
    sys.exit(0 if result.get("passed", False) else 1)


if __name__ == "__main__":
    main()
