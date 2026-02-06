# Use Case: Introspect Database Schema

## Pattern Definition

### Requirement Statement

**Need**: Programmatically read an existing database's structure to discover all tables, columns, data types, constraints, indexes, and foreign key relationships.

**Why This Matters**: Applications need to:
- Understand databases they don't control
- Validate expected schema exists
- Build dynamic UIs based on structure
- Generate documentation
- Support multi-tenant systems with varying schemas

### Input Parameters

| Parameter | Range | Impact |
|-----------|-------|--------|
| Database Size | 5-10,000 tables | Performance, memory usage |
| Column Count | 10-500 per table | API ergonomics, speed |
| Constraint Complexity | None to many FKs/indexes | Completeness requirements |
| Database Type | PostgreSQL, MySQL, SQLite | Dialect compatibility |
| Schema Access | Single vs multi-schema | API complexity |

### Success Criteria

**Must Achieve**:
1. List all tables in target schema/database
2. For each table, retrieve all columns with accurate types
3. Identify primary keys correctly
4. Detect foreign key relationships with correct references
5. Find indexes including unique constraints
6. Return results in structured, programmatically accessible format

**Performance Target**: <1 second for typical database (50 tables, 1000 total columns)

### Constraints

- Read-only operation (no database modification)
- Must work with databases lacking write permissions
- Should handle databases created by other tools/ORMs
- Type mapping must be accurate for target database

## Library Fit Analysis

### Option 1: SQLAlchemy Inspector

**API Example**:
```python
from sqlalchemy import create_engine, inspect

engine = create_engine('postgresql://user:pass@localhost/db')
inspector = inspect(engine)

# List all tables
tables = inspector.get_table_names()

# Introspect specific table
columns = inspector.get_columns('users')
pk = inspector.get_pk_constraint('users')
fks = inspector.get_foreign_keys('users')
indexes = inspector.get_indexes('users')
```

**Strengths**:
- **Complete Coverage**: Handles tables, columns, types, PKs, FKs, indexes, unique constraints
- **Multi-Database**: Works across PostgreSQL, MySQL, SQLite, Oracle, SQL Server
- **Caching**: Inspector caches results to avoid redundant queries
- **Type Accuracy**: Returns SQLAlchemy type objects with database-specific details
- **Low-Level Control**: Direct access to schema metadata without ORM overhead

**Limitations**:
- **Performance on Large Schemas**: GitHub issue #4379 documents 15 minutes for 3,300 tables (MSSQL), 45 minutes for 18,000 tables (PostgreSQL)
- **No Batch Operations**: Iterates table-by-table rather than bulk queries
- **Schema Iteration**: For multi-schema databases, must specify schema parameter explicitly

**Evidence from Documentation**:
> "The Inspector acts as a proxy to the reflection methods of the Dialect, providing a consistent interface as well as caching support for previously fetched metadata."
>
> - SQLAlchemy 2.0 Documentation

**Best For**:
- Medium-sized databases (< 500 tables)
- Need complete metadata (not just table names)
- Require multi-database compatibility
- Want consistent API across backends

### Option 2: SQLAlchemy Table Reflection

**API Example**:
```python
from sqlalchemy import MetaData, Table, create_engine

engine = create_engine('postgresql://user:pass@localhost/db')
metadata = MetaData()

# Reflect single table
users = Table('users', metadata, autoload_with=engine)

# Access reflected structure
for column in users.columns:
    print(f"{column.name}: {column.type}")

# Reflect all tables
metadata.reflect(bind=engine)
for table_name in metadata.tables:
    table = metadata.tables[table_name]
```

**Strengths**:
- **ORM Integration**: Reflected tables usable in queries immediately
- **Relationship Detection**: Can infer ForeignKey relationships
- **Metadata Object**: Centralized schema representation
- **Selective Reflection**: Choose specific tables vs entire schema

**Limitations**:
- **Higher Overhead**: Creates full Table objects, not just metadata
- **Same Performance Issues**: Uses Inspector internally
- **Less Direct**: More abstraction than Inspector for pure introspection

**Evidence from Documentation**:
> "Table objects can be instructed to load information about themselves from the corresponding database schema object already existing within the database through a process called reflection."
>
> - SQLAlchemy Reflection Documentation

**Best For**:
- Need to query reflected tables immediately
- Want ORM-style Table objects
- Selective introspection (few specific tables)

### Option 3: Direct SQL Queries to Information Schema

**API Example**:
```python
# PostgreSQL
result = engine.execute("""
    SELECT table_name, column_name, data_type
    FROM information_schema.columns
    WHERE table_schema = 'public'
    ORDER BY table_name, ordinal_position
""")

# MySQL
result = engine.execute("""
    SELECT table_name, column_name, column_type
    FROM information_schema.columns
    WHERE table_schema = DATABASE()
""")
```

**Strengths**:
- **Maximum Performance**: Single query for all tables/columns
- **Full Control**: Custom filtering, ordering, aggregation
- **No Abstraction Overhead**: Direct database results

**Limitations**:
- **Database-Specific SQL**: Different queries for PostgreSQL vs MySQL vs SQLite
- **Manual Type Parsing**: String types need conversion to structured format
- **Incomplete Metadata**: Information schema varies by database
- **No Caching**: Repeat queries hit database each time

**Best For**:
- Performance-critical scenarios with large schemas
- Single database platform (no multi-DB requirement)
- Need specific metadata subset (not full introspection)

## Comparison Matrix

| Criterion | Inspector | Table Reflection | Direct SQL |
|-----------|-----------|------------------|------------|
| Coverage | Complete | Complete | Partial |
| Multi-Database | Excellent | Excellent | Poor |
| Performance (small) | Good (0.1-1s) | Good (0.2-2s) | Excellent (<0.1s) |
| Performance (large) | Poor (minutes) | Poor (minutes) | Good (seconds) |
| API Complexity | Low | Medium | High |
| Type Accuracy | Excellent | Excellent | Manual |
| Caching | Built-in | Built-in | Manual |
| ORM Integration | Medium | Excellent | None |

## Recommendation

### Primary Choice: SQLAlchemy Inspector

**Rationale**:
1. **Complete Coverage**: Handles all metadata types (tables, columns, constraints, indexes)
2. **Multi-Database Support**: Single API works across PostgreSQL, MySQL, SQLite
3. **Type Accuracy**: Proper SQLAlchemy type mapping for each database
4. **Production-Ready**: Widely used, well-tested, actively maintained
5. **Caching**: Avoids redundant queries during single session

**When to Use Inspector**:
- Medium-sized databases (< 1,000 tables)
- Need complete schema metadata
- Multi-database compatibility required
- Standard introspection workflow

### Alternative: Direct SQL for Large Schemas

**Rationale**:
For databases with 1,000+ tables, Inspector's performance issues become critical. Direct SQL queries to information_schema provide 10-100x speedup.

**Trade-off**: Lose multi-database abstraction, gain performance.

**Hybrid Approach**:
```python
def fast_table_list(engine):
    """Fast table enumeration via direct SQL"""
    if engine.dialect.name == 'postgresql':
        return engine.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    elif engine.dialect.name == 'mysql':
        return engine.execute("SHOW TABLES")
    elif engine.dialect.name == 'sqlite':
        return engine.execute("SELECT name FROM sqlite_master WHERE type='table'")

def introspect_table(engine, table_name):
    """Detailed introspection via Inspector for specific table"""
    inspector = inspect(engine)
    return {
        'columns': inspector.get_columns(table_name),
        'pk': inspector.get_pk_constraint(table_name),
        'fks': inspector.get_foreign_keys(table_name),
        'indexes': inspector.get_indexes(table_name)
    }
```

This combines fast enumeration with accurate detailed introspection.

## Confidence Level

**High (90%)** - SQLAlchemy Inspector is the clear best-fit for this use case.

**Evidence Quality**: Excellent
- Official documentation with comprehensive examples
- Known performance issues documented in GitHub
- Clear API design for introspection workflow
- Wide production usage
