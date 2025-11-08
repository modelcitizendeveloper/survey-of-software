"""
Pytest configuration for Vikunja API tests.

For Method 4 testing, tests run against REAL Vikunja API.
Set environment variables:
- VIKUNJA_BASE_URL (default: https://app.vikunja.cloud)
- VIKUNJA_API_TOKEN (required)
"""

import pytest
import os
from vikunja_wrapper import VikunjaClient


@pytest.fixture(scope="session")
def vikunja_client():
    """
    Create a VikunjaClient for testing against real API.

    Requires VIKUNJA_API_TOKEN environment variable.
    """
    base_url = os.getenv("VIKUNJA_BASE_URL", "https://app.vikunja.cloud")
    token = os.getenv("VIKUNJA_API_TOKEN")

    if not token:
        pytest.skip("VIKUNJA_API_TOKEN environment variable not set")

    return VikunjaClient(base_url=base_url, token=token)


@pytest.fixture(scope="function")
def test_project(vikunja_client):
    """
    Create a test project for each test, clean up after.
    """
    project = vikunja_client.projects.create(
        title=f"Test Project {os.urandom(4).hex()}"
    )

    yield project

    # Cleanup
    try:
        vikunja_client.projects.delete(project.id)
    except Exception:
        pass  # Ignore cleanup errors
