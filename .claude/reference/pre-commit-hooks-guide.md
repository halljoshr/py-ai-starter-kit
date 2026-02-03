# Pre-Commit and Pre-Push Hooks Reference Guide

This guide provides a comprehensive catalog of commands typically used in pre-commit and pre-push hooks across different programming ecosystems.

---

## Table of Contents

1. [Hook Strategy](#hook-strategy)
2. [Code Formatting](#code-formatting)
3. [Linting](#linting)
4. [Type Checking](#type-checking)
5. [Testing](#testing)
6. [Security Scanning](#security-scanning)
7. [Dependency Management](#dependency-management)
8. [Build Verification](#build-verification)
9. [File Validation](#file-validation)
10. [Documentation](#documentation)
11. [Best Practices](#best-practices)
12. [Example Configurations](#example-configurations)

---

## Hook Strategy

### Pre-Commit (< 10 seconds)
Fast, auto-fixable checks that provide immediate feedback:
- Code formatting with auto-fix
- Import sorting
- Trailing whitespace removal
- File syntax validation
- Quick linting with auto-fixes
- Secret detection

### Pre-Push (< 2 minutes)
More thorough checks before sharing code:
- Type checking
- Full linting without auto-fix
- Unit tests
- Security vulnerability scanning
- Build verification
- Dependency validation

### CI/CD Only (> 2 minutes)
Save slowest checks for continuous integration:
- Integration tests
- E2E tests
- Full security audits
- Release builds
- Comprehensive coverage reports

---

## Code Formatting

### Python

| Command | Purpose | Hook Type | Speed |
|---------|---------|-----------|-------|
| `ruff format .` | Fast formatter (Black-compatible) | Pre-commit | Fast |
| `ruff format --check .` | Check formatting without changes | Pre-push | Fast |
| `black .` | Opinionated code formatter | Pre-commit | Medium |
| `black --check .` | Validation mode | Pre-push | Medium |
| `isort .` | Import statement sorter | Pre-commit | Fast |
| `isort --check-only .` | Check import sorting | Pre-push | Fast |

**Recommended for this project:**
```bash
# Pre-commit: auto-fix
uv run ruff format .

# Pre-push: validate
uv run ruff format --check .
```

### JavaScript/TypeScript

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `prettier --write .` | Auto-format code | Pre-commit |
| `prettier --check .` | Validate formatting | Pre-push |
| `eslint --fix .` | Fix auto-fixable issues | Pre-commit |

### Go

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `gofmt -w .` | Standard Go formatter | Pre-commit |
| `goimports -w .` | Format + organize imports | Pre-commit |
| `go fmt ./...` | Format all packages | Pre-commit |

### Rust

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `cargo fmt` | Standard Rust formatter | Pre-commit |
| `cargo fmt -- --check` | Validate formatting | Pre-push |

### Other Languages

| Language | Command | Hook Type |
|----------|---------|-----------|
| Java | `google-java-format -i **/*.java` | Pre-commit |
| Ruby | `rubocop -a` | Pre-commit |
| Swift | `swift-format format -i -r .` | Pre-commit |
| Shell | `shfmt -w .` | Pre-commit |
| Terraform | `terraform fmt -recursive` | Pre-commit |

---

## Linting

### Python

| Command | Purpose | Hook Type | Speed |
|---------|---------|-----------|-------|
| `ruff check .` | Fast, comprehensive linter | Pre-commit | Fast |
| `ruff check --fix .` | Auto-fix issues | Pre-commit | Fast |
| `flake8 .` | Classic style checker | Pre-commit | Medium |
| `pylint src/` | Thorough static analyzer | Pre-push | Slow |
| `bandit -r .` | Security linter | Pre-push | Medium |

**Recommended for this project:**
```bash
# Pre-commit: fix automatically
uv run ruff check --fix .

# Pre-push: strict validation
uv run ruff check .
```

### JavaScript/TypeScript

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `eslint .` | Pluggable linter | Pre-commit |
| `eslint . --max-warnings 0` | Strict mode | Pre-push |
| `biome check .` | Fast all-in-one tool | Pre-commit |

### Go

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `golangci-lint run` | Meta-linter (recommended) | Pre-commit/Pre-push |
| `go vet ./...` | Built-in code analysis | Pre-commit |
| `staticcheck ./...` | Advanced static analyzer | Pre-push |

### Rust

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `cargo clippy` | Rust linter | Pre-commit |
| `cargo clippy -- -D warnings` | Strict mode | Pre-push |

### Java

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `mvn checkstyle:check` | Style checker (Maven) | Pre-commit |
| `./gradlew checkstyleMain` | Style checker (Gradle) | Pre-commit |
| `mvn pmd:check` | Code analyzer (Maven) | Pre-push |

---

## Type Checking

### Python

| Command | Purpose | Hook Type | Speed |
|---------|---------|-----------|-------|
| `mypy .` | Static type checker | Pre-push | Medium |
| `mypy . --strict` | Strict type checking | Pre-push | Medium |
| `pyright` | Microsoft's type checker | Pre-push | Fast |

**Recommended for this project:**
```bash
# Pre-push: type validation
uv run mypy app/ src/
```

### JavaScript/TypeScript

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `tsc --noEmit` | Type checking only | Pre-push |
| `tsc --build --dry-run` | Build validation | Pre-push |

**Note:** Type checking is built into compilation for Go, Rust, Java, etc.

---

## Testing

### Python - Unit Tests

| Command | Purpose | Hook Type | Speed |
|---------|---------|-----------|-------|
| `pytest tests/unit/ -v` | Run unit tests | Pre-push | Fast |
| `pytest tests/unit/ --maxfail=1` | Stop on first failure | Pre-commit | Very Fast |
| `pytest -m "not slow"` | Skip slow tests | Pre-commit | Fast |
| `pytest --lf` | Run last failed tests | Pre-commit | Very Fast |

**Recommended for this project:**
```bash
# Pre-commit: quick feedback (optional)
uv run pytest tests/unit/ --maxfail=1 -q

# Pre-push: full unit test suite
uv run pytest tests/unit/ -v
```

### Python - Integration Tests

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `pytest tests/integration/ -m "not very_slow"` | Fast integration tests | Pre-push |
| `pytest tests/integration/ -v` | All integration tests | CI only |

**Recommended for this project:**
```bash
# Pre-push: fast integration tests only
uv run pytest tests/integration/ -m "not very_slow" -v
```

### JavaScript/TypeScript

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `jest --onlyChanged` | Test changed files only | Pre-commit |
| `npm test` | Full test suite | Pre-push |
| `vitest run` | Fast test runner | Pre-push |

### Go

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `go test -short ./...` | Skip long tests | Pre-commit |
| `go test ./...` | Run all tests | Pre-push |
| `go test -race ./...` | Race detection | Pre-push |

### Rust

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `cargo test --lib` | Library tests only | Pre-commit |
| `cargo test` | All tests | Pre-push |

### Java

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `mvn test -Dtest=UnitTest*` | Unit tests only | Pre-commit |
| `mvn test` | All tests | Pre-push |
| `./gradlew test` | Run tests (Gradle) | Pre-push |

---

## Security Scanning

### Secret Detection

| Command | Purpose | Hook Type | Ecosystem |
|---------|---------|-----------|-----------|
| `gitleaks detect --no-git` | Detect secrets | Pre-commit | Universal |
| `trufflehog filesystem .` | Find secrets | Pre-commit | Universal |
| `detect-secrets scan` | Secret scanner | Pre-commit | Universal |

**Critical:** Always run secret detection in pre-commit to prevent credential leaks.

### Dependency Vulnerability Scanning

#### Python
| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `safety check` | Python dependency scanner | Pre-push |
| `pip-audit` | Python package auditor | Pre-push |
| `bandit -r .` | Security linter | Pre-push |

**Recommended for this project:**
```bash
# Pre-push: security checks
uv run bandit -r app/ src/
uv run pip-audit
```

#### JavaScript/TypeScript
| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `npm audit` | Vulnerability scanner | Pre-push |
| `yarn audit` | Yarn vulnerability scanner | Pre-push |
| `pnpm audit` | PNPM vulnerability scanner | Pre-push |

#### Other Languages
| Language | Command | Hook Type |
|----------|---------|-----------|
| Rust | `cargo audit` | Pre-push |
| Go | `go list -json -m all \| nancy sleuth` | Pre-push |
| Java | `mvn dependency:check` | Pre-push |

### Multi-Language Security

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `snyk test` | Multi-language scanner | Pre-push |
| `semgrep --config=auto` | SAST tool | Pre-push |

---

## Dependency Management

### Python

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `uv sync --check` | Check dependency sync | Pre-commit |
| `pip check` | Verify dependencies | Pre-push |
| `poetry check` | Validate pyproject.toml | Pre-commit |

**Recommended for this project:**
```bash
# Pre-commit: ensure sync
uv sync --check
```

### JavaScript/TypeScript

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `npm ls` | List dependencies | Pre-push |
| `depcheck` | Find unused dependencies | Pre-push |

### Go

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `go mod tidy` | Clean up go.mod | Pre-commit |
| `go mod verify` | Verify dependencies | Pre-push |

### Rust

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `cargo check` | Check compilation | Pre-commit |

---

## Build Verification

### Python

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `python -m compileall .` | Compile all .py files | Pre-push |
| `python -m py_compile file.py` | Compile single file | Pre-commit |
| `python -m build` | Build wheel/sdist | Pre-push |

**Recommended for this project:**
```bash
# Pre-push: syntax validation
python -m compileall app/ src/
```

### JavaScript/TypeScript

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `npm run build` | Build project | Pre-push |
| `tsc --build` | TypeScript compilation | Pre-push |
| `vite build` | Production build | Pre-push |

### Go

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `go build ./...` | Build all packages | Pre-push |
| `go build -o /dev/null ./...` | Validate only | Pre-push |

### Rust

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `cargo check` | Fast build check | Pre-commit |
| `cargo build` | Debug build | Pre-push |
| `cargo build --release` | Release build | CI only |

### Java

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `mvn compile` | Compile source | Pre-push |
| `./gradlew build` | Full build | Pre-push |

---

## File Validation

### Syntax Validation

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `check-yaml` | Validate YAML | Pre-commit |
| `check-json` | Validate JSON | Pre-commit |
| `check-toml` | Validate TOML | Pre-commit |
| `yamllint .` | YAML linter | Pre-commit |

**Recommended for this project:**
```bash
# Pre-commit: validate config files
check-yaml
check-toml
```

### Whitespace & Line Endings

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `trailing-whitespace` | Remove trailing spaces | Pre-commit |
| `end-of-file-fixer` | Ensure newline at EOF | Pre-commit |
| `mixed-line-ending` | Normalize line endings | Pre-commit |
| `check-merge-conflict` | Detect merge markers | Pre-commit |

### File Safety

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `check-added-large-files` | Prevent large files | Pre-commit |
| `detect-private-key` | Detect SSH keys | Pre-commit |
| `detect-aws-credentials` | Detect AWS creds | Pre-commit |

---

## Documentation

| Command | Purpose | Hook Type |
|---------|---------|-----------|
| `markdownlint **/*.md` | Markdown linter | Pre-commit |
| `vale .` | Prose linter | Pre-commit |
| `typos` | Spell checker | Pre-commit |
| `cspell **/*.{py,md}` | Code spell checker | Pre-commit |
| `doctoc README.md` | Generate TOC | Pre-commit |

**Recommended for this project:**
```bash
# Pre-commit: documentation quality
markdownlint **/*.md
typos
```

---

## Best Practices

### Performance Optimization

1. **Keep pre-commit fast** (< 10 seconds)
   - Only auto-fixable checks
   - Use `--check` modes in pre-push
   - Cache aggressively

2. **Run only on changed files**
   - Use pre-commit framework's file filtering
   - `git diff --cached --name-only` for manual filtering

3. **Parallelize independent checks**
   - Most hook frameworks support parallel execution
   - Group by similar execution time

4. **Use fast tools**
   - `ruff` instead of `black` + `flake8` + `isort`
   - `biome` instead of `eslint` + `prettier`
   - Native tools over Python-based alternatives

### Hook Management

1. **Document skip procedures**
   ```bash
   # Skip all hooks (emergencies only)
   git commit --no-verify

   # Skip specific hook
   SKIP=mypy git commit
   ```

2. **Version control your hooks**
   - Use `.pre-commit-config.yaml`
   - Pin tool versions for reproducibility

3. **Test hooks in CI**
   - Run same checks in CI pipeline
   - Catch issues if hooks are skipped

4. **Update regularly**
   ```bash
   pre-commit autoupdate
   ```

### Hook Composition

#### Minimal Pre-Commit (< 5 seconds)
```bash
ruff format .
ruff check --fix .
check-yaml
detect-private-key
```

#### Standard Pre-Commit (< 10 seconds)
```bash
ruff format .
ruff check --fix .
check-yaml
check-toml
trailing-whitespace
end-of-file-fixer
gitleaks detect --no-git
```

#### Comprehensive Pre-Push (< 2 minutes)
```bash
ruff format --check .
ruff check .
mypy app/ src/
pytest tests/unit/ -v
python -m compileall app/ src/
bandit -r app/ src/
pip-audit
```

---

## Example Configurations

### Python Project (Recommended for this repository)

#### `.pre-commit-config.yaml`

```yaml
repos:
  # Universal file checks
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key
      - id: check-merge-conflict

  # Security - secret detection
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.1
    hooks:
      - id: gitleaks

  # Python - formatting and linting (ruff)
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.9
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format

  # Python - type checking (pre-push only)
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        args: [--strict]
        additional_dependencies: [types-requests]
        stages: [push]

  # Python - security linting (pre-push only)
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [-r, app/, src/]
        stages: [push]

  # Python - tests (pre-push only)
  - repo: local
    hooks:
      - id: pytest-unit
        name: pytest (unit tests)
        entry: uv run pytest tests/unit/ -v
        language: system
        pass_filenames: false
        stages: [push]

      - id: pytest-integration-fast
        name: pytest (fast integration tests)
        entry: uv run pytest tests/integration/ -m "not very_slow" -v
        language: system
        pass_filenames: false
        stages: [push]

  # Documentation
  - repo: https://github.com/markdownlint/markdownlint
    rev: v0.12.0
    hooks:
      - id: markdownlint
        args: [--fix]
```

#### Installation and Usage

```bash
# Install pre-commit
uv add --dev pre-commit

# Install hooks
uv run pre-commit install

# Install pre-push hooks
uv run pre-commit install --hook-type pre-push

# Run manually on all files
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run ruff --all-files

# Update hook versions
uv run pre-commit autoupdate

# Skip hooks (emergency only)
git commit --no-verify
```

### Manual Hook Scripts (Alternative)

If not using the pre-commit framework, you can create manual scripts:

#### `.git/hooks/pre-commit`

```bash
#!/bin/bash
set -e

echo "Running pre-commit checks..."

# Fast checks only (< 10 seconds total)
echo "→ Formatting with ruff..."
uv run ruff format .

echo "→ Linting with ruff (auto-fix)..."
uv run ruff check --fix .

echo "→ Checking for secrets..."
gitleaks detect --no-git

echo "→ Validating file formats..."
check-yaml
check-toml

echo "✓ Pre-commit checks passed!"
```

#### `.git/hooks/pre-push`

```bash
#!/bin/bash
set -e

echo "Running pre-push checks..."

# More thorough checks (< 2 minutes total)
echo "→ Validating formatting..."
uv run ruff format --check .

echo "→ Running linter..."
uv run ruff check .

echo "→ Type checking..."
uv run mypy app/ src/

echo "→ Running unit tests..."
uv run pytest tests/unit/ -v

echo "→ Running fast integration tests..."
uv run pytest tests/integration/ -m "not very_slow" -v

echo "→ Security scanning..."
uv run bandit -r app/ src/

echo "→ Checking dependencies..."
uv run pip-audit

echo "→ Validating Python syntax..."
python -m compileall app/ src/

echo "✓ Pre-push checks passed!"
```

Make scripts executable:
```bash
chmod +x .git/hooks/pre-commit
chmod +x .git/hooks/pre-push
```

---

## Integration with CI/CD

Your pre-commit and pre-push hooks should mirror CI checks:

```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Install uv
        run: curl -LsSf https://astral.sh/uv/install.sh | sh

      - name: Install dependencies
        run: uv sync

      - name: Run pre-commit checks
        run: uv run pre-commit run --all-files

      - name: Run tests with coverage
        run: uv run pytest --cov=app --cov=src --cov-fail-under=80
```

---

## Summary

### For This Python Project

**Recommended Pre-Commit Checks (< 10 seconds):**
- `ruff format .` - Auto-format code
- `ruff check --fix .` - Auto-fix linting issues
- File validation (YAML, TOML, whitespace)
- Secret detection (`gitleaks`)

**Recommended Pre-Push Checks (< 2 minutes):**
- `ruff format --check .` - Validate formatting
- `ruff check .` - Full linting
- `mypy app/ src/` - Type checking
- `pytest tests/unit/ -v` - Unit tests
- `pytest tests/integration/ -m "not very_slow" -v` - Fast integration tests
- `bandit -r app/ src/` - Security scanning
- `pip-audit` - Dependency vulnerabilities
- `python -m compileall app/ src/` - Syntax validation

**Skip for CI Only (> 2 minutes):**
- Full integration test suite
- E2E tests
- Coverage reports
- Full security audits

---

_This guide should be updated as new tools and patterns emerge in the development ecosystem._
