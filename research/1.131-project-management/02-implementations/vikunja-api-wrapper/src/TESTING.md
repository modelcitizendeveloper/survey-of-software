# Vikunja API Wrapper - Testing Documentation

**Last Updated**: November 7, 2025
**Status**: ✅ All tests passing (11/11)

---

## Overview

This directory contains three test/setup scripts for the Vikunja API wrapper:

1. **test_token.py** - Smoke test (validates API token configuration)
2. **integration_tests.py** - Comprehensive CRUD tests (validates wrapper functionality)
3. **add_api_reminder.py** - One-time setup script (creates security reminder task)

---

## Quick Start

```bash
# 1. Test your API token (2 minutes)
python test_token.py

# 2. Run full integration tests (30 seconds)
python integration_tests.py

# 3. Create security reminder task (one-time, 10 seconds)
python add_api_reminder.py
```

---

## Script 1: test_token.py

### Purpose

**Smoke test** - Validates that your Vikunja API token is properly configured and working.

### What it Does

1. ✅ Checks .env file exists at `/home/ivanadmin/spawn-solutions/.env`
2. ✅ Loads `VIKUNJA_API_TOKEN` and `VIKUNJA_BASE_URL`
3. ✅ Tests API connection by listing projects
4. ✅ Tests write permissions by creating a test label
5. ✅ Shows your existing projects and task counts

### Usage

```bash
python test_token.py
```

### Expected Output

```
======================================================================
Vikunja API Token Test
======================================================================

✅ Found .env file: /home/ivanadmin/spawn-solutions/.env
✅ VIKUNJA_API_TOKEN loaded
✅ Base URL: https://app.vikunja.cloud
✅ Token preview: tk_b58cb267d291c55985136b9f054...

Testing API connection...
----------------------------------------------------------------------
✅ SUCCESS! Connected to Vikunja API
✅ Found 5 project(s)

Your Projects:
  📁 Inbox
     ID: 13426
     Tasks: 0

  📁 spawn-solutions
     ID: 13431
     Tasks: 1

Testing permissions (will create test label)...
✅ Create permission: OK (created label ID: 6520)
✅ Test label created (you can delete manually if needed)

======================================================================
✅ API TOKEN IS WORKING CORRECTLY!
======================================================================
```

### When to Run

- **First time setup** - After creating API token and adding to .env
- **After token rotation** - When you renew your API token (every 6-12 months)
- **Troubleshooting** - When wrapper isn't working as expected

### Exit Codes

- `0` - Success (token works)
- `1` - Failure (token invalid, .env missing, or API error)

---

## Script 2: integration_tests.py

### Purpose

**End-to-end integration tests** - Validates all CRUD operations against the real Vikunja API.

### What it Tests

#### Labels (3 tests)
- ✅ **Create** - Creates label with title and hex color
- ✅ **List** - Lists all labels in account
- ✅ **Update** - Updates label title and color
- ⚠️ **Get by ID** - SKIPPED (method not implemented in wrapper)

#### Projects (4 tests)
- ✅ **Create** - Creates project with title and description
- ✅ **List** - Lists all projects in account
- ✅ **Get by ID** - Retrieves specific project
- ✅ **Update** - Updates project title and description

#### Tasks (4 tests)
- ✅ **Create** - Creates task with title, description, due date, priority
- ✅ **List by Project** - Lists all tasks in a project
- ✅ **Get by ID** - Retrieves specific task
- ✅ **Update** - Updates task title, done status, priority
- ⚠️ **List All** - SKIPPED (requires project_id parameter)

### Usage

```bash
python integration_tests.py
```

### Expected Output

```
======================================================================
VIKUNJA API WRAPPER - INTEGRATION TESTS
======================================================================
✅ Using API: https://app.vikunja.cloud
✅ Token loaded: tk_b58cb267d291c55985136b9f054...

======================================================================
LABELS - CRUD TESTS
======================================================================

▶ Testing: Labels - Create
✅ PASS: Labels - Create
   Created label ID: 6519

▶ Testing: Labels - List
✅ PASS: Labels - List
   Found 8 label(s)

⚠️  SKIP: Labels - Get by ID (method not implemented)

▶ Testing: Labels - Update
✅ PASS: Labels - Update
   Updated label title: Test-Label-Updated

======================================================================
PROJECTS - CRUD TESTS
======================================================================

▶ Testing: Projects - Create
✅ PASS: Projects - Create
   Created project ID: 13430

... (etc)

======================================================================
INTEGRATION TEST SUMMARY
======================================================================
Total tests: 11
Passed: 11
Failed: 0

✅ ALL TESTS PASSED!

======================================================================
Next steps:
- Clean up test resources manually in Vikunja
- Use wrapper for real automation (SEA, cookbooks, qrcards)
- See SETUP_GUIDE.md for examples
======================================================================
```

### Test Resources Created

**Important**: This script creates real resources in your Vikunja account:
- 1 test label (e.g., "Test-Label-Integration")
- 1 test project (e.g., "Test-Project-Integration")
- 1 test task (in the test project)

**Cleanup**: Currently manual - delete these in Vikunja UI after testing.

### When to Run

- **After wrapper changes** - To verify nothing broke
- **Before production use** - To validate wrapper works with real API
- **After Vikunja API updates** - To detect breaking changes
- **Continuous integration** - As part of automated testing pipeline

### Exit Codes

- `0` - All tests passed
- `1` - One or more tests failed

---

## Script 3: add_api_reminder.py

### Purpose

**One-time setup script** - Creates a security maintenance task to remind you to rotate your Vikunja API token.

### What it Does

1. ✅ Finds or creates "spawn-solutions" project
2. ✅ Creates "Security" label (red, #FF0000)
3. ✅ Creates "Renew API token" task:
   - Due date: 30 days from today
   - Priority: 5 (medium)
   - Description: Step-by-step token rotation instructions

### Usage

```bash
# Run once after initial setup
python add_api_reminder.py
```

### Expected Output

```
======================================================================
CREATE API TOKEN RENEWAL REMINDER
======================================================================

✅ Using API: https://app.vikunja.cloud
✅ Token loaded

Looking for 'spawn-solutions' project...
✅ Found 5 project(s)
Creating new project: spawn-solutions...
✅ Created project: spawn-solutions (ID: 13431)

Creating 'Security' label...
✅ Created label: Security (ID: 6520)

Creating 'Renew API token' task...
✅ Created task: 'Renew API token' (ID: 216262)
   Due date: 2025-12-07T19:01:21Z
   Priority: 0

======================================================================
✅ SETUP COMPLETE!
======================================================================

Created:
  📁 Project: spawn-solutions (ID: 13431)
  🏷️  Label: Security (ID: 6520)
  ✅ Task: Renew API token (ID: 216262, due: 2025-12-07T19:01:21Z)

Next steps:
  - View task in Vikunja: https://app.vikunja.cloud/
  - Set reminder notifications in Vikunja settings
  - Use wrapper for other automation (see SETUP_GUIDE.md)
======================================================================
```

### Task Details

The created task includes:

```
Title: Renew API token
Due: 30 days from creation
Priority: 0 (unset/normal)

Description (uses HTML formatting - see note below):
Security maintenance: Rotate Vikunja API token

Steps: (bold)

1. Login to https://app.vikunja.cloud/
2. Go to Settings → API Tokens
3. Delete old token
4. Create new token with same permissions
5. Update /home/ivanadmin/spawn-solutions/.env
6. Run test_token.py to verify
7. Reschedule this task for 6-12 months

Recommended frequency: (bold) Every 6-12 months
```

**Important: Vikunja Formatting**

Vikunja requires **HTML tags** for formatting in task descriptions:
- Use `<br>` for line breaks (not `\n`)
- Use `<br><br>` for paragraph spacing
- Use `<strong>text</strong>` for bold (not `**text**`)
- Plain `\n` newlines are stripped by Vikunja's UI

### When to Run

- **Once after initial setup** - To create the first reminder
- **After each token rotation** - To reschedule the next reminder (or update task manually in Vikunja UI)

### Exit Codes

- `0` - Task created successfully
- `1` - Error (API issue, permission problem, etc.)

---

## Skipped Tests Explained

### Why Some Tests Are Skipped

#### ⚠️ Labels - Get by ID

**Reason**: `labels.get()` method not implemented in wrapper yet.

**Impact**: Low - You can still list all labels and filter by ID in your code.

**Example Workaround**:
```python
# Instead of:
# label = client.labels.get(label_id=123)

# Use:
labels = client.labels.list()
label = next((l for l in labels if l.id == 123), None)
```

**Implementation Needed** (for future):
```python
# In LabelsManager class
def get(self, label_id: int) -> Label:
    """Get a specific label."""
    response = self.client._request("GET", f"/api/v1/labels/{label_id}")
    return self._parse_label(response)
```

---

#### ⚠️ Tasks - List All

**Reason**: Vikunja API requires `project_id` to list tasks - there's no "list all tasks across all projects" endpoint.

**Impact**: None - This is an API design choice by Vikunja.

**Correct Usage**:
```python
# List tasks in a specific project
tasks = client.tasks.list(project_id=13431)

# To get all tasks across all projects:
all_tasks = []
for project in client.projects.list():
    tasks = client.tasks.list(project_id=project.id)
    all_tasks.extend(tasks)
```

**Not Possible**:
```python
# This doesn't exist in Vikunja API
all_tasks = client.tasks.list()  # ❌ Missing project_id
```

---

## Test Coverage Summary

### Current Coverage: 11/13 tests (84.6%)

| Resource | Create | List | Get | Update | Delete |
|----------|--------|------|-----|--------|--------|
| **Labels** | ✅ | ✅ | ⚠️ | ✅ | ❌ |
| **Projects** | ✅ | ✅ | ✅ | ✅ | ❌ |
| **Tasks** | ✅ | ✅* | ✅ | ✅ | ❌ |

**Legend**:
- ✅ Tested and passing
- ⚠️ Skipped (method not implemented)
- ❌ Not tested (delete operations)
- \* List requires project_id parameter

### Why Delete Operations Not Tested

Delete methods are implemented in the wrapper but not tested in integration_tests.py because:
1. **Safety** - Avoids accidentally deleting wrong resources
2. **Cleanup complexity** - Would need to create resources just to delete them
3. **Manual verification** - Easier to test manually when needed

To test delete operations manually:
```python
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(base_url="...", token="...")

# Create a test resource
label = client.labels.create(title="Test-Delete", hex_color="#FF0000")
print(f"Created label {label.id}")

# Delete it
client.labels.delete(label_id=label.id)
print(f"Deleted label {label.id}")

# Verify deletion
labels = client.labels.list()
assert not any(l.id == label.id for l in labels)
print("✅ Delete successful")
```

---

## API Endpoint Discovery

### How We Found the Correct Endpoints

Vikunja's API documentation was minified JavaScript, so we used **empirical testing** to discover endpoints.

#### Test Script: test_endpoints.py

```python
# Tested combinations:
endpoints_to_try = [
    ("POST", "/api/v1/lists"),      # ❌ 404
    ("PUT", "/api/v1/lists"),       # ❌ 404
    ("POST", "/api/v1/projects"),   # ❌ 404
    ("PUT", "/api/v1/projects"),    # ✅ 201 SUCCESS
]
```

### Discovered Endpoints

| Operation | Endpoint | Method | Notes |
|-----------|----------|--------|-------|
| **Projects** |
| Create | `/api/v1/projects` | PUT | Not POST! |
| List | `/api/v1/projects` | GET | |
| Get | `/api/v1/projects/{id}` | GET | |
| Update | `/api/v1/projects/{id}` | POST | Not PUT! |
| Delete | `/api/v1/projects/{id}` | DELETE | |
| **Tasks** |
| Create | `/api/v1/projects/{id}/tasks` | PUT | |
| List | `/api/v1/projects/{id}/tasks` | GET | Requires project_id |
| Get | `/api/v1/tasks/{id}` | GET | |
| Update | `/api/v1/tasks/{id}` | POST | |
| Delete | `/api/v1/tasks/{id}` | DELETE | |
| **Labels** |
| Create | `/api/v1/labels` | PUT | |
| List | `/api/v1/labels` | GET | |
| Get | `/api/v1/labels/{id}` | GET | Not implemented yet |
| Update | `/api/v1/labels/{id}` | POST | |
| Delete | `/api/v1/labels/{id}` | DELETE | Not tested |

### Quirks Discovered

1. **Projects use PUT for create** - Not standard REST (usually POST)
2. **Projects use POST for update** - Not standard REST (usually PUT/PATCH)
3. **Tasks require project_id to list** - No global task list
4. **Dates must be RFC3339** - `2025-11-14T12:00:00Z`, not `2025-11-14`

---

## Troubleshooting

### Test Failures

#### "VIKUNJA_API_TOKEN not found"

**Problem**: .env file missing or token not set

**Fix**:
```bash
cd /home/ivanadmin/spawn-solutions
cp .env.template .env
nano .env  # Add your token
chmod 600 .env
```

---

#### "401 Unauthorized"

**Problem**: Token invalid or expired

**Fix**:
1. Go to https://app.vikunja.cloud/ → Settings → API Tokens
2. Check if token is active
3. If expired, create new token with same permissions
4. Update .env file
5. Run test_token.py to verify

---

#### "403 Forbidden"

**Problem**: Token lacks required permissions

**Fix**:
1. Go to https://app.vikunja.cloud/ → Settings → API Tokens
2. Edit token permissions:
   - **Projects**: ☑ Read, Create, Update, Delete
   - **Tasks**: ☑ Read, Create, Update, Delete
   - **Labels**: ☑ Read, Create, Update
3. Save changes
4. Run test_token.py to verify

---

#### "404 Not Found" on Projects Create

**Problem**: Wrapper using wrong endpoint

**Fix**: This is a bug - file an issue. The wrapper should use `PUT /api/v1/projects` not `POST`.

---

#### "Validation error: parsing time"

**Problem**: Date format incorrect

**Fix**: Use RFC3339 format with time component:
```python
# ❌ Wrong
due_date = "2025-11-14"

# ✅ Correct
from datetime import datetime
due_date = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
# Result: "2025-11-14T12:00:00Z"
```

---

#### "ModuleNotFoundError: No module named 'dateutil'"

**Problem**: Dependencies not installed

**Fix**:
```bash
cd method-4-adaptive-tdd
uv pip install -r requirements.txt python-dotenv
```

---

### Performance Issues

**Slow API responses**:
- Normal response time: 200-500ms per request
- If slower: Check internet connection or Vikunja Cloud status

**Integration tests timing out**:
- Default timeout: 120 seconds (plenty for 11 tests)
- If timeout: Check API is reachable: `curl -I https://app.vikunja.cloud`

---

## Running Tests in CI/CD

### GitHub Actions Example

```yaml
name: Test Vikunja Wrapper

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.12'

      - name: Install uv
        run: pip install uv

      - name: Install dependencies
        run: |
          cd research/1.131-project-management/02-implementations/vikunja-api-wrapper/method-4-adaptive-tdd
          uv pip install -r requirements.txt python-dotenv

      - name: Create .env
        run: |
          echo "VIKUNJA_API_TOKEN=${{ secrets.VIKUNJA_API_TOKEN }}" > .env
          echo "VIKUNJA_BASE_URL=https://app.vikunja.cloud" >> .env
        working-directory: .

      - name: Run smoke test
        run: python test_token.py
        working-directory: research/1.131-project-management/02-implementations/vikunja-api-wrapper/method-4-adaptive-tdd

      - name: Run integration tests
        run: python integration_tests.py
        working-directory: research/1.131-project-management/02-implementations/vikunja-api-wrapper/method-4-adaptive-tdd
```

**Note**: Store `VIKUNJA_API_TOKEN` as a GitHub secret.

---

## Cleaning Up Test Resources

After running integration tests, you'll have test resources in your Vikunja account:

### Manual Cleanup (Current Method)

1. Login to https://app.vikunja.cloud/
2. Delete test projects (e.g., "Test-Project-Integration")
3. Delete test labels (e.g., "Test-Label-Integration", "Test-Label-Updated")
4. Test tasks will be deleted automatically when you delete their project

### Automated Cleanup (Future)

When delete methods are fully tested, we could add:
```python
# In integration_tests.py cleanup()
for label_id in self.test_resources['labels']:
    client.labels.delete(label_id=label_id)

for task_id in self.test_resources['tasks']:
    client.tasks.delete(task_id=task_id)

for project_id in self.test_resources['projects']:
    client.projects.delete(project_id=project_id)
```

---

## Production Usage Examples

**Important: Task Description Formatting**

When creating tasks with multi-line descriptions, Vikunja requires HTML formatting:

```python
# ❌ Plain newlines don't render in UI
description = "Line 1\nLine 2\nLine 3"

# ✅ Use HTML tags for proper formatting
description = "Line 1<br>Line 2<br>Line 3"

# ✅ Use <strong> for bold text
description = "<strong>Important:</strong> Remember this<br>Next line"

# ✅ Use <br><br> for paragraph spacing
description = "Paragraph 1<br><br>Paragraph 2"
```

### Example 1: SEA Sprint Planning

```python
#!/usr/bin/env python3
"""Auto-populate SEA sprint tasks"""
from vikunja_wrapper import VikunjaClient
from datetime import datetime, timedelta

client = VikunjaClient(base_url="...", token="...")

# Create SEA project
sea = client.projects.create(
    title="Schema Evolution Automation",
    description="12-week implementation plan"
)

# Create tasks for each week
start_date = datetime(2025, 11, 10)
for week in range(1, 13):
    due = start_date + timedelta(weeks=week)
    client.tasks.create(
        project_id=sea.id,
        title=f"Week {week}: Implementation milestone",
        due_date=due.strftime("%Y-%m-%dT09:00:00Z"),
        priority=5
    )

print(f"Created {sea.title} with 12 weekly tasks")
```

### Example 2: Cookbooks Content Calendar

```python
#!/usr/bin/env python3
"""Generate content pipeline tasks from research"""
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(base_url="...", token="...")

# Create cookbooks project
cookbooks = client.projects.create(title="Content Pipeline")

# Research to convert
research = [
    ("1.131", "PM Platforms", "2025-11-15"),
    ("3.007", "FP&A", "2025-11-22"),
    ("3.044", "Data Warehouse", "2025-11-29"),
]

for exp_id, title, due in research:
    client.tasks.create(
        project_id=cookbooks.id,
        title=f"Convert {exp_id}: {title}",
        due_date=f"{due}T17:00:00Z",
        priority=3
    )

print(f"Created {len(research)} content tasks")
```

### Example 3: QRCards Bug Tracker

```python
#!/usr/bin/env python3
"""Report bugs to Vikunja"""
from vikunja_wrapper import VikunjaClient
import sys

client = VikunjaClient(base_url="...", token="...")

# Find qrcards project (or use Inbox)
projects = client.projects.list()
qrcards = next((p for p in projects if p.title == "qrcards"), projects[0])

# Create bug task
bug = client.tasks.create(
    project_id=qrcards.id,
    title=f"Bug: {sys.argv[1]}",
    description=sys.argv[2] if len(sys.argv) > 2 else "",
    priority=8  # High
)

print(f"Created bug task: {bug.id}")
```

**Usage**: `python report_bug.py "Trail rendering issue" "Stacktrace here..."`

---

## Next Steps

1. ✅ **Run test_token.py** - Verify your setup works
2. ✅ **Run integration_tests.py** - Validate full wrapper functionality
3. ✅ **Run add_api_reminder.py** - Create security maintenance task
4. ⬜ **Clean up test resources** - Delete test projects/labels in Vikunja UI
5. ⬜ **Build automation scripts** - Use examples above for SEA/cookbooks/qrcards
6. ⬜ **Set up CI/CD** - Add integration tests to your pipeline
7. ⬜ **Implement missing methods** - Add `labels.get()` if needed
8. ⬜ **Schedule token rotation** - Set calendar reminder for 6-12 months

---

## References

- **Wrapper Documentation**: [../vikunja_wrapper.py](./vikunja_wrapper.py)
- **Setup Guide**: [../SETUP_GUIDE.md](../SETUP_GUIDE.md)
- **Quick Start**: [../QUICK_START.md](../QUICK_START.md)
- **Task Specification**: [../TASK_SPECIFICATION.md](../TASK_SPECIFICATION.md)
- **Vikunja API Docs**: https://try.vikunja.io/api/v1/docs (interactive)
- **Vikunja Official Docs**: https://vikunja.io/docs/

---

**Last Tested**: November 7, 2025
**Vikunja Version**: Cloud (latest)
**Python Version**: 3.12.3
**Test Results**: 11/11 passing ✅
