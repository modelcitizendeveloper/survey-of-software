# Use Case: Multi-Database Support

## Pattern Definition

### Requirement Statement

**Need**: Use a single library/API to introspect schema across different database platforms (PostgreSQL, MySQL, SQLite, and potentially others) without writing database-specific code for each backend.

**Why This Matters**: Applications need to:
- Support multiple database backends (user choice)
- Migrate between database platforms
- Develop tools that work with any database
- Maintain single codebase for multi-tenant systems
- Provide database-agnostic APIs/libraries

### Input Parameters

| Parameter | Range | Impact |
|-----------|-------|--------|
| Database Platforms | 2-5 different systems | Abstraction complexity |
| Feature Parity | Same features vs subset | API design |
| Platform-Specific Features | Generic vs specialized | Capability limitations |
| Type Mapping | Simple vs complex types | Accuracy requirements |
| Schema Concepts | Tables only vs schemas/catalogs | Naming complexity |

### Success Criteria

**Must Achieve**:
1. Single API works across PostgreSQL, MySQL, SQLite (minimum)
2. Consistent return types and data structures
3. Handle equivalent types correctly (INT vs INTEGER)
4. Abstract database-specific naming (schema vs database)
5. Gracefully handle unsupported features
6. Clear documentation of platform differences

**Performance Target**: Consistent performance across databases (no 10x differences)

**Code Example Goal**:
```python
# Same code works for any database
def introspect_database(connection_uri):
    engine = create_engine(connection_uri)
    inspector = inspect(engine)

    tables = inspector.get_table_names()
    for table in tables:
        columns = inspector.get_columns(table)
        # Process columns uniformly
```

### Constraints

- Must handle databases with different schema concepts
- Should map types to common representation
- Cannot require database-specific code paths
- Must document limitations per platform
- Should work with dialect-specific extensions

## Library Fit Analysis

### Option 1: SQLAlchemy Inspector

**API Example (Multi-Database)**:
```python
from sqlalchemy import create_engine, inspect

def introspect_any_database(uri):
    """Works with PostgreSQL, MySQL, SQLite, Oracle, MSSQL"""
    engine = create_engine(uri)
    inspector = inspect(engine)

    # Same API across all databases
    tables = inspector.get_table_names()
    print(f"Found {len(tables)} tables")

    for table in tables:
        columns = inspector.get_columns(table)
        for col in columns:
            print(f"  {col['name']}: {col['type']}")

# Works with any database
introspect_any_database('postgresql://localhost/mydb')
introspect_any_database('mysql://localhost/mydb')
introspect_any_database('sqlite:///mydb.db')
introspect_any_database('oracle://localhost/mydb')
introspect_any_database('mssql://localhost/mydb')
```

**Supported Databases**:
- PostgreSQL (psycopg2, asyncpg)
- MySQL (pymysql, mysqlclient)
- SQLite (built-in)
- Oracle (cx_oracle)
- Microsoft SQL Server (pyodbc, pymssql)
- MariaDB (same as MySQL)
- CockroachDB (PostgreSQL protocol)
- Amazon Redshift (PostgreSQL protocol)

**Strengths**:
- **Comprehensive Database Support**: 8+ major databases
- **Consistent API**: Same methods work across all platforms
- **Type Abstraction**: SQLAlchemy types abstract database differences
- **Dialect System**: Clean extension point for new databases
- **Production-Tested**: Used in millions of projects
- **Active Development**: New database support added regularly

**How It Works**:
```python
# SQLAlchemy uses dialect pattern
engine = create_engine('postgresql://...')  # PostgreSQL dialect
engine = create_engine('mysql://...')       # MySQL dialect
engine = create_engine('sqlite://...')      # SQLite dialect

# Inspector delegates to dialect-specific implementation
inspector = inspect(engine)

# Same method, different SQL under the hood
tables = inspector.get_table_names()

# PostgreSQL: SELECT tablename FROM pg_tables WHERE schemaname='public'
# MySQL: SHOW TABLES
# SQLite: SELECT name FROM sqlite_master WHERE type='table'
```

**Type Mapping Example**:
```python
# PostgreSQL column: id SERIAL
# MySQL column: id INT AUTO_INCREMENT
# SQLite column: id INTEGER PRIMARY KEY

# All returned as:
{
    'name': 'id',
    'type': INTEGER(),
    'autoincrement': True,
    'primary_key': True
}
```

**Handling Schema Differences**:
```python
# PostgreSQL: schema.table
inspector.get_table_names(schema='public')

# MySQL: database.table (schema parameter maps to database)
inspector.get_table_names(schema='mydb')

# SQLite: no schema concept (all tables in main database)
inspector.get_table_names()  # schema parameter ignored
```

**Evidence from Documentation**:
> "The Inspector acts as a proxy to the reflection methods of the Dialect, providing a consistent interface as well as caching support for previously fetched metadata."
>
> - SQLAlchemy 2.0 Documentation

> "Each database has a slightly different understanding of the word 'schema'."
>
> - Stack Overflow SQLAlchemy Multi-Schema Discussion

**Limitations**:
- **Platform-Specific Features**: Not all databases support all methods
  - `get_temp_table_names()`: Only Oracle, PostgreSQL, SQLite
  - `get_view_definition()`: Database-specific SQL
- **Type Nuances**: Some types map imperfectly
  - PostgreSQL ARRAY → not available in MySQL
  - MySQL ENUM → different representation in PostgreSQL
- **Schema Concepts**: Terminology differs (schema vs catalog vs database)
- **Feature Detection**: No standard way to check "does this DB support X?"

**Best For**:
- Applications supporting multiple databases
- Database-agnostic tools and libraries
- Migration between platforms
- ORM-integrated workflows

### Option 2: Alembic Autogenerate (Multi-Database)

**API Example**:
```python
from alembic.migration import MigrationContext
from alembic.autogenerate import compare_metadata

# Works with any SQLAlchemy-supported database
def compare_schema_any_db(metadata, uri):
    engine = create_engine(uri)
    context = MigrationContext.configure(engine.connect())
    diff = compare_metadata(context, metadata)
    return diff

# Same code for all databases
compare_schema_any_db(metadata, 'postgresql://...')
compare_schema_any_db(metadata, 'mysql://...')
compare_schema_any_db(metadata, 'sqlite://...')
```

**Strengths**:
- **Built on SQLAlchemy**: Inherits multi-database support
- **Consistent Comparison**: Same diff format across databases
- **Migration Generation**: Database-specific DDL generated correctly
- **Type Handling**: Dialect-aware type comparison

**Limitations**:
- **Same as SQLAlchemy**: Platform-specific feature limitations
- **Type Comparison Complexity**: `compare_type` may flag false positives across databases
- **Database-Specific DDL**: Generated migrations not portable between databases

**Best For**:
- Schema comparison across different database types
- Generating platform-specific migrations
- ORM-based multi-database applications

### Option 3: Database-Specific Tools (Anti-Pattern)

**Example (PostgreSQL-only)**:
```python
# migra - PostgreSQL only
from migra import Migration
m = Migration('postgresql://...', 'postgresql://...')
# Does NOT work with MySQL, SQLite, etc.
```

**Example (MySQL-only)**:
```python
# mysql-schema-diff
import pymysql
conn = pymysql.connect(...)
# Only works with MySQL
```

**Limitations**:
- **Single Database**: No cross-platform support
- **Code Duplication**: Must implement for each database separately
- **Maintenance Burden**: Multiple codebases to maintain
- **Migration Pain**: Switching databases requires rewrite

**Why Not Recommended**:
Unless absolutely constrained to a single database forever, starting with database-specific tools creates technical debt.

**Exception**: When leveraging database-specific features that have no cross-platform equivalent (PostgreSQL full-text search, MySQL JSON functions).

## Platform-Specific Considerations

### PostgreSQL
**Strengths**:
- Full schema support (PUBLIC, custom schemas)
- Rich type system (ARRAY, JSON, UUID, etc.)
- Advanced constraints (CHECK, EXCLUDE)
- Inheritance (table inheritance)

**SQLAlchemy Support**: Excellent
- All features supported
- PostgreSQL-specific types available
- Schema introspection robust

### MySQL
**Strengths**:
- Database-centric (database ~ schema)
- ENUM types
- AUTO_INCREMENT
- Storage engines (InnoDB, MyISAM)

**SQLAlchemy Support**: Excellent
- Full introspection support
- MySQL-specific types (ENUM, YEAR, etc.)
- Handle MySQL peculiarities (SHOW syntax)

**Quirks**:
- Schema parameter maps to database name
- Case sensitivity varies by platform (Linux vs Windows)
- Storage engine metadata not in standard API

### SQLite
**Strengths**:
- Simple, file-based
- No separate server
- Fast for small databases

**SQLAlchemy Support**: Good
- Basic introspection works well
- Type affinity (flexible typing) handled

**Limitations**:
- No schema concept (single database)
- Limited ALTER TABLE support (SQLAlchemy works around)
- No DROP COLUMN until SQLite 3.35.0

### Oracle
**Strengths**:
- Enterprise features
- Schemas per user
- Advanced constraints

**SQLAlchemy Support**: Good (with cx_Oracle)
- Full introspection
- Oracle-specific types

**Limitations**:
- Commercial database (licensing)
- Complex connection strings

### Microsoft SQL Server
**Strengths**:
- Schema support (dbo, custom)
- Windows integration
- Enterprise features

**SQLAlchemy Support**: Good (with pyodbc)
- Full introspection
- MSSQL-specific types

**Limitations**:
- Verbose connection strings
- Platform dependency (Windows-centric)

## Comparison Matrix

| Feature | PostgreSQL | MySQL | SQLite | Oracle | MSSQL |
|---------|------------|-------|--------|--------|-------|
| SQLAlchemy Inspector | Excellent | Excellent | Good | Good | Good |
| Schema Concept | schema.table | database.table | No schemas | schema.table | schema.table |
| Type Richness | Highest | High | Basic | High | High |
| ALTER TABLE | Full | Full | Limited | Full | Full |
| Introspection Speed | Fast | Fast | Fastest | Medium | Medium |
| Platform-Specific Tools | Many | Some | Few | Few | Few |

## Recommendations

### Primary: SQLAlchemy Inspector

**Rationale**:
1. **Comprehensive Database Support**: PostgreSQL, MySQL, SQLite, Oracle, MSSQL, and more
2. **Single API**: One codebase works across all platforms
3. **Production-Ready**: Battle-tested in millions of projects
4. **Type Abstraction**: Handles type differences gracefully
5. **Active Development**: Continuous improvement, new databases added

**Implementation Pattern**:
```python
from sqlalchemy import create_engine, inspect
from typing import Dict, List

class DatabaseIntrospector:
    """Database-agnostic schema introspection"""

    def __init__(self, uri: str):
        self.engine = create_engine(uri)
        self.inspector = inspect(self.engine)
        self.dialect_name = self.engine.dialect.name

    def get_all_tables(self, schema: str = None) -> List[str]:
        """Get tables - works across all databases"""
        if self.dialect_name == 'sqlite' and schema:
            # SQLite doesn't support schema parameter
            return self.inspector.get_table_names()
        return self.inspector.get_table_names(schema=schema)

    def get_table_structure(self, table_name: str, schema: str = None) -> Dict:
        """Get complete table structure"""
        return {
            'columns': self.inspector.get_columns(table_name, schema=schema),
            'primary_key': self.inspector.get_pk_constraint(table_name, schema=schema),
            'foreign_keys': self.inspector.get_foreign_keys(table_name, schema=schema),
            'indexes': self.inspector.get_indexes(table_name, schema=schema),
        }

    def supports_feature(self, feature: str) -> bool:
        """Check if database supports specific feature"""
        feature_support = {
            'schemas': self.dialect_name in ('postgresql', 'oracle', 'mssql'),
            'temp_tables': hasattr(self.inspector, 'get_temp_table_names'),
            'arrays': self.dialect_name == 'postgresql',
            'enums': self.dialect_name in ('postgresql', 'mysql'),
        }
        return feature_support.get(feature, False)

# Works with any database
db = DatabaseIntrospector('postgresql://localhost/mydb')
db = DatabaseIntrospector('mysql://localhost/mydb')
db = DatabaseIntrospector('sqlite:///mydb.db')
```

**Confidence**: High (95%)

### Secondary: Alembic for Schema Comparison

**Rationale**:
Extends SQLAlchemy Inspector with schema comparison and migration generation while maintaining multi-database support.

**Use When**:
- Need schema comparison, not just introspection
- Generate database-specific migrations
- ORM-based application with migrations

**Confidence**: High (90%)

### Not Recommended: Database-Specific Tools

**Exception Criteria**:
Only use database-specific tools when:
1. **Single Database Commitment**: 100% certain will never support other databases
2. **Unique Features**: Need features unavailable in SQLAlchemy (rare)
3. **Performance Critical**: Database-specific tool 10x+ faster (measure first)

**Example Valid Exception**: PostgreSQL-only application using advanced features (LISTEN/NOTIFY, full-text search, PostGIS) where generic abstraction adds no value.

## Handling Platform Differences

### Pattern 1: Feature Detection

```python
def introspect_with_fallback(inspector, table_name):
    """Safely introspect with feature detection"""
    result = {
        'columns': inspector.get_columns(table_name),
        'indexes': inspector.get_indexes(table_name),
    }

    # Only try if database might support it
    if hasattr(inspector, 'get_check_constraints'):
        try:
            result['check_constraints'] = inspector.get_check_constraints(table_name)
        except NotImplementedError:
            result['check_constraints'] = []

    return result
```

### Pattern 2: Dialect-Specific Handling

```python
def get_schema_name(engine):
    """Get appropriate schema/database name per dialect"""
    if engine.dialect.name == 'postgresql':
        return 'public'
    elif engine.dialect.name == 'mysql':
        return engine.url.database
    elif engine.dialect.name == 'sqlite':
        return None  # No schema concept
    else:
        return 'dbo'  # MSSQL, Oracle default
```

### Pattern 3: Type Normalization

```python
from sqlalchemy import types

def normalize_column_type(column_info):
    """Normalize type across databases"""
    col_type = column_info['type']

    if isinstance(col_type, types.Integer):
        return 'integer'
    elif isinstance(col_type, types.String):
        return f'string({col_type.length or "max"})'
    elif isinstance(col_type, types.DateTime):
        return 'datetime'
    else:
        return str(col_type)
```

## Confidence Level

**Very High (95%)** - SQLAlchemy Inspector is the definitive solution for multi-database schema introspection.

**Evidence Quality**: Excellent
- Explicit documentation of multi-database support
- Proven production usage across all major databases
- Clear dialect system for extensibility
- Active maintenance with new database support added regularly
- Industry standard for Python database abstraction
