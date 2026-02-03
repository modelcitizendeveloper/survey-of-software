# Use Case: Detect Schema Differences

## Pattern Definition

### Requirement Statement

**Need**: Compare two schema representations to identify structural differences - what tables, columns, constraints, or indexes exist in one but not the other, or have changed between versions.

**Why This Matters**: Applications need to:
- Detect schema drift between code models and database
- Compare staging vs production database schemas
- Validate migrations applied correctly
- Identify manual schema changes outside migration system
- Generate sync scripts to align schemas

### Input Parameters

| Parameter | Range | Impact |
|-----------|-------|--------|
| Comparison Type | Code-to-DB, DB-to-DB | Tool selection |
| Database Size | 10-1,000 tables | Performance requirements |
| Change Frequency | Daily vs quarterly | Automation needs |
| Difference Scope | Tables only vs full detail | Accuracy requirements |
| Output Format | Boolean match vs detailed diff | Integration complexity |

### Success Criteria

**Must Achieve**:
1. Detect added tables, removed tables, renamed tables
2. Identify added/removed/modified columns per table
3. Catch type changes (VARCHAR(50) → VARCHAR(100))
4. Find constraint differences (added/removed FK, unique, check)
5. Spot index changes (added/removed/modified)
6. Report nullable changes (NULL → NOT NULL)
7. Detect default value changes

**Performance Target**: <5 seconds for 100-table comparison

**Accuracy**: Zero false positives/negatives for structural differences

### Constraints

- Must distinguish between semantically equivalent representations (e.g., INT vs INTEGER)
- Should ignore irrelevant differences (comment changes if not tracked)
- Must handle schema naming variations across databases
- Should provide actionable diff output (not just "different")

## Library Fit Analysis

### Option 1: Alembic Autogenerate

**API Example**:
```python
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata
from sqlalchemy import MetaData, create_engine

# Define expected schema in code
metadata = MetaData()
# ... define tables via SQLAlchemy ORM or Core

# Compare to database
engine = create_engine('postgresql://...')
context = MigrationContext.configure(engine.connect())

diff = compare_metadata(context, metadata)

# Analyze differences
for change in diff:
    if change[0] == 'add_table':
        print(f"Table added: {change[1].name}")
    elif change[0] == 'remove_table':
        print(f"Table removed: {change[1].name}")
    elif change[0] == 'add_column':
        print(f"Column added: {change[3]} to {change[2]}")
```

**Strengths**:
- **Code-to-Database Comparison**: Primary use case - compare SQLAlchemy models to database
- **Comprehensive Detection**: Tables, columns, indexes, constraints, nullable, types, server defaults
- **Migration Generation**: Not just detection - produces migration scripts
- **Type Comparison**: Optional `compare_type` flag for detailed type checking
- **Default Comparison**: Optional `compare_server_default` for default value changes
- **Production-Tested**: Core Alembic feature, heavily used in production
- **Customizable**: Hooks to add custom comparison logic

**Limitations**:
- **Requires SQLAlchemy Models**: Must define expected schema in SQLAlchemy
- **Name Change Detection**: Detects renames as add+remove (manual editing needed)
- **One-Way Comparison**: Database → Models, not DB → DB directly
- **Type Equivalence**: May flag equivalent types as different (INT vs INTEGER)

**Evidence from Documentation**:
> "The autogenerate feature will inspect the current status of a database using SQLAlchemy's schema inspection capabilities, compare it to the current state of the database model as specified in Python, and generate a series of 'candidate' migrations."
>
> - Alembic Autogenerate Documentation

**What It Detects**:
- Table additions and removals ✓
- Column additions and removals ✓
- Nullable status changes ✓
- Indexes and explicitly-named unique constraints ✓
- Column type changes (with compare_type=True) ✓
- Server default changes (with compare_server_default=True) ✓

**What It Misses**:
- Column renames (shows as add+remove)
- Table renames (shows as add+remove)
- Check constraint changes (limited support)

**Best For**:
- ORM-based applications with SQLAlchemy models
- Migration generation workflow
- Code-driven schema expectations
- PostgreSQL, MySQL, SQLite support needed

### Option 2: migra (PostgreSQL-specific)

**API Example**:
```python
from migra import Migration

# Compare two PostgreSQL databases
m = Migration(
    'postgresql:///source_db',
    'postgresql:///target_db'
)

m.set_safety(False)  # Allow potentially destructive changes
m.add_all_changes()

# Get SQL to sync target to match source
print(m.sql)
```

**CLI Example**:
```bash
migra postgresql:///source postgresql:///target
```

**Strengths**:
- **Database-to-Database**: Direct comparison without code models
- **PostgreSQL-Native**: Understands Postgres-specific features (schemas, extensions, functions)
- **Bi-Directional**: Compare either direction
- **SQL Output**: Generates ALTER statements to sync
- **Rename Detection**: Better at distinguishing renames from add+remove
- **CLI Tool**: Easy integration into scripts/CI

**Limitations**:
- **PostgreSQL Only**: No MySQL, SQLite, or other database support
- **DEPRECATED Python Version**: Original djrobstep/migra repository marked deprecated
- **TypeScript Port**: Active version is @pgkit/migra (not Python)
- **No ORM Integration**: Standalone tool, not integrated with migration frameworks

**Evidence from Research**:
> "Migra magically figures out all the statements required to get from A to B. It compares two PostgreSQL database schemas and generates the SQL migration statements needed to transform one schema to match the other."
>
> - migra PyPI Description

**Status Warning**:
> "DEPRECATED: Like diff but for PostgreSQL schemas"
>
> - GitHub Repository Status

**Best For**:
- PostgreSQL-only environments
- Database-to-database comparison (no code models)
- CI/CD validation pipelines
- Schema sync operations

**Risk**: Deprecation means no active maintenance on Python version

### Option 3: sqlalchemy-diff

**API Example**:
```python
from sqlalchemydiff import compare

result = compare(
    'postgresql://user:pass@host/db1',
    'postgresql://user:pass@host/db2'
)

if result.is_match:
    print("Schemas are identical")
else:
    print("Differences found:")
    for error in result.errors:
        print(f"  {error}")
```

**Strengths**:
- **Database-to-Database**: Compare two live databases directly
- **Multi-Database**: Works with PostgreSQL, MySQL, SQLite
- **Simple API**: Boolean match + error list
- **Pure SQLAlchemy**: Uses Inspector underneath
- **Programmatic**: Python library, not CLI tool

**Limitations**:
- **Limited Output**: Only reports "different" with basic error messages
- **No Sync SQL**: Doesn't generate migration scripts
- **Last Updated 2021**: Low maintenance activity
- **Coarse Granularity**: Less detailed than Alembic or migra
- **No Customization**: Fixed comparison logic

**Evidence from Documentation**:
> "Comparing two schemas is easy - you can verify they are the same by calling result = compare(uri_left, uri_right) and checking if result.is_match is True or False."
>
> - sqlalchemy-diff Documentation

**Best For**:
- Simple boolean "are these the same?" checks
- Multi-database support needed
- Don't need detailed diff or sync SQL
- Testing/validation workflows

### Option 4: Manual Inspector Comparison

**API Example**:
```python
from sqlalchemy import inspect

def compare_schemas(engine1, engine2):
    insp1 = inspect(engine1)
    insp2 = inspect(engine2)

    tables1 = set(insp1.get_table_names())
    tables2 = set(insp2.get_table_names())

    added = tables2 - tables1
    removed = tables1 - tables2
    common = tables1 & tables2

    for table in common:
        cols1 = {c['name']: c for c in insp1.get_columns(table)}
        cols2 = {c['name']: c for c in insp2.get_columns(table)}
        # Compare column details...
```

**Strengths**:
- **Full Control**: Custom comparison logic for specific needs
- **Multi-Database**: SQLAlchemy Inspector supports all databases
- **No Dependencies**: Only requires SQLAlchemy
- **Customizable Output**: Format results any way needed

**Limitations**:
- **Manual Implementation**: Write all comparison logic yourself
- **Type Comparison Complexity**: Handling equivalent types is non-trivial
- **No Migration Generation**: Only detection, not sync SQL
- **Maintenance Burden**: Custom code to maintain

**Best For**:
- Unique comparison requirements not met by existing tools
- Need custom difference reporting format
- Want to embed comparison in larger workflow

## Comparison Matrix

| Criterion | Alembic | migra | sqlalchemy-diff | Manual |
|-----------|---------|-------|-----------------|--------|
| Code-to-DB | Excellent | N/A | N/A | Good |
| DB-to-DB | Workaround | Excellent | Good | Good |
| Multi-Database | Yes | PostgreSQL only | Yes | Yes |
| Detail Level | High | Highest | Low | Custom |
| SQL Generation | Yes | Yes | No | No |
| Rename Detection | Poor | Good | Poor | Custom |
| Active Maintenance | Excellent | Deprecated | Low | N/A |
| API Complexity | Medium | Low | Low | High |
| Customization | Hooks | Limited | None | Full |

## Recommendations

### Primary: Alembic Autogenerate (Code-to-Database)

**Use When**:
- Application uses SQLAlchemy ORM or Core
- Schema defined in Python code
- Need migration generation, not just detection
- Multi-database support required

**Example Workflow**:
```python
# In migrations/env.py or custom script
from alembic.autogenerate import compare_metadata

def detect_drift():
    context = MigrationContext.configure(engine.connect())
    diff = compare_metadata(context, target_metadata)

    if diff:
        print("Schema drift detected!")
        for change in diff:
            print(f"  {change}")
        return False
    return True

# Run in CI/CD
if not detect_drift():
    sys.exit(1)
```

**Confidence**: High (85%)

### Secondary: Manual Inspector (Database-to-Database)

**Use When**:
- Need to compare two live databases
- No SQLAlchemy models available
- PostgreSQL-only limitation of migra unacceptable
- Need custom comparison logic

**Example Workflow**:
```python
def compare_databases(uri1, uri2):
    """Compare two databases without code models"""
    engine1 = create_engine(uri1)
    engine2 = create_engine(uri2)

    insp1 = inspect(engine1)
    insp2 = inspect(engine2)

    # Custom comparison logic...
    differences = []

    # Table comparison
    tables1 = set(insp1.get_table_names())
    tables2 = set(insp2.get_table_names())

    if tables1 != tables2:
        differences.append({
            'type': 'tables',
            'added': tables2 - tables1,
            'removed': tables1 - tables2
        })

    return differences
```

**Confidence**: Medium (70%) - requires implementation effort

### Not Recommended: migra

**Reason**: Despite excellent feature set, deprecated status makes it risky for new projects.

**Exception**: If already using PostgreSQL and need database-to-database comparison, consider the TypeScript port @pgkit/migra or accept the Python deprecation risk for short-term use.

### Not Recommended: sqlalchemy-diff

**Reason**: Too limited - only boolean match without detailed diff or sync SQL. Manual Inspector implementation provides more value.

**Exception**: Quick validation checks where boolean "same or different" is sufficient.

## Hybrid Strategy

**Best of Both Worlds**:

```python
from alembic.autogenerate import compare_metadata
from sqlalchemy import inspect, MetaData

def compare_code_to_db(metadata, engine):
    """Alembic for code-to-database"""
    context = MigrationContext.configure(engine.connect())
    return compare_metadata(context, metadata)

def compare_db_to_db(engine1, engine2):
    """Manual Inspector for database-to-database"""
    # Reflect database1 into metadata
    metadata1 = MetaData()
    metadata1.reflect(bind=engine1)

    # Compare database2 against reflected metadata
    context = MigrationContext.configure(engine2.connect())
    return compare_metadata(context, metadata1)
```

This leverages Alembic's robust comparison logic for both scenarios.

## Confidence Level

**High (80%)** - Alembic autogenerate is the clear leader for code-to-database comparison, which is the most common use case.

**Medium (65%)** - Database-to-database comparison has no ideal Python solution post-migra deprecation. Manual implementation or hybrid approach needed.

**Evidence Quality**: Good
- Alembic extensively documented and battle-tested
- migra deprecation confirmed via GitHub
- sqlalchemy-diff limitations evident from minimal documentation
