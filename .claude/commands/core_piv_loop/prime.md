# Prime Command

**Establish comprehensive codebase context before planning or implementation.**

---

## Purpose

The Prime command establishes a complete understanding of the codebase, its patterns, conventions, and current state BEFORE any planning or implementation work begins.

**Philosophy:** "Context is King" - Understanding the system prevents assumptions, reduces errors, and accelerates development.

---

## When to Use Prime

Use Prime at the beginning of:
- ✅ **New conversations** - Start with full context
- ✅ **Major features** - Understand before planning
- ✅ **Refactoring work** - Know what exists before changing
- ✅ **Bug investigation** - Understand the system state
- ✅ **Team onboarding** - Accelerate new developer ramp-up
- ✅ **After long breaks** - Refresh understanding of codebase

---

## Prime Process

### Step 1: Analyze Project Structure

```bash
# Enumerate all tracked files
git ls-files | head -100

# Visualize directory hierarchy (if tree installed)
find . -type d -maxdepth 3 ! -path "*/\.*" ! -path "*/node_modules/*" ! -path "*/venv_linux/*" | sort

# Count files by type
git ls-files | rg "\.(py|md|json|yaml|toml)$" | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

**Extract:**
- Project layout (app/, src/, tests/, docs/)
- Module organization (services, models, schemas, agents)
- Configuration locations (.env.example, pyproject.toml, configs/)
- Documentation structure (docs/, README.md, CLAUDE.md)

---

### Step 2: Read Core Documentation

```bash
# Priority order
1. CLAUDE.md - Development standards and conventions
2. README.md - Project overview and setup
3. .claude/PIV-LOOP.md - Development methodology
4. pyproject.toml - Dependencies and configuration
5. .env.example - Required environment variables
```

**For each document, note:**
- Core principles and philosophies
- Naming conventions
- Testing standards
- Quality thresholds
- Special requirements

---

### Step 3: Identify Key Files

**Entry Points:**
```bash
# Find main application entry point
rg "if __name__ == .__main__.:" --files-with-matches

# Find FastAPI app initialization
rg "FastAPI\(" --files-with-matches

# Find Lambda handlers
rg "@app.lambda_function" --files-with-matches -g "*.py"
```

**Data Models:**
```bash
# Find Pydantic models
rg "class.*BaseModel" --files-with-matches -g "*.py"

# Find type definitions
rg "^class.*:" app/ src/ | rg -v "def " | head -20
```

**Services:**
```bash
# Find service implementations
ls -la app/services/ src/services/ 2>/dev/null

# Find agent implementations
ls -la app/agents/ src/agents/ 2>/dev/null
```

**Tests:**
```bash
# Test structure
ls -la tests/

# Test count by type
find tests/unit -name "test_*.py" 2>/dev/null | wc -l
find tests/integration -name "test_*.py" 2>/dev/null | wc -l
find tests/e2e -name "test_*.py" 2>/dev/null | wc -l
```

---

### Step 4: Understand Current State

```bash
# Current branch and status
git branch --show-current
git status

# Recent commits (understand recent work)
git log -10 --oneline --decorate

# Active branches
git branch -a | head -10

# Uncommitted changes
git diff --stat
```

**Note:**
- Current feature work
- Recent changes
- Active development focus
- Any WIP indicators

---

### Step 5: Map Architecture

**Framework Patterns:**
```bash
# FastAPI routers
rg "APIRouter" --files-with-matches -g "*.py"

# Dependency injection
rg "Depends\(" --files-with-matches -g "*.py"

# Pydantic validators
rg "@validator|@field_validator" --files-with-matches -g "*.py"
```

**Data Flow:**
```bash
# Find request handlers
rg "@router\.(get|post|put|delete)" -A 2 -g "*.py" | head -30

# Find service calls
rg "Service\(\)" --files-with-matches -g "*.py"

# Find agent invocations
rg "invoke_agent|BedrockAgentService" --files-with-matches -g "*.py"
```

**External Integrations:**
```bash
# Find API clients
rg "httpx|requests" --files-with-matches -g "*.py"

# Find AWS service usage
rg "boto3|BedrockAgentService|SecretsManager" --files-with-matches -g "*.py"
```

**Testing Approach:**
```bash
# Read test README
cat tests/README.md 2>/dev/null | head -50

# Check pytest configuration
rg "\[tool.pytest" pyproject.toml -A 30

# Common test patterns
rg "@pytest.mark\." tests/ --no-filename | sort | uniq -c | sort -rn | head -15
```

---

### Step 6: Review Recent Plans

```bash
# List recent plans
ls -lt .agents/plans/*.md 2>/dev/null | head -5

# List recent execution reports
ls -lt .agents/execution-reports/*.md 2>/dev/null | head -5
```

**Extract patterns from recent work:**
- Implementation approaches
- Common gotchas
- Testing strategies
- Successful patterns

---

### Step 7: Identify Conventions

From CLAUDE.md and codebase analysis:

**Naming Conventions:**
- Variables/functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Database fields: Entity-specific primary keys (e.g., `session_id`, `lead_id`)

**File Organization:**
- Max 500 lines per file
- Functions under 100 lines
- Single responsibility per module
- Clear separation of concerns

**Testing Standards:**
- 80%+ code coverage required
- Unit tests in `tests/unit/`
- Integration tests in `tests/integration/`
- E2E tests in `tests/e2e/`
- Pytest markers for categorization

**Quality Standards:**
- Ruff for linting
- Mypy for type checking
- All tests must pass
- No secrets in code

---

## Output: Context Report

Generate a comprehensive context report saved to:
```
.agents/init-context/{project-name}-context-{YYYY-MM-DD}.md
```

### Report Template

```markdown
# {Project Name} Context Report

**Generated:** {Date and Time}
**Branch:** {Current Branch}
**Agent:** Claude Sonnet 4.5

---

## Project Overview

**Purpose:** {What the system does - from README}

**Version:** {From pyproject.toml}

**Technologies:**
- Language: Python {version}
- Frameworks: FastAPI, LangGraph, Pydantic v2
- AWS Services: Bedrock, Lambda, Secrets Manager
- Testing: pytest, pytest-asyncio, pytest-cov
- Tools: UV, ruff, mypy, SAM CLI

**Key Capabilities:**
- {List main features}

---

## Architecture

**Pattern:** {e.g., Event-driven, multi-agent workflow orchestration}

**Directory Structure:**
```
{project-root}/
├── app/                 # Main application code
│   ├── agents/         # LangGraph agents
│   ├── models/         # Pydantic models
│   ├── routes/         # FastAPI routes
│   ├── schemas/        # Request/response schemas
│   └── services/       # Business logic services
├── src/                # Source modules
├── tests/              # Test suite
│   ├── unit/          # Unit tests (no APIs)
│   ├── integration/   # Integration tests (with APIs)
│   └── e2e/           # End-to-end tests
├── docs/               # Documentation
├── configs/            # Configuration files
└── scripts/            # Utility scripts
```

**Data Flow:**
1. {Describe request flow}
2. {Service orchestration}
3. {Agent processing}
4. {Response generation}

---

## Tech Stack Details

**Core Dependencies:** (from pyproject.toml)
- langgraph >= {version} - Workflow orchestration
- fastapi >= {version} - Web framework
- pydantic >= {version} - Data validation
- boto3 >= {version} - AWS SDK
- httpx >= {version} - HTTP client

**Dev Dependencies:**
- pytest - Testing framework
- ruff - Linting and formatting
- mypy - Type checking
- aws-sam-cli - Local Lambda testing

---

## Core Principles (from CLAUDE.md)

**Development Philosophy:**
- KISS (Keep It Simple, Stupid)
- YAGNI (You Aren't Gonna Need It)
- Dependency Inversion
- Open/Closed Principle
- Single Responsibility
- Fail Fast

**Code Standards:**
- Line length: 100 characters
- File length: Max 500 lines
- Function length: Max 100 lines
- Coverage threshold: 80%

**Testing Strategy:**
- 3-tier: unit / integration / e2e
- Test-driven development encouraged
- Markers for categorization
- Fast tests in CI, slow tests on merge

---

## Current State

**Branch:** {branch name}

**Status:** {git status summary}

**Recent Work:** (last 10 commits)
```
{git log -10 --oneline}
```

**Recent Focus:** {Analysis of what's been worked on recently}

**Active Plans:**
{List any in-progress feature plans from .agents/plans/}

**Uncommitted Changes:**
{If any, summarize git diff --stat}

---

## Key Patterns Observed

### Database Naming
- Entity-specific primary keys: `session_id`, `lead_id`, `message_id`
- Foreign keys: `{referenced_entity}_id`
- Timestamps: `{action}_at` (created_at, updated_at)
- Booleans: `is_{state}` (is_active, is_connected)

### Repository Pattern
- BaseRepository with auto-derivation
- Convention-based table names
- Type-safe CRUD operations

### API Routes
- RESTful conventions
- Consistent parameter naming
- Router organization by feature
- Dependency injection for services

### Error Handling
- Custom exceptions per domain
- Specific exception handling
- Context managers for resources
- Structured logging

### Validation
- Pydantic v2 for all data models
- Field validators for business rules
- Settings management via pydantic-settings
- Type hints everywhere

---

## Testing Architecture

**Test Organization:**
- `tests/unit/` - {count} tests - Pure unit tests, < 1 second
- `tests/integration/` - {count} tests - API tests, 1-30 seconds
- `tests/e2e/` - {count} tests - Full workflows, > 30 seconds
- `tests/manual/` - Manual testing scripts (not in CI)

**Active Markers:**
- Speed: `fast`, `slow`, `very_slow`
- Services: `hubspot`, `bedrock`, `heron`, `alloy`
- Features: `flag_validation`, `business_risks`, `debt_validation`
- Dependencies: `requires_api`, `requires_secrets`

**Coverage:** {Current coverage %} (threshold: 80%)

---

## External Integrations

**APIs:**
- {List external APIs used}
- {Authentication methods}

**AWS Services:**
- {List AWS services used}
- {Configuration notes}

**Third-party Libraries:**
- {Key libraries and usage}

---

## Configuration Management

**Environment Variables:** (from .env.example)
- {List required env vars}
- {Where they're used}

**Secrets Management:**
- AWS Secrets Manager for production secrets
- .env file for local development

**Settings:**
- Pydantic BaseSettings for configuration
- Environment-specific configs in configs/

---

## Reference Documentation

**Available in `.claude/reference/`:**
- fastapi-best-practices.md
- pydantic-best-practices.md
- pytest-best-practices.md
- aws-lambda-best-practices.md
- security-best-practices.md
- uv-package-manager.md
- git-workflow.md
- rg-search-patterns.md

---

## Observations & Recommendations

**Strengths:**
- {What's working well}
- {Good patterns to continue}

**Areas of Note:**
- {Anything that stands out}
- {Potential improvements}

**Patterns to Follow:**
- {Specific examples from codebase}
- {Reference files and line numbers}

**Recent Changes:**
- {Notable recent commits}
- {New patterns introduced}

---

## Next Steps

Based on this context, you are now ready to:
1. Plan features using `/plan-feature {name}`
2. Review existing plans in `.agents/plans/`
3. Implement features using `/implement-plan {plan-file}`
4. Validate code using `/validate`

**Refer back to this context report** throughout development to ensure consistency with project conventions.
```

---

## Checklist

Before completing Prime, verify:

- [ ] Read CLAUDE.md completely
- [ ] Read README.md
- [ ] Analyzed directory structure
- [ ] Identified key files (entry points, models, services)
- [ ] Reviewed recent commits (last 10)
- [ ] Checked current branch and status
- [ ] Mapped architecture patterns
- [ ] Understood testing structure
- [ ] Reviewed recent plans (if any)
- [ ] Extracted naming conventions
- [ ] Generated context report
- [ ] Saved report to `.agents/init-context/`

---

## Tips

**For Large Codebases:**
- Focus on core modules first
- Sample files rather than reading everything
- Use `rg` for pattern discovery
- Prioritize recently modified files

**For Unfamiliar Domains:**
- Read domain-specific docs in `docs/`
- Look for design documents or architecture diagrams
- Review integration tests for usage examples
- Check `tests/test_config.py` for test data patterns

**For Active Development:**
- Check open PRs for in-flight work
- Review recent CHANGELOG.md entries
- Look for TODO or FIXME comments
- Understand current sprint/milestone goals

---

## Success Criteria

A successful Prime produces a context report that:

✅ **Comprehensive** - Covers all major aspects of the codebase
✅ **Actionable** - Provides specific file references and line numbers
✅ **Current** - Reflects the actual state of the code
✅ **Scannable** - Easy to reference during planning/implementation
✅ **Preserved** - Saved for future reference and onboarding

**Result:** You understand the codebase well enough to plan features that align with existing patterns and conventions.
