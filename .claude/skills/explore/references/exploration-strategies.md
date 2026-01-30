# Exploration Strategies

**Guide for effective discovery questioning during `/explore` Phase 1**

---

## Question Framework

### The 5 W's + H

1. **What** - What are we building?
2. **Why** - What problem does it solve?
3. **Who** - Who are the users?
4. **When** - What's the context/trigger?
5. **Where** - Where does it fit in the system?
6. **How** - How might it work (high-level)?

---

## Question Patterns

### Pattern 1: Problem Clarification

**Goal:** Understand the actual problem, not just the proposed solution

```markdown
Q: "What problem are you experiencing right now?"
Q: "What would success look like?"
Q: "What have you tried so far?"
Q: "What's not working with the current approach?"
```

**Example:**
```
User: "We need WebSockets"
↓
Q: "What real-time feature are you trying to enable?"
A: "Users should see when someone comments on their post"
↓
Q: "How quickly do they need to see it?"
A: "Within a few seconds is fine"
↓
Insight: Don't actually need WebSockets, SSE or polling would work
```

### Pattern 2: Scale & Context

**Goal:** Understand scope to avoid over-engineering

```markdown
Q: "How many users/requests/items are we targeting?"
Q: "Is this for MVP or production scale?"
Q: "What's the growth trajectory?"
Q: "Are there compliance/security requirements?"
```

**Scale Classifications:**
- **Prototype:** < 100 users, demo purposes
- **Small:** 100-1K users, single instance
- **Medium:** 1K-100K users, multiple instances
- **Large:** 100K+ users, distributed system

### Pattern 3: Constraints Discovery

**Goal:** Identify boundaries and limitations

```markdown
Q: "What tech stack are you already using?"
Q: "Any deployment constraints (AWS only, on-prem, etc.)?"
Q: "Team expertise level (junior, senior, mixed)?"
Q: "Timeline expectations?"
Q: "Budget constraints?"
```

**Constraint Impact:**

| Constraint | Low Impact | High Impact |
|------------|-----------|-------------|
| Tech stack | "Use any Python library" | "Must integrate with legacy Java system" |
| Timeline | "No rush, explore options" | "Need in production ASAP" |
| Team | "Senior engineers" | "Junior team, learning as we go" |
| Budget | "Can use paid services" | "Open source only, no external costs" |

### Pattern 4: Success Criteria

**Goal:** Define measurable outcomes

```markdown
Q: "How will we know this is working well?"
Q: "What metrics matter most?"
Q: "What's the acceptable performance threshold?"
Q: "What's the failure mode we're most worried about?"
```

**Make Concrete:**

| Vague | Concrete |
|-------|----------|
| "Fast" | "< 500ms p95 response time" |
| "Reliable" | "99.9% uptime, automatic failover" |
| "Scalable" | "Handle 10K concurrent connections" |
| "Secure" | "OWASP Top 10 compliant, SOC2 certified" |

### Pattern 5: Alternatives Exploration

**Goal:** Understand why they're exploring this direction

```markdown
Q: "Have you considered [alternative approach]?"
Q: "What made you think of [their proposed solution]?"
Q: "Are there existing features that do something similar?"
Q: "What's the upgrade path if we start simple?"
```

---

## Progressive Questioning

**Start broad, narrow down:**

```
Level 1 (Broad):
"Tell me about what you're trying to build"

Level 2 (Category):
"Is this primarily about performance, features, or user experience?"

Level 3 (Specific):
"You mentioned performance - are we talking about response time, throughput, or resource usage?"

Level 4 (Measurable):
"What's the target response time? What's acceptable vs ideal?"
```

---

## Question Sequencing

### Bad Sequencing
```
Q1: "Which database should we use?"
Q2: "How should we structure the tables?"
Q3: "What about indexing strategy?"
```
❌ Jumped to solution before understanding problem

### Good Sequencing
```
Q1: "What data are we storing and how will it be queried?"
Q2: "What's the expected data volume and growth rate?"
Q3: "Are there specific query patterns or performance requirements?"
[Now we can recommend database based on actual needs]
```

---

## Anti-Patterns to Avoid

### 1. Leading Questions

**❌ Bad:**
```
"You want to use PostgreSQL for this, right?"
"Wouldn't Redis be faster for caching?"
```

**✅ Good:**
```
"What are your thoughts on database choice?"
"Have you considered caching? What would you want to cache?"
```

### 2. Yes/No Questions

**❌ Bad:**
```
"Do you need authentication?"
"Should we add caching?"
```

**✅ Good:**
```
"What types of user authentication does your system need?"
"What parts of the system would benefit from caching and why?"
```

### 3. Overwhelming Options

**❌ Bad:**
```
"For your API, you could use FastAPI, Flask, Django, Express, NestJS,
Gin, Echo, or Rails. Which one do you want?"
```

**✅ Good:**
```
"I see you're building an API. Given your team uses Python,
I'd recommend FastAPI (modern, async) or Flask (simple, flexible).
Which approach appeals more - feature-rich or minimal?"
```

### 4. Assuming Context

**❌ Bad:**
```
"Obviously you'll need a load balancer and Redis cluster for this"
```

**✅ Good:**
```
"At your current scale (1K users), we could start simple.
As you grow past 10K users, you'd likely need load balancing
and distributed caching. Sound reasonable?"
```

---

## Use AskUserQuestion Effectively

### Single Focus Questions

```
Question: "What scale are you targeting?"
Options:
- Prototype (< 100 users, testing ideas)
- Small production (100-1K users, single server)
- Medium production (1K-100K users, multiple servers)
- Large production (100K+ users, distributed system)
```

### Multiple Related Questions

```
Questions:
1. "What's your current backend tech stack?"
   - Python (FastAPI, Flask, Django)
   - JavaScript (Node.js, Express, NestJS)
   - Go, Rust, Java
   - Other

2. "What's your team's expertise level?"
   - Mostly junior (learning as we go)
   - Mixed (some seniors, some juniors)
   - Mostly senior (experienced engineers)

3. "What's the deployment environment?"
   - AWS (Lambda, ECS, EC2)
   - On-premise servers
   - Other cloud (GCP, Azure)
   - Haven't decided
```

---

## Common Discovery Patterns

### Pattern: API Development

```
Discovery sequence:
1. What data does the API expose?
2. Who are the API consumers (internal, external, mobile, web)?
3. What's the expected request volume?
4. Any specific performance requirements?
5. Authentication/authorization needs?
6. Versioning strategy?

→ Research: FastAPI vs Flask vs Django REST Framework
```

### Pattern: Data Processing

```
Discovery sequence:
1. What data are we processing (size, format, frequency)?
2. Real-time or batch processing?
3. Where is the data coming from and going to?
4. Any transformation/validation requirements?
5. Error handling needs?
6. Monitoring/observability requirements?

→ Research: Celery vs AWS Lambda vs Apache Airflow
```

### Pattern: Authentication

```
Discovery sequence:
1. Who needs to authenticate (end users, services, APIs)?
2. What's the user journey (signup, login, SSO)?
3. Session management needs (stateless, stateful)?
4. MFA/2FA requirements?
5. Compliance requirements (GDPR, HIPAA)?
6. Existing identity providers?

→ Research: JWT vs Sessions, OAuth 2.0, Auth0 vs Cognito vs custom
```

---

## Documentation Template

After discovery, document findings:

```markdown
## Discovery Summary

**Problem Statement:**
[Clear, concise problem description]

**Context:**
- Current state: [what exists now]
- Desired state: [what we want]
- Gap: [what's missing]

**Constraints:**
- Technical: [tech stack, infrastructure]
- Scale: [users, requests, data volume]
- Team: [expertise, size, availability]
- Timeline: [urgency, dependencies]

**Success Criteria:**
1. [Measurable outcome 1]
2. [Measurable outcome 2]
3. [Measurable outcome 3]

**Key Questions for Research:**
1. [What we need to find out]
2. [What solutions exist]
3. [What are the trade-offs]
```

---

## Remember

**Good discovery:**
- Clarifies the problem before jumping to solutions
- Uncovers constraints that affect solution choice
- Establishes measurable success criteria
- Reveals user and system context
- Identifies what research is actually needed

**"Hours spent in discovery save days spent in rework."**
