# Feasibility Assessment Guide

**Complexity estimation rubrics for `/explore` Phase 4**

---

## Purpose

Assess implementation feasibility to:
- Set realistic expectations
- Identify risks early
- Inform architectural decisions
- Guide resource planning

**Not for precise estimates** - For understanding scope and complexity level.

---

## Complexity Dimensions

### 1. Code Complexity

**Metrics:**
- Number of files/modules needed
- Lines of code (approximate)
- Cyclomatic complexity
- Number of dependencies
- Integration points

**Classification:**

| Level | Files | LOC | Dependencies | Integration Points |
|-------|-------|-----|--------------|-------------------|
| **Small** | 1-3 | < 500 | 0-2 new | 1-2 |
| **Medium** | 4-10 | 500-2000 | 3-6 new | 3-5 |
| **Large** | 10-30 | 2000-10000 | 7-15 new | 6-10 |
| **Very Large** | 30+ | 10000+ | 15+ new | 10+ |

**Examples:**

```markdown
Small: Add password reset endpoint
- 1 route handler file
- 1 email template
- 1 token validation util
- 2 new dependencies (email library, token lib)
→ Complexity: Small

Medium: Add user authentication system
- 4 route handlers (login, signup, logout, refresh)
- 2 models (User, Session)
- 3 utilities (password hash, JWT, validation)
- 1 middleware (auth check)
- 4 new dependencies
→ Complexity: Medium

Large: Add real-time collaboration
- 10+ files (WebSocket handlers, state management, sync logic)
- 5000+ LOC (bidirectional sync, conflict resolution)
- 8 new dependencies (WS library, Redis, etc.)
- Multiple integration points (DB, cache, frontend)
→ Complexity: Large
```

---

### 2. Learning Curve

**Factors:**
- New technologies to learn
- Unfamiliar concepts
- Documentation quality
- Community support
- Team expertise

**Classification:**

| Level | Description | Time to Productivity |
|-------|-------------|---------------------|
| **Low** | Familiar tech, clear docs, team has expertise | 1-2 days |
| **Medium** | Some new concepts, good docs, team can learn | 1-2 weeks |
| **High** | New paradigm, sparse docs, limited expertise | 1+ months |

**Examples:**

```markdown
Low Learning Curve:
- Adding FastAPI endpoint (team uses FastAPI)
- Using pytest for tests (team familiar)
- SQLite for prototype (standard library)

Medium Learning Curve:
- First time using async/await in Python
- Learning Redis caching patterns
- Implementing OAuth 2.0 (with good docs)

High Learning Curve:
- Moving from sync to async architecture
- Implementing CRDT for conflict resolution
- Building custom consensus protocol
```

---

### 3. Risk Assessment

**Risk Categories:**

#### Technical Risks

| Risk | Low | Medium | High |
|------|-----|--------|------|
| **Breaking Changes** | Isolated feature | Touches core logic | Architectural change |
| **Performance** | Minimal impact | Some concerns | Could cause degradation |
| **Security** | Standard patterns | Custom auth | New attack surface |
| **Data Loss** | Read-only | Safe writes | Complex migrations |

#### Operational Risks

| Risk | Low | Medium | High |
|------|-----|--------|------|
| **Deployment** | No infra changes | New services | New infrastructure |
| **Monitoring** | Existing tools | New metrics | New monitoring system |
| **Rollback** | Easy rollback | Some complexity | Difficult/impossible |
| **Dependencies** | Battle-tested libs | Popular but newer | Experimental |

**Risk Scoring:**

```markdown
Count risk levels:
- Each High risk: +3 points
- Each Medium risk: +2 points
- Each Low risk: +1 point

Total Score:
- 0-5: Low Risk
- 6-10: Medium Risk
- 11+: High Risk
```

---

### 4. Implementation Estimate

**Size Categories:**

#### Small (1-3 days)
- Single feature, well-defined
- 1-3 files
- < 500 LOC
- 0-2 new dependencies
- Clear patterns exist
- Minimal testing complexity

**Examples:**
- Add CORS middleware
- New API endpoint (CRUD)
- Simple data validation
- Basic error handling

#### Medium (1-2 weeks)
- Multiple related features
- 4-10 files
- 500-2000 LOC
- 3-6 new dependencies
- Some design decisions needed
- Moderate testing complexity

**Examples:**
- User authentication system
- Background job processing
- Caching layer
- Admin dashboard

#### Large (1+ months)
- Complex system or major refactor
- 10-30 files
- 2000-10000 LOC
- 7-15 new dependencies
- Significant architectural decisions
- Comprehensive testing needed

**Examples:**
- Real-time collaboration
- Multi-tenancy support
- Event-driven architecture
- Search infrastructure

#### Very Large (Multiple months)
- Major platform feature
- 30+ files
- 10000+ LOC
- 15+ new dependencies
- New architectural patterns
- Extensive testing & monitoring

**Examples:**
- Microservices migration
- Custom ML pipeline
- Distributed system
- Multi-region deployment

---

## Assessment Framework

### Step 1: Count Touchpoints

```markdown
| Area | Count | Notes |
|------|-------|-------|
| New files | | |
| Modified files | | |
| New models/schemas | | |
| New endpoints | | |
| Database migrations | | |
| New dependencies | | |
| Integration points | | |
| Test files needed | | |
```

### Step 2: Evaluate Each Dimension

```markdown
## Code Complexity: [Small/Medium/Large]
- Rationale: [Why this classification]

## Learning Curve: [Low/Medium/High]
- New technologies: [List]
- Team familiarity: [Assessment]
- Documentation quality: [Available/Sparse]

## Risk Assessment: [Low/Medium/High]
- Technical risks: [List with severity]
- Operational risks: [List with severity]
- Mitigation strategies: [How to reduce risk]

## Implementation Estimate: [Small/Medium/Large/Very Large]
- Based on: [Complexity + Learning + Risk]
```

### Step 3: Consider Dependencies

```markdown
## Critical Path Dependencies

- [ ] Dependency 1: [What needs to happen first]
- [ ] Dependency 2: [What this blocks]

## External Dependencies

- [ ] Third-party service availability
- [ ] Library compatibility
- [ ] Infrastructure provisioning
```

### Step 4: Identify Unknowns

```markdown
## Known Unknowns

1. [Thing we know we don't know yet]
   - Impact: [High/Medium/Low]
   - Mitigation: [How to resolve]

2. [Another unknown]
   - Impact: [High/Medium/Low]
   - Mitigation: [How to resolve]
```

---

## Complexity Multipliers

### Factors That Increase Complexity

**×1.5 Multiplier:**
- Working with legacy code
- No existing tests
- Poor documentation
- Tight coupling

**×2.0 Multiplier:**
- Distributed systems involved
- Complex state management
- Cross-team dependencies
- Production data migration

**×3.0 Multiplier:**
- No similar examples exist
- Pioneering new approach
- Critical path / high risk
- Complex regulatory requirements

**Example:**

```markdown
Base estimate: Medium (1-2 weeks)
Factors:
- Legacy code integration (×1.5)
- Production migration (×2.0)

Adjusted estimate: Medium → Large (1+ months)
```

---

## Decision Matrix

Use complexity assessment to inform decisions:

```markdown
| Complexity | Learning | Risk | Recommendation |
|-----------|----------|------|----------------|
| Small | Low | Low | ✅ Proceed immediately |
| Small | Low | Medium | ✅ Proceed with monitoring |
| Small | Medium | Low | ✅ Proceed with learning plan |
| Medium | Low | Low | ✅ Proceed with design phase |
| Medium | Medium | Medium | ⚠️ Proceed cautiously, plan well |
| Large | High | High | ⛔ Reconsider, explore alternatives |
```

---

## Example Assessment

### Feature: Real-Time Notifications

**Step 1: Touchpoints**
- New files: 6 (WebSocket handler, notification service, models)
- Modified files: 3 (main app, auth, frontend)
- New dependencies: 4 (WebSocket library, Redis, etc.)
- Integration points: 4 (DB, cache, auth, frontend)

**Step 2: Dimensions**

**Code Complexity: Medium**
- 6-8 files needed
- ~1200 LOC estimated
- 4 new dependencies
- Standard WebSocket patterns available

**Learning Curve: Medium**
- Team hasn't used WebSockets before
- Good documentation available
- Similar to HTTP endpoints (familiar)

**Risk Assessment: Medium**
- Performance impact unknown
- Need load testing
- Graceful degradation required
- Can't easily rollback active connections

**Step 3: Dependencies**
- Need Redis for pub/sub (can use existing instance)
- Frontend changes required (separate work)
- Auth middleware needs WebSocket support

**Step 4: Unknowns**
- Connection scaling (100 or 10K simultaneous?)
- Message delivery guarantees needed?
- Reconnection strategy?

**Final Assessment:**

```markdown
## Feasibility: MEDIUM COMPLEXITY

**Implementation Estimate:** Medium (1-2 weeks)
- Development: 1 week
- Testing & refinement: 3-5 days

**Risk Level:** Medium
- Mitigation: Spike to test scaling, plan rollback strategy

**Recommendation:** Proceed with POC first
- Validate scaling assumptions
- Test with load testing
- Then full implementation
```

---

## Use Codebase Analysis

If similar code exists, analyze it:

```bash
# Use complexity script
uv run python .claude/skills/explore/scripts/estimate_complexity.py [path]

# Review output:
- File sizes (compare to your estimate)
- Function complexity (expect similar patterns)
- Import counts (dependency indicator)
```

**Adjust estimates based on findings:**

```markdown
Similar feature: User authentication
- Actual: 8 files, 1400 LOC
- Our estimate: 6 files, 1000 LOC
→ Adjust up by 30%
```

---

## Remember

**Feasibility assessment is:**
- A guide, not a commitment
- Based on current understanding
- Subject to change as we learn
- Tool for risk identification

**Feasibility assessment is NOT:**
- Precise schedule estimate
- Binding commitment
- Replacement for planning
- Excuse to over-engineer

**"The goal is to understand scope, not predict the future."**

---

## Output Template

```markdown
## Feasibility Assessment: [Feature]

### Complexity Analysis

**Code Complexity:** [Small/Medium/Large/Very Large]
- Files: [Count]
- LOC: [Estimate]
- Dependencies: [Count new]
- Integration points: [Count]

**Learning Curve:** [Low/Medium/High]
- New technologies: [List]
- Team expertise: [Assessment]
- Documentation: [Quality assessment]

**Risk Level:** [Low/Medium/High]
- Technical risks: [List with severity]
- Operational risks: [List with severity]
- Mitigation: [Strategy]

### Implementation Estimate

**Size:** [Small/Medium/Large/Very Large]
**Rationale:** [Why this classification]

### Dependencies & Blockers

- [Dependency 1]
- [Dependency 2]

### Known Unknowns

1. [Unknown with mitigation]
2. [Unknown with mitigation]

### Recommendation

✅ / ⚠️ / ⛔ [Proceed / Proceed cautiously / Reconsider]

**Rationale:** [Why this recommendation]

**Next Steps:** [What to do based on recommendation]
```
