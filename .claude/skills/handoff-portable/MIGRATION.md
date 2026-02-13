# Migration Guide

How to migrate from project-specific handoff systems to the portable handoff skill.

---

## From Imp-Style Handoff

**You have:**
- `HANDOFF.md` with specific sections
- `.claude/memory/MEMORY.md`
- `conversation-logs/` with sequential numbering
- Custom section names like "What Has Been Decided"

**Migration steps:**

### 1. Copy the Imp config template

```bash
cd your-project
cp ~/.claude/skills/handoff-portable/examples/imp-style.yaml .handoff.yaml
```

### 2. Verify file paths match

Edit `.handoff.yaml` to match your actual paths:

```yaml
files:
  state: HANDOFF.md                          # ← Your state file
  memory: .claude/memory/MEMORY.md           # ← Your memory file
  logs: conversation-logs/                   # ← Your logs directory
```

### 3. Map your sections

Check your `HANDOFF.md` and `MEMORY.md` for section names. Update config:

```yaml
sections:
  state:
    - last_updated
    - last_phase_completed     # ← Your custom section
    - current_phase            # ← Your custom section
    - next_task
    - what_has_been_decided    # ← Your custom section

  memory:
    - current_phase
    - conversation_log
    - key_design_decisions     # ← Your custom section
    - research_still_needed    # ← Your custom section
```

### 4. Test it

```bash
# In Claude Code session
/handoff
```

The skill will:
- Read your config
- Find existing files
- Update sections in place
- Save new conversation log with next sequential number

### 5. Done!

Your existing files work as-is. The portable skill handles the same structure.

---

## From Manual Session Notes

**You have:**
- Random text files or docs
- No consistent structure
- Session notes scattered around
- Maybe a TODO.md or STATUS.md

**Migration steps:**

### 1. Choose a mode

**Option A: Start minimal** (recommended)

```bash
cd your-project
cat > .handoff.yaml << EOF
profile: minimal
EOF
```

This creates `.sessions/` and starts fresh. **Keep your old notes** as archive.

**Option B: Migrate existing notes**

1. Create structured files:
```bash
# Create state file
echo "## Current Status" > STATUS.md
echo "## Next Task" >> STATUS.md

# Create logs directory
mkdir -p docs/sessions
```

2. Copy best content from old notes into `STATUS.md`

3. Create config:
```yaml
profile: software-project
files:
  state: STATUS.md
  logs: docs/sessions/
```

### 2. Test it

```bash
/handoff
```

### 3. Archive old notes

```bash
mkdir archive-old-notes
mv *.txt archive-old-notes/
```

Keep the archive for reference, but use new system going forward.

---

## From Git Commit Messages Only

**You have:**
- Just git commits
- No session tracking
- No handoff system

**Migration steps:**

### 1. Start minimal

```bash
cd your-project
cat > .handoff.yaml << EOF
profile: minimal
EOF
```

### 2. Run handoff after every session

Instead of just:
```bash
git commit -m "add feature X"
```

Do:
```bash
# Work on feature X
# ...
/handoff  # ← Capture session state
# Then commit
git commit -m "feat: add feature X"
```

### 3. Gradually add structure

After a few sessions, if you want more tracking:

```bash
cp ~/.claude/skills/handoff-portable/examples/software-project.yaml .handoff.yaml
```

The skill will create `HANDOFF.md` and `MEMORY.md` automatically.

---

## From Notion/Obsidian/Roam

**You have:**
- Notes in external tool (Notion, Obsidian, Roam, etc.)
- Want to keep those notes
- But also want local handoff tracking

**Migration steps:**

### 1. Decide: Migrate or Parallel?

**Option A: Migrate to local files**
- Pro: Everything in one place, git-tracked
- Con: Lose external tool features

**Option B: Keep both**
- Pro: Keep external tool, add local tracking
- Con: Two sources of truth

### 2. If migrating:

```bash
# Export from external tool to markdown
# (Each tool has export options)

# Create local structure
mkdir -p docs/sessions

# Copy exported notes to docs/sessions/
# Rename to match handoff format:
# 001-topic.md, 002-topic.md, etc.

# Create config
cp ~/.claude/skills/handoff-portable/examples/software-project.yaml .handoff.yaml
```

### 3. If keeping both:

Use minimal mode for local tracking, link to external tool:

```yaml
mode: minimal
files:
  logs: .sessions/

# Add link in session logs
logs:
  template:
    - summary
    - next
    - external_links
```

In session logs, add:
```markdown
## External Links
- [Notion page](https://notion.so/project/...)
- [Obsidian vault](obsidian://open?vault=project)
```

---

## From README-only Projects

**You have:**
- Just a README.md
- Maybe a TODO section in README
- No formal tracking

**Migration steps:**

### 1. Keep README for "what it is", add handoff for "what's happening"

README = static project info
Handoff = dynamic session tracking

### 2. Start minimal

```bash
cat > .handoff.yaml << EOF
profile: minimal
EOF
```

### 3. Move TODO items to HANDOFF.md

Extract TODO from README:

**Before (README.md):**
```markdown
# My Project

## TODO
- [ ] Add tests
- [ ] Fix bug in parser
- [ ] Deploy to prod
```

**After:**

**README.md:**
```markdown
# My Project

A tool that does X.

## Status

See [HANDOFF.md](HANDOFF.md) for current status and next steps.
```

**HANDOFF.md:**
```markdown
## Next Task
Add tests for parser module

## Backlog
- Fix bug in parser
- Deploy to prod
```

---

## From Issue Tracker Only (GitHub/Linear/Jira)

**You have:**
- All tracking in issue tracker
- No local documentation
- Want to add session notes

**Migration steps:**

### 1. Use minimal mode for session logs only

```yaml
profile: minimal
files:
  logs: .sessions/
```

### 2. Link issues in session logs

```markdown
# Session Log

**Date:** 2026-02-13

## Summary
Fixed authentication bug

## Issues
- Closes #123
- Related to #124

## Next
Continue with #125 (API refactor)
```

### 3. Optional: Sync with issue tracker

Add hook to update issues:

```yaml
hooks:
  post_handoff:
    - gh issue comment $ISSUE_NUMBER --body "Session complete. See .sessions/latest.md"
```

---

## From Nothing (First Project)

**You have:**
- Brand new project
- No tracking system
- Not sure what you need

**Migration steps:**

### 1. Just start using it

No config needed. Say `/handoff` at end of first session.

### 2. Skill will guide you

It will ask:
- "What tracking do you want?" → Choose `minimal`
- "What happened this session?" → Answer briefly

It creates `.sessions/2026-02-13-initial-work.md`

### 3. Evolve as needed

After a few sessions, if you want more structure:
```bash
cp ~/.claude/skills/handoff-portable/examples/software-project.yaml .handoff.yaml
```

**Start simple. Add complexity only when you need it.**

---

## Config Validation Checklist

After creating `.handoff.yaml`, verify:

- [ ] File paths exist or can be created
- [ ] Section names match your existing files (if any)
- [ ] Numbering format matches existing logs (if any)
- [ ] Profile matches your project type
- [ ] YAML syntax is valid (use `yamllint` or online validator)

Test:
```bash
# In Claude Code
/handoff

# Should work without errors
# If errors, check config file paths and syntax
```

---

## Common Migration Issues

### Issue: "Section not found"

**Problem:** Section name in config doesn't match file

**Fix:**
1. Check exact section names in your files
2. Update config to match
3. Or let skill create missing sections

### Issue: "File not writable"

**Problem:** File permissions or file is open

**Fix:**
```bash
chmod 644 HANDOFF.md
# Close file in editor
```

### Issue: "Conversation number collision"

**Problem:** Existing logs use same numbering

**Fix:**
```yaml
logs:
  numbering: date  # Switch to date-based
```

Or:
```bash
# Rename existing logs
mv 001-old.md archive/001-old.md
# Start fresh numbering
```

### Issue: "Memory file too large"

**Problem:** Old memory file exceeds limit

**Fix:**
```yaml
limits:
  memory_lines: 500  # Increase limit
```

Or archive old content:
```bash
# Extract old content
head -200 MEMORY.md > MEMORY-new.md
tail -n +201 MEMORY.md > archive/MEMORY-old.md
mv MEMORY-new.md MEMORY.md
```

---

## Rollback Plan

If migration doesn't work:

### 1. Backup first (ALWAYS)

```bash
cp HANDOFF.md HANDOFF.md.backup
cp MEMORY.md MEMORY.md.backup
cp -r conversation-logs/ conversation-logs.backup/
```

### 2. If something breaks

```bash
# Restore backups
mv HANDOFF.md.backup HANDOFF.md
mv MEMORY.md.backup MEMORY.md
rm -rf conversation-logs/
mv conversation-logs.backup/ conversation-logs/

# Remove config
rm .handoff.yaml

# Go back to old system
```

### 3. Report issue

Open issue with:
- Your `.handoff.yaml` config
- File structure (ls -la)
- Error message
- What you expected vs what happened

---

## Success Criteria

Migration succeeded when:

- ✅ You can run `/handoff` without errors
- ✅ Files are updated correctly
- ✅ Session logs are created in right place
- ✅ Next session can pick up where you left off
- ✅ No information was lost from old system

Test by:
1. Run `/handoff` twice
2. Check files were updated
3. Read last session log
4. Verify next task is clear

If all ✅, migration complete!

---

## Need Help?

- Read `SKILL.md` for full documentation
- Check `examples/` for working configs
- Start with `minimal` profile if unsure
- Can always add structure later

**Remember:** The goal is to capture session state, not to build the perfect system on day one.
