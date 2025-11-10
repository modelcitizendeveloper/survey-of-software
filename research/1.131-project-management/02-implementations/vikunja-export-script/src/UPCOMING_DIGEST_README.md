# Upcoming Digest - Start Date Aware Task View

**Problem**: Vikunja's "Upcoming" view only filters by `due_date`, not `start_date`. Tasks with start dates but no due dates don't appear.

**Solution**: `upcoming_digest.py` - shows tasks starting OR due within N days

---

## Usage

```bash
# Next 7 days (default)
python upcoming_digest.py --days 7

# Next 14 days
python upcoming_digest.py --days 14

# Today only
python upcoming_digest.py --days 0

# Include task descriptions
python upcoming_digest.py --days 7 --show-description

# Include high priority tasks regardless of dates
python upcoming_digest.py --days 7 --include-priority
```

---

## What It Shows

### 🔴 OVERDUE
Tasks past their due_date

### 🟢 STARTING SOON
Tasks with `start_date` within next N days
**This is the key feature - Vikunja UI doesn't show these**

### 🟡 DUE SOON
Tasks with `due_date` within next N days

### ⚡ HIGH PRIORITY (optional)
Priority 4-5 tasks regardless of dates (with `--include-priority`)

---

## Output Format

**Default output includes:**
- Title
- Priority ([Low/Med/High/Urgent/DO NOW])
- Project hierarchy (Parent > Child)
- Start date | Due date
- Labels
- Vikunja URL

**With `--show-description`:**
- First 200 chars of task description

---

## Examples

**Monday morning check:**
```bash
python upcoming_digest.py --days 7
```

**Weekly planning:**
```bash
python upcoming_digest.py --days 14 --include-priority
```

**Detailed review:**
```bash
python upcoming_digest.py --days 7 --show-description
```

---

## Integration with Vikunja Suite

Part of the vikunja-export-script suite:
- `export_vikunja.py` - Full portfolio export (JSON/Markdown)
- `upcoming_digest.py` - **Start/due date filtered view** (this tool)

Both use vikunja-api-wrapper foundation.

---

## Future: Email Digest

Could be automated as daily/weekly email:

```bash
# Cron job examples
0 6 * * * python upcoming_digest.py --days 7 | mail -s "Weekly Digest" you@email.com
0 6 * * MON python upcoming_digest.py --days 14 --include-priority | mail -s "Monday Planning" you@email.com
```

---

## Why This Exists

Vikunja's UI "Upcoming" view:
- ✅ Shows tasks with `due_date`
- ❌ Ignores tasks with only `start_date`

This tool:
- ✅ Shows tasks with `start_date` (STARTING SOON)
- ✅ Shows tasks with `due_date` (DUE SOON)
- ✅ Shows overdue tasks
- ✅ Optional: High priority tasks

Addresses the gap where tasks scheduled to start (but not due) are invisible in Vikunja UI.

---

**Status**: Production ready
**Date**: November 9, 2025
**Location**: `vikunja-export-script/src/upcoming_digest.py`
