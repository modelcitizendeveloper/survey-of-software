#!/usr/bin/env python3
"""
Schema validation for Vikunja population script

Validates YAML/JSON input against defined schema (see SCHEMA.md).
"""

from datetime import datetime
from typing import Any, Dict, List


class ValidationError(Exception):
    """Raised when schema validation fails"""
    pass


def validate_hex_color(color: str) -> bool:
    """
    Validate hex color format (6 characters, no # prefix)

    Args:
        color: Hex color string

    Returns:
        True if valid

    Raises:
        ValidationError: If color format is invalid
    """
    if not isinstance(color, str):
        raise ValidationError("Color must be a string")

    if color.startswith("#"):
        raise ValidationError("Hex color must not include '#' prefix")

    if len(color) != 6:
        raise ValidationError(f"Hex color must be exactly 6 characters, got {len(color)}")

    try:
        int(color, 16)
    except ValueError:
        raise ValidationError(f"Invalid hex color: {color}")

    return True


def validate_date_format(date_str: str) -> bool:
    """
    Validate date format (YYYY-MM-DD)

    Args:
        date_str: Date string

    Returns:
        True if valid

    Raises:
        ValidationError: If date format is invalid
    """
    if not isinstance(date_str, str):
        raise ValidationError("Date must be a string")

    # Check format first (YYYY-MM-DD pattern)
    if len(date_str) != 10 or date_str[4] != '-' or date_str[7] != '-':
        raise ValidationError(f"Date must be YYYY-MM-DD format, got: {date_str}")

    try:
        datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        # If format is correct but date is invalid (e.g., Feb 30)
        raise ValidationError(f"Invalid date: {date_str}")

    return True


def validate_project(project: Dict[str, Any]) -> bool:
    """
    Validate project schema

    Args:
        project: Project dictionary

    Returns:
        True if valid

    Raises:
        ValidationError: If project schema is invalid
    """
    if not isinstance(project, dict):
        raise ValidationError("Project must be a dictionary")

    # Required: title
    if "title" not in project:
        raise ValidationError("Project missing required field: title")

    title = project["title"]
    if not isinstance(title, str):
        raise ValidationError("Project title must be a string")

    if not title.strip():
        raise ValidationError("Project title cannot be empty")

    if len(title) > 250:
        raise ValidationError(f"Project title cannot exceed 250 characters, got {len(title)}")

    # Optional: description
    if "description" in project:
        description = project["description"]
        if not isinstance(description, str):
            raise ValidationError("Project description must be a string")

        if len(description) > 5000:
            raise ValidationError(f"Project description cannot exceed 5000 characters, got {len(description)}")

    # Optional: color
    if "color" in project:
        validate_hex_color(project["color"])

    return True


def validate_label(label: Dict[str, Any]) -> bool:
    """
    Validate label schema

    Args:
        label: Label dictionary

    Returns:
        True if valid

    Raises:
        ValidationError: If label schema is invalid
    """
    if not isinstance(label, dict):
        raise ValidationError("Label must be a dictionary")

    # Required: title
    if "title" not in label:
        raise ValidationError("Label missing required field: title")

    title = label["title"]
    if not isinstance(title, str):
        raise ValidationError("Label title must be a string")

    if not title.strip():
        raise ValidationError("Label title cannot be empty")

    if len(title) > 100:
        raise ValidationError(f"Label title cannot exceed 100 characters, got {len(title)}")

    # Optional: description
    if "description" in label:
        description = label["description"]
        if not isinstance(description, str):
            raise ValidationError("Label description must be a string")

        if len(description) > 500:
            raise ValidationError(f"Label description cannot exceed 500 characters, got {len(description)}")

    # Optional: color
    if "color" in label:
        validate_hex_color(label["color"])

    return True


def validate_task(task: Dict[str, Any], available_labels: List[str]) -> bool:
    """
    Validate task schema

    Args:
        task: Task dictionary
        available_labels: List of available label titles

    Returns:
        True if valid

    Raises:
        ValidationError: If task schema is invalid
    """
    if not isinstance(task, dict):
        raise ValidationError("Task must be a dictionary")

    # Required: title
    if "title" not in task:
        raise ValidationError("Task missing required field: title")

    title = task["title"]
    if not isinstance(title, str):
        raise ValidationError("Task title must be a string")

    if not title.strip():
        raise ValidationError("Task title cannot be empty")

    if len(title) > 250:
        raise ValidationError(f"Task title cannot exceed 250 characters, got {len(title)}")

    # Optional: description
    if "description" in task:
        description = task["description"]
        if not isinstance(description, str):
            raise ValidationError("Task description must be a string")

        if len(description) > 50000:
            raise ValidationError(f"Task description cannot exceed 50000 characters, got {len(description)}")

    # Optional: due_date
    if "due_date" in task:
        validate_date_format(task["due_date"])

    # Optional: priority
    if "priority" in task:
        priority = task["priority"]
        if not isinstance(priority, int):
            raise ValidationError("Task priority must be an integer")

        if priority < 0 or priority > 5:
            raise ValidationError(f"Task priority must be between 0 and 5, got {priority}")

    # Optional: done
    if "done" in task:
        done = task["done"]
        if not isinstance(done, bool):
            raise ValidationError("Task 'done' field must be a boolean")

    # Optional: labels
    if "labels" in task:
        labels = task["labels"]
        if not isinstance(labels, list):
            raise ValidationError("Task labels must be a list")

        for label_title in labels:
            if label_title not in available_labels:
                raise ValidationError(f"Label '{label_title}' not found in available labels")

    return True


def validate_schema(schema: Dict[str, Any]) -> bool:
    """
    Validate full schema (project, labels, tasks)

    Args:
        schema: Full schema dictionary

    Returns:
        True if valid

    Raises:
        ValidationError: If schema is invalid
    """
    if not isinstance(schema, dict):
        raise ValidationError("Schema must be a dictionary")

    # Required: project
    if "project" not in schema:
        raise ValidationError("Schema missing required field: project")

    validate_project(schema["project"])

    # Optional: labels (default to empty list)
    labels = schema.get("labels", [])
    if not isinstance(labels, list):
        raise ValidationError("Labels must be a list")

    available_label_titles = []
    for i, label in enumerate(labels):
        try:
            validate_label(label)
            available_label_titles.append(label["title"])
        except ValidationError as e:
            raise ValidationError(f"Label {i}: {e}")

    # Optional: tasks (default to empty list)
    tasks = schema.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValidationError("Tasks must be a list")

    for i, task in enumerate(tasks):
        try:
            validate_task(task, available_label_titles)
        except ValidationError as e:
            raise ValidationError(f"Task {i}: {e}")

    return True
