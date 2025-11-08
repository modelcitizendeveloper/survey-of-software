# Vikunja API Wrapper - Library Wrapper Experiment

**Date**: November 7, 2025
**Type**: Library Wrapper Code Generation
**Framework**: Method 4 (Adaptive TDD) from spawn-experiments
**Status**: In Progress

---

## Purpose

Create a production-quality Python wrapper for the Vikunja REST API to simplify integration with automation systems (SEA, cookbooks, qrcards, etc.).

**Hardware Store Value**: Generic reference implementation for anyone using Vikunja who needs programmatic access.

---

## Research Question

Can we generate a clean, production-ready API wrapper for Vikunja using Method 4 (Adaptive TDD)?

**Hypothesis**: Method 4 will produce 90-95/100 quality score (consistent with spawn-experiments 1.610 library wrapper findings)

---

## Context from spawn-experiments

### Established Pattern (Experiments 1.610, 1.611)

**Method 4 (Adaptive TDD) consistently wins for library wrappers**:
- FastText wrapper: 92/100
- sklearn wrapper: 94/100
- Prophet wrapper: (experiment 1.611 validation)

**Why Method 4 wins**:
1. ✅ Defensive error handling (critical for API wrappers)
2. ✅ Production quality (not over-engineered like Method 2)
3. ✅ Fast development (1-2 minutes with Task agents)
4. ✅ Right abstraction level (200-300 lines, not 1000+)

**Rejected methodologies**:
- ❌ Method 1: 50% failure rate, missing error handling
- ❌ Method 2: Over-engineered by 5-6X (unnecessary abstractions)
- ⚠️ Method 3: Works but less robust than Method 4

---

## Target: Vikunja REST API

**API Documentation**: https://try.vikunja.io/api/v1/docs

### Core Endpoints to Wrap

**Projects** (Lists):
- `GET /api/v1/projects` - List all projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

**Tasks**:
- `GET /api/v1/projects/{id}/tasks` - List tasks in project
- `POST /api/v1/projects/{id}/tasks` - Create task
- `GET /api/v1/tasks/{id}` - Get task
- `PUT /api/v1/tasks/{id}` - Update task
- `DELETE /api/v1/tasks/{id}` - Delete task

**Labels**:
- `GET /api/v1/labels` - List all labels
- `POST /api/v1/labels` - Create label
- `PUT /api/v1/labels/{id}` - Update label

**Authentication**:
- `POST /api/v1/login` - Get auth token
- Token-based auth for all API calls

---

## Success Criteria

### Functionality (40 points)
- ✅ All CRUD operations work (Projects, Tasks, Labels)
- ✅ Authentication handling (token-based)
- ✅ Error handling (network, auth, rate limits, API errors)
- ✅ Edge cases handled (empty responses, missing fields)

### Code Quality (30 points)
- ✅ Clean, readable code
- ✅ Good class design (not over-engineered)
- ✅ Follows Python conventions (PEP 8)
- ✅ No unnecessary abstractions

### Documentation (15 points)
- ✅ Module-level docstring
- ✅ Method docstrings with examples
- ✅ Usage examples in README
- ✅ Clear error messages

### Testing (15 points)
- ✅ Unit tests for key methods
- ✅ Mock API responses for testing
- ✅ Test coverage >70%

**Target Score**: 90-95/100 (Method 4 historical average)

---

## API Simplification Goal

### Before (Raw requests)
```python
import requests

token = "eyJ..."
response = requests.post(
    "https://vikunja.cloud/api/v1/projects/123/tasks",
    headers={"Authorization": f"Bearer {token}"},
    json={
        "title": "New task",
        "description": "Task description",
        "due_date": "2025-11-15T00:00:00Z"
    }
)
if response.status_code == 200:
    task = response.json()
else:
    # Handle error...
    pass
```

### After (Wrapper)
```python
from vikunja_wrapper import VikunjaClient

client = VikunjaClient(
    base_url="https://vikunja.cloud",
    token="eyJ..."
)

task = client.tasks.create(
    project_id=123,
    title="New task",
    description="Task description",
    due_date="2025-11-15"
)
```

**Benefits**:
- ✅ Cleaner API (no manual headers, JSON handling)
- ✅ Automatic error handling
- ✅ Type hints for better IDE support
- ✅ Pythonic interface (snake_case, not camelCase)

---

## Use Cases (from 1.131 Research)

### 1. SEA (Schema Evolution Automation)
**Auto-populate Vikunja from implementation plan**:
```python
# Parse SEA/project/IMPLEMENTATION_PLAN.md
client = VikunjaClient(...)
sea_project = client.projects.create(name="Schema Evolution Automation")

for week in range(1, 13):
    client.tasks.create(
        project_id=sea_project.id,
        title=f"Week {week}: {milestone_name}",
        due_date=week_end_date,
        description=milestone_details
    )
```

### 2. Cookbooks (Content Pipeline)
**Automated content calendar**:
```python
# When research completes, create content tasks
research_experiments = [
    ("1.131", "Self-hosted PM", "2025-11-15"),
    ("3.007", "FP&A Platforms", "2025-11-22"),
]

for exp_id, title, publish_date in research_experiments:
    client.tasks.create(
        project_id=cookbooks_project_id,
        title=f"Convert {exp_id} to framework",
        due_date=publish_date,
        labels=["research-to-content", exp_id]
    )
```

### 3. QRCards (Issue Tracking)
**Auto-create tasks from production errors**:
```python
# Sentry webhook integration
@sentry_sdk.before_send
def create_vikunja_bug(event, hint):
    if is_new_error(event):
        client.tasks.create(
            project_id=qrcards_project_id,
            title=f"Bug: {event['message']}",
            description=event['stacktrace'],
            labels=["bug", "auto-created"]
        )
    return event
```

---

## Execution Plan

### Phase 1: Documentation (30 min) ✅
1. ✅ Create `README.md` (this file)
2. ⏳ Create `TASK_SPECIFICATION.md` (detailed requirements)
3. ⏳ Create `PREDICTIONS.md` (V4 framework predictions)

### Phase 2: Method 4 Execution (15-30 min)
1. Run Method 4 (Adaptive TDD) with Task agent
2. Generate `method-4-adaptive-tdd/vikunja_wrapper.py`
3. Generate `method-4-adaptive-tdd/test_vikunja_wrapper.py`
4. Review generated code

### Phase 3: Validation (30 min)
1. Run tests (pytest)
2. Manual API testing (if have Vikunja instance)
3. Score against rubric (100 points)
4. Compare to predictions

### Phase 4: Integration (15 min)
1. Document findings in `EXPERIMENT_REPORT.md`
2. Update 1.131 S1 to reference implementation
3. Add usage examples to S3 patterns

**Total Time**: ~2 hours

---

## Expected Outcomes

### Methodology Validation
- **Prediction**: Method 4 scores 90-95/100 (consistent with 1.610)
- **Test**: Does API wrapper domain match text processing/time series pattern?

### Reference Implementation
**Winner** (likely Method 4) becomes:
- Generic reference for Vikunja integrations
- Example for other PM tool API wrappers (Plane, Taiga, etc.)
- Pattern for 1.131 S3 automation examples

### Hardware Store Value
**Developers find**:
1. S1: "Vikunja has full REST API"
2. S3: "Pattern: Multi-project automation"
3. **02-implementations**: "Here's production Python wrapper" ← THIS

**Time saved**: 8-12 hours vs writing wrapper from scratch

---

## Files

- `README.md` - This file (experiment overview)
- `TASK_SPECIFICATION.md` - Detailed wrapper requirements
- `PREDICTIONS.md` - Pre-execution predictions (V4 framework)
- `method-4-adaptive-tdd/` - Method 4 implementation (EXPECTED WINNER)
  - `vikunja_wrapper.py` - Main wrapper code
  - `test_vikunja_wrapper.py` - Test suite
  - `requirements.txt` - Dependencies
  - `README.md` - Usage examples
- `EXPERIMENT_REPORT.md` - Results and findings (after completion)

---

## Integration After Completion

**Reference in S1**:
> **API Access**: Vikunja provides full REST API. See [02-implementations/vikunja-api-wrapper](../02-implementations/vikunja-api-wrapper/) for production Python wrapper.

**Reference in S3 patterns**:
> **Automation Example**: See [02-implementations/vikunja-api-wrapper](../../02-implementations/vikunja-api-wrapper/) for integration code examples.

**Reference in applications/project-management**:
> **SEA Integration**: Use Vikunja API wrapper to auto-populate sprint tasks from implementation plan. See [wrapper documentation](../../research/1.131-project-management/02-implementations/vikunja-api-wrapper/).

---

## Connection to spawn-experiments

**Methodology**: Follows spawn-experiments 1.610 (Library Wrapper) pattern
**Framework**: V4 (with Predictions)
**Expected Result**: Method 4 wins with 90-95/100 score

**Why this matters**: Validates library wrapper methodology across different domains:
- 1.610: Text processing (FastText, sklearn)
- 1.611: Time series (Prophet)
- **This**: API wrappers (Vikunja REST API)

**If pattern holds**: Method 4 is ROBUST methodology for library wrappers

---

**Status**: Phase 1 in progress (documentation)
**Next Step**: Create TASK_SPECIFICATION.md with detailed requirements
**Last Updated**: November 7, 2025
