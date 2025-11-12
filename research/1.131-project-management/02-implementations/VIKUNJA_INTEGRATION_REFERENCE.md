# Vikunja Integration Reference

This document provides a comprehensive guide for other repositories and agents to generate Vikunja projects, subprojects, tasks, labels, and Kanban bucket assignments using the YAML schema and Python API wrapper.

## Table of Contents

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [YAML Schema Reference](#yaml-schema-reference)
4. [Python API Wrapper](#python-api-wrapper)
5. [Population Script](#population-script)
6. [Examples](#examples)
7. [Best Practices](#best-practices)

---

## Overview

The Vikunja integration system consists of three main components:

1. **YAML Schema** - Declarative format for defining projects, tasks, labels, and buckets
2. **Python API Wrapper** (`vikunja_wrapper.py`) - Production-ready client for Vikunja REST API
3. **Population Script** (`populate_vikunja.py`) - Validates YAML and creates resources in Vikunja

### Key Features

- **Hierarchical Projects** - Support for parent/child project relationships
- **Global Labels** - Reusable labels with hex colors
- **Task Relations** - Blocking dependencies and subtasks
- **Kanban Buckets** - Assign tasks to workflow stages
- **Dry Run Mode** - Preview changes before execution
- **Idempotent** - Safely rerun without duplicates

---

## Architecture

```
┌─────────────────┐
│  YAML Schema    │ ← Human/LLM authored
│  (tasks.yaml)   │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Validation     │ ← Validates schema
│  (validation.py)│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Population     │ ← Creates resources
│  (population.py)│
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  API Wrapper    │ ← HTTP calls to Vikunja
│ (vikunja_wrapper│
│      .py)       │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  Vikunja API    │
│  (REST API)     │
└─────────────────┘
```

---

## YAML Schema Reference

### Complete Schema Structure

```yaml
project:
  # Option 1: Create new project
  title: "My Project"
  description: "Optional description"
  color: "3498db"  # Hex color (6 chars, no # prefix)
  parent_project: "Applications/Products"  # Slash-separated path
  # OR
  parent_project_id: 12345  # Direct parent ID

  # Option 2: Add tasks to existing project
  project_id: 13426  # Skip project creation, add tasks to existing

  # Optional: Define Kanban buckets
  buckets:
    - name: "💡 Ideas"
      position: 0
      limit: 0  # 0 = no WIP limit
    - name: "📋 Todo"
      position: 1
      limit: 5
    - name: "✅ Done"
      position: 2
      limit: 0

labels:
  - title: "Design"
    hex_color: "e74c3c"  # Required (6 chars, no # prefix)
    description: "Design work"  # Optional
  - title: "Code"
    hex_color: "3498db"
  - title: "Next Action"
    hex_color: "2ecc71"

tasks:
  - title: "Task title"
    description: |
      <p>HTML-formatted description</p>
      <ul>
        <li>Supports rich text</li>
        <li>Lists, bold, links</li>
      </ul>
    labels:
      - Design
      - Code
    priority: 3  # 0=unset, 1=low, 2=medium, 3=high, 4=urgent, 5=critical
    due_date: "2025-11-30"  # YYYY-MM-DD format
    start_date: "2025-11-15"  # Optional
    bucket: "📋 Todo"  # Assign to Kanban bucket
    blocked_by:  # Task dependencies
      - "Setup development environment"
    subtask_of: "Parent task title"  # Subtask relation
    assignees:  # User assignment (requires user lookup)
      - "user@example.com"
```

### Field Reference

#### Project Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Project name (max 250 chars) |
| `description` | string | No | Project description (max 5000 chars) |
| `color` | string | No | Hex color: 6 chars, no `#` prefix (e.g., `3498db`) |
| `parent_project` | string | Conditional | Slash-separated path (e.g., `Applications/Products`) |
| `parent_project_id` | integer | Conditional | Direct parent project ID |
| `project_id` | integer | No | If set, adds tasks to existing project (skips creation) |
| `buckets` | array | No | List of Kanban buckets to create |

**Note:** Either `parent_project`, `parent_project_id`, OR `project_id` is required. Root-level projects are not allowed by default (use `--allow-root-project` flag to override).

#### Bucket Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `name` | string | Yes | Bucket display name |
| `position` | integer | Yes | Sort order (0, 1, 2...) |
| `limit` | integer | No | WIP limit (0 = no limit) |

#### Label Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Label name (max 100 chars) |
| `hex_color` | string | Yes | Hex color: 6 chars, no `#` prefix |
| `description` | string | No | Label description (max 500 chars) |

**Note:** Labels are global in Vikunja (shared across all projects).

#### Task Fields

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `title` | string | Yes | Task name (max 250 chars) |
| `description` | string | No | HTML-formatted description (max 50,000 chars) |
| `labels` | array | No | List of label titles (can reference existing labels) |
| `priority` | integer | No | 0-5 (0=unset, 1=low, 2=medium, 3=high, 4=urgent, 5=critical) |
| `due_date` | string | No | Due date in `YYYY-MM-DD` format |
| `start_date` | string | No | Start date in `YYYY-MM-DD` format |
| `bucket` | string | No | Bucket name to assign task to |
| `blocked_by` | array | No | List of task titles that block this task |
| `subtask_of` | string | No | Parent task title (for subtask relation) |
| `assignees` | array | No | List of user emails/usernames |
| `done` | boolean | No | Mark task as completed |

---

## Python API Wrapper

### Installation

```python
# Add to your Python path
import sys
sys.path.append('/path/to/vikunja-api-wrapper/src')
from vikunja_wrapper import VikunjaClient
```

### Authentication

```python
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url="https://app.vikunja.cloud",  # Or self-hosted URL
    token="your-api-token"  # Generate from Settings > API Tokens
)
```

### Core Resources

#### Projects

```python
# Create project
project = client.projects.create(
    title="My Project",
    description="Optional description",
    hex_color="3498db",
    parent_project_id=12345  # 0 = top-level (not recommended)
)

# List all projects
projects = client.projects.list()

# Get specific project
project = client.projects.get(project_id=123)

# Update project
project = client.projects.update(
    project_id=123,
    title="New Title",
    hex_color="e74c3c"
)

# Move project to different parent
project = client.projects.move_project(
    project_id=123,
    new_parent_id=456  # 0 = top-level
)

# Get project hierarchy
children = client.projects.get_children(parent_id=123)
parent = client.projects.get_parent(project)

# Delete project
client.projects.delete(project_id=123)
```

#### Tasks

```python
# Create task
task = client.tasks.create(
    project_id=123,
    title="My Task",
    description="<p>HTML description</p>",
    due_date="2025-11-30T23:59:59Z",  # ISO format with timezone
    priority=3,
    bucket_id=456  # Optional: assign to bucket
)

# List tasks in project
tasks = client.tasks.list(project_id=123)

# Get specific task
task = client.tasks.get(task_id=789)

# Update task
task = client.tasks.update(
    task_id=789,
    title="Updated Title",
    priority=5,
    done=True,
    bucket_id=456
)

# Delete task
client.tasks.delete(task_id=789)

# Assign task to Kanban bucket
kanban_view = client.views.get_kanban_view(project_id=123)
client.tasks.set_position(
    task_id=789,
    project_view_id=kanban_view.id,
    bucket_id=456,
    project_id=123
)
```

#### Labels

```python
# Create label (global)
label = client.labels.create(
    title="Design",
    hex_color="e74c3c"
)

# List all labels
labels = client.labels.list()

# Update label
label = client.labels.update(
    label_id=123,
    title="New Name",
    hex_color="3498db"
)

# Delete label
client.labels.delete(label_id=123)

# Attach label to task
client.tasks.add_label(task_id=789, label_id=123)
```

#### Task Relations

```python
# Create blocking relation (task_a blocks task_b)
relation = client.task_relations.create(
    task_id=task_a.id,
    relation_kind="blocking",
    other_task_id=task_b.id
)

# Create subtask relation (task is subtask of parent)
relation = client.task_relations.create(
    task_id=task.id,
    relation_kind="subtask",
    other_task_id=parent_task.id
)

# List all relations for task
relations = client.task_relations.list(task_id=789)

# Delete relation
client.task_relations.delete(
    task_id=task_a.id,
    relation_kind="blocking",
    other_task_id=task_b.id
)
```

#### Buckets (Kanban Columns)

```python
# Get Kanban view for project
kanban_view = client.views.get_kanban_view(project_id=123)

# Create bucket
bucket = client.buckets.create(
    project_id=123,
    view_id=kanban_view.id,
    title="💡 Ideas",
    position=0,
    limit=5  # WIP limit, 0 = no limit
)

# List buckets
buckets = client.buckets.list(
    project_id=123,
    view_id=kanban_view.id
)

# Update bucket
bucket = client.buckets.update(
    project_id=123,
    view_id=kanban_view.id,
    bucket_id=456,
    title="New Name",
    position=1,
    limit=10
)

# Delete bucket
client.buckets.delete(
    project_id=123,
    view_id=kanban_view.id,
    bucket_id=456
)
```

#### Views

```python
# List all views for project
views = client.views.list(project_id=123)

# Get specific view
view = client.views.get(project_id=123, view_id=456)

# Get Kanban view (convenience method)
kanban_view = client.views.get_kanban_view(project_id=123)
```

### Error Handling

```python
from vikunja_wrapper import (
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    VikunjaError
)

try:
    project = client.projects.create(title="My Project")
except AuthenticationError:
    print("Invalid API token")
except NotFoundError:
    print("Resource not found")
except ValidationError as e:
    print(f"Invalid data: {e}")
except RateLimitError:
    print("Rate limit exceeded")
except ServerError:
    print("Vikunja server error")
except VikunjaError as e:
    print(f"API error: {e}")
```

---

## Population Script

### Usage

```bash
# Basic usage (validate + create)
python3 populate_vikunja.py tasks.yaml

# Dry run (validate only, no API calls)
python3 populate_vikunja.py tasks.yaml --dry-run

# Allow root-level projects (bypass parent requirement)
python3 populate_vikunja.py tasks.yaml --allow-root-project

# Preserve API order (tasks added to top, default reverses for YAML order)
python3 populate_vikunja.py tasks.yaml --preserve-api-order

# Environment variables
export VIKUNJA_BASE_URL="https://app.vikunja.cloud"
export VIKUNJA_API_TOKEN="your-token"
```

### Environment Setup

Create `.env` file in your repo root:

```bash
VIKUNJA_BASE_URL=https://app.vikunja.cloud
VIKUNJA_API_TOKEN=your-api-token-here
```

The population script automatically loads `.env` from:
1. Current directory
2. `~/spawn-solutions/.env`

### Script Behavior

#### Idempotent Operations

The script is designed to be safely rerun:

- **Projects**: Matched by `title` + `parent_project_id`. Updates existing if found, creates new otherwise.
- **Labels**: Global labels matched by `title`. Reuses existing, creates new otherwise.
- **Tasks**: Matched by `title` within project. Updates existing if found, creates new otherwise.
- **Buckets**: Matched by `name` within project. Reuses existing, creates new otherwise.

#### Task Ordering

By default, the script **reverses** task order to match YAML sequence (Vikunja API adds new tasks to the top). Use `--preserve-api-order` to disable.

#### Parent Project Resolution

The `parent_project` field supports slash-separated paths:

```yaml
project:
  title: "My Subproject"
  parent_project: "Applications/Products"
```

The script walks the hierarchy from root to find the target parent. Raises error if path not found.

---

## Examples

### Example 1: Simple Project with Tasks

```yaml
project:
  title: "Website Redesign"
  parent_project: "Marketing"
  color: "3498db"

labels:
  - title: "Design"
    hex_color: "e74c3c"
  - title: "Development"
    hex_color: "3498db"

tasks:
  - title: "Create wireframes"
    labels:
      - Design
    priority: 3
    due_date: "2025-11-20"

  - title: "Develop frontend"
    labels:
      - Development
    priority: 3
    due_date: "2025-11-30"
    blocked_by:
      - "Create wireframes"
```

### Example 2: Kanban Board Setup

```yaml
project:
  project_id: 13481  # Add to existing project
  buckets:
    - name: "💡 Ideas"
      position: 0
      limit: 0
    - name: "📋 Todo"
      position: 1
      limit: 5
    - name: "🚧 In Progress"
      position: 2
      limit: 3
    - name: "✅ Done"
      position: 3
      limit: 0

tasks:
  - title: "Brainstorm features"
    bucket: "💡 Ideas"
    priority: 1

  - title: "Implement authentication"
    bucket: "📋 Todo"
    priority: 3
    due_date: "2025-11-25"

  - title: "Design landing page"
    bucket: "🚧 In Progress"
    priority: 4
```

### Example 3: Task Dependencies

```yaml
project:
  title: "Mobile App Launch"
  parent_project: "Products"

tasks:
  - title: "Setup development environment"
    priority: 5
    due_date: "2025-11-15"

  - title: "Implement core features"
    priority: 4
    due_date: "2025-11-25"
    blocked_by:
      - "Setup development environment"

  - title: "Write unit tests"
    priority: 3
    due_date: "2025-11-30"
    subtask_of: "Implement core features"

  - title: "Deploy to production"
    priority: 5
    due_date: "2025-12-05"
    blocked_by:
      - "Implement core features"
      - "Write unit tests"
```

### Example 4: Event Preparation (QRCard Template)

See `qrcard-design-template.yaml` for a complete real-world example of:
- Multi-step workflow (design → generate → print → prepare → follow-up)
- HTML descriptions with structured content
- Label assignments for categorization
- Priority and due date management
- Event preparation checklist

### Example 5: Adding Tasks to Existing Project

```yaml
project:
  project_id: 13426  # Don't create new project, add to existing
  title: "Existing Project Name"  # Still need title for display

tasks:
  - title: "New task 1"
    priority: 3

  - title: "New task 2"
    priority: 2
    labels:
      - Existing Label  # Can reference global labels
```

---

## Best Practices

### 1. Project Organization

**Always use parent projects** - Avoid root-level clutter:

```yaml
# ✅ Good
project:
  title: "New Feature"
  parent_project: "Applications/Products"

# ❌ Bad (requires --allow-root-project flag)
project:
  title: "New Feature"
```

**Use descriptive project hierarchy**:

```
Foundations/
├── Infrastructure
├── Tooling
└── Documentation

Applications/
├── Products
├── Internal Tools
└── Prototypes

Operations/
├── Maintenance
├── Security
└── Compliance
```

### 2. Label Strategy

**Create reusable global labels**:

```yaml
labels:
  - title: "Next Action"
    hex_color: "2ecc71"
    description: "Immediate actionable task"

  - title: "Waiting For"
    hex_color: "f39c12"
    description: "Blocked on external dependency"

  - title: "Someday/Maybe"
    hex_color: "95a5a6"
    description: "Future consideration"
```

**Reference existing labels in tasks** without redefining them:

```yaml
tasks:
  - title: "Follow up with client"
    labels:
      - Waiting For  # References existing global label
```

### 3. Task Descriptions

**Use HTML for rich formatting**:

```yaml
tasks:
  - title: "Research CDN providers"
    description: |
      <h3>Goal:</h3>
      <p>Compare Cloudflare vs Fastly vs AWS CloudFront</p>

      <h3>Evaluation Criteria:</h3>
      <ul>
        <li>Performance (TTFB, cache hit rate)</li>
        <li>Pricing ($0.08-0.12/GB typical)</li>
        <li>Feature set (edge functions, analytics)</li>
      </ul>

      <h3>Resources:</h3>
      <ul>
        <li><a href="https://example.com">CDN Comparison Guide</a></li>
        <li><strong>Budget:</strong> $500-2000/month</li>
      </ul>
```

### 4. Priority Levels

Use consistent priority scale:

| Priority | UI Label | Use Case |
|----------|----------|----------|
| 0 | Unset | Backlog items, ideas |
| 1 | Low | Nice-to-have enhancements |
| 2 | Medium | Standard tasks, routine work |
| 3 | High | Important deliverables |
| 4 | Urgent | Time-sensitive tasks |
| 5 | Critical | Emergencies, blockers |

### 5. Kanban Workflow

**Design workflow stages first**:

```yaml
buckets:
  - name: "💡 Ideas"        # position: 0, limit: 0 (no limit)
  - name: "📋 Todo"         # position: 1, limit: 10
  - name: "🚧 In Progress"  # position: 2, limit: 3 (WIP limit)
  - name: "👀 Review"       # position: 3, limit: 5
  - name: "✅ Done"         # position: 4, limit: 0
```

**Use emojis for visual clarity** - Makes columns easy to scan.

### 6. Task Dependencies

**Use `blocked_by` for parallel work**:

```yaml
tasks:
  - title: "Setup CI/CD"
    priority: 5

  - title: "Write tests"
    blocked_by:
      - "Setup CI/CD"

  - title: "Deploy to staging"
    blocked_by:
      - "Setup CI/CD"
      - "Write tests"
```

**Use `subtask_of` for decomposition**:

```yaml
tasks:
  - title: "Implement authentication"
    priority: 4

  - title: "Add login page"
    subtask_of: "Implement authentication"

  - title: "Add logout functionality"
    subtask_of: "Implement authentication"

  - title: "Add password reset"
    subtask_of: "Implement authentication"
```

### 7. Date Formats

**Always use `YYYY-MM-DD` format in YAML**:

```yaml
# ✅ Good
due_date: "2025-11-30"
start_date: "2025-11-15"

# ❌ Bad (will fail validation)
due_date: "11/30/2025"
due_date: "Nov 30, 2025"
```

The population script converts to ISO datetime for API (e.g., `2025-11-30T23:59:59Z`).

### 8. Validation Workflow

**Always dry-run first**:

```bash
# Step 1: Validate schema
python3 populate_vikunja.py tasks.yaml --dry-run

# Step 2: Review output, fix errors

# Step 3: Execute
python3 populate_vikunja.py tasks.yaml
```

### 9. LLM Integration Tips

When generating YAML from LLMs:

1. **Provide this reference document** as context
2. **Show example YAML** for the specific use case
3. **Validate output** with dry-run before execution
4. **Use templates** (like `qrcard-design-template.yaml`) for common workflows

Example LLM prompt:

```
Generate a Vikunja YAML file for a website redesign project.

Requirements:
- Parent project: "Marketing"
- Tasks: wireframes, design system, frontend dev, testing
- Use "Design" and "Development" labels
- Set up Kanban board with Ideas, Todo, In Progress, Done
- Add blocking dependencies where appropriate

Reference schema: [paste relevant sections from this doc]
```

### 10. Quick Task Creation Script

For ad-hoc task creation, use `create_task.py`:

```bash
# Simple task
python3 create_task.py --project-id 13426 --title "Review metrics"

# Task with bucket assignment
python3 create_task.py \
  --project-id 13481 \
  --title "Implement feature X" \
  --bucket "Todo" \
  --priority 3 \
  --due-date "2025-11-30"

# Recurring task
python3 create_task.py \
  --project-id 13426 \
  --title "Weekly review" \
  --repeat-weekly \
  --repeat-from-completion \
  --due-date "next sunday"
```

---

## Integration Patterns

### Pattern 1: Agent-Driven Task Generation

```python
# LLM agent generates YAML from conversation
from vikunja_wrapper import VikunjaClient
from population import populate_vikunja
import yaml

# 1. Agent generates YAML
yaml_content = agent.generate_task_yaml(user_request)

# 2. Validate schema
schema = yaml.safe_load(yaml_content)
validate_schema(schema)

# 3. Populate Vikunja
client = VikunjaClient(base_url="...", token="...")
result = populate_vikunja(client, schema, dry_run=False)

print(f"Created project: {result['project'].title}")
print(f"Created {len(result['tasks'])} tasks")
```

### Pattern 2: Batch Project Setup

```python
# Setup multiple related projects from templates
import glob

for template_file in glob.glob("templates/*.yaml"):
    print(f"Processing {template_file}...")

    # Validate first
    result = subprocess.run(
        ["python3", "populate_vikunja.py", template_file, "--dry-run"],
        capture_output=True
    )

    if result.returncode == 0:
        # Execute
        subprocess.run(["python3", "populate_vikunja.py", template_file])
    else:
        print(f"Validation failed: {result.stderr}")
```

### Pattern 3: Dynamic Project from Data

```python
# Generate project from external data (e.g., GitHub issues)
import requests
import yaml

# Fetch issues from GitHub
response = requests.get("https://api.github.com/repos/owner/repo/issues")
issues = response.json()

# Build YAML schema
schema = {
    "project": {
        "title": "GitHub Migration",
        "parent_project": "Operations/Maintenance"
    },
    "labels": [
        {"title": "Bug", "hex_color": "d73a4a"},
        {"title": "Enhancement", "hex_color": "a2eeef"}
    ],
    "tasks": []
}

for issue in issues:
    schema["tasks"].append({
        "title": issue["title"],
        "description": issue["body"],
        "labels": [label["name"] for label in issue["labels"]],
        "priority": 3 if "bug" in [l["name"] for l in issue["labels"]] else 2
    })

# Populate Vikunja
with open("github-migration.yaml", "w") as f:
    yaml.dump(schema, f)

subprocess.run(["python3", "populate_vikunja.py", "github-migration.yaml"])
```

---

## Troubleshooting

### Common Errors

#### "Project must have a parent_project or parent_project_id"

**Cause:** Root-level projects are not allowed by default.

**Solution:**
```yaml
# Add parent project
project:
  title: "My Project"
  parent_project: "Applications"  # Add this

# OR use flag (not recommended)
python3 populate_vikunja.py tasks.yaml --allow-root-project
```

#### "Parent project not found: 'Applications/Products'"

**Cause:** Parent project path doesn't exist.

**Solution:** Create parent projects first:
```yaml
# Step 1: Create parent
project:
  title: "Products"
  parent_project: "Applications"

# Step 2: Create child
project:
  title: "My Product"
  parent_project: "Applications/Products"
```

#### "Label 'Design' not found"

**Cause:** Task references label not defined in YAML or globally.

**Solution:**
```yaml
# Add label definition
labels:
  - title: "Design"
    hex_color: "e74c3c"

tasks:
  - title: "My Task"
    labels:
      - Design  # Now found
```

#### "Hex color must be exactly 6 characters"

**Cause:** Invalid color format.

**Solution:**
```yaml
# ✅ Good
color: "3498db"
hex_color: "e74c3c"

# ❌ Bad
color: "#3498db"  # Remove #
color: "34db"     # Need 6 chars
```

#### "Date must be YYYY-MM-DD format"

**Cause:** Invalid date format.

**Solution:**
```yaml
# ✅ Good
due_date: "2025-11-30"

# ❌ Bad
due_date: "11/30/2025"
due_date: "Nov 30"
```

### API Token Issues

If authentication fails:

1. **Generate new token** in Vikunja UI: Settings > API Tokens
2. **Verify environment variable**:
   ```bash
   echo $VIKUNJA_API_TOKEN
   ```
3. **Check `.env` file** exists and is loaded
4. **Test connection**:
   ```python
   from vikunja_wrapper import VikunjaClient
   client = VikunjaClient(base_url="...", token="...")
   projects = client.projects.list()  # Should not raise AuthenticationError
   ```

---

## Additional Resources

- **Vikunja API Docs**: https://vikunja.io/docs/api/
- **Example YAML Files**: `research/1.131-project-management/02-implementations/vikunja-populate-script/`
- **API Wrapper Source**: `research/1.131-project-management/02-implementations/vikunja-api-wrapper/src/vikunja_wrapper.py`
- **Population Script**: `research/1.131-project-management/02-implementations/vikunja-populate-script/src/populate_vikunja.py`

---

## Quick Reference: File Paths

```
research/1.131-project-management/02-implementations/
├── vikunja-api-wrapper/
│   └── src/
│       └── vikunja_wrapper.py          # Python API client
├── vikunja-populate-script/
│   ├── src/
│   │   ├── populate_vikunja.py         # Main population script
│   │   ├── validation.py               # Schema validation
│   │   ├── population.py               # Population logic
│   │   └── parsing.py                  # YAML parsing
│   ├── qrcard-design-template.yaml     # Real-world example
│   └── llm-gtd-next-steps.yaml         # Complex example
└── tools/
    └── create_task.py                   # Quick task creation CLI
```

---

**Last Updated:** November 12, 2025
**Version:** 1.0
**Maintainer:** inversefractional.com
