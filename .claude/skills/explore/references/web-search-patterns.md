# Web Search Patterns

**Strategic research strategies for `/explore` Phase 2**

---

## Research Hierarchy

### Priority Order

1. **Official Documentation** (Most authoritative)
   - Framework/library docs
   - RFC specifications
   - Standards bodies (OWASP, NIST, W3C)

2. **Production-Grade Examples**
   - Open source projects (10K+ stars)
   - Reference implementations
   - Case studies from major companies

3. **Expert Knowledge**
   - Blog posts from maintainers/contributors
   - Conference talks
   - Technical deep-dives

4. **Community Knowledge** (Use cautiously)
   - Stack Overflow (high-voted answers)
   - Reddit technical subreddits
   - GitHub discussions/issues

---

## WebFetch Strategy

### Start with Official Sources

```bash
# Pattern 1: Official Documentation
WebFetch: "https://fastapi.tiangolo.com/"
Prompt: "Summarize FastAPI's async capabilities, dependency injection,
and when to use it vs Flask"

# Pattern 2: Framework Comparisons
WebFetch: "https://www.python.org/dev/peps/pep-0249/"
Prompt: "Explain DB-API 2.0 specification and compliance requirements"

# Pattern 3: Standards & RFCs
WebFetch: "https://datatracker.ietf.org/doc/html/rfc7519"
Prompt: "Extract JWT security best practices and common vulnerabilities"
```

### Search for Real Implementations

```bash
# GitHub search patterns
Search: "repo:microsoft/vscode authentication patterns"
Search: "repo:netflix/eureka service discovery architecture"
Search: "language:python stars:>5000 topic:real-time"

# Look for:
- How they structure code
- What libraries they use
- How they handle edge cases
- What their testing looks like
```

---

## Research Patterns by Topic

### Pattern: API Design

**Sources to check:**
1. Framework documentation (FastAPI, Express, etc.)
2. REST API design guides (Microsoft, Google API design)
3. OpenAPI specification
4. Real-world APIs (GitHub, Stripe, Twilio)

**Key information to extract:**
- URL structure patterns (/api/v1/resource/:id)
- Error handling conventions (RFC 7807)
- Authentication methods (API keys, OAuth, JWT)
- Rate limiting strategies
- Versioning approaches

**WebFetch prompts:**
```
"Summarize REST API best practices for error handling"
"Extract authentication patterns and security considerations"
"Compare versioning strategies (URL vs header vs content negotiation)"
```

### Pattern: Database Selection

**Sources to check:**
1. Database documentation (PostgreSQL, MongoDB, Redis)
2. Comparison articles (avoid clickbait, prefer technical depth)
3. Performance benchmarks (TechEmpower, PingCAP)
4. Case studies (how X company chose Y database)

**Key information to extract:**
- ACID vs eventual consistency
- Scaling characteristics (vertical vs horizontal)
- Query patterns and performance
- Operational complexity
- Cost considerations

**Comparison framework:**
```markdown
| Database | Best For | Not Good For | Complexity |
|----------|----------|--------------|------------|
| PostgreSQL | Relational data, ACID | Massive scale (100M+ rows) | Medium |
| MongoDB | Flexible schema, JSON | Complex joins | Low |
| Redis | Caching, pub/sub | Primary data store | Low |
```

### Pattern: Authentication/Authorization

**Sources to check:**
1. OWASP Authentication Cheat Sheet
2. OAuth 2.0 specification (RFC 6749)
3. Auth provider docs (Auth0, Cognito, Keycloak)
4. JWT specification (RFC 7519)

**Key information to extract:**
- Security best practices (password hashing, token storage)
- Session management (stateless vs stateful)
- SSO/SAML/OAuth flows
- Common vulnerabilities (CSRF, session fixation)

**Security checklist:**
```markdown
- [ ] Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
- [ ] JWT tokens signed and verified
- [ ] HTTPS enforced
- [ ] Rate limiting on auth endpoints
- [ ] Account lockout after failed attempts
- [ ] Secure password reset flow
```

### Pattern: Caching Strategy

**Sources to check:**
1. Redis documentation
2. HTTP caching specs (RFC 7234)
3. CDN provider docs (CloudFront, Cloudflare)
4. Caching patterns (Cache-Aside, Write-Through, Read-Through)

**Key information to extract:**
- Cache invalidation strategies
- TTL recommendations
- Distributed caching patterns
- Cache stampede prevention
- Memory vs disk tradeoffs

### Pattern: Background Jobs

**Sources to check:**
1. Celery, RQ, APScheduler documentation
2. Message queue docs (RabbitMQ, Redis, SQS)
3. Serverless options (Lambda, Cloud Functions)
4. Job processing patterns

**Key information to extract:**
- Task queuing mechanisms
- Retry and error handling
- Monitoring and observability
- Scaling characteristics
- Deployment complexity

---

## Evaluating Sources

### Trust Signals

**✅ High Trust:**
- Official documentation
- Posts from library maintainers
- Companies using it in production (with details)
- GitHub repos with 10K+ stars
- Recent content (last 2 years)
- Technical depth (shows code, discusses trade-offs)

**⚠️ Medium Trust:**
- Technical blogs (evaluate author credentials)
- Stack Overflow answers (check votes and date)
- Medium articles (if from verified experts)
- Conference talks (from recognized events)

**❌ Low Trust:**
- Random blogs with no credentials
- Outdated content (> 3 years for fast-moving tech)
- No code examples or implementation details
- Clickbait titles ("X is DEAD, use Y instead!")
- Blanket statements without nuance

### Red Flags

```markdown
❌ "X is always better than Y"
   → Look for: "X is better than Y when [conditions]"

❌ "You should never use Z"
   → Look for: "Z has trade-offs in [scenarios]"

❌ "This is the only way to do it"
   → Look for: "Common approaches include..."

❌ No mention of trade-offs or limitations
   → Look for: "Pros, cons, when to use"
```

---

## Documentation Patterns

### Capture Structure

For each solution researched:

```markdown
## Solution: [Name]

**Source:** [URL]
**Date:** [When researched]
**Authority:** Official docs / Open source / Expert blog / Community

### Overview
[2-3 sentence description]

### Key Capabilities
- Feature 1
- Feature 2
- Feature 3

### Pros
- ✅ Benefit 1 (with context)
- ✅ Benefit 2

### Cons
- ❌ Limitation 1 (with context)
- ❌ Limitation 2

### When to Use
- Scenario 1
- Scenario 2

### When to Avoid
- Scenario 1
- Scenario 2

### Code Example
\`\`\`python
# Simple, runnable example
\`\`\`

### Resources
- [Documentation](url)
- [Tutorial](url)
- [Example project](url)
```

---

## Common Research Workflows

### Workflow 1: Finding the Right Tool

```
1. Identify category (caching, auth, database, etc.)
2. WebFetch official "awesome" list for category
3. Filter by stars (10K+) and recent activity
4. Read documentation for top 3-5 options
5. Look for comparison articles from trusted sources
6. Check GitHub issues for common problems
7. Document findings in comparison table
```

### Workflow 2: Understanding Best Practices

```
1. Start with official framework documentation
2. Look for "best practices" guides from maintainers
3. Check OWASP/NIST for security-related topics
4. Find 2-3 production examples (open source)
5. Look at how they structure code
6. Extract patterns and anti-patterns
7. Document as reusable guidelines
```

### Workflow 3: Evaluating Trade-offs

```
1. List requirements and constraints
2. Research 3-4 candidate solutions
3. For each solution:
   - Read documentation
   - Find production usage examples
   - Check GitHub issues for problems
   - Look for benchmarks/comparisons
4. Create trade-off matrix
5. Recommend best fit with rationale
```

---

## Search Query Patterns

### GitHub Search

```
# Find popular implementations
language:python stars:>5000 topic:authentication

# Find recent activity
language:python pushed:>2024-01-01 topic:caching

# Find specific patterns
"dependency injection" language:python path:src/

# Find testing approaches
filename:test_*.py "async def test_"
```

### Documentation Search

```
# Framework-specific
site:fastapi.tiangolo.com dependency injection

# Standard bodies
site:owasp.org authentication cheat sheet

# RFCs
site:datatracker.ietf.org JWT

# PEPs (Python)
site:python.org/dev/peps/ async
```

---

## Time Management

### Research Depth Levels

**Quick Research (30-60 minutes):**
- Read official docs for 2-3 options
- Skim comparison article
- Check GitHub stars and recent activity
- Capture basic pros/cons

**Medium Research (2-3 hours):**
- Deep dive on official docs
- Read 2-3 production examples
- Check performance benchmarks
- Review security considerations
- Create comparison table

**Deep Research (4-6 hours):**
- Comprehensive documentation review
- Multiple example implementations
- Read relevant RFCs/specs
- Security audit
- Performance analysis
- POC implementation
- Full trade-off analysis

**When to stop researching:**
- Found 3-4 viable options
- Understand key trade-offs
- Can make informed recommendation
- Have enough resources to proceed

**"Perfect information is impossible. Sufficient information is the goal."**

---

## Output Quality Checklist

Research is sufficient when you can answer:

- [ ] What are the top 3-4 solutions in this space?
- [ ] What are the key differences between them?
- [ ] What are the trade-offs for each?
- [ ] Which solution fits our context best and why?
- [ ] What are the security considerations?
- [ ] What's the learning curve and complexity?
- [ ] What are the common pitfalls?
- [ ] Where can we find good examples?
- [ ] What resources would help implementation?

---

## Remember

**Research Goals:**
1. **Inform** - Give enough context to make decisions
2. **Compare** - Show alternatives and trade-offs
3. **Guide** - Recommend direction with rationale
4. **Resource** - Provide links for deep implementation

**Not Research Goals:**
1. Read everything ever written on the topic
2. Become an expert before starting
3. Achieve perfect certainty
4. Eliminate all risk

**"Research reduces uncertainty to acceptable levels, not zero."**
