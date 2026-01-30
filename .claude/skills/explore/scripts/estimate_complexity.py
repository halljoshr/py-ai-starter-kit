#!/usr/bin/env python3
"""
Codebase complexity estimation script for /explore skill

Analyzes codebase structure to inform feasibility assessment:
- File counts and LOC
- Dependency analysis
- Module structure
- Complexity indicators

Usage:
    uv run python .claude/skills/explore/scripts/estimate_complexity.py <path>

Returns:
    Summary statistics for feasibility assessment
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List
from collections import Counter


def count_imports(tree: ast.AST) -> tuple[int, set]:
    """Count imports and extract unique packages"""
    import_count = 0
    packages = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            import_count += 1
            for alias in node.names:
                packages.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            import_count += 1
            if node.module:
                packages.add(node.module.split('.')[0])

    return import_count, packages


def analyze_file(file_path: Path) -> Dict:
    """Analyze single Python file"""
    try:
        content = file_path.read_text()
        lines = content.splitlines()
        tree = ast.parse(content, filename=str(file_path))
    except (SyntaxError, UnicodeDecodeError):
        return {
            "file": str(file_path),
            "error": "Parse error",
            "skipped": True,
        }

    # Count code elements
    functions = sum(1 for node in ast.walk(tree) if isinstance(node, ast.FunctionDef))
    classes = sum(1 for node in ast.walk(tree) if isinstance(node, ast.ClassDef))
    imports, packages = count_imports(tree)

    # Count non-empty lines (approximate LOC)
    loc = sum(1 for line in lines if line.strip() and not line.strip().startswith('#'))

    return {
        "file": str(file_path),
        "loc": loc,
        "functions": functions,
        "classes": classes,
        "imports": imports,
        "packages": list(packages),
    }


def analyze_codebase(path: Path) -> Dict:
    """Analyze entire codebase for complexity metrics"""

    if not path.exists():
        return {
            "error": f"Path does not exist: {path}",
            "total_files": 0,
        }

    # Find Python files
    if path.is_file():
        python_files = [path]
    else:
        python_files = [
            f for f in path.rglob("*.py")
            if "venv" not in f.parts
            and ".tox" not in f.parts
            and "__pycache__" not in f.parts
            and ".venv" not in f.parts
        ]

    # Analyze each file
    results = []
    all_packages = Counter()

    for file_path in python_files:
        file_result = analyze_file(file_path)

        if not file_result.get("skipped"):
            results.append(file_result)
            for pkg in file_result.get("packages", []):
                all_packages[pkg] += 1

    # Aggregate statistics
    total_files = len(results)
    total_loc = sum(r["loc"] for r in results)
    total_functions = sum(r["functions"] for r in results)
    total_classes = sum(r["classes"] for r in results)
    total_imports = sum(r["imports"] for r in results)

    # File size distribution
    loc_distribution = {
        "small": sum(1 for r in results if r["loc"] < 100),
        "medium": sum(1 for r in results if 100 <= r["loc"] < 500),
        "large": sum(1 for r in results if 500 <= r["loc"] < 1000),
        "very_large": sum(1 for r in results if r["loc"] >= 1000),
    }

    # Complexity indicators
    avg_loc_per_file = total_loc / total_files if total_files > 0 else 0
    avg_functions_per_file = total_functions / total_files if total_files > 0 else 0

    # Classify complexity
    if total_files <= 3 and total_loc < 500:
        complexity = "Small"
    elif total_files <= 10 and total_loc < 2000:
        complexity = "Medium"
    elif total_files <= 30 and total_loc < 10000:
        complexity = "Large"
    else:
        complexity = "Very Large"

    return {
        "path": str(path),
        "total_files": total_files,
        "total_loc": total_loc,
        "total_functions": total_functions,
        "total_classes": total_classes,
        "total_imports": total_imports,
        "unique_packages": len(all_packages),
        "top_packages": all_packages.most_common(10),
        "avg_loc_per_file": round(avg_loc_per_file, 1),
        "avg_functions_per_file": round(avg_functions_per_file, 1),
        "file_size_distribution": loc_distribution,
        "complexity_estimate": complexity,
        "files": results,
    }


def print_summary(analysis: Dict) -> None:
    """Print human-readable summary"""

    if "error" in analysis:
        print(f"\n❌ Error: {analysis['error']}")
        return

    print(f"\n📦 Codebase Complexity Estimate\n")
    print(f"Analyzed: {analysis['path']}")
    print(f"\n{'='*60}\n")

    # Overview
    print("## Overview")
    print(f"   Files: {analysis['total_files']}")
    print(f"   Total LOC: {analysis['total_loc']:,}")
    print(f"   Functions: {analysis['total_functions']}")
    print(f"   Classes: {analysis['total_classes']}")
    print(f"   Imports: {analysis['total_imports']}")
    print(f"   Unique packages: {analysis['unique_packages']}")

    # Averages
    print(f"\n## Averages")
    print(f"   LOC per file: {analysis['avg_loc_per_file']}")
    print(f"   Functions per file: {analysis['avg_functions_per_file']}")

    # File distribution
    print(f"\n## File Size Distribution")
    dist = analysis['file_size_distribution']
    print(f"   Small (< 100 LOC): {dist['small']}")
    print(f"   Medium (100-500 LOC): {dist['medium']}")
    print(f"   Large (500-1000 LOC): {dist['large']}")
    print(f"   Very Large (1000+ LOC): {dist['very_large']}")

    # Top packages
    if analysis['top_packages']:
        print(f"\n## Top Dependencies")
        for pkg, count in analysis['top_packages'][:5]:
            print(f"   {pkg}: {count} files")

    # Complexity estimate
    complexity = analysis['complexity_estimate']
    icon = {
        "Small": "🟢",
        "Medium": "🟡",
        "Large": "🟠",
        "Very Large": "🔴",
    }.get(complexity, "⚪")

    print(f"\n{'='*60}\n")
    print(f"{icon} Complexity Estimate: {complexity}")
    print(f"\n{'='*60}\n")

    # Guidance
    print("## Complexity Guidelines")
    if complexity == "Small":
        print("   ✅ Low complexity - Quick to implement")
        print("   ⏱️  Typical range: 1-3 days")
    elif complexity == "Medium":
        print("   ⚠️  Medium complexity - Moderate effort")
        print("   ⏱️  Typical range: 1-2 weeks")
    elif complexity == "Large":
        print("   🔶 High complexity - Significant effort")
        print("   ⏱️  Typical range: 1+ months")
    else:
        print("   🔴 Very high complexity - Major undertaking")
        print("   ⏱️  Typical range: Multiple months")

    print(f"\n{'='*60}\n")


def print_detailed_files(analysis: Dict, top_n: int = 10) -> None:
    """Print details about largest files"""

    if not analysis.get("files"):
        return

    print(f"\n## Largest Files (Top {top_n})\n")

    # Sort by LOC
    sorted_files = sorted(
        analysis["files"],
        key=lambda x: x["loc"],
        reverse=True
    )[:top_n]

    for i, file_data in enumerate(sorted_files, 1):
        rel_path = Path(file_data["file"]).name
        print(f"   {i}. {rel_path}")
        print(f"      LOC: {file_data['loc']}")
        print(f"      Functions: {file_data['functions']}")
        print(f"      Classes: {file_data['classes']}")
        print()


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python estimate_complexity.py <path>")
        print("\nExamples:")
        print("   # Analyze directory")
        print("   uv run python .claude/skills/explore/scripts/estimate_complexity.py app/")
        print("\n   # Analyze single file")
        print("   uv run python .claude/skills/explore/scripts/estimate_complexity.py app/main.py")
        sys.exit(1)

    path = Path(sys.argv[1])

    print(f"Analyzing: {path}")
    analysis = analyze_codebase(path)

    # Print summary
    print_summary(analysis)

    # Print detailed file list
    if analysis.get("files") and len(analysis["files"]) > 1:
        print_detailed_files(analysis)

    # Write JSON output
    output_path = Path("complexity-estimate.json")
    with open(output_path, "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"📄 Detailed results saved to: {output_path}\n")

    # Exit code based on complexity
    complexity = analysis.get("complexity_estimate", "Small")
    exit_codes = {
        "Small": 0,
        "Medium": 0,
        "Large": 1,
        "Very Large": 2,
    }
    sys.exit(exit_codes.get(complexity, 0))


if __name__ == "__main__":
    main()
