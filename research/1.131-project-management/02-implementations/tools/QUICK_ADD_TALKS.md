# Quick Add Talks - Multiple Methods

Three ways to quickly add speaking opportunities to your Vikunja Talks project.

## Method 1: Enhanced create_task.py (Universal)

**Location:** `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools/create_task.py`

**New feature:** `--bucket` flag accepts bucket name or index

### Examples

```bash
# By bucket name (partial match)
uv run python create_task.py \
  --project-id 13481 \
  --title "PyCon 2026" \
  --bucket "Ideas" \
  --due-date 2026-03-01

# By bucket index (1-based)
uv run python create_task.py \
  --project-id 13481 \
  --title "Event opportunity" \
  --bucket 1 \
  --due-date "next month"

# Without bucket assignment
uv run python create_task.py \
  --project-id 13481 \
  --title "Simple task" \
  --due-date 2026-02-15
```

### Bucket Index Reference (Talks Project)
1. 💡 Ideas
2. 📝 Proposal Writing
3. 📤 Submitted
4. ✅ Accepted
5. 🎯 Preparing
6. 🎤 Delivered

### Use When
- You need full control over task properties
- You're working with any Vikunja project (not just Talks)
- You want to script task creation

---

## Method 2: add_talk.py (Talk-Specific)

**Location:** `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools/add_talk.py`

**Features:**
- Auto-assigns to Talks project (13481)
- Auto-assigns to "💡 Ideas" bucket
- Auto-calculates proposal deadline (3 months before event)
- Generates structured HTML description

### Examples

```bash
# Simple talk
uv run python add_talk.py \
  --title "PyCon 2026" \
  --event-date 2026-05-15 \
  --location "Pittsburgh, PA"

# Full details (like inControl Summit)
uv run python add_talk.py \
  --title "inControl Summit 2026" \
  --event-date 2026-06-02 \
  --location "Düsseldorf, Germany" \
  --focus "Europe's first AI-focused event industry conference" \
  --organizer "run.events (Damir Tomicic)" \
  --contact "hello@runevents.net" \
  --speakers "Colja Dams, Prof. Dr. Stefan Luppold, Orla Pearson" \
  --notes "Code SUMMIT20 for 20% off"

# Custom proposal deadline
uv run python add_talk.py \
  --title "PyData Seattle" \
  --event-date 2026-04-20 \
  --proposal-deadline 2026-01-15 \
  --location "Seattle, WA"

# Skip bucket assignment
uv run python add_talk.py \
  --title "Local meetup" \
  --no-bucket

# Dry run (preview)
uv run python add_talk.py \
  --title "Test Event" \
  --event-date 2026-08-15 \
  --dry-run
```

### Use When
- Adding speaking opportunities specifically
- You want automatic HTML formatting
- You want automatic deadline calculation
- You want the fastest workflow for talks

---

## Method 3: Shell Function (Quickest)

**Function:** `vikunja-add-talk`
**Location:** Added to `~/.bashrc`

### Usage

```bash
# Reload shell to enable function
source ~/.bashrc

# Simple usage
vikunja-add-talk "PyCon 2026" "2026-05-15" "Pittsburgh"

# Just title (no date)
vikunja-add-talk "Conference Name"

# With date but no location
vikunja-add-talk "Event 2026" "2026-08-20"
```

### Bonus Function: View Talks

```bash
vikunja-talks  # View all tasks in Talks project
```

### Use When
- You're already in terminal
- You want the absolute fastest method
- You have basic details (title, date, location)
- You don't need complex descriptions

---

## Method 4: Claude Skill (Natural Language) ⭐

**Skill:** `add-talk`
**Location:** `~/.claude/skills/add-talk.md`

### Usage

Just tell Claude in natural language:

```
"Add inControl Summit to my talks - it's June 2026 in Düsseldorf"

"Track this speaking opportunity: PyData Seattle, April 20, 2026"

"Add PyCon 2026 to my talks list"

[Forward conference CFP email]
```

Claude will:
1. Extract event details from your message
2. Ask clarifying questions if needed
3. Generate structured HTML description
4. Create task with auto-calculated deadline
5. Assign to "💡 Ideas" bucket
6. Confirm with task URL

### Use When
- You're already chatting with Claude
- You have unstructured info (emails, notes)
- You want Claude to extract/structure details
- You prefer conversational interface

---

## Comparison Matrix

| Method | Speed | Flexibility | Best For |
|--------|-------|-------------|----------|
| **create_task.py** | Medium | ⭐⭐⭐⭐⭐ | Any project, any task type, full control |
| **add_talk.py** | Fast | ⭐⭐⭐ | Speaking opportunities, structured HTML |
| **Shell function** | ⚡ Fastest | ⭐⭐ | Quick terminal adds, basic details |
| **Claude skill** | Medium | ⭐⭐⭐⭐ | Natural language, email forwarding, extraction |

---

## Real-World Workflow

### Scenario 1: Conference CFP Email
1. Forward email to Claude
2. Say "add this to my talks"
3. Claude extracts details and uses `add_talk.py`

### Scenario 2: Quick Terminal Add
```bash
vikunja-add-talk "Seattle Tech Talks" "2026-07-10" "Seattle"
```

### Scenario 3: Complex Event with Full Details
```bash
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools
uv run python add_talk.py \
  --title "Major Conference 2026" \
  --event-date 2026-09-15 \
  --location "San Francisco, CA" \
  --focus "AI and Cloud Native" \
  --organizer "CNCF" \
  --contact "events@cncf.io" \
  --url "https://conference.cncf.io" \
  --priority 2
```

### Scenario 4: Non-Talk Task in Talks Project
```bash
uv run python create_task.py \
  --project-id 13481 \
  --title "Update speaker bio on website" \
  --bucket 5 \
  --due-date "next week"
```

---

## Environment Setup

All methods automatically load credentials from:
```
/home/ivanadmin/spawn-solutions/.env
```

Required variables:
- `VIKUNJA_API_TOKEN`
- `VIKUNJA_BASE_URL`

---

## Testing

```bash
# Test create_task.py with bucket
cd /home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/tools
uv run python create_task.py --project-id 13481 --title "Test" --bucket 1 --dry-run

# Test add_talk.py
uv run python add_talk.py --title "Test Event" --event-date 2026-12-01 --dry-run

# Test shell function
source ~/.bashrc
vikunja-talks  # View current talks

# Test Claude skill
# Just say "add talk" to Claude and provide details
```

---

## Summary

**Use `add_talk.py`** for 90% of speaking opportunities - it's optimized for this exact use case.

**Use shell function** when you're already in terminal and have basic details.

**Use Claude skill** when forwarding emails or working with unstructured information.

**Use `create_task.py`** when you need precise control or working with non-talk tasks.

All methods integrate seamlessly with your existing Vikunja workflow!
