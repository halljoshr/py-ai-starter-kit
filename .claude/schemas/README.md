# Decision Schemas

**Purpose:** Provide smart defaults to skills, reducing unnecessary questions and improving decision quality.

## Philosophy

Instead of asking 35 questions during `/discuss`, skills read these schemas and apply heuristics:

- **Auto-apply** when context is clear (e.g., "prototype" → SQLite)
- **Ask only** when genuinely ambiguous
- **Provide context** from schemas in questions

**Result:** Question volume reduced by 70% (35 → ~10)

## How Skills Use Schemas

### Example: /discuss skill

```markdown
## Step 1: Load Decision Context

Read schemas for this domain:
```bash
cat .claude/schemas/database-decisions.yaml
cat .claude/schemas/api-patterns.yaml
cat .claude/schemas/architecture-patterns.yaml
```

Apply smart defaults:
- If project type = "prototype" → use SQLite (don't ask)
- If project type = "production" + "scale" → use PostgreSQL (don't ask)
- If ambiguous → ask with context from schema

Only ask questions not covered by schemas.
```

### Example: /explore skill

```markdown
## Step 3: Feasibility Assessment

Consult schemas for complexity heuristics:
```bash
cat .claude/schemas/architecture-patterns.yaml
```

Apply classification:
- If < 5 files, < 10 endpoints → Simple
- If 10-50 files, need database → Moderate
- If microservices mentioned → Complex
```

## Schema Structure

### Standard Sections

**use_when** - Conditions when this option is appropriate
**pros** - Benefits of this choice
**cons** - Drawbacks to consider
**default_when** - Heuristic for automatic selection

**always_use** - Apply these without asking
**never_do** - Anti-patterns to avoid

### Example

```yaml
database_choice:
  sqlite:
    use_when:
      - "Project is demo, example, or prototype"
      - "< 5 models, < 10 endpoints"
    pros:
      - "Zero configuration"
      - "Perfect for development"
    cons:
      - "Not suitable for high concurrency"
    default_when: "prototype OR demo"
```

## Available Schemas

### 1. database-decisions.yaml
**When to use:** Choosing database technology
**Covers:** SQLite, PostgreSQL, MySQL, DynamoDB
**Smart defaults:** Auto-select based on project type

### 2. api-patterns.yaml
**When to use:** API architecture decisions
**Covers:** FastAPI/Flask/Django, auth patterns, error handling
**Smart defaults:** Always Pydantic v2, async/await, httpx

### 3. testing-strategies.yaml
**When to use:** Test structure and tooling
**Covers:** Unit/Integration/E2E tiers, pytest, coverage
**Smart defaults:** 80% coverage minimum, three-tier structure

### 4. architecture-patterns.yaml
**When to use:** High-level application structure
**Covers:** Monolith vs microservices, layered architecture
**Smart defaults:** API → Service → Repository flow

### 5. deployment-options.yaml
**When to use:** Deployment and infrastructure decisions
**Covers:** Lambda vs ECS vs K8s, CI/CD, monitoring
**Smart defaults:** Health checks, structured logging, IaC

## Adding New Schemas

When creating a new schema:

1. **Identify decision pattern** - Is this asked repeatedly?
2. **Extract heuristics** - What context makes the choice obvious?
3. **Document trade-offs** - Pros/cons for each option
4. **Define smart defaults** - When can we auto-apply?

### Template

```yaml
# Problem-Area Decision Schema
# Used by [list skills that read this]

choice_name:
  option_1:
    use_when:
      - "Condition that makes this obvious"
    pros:
      - "Benefit"
    cons:
      - "Drawback"
    default_when: "clear_condition"

  option_2:
    use_when:
      - "Different condition"
    pros: [...]
    cons: [...]
    default_when: "other_condition"

always_use:
  - "Best practice to apply without asking"

never_do:
  - "Anti-pattern to avoid"
```

## Updating Schemas

Schemas evolve based on usage:

- **Add options** when new technologies emerge
- **Refine heuristics** when defaults are wrong
- **Add anti-patterns** when team makes mistakes
- **Document rationale** for future reference

Track changes in git commit messages.

## Related

- **`.claude/reference/`** - Shared technical documentation (load on-demand)
- **`skills/*/references/`** - Skill-specific reference files
- **`.claude/schemas/`** - Decision guidance (this directory)

**Difference:**
- **Schemas** = Decision-making heuristics
- **References** = Technical implementation details
