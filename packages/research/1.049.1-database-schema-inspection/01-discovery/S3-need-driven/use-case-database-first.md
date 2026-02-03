# Use Case: Database-First Development

## Scenario Description

Your organization follows a database-first approach where database architects design schemas in SQL, and application developers build code around existing structures. You need tools that keep application models synchronized with evolving database schemas without manual model updates.

## Primary Requirements

### Must-Have Features
1. **Automatic model synchronization** from database schema
2. **Change detection** when database schema updates
3. **Bidirectional sync** (DB -> Models -> DB roundtrip)
4. **Schema versioning** integration
5. **Minimal manual intervention** in model updates

### Operational Constraints
- Database schema is the source of truth
- DBAs manage schema changes via SQL scripts
- Application code must adapt to schema changes
- Multiple applications share the same database
- Schema changes are frequent during active development

## Recommended Toolchain

### Primary Tools: sqlacodegen + Alembic + SQL migration scripts

**Why this combination:**
- **sqlacodegen**: Regenerate models from updated schema
- **Alembic**: Track application-level migrations
- **SQL scripts**: Database team's preferred workflow

**Installation:**
```bash
uv pip install sqlacodegen alembic sqlalchemy psycopg2-binary
```

## Workflow Integration

### Phase 1: Initial Setup

**Project Structure:**
```
myproject/
  models/
    generated/
      __init__.py
      schema_v1.py      # Generated models
    custom/
      __init__.py
      business_logic.py # Custom extensions
    __init__.py         # Combined exports
  db_migrations/
    001_initial_schema.sql
    002_add_indexes.sql
  alembic/
    versions/
  scripts/
    sync_models.py
    detect_changes.py
```

### Phase 2: Model Generation Strategy

**Initial Model Generation:**
```bash
# Generate models from current database
sqlacodegen \
  --outfile models/generated/schema_v1.py \
  --generator declarative \
  postgresql://localhost/production_db
```

**Wrapper Script for Consistent Generation:**
```python
# scripts/sync_models.py
import subprocess
import sys
from datetime import datetime

DATABASE_URL = sys.argv[1] if len(sys.argv) > 1 else 'postgresql://localhost/mydb'
OUTPUT_FILE = 'models/generated/schema_latest.py'

def generate_models():
    """Generate models from database schema"""
    cmd = [
        'sqlacodegen',
        '--outfile', OUTPUT_FILE,
        '--generator', 'declarative',
        '--nojoined',  # Avoid complex joined inheritance
        DATABASE_URL
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error generating models: {result.stderr}")
        sys.exit(1)

    # Add generation timestamp
    with open(OUTPUT_FILE, 'r') as f:
        content = f.read()

    header = f"""# Auto-generated models from database schema
# Generated: {datetime.now().isoformat()}
# Database: {DATABASE_URL}
# DO NOT EDIT MANUALLY - Use scripts/sync_models.py

"""
    with open(OUTPUT_FILE, 'w') as f:
        f.write(header + content)

    print(f"Models generated: {OUTPUT_FILE}")

if __name__ == '__main__':
    generate_models()
```

### Phase 3: Change Detection

**Detect Schema Changes:**
```python
# scripts/detect_changes.py
import difflib
from pathlib import Path

def detect_model_changes():
    """Compare current models with newly generated ones"""
    current_models = Path('models/generated/schema_current.py').read_text()

    # Generate fresh models
    import subprocess
    subprocess.run(['python', 'scripts/sync_models.py'])

    new_models = Path('models/generated/schema_latest.py').read_text()

    # Generate diff
    diff = difflib.unified_diff(
        current_models.splitlines(keepends=True),
        new_models.splitlines(keepends=True),
        fromfile='current',
        tofile='latest'
    )

    diff_output = ''.join(diff)

    if diff_output:
        print("SCHEMA CHANGES DETECTED:")
        print(diff_output)
        return True
    else:
        print("No schema changes detected")
        return False
```

### Phase 4: Custom Model Extensions

**Separate Generated from Custom Code:**
```python
# models/generated/schema_latest.py (auto-generated)
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255))
    username = Column(String(100))
```

**Custom Business Logic:**
```python
# models/custom/user_extensions.py
from models.generated.schema_latest import User as GeneratedUser
from sqlalchemy import event
from sqlalchemy.orm import validates

class User(GeneratedUser):
    """Extended User model with business logic"""

    @validates('email')
    def validate_email(self, key, email):
        """Validate email format"""
        if '@' not in email:
            raise ValueError("Invalid email address")
        return email.lower()

    def full_profile(self):
        """Custom method for profile data"""
        return {
            'username': self.username,
            'email': self.email
        }

# Listen to database events
@event.listens_for(User, 'before_insert')
def receive_before_insert(mapper, connection, target):
    """Normalize data before insert"""
    target.username = target.username.strip()
```

**Unified Model Export:**
```python
# models/__init__.py
# Import custom extensions (which inherit from generated models)
from .custom.user_extensions import User
from .generated.schema_latest import Product, Order

__all__ = ['User', 'Product', 'Order']
```

## Continuous Synchronization

### Automated Sync in CI/CD

**GitHub Actions Workflow:**
```yaml
name: Model Sync Check

on:
  schedule:
    - cron: '0 0 * * *'  # Daily check
  workflow_dispatch:       # Manual trigger

jobs:
  check-model-sync:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install uv
          uv pip install sqlacodegen sqlalchemy psycopg2-binary

      - name: Generate models from database
        env:
          DATABASE_URL: ${{ secrets.DATABASE_URL }}
        run: |
          python scripts/sync_models.py

      - name: Detect changes
        id: changes
        run: |
          python scripts/detect_changes.py > changes.txt
          echo "changed=$(test -s changes.txt && echo true || echo false)" >> $GITHUB_OUTPUT

      - name: Create PR if changes detected
        if: steps.changes.outputs.changed == 'true'
        uses: peter-evans/create-pull-request@v5
        with:
          commit-message: "Update models from database schema"
          title: "Schema Sync: Database changes detected"
          body: |
            Database schema has changed. Review and merge to update application models.

            See changes.txt for details.
          branch: schema-sync-${{ github.run_number }}
```

### Pre-Deployment Validation

```python
# scripts/validate_schema_sync.py
from sqlalchemy import create_engine, MetaData, inspect
from models import Base

def validate_models_match_database():
    """Ensure models match actual database schema"""
    engine = create_engine(DATABASE_URL)

    # Get database schema
    inspector = inspect(engine)
    db_tables = set(inspector.get_table_names())

    # Get model tables
    model_tables = set(Base.metadata.tables.keys())

    # Check for mismatches
    missing_in_models = db_tables - model_tables
    missing_in_db = model_tables - db_tables

    if missing_in_models:
        print(f"Tables in DB but not in models: {missing_in_models}")
        return False

    if missing_in_db:
        print(f"Tables in models but not in DB: {missing_in_db}")
        return False

    print("Models are in sync with database")
    return True
```

## Common Pitfalls

### 1. Loss of Custom Code
**Problem:** Regenerating models overwrites custom methods

**Solution:** Always separate generated and custom code
```
models/
  generated/     # Auto-generated, can be overwritten
  custom/        # Hand-written extensions
```

### 2. Relationship Inference Errors
**Problem:** sqlacodegen misinterprets foreign keys

**Solution:**
```python
# Review and override in custom extensions
class Order(GeneratedOrder):
    # Override incorrect relationship
    items = relationship('OrderItem', back_populates='order', lazy='joined')
```

### 3. Missing Business Constraints
**Problem:** Database constraints not reflected in Python models

**Solution:**
```python
# Add Python-level validation in custom models
@validates('quantity')
def validate_quantity(self, key, quantity):
    if quantity < 0:
        raise ValueError("Quantity cannot be negative")
    return quantity
```

### 4. Schema Evolution Without Model Updates
**Problem:** Database changes but models not regenerated

**Solution:** Implement scheduled checks (see CI/CD workflow above)

## Advanced Strategies

### 1. Selective Model Generation

```python
# Generate only specific tables
sqlacodegen \
  --tables users,products,orders \
  postgresql://localhost/mydb
```

### 2. Schema Comparison Tool

```python
# scripts/compare_schemas.py
from migra import Migration

def compare_models_to_database():
    """Compare SQLAlchemy models to actual database"""
    model_engine = create_engine('postgresql://')  # In-memory from models
    Base.metadata.create_all(model_engine)

    db_engine = create_engine(DATABASE_URL)

    migration = Migration(model_engine, db_engine)
    migration.set_safety(False)
    migration.add_all_changes()

    if migration.statements:
        print("Models differ from database:")
        print(migration.sql)
```

### 3. Hybrid Approach: Track DB Migrations

```bash
# DBA applies SQL migration
psql -f db_migrations/003_add_user_roles.sql

# Regenerate models
python scripts/sync_models.py

# Create Alembic migration for application tracking
alembic revision --autogenerate -m "Sync with DB migration 003"
```

## Alternative Approaches

### For Django: inspectdb workflow
```bash
# Generate Django models from database
python manage.py inspectdb > models_generated.py

# Review and move to app
# Add custom methods in separate files
```

### For Read-Only Applications: Direct Reflection
```python
# No model files needed for simple reporting
from sqlalchemy import MetaData, Table

metadata = MetaData()
users = Table('users', metadata, autoload_with=engine)

# Query directly
session.query(users).all()
```

### For TypeScript/Prisma: Prisma introspect
```bash
# Generate Prisma schema from database
npx prisma db pull

# Generate client
npx prisma generate
```

## Success Metrics

### Technical Success
- Models stay synchronized with database (<24hr lag)
- No runtime errors due to schema mismatches
- Automated detection of schema drift
- Clear separation of generated vs. custom code

### Operational Success
- DBA team maintains schema independence
- Application team responds to changes quickly
- Reduced manual model maintenance
- Clear audit trail of schema changes

## Example Workflow

**Database Team:**
```sql
-- db_migrations/004_add_user_preferences.sql
ALTER TABLE users ADD COLUMN preferences JSONB;
CREATE INDEX idx_users_preferences ON users USING gin(preferences);
```

**Application Team (Automated):**
```bash
# CI/CD detects change and creates PR
1. Scheduled job runs sync_models.py
2. Detects schema changes
3. Generates new models/generated/schema_latest.py
4. Creates PR with changes
```

**Application Team (Manual):**
```python
# Review PR and add custom logic
# models/custom/user_extensions.py
class User(GeneratedUser):
    def get_preference(self, key, default=None):
        """Helper for accessing preferences"""
        if not self.preferences:
            return default
        return self.preferences.get(key, default)
```

## When NOT to Use This Approach

- Application controls schema design
- Rapid prototyping phase
- Microservices with database-per-service
- Small teams where developers are also DBAs

Date compiled: December 4, 2025
