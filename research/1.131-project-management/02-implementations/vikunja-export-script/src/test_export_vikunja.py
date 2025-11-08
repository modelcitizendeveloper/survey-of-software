"""
Test suite for Vikunja Export Script (Method 4: Adaptive TDD)

Critical requirements:
- Source document extraction from HTML descriptions
- Project hierarchy (parent-child relationships)
- Labels with colors
- Complete task metadata export
- JSON and Markdown formats

Test strategy:
1. Unit tests for extraction functions
2. Integration tests with mock API data
3. End-to-end test with real Applications project
"""

import pytest
from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock
from pathlib import Path
import json
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "vikunja-api-wrapper" / "src"))

from export_vikunja import (
    extract_source_documents,
    get_project_hierarchy,
    get_task_with_metadata,
    export_portfolio,
    format_spawn_analysis,
)


class TestSourceDocumentExtraction:
    """Test extraction of source document paths from task descriptions."""

    def test_extract_basic_source_docs(self):
        """Test extraction of project definition and folder."""
        description = """
        Some task description here.

        ---
        <strong>📂 Source Documents for Analysis:</strong><br>
        <ul>
        <li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml</code></li>
        <li>Project folder: <code>/home/ivanadmin/spawn-solutions/applications/qrcards/</code></li>
        </ul>
        """

        result = extract_source_documents(description)

        assert result is not None
        assert result['project_definition'] == '/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml'
        assert result['project_folder'] == '/home/ivanadmin/spawn-solutions/applications/qrcards/'
        assert 'codebase' not in result

    def test_extract_source_docs_with_codebase(self):
        """Test extraction including codebase path."""
        description = """
        ---
        <strong>📂 Source Documents for Analysis:</strong><br>
        <ul>
        <li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml</code></li>
        <li>Project folder: <code>/home/ivanadmin/spawn-solutions/applications/qrcards/</code></li>
        <li>Codebase: <code>/home/ivanadmin/qrcards/</code></li>
        </ul>
        """

        result = extract_source_documents(description)

        assert result is not None
        assert result['codebase'] == '/home/ivanadmin/qrcards/'

    def test_extract_no_source_docs(self):
        """Test handling task without source documents."""
        description = "Just a regular task description without source docs."

        result = extract_source_documents(description)

        assert result is None or result == {}

    def test_extract_source_docs_html_variations(self):
        """Test extraction works with HTML variations."""
        # Test with different HTML formatting
        description = """
        <p>Some content</p>
        <strong>📂 Source Documents for Analysis:</strong><br>
        <ul>
        <li>Project definition: <code>/path/to/file.yaml</code></li>
        </ul>
        """

        result = extract_source_documents(description)
        assert result is not None
        assert '/path/to/file.yaml' in result['project_definition']


class TestProjectHierarchy:
    """Test project hierarchy extraction."""

    def test_get_flat_hierarchy(self):
        """Test single-level project (no parent)."""
        project = Mock()
        project.id = 123
        project.title = "Applications"
        project.parent_project_id = None

        client = Mock()

        hierarchy = get_project_hierarchy(client, project)

        assert hierarchy == ["Applications"]

    def test_get_nested_hierarchy(self):
        """Test multi-level hierarchy (Applications > Products > QRCards)."""
        # Mock the project structure
        qrcards = Mock()
        qrcards.id = 13472
        qrcards.title = "QRCards"
        qrcards.parent_project_id = 13585

        products = Mock()
        products.id = 13585
        products.title = "Products"
        products.parent_project_id = 13448

        applications = Mock()
        applications.id = 13448
        applications.title = "Applications"
        applications.parent_project_id = None

        client = Mock()
        client.projects.get.side_effect = lambda id: {
            13585: products,
            13448: applications,
        }.get(id)

        hierarchy = get_project_hierarchy(client, qrcards)

        assert hierarchy == ["Applications", "Products", "QRCards"]

    def test_hierarchy_handles_missing_parent(self):
        """Test graceful handling if parent project not found."""
        project = Mock()
        project.id = 123
        project.title = "Orphan Project"
        project.parent_project_id = 999  # Non-existent

        client = Mock()
        client.projects.get.side_effect = Exception("Not found")

        hierarchy = get_project_hierarchy(client, project)

        # Should return at least the project itself
        assert "Orphan Project" in hierarchy


class TestTaskMetadataExtraction:
    """Test extraction of complete task metadata."""

    def test_get_task_with_all_metadata(self):
        """Test extraction of task with labels, priority, dates, etc."""
        task = Mock()
        task.id = 217411
        task.title = "QRCards"
        task.description = """
        Platform description

        ---
        <strong>📂 Source Documents for Analysis:</strong><br>
        <ul>
        <li>Project definition: <code>/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml</code></li>
        </ul>
        """
        task.project_id = 13448
        task.done = False
        task.priority = 5
        task.due_date = "2025-12-01T00:00:00Z"
        task.created = "2025-11-01T00:00:00Z"
        task.bucket_id = 123

        # Mock labels
        label1 = Mock()
        label1.id = 1
        label1.title = "High Priority"
        label1.hex_color = "#ff0000"
        label1.description = "Critical work"

        label2 = Mock()
        label2.id = 2
        label2.title = "Product"
        label2.hex_color = "#00ff00"
        label2.description = None

        task.labels = [label1, label2]

        project = Mock()
        project.id = 13448
        project.title = "Applications"
        project.parent_project_id = None

        client = Mock()
        client.projects.get.return_value = project

        result = get_task_with_metadata(client, task)

        # Check all metadata is present
        assert result['id'] == 217411
        assert result['title'] == "QRCards"
        assert result['project_id'] == 13448
        assert result['project_hierarchy'] == ["Applications"]
        assert result['done'] == False
        assert result['priority'] == 5
        assert result['due_date'] == "2025-12-01T00:00:00Z"
        assert result['bucket_id'] == 123

        # Check labels
        assert len(result['labels']) == 2
        assert result['labels'][0]['title'] == "High Priority"
        assert result['labels'][0]['color'] == "#ff0000"
        assert result['labels'][0]['description'] == "Critical work"

        # Check source documents
        assert result['source_documents'] is not None
        assert 'qrcards/vikunja-tasks.yaml' in result['source_documents']['project_definition']

    def test_get_task_minimal_metadata(self):
        """Test task with minimal metadata (no labels, no dates)."""
        task = Mock()
        task.id = 123
        task.title = "Simple Task"
        task.description = "No extra metadata"
        task.project_id = 456
        task.done = False
        task.priority = 0
        task.due_date = None
        task.labels = []
        task.bucket_id = None

        project = Mock()
        project.id = 456
        project.title = "Project"
        project.parent_project_id = None

        client = Mock()
        client.projects.get.return_value = project

        result = get_task_with_metadata(client, task)

        assert result['id'] == 123
        assert result['labels'] == []
        assert result['source_documents'] is None or result['source_documents'] == {}


class TestJSONExport:
    """Test JSON export format."""

    def test_json_export_structure(self):
        """Test JSON export has all required fields."""
        # This will be an integration test with mocked client
        client = Mock()

        # Mock projects list
        project = Mock()
        project.id = 13448
        project.title = "Applications"
        project.description = "Portfolio of applications"
        project.parent_project_id = None
        project.created = datetime.now(timezone.utc).isoformat()

        client.projects.list.return_value = [project]

        # Mock tasks
        task = Mock()
        task.id = 217411
        task.title = "QRCards"
        task.description = "Platform"
        task.project_id = 13448
        task.done = False
        task.priority = 5
        task.labels = []
        task.due_date = None
        task.done_at = None

        client.tasks.list.return_value = [task]
        client.projects.get.return_value = project

        result = export_portfolio(client)

        # Check top-level structure
        assert 'exported_at' in result
        assert 'projects' in result
        assert 'summary' in result

        # Check project structure
        assert len(result['projects']) == 1
        proj = result['projects'][0]
        assert 'id' in proj
        assert 'title' in proj
        assert 'hierarchy' in proj
        assert 'tasks' in proj

        # Check task structure
        assert len(proj['tasks']) == 1
        task_data = proj['tasks'][0]
        assert 'id' in task_data
        assert 'title' in task_data
        assert 'labels' in task_data
        assert 'source_documents' in task_data


class TestMarkdownExport:
    """Test Markdown export format for spawn-analysis."""

    def test_markdown_includes_source_documents(self):
        """Test markdown output includes source document section."""
        portfolio = {
            'exported_at': '2025-11-08T00:00:00Z',
            'summary': {
                'total_projects': 1,
                'total_tasks': 1,
                'total_done': 0,
                'total_pending': 1,
                'total_overdue': 0,
            },
            'projects': [
                {
                    'id': 13448,
                    'title': 'Applications',
                    'hierarchy': ['Applications'],
                    'tasks': [
                        {
                            'id': 217411,
                            'title': 'QRCards',
                            'source_documents': {
                                'project_definition': '/home/ivanadmin/spawn-solutions/applications/qrcards/vikunja-tasks.yaml',
                                'project_folder': '/home/ivanadmin/spawn-solutions/applications/qrcards/',
                                'codebase': '/home/ivanadmin/qrcards/',
                            },
                            'labels': [
                                {'title': 'Product', 'color': '#00ff00'}
                            ]
                        }
                    ]
                }
            ]
        }

        output = format_spawn_analysis(portfolio)

        # Check source documents are included
        assert 'Source Documents' in output or 'Evidence' in output
        assert '/home/ivanadmin/spawn-solutions/applications/qrcards/' in output
        assert '/home/ivanadmin/qrcards/' in output

        # Check labels are shown
        assert 'Product' in output

    def test_markdown_shows_hierarchy(self):
        """Test markdown displays project hierarchy."""
        portfolio = {
            'exported_at': '2025-11-08T00:00:00Z',
            'summary': {
                'total_projects': 1,
                'total_tasks': 1,
                'total_done': 0,
                'total_pending': 1,
                'total_overdue': 0,
            },
            'projects': [
                {
                    'id': 13472,
                    'title': 'QRCards',
                    'hierarchy': ['Applications', 'Products', 'QRCards'],
                    'tasks': []
                }
            ]
        }

        output = format_spawn_analysis(portfolio)

        # Check hierarchy is shown
        assert 'Applications' in output
        assert 'Products' in output
        assert 'QRCards' in output


class TestIntegrationWithApplicationsProject:
    """Integration tests with real Applications project (ID: 13448)."""

    @pytest.mark.integration
    def test_export_applications_project_real(self):
        """
        Test export with real Applications project.

        This test requires:
        - Vikunja API access
        - Applications project (ID: 13448) with tasks
        - Source documents already added to tasks
        """
        import os
        from pathlib import Path
        from dotenv import load_dotenv
        from vikunja_wrapper import VikunjaClient

        # Load environment
        env_path = Path(__file__).parent.parent.parent.parent.parent.parent / '.env'
        load_dotenv(env_path)

        api_token = os.environ.get("VIKUNJA_API_TOKEN")
        if not api_token:
            pytest.skip("VIKUNJA_API_TOKEN not found, skipping integration test")

        client = VikunjaClient(
            base_url="https://app.vikunja.cloud",
            token=api_token
        )

        # Export just Applications project
        project = client.projects.get(13448)
        tasks = client.tasks.list(project_id=13448)

        # Test that we can extract source documents from real tasks
        tasks_with_sources = [
            task for task in tasks
            if task.description and 'Source Documents' in (task.description or '')
        ]

        assert len(tasks_with_sources) >= 10, "Expected at least 10 tasks with source documents"

        # Test extraction from one real task
        for task in tasks_with_sources[:3]:  # Test first 3
            source_docs = extract_source_documents(task.description)
            assert source_docs is not None
            assert 'project_definition' in source_docs or 'project_folder' in source_docs
