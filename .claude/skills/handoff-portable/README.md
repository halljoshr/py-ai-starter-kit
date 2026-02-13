# Handoff Skill (Portable Edition)

A **flexible, project-agnostic handoff system** for capturing session state and maintaining project continuity across AI-assisted work sessions.

## What This Does

- **Captures session state** at the end of every work session
- **Updates project tracking files** (configurable)
- **Saves conversation logs** for future reference
- **Maintains consistency** across handoff files
- **Adapts to any project structure** via config or auto-detection

## Quick Start

### Install

This skill is already installed at `~/.claude/skills/handoff-portable/`.

### Use in Any Project

Just say **"handoff"** or **"/handoff"** at the end of your session. The skill will:

1. **Auto-detect** your project structure or ask you to choose a mode
2. **Capture** what happened this session
3. **Update** tracking files (or create them)
4. **Save** a conversation log
5. **Verify** everything is consistent

**First time?** It will create a minimal `.sessions/` directory and save your first log.

**Have existing files?** It will detect `HANDOFF.md`, `MEMORY.md`, etc. and use them.

### Customize (Optional)

Create `.handoff.yaml` in your project root:

```yaml
profile: software-project
```

Or copy an example from `examples/`:

```bash
cp ~/.claude/skills/handoff-portable/examples/software-project.yaml .handoff.yaml
```

## Profiles

Choose a profile based on your project type:

| Profile | Best For | Tracking |
|---------|----------|----------|
| `minimal` | Small projects, experiments | Just conversation logs |
| `software-project` | Code projects | State + memory + logs |
| `research` | Research, exploration | Findings + insights + logs |
| `documentation` | Writing, content | Content tracking + logs |

## Examples by Project Type

### Example 1: Quick Script or Experiment

No config needed. Just use the skill:

```
You: "handoff"
Skill: "What happened this session?"
You: "Built a data parser"
Skill: Creates .sessions/2026-02-13-data-parser.md
```

**Result:** One log file, zero overhead.

### Example 2: Software Project

Create `.handoff.yaml`:
```yaml
profile: software-project
```

Use the skill:
```
You: "handoff"
Skill: Captures session, updates HANDOFF.md, MEMORY.md, saves log
```

**Result:** Full state tracking, decision capture, linked files.

### Example 3: Research Project

Create `.handoff.yaml`:
```yaml
profile: research
files:
  state: STATUS.md
  memory: RESEARCH-NOTES.md
  logs: sessions/
```

Use the skill:
```
You: "handoff"
Skill: Updates STATUS.md with findings, logs research questions
```

**Result:** Research-optimized tracking with insights and references.

## File Structure

### Minimal Mode

```
your-project/
├── .sessions/
│   ├── 2026-02-13-initial-work.md
│   └── 2026-02-14-feature-x.md
└── (your project files)
```

### Structured Mode (Software)

```
your-project/
├── .handoff.yaml
├── HANDOFF.md              # Current state, next task
├── .claude/
│   └── memory/
│       └── MEMORY.md       # Long-term memory, decisions
├── docs/
│   └── sessions/
│       ├── 001-scaffolding.md
│       ├── 002-feature-x.md
│       └── 003-bug-fix.md
└── (your project files)
```

### Structured Mode (Research)

```
your-research/
├── .handoff.yaml
├── STATUS.md               # Current focus, findings
├── RESEARCH-NOTES.md       # Insights, methodology
├── REFERENCES.md           # Citations
├── sessions/
│   ├── 2026-02-13-lit-review.md
│   └── 2026-02-14-experiment-1.md
└── (your research files)
```

## Configuration Options

See `SKILL.md` for full config reference.

**Quick reference:**

```yaml
mode: structured | minimal | custom

files:
  state: HANDOFF.md
  memory: MEMORY.md
  logs: docs/sessions/

sections:
  state: [current_status, next_task, blockers]
  memory: [session_log, decisions]

logs:
  numbering: sequential | date | none
  pattern: "{number:03d}-{slug}.md"
```

## Migration from Imp-Style Handoff

If you're using the Imp-specific handoff skill:

1. Copy the Imp example config:
```bash
cp ~/.claude/skills/handoff-portable/examples/imp-style.yaml .handoff.yaml
```

2. Your existing `HANDOFF.md` and `MEMORY.md` will work as-is

3. Start using `/handoff` — it will detect your structure

## When to Use This

**Use at the end of EVERY session where you:**
- Wrote code
- Made decisions
- Researched anything
- Changed direction
- Fixed bugs
- Had insights

**Even 5-minute sessions.** Future you will thank present you.

## What Gets Captured

The skill captures:

1. **What happened** — summary of the session
2. **Decisions made** — architectural, design, approach choices
3. **Next task** — clear, actionable next step
4. **Blockers** — anything preventing progress
5. **Open questions** — things to figure out later

## Best Practices

### Do This ✅

- Run handoff at the end of **every session**
- Make "next task" **crystal clear** (specific file, line, action)
- Capture decisions **with rationale** ("we chose X because Y")
- Use **minimal mode** for simple projects (don't over-engineer)
- Review memory files **regularly** (keep them current)

### Don't Do This ❌

- Skip handoff because "nothing important happened"
- Write vague next tasks ("continue working on X")
- Forget to capture decisions ("we'll remember")
- Over-configure before you know what you need
- Edit tracking files manually without running handoff

## Advanced Usage

### Multiple Related Projects

Link projects in memory files:

```markdown
## Related Projects
- [Frontend](../frontend/HANDOFF.md)
- [Backend](../backend/HANDOFF.md)
- [Shared Types](../types/.sessions/)
```

### Custom Templates

Define custom log templates in config:

```yaml
logs:
  custom_template: |
    # {title}
    **Date:** {date}

    ## Summary
    {summary}

    ## Next
    {next_task}
```

### Git Integration (Optional)

Add hooks to auto-commit:

```yaml
hooks:
  post_handoff:
    - git add HANDOFF.md MEMORY.md
    - git commit -m "chore: session handoff"
```

## Troubleshooting

**"No config found, using minimal mode"**
→ Normal! The skill works without config. Create `.handoff.yaml` if you want more structure.

**"Section not found in HANDOFF.md"**
→ The skill will create missing sections automatically. Or check your section names match the config.

**"Memory file is getting large"**
→ Consider archiving old sessions or extracting to topic files.

**"Can't write to file"**
→ Check file permissions and that the file isn't open elsewhere.

## Files in This Directory

```
handoff-portable/
├── SKILL.md                    # Full skill implementation
├── README.md                   # This file
└── examples/
    ├── minimal.yaml            # Minimal tracking
    ├── software-project.yaml   # Full software project
    ├── research.yaml           # Research workflow
    ├── documentation.yaml      # Writing/docs workflow
    └── imp-style.yaml          # Imp project compatibility
```

## Philosophy

This skill embodies a few core principles:

1. **No handoff, no memory** — If you don't capture it, it didn't happen
2. **Make next steps obvious** — Your future self is a different person
3. **Decisions need rationale** — "What" is useless without "why"
4. **Adapt to the project** — Not every project needs the same tracking
5. **Start simple, add complexity only when needed** — Minimal mode is fine

## Credits

Originally developed for the [Imp](https://github.com/halljoshr/imp) project, then generalized for universal use.

## License

Public domain. Use it, fork it, modify it, share it. No attribution required.

---

**Questions?** Check `SKILL.md` for detailed documentation.

**Want to improve it?** The skill is designed to be extended. Add your own profiles, templates, and conventions.
