#!/usr/bin/env python3
"""
Vikunja population logic

Creates projects, labels, and tasks in Vikunja from validated schema.
"""

from typing import Dict, Any, List


class PopulationError(Exception):
    """Raised when population fails"""
    pass


def populate_vikunja(client: Any, schema: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
    """
    Populate Vikunja with projects, labels, and tasks from schema

    Args:
        client: VikunjaClient instance
        schema: Validated schema dictionary
        dry_run: If True, validate without creating (no API calls)

    Returns:
        Dictionary with created resources:
        {
            "project": Project object,
            "labels": [Label objects],
            "tasks": [Task objects]
        }

    Raises:
        PopulationError: If population fails
    """
    if dry_run:
        return _dry_run_summary(schema)

    result = {
        "project": None,
        "labels": [],
        "tasks": [],
    }

    # Step 1: Create project
    try:
        project_data = schema["project"]
        kwargs = {"title": project_data["title"]}

        if "description" in project_data:
            kwargs["description"] = project_data["description"]
        if "color" in project_data:
            kwargs["color"] = project_data["color"]

        project = client.projects.create(**kwargs)
        result["project"] = project

    except Exception as e:
        raise PopulationError(f"Failed to create project: {e}")

    # Step 2: Create labels
    label_map = {}  # Map label title -> label object

    for label_data in schema.get("labels", []):
        try:
            kwargs = {"title": label_data["title"]}

            if "description" in label_data:
                kwargs["description"] = label_data["description"]
            if "color" in label_data:
                kwargs["color"] = label_data["color"]

            label = client.labels.create(**kwargs)
            result["labels"].append(label)
            label_map[label.title] = label

        except Exception as e:
            raise PopulationError(f"Failed to create label '{label_data['title']}': {e}")

    # Step 3: Create tasks
    for task_data in schema.get("tasks", []):
        try:
            # Prepare task kwargs (exclude 'labels' field)
            kwargs = {
                "project_id": project.id,
                "title": task_data["title"]
            }

            for field in ["description", "due_date", "priority", "done"]:
                if field in task_data:
                    kwargs[field] = task_data[field]

            task = client.tasks.create(**kwargs)
            result["tasks"].append(task)

            # Attach labels to task
            if "labels" in task_data:
                for label_title in task_data["labels"]:
                    if label_title not in label_map:
                        raise PopulationError(
                            f"Label '{label_title}' not found in created labels. "
                            f"Available labels: {list(label_map.keys())}"
                        )

                    try:
                        client.tasks.add_label(
                            task_id=task.id,
                            label_id=label_map[label_title].id
                        )
                    except Exception as e:
                        raise PopulationError(
                            f"Failed to attach label '{label_title}' to task '{task_data['title']}': {e}"
                        )

        except PopulationError:
            raise  # Re-raise our own errors
        except Exception as e:
            raise PopulationError(f"Failed to create task '{task_data['title']}': {e}")

    return result


def _dry_run_summary(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate summary for dry-run mode (no API calls)

    Args:
        schema: Validated schema

    Returns:
        Summary dictionary
    """
    num_labels = len(schema.get("labels", []))
    num_tasks = len(schema.get("tasks", []))

    summary = {
        "dry_run": True,
        "summary": {
            "project": schema["project"]["title"],
            "labels": num_labels,
            "tasks": num_tasks,
        }
    }

    # Add label details
    if num_labels > 0:
        summary["label_titles"] = [
            label["title"] for label in schema.get("labels", [])
        ]

    # Add task details
    if num_tasks > 0:
        summary["task_titles"] = [
            task["title"] for task in schema.get("tasks", [])
        ]

    return summary
