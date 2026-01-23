# From Feature Doc to Implementation Spec: The Process

**Question:** How do you go from a requirements document (like TaxDoc.md) to a complete Anthropic-style spec (like tax_analysis_spec.txt)?

---

## The Anthropic Process (Inferred)

### Phase 1: Requirements Gathering (Human-Led)

**Input:** Business requirements, user stories, mockups
**Output:** Feature document (like your TaxDoc.md)
**Who:** Product manager, domain experts, stakeholders
**Duration:** Days to weeks

**What they create:**
- User-facing requirements
- Business logic rules
- Data sources identified
- Success criteria (business-level)

**Your TaxDoc.md is this artifact.**

---

### Phase 2: Technical Discovery (Human + AI Collaboration)

**Input:** Feature doc + existing codebase
**Output:** Technical research, API analysis, architecture decisions
**Who:** Senior engineer + Claude (research mode)
**Duration:** 1-2 days

#### 2.1: Codebase Analysis

**Human asks Claude:**
```
I need to implement tax analysis in uw-portal-api.
Here's the feature doc: [TaxDoc.md]
Here's the codebase: [uw-portal-api context]

Help me understand:
1. What existing patterns should I follow?
2. What services already exist that I can reuse?
3. What's the current architecture for agents?
4. Show me 3-5 similar features as examples
```

**Claude does research:**
- Reads existing agent implementations (debt, risk, bank statement)
- Identifies patterns (LangGraph workflows, TypedDict states, service layer)
- Maps existing infrastructure (S3, Bedrock, workflow manager)
- Finds reference implementations

**Output: Technical Context Document**
```markdown
# Tax Analysis - Technical Context

## Existing Patterns to Follow
- DebtAnalysisWorkflow (parallel data fetching)
- RiskAssessmentState (TypedDict with error accumulation)
- HeronService pattern (async httpx, S3 caching)

## Reusable Components
- HubSpot fetch node (extract prescreen_id, deal data)
- BedrockAgentService (agent invocation wrapper)
- AgentResponseValidator (JSON validation/repair)
- WorkflowManager.execute_agent() (standard integration point)

## New Components Needed
- TOD Filing service (migrate from demo-tax)
- Heron tax service (new, generic file parsing)
- Tax-specific data models (5 model groups)
- 3 new workflow nodes
```

---

#### 2.2: API Research

**Human asks Claude:**
```
Research these APIs and document their capabilities:
1. Heron Data API - tax document extraction
2. TOD Filing API - IRS transcript access
3. What endpoints exist? What's the response format?
```

**Claude does:**
- Reads API documentation
- Identifies endpoints
- Documents authentication methods
- Notes limitations/gotchas

**Output: API Analysis Document**
```markdown
# API Analysis

## Heron Data API
- No tax-specific endpoints (GOTCHA!)
- Use generic file upload: POST /end_users/{id}/files
- Response format: [document fixture examples]
- Authentication: API key in header

## TOD Filing API
- OAuth via Auth0
- Endpoint: GET /filing-requests/{id}/summary
- Polling required (max 30 attempts, 10s interval)
- Response includes: account balance, filing status, notice codes
```

---

#### 2.3: Data Model Design

**Human asks Claude:**
```
Based on TaxDoc.md requirements and the APIs, design the Pydantic models.
Show me:
1. All enums needed
2. All data classes
3. Computed fields
4. Validation rules
```

**Claude produces:**
```python
# Proposed Data Models

class ReconciliationLineItem(str, Enum):
    REVENUE = "revenue"
    # ... etc

class ReconciliationVariance(BaseModel):
    line_item: ReconciliationLineItem
    tax_return_value: Decimal
    irs_transcript_value: Decimal
    absolute_variance: Decimal = Field(default=Decimal("0"))
    status: Literal["match", "variance"] = "match"

    @model_validator(mode='after')
    def calculate_variance(self):
        # Auto-compute variance
```

**Human reviews and approves** (or requests changes)

---

#### 2.4: Workflow Design

**Human asks Claude:**
```
Design the LangGraph workflow for tax analysis.
Show me:
1. What nodes are needed
2. What order should they run
3. What data flows between nodes
4. What's the state schema
```

**Claude produces:**
```
Workflow: TaxAnalysis

Nodes:
1. fetch_hubspot (reuse existing)
2. fetch_heron_tax (new)
3. fetch_tod_filing (new)
4. analyze_tax_bedrock (new)

Flow:
fetch_hubspot → [fetch_heron_tax, fetch_tod_filing] (parallel) → analyze_tax_bedrock

State: TaxAnalysisState
- deal_id, analysis_date
- hubspot_data, hubspot_success
- heron_tax_data, heron_tax_success
- tod_filing_data, tod_filing_success
- analysis_result
- errors (Annotated[List[str], operator.add])
```

**Human reviews:** "Yes, this matches our debt analysis pattern"

---

### Phase 3: Spec Assembly (Human + AI)

**Input:** All discovery artifacts from Phase 2
**Output:** Complete implementation spec (tax_analysis_spec.txt)
**Who:** Senior engineer dictates, Claude writes/formats
**Duration:** 2-4 hours

#### 3.1: Structure Setup

**Human:** "Create a spec file using Anthropic's XML format"

**Claude:** Creates structure with all XML tags:
```xml
<project_specification>
  <project_name>...</project_name>
  <overview>...</overview>
  <technology_stack>...</technology_stack>
  <core_features>...</core_features>
  <data_models>...</data_models>
  <api_endpoints>...</api_endpoints>
  <services_to_implement>...</services_to_implement>
  <workflow_nodes>...</workflow_nodes>
  <workflow_graph>...</workflow_graph>
  <integration_points>...</integration_points>
  <testing_strategy>...</testing_strategy>
  <implementation_steps>...</implementation_steps>
  <session_management>...</session_management>
  <success_criteria>...</success_criteria>
  <constraints>...</constraints>
  <gotchas>...</gotchas>
</project_specification>
```

---

#### 3.2: Fill in Each Section

**For each section, human provides content and Claude formats:**

**Example - Core Features:**

**Human says:**
```
"Phase 1 is tax reconciliation. We compare 5 line items from Heron against TOD Filing transcripts over 3 years. Flag variances. Support both business and personal returns."
```

**Claude writes:**
```xml
<phase_1_tax_reconciliation>
  - Compare submitted tax returns (Heron) against IRS transcripts (TOD Filing)
  - Reconcile 5 line items: revenue, gross profit, interest expense, depreciation, net income
  - Track 3 years of historical data per taxpayer
  - Flag variances with orange status (green for exact matches)
  - Support both business (1120S, 1065, Schedule C) and personal (1040) returns
  - Generate ReconciliationResult with year-by-year variance analysis
</phase_1_tax_reconciliation>
```

---

**Example - Implementation Steps:**

**Human says:**
```
"Break this into 10 steps. Start with fixtures, then models, then services, then nodes, then workflow, then integration."
```

**Claude writes:**
```xml
<implementation_steps>
  <step_0>
    Task: Setup test infrastructure and fixtures
    Duration: 1 session (~20K tokens)

    Actions:
    - Create fixture directories
    - Research Heron API response format
    - Create mock responses
    ...
  </step_0>

  <step_1>
    Task: Implement reconciliation data models
    Duration: 1 session (~25K tokens)
    TDD: Write tests first
    ...
  </step_1>
</implementation_steps>
```

---

#### 3.3: Add Session Management Rules

**This is where Anthropic's innovation comes in.**

**Human dictates rules:**
```
"For session management:
- Every session starts with: ls, cat progress file, git status, baseline tests
- Token budget: 20-40K per session, stop at 50K
- Progress file format: plain text with sections
- End every session with: validation, progress update, commit
- Never end with broken tests
"
```

**Claude formalizes:**
```xml
<session_management>
  <startup_ritual>
    Every session begins with:
    1. ls (verify working directory)
    2. cat .agents/progress/tax-current.txt (read progress)
    3. git status && git log -5 (understand current state)
    4. uv run pytest tests/unit/ -v --tb=short (baseline validation)
    5. Read relevant section of tax_analysis_spec.txt

    Never start coding without completing startup ritual.
  </startup_ritual>

  <token_budgeting>
    Target per session: 20-40K tokens
    Warning threshold: 50K tokens
    Critical threshold: 75K tokens
    ...
  </token_budgeting>
</session_management>
```

---

#### 3.4: Document Gotchas

**Human shares experience/concerns:**
```
"Watch out for:
1. Heron has no tax-specific endpoints - use generic file upload
2. Bedrock might timeout with full 3 years of PDFs - extract key fields first
3. Pydantic v2 syntax is different from v1 - use model_validator not @validator
"
```

**Claude captures:**
```xml
<gotchas>
  <heron_api_uncertainty>
    Issue: Heron API documentation shows no tax-specific endpoints
    Solution: Use generic file upload/parsing endpoints
    Impact: May need to adjust parsing logic based on actual responses
    Mitigation: Create fixtures early to validate assumptions
  </gotchas>

  <bedrock_token_usage>
    Issue: Sending full 3 years of tax returns may exceed token limits
    Solution: Extract key fields from Heron before sending to Bedrock
    Impact: Need to pre-process Heron data in node
    Mitigation: Use structured summaries, not raw PDFs
  </bedrock_token_usage>
</gotchas>
```

---

### Phase 4: Spec Validation (Human Review)

**Input:** Draft spec
**Output:** Approved spec
**Who:** Senior engineer + tech lead review
**Duration:** 1-2 hours

**Review checklist:**
- [ ] All requirements from TaxDoc.md covered?
- [ ] Follows existing codebase patterns?
- [ ] Implementation steps are session-sized (<40K tokens each)?
- [ ] Testing strategy comprehensive?
- [ ] Session management rules clear?
- [ ] Success criteria measurable?
- [ ] Gotchas documented?

**Human makes final edits**, then **spec is approved**.

---

## The Realistic Process for You

### Option A: Full Anthropic Process (2-3 days upfront)

**Day 1: Technical Discovery**
```
Session 1 (90 min): Codebase analysis
- You: "Claude, analyze uw-portal-api for patterns I should follow"
- Claude: Generates technical context doc

Session 2 (60 min): API research
- You: "Claude, research Heron and TOD Filing APIs"
- Claude: Documents endpoints, auth, gotchas

Session 3 (90 min): Data model design
- You: "Claude, design Pydantic models for TaxDoc requirements"
- Claude: Proposes models, you review and approve

Session 4 (60 min): Workflow design
- You: "Claude, design the LangGraph workflow"
- Claude: Proposes node graph, you approve
```

**Day 2: Spec Assembly**
```
Session 5 (120 min): Write spec
- You dictate content section by section
- Claude formats in XML structure
- You review each section as it's written

Session 6 (60 min): Add session management rules
- You: "Add Anthropic-style session management"
- Claude: Adds startup ritual, token budgeting, progress tracking

Session 7 (30 min): Final review
- Read entire spec
- Check all requirements covered
- Approve for implementation
```

**Day 3: Implement Phase 1 (using spec)**
```
Session 8-14: Implementation following spec
- Each session follows spec's implementation_steps
- Startup ritual enforced
- Token budgets respected
- Progress tracked
```

**Total time investment:**
- **2 days planning** (12 hours)
- **5-7 days implementing** (all 5 phases)
- **Result:** Clean, predictable implementation with 0 compactions

---

### Option B: Lightweight Spec (1 day upfront) - RECOMMENDED

**Morning: Quick Discovery (3-4 hours)**
```
Session 1 (90 min): Combined analysis
You: "Claude, I need to implement tax analysis. Here's TaxDoc.md and uw-portal-api context.
Give me:
1. What patterns to follow (show me existing code examples)
2. What new services/models/nodes needed
3. Proposed data models
4. Proposed workflow design
5. Any API gotchas"

Claude: Produces combined technical design doc (15-20K tokens)
```

```
Session 2 (90 min): Write minimal spec
You: "Convert this design into an Anthropic-style spec with:
- Core features by phase
- Data models (just the key ones)
- Services to implement
- Workflow nodes and graph
- Implementation steps (10 steps max)
- Session management (startup ritual, token budgets)
- Top 5 gotchas"

Claude: Produces minimal spec (20K tokens)
```

**Afternoon: Validate Spec (1 hour)**
```
Session 3 (60 min): Review and approve
- Read spec
- Check requirements covered
- Add any missing gotchas
- Approve
```

**Next 5-7 Days: Implement**
```
Follow spec session by session
```

**Total time investment:**
- **4-5 hours planning**
- **5-7 days implementing**
- **Result:** Good enough spec, clean implementation

---

### Option C: No Spec, Iterative Planning (What you're doing now)

**Current approach:**
```
Session 1: Prime + Plan (55K tokens)
Session 2: Try to implement Phase 1... COMPACTION at Task 1.3
Session 3: Restart, try again... COMPACTION again
Session 4: Frustration, ask for help
```

**Problems:**
- No upfront technical design
- Plans too large (1,669 lines)
- No session boundaries defined
- Token budgets not planned
- Hitting compaction repeatedly

**Why Anthropic doesn't do this:**
- Wastes time restarting
- Inconsistent implementation
- Context loss damages quality
- Developer frustration

---

## The Key Insight

**Anthropic's secret sauce:**

> **"Spend 2 days planning to save 10 days debugging"**

The spec is **not extra work** - it's **investment in predictability**.

### What the Spec Provides

1. **Clear session boundaries** (20-40K per session)
2. **Explicit patterns to follow** (reduces decision-making during implementation)
3. **Complete data model design** (no "figure it out as you go")
4. **Token budget planning** (prevents compaction)
5. **Testing strategy upfront** (TDD from the start)
6. **Gotchas documented** (avoid common mistakes)
7. **Success criteria** (know when done)

### Without Spec

- Figure out patterns during implementation
- Design models as you go
- Hope you don't hit compaction
- Discover gotchas the hard way
- Unclear when "done"
- **Result: 2-3x longer, lower quality**

---

## Practical Recommendation for Your Tax Feature

**You're at the decision point:**

### Path 1: Write Spec Now (Recommended)

**Time:** 1 day (4-5 hours with Claude)
**Outcome:** Clean implementation, 0 compactions, predictable timeline

**Process:**
```
Today:
1. Session with Claude: Technical discovery (90 min)
   - "Claude, analyze uw-portal-api patterns, research APIs, design models"

2. Session with Claude: Write spec (90 min)
   - "Claude, write Anthropic-style spec from this design"

3. Review spec (30 min)
   - Read, approve, save as tax_analysis_spec.txt

Tomorrow: Start implementation following spec
   - Session 1: Fixtures (Step 0)
   - Session 2: Models (Step 1)
   - etc.
```

---

### Path 2: Use Existing Plan, Add Session Management

**Time:** 1-2 hours
**Outcome:** Better than current, not as good as full spec

**Process:**
```
Today:
1. Take existing tax-analysis-complete.md
2. Add session boundaries:
   - Session 1: Tasks 1.1 only
   - Session 2: Task 1.2 only
   - Session 3: Task 1.3 only
   - etc.
3. Add startup ritual to each session
4. Add token budgets
5. Create progress file template

Tomorrow: Implement with session discipline
```

---

### Path 3: Continue Current Approach

**Time:** Unknown (keep restarting on compaction)
**Outcome:** Eventually works, but painful

**Not recommended.**

---

## The Anthropic Philosophy

**Their blog post revealed:**

> "We found that agents working in shifts (multiple sessions) completed projects faster and with better code quality than single long-running sessions."

**Why:**
1. Fresh context each session = clear thinking
2. Session boundaries = natural checkpoints
3. Progress files = no memory loss between sessions
4. Token budgets = never hit compaction
5. Startup ritual = always know current state

**The spec enables this model.**

Without spec:
- Sessions don't know where they left off
- No clear task boundaries
- Token usage unpredictable
- Context loss catastrophic

With spec:
- Each session knows exactly what to do
- Clear stop/start points
- Token usage planned
- Progress tracked in files

---

## Bottom Line

**Your question:** "How did Anthropic get to their spec?"

**Answer:**
1. **Human-led discovery** (1-2 days: research APIs, design models, plan workflow)
2. **Claude-assisted documentation** (Claude writes spec in XML format as human dictates)
3. **Human approval** (review, edit, approve)
4. **Claude executes spec** (multiple sessions, fresh context each time, following spec exactly)

**The spec is the interface between:**
- Human strategic thinking (what to build, how to architect)
- AI tactical execution (write code following the plan)

**For your tax feature:**

**Minimum viable spec:** 4-5 hours to create
**Savings during implementation:** 10-15 hours (avoid restarts, compactions, confusion)
**ROI:** 2-3x time savings

**My recommendation:** Spend tomorrow morning creating a proper spec with Claude, then implement cleanly over the next week.

The spec you have now (tax_analysis_spec.txt) is 80% there. Just need to validate it covers everything from TaxDoc.md and you're ready to go.
