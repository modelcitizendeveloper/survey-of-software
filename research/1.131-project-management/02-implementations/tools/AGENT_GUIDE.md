# Vikunja Task Management - Agent Guide

**Target Audience**: AI agents completing tasks that need to update Vikunja
**Last Updated**: 2025-12-02
**Tools Location**: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/`

---

## Quick Reference: What Tool Should I Use?

| Task | Tool | Example |
|------|------|---------|
| Create new task | `create_task.py` | `python3 create_task.py --project-id 123 --title "New task"` |
| Update existing task | `update_task.py` | `python3 update_task.py --task-id 456 --description-file results.html` |
| Mark task as done | `update_task.py` | `python3 update_task.py --task-id 456 --done` |
| Add completion details | `update_task.py` | `python3 update_task.py --task-id 456 --done --description-file completion.html` |

---

## ❌ ANTI-PATTERN: Don't Create One-Off Scripts

**Wrong approach** (script proliferation):
```python
# DON'T DO THIS - creates a new file for every task update
cat > update_specific_task_123.py << 'EOF'
#!/usr/bin/env python3
import sys
sys.path.insert(0, '/home/ivanadamin/spawn-solutions/research/1.131-project-management/...')
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(...)
client.tasks.update(task_id=123, done=True, description="...")
EOF

python3 update_specific_task_123.py
```

**Why this is wrong**:
- Creates script clutter in repository
- Each task needs a new script
- Not reusable for future tasks
- Harder to maintain

---

## ✅ CORRECT PATTERN: Use General-Purpose Tools

**Right approach** (use existing tools):
```bash
# Use the general-purpose update_task.py tool
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/update_task.py \
  --task-id 123 \
  --done \
  --description-file /tmp/completion_details.html
```

**Why this is right**:
- No new files created
- Reusable for any task
- Consistent interface
- Well-tested and maintained

---

## Common Agent Workflow: Mark Task Complete

When an AI agent completes work and needs to update Vikunja:

### Step 1: Prepare completion details (HTML format)

Create a temporary HTML file with results:

```bash
cat > /tmp/task_completion.html << 'EOF'
<p><strong>✅ Research Complete</strong></p>

<p><strong>Deliverables:</strong></p>
<ul>
<li><code>path/to/file1.md</code> - Analysis results</li>
<li><code>path/to/file2.py</code> - Implementation</li>
<li>Total: 5 files, 1,234 lines</li>
</ul>

<p><strong>Key Findings:</strong></p>
<ol>
<li>Finding #1 with evidence</li>
<li>Finding #2 with evidence</li>
</ol>

<p><strong>Completed:</strong> 2025-12-02</p>
EOF
```

### Step 2: Update task using the tool

```bash
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/update_task.py \
  --task-id 216372 \
  --done \
  --description-file /tmp/task_completion.html
```

**Output:**
```
================================================================================
TASK UPDATE TOOL
================================================================================

Task ID: 216372
Current Title: Research patent filing decision

✅ Status: Not done → Done
📝 Description: Updating (432 chars)
   Preview: <p><strong>✅ Research Complete</strong></p>...

Applying updates...

✅ Task updated successfully

View at: https://app.vikunja.cloud/tasks/216372

================================================================================
COMPLETE
================================================================================
```

### Step 3: Clean up temporary file (optional)

```bash
rm /tmp/task_completion.html
```

---

## HTML Formatting Guide

Vikunja renders HTML in task descriptions. Use these tags:

### Basic Formatting
```html
<p>Paragraph text</p>
<strong>Bold text</strong>
<em>Italic text</em>
<code>file_path.py</code>
<hr>  <!-- Horizontal rule -->
<br>  <!-- Line break -->
```

### Lists
```html
<!-- Unordered list -->
<ul>
<li>Item 1</li>
<li>Item 2</li>
</ul>

<!-- Ordered list -->
<ol>
<li>Step 1</li>
<li>Step 2</li>
</ol>

<!-- Nested lists -->
<ul>
<li>Main item
  <ul>
    <li>Sub-item 1</li>
    <li>Sub-item 2</li>
  </ul>
</li>
</ul>
```

### Tables
```html
<table>
<thead>
<tr><th>Column 1</th><th>Column 2</th></tr>
</thead>
<tbody>
<tr><td>Data 1</td><td>Data 2</td></tr>
</tbody>
</table>
```

### Links
```html
<a href="https://example.com">Link text</a>
```

### Blockquotes
```html
<blockquote>
<p>Quoted text here</p>
</blockquote>
```

---

## Complete update_task.py Reference

### Available Options

```bash
python3 update_task.py \
  --task-id 123           # Required: Task ID to update
  --title "New title"     # Optional: Update title
  --description "HTML"    # Optional: Update description (inline HTML)
  --description-file path # Optional: Update description from file
  --priority 3            # Optional: 0=Unset, 1=Low, 2=Med, 3=High, 4=Urgent, 5=DO NOW
  --due-date 2025-12-31   # Optional: Due date (YYYY-MM-DD)
  --start-date 2025-12-01 # Optional: Start date (YYYY-MM-DD)
  --done                  # Optional: Mark as done
  --not-done              # Optional: Mark as not done
  --dry-run               # Optional: Preview without applying
  --show-current          # Optional: Show current task details
```

### Common Use Cases

**1. Mark task done (no description change):**
```bash
python3 update_task.py --task-id 123 --done
```

**2. Mark task done with completion details:**
```bash
python3 update_task.py --task-id 123 --done --description-file completion.html
```

**3. Update description only (keep status):**
```bash
python3 update_task.py --task-id 123 --description-file notes.html
```

**4. Update multiple fields:**
```bash
python3 update_task.py --task-id 123 \
  --done \
  --priority 5 \
  --description-file completion.html
```

**5. Preview changes before applying:**
```bash
python3 update_task.py --task-id 123 --done --dry-run
```

**6. Reopen a completed task:**
```bash
python3 update_task.py --task-id 123 --not-done
```

---

## Environment Setup

The tools automatically load credentials from:
```
/home/ivanadamin/spawn-solutions/.env
```

Required environment variables:
```bash
VIKUNJA_BASE_URL=https://app.vikunja.cloud
VIKUNJA_API_TOKEN=v1.YOUR_TOKEN_HERE
```

**Note**: The `.env` file is gitignored and contains credentials. Don't commit it.

---

## Best Practices for AI Agents

### ✅ DO:
1. Use `update_task.py` for all task updates
2. Create temporary HTML files in `/tmp/` for descriptions
3. Use `--dry-run` if uncertain about changes
4. Clean up temporary files after use
5. Include structured completion details (deliverables, findings, date)

### ❌ DON'T:
1. Create one-off Python scripts for individual task updates
2. Hard-code descriptions in command line (use files for >100 chars)
3. Skip the `--done` flag when marking tasks complete
4. Forget to include completion date in descriptions
5. Use plain text instead of HTML formatting

---

## Troubleshooting

### Error: "Must specify at least one field to update"
**Solution**: Add at least one flag like `--done`, `--description`, `--title`, etc.

### Error: "Cannot specify both --description and --description-file"
**Solution**: Choose one approach - either inline `--description` or `--description-file`

### Error: "Cannot specify both --done and --not-done"
**Solution**: Use only one status flag

### Error: "Failed to get task 123"
**Solution**: Verify task ID exists at https://app.vikunja.cloud/tasks/123

### Error: "File not found: /path/to/file.html"
**Solution**: Check file path is correct and file exists

---

## Related Tools

| Tool | Purpose | Location |
|------|---------|----------|
| `vikunja_wrapper.py` | Python API client | `../vikunja-api-wrapper/src/vikunja_wrapper.py` |
| `create_task.py` | Create new tasks | `./create_task.py` |
| `update_task.py` | Update existing tasks | `./update_task.py` |
| `add_talk.py` | Create speaking tasks | `./add_talk.py` |
| `upcoming_digest.py` | Show tasks due soon | `../vikunja-export-script/src/upcoming_digest.py` |
| `export_vikunja.py` | Export full portfolio | `../vikunja-export-script/src/export_vikunja.py` |

---

## Task Discovery: Finding What's Due

### upcoming_digest.py - Show tasks starting or due soon

**Location**: `../vikunja-export-script/src/upcoming_digest.py`

This script addresses a Vikunja UI limitation: the UI only filters by `due_date`, but this script filters by both `start_date` AND `due_date`.

**Common Use Cases:**

```bash
# Show what's overdue or due today
python3 ../vikunja-export-script/src/upcoming_digest.py --days 0

# Show next 7 days (typical weekly planning)
python3 ../vikunja-export-script/src/upcoming_digest.py --days 7

# Show next 14 days with full descriptions
python3 ../vikunja-export-script/src/upcoming_digest.py --days 14 --show-description

# Show next 7 days + all high priority tasks
python3 ../vikunja-export-script/src/upcoming_digest.py --days 7 --include-priority
```

**Available Options:**
- `--days N` - Days ahead to look (default: 7, use 0 for overdue/today)
- `--show-description` - Include full task descriptions
- `--include-priority` - Include high priority (4-5) tasks regardless of dates
- `--include-done` - Include completed tasks (default: exclude)

**Output Format:**
```
================================================================================
UPCOMING TASKS (Next 7 days)
================================================================================

📅 DUE: Dec 2, 2025 (Today)
───────────────────────────────────────────────────────────────────────────────
  [ID: 219666] Patents for QR Cards
  Project: Applications > QRCards > Business Development
  Priority: High (3)
  https://app.vikunja.cloud/tasks/219666

🏁 STARTING: Dec 3, 2025 (Tomorrow)
───────────────────────────────────────────────────────────────────────────────
  [ID: 220123] Research competitor pricing
  Project: Business > Market Analysis
  Priority: Medium (2)
  https://app.vikunja.cloud/tasks/220123
```

### export_vikunja.py - Full portfolio export

**Location**: `../vikunja-export-script/src/export_vikunja.py`

Export entire Vikunja portfolio for analysis or backup.

**Usage:**
```bash
# Export for spawn-analysis decision cards
python3 ../vikunja-export-script/src/export_vikunja.py --format spawn-analysis

# Export to markdown file
python3 ../vikunja-export-script/src/export_vikunja.py --format markdown --output /tmp/tasks.md

# Export as JSON
python3 ../vikunja-export-script/src/export_vikunja.py --format json --output /tmp/tasks.json

# Export specific project only
python3 ../vikunja-export-script/src/export_vikunja.py --project-id 13792
```

---

## Example: Complete Agent Session

Scenario: Agent researched patent filing and needs to mark task done.

```bash
# Agent creates completion summary
cat > /tmp/patent_research_complete.html << 'EOF'
<p><strong>✅ RECOMMENDATION: FILE PROVISIONAL PATENT</strong></p>

<p><strong>Research Completed:</strong> December 2, 2025</p>

<p><strong>Deliverables:</strong></p>
<ul>
<li><code>applications/qrcards/patent-research/FILING_DECISION.md</code></li>
<li><code>applications/qrcards/patent-research/REALISTIC_EXPECTED_VALUE.md</code></li>
<li>Total: 32 documents, 20,444 lines</li>
</ul>

<p><strong>Decision:</strong></p>
<ul>
<li>Investment: $2,500 (provisional)</li>
<li>Expected ROI: +$9,985 (Year 1)</li>
<li>Confidence: 85% (HIGH)</li>
</ul>
EOF

# Agent updates task
python3 /home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/tools/update_task.py \
  --task-id 216372 \
  --done \
  --description-file /tmp/patent_research_complete.html

# Agent cleans up
rm /tmp/patent_research_complete.html
```

---

## Summary

**Key Takeaway**: Always use the general-purpose `update_task.py` tool instead of creating one-off scripts. This keeps the repository clean and tools consistent.

**For future reference**: If you find yourself wanting to create a new Python script to update a Vikunja task, STOP and use `update_task.py` instead.

---

**Questions?** See `README.md` in this directory or check `vikunja_wrapper.py` source code.
