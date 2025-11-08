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
    priority: int = 0
    labels: Optional[List[str]] = None
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


# Manager Classes
class ProjectsManager:
    """Manages project operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

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
        data = {"title": title}
        if description:
            data["description"] = description

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

    def update(self, project_id: int, title: str = None, description: str = None) -> Project:
        """
        Update a project.

        Args:
            project_id: ID of the project
            title: New title (optional)
            description: New description (optional)

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

        response = self.client._request("POST", f"/api/v1/projects/{project_id}", json=data)
        return self._parse_project(response)

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
            created_at=parser.parse(data["created"]) if "created" in data else None,
            updated_at=parser.parse(data["updated"]) if "updated" in data else None
        )


class TasksManager:
    """Manages task operations."""

    def __init__(self, client: 'VikunjaClient'):
        self.client = client

    def create(self, project_id: int, title: str, description: str = None,
               due_date: str = None, priority: int = 0, labels: List[str] = None) -> Task:
        """
        Create a new task.

        Args:
            project_id: ID of the project
            title: Task title
            description: Task description (optional)
            due_date: Due date (ISO format string or datetime)
            priority: Task priority (0-5, default 0)
            labels: List of label names (optional)

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
               done: bool = None, priority: int = None) -> Task:
        """
        Update a task.

        Args:
            task_id: ID of the task
            title: New title (optional)
            description: New description (optional)
            done: Mark as done/undone (optional)
            priority: New priority (optional)

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

    def _parse_task(self, data: Dict[str, Any]) -> Task:
        """Parse task data from API response."""
        return Task(
            id=data["id"],
            title=data["title"],
            project_id=data.get("list_id", 0),
            description=data.get("description"),
            done=data.get("done", False),
            due_date=parser.parse(data["due_date"]) if data.get("due_date") else None,
            priority=data.get("priority", 0),
            labels=data.get("labels"),
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
    'VikunjaError',
    'AuthenticationError',
    'NotFoundError',
    'ValidationError',
    'RateLimitError',
    'ServerError',
]
