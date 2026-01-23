# UW Portal API - Tax Analysis Agent Specification

**Project:** uw-portal-api
**Feature:** Tax Analysis Agent (PRO-142)
**Pattern:** Anthropic Harness-style session management
**Created:** 2026-01-23

---

## Overview

This specification defines the session-based implementation approach for the Tax Analysis Agent feature, following Anthropic's effective harnesses pattern with PIV Loop quality gates.

**Key Principles:**
1. **Session-first design** - Each session completes 1-3 related tasks
2. **File-based state** - Progress tracked in files that survive session boundaries
3. **Natural token limits** - Sessions designed to stay under 50K tokens
4. **Quality gates** - Validation after every session before proceeding
5. **Incremental commits** - Checkpoint work after each successful session

---

## Session Structure

### Session 0: Planning (One-Time Setup)

**Purpose:** Create comprehensive implementation plan with embedded context

**Commands:**
```bash
# In new conversation
/prime --quick  # 8K tokens (skip full prime if recently done)
/plan-feature tax-analysis-agent

# Saves to: .agents/plans/tax-analysis-complete.md
```

**Deliverables:**
- ✅ Self-contained plan with all necessary context embedded
- ✅ Task breakdown by session
- ✅ Token estimates per session
- ✅ Complete code examples inline (not references)
- ✅ Validation commands for each task

**Token Budget:** ~18K tokens

**Session End:**
- Close conversation
- Plan saved to `.agents/plans/tax-analysis-complete.md`
- Ready to start implementation sessions

---

### Session Initialization File

**Before any implementation session, create:**

**File:** `.agents/progress/tax-current.txt`

```txt
Feature: Tax Analysis Agent (PRO-142)
Plan: .agents/plans/tax-analysis-complete.md
Branch: feature/pro-142-tax-build-agent
Context: .agents/init-context/uw-portal-api-quick-2026-01-23.md
Started: 2026-01-23 09:00 AM
Last Updated: 2026-01-23 09:00 AM

=== PROGRESS TRACKING ===

STATUS: Not started

PHASES:
- [ ] Phase 1: Tax Return Reconciliation (6 sessions estimated)
- [ ] Phase 2: Tax Compliance Verification (3 sessions estimated)
- [ ] Phase 3: Entity Identification (3 sessions estimated)
- [ ] Phase 4: Affiliate Discovery (4 sessions estimated)
- [ ] Phase 5: Implied Debt Analysis (3 sessions estimated)

CURRENT SESSION: None
NEXT SESSION: Session 1 - Phase 1.1 Models

COMPLETED TASKS: None

VALIDATION STATUS: Baseline
- Tests passing: Yes (baseline)
- Coverage: 86.1%
- Linting: Clean
- Type checking: Clean

GIT STATUS: Clean working tree

TOKEN USAGE: No sessions yet
```

---

## Session Startup Ritual

**Every implementation session must begin with:**

```markdown
# Session Startup Checklist

## 1. Read Progress File (2K tokens)
Read: .agents/progress/tax-current.txt

Extract:
- What was completed last session
- What's the current task
- Current validation status
- Any blockers or notes

## 2. Read Relevant Plan Section (2-3K tokens)
Read: .agents/plans/tax-analysis-complete.md
- Only read the section for current session/phase
- Note the specific tasks, validation commands, gotchas

## 3. Verify Git State (0.5K tokens)
```bash
git status
git log -5 --oneline
git branch --show-current
```

Verify:
- On correct branch
- No uncommitted changes from previous session
- No merge conflicts

## 4. Baseline Validation (1K tokens)
```bash
# Run existing tests to ensure nothing broken
uv run pytest tests/unit/ -v --tb=short
uv run ruff check app/ src/
uv run mypy app/ src/
```

Verify all passing before starting work.

## 5. Token Budget Check
- Session start: 0K tokens
- After startup ritual: ~6K tokens
- Remaining budget: 194K tokens
- Target for this session: 20-40K tokens max

✅ Ready to implement
```

---

## Implementation Sessions

### Phase 1: Tax Return Reconciliation

#### Session 1: Data Models (Task 1.1)

**File:** Session script for models

**Startup:**
```bash
# Read progress file
# Read plan Phase 1, Task 1.1
# Git status check
# Baseline validation
```

**Implementation (TDD):**

1. **Write tests first** (5K tokens):
   ```python
   # tests/unit/models/test_tax_models.py

   def test_reconciliation_variance_match():
       """Test variance when values match exactly"""
       variance = ReconciliationVariance(
           line_item=ReconciliationLineItem.REVENUE,
           tax_return_value=Decimal("1500000"),
           irs_transcript_value=Decimal("1500000")
       )
       assert variance.absolute_variance == Decimal("0")
       assert variance.status == "match"

   def test_reconciliation_variance_mismatch():
       """Test variance when values differ"""
       variance = ReconciliationVariance(
           line_item=ReconciliationLineItem.NET_INCOME,
           tax_return_value=Decimal("85000"),
           irs_transcript_value=Decimal("82500")
       )
       assert variance.absolute_variance == Decimal("2500")
       assert variance.status == "variance"
   ```

2. **Implement models** (8K tokens):
   ```python
   # app/models/schemas.py (append)

   class ReconciliationLineItem(str, Enum):
       REVENUE = "revenue"
       GROSS_PROFIT = "gross_profit"
       INTEREST_EXPENSE = "interest_expense"
       DEPRECIATION = "depreciation"
       NET_INCOME = "net_income"
       ADJUSTED_GROSS_INCOME = "adjusted_gross_income"

   class ReconciliationVariance(BaseModel):
       line_item: ReconciliationLineItem
       tax_return_value: Decimal
       irs_transcript_value: Decimal
       absolute_variance: Decimal = Field(default=Decimal("0"))
       status: Literal["match", "variance"] = "match"
       notes: str = ""

       model_config = ConfigDict(use_enum_values=True)

       @model_validator(mode='after')
       def calculate_variance(self) -> 'ReconciliationVariance':
           self.absolute_variance = abs(
               self.tax_return_value - self.irs_transcript_value
           )
           self.status = "match" if self.absolute_variance == 0 else "variance"
           return self

   # Add YearReconciliation, ReconciliationResult models...
   ```

3. **Run tests** (2K tokens):
   ```bash
   uv run pytest tests/unit/models/test_tax_models.py -v
   ```

4. **Validate** (1K tokens):
   ```bash
   ruff check app/models/schemas.py
   mypy app/models/schemas.py
   ```

**Token Check:**
```
Startup: 6K
Tests: 5K
Implementation: 8K
Testing: 2K
Validation: 1K
Documentation: 2K
Total: ~24K tokens ✅ GREEN
```

**Session End:**

1. **Update progress file**:
   ```txt
   Last Updated: 2026-01-23 10:15 AM

   COMPLETED SESSIONS:
   ✓ Session 1 (Jan 23 09:00-10:15): Phase 1.1 - Data Models (24K tokens)

   COMPLETED TASKS:
   ✓ Phase 1, Task 1.1: Reconciliation models
     - ReconciliationVariance with auto-calculation
     - YearReconciliation model
     - ReconciliationResult model
     - Tests: 12 passing
     - Files: app/models/schemas.py (+85 lines)

   NEXT SESSION: Session 2 - Phase 1.2 TOD Filing Service

   VALIDATION STATUS:
   - Tests: 271 passing (was 259, +12)
   - Coverage: 86.3% (was 86.1%, +0.2%)
   - Linting: Clean
   - Type checking: Clean
   ```

2. **Commit work**:
   ```bash
   git add app/models/schemas.py tests/unit/models/test_tax_models.py
   git add .agents/progress/tax-current.txt

   git commit -m "$(cat <<'EOF'
   feat(tax): Add reconciliation data models (Phase 1.1)

   - Add ReconciliationVariance with auto-variance calculation
   - Add YearReconciliation for multi-year tracking
   - Add ReconciliationResult for taxpayer reconciliation
   - Add 12 comprehensive unit tests
   - All tests passing, coverage increased 0.2%

   Part of PRO-142 Tax Analysis Agent - Session 1/6 for Phase 1

   Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
   EOF
   )"
   ```

3. **Close session** - End conversation, free up context

---

#### Session 2: TOD Filing Service (Task 1.2)

**Startup:**
```bash
# New conversation - FRESH CONTEXT (0K tokens)
# Read .agents/progress/tax-current.txt (2K)
# Read plan Phase 1, Task 1.2 (2K)
# git status && git log -3 (0.5K)
# Baseline validation (1K)
```

**Implementation:**

1. **Copy service from demo-tax** (6K tokens):
   ```bash
   # Copy and adapt TOD Filing service
   cp ~/demo-tax/app/services/tod_filing_service.py app/services/
   ```

2. **Update imports and config** (4K tokens):
   ```python
   # app/services/tod_filing_service.py
   from app.core.config import settings  # Changed from get_settings()
   from app.models.schemas import TODFilingSummary  # Update path
   ```

3. **Write tests** (8K tokens):
   ```python
   # tests/unit/services/test_tod_filing_service.py

   @pytest.mark.asyncio
   async def test_authenticate_success():
       service = TODFilingService()
       with patch('httpx.AsyncClient') as mock_client:
           mock_client.return_value.__aenter__.return_value.post = AsyncMock(
               return_value=MagicMock(
                   json=lambda: {"access_token": "test_token"},
                   raise_for_status=MagicMock()
               )
           )
           token = await service.authenticate()
       assert token == "test_token"
   ```

4. **Run tests** (2K tokens)
5. **Validate** (1K tokens)

**Token Check:** ~25.5K tokens ✅ GREEN

**Session End:**
- Update progress file
- Commit: "feat(tax): Migrate TOD Filing service (Phase 1.2)"
- Close session

---

#### Session 3: Heron Tax Service (Task 1.3) - CRITICAL

**Startup Ritual** (6K tokens)

**Implementation:**

1. **Research Heron API** (8K tokens):
   - Read Heron documentation
   - Understand file upload/parsing endpoints
   - Create mock response fixtures

2. **Write tests** (6K tokens):
   ```python
   # tests/unit/services/test_heron_tax_service.py

   @pytest.mark.asyncio
   async def test_upload_tax_document():
       service = HeronTaxService()
       with patch('httpx.AsyncClient') as mock_client:
           # Test implementation
           pass
   ```

3. **Implement service** (12K tokens):
   ```python
   # app/services/heron_tax_service.py

   class HeronTaxService:
       def __init__(self):
           self.base_url = settings.heron_api_base_url
           self.api_key = settings.heron_api_key

       async def upload_document(
           self,
           end_user_id: str,
           file_path: str
       ) -> str:
           """Upload tax document to Heron"""
           # Implementation

       async def get_tax_documents(
           self,
           end_user_id: str
       ) -> List[Dict[str, Any]]:
           """Fetch parsed tax documents"""
           # Implementation
   ```

4. **Run tests** (2K tokens)
5. **Validate** (1K tokens)

**Token Check:** ~35K tokens ⚠️ YELLOW (higher than usual due to research)

**Critical Task Handling:**
- This task has uncertainty (Heron API research needed)
- Monitored tokens every 5K during research phase
- Stayed under 50K threshold
- Would have split if approaching 50K

**Session End:**
- Update progress file (note: research took extra tokens)
- Commit: "feat(tax): Add Heron tax service with file parsing (Phase 1.3)"
- Close session

---

#### Session 4: Workflow Nodes (Tasks 1.4-1.5)

**Why batch these tasks:**
- Both are node implementations
- Similar patterns (fetch data, handle errors)
- Small tasks (~8K each)
- Related functionality

**Startup Ritual** (6K tokens)

**Implementation:**

1. **TOD Filing Node** (8K tokens):
   ```python
   # src/nodes/tod_filing.py

   async def fetch_tod_filing_node(state: TaxAnalysisState) -> Dict[str, Any]:
       """Fetch TOD Filing transcript data"""
       if not state.get("hubspot_success"):
           return {
               "tod_filing_success": False,
               "errors": ["TOD Filing skipped: HubSpot data unavailable"]
           }

       # Extract tod_deal_id from HubSpot data
       # Call TODFilingService
       # Return state updates
   ```

2. **Heron Tax Node** (8K tokens):
   ```python
   # src/nodes/heron_tax.py

   async def fetch_heron_tax_node(state: TaxAnalysisState) -> Dict[str, Any]:
       """Fetch Heron tax document data"""
       # Similar pattern to TOD node
   ```

3. **Tests for both** (6K tokens)
4. **Validation** (2K tokens)

**Token Check:** ~30K tokens ✅ GREEN

**Session End:**
- Update progress file
- Commit: "feat(tax): Add TOD and Heron fetch nodes (Phase 1.4-1.5)"
- Close session

---

#### Session 5: Bedrock & Workflow (Tasks 1.6-1.7)

**Startup Ritual** (6K tokens)

**Implementation:**

1. **Bedrock Analysis Node** (10K tokens):
   ```python
   # src/nodes/tax_bedrock.py

   async def analyze_tax_with_bedrock_node(
       state: TaxAnalysisState
   ) -> Dict[str, Any]:
       """Invoke Bedrock tax analysis agent"""

       # Check prerequisites
       if not state.get("heron_tax_success") or not state.get("tod_filing_success"):
           return {"analysis_result": None, "errors": ["Missing data"]}

       # Build payload
       # Invoke Bedrock
       # Validate response
       # Return result
   ```

2. **Workflow Creation** (12K tokens):
   ```python
   # src/graph/workflows.py

   def create_tax_analysis_workflow() -> StateGraph:
       """Create tax analysis workflow"""
       workflow = StateGraph(TaxAnalysisState)

       # Add nodes
       workflow.add_node("fetch_hubspot", fetch_hubspot_node)
       workflow.add_node("fetch_heron_tax", fetch_heron_tax_node)
       workflow.add_node("fetch_tod_filing", fetch_tod_filing_node)
       workflow.add_node("analyze_tax_bedrock", analyze_tax_with_bedrock_node)

       # Define flow
       workflow.set_entry_point("fetch_hubspot")
       workflow.add_edge("fetch_hubspot", "fetch_heron_tax")
       workflow.add_edge("fetch_hubspot", "fetch_tod_filing")
       workflow.add_edge("fetch_heron_tax", "analyze_tax_bedrock")
       workflow.add_edge("fetch_tod_filing", "analyze_tax_bedrock")
       workflow.set_finish_point("analyze_tax_bedrock")

       return workflow.compile()
   ```

3. **Integration tests** (6K tokens)
4. **Validation** (2K tokens)

**Token Check:** ~36K tokens ✅ GREEN

**Session End:**
- Update progress file
- Commit: "feat(tax): Add Bedrock node and workflow (Phase 1.6-1.7)"
- Close session

---

#### Session 6: Integration & Configuration (Tasks 1.8-1.11)

**Startup Ritual** (6K tokens)

**Implementation:**

1. **Config updates** (4K tokens):
   ```python
   # app/core/config.py

   # TOD Filing
   tod_filing_base_url: str = Field(default="https://stg.todtax.com/api")
   tod_filing_client_id: str = Field(...)
   tod_filing_client_secret: str = Field(...)

   # Bedrock Tax Agent
   bedrock_tax_agent_id: str = Field(...)
   bedrock_tax_agent_alias_id: str = Field(...)
   ```

2. **Workflow Manager integration** (8K tokens):
   ```python
   # app/services/workflow_manager.py

   elif agent_type == AgentType.TAX_ANALYSIS:
       from src.graph.workflows import run_tax_analysis

       final_state = await run_tax_analysis(deal_id=deal_id)

       if final_state["analysis_result"]:
           # Save to S3
           # Send to data worker
           return success_response
   ```

3. **Agent Router updates** (4K tokens):
   ```python
   # app/core/agent_router.py

   class AgentType(str, Enum):
       TAX_ANALYSIS = "tax_analysis"  # NEW

   class DealStage(str, Enum):
       TAX_ANALYSIS_READY = "tax analysis - ready"  # NEW

   STAGE_AGENT_MAP = {
       DealStage.TAX_ANALYSIS_READY: [AgentType.TAX_ANALYSIS]
   }
   ```

4. **Comprehensive tests** (12K tokens)
5. **Full validation suite** (4K tokens)

**Token Check:** ~38K tokens ✅ GREEN

**Session End:**
- Update progress file (mark Phase 1 complete!)
- Commit: "feat(tax): Complete Phase 1 integration and testing"
- Close session

---

#### Session 7: Phase 1 Review & Validation

**Startup Ritual** (6K tokens)

**Review & Fix:**

1. **Run full test suite** (4K tokens):
   ```bash
   uv run pytest tests/unit/ tests/integration/ -v
   uv run pytest --cov=app --cov=src --cov-fail-under=80
   ```

2. **Code review findings** (8K tokens):
   - Review all Phase 1 code
   - Check for patterns consistency
   - Verify error handling
   - Check type hints

3. **Fix any issues** (6K tokens)

4. **Final validation** (3K tokens):
   ```bash
   ruff check app/ src/ tests/
   mypy app/ src/
   uv run pytest --cov=app --cov=src --cov-fail-under=80
   ```

5. **Update CHANGELOG** (2K tokens):
   ```markdown
   ## [Unreleased]

   ### Added
   - Tax Analysis Agent - Phase 1: Tax Return Reconciliation (PRO-142)
     - Reconciliation data models with auto-variance calculation
     - TOD Filing API integration for IRS transcript data
     - Heron tax document service for tax return extraction
     - LangGraph workflow with parallel data fetching
     - Bedrock agent integration for tax analysis
     - Comprehensive test suite (60+ new tests)
     - 80%+ code coverage maintained
   ```

**Token Check:** ~29K tokens ✅ GREEN

**Session End:**
- Update progress file (Phase 1 COMPLETE, Phase 2 READY)
- Final commit: "feat(tax): Phase 1 complete with validation and docs"
- Close session

---

## Session Template

**For future sessions, use this template:**

```markdown
# Session {N}: {Phase} - {Task Name}

## Startup (6K tokens)
- [ ] Read .agents/progress/tax-current.txt
- [ ] Read plan section for this task
- [ ] git status && git log -3
- [ ] Baseline validation (pytest, ruff, mypy)

## Implementation
- [ ] Task 1: {description} (XK tokens)
- [ ] Task 2: {description} (XK tokens)
- [ ] Tests (XK tokens)
- [ ] Validation (XK tokens)

## Token Check
Target: 20-40K tokens
Actual: __K tokens
Status: ☐ GREEN (<40K) ☐ YELLOW (40-50K) ☐ RED (>50K)

## Session End
- [ ] Update progress file
- [ ] Commit with semantic message
- [ ] Close conversation

## Notes
- Any deviations from plan
- Any blockers encountered
- Any learnings for next session
```

---

## Progress File Structure

**File:** `.agents/progress/tax-current.txt`

**Format:**

```txt
Feature: Tax Analysis Agent (PRO-142)
Plan: .agents/plans/tax-analysis-complete.md
Branch: feature/pro-142-tax-build-agent
Started: 2026-01-23 09:00 AM
Last Updated: 2026-01-23 16:45 PM

=== SESSION HISTORY ===

Completed:
1. [09:00-10:15] Phase 1.1 - Models (24K tokens) ✓
2. [10:30-11:30] Phase 1.2 - TOD Service (25.5K tokens) ✓
3. [13:00-14:15] Phase 1.3 - Heron Service (35K tokens) ✓
4. [14:30-15:30] Phase 1.4-1.5 - Nodes (30K tokens) ✓
5. [15:45-16:45] Phase 1.6-1.7 - Bedrock & Workflow (36K tokens) ✓
6. [Next day 09:00-10:30] Phase 1.8-1.11 - Integration (38K tokens) ✓
7. [10:45-11:45] Phase 1 Review (29K tokens) ✓

Current: None (Phase 1 complete, Phase 2 ready)
Next: Session 8 - Phase 2.1 Compliance Models

=== PHASE STATUS ===

✅ Phase 1: Tax Return Reconciliation (7 sessions, 217.5K tokens, 0 compactions)
🔄 Phase 2: Tax Compliance Verification (starting)
⏳ Phase 3: Entity Identification (pending)
⏳ Phase 4: Affiliate Discovery (pending)
⏳ Phase 5: Implied Debt Analysis (pending)

=== COMPLETED TASKS ===

Phase 1:
✓ Task 1.1: Reconciliation models (app/models/schemas.py +85 lines)
✓ Task 1.2: TOD Filing service (app/services/tod_filing_service.py, 350 lines)
✓ Task 1.3: Heron tax service (app/services/heron_tax_service.py +180 lines)
✓ Task 1.4: TOD Filing node (src/nodes/tod_filing.py +90 lines)
✓ Task 1.5: Heron tax node (src/nodes/heron_tax.py +85 lines)
✓ Task 1.6: Tax Bedrock node (src/nodes/tax_bedrock.py +110 lines)
✓ Task 1.7: Tax workflow (src/graph/workflows.py +150 lines)
✓ Task 1.8: Config updates (app/core/config.py +20 lines)
✓ Task 1.9: Workflow manager (app/services/workflow_manager.py +80 lines)
✓ Task 1.10: Agent router (app/core/agent_router.py +15 lines)
✓ Task 1.11: Tests & validation (60+ new tests)

=== VALIDATION STATUS ===

Tests: 319 passing (was 259, +60)
Coverage: 87.3% (was 86.1%, +1.2%)
Linting: Clean (ruff check)
Type checking: Clean (mypy)
CHANGELOG: Updated

=== GIT STATUS ===

Commits: 7 (one per session)
- 1a2b3c4 feat(tax): Add reconciliation models (Phase 1.1)
- 2b3c4d5 feat(tax): Migrate TOD Filing service (Phase 1.2)
- 3c4d5e6 feat(tax): Add Heron tax service (Phase 1.3)
- 4d5e6f7 feat(tax): Add TOD and Heron nodes (Phase 1.4-1.5)
- 5e6f7g8 feat(tax): Add Bedrock and workflow (Phase 1.6-1.7)
- 6f7g8h9 feat(tax): Complete integration and testing (Phase 1.8-1.11)
- 7g8h9i0 feat(tax): Phase 1 complete with validation

Branch: feature/pro-142-tax-build-agent
Status: Up to date with dev
Conflicts: None

=== TOKEN ANALYTICS ===

Total sessions: 7
Total tokens: 217.5K (across 7 fresh sessions)
Average per session: 31.1K tokens
Max session: 38K tokens (Session 6)
Min session: 24K tokens (Session 1)
Compactions: 0 ✅
Success rate: 100% ✅

=== DEVIATIONS FROM PLAN ===

1. Session 3 took more tokens than estimated (35K vs 25K)
   - Reason: Heron API research and documentation review
   - Impact: None (stayed under 50K threshold)
   - Mitigation: Monitored tokens every 5K increments

2. Batched Tasks 1.4-1.5 into Session 4
   - Reason: Both small, related node implementations
   - Impact: Positive (saved one session)

3. Added Session 7 for review (not in original plan)
   - Reason: Best practice to validate before next phase
   - Impact: Positive (caught 2 minor issues)

=== LEARNINGS ===

✓ Quick prime sufficient (didn't need full prime context)
✓ Self-contained plan works well (no context lookups needed)
✓ Session checkpoints every 30-40K optimal
✓ Progress file essential for multi-session continuity
✓ Token monitoring every 10K prevents surprises
✓ TDD approach reduces debugging time
✓ Baseline validation catches regressions early
✓ Batching small related tasks efficient

=== BLOCKERS ===

None currently

=== NEXT SESSION PREP ===

Session 8: Phase 2.1 - Compliance Models
Estimated tokens: 20-25K
Files to create:
- ComplianceCheck model
- TranscriptYear model
- Tests

Prerequisites:
- None (Phase 1 complete)

Estimated start: Next morning
```

---

## Validation Gates

**After EVERY session:**

```bash
#!/bin/bash
# .agents/scripts/validate-session.sh

echo "=== Session Validation Gate ==="

echo "1. Running tests..."
uv run pytest tests/unit/ tests/integration/ -v --tb=short
if [ $? -ne 0 ]; then
    echo "❌ TESTS FAILED - Do not proceed"
    exit 1
fi

echo "2. Checking coverage..."
uv run pytest --cov=app --cov=src --cov-fail-under=80 --cov-report=term-missing
if [ $? -ne 0 ]; then
    echo "❌ COVERAGE BELOW THRESHOLD - Do not proceed"
    exit 1
fi

echo "3. Linting..."
uv run ruff check app/ src/ tests/
if [ $? -ne 0 ]; then
    echo "❌ LINTING FAILED - Do not proceed"
    exit 1
fi

echo "4. Type checking..."
uv run mypy app/ src/
if [ $? -ne 0 ]; then
    echo "❌ TYPE CHECKING FAILED - Do not proceed"
    exit 1
fi

echo "✅ All validation gates passed - Safe to commit and close session"
exit 0
```

---

## Token Budget Management

**Monitor tokens every 10K:**

```markdown
# Token Budget Monitoring

## Checkpoints

At 10K: ☐ Check
At 20K: ☐ Check
At 30K: ☐ Check
At 40K: ⚠️ WARNING - Consider checkpointing soon
At 50K: 🚨 CRITICAL - Checkpoint NOW or risk compaction
At 75K: ❌ DANGER ZONE - Compaction imminent

## Actions by Budget Level

GREEN (<40K): Continue normally
YELLOW (40-50K):
  - Finish current task
  - Don't start new tasks
  - Prepare to checkpoint

RED (>50K):
  - Checkpoint immediately
  - Update progress file
  - Commit work
  - Close session

## Formula

Remaining work estimate = (Target tokens per task) × (Tasks remaining)

If (Current tokens + Remaining work estimate) > 75K:
  → Checkpoint now
Else:
  → Can continue
```

---

## Feature Tracking JSON

**File:** `.agents/features/uw-portal-features.json`

```json
{
  "project": "uw-portal-api",
  "features": [
    {
      "id": "PRO-142",
      "name": "Tax Analysis Agent",
      "status": "in_progress",
      "plan": ".agents/plans/tax-analysis-complete.md",
      "progress_file": ".agents/progress/tax-current.txt",
      "branch": "feature/pro-142-tax-build-agent",
      "phases": [
        {
          "phase": 1,
          "name": "Tax Return Reconciliation",
          "status": "completed",
          "sessions": 7,
          "tokens_used": 217500,
          "started": "2026-01-23",
          "completed": "2026-01-24"
        },
        {
          "phase": 2,
          "name": "Tax Compliance Verification",
          "status": "in_progress",
          "sessions": 0,
          "tokens_used": 0,
          "started": "2026-01-24",
          "completed": null
        },
        {
          "phase": 3,
          "name": "Entity Identification",
          "status": "pending",
          "sessions": null,
          "tokens_used": null,
          "started": null,
          "completed": null
        },
        {
          "phase": 4,
          "name": "Affiliate Discovery",
          "status": "pending",
          "sessions": null,
          "tokens_used": null,
          "started": null,
          "completed": null
        },
        {
          "phase": 5,
          "name": "Implied Debt Analysis",
          "status": "pending",
          "sessions": null,
          "tokens_used": null,
          "started": null,
          "completed": null
        }
      ],
      "sessions": [
        {
          "session": 1,
          "date": "2026-01-23",
          "phase": 1,
          "tasks": ["1.1"],
          "work": "Reconciliation models",
          "tokens": 24000,
          "duration_minutes": 75,
          "compactions": 0,
          "status": "completed"
        },
        {
          "session": 2,
          "date": "2026-01-23",
          "phase": 1,
          "tasks": ["1.2"],
          "work": "TOD Filing service",
          "tokens": 25500,
          "duration_minutes": 60,
          "compactions": 0,
          "status": "completed"
        }
      ],
      "metrics": {
        "total_sessions": 7,
        "total_tokens": 217500,
        "avg_tokens_per_session": 31071,
        "max_session_tokens": 38000,
        "total_compactions": 0,
        "success_rate": 1.0,
        "phases_completed": 1,
        "phases_total": 5,
        "completion_percentage": 20,
        "estimated_remaining_sessions": 18,
        "estimated_remaining_tokens": 540000
      },
      "created": "2026-01-23",
      "last_updated": "2026-01-24",
      "target_completion": "2026-02-05"
    }
  ]
}
```

---

## Commit Message Format

**Every session commit:**

```bash
git commit -m "$(cat <<'EOF'
{type}(tax): {description} (Phase {phase}.{task})

- {Detail 1}
- {Detail 2}
- {Detail 3}
- Tests: {N} passing, coverage {X}%

Part of PRO-142 Tax Analysis Agent - Session {N}/{total} for Phase {phase}

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

**Example:**

```bash
git commit -m "$(cat <<'EOF'
feat(tax): Add reconciliation data models (Phase 1.1)

- ReconciliationVariance with auto-variance calculation
- YearReconciliation for multi-year tracking
- ReconciliationResult for complete taxpayer reconciliation
- 12 comprehensive unit tests with parametrization
- Tests: 271 passing (+12), coverage 86.3% (+0.2%)

Part of PRO-142 Tax Analysis Agent - Session 1/7 for Phase 1

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Success Metrics

**Per Session:**
- ✅ Tokens used < 50K
- ✅ All tests passing
- ✅ Coverage maintained or improved
- ✅ Linting clean
- ✅ Type checking clean
- ✅ Progress file updated
- ✅ Clean commit created
- ✅ 0 compactions

**Per Phase:**
- ✅ All planned tasks completed
- ✅ Acceptance criteria met
- ✅ Integration tests passing
- ✅ CHANGELOG updated
- ✅ Documentation updated

**Overall Feature:**
- ✅ All 5 phases complete
- ✅ 80%+ code coverage
- ✅ E2E tests passing
- ✅ Production deployment successful
- ✅ < 25 sessions total
- ✅ 0 compactions across all sessions

---

## Troubleshooting

### Session Approaching 50K Tokens

**Symptoms:**
- Token count > 45K
- Still have work remaining in session

**Actions:**
1. Stop current task
2. Update progress file with current state
3. Commit work done so far
4. Note where to resume in progress file
5. Close session
6. Start fresh session for remaining work

### Baseline Validation Failing

**Symptoms:**
- Tests failing at session startup
- Previous session left broken state

**Actions:**
1. DO NOT PROCEED with new work
2. Read progress file for last session notes
3. Check git log for last commit
4. Fix broken tests
5. Re-run validation
6. Update progress file with fix
7. Create fix commit
8. Only then start planned session work

### Uncertain How to Implement

**Symptoms:**
- Task complexity higher than estimated
- Token usage accelerating
- Need significant research

**Actions:**
1. Note in progress file: "Research needed for task X"
2. Allocate research budget (e.g., 10K tokens)
3. If research + implementation > 50K:
   - Split into 2 sessions
   - Session A: Research + design
   - Session B: Implementation
4. Update task estimates for future

### Forgot to Update Progress File

**Symptoms:**
- Session ended without progress update
- Next session starts confused

**Actions:**
1. Reconstruct from git log
2. Review code changes
3. Update progress file retroactively
4. Commit update with note:
   ```
   chore(progress): Update session {N} notes (retroactive)
   ```

---

## Summary

This specification provides:

✅ **Session-based structure** - Never hit compaction
✅ **File-based state** - Progress survives conversation boundaries
✅ **Startup ritual** - Consistent session initialization
✅ **Token budgets** - Clear thresholds and monitoring
✅ **Validation gates** - Quality checks at every session
✅ **Progress tracking** - Comprehensive state management
✅ **Commit pattern** - Clean, semantic git history
✅ **Success metrics** - Clear goals and measurements
✅ **Troubleshooting** - Common issues and solutions

**Expected Outcome:**
- Complete Tax Analysis Agent feature
- 20-25 total sessions across 5 phases
- 0 compactions
- 100% success rate
- High-quality, well-tested code
- Complete institutional knowledge preserved

**Use this specification as the playbook for implementing PRO-142 and future large features.**
