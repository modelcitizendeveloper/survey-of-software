# Task Specification: Vikunja Python API Wrapper

**Experiment**: Vikunja API Wrapper (Method 4 - Adaptive TDD)
**Date**: November 7, 2025
**Framework**: spawn-experiments library wrapper pattern

---

## Objective

Create a production-quality Python wrapper for the Vikunja REST API that simplifies integration and handles errors gracefully.

---

## Requirements

### 1. Core Functionality

#### 1.1 Authentication
```python
client = VikunjaClient(
    base_url="https://vikunja.cloud",
    token="your-api-token"
)

# Alternative: login with credentials
client = VikunjaClient.login(
    base_url="https://vikunja.cloud",
    username="user@example.com",
    password="password"
)
```

**Requirements**:
- Support token-based authentication
- Support username/password login (gets token)
- Store token for subsequent requests
- Handle token refresh if needed

---

#### 1.2 Projects (Lists) Management

**Create Project**:
```python
project = client.projects.create(
    title="My Project",
    description="Project description"
)
# Returns: Project object with id, title, description, created_at, etc.
```

**List Projects**:
```python
projects = client.projects.list()
# Returns: List of Project objects
```

**Get Project**:
```python
project = client.projects.get(project_id=123)
# Returns: Project object
```

**Update Project**:
```python
updated = client.projects.update(
    project_id=123,
    title="Updated Title",
    description="Updated description"
)
# Returns: Updated Project object
```

**Delete Project**:
```python
client.projects.delete(project_id=123)
# Returns: None (or success boolean)
```

---

#### 1.3 Tasks Management

**Create Task**:
```python
task = client.tasks.create(
    project_id=123,
    title="New task",
    description="Task description",
    due_date="2025-11-15",  # String or datetime
    priority=5,
    labels=["bug", "urgent"]
)
# Returns: Task object
```

**List Tasks**:
```python
# All tasks in project
tasks = client.tasks.list(project_id=123)

# With filters
tasks = client.tasks.list(
    project_id=123,
    filter_by_labels=["bug"],
    filter_by_priority=5,
    sort_by="due_date"
)
# Returns: List of Task objects
```

**Get Task**:
```python
task = client.tasks.get(task_id=456)
# Returns: Task object
```

**Update Task**:
```python
updated = client.tasks.update(
    task_id=456,
    title="Updated title",
    done=True,
    priority=3
)
# Returns: Updated Task object
```

**Delete Task**:
```python
client.tasks.delete(task_id=456)
# Returns: None (or success boolean)
```

---

#### 1.4 Labels Management

**Create Label**:
```python
label = client.labels.create(
    title="bug",
    hex_color="#FF0000"
)
# Returns: Label object
```

**List Labels**:
```python
labels = client.labels.list()
# Returns: List of Label objects
```

**Update Label**:
```python
updated = client.labels.update(
    label_id=789,
    title="critical-bug",
    hex_color="#FF0000"
)
# Returns: Updated Label object
```

---

### 2. Error Handling

**Handle all common errors gracefully**:

```python
from vikunja_wrapper import VikunjaClient, VikunjaError, AuthenticationError, NotFoundError

try:
    client = VikunjaClient(base_url="https://vikunja.cloud", token="invalid")
    task = client.tasks.create(...)
except AuthenticationError:
    print("Invalid credentials")
except NotFoundError:
    print("Resource not found")
except VikunjaError as e:
    print(f"API error: {e}")
```

**Required Exception Classes**:
- `VikunjaError` (base exception)
- `AuthenticationError` (401 errors)
- `NotFoundError` (404 errors)
- `ValidationError` (400 errors)
- `RateLimitError` (429 errors)
- `ServerError` (500+ errors)

**Error Handling Requirements**:
- Clear error messages
- Include API response details when available
- Handle network errors (connection timeout, DNS failure)
- Handle malformed JSON responses

---

### 3. Data Models

**Use dataclasses or Pydantic for type safety**:

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

@dataclass
class Project:
    id: int
    title: str
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Task:
    id: int
    title: str
    project_id: int
    description: Optional[str] = None
    done: bool = False
    due_date: Optional[datetime] = None
    priority: int = 0
    labels: List[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Label:
    id: int
    title: str
    hex_color: str
    created_at: Optional[datetime] = None
```

**Requirements**:
- Type hints for all fields
- Convert API JSON to Python objects
- Handle datetime parsing (ISO 8601 format)
- Provide `.to_dict()` method for serialization

---

### 4. Code Quality

**Follow Python best practices**:

- ✅ PEP 8 style guide
- ✅ Type hints throughout
- ✅ Docstrings for all public methods
- ✅ Clear variable names
- ✅ Single Responsibility Principle
- ✅ DRY (Don't Repeat Yourself)

**No over-engineering**:
- ❌ Don't create unnecessary abstraction layers
- ❌ Don't implement features not in spec
- ❌ Don't add complex dependency injection
- ✅ Keep it simple and readable

**Target LOC**: 200-300 lines (consistent with spawn-experiments 1.610 pattern)

---

### 5. Testing

**Comprehensive test suite**:

```python
# test_vikunja_wrapper.py

import pytest
from vikunja_wrapper import VikunjaClient, AuthenticationError
from unittest.mock import Mock, patch

def test_client_creation():
    client = VikunjaClient(base_url="https://test.com", token="test-token")
    assert client.base_url == "https://test.com"
    assert client.token == "test-token"

def test_authentication_error():
    with pytest.raises(AuthenticationError):
        client = VikunjaClient(base_url="https://test.com", token="invalid")
        # Mock API call that returns 401
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 401
            client.projects.list()

def test_create_project():
    client = VikunjaClient(base_url="https://test.com", token="test")
    with patch('requests.post') as mock_post:
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            "id": 123,
            "title": "Test Project",
            "created_at": "2025-11-07T12:00:00Z"
        }

        project = client.projects.create(title="Test Project")
        assert project.id == 123
        assert project.title == "Test Project"

# More tests...
```

**Required Tests**:
- Client initialization
- Authentication (valid/invalid tokens)
- CRUD operations for Projects, Tasks, Labels
- Error handling (401, 404, 500, network errors)
- Data model serialization/deserialization
- Edge cases (empty responses, missing fields)

**Test Coverage Target**: >70%

---

### 6. Documentation

**Module Docstring**:
```python
"""
Vikunja Python API Wrapper

A simple, production-ready wrapper for the Vikunja REST API.

Basic Usage:
    from vikunja_wrapper import VikunjaClient

    # Initialize client
    client = VikunjaClient(
        base_url="https://vikunja.cloud",
        token="your-api-token"
    )

    # Create project
    project = client.projects.create(title="My Project")

    # Create task
    task = client.tasks.create(
        project_id=project.id,
        title="My Task",
        due_date="2025-11-15"
    )

For full documentation, see: https://vikunja.io/docs/api/
"""
```

**Method Docstrings**:
```python
def create(self, title: str, description: str = None) -> Project:
    """
    Create a new project.

    Args:
        title: Project title (required)
        description: Project description (optional)

    Returns:
        Project: Created project object

    Raises:
        AuthenticationError: If token is invalid
        ValidationError: If title is empty or invalid
        VikunjaError: For other API errors

    Example:
        >>> client = VikunjaClient(...)
        >>> project = client.projects.create(title="My Project")
        >>> print(project.id)
        123
    """
```

**README with examples**:
- Installation instructions
- Quick start guide
- Common use cases
- Error handling examples
- API reference link

---

### 7. Dependencies

**Minimal dependencies**:
```
# requirements.txt
requests>=2.31.0
python-dateutil>=2.8.2
```

**Optional** (if using Pydantic instead of dataclasses):
```
pydantic>=2.0.0
```

---

## Non-Requirements

**Out of Scope** (don't implement):
- ❌ Advanced features (webhooks, attachments, comments)
- ❌ Rate limit handling (just raise error if hit)
- ❌ Pagination (return all results, no lazy loading)
- ❌ Caching (every call hits API)
- ❌ Retry logic (fail fast)
- ❌ Async support (synchronous only)

**Keep it simple**: Focus on core CRUD operations with good error handling.

---

## Acceptance Criteria

### Must Have:
1. ✅ All CRUD operations work (Projects, Tasks, Labels)
2. ✅ Authentication with token
3. ✅ Proper error handling with custom exceptions
4. ✅ Type hints throughout
5. ✅ Comprehensive docstrings
6. ✅ Test coverage >70%
7. ✅ Usage examples in README

### Should Have:
1. ✅ Data models (dataclasses or Pydantic)
2. ✅ Date/time handling (ISO 8601 parsing)
3. ✅ Clean, readable code (<300 LOC)
4. ✅ PEP 8 compliant

### Nice to Have:
1. ⚠️ Login method (username/password → token)
2. ⚠️ Filter support for task listing
3. ⚠️ Sort support for task listing

---

## Example Usage (Reference Implementation)

```python
from vikunja_wrapper import VikunjaClient

# Initialize
client = VikunjaClient(
    base_url="https://vikunja.cloud",
    token="your-api-token"
)

# Create project
project = client.projects.create(
    title="Schema Evolution Automation",
    description="12-week implementation plan"
)

# Create tasks for each week
for week in range(1, 13):
    task = client.tasks.create(
        project_id=project.id,
        title=f"Week {week}: Implementation milestone",
        description=f"Complete week {week} tasks",
        due_date=f"2025-{week:02d}-01",
        priority=5 if week <= 4 else 3,
        labels=["SEA", "development"]
    )
    print(f"Created task: {task.id} - {task.title}")

# List all tasks
tasks = client.tasks.list(project_id=project.id)
print(f"Total tasks: {len(tasks)}")

# Update task (mark as done)
updated = client.tasks.update(task_id=tasks[0].id, done=True)
print(f"Task {updated.id} marked as done")

# Delete task
client.tasks.delete(task_id=tasks[-1].id)
print("Last task deleted")
```

---

## Success Metrics

**Target Score**: 90-95/100 (Method 4 historical average)

**Rubric** (100 points total):
- **Functionality** (40 pts): All CRUD operations, error handling, edge cases
- **Code Quality** (30 pts): Readable, well-designed, not over-engineered, PEP 8
- **Documentation** (15 pts): Module docs, method docs, usage examples
- **Testing** (15 pts): Test coverage, test quality

**Historical Context** (spawn-experiments 1.610):
- FastText wrapper: 92/100
- sklearn wrapper: 94/100
- **Target**: Vikunja wrapper: 90-95/100

---

**Specification Complete**: Ready for Method 4 (Adaptive TDD) execution
**Estimated Development Time**: 15-30 minutes (with Task agent)
**Last Updated**: November 7, 2025
