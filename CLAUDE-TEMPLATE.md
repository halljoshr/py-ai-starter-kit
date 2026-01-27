# CLAUDE.md Template

This template shows which sections to customize for each new project.

**Legend:**
- 🔄 **CUSTOMIZE** - Change for each project
- ✅ **STANDARD** - Keep the same across projects

---

## 🔄 CUSTOMIZE: Project Overview

```markdown
## Project Overview

**[Project Name]** - [Brief description of what this project does]

[Optional: Note about project purpose, e.g., "test case for X", "production system for Y"]
```

**Example:**
```markdown
**Analytics Pipeline** - High-volume event analytics system designed to ingest,
aggregate, and query 10M+ rows of event data with performant APIs.

This project is a **test case for PIV-Swarm workflow** at scale.
```

---

## ✅ STANDARD: Core Development Philosophy

Keep this section identical across all projects:
- KISS
- YAGNI
- Design Principles

---

## ✅ STANDARD: Development Methodology

Keep the PIV-Swarm or PIV Loop section standard, just update the skill list if needed.

---

## ✅ STANDARD: Code Structure & Modularity

Keep rules the same:
- 500 line file limit
- 100 line function limit
- 100 char line length

---

## ✅ STANDARD: Development Environment

Keep UV commands and patterns the same.

## 🔄 CUSTOMIZE: Development Commands

Update the example commands for project specifics:

```markdown
### Development Commands

```bash
# Run server (if applicable)
uv run uvicorn src.main:app --reload

# Run all tests
uv run pytest

# 🔄 ADD PROJECT-SPECIFIC COMMANDS HERE
# Generate test data
uv run python -m src.generators.fake_data --rows 10000000

# Run migrations
uv run alembic upgrade head
```
```

---

## ✅ STANDARD: Style & Conventions

Keep all style rules the same:
- PEP8
- Type hints
- Naming conventions
- Ruff, mypy

---

## 🔄 CUSTOMIZE: Testing Strategy

**Keep structure the same** (unit/integration/e2e tiers)

**Customize:**
- Test directory names if different
- Add performance/load test tier if needed
- Update coverage paths (`--cov=src` vs `--cov=app`)

Example additions:
```markdown
#### Performance Tests (`tests/performance/`)
- **Purpose:** Test system under load (10M rows)
- **Speed:** > 30 seconds
- **When to Run:** Before merge to main
```

---

## ✅ STANDARD: Git Workflow

Keep branch strategy and commit format the same.

---

## ✅ STANDARD: Reference Documentation

Keep the entire table the same - these docs are project-agnostic.

---

## 🔄 CUSTOMIZE: Project-Specific Sections

Add sections unique to this project:

### Examples:

#### For Analytics Pipeline:
```markdown
## 🎯 Analytics Pipeline Specifics

### Performance Targets
| Operation | Target |
|-----------|--------|
| Single event insert | < 10ms |
| Batch insert (10K) | < 1s |

### Event Types
- `page_view` - Page visits
- `click` - UI interactions
```

#### For E-commerce:
```markdown
## 🛒 E-commerce Specifics

### Payment Providers
- Stripe (primary)
- PayPal (secondary)

### Order States
1. pending → 2. paid → 3. fulfilled → 4. completed
```

#### For SaaS API:
```markdown
## 🔐 Multi-tenancy

### Tenant Isolation
- Database: Schema per tenant
- Caching: Tenant-prefixed keys
- Auth: Tenant ID in JWT claims
```

---

## ✅ STANDARD: Important Notes

Keep the warnings the same.

---

## ✅ STANDARD: Search Command Requirements

Keep rg/ripgrep requirements the same.

---

## 🔄 CUSTOMIZE: Directory Structure

Update the ASCII tree to match your actual project structure:

```markdown
## 📁 Directory Structure

```
src/                     # 🔄 Main source directory
├── main.py              # 🔄 Entry point
├── api/                 # 🔄 Your modules
│   ├── [routes].py
│   └── ...
├── models/              # 🔄 Your models
├── services/            # 🔄 Your services
└── [custom dirs]/       # 🔄 Project-specific

tests/                   # ✅ Standard structure
├── unit/
├── integration/
└── [performance]/       # 🔄 Optional

.agents/                 # ✅ Standard PIV-Swarm
├── state/
├── tasks/
├── plans/
└── research/

.claude/                 # ✅ Standard
├── skills/
├── reference/
└── settings.json
```
```

---

## Quick Checklist for New Projects

When creating CLAUDE.md for a new project:

- [ ] Update Project Overview with project name and description
- [ ] Add project-specific development commands
- [ ] Add performance/load test tier if applicable
- [ ] Update coverage paths in pytest commands
- [ ] Add project-specific sections (Performance Targets, Domain Models, etc.)
- [ ] Update directory structure ASCII tree
- [ ] Add any domain-specific event types, states, or workflows
- [ ] Add technology-specific notes (database, caching, queue system)
- [ ] Keep all standard sections unchanged (philosophy, conventions, reference table)

---

## Sections Summary

| Section | Status | Notes |
|---------|--------|-------|
| Project Overview | 🔄 CUSTOMIZE | Name, description, purpose |
| Core Philosophy | ✅ STANDARD | KISS, YAGNI, principles |
| Methodology | ✅ STANDARD | PIV-Swarm workflow |
| Code Structure | ✅ STANDARD | File/function limits |
| Development Env | ✅ STANDARD | UV commands |
| Development Commands | 🔄 CUSTOMIZE | Add project-specific commands |
| Style & Conventions | ✅ STANDARD | PEP8, naming, type hints |
| Testing Strategy | 🔄 CUSTOMIZE | Add custom test tiers, update paths |
| Git Workflow | ✅ STANDARD | Branches, commits |
| Reference Docs | ✅ STANDARD | Same table every project |
| Project Specifics | 🔄 CUSTOMIZE | Performance, domain models, tech stack |
| Important Notes | ✅ STANDARD | Warnings, best practices |
| Search Commands | ✅ STANDARD | rg/ripgrep usage |
| Directory Structure | 🔄 CUSTOMIZE | Match actual project layout |

---

## Example: Copy-Paste Starting Point

When starting a new project, copy from the template and search for "🔄" markers to know what needs updating.
