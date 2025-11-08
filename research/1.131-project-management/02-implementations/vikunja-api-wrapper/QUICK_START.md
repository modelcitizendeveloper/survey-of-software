# Vikunja API Wrapper - Quick Start

**5-Minute Setup Guide** (full details in SETUP_GUIDE.md)

---

## Prerequisites

- Vikunja Cloud account: https://app.vikunja.cloud/
- Python 3.8+
- spawn-solutions repo cloned

---

## Step 1: Create API Token (2 minutes)

1. **Login**: https://app.vikunja.cloud/
2. **Navigate**: Avatar → Settings → API Tokens
3. **Create new token**:
   - Title: `Python Wrapper - Automation`
   - Expires: `Never`
   - Permissions: Check ALL for **Projects**, **Tasks**, **Labels**
4. **Copy token** (you'll only see it once!)

---

## Step 2: Configure .env File (1 minute)

```bash
# Navigate to spawn-solutions root
cd /home/ivanadamin/spawn-solutions

# Create .env from template (if doesn't exist)
cp .env.template .env

# Edit .env
nano .env

# Add your token (replace your_vikunja_token_here):
VIKUNJA_API_TOKEN=v1.eyJhbGci...  # Paste your token here
VIKUNJA_BASE_URL=https://app.vikunja.cloud

# Save and exit (Ctrl+X, Y, Enter)

# Secure the file
chmod 600 .env
```

---

## Step 3: Install & Test (2 minutes)

```bash
# Navigate to wrapper directory
cd research/1.131-project-management/02-implementations/vikunja-api-wrapper/src

# Install dependencies
pip install -r requirements.txt python-dotenv

# Test token
python test_token.py
```

**Expected output**:
```
✅ Found .env file: /home/ivanadamin/spawn-solutions/.env
✅ VIKUNJA_API_TOKEN loaded
✅ Base URL: https://app.vikunja.cloud
✅ Token preview: v1.eyJhbGci...

Testing API connection...
✅ SUCCESS! Connected to Vikunja API
✅ Found 0 project(s)

✅ API TOKEN IS WORKING CORRECTLY!
```

---

## Step 4: Use in Your Scripts

### Basic Usage

```python
#!/usr/bin/env python3
import os
from pathlib import Path
from dotenv import load_dotenv
from vikunja_wrapper import VikunjaClient

# Load .env from spawn-solutions root
env_path = Path(__file__).parent.parent.parent / '.env'  # Adjust levels
load_dotenv(env_path)

# Initialize client
client = VikunjaClient(
    base_url=os.environ['VIKUNJA_BASE_URL'],
    token=os.environ['VIKUNJA_API_TOKEN']
)

# Create project
project = client.projects.create(title="My Project")

# Create task
task = client.tasks.create(
    project_id=project.id,
    title="My Task",
    due_date="2025-11-15"
)

print(f"Created task: {task.title}")
```

---

## Common Use Cases

### SEA: Auto-populate sprint tasks

```python
# Create SEA project
sea = client.projects.create(
    title="Schema Evolution Automation",
    description="12-week implementation plan"
)

# Create tasks for each week
for week in range(1, 13):
    client.tasks.create(
        project_id=sea.id,
        title=f"Week {week}: Implementation milestone",
        due_date=f"2025-11-{week:02d}-01",
        priority=5,
        labels=["SEA", "development"]
    )
```

### Cookbooks: Content calendar

```python
# Create cookbooks project
cookbooks = client.projects.create(title="Content Pipeline")

# Add research conversion tasks
research = [
    ("1.131", "PM Platforms", "2025-11-15"),
    ("3.007", "FP&A", "2025-11-22"),
]

for exp_id, title, due_date in research:
    client.tasks.create(
        project_id=cookbooks.id,
        title=f"Convert {exp_id}: {title}",
        due_date=due_date,
        labels=["research-to-content"]
    )
```

### QRCards: Bug tracking

```python
# Create qrcards project
qrcards = client.projects.create(title="QRCards Maintenance")

# Create bug task
bug = client.tasks.create(
    project_id=qrcards.id,
    title="Bug: Trail rendering issue",
    description="Error stacktrace here...",
    priority=8,
    labels=["bug", "urgent"]
)
```

---

## Troubleshooting

### "VIKUNJA_API_TOKEN not found"
→ Check .env file exists: `ls -la .env`
→ Check token is set: `grep VIKUNJA .env`

### "401 Unauthorized"
→ Token is invalid or expired
→ Create new token in Vikunja Cloud

### "403 Forbidden"
→ Token lacks permissions
→ Update token permissions in Vikunja Cloud

---

## Full Documentation

- **Complete Setup**: [SETUP_GUIDE.md](./SETUP_GUIDE.md)
- **Testing Guide**: [src/TESTING.md](./src/TESTING.md) ⭐ NEW
- **API Reference**: [src/README.md](./src/README.md)
- **Task Specification**: [TASK_SPECIFICATION.md](./TASK_SPECIFICATION.md)
- **Experiment Details**: [README.md](./README.md)

---

## Security Checklist

- [x] .env file created and secured (`chmod 600`)
- [x] .env is gitignored (never commit tokens!)
- [x] Token has minimal permissions (only what's needed)
- [x] Test script passed
- [x] API token renewal task created (run `add_api_reminder.py`)

---

**Ready to automate!** 🚀

See SETUP_GUIDE.md for detailed instructions and examples.
