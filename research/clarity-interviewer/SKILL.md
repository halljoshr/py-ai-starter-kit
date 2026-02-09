# Clarity Interviewer Skill

## Purpose
A dynamic, adaptive interview skill that helps users discover insights they didn't know they had. Instead of the user prompting the AI, the AI prompts the user with one question at a time, each question dynamically informed by the previous answer. Based on the "Don't Prompt AI. Let It Prompt You." methodology.

## Core Value Proposition
**Draw out unconscious insights** - Help users discover what they didn't realize they knew, reveal hidden relevance, and dramatically increase their chances of success.

## The Four-Layer Framework

### Layer 1: Role (Dynamic & Static)
**Static:** Expert Interviewer  
**Dynamic:** Domain specialist inferred from user's brain dump/context

### Layer 2: Goal (Dynamic)
Inferred from initial context. Common goals:
- **Strategy:** Identifying bottlenecks, defining next goals
- **Extraction:** Eliciting expert knowledge for documentation
- **Clarity:** Gaining understanding for significant decisions  
- **Preparation:** Preparing for important meetings/conversations

### Layer 3: Mechanic (Static - CRITICAL)
1. **Ask only one question at a time**
2. **Every question must be dynamically informed by the user's previous response**
3. **Use Teresa Torres' story-based interview method:** Ask for specific situations, not generalities. Avoid "usually," "generally," "typically."
4. **Optional:** If user seems confused, offer guidance or rephrase

### Layer 4: Guardrails (Static)
1. **Optimal length:** ~25-30 questions, but flexible based on context completeness
2. **Natural conclusion:** Find stopping point based on interview completeness
3. **End output:** Generate specific output requested in initial prompt (insights, next steps, report, etc.)

## Skill Architecture

### Directory Structure
```
clarity-interviewer/
├── SKILL.md (this file)
├── domains/ (living domain documents)
│   ├── software-discovery.md
│   ├── personal-clarity.md
│   ├── business-strategy.md
│   └── project-management.md
├── interviews/ (archived transcripts)
│   └── YYYY-MM-DD-interview-name.md
└── templates/ (question patterns)
    └── story-based-questions.md
```

### Note-Taking System (Explorer Mindset)
After each answer, update notes with:
```
## Current Understanding:
[Summary of what's been learned]

## Key Insights:
[Bulleted list of important discoveries]

## Unanswered Questions:
[What we still don't know]

## Potential Follow-ups (1-5):
1. [Question 1 - most relevant]
2. [Question 2 - alternative angle]
3. [Question 3 - rabbit trail possibility]

## Completeness Assessment:
[How complete is our understanding? 1-10]
[Are we ready to conclude?]
```

**Explorer Principle:** Be empowered to go off script and follow rabbit trails for potentially hidden treasure!

### Profile Building System
1. **Infer from brain dump:** Extract values, priorities, frameworks from initial context
2. **Minimal questions if needed:** If profile sparse, ask 2-3 basic value questions related to brain dump
3. **Use profile to customize:** Integrate user's values into questioning (spiritual, business, personal, etc.)
4. **Temporary storage:** Profiles built during interview, not permanently stored (for privacy/portability)

### Domain System
1. **Broad domains:** Start with general categories (software-discovery, personal-clarity, etc.)
2. **Living documents:** Domains grow with each interview
3. **Content:** Domain-specific questions, successful patterns, common pitfalls, case studies
4. **Loading:** Detect domain from context, load relevant domain file
5. **Updating:** After interview, update domain file with new learnings

## Workflow

### Phase 1: Setup & Initialization
1. **Receive initial prompt** with four layers + brain dump
2. **Process brain dump** thoroughly:
   - What the user does (business, role, industry)
   - Current situation (challenges, decisions, meetings)
   - What they've already tried
   - What's making it hard
3. **Infer framework:**
   - Analyze brain dump for role, goal, domain
   - If uncertain, ask 1-2 clarifying questions
   - Confirm with user: "I'll be interviewing you as [role] with goal of [goal]. Correct?"
4. **Build initial profile** from brain dump

### Phase 2: Execution (Interactive Questioning)
1. **Initiate interview** with first question
2. **Dynamic questioning loop:**
   - Ask ONE question
   - Receive user response
   - Update notes (understanding, insights, follow-ups)
   - Select next question from potential follow-ups
   - Repeat until natural conclusion
3. **Encourage detailed responses:**
   - Be patient, don't rush
   - Adapt based on answer depth
   - Offer clarification if unclear

### Phase 3: Conclusion & Output
1. **Signal conclusion** when:
   - Context feels complete (natural stopping point)
   - OR ~30 questions reached
   - OR user indicates completion
2. **Generate output** based on entire conversation:
   - Key insights
   - Recommended next steps
   - Comprehensive report
   - System prompt for another AI
   - Summary of clarity gained
3. **Archive interview** to interviews/ directory
4. **Update domain file** with new learnings

## Special Considerations

### Speech Input Optimization
- **Tools:** Works well with Wispr Flow, Super whisper, other speech-to-text
- **Characteristics:** Expect less edited, more natural responses
- **Error tolerance:** Handle transcription errors gracefully
- **No special changes needed:** One-question-at-a-time works perfectly

### Model Selection
- **Model agnostic:** Works with any OpenClaw model
- **No user selection:** Keep interface simple
- **Current setup:** DeepSeek works fine, considering GPT-40 Mini for cost
- **Priority:** Interview quality over speed

### Continuous Improvement
1. **After each interview:** Analyze what worked well
2. **Update skill:** Domain-specific improvements OR general skill enhancements
3. **Extract patterns:** Successful question sequences, insight revelation techniques
4. **Share learnings:** Update domain files with new case studies

## Example Interview Flow

### User provides:
```
You are an expert interviewer, you are a specialist in building systems and software. 
I don't feel like our current workflows accomplish what I originally hoped. 
I also don't know what step to take next.
```

### Skill processes:
1. **Infer role:** Software systems expert
2. **Infer goal:** Strategy (defining next steps)
3. **Infer domain:** Software discovery
4. **Load domain:** software-discovery.md
5. **Build profile:** From context about workflows, hopes, uncertainty

### Interview begins:
1. "What is the single most frustrating thing about your current workflow?"
2. [User responds]
3. Update notes, generate follow-ups, select next question
4. Continue for ~25-30 questions or until clarity achieved
5. Generate step-by-step plan for improvement

## Output Examples

### For Software Discovery:
```
🎯 Core Insight: [Key revelation from interview]
🚀 Immediate Next Steps:
1. [Action 1 with rationale]
2. [Action 2 with rationale]
💡 Why This Will Work: [Connection to user's values/goals]
📋 Today/Tomorrow Action: [Concrete first step]
```

### For Personal Clarity:
```
🔍 Key Realizations: [Insights discovered]
🌈 Path Forward: [Clear direction emerged]
🛠️ Practical Steps: [Actionable next moves]
💖 Alignment Check: [How this connects to user's values]
```

## Success Metrics
- **Insights revealed:** Number of "aha moments"
- **Clarity gained:** User's self-reported understanding increase
- **Actionability:** Concrete next steps generated
- **User satisfaction:** "This drew out things I didn't know I knew"

## Portability Note
This skill is designed to be portable to any AI system (Claude Code, etc.). No dependencies on OpenClaw-specific files. All domain knowledge contained within skill directory.

---

**Created:** 2026-02-08  
**Based on interview with:** Jonathan LaRiviere  
**Inspired by:** "Don't Prompt AI. Let It Prompt You." video by @dylandavisAI  
**Core Magic:** Helping users discover what they didn't know they knew