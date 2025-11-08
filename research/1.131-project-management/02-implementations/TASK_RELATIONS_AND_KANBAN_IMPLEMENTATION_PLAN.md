# Task Relations & Kanban Implementation Plan

**Status**: Ready for Implementation
**Goal**: Enable spawn-plans agents to create fully-formed projects with dependencies and kanban workflow
**Approach**: Method 4 Adaptive TDD (Validated TDD)
**Quality Target**: 100/100 score (match vikunja-api-wrapper quality)

---

## Methodology: Method 4 - Mutation-Tested TDD

**Method 4 = Method 3 (Pure TDD) + Mutation Testing**

**The Formula**:
```
M4 = Write comprehensive tests +
     Implement code +
     INTENTIONALLY BREAK CODE +
     Verify tests FAIL +
     Fix code +
     Document GREEN → RED → GREEN cycle
```

**Reference**: `/home/ivanadmin/spawn-experiments/M4_DEFINITION_UPDATE_PROPOSAL.md`

**The M4 Process (RED → GREEN → MUTATE → RED → FIX → GREEN)**:
1. **RED**: Write comprehensive test (test first)
2. **GREEN**: Implement code to make test pass
3. **MUTATE**: Intentionally break the code (bug injection)
4. **RED**: Run tests → MUST FAIL (if they pass, tests are inadequate!)
5. **FIX**: Restore correct implementation
6. **GREEN**: Run tests → MUST PASS
7. **DOCUMENT**: Log the mutation cycle in M4_MUTATION_LOG.md

**Key Principles**:
1. Write ALL tests comprehensively (not selective)
2. Prove tests work by breaking code intentionally
3. Tests against real Vikunja API (not mocked)
4. Document each mutation cycle
5. Clean up test resources after each test

**NOT Method 4**:
- ❌ NOT "risk-based testing" (test only complex code)
- ❌ NOT "strategic testing" (fewer tests based on risk)
- ❌ NOT "selective validation" (skip tests for simple code)
- ✅ IS "M3 + test the tests via bug injection"

---

## Context

Spawn-plans task agents need to generate complete, production-ready project YAMLs that include:
- **Task dependencies** (A blocks B, C is subtask of D)
- **Kanban workflow** (backlog → in progress → done)
- **Task assignments** (who's responsible)

This enables automated project generation with realistic task relationships and workflow management.

---

## API Research Summary

### Task Relations
- **Endpoint Pattern**: `/tasks/{taskID}/relations/{relationKind}/{otherTaskID}`
- **HTTP Method**: PUT to create, DELETE to remove
- **Relation Kinds**: `subtask`, `parenttask`, `related`, `duplicateof`, `duplicates`, `blocking`, `blocked`, `precedes`, `follows`, `copiedfrom`, `copiedto`
- **Documentation**: https://vikunja.io/docs/task-relation-kinds/

### Kanban Buckets
- **Endpoints**:
  - GET `/projects/{id}/buckets` - List all buckets
  - PUT `/projects/{id}/buckets` - Create bucket
  - POST `/projects/{id}/buckets/{bucketId}` - Update bucket
  - DELETE `/projects/{id}/buckets/{bucketId}` - Delete bucket
- **Task Assignment to Bucket**: Update task's `bucket_id` field
- **Bucket Properties**: `id`, `title`, `project_id`, `position`, `limit`, `created`, `updated`

### Task Assignments
- **Field**: `assignees` (array of user objects)
- **Endpoint**: POST `/tasks/{taskId}/assignees/bulk` to assign multiple users
- **User Object**: `{id, username, name, email}`

---

## Implementation Plan

### Phase 1: Wrapper API Extensions (TDD)

**Location**: `/home/ivanadmin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-api-wrapper/src/`

#### 1.1 Task Relations Manager

**File**: `vikunja_wrapper.py` (extend existing)

**Data Model**:
```python
@dataclass
class TaskRelation:
    """Represents a task relation."""
    task_id: int
    other_task_id: int
    relation_kind: str  # 'subtask', 'blocking', etc.
    created_at: Optional[datetime] = None
```

**Manager Class**:
```python
class TaskRelationsManager:
    def create(self, task_id: int, relation_kind: str, other_task_id: int) -> TaskRelation
    def delete(self, task_id: int, relation_kind: str, other_task_id: int) -> None
    def list(self, task_id: int) -> List[TaskRelation]
```

**Method 4 Validated Tests** (`test_task_relations.py`):
```python
def test_create_subtask_relation():
    # Create parent task
    # Create child task
    # Create subtask relation
    # Assert relation exists

def test_create_blocking_relation():
    # Create task A
    # Create task B
    # Create blocking relation (A blocks B)
    # Assert relation exists

def test_delete_relation():
    # Create relation
    # Delete relation
    # Assert relation removed

def test_list_relations():
    # Create task with multiple relations
    # List relations
    # Assert all relations returned
```

#### 1.2 Buckets Manager

**File**: `vikunja_wrapper.py` (extend existing)

**Data Model**:
```python
@dataclass
class Bucket:
    """Represents a kanban bucket."""
    id: int
    title: str
    project_id: int
    position: int = 0
    limit: int = 0  # 0 = no limit
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
```

**Manager Class**:
```python
class BucketsManager:
    def create(self, project_id: int, title: str, position: int = 0, limit: int = 0) -> Bucket
    def list(self, project_id: int) -> List[Bucket]
    def update(self, project_id: int, bucket_id: int, title: str = None, position: int = None) -> Bucket
    def delete(self, project_id: int, bucket_id: int) -> None
```

**Method 4 Validated Tests** (`test_buckets.py`):
```python
def test_create_bucket():
    # Create project
    # Create bucket
    # Assert bucket created with correct properties

def test_create_multiple_buckets():
    # Create project
    # Create buckets: Backlog (pos 0), In Progress (pos 1), Done (pos 2)
    # Assert all buckets created

def test_update_bucket():
    # Create bucket
    # Update title
    # Assert title updated

def test_delete_bucket():
    # Create bucket
    # Delete bucket
    # Assert bucket removed

def test_move_task_to_bucket():
    # Create buckets
    # Create task
    # Move task to bucket (update bucket_id)
    # Assert task in correct bucket
```

#### 1.3 Task Assignees

**Extend existing TasksManager**:
```python
class TasksManager:
    # Existing methods...

    def assign_user(self, task_id: int, user_id: int) -> Task:
        """Assign a user to a task."""

    def unassign_user(self, task_id: int, user_id: int) -> Task:
        """Remove user assignment from task."""

    def list_assignees(self, task_id: int) -> List[Dict]:
        """List all users assigned to a task."""
```

**Method 4 Validated Tests** (add to `test_vikunja_wrapper.py`):
```python
def test_assign_user_to_task():
    # Create task
    # Assign current user
    # Assert user assigned

def test_unassign_user_from_task():
    # Create task with assignee
    # Unassign user
    # Assert user removed

def test_list_assignees():
    # Create task
    # Assign multiple users
    # List assignees
    # Assert all users returned
```

---

### Phase 2: YAML Schema Design

**Location**: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src/SCHEMA.md`

#### 2.1 Task Relations Schema

**Option A: Explicit Relations Block**
```yaml
project:
  title: "My Project"

tasks:
  - title: "Parent Task"
    id: parent-task  # Local reference ID

  - title: "Subtask 1"
    parent: parent-task  # Shorthand for subtask relation

  - title: "Subtask 2"
    relations:
      subtask_of: parent-task

  - title: "Blocking Task"
    relations:
      blocks: ["Subtask 1", "Subtask 2"]  # Can block multiple
```

**Option B: Task References by Title**
```yaml
tasks:
  - title: "Backend API"

  - title: "Frontend UI"
    blocked_by: ["Backend API"]  # Simpler syntax

  - title: "Deploy to Production"
    blocked_by:
      - "Backend API"
      - "Frontend UI"
```

**Recommendation**: Option B (simpler, more readable)

#### 2.2 Kanban Buckets Schema

```yaml
project:
  title: "My Project"
  buckets:
    - name: "Backlog"
      position: 0
    - name: "In Progress"
      position: 1
      limit: 5  # WIP limit
    - name: "Done"
      position: 2

tasks:
  - title: "New Task"
    bucket: "Backlog"  # Assign to bucket by name

  - title: "Active Task"
    bucket: "In Progress"
```

#### 2.3 Task Assignments Schema

```yaml
tasks:
  - title: "Design Homepage"
    assignees:
      - "user@example.com"  # By email
      - "username"           # By username

  - title: "Code Review"
    assignees: ["alice@team.com", "bob@team.com"]
```

---

### Phase 3: Populate Script Updates

**Location**: `/home/ivanadamin/spawn-solutions/research/1.131-project-management/02-implementations/vikunja-populate-script/src/`

#### 3.1 Validation (`validation.py`)

Add validation for:
- `project.buckets` (list of bucket definitions)
- `task.bucket` (string, must match defined bucket name)
- `task.blocked_by` (list of task titles)
- `task.subtask_of` (task title or local ID)
- `task.assignees` (list of email/username strings)

```python
def validate_project(project: Dict[str, Any]) -> bool:
    # Existing validation...

    # Optional: buckets
    if "buckets" in project:
        buckets = project["buckets"]
        if not isinstance(buckets, list):
            raise ValidationError("Buckets must be a list")

        for bucket in buckets:
            validate_bucket(bucket)

    return True

def validate_bucket(bucket: Dict[str, Any]) -> bool:
    if "name" not in bucket:
        raise ValidationError("Bucket missing required field: name")

    if "position" in bucket:
        if not isinstance(bucket["position"], int):
            raise ValidationError("Bucket position must be an integer")

    if "limit" in bucket:
        if not isinstance(bucket["limit"], int):
            raise ValidationError("Bucket limit must be an integer")

    return True

def validate_task(task: Dict[str, Any], available_labels: List[str]) -> bool:
    # Existing validation...

    # Optional: bucket
    if "bucket" in task:
        if not isinstance(task["bucket"], str):
            raise ValidationError("Task bucket must be a string")

    # Optional: blocked_by
    if "blocked_by" in task:
        if not isinstance(task["blocked_by"], list):
            raise ValidationError("Task blocked_by must be a list")
        for blocker in task["blocked_by"]:
            if not isinstance(blocker, str):
                raise ValidationError("blocked_by tasks must be strings (task titles)")

    # Optional: assignees
    if "assignees" in task:
        if not isinstance(task["assignees"], list):
            raise ValidationError("Task assignees must be a list")
        for assignee in task["assignees"]:
            if not isinstance(assignee, str):
                raise ValidationError("Assignees must be strings (email or username)")

    return True
```

#### 3.2 Population (`population.py`)

**Updated Flow**:
1. Create/update project
2. **Create buckets** (if defined)
3. Create/reuse labels
4. Create/update tasks (store title → ID mapping)
5. **Create task relations** (using title → ID mapping)
6. **Assign tasks to buckets** (using bucket name → ID mapping)
7. **Assign users to tasks** (lookup user by email/username)
8. Attach labels to tasks

```python
def populate_vikunja(client: Any, schema: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    if dry_run:
        return _dry_run_summary(schema)

    result = {
        "project": None,
        "buckets": [],
        "labels": [],
        "tasks": [],
        "relations": [],
    }

    # Step 1: Create/update project
    project = _create_or_update_project(client, schema)
    result["project"] = project

    # Step 2: Create buckets
    bucket_map = {}  # name → bucket object
    if "buckets" in schema.get("project", {}):
        for bucket_data in schema["project"]["buckets"]:
            bucket = _create_or_update_bucket(client, project.id, bucket_data)
            result["buckets"].append(bucket)
            bucket_map[bucket.title] = bucket

    # Step 3-4: Labels and tasks (existing logic)
    label_map = _create_or_reuse_labels(client, schema)
    task_map = _create_or_update_tasks(client, project.id, schema)  # title → task object

    # Step 5: Create task relations
    for task_data in schema.get("tasks", []):
        task = task_map[task_data["title"]]

        # Handle blocked_by relations
        if "blocked_by" in task_data:
            for blocker_title in task_data["blocked_by"]:
                blocker_task = task_map.get(blocker_title)
                if not blocker_task:
                    raise PopulationError(f"Task '{blocker_title}' not found (referenced by '{task_data['title']}')")

                # Create blocking relation: blocker_task blocks task
                relation = client.task_relations.create(
                    task_id=blocker_task.id,
                    relation_kind="blocking",
                    other_task_id=task.id
                )
                result["relations"].append(relation)

        # Handle subtask_of relations
        if "subtask_of" in task_data:
            parent_title = task_data["subtask_of"]
            parent_task = task_map.get(parent_title)
            if not parent_task:
                raise PopulationError(f"Parent task '{parent_title}' not found")

            relation = client.task_relations.create(
                task_id=task.id,
                relation_kind="subtask",
                other_task_id=parent_task.id
            )
            result["relations"].append(relation)

    # Step 6: Assign tasks to buckets
    for task_data in schema.get("tasks", []):
        if "bucket" in task_data:
            bucket_name = task_data["bucket"]
            bucket = bucket_map.get(bucket_name)
            if not bucket:
                raise PopulationError(f"Bucket '{bucket_name}' not found")

            task = task_map[task_data["title"]]
            # Update task's bucket_id
            client.tasks.update(task.id, bucket_id=bucket.id)

    # Step 7: Assign users to tasks
    for task_data in schema.get("tasks", []):
        if "assignees" in task_data:
            task = task_map[task_data["title"]]
            for assignee in task_data["assignees"]:
                # Lookup user by email or username
                # This may require a new client.users.find() method
                client.tasks.assign_user(task.id, assignee)

    # Step 8: Attach labels (existing logic)
    _attach_labels(client, schema, task_map, label_map)

    return result
```

---

### Phase 4: Testing Strategy

#### 4.1 Validated Tests (Wrapper) - Method 4
- **Run against REAL Vikunja API** (app.vikunja.cloud)
- Test each manager method against live API
- Validate actual API responses (not mocked)
- Clean up test resources after each test
- Follow vikunja-api-wrapper test patterns

#### 4.2 Integration Tests (Populate Script)
- Test complete YAML → Vikunja flow
- Test idempotent behavior (re-running doesn't duplicate)
- Test error handling (missing task references, etc.)

#### 4.3 Example Test YAMLs

**Example 1: Sprint with Dependencies**
```yaml
project:
  title: "Sprint Planning"
  buckets:
    - name: "Backlog"
      position: 0
    - name: "In Progress"
      position: 1
      limit: 3
    - name: "Done"
      position: 2

tasks:
  - title: "Design Database Schema"
    bucket: "In Progress"
    assignees: ["architect@team.com"]

  - title: "Implement API Endpoints"
    bucket: "Backlog"
    blocked_by: ["Design Database Schema"]
    assignees: ["backend@team.com"]

  - title: "Build UI Components"
    bucket: "Backlog"
    blocked_by: ["Implement API Endpoints"]
    assignees: ["frontend@team.com"]

  - title: "Deploy to Staging"
    bucket: "Backlog"
    blocked_by:
      - "Implement API Endpoints"
      - "Build UI Components"
    assignees: ["devops@team.com"]
```

**Example 2: Subtasks**
```yaml
tasks:
  - title: "Implement User Authentication"
    bucket: "In Progress"

  - title: "Add login endpoint"
    subtask_of: "Implement User Authentication"
    bucket: "Done"

  - title: "Add registration endpoint"
    subtask_of: "Implement User Authentication"
    bucket: "In Progress"

  - title: "Add password reset"
    subtask_of: "Implement User Authentication"
    bucket: "Backlog"
```

---

## Implementation Order (Method 4: Mutation-Tested TDD)

1. **Wrapper API (3-4 hours)** - RED → GREEN → MUTATE → RED → FIX → GREEN

   **Task Relations**:
   - RED: Write test `test_create_subtask_relation()`
   - GREEN: Implement `TaskRelationsManager.create()`
   - **MUTATE**: Change relation_kind from "subtask" to "related" in implementation
   - RED: Test MUST FAIL (if passes, test is inadequate!)
   - FIX: Restore correct "subtask"
   - GREEN: Test MUST PASS
   - DOCUMENT: Log mutation in `M4_MUTATION_LOG.md`
   - Repeat for other relation types

   **Buckets**:
   - RED: Write test `test_create_bucket()`
   - GREEN: Implement `BucketsManager.create()`
   - **MUTATE**: Remove bucket position assignment
   - RED: Test MUST FAIL
   - FIX: Restore position
   - GREEN: Test MUST PASS
   - DOCUMENT: Log mutation
   - Repeat for update/delete/list operations

   **Assignments**:
   - RED: Write test `test_assign_user_to_task()`
   - GREEN: Extend `TasksManager.assign_user()`
   - **MUTATE**: Skip API call, return without assigning
   - RED: Test MUST FAIL
   - FIX: Restore API call
   - GREEN: Test MUST PASS
   - DOCUMENT: Log mutation

2. **YAML Schema (30 min)**
   - Update SCHEMA.md with new fields
   - Document examples

3. **Validation (1 hour)**
   - Add bucket validation
   - Add relation validation
   - Add assignee validation
   - Write validation tests

4. **Population Logic (2-3 hours)**
   - Implement bucket creation
   - Implement relation creation
   - Implement bucket assignment
   - Implement user assignment
   - Write integration tests

5. **Documentation (30 min)**
   - Update populate script README
   - Update QUICK_START_FOR_OTHER_REPOS.md
   - Add example YAMLs

**Total Estimated Time**: 8-10 hours (includes mutation testing cycles)

---

## Success Criteria (Method 4)

**Wrapper Implementation**:
- [ ] Wrapper supports all task relation kinds
- [ ] Wrapper supports bucket CRUD operations
- [ ] Wrapper supports task assignments
- [ ] All wrapper tests passing (comprehensive coverage)

**Method 4 Mutation Testing**:
- [ ] **M4_MUTATION_LOG.md created** documenting all mutations
- [ ] Each feature has GREEN → RED → GREEN cycle documented
- [ ] All mutations caught by tests (RED phase successful)
- [ ] Example mutations:
  - [ ] Task relation: Wrong relation_kind → test FAILS ✓
  - [ ] Bucket: Missing position → test FAILS ✓
  - [ ] Assignment: Skipped API call → test FAILS ✓
  - [ ] Relation validation: Task not found → test FAILS ✓

**Integration**:
- [ ] YAML schema documented
- [ ] Validation handles all new fields
- [ ] Populate script creates relations correctly
- [ ] Populate script creates buckets correctly
- [ ] Populate script assigns tasks to buckets
- [ ] Populate script assigns users to tasks
- [ ] All integration tests passing
- [ ] Example YAMLs demonstrate all features
- [ ] Documentation complete

**M4 Quality Target**: Score 105/100 (100 for completeness + 5 for mutation testing)

---

## Questions to Resolve During Implementation

1. **User Lookup**: How to find user ID from email/username?
   - May need `client.users.find(email)` or `client.users.list()`
   - Document this requirement

2. **Idempotent Relations**: How to handle re-running with relations?
   - Check if relation already exists before creating?
   - API behavior on duplicate relation creation?

3. **Bucket Deletion**: Should populate script delete buckets not in YAML?
   - Current approach: Only create/update, never delete
   - Recommend same for buckets

4. **Default Bucket**: What happens if task doesn't specify bucket?
   - Vikunja creates default "Backlog" bucket?
   - Leave task in default bucket

---

## Files to Create/Modify

**Wrapper** (`/vikunja-api-wrapper/src/`):
- [ ] `vikunja_wrapper.py` - Add TaskRelationsManager, BucketsManager
- [ ] `test_task_relations.py` - New file (with mutation tests)
- [ ] `test_buckets.py` - New file (with mutation tests)
- [ ] `test_vikunja_wrapper.py` - Add assignment tests (with mutations)
- [ ] **`M4_MUTATION_LOG.md`** - Document all mutation cycles (CRITICAL)

**Populate Script** (`/vikunja-populate-script/src/`):
- [ ] `SCHEMA.md` - Document new fields
- [ ] `validation.py` - Add bucket/relation/assignee validation
- [ ] `population.py` - Add bucket/relation/assignee population
- [ ] `test_validation.py` - Add validation tests
- [ ] `test_population.py` - Add population tests
- [ ] `examples/sprint-with-dependencies.yaml` - New example
- [ ] `examples/project-with-subtasks.yaml` - New example

**Documentation**:
- [ ] `QUICK_START_FOR_OTHER_REPOS.md` - Add relation/bucket examples
- [ ] `README.md` - Update feature list

---

## Next Steps

1. Start fresh agent with this plan
2. Begin with Phase 1: Wrapper API Extensions (TDD approach)
3. Iterate through phases sequentially
4. Test thoroughly at each phase
5. Update vikunja-tasks.yaml when complete

---

**Last Updated**: 2025-11-08
**Ready for**: Fresh agent implementation
