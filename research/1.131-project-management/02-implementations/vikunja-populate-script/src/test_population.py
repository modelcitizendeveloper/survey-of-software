#!/usr/bin/env python3
"""
Unit tests for Vikunja population logic

Uses mocking to avoid hitting the real API during tests.
"""

import pytest
from unittest.mock import Mock, MagicMock, call
from population import populate_vikunja, PopulationError


class TestPopulateMinimal:
    """Test minimal population (project only)"""

    def test_create_project_only(self):
        """Should create project when schema has only project"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        schema = {
            "project": {"title": "My Project"}
        }

        result = populate_vikunja(mock_client, schema)

        # Verify project was created
        mock_client.projects.create.assert_called_once_with(
            title="My Project"
        )

        # Verify result
        assert result["project"] == mock_project
        assert result["labels"] == []
        assert result["tasks"] == []

    def test_create_project_with_description(self):
        """Should pass description to project.create()"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        schema = {
            "project": {
                "title": "My Project",
                "description": "Test description"
            }
        }

        populate_vikunja(mock_client, schema)

        mock_client.projects.create.assert_called_once_with(
            title="My Project",
            description="Test description"
        )

    def test_create_project_with_color(self):
        """Should pass color to project.create()"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        schema = {
            "project": {
                "title": "My Project",
                "color": "FF0000"
            }
        }

        populate_vikunja(mock_client, schema)

        mock_client.projects.create.assert_called_once_with(
            title="My Project",
            color="FF0000"
        )

    def test_create_project_with_parent(self):
        """Should pass parent_project_id to project.create() for hierarchy"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=456, parent_project_id=1)
        mock_client.projects.create.return_value = mock_project

        schema = {
            "project": {
                "title": "Child Project",
                "parent_project_id": 1
            }
        }

        result = populate_vikunja(mock_client, schema)

        mock_client.projects.create.assert_called_once_with(
            title="Child Project",
            parent_project_id=1
        )

        # Verify result includes the created project with parent
        assert result["project"] == mock_project
        assert result["project"].parent_project_id == 1

    def test_create_project_with_all_fields(self):
        """Should pass all project fields including parent_project_id"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=789, parent_project_id=5)
        mock_client.projects.create.return_value = mock_project

        schema = {
            "project": {
                "title": "Full Project",
                "description": "Complete test",
                "color": "00FF00",
                "parent_project_id": 5
            }
        }

        populate_vikunja(mock_client, schema)

        mock_client.projects.create.assert_called_once_with(
            title="Full Project",
            description="Complete test",
            color="00FF00",
            parent_project_id=5
        )


class TestPopulateLabels:
    """Test label creation"""

    def test_create_labels(self):
        """Should create all labels"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label1 = Mock(id=1, title="Bug")
        mock_label2 = Mock(id=2, title="Feature")
        mock_client.labels.create.side_effect = [mock_label1, mock_label2]

        schema = {
            "project": {"title": "My Project"},
            "labels": [
                {"title": "Bug", "color": "FF0000"},
                {"title": "Feature", "color": "00FF00"},
            ]
        }

        result = populate_vikunja(mock_client, schema)

        # Verify labels were created (code converts color to hex_color)
        assert mock_client.labels.create.call_count == 2
        mock_client.labels.create.assert_any_call(
            title="Bug",
            hex_color="FF0000"
        )
        mock_client.labels.create.assert_any_call(
            title="Feature",
            hex_color="00FF00"
        )

        # Verify result
        assert len(result["labels"]) == 2

    def test_create_labels_without_color(self):
        """Should raise error if label missing hex_color"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        schema = {
            "project": {"title": "My Project"},
            "labels": [
                {"title": "Bug"}  # No color - should fail
            ]
        }

        # Should raise PopulationError for missing hex_color
        with pytest.raises(PopulationError, match="missing required field 'hex_color'"):
            populate_vikunja(mock_client, schema)


class TestPopulateTasks:
    """Test task creation"""

    def test_create_tasks(self):
        """Should create all tasks"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_task1 = Mock(id=1)
        mock_task2 = Mock(id=2)
        mock_client.tasks.create.side_effect = [mock_task1, mock_task2]

        schema = {
            "project": {"title": "My Project"},
            "tasks": [
                {"title": "Task 1"},
                {"title": "Task 2"},
            ]
        }

        result = populate_vikunja(mock_client, schema)

        # Verify tasks were created
        assert mock_client.tasks.create.call_count == 2
        mock_client.tasks.create.assert_any_call(
            project_id=123,
            title="Task 1"
        )
        mock_client.tasks.create.assert_any_call(
            project_id=123,
            title="Task 2"
        )

        # Verify result
        assert len(result["tasks"]) == 2

    def test_create_task_with_all_fields(self):
        """Should pass all task fields to API"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_task = Mock(id=1)
        mock_client.tasks.create.return_value = mock_task

        schema = {
            "project": {"title": "My Project"},
            "tasks": [
                {
                    "title": "Task 1",
                    "description": "Test description",
                    "due_date": "2025-11-15",
                    "priority": 5,
                }
            ]
        }

        populate_vikunja(mock_client, schema)

        # Note: code only passes description and priority, not done
        mock_client.tasks.create.assert_called_once_with(
            project_id=123,
            title="Task 1",
            description="Test description",
            due_date="2025-11-15T23:59:59Z",  # Gets converted to ISO format
            priority=5
        )

    def test_attach_labels_to_tasks(self):
        """Should attach labels to tasks after creation"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label = Mock(id=999, title="Bug")
        mock_client.labels.create.return_value = mock_label

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        schema = {
            "project": {"title": "My Project"},
            "labels": [
                {"title": "Bug", "hex_color": "FF0000"}  # hex_color required
            ],
            "tasks": [
                {
                    "title": "Fix bug",
                    "labels": ["Bug"]
                }
            ]
        }

        populate_vikunja(mock_client, schema)

        # Task should be created first
        mock_client.tasks.create.assert_called_once()

        # Then label should be attached
        mock_client.tasks.add_label.assert_called_once_with(
            task_id=456,
            label_id=999
        )

    def test_attach_multiple_labels_to_task(self):
        """Should attach multiple labels to one task"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label1 = Mock(id=1, title="Bug")
        mock_label2 = Mock(id=2, title="Urgent")
        mock_client.labels.create.side_effect = [mock_label1, mock_label2]

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        schema = {
            "project": {"title": "My Project"},
            "labels": [
                {"title": "Bug", "hex_color": "FF0000"},  # hex_color required
                {"title": "Urgent", "hex_color": "FFA500"},  # hex_color required
            ],
            "tasks": [
                {
                    "title": "Fix critical bug",
                    "labels": ["Bug", "Urgent"]
                }
            ]
        }

        populate_vikunja(mock_client, schema)

        # Should attach both labels
        assert mock_client.tasks.add_label.call_count == 2
        mock_client.tasks.add_label.assert_any_call(task_id=456, label_id=1)
        mock_client.tasks.add_label.assert_any_call(task_id=456, label_id=2)


class TestPopulationErrors:
    """Test error handling"""

    def test_error_creating_project(self):
        """Should raise PopulationError if project creation fails"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_client.projects.create.side_effect = Exception("API error")

        schema = {
            "project": {"title": "My Project"}
        }

        with pytest.raises(PopulationError, match="Failed to create/update project"):
            populate_vikunja(mock_client, schema)

    def test_error_creating_label(self):
        """Should raise PopulationError if label creation fails"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project
        mock_client.labels.create.side_effect = Exception("API error")

        schema = {
            "project": {"title": "My Project"},
            "labels": [{"title": "Bug"}]
        }

        with pytest.raises(PopulationError, match="Failed to create label"):
            populate_vikunja(mock_client, schema)

    def test_error_creating_task(self):
        """Should raise PopulationError if task creation fails"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project
        mock_client.tasks.create.side_effect = Exception("API error")

        schema = {
            "project": {"title": "My Project"},
            "tasks": [{"title": "Task 1"}]
        }

        with pytest.raises(PopulationError, match="Failed to create task"):
            populate_vikunja(mock_client, schema)

    def test_error_attaching_label(self):
        """Should raise PopulationError if label attachment fails"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label = Mock(id=999, title="Bug")
        mock_client.labels.create.return_value = mock_label

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        mock_client.tasks.add_label.side_effect = Exception("API error")

        schema = {
            "project": {"title": "My Project"},
            "labels": [{"title": "Bug", "hex_color": "FF0000"}],  # hex_color required
            "tasks": [{"title": "Task", "labels": ["Bug"]}]
        }

        with pytest.raises(PopulationError, match="Failed to attach label"):
            populate_vikunja(mock_client, schema)

    def test_task_references_undefined_label(self):
        """Should raise PopulationError if task references non-existent label"""
        mock_client = Mock()
        # Mocks for idempotent behavior
        mock_client.projects.list.return_value = []
        mock_client.tasks.list.return_value = []
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label = Mock(id=999, title="Bug")
        mock_client.labels.create.return_value = mock_label

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        schema = {
            "project": {"title": "My Project"},
            "labels": [{"title": "Bug", "hex_color": "FF0000"}],  # hex_color required
            "tasks": [{"title": "Task", "labels": ["Feature"]}]  # Feature not defined
        }

        with pytest.raises(PopulationError, match="Label 'Feature' not found"):
            populate_vikunja(mock_client, schema)


class TestDryRun:
    """Test dry-run mode (validate without creating)"""

    def test_dry_run_mode(self):
        """Dry run should not make any API calls"""
        mock_client = Mock()

        schema = {
            "project": {"title": "My Project"},
            "labels": [{"title": "Bug"}],
            "tasks": [{"title": "Task", "labels": ["Bug"]}]
        }

        result = populate_vikunja(mock_client, schema, dry_run=True)

        # No API calls should be made
        mock_client.projects.create.assert_not_called()
        mock_client.labels.create.assert_not_called()
        mock_client.tasks.create.assert_not_called()
        mock_client.tasks.add_label.assert_not_called()

        # Result should indicate dry run
        assert result["dry_run"] is True
        assert "summary" in result


class TestIdempotentPopulation:
    """Test that re-running population updates instead of duplicating"""

    def test_update_existing_project(self):
        """Should update project if it already exists with same title and parent"""
        mock_client = Mock()

        # Existing project with same title and parent
        existing_project = Mock(id=123, title="My Project", parent_project_id=0)
        mock_client.projects.list.return_value = [existing_project]

        # Updated project returned by update()
        updated_project = Mock(id=123, title="My Project", description="Updated")
        mock_client.projects.update.return_value = updated_project

        # No existing tasks (needed for Step 3)
        mock_client.tasks.list.return_value = []

        schema = {
            "project": {
                "title": "My Project",
                "description": "Updated"
            }
        }

        result = populate_vikunja(mock_client, schema)

        # Should NOT create new project
        mock_client.projects.create.assert_not_called()

        # Should UPDATE existing project
        mock_client.projects.update.assert_called_once_with(
            123,  # existing project ID
            title="My Project",
            description="Updated"
        )

        # Result should indicate update
        assert result["project"] == updated_project
        assert result["project_updated"] is True

    def test_create_new_project_if_not_exists(self):
        """Should create project if no matching project exists"""
        mock_client = Mock()

        # No existing projects
        mock_client.projects.list.return_value = []

        # New project returned by create()
        new_project = Mock(id=456, title="New Project", parent_project_id=0)
        mock_client.projects.create.return_value = new_project

        # No existing tasks (needed for Step 3)
        mock_client.tasks.list.return_value = []

        schema = {
            "project": {
                "title": "New Project"
            }
        }

        result = populate_vikunja(mock_client, schema)

        # Should CREATE new project
        mock_client.projects.create.assert_called_once_with(
            title="New Project"
        )

        # Should NOT update
        mock_client.projects.update.assert_not_called()

        # Result should indicate creation
        assert result["project"] == new_project
        assert result["project_updated"] is False

    def test_distinguish_projects_by_parent(self):
        """Should distinguish projects with same title but different parents"""
        mock_client = Mock()

        # Existing project with different parent
        existing_project = Mock(id=123, title="My Project", parent_project_id=5)
        mock_client.projects.list.return_value = [existing_project]

        # New project returned by create() (different parent)
        new_project = Mock(id=456, title="My Project", parent_project_id=10)
        mock_client.projects.create.return_value = new_project

        # No existing tasks (needed for Step 3)
        mock_client.tasks.list.return_value = []

        schema = {
            "project": {
                "title": "My Project",
                "parent_project_id": 10  # Different parent
            }
        }

        result = populate_vikunja(mock_client, schema)

        # Should CREATE new project (different parent means different project)
        mock_client.projects.create.assert_called_once()
        mock_client.projects.update.assert_not_called()

        assert result["project_updated"] is False

    def test_update_existing_tasks(self):
        """Should update tasks if they already exist in project"""
        mock_client = Mock()

        # Existing project
        mock_project = Mock(id=123, title="My Project", parent_project_id=0)
        mock_client.projects.list.return_value = [mock_project]
        mock_client.projects.update.return_value = mock_project

        # Existing tasks in project
        existing_task = Mock(id=789, title="Task 1", description="Old description")
        mock_client.tasks.list.return_value = [existing_task]

        # Updated task returned by update()
        updated_task = Mock(id=789, title="Task 1", description="New description")
        mock_client.tasks.update.return_value = updated_task

        schema = {
            "project": {"title": "My Project"},
            "tasks": [
                {
                    "title": "Task 1",
                    "description": "New description"
                }
            ]
        }

        result = populate_vikunja(mock_client, schema)

        # Should NOT create new task
        mock_client.tasks.create.assert_not_called()

        # Should UPDATE existing task
        mock_client.tasks.update.assert_called_once_with(
            789,  # existing task ID
            project_id=123,
            title="Task 1",
            description="New description"
        )

        assert len(result["tasks"]) == 1
        assert result["tasks"][0] == updated_task

    def test_create_new_tasks_if_not_exist(self):
        """Should create tasks if they don't exist in project"""
        mock_client = Mock()

        # Existing project
        mock_project = Mock(id=123, title="My Project", parent_project_id=0)
        mock_client.projects.list.return_value = [mock_project]
        mock_client.projects.update.return_value = mock_project

        # No existing tasks
        mock_client.tasks.list.return_value = []

        # New task returned by create()
        new_task = Mock(id=999, title="New Task")
        mock_client.tasks.create.return_value = new_task

        schema = {
            "project": {"title": "My Project"},
            "tasks": [{"title": "New Task"}]
        }

        result = populate_vikunja(mock_client, schema)

        # Should CREATE new task
        mock_client.tasks.create.assert_called_once_with(
            project_id=123,
            title="New Task"
        )

        # Should NOT update
        mock_client.tasks.update.assert_not_called()

    def test_mixed_update_and_create_tasks(self):
        """Should update existing tasks and create new tasks in same run"""
        mock_client = Mock()

        # Existing project
        mock_project = Mock(id=123, title="My Project", parent_project_id=0)
        mock_client.projects.list.return_value = [mock_project]
        mock_client.projects.update.return_value = mock_project

        # One existing task
        existing_task = Mock(id=789, title="Existing Task")
        mock_client.tasks.list.return_value = [existing_task]

        # Mocks for update and create
        updated_task = Mock(id=789, title="Existing Task", description="Updated")
        mock_client.tasks.update.return_value = updated_task

        new_task = Mock(id=999, title="New Task")
        mock_client.tasks.create.return_value = new_task

        schema = {
            "project": {"title": "My Project"},
            "tasks": [
                {"title": "Existing Task", "description": "Updated"},
                {"title": "New Task"}
            ]
        }

        result = populate_vikunja(mock_client, schema)

        # Should update existing and create new
        mock_client.tasks.update.assert_called_once()
        mock_client.tasks.create.assert_called_once()

        assert len(result["tasks"]) == 2
