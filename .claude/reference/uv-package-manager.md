# UV Package Manager

Quick reference for UV package manager commands.

---

## Basic Commands

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Sync dependencies from pyproject.toml
uv sync

# Add package
uv add requests

# Add dev dependency
uv add --dev pytest ruff mypy

# Remove package
uv remove requests

# Run command in environment
uv run python script.py
uv run pytest
uv run ruff check .

# Install specific Python version
uv python install 3.12
```

---

## Dependency Management

### Adding Dependencies

```bash
# ✅ GOOD: Use uv add (updates pyproject.toml and uv.lock)
uv add httpx pydantic

# ❌ BAD: Never edit pyproject.toml directly
# Manually editing can cause lock file inconsistencies
```

### Updating Dependencies

```bash
# Update all dependencies
uv sync --upgrade

# Update specific package
uv add httpx --upgrade
```

---

## Lock File

**uv.lock** is the lock file (like package-lock.json or poetry.lock)

- ✅ Commit uv.lock to repository
- ✅ Ensures reproducible installs
- ❌ Don't edit manually

---

## Virtual Environments

```bash
# Create venv
uv venv

# Activate (if needed for IDEs)
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Run without activating
uv run python script.py
```

**In this project:** Use `venv_linux` virtual environment.

---

## Common Workflows

### Starting New Feature

```bash
# Sync dependencies
uv sync

# Run tests to verify baseline
uv run pytest
```

### Adding New Dependency

```bash
# Add package
uv add new-package

# Sync
uv sync

# Test
uv run pytest
```

### Running Tests

```bash
# All tests
uv run pytest

# Specific test file
uv run pytest tests/unit/test_service.py -v

# With coverage
uv run pytest --cov=app --cov=src
```

---

## CI/CD Integration

```yaml
# GitHub Actions
- name: Install UV
  run: curl -LsSf https://astral.sh/uv/install.sh | sh

- name: Sync dependencies
  run: uv sync

- name: Run tests
  run: uv run pytest
```

---

## Troubleshooting

### "Package not found"
```bash
uv sync  # Re-sync dependencies
```

### "Import error"
```bash
uv run python  # Make sure using uv run
```

### "Lock file out of sync"
```bash
uv lock  # Regenerate lock file
uv sync  # Sync dependencies
```

---

## Best Practices

✅ **DO:**
- Use `uv add` to add packages
- Commit uv.lock
- Use `uv run` for commands
- Sync before starting work

❌ **DON'T:**
- Edit pyproject.toml dependencies directly
- Delete uv.lock
- Use pip install (use uv add)
- Activate venv manually (use uv run)

---

## References

- [UV Documentation](https://github.com/astral-sh/uv)
- [UV Guide](https://docs.astral.sh/uv/)
