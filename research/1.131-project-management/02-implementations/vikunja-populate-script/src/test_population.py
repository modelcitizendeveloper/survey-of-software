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


class TestPopulateLabels:
    """Test label creation"""

    def test_create_labels(self):
        """Should create all labels"""
        mock_client = Mock()
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

        # Verify labels were created
        assert mock_client.labels.create.call_count == 2
        mock_client.labels.create.assert_any_call(
            title="Bug",
            color="FF0000"
        )
        mock_client.labels.create.assert_any_call(
            title="Feature",
            color="00FF00"
        )

        # Verify result
        assert len(result["labels"]) == 2

    def test_create_labels_without_color(self):
        """Should create labels without color field"""
        mock_client = Mock()
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label = Mock(id=1, title="Bug")
        mock_client.labels.create.return_value = mock_label

        schema = {
            "project": {"title": "My Project"},
            "labels": [
                {"title": "Bug"}  # No color
            ]
        }

        populate_vikunja(mock_client, schema)

        # Should only pass title
        mock_client.labels.create.assert_called_once_with(
            title="Bug"
        )


class TestPopulateTasks:
    """Test task creation"""

    def test_create_tasks(self):
        """Should create all tasks"""
        mock_client = Mock()
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
                    "done": True,
                }
            ]
        }

        populate_vikunja(mock_client, schema)

        mock_client.tasks.create.assert_called_once_with(
            project_id=123,
            title="Task 1",
            description="Test description",
            due_date="2025-11-15",
            priority=5,
            done=True
        )

    def test_attach_labels_to_tasks(self):
        """Should attach labels to tasks after creation"""
        mock_client = Mock()
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label = Mock(id=999, title="Bug")
        mock_client.labels.create.return_value = mock_label

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        schema = {
            "project": {"title": "My Project"},
            "labels": [
                {"title": "Bug"}
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
                {"title": "Bug"},
                {"title": "Urgent"},
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
        mock_client.projects.create.side_effect = Exception("API error")

        schema = {
            "project": {"title": "My Project"}
        }

        with pytest.raises(PopulationError, match="Failed to create project"):
            populate_vikunja(mock_client, schema)

    def test_error_creating_label(self):
        """Should raise PopulationError if label creation fails"""
        mock_client = Mock()
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
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_label = Mock(id=999, title="Bug")
        mock_client.labels.create.return_value = mock_label

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        mock_client.tasks.add_label.side_effect = Exception("API error")

        schema = {
            "project": {"title": "My Project"},
            "labels": [{"title": "Bug"}],
            "tasks": [{"title": "Task", "labels": ["Bug"]}]
        }

        with pytest.raises(PopulationError, match="Failed to attach label"):
            populate_vikunja(mock_client, schema)

    def test_task_references_undefined_label(self):
        """Should raise PopulationError if task references non-existent label"""
        mock_client = Mock()
        mock_project = Mock(id=123)
        mock_client.projects.create.return_value = mock_project

        mock_task = Mock(id=456)
        mock_client.tasks.create.return_value = mock_task

        schema = {
            "project": {"title": "My Project"},
            "labels": [{"title": "Bug"}],
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
