# ripgrep (rg) Search Patterns

Why and how to use ripgrep over grep/find.

---

## Why ripgrep?

**Performance:**
- 10-100x faster than grep
- Respects .gitignore automatically
- Smart defaults (skip binary files, etc.)

**Better UX:**
- Colored output
- Better readability
- Simpler syntax

---

## Basic Usage

```bash
# Search for pattern
rg "pattern"

# Case insensitive
rg -i "pattern"

# Whole word only
rg -w "function_name"
```

---

## File Filtering

```bash
# By file type
rg "pattern" -t py        # Python files only
rg "pattern" -t js        # JavaScript files
rg "pattern" -T test      # Exclude test files

# By glob
rg "pattern" -g "*.py"
rg "pattern" -g "!test_*"  # Exclude test files
```

---

## Output Modes

```bash
# Show matching lines (default)
rg "pattern"

# Show only filenames
rg "pattern" -l
rg "pattern" --files-with-matches

# Show count per file
rg "pattern" -c
rg "pattern" --count
```

---

## Context Lines

```bash
# Show 3 lines after match
rg "pattern" -A 3

# Show 3 lines before match
rg "pattern" -B 3

# Show 3 lines before and after
rg "pattern" -C 3
```

---

## Common Patterns

### Find Class Definitions

```bash
rg "^class \w+\(BaseModel\)" -t py
```

### Find Function Calls

```bash
rg "get_secret\(" -t py
```

### Find TODO Comments

```bash
rg "TODO|FIXME" -t py
```

### Find Imports

```bash
rg "^from fastapi import" -t py
```

### Find API Keys (security audit)

```bash
rg "(api_key|secret|password|token)" --ignore-case
```

---

## Replacement for find

```bash
# ❌ OLD: find -name
find . -name "*.py"

# ✅ NEW: rg --files
rg --files -g "*.py"

# ❌ OLD: find with grep
find . -name "*.py" -exec grep "pattern" {} \;

# ✅ NEW: rg (does this automatically)
rg "pattern" -t py
```

---

## Multiline Search

```bash
# Search across multiple lines
rg -U "pattern.*\n.*other_pattern"

# Multiline with context
rg -U "class.*:.*\n.*def" -A 5
```

---

## Practical Examples

### Find All Services

```bash
rg "class \w+Service" app/services/ -l
```

### Find All Routes

```bash
rg "@router\.(get|post|put|delete)" app/routes/
```

### Find Pydantic Validators

```bash
rg "@field_validator" -t py
```

### Find Async Functions

```bash
rg "async def" -t py -l
```

### Find Test Markers

```bash
rg "@pytest.mark\.\w+" tests/ --no-filename | sort | uniq -c
```

---

## Performance Tips

```bash
# Limit search to specific directories
rg "pattern" app/ tests/

# Use file type filters
rg "pattern" -t py  # Faster than -g "*.py"

# Limit results
rg "pattern" | head -20
```

---

## Integration with Other Tools

```bash
# Pipe to other commands
rg "pattern" -l | xargs wc -l

# Count unique matches
rg "import \w+" --no-filename | sort | uniq -c

# Find and edit
rg "pattern" -l | xargs vim
```

---

## Best Practices

✅ **DO:**
- Use `rg` instead of `grep`
- Use `-t` for file type filtering
- Use `-l` to list files only
- Let rg respect .gitignore

❌ **DON'T:**
- Use `find` + `grep` (use `rg`)
- Search without file type filters (slower)
- Ignore .gitignore (rg respects it automatically)

---

## Common Aliases

```bash
# Add to ~/.bashrc or ~/.zshrc
alias rgpy="rg -t py"           # Search Python files
alias rgjs="rg -t js"           # Search JavaScript files
alias rgtest="rg -g '*test*.py'" # Search test files
```

---

## References

- [ripgrep Documentation](https://github.com/BurntSushi/ripgrep)
- [ripgrep User Guide](https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md)
