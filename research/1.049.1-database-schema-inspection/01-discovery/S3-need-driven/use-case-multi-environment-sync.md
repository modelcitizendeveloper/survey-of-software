# Use Case: Multi-Environment Schema Synchronization

## Scenario Description

Your team maintains development, staging, and production environments. Schema changes must propagate correctly through each environment, but drift occurs due to hotfixes, manual changes, and incomplete migrations. You need tools to detect drift and ensure consistency.

## Primary Requirements

### Must-Have Features
1. **Schema drift detection** across environments
2. **Automated sync verification** in deployment pipeline
3. **Diff generation** showing exact discrepancies
4. **Safe synchronization** without data loss
5. **Audit trail** of schema changes

### Operational Constraints
- Cannot disrupt production operations
- Must handle environments with different data volumes
- Need read-only inspection of production
- Support gradual rollout strategies
- Integrate with existing deployment tools

## Recommended Toolchain

### Primary Tools: Alembic + migra + SQLAlchemy

**Why this combination:**
- **Alembic**: Version-controlled migration history
- **migra**: Fast, accurate schema comparison
- **SQLAlchemy**: Cross-platform database abstraction

**Installation:**
```bash
uv pip install alembic migra sqlalchemy psycopg2-binary
```

## Workflow Integration

### Phase 1: Environment Setup

**Configuration Structure:**
```
config/
  dev.env          # Development database URL
  staging.env      # Staging database URL
  prod.env         # Production database URL (read-only)
alembic/
  env.py           # Alembic configuration
  versions/        # Migration scripts
scripts/
  check_drift.py   # Schema drift detection
  sync_report.py   # Generate sync reports
```

**Environment Configuration:**
```python
# config/environments.py
import os

ENVIRONMENTS = {
    'dev': os.getenv('DEV_DATABASE_URL'),
    'staging': os.getenv('STAGING_DATABASE_URL'),
    'prod': os.getenv('PROD_DATABASE_URL')
}
```

### Phase 2: Drift Detection

**Automated Drift Check Script:**
```python
# scripts/check_drift.py
from migra import Migration
from sqlalchemy import create_engine
import sys

def check_drift(source_env, target_env):
    """Compare schemas between environments"""
    source_engine = create_engine(ENVIRONMENTS[source_env])
    target_engine = create_engine(ENVIRONMENTS[target_env])

    migration = Migration(source_engine, target_engine)
    migration.set_safety(False)
    migration.add_all_changes()

    if migration.statements:
        print(f"DRIFT DETECTED: {source_env} -> {target_env}")
        print(migration.sql)
        return False
    else:
        print(f"✓ {source_env} and {target_env} are in sync")
        return True

if __name__ == "__main__":
    # Check dev -> staging -> prod chain
    dev_staging_ok = check_drift('dev', 'staging')
    staging_prod_ok = check_drift('staging', 'prod')

    if not (dev_staging_ok and staging_prod_ok):
        sys.exit(1)
```

### Phase 3: Migration History Verification

**Verify Alembic History Consistency:**
```python
# scripts/verify_migrations.py
from alembic.script import ScriptDirectory
from alembic.runtime.migration import MigrationContext
from sqlalchemy import create_engine

def get_current_revision(environment):
    """Get current migration revision for environment"""
    engine = create_engine(ENVIRONMENTS[environment])
    with engine.connect() as conn:
        context = MigrationContext.configure(conn)
        return context.get_current_revision()

def verify_migration_chain():
    """Verify all environments are on expected revisions"""
    script_dir = ScriptDirectory.from_config(alembic_config)

    dev_rev = get_current_revision('dev')
    staging_rev = get_current_revision('staging')
    prod_rev = get_current_revision('prod')

    print(f"Dev:     {dev_rev}")
    print(f"Staging: {staging_rev}")
    print(f"Prod:    {prod_rev}")

    # Verify staging is not ahead of prod by more than 1 revision
    # Add business logic for acceptable drift
```

### Phase 4: Automated Sync Reporting

**Daily Sync Report:**
```python
# scripts/sync_report.py
import datetime
from migra import Migration

def generate_daily_report():
    """Generate schema sync status report"""
    report = {
        'date': datetime.datetime.now().isoformat(),
        'comparisons': []
    }

    comparisons = [
        ('dev', 'staging'),
        ('staging', 'prod')
    ]

    for source, target in comparisons:
        source_engine = create_engine(ENVIRONMENTS[source])
        target_engine = create_engine(ENVIRONMENTS[target])

        migration = Migration(source_engine, target_engine)
        migration.set_safety(False)
        migration.add_all_changes()

        report['comparisons'].append({
            'source': source,
            'target': target,
            'in_sync': len(migration.statements) == 0,
            'diff': migration.sql if migration.statements else None
        })

    return report
```

## Deployment Integration

### Pre-Deployment Validation

**GitHub Actions Workflow:**
```yaml
name: Schema Sync Check

on:
  pull_request:
    paths:
      - 'alembic/versions/**'

jobs:
  check-schema-sync:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Check for drift
        env:
          DEV_DATABASE_URL: ${{ secrets.DEV_DATABASE_URL }}
          STAGING_DATABASE_URL: ${{ secrets.STAGING_DATABASE_URL }}
        run: |
          python scripts/check_drift.py

      - name: Verify migration history
        run: |
          python scripts/verify_migrations.py

      - name: Generate sync report
        run: |
          python scripts/sync_report.py > sync-report.json

      - name: Upload report
        uses: actions/upload-artifact@v3
        with:
          name: sync-report
          path: sync-report.json
```

### Staging Deployment Hook

```bash
#!/bin/bash
# deploy_staging.sh

echo "Checking schema drift before deployment..."
python scripts/check_drift.py dev staging

if [ $? -ne 0 ]; then
    echo "ERROR: Schema drift detected between dev and staging"
    echo "Run sync_report.py for details"
    exit 1
fi

echo "Running migrations on staging..."
alembic -c staging.ini upgrade head

echo "Verifying post-deployment schema..."
python scripts/check_drift.py staging staging
```

## Common Pitfalls

### 1. Production Schema Drift from Hotfixes
**Problem:** Emergency fixes applied directly to production

**Solution:**
```python
def detect_unauthorized_changes():
    """Flag changes not in Alembic history"""
    # Compare production schema to expected state from migrations
    prod_engine = create_engine(ENVIRONMENTS['prod'])

    # Generate expected schema from migrations
    expected_metadata = generate_metadata_from_migrations()

    # Compare to actual production schema
    migration = Migration(expected_metadata, prod_engine)
    migration.add_all_changes()

    if migration.statements:
        alert_team("Unauthorized production schema changes detected")
```

### 2. Case Sensitivity Differences
**Problem:** PostgreSQL vs MySQL case handling causes false drift

**Solution:**
- Normalize identifiers in comparison
- Configure migra with case-insensitive mode
- Establish naming conventions

### 3. Timezone and Locale Differences
**Problem:** Timestamp columns show drift due to timezone settings

**Solution:**
```python
# Always use timezone-aware timestamps
from sqlalchemy import TIMESTAMP
from sqlalchemy.dialects.postgresql import TIMESTAMP as PG_TIMESTAMP

created_at = Column(PG_TIMESTAMP(timezone=True), default=datetime.utcnow)
```

### 4. Ignored Objects
**Problem:** Views, functions, triggers cause drift but aren't managed

**Solution:**
- Include database objects in migration scripts
- Document objects outside migration control
- Use separate sync strategy for procedural code

## Advanced Strategies

### 1. Gradual Rollout Validation

```python
def verify_canary_deployment():
    """Check schema sync for canary instances"""
    canary_engine = create_engine(CANARY_DATABASE_URL)
    prod_engine = create_engine(PROD_DATABASE_URL)

    migration = Migration(canary_engine, prod_engine)
    migration.add_all_changes()

    # Canary should be 1 version ahead
    assert len(migration.statements) == expected_diff_count
```

### 2. Blue-Green Deployment Support

```python
def prepare_blue_green_switch():
    """Ensure blue and green are schema-compatible"""
    blue_engine = create_engine(BLUE_DATABASE_URL)
    green_engine = create_engine(GREEN_DATABASE_URL)

    migration = Migration(blue_engine, green_engine)
    migration.add_all_changes()

    # Must be identical or backward-compatible
    assert is_backward_compatible(migration.statements)
```

### 3. Compliance Audit Trail

```python
def log_schema_change(environment, revision, operator):
    """Maintain audit log of schema changes"""
    audit_entry = {
        'timestamp': datetime.utcnow(),
        'environment': environment,
        'revision': revision,
        'operator': operator,
        'approved_by': get_approval_record(revision)
    }
    # Store in compliance database
```

## Alternative Approaches

### For PostgreSQL: pg_dump + diff
```bash
# Generate schema-only dumps
pg_dump --schema-only prod_db > prod_schema.sql
pg_dump --schema-only staging_db > staging_schema.sql

# Compare with diff
diff -u prod_schema.sql staging_schema.sql
```

### For MySQL: mysqldump + diff
```bash
mysqldump --no-data prod_db > prod_schema.sql
mysqldump --no-data staging_db > staging_schema.sql
diff -u prod_schema.sql staging_schema.sql
```

### For Django: Django migrations check
```bash
python manage.py migrate --plan
python manage.py showmigrations
```

## Success Metrics

### Technical Success
- Zero undetected schema drift incidents
- 100% migration consistency across environments
- Automated drift detection runs daily
- All environments track migration history

### Operational Success
- Reduced deployment rollbacks due to schema issues
- Clear visibility into environment states
- Faster incident response with drift detection
- Compliance-ready audit trail

## Example Daily Workflow

```bash
# Morning: Check overnight drift
python scripts/sync_report.py | mail -s "Daily Schema Sync Report" team@company.com

# Before deployment: Validate sync
python scripts/check_drift.py staging prod

# Deploy to staging
alembic -c staging.ini upgrade head

# Verify deployment
python scripts/verify_migrations.py

# After production deployment
python scripts/check_drift.py prod prod  # Verify internal consistency
python scripts/generate_compliance_report.py
```

## When NOT to Use This Approach

- Single environment deployments
- Read-only reporting databases
- Databases managed by external tools
- Fully isolated development environments

Date compiled: December 4, 2025
