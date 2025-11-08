# Vikunja Python API Wrapper

A simple, production-ready Python wrapper for the [Vikunja](https://vikunja.io) REST API.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```python
from vikunja_wrapper import VikunjaClient

# Initialize client with API token
client = VikunjaClient(
    base_url="https://vikunja.cloud",
    token="your-api-token"
)

# Create a project
project = client.projects.create(
    title="My Project",
    description="Project description"
)

# Create a task
task = client.tasks.create(
    project_id=project.id,
    title="My First Task",
    description="Task description",
    priority=5,
    due_date="2025-11-15"
)

# List all tasks
tasks = client.tasks.list(project_id=project.id)
for task in tasks:
    print(f"{task.id}: {task.title}")

# Update task
updated_task = client.tasks.update(
    task_id=task.id,
    done=True
)

# Delete task
client.tasks.delete(task_id=task.id)
```

## Features

- **Simple API**: Clean, Pythonic interface for Vikunja operations
- **Type Safety**: Full type hints throughout
- **Error Handling**: Comprehensive custom exceptions
- **Data Models**: Strongly-typed dataclasses for Projects, Tasks, Labels
- **Production Ready**: Defensive programming with proper error handling

## API Reference

### Client Initialization

```python
client = VikunjaClient(base_url="https://vikunja.cloud", token="your-token")
```

### Projects

```python
# Create project
project = client.projects.create(title="Project Name", description="Description")

# List all projects
projects = client.projects.list()

# Get specific project
project = client.projects.get(project_id=123)

# Update project
project = client.projects.update(project_id=123, title="New Title")

# Delete project
client.projects.delete(project_id=123)
```

### Tasks

```python
# Create task
task = client.tasks.create(
    project_id=123,
    title="Task Title",
    description="Task description",
    due_date="2025-11-15",
    priority=5,
    labels=["bug", "urgent"]
)

# List tasks in project
tasks = client.tasks.list(project_id=123)

# Get specific task
task = client.tasks.get(task_id=456)

# Update task
task = client.tasks.update(
    task_id=456,
    title="Updated Title",
    done=True,
    priority=3
)

# Delete task
client.tasks.delete(task_id=456)
```

### Labels

```python
# Create label
label = client.labels.create(title="bug", hex_color="#FF0000")

# List all labels
labels = client.labels.list()

# Update label
label = client.labels.update(label_id=789, title="critical-bug")
```

## Error Handling

The wrapper provides custom exceptions for different error scenarios:

```python
from vikunja_wrapper import (
    VikunjaError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError
)

try:
    task = client.tasks.create(project_id=123, title="New Task")
except AuthenticationError:
    print("Invalid API token")
except NotFoundError:
    print("Project not found")
except ValidationError:
    print("Invalid task parameters")
except RateLimitError:
    print("Rate limit exceeded")
except ServerError:
    print("Server error")
except VikunjaError as e:
    print(f"API error: {e}")
```

## Data Models

### Project

```python
@dataclass
class Project:
    id: int
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### Task

```python
@dataclass
class Task:
    id: int
    title: str
    project_id: int
    description: Optional[str] = None
    done: bool = False
    due_date: Optional[datetime] = None
    priority: int = 0
    labels: Optional[List[str]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

### Label

```python
@dataclass
class Label:
    id: int
    title: str
    hex_color: str
    created_at: Optional[datetime] = None
```

## Real-World Examples

### Schema Evolution Automation (SEA)

Auto-populate Vikunja from an implementation plan:

```python
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url="https://vikunja.cloud",
    token="your-token"
)

# Create project for SEA implementation
sea_project = client.projects.create(
    title="Schema Evolution Automation",
    description="12-week implementation plan"
)

# Create tasks for each week
milestones = [
    ("Week 1: Setup", "2025-11-15", 5),
    ("Week 2: Core Features", "2025-11-22", 5),
    ("Week 3: Testing", "2025-11-29", 4),
    # ... more weeks
]

for title, due_date, priority in milestones:
    task = client.tasks.create(
        project_id=sea_project.id,
        title=title,
        due_date=due_date,
        priority=priority,
        labels=["SEA", "development"]
    )
    print(f"Created: {task.title}")
```

### Content Pipeline Automation

Auto-create content tasks from research:

```python
# When research completes, create content tasks
research_items = [
    ("1.131", "Self-hosted PM", "2025-11-15"),
    ("3.007", "FP&A Platforms", "2025-11-22"),
]

content_project = client.projects.create(title="Content Pipeline")

for exp_id, title, publish_date in research_items:
    client.tasks.create(
        project_id=content_project.id,
        title=f"Convert {exp_id} to framework",
        description=f"Research: {title}",
        due_date=publish_date,
        labels=["research-to-content", exp_id]
    )
```

### Bug Tracking Integration

Auto-create tasks from production errors:

```python
def create_bug_task(error_info):
    """Create Vikunja task from error."""
    client = VikunjaClient(
        base_url="https://vikunja.cloud",
        token="your-token"
    )

    task = client.tasks.create(
        project_id=bugs_project_id,
        title=f"Bug: {error_info['message']}",
        description=error_info['stacktrace'],
        priority=5 if error_info['severity'] == 'critical' else 3,
        labels=["bug", "auto-created", error_info['severity']]
    )

    return task
```

## Testing

Run the test suite:

```bash
pytest test_vikunja_wrapper.py -v
```

Expected output:
```
test_vikunja_wrapper.py::TestClientInitialization::test_client_with_token PASSED
test_vikunja_wrapper.py::TestProjects::test_create_project PASSED
test_vikunja_wrapper.py::TestTasks::test_create_task PASSED
test_vikunja_wrapper.py::TestLabels::test_create_label PASSED
test_vikunja_wrapper.py::TestErrorHandling::test_authentication_error PASSED
...
```

## Development

This wrapper was created using **Method 4 (Adaptive TDD)** from spawn-experiments:

1. Write tests first for core functionality
2. Implement code to pass tests
3. Refactor for quality
4. Strong error handling (defensive programming)
5. Clean code (200-300 lines target)
6. Comprehensive docstrings

## API Documentation

For full Vikunja API documentation, see: https://vikunja.io/docs/api/

## License

MIT License

## Contributing

This is a reference implementation from spawn-solutions research. Feel free to adapt and extend for your use case.
