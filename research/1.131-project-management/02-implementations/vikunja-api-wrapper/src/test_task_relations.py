"""
Test suite for Task Relations Manager (Method 4 - Validated TDD).

Tests run against REAL Vikunja API to validate actual behavior.

Relation kinds supported:
- subtask / parenttask
- blocking / blocked
- related
- duplicateof / duplicates
- precedes / follows
- copiedfrom / copiedto

API: PUT /tasks/{taskID}/relations/{relationKind}/{otherTaskID}
"""

import pytest
from vikunja_wrapper import VikunjaClient


class TestTaskRelationsCreate:
    """Test creating task relations."""

    def test_create_subtask_relation(self, vikunja_client, test_project):
        """Test creating a subtask relation (child → parent)."""
        # Create parent task
        parent = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Parent Task"
        )

        # Create child task
        child = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Child Task"
        )

        # Create subtask relation: child is subtask of parent
        relation = vikunja_client.task_relations.create(
            task_id=child.id,
            relation_kind="subtask",
            other_task_id=parent.id
        )

        # Assertions
        assert relation.task_id == child.id
        assert relation.other_task_id == parent.id
        assert relation.relation_kind == "subtask"
        assert relation.created_at is not None

    def test_create_blocking_relation(self, vikunja_client, test_project):
        """Test creating a blocking relation (A blocks B)."""
        # Create task A (blocker)
        task_a = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task A (Blocker)"
        )

        # Create task B (blocked)
        task_b = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task B (Blocked)"
        )

        # Create blocking relation: A blocks B
        relation = vikunja_client.task_relations.create(
            task_id=task_a.id,
            relation_kind="blocking",
            other_task_id=task_b.id
        )

        # Assertions
        assert relation.task_id == task_a.id
        assert relation.other_task_id == task_b.id
        assert relation.relation_kind == "blocking"

    def test_create_related_relation(self, vikunja_client, test_project):
        """Test creating a related relation (bidirectional)."""
        task_1 = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task 1"
        )

        task_2 = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task 2"
        )

        # Create related relation
        relation = vikunja_client.task_relations.create(
            task_id=task_1.id,
            relation_kind="related",
            other_task_id=task_2.id
        )

        # Assertions
        assert relation.task_id == task_1.id
        assert relation.other_task_id == task_2.id
        assert relation.relation_kind == "related"

    def test_create_precedes_relation(self, vikunja_client, test_project):
        """Test creating a precedes relation (A must finish before B starts)."""
        task_a = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="First Task"
        )

        task_b = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Second Task"
        )

        # Create precedes relation: A precedes B
        relation = vikunja_client.task_relations.create(
            task_id=task_a.id,
            relation_kind="precedes",
            other_task_id=task_b.id
        )

        assert relation.relation_kind == "precedes"


class TestTaskRelationsDelete:
    """Test deleting task relations."""

    def test_delete_relation(self, vikunja_client, test_project):
        """Test deleting a task relation."""
        # Create two tasks
        task_1 = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task 1"
        )

        task_2 = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task 2"
        )

        # Create relation
        vikunja_client.task_relations.create(
            task_id=task_1.id,
            relation_kind="blocking",
            other_task_id=task_2.id
        )

        # Delete relation
        vikunja_client.task_relations.delete(
            task_id=task_1.id,
            relation_kind="blocking",
            other_task_id=task_2.id
        )

        # Verify relation is removed
        relations = vikunja_client.task_relations.list(task_id=task_1.id)
        blocking_relations = [r for r in relations if r.relation_kind == "blocking" and r.other_task_id == task_2.id]
        assert len(blocking_relations) == 0

    def test_delete_nonexistent_relation(self, vikunja_client, test_project):
        """Test deleting a relation that doesn't exist (should not error)."""
        # Create task
        task = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task"
        )

        # Try to delete non-existent relation (should not raise error)
        vikunja_client.task_relations.delete(
            task_id=task.id,
            relation_kind="blocking",
            other_task_id=99999
        )


class TestTaskRelationsList:
    """Test listing task relations."""

    def test_list_relations_empty(self, vikunja_client, test_project):
        """Test listing relations for a task with no relations."""
        task = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Isolated Task"
        )

        relations = vikunja_client.task_relations.list(task_id=task.id)
        assert isinstance(relations, list)
        assert len(relations) == 0

    def test_list_relations_multiple(self, vikunja_client, test_project):
        """Test listing relations for a task with multiple relations."""
        # Create main task
        main_task = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Main Task"
        )

        # Create related tasks
        task_a = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task A"
        )

        task_b = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task B"
        )

        # Create multiple relations
        vikunja_client.task_relations.create(
            task_id=main_task.id,
            relation_kind="blocking",
            other_task_id=task_a.id
        )

        vikunja_client.task_relations.create(
            task_id=main_task.id,
            relation_kind="blocking",
            other_task_id=task_b.id
        )

        # List relations
        relations = vikunja_client.task_relations.list(task_id=main_task.id)

        # Assertions
        assert len(relations) >= 2
        blocking_relations = [r for r in relations if r.relation_kind == "blocking"]
        assert len(blocking_relations) == 2

        # Verify both tasks are in relations
        other_task_ids = {r.other_task_id for r in blocking_relations}
        assert task_a.id in other_task_ids
        assert task_b.id in other_task_ids

    def test_list_relations_includes_both_directions(self, vikunja_client, test_project):
        """Test that list includes both outgoing and incoming relations."""
        task_a = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task A"
        )

        task_b = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task B"
        )

        # Create relation: A blocks B
        vikunja_client.task_relations.create(
            task_id=task_a.id,
            relation_kind="blocking",
            other_task_id=task_b.id
        )

        # List relations from task A perspective (outgoing)
        relations_a = vikunja_client.task_relations.list(task_id=task_a.id)
        blocking_from_a = [r for r in relations_a if r.relation_kind == "blocking"]
        assert len(blocking_from_a) >= 1

        # List relations from task B perspective (incoming - should show as "blocked")
        relations_b = vikunja_client.task_relations.list(task_id=task_b.id)
        blocked_from_b = [r for r in relations_b if r.relation_kind == "blocked"]
        assert len(blocked_from_b) >= 1


class TestTaskRelationsValidation:
    """Test validation and error handling."""

    def test_invalid_relation_kind(self, vikunja_client, test_project):
        """Test that invalid relation kinds are rejected."""
        task_1 = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task 1"
        )

        task_2 = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task 2"
        )

        # Try to create relation with invalid kind
        with pytest.raises(Exception):  # Should raise ValidationError or similar
            vikunja_client.task_relations.create(
                task_id=task_1.id,
                relation_kind="invalid_kind",
                other_task_id=task_2.id
            )

    def test_relation_with_nonexistent_task(self, vikunja_client, test_project):
        """Test creating relation with non-existent task."""
        task = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task"
        )

        # Try to create relation with non-existent task
        with pytest.raises(Exception):  # Should raise NotFoundError or similar
            vikunja_client.task_relations.create(
                task_id=task.id,
                relation_kind="blocking",
                other_task_id=99999
            )
