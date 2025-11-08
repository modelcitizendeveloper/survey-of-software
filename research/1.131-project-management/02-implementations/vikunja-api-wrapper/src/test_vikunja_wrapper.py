"""
Test suite for Vikunja Python API Wrapper.

Tests cover:
- Client initialization
- Authentication
- CRUD operations (Projects, Tasks, Labels)
- Error handling
- Data model serialization
"""

import pytest
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from vikunja_wrapper import (
    VikunjaClient,
    Project,
    Task,
    Label,
    VikunjaError,
    AuthenticationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
)


class TestClientInitialization:
    """Test VikunjaClient initialization."""

    def test_client_with_token(self):
        """Test client creation with token."""
        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        assert client.base_url == "https://test.vikunja.cloud"
        assert client.token == "test-token"

    def test_client_normalizes_base_url(self):
        """Test that trailing slashes are removed from base_url."""
        client = VikunjaClient(base_url="https://test.vikunja.cloud/", token="test")
        assert client.base_url == "https://test.vikunja.cloud"


class TestProjects:
    """Test Projects manager CRUD operations."""

    @patch('vikunja_wrapper.requests.request')
    def test_create_project(self, mock_request):
        """Test creating a project."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "title": "Test Project",
            "description": "Test description",
            "created": "2025-11-07T12:00:00Z",
            "updated": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        project = client.projects.create(title="Test Project", description="Test description")

        assert project.id == 123
        assert project.title == "Test Project"
        assert project.description == "Test description"

    @patch('vikunja_wrapper.requests.request')
    def test_list_projects(self, mock_request):
        """Test listing all projects."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "title": "Project 1", "created": "2025-11-07T12:00:00Z"},
            {"id": 2, "title": "Project 2", "created": "2025-11-07T12:00:00Z"}
        ]
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        projects = client.projects.list()

        assert len(projects) == 2
        assert projects[0].id == 1
        assert projects[1].title == "Project 2"

    @patch('vikunja_wrapper.requests.request')
    def test_get_project(self, mock_request):
        """Test getting a specific project."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "title": "Test Project",
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        project = client.projects.get(project_id=123)

        assert project.id == 123
        assert project.title == "Test Project"

    @patch('vikunja_wrapper.requests.request')
    def test_update_project(self, mock_request):
        """Test updating a project."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 123,
            "title": "Updated Title",
            "description": "Updated description",
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        project = client.projects.update(project_id=123, title="Updated Title")

        assert project.title == "Updated Title"

    @patch('vikunja_wrapper.requests.request')
    def test_delete_project(self, mock_request):
        """Test deleting a project."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        client.projects.delete(project_id=123)

        mock_request.assert_called_once()


class TestTasks:
    """Test Tasks manager CRUD operations."""

    @patch('vikunja_wrapper.requests.request')
    def test_create_task(self, mock_request):
        """Test creating a task."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 456,
            "title": "New Task",
            "description": "Task description",
            "list_id": 123,
            "done": False,
            "priority": 5,
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        task = client.tasks.create(
            project_id=123,
            title="New Task",
            description="Task description",
            priority=5
        )

        assert task.id == 456
        assert task.title == "New Task"
        assert task.project_id == 123

    @patch('vikunja_wrapper.requests.request')
    def test_list_tasks(self, mock_request):
        """Test listing tasks in a project."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "title": "Task 1", "list_id": 123, "created": "2025-11-07T12:00:00Z"},
            {"id": 2, "title": "Task 2", "list_id": 123, "created": "2025-11-07T12:00:00Z"}
        ]
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        tasks = client.tasks.list(project_id=123)

        assert len(tasks) == 2
        assert tasks[0].title == "Task 1"

    @patch('vikunja_wrapper.requests.request')
    def test_get_task(self, mock_request):
        """Test getting a specific task."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 456,
            "title": "Test Task",
            "list_id": 123,
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        task = client.tasks.get(task_id=456)

        assert task.id == 456
        assert task.title == "Test Task"

    @patch('vikunja_wrapper.requests.request')
    def test_update_task(self, mock_request):
        """Test updating a task."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 456,
            "title": "Updated Task",
            "done": True,
            "list_id": 123,
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        task = client.tasks.update(task_id=456, title="Updated Task", done=True)

        assert task.title == "Updated Task"
        assert task.done is True

    @patch('vikunja_wrapper.requests.request')
    def test_delete_task(self, mock_request):
        """Test deleting a task."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        client.tasks.delete(task_id=456)

        mock_request.assert_called_once()


class TestLabels:
    """Test Labels manager CRUD operations."""

    @patch('vikunja_wrapper.requests.request')
    def test_create_label(self, mock_request):
        """Test creating a label."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 789,
            "title": "bug",
            "hex_color": "#FF0000",
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        label = client.labels.create(title="bug", hex_color="#FF0000")

        assert label.id == 789
        assert label.title == "bug"
        assert label.hex_color == "#FF0000"

    @patch('vikunja_wrapper.requests.request')
    def test_list_labels(self, mock_request):
        """Test listing all labels."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {"id": 1, "title": "bug", "hex_color": "#FF0000", "created": "2025-11-07T12:00:00Z"},
            {"id": 2, "title": "feature", "hex_color": "#00FF00", "created": "2025-11-07T12:00:00Z"}
        ]
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        labels = client.labels.list()

        assert len(labels) == 2
        assert labels[0].title == "bug"

    @patch('vikunja_wrapper.requests.request')
    def test_update_label(self, mock_request):
        """Test updating a label."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "id": 789,
            "title": "critical-bug",
            "hex_color": "#FF0000",
            "created": "2025-11-07T12:00:00Z"
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        label = client.labels.update(label_id=789, title="critical-bug")

        assert label.title == "critical-bug"


class TestErrorHandling:
    """Test error handling for various HTTP status codes."""

    @patch('vikunja_wrapper.requests.request')
    def test_authentication_error(self, mock_request):
        """Test 401 authentication error."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Invalid token"
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="invalid")
        with pytest.raises(AuthenticationError):
            client.projects.list()

    @patch('vikunja_wrapper.requests.request')
    def test_not_found_error(self, mock_request):
        """Test 404 not found error."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = "Project not found"
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        with pytest.raises(NotFoundError):
            client.projects.get(project_id=99999)

    @patch('vikunja_wrapper.requests.request')
    def test_validation_error(self, mock_request):
        """Test 400 validation error."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Title is required"
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        with pytest.raises(ValidationError):
            client.projects.create(title="")

    @patch('vikunja_wrapper.requests.request')
    def test_rate_limit_error(self, mock_request):
        """Test 429 rate limit error."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.text = "Rate limit exceeded"
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        with pytest.raises(RateLimitError):
            client.projects.list()

    @patch('vikunja_wrapper.requests.request')
    def test_server_error(self, mock_request):
        """Test 500 server error."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal server error"
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test")
        with pytest.raises(ServerError):
            client.projects.list()


class TestDataModels:
    """Test data model serialization and deserialization."""

    def test_project_to_dict(self):
        """Test Project to_dict method."""
        project = Project(id=123, title="Test Project", description="Test desc")
        data = project.to_dict()

        assert data["id"] == 123
        assert data["title"] == "Test Project"
        assert data["description"] == "Test desc"

    def test_task_to_dict(self):
        """Test Task to_dict method."""
        task = Task(id=456, title="Test Task", project_id=123, done=False)
        data = task.to_dict()

        assert data["id"] == 456
        assert data["title"] == "Test Task"
        assert data["project_id"] == 123
        assert data["done"] is False

    def test_label_to_dict(self):
        """Test Label to_dict method."""
        label = Label(id=789, title="bug", hex_color="#FF0000")
        data = label.to_dict()

        assert data["id"] == 789
        assert data["title"] == "bug"
        assert data["hex_color"] == "#FF0000"
