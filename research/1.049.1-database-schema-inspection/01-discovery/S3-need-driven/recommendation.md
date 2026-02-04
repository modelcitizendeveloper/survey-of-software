# S3 Need-Driven Recommendations: Database Schema Inspection

## Executive Summary

This document provides specific tool recommendations matched to workflow requirements. Choose your use case below to find the optimal toolchain for your needs.

## Decision Matrix

| Use Case | Primary Tool | Supporting Tools | Complexity | Setup Time |
|----------|-------------|------------------|------------|------------|
| Legacy Reverse Engineering | sqlacodegen | SQLAlchemy | Low | 15 mins |
| CI/CD Migration Validation | Alembic + pytest | migra | Medium | 2 hours |
| Multi-Environment Sync | migra | Alembic, SQLAlchemy | Medium | 3 hours |
| Greenfield Project | Alembic | SQLAlchemy | Low | 30 mins |
| Database-First Development | sqlacodegen | Alembic, CI/CD | High | 4 hours |

## Use Case Recommendations

### 1. Legacy Database Reverse Engineering

**Recommended: sqlacodegen**

**Best fit when:**
- Inheriting existing database without models
- One-time model generation needed
- Database has good foreign key relationships
- Need SQLAlchemy declarative models

**Installation:**
```bash
uv pip install sqlacodegen
```

**Quick Start:**
```bash
# Generate models with relationships
sqlacodegen postgresql://localhost/legacy_db > models.py

# For advanced features
sqlacodegen \
  --generator declarative \
  --outfile models.py \
  postgresql://localhost/legacy_db
```

**Pros:**
- Excellent relationship inference
- Handles complex schemas well
- Supports advanced SQLAlchemy features
- One command generates complete models

**Cons:**
- Generated code needs manual cleanup
- Naming conventions may not match project standards
- Large schemas produce very long files
- Relationships may need manual correction

**Alternative for Django:**
```bash
python manage.py inspectdb > models.py
```

**Success Criteria:**
- All tables mapped to models: 100%
- Relationships correctly inferred: >90%
- Type mappings accurate: 100%
- Manual cleanup required: <20% of code

---

### 2. CI/CD Migration Validation

**Recommended: Alembic + pytest + migra**

**Best fit when:**
- Automated deployment pipeline exists
- Multiple environments (dev/staging/prod)
- Need to catch migration errors before production
- Team follows test-driven development

**Installation:**
```bash
uv pip install alembic pytest pytest-postgresql migra
```

**Quick Start:**
```python
# tests/test_migrations.py
def test_migrations_apply_cleanly(alembic_config):
    command.upgrade(alembic_config, "head")
    assert True

def test_schema_matches_models(db_engine, app_models):
    migration = Migration(db_engine, app_models)
    migration.add_all_changes()
    assert not migration.statements
```

**Pros:**
- Catches migration issues before production
- Automated in CI/CD pipeline
- Validates both upgrade and downgrade paths
- Clear pass/fail criteria

**Cons:**
- Initial setup complexity
- Requires test database infrastructure
- May slow down CI/CD pipeline
- Needs maintenance as tests evolve

**Key Components:**

1. **Migration Tests:** Verify migrations apply successfully
2. **Schema Comparison:** Ensure migrations produce expected schema
3. **Rollback Tests:** Validate downgrade paths work
4. **Performance Tests:** Check migration speed

**Success Criteria:**
- 100% migration test coverage
- Zero production migration failures
- CI/CD pipeline time increase: <5 minutes
- Clear error reporting on failures

---

### 3. Multi-Environment Schema Synchronization

**Recommended: migra + Alembic**

**Best fit when:**
- Managing dev/staging/production environments
- Schema drift is a recurring problem
- Need automated drift detection
- Compliance requires audit trail

**Installation:**
```bash
uv pip install migra alembic sqlalchemy
```

**Quick Start:**
```bash
# Compare two databases
migra \
  postgresql://localhost/staging \
  postgresql://localhost/production

# Generate SQL to sync
migra \
  --unsafe \
  postgresql://localhost/staging \
  postgresql://localhost/production > sync.sql
```

**Pros:**
- Fast, accurate schema comparison
- PostgreSQL-specific optimizations
- Generates SQL to fix drift
- Minimal dependencies

**Cons:**
- PostgreSQL-only (no MySQL/SQLite)
- Requires direct database access
- No built-in automation (need scripting)
- Doesn't handle data migrations

**Architecture:**

```
[Dev DB] --migra--> [Staging DB] --migra--> [Prod DB]
    |                    |                     |
    +-- Alembic --------+--------Alembic -----+
```

**Daily Workflow:**
```bash
# Morning: Check for drift
python scripts/check_drift.py

# Before deployment: Validate
migra staging_db prod_db

# After deployment: Verify
python scripts/verify_sync.py
```

**Alternative for MySQL:**
```bash
# Use mysqldump + diff approach
mysqldump --no-data staging_db > staging_schema.sql
mysqldump --no-data prod_db > prod_schema.sql
diff -u staging_schema.sql prod_schema.sql
```

**Success Criteria:**
- Drift detected within: 24 hours
- False positive rate: <5%
- Time to identify drift: <5 minutes
- Automated drift alerts: Yes

---

### 4. Greenfield SQLAlchemy Project

**Recommended: Alembic (with SQLAlchemy)**

**Best fit when:**
- Starting new Python project
- Using SQLAlchemy ORM
- Want version-controlled schema changes
- Team collaboration on schema

**Installation:**
```bash
uv pip install alembic sqlalchemy psycopg2-binary
```

**Quick Start:**
```bash
# Initialize Alembic
alembic init alembic

# Edit alembic/env.py to import your models
# Then generate first migration
alembic revision --autogenerate -m "Initial schema"

# Apply migration
alembic upgrade head
```

**Pros:**
- Industry standard for SQLAlchemy
- Auto-generates migrations from model changes
- Excellent documentation
- Production-proven

**Cons:**
- Learning curve for team
- Auto-generation needs review
- Complex migrations require manual coding
- Migration conflicts need resolution

**Project Structure:**
```
myproject/
  models/
    __init__.py
    user.py
    product.py
  alembic/
    env.py
    versions/
      001_initial_schema.py
      002_add_indexes.py
  alembic.ini
```

**Development Workflow:**

1. **Update Models:** Change SQLAlchemy model definitions
2. **Generate Migration:** `alembic revision --autogenerate`
3. **Review Migration:** Manually check generated code
4. **Test Migration:** Apply to dev database
5. **Commit:** Version control migration script
6. **Deploy:** Apply in staging, then production

**Best Practices:**
- Always review auto-generated migrations
- Test migrations in fresh database
- Use descriptive migration messages
- Never skip migration files in version control

**Success Criteria:**
- All schema changes via migrations: 100%
- Manual SQL in production: 0%
- New developer setup time: <10 minutes
- Migration conflicts: <1 per month

---

### 5. Database-First Development

**Recommended: sqlacodegen + Alembic + CI/CD automation**

**Best fit when:**
- Database team controls schema
- DBAs use SQL for schema changes
- Multiple applications share database
- Need automatic model synchronization

**Installation:**
```bash
uv pip install sqlacodegen alembic sqlalchemy
```

**Architecture:**

```
[DBA Team]
    |
    v
[SQL Migrations] --> [Database]
                        |
                        v
                   [sqlacodegen] --> [Generated Models]
                        |
                        v
                   [Custom Extensions] --> [Application]
```

**Quick Start:**

1. **Generate Models:**
```bash
sqlacodegen postgresql://localhost/mydb > models/generated/schema.py
```

2. **Separate Custom Code:**
```python
# models/custom/user_extensions.py
from models.generated.schema import User as GeneratedUser

class User(GeneratedUser):
    def custom_method(self):
        pass
```

3. **Automate Sync:**
```yaml
# .github/workflows/model-sync.yml
on:
  schedule:
    - cron: '0 0 * * *'
jobs:
  sync-models:
    steps:
      - run: python scripts/sync_models.py
      - uses: peter-evans/create-pull-request@v5
```

**Pros:**
- Respects database-first workflow
- DBAs maintain independence
- Automatic model updates
- Clear separation of concerns

**Cons:**
- High initial setup complexity
- Requires CI/CD infrastructure
- Risk of custom code loss
- Coordination between teams needed

**Critical Success Factors:**

1. **Separation of Generated/Custom Code:** Never mix
2. **Automated Sync Checks:** Daily or more frequent
3. **Clear Communication:** DB team alerts app team
4. **Version Control:** Track generated models

**Success Criteria:**
- Model sync lag: <24 hours
- Custom code preserved: 100%
- Manual model updates: 0%
- Schema-related bugs: <1 per quarter

---

## Cross-Cutting Tool Evaluations

### sqlacodegen

**Use for:**
- Generating models from existing databases
- One-time reverse engineering
- Periodic model regeneration

**Avoid for:**
- Ongoing schema management
- Complex custom model logic
- Real-time schema tracking

**Version:** Latest stable (3.0.0+)

---

### Alembic

**Use for:**
- Version-controlled migrations
- SQLAlchemy-based projects
- Team collaboration on schema
- Production deployments

**Avoid for:**
- Non-SQLAlchemy ORMs
- Simple prototypes
- Read-only database access

**Version:** Latest stable (1.13.0+)

---

### migra

**Use for:**
- PostgreSQL schema comparison
- Drift detection
- Environment synchronization
- Generating sync SQL

**Avoid for:**
- MySQL/SQLite (not supported)
- Data migration
- Complex transformation logic

**Version:** Latest stable (3.0.0+)
**Platform:** PostgreSQL only

---

### pytest + pytest-postgresql

**Use for:**
- Automated migration testing
- CI/CD validation
- Schema consistency checks

**Avoid for:**
- Simple manual testing
- Non-Python projects

**Version:** pytest 7.0+, pytest-postgresql 5.0+

---

## Decision Flowchart

```
Start: What is your primary need?

├─ Generate models from existing DB?
│  └─> Use sqlacodegen
│
├─ Validate migrations in CI/CD?
│  └─> Use Alembic + pytest + migra
│
├─ Detect schema drift across environments?
│  └─> Use migra + Alembic
│
├─ Start new project with migrations?
│  └─> Use Alembic
│
└─ Database-first with DBA team?
   └─> Use sqlacodegen + Alembic + automation
```

---

## Combination Strategies

### Strategy 1: Full-Stack Schema Management
**Tools:** Alembic + migra + pytest
**Use case:** Mature project with multiple environments

### Strategy 2: Hybrid Database-First
**Tools:** sqlacodegen + Alembic
**Use case:** DBA-managed schema with application migrations

### Strategy 3: Simple Greenfield
**Tools:** Alembic only
**Use case:** New project, application controls schema

### Strategy 4: Legacy Migration
**Tools:** sqlacodegen + manual cleanup
**Use case:** One-time reverse engineering

---

## Common Anti-Patterns

### Anti-Pattern 1: Manual SQL in Production
**Problem:** Bypassing migration tools
**Solution:** All changes through Alembic migrations

### Anti-Pattern 2: Ignoring Migration Tests
**Problem:** Migrations fail in production
**Solution:** Implement CI/CD validation with pytest

### Anti-Pattern 3: Mixing Generated and Custom Code
**Problem:** Regeneration overwrites custom logic
**Solution:** Strict separation of generated/custom files

### Anti-Pattern 4: No Schema Version Control
**Problem:** Unknown database state in environments
**Solution:** Track all migrations in version control

---

## Quick Reference Commands

```bash
# Generate models from database
sqlacodegen postgresql://localhost/mydb > models.py

# Initialize Alembic
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Compare schemas (PostgreSQL)
migra postgresql://localhost/db1 postgresql://localhost/db2

# Run migration tests
pytest tests/migrations/ -v
```

---

## When to Seek Custom Solutions

Consider building custom tooling when:
- Using non-standard database (e.g., ClickHouse, TimescaleDB)
- Complex domain-specific requirements
- Existing tools don't support your workflow
- High-volume schema automation needed

---

## Further Resources

### Documentation
- Alembic: https://alembic.sqlalchemy.org/
- SQLAlchemy: https://www.sqlalchemy.org/
- migra: https://github.com/djrobstep/migra
- sqlacodegen: https://github.com/agronholm/sqlacodegen

### Community
- SQLAlchemy Google Group
- Alembic GitHub Discussions
- Stack Overflow: [sqlalchemy], [alembic], [database-migration]

---

Date compiled: December 4, 2025
