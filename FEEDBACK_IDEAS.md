# Areas that could be added/improved

1. Building out a full tests first deployment that helps the feature builds and know what tests need passed before it can commit/finish feature.
2. A better prime function that is more effiecent with our token usage. Right now on large codebases this can be pretty rough.



# Company issues

1. It feels like everyone is using AI but everyone is doing something different. 
    1. Cowork is in beta right now and can probably help out any not developers who work on files regularly.
1. All developers should use a similar-ish system if we are not going to say each person is in-charge of a particular project.


# Possible solutions

## GET SHIT DONE (GSD) - Primary Candidate
- **Link:** https://github.com/glittercowboy/get-shit-done
- **Install:** `npx get-shit-done-cc`
- **What it is:** Meta-prompting and context engineering system that solves "context rot"
- **Key Features:**
  - 6-stage workflow: Init → Discuss → Plan → Execute → Verify → Complete
  - Fresh 200k context per task execution (prevents quality degradation)
  - Multi-agent orchestration (4 parallel research agents, planner/checker loop)
  - XML structured tasks with `<verify>` and `<done>` tags
  - Automatic atomic git commits per task
  - `STATE.md` for session persistence across interruptions
  - `pause-work` / `resume-work` commands
- **Solves Priority 1 Goals:**
  - Session Management → `STATE.md` + pause/resume
  - Multi-Session Architecture → Fresh context per task
  - Token Budget → Never fills context (automatic management)
  - Spec Creation → `discuss-phase` + `plan-phase` workflow
- **Recommendation:** Try on a real project before deciding to adopt, borrow concepts, or stay with PIV
- **Full Analysis:** See `.agents/research/GSD-VS-PIV-ANALYSIS.md`
- **Added:** 2026-01-26


# Future Exploration (Worth Watching)

## claude-sneakpeek - Multi-Agent Orchestration
- **Link:** https://github.com/mikekelly/claude-sneakpeek
- **What it is:** Parallel Claude Code installation unlocking experimental features
- **Key Features:**
  - Swarm mode - Native multi-agent orchestration with TeammateTool
  - Delegate mode - Task tool with background agent spawning
  - Team coordination - Messaging and task ownership between agents
- **Relevance:** Could inform multi-session architecture and compound skills design
- **Status:** Experimental/unofficial - features are built-in but feature-flagged
- **Recommendation:** Worth experimenting with separately, but don't adopt until Priority 1 goals complete. These features will likely come to mainline Claude Code eventually.
- **When to revisit:** After session management and token budget systems are implemented (Priority 1 complete)
- **Added:** 2026-01-26