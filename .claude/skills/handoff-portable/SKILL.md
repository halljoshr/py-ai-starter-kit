# Handoff Skill (Portable)

**Trigger:** User says "handoff", "/handoff", "create handoff", "save session", or similar end-of-session language

**Purpose:** Capture session state, update project tracking, and create a handoff for the next session.

---

## Overview

This skill provides a **flexible handoff system** that adapts to any project structure. It supports:

- **Minimal mode** — just save conversation logs (good for any project)
- **Structured mode** — full state tracking with multiple files (good for complex projects)
- **Custom mode** — user-defined files and sections via config

The skill auto-detects your project structure and uses sensible defaults. Projects can customize behavior with a `.handoff.yaml` config file.

---

## Quick Start

### For Any Project (Minimal Mode)

No setup required. The skill will:
1. Ask you what happened this session
2. Save a conversation log to `docs/sessions/` or `.sessions/`
3. Done

### For Structured Projects

Create `.handoff.yaml` in your project root:

```yaml
mode: structured
files:
  state: HANDOFF.md
  memory: .claude/memory/MEMORY.md
  logs: docs/sessions/

sections:
  state:
    - current_status
    - next_task
    - blockers
  memory:
    - session_log
    - decisions
```

---

## Configuration

### Config File Location

The skill looks for config in this order:
1. `.handoff.yaml` in project root
2. `.handoff.json` in project root
3. `.claude/handoff.yaml`
4. Auto-detect based on existing files

### Config Schema

```yaml
# Operation mode: minimal | structured | custom
mode: structured

# Files to maintain
files:
  # Primary state file (optional)
  state: HANDOFF.md

  # Long-term memory file (optional)
  memory: .claude/memory/MEMORY.md

  # Conversation logs directory (required)
  logs: docs/sessions/

  # Additional tracking files (optional)
  extra:
    - DECISIONS.md
    - BACKLOG.md

# Sections to maintain in each file
sections:
  state:
    - last_updated
    - current_status
    - next_task
    - blockers
    - recent_changes

  memory:
    - session_log
    - decisions
    - open_questions

  # Section format: "## {section}" or "# {section}" (auto-detected)
  heading_level: 2

# Conversation log format
logs:
  # Numbering: sequential | date | none
  numbering: sequential

  # Filename pattern (variables: {number}, {date}, {slug})
  pattern: "{number:03d}-{slug}.md"

  # Template sections
  template:
    - summary
    - decisions
    - accomplishments
    - next_steps

# Project metadata (optional, used in templates)
project:
  name: My Project
  type: software  # software | research | docs | mixed

# Limits and warnings
limits:
  memory_lines: 200  # Warn if memory file exceeds this
  session_length: 5000  # Warn if session log exceeds this many words
```

### Built-in Profiles

Instead of writing full config, use a profile:

```yaml
profile: software-project
# Options: minimal | software-project | research | documentation
```

**Minimal:**
```yaml
mode: minimal
files:
  logs: .sessions/
logs:
  numbering: date
  pattern: "{date}-session.md"
```

**Software Project:**
```yaml
mode: structured
files:
  state: HANDOFF.md
  memory: .claude/memory/MEMORY.md
  logs: docs/sessions/
sections:
  state: [current_status, next_task, blockers, recent_changes]
  memory: [session_log, decisions, open_questions]
logs:
  numbering: sequential
  pattern: "{number:03d}-{slug}.md"
```

**Research:**
```yaml
mode: structured
files:
  state: STATUS.md
  memory: NOTES.md
  logs: sessions/
sections:
  state: [current_focus, findings, next_questions]
  memory: [session_log, insights, references]
```

**Documentation:**
```yaml
mode: minimal
files:
  logs: writing-sessions/
logs:
  numbering: date
  pattern: "{date}.md"
  template: [summary, content_added, next_topics]
```

---

## How It Works

### Step 1: Detect Configuration

1. Look for `.handoff.yaml` or `.handoff.json`
2. If not found, auto-detect based on existing files:
   - If `HANDOFF.md` exists → use structured mode
   - If `.sessions/` exists → use minimal mode
   - Otherwise → ask user to choose

### Step 2: Capture Session Summary

Ask the user (or infer from context):
- **What was accomplished?**
- **What decisions were made?**
- **What's next?**
- **Any blockers or open questions?**

### Step 3: Update Files

**Minimal mode:**
- Save conversation log only

**Structured mode:**
- Update state file (e.g., `HANDOFF.md`)
- Update memory file (e.g., `MEMORY.md`)
- Save conversation log
- Update any extra files defined in config

### Step 4: Verify Consistency

Check that:
- All required files were updated
- Cross-references are consistent (if applicable)
- File sizes are within limits
- Next task is clear and actionable

### Step 5: Present Summary

Show formatted handoff summary:
```
## Session Handoff Complete

**Session:** [Title]
**Accomplished:** [Summary]
**Decisions:** [Key decisions]
**Next:** [Clear next step]

**Files Updated:**
- HANDOFF.md
- MEMORY.md
- docs/sessions/042-feature-implementation.md

**Status:** Ready for next session
```

---

## File Update Logic

### State File (e.g., HANDOFF.md)

Update or create sections defined in `sections.state`:

```markdown
## Last Updated
2026-02-13

## Current Status
[Auto-updated from session summary]

## Next Task
[Clear, actionable next step]

## Blockers
[Any blocking issues]

## Recent Changes
- 2026-02-13: Completed feature X
- 2026-02-12: Research Y
```

**Update strategy:**
- `last_updated` → replace with current date
- `current_status` → replace with new status
- `next_task` → replace with new next task
- `blockers` → replace or append
- `recent_changes` → prepend new entry (keep last 5-10)

### Memory File (e.g., MEMORY.md)

Update or create sections defined in `sections.memory`:

```markdown
## Session Log
- [042] 2026-02-13 — Feature implementation complete
- [041] 2026-02-12 — Research phase Y
- [040] 2026-02-11 — Architecture design

## Decisions
**Feature X implementation (042):** Use approach A over B because...
**Architecture pattern (040):** Chose pattern Y for...

## Open Questions
- How should we handle edge case Z? (opened in 042)
```

**Update strategy:**
- `session_log` → prepend new entry with link to conversation log
- `decisions` → append new decisions from this session
- `open_questions` → remove resolved, add new ones

### Conversation Log

Create new file in logs directory:

```markdown
# [Session Title]

**Date:** 2026-02-13
**Session:** 042 (or date-based ID)

## Summary

[2-3 sentence summary]

## Decisions

- [Decision 1 with rationale]
- [Decision 2 with rationale]

## Accomplishments

- [What was built/researched]
- [Key outcomes]

## Next Steps

- [Next task from state file]

## Transcript

[Key exchanges or full transcript]
```

**Filename generation:**
- Sequential: `042-feature-implementation.md`
- Date-based: `2026-02-13-feature-implementation.md`
- Slug generated from session title

---

## Usage Examples

### Example 1: New Project (Auto-Setup)

**User:** "handoff"

**Skill:**
1. Detects no config, no existing files
2. Asks: "What tracking structure do you want? (minimal/structured/custom)"
3. User chooses "minimal"
4. Creates `.sessions/` directory
5. Captures session summary
6. Saves first log: `.sessions/2026-02-13-initial-session.md`
7. Offers to create `.handoff.yaml` for future sessions

### Example 2: Existing Structured Project

**User:** "handoff"

**Skill:**
1. Reads `.handoff.yaml` (or auto-detects `HANDOFF.md`)
2. Captures session summary
3. Updates `HANDOFF.md` sections
4. Updates `MEMORY.md` session log
5. Saves `docs/sessions/042-implementation.md`
6. Verifies all files consistent
7. Presents summary

### Example 3: Custom Workflow

**Config (.handoff.yaml):**
```yaml
mode: custom
files:
  state: STATUS.txt
  logs: archive/
logs:
  numbering: none
  pattern: "session-{date}.txt"
  template: [summary, next]
```

**Skill:**
1. Updates `STATUS.txt` (freeform, just appends)
2. Saves `archive/session-2026-02-13.txt` with minimal template
3. Done

---

## Section Matching Logic

The skill intelligently finds and updates sections:

1. **Exact match:** `## Next Task` → `sections.state.next_task`
2. **Normalized match:** `## Next task` or `## NEXT TASK` → `next_task`
3. **Fuzzy match:** `## Next Steps` → `next_task` (common variations)
4. **Create if missing:** If section not found, append at end

**Common section aliases:**
- `next_task` → "Next Task", "Next Steps", "Next", "TODO"
- `current_status` → "Current Status", "Status", "Current Phase", "Now"
- `blockers` → "Blockers", "Blocked", "Issues", "Problems"
- `session_log` → "Session Log", "Sessions", "History", "Changelog"
- `decisions` → "Decisions", "Key Decisions", "Design Decisions"

---

## Edge Cases

### First Session (No Files Exist)

1. Create logs directory
2. If structured mode, create state and memory files from template
3. Save first conversation log as `001` or `2026-02-13` depending on mode

### User Changed Files Manually

Before updating, check if files were modified since last handoff:
- If yes: ask user if changes should be preserved or overwritten
- Default: merge (append new content, keep manual edits)

### Session Had No Decisions

Still create handoff, mark as "maintenance" or "exploratory" session.

### Multiple Topics in One Session

Offer to:
- Create single log with multiple sections
- Create multiple logs (e.g., `042a`, `042b`)

### Config File Invalid

Fall back to auto-detect or minimal mode, warn user about config error.

### Memory File Exceeds Limit

Warn user, suggest:
- Extract to separate topic files
- Archive old sessions
- Increase limit in config

---

## Migration Guide

### From Imp-Specific Handoff

If you have the old Imp-style handoff:

1. Create `.handoff.yaml`:
```yaml
profile: software-project
files:
  state: HANDOFF.md
  memory: .claude/memory/MEMORY.md
  logs: conversation-logs/
sections:
  state:
    - last_updated
    - current_phase
    - next_task
  memory:
    - conversation_log
    - key_decisions
    - research_needed
```

2. The skill will work with your existing files

### From No Handoff System

1. Choose a profile: `minimal` (safest) or `software-project` (most structure)
2. Let skill create initial files
3. Customize `.handoff.yaml` if needed

---

## Best Practices

### For Any Project

- **Run handoff at end of every session** — even 5-minute sessions
- **Make "next task" crystal clear** — future you will thank you
- **Capture decisions immediately** — don't trust your memory

### For Complex Projects

- **Use structured mode** — the overhead is worth it
- **Link files together** — state references logs, logs reference state
- **Review memory file regularly** — keep it under the limit
- **Archive old sessions** — move to `archive/` after 3-6 months

### For Research/Exploration

- **Use minimal mode** — less overhead, more flexibility
- **Date-based numbering** — easier to navigate
- **Focus on insights** — what did you learn, not just what you did

---

## Anti-Patterns

- ❌ Skipping handoff because "nothing important happened" — wrong, always handoff
- ❌ Vague next tasks — "continue working on X" is useless
- ❌ Not capturing decisions — "we'll remember" is a lie
- ❌ Over-engineering the config — start simple, add complexity only when needed
- ❌ Manual file editing without running handoff — breaks consistency

---

## Advanced Features

### Cross-Project Links

If you have related projects, link them in memory files:

```markdown
## Related Projects
- [ProjectX](../projectx/.claude/memory/MEMORY.md) — shared API patterns
- [ProjectY](../projecty/HANDOFF.md) — uses our library
```

### Custom Templates

Define custom Markdown templates in config:

```yaml
logs:
  custom_template: |
    # {title}

    **Date:** {date}
    **Duration:** {duration}

    ## What Happened
    {summary}

    ## Next Time
    {next_task}
```

### Hooks (Optional)

Run commands before/after handoff:

```yaml
hooks:
  pre_handoff:
    - git status
    - imp check  # validate before handoff
  post_handoff:
    - git add HANDOFF.md MEMORY.md
    - git commit -m "chore: session handoff"
```

---

## Troubleshooting

**"Section not found" warning:**
- Check section name in config matches file
- Use aliases or add custom mapping

**"File not writable" error:**
- Check file permissions
- Check if file is open in another program

**"Config invalid" error:**
- Validate YAML syntax
- Check required fields are present

**Memory file too large:**
- Extract to topic files
- Archive old sessions
- Increase limit or switch to database

---

## Success Criteria

A good handoff means:

1. ✅ Anyone can pick up the project and know what to do next
2. ✅ All decisions are documented with rationale
3. ✅ Session history is preserved and navigable
4. ✅ Files are consistent and up-to-date
5. ✅ No information was lost

**Test:** If you can't explain "what's next" in 2 sentences after handoff, it failed.

---

## Contributing

This is a portable skill. If you find patterns that work well for your projects, consider:
- Adding new built-in profiles
- Improving section aliases
- Adding project type templates
- Sharing your `.handoff.yaml` as an example

---

## License

Public domain. Use anywhere, modify freely, no attribution required.
