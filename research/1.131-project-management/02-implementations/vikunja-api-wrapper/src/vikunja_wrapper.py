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

from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional, List, Dict, Any
import requests
from dateutil import parser


# Custom Exceptions
class VikunjaError(Exception):
    """Base exception for all Vikunja API errors."""
    pass


class AuthenticationError(VikunjaError):
    """Raised when authentication fails (401)."""
    pass


class NotFoundError(VikunjaError):
    """Raised when a resource is not found (404)."""
    pass


class ValidationError(VikunjaError):
    """Raised when request validation fails (400)."""
    pass


class RateLimitError(VikunjaError):
    """Raised when rate limit is exceeded (429)."""
    pass


class ServerError(VikunjaError):
    """Raised when server returns 5xx error."""
    pass


# Data Models
@dataclass
class Project:
    """Represents a Vikunja project (list)."""
    id: int
    title: str
    description: Optional[str] = None
    hex_color: Optional[str] = None
    parent_project_id: int = 0  # 0 = top-level (no parent)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert Project to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Task:
    """Represents a Vikunja task."""
    id: int
    title: str
    project_id: int
    description: Optional[str] = None
    done: bool = False
    due_date: Optional[datetime] = None
    start_date: Optional[datetime] = None
    priority: int = 0
    bucket_id: int = 0
    repeat_after: Optional[int] = None  # Recurrence interval in seconds (86400 = daily)
    repeat_mode: int = 0  # 0 = repeat from due date, 1 = repeat from completion
    labels: Optional[List[str]] = None
    assignees: Optional[List[Dict[str, Any]]] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert Task to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Label:
    """Represents a Vikunja label."""
    id: int
    title: str
    hex_color: str
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert Label to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class TaskRelation:
    """Represents a task relation."""
    task_id: int
    other_task_id: int
    relation_kind: str  # 'subtask', 'parenttask', 'related', 'blocking', 'blocked', etc.
    created_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert TaskRelation to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


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

    def to_dict(self) -> Dict[str, Any]:
        """Convert Bucket to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class View:
    """Represents a project view (List, Gantt, Table, Kanban)."""
    id: int
    title: str
    project_id: int
    view_kind: str  # 'list', 'gantt', 'table', 'kanban'
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert View to dictionary."""
        return {k: v for k, v in asdict(self).items() if v is not None}


# Manager Classes
class ProjectsManager:
    """Manages project operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def create(self, title: str, description: str = None, hex_color: str = None, parent_project_id: int = None) -> Project:
        """
        Create a new project.

        Args:
            title: Project title (required)
            description: Project description (optional)
            hex_color: Project color in hex format (e.g., "#3498db" or "3498db") (optional)
            parent_project_id: ID of parent project for hierarchy (optional, 0 = top-level)

        Returns:
            Project: Created project object

        Raises:
            AuthenticationError: If token is invalid
            ValidationError: If title is empty or invalid
            NotFoundError: If parent_project_id doesn't exist
            VikunjaError: For other API errors

        Example:
            >>> client = VikunjaClient(...)
            >>> project = client.projects.create(title="My Project", hex_color="#3498db")
            >>> print(project.id)
            123
            >>> child = client.projects.create(title="Child Project", parent_project_id=123)
        """
        data = {"title": title}
        if description:
            data["description"] = description
        if hex_color:
            data["hex_color"] = hex_color
        if parent_project_id is not None:
            data["parent_project_id"] = parent_project_id

        response = self.client._request("PUT", "/api/v1/projects", json=data)
        return self._parse_project(response)

    def list(self) -> List[Project]:
        """
        List all projects.

        Returns:
            List[Project]: List of project objects

        Raises:
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", "/api/v1/projects")
        return [self._parse_project(p) for p in response]

    def get(self, project_id: int) -> Project:
        """
        Get a specific project.

        Args:
            project_id: ID of the project

        Returns:
            Project: Project object

        Raises:
            NotFoundError: If project doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", f"/api/v1/projects/{project_id}")
        return self._parse_project(response)

    def update(self, project_id: int, title: str = None, description: str = None, hex_color: str = None, parent_project_id: int = None) -> Project:
        """
        Update a project.

        Args:
            project_id: ID of the project
            title: New title (optional)
            description: New description (optional)
            hex_color: New color in hex format (optional)
            parent_project_id: New parent project ID (optional, 0 = move to top-level)

        Returns:
            Project: Updated project object

        Raises:
            NotFoundError: If project doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        data = {}
        if title:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if hex_color is not None:
            data["hex_color"] = hex_color
        if parent_project_id is not None:
            data["parent_project_id"] = parent_project_id

        response = self.client._request("POST", f"/api/v1/projects/{project_id}", json=data)
        return self._parse_project(response)

    def get_children(self, parent_id: int) -> List[Project]:
        """
        Get all child projects of a parent project.

        Args:
            parent_id: ID of the parent project

        Returns:
            List[Project]: List of child projects

        Example:
            >>> parent = client.projects.create(title="Foundations")
            >>> children = client.projects.get_children(parent.id)
        """
        all_projects = self.list()
        return [p for p in all_projects if p.parent_project_id == parent_id]

    def get_parent(self, project: Project) -> Optional[Project]:
        """
        Get the parent project of a given project.

        Args:
            project: Project object or project with parent_project_id

        Returns:
            Optional[Project]: Parent project, or None if top-level

        Example:
            >>> child = client.projects.get(123)
            >>> parent = client.projects.get_parent(child)
        """
        if project.parent_project_id == 0:
            return None
        return self.get(project.parent_project_id)

    def move_project(self, project_id: int, new_parent_id: int) -> Project:
        """
        Move a project to a different parent (or to top-level).

        This is a convenience method that fetches the project and updates it
        with the new parent_project_id while preserving all other fields.
        Use this to migrate existing projects into a hierarchy.

        Args:
            project_id: ID of the project to move
            new_parent_id: ID of the new parent project (0 = top-level)

        Returns:
            Project: Updated project object with new parent

        Raises:
            NotFoundError: If project or new parent doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors

        Example:
            >>> # Move project 5 under Applications (ID: 13448)
            >>> project = client.projects.move_project(5, 13448)
            >>> print(project.parent_project_id)
            13448
            >>>
            >>> # Move project to top-level
            >>> project = client.projects.move_project(5, 0)
        """
        # Fetch current project to preserve its title (required by Vikunja API)
        current = self.get(project_id)
        return self.update(project_id, title=current.title, parent_project_id=new_parent_id)

    def delete(self, project_id: int) -> None:
        """
        Delete a project.

        Args:
            project_id: ID of the project

        Raises:
            NotFoundError: If project doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        self.client._request("DELETE", f"/api/v1/projects/{project_id}")

    def _parse_project(self, data: Dict[str, Any]) -> Project:
        """Parse project data from API response."""
        return Project(
            id=data["id"],
            title=data["title"],
            description=data.get("description"),
            hex_color=data.get("hex_color"),
            parent_project_id=data.get("parent_project_id", 0),
            created_at=parser.parse(data["created"]) if "created" in data else None,
            updated_at=parser.parse(data["updated"]) if "updated" in data else None
        )


class TasksManager:
    """Manages task operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def create(self, project_id: int, title: str, description: str = None,
               due_date: str = None, priority: int = 0, labels: List[str] = None,
               bucket_id: int = None) -> Task:
        """
        Create a new task.

        Args:
            project_id: ID of the project
            title: Task title
            description: Task description (optional)
            due_date: Due date (ISO format string or datetime)
            priority: Task priority (0-5, default 0)
            labels: List of label names (optional)
            bucket_id: Bucket ID to assign task to (optional)

        Returns:
            Task: Created task object

        Raises:
            AuthenticationError: If token is invalid
            ValidationError: If parameters are invalid
            VikunjaError: For other API errors
        """
        data = {"title": title}
        if description:
            data["description"] = description
        if due_date:
            data["due_date"] = due_date
        if priority:
            data["priority"] = priority
        if labels:
            data["labels"] = labels
        if bucket_id is not None:
            data["bucket_id"] = bucket_id

        response = self.client._request("PUT", f"/api/v1/projects/{project_id}/tasks", json=data)
        return self._parse_task(response)

    def list(self, project_id: int) -> List[Task]:
        """
        List all tasks in a project.

        Args:
            project_id: ID of the project

        Returns:
            List[Task]: List of task objects

        Raises:
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", f"/api/v1/projects/{project_id}/tasks")
        return [self._parse_task(t) for t in response]

    def get(self, task_id: int) -> Task:
        """
        Get a specific task.

        Args:
            task_id: ID of the task

        Returns:
            Task: Task object

        Raises:
            NotFoundError: If task doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", f"/api/v1/tasks/{task_id}")
        return self._parse_task(response)

    def update(self, task_id: int, title: str = None, description: str = None,
               done: bool = None, priority: int = None, bucket_id: int = None,
               due_date: str = None, start_date: str = None) -> Task:
        """
        Update a task.

        Args:
            task_id: ID of the task
            title: New title (optional)
            description: New description (optional)
            done: Mark as done/undone (optional)
            priority: New priority (optional)
            bucket_id: Move task to bucket (optional)
            due_date: New due date in ISO format (YYYY-MM-DDTHH:MM:SSZ) (optional)
            start_date: New start date in ISO format (optional)

        Returns:
            Task: Updated task object

        Raises:
            NotFoundError: If task doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        data = {}
        if title:
            data["title"] = title
        if description is not None:
            data["description"] = description
        if done is not None:
            data["done"] = done
        if priority is not None:
            data["priority"] = priority
        if bucket_id is not None:
            data["bucket_id"] = bucket_id
        if due_date is not None:
            data["due_date"] = due_date
        if start_date is not None:
            data["start_date"] = start_date

        response = self.client._request("POST", f"/api/v1/tasks/{task_id}", json=data)
        return self._parse_task(response)

    def delete(self, task_id: int) -> None:
        """
        Delete a task.

        Args:
            task_id: ID of the task

        Raises:
            NotFoundError: If task doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        self.client._request("DELETE", f"/api/v1/tasks/{task_id}")

    def set_position(self, task_id: int, project_view_id: int, bucket_id: int = None, position: int = None, project_id: int = None) -> Dict[str, Any]:
        """
        Set a task's position in a project view (e.g., assign to Kanban bucket).

        Note: In Vikunja 0.24+, bucket assignment is now view-based. When assigning
        a task to a bucket, this method makes TWO API calls (like the UI does):
        1. Add task to bucket: POST /projects/{pid}/views/{vid}/buckets/{bid}/tasks
        2. Set position: POST /tasks/{tid}/position

        Args:
            task_id: ID of the task
            project_view_id: ID of the project view (from ViewsManager.get_kanban_view())
            bucket_id: Bucket ID to assign task to (optional, for Kanban views)
            position: Position within the bucket/view (optional, None = append to end)
            project_id: Project ID (required if bucket_id is provided)

        Returns:
            Dict: Position information from the final API call

        Raises:
            NotFoundError: If task or view doesn't exist
            AuthenticationError: If token is invalid
            ValueError: If bucket_id provided without project_id
            VikunjaError: For other API errors

        Example:
            >>> # Assign task to "In Progress" bucket in Kanban view
            >>> kanban_view = client.views.get_kanban_view(project_id=13481)
            >>> buckets = client.buckets.list(project_id=13481, view_id=kanban_view.id)
            >>> bucket = [b for b in buckets if b.title == "In Progress"][0]
            >>> client.tasks.set_position(
            ...     task_id=task.id,
            ...     project_view_id=kanban_view.id,
            ...     bucket_id=bucket.id,
            ...     project_id=13481
            ... )
        """
        # If bucket_id is provided, first add task to bucket (Call 1)
        # This is the CORRECT endpoint discovered from UI network capture
        if bucket_id is not None:
            if project_id is None:
                raise ValueError("project_id is required when bucket_id is provided")

            bucket_data = {
                "max_permission": None,
                "task_id": task_id,
                "bucket_id": bucket_id,
                "project_view_id": project_view_id,
                "project_id": project_id
            }
            # CRITICAL: Use the buckets/tasks endpoint, NOT the position endpoint
            self.client._request(
                "POST",
                f"/api/v1/projects/{project_id}/views/{project_view_id}/buckets/{bucket_id}/tasks",
                json=bucket_data
            )

        # Then set the position (Call 2) - only if position is explicitly provided
        if position is not None or bucket_id is None:
            position_data = {
                "max_permission": None,
                "project_view_id": project_view_id,
                "task_id": task_id
            }
            if position is not None:
                position_data["position"] = position

            response = self.client._request("POST", f"/api/v1/tasks/{task_id}/position", json=position_data)
            return response

        # If only bucket was set, return a success indicator
        return {"task_id": task_id, "project_view_id": project_view_id, "bucket_id": bucket_id}

    def add_label(self, task_id: int, label_id: int) -> None:
        """
        Add a label to a task.

        Args:
            task_id: ID of the task
            label_id: ID of the label to attach

        Raises:
            NotFoundError: If task or label doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        self.client._request("PUT", f"/api/v1/tasks/{task_id}/labels", json={"label_id": label_id})

    def assign_user(self, task_id: int, user_id: int) -> Task:
        """
        Assign a user to a task.

        Args:
            task_id: ID of the task
            user_id: ID of the user to assign

        Returns:
            Task: Updated task object with assignee

        Raises:
            NotFoundError: If task or user doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        data = {"user_id": user_id}
        response = self.client._request("PUT", f"/api/v1/tasks/{task_id}/assignees", json=data)
        return self._parse_task(response)

    def unassign_user(self, task_id: int, user_id: int) -> Task:
        """
        Remove user assignment from a task.

        Args:
            task_id: ID of the task
            user_id: ID of the user to unassign

        Returns:
            Task: Updated task object

        Raises:
            NotFoundError: If task or user doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("DELETE", f"/api/v1/tasks/{task_id}/assignees/{user_id}")
        return self._parse_task(response)

    def list_assignees(self, task_id: int) -> List[Dict[str, Any]]:
        """
        List all users assigned to a task.

        Args:
            task_id: ID of the task

        Returns:
            List[Dict]: List of user dictionaries with 'id', 'username', 'name', etc.

        Raises:
            NotFoundError: If task doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        task = self.get(task_id)
        return task.assignees if task.assignees else []

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data from API response."""
        return Task(
            id=data["id"],
            title=data["title"],
            project_id=data.get("list_id", 0) or data.get("project_id", 0),
            description=data.get("description"),
            done=data.get("done", False),
            due_date=parser.parse(data["due_date"]) if data.get("due_date") else None,
            start_date=parser.parse(data["start_date"]) if data.get("start_date") else None,
            priority=data.get("priority", 0),
            bucket_id=data.get("bucket_id", 0),
            repeat_after=data.get("repeat_after"),
            repeat_mode=data.get("repeat_mode", 0),
            labels=data.get("labels"),
            assignees=data.get("assignees"),
            created_at=parser.parse(data["created"]) if "created" in data else None,
            updated_at=parser.parse(data["updated"]) if "updated" in data else None
        )


class LabelsManager:
    """Manages label operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def create(self, title: str, hex_color: str) -> Label:
        """
        Create a new label.

        Args:
            title: Label title
            hex_color: Color in hex format (e.g., "#FF0000")

        Returns:
            Label: Created label object

        Raises:
            AuthenticationError: If token is invalid
            ValidationError: If parameters are invalid
            VikunjaError: For other API errors
        """
        data = {"title": title, "hex_color": hex_color}
        response = self.client._request("PUT", "/api/v1/labels", json=data)
        return self._parse_label(response)

    def list(self) -> List[Label]:
        """
        List all labels.

        Returns:
            List[Label]: List of label objects

        Raises:
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", "/api/v1/labels")
        return [self._parse_label(l) for l in response]

    def update(self, label_id: int, title: str = None, hex_color: str = None) -> Label:
        """
        Update a label.

        Args:
            label_id: ID of the label
            title: New title (optional)
            hex_color: New color (optional)

        Returns:
            Label: Updated label object

        Raises:
            NotFoundError: If label doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        data = {}
        if title:
            data["title"] = title
        if hex_color:
            data["hex_color"] = hex_color

        response = self.client._request("POST", f"/api/v1/labels/{label_id}", json=data)
        return self._parse_label(response)

    def delete(self, label_id: int) -> None:
        """
        Delete a label.

        Args:
            label_id: ID of the label

        Raises:
            NotFoundError: If label doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        self.client._request("DELETE", f"/api/v1/labels/{label_id}")

    def _parse_label(self, data: Dict[str, Any]) -> Label:
        """Parse label data from API response."""
        return Label(
            id=data["id"],
            title=data["title"],
            hex_color=data["hex_color"],
            created_at=parser.parse(data["created"]) if "created" in data else None
        )


class TaskRelationsManager:
    """Manages task relation operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def create(self, task_id: int, relation_kind: str, other_task_id: int) -> TaskRelation:
        """
        Create a task relation.

        Args:
            task_id: ID of the source task
            relation_kind: Type of relation ('subtask', 'blocking', 'related', etc.)
            other_task_id: ID of the target task

        Returns:
            TaskRelation: Created relation object

        Raises:
            AuthenticationError: If token is invalid
            NotFoundError: If task doesn't exist
            ValidationError: If relation_kind is invalid
            VikunjaError: For other API errors

        Example:
            >>> # Create blocking relation: task_a blocks task_b
            >>> relation = client.task_relations.create(
            ...     task_id=task_a.id,
            ...     relation_kind="blocking",
            ...     other_task_id=task_b.id
            ... )
        """
        endpoint = f"/api/v1/tasks/{task_id}/relations/{relation_kind}/{other_task_id}"
        response = self.client._request("PUT", endpoint)
        return self._parse_relation(response)

    def delete(self, task_id: int, relation_kind: str, other_task_id: int) -> None:
        """
        Delete a task relation.

        Args:
            task_id: ID of the source task
            relation_kind: Type of relation to delete
            other_task_id: ID of the target task

        Raises:
            AuthenticationError: If token is invalid
            NotFoundError: If task or relation doesn't exist
            VikunjaError: For other API errors
        """
        endpoint = f"/api/v1/tasks/{task_id}/relations/{relation_kind}/{other_task_id}"
        self.client._request("DELETE", endpoint)

    def list(self, task_id: int) -> List[TaskRelation]:
        """
        List all relations for a task.

        Args:
            task_id: ID of the task

        Returns:
            List[TaskRelation]: List of relation objects

        Raises:
            AuthenticationError: If token is invalid
            NotFoundError: If task doesn't exist
            VikunjaError: For other API errors

        Note:
            This returns relations from the task details endpoint,
            which includes both outgoing and incoming relations.
        """
        # Get task details which includes relations
        response = self.client._request("GET", f"/api/v1/tasks/{task_id}")

        relations = []

        # Parse related_tasks field which contains all relations
        if "related_tasks" in response and response["related_tasks"]:
            for relation_kind, tasks in response["related_tasks"].items():
                if tasks:
                    for task in tasks:
                        relations.append(TaskRelation(
                            task_id=task_id,
                            other_task_id=task["id"],
                            relation_kind=relation_kind,
                            created_at=parser.parse(task.get("created", "")) if task.get("created") else None
                        ))

        return relations

    def _parse_relation(self, data: Dict[str, Any]) -> TaskRelation:
        """Parse relation data from API response."""
        return TaskRelation(
            task_id=data.get("task_id", 0),
            other_task_id=data.get("other_task_id", 0) or data.get("id", 0),
            relation_kind=data.get("relation_kind", ""),
            created_at=parser.parse(data["created"]) if "created" in data else None
        )


class BucketsManager:
    """Manages bucket (kanban column) operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def create(self, project_id: int, view_id: int, title: str, position: int = 0, limit: int = 0) -> Bucket:
        """
        Create a new bucket in a view (typically Kanban view).

        Args:
            project_id: ID of the project
            view_id: ID of the view (get from ViewsManager.get_kanban_view())
            title: Bucket title
            position: Sort position (default 0)
            limit: WIP limit, 0 = no limit (default 0)

        Returns:
            Bucket: Created bucket object

        Raises:
            AuthenticationError: If token is invalid
            NotFoundError: If project or view doesn't exist
            ValidationError: If parameters are invalid
            VikunjaError: For other API errors
        """
        data = {
            "title": title,
            "position": position,
            "limit": limit
        }
        response = self.client._request("PUT", f"/api/v1/projects/{project_id}/views/{view_id}/buckets", json=data)
        return self._parse_bucket(response)

    def list(self, project_id: int, view_id: int) -> List[Bucket]:
        """
        List all buckets in a view.

        Args:
            project_id: ID of the project
            view_id: ID of the view (get from ViewsManager.get_kanban_view())

        Returns:
            List[Bucket]: List of bucket objects

        Raises:
            AuthenticationError: If token is invalid
            NotFoundError: If project or view doesn't exist
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", f"/api/v1/projects/{project_id}/views/{view_id}/buckets")
        return [self._parse_bucket(b) for b in response]

    def update(self, project_id: int, view_id: int, bucket_id: int, title: str = None, position: int = None, limit: int = None) -> Bucket:
        """
        Update a bucket.

        Args:
            project_id: ID of the project
            view_id: ID of the view
            bucket_id: ID of the bucket
            title: New title (optional)
            position: New position (optional)
            limit: New WIP limit (optional)

        Returns:
            Bucket: Updated bucket object

        Raises:
            NotFoundError: If bucket doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        data = {}
        if title is not None:
            data["title"] = title
        if position is not None:
            data["position"] = position
        if limit is not None:
            data["limit"] = limit

        response = self.client._request("POST", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}", json=data)
        return self._parse_bucket(response)

    def delete(self, project_id: int, view_id: int, bucket_id: int) -> None:
        """
        Delete a bucket.

        Args:
            project_id: ID of the project
            view_id: ID of the view
            bucket_id: ID of the bucket

        Raises:
            NotFoundError: If bucket doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        self.client._request("DELETE", f"/api/v1/projects/{project_id}/views/{view_id}/buckets/{bucket_id}")

    def _parse_bucket(self, data: Dict[str, Any]) -> Bucket:
        """Parse bucket data from API response."""
        return Bucket(
            id=data["id"],
            title=data["title"],
            project_id=data.get("project_id", 0) or data.get("list_id", 0),
            position=data.get("position", 0),
            limit=data.get("limit", 0),
            created_at=parser.parse(data["created"]) if "created" in data else None,
            updated_at=parser.parse(data["updated"]) if "updated" in data else None
        )


class ViewsManager:
    """Manages view operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def list(self, project_id: int) -> List[View]:
        """
        List all views for a project.

        Vikunja auto-creates 4 default views when a project is created:
        - List view
        - Gantt view
        - Table view
        - Kanban view

        Args:
            project_id: ID of the project

        Returns:
            List[View]: List of view objects

        Raises:
            NotFoundError: If project doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", f"/api/v1/projects/{project_id}/views")
        return [self._parse_view(view) for view in response]

    def get(self, project_id: int, view_id: int) -> View:
        """
        Get a specific view.

        Args:
            project_id: ID of the project
            view_id: ID of the view

        Returns:
            View: View object

        Raises:
            NotFoundError: If view doesn't exist
            AuthenticationError: If token is invalid
            VikunjaError: For other API errors
        """
        response = self.client._request("GET", f"/api/v1/projects/{project_id}/views/{view_id}")
        return self._parse_view(response)

    def get_kanban_view(self, project_id: int) -> View:
        """
        Convenience method to get the Kanban view for a project.

        Args:
            project_id: ID of the project

        Returns:
            View: Kanban view object

        Raises:
            NotFoundError: If no Kanban view exists
        """
        views = self.list(project_id)
        kanban_views = [v for v in views if v.view_kind == 'kanban']
        if not kanban_views:
            raise NotFoundError(f"No Kanban view found for project {project_id}")
        return kanban_views[0]

    def _parse_view(self, data: Dict[str, Any]) -> View:
        """Parse view data from API response."""
        return View(
            id=data["id"],
            title=data["title"],
            project_id=data.get("project_id", 0),
            view_kind=data.get("view_kind", "unknown"),
            created_at=parser.parse(data["created"]) if "created" in data else None,
            updated_at=parser.parse(data["updated"]) if "updated" in data else None
        )


# Main Client
class VikunjaClient:
    """
    Vikunja API client.

    Provides access to Projects, Tasks, and Labels resources.

    Example:
        >>> client = VikunjaClient(
        ...     base_url="https://vikunja.cloud",
        ...     token="your-api-token"
        ... )
        >>> projects = client.projects.list()
    """

    def __init__(self, base_url: str, token: str):
        """
        Initialize Vikunja client.

        Args:
            base_url: Base URL of Vikunja instance (e.g., "https://vikunja.cloud")
            token: API authentication token

        Example:
            >>> client = VikunjaClient(
            ...     base_url="https://vikunja.cloud",
            ...     token="your-token"
            ... )
        """
        self.base_url = base_url.rstrip('/')
        self.token = token
        self.projects = ProjectsManager(self)
        self.tasks = TasksManager(self)
        self.labels = LabelsManager(self)
        self.task_relations = TaskRelationsManager(self)
        self.buckets = BucketsManager(self)
        self.views = ViewsManager(self)

    def _request(self, method: str, endpoint: str, **kwargs) -> Any:
        """
        Make HTTP request to Vikunja API.

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint path
            **kwargs: Additional arguments for requests

        Returns:
            Parsed JSON response

        Raises:
            AuthenticationError: For 401 errors
            NotFoundError: For 404 errors
            ValidationError: For 400 errors
            RateLimitError: For 429 errors
            ServerError: For 5xx errors
            VikunjaError: For other errors
        """
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.request(method, url, headers=headers, **kwargs)

            # Handle error status codes
            if response.status_code == 401:
                raise AuthenticationError(f"Authentication failed: {response.text}")
            elif response.status_code == 404:
                raise NotFoundError(f"Resource not found: {response.text}")
            elif response.status_code == 400:
                raise ValidationError(f"Validation error: {response.text}")
            elif response.status_code == 429:
                raise RateLimitError(f"Rate limit exceeded: {response.text}")
            elif response.status_code >= 500:
                raise ServerError(f"Server error: {response.text}")
            elif response.status_code >= 400:
                raise VikunjaError(f"API error: {response.text}")

            # Parse JSON response (if not DELETE)
            if method != "DELETE":
                return response.json()
            return None

        except requests.RequestException as e:
            raise VikunjaError(f"Request failed: {str(e)}")


__all__ = [
    'VikunjaClient',
    'Project',
    'Task',
    'Label',
    'TaskRelation',
    'Bucket',
    'VikunjaError',
    'AuthenticationError',
    'NotFoundError',
    'ValidationError',
    'RateLimitError',
    'ServerError',
]
