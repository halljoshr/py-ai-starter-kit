#!/usr/bin/env python3
"""
Code complexity analysis script for /code-review skill

Analyzes Python code for complexity metrics:
- Cyclomatic complexity
- Function length
- File length
- Import count

Usage:
    uv run python .claude/skills/code-review/scripts/analyze_complexity.py <path>

Returns:
    JSON with complexity metrics and warnings
"""

import ast
import json
import sys
from pathlib import Path
from typing import Dict, List


def calculate_cyclomatic_complexity(node: ast.FunctionDef) -> int:
    """
    Calculate cyclomatic complexity for a function

    Cyclomatic complexity = number of decision points + 1
    Decision points: if, for, while, except, with, and, or, etc.
    """
    complexity = 1  # Base complexity

    for child in ast.walk(node):
        # Decision points
        if isinstance(child, (ast.If, ast.For, ast.While, ast.With)):
            complexity += 1
        elif isinstance(child, ast.ExceptHandler):
            complexity += 1
        elif isinstance(child, ast.BoolOp):
            # 'and'/'or' operators
            complexity += len(child.values) - 1

    return complexity


def analyze_function(func: ast.FunctionDef, source_lines: List[str]) -> Dict:
    """Analyze a single function for complexity metrics"""

    # Get function source lines
    start_line = func.lineno
    end_line = func.end_lineno or start_line
    func_lines = end_line - start_line + 1

    # Calculate cyclomatic complexity
    complexity = calculate_cyclomatic_complexity(func)

    # Determine severity
    if complexity > 15:
        severity = "high"
        message = f"Very complex function (complexity: {complexity}). Consider refactoring."
    elif complexity > 10:
        severity = "medium"
        message = f"Complex function (complexity: {complexity}). May benefit from refactoring."
    elif func_lines > 100:
        severity = "medium"
        message = f"Long function ({func_lines} lines). Consider breaking into smaller functions."
    else:
        severity = "ok"
        message = None

    return {
        "name": func.name,
        "start_line": start_line,
        "end_line": end_line,
        "length": func_lines,
        "complexity": complexity,
        "severity": severity,
        "message": message,
    }


def analyze_file(file_path: Path) -> Dict:
    """Analyze a single Python file"""

    try:
        source = file_path.read_text()
        source_lines = source.splitlines()
        tree = ast.parse(source, filename=str(file_path))
    except SyntaxError as e:
        return {
            "file": str(file_path),
            "error": f"Syntax error: {e}",
            "skipped": True,
        }
    except Exception as e:
        return {
            "file": str(file_path),
            "error": f"Parse error: {e}",
            "skipped": True,
        }

    # Count imports
    imports = sum(1 for node in ast.walk(tree) if isinstance(node, (ast.Import, ast.ImportFrom)))

    # Analyze functions
    functions = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            func_analysis = analyze_function(node, source_lines)
            functions.append(func_analysis)

    # File metrics
    total_lines = len(source_lines)
    file_warnings = []

    if total_lines > 500:
        file_warnings.append({
            "severity": "high",
            "message": f"File is {total_lines} lines (max 500). Consider splitting into modules.",
        })

    if imports > 20:
        file_warnings.append({
            "severity": "medium",
            "message": f"File has {imports} imports. May indicate tight coupling.",
        })

    # Aggregate severity
    high_complexity = [f for f in functions if f["severity"] == "high"]
    medium_complexity = [f for f in functions if f["severity"] == "medium"]

    if high_complexity or file_warnings:
        file_severity = "high"
    elif medium_complexity:
        file_severity = "medium"
    else:
        file_severity = "ok"

    return {
        "file": str(file_path),
        "total_lines": total_lines,
        "num_functions": len(functions),
        "num_imports": imports,
        "functions": functions,
        "warnings": file_warnings,
        "severity": file_severity,
    }


def analyze_codebase(path: Path) -> Dict:
    """Analyze entire codebase starting from path"""

    if path.is_file():
        # Single file
        files = [path]
    else:
        # Directory - find all .py files
        files = list(path.rglob("*.py"))
        # Filter out venv, .tox, etc.
        files = [
            f for f in files
            if "venv" not in f.parts
            and ".tox" not in f.parts
            and "__pycache__" not in f.parts
        ]

    results = []
    for file_path in files:
        file_result = analyze_file(file_path)
        results.append(file_result)

    # Aggregate statistics
    total_files = len(results)
    high_severity = [r for r in results if r.get("severity") == "high"]
    medium_severity = [r for r in results if r.get("severity") == "medium"]
    ok_files = [r for r in results if r.get("severity") == "ok"]
    skipped = [r for r in results if r.get("skipped")]

    return {
        "total_files": total_files,
        "high_severity_files": len(high_severity),
        "medium_severity_files": len(medium_severity),
        "ok_files": len(ok_files),
        "skipped_files": len(skipped),
        "files": results,
    }


def print_summary(analysis: Dict) -> None:
    """Print human-readable summary"""

    print(f"\n📊 Complexity Analysis Summary\n")
    print(f"Total files analyzed: {analysis['total_files']}")
    print(f"  🔴 High complexity: {analysis['high_severity_files']}")
    print(f"  🟡 Medium complexity: {analysis['medium_severity_files']}")
    print(f"  ✅ OK: {analysis['ok_files']}")

    if analysis['skipped_files']:
        print(f"  ⚠️  Skipped: {analysis['skipped_files']}")

    # Show high severity files
    high_files = [f for f in analysis['files'] if f.get('severity') == 'high']
    if high_files:
        print(f"\n🔴 High Complexity Files:\n")
        for file_data in high_files:
            print(f"   {file_data['file']}")

            # Show file warnings
            for warning in file_data.get('warnings', []):
                print(f"      - {warning['message']}")

            # Show high complexity functions
            high_funcs = [f for f in file_data.get('functions', []) if f['severity'] == 'high']
            for func in high_funcs:
                print(f"      - {func['name']}() at line {func['start_line']}: {func['message']}")
            print()

    # Recommendations
    if high_files or analysis['medium_severity_files']:
        print("\n💡 Recommendations:")
        print("   - Refactor complex functions (complexity > 10)")
        print("   - Break long files into smaller modules (< 500 lines)")
        print("   - Extract helper functions from large functions")
        print("   - Consider using classes to group related functions")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_complexity.py <path>")
        print("\nExamples:")
        print("   # Analyze single file")
        print("   uv run python .claude/skills/code-review/scripts/analyze_complexity.py app/services/user.py")
        print("\n   # Analyze directory")
        print("   uv run python .claude/skills/code-review/scripts/analyze_complexity.py app/")
        sys.exit(1)

    path = Path(sys.argv[1])

    if not path.exists():
        print(f"Error: Path does not exist: {path}")
        sys.exit(1)

    print(f"Analyzing: {path}")
    analysis = analyze_codebase(path)

    # Print summary
    print_summary(analysis)

    # Write JSON output
    output_path = Path("complexity-analysis.json")
    with open(output_path, "w") as f:
        json.dump(analysis, f, indent=2)

    print(f"\n📄 Detailed results saved to: {output_path}")

    # Exit code based on severity
    if analysis['high_severity_files'] > 0:
        sys.exit(2)  # High complexity found
    elif analysis['medium_severity_files'] > 0:
        sys.exit(1)  # Medium complexity found
    else:
        sys.exit(0)  # All OK


if __name__ == "__main__":
    main()
