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
    labels:                                # Optional: list of label titles
      - "Bug"
      - "Feature"
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

### Labels
- `title` (required): Non-empty string, max 100 chars
- `description` (optional): String, max 500 chars
- `color` (optional): 6-char hex color without `#`

### Tasks
- `title` (required): Non-empty string, max 250 chars
- `description` (optional): String (HTML allowed), max 50000 chars
- `due_date` (optional): ISO date `YYYY-MM-DD` format
- `priority` (optional): Integer 0-5
- `labels` (optional): List of strings matching label titles
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
