"""
Test suite for Vikunja Project Hierarchy support.

Tests cover:
- Creating parent projects
- Creating child projects with parent_project_id
- Listing projects by parent
- Updating parent relationships
- Validation and error handling
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from vikunja_wrapper import (
    VikunjaClient,
    Project,
    ValidationError,
    NotFoundError,
)


class TestProjectHierarchy:
    """Test project hierarchy operations."""

    @patch('vikunja_wrapper.requests.request')
    def test_create_parent_project(self, mock_request):
        """Test creating a parent project (no parent_project_id)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'title': 'Foundations',
            'description': 'Capability development projects',
            'parent_project_id': 0,  # Vikunja uses 0 for no parent
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.create(
            title="Foundations",
            description="Capability development projects"
        )

        assert project.id == 1
        assert project.title == "Foundations"
        assert project.parent_project_id == 0

        # Verify API call (Vikunja uses PUT for creating projects)
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert args[0] == 'PUT'
        assert '/api/v1/projects' in args[1]
        assert kwargs['json']['title'] == 'Foundations'

    @patch('vikunja_wrapper.requests.request')
    def test_create_child_project(self, mock_request):
        """Test creating a child project with parent_project_id."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 2,
            'title': 'spawn-experiments',
            'description': 'Methodology validation',
            'parent_project_id': 1,  # Child of Foundations
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.create(
            title="spawn-experiments",
            description="Methodology validation",
            parent_project_id=1
        )

        assert project.id == 2
        assert project.title == "spawn-experiments"
        assert project.parent_project_id == 1

        # Verify API call includes parent_project_id
        mock_request.assert_called_once()
        args, kwargs = mock_request.call_args
        assert kwargs['json']['parent_project_id'] == 1

    @patch('vikunja_wrapper.requests.request')
    def test_list_all_projects_includes_hierarchy(self, mock_request):
        """Test that listing all projects includes parent_project_id field."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'title': 'Foundations',
                'parent_project_id': 0,
                'created': '2025-11-08T12:00:00Z',
                'updated': '2025-11-08T12:00:00Z',
            },
            {
                'id': 2,
                'title': 'spawn-experiments',
                'parent_project_id': 1,
                'created': '2025-11-08T12:00:00Z',
                'updated': '2025-11-08T12:00:00Z',
            },
            {
                'id': 3,
                'title': 'spawn-solutions',
                'parent_project_id': 1,
                'created': '2025-11-08T12:00:00Z',
                'updated': '2025-11-08T12:00:00Z',
            }
        ]
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        projects = client.projects.list()

        assert len(projects) == 3
        assert projects[0].parent_project_id == 0  # Foundations (parent)
        assert projects[1].parent_project_id == 1  # spawn-experiments (child)
        assert projects[2].parent_project_id == 1  # spawn-solutions (child)

    @patch('vikunja_wrapper.requests.request')
    def test_list_projects_by_parent(self, mock_request):
        """Test filtering projects by parent_project_id using get_children()."""
        # Vikunja API doesn't support filtering by parent_project_id in query params
        # So we fetch all projects and filter client-side via get_children()
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [
            {
                'id': 1,
                'title': 'Foundations',
                'parent_project_id': 0,
                'created': '2025-11-08T12:00:00Z',
                'updated': '2025-11-08T12:00:00Z',
            },
            {
                'id': 2,
                'title': 'spawn-experiments',
                'parent_project_id': 1,
                'created': '2025-11-08T12:00:00Z',
                'updated': '2025-11-08T12:00:00Z',
            },
            {
                'id': 3,
                'title': 'spawn-solutions',
                'parent_project_id': 1,
                'created': '2025-11-08T12:00:00Z',
                'updated': '2025-11-08T12:00:00Z',
            }
        ]
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        # Use get_children() helper to filter client-side
        children = client.projects.get_children(parent_id=1)

        assert len(children) == 2
        assert all(p.parent_project_id == 1 for p in children)

        # Verify API call (fetches all projects, then filters client-side)
        mock_request.assert_called_once()

    @patch('vikunja_wrapper.requests.request')
    def test_get_project_hierarchy_info(self, mock_request):
        """Test getting a single project includes hierarchy information."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 2,
            'title': 'spawn-experiments',
            'description': 'Methodology validation',
            'parent_project_id': 1,
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.get(2)

        assert project.parent_project_id == 1

    @patch('vikunja_wrapper.requests.request')
    def test_update_project_parent(self, mock_request):
        """Test updating a project's parent_project_id."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 2,
            'title': 'spawn-experiments',
            'parent_project_id': 5,  # Moved to different parent
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.update(2, parent_project_id=5)

        assert project.parent_project_id == 5

        # Verify API call
        args, kwargs = mock_request.call_args
        assert kwargs['json']['parent_project_id'] == 5

    @patch('vikunja_wrapper.requests.request')
    def test_remove_project_parent(self, mock_request):
        """Test moving a project to top-level (parent_project_id=0)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 2,
            'title': 'spawn-experiments',
            'parent_project_id': 0,  # No parent (top-level)
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.update(2, parent_project_id=0)

        assert project.parent_project_id == 0

    @patch('vikunja_wrapper.requests.request')
    def test_create_child_with_invalid_parent(self, mock_request):
        """Test that creating a child with non-existent parent_project_id fails."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.text = 'Parent project does not exist.'
        mock_response.json.return_value = {
            'code': 3001,
            'message': 'Parent project does not exist.'
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        with pytest.raises(NotFoundError, match="Parent project does not exist"):
            client.projects.create(
                title="orphan-project",
                parent_project_id=9999  # Non-existent parent
            )

    @patch('vikunja_wrapper.requests.request')
    def test_project_model_has_parent_field(self, mock_request):
        """Test that Project model includes parent_project_id field."""
        # This is a data model test - verify Project dataclass has the field
        from vikunja_wrapper import Project

        # Create a Project instance
        project = Project(
            id=1,
            title="Test",
            parent_project_id=5
        )

        assert hasattr(project, 'parent_project_id')
        assert project.parent_project_id == 5

    @patch('vikunja_wrapper.requests.request')
    def test_project_model_parent_defaults_to_zero(self, mock_request):
        """Test that parent_project_id defaults to 0 (top-level) if not specified."""
        from vikunja_wrapper import Project

        # Create a Project without specifying parent
        project = Project(
            id=1,
            title="Test"
        )

        # Should default to 0 (top-level)
        assert project.parent_project_id == 0


class TestHierarchyHelpers:
    """Test helper methods for working with hierarchies."""

    @patch('vikunja_wrapper.requests.request')
    def test_get_children_of_project(self, mock_request):
        """Test helper method to get all children of a parent project."""
        # First call: get all projects
        mock_response1 = MagicMock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = [
            {'id': 1, 'title': 'Foundations', 'parent_project_id': 0},
            {'id': 2, 'title': 'spawn-experiments', 'parent_project_id': 1},
            {'id': 3, 'title': 'spawn-solutions', 'parent_project_id': 1},
            {'id': 4, 'title': 'Applications', 'parent_project_id': 0},
            {'id': 5, 'title': 'qrcards', 'parent_project_id': 4},
        ]
        mock_request.return_value = mock_response1

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        # Get children of Foundations (id=1)
        children = client.projects.get_children(parent_id=1)

        assert len(children) == 2
        assert {p.id for p in children} == {2, 3}
        assert all(p.parent_project_id == 1 for p in children)

    @patch('vikunja_wrapper.requests.request')
    def test_get_parent_of_project(self, mock_request):
        """Test helper method to get parent project."""
        # First call: get child project
        mock_response1 = MagicMock()
        mock_response1.status_code = 200
        mock_response1.json.return_value = {
            'id': 2,
            'title': 'spawn-experiments',
            'parent_project_id': 1
        }

        # Second call: get parent project
        mock_response2 = MagicMock()
        mock_response2.status_code = 200
        mock_response2.json.return_value = {
            'id': 1,
            'title': 'Foundations',
            'parent_project_id': 0
        }

        mock_request.side_effect = [mock_response1, mock_response2]

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        # Get project then its parent
        child = client.projects.get(2)
        parent = client.projects.get_parent(child)

        assert parent.id == 1
        assert parent.title == "Foundations"

    @patch('vikunja_wrapper.requests.request')
    def test_get_parent_of_top_level_returns_none(self, mock_request):
        """Test that getting parent of top-level project returns None."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'title': 'Foundations',
            'parent_project_id': 0  # Top-level
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        project = client.projects.get(1)
        parent = client.projects.get_parent(project)

        assert parent is None


class TestProjectColors:
    """Test project color support."""

    @patch('vikunja_wrapper.requests.request')
    def test_create_project_with_hex_color(self, mock_request):
        """Test creating a project with hex_color."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'title': 'Foundations',
            'hex_color': '3498db',
            'parent_project_id': 0,
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.create(
            title="Foundations",
            hex_color="#3498db"
        )

        assert project.id == 1
        assert project.hex_color == "3498db"

        # Verify API call includes hex_color
        args, kwargs = mock_request.call_args
        assert kwargs['json']['hex_color'] == '#3498db'

    @patch('vikunja_wrapper.requests.request')
    def test_update_project_hex_color(self, mock_request):
        """Test updating a project's hex_color."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'id': 1,
            'title': 'Foundations',
            'hex_color': 'e74c3c',
            'parent_project_id': 0,
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }
        mock_request.return_value = mock_response

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")
        project = client.projects.update(1, hex_color="#e74c3c")

        assert project.hex_color == "e74c3c"

        # Verify API call
        args, kwargs = mock_request.call_args
        assert kwargs['json']['hex_color'] == '#e74c3c'

    @patch('vikunja_wrapper.requests.request')
    def test_project_model_has_hex_color_field(self, mock_request):
        """Test that Project model includes hex_color field."""
        from vikunja_wrapper import Project

        # Create a Project instance with hex_color
        project = Project(
            id=1,
            title="Test",
            hex_color="3498db"
        )

        assert hasattr(project, 'hex_color')
        assert project.hex_color == "3498db"

    @patch('vikunja_wrapper.requests.request')
    def test_project_model_hex_color_defaults_to_none(self, mock_request):
        """Test that hex_color defaults to None if not specified."""
        from vikunja_wrapper import Project

        # Create a Project without specifying hex_color
        project = Project(
            id=1,
            title="Test"
        )

        # Should default to None
        assert project.hex_color is None


class TestMoveProject:
    """Test moving projects between parents."""

    @patch('vikunja_wrapper.requests.request')
    def test_move_project_to_different_parent(self, mock_request):
        """Test moving a project to a different parent using move_project()."""
        # First call: GET to fetch current project
        get_response = MagicMock()
        get_response.status_code = 200
        get_response.json.return_value = {
            'id': 5,
            'title': 'qrcards',
            'parent_project_id': 0,  # Currently top-level
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }

        # Second call: POST to update with new parent
        post_response = MagicMock()
        post_response.status_code = 200
        post_response.json.return_value = {
            'id': 5,
            'title': 'qrcards',
            'parent_project_id': 13448,  # Moved to Applications
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }

        mock_request.side_effect = [get_response, post_response]

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        # Move project 5 to parent 13448
        project = client.projects.move_project(project_id=5, new_parent_id=13448)

        assert project.id == 5
        assert project.parent_project_id == 13448

        # Verify two API calls: GET then POST
        assert mock_request.call_count == 2

        # First call: GET
        get_args = mock_request.call_args_list[0][0]
        assert get_args[0] == 'GET'
        assert '/api/v1/projects/5' in get_args[1]

        # Second call: POST with title preserved
        post_args, post_kwargs = mock_request.call_args_list[1]
        assert post_args[0] == 'POST'
        assert '/api/v1/projects/5' in post_args[1]
        assert post_kwargs['json']['title'] == 'qrcards'  # Title preserved
        assert post_kwargs['json']['parent_project_id'] == 13448

    @patch('vikunja_wrapper.requests.request')
    def test_move_project_to_top_level(self, mock_request):
        """Test moving a project to top-level (no parent) using move_project()."""
        # First call: GET to fetch current project
        get_response = MagicMock()
        get_response.status_code = 200
        get_response.json.return_value = {
            'id': 5,
            'title': 'qrcards',
            'parent_project_id': 13448,  # Currently under Applications
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }

        # Second call: POST to update to top-level
        post_response = MagicMock()
        post_response.status_code = 200
        post_response.json.return_value = {
            'id': 5,
            'title': 'qrcards',
            'parent_project_id': 0,  # Top-level
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }

        mock_request.side_effect = [get_response, post_response]

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        # Move project to top-level
        project = client.projects.move_project(project_id=5, new_parent_id=0)

        assert project.parent_project_id == 0

        # Verify API call includes title and parent_project_id=0
        assert mock_request.call_count == 2
        post_kwargs = mock_request.call_args_list[1][1]
        assert post_kwargs['json']['title'] == 'qrcards'
        assert post_kwargs['json']['parent_project_id'] == 0

    @patch('vikunja_wrapper.requests.request')
    def test_move_project_with_invalid_parent(self, mock_request):
        """Test that moving to non-existent parent raises NotFoundError."""
        # First call: GET succeeds
        get_response = MagicMock()
        get_response.status_code = 200
        get_response.json.return_value = {
            'id': 5,
            'title': 'qrcards',
            'parent_project_id': 0,
            'created': '2025-11-08T12:00:00Z',
            'updated': '2025-11-08T12:00:00Z',
        }

        # Second call: POST fails (parent doesn't exist)
        post_response = MagicMock()
        post_response.status_code = 404
        post_response.text = 'Parent project does not exist.'
        post_response.json.return_value = {
            'code': 3001,
            'message': 'Parent project does not exist.'
        }

        mock_request.side_effect = [get_response, post_response]

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        with pytest.raises(NotFoundError, match="Parent project does not exist"):
            client.projects.move_project(project_id=5, new_parent_id=9999)


class TestHierarchyIntegration:
    """Integration tests for complete hierarchy workflows."""

    @patch('vikunja_wrapper.requests.request')
    def test_create_full_hierarchy(self, mock_request):
        """Test creating a complete 2-level hierarchy."""
        # Response for creating parent
        parent_response = MagicMock()
        parent_response.status_code = 200
        parent_response.json.return_value = {
            'id': 1,
            'title': 'Foundations',
            'parent_project_id': 0
        }

        # Responses for creating children
        child1_response = MagicMock()
        child1_response.status_code = 200
        child1_response.json.return_value = {
            'id': 2,
            'title': 'spawn-experiments',
            'parent_project_id': 1
        }

        child2_response = MagicMock()
        child2_response.status_code = 200
        child2_response.json.return_value = {
            'id': 3,
            'title': 'spawn-solutions',
            'parent_project_id': 1
        }

        mock_request.side_effect = [parent_response, child1_response, child2_response]

        client = VikunjaClient(base_url="https://test.vikunja.cloud", token="test-token")

        # Create parent
        parent = client.projects.create(title="Foundations")

        # Create children
        child1 = client.projects.create(
            title="spawn-experiments",
            parent_project_id=parent.id
        )
        child2 = client.projects.create(
            title="spawn-solutions",
            parent_project_id=parent.id
        )

        assert parent.id == 1
        assert child1.parent_project_id == parent.id
        assert child2.parent_project_id == parent.id
