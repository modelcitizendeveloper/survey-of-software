# Vikunja Population Script - Input Schema

**Valid formats**: YAML or JSON

---

## Schema Structure

```yaml
# Project definition
project:
  title: "Project Name"                    # Required: string
  description: "Project description"       # Optional: string
  color: "FF0000"                          # Optional: hex color (no #)
  buckets:                                 # Optional: Kanban board buckets
    - name: "Backlog"                      # Required: bucket name
      position: 0                          # Required: sort order
      limit: 0                             # Optional: WIP limit (0 = no limit)
    - name: "In Progress"
      position: 1
      limit: 3                             # WIP limit: max 3 tasks
    - name: "Done"
      position: 2

# Labels to create/use
labels:
  - title: "Bug"                           # Required: string
    description: "Bug fixes"               # Optional: string
    color: "FF0000"                        # Optional: hex color (default: random)
  - title: "Feature"
    color: "00FF00"

# Tasks to create
tasks:
  - title: "Task name"                     # Required: string
    description: "Task description"        # Optional: string (HTML formatting supported)
    due_date: "2025-11-15"                 # Optional: YYYY-MM-DD format
    priority: 0                            # Optional: 0-5 (0=unset, 5=DO NOW)
    bucket: "Backlog"                      # Optional: bucket name (Kanban column)
    labels:                                # Optional: list of label titles
      - "Bug"
      - "Feature"
    blocked_by:                            # Optional: list of blocking task titles
      - "Other Task Name"
    subtask_of: "Parent Task Name"         # Optional: parent task title
    assignees:                             # Optional: list of user emails/usernames
      - "user@example.com"
      - "username"
    done: false                            # Optional: boolean (default: false)
```

---

## Example: SEA Week 1 Tasks

```yaml
project:
  title: "Schema Evolution Automation"
  description: "12-week implementation plan for Phase 1"
  color: "4287f5"

labels:
  - title: "Week 1"
    color: "ff6b6b"
  - title: "Foundation"
    color: "4ecdc4"

tasks:
  - title: "Week 1: Project Foundation"
    description: |
      <strong>Goal:</strong> Set up development environment, core structure, CI/CD<br><br>
      <strong>Tasks:</strong><br>
      - Initialize git repository<br>
      - Set up Python project structure<br>
      - Configure pytest<br>
      - Set up pre-commit hooks<br>
      - GitHub Actions CI/CD<br>
      - Create core data structures
    due_date: "2025-11-14"
    priority: 0
    labels:
      - "Week 1"
      - "Foundation"
```

---

## Example: Sprint with Dependencies and Kanban

```yaml
project:
  title: "Sprint 1: User Authentication"
  description: "Implement user authentication with dependencies and workflow"
  color: "4287f5"
  buckets:
    - name: "Backlog"
      position: 0
    - name: "In Progress"
      position: 1
      limit: 3  # WIP limit
    - name: "Code Review"
      position: 2
      limit: 2
    - name: "Done"
      position: 3

labels:
  - title: "Backend"
    color: "ff6b6b"
  - title: "Frontend"
    color: "4ecdc4"
  - title: "DevOps"
    color: "95e1d3"

tasks:
  # Foundation tasks
  - title: "Design Database Schema"
    description: "Create user tables and authentication schema"
    bucket: "In Progress"
    priority: 5
    labels:
      - "Backend"
    assignees:
      - "architect@team.com"

  # Backend tasks (blocked by schema)
  - title: "Implement Login Endpoint"
    description: "POST /api/auth/login with JWT"
    bucket: "Backlog"
    priority: 4
    blocked_by:
      - "Design Database Schema"
    subtask_of: "Backend API Implementation"
    labels:
      - "Backend"
    assignees:
      - "backend-dev@team.com"

  - title: "Implement Registration Endpoint"
    description: "POST /api/auth/register with validation"
    bucket: "Backlog"
    priority: 4
    blocked_by:
      - "Design Database Schema"
    subtask_of: "Backend API Implementation"
    labels:
      - "Backend"
    assignees:
      - "backend-dev@team.com"

  # Parent task for backend
  - title: "Backend API Implementation"
    description: "Complete all authentication endpoints"
    bucket: "In Progress"
    priority: 5
    labels:
      - "Backend"

  # Frontend tasks (blocked by backend)
  - title: "Build Login Form Component"
    description: "React component with form validation"
    bucket: "Backlog"
    priority: 3
    blocked_by:
      - "Implement Login Endpoint"
    labels:
      - "Frontend"
    assignees:
      - "frontend-dev@team.com"

  - title: "Build Registration Form"
    description: "React component with email validation"
    bucket: "Backlog"
    priority: 3
    blocked_by:
      - "Implement Registration Endpoint"
    labels:
      - "Frontend"
    assignees:
      - "frontend-dev@team.com"

  # Deployment (blocked by everything)
  - title: "Deploy to Staging"
    description: "Deploy authentication system to staging environment"
    bucket: "Backlog"
    priority: 2
    blocked_by:
      - "Build Login Form Component"
      - "Build Registration Form"
      - "Backend API Implementation"
    labels:
      - "DevOps"
    assignees:
      - "devops@team.com"
```

**This example demonstrates**:
- Kanban board with 4 buckets (Backlog → In Progress → Code Review → Done)
- WIP limits on "In Progress" and "Code Review"
- Task dependencies (`blocked_by`)
- Parent-child relationships (`subtask_of`)
- Task assignments to team members
- Multiple labels per task
- Priority-based ordering

---

## JSON Example

```json
{
  "project": {
    "title": "My Project",
    "description": "Project description"
  },
  "labels": [
    {"title": "Bug", "color": "FF0000"}
  ],
  "tasks": [
    {
      "title": "Fix login",
      "priority": 5,
      "labels": ["Bug"]
    }
  ]
}
```

---

## Validation Rules

### Project
- `title` (required): Non-empty string, max 250 chars
- `description` (optional): String, max 5000 chars
- `color` (optional): 6-char hex color without `#`
- `buckets` (optional): List of bucket definitions
  - `name` (required): Non-empty string
  - `position` (required): Integer (sort order)
  - `limit` (optional): Integer (0 = no limit)

### Labels
- `title` (required): Non-empty string, max 100 chars
- `description` (optional): String, max 500 chars
- `color` (optional): 6-char hex color without `#`

### Tasks
- `title` (required): Non-empty string, max 250 chars
- `description` (optional): String (HTML allowed), max 50000 chars
- `due_date` (optional): ISO date `YYYY-MM-DD` format
- `priority` (optional): Integer 0-5
- `bucket` (optional): String (must match a defined bucket name)
- `labels` (optional): List of strings matching label titles
- `blocked_by` (optional): List of strings (task titles that block this task)
- `subtask_of` (optional): String (parent task title)
- `assignees` (optional): List of strings (user emails or usernames)
- `done` (optional): Boolean

---

## Error Handling

**Schema validation errors:**
- Missing required fields → Clear error message with field name
- Invalid data types → Type mismatch error
- Invalid formats (dates, colors) → Format validation error
- Label references non-existent label → Reference error

**API errors:**
- 401 Unauthorized → Token invalid/expired
- 403 Forbidden → Insufficient permissions
- 404 Not Found → Invalid endpoint (check wrapper version)
- 422 Validation Error → Vikunja rejected data (check field constraints)

---

## Usage

```bash
# YAML input
python populate_vikunja.py tasks.yaml

# JSON input
python populate_vikunja.py tasks.json

# Dry run (validate only, don't create)
python populate_vikunja.py --dry-run tasks.yaml

# Verbose output
python populate_vikunja.py --verbose tasks.yaml
```
