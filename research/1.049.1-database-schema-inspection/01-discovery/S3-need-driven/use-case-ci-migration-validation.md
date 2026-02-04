# Use Case: CI/CD Migration Validation

## Scenario Description

Your team deploys database migrations through CI/CD pipelines. You need automated validation that migrations apply cleanly, produce the expected schema, and don't introduce unintended changes across dev, staging, and production environments.

## Primary Requirements

### Must-Have Features
1. **Schema comparison** before and after migration
2. **Automated validation** in CI/CD pipeline
3. **Diff detection** for unintended changes
4. **Rollback verification** for down migrations
5. **Environment-agnostic testing** (dev/staging/prod)

### Operational Constraints
- Must run in CI/CD without human intervention
- Fast execution (< 2 minutes for schema checks)
- Clear error reporting for failures
- Integration with existing test frameworks
- Support for multiple database backends

## Recommended Toolchain

### Primary Tool: Alembic + pytest + migra

**Why this combination:**
- **Alembic**: Industry-standard SQLAlchemy migration tool
- **pytest**: Flexible test framework with fixtures
- **migra**: Fast PostgreSQL schema diffing

**Installation:**
```bash
uv pip install alembic pytest pytest-postgresql migra
```

## Workflow Integration

### Phase 1: Migration Testing Setup

**Directory Structure:**
```
tests/
  migrations/
    test_migration_validity.py
    test_schema_consistency.py
    conftest.py
alembic/
  versions/
    001_initial_schema.py
    002_add_user_table.py
```

### Phase 2: Validation Tests

**Test 1: Migration Applies Cleanly**
```python
# tests/migrations/test_migration_validity.py
import pytest
from alembic import command
from alembic.config import Config

def test_upgrade_migrations(alembic_config, empty_db):
    """Verify all migrations apply successfully"""
    command.upgrade(alembic_config, "head")

def test_downgrade_migrations(alembic_config, migrated_db):
    """Verify migrations can roll back"""
    command.downgrade(alembic_config, "base")
```

**Test 2: Schema Matches Expected State**
```python
from migra import Migration
from sqlalchemy import create_engine, MetaData

def test_schema_matches_models(migrated_db, app_models):
    """Verify migrated schema matches SQLAlchemy models"""
    # Compare database schema to model definitions
    migration = Migration(migrated_db, app_models)
    migration.set_safety(False)
    migration.add_all_changes()

    diff = migration.sql
    assert not diff, f"Schema mismatch detected:\n{diff}"
```

**Test 3: No Unintended Changes**
```python
def test_migration_is_reversible(alembic_config, db_engine):
    """Verify up/down migrations are reversible"""
    metadata_before = MetaData()
    metadata_before.reflect(bind=db_engine)

    # Apply and rollback migration
    command.upgrade(alembic_config, "+1")
    command.downgrade(alembic_config, "-1")

    metadata_after = MetaData()
    metadata_after.reflect(bind=db_engine)

    # Schema should be identical
    assert set(metadata_before.tables.keys()) == set(metadata_after.tables.keys())
```

### Phase 3: CI/CD Integration

**GitHub Actions Example:**
```yaml
name: Migration Tests

on: [push, pull_request]

jobs:
  test-migrations:
    runs-on: ubuntu-latest

    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install -r requirements.txt

      - name: Run migration tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
        run: |
          pytest tests/migrations/ -v
```

## Advanced Validation Strategies

### 1. Performance Regression Detection

```python
import time

def test_migration_performance(alembic_config):
    """Ensure migrations complete within acceptable time"""
    start = time.time()
    command.upgrade(alembic_config, "head")
    duration = time.time() - start

    assert duration < 30, f"Migration took {duration}s (limit: 30s)"
```

### 2. Data Migration Validation

```python
def test_data_migration_preserves_records(db_session):
    """Verify data migrations don't lose records"""
    # Insert test data before migration
    initial_count = db_session.query(User).count()

    # Run migration that transforms data
    command.upgrade(alembic_config, "+1")

    # Verify all records still exist
    final_count = db_session.query(User).count()
    assert final_count == initial_count
```

### 3. Multi-Environment Consistency

```python
@pytest.mark.parametrize("db_type", ["postgresql", "mysql", "sqlite"])
def test_migration_cross_platform(db_type, alembic_config):
    """Ensure migrations work across database backends"""
    # Test same migrations on different databases
    engine = create_engine(get_connection_string(db_type))
    alembic_config.attributes['connection'] = engine

    command.upgrade(alembic_config, "head")
    # Verify schema structure matches
```

## Common Pitfalls

### 1. Test Database Isolation
**Problem:** Tests interfere with each other

**Solution:**
```python
@pytest.fixture(scope="function")
def isolated_db():
    """Create fresh database for each test"""
    db_name = f"test_{uuid.uuid4().hex}"
    create_database(db_name)
    yield db_name
    drop_database(db_name)
```

### 2. Missing Down Migration Tests
**Problem:** Rollbacks fail in production

**Solution:** Always test both upgrade and downgrade paths

### 3. Incomplete Schema Comparison
**Problem:** Missing indexes or constraints not detected

**Solution:**
```python
def test_indexes_match(migrated_db, expected_indexes):
    """Verify all expected indexes exist"""
    inspector = inspect(migrated_db)
    for table in expected_indexes:
        actual = inspector.get_indexes(table)
        expected = expected_indexes[table]
        assert actual == expected
```

### 4. Timing Issues in CI
**Problem:** Database not ready when tests start

**Solution:** Add retry logic and health checks

## Alternative Approaches

### For PostgreSQL: migra standalone
```bash
# Compare schemas directly in CI
migra \
  --unsafe \
  postgresql://localhost/before \
  postgresql://localhost/after
```

### For Django: Django test migrations
```python
from django.test import TransactionTestCase

class MigrationTest(TransactionTestCase):
    migrate_from = '0001_initial'
    migrate_to = '0002_add_field'

    def test_migration(self):
        # Django handles migration testing
        pass
```

### For MySQL: pt-table-checksum
Percona Toolkit for MySQL schema validation

## Success Metrics

### Technical Success
- 100% of migrations tested before production
- Zero unintended schema changes deployed
- Rollback procedures validated
- Cross-environment consistency verified

### Operational Success
- Migration failures caught in CI, not production
- Clear error messages for debugging
- Fast feedback loop (< 5 minutes)
- Reduced production incidents

## Example CI Workflow

```bash
# 1. Checkout code
git checkout feature/add-user-roles

# 2. Start test database
docker run -d --name test-db postgres:15

# 3. Run migration tests
pytest tests/migrations/ --verbose

# 4. Generate schema diff report
migra postgresql://localhost/baseline postgresql://localhost/migrated > diff.sql

# 5. Upload artifacts
# Store diff.sql for review

# 6. Cleanup
docker rm -f test-db
```

## When NOT to Use This Approach

- Trivial single-developer projects
- No production deployment automation
- Schema changes are rare (< 1 per month)
- Legacy systems without migration infrastructure

Date compiled: December 4, 2025
