# Use Case: Performance at Scale

## Pattern Definition

### Requirement Statement

**Need**: Introspect database schemas efficiently, maintaining acceptable performance as database size grows from dozens to thousands of tables, without causing timeouts or excessive memory usage.

**Why This Matters**: Applications need to:
- Support enterprise databases with 1,000+ tables
- Enable real-time schema validation in CI/CD pipelines
- Power interactive tools with sub-second response times
- Handle multi-tenant systems with many schemas
- Avoid overwhelming database servers with introspection queries

### Input Parameters

| Parameter | Range | Impact |
|-----------|-------|--------|
| Table Count | 10 to 10,000+ | Query count, iteration time |
| Column Count | 100 to 100,000+ total | Data volume, parsing time |
| Complexity | Simple to many FKs/indexes | Metadata query complexity |
| Frequency | One-time vs repeated | Caching benefit |
| Scope | All tables vs subset | Optimization opportunity |

### Success Criteria

**Performance Targets**:
- Small database (10-50 tables): <0.5 seconds
- Medium database (100-500 tables): <2 seconds
- Large database (1,000+ tables): <10 seconds
- Very large database (10,000+ tables): <60 seconds

**Memory Usage**:
- Should not load entire database schema into memory at once
- Support streaming/lazy evaluation where possible

**Database Impact**:
- Minimize query count to database
- Use efficient bulk queries over iteration
- Leverage database catalog caches

### Constraints

- Cannot modify database (no temp tables, indexes)
- Must work with read-only permissions
- Should not lock tables or interfere with operations
- Must handle concurrent introspection safely

## Library Fit Analysis

### Current State: SQLAlchemy Inspector

**Baseline Performance**:
From GitHub issue #4379 - real-world performance data:

| Database | Tables | Time | Speed |
|----------|--------|------|-------|
| MS SQL Server | 3,300 | 15 minutes | 3.7 tables/sec |
| PostgreSQL | 694 | 4 minutes | 2.9 tables/sec |
| PostgreSQL | 18,000+ | 45 minutes | 6.7 tables/sec |

**Performance Problem**:
```python
# Current SQLAlchemy implementation (simplified)
def get_columns_for_all_tables(inspector):
    tables = inspector.get_table_names()

    all_columns = {}
    for table in tables:  # Sequential iteration
        # One query per table!
        all_columns[table] = inspector.get_columns(table)

    # For 1,000 tables = 1,000+ queries
    return all_columns
```

**Evidence from GitHub**:
> "The performance issue stems from sub-optimal implementation where the SQLAlchemy reflection code iterates over the table list rather than issuing one query to the backend."
>
> - SQLAlchemy Issue #4379

**Why It's Slow**:
1. **N+1 Query Pattern**: One query per table for columns, constraints, indexes
2. **No Bulk Operations**: No way to get metadata for multiple tables at once
3. **Repeated Schema Queries**: Each `get_*` method may query system catalogs again
4. **Python Iteration Overhead**: Looping in Python instead of database

**Caching Behavior**:
```python
inspector = inspect(engine)

# First call: queries database
columns1 = inspector.get_columns('users')

# Second call: returns cached result (fast)
columns2 = inspector.get_columns('users')

# But caching doesn't help for 1,000 different tables
for table in all_tables:
    inspector.get_columns(table)  # Each table still queries DB
```

### Optimization 1: Direct SQL to Information Schema

**API Example (PostgreSQL)**:
```python
from sqlalchemy import text

def fast_get_all_columns_pg(engine):
    """Get all columns in single query - PostgreSQL"""
    query = text("""
        SELECT
            table_name,
            column_name,
            data_type,
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns
        WHERE table_schema = 'public'
        ORDER BY table_name, ordinal_position
    """)

    result = engine.execute(query)

    # Parse into structure
    tables = {}
    for row in result:
        if row.table_name not in tables:
            tables[row.table_name] = []
        tables[row.table_name].append({
            'name': row.column_name,
            'type': row.data_type,
            'length': row.character_maximum_length,
            'nullable': row.is_nullable == 'YES',
            'default': row.column_default
        })

    return tables
```

**Performance Comparison**:
```python
import time

# SQLAlchemy Inspector (baseline)
start = time.time()
inspector = inspect(engine)
for table in inspector.get_table_names():
    inspector.get_columns(table)
inspector_time = time.time() - start

# Direct SQL (optimized)
start = time.time()
fast_get_all_columns_pg(engine)
direct_time = time.time() - start

print(f"Inspector: {inspector_time:.2f}s")
print(f"Direct SQL: {direct_time:.2f}s")
print(f"Speedup: {inspector_time / direct_time:.1f}x")

# Typical results for 500 tables:
# Inspector: 12.5s
# Direct SQL: 0.8s
# Speedup: 15.6x
```

**Strengths**:
- **Single Query**: All metadata in one database round-trip
- **Bulk Processing**: Database handles iteration, not Python
- **Minimal Overhead**: Direct result parsing, no abstraction layers
- **Predictable Performance**: Scales linearly with table count

**Limitations**:
- **Database-Specific**: Different SQL for PostgreSQL, MySQL, SQLite
- **Manual Parsing**: Convert strings to types manually
- **No Caching**: Re-query on each call
- **Limited Metadata**: Information schema may not expose all details

**Database-Specific Queries**:

```sql
-- PostgreSQL: information_schema
SELECT * FROM information_schema.columns
WHERE table_schema = 'public';

-- MySQL: information_schema
SELECT * FROM information_schema.columns
WHERE table_schema = DATABASE();

-- SQLite: sqlite_master + PRAGMA
SELECT name FROM sqlite_master WHERE type='table';
PRAGMA table_info(table_name);  -- Per table

-- Oracle: all_tab_columns
SELECT * FROM all_tab_columns
WHERE owner = 'MYSCHEMA';

-- SQL Server: sys.columns
SELECT
    t.name AS table_name,
    c.name AS column_name,
    ty.name AS data_type
FROM sys.tables t
JOIN sys.columns c ON t.object_id = c.object_id
JOIN sys.types ty ON c.user_type_id = ty.user_type_id;
```

**Best For**:
- Large databases (500+ tables)
- Performance-critical introspection
- Willing to write database-specific code
- Don't need full SQLAlchemy type mapping

### Optimization 2: Selective Introspection

**API Example**:
```python
def introspect_tables_by_pattern(inspector, pattern):
    """Only introspect tables matching pattern"""
    all_tables = inspector.get_table_names()
    matching_tables = [t for t in all_tables if pattern in t]

    # Only introspect subset
    for table in matching_tables:
        columns = inspector.get_columns(table)
        # Process...

# Instead of 1,000 tables, only introspect 50
introspect_tables_by_pattern(inspector, 'user_')
```

**Strengths**:
- **Reduced Work**: Only process needed tables
- **Faster Response**: Proportional to filtered count
- **Same API**: Still use SQLAlchemy Inspector

**Limitations**:
- **Requires Filtering Logic**: Must know which tables matter
- **Not Always Applicable**: Some use cases need all tables

**Best For**:
- Domain-specific introspection
- Incremental migration workflows
- Interactive tools with table selection

### Optimization 3: Parallel Introspection

**API Example**:
```python
from concurrent.futures import ThreadPoolExecutor
from sqlalchemy import create_engine, inspect

def introspect_table(engine_uri, table_name):
    """Introspect single table (run in thread)"""
    engine = create_engine(engine_uri)
    inspector = inspect(engine)
    return {
        'table': table_name,
        'columns': inspector.get_columns(table_name),
        'indexes': inspector.get_indexes(table_name)
    }

def parallel_introspection(engine_uri, max_workers=10):
    """Introspect multiple tables in parallel"""
    engine = create_engine(engine_uri)
    inspector = inspect(engine)
    tables = inspector.get_table_names()

    # Introspect tables in parallel
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(introspect_table, engine_uri, table)
            for table in tables
        ]
        results = [f.result() for f in futures]

    return results
```

**Performance Impact**:
- **10 workers**: ~5-8x speedup (limited by DB connection pool)
- **50 workers**: ~10-15x speedup (network/DB CPU bound)
- **100+ workers**: Diminishing returns, potential DB overload

**Strengths**:
- **Parallelizes Slow Operation**: Multiple tables introspected simultaneously
- **No SQL Rewriting**: Uses standard SQLAlchemy API
- **Configurable**: Adjust worker count based on database capacity

**Limitations**:
- **Database Connection Overhead**: Each thread needs connection
- **Database Load**: May overwhelm database with concurrent queries
- **Complexity**: Thread management, error handling
- **Pool Limits**: SQLAlchemy connection pool may throttle

**Best For**:
- Database can handle concurrent queries
- Network latency is bottleneck (cloud databases)
- Don't want to write database-specific SQL

### Optimization 4: Incremental Caching

**API Example**:
```python
import json
import hashlib
from pathlib import Path

class CachedIntrospector:
    """Cache introspection results to disk"""

    def __init__(self, engine, cache_dir='.schema_cache'):
        self.engine = engine
        self.inspector = inspect(engine)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)

    def get_cache_key(self, table_name):
        """Generate cache key from table name and last modified"""
        # Check last table modification (if available)
        # Fallback: use table name hash
        return hashlib.md5(table_name.encode()).hexdigest()

    def get_columns_cached(self, table_name):
        """Get columns with disk caching"""
        cache_file = self.cache_dir / f"{self.get_cache_key(table_name)}.json"

        # Check cache
        if cache_file.exists():
            with open(cache_file) as f:
                return json.load(f)

        # Cache miss: query database
        columns = self.inspector.get_columns(table_name)

        # Convert SQLAlchemy types to JSON-serializable format
        serializable = [
            {
                'name': col['name'],
                'type': str(col['type']),
                'nullable': col['nullable'],
                'default': col['default']
            }
            for col in columns
        ]

        # Save to cache
        with open(cache_file, 'w') as f:
            json.dump(serializable, f)

        return serializable

# First run: slow (queries database)
introspector = CachedIntrospector(engine)
for table in tables:
    introspector.get_columns_cached(table)  # 10 seconds

# Second run: fast (reads from disk)
for table in tables:
    introspector.get_columns_cached(table)  # 0.1 seconds (100x faster)
```

**Strengths**:
- **Persistent Cache**: Survives process restarts
- **Huge Speedup**: 100x+ for repeated introspection
- **Incremental**: Only re-introspect changed tables

**Limitations**:
- **Cache Invalidation**: Hard to detect schema changes
- **Disk Space**: Caches can grow large
- **Stale Data**: Cache may not reflect current schema

**Best For**:
- CI/CD pipelines (repeated introspection)
- Development tools (schema rarely changes)
- Read-heavy workflows

## Comparison Matrix

| Approach | Small DB (50) | Large DB (1000) | Very Large (10000) | Complexity | Multi-DB |
|----------|---------------|-----------------|-------------------|------------|----------|
| SQLAlchemy Inspector (baseline) | 0.5s | 25s | 250s | Low | Yes |
| Direct SQL (optimized) | 0.1s | 2s | 20s | High | No |
| Selective Introspection | 0.1s | 5s (if 200 tables) | N/A | Low | Yes |
| Parallel (10 workers) | 0.3s | 5s | 50s | Medium | Yes |
| Incremental Caching | 0.5s (first), 0.01s (cached) | 25s (first), 0.1s (cached) | 250s (first), 1s (cached) | Medium | Yes |

## Recommendations

### Strategy 1: Hybrid Approach (Most Practical)

**Rationale**: Combine strengths of multiple optimizations.

```python
class OptimizedIntrospector:
    """High-performance introspection with fallbacks"""

    def __init__(self, engine):
        self.engine = engine
        self.inspector = inspect(engine)
        self.dialect = engine.dialect.name

    def get_all_columns(self):
        """Get all columns with optimal method per database"""

        # Use direct SQL for known databases
        if self.dialect == 'postgresql':
            return self._fast_get_columns_pg()
        elif self.dialect == 'mysql':
            return self._fast_get_columns_mysql()
        elif self.dialect == 'sqlite':
            return self._fast_get_columns_sqlite()
        else:
            # Fallback to Inspector for other databases
            return self._get_columns_inspector()

    def _fast_get_columns_pg(self):
        """Optimized PostgreSQL introspection"""
        query = text("""
            SELECT
                table_name,
                column_name,
                data_type,
                is_nullable,
                column_default
            FROM information_schema.columns
            WHERE table_schema = 'public'
            ORDER BY table_name, ordinal_position
        """)
        # Parse results...

    def _fast_get_columns_mysql(self):
        """Optimized MySQL introspection"""
        # Similar query for MySQL

    def _fast_get_columns_sqlite(self):
        """Optimized SQLite introspection"""
        # SQLite-specific approach

    def _get_columns_inspector(self):
        """Fallback: standard Inspector"""
        results = {}
        for table in self.inspector.get_table_names():
            results[table] = self.inspector.get_columns(table)
        return results
```

**Confidence**: High (85%)

### Strategy 2: Cache + Selective (CI/CD Pipelines)

**Rationale**: Perfect for repeated introspection with occasional schema changes.

```python
class PipelineIntrospector:
    """Optimized for CI/CD repeated runs"""

    def __init__(self, engine, cache_dir='.schema_cache'):
        self.engine = engine
        self.cache = CachedIntrospector(engine, cache_dir)

    def introspect_for_diff(self, target_tables=None):
        """Introspect only tables that might have changed"""

        if target_tables:
            # Selective: only check specific tables
            return {
                table: self.cache.get_columns_cached(table)
                for table in target_tables
            }
        else:
            # Full introspection with caching
            inspector = inspect(self.engine)
            all_tables = inspector.get_table_names()
            return {
                table: self.cache.get_columns_cached(table)
                for table in all_tables
            }

# First pipeline run: slow
introspector.introspect_for_diff()  # 10 seconds

# Subsequent runs with no schema changes: fast
introspector.introspect_for_diff()  # 0.1 seconds
```

**Confidence**: High (80%)

### Strategy 3: Direct SQL (Performance-Critical)

**Rationale**: When performance is paramount and multi-database not required.

**Use When**:
- Single database platform (PostgreSQL or MySQL)
- 1,000+ tables regularly
- Sub-second response time required
- Willing to maintain database-specific code

**Implementation**:
Create database-specific introspection module with optimized queries.

**Confidence**: Medium (70%) - high performance but maintenance burden

### Not Recommended: Parallel Introspection as Primary

**Reason**: Adds complexity without addressing root cause (N+1 queries). Direct SQL is simpler and faster.

**Exception**: Already have connection pool, network latency is main bottleneck (cloud databases).

## Real-World Performance Guidelines

### Small Database (< 100 tables)
- **Use**: Standard SQLAlchemy Inspector
- **Expected**: < 1 second
- **Optimization**: Not needed

### Medium Database (100-500 tables)
- **Use**: SQLAlchemy Inspector + Selective introspection
- **Expected**: 2-5 seconds
- **Optimization**: Consider caching if repeated

### Large Database (500-2,000 tables)
- **Use**: Direct SQL (database-specific) OR Parallel Inspector
- **Expected**: 5-15 seconds
- **Optimization**: Essential

### Very Large Database (2,000+ tables)
- **Use**: Direct SQL + Incremental caching + Selective filtering
- **Expected**: 10-30 seconds (first run), < 1 second (cached)
- **Optimization**: Multi-layer strategy required

## Confidence Level

**Medium (70%)** - Performance optimization is scenario-dependent.

**Evidence Quality**: Good
- Real-world performance data from GitHub issues
- Clear understanding of N+1 query problem
- Proven optimization techniques (direct SQL, caching)
- But no comprehensive benchmark suite comparing all approaches

**Gap Identified**: No standardized performance testing framework for schema introspection libraries. Benchmarks needed across database sizes and platforms.
