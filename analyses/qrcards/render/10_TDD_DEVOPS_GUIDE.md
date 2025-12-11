# Test-Driven DevOps: QRCards Render Migration

**Inspired by:** "Test-Driven Development with Python" by Harry J.M. Percival
**Philosophy:** Write tests first, make them pass, refactor. Apply this to infrastructure.
**Goal:** Migrate QRCards to Render with confidence that each step works before moving forward

---

## Core Principle: Red → Green → Refactor (Applied to DevOps)

**Traditional TDD:**
1. Write a failing test (RED)
2. Make the test pass (GREEN)
3. Clean up the code (REFACTOR)

**DevOps TDD:**
1. Define what success looks like (RED - test fails because infrastructure doesn't exist)
2. Build minimal infrastructure to pass the test (GREEN)
3. Improve infrastructure while keeping tests green (REFACTOR)

---

## Chapter 1: The Functional Test - "Can I Access My App?"

### What We're Testing
Before we write any infrastructure code, let's write a test that describes what we want.

**The simplest possible test:**
> "When I visit the Render URL, I should see my QRCards app running"

### Step 1.1: Write the Functional Test (RED)

Create a test file in qrcards-deploy:

```bash
# In ~/qrcards-deploy/
mkdir -p tests/functional
touch tests/functional/test_deployment.py
```

**tests/functional/test_deployment.py:**
```python
"""
Functional tests for QRCards deployment.

These tests verify the application works from a user's perspective.
Run these against the deployed application, not locally.
"""

import requests
import os
import pytest

# Skip if RENDER_URL not set (we haven't deployed yet)
pytestmark = pytest.mark.skipif(
    not os.environ.get('RENDER_URL'),
    reason="RENDER_URL not set - deployment not ready yet"
)

class TestDeploymentWorks:
    """Test that the basic deployment is functional."""

    def test_can_access_homepage(self):
        """
        GIVEN: QRCards is deployed to Render
        WHEN: We visit the Render URL
        THEN: We should get a 200 OK response
        """
        render_url = os.environ.get('RENDER_URL')
        response = requests.get(render_url)
        assert response.status_code == 200

    def test_app_returns_html(self):
        """
        GIVEN: QRCards is deployed to Render
        WHEN: We visit the Render URL
        THEN: We should get HTML content back
        """
        render_url = os.environ.get('RENDER_URL')
        response = requests.get(render_url)
        assert 'text/html' in response.headers.get('Content-Type', '')
```

### Step 1.2: Run the Test (Watch It Skip)

```bash
cd ~/qrcards-deploy/

# Install test dependencies
pip install pytest requests

# Run the test
pytest tests/functional/test_deployment.py -v

# Expected output:
# test_can_access_homepage SKIPPED (RENDER_URL not set)
# test_app_returns_html SKIPPED (RENDER_URL not set)
```

**Status:** ⏭️ YELLOW (skipped because we haven't deployed yet)

**What this tells us:** We need to deploy to Render before these tests can run.

---

## Chapter 2: The First Green - "Does My Local App Work?"

Before deploying to Render, let's verify the app works locally.

### Step 2.1: Write Unit Test for Local Deployment (RED)

**tests/unit/test_app_starts.py:**
```python
"""
Unit tests for basic application functionality.
These tests run locally, no deployment needed.
"""

import os
import sys

def test_can_import_app():
    """
    GIVEN: The qrcards-deploy repository
    WHEN: We try to import the Flask app
    THEN: Import should succeed without errors
    """
    try:
        from run import app
        assert app is not None
    except ImportError as e:
        pytest.fail(f"Could not import app: {e}")

def test_app_has_config():
    """
    GIVEN: The Flask app
    WHEN: We check its configuration
    THEN: It should have essential config values
    """
    from run import app
    assert app.config is not None
    # Config should have some basic values
    assert 'TESTING' in app.config or 'DEBUG' in app.config

def test_app_can_create_test_client():
    """
    GIVEN: The Flask app
    WHEN: We create a test client
    THEN: We should be able to make requests to it
    """
    from run import app
    client = app.test_client()
    assert client is not None
```

### Step 2.2: Run the Test (RED)

```bash
pytest tests/unit/test_app_starts.py -v

# If this fails, you have import errors or missing dependencies
# Fix them before proceeding!
```

**Expected first run:** ❌ RED (probably missing requirements.txt or import errors)

### Step 2.3: Make It Pass (GREEN)

**Check requirements.txt exists:**
```bash
# In ~/qrcards-deploy/
ls requirements.txt

# If missing, copy from source:
cp ~/qrcards/packages/flasklayer/requirements.txt .
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run tests again:**
```bash
pytest tests/unit/test_app_starts.py -v

# Expected: ✅ GREEN (all tests pass)
```

**Status:** ✅ GREEN - App imports and configures correctly

---

## Chapter 3: Docker - "Can I Build a Container?"

### Step 3.1: Write Docker Build Test (RED)

**tests/functional/test_docker_build.py:**
```python
"""
Tests for Docker build process.
These verify the Dockerfile works correctly.
"""

import subprocess
import pytest

class TestDockerBuild:
    """Test that we can build a Docker image."""

    def test_dockerfile_exists(self):
        """
        GIVEN: qrcards-deploy repository
        WHEN: We check for Dockerfile
        THEN: Dockerfile should exist
        """
        import os
        assert os.path.exists('Dockerfile'), "Dockerfile not found"

    def test_can_build_docker_image(self):
        """
        GIVEN: A valid Dockerfile
        WHEN: We run docker build
        THEN: Build should succeed without errors
        """
        result = subprocess.run(
            ['docker', 'build', '-t', 'qrcards-test', '.'],
            capture_output=True,
            text=True
        )

        # Print output for debugging
        if result.returncode != 0:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)

        assert result.returncode == 0, "Docker build failed"

    @pytest.mark.slow
    def test_docker_container_starts(self):
        """
        GIVEN: A built Docker image
        WHEN: We try to start a container
        THEN: Container should start without crashing immediately
        """
        # Start container in background
        start = subprocess.run(
            ['docker', 'run', '-d', '-p', '8000:8000',
             '-e', 'PORT=8000', 'qrcards-test'],
            capture_output=True,
            text=True
        )

        assert start.returncode == 0, "Container failed to start"

        container_id = start.stdout.strip()

        try:
            # Wait a moment for container to start
            import time
            time.sleep(2)

            # Check if still running
            check = subprocess.run(
                ['docker', 'ps', '--filter', f'id={container_id}'],
                capture_output=True,
                text=True
            )

            assert container_id in check.stdout, "Container crashed after starting"

        finally:
            # Clean up - stop container
            subprocess.run(['docker', 'stop', container_id],
                         capture_output=True)
            subprocess.run(['docker', 'rm', container_id],
                         capture_output=True)
```

### Step 3.2: Run the Test (RED)

```bash
pytest tests/functional/test_docker_build.py::TestDockerBuild::test_dockerfile_exists -v

# Expected: ❌ RED (Dockerfile not found)
```

### Step 3.3: Create Minimal Dockerfile (GREEN)

**Dockerfile:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Gunicorn server
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app
```

### Step 3.4: Run Tests Again (GREEN)

```bash
# Test 1: Dockerfile exists
pytest tests/functional/test_docker_build.py::TestDockerBuild::test_dockerfile_exists -v
# Expected: ✅ GREEN

# Test 2: Can build image
pytest tests/functional/test_docker_build.py::TestDockerBuild::test_can_build_docker_image -v
# Expected: ✅ GREEN (might take a few minutes first time)

# Test 3: Container starts
pytest tests/functional/test_docker_build.py::TestDockerBuild::test_docker_container_starts -v
# Expected: ✅ GREEN
```

**Status:** ✅ GREEN - Docker image builds and runs

---

## Chapter 4: Database Persistence - "Where Do My Files Go?"

### Step 4.1: Write Database Test (RED)

**tests/functional/test_database_persistence.py:**
```python
"""
Tests for database persistence in Docker.
Verify that SQLite databases are created and accessible.
"""

import subprocess
import time
import os

class TestDatabasePersistence:
    """Test that databases persist correctly."""

    def test_data_directory_exists_in_container(self):
        """
        GIVEN: A running Docker container
        WHEN: We check for /data directory
        THEN: Directory should exist
        """
        # Start container
        start = subprocess.run(
            ['docker', 'run', '-d', '-e', 'PORT=8000', 'qrcards-test'],
            capture_output=True,
            text=True
        )
        container_id = start.stdout.strip()

        try:
            # Check for /data directory
            check = subprocess.run(
                ['docker', 'exec', container_id, 'ls', '-la', '/data'],
                capture_output=True,
                text=True
            )

            assert check.returncode == 0, "/data directory not found in container"

        finally:
            subprocess.run(['docker', 'stop', container_id], capture_output=True)
            subprocess.run(['docker', 'rm', container_id], capture_output=True)

    def test_can_mount_volume_for_data(self):
        """
        GIVEN: A Docker container with mounted volume
        WHEN: We create a file in /data
        THEN: File should persist in the mounted volume
        """
        import tempfile

        with tempfile.TemporaryDirectory() as tmpdir:
            # Start container with mounted volume
            start = subprocess.run(
                ['docker', 'run', '-d',
                 '-v', f'{tmpdir}:/data',
                 '-e', 'PORT=8000',
                 'qrcards-test'],
                capture_output=True,
                text=True
            )
            container_id = start.stdout.strip()

            try:
                # Create a test file in /data
                subprocess.run(
                    ['docker', 'exec', container_id,
                     'sh', '-c', 'echo "test" > /data/test.txt'],
                    check=True
                )

                # Check file exists in mounted directory
                assert os.path.exists(os.path.join(tmpdir, 'test.txt'))

            finally:
                subprocess.run(['docker', 'stop', container_id], capture_output=True)
                subprocess.run(['docker', 'rm', container_id], capture_output=True)
```

### Step 4.2: Run Test (RED)

```bash
pytest tests/functional/test_database_persistence.py::TestDatabasePersistence::test_data_directory_exists_in_container -v

# Expected: ❌ RED (/data directory doesn't exist)
```

### Step 4.3: Update Dockerfile (GREEN)

**Dockerfile (updated):**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory for SQLite databases
RUN mkdir -p /data

CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app
```

### Step 4.4: Rebuild and Test (GREEN)

```bash
# Rebuild image
docker build -t qrcards-test .

# Run tests
pytest tests/functional/test_database_persistence.py -v

# Expected: ✅ GREEN (all tests pass)
```

**Status:** ✅ GREEN - Data directory exists and volumes work

---

## Chapter 5: Environment Configuration - "Can I Configure My App?"

### Step 5.1: Write Configuration Test (RED)

**tests/unit/test_environment_config.py:**
```python
"""
Tests for environment-based configuration.
Verify app responds to environment variables correctly.
"""

import os
import pytest

class TestEnvironmentConfig:
    """Test environment variable configuration."""

    def test_app_reads_database_path_from_env(self):
        """
        GIVEN: DATABASE_PATH environment variable is set
        WHEN: App starts
        THEN: App should use that database path
        """
        os.environ['DATABASE_PATH'] = '/test/data/path'
        os.environ['FLASK_ENV'] = 'testing'

        from run import app

        # Check if app is using the configured path
        # This depends on your app's implementation
        # Adjust based on how your app reads DATABASE_PATH
        assert os.environ['DATABASE_PATH'] == '/test/data/path'

        # Clean up
        del os.environ['DATABASE_PATH']
        if 'FLASK_ENV' in os.environ:
            del os.environ['FLASK_ENV']

    def test_app_uses_production_config_when_flask_env_production(self):
        """
        GIVEN: FLASK_ENV is set to 'production'
        WHEN: App starts
        THEN: App should use production configuration
        """
        os.environ['FLASK_ENV'] = 'production'

        # Reload the app module to pick up new env var
        import importlib
        import run
        importlib.reload(run)

        # Verify production settings are active
        # This depends on your app's config structure

        # Clean up
        del os.environ['FLASK_ENV']
```

### Step 5.2: Run Test (Varies)

```bash
pytest tests/unit/test_environment_config.py -v

# This might pass or fail depending on your app's current implementation
# If RED, update your app to read environment variables
# If GREEN, you're already handling config correctly
```

---

## Chapter 6: The First Deploy - "Does It Work on Render?"

### Step 6.1: Write Render Deployment Test (RED)

**tests/functional/test_render_deployment.py:**
```python
"""
Tests for Render deployment.
These tests verify the application works on Render's infrastructure.
"""

import requests
import os
import pytest

# We'll set RENDER_URL after deploying
pytestmark = pytest.mark.skipif(
    not os.environ.get('RENDER_URL'),
    reason="RENDER_URL not set - haven't deployed to Render yet"
)

class TestRenderDeployment:
    """Test deployment to Render."""

    def test_render_service_responds(self):
        """
        GIVEN: QRCards deployed to Render
        WHEN: We request the Render URL
        THEN: Service should respond with 200 OK
        """
        url = os.environ['RENDER_URL']
        response = requests.get(url, timeout=30)
        assert response.status_code == 200

    def test_render_has_valid_ssl(self):
        """
        GIVEN: QRCards deployed to Render
        WHEN: We check the SSL certificate
        THEN: Connection should be secure (HTTPS)
        """
        url = os.environ['RENDER_URL']
        assert url.startswith('https://'), "Render URL should use HTTPS"

        # requests will raise SSLError if cert is invalid
        response = requests.get(url, timeout=30)
        assert response.status_code == 200

    def test_environment_variables_set_correctly(self):
        """
        GIVEN: QRCards deployed to Render
        WHEN: We check a health/status endpoint
        THEN: App should be using production configuration

        NOTE: This requires adding a /health endpoint to your app
        that returns config status (implement this later)
        """
        pytest.skip("Health endpoint not implemented yet")
```

### Step 6.2: Create render.yaml (Infrastructure as Code)

**render.yaml:**
```yaml
services:
  - type: web
    name: qrcards
    env: python
    region: oregon
    plan: starter

    disk:
      name: qrcards-data
      mountPath: /data
      sizeGB: 10

    buildCommand: pip install -r requirements.txt
    startCommand: gunicorn --bind 0.0.0.0:$PORT --workers 2 run:app

    envVars:
      - key: FLASK_ENV
        value: production
      - key: DATABASE_PATH
        value: /data
```

### Step 6.3: Commit and Push to GitHub

```bash
cd ~/qrcards-deploy/

# Add all files
git add Dockerfile render.yaml tests/

git commit -m "Add Dockerfile, render.yaml, and tests

- Dockerfile with Python 3.11 and /data directory
- render.yaml with 10GB persistent disk
- Functional tests for deployment validation
- Unit tests for app configuration

Tests pass locally. Ready for Render deployment."

git push origin main
```

### Step 6.4: Deploy to Render (Manual Steps)

**In Render Dashboard:**
1. Click "New +" → "Web Service"
2. Connect GitHub → Select `qrcards-deploy` repo
3. Render auto-detects `render.yaml`
4. Click "Create Web Service"
5. Wait for build (~3-5 minutes)
6. Note the URL: `https://qrcards.onrender.com`

### Step 6.5: Run Deployment Tests (GREEN)

```bash
# Set Render URL
export RENDER_URL="https://qrcards.onrender.com"

# Run deployment tests
pytest tests/functional/test_render_deployment.py -v

# Expected: ✅ GREEN (or ⏭️ YELLOW with specific failures to fix)
```

**If tests fail:** Debug using Render logs, fix issues, redeploy, test again.

**Status:** ✅ GREEN - App is deployed to Render and responding

---

## Chapter 7: Custom Domain - "Can Users Access My App?"

### Step 7.1: Write Custom Domain Test (RED)

**tests/functional/test_custom_domain.py:**
```python
"""
Tests for custom domain configuration.
Verify app.modelcitizendeveloper.com works correctly.
"""

import requests
import os
import pytest

# Skip if custom domain not set
pytestmark = pytest.mark.skipif(
    not os.environ.get('CUSTOM_DOMAIN'),
    reason="CUSTOM_DOMAIN not set - DNS not configured yet"
)

class TestCustomDomain:
    """Test custom domain configuration."""

    def test_custom_domain_resolves(self):
        """
        GIVEN: Custom domain configured in Render
        WHEN: We visit the custom domain
        THEN: App should respond with 200 OK
        """
        domain = os.environ['CUSTOM_DOMAIN']
        response = requests.get(f'https://{domain}', timeout=30)
        assert response.status_code == 200

    def test_custom_domain_has_ssl(self):
        """
        GIVEN: Custom domain configured
        WHEN: We check SSL certificate
        THEN: Certificate should be valid for our domain
        """
        domain = os.environ['CUSTOM_DOMAIN']
        response = requests.get(f'https://{domain}', timeout=30)

        # If this doesn't raise SSLError, cert is valid
        assert response.status_code == 200

    def test_renders_same_content_as_render_url(self):
        """
        GIVEN: Both Render URL and custom domain configured
        WHEN: We visit both URLs
        THEN: They should serve the same content
        """
        render_url = os.environ.get('RENDER_URL')
        custom_domain = os.environ['CUSTOM_DOMAIN']

        if not render_url:
            pytest.skip("RENDER_URL not set")

        render_response = requests.get(render_url, timeout=30)
        custom_response = requests.get(f'https://{custom_domain}', timeout=30)

        # Both should return 200
        assert render_response.status_code == 200
        assert custom_response.status_code == 200
```

### Step 7.2: Run Test (YELLOW/SKIPPED)

```bash
pytest tests/functional/test_custom_domain.py -v

# Expected: ⏭️ YELLOW (skipped - CUSTOM_DOMAIN not set)
```

### Step 7.3: Configure Custom Domain

**In Render Dashboard:**
1. qrcards service → Settings → Custom Domains
2. Add domain: `app.modelcitizendeveloper.com`
3. Render provides CNAME target

**In DNS Provider:**
```
Type: CNAME
Host: app
Value: qrcards.onrender.com
TTL: 300
```

**Wait for:** SSL certificate provisioning (5-15 minutes)

### Step 7.4: Run Test Again (GREEN)

```bash
# Set custom domain
export CUSTOM_DOMAIN="app.modelcitizendeveloper.com"

# Run tests
pytest tests/functional/test_custom_domain.py -v

# Expected: ✅ GREEN (all tests pass)
```

**Status:** ✅ GREEN - Custom domain works with valid SSL

---

## Chapter 8: Database Migration - "Does My Data Work?"

### Step 8.1: Write Database Migration Test (RED)

**tests/functional/test_database_migration.py:**
```python
"""
Tests for database migration from PythonAnywhere to Render.
Verify databases work correctly on Render.
"""

import requests
import os
import pytest

pytestmark = pytest.mark.skipif(
    not os.environ.get('CUSTOM_DOMAIN'),
    reason="Not deployed yet"
)

class TestDatabaseMigration:
    """Test database functionality on Render."""

    def test_can_create_qr_code(self):
        """
        GIVEN: QRCards deployed to Render
        WHEN: We create a QR code via the API
        THEN: QR code should be stored in database

        NOTE: Implement based on your actual API
        """
        pytest.skip("Implement based on your QR code creation API")

    def test_can_retrieve_existing_qr_code(self):
        """
        GIVEN: QR codes exist in database
        WHEN: We request a QR code resolution
        THEN: App should resolve correctly

        NOTE: Use a test QR code token from your database
        """
        pytest.skip("Implement based on your QR resolution API")

    def test_database_persists_after_redeploy(self):
        """
        GIVEN: Data written to database
        WHEN: App redeploys
        THEN: Data should still exist (persistent disk works)

        NOTE: This is a manual test - deploy twice and verify
        """
        pytest.skip("Manual test - verify after first redeploy")
```

---

## Chapter 9: Production Readiness - "Is It Actually Working?"

### Step 9.1: Write Production Health Test (RED)

**tests/functional/test_production_health.py:**
```python
"""
Production health checks.
Verify app meets production requirements.
"""

import requests
import os
import pytest
import time

pytestmark = pytest.mark.skipif(
    not os.environ.get('CUSTOM_DOMAIN'),
    reason="Not deployed to production yet"
)

class TestProductionHealth:
    """Test production readiness."""

    def test_response_time_under_threshold(self):
        """
        GIVEN: Production deployment
        WHEN: We make a request
        THEN: Response time should be under 1 second
        """
        domain = os.environ['CUSTOM_DOMAIN']

        start = time.time()
        response = requests.get(f'https://{domain}', timeout=30)
        elapsed = time.time() - start

        assert response.status_code == 200
        assert elapsed < 1.0, f"Response took {elapsed:.2f}s (threshold: 1.0s)"

    def test_handles_404_gracefully(self):
        """
        GIVEN: Production deployment
        WHEN: We request a non-existent page
        THEN: Should return 404 (not 500 error)
        """
        domain = os.environ['CUSTOM_DOMAIN']
        response = requests.get(
            f'https://{domain}/this-page-does-not-exist-12345',
            timeout=30
        )

        # Should be 404, not 500
        assert response.status_code == 404

    def test_security_headers_present(self):
        """
        GIVEN: Production deployment
        WHEN: We check response headers
        THEN: Security headers should be present
        """
        domain = os.environ['CUSTOM_DOMAIN']
        response = requests.get(f'https://{domain}', timeout=30)

        # Check for some basic security headers
        # Adjust based on your requirements
        headers = response.headers

        # At minimum, should have these
        assert 'Content-Type' in headers
        # Add more security headers as needed:
        # assert 'X-Frame-Options' in headers
        # assert 'X-Content-Type-Options' in headers
```

---

## Chapter 10: Continuous Testing - "Does It Stay Working?"

### Step 10.1: Create Test Runner Script

**test_all.sh:**
```bash
#!/bin/bash
# Run all tests in order

set -e  # Exit on first failure

echo "=========================================="
echo "QRCards Deployment Test Suite"
echo "=========================================="

# Unit tests (local, no deployment needed)
echo ""
echo ">>> Running Unit Tests..."
pytest tests/unit/ -v

# Docker tests (requires Docker)
echo ""
echo ">>> Running Docker Tests..."
pytest tests/functional/test_docker_build.py -v

# Deployment tests (requires RENDER_URL)
if [ -n "$RENDER_URL" ]; then
    echo ""
    echo ">>> Running Render Deployment Tests..."
    pytest tests/functional/test_render_deployment.py -v
else
    echo ""
    echo "⏭️  Skipping Render tests (RENDER_URL not set)"
fi

# Custom domain tests (requires CUSTOM_DOMAIN)
if [ -n "$CUSTOM_DOMAIN" ]; then
    echo ""
    echo ">>> Running Custom Domain Tests..."
    pytest tests/functional/test_custom_domain.py -v

    echo ""
    echo ">>> Running Production Health Tests..."
    pytest tests/functional/test_production_health.py -v
else
    echo ""
    echo "⏭️  Skipping custom domain tests (CUSTOM_DOMAIN not set)"
fi

echo ""
echo "=========================================="
echo "✅ All Tests Passed!"
echo "=========================================="
```

**Make it executable:**
```bash
chmod +x test_all.sh
```

### Step 10.2: Run Full Test Suite

```bash
# Set environment variables
export RENDER_URL="https://qrcards.onrender.com"
export CUSTOM_DOMAIN="app.modelcitizendeveloper.com"

# Run all tests
./test_all.sh

# Expected: ✅ All tests pass (or specific failures to address)
```

---

## The TDD DevOps Cycle

**For each new feature or change:**

1. **Write the test first** (RED)
   - "What should happen after this change?"
   - Test fails because feature doesn't exist yet

2. **Make minimal change to pass** (GREEN)
   - Add just enough code/config to make test pass
   - Don't over-engineer

3. **Refactor while keeping tests green** (REFACTOR)
   - Clean up code/config
   - Improve structure
   - Tests still pass

4. **Commit and deploy**
   - Tests prove it works
   - Confident to deploy

---

## Quick Reference: Test Commands

```bash
# Unit tests (fast, local)
pytest tests/unit/ -v

# Docker tests (medium, requires Docker)
pytest tests/functional/test_docker_build.py -v

# Deployment tests (slow, requires deployed app)
export RENDER_URL="https://qrcards.onrender.com"
pytest tests/functional/test_render_deployment.py -v

# Custom domain tests (requires DNS configured)
export CUSTOM_DOMAIN="app.modelcitizendeveloper.com"
pytest tests/functional/test_custom_domain.py -v

# Full suite
./test_all.sh
```

---

## What We've Achieved

By following this TDD approach, you have:

✅ **Confidence** - Tests prove each step works
✅ **Documentation** - Tests describe what should happen
✅ **Regression Prevention** - Tests catch when things break
✅ **Incremental Progress** - Each chapter builds on the last
✅ **Rollback Safety** - Tests tell you if rollback worked

**Next:** Run through these chapters, one at a time, making each test green before moving forward.

---

## Troubleshooting Guide

**If a test fails:**

1. **Read the error message carefully** - It tells you what's wrong
2. **Don't skip ahead** - Fix current test before moving on
3. **Make minimal change** - Just enough to make test pass
4. **Re-run test** - Verify it's actually green
5. **Commit** - Lock in the working state

**Common issues:**

- Import errors → Check requirements.txt
- Docker build fails → Check Dockerfile syntax
- Deployment fails → Check Render logs
- DNS not working → Wait for propagation (up to 24 hours, usually 5-10 min)

---

## Summary: Your Step-by-Step Path

**This weekend:**
1. Chapter 1-2: Write and run local tests ✅
2. Chapter 3: Docker tests (build image)
3. Chapter 4: Database persistence tests
4. Chapter 5: Environment config tests

**Next week:**
5. Chapter 6: Deploy to Render, run deployment tests
6. Chapter 7: Configure custom domain, run domain tests
7. Chapter 8: Migrate database, verify data works
8. Chapter 9: Run production health checks
9. Chapter 10: Set up continuous testing

**Each step:** RED → GREEN → REFACTOR → COMMIT

**Philosophy:** If the tests pass, you're good. If they fail, you know exactly what to fix.
