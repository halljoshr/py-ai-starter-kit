# Clarity Interviewer Skill - Interview Notes

## Initial Context Analysis

**User:** Jonathan LaRiviere
**Date:** 2026-02-06
**Skill Goal:** Create a "Clarity Interviewer AI" skill based on the "Don't Prompt AI. Let It Prompt You." methodology

### Key Points from Initial Context:

1. **User Experience:** Had an "extremely enlightening" experience with this interview technique in OpenClaw/Telegram
2. **Super Power:** Technique pulls out insights "I didn't even know were relevant"
3. **Input Method Preference:** Speech dictation (Wispr Flow, Super whisper) - speaking gives better context than typing
4. **Current Pain Points:**
   - OpenClaw workflows/dashboard not accomplishing original hopes
   - Unsure of next steps
   - Need to offload brain's effort of remembering when/what order to do things
   - Apple Reminders is just an inbox, not "smart" like OpenClaw could be
   - Doesn't understand OpenClaw's myriad capabilities/architecture

5. **Skill Requirements from Video:**
   - Four-layer framework (Role, Goal, Mechanic, Guardrails)
   - Dynamic, adaptive interview (one question at a time)
   - 25-30 question optimal length
   - Specific output at end (insights, next steps, report, etc.)
   - Fast model priority for smooth conversation

### Initial Questions to Explore:
1. What specific aspects of the original OpenClaw/Telegram experience were most valuable?
2. How should this skill integrate with existing OpenClaw workflows?
3. What output formats would be most useful?
4. How to handle the speech dictation preference?
5. What domain specializations are needed?

---

## Question 1 Response Analysis

**Key Insights from Jonathan's Answer:**

1. **Target Date vs Due Date Distinction:** The interview revealed this important conceptual separation that wasn't initially apparent.

2. **Teresa Torres' Story-Based Interview Method:**
   - Ask for specific situations, not generalities
   - Avoid "usually," "generally," "typically" questions
   - Humans have biased memories and are poor at generalizing
   - Best discovery interviews use this method

3. **Spiritual Dimension Discovery:**
   - Tasks have spiritual significance
   - Can be categorized by spiritual goals (e.g., stewardship)
   - This emerged through specific situation questioning

**Implications for Skill Design:**
- Must incorporate story-based interview techniques
- Need to avoid generalization questions
- Should explore deeper dimensions (spiritual, emotional, etc.)
- Structure questions around specific past experiences

**Follow-up Areas:**
- How to implement Teresa Torres' method in AI questioning
- How to surface spiritual/goal dimensions systematically
- How to structure questions for specific situation recall

---

## Question 2 Response Analysis

**Key Insights:**

1. **Hybrid Approach Preferred:**
   - Templates/patterns for consistency and improvement over time
   - Dynamic generation for situation-specific questions

2. **Empowered Triad Role:**
   - AI should act as empowered product manager, designer, and engineer combined
   - Following Marty Cagan's "Inspired" approach
   - All three roles "present in the room" during interview

3. **Domain-Specific Simulation:**
   - For software/experience creation: simulate engineer/designer/PM triad
   - For other domains (house projects, etc.): different role configurations
   - Role simulation should be context-appropriate

**Implications for Skill Design:**
- Need role configuration system based on interview domain
- Marty Cagan "Inspired" methodology integration
- Template library + dynamic question generation
- Domain detection for appropriate role simulation

**Technical Considerations:**
- How to detect interview domain (software vs other)
- How to configure role simulation dynamically
- Template management system
- "Empowered" questioning style implementation

---

## Question 3 Response Analysis

**Key Insight:**
- Primary use case: Software products we create together
- Focus is on our collaborative software development projects
- Other domains are secondary consideration

**Implication:**
- Can focus primarily on software development interview configuration
- Engineer/designer/PM triad is the default/most important role set
- Skill can be optimized for software product discovery

**Refined Focus:**
- Skill will be tailored for software product interviews
- Marty Cagan "Inspired" methodology as primary framework
- Teresa Torres story-based techniques within software context
- Target date vs due date, spiritual dimensions in software tasks

**Open Questions:**
- What specific software products do we envision?
- How does this integrate with our existing OpenClaw work?
- What's the relationship between this skill and our dashboard/task system?

---

## Question 4 Response Analysis

**Key Insight:**
- Dashboard provided information but lacked context for good decision-making
- Specific pain: Information without context = poor decisions
- Transcript available for deeper analysis

**Implication for Skill Design:**
- Clarity Interviewer should help uncover what "context" means for decision-making
- Need to understand gap between information display and actionable insight
- Transcript analysis could reveal specific patterns of missing context

**Potential Root Causes:**
- Dashboard shows data but not relationships between data points
- Missing prioritization context (why this task now vs later)
- Lack of energy/context matching (right task for current mental state)
- No connection to spiritual/meaning dimensions previously mentioned

**Follow-up Direction:**
- Need to explore specific decision-making failures
- Understand what contextual information is missing
- How dashboard could better support decision-making

---

## Question 5 Response Analysis

**Key Insight:**
- Transcript provided of the original valuable interview
- Dashboards were "basic and primitive" - question not relevant to current skill design
- The real value was in the interview process itself, not the dashboard output

**Transcript Analysis (Initial Scan):**
- 27 questions asked in original interview
- Revealed: target date vs due date distinction, spiritual dimensions, Teresa Torres methodology
- Output: Step-by-step plan for conversational task system
- User found it "absolutely illuminating" and "elated"

**Implication for Skill Design:**
- Skill should replicate THIS interview experience
- Focus on conversational discovery, not dashboard display
- Capture the magic of the original transcript
- Implement the 4-layer framework from video

**Skill Requirements from Transcript:**
1. Conversational task interviewing
2. Spiritual dimension integration
3. Trust-building through transparency
4. "Little by little" execution support
5. Connection to faith/stewardship

---

## Question 6 Response Analysis

**Key Insights:**

1. **General-Purpose Design:**
   - Must adapt to any situation/domain
   - Not limited to software discovery
   - Flexible framework for various interview types

2. **Continuous Improvement System:**
   - Learn from each interview
   - Update skill based on what worked well
   - Apply learned principles to future interviews

3. **Post-Interview Enhancement:**
   - After each interview: improve the skill
   - Domain-specific template/pattern improvements
   - General skill improvements for all future uses

4. **Software Discovery Specialization:**
   - For software projects: apply learned principles
   - Build domain-specific expertise over time
   - Capture successful patterns from software interviews

**Implications for Skill Architecture:**

1. **Modular Design:**
   - Core interview engine
   - Domain-specific modules
   - Template/pattern library

2. **Learning System:**
   - Post-interview analysis
   - Pattern extraction
   - Template refinement

3. **Adaptive Framework:**
   - Detect interview domain
   - Apply relevant patterns
   - Learn and improve

**Technical Requirements:**
- Skill state persistence
- Template versioning
- Domain classification
- Pattern recognition

---

## Question 7 Response Analysis

**Key Insights on Speech Input:**

1. **Speech-to-Text Tools:**
   - Wispr Flow, Super whisper mentioned
   - Extremely capable voice models
   - Convert voice to text accurately

2. **One Question at a Time Advantage:**
   - Allows extensive context per question
   - Interviewee can elaborate fully
   - Context informs next question dynamically

3. **Speech vs Text Characteristics:**
   - **Transcription errors possible** - need error tolerance
   - **Intonation lost** - can't hear vocal cues
   - **Less edited/unstructured** - more natural, raw thoughts
   - **More context-rich** - speaking reveals more than typing

4. **Minimal Process Changes:**
   - Interview process largely unchanged
   - Same one-question-at-a-time approach
   - Same dynamic adaptation

**Implications for Skill Design:**

1. **Error Tolerance:**
   - Handle transcription errors gracefully
   - Clarify if response seems garbled
   - Don't assume perfect transcription

2. **Context Interpretation:**
   - Expect less structured responses
   - Handle natural speech patterns
   - Extract meaning from verbose answers

3. **Question Design:**
   - Clear, unambiguous questions
   - Avoid complex phrasing that might not transcribe well
   - Single focus per question

4. **Clarification Protocol:**
   - If response seems unclear, ask for clarification
   - "I want to make sure I understood correctly..."
   - Rephrase key points for confirmation

**No Special Optimization Needed:**
- Process remains the same
- One question at a time works well for speech
- Dynamic adaptation based on response

**Key Principle:** The interview methodology (one question, dynamic adaptation) already works perfectly for speech input. No major changes needed.

---

## Question 8 Response Analysis

**Key Insights on Framework Configuration:**

1. **Primary Method: Infer from Context**
   - Analyze initial brain dump/context
   - Extract role, goal, domain from user's description
   - Dynamic inference based on content

2. **Secondary Method: Request Clarification**
   - If inference uncertain, ask clarifying questions
   - "To help me interview you effectively, could you clarify..."
   - Suggestions for domain expertise needed

3. **Interactive Setup:**
   - Start with brain dump
   - Analyze and infer framework
   - Request clarification if needed
   - Confirm with user before proceeding

4. **No Pre-Configuration Interface:**
   - Don't force users through configuration steps
   - Start natural, infer as much as possible
   - Only interrupt for essential clarifications

**Implications for Skill Design:**

1. **Context Analysis Engine:**
   - Parse initial brain dump
   - Identify key themes, domains, goals
   - Extract implicit role requirements

2. **Clarification Protocol:**
   - Confidence threshold for inference
   - When uncertain, ask targeted questions
   - Keep clarification minimal (1-2 questions max)

3. **Domain Suggestion:**
   - Based on context, suggest possible domains
   - "Based on what you've shared, this seems like a [domain] interview. Is that correct?"
   - Allow user to confirm or correct

4. **Transparent Process:**
   - Show inferred framework to user
   - "I'll be interviewing you as a [role] with the goal of [goal]"
   - Get confirmation before starting questions

**Example Flow:**
1. User provides brain dump
2. Skill analyzes: "This appears to be software product discovery"
3. Skill infers: Role=Software PM/Engineer/Designer, Goal=Requirements extraction
4. Skill asks: "I'll be interviewing you as a software product expert. Does that sound right?"
5. User confirms or corrects
6. Interview begins

**Key Principle:** Start natural, infer intelligently, clarify minimally, confirm transparently.

---

## Question 9 Response Analysis

**Key Insights on Model Selection:**

1. **User Perspective:**
   - Interviewee should not care about model
   - No model selection exposed to user
   - Keep interview simple and focused

2. **Current Setup:**
   - DeepSeek configured and working
   - Speed acceptable for price/value
   - Considering GPT-40 Mini for cost savings

3. **Skill Design Principle:**
   - **No model selection interface** for users
   - Use whatever model is configured in OpenClaw
   - Interview experience should be model-agnostic

4. **Performance Considerations:**
   - Current DeepSeek speed is "a little slow but worth it"
   - Cost optimization considered (GPT-40 Mini)
   - But not exposed to interviewee

**Implications for Skill Design:**

1. **Model Agnostic:**
   - Skill works with any OpenClaw model
   - No model-specific logic
   - Universal interview protocol

2. **Speed Tolerance:**
   - Accept current response times
   - No special optimizations for speed
   - Focus on interview quality over speed

3. **Cost Transparency:**
   - Model cost considerations handled at system level
   - Not exposed during interview
   - User experience unaffected

4. **Simple Interface:**
   - Just start interview
   - No configuration, no model selection
   - Brain dump → analysis → questions

**Key Principle:** The interview skill should be completely model-agnostic. Whatever model OpenClaw is configured to use should work fine. No model selection exposed to users - keep it simple.

---

## Question 10 Response Analysis

**Key Insights on Interview Conclusion:**

1. **Flexible Length:**
   - No hard 30-question limit
   - Can be much shorter if circumstances allow
   - Model should find natural stopping point

2. **Intelligent Note-Taking System:**
   - Notes help model think several questions ahead
   - Build context to know when interview is complete
   - Surface or abandon questions based on context

3. **Question Generation in Notes:**
   - After each answer: document 1-5 potential follow-up questions
   - Questions stored in notes, not asked immediately
   - Prevents 30 questions becoming 150 questions

4. **Natural Conclusion Detection:**
   - Model was "pretty good at finding stopping point on its own"
   - Watch for completeness of context
   - Sense when core insights have been extracted

**Implications for Skill Design:**

1. **Note-Taking Framework:**
   - Structured note format
   - Section for potential follow-up questions
   - Context building and synthesis

2. **Question Management:**
   - Generate multiple potential questions
   - Select most relevant one for next question
   - Archive others in notes for possible later use

3. **Conclusion Intelligence:**
   - Monitor context completeness
   - Detect when core issues addressed
   - Natural stopping based on content, not count

4. **Flexible Guardrails:**
   - "Stop around 30 questions" as guideline, not rule
   - Allow shorter interviews when appropriate
   - Model discretion for optimal length

**Note-Taking Methodology:**
```
After each answer:
1. Analyze response for new insights
2. Update context understanding
3. Generate 1-5 potential follow-up questions
4. Select most relevant question for next
5. Track completeness of interview
```

**Key Principle:** Intelligent note-taking enables natural conclusion detection. Generate multiple questions but ask only one. Flexible length based on context completeness.

---

## Question 11 Response Analysis

**Key Insights on Note Structure:**

1. **Suggested Structure (Flexible):**
   - Current understanding
   - Key insights discovered
   - Unanswered questions
   - Potential follow-up questions (1-5)
   - Interview completeness assessment

2. **Explorer Mindset:**
   - Interviewer should be an "explorer"
   - Empowered to go off script
   - Follow rabbit trails for "hidden treasure"
   - Not too strict about methodology

3. **Balance Structure & Flexibility:**
   - Provide note framework as guide
   - Allow deviation when valuable
   - Structured enough for consistency
   - Flexible enough for exploration

**Implications for Skill Design:**

1. **Note Template (Suggested):**
   ```
   ## Current Understanding:
   [Summary of what's been learned]
   
   ## Key Insights:
   [Bulleted list of important discoveries]
   
   ## Unanswered Questions:
   [What we still don't know]
   
   ## Potential Follow-ups (1-5):
   1. [Question 1]
   2. [Question 2]
   3. [Question 3]
   
   ## Completeness Assessment:
   [How complete is our understanding? 1-10]
   [Are we ready to conclude?]
   ```

2. **Explorer Protocol:**
   - Use structure as starting point
   - Deviate when interesting trails appear
   - Return to structure when needed
   - Balance discovery with methodology

3. **Hidden Treasure Principle:**
   - Value unexpected insights
   - Follow interesting tangents
   - Allow creative exploration
   - Capture serendipitous discoveries

4. **Empowered Interviewer:**
   - Trust model's judgment
   - Allow off-script questioning
   - Encourage deep exploration
   - Value discovery over rigid process

**Key Principle:** Provide flexible note structure as guide, but empower interviewer as explorer to follow valuable rabbit trails and discover hidden treasures.

---

## Question 12 Response Analysis

**Key Insight:**
- User is satisfied with interview progress
- Open to additional questions or rabbit trails
- Willing to explore any remaining aspects

**Current Coverage Assessment:**
We've covered:
1. Purpose & value proposition
2. Methodology (4-layer framework)
3. Configuration (inference from context)
4. Model selection (agnostic approach)
5. Note-taking structure
6. Interview conclusion strategy
7. Explorer mindset

**Potential Rabbit Trails to Pursue:**

1. **Integration with OpenClaw:**
   - How does this skill interact with other OpenClaw features?
   - Where are interview outputs stored/used?

2. **Output Formats:**
   - What specific deliverables should interviews produce?
   - How are insights packaged for users?

3. **Skill Improvement System:**
   - Concrete mechanism for learning from interviews
   - How templates/patterns get updated

4. **Edge Cases:**
   - Handling uncooperative or confused interviewees
   - Technical failures or interruptions

5. **Spiritual Dimension Integration:**
   - How to systematically incorporate faith/stewardship
   - Template questions for spiritual discovery

**Completeness Assessment: 8/10**
- Core framework well-defined
- Some implementation details needed
- Integration aspects unclear

**Decision Point:** Pursue rabbit trails or conclude?

---

## Question 13 Response Analysis

**Key Insights on OpenClaw Integration:**

1. **Documentation Capture:**
   - Connect to existing project documentation OR generate new
   - Capture all context properly
   - Automatically save interview history to file for reference
   - Preserve original source of notes

2. **Skill Template Updates:**
   - Update skill templates based on learnings
   - But avoid bloating single skill file
   - Domain-specific reference files instead

3. **Domain Reference System:**
   - Separate files for each domain
   - Skill references domain file paths
   - AI can read relevant domain files
   - System for adding/enhancing domains

4. **Task/Workflow Generation:**
   - Dependent on interview content
   - Pulled from interview insights
   - Not hardcoded in skill
   - Flexible based on interview outcomes

**Implications for Skill Design:**

1. **File Management:**
   - Auto-save interview transcripts
   - Domain reference file system
   - Project documentation linking

2. **Modular Architecture:**
   ```
   clarity-interviewer/
   ├── SKILL.md (core engine)
   ├── domains/
   │   ├── software-discovery.md
   │   ├── personal-clarity.md
   │   └── business-strategy.md
   └── interviews/
       └── YYYY-MM-DD-interview-name.md
   ```

3. **Domain Detection & Loading:**
   - Detect interview domain from context
   - Load relevant domain reference file
   - Apply domain-specific patterns
   - Update domain file with new learnings

4. **Output Processing:**
   - Generate appropriate documentation
   - Create tasks if interview indicates
   - Trigger workflows as needed
   - All based on interview content

**Key Principle:** Modular domain system with auto-saved interviews. Skill core remains lean, domains expand independently. Outputs flexible based on interview insights.

---

## Question 14 Response Analysis

**Key Insights on Domain Files:**

1. **Living Documents Approach:**
   - Domain files should be living documents
   - Grow and evolve with each interview
   - Capture increasing domain expertise

2. **Broad Domain Categories:**
   - Project management (broad)
   - Software discovery (broad)  
   - Not overly specific domains
   - Flexible categorization

3. **Content Distribution:**
   - **Primary Skill Document:**
     - Successful interview patterns
     - Common pitfalls
     - General question libraries
     - Core methodology

   - **Domain-Specific Files:**
     - Domain-specific questions
     - Domain insights and patterns
     - Case studies/examples
     - Evolving expertise

4. **Hybrid Flexibility:**
   - Open to hybrid approach
   - Core templates that enhance
   - Living documents that grow
   - Balance structure with evolution

**Implications for Skill Design:**

1. **Domain File Structure:**
   ```
   # Domain: Software Discovery
   
   ## Domain Overview
   [Purpose, typical goals, common scenarios]
   
   ## Successful Patterns
   [What works well in this domain]
   
   ## Common Pitfalls  
   [What to avoid in this domain]
   
   ## Question Library
   [Domain-specific questions that work well]
   
   ## Case Studies
   [Examples from past interviews]
   
   ## Evolving Insights
   [New learnings from recent interviews]
   ```

2. **Growth Mechanism:**
   - After each interview: update relevant domain file
   - Add successful questions/patterns
   - Note new insights
   - Expand question library

3. **Broad vs Specific:**
   - Start with broad domains
   - Allow natural specialization
   - Domains can split if they grow too large
   - Organic organization

**Key Principle:** Living domain documents that grow with experience. Broad categories with evolving expertise. Core skill document for general patterns, domain files for specialized knowledge.

---

## Question 15 Response Analysis

**Key Insights on Spiritual/Personal Integration:**

1. **User-Specific Integration:**
   - Spiritual/faith integration important FOR YOU
   - Should pull from YOUR documentation/profile
   - Not universal - others may not want this

2. **Generalizable Principle:**
   - Every user has unique profile
   - Interview should pull from user's unique context
   - Custom integration based on user values

3. **Profile-Based Customization:**
   - Your profile: includes spiritual dimensions
   - Other profiles: different value systems
   - Interview adapts to user's documented values

4. **Not Hardcoded Spirituality:**
   - Don't hardcode spiritual module
   - Make it profile-driven
   - Flexible for different user types

**Implications for Skill Design:**

1. **User Profile System:**
   - Each user has profile document
   - Contains values, priorities, frameworks
   - Interviewer reads profile before/during interview

2. **Profile Content Examples:**
   - **Your profile:** spiritual goals, stewardship, faith integration
   - **Other profiles:** business values, personal goals, etc.
   - **Common elements:** core values, decision frameworks

3. **Adaptive Interviewing:**
   - Detect user from context
   - Load user profile
   - Integrate profile values into questions
   - Customize based on documented priorities

4. **Profile-Aware Questioning:**
   - "Based on your profile emphasizing stewardship, how does this task connect..."
   - "Given your documented business values, what aspects..."
   - Profile provides lens for interview

**Key Principle:** User profile-driven customization, not hardcoded modules. Your spiritual integration comes from your profile. Others get integration based on their documented values.

---

## Question 16 Response Analysis

**Key Insights on Profile Management:**

1. **Inference-Based Profiles:**
   - Profiles should be inferred and built during interviews
   - Start from brain dump/initial context
   - Learn user values through questioning

2. **Fallback Mechanism:**
   - If no profile exists, ask basic questions
   - Questions related to initial brain dump
   - Build profile dynamically

3. **Transferability Goal:**
   - Skill should work for any person
   - Not tied to OpenClaw-specific files
   - Portable to other AI systems (Claude Code, etc.)

4. **Profile Building Flow:**
   ```
   1. User provides brain dump
   2. AI infers initial profile from context
   3. If profile sparse, ask 2-3 basic value questions
   4. Build profile during interview
   5. Use profile to customize remaining questions
   ```

**Implications for Skill Design:**

1. **Profile Inference Engine:**
   - Analyze brain dump for values, priorities
   - Extract implicit profile elements
   - Build initial profile hypothesis

2. **Minimal Profile Questions:**
   - Only ask if profile is insufficient
   - "To help me understand your perspective better..."
   - "What values are most important in this situation?"
   - Keep to 2-3 questions max

3. **Portable Architecture:**
   - No dependency on OpenClaw-specific files
   - Self-contained skill package
   - Works in any AI system
   - You'll transfer files to Claude Code

4. **Profile Storage:**
   - Temporary within interview session
   - Not permanently stored (privacy/portability)
   - Rebuilt each interview if needed
   - Option to save if user wants continuity

**Key Principle:** Dynamic profile inference from brain dump, minimal questions if needed. Portable design for any AI system. Profiles built during interview, not pre-requisite.

---

## Question 17 Response Analysis

**Key Insight - Core Value Proposition:**
- **Most Exciting Aspect:** Drawing out insights users didn't realize they knew
- **Hidden Knowledge Revelation:** Things users didn't realize were important/relevant
- **Personal Validation:** "Even this interview did exactly that for me"
- **Success Amplification:** "Much higher chance of success achieving their goals"
- **Human Benefit Focus:** "Very excited to see how this can help people"

**The Magic Revealed:**
1. **Unconscious Knowledge Surfacing:** Accessing insights beneath conscious awareness
2. **Relevance Discovery:** Revealing connections users didn't see
3. **Personal Proof:** This interview itself demonstrated the value
4. **Success Catalyst:** Increases likelihood of achieving goals
5. **Human-Centered Design:** Ultimately about helping people

**Implication for Skill Essence:**
- The skill's core magic is **insight revelation**
- Not just information gathering, but **knowledge discovery**
- Creates **"aha moments"** for users
- **Transforms** understanding of problems/solutions
- **Empowers** users with self-knowledge

**Completeness Assessment: 95/100**
- Core value crystal clear
- Methodology well-defined
- Architecture designed
- Integration planned
- Human benefit emphasized

**Ready to conclude and create skill.**

---

## Interview Complete - Ready for Output