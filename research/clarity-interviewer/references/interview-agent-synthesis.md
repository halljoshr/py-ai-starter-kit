# Interview Agent Synthesis — Combining Two Approaches

**Date:** 2026-02-09
**Purpose:** Compare the clarity-interviewer skill with the TeamBuild Interview Agent requirements, and propose a synthesis that captures the best of both.

---

## Background

We have two interview approaches to compare:

1. **Clarity-Interviewer** — A story-based interviewer skill using Teresa Torres methodology and Dylan Davis' "Don't Prompt AI. Let It Prompt You" approach
2. **TeamBuild Interview 001** — A requirements discovery interview that produced the v0.1 build order and requirements spec for the TeamBuild project

Both aim to extract clarity before building, but they use different mechanics and have different philosophies.

---

## What Clarity-Interviewer Does

**Location:** `research/clarity-interviewer/`

A **story-based interviewer** that helps users discover insights they didn't know they had. Core mechanics:

### Key Features
- **ONE question at a time** — dynamically selected from multiple candidates based on the previous answer
- **Story-based questioning** — "Tell me about the last time you..." not "What do you usually..."
- **Explorer mindset** — empowered to follow rabbit trails for hidden insights
- **Profile-driven** — builds a user profile (values, priorities) during the interview and adapts questions accordingly
- **Internal completeness tracking** — maintains a 1-10 score to know when to stop (not a fixed question count)
- **Domain libraries** — reusable question patterns for software discovery, personal clarity, business strategy, etc.
- **Natural conclusion** — stops when clarity is achieved (completeness 9-10), produces key insights + next steps + first action

### Philosophy
The interview process itself draws out unconscious knowledge. The user discovers insights they didn't know they had. The interviewer is an explorer, not just a form-filler.

### Supporting Files
- `references/story-based-questions.md` — Teresa Torres templates and anti-patterns
- `references/domains/software-discovery.md` — Software-specific question libraries and case studies
- `references/domains/personal-clarity.md` — Personal decision-making question patterns

---

## What TeamBuild Interview 001 Did

**Location:** `conversation-logs/001-initial-interview.md`

A **requirements discovery interview** focused on building a v0.1 spec for the TeamBuild project. Core mechanics:

### Key Features
- **10 questions total** — sequenced around an arc (vision → pain → components → constraints)
- **Adaptive but structured** — each question built on the last, but there was an overall plan
- **Focused on outputs** — inputs/expected outputs, build order, technical decisions, trade-offs
- **Decision forcing** — confirmed priorities, ruled things out of scope
- **Produced artifacts** — requirements.md, build order, handoff documents, context management spec

### Philosophy
Extract clarity *before coding starts*. Inputs and outputs must be well-defined or the build will fail. The interview should produce concrete, actionable deliverables.

### Outputs Produced
- `requirements.md` — standalone requirements spec with 6 modules defined
- `HANDOFF.md` — current state, next task, research inventory
- Updated `CLAUDE.md` — agent entry point
- Conversation log with metrics and observations

---

## Side-by-Side Comparison

| Dimension | Clarity-Interviewer | TeamBuild Interview 001 |
|-----------|---------------------|-------------------------|
| **Question style** | Story-based ("Tell me about the last time...") | Direct ("What do you need? What's the priority?") |
| **Flow** | ONE at a time, dynamic generation | Sequential with an arc, adaptive |
| **Goal** | General clarity, discover hidden insights | Requirements spec, build order, technical decisions |
| **Stopping condition** | Completeness score 9-10 | Covered all necessary ground for requirements |
| **Outputs** | Key insights + next steps + first action | Requirements doc, build order, handoff docs |
| **Explorer mindset** | Empowered to follow tangents | Stayed on track toward requirements |
| **Profile-driven** | Adapts to user values | Not used (didn't build a profile) |
| **Question generation** | Generates 3-5 candidates, picks best | Pre-planned sequence, adaptive within it |
| **Internal tracking** | Explicit completeness scoring | Implicit (interviewer judgment) |
| **Domain knowledge** | Reusable libraries that grow over time | Custom to this interview |

---

## What Each Does Better

### Clarity-Interviewer Strengths
1. ✅ **Story-based questioning** — gets real examples, reveals patterns, avoids biased generalizations
2. ✅ **Explorer mindset** — finds hidden treasure in tangents (e.g., the context window management insight came from a tangent)
3. ✅ **Profile-driven adaptation** — connects to user's actual values and working style
4. ✅ **Completeness tracking** — systematic way to know when you're done
5. ✅ **Dynamic question generation** — not pre-scripted, generates candidates and picks the best
6. ✅ **Domain libraries** — reusable patterns that improve over time with learnings
7. ✅ **Teresa Torres methodology** — proven approach for discovery interviews

### TeamBuild Interview 001 Strengths
1. ✅ **Focus on deliverables** — produced a concrete build order and requirements doc
2. ✅ **Technical depth** — covered architecture, constraints, tech stack, context management
3. ✅ **Decision forcing** — confirmed what's in/out of scope, prioritized the build order
4. ✅ **Handoff readiness** — produced artifacts an agent can pick up and run with
5. ✅ **Scoped to a goal** — knew we were building requirements, not just exploring
6. ✅ **Structured output** — requirements.md is ready to use for building
7. ✅ **Metrics tracking** — estimated tokens, cost, duration for the session

---

## The Synthesis: A Hybrid Interview Agent

**Recommendation:** Combine the best of both approaches into the TeamBuild Interview Agent.

### Core Concept
Use **clarity-interviewer mechanics** (story-based, explorer mindset, completeness tracking) but keep the **TeamBuild focus** (deliverables, technical depth, structured outputs).

The Interview Agent has two modes (as defined in requirements.md) but uses story-based mechanics in both:

---

### Mode 1: Direct Interview (Story-Based Requirements Discovery)

**Goal:** Extract requirements from a stakeholder who is available for conversation

**Mechanics:**
- Uses **story-based questioning** scoped to a specific deliverable (requirements doc, feature spec, architecture decision)
- Example: "Tell me about the last time you tried to build a feature like this and ran into problems. What happened?"
- Follows **explorer mindset** — empowered to follow rabbit trails when they reveal important insights
- Tracks **completeness** — knows when enough clarity has been achieved for the deliverable
- Produces **structured output** — requirements doc with inputs/outputs, build order, constraints

**Example Flow:**
1. User provides brain dump or topic
2. Agent infers role/goal (e.g., "I'll interview you as a product strategist to define requirements for this feature")
3. Confirms with user
4. Begins story-based questioning
5. Internally tracks completeness (1-10)
6. Follows valuable tangents
7. Concludes naturally when completeness is high (9-10)
8. Produces requirements.md with clear inputs, outputs, scope, constraints

---

### Mode 2: Gap Analysis (Story-Based Spec Critique)

**Goal:** Identify what's missing from an existing spec or plan

**Mechanics:**
- Takes an existing spec/plan as input
- Analyzes against domain patterns (what's typically needed in a software spec)
- Identifies gaps (missing inputs, undefined outputs, unclear scope, etc.)
- Generates **targeted story-based questions** to fill gaps
- Example: "I don't see how errors are handled in this spec. Tell me about the last time this system encountered an error. What happened?"
- Uses **domain libraries** to know what's typically missing
- Produces an **updated spec** or a list of targeted questions for the stakeholder

**Example Flow:**
1. User provides existing spec/plan
2. Agent reads and analyzes it
3. Identifies gaps using domain knowledge
4. Generates story-based questions to fill each gap
5. Either interviews the user directly OR produces a list of questions to send to stakeholders
6. Updates the spec with new information
7. Produces updated requirements.md or a gap report

---

### Shared Mechanics (Both Modes)

These mechanics apply to both Direct Interview and Gap Analysis:

#### 1. ONE Question at a Time
- Never ask two questions
- Never ask a question with sub-parts
- Wait for the answer before generating the next question

#### 2. Dynamic Question Generation
After each user response, generate 3-5 candidate questions internally, then pick the best one:
```
Potential Follow-ups:
  1. [Most relevant to current understanding gaps]
  2. [Alternative angle on the same topic]
  3. [Rabbit trail that might reveal hidden insight]
  4. [Confirmation question if something seems contradictory]
  5. [Scope/constraint question]
Selected: [Pick the best based on completeness gaps]
```

#### 3. Internal Note-Taking
After each user response, maintain internal notes (not shown to user):
```
Current Understanding: [Summary of what's been learned so far]
Key Insights: [Important discoveries — especially things the user didn't realize]
Unanswered Questions: [What we still don't know for the deliverable]
Potential Follow-ups (1-5): [Next question candidates]
Completeness: [1-10 — how complete is our understanding for this deliverable?]
```

#### 4. Story-Based Questioning (When Appropriate)
Prefer specific situations over generalizations:

**❌ DON'T ASK:**
- "What do you usually do when..."
- "How do you generally handle..."
- "What typically happens when..."

**✅ DO ASK:**
- "Tell me about the last time you..."
- "Describe a specific situation where..."
- "Walk me through exactly what happened when..."

**When to use it:** Best for understanding pain points, workflows, past decisions, user behavior. Less useful for pure technical constraints or scope decisions.

#### 5. Profile Building
Build a lightweight profile during the interview:
- Working style (terminal-first, IDE-based, keyboard shortcuts, etc.)
- Values (efficiency, quality, cost, etc.)
- Pain points (re-explaining errors, context management, etc.)
- Priorities (what matters most vs. least)

Use this profile to adapt questions and connect deliverables to what the user cares about.

#### 6. Explorer Mindset
When a user's answer hints at something unexpected or potentially valuable, pursue it. Don't rigidly stick to a script.

**Example:** In TeamBuild Interview 001, the context window management insight came as a post-interview addition. With explorer mindset, that would have been discovered *during* the interview as a natural tangent.

#### 7. Natural Conclusion
Stop when:
- Completeness score reaches 9-10 for the deliverable
- All critical gaps are filled (inputs, outputs, scope, constraints)
- User indicates they're done
- No new insights are emerging

Signal the transition: "I think we've covered the core of this. Let me pull together what we've discovered."

#### 8. Structured Output
Always produce a concrete deliverable. The output format depends on the domain and goal:

**For Requirements Discovery:**
```markdown
# [Project Name] — Requirements Specification

## Problem Statement
[Core problem being solved]

## System Overview
[High-level description]

## Requirements
### Component 1: [Name]
**Purpose:** [What it does]
**Inputs:** [What it needs]
**Outputs:** [What it produces]
**Constraints:** [Technical/business limits]

[Repeat for each component]

## Out of Scope
[What's explicitly not included]
```

**For Feature Specifications:**
```markdown
# Feature: [Name]

## User Story
[Specific situation from interview]

## Inputs
- [Data/info the feature needs]

## Outputs
- [What the feature produces]

## Success Criteria
- [How we know it works]

## Edge Cases
- [From interview stories]
```

---

## Integration with TeamBuild Requirements

The Interview Agent (as defined in `requirements.md`) should be updated to include:

### 1. Story-Based Questioning Templates
Add domain libraries similar to clarity-interviewer:
- `domains/software-requirements.md` — patterns for discovering software requirements
- `domains/feature-specs.md` — patterns for feature definition
- `domains/architecture-decisions.md` — patterns for technical decision interviews

### 2. Internal Completeness Tracking
Add explicit completeness scoring (1-10) for:
- Inputs defined
- Outputs defined
- Scope defined
- Constraints identified
- Edge cases covered
- Success criteria established

### 3. Dynamic Question Generation
The agent should generate multiple question candidates after each response and select the best one, not follow a pre-scripted sequence.

### 4. Profile Building
Capture and use:
- User's working style (from the interview itself)
- Pain points (what frustrates them)
- Values (what they prioritize)
- Technical preferences (languages, tools, patterns)

### 5. Explorer Mindset
Empower the agent to follow valuable tangents. Example: If the user mentions "our previous prime function consumed all the context," that's a rabbit trail worth exploring even if it wasn't in the original question plan.

### 6. Domain Libraries That Grow
After each interview, the agent should:
- Update domain files with new patterns discovered
- Add successful questions to the library
- Document pitfalls encountered
- Record case studies

This makes the Interview Agent smarter over time.

---

## Example: Hybrid Interview in Action

**Scenario:** User wants to build a new authentication feature

**Setup Phase:**
- User provides brain dump: "Need to add login to the app, OAuth probably, don't want the session management nightmare from last time"
- Agent infers: Role = Software PM/Engineer, Goal = Requirements discovery for auth feature, Domain = software-requirements
- Agent confirms: "I'll interview you as a software architect to help define requirements for this authentication feature. Sound right?"
- User: "Yeah"

**Interview Phase:**

**Agent:** "You mentioned 'session management nightmare from last time.' Tell me about that specific situation. What happened?"

**User:** "We used OAuth with Google and it worked great until users started getting randomly logged out..."

*[Internal notes: pain point = random logouts, assumption = using OAuth again, unanswered = root cause of logouts, completeness = 2/10]*

**Agent:** "Walk me through a specific instance when a user got logged out. What were they doing when it happened?"

**User:** "One user was in the middle of filling out a long form, token expired after 30 minutes, they got kicked to login, lost all their work..."

*[Internal notes: key insight = token expiry + no refresh = data loss, user pain = lost work, unanswered = desired token lifetime?, completeness = 3/10]*

**Agent:** "What was going through your mind when you found out about that? What did you realize needed to be different?"

**User:** "We needed automatic token refresh in the background, and we needed to save form state even if they get logged out..."

*[Internal notes: requirements emerging = auto-refresh + state persistence, completeness = 5/10]*

**Agent:** "For this new feature, what's the absolute worst thing that could happen if authentication fails?"

**User:** "Honestly? Same thing — user loses work. Or worse, they're in the middle of a transaction and it gets corrupted..."

*[Internal notes: critical constraint = never lose user work or corrupt transactions, completeness = 7/10]*

**Agent:** "Tell me about the last time you had to choose an authentication approach for a project. What made you pick OAuth then?"

*[Continues with story-based questions, following tangents about token storage, security requirements, third-party vs. custom auth]*

*[After ~15 questions, completeness = 9/10]*

**Agent:** "I think we've covered the core of this. Let me pull together what we've discovered."

**Output Phase:**

Agent produces:

```markdown
# Authentication Feature — Requirements Specification

## Problem Statement
Users need to authenticate with the app. Previous OAuth implementation caused data loss due to token expiry and lack of refresh mechanism. Critical constraint: never lose user work or corrupt transactions.

## Requirements

### Component 1: Authentication Provider
**Purpose:** Handle user login and session management
**Inputs:** User credentials (OAuth via Google)
**Outputs:** Access token, refresh token, user profile
**Constraints:** Must support automatic token refresh without user interaction

### Component 2: Session Persistence
**Purpose:** Preserve user state even during authentication failures
**Inputs:** Form data, transaction state, user context
**Outputs:** Restored state after re-authentication
**Constraints:** Must handle mid-transaction failures gracefully

### Component 3: Token Management
**Purpose:** Automatic token refresh in background
**Inputs:** Expiring access token, refresh token
**Outputs:** New access token
**Constraints:** Must refresh before expiry, no user disruption

## Success Criteria
- User completes 30+ minute form without losing data
- Transactions complete even if token expires mid-process
- No user-visible session interruptions

## Edge Cases (From Interview)
- Token expires during form submission
- Refresh token is revoked
- User opens multiple tabs
- Network interruption during refresh

## Out of Scope for v1
- Multi-provider OAuth (Google only for now)
- Passwordless authentication
- 2FA
```

---

## Recommendations for Implementation

### 1. Start with Story-Based Templates
Incorporate the clarity-interviewer question templates into the Interview Agent's domain libraries. This is low-hanging fruit.

### 2. Add Completeness Tracking
Implement the 1-10 scoring system with explicit criteria for each score level:
- 1-3: Very incomplete, major gaps
- 4-6: Partial understanding, some gaps
- 7-8: Mostly complete, minor gaps
- 9-10: Complete, ready to build

### 3. Build Dynamic Question Generation
Instead of pre-scripting questions, generate candidates after each response and select the best one.

### 4. Enable Explorer Mindset
Don't rigidly stick to a sequence. Follow valuable tangents.

### 5. Profile-Driven Customization
Build a lightweight profile and adapt questions to the user's context.

### 6. Structured Outputs Always
Every interview produces a concrete deliverable, formatted appropriately for the domain.

### 7. Living Domain Libraries
After each interview, update domain files with learnings. Make the agent smarter over time.

---

## Next Steps

1. **Update requirements.md** — Add story-based mechanics, completeness tracking, domain libraries to the Interview Agent spec
2. **Create domain libraries** — Start with `domains/software-requirements.md` using patterns from clarity-interviewer
3. **Design the completeness scoring system** — Define what 1-10 means for different deliverable types
4. **Build question generation logic** — Implement the candidate generation and selection mechanism
5. **Test with a real interview** — Use the hybrid approach on a real requirements discovery session and compare to interview 001

---

## Conclusion

The clarity-interviewer and TeamBuild Interview 001 are complementary, not competing. By combining:

- **Clarity-interviewer's mechanics** (story-based, explorer mindset, completeness tracking, domain libraries)
- **TeamBuild's focus** (deliverables, technical depth, structured outputs, handoff readiness)

We get an Interview Agent that is both insightful (discovers what users don't realize they know) AND practical (produces concrete requirements docs ready for building).

This synthesis makes the Interview Agent significantly more powerful than either approach alone.
