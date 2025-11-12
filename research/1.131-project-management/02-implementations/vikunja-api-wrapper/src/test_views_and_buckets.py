"""
TDD Test Suite for Views and Buckets API

Tests the correct View-based bucket API endpoints discovered through research:
- GET /api/v1/projects/{id}/views - List views
- GET /api/v1/projects/{id}/views/{view_id}/buckets - List buckets in view
- PUT /api/v1/projects/{id}/views/{view_id}/buckets - Create bucket in view
- POST /api/v1/projects/{id}/views/{view_id}/buckets/{bucket_id} - Update bucket
- DELETE /api/v1/projects/{id}/views/{view_id}/buckets/{bucket_id} - Delete bucket

Research findings:
- Vikunja auto-creates 4 views when project is created (List, Gantt, Table, Kanban)
- Buckets belong to views, not directly to projects
- Old endpoint /api/v1/projects/{id}/buckets returns 404
- New endpoint /api/v1/projects/{id}/views/{view_id}/buckets works
"""

import pytest
from vikunja_wrapper import VikunjaClient


class TestViewsList:
    """Test listing views for a project."""

    def test_list_views_for_new_project(self, vikunja_client, test_project):
        """Test that new projects have 4 default views."""
        views = vikunja_client.views.list(project_id=test_project.id)

        assert isinstance(views, list)
        assert len(views) == 4  # Vikunja creates 4 default views

        # Verify all view types are present
        view_kinds = {v.view_kind for v in views}
        assert 'list' in view_kinds
        assert 'gantt' in view_kinds
        assert 'table' in view_kinds
        assert 'kanban' in view_kinds

    def test_get_kanban_view(self, vikunja_client, test_project):
        """Test getting the Kanban view specifically."""
        views = vikunja_client.views.list(project_id=test_project.id)
        kanban_views = [v for v in views if v.view_kind == 'kanban']

        assert len(kanban_views) == 1
        kanban = kanban_views[0]
        assert kanban.id > 0
        assert kanban.title == "Kanban"
        assert kanban.project_id == test_project.id


class TestBucketsInView:
    """Test bucket operations within a view."""

    def test_create_bucket_in_kanban_view(self, vikunja_client, test_project):
        """Test creating a bucket in the Kanban view."""
        # Get Kanban view
        views = vikunja_client.views.list(project_id=test_project.id)
        kanban = [v for v in views if v.view_kind == 'kanban'][0]

        # Create bucket
        bucket = vikunja_client.buckets.create(
            project_id=test_project.id,
            view_id=kanban.id,
            title="Backlog",
            position=1
        )

        assert bucket.id > 0
        assert bucket.title == "Backlog"
        assert bucket.position == 1
        assert bucket.limit == 0

    def test_list_buckets_in_kanban_view(self, vikunja_client, test_project):
        """Test listing buckets in a Kanban view."""
        # Get Kanban view
        views = vikunja_client.views.list(project_id=test_project.id)
        kanban = [v for v in views if v.view_kind == 'kanban'][0]

        # Create a few buckets
        vikunja_client.buckets.create(test_project.id, kanban.id, "To Do", position=1)
        vikunja_client.buckets.create(test_project.id, kanban.id, "Doing", position=2)
        vikunja_client.buckets.create(test_project.id, kanban.id, "Done", position=3)

        # List buckets
        buckets = vikunja_client.buckets.list(project_id=test_project.id, view_id=kanban.id)

        assert len(buckets) >= 3
        bucket_titles = {b.title for b in buckets}
        assert "To Do" in bucket_titles
        assert "Doing" in bucket_titles
        assert "Done" in bucket_titles

    def test_update_bucket(self, vikunja_client, test_project):
        """Test updating a bucket's properties."""
        # Get Kanban view and create bucket
        views = vikunja_client.views.list(project_id=test_project.id)
        kanban = [v for v in views if v.view_kind == 'kanban'][0]

        bucket = vikunja_client.buckets.create(
            test_project.id, kanban.id, "In Progress", position=1, limit=0
        )

        # Update bucket
        updated = vikunja_client.buckets.update(
            project_id=test_project.id,
            view_id=kanban.id,
            bucket_id=bucket.id,
            title="Active Work",
            limit=3
        )

        assert updated.id == bucket.id
        assert updated.title == "Active Work"
        assert updated.limit == 3

    def test_delete_bucket(self, vikunja_client, test_project):
        """Test deleting a bucket."""
        # Get Kanban view and create bucket
        views = vikunja_client.views.list(project_id=test_project.id)
        kanban = [v for v in views if v.view_kind == 'kanban'][0]

        bucket = vikunja_client.buckets.create(
            test_project.id, kanban.id, "To Delete", position=1
        )

        # Delete bucket
        vikunja_client.buckets.delete(
            project_id=test_project.id,
            view_id=kanban.id,
            bucket_id=bucket.id
        )

        # Verify it's gone
        buckets = vikunja_client.buckets.list(test_project.id, kanban.id)
        bucket_ids = {b.id for b in buckets}
        assert bucket.id not in bucket_ids


class TestBulkBucketCreation:
    """Test creating multiple buckets at once (helper function)."""

    def test_create_standard_kanban_buckets(self, vikunja_client, test_project):
        """Test helper function to create standard Kanban buckets."""
        # This will be the reusable script functionality
        buckets_config = [
            {"title": "Backlog", "position": 1, "limit": 0},
            {"title": "To Do", "position": 2, "limit": 5},
            {"title": "In Progress", "position": 3, "limit": 3},
            {"title": "Done", "position": 4, "limit": 0},
        ]

        # Get Kanban view
        views = vikunja_client.views.list(project_id=test_project.id)
        kanban = [v for v in views if v.view_kind == 'kanban'][0]

        # Create all buckets
        created_buckets = []
        for config in buckets_config:
            bucket = vikunja_client.buckets.create(
                project_id=test_project.id,
                view_id=kanban.id,
                **config
            )
            created_buckets.append(bucket)

        assert len(created_buckets) == 4
        assert created_buckets[0].title == "Backlog"
        assert created_buckets[2].limit == 3  # In Progress has WIP limit
