# Vikunja API Token Setup & Security Guide

**Last Updated**: November 7, 2025

---

## Overview

This guide walks you through creating a Vikunja API token and setting it up securely for use with the Python wrapper.

**Security Model**: Store token in `.env` file (gitignored) in spawn-solutions repo root, accessible to all applications.

---

## Step 1: Create API Token in Vikunja Cloud

### 1.1 Navigate to API Tokens Page

1. Login to Vikunja Cloud: https://app.vikunja.cloud/
2. Click your **avatar/profile** (top right)
3. Select **Settings**
4. Click **API Tokens** (in left sidebar)

---

### 1.2 Create New Token

**Click**: "Create new API token" or similar button

**Fill in the form**:

#### Title
```
Python Wrapper - SEA/Cookbooks/QRCards Automation
```
(Or any name you'll recognize later)

#### Expires at
Select: **Never** (recommended for automation)

**Alternative**: If you prefer expiration for security, choose **1 year** and set calendar reminder to renew

---

### 1.3 Set Permissions

**Check ALL these boxes**:

```
Projects (Lists):
☑ Read
☑ Create
☑ Update
☑ Delete

Tasks:
☑ Read
☑ Create
☑ Update
☑ Delete

Labels:
☑ Read
☑ Create
☑ Update
☐ Delete (optional - only if you need to delete labels)
```

**Leave unchecked** (not needed for wrapper):
- Teams
- Namespaces
- Users
- Sharing
- Comments
- Attachments
- Reminders
- Webhooks

---

### 1.4 Create & Copy Token

1. Click **"Create"** or **"Save"** button
2. **IMPORTANT**: Copy the token immediately - you'll only see it once!
3. Token format: `v1.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (long string)

**Keep this browser tab open** until you've saved the token in Step 2.

---

## Step 2: Store Token Securely in .env File

### 2.1 Navigate to spawn-solutions Repo

```bash
cd /home/ivanadamin/spawn-solutions
```

---

### 2.2 Create .env File

**Create new file** (if doesn't exist):
```bash
touch .env
```

**Open in editor**:
```bash
# VS Code
code .env

# Or nano
nano .env

# Or vim
vim .env
```

---

### 2.3 Add Vikunja Token

**Add this line to `.env`**:
```bash
# Vikunja API Token (for PM automation - SEA, cookbooks, qrcards)
# Created: 2025-11-07
# Expires: Never (or date if you set expiration)
# Permissions: Projects (CRUD), Tasks (CRUD), Labels (CRU)
VIKUNJA_API_TOKEN=v1.eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
VIKUNJA_BASE_URL=https://app.vikunja.cloud
```

**Replace** `v1.eyJhbGci...` with your actual token from Step 1.4

---

### 2.4 Verify .env is Gitignored

**Check if .env is already gitignored**:
```bash
grep -r "^\.env$" .gitignore
```

**If NOT found**, add to `.gitignore`:
```bash
echo ".env" >> .gitignore
```

**Verify .env won't be committed**:
```bash
git status
# Should NOT show .env as untracked
```

---

### 2.5 Set File Permissions (Security)

**Make .env readable only by you**:
```bash
chmod 600 .env
```

**Verify**:
```bash
ls -la .env
# Should show: -rw------- (only owner can read/write)
```

---

## Step 3: Test API Token

### 3.1 Navigate to Wrapper Directory

```bash
cd research/1.131-project-management/02-implementations/vikunja-api-wrapper/method-4-adaptive-tdd
```

---

### 3.2 Install Dependencies

```bash
# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Also install python-dotenv for .env file loading
pip install python-dotenv
```

---

### 3.3 Create Test Script

**Create file**: `test_token.py`

```python
#!/usr/bin/env python3
"""
Test Vikunja API token from .env file
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient, VikunjaError

# Load .env from spawn-solutions root (5 levels up from this script)
env_path = Path(__file__).parent.parent.parent.parent.parent / '.env'
load_dotenv(env_path)

# Get credentials from environment
token = os.environ.get('VIKUNJA_API_TOKEN')
base_url = os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud')

# Validate environment variables
if not token:
    print("❌ ERROR: VIKUNJA_API_TOKEN not found in .env file")
    print(f"   Expected .env location: {env_path}")
    print("   Please follow SETUP_GUIDE.md to create .env file")
    exit(1)

print(f"✅ Loaded token from: {env_path}")
print(f"✅ Base URL: {base_url}")
print(f"✅ Token preview: {token[:20]}...")

# Test API connection
try:
    print("\nTesting API connection...")
    client = VikunjaClient(base_url=base_url, token=token)

    # List projects
    projects = client.projects.list()
    print(f"✅ SUCCESS! Connected to Vikunja API")
    print(f"✅ Found {len(projects)} project(s)")

    if projects:
        print("\nProjects:")
        for project in projects:
            print(f"  - {project.title} (ID: {project.id})")
    else:
        print("\nNo projects yet. Create one with:")
        print('  project = client.projects.create(title="My First Project")')

    print("\n✅ API token is working correctly!")

except VikunjaError as e:
    print(f"❌ API Error: {e}")
    print("\nTroubleshooting:")
    print("1. Verify token has correct permissions (Projects: Read)")
    print("2. Check token hasn't expired")
    print("3. Ensure base_url is correct")
    exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    exit(1)
```

---

### 3.4 Run Test

```bash
python test_token.py
```

**Expected output**:
```
✅ Loaded token from: /home/ivanadamin/spawn-solutions/.env
✅ Base URL: https://app.vikunja.cloud
✅ Token preview: v1.eyJhbGciOiJIUzI1...

Testing API connection...
✅ SUCCESS! Connected to Vikunja API
✅ Found 0 project(s)

No projects yet. Create one with:
  project = client.projects.create(title="My First Project")

✅ API token is working correctly!
```

**If you see errors**, see Troubleshooting section below.

---

## Step 4: Use Token in Applications

### 4.1 Pattern for All Scripts

**Standard pattern** to use in SEA, cookbooks, qrcards automation:

```python
#!/usr/bin/env python3
"""
Your automation script (SEA, cookbooks, qrcards)
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

# Load .env from spawn-solutions root
# Adjust parent levels based on your script location
spawn_solutions_root = Path(__file__).parent.parent.parent  # Adjust as needed
env_path = spawn_solutions_root / '.env'
load_dotenv(env_path)

# Initialize Vikunja client
client = VikunjaClient(
    base_url=os.environ.get('VIKUNJA_BASE_URL', 'https://app.vikunja.cloud'),
    token=os.environ['VIKUNJA_API_TOKEN']  # Will raise error if missing
)

# Your automation code here
project = client.projects.create(title="My Project")
task = client.tasks.create(
    project_id=project.id,
    title="My Task",
    due_date="2025-11-15"
)
```

---

### 4.2 SEA Integration Example

**Location**: `applications/schema-evolution-automation/scripts/populate_vikunja.py`

```python
#!/usr/bin/env python3
"""
Auto-populate Vikunja with SEA implementation plan tasks
"""
import os
from pathlib import Path
from datetime import datetime, timedelta
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

# Load .env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

client = VikunjaClient(
    base_url=os.environ.get('VIKUNJA_BASE_URL'),
    token=os.environ['VIKUNJA_API_TOKEN']
)

# Create SEA project
sea_project = client.projects.create(
    title="Schema Evolution Automation",
    description="12-week Phase 1 implementation plan"
)

# Weekly milestones (simplified - parse from IMPLEMENTATION_PLAN.md in reality)
milestones = [
    "Week 1: Project foundation",
    "Week 2: Pattern & template library",
    "Week 3-4: Request parsing",
    "Week 5-6: Code generation",
    "Week 7-8: Code insertion",
    "Week 9: Validation layer",
    "Week 10: Pattern library completion",
    "Week 11: Integration testing",
    "Week 12: CLI + documentation"
]

start_date = datetime(2025, 11, 10)  # Adjust to your start date

for i, milestone in enumerate(milestones, start=1):
    due_date = start_date + timedelta(weeks=i)

    task = client.tasks.create(
        project_id=sea_project.id,
        title=milestone,
        description=f"Complete all tasks for {milestone}",
        due_date=due_date.strftime("%Y-%m-%d"),
        priority=5 if i <= 4 else 3,
        labels=["SEA", "development"]
    )
    print(f"✅ Created: {task.title}")

print(f"\n✅ Created {len(milestones)} tasks in project: {sea_project.title}")
print(f"   Project ID: {sea_project.id}")
print(f"   View at: https://app.vikunja.cloud/projects/{sea_project.id}")
```

**Run**:
```bash
cd applications/schema-evolution-automation/scripts
python populate_vikunja.py
```

---

### 4.3 Cookbooks Content Calendar Example

**Location**: `applications/cookbooks/scripts/sync_content_calendar.py`

```python
#!/usr/bin/env python3
"""
Sync research completions to Vikunja content calendar
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

# Load .env
env_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(env_path)

client = VikunjaClient(
    base_url=os.environ.get('VIKUNJA_BASE_URL'),
    token=os.environ['VIKUNJA_API_TOKEN']
)

# Create cookbooks project
cookbooks = client.projects.create(
    title="Cookbooks Content Pipeline",
    description="Research → Framework → Case Study → Synthesis"
)

# Research experiments ready for conversion
research_pipeline = [
    ("1.131", "Self-hosted PM", "2025-11-15"),
    ("3.007", "FP&A Platforms", "2025-11-22"),
    ("1.104.1", "Code parsing & AST", "2025-11-29"),
]

for exp_id, title, publish_date in research_pipeline:
    task = client.tasks.create(
        project_id=cookbooks.id,
        title=f"Convert {exp_id} to framework",
        description=f"Research: {title}\nPublish date: {publish_date}",
        due_date=publish_date,
        priority=5,
        labels=["research-to-content", exp_id]
    )
    print(f"✅ Created: {task.title}")

print(f"\n✅ Content calendar synced to Vikunja")
```

---

## Security Best Practices

### ✅ DO:

1. **Use .env file** in repo root (spawn-solutions/.env)
2. **Gitignore .env** (never commit tokens)
3. **Set file permissions** (`chmod 600 .env`)
4. **Use environment variables** in code (os.environ)
5. **Use python-dotenv** to load .env files
6. **Rotate tokens** periodically (every 6-12 months if "Never" expires)
7. **Revoke old tokens** when creating new ones
8. **Use minimal permissions** (only what wrapper needs)
9. **Document token purpose** (comments in .env)
10. **Set expiration** if security policy requires (then set calendar reminder)

### ❌ DON'T:

1. **Never hardcode tokens** in scripts
2. **Never commit .env** to git
3. **Never share tokens** publicly (screenshots, logs, issues)
4. **Never use same token** across different services
5. **Never store tokens** in cloud sync folders (Dropbox, Google Drive)
6. **Never log tokens** (use `token[:20]...` for debugging)
7. **Never put tokens** in error messages
8. **Don't create tokens** with more permissions than needed

---

## Troubleshooting

### Error: "VIKUNJA_API_TOKEN not found in .env"

**Fix**:
1. Verify `.env` exists: `ls -la /home/ivanadamin/spawn-solutions/.env`
2. Check token is set: `grep VIKUNJA_API_TOKEN /home/ivanadamin/spawn-solutions/.env`
3. Ensure no extra spaces: `VIKUNJA_API_TOKEN=token` (not `VIKUNJA_API_TOKEN = token`)
4. Reload terminal: `source ~/.bashrc` or restart terminal

---

### Error: "401 Unauthorized"

**Causes**:
- Token is invalid or revoked
- Token not properly copied (extra spaces, truncated)
- Token expired

**Fix**:
1. Check token in Vikunja Cloud (Settings → API Tokens)
2. Verify token hasn't expired
3. Copy token again (ensure no spaces at start/end)
4. Try creating new token

---

### Error: "403 Forbidden" on specific operations

**Causes**:
- Token lacks required permissions

**Fix**:
1. Go to Settings → API Tokens in Vikunja Cloud
2. Click your token
3. Verify these permissions are checked:
   - Projects: Read, Create, Update, Delete
   - Tasks: Read, Create, Update, Delete
   - Labels: Read, Create, Update
4. Update permissions and save
5. Test again (no need to copy token again - same token, just more permissions)

---

### Error: "Connection refused" or "Name resolution failed"

**Causes**:
- Wrong VIKUNJA_BASE_URL
- No internet connection
- Vikunja Cloud is down (rare)

**Fix**:
1. Check `.env` has correct URL: `VIKUNJA_BASE_URL=https://app.vikunja.cloud`
2. Test internet: `curl https://app.vikunja.cloud/api/v1/info`
3. Check Vikunja Cloud status (if down, wait)

---

### Error: ".env file not loaded" (path issues)

**Causes**:
- Script in different location than expected
- Path calculation wrong

**Fix**:
```python
# Debug: Print where script is looking for .env
from pathlib import Path
env_path = Path(__file__).parent.parent.parent / '.env'
print(f"Looking for .env at: {env_path}")
print(f"Exists? {env_path.exists()}")

# Adjust parent levels:
# If script is 2 levels deep: .parent.parent
# If script is 3 levels deep: .parent.parent.parent
# If script is 4 levels deep: .parent.parent.parent.parent
```

**Alternative** (absolute path for debugging):
```python
load_dotenv('/home/ivanadamin/spawn-solutions/.env')
```

---

## Token Rotation (Maintenance)

**When to rotate** (every 6-12 months, or immediately if compromised):

### 1. Create New Token
Follow Step 1 (Create API Token) above with new title:
```
Python Wrapper - Automation (2025-11-07 to 2026-11-07)
```

### 2. Update .env
Replace old token with new token in `.env`:
```bash
# Old token (revoke after testing new one)
# VIKUNJA_API_TOKEN=v1.old_token_here

# New token (created 2025-11-07, expires 2026-11-07 or Never)
VIKUNJA_API_TOKEN=v1.new_token_here
```

### 3. Test New Token
```bash
python test_token.py
```

### 4. Revoke Old Token
1. Go to Settings → API Tokens in Vikunja Cloud
2. Find old token
3. Click "Delete" or "Revoke"
4. Confirm

### 5. Remove Old Token from .env
Delete commented-out old token line

---

## Multi-Environment Setup (Optional)

**If you need different tokens for different environments** (dev, staging, prod):

### .env.development
```bash
VIKUNJA_API_TOKEN=v1.dev_token
VIKUNJA_BASE_URL=https://dev.vikunja.cloud
```

### .env.production
```bash
VIKUNJA_API_TOKEN=v1.prod_token
VIKUNJA_BASE_URL=https://app.vikunja.cloud
```

### Load correct .env:
```python
import os
env = os.environ.get('ENV', 'development')
load_dotenv(f'.env.{env}')
```

**For now**: Single .env is sufficient (only production Vikunja Cloud)

---

## Summary Checklist

**Setup Complete When**:
- [ ] Created API token in Vikunja Cloud (Step 1)
- [ ] Set permissions: Projects, Tasks, Labels (CRUD)
- [ ] Created `/home/ivanadamin/spawn-solutions/.env` (Step 2)
- [ ] Added `VIKUNJA_API_TOKEN` and `VIKUNJA_BASE_URL` to .env
- [ ] Verified `.env` is gitignored
- [ ] Set file permissions: `chmod 600 .env`
- [ ] Installed dependencies: `pip install -r requirements.txt python-dotenv`
- [ ] Ran test script: `python test_token.py` (Step 3)
- [ ] Saw "✅ API token is working correctly!"

**Ready to use** in SEA, cookbooks, qrcards automation scripts!

---

**Last Updated**: November 7, 2025
**Next Review**: 2026-11-07 (token rotation)
