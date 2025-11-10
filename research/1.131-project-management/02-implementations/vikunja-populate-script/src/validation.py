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


def validate_bucket(bucket: Dict[str, Any]) -> bool:
    """
    Validate bucket schema

    Args:
        bucket: Bucket dictionary

    Returns:
        True if valid

    Raises:
        ValidationError: If bucket schema is invalid
    """
    if not isinstance(bucket, dict):
        raise ValidationError("Bucket must be a dictionary")

    # Required: name
    if "name" not in bucket:
        raise ValidationError("Bucket missing required field: name")

    name = bucket["name"]
    if not isinstance(name, str):
        raise ValidationError("Bucket name must be a string")

    if not name.strip():
        raise ValidationError("Bucket name cannot be empty")

    # Required: position
    if "position" not in bucket:
        raise ValidationError("Bucket missing required field: position")

    position = bucket["position"]
    if not isinstance(position, int):
        raise ValidationError("Bucket position must be an integer")

    # Optional: limit
    if "limit" in bucket:
        limit = bucket["limit"]
        if not isinstance(limit, int):
            raise ValidationError("Bucket limit must be an integer")

        if limit < 0:
            raise ValidationError("Bucket limit cannot be negative")

    return True


def validate_project(project: Dict[str, Any], allow_root_project: bool = False) -> bool:
    """
    Validate project schema

    Args:
        project: Project dictionary
        allow_root_project: If True, allow projects without parent (for automation/testing)

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

    # Required: parent_project or parent_project_id (no root-level projects allowed by default)
    # UNLESS: project_id is specified (adding tasks to existing project, not creating new)
    has_parent = "parent_project" in project or "parent_project_id" in project
    is_adding_to_existing = "project_id" in project

    if not has_parent and not allow_root_project and not is_adding_to_existing:
        raise ValidationError(
            f"Project '{title}' must have a parent_project or parent_project_id field. "
            "Root-level projects are not allowed. "
            "Specify the parent project hierarchy (e.g., 'Applications/Products') or parent_project_id. "
            "Use --allow-root-project flag to override this check."
        )

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

    # Optional: buckets
    if "buckets" in project:
        buckets = project["buckets"]
        if not isinstance(buckets, list):
            raise ValidationError("Project buckets must be a list")

        for i, bucket in enumerate(buckets):
            try:
                validate_bucket(bucket)
            except ValidationError as e:
                raise ValidationError(f"Bucket {i}: {e}")

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

        # Note: We don't validate label existence here because:
        # 1. Labels are global in Vikunja (shared across projects)
        # 2. Tasks can reference bootstrap/global labels not defined in this YAML
        # 3. The populate script will check label existence at runtime
        for label_title in labels:
            if not isinstance(label_title, str):
                raise ValidationError(f"Label title must be a string, got {type(label_title)}")

    # Optional: bucket
    if "bucket" in task:
        bucket = task["bucket"]
        if not isinstance(bucket, str):
            raise ValidationError("Task bucket must be a string")

        if not bucket.strip():
            raise ValidationError("Task bucket name cannot be empty")

    # Optional: blocked_by
    if "blocked_by" in task:
        blocked_by = task["blocked_by"]
        if not isinstance(blocked_by, list):
            raise ValidationError("Task blocked_by must be a list")

        for i, blocker in enumerate(blocked_by):
            if not isinstance(blocker, str):
                raise ValidationError(f"blocked_by[{i}] must be a string (task title)")

            if not blocker.strip():
                raise ValidationError(f"blocked_by[{i}] cannot be empty")

    # Optional: subtask_of
    if "subtask_of" in task:
        subtask_of = task["subtask_of"]
        if not isinstance(subtask_of, str):
            raise ValidationError("Task subtask_of must be a string (parent task title)")

        if not subtask_of.strip():
            raise ValidationError("Task subtask_of cannot be empty")

    # Optional: assignees
    if "assignees" in task:
        assignees = task["assignees"]
        if not isinstance(assignees, list):
            raise ValidationError("Task assignees must be a list")

        for i, assignee in enumerate(assignees):
            if not isinstance(assignee, str):
                raise ValidationError(f"assignees[{i}] must be a string (email or username)")

            if not assignee.strip():
                raise ValidationError(f"assignees[{i}] cannot be empty")

    return True


def validate_schema(schema: Dict[str, Any], allow_root_project: bool = False) -> bool:
    """
    Validate full schema (project, labels, tasks)

    Args:
        schema: Full schema dictionary
        allow_root_project: If True, allow projects without parent (for automation/testing)

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

    validate_project(schema["project"], allow_root_project=allow_root_project)

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
