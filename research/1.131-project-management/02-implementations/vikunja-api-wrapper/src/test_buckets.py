"""
Test suite for Buckets Manager (Method 4 - Validated TDD).

Tests run against REAL Vikunja API to validate actual behavior.

Buckets represent Kanban columns/boards in Vikunja.

API Endpoints:
- GET /projects/{id}/buckets - List all buckets
- PUT /projects/{id}/buckets - Create bucket
- POST /projects/{id}/buckets/{bucketId} - Update bucket
- DELETE /projects/{id}/buckets/{bucketId} - Delete bucket
"""

import pytest
from vikunja_wrapper import VikunjaClient


class TestBucketsCreate:
    """Test creating buckets."""

    def test_create_bucket(self, vikunja_client, test_project):
        """Test creating a basic bucket."""
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Backlog",
            position=0
        )

        # Assertions
        assert bucket.id > 0
        assert bucket.title == "Backlog"
        assert bucket.project_id == test_project.id
        assert bucket.position == 0
        assert bucket.limit == 0  # Default: no limit
        assert bucket.created_at is not None

    def test_create_bucket_with_limit(self, vikunja_client, test_project):
        """Test creating a bucket with WIP limit."""
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="In Progress",
            position=1,
            limit=5  # WIP limit
        )

        assert bucket.title == "In Progress"
        assert bucket.position == 1
        assert bucket.limit == 5

    def test_create_multiple_buckets(self, vikunja_client, test_project):
        """Test creating multiple buckets (typical Kanban board)."""
        # Create standard Kanban buckets
        backlog = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Backlog",
            position=0
        )

        in_progress = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="In Progress",
            position=1,
            limit=3
        )

        done = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Done",
            position=2
        )

        # Assertions
        assert backlog.position == 0
        assert in_progress.position == 1
        assert done.position == 2
        assert in_progress.limit == 3


class TestBucketsList:
    """Test listing buckets."""

    def test_list_buckets_empty(self, vikunja_client, test_project):
        """Test listing buckets for a new project (may have default bucket)."""
        buckets = vikunja_client.buckets.list(project_id=test_project.id)

        assert isinstance(buckets, list)
        # Vikunja may create a default bucket, so we just check it's a list

    def test_list_buckets_multiple(self, vikunja_client, test_project):
        """Test listing multiple buckets."""
        # Create buckets
        vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Todo",
            position=0
        )

        vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Doing",
            position=1
        )

        vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Done",
            position=2
        )

        # List buckets
        buckets = vikunja_client.buckets.list(project_id=test_project.id)

        # Should have at least the 3 we created (may have default bucket)
        assert len(buckets) >= 3

        # Verify our buckets are in the list
        bucket_titles = {b.title for b in buckets}
        assert "Todo" in bucket_titles
        assert "Doing" in bucket_titles
        assert "Done" in bucket_titles


class TestBucketsUpdate:
    """Test updating buckets."""

    def test_update_bucket_title(self, vikunja_client, test_project):
        """Test updating bucket title."""
        # Create bucket
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Original Title",
            position=0
        )

        # Update title
        updated = vikunja_client.buckets.update(
            project_id=test_project.id,
            bucket_id=bucket.id,
            title="New Title"
        )

        assert updated.id == bucket.id
        assert updated.title == "New Title"
        assert updated.position == 0  # Should remain unchanged

    def test_update_bucket_position(self, vikunja_client, test_project):
        """Test updating bucket position."""
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Bucket",
            position=0
        )

        # Move bucket to position 5
        updated = vikunja_client.buckets.update(
            project_id=test_project.id,
            bucket_id=bucket.id,
            position=5
        )

        assert updated.position == 5

    def test_update_bucket_limit(self, vikunja_client, test_project):
        """Test updating WIP limit."""
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="In Progress",
            position=0,
            limit=0
        )

        # Set WIP limit
        updated = vikunja_client.buckets.update(
            project_id=test_project.id,
            bucket_id=bucket.id,
            limit=3
        )

        assert updated.limit == 3


class TestBucketsDelete:
    """Test deleting buckets."""

    def test_delete_bucket(self, vikunja_client, test_project):
        """Test deleting a bucket."""
        # Create bucket
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="To Delete",
            position=0
        )

        # Delete bucket
        vikunja_client.buckets.delete(
            project_id=test_project.id,
            bucket_id=bucket.id
        )

        # Verify bucket is removed
        buckets = vikunja_client.buckets.list(project_id=test_project.id)
        bucket_ids = {b.id for b in buckets}
        assert bucket.id not in bucket_ids


class TestTaskBucketAssignment:
    """Test assigning tasks to buckets."""

    def test_move_task_to_bucket(self, vikunja_client, test_project):
        """Test moving a task to a specific bucket."""
        # Create buckets
        backlog = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Backlog",
            position=0
        )

        in_progress = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="In Progress",
            position=1
        )

        # Create task
        task = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Test Task"
        )

        # Move task to "In Progress" bucket
        updated_task = vikunja_client.tasks.update(
            task_id=task.id,
            bucket_id=in_progress.id
        )

        # Verify task is in correct bucket
        assert updated_task.bucket_id == in_progress.id

    def test_create_task_in_specific_bucket(self, vikunja_client, test_project):
        """Test creating a task directly in a specific bucket."""
        # Create bucket
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            title="Backlog",
            position=0
        )

        # Create task in bucket (may need to be done via update after creation)
        task = vikunja_client.tasks.create(
            project_id=test_project.id,
            title="Task in Bucket"
        )

        # Move to bucket
        task = vikunja_client.tasks.update(
            task_id=task.id,
            bucket_id=bucket.id
        )

        # Verify
        assert task.bucket_id == bucket.id


class TestBucketsValidation:
    """Test validation and error handling."""

    def test_delete_nonexistent_bucket(self, vikunja_client, test_project):
        """Test deleting a bucket that doesn't exist."""
        with pytest.raises(Exception):  # Should raise NotFoundError
            vikunja_client.buckets.delete(
                project_id=test_project.id,
                bucket_id=99999
            )

    def test_update_nonexistent_bucket(self, vikunja_client, test_project):
        """Test updating a bucket that doesn't exist."""
        with pytest.raises(Exception):  # Should raise NotFoundError
            vikunja_client.buckets.update(
                project_id=test_project.id,
                bucket_id=99999,
                title="New Title"
            )
