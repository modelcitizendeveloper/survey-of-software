#!/usr/bin/env python3
"""
Unit tests for schema validation

Tests written BEFORE implementation (TDD).
After implementation, these tests will be verified by injecting bugs (Adaptive TDD).
"""

import pytest
from validation import (
    validate_schema,
    ValidationError,
    validate_project,
    validate_label,
    validate_task,
    validate_date_format,
    validate_hex_color,
)


class TestValidateHexColor:
    """Test hex color validation"""

    def test_valid_6_char_hex(self):
        """Valid 6-character hex colors should pass"""
        assert validate_hex_color("FF0000") is True
        assert validate_hex_color("00ff00") is True
        assert validate_hex_color("123abc") is True

    def test_invalid_with_hash(self):
        """Hex colors with # prefix should fail"""
        with pytest.raises(ValidationError, match="must not include"):
            validate_hex_color("#FF0000")

    def test_invalid_length(self):
        """Non-6-character strings should fail"""
        with pytest.raises(ValidationError, match="must be exactly 6"):
            validate_hex_color("FFF")
        with pytest.raises(ValidationError, match="must be exactly 6"):
            validate_hex_color("FF00000")

    def test_invalid_characters(self):
        """Non-hex characters should fail"""
        with pytest.raises(ValidationError, match="Invalid hex"):
            validate_hex_color("GGGGGG")
        with pytest.raises(ValidationError, match="Invalid hex"):
            validate_hex_color("FF00ZZ")


class TestValidateDateFormat:
    """Test date format validation"""

    def test_valid_dates(self):
        """Valid YYYY-MM-DD dates should pass"""
        assert validate_date_format("2025-11-15") is True
        assert validate_date_format("2025-01-01") is True
        assert validate_date_format("2025-12-31") is True

    def test_invalid_format(self):
        """Invalid date formats should fail"""
        with pytest.raises(ValidationError, match="must be YYYY-MM-DD"):
            validate_date_format("11/15/2025")
        with pytest.raises(ValidationError, match="must be YYYY-MM-DD"):
            validate_date_format("2025-11-15T12:00:00")
        with pytest.raises(ValidationError, match="must be YYYY-MM-DD"):
            validate_date_format("15-11-2025")

    def test_invalid_dates(self):
        """Invalid dates (like Feb 30) should fail"""
        with pytest.raises(ValidationError, match="Invalid date"):
            validate_date_format("2025-02-30")
        with pytest.raises(ValidationError, match="Invalid date"):
            validate_date_format("2025-13-01")
        with pytest.raises(ValidationError, match="Invalid date"):
            validate_date_format("2025-00-01")


class TestValidateProject:
    """Test project schema validation"""

    def test_valid_minimal_project(self):
        """Minimal valid project (title only) should pass"""
        project = {"title": "My Project"}
        assert validate_project(project) is True

    def test_valid_full_project(self):
        """Full project with all fields should pass"""
        project = {
            "title": "My Project",
            "description": "A detailed description",
            "color": "FF0000",
        }
        assert validate_project(project) is True

    def test_missing_title(self):
        """Project without title should fail"""
        project = {"description": "No title"}
        with pytest.raises(ValidationError, match="missing required field: title"):
            validate_project(project)

    def test_empty_title(self):
        """Project with empty title should fail"""
        project = {"title": ""}
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_project(project)

    def test_title_too_long(self):
        """Project title over 250 chars should fail"""
        project = {"title": "x" * 251}
        with pytest.raises(ValidationError, match="cannot exceed 250"):
            validate_project(project)

    def test_description_too_long(self):
        """Project description over 5000 chars should fail"""
        project = {"title": "Valid", "description": "x" * 5001}
        with pytest.raises(ValidationError, match="cannot exceed 5000"):
            validate_project(project)

    def test_invalid_color(self):
        """Project with invalid color should fail"""
        project = {"title": "Valid", "color": "#FF0000"}
        with pytest.raises(ValidationError, match="must not include"):
            validate_project(project)

    def test_wrong_type_title(self):
        """Project with non-string title should fail"""
        project = {"title": 123}
        with pytest.raises(ValidationError, match="must be a string"):
            validate_project(project)


class TestValidateLabel:
    """Test label schema validation"""

    def test_valid_minimal_label(self):
        """Minimal valid label (title only) should pass"""
        label = {"title": "Bug"}
        assert validate_label(label) is True

    def test_valid_full_label(self):
        """Full label with all fields should pass"""
        label = {
            "title": "Bug",
            "description": "Bug tracking label",
            "color": "FF0000",
        }
        assert validate_label(label) is True

    def test_missing_title(self):
        """Label without title should fail"""
        label = {"color": "FF0000"}
        with pytest.raises(ValidationError, match="missing required field: title"):
            validate_label(label)

    def test_empty_title(self):
        """Label with empty title should fail"""
        label = {"title": ""}
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_label(label)

    def test_title_too_long(self):
        """Label title over 100 chars should fail"""
        label = {"title": "x" * 101}
        with pytest.raises(ValidationError, match="cannot exceed 100"):
            validate_label(label)

    def test_description_too_long(self):
        """Label description over 500 chars should fail"""
        label = {"title": "Valid", "description": "x" * 501}
        with pytest.raises(ValidationError, match="cannot exceed 500"):
            validate_label(label)


class TestValidateTask:
    """Test task schema validation"""

    def test_valid_minimal_task(self):
        """Minimal valid task (title only) should pass"""
        task = {"title": "My Task"}
        assert validate_task(task, available_labels=[]) is True

    def test_valid_full_task(self):
        """Full task with all fields should pass"""
        task = {
            "title": "My Task",
            "description": "Detailed description<br>with HTML",
            "due_date": "2025-11-15",
            "priority": 5,
            "labels": ["Bug", "Feature"],
            "done": False,
        }
        assert validate_task(task, available_labels=["Bug", "Feature"]) is True

    def test_missing_title(self):
        """Task without title should fail"""
        task = {"description": "No title"}
        with pytest.raises(ValidationError, match="missing required field: title"):
            validate_task(task, available_labels=[])

    def test_empty_title(self):
        """Task with empty title should fail"""
        task = {"title": ""}
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_task(task, available_labels=[])

    def test_title_too_long(self):
        """Task title over 250 chars should fail"""
        task = {"title": "x" * 251}
        with pytest.raises(ValidationError, match="cannot exceed 250"):
            validate_task(task, available_labels=[])

    def test_description_too_long(self):
        """Task description over 50000 chars should fail"""
        task = {"title": "Valid", "description": "x" * 50001}
        with pytest.raises(ValidationError, match="cannot exceed 50000"):
            validate_task(task, available_labels=[])

    def test_invalid_date(self):
        """Task with invalid date should fail"""
        task = {"title": "Valid", "due_date": "11/15/2025"}
        with pytest.raises(ValidationError, match="must be YYYY-MM-DD"):
            validate_task(task, available_labels=[])

    def test_invalid_priority_low(self):
        """Task with priority < 0 should fail"""
        task = {"title": "Valid", "priority": -1}
        with pytest.raises(ValidationError, match="must be between 0 and 5"):
            validate_task(task, available_labels=[])

    def test_invalid_priority_high(self):
        """Task with priority > 5 should fail"""
        task = {"title": "Valid", "priority": 6}
        with pytest.raises(ValidationError, match="must be between 0 and 5"):
            validate_task(task, available_labels=[])

    def test_invalid_done_type(self):
        """Task with non-boolean done should fail"""
        task = {"title": "Valid", "done": "yes"}
        with pytest.raises(ValidationError, match="must be a boolean"):
            validate_task(task, available_labels=[])

    def test_label_reference_not_found(self):
        """Task referencing non-existent label should fail"""
        task = {"title": "Valid", "labels": ["NonExistent"]}
        with pytest.raises(ValidationError, match="Label 'NonExistent' not found"):
            validate_task(task, available_labels=["Bug", "Feature"])

    def test_labels_not_list(self):
        """Task with non-list labels should fail"""
        task = {"title": "Valid", "labels": "Bug"}
        with pytest.raises(ValidationError, match="must be a list"):
            validate_task(task, available_labels=["Bug"])


class TestValidateSchema:
    """Test full schema validation"""

    def test_valid_minimal_schema(self):
        """Minimal valid schema (project + empty tasks) should pass"""
        schema = {
            "project": {"title": "My Project"},
            "tasks": [],
        }
        assert validate_schema(schema) is True

    def test_valid_full_schema(self):
        """Full schema with project, labels, tasks should pass"""
        schema = {
            "project": {
                "title": "My Project",
                "description": "Description",
            },
            "labels": [
                {"title": "Bug", "color": "FF0000"},
            ],
            "tasks": [
                {
                    "title": "Fix bug",
                    "labels": ["Bug"],
                }
            ],
        }
        assert validate_schema(schema) is True

    def test_missing_project(self):
        """Schema without project should fail"""
        schema = {"tasks": []}
        with pytest.raises(ValidationError, match="missing required field: project"):
            validate_schema(schema)

    def test_invalid_project(self):
        """Schema with invalid project should fail"""
        schema = {
            "project": {"title": ""},  # Empty title
            "tasks": [],
        }
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_schema(schema)

    def test_invalid_label(self):
        """Schema with invalid label should fail"""
        schema = {
            "project": {"title": "Valid"},
            "labels": [{"title": ""}],  # Empty title
            "tasks": [],
        }
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_schema(schema)

    def test_invalid_task(self):
        """Schema with invalid task should fail"""
        schema = {
            "project": {"title": "Valid"},
            "tasks": [{"title": ""}],  # Empty title
        }
        with pytest.raises(ValidationError, match="cannot be empty"):
            validate_schema(schema)

    def test_task_label_reference(self):
        """Task referencing undefined label should fail"""
        schema = {
            "project": {"title": "Valid"},
            "labels": [{"title": "Bug"}],
            "tasks": [{"title": "Valid", "labels": ["Feature"]}],
        }
        with pytest.raises(ValidationError, match="Label 'Feature' not found"):
            validate_schema(schema)

    def test_not_dict(self):
        """Non-dict schema should fail"""
        with pytest.raises(ValidationError, match="must be a dictionary"):
            validate_schema("not a dict")

    def test_tasks_not_list(self):
        """Schema with non-list tasks should fail"""
        schema = {
            "project": {"title": "Valid"},
            "tasks": "not a list",
        }
        with pytest.raises(ValidationError, match="must be a list"):
            validate_schema(schema)

    def test_labels_not_list(self):
        """Schema with non-list labels should fail"""
        schema = {
            "project": {"title": "Valid"},
            "labels": "not a list",
            "tasks": [],
        }
        with pytest.raises(ValidationError, match="must be a list"):
            validate_schema(schema)
