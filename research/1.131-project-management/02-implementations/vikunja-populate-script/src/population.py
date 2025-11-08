#!/usr/bin/env python3
"""
Vikunja population logic

Creates projects, labels, and tasks in Vikunja from validated schema.
"""

from typing import Dict, Any, List
from datetime import datetime


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
        "buckets": [],
        "labels": [],
        "tasks": [],
        "relations": [],
    }

    # Step 1: Create or update project
    try:
        project_data = schema["project"]
        title = project_data["title"]
        parent_id = project_data.get("parent_project_id", 0)

        # Check if project already exists
        all_projects = client.projects.list()
        existing_project = None
        for p in all_projects:
            if p.title == title and p.parent_project_id == parent_id:
                existing_project = p
                break

        # Prepare kwargs
        kwargs = {"title": title}
        if "description" in project_data:
            kwargs["description"] = project_data["description"]
        if "color" in project_data:
            kwargs["color"] = project_data["color"]
        if "parent_project_id" in project_data:
            kwargs["parent_project_id"] = project_data["parent_project_id"]

        if existing_project:
            # Update existing project
            project = client.projects.update(existing_project.id, **kwargs)
            result["project"] = project
            result["project_updated"] = True
        else:
            # Create new project
            project = client.projects.create(**kwargs)
            result["project"] = project
            result["project_updated"] = False

    except Exception as e:
        raise PopulationError(f"Failed to create/update project: {e}")

    # Step 2: Create buckets (if defined)
    bucket_map = {}  # Map bucket name -> bucket object

    if "buckets" in schema.get("project", {}):
        # Get existing buckets
        try:
            existing_buckets = client.buckets.list(project_id=project.id)
            existing_bucket_map = {b.title: b for b in existing_buckets}
        except Exception as e:
            raise PopulationError(f"Failed to list existing buckets: {e}")

        for bucket_data in schema["project"]["buckets"]:
            try:
                bucket_name = bucket_data["name"]

                # Check if bucket already exists
                if bucket_name in existing_bucket_map:
                    # Use existing bucket
                    bucket = existing_bucket_map[bucket_name]
                    # Optionally update bucket properties
                    if "position" in bucket_data or "limit" in bucket_data:
                        update_kwargs = {}
                        if "position" in bucket_data:
                            update_kwargs["position"] = bucket_data["position"]
                        if "limit" in bucket_data:
                            update_kwargs["limit"] = bucket_data["limit"]
                        if update_kwargs:
                            bucket = client.buckets.update(
                                project_id=project.id,
                                bucket_id=bucket.id,
                                **update_kwargs
                            )
                else:
                    # Create new bucket
                    bucket = client.buckets.create(
                        project_id=project.id,
                        title=bucket_name,
                        position=bucket_data.get("position", 0),
                        limit=bucket_data.get("limit", 0)
                    )
                    result["buckets"].append(bucket)

                bucket_map[bucket_name] = bucket

            except Exception as e:
                raise PopulationError(f"Failed to create/update bucket '{bucket_data['name']}': {e}")

    # Step 3: Create or reuse labels (labels are global in Vikunja)
    label_map = {}  # Map label title -> label object

    # Get existing labels
    try:
        existing_labels = client.labels.list()
        existing_labels_map = {label.title: label for label in existing_labels}
    except Exception as e:
        raise PopulationError(f"Failed to list existing labels: {e}")

    for label_data in schema.get("labels", []):
        try:
            label_title = label_data["title"]

            # Check if label already exists (labels are global)
            if label_title in existing_labels_map:
                # Use existing label
                label = existing_labels_map[label_title]
                label_map[label.title] = label
            else:
                # Create new label
                kwargs = {"title": label_title}

                # hex_color is required by the API
                if "hex_color" in label_data:
                    kwargs["hex_color"] = label_data["hex_color"]
                elif "color" in label_data:
                    kwargs["hex_color"] = label_data["color"]
                else:
                    raise PopulationError(f"Label '{label_title}' missing required field 'hex_color'")

                label = client.labels.create(**kwargs)
                result["labels"].append(label)
                label_map[label.title] = label

        except PopulationError:
            raise  # Re-raise our own errors
        except Exception as e:
            raise PopulationError(f"Failed to create label '{label_data['title']}': {e}")

    # Step 4: Create or update tasks
    # Get existing tasks for this project
    existing_tasks = client.tasks.list(project_id=project.id)
    existing_tasks_map = {task.title: task for task in existing_tasks}
    task_map = {}  # Map task title -> task object (for relations)

    for task_data in schema.get("tasks", []):
        try:
            task_title = task_data["title"]
            existing_task = existing_tasks_map.get(task_title)

            # Prepare task kwargs (exclude 'labels' field)
            kwargs = {
                "project_id": project.id,
                "title": task_title
            }

            for field in ["description", "priority"]:
                if field in task_data:
                    kwargs[field] = task_data[field]

            # Convert YYYY-MM-DD to ISO datetime for API
            if "due_date" in task_data:
                date_str = task_data["due_date"]
                # If it's just a date (YYYY-MM-DD), convert to ISO datetime
                if len(date_str) == 10:
                    kwargs["due_date"] = f"{date_str}T23:59:59Z"
                else:
                    kwargs["due_date"] = date_str

            if existing_task:
                # Update existing task (only supported fields: title, description, priority)
                # Note: project_id and due_date cannot be updated via tasks.update()
                update_kwargs = {}
                for field in ['title', 'description', 'priority']:
                    if field in kwargs:
                        update_kwargs[field] = kwargs[field]
                task = client.tasks.update(existing_task.id, **update_kwargs)
            else:
                # Create new task
                task = client.tasks.create(**kwargs)

            result["tasks"].append(task)
            task_map[task_title] = task  # Store for relations

            # Attach labels to task
            if "labels" in task_data:
                for label_title in task_data["labels"]:
                    # Check both YAML-defined labels and existing global labels
                    label = None
                    if label_title in label_map:
                        label = label_map[label_title]
                    elif label_title in existing_labels_map:
                        label = existing_labels_map[label_title]
                    else:
                        raise PopulationError(
                            f"Label '{label_title}' not found. "
                            f"Available labels in YAML: {list(label_map.keys())}. "
                            f"Available global labels: {list(existing_labels_map.keys())}"
                        )

                    try:
                        client.tasks.add_label(
                            task_id=task.id,
                            label_id=label.id
                        )
                    except Exception as e:
                        raise PopulationError(
                            f"Failed to attach label '{label_title}' to task '{task_data['title']}': {e}"
                        )

        except PopulationError:
            raise  # Re-raise our own errors
        except Exception as e:
            raise PopulationError(f"Failed to create task '{task_data['title']}': {e}")

    # Step 5: Create task relations
    for task_data in schema.get("tasks", []):
        task_title = task_data["title"]
        task = task_map[task_title]

        # Handle blocked_by relations
        if "blocked_by" in task_data:
            for blocker_title in task_data["blocked_by"]:
                blocker_task = task_map.get(blocker_title)
                if not blocker_task:
                    raise PopulationError(
                        f"Task '{task_title}' blocked by '{blocker_title}', but '{blocker_title}' not found in tasks"
                    )

                try:
                    # Create blocking relation: blocker_task blocks task
                    relation = client.task_relations.create(
                        task_id=blocker_task.id,
                        relation_kind="blocking",
                        other_task_id=task.id
                    )
                    result["relations"].append(relation)
                except Exception as e:
                    # Ignore if relation already exists
                    if "already exists" not in str(e).lower():
                        raise PopulationError(
                            f"Failed to create blocking relation '{blocker_title}' → '{task_title}': {e}"
                        )

        # Handle subtask_of relations
        if "subtask_of" in task_data:
            parent_title = task_data["subtask_of"]
            parent_task = task_map.get(parent_title)
            if not parent_task:
                raise PopulationError(
                    f"Task '{task_title}' is subtask of '{parent_title}', but '{parent_title}' not found in tasks"
                )

            try:
                # Create subtask relation: task is subtask of parent_task
                relation = client.task_relations.create(
                    task_id=task.id,
                    relation_kind="subtask",
                    other_task_id=parent_task.id
                )
                result["relations"].append(relation)
            except Exception as e:
                # Ignore if relation already exists
                if "already exists" not in str(e).lower():
                    raise PopulationError(
                        f"Failed to create subtask relation '{task_title}' → '{parent_title}': {e}"
                    )

    # Step 6: Assign tasks to buckets
    for task_data in schema.get("tasks", []):
        if "bucket" in task_data:
            task_title = task_data["title"]
            bucket_name = task_data["bucket"]
            bucket = bucket_map.get(bucket_name)

            if not bucket:
                raise PopulationError(
                    f"Task '{task_title}' assigned to bucket '{bucket_name}', but bucket not found. "
                    f"Available buckets: {list(bucket_map.keys())}"
                )

            task = task_map[task_title]

            try:
                # Update task's bucket_id
                client.tasks.update(task_id=task.id, bucket_id=bucket.id)
            except Exception as e:
                raise PopulationError(
                    f"Failed to assign task '{task_title}' to bucket '{bucket_name}': {e}"
                )

    # Step 7: Assign users to tasks
    for task_data in schema.get("tasks", []):
        if "assignees" in task_data:
            task_title = task_data["title"]
            task = task_map[task_title]

            for assignee in task_data["assignees"]:
                try:
                    # Note: This requires user lookup by email/username
                    # For now, we'll assume assignee is a user ID
                    # TODO: Implement user lookup by email/username
                    # user = client.users.find(assignee)
                    # client.tasks.assign_user(task.id, user.id)

                    # Placeholder: Skip assignee assignment for now
                    # This will be implemented when user lookup API is available
                    pass
                except Exception as e:
                    raise PopulationError(
                        f"Failed to assign user '{assignee}' to task '{task_title}': {e}"
                    )

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
