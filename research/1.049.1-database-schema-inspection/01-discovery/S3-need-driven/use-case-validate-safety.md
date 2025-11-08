# Use Case: Validate Migration Safety

## Pattern Definition

### Requirement Statement

**Need**: Analyze planned database schema changes to detect potentially destructive operations that could cause data loss, downtime, or application breakage before executing migrations.

**Why This Matters**: Applications need to:
- Prevent accidental data deletion (DROP TABLE, DROP COLUMN)
- Detect breaking changes for running applications (NULL → NOT NULL)
- Catch type incompatibilities (VARCHAR → INTEGER with existing data)
- Identify performance risks (adding index to large table)
- Validate multi-step migration safety
- Enable automated deployment with confidence

### Input Parameters

| Parameter | Range | Impact |
|-----------|-------|--------|
| Migration Type | Additive, Destructive, Transformative | Risk level |
| Table Size | 100 rows to 100M rows | Downtime risk |
| Data Presence | Empty vs populated tables | Data loss risk |
| Application State | Live traffic vs maintenance window | Breaking change impact |
| Rollback Strategy | Reversible vs one-way | Recovery options |

### Success Criteria

**Must Detect**:
1. DROP TABLE on table with data
2. DROP COLUMN on column with data
3. NOT NULL addition to column with nulls
4. Type changes incompatible with existing data
5. Foreign key addition that would fail on existing data
6. Unique constraint addition that would fail
7. Reducing column size with data truncation risk (VARCHAR(100) → VARCHAR(50))

**Performance Target**: <1 second validation for typical migration

**Accuracy**: 100% detection of destructive operations (zero false negatives acceptable)

### Constraints

- Must check actual database state, not just schema definitions
- Should distinguish between safe operations (add column) and risky ones (drop column)
- Must handle database-specific behavior (PostgreSQL vs MySQL locking)
- Should provide actionable remediation suggestions

## Library Fit Analysis

### Option 1: Alembic with Custom Validators

**API Example**:
```python
from alembic import op
from alembic.operations import Operations, MigrateOperation
from sqlalchemy import inspect

@Operations.register_operation("validate_safe_drop")
class ValidateSafeDrop(MigrateOperation):
    """Custom operation to validate table has no data before dropping"""

    def __init__(self, table_name):
        self.table_name = table_name

    @classmethod
    def validate_safe_drop(cls, operations, table_name):
        op = ValidateSafeDrop(table_name)
        return operations.invoke(op)

    def reverse(self):
        return None

@Operations.implementation_for(ValidateSafeDrop)
def validate_safe_drop_impl(operations, operation):
    """Check table is empty before allowing drop"""
    bind = operations.get_bind()
    result = bind.execute(f"SELECT COUNT(*) FROM {operation.table_name}")
    count = result.scalar()

    if count > 0:
        raise ValueError(
            f"Cannot drop table {operation.table_name}: "
            f"contains {count} rows. Manual intervention required."
        )

# In migration file
def upgrade():
    op.validate_safe_drop('old_table')
    op.drop_table('old_table')
```

**Strengths**:
- **Integration**: Works within migration workflow
- **Customizable**: Write validators for specific risk checks
- **Pre-Migration**: Runs before actual schema changes
- **Multi-Database**: SQLAlchemy connection works across databases
- **Contextual**: Access to both schema metadata and database state

**Limitations**:
- **Manual Implementation**: No built-in safety validators
- **Migration-Embedded**: Validation logic lives in migration files
- **No Standard Library**: Each project implements their own
- **Runtime Only**: Validates during migration execution, not at planning time

**Evidence from Practice**:
Alembic provides hooks and operation registration, but safety validation is application responsibility. Common pattern in production:

```python
# Standard pattern for safe migrations
def upgrade():
    # Check preconditions
    validate_no_data('legacy_table')
    validate_no_nulls('users', 'email')

    # Perform migration
    op.drop_table('legacy_table')
    op.alter_column('users', 'email', nullable=False)
```

**Best For**:
- Projects already using Alembic
- Custom validation logic needed
- Runtime validation acceptable
- Team willing to build safety infrastructure

### Option 2: Atlas Go (Cross-Language Tool)

**CLI Example**:
```bash
# Dry-run with pre-migration checks
atlas migrate apply \
  --url "postgres://localhost:5432/mydb" \
  --dry-run

# Built-in safety checks
atlas migrate lint \
  --dev-url "docker://postgres/15" \
  --dir "file://migrations"
```

**Strengths**:
- **Built-in Safety Checks**: Detects destructive operations automatically
- **Pre-Migration Analysis**: Validates before execution
- **Data-Aware**: Checks if operations would fail on existing data
- **Lint Mode**: Catch issues during migration authoring
- **Comprehensive**: DROP detection, constraint validation, type compatibility

**Limitations**:
- **Not Python**: Go-based tool, not a library
- **Separate Tool**: External to application code
- **CLI-Focused**: Limited programmatic API
- **Adoption Requirement**: New tool in stack

**Evidence from Documentation**:
> "Atlas provides a mechanism for defining pre-migration checks that run before applying the migration to analyze the state of the database and data to determine if the migration is safe to apply, and can prevent the migration from running if there's an issue."
>
> - Atlas Blog: Strategies for Reliable Migrations

**Best For**:
- Polyglot environments (not Python-only)
- CI/CD pipeline integration
- Teams wanting pre-built safety checks
- Willing to adopt external tool

### Option 3: Manual Pre-Migration Validation

**API Example**:
```python
from sqlalchemy import create_engine, text, inspect

class MigrationSafetyValidator:
    def __init__(self, engine):
        self.engine = engine
        self.inspector = inspect(engine)

    def validate_safe_to_drop_table(self, table_name):
        """Check table exists and is empty"""
        if table_name not in self.inspector.get_table_names():
            return True  # Already doesn't exist

        result = self.engine.execute(
            text(f"SELECT COUNT(*) FROM {table_name}")
        )
        count = result.scalar()

        if count > 0:
            raise ValueError(
                f"Cannot drop {table_name}: contains {count} rows"
            )

    def validate_safe_to_add_not_null(self, table_name, column_name):
        """Check column has no nulls before adding NOT NULL"""
        result = self.engine.execute(text(
            f"SELECT COUNT(*) FROM {table_name} "
            f"WHERE {column_name} IS NULL"
        ))
        count = result.scalar()

        if count > 0:
            raise ValueError(
                f"Cannot add NOT NULL to {table_name}.{column_name}: "
                f"{count} rows have NULL values"
            )

    def validate_safe_to_add_foreign_key(self, table, column, ref_table, ref_column):
        """Check all values exist in referenced table"""
        result = self.engine.execute(text(f"""
            SELECT COUNT(*)
            FROM {table} t
            LEFT JOIN {ref_table} r ON t.{column} = r.{ref_column}
            WHERE t.{column} IS NOT NULL AND r.{ref_column} IS NULL
        """))
        count = result.scalar()

        if count > 0:
            raise ValueError(
                f"Cannot add FK: {count} orphaned rows in {table}.{column}"
            )

    def validate_safe_to_reduce_column_size(self, table, column, new_size):
        """Check no data would be truncated"""
        result = self.engine.execute(text(f"""
            SELECT COUNT(*)
            FROM {table}
            WHERE LENGTH({column}) > {new_size}
        """))
        count = result.scalar()

        if count > 0:
            raise ValueError(
                f"Cannot reduce {table}.{column} to {new_size}: "
                f"{count} rows would be truncated"
            )

# Usage in migration
validator = MigrationSafetyValidator(engine)

def upgrade():
    # Validate before migrating
    validator.validate_safe_to_drop_table('legacy_users')
    validator.validate_safe_to_add_not_null('users', 'email')

    # Execute migration
    op.drop_table('legacy_users')
    op.alter_column('users', 'email', nullable=False)
```

**Strengths**:
- **Full Control**: Custom validation logic for any scenario
- **Python Native**: Pure Python, no external tools
- **Flexible Integration**: Use with any migration framework
- **Reusable**: Build library of validators for common cases

**Limitations**:
- **Manual Implementation**: Write all validation logic
- **Maintenance Burden**: Custom code to maintain and test
- **No Standard**: Each project implements differently
- **SQL Complexity**: Database-specific queries needed

**Best For**:
- Teams with specific validation requirements
- Want Python-native solution
- Willing to build and maintain validation library
- Need integration flexibility

### Option 4: Database-Specific Features

**PostgreSQL - Constraints with Validation**:
```sql
-- Add NOT NULL in steps to validate safely
ALTER TABLE users ALTER COLUMN email SET DEFAULT '';
UPDATE users SET email = '' WHERE email IS NULL;
ALTER TABLE users ALTER COLUMN email SET NOT NULL;

-- Add FK without immediate validation
ALTER TABLE orders
ADD CONSTRAINT fk_user
FOREIGN KEY (user_id) REFERENCES users(id)
NOT VALID;

-- Validate later (can be canceled if issues found)
ALTER TABLE orders VALIDATE CONSTRAINT fk_user;
```

**MySQL - Online DDL**:
```sql
-- Use ALGORITHM=INSTANT for safe additions
ALTER TABLE users
ADD COLUMN status VARCHAR(20) DEFAULT 'active',
ALGORITHM=INSTANT;

-- Check before modifying
SELECT COUNT(*) FROM users WHERE email IS NULL;
-- Only proceed if 0
```

**Strengths**:
- **Database-Native**: Leverage built-in safety features
- **Transactional**: Can rollback on validation failure
- **Online Operations**: Minimize locking for large tables
- **Validated Constraints**: PostgreSQL NOT VALID pattern

**Limitations**:
- **Database-Specific**: Different approaches per database
- **Manual SQL**: Harder to automate
- **Limited Scope**: Only what database provides
- **No Pre-Check**: Validation during execution, not before

**Best For**:
- Single database platform
- Large tables requiring online operations
- Leveraging database-specific optimizations

## Comparison Matrix

| Criterion | Alembic Custom | Atlas | Manual Validator | DB-Specific |
|-----------|----------------|-------|------------------|-------------|
| Python Native | Yes | No (Go) | Yes | SQL |
| Pre-Built Checks | No | Yes | No | Limited |
| Customization | High | Medium | Highest | Low |
| Multi-Database | Yes | Yes | Yes | No |
| Pre-Migration | Partial | Yes | Yes | No |
| Learning Curve | Medium | High | Low | Medium |
| Maintenance | Medium | Low | High | Low |
| Data-Aware | Manual | Yes | Manual | Manual |

## Recommendations

### Primary: Manual Pre-Migration Validator

**Rationale**:
1. **Python Native**: Pure Python solution, no external tools
2. **Flexible**: Customize for any validation scenario
3. **Reusable**: Build library once, use across projects
4. **Framework Agnostic**: Works with Alembic, Django, Flask-Migrate
5. **Pre-Migration**: Validates before execution

**Implementation Strategy**:

```python
# validators.py - reusable library
class MigrationSafetyValidator:
    """Reusable migration safety validation library"""

    def __init__(self, engine):
        self.engine = engine
        self.inspector = inspect(engine)

    def check_all(self, checks):
        """Run multiple validators, collect all errors"""
        errors = []
        for check in checks:
            try:
                check()
            except ValueError as e:
                errors.append(str(e))

        if errors:
            raise ValueError(
                "Migration safety validation failed:\n" +
                "\n".join(f"  - {e}" for e in errors)
            )

    # Core validators
    def validate_safe_to_drop_table(self, table_name):
        """Ensure table is empty before dropping"""
        # Implementation as shown above
        pass

    def validate_safe_to_add_not_null(self, table_name, column_name):
        """Ensure no nulls before adding NOT NULL"""
        pass

    def validate_safe_to_add_unique(self, table_name, column_name):
        """Ensure no duplicates before adding UNIQUE"""
        pass

    # Add more validators as needed...

# migrations/env.py
def run_migrations_online():
    """Run migrations with safety validation"""
    engine = engine_from_config(...)

    with engine.connect() as connection:
        # Create validator
        validator = MigrationSafetyValidator(engine)

        # Add validation context
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            validator=validator  # Make available in migrations
        )

        with context.begin_transaction():
            context.run_migrations()

# Individual migration file
def upgrade():
    # Access validator from context
    validator = op.get_context().config.attributes.get('validator')

    # Validate before migrating
    validator.check_all([
        lambda: validator.validate_safe_to_drop_table('old_users'),
        lambda: validator.validate_safe_to_add_not_null('users', 'email'),
    ])

    # Execute migration
    op.drop_table('old_users')
    op.alter_column('users', 'email', nullable=False)
```

**Confidence**: High (80%)

### Alternative: Atlas for Comprehensive Safety

**Use When**:
- Multi-language environment (not Python-only)
- Want pre-built safety checks without custom implementation
- CI/CD focused validation
- Team resources available to adopt new tool

**Integration Example**:
```yaml
# .github/workflows/migration-safety.yml
name: Migration Safety Check

on: [pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install Atlas
        run: |
          curl -sSf https://atlasgo.sh | sh
      - name: Lint Migrations
        run: |
          atlas migrate lint \
            --dev-url "docker://postgres/15" \
            --dir "file://migrations"
```

**Confidence**: Medium (70%) - excellent tool but requires adoption

### Not Recommended: Alembic Custom Operations Only

**Reason**: While Alembic supports custom operations, having validation logic scattered across migration files is less maintainable than a centralized validator library.

**Use Instead**: Manual validator library integrated with Alembic (combines both strengths).

### Hybrid Strategy: Defense in Depth

**Multi-Layer Validation**:

```python
# Layer 1: Static analysis during migration authoring
def analyze_migration_file(migration_path):
    """Parse migration file, detect obvious issues"""
    with open(migration_path) as f:
        content = f.read()

    issues = []
    if 'drop_table' in content:
        issues.append("Contains DROP TABLE - ensure table is empty")
    if 'nullable=False' in content:
        issues.append("Adds NOT NULL - ensure no nulls exist")

    return issues

# Layer 2: Pre-migration validation (runtime)
validator = MigrationSafetyValidator(engine)
validator.check_all([...])

# Layer 3: Database transaction safety
with engine.begin() as conn:
    # Migration runs in transaction
    # Rollback on any error
    pass

# Layer 4: Post-migration validation
def verify_migration_success():
    """Check expected schema state after migration"""
    inspector = inspect(engine)
    assert 'users' in inspector.get_table_names()
    assert not inspector.get_columns('users', 'email')[0]['nullable']
```

This provides maximum safety through multiple validation layers.

## Confidence Level

**High (75%)** - Manual validator library is the most practical Python-native solution.

**Evidence Quality**: Medium
- No standard Python library for migration safety exists
- Atlas documented as best-practice tool but not Python
- Manual validation patterns common in production but not standardized
- Database-specific features well-documented but limited scope

**Gap Identified**: Python ecosystem lacks a comprehensive, production-ready migration safety validation library. Opportunity for open-source contribution.
