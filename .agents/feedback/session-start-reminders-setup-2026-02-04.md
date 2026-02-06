# Session Start Reminders - Setup Guide

**Created:** 2026-02-04
**Purpose:** Help you remember to use PIV-Swarm workflow when starting Claude Code sessions

---

## The Problem

From hubspot-integration retrospective:
> "The urge to 'just start coding' is strong. Resist it."

You built hubspot-integration without PIV workflow → scope creep, refactoring, ~70k extra tokens.

**Solution:** Create reminders so you can't forget PIV workflow when starting work.

---

## 4 Reminder Solutions (Pick What Works for You)

### Option 1: In-Claude Checklist ✅ (Already Installed)

**Location:** `.claude/SESSION-START-CHECKLIST.md`

**How it works:**
- File lives in `.claude/` directory
- Claude Code loads CLAUDE.md which now references it
- Visual checklist when you need a reminder

**Usage:**
```bash
# In Claude Code chat:
"Can you show me the session start checklist?"

# Or ask Claude to read it:
"Read .claude/SESSION-START-CHECKLIST.md"
```

**Pros:**
- No installation needed
- Always available in Claude context
- Easy to update

**Cons:**
- You have to remember to ask for it
- Not automatic

---

### Option 2: Updated CLAUDE.md ✅ (Already Installed)

**Location:** Top of `CLAUDE.md`

**How it works:**
- Claude reads CLAUDE.md on every session
- New "Session Start Protocol" section instructs Claude to ask you about workflow
- Claude proactively suggests PIV workflow when you request a feature

**What Claude will now do:**
1. When you say "build X", Claude asks: "Should we use PIV-Swarm workflow?"
2. Suggests `/prime` if this is first message in session
3. Asks clarifying questions before jumping to code

**Example interaction:**
```
You: "Build a CLI tool to query our database"

Claude: "This sounds like a new feature. Should we use the PIV-Swarm
workflow? I recommend:
1. /prime - Understand codebase
2. /discuss database-cli - Clarify requirements
3. /spec → /plan → /execute

Or we can proceed directly if this is a quick task. What do you prefer?"
```

**Pros:**
- Automatic - Claude reminds YOU
- No extra steps needed
- Integrated into every session

**Cons:**
- Relies on Claude following instructions (usually does)
- Might feel repetitive if you're doing many small tasks

---

### Option 3: Shell Prompt Reminder (Requires Setup)

**Location:** `.envrc` or `.bashrc_project`

**How it works:**
- When you `cd` into project directory, shell prints workflow reminder
- Uses `direnv` (recommended) or manual sourcing

**Setup - Option A: Using direnv (Recommended)**

```bash
# Install direnv
sudo apt install direnv

# Add to ~/.bashrc (at the end)
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# Reload shell
source ~/.bashrc

# Allow direnv for this project
cd /home/jhall/Projects/py-ai-starter-kit
direnv allow
```

**Setup - Option B: Manual sourcing**

```bash
# Add to your ~/.bashrc (at the end)
if [ -d "$HOME/Projects/py-ai-starter-kit" ]; then
    if [ "$PWD" = "$HOME/Projects/py-ai-starter-kit" ] || [[ "$PWD" == "$HOME/Projects/py-ai-starter-kit"/* ]]; then
        source "$HOME/Projects/py-ai-starter-kit/.bashrc_project"
    fi
fi

# Reload
source ~/.bashrc
```

**What you'll see:**

```
$ cd ~/Projects/py-ai-starter-kit

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  📋 PIV-Swarm Project Loaded
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Starting a new feature? Run the workflow:

    /prime → /discuss → /spec → /plan → /execute → /validate → /commit

  See: .claude/SESSION-START-CHECKLIST.md

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PIV-Swarm aliases loaded:
  - piv              : Show workflow checklist
  - piv-start        : Interactive workflow starter

$
```

**Bonus aliases:**

```bash
# Show checklist anytime
$ piv

# Interactive workflow starter
$ piv-start
Step 1: What are you building?
Feature name: database-cli
Opening Claude Code with reminder...
RUN: /prime
THEN: /discuss database-cli
```

**Pros:**
- Visual reminder before opening Claude
- Can't miss it
- Includes helpful aliases

**Cons:**
- Requires shell configuration
- Only works when you `cd` into project
- Might be annoying if you `cd` frequently

---

### Option 4: Interactive /session-start Skill ✅ (Already Installed)

**Location:** `.claude/skills/session-start/SKILL.md`

**How it works:**
- Manual skill you run at session start
- Interactive Q&A to choose workflow
- Offers to execute first step for you

**Usage:**

```bash
# In Claude Code:
/session-start
```

**What happens:**

```
🚀 Session Start - Workflow Guide

What type of work are you starting?

1. New feature or module → PIV Workflow
2. Bug fix or investigation → /rca workflow
3. Quick refactor (<50 lines) → Proceed directly
4. Documentation updates → Proceed directly
5. Exploration or research → /explore or /discuss

[You select option]

[Claude explains workflow and offers to start]
```

**Pros:**
- Interactive guidance
- Helps you choose right workflow
- Can execute first step for you
- Educational for team members

**Cons:**
- Manual - you have to remember to run it
- Adds 1-2 minutes to session start

---

## Recommended Setup

**For Maximum Effectiveness, Use 2 + 3 Together:**

1. **CLAUDE.md (Option 2)** - Already active, Claude reminds you
2. **Shell prompt (Option 3)** - Visual reminder before you even open Claude

**Setup Steps:**

```bash
# 1. Install direnv
sudo apt install direnv

# 2. Add to ~/.bashrc
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc

# 3. Reload shell
source ~/.bashrc

# 4. Allow direnv
cd /home/jhall/Projects/py-ai-starter-kit
direnv allow

# 5. Test it
cd ..
cd py-ai-starter-kit
# You should see the banner
```

**Then add to your workflow:**

```bash
# When starting new work:
cd ~/Projects/py-ai-starter-kit
# See reminder banner

claude
# Claude automatically suggests workflow due to CLAUDE.md

# If you forget, ask:
"Show me the session start checklist"

# Or run:
/session-start
```

---

## Testing the Reminders

### Test 1: Shell Prompt

```bash
cd ~/Projects/py-ai-starter-kit

# Expected output:
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#   📋 PIV-Swarm Project Loaded
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ...
```

### Test 2: Claude Reminder

```bash
claude
```

Then type: **"Build a new API endpoint for user authentication"**

**Expected Claude response:**
```
This sounds like a new feature that would benefit from the PIV-Swarm
workflow. Let me suggest:

1. /prime - First, let me understand the current codebase structure
2. /discuss user-auth-api - Clarify authentication requirements
3. /spec → /plan → /execute

Would you like me to start with /prime?
```

### Test 3: Session Start Skill

```bash
claude
```

Then type: **`/session-start`**

**Expected:** Interactive Q&A guiding you to the right workflow.

---

## Customization

### Adjust Reminder Frequency

**If shell prompt feels too aggressive:**

Edit `.envrc` and comment out the echo statements:

```bash
# echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
# echo "  📋 PIV-Swarm Project Loaded"
# ...
```

Keep only the alias loading:

```bash
# Load aliases silently
source .bashrc_project
```

**If Claude suggestions feel repetitive:**

Edit `CLAUDE.md` and adjust the "Session Start Protocol":

```markdown
## 🚨 Session Start Protocol

**For new features only**, ask: "Should we use PIV-Swarm workflow?"
[Rest of section...]
```

---

## When Reminders Fire

| Trigger | Option 1 | Option 2 | Option 3 | Option 4 |
|---------|----------|----------|----------|----------|
| `cd` into project | ❌ | ❌ | ✅ | ❌ |
| Open Claude Code | ❌ | ✅ | ❌ | ❌ |
| Say "build X" to Claude | ❌ | ✅ | ❌ | ❌ |
| Manually request | ✅ | ❌ | ✅ (`piv`) | ✅ (`/session-start`) |

---

## Success Metrics

Track whether reminders are working:

**After 1 week, check:**
- How many features did you build?
- How many used PIV workflow?
- Did you catch yourself before jumping to code?
- Did scope creep decrease?

**Add to thoughts.md:**
```markdown
## Reminder System Results (Week of [DATE])

- Built 3 features this week
- Used PIV for: 2/3 (database-cli, user-auth-api)
- Skipped PIV for: 1/3 (quick config fix - appropriate)
- Caught scope creep early: 2 times (good!)
- Shell prompt useful: YES / NO
- Claude suggestions useful: YES / NO

Notes:
- Shell prompt helped me remember to /prime
- Caught myself adding global CLI mid-stream, moved to v1.1
```

---

## Troubleshooting

### direnv not working

**Check if installed:**
```bash
which direnv
# Should show: /usr/bin/direnv or similar
```

**Check if hook added:**
```bash
grep direnv ~/.bashrc
# Should show: eval "$(direnv hook bash)"
```

**Re-allow:**
```bash
cd ~/Projects/py-ai-starter-kit
direnv allow
```

### Claude not suggesting workflow

**Check CLAUDE.md was updated:**
```bash
head -30 CLAUDE.md | grep "Session Start Protocol"
# Should show the new section
```

**Start fresh session:**
- Close Claude Code completely
- Reopen in project directory
- Try saying "build X"

### Aliases not working

**Check if bashrc_project sourced:**
```bash
type piv
# Should show: piv is a function
```

**Manually source:**
```bash
source .bashrc_project
piv  # Should show checklist
```

---

## Next Steps

1. **Choose your setup** (recommend Options 2 + 3)
2. **Install if needed** (direnv for Option 3)
3. **Test all reminders** (use tests above)
4. **Try on next feature** (pick something from thoughts.md)
5. **Track results** (update thoughts.md after 1 week)

---

## Files Created

```
.claude/SESSION-START-CHECKLIST.md     # Visual checklist
.claude/skills/session-start/SKILL.md  # Interactive skill
.envrc                                  # Shell prompt (direnv)
.bashrc_project                         # Shell prompt (manual)
CLAUDE.md                               # Updated with protocol (top of file)
```

All files are ready to use. Choose your reminder setup and test it!

---

**Questions?** Add to thoughts.md or ask Claude: "How do I set up the session reminders?"
