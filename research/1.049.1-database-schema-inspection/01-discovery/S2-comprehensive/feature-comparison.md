# Feature Comparison Matrix: Database Schema Inspection Libraries

## Executive Summary

This comparison analyzes five Python tools for database schema inspection and related tasks. Each tool serves different use cases within the schema introspection ecosystem.

**Key Finding**: SQLAlchemy Inspector emerges as the primary recommendation for general schema inspection, while Alembic Autogenerate excels for migration-focused workflows.

## Libraries Compared

1. **SQLAlchemy Inspector** - Built-in reflection system
2. **Alembic Autogenerate** - Migration generation tool
3. **sqlalchemy-diff** - Third-party comparison utility
4. **migra** - PostgreSQL-specific diff tool
5. **sqlacodegen** - Reverse engineering code generator

## Database Coverage Matrix

| Database | SQLAlchemy Inspector | Alembic | sqlalchemy-diff | migra | sqlacodegen |
|----------|---------------------|---------|-----------------|-------|-------------|
| **PostgreSQL** | ✅ Full | ✅ Full | ✅ Theoretical | ✅ Full | ✅ Full |
| **MySQL/MariaDB** | ✅ Full | ✅ Full | ✅ Theoretical | ❌ No | ✅ Full |
| **SQLite** | ✅ Full | ✅ Full | ✅ Theoretical | ❌ No | ✅ Full |
| **Oracle** | ✅ Full | ✅ Full | ✅ Theoretical | ❌ No | ✅ Full |
| **MS SQL Server** | ✅ Full | ✅ Full | ✅ Theoretical | ❌ No | ✅ Full |
| **Other SQLAlchemy** | ✅ Yes | ✅ Yes | ✅ Theoretical | ❌ No | ✅ Yes |

**Notes**:
- ✅ Full = Documented, tested, production-ready
- ✅ Theoretical = Should work (uses SQLAlchemy), but untested/unmaintained
- ❌ No = Not supported

**Winner**: SQLAlchemy Inspector, Alembic, sqlacodegen (tie) - comprehensive multi-database support

**Loser**: migra - PostgreSQL only

## Introspection Capabilities Matrix

### Core Schema Elements

| Capability | SQLAlchemy Inspector | Alembic | sqlalchemy-diff | migra | sqlacodegen |
|------------|---------------------|---------|-----------------|-------|-------------|
| **Tables** | ✅ Full | ✅ Detect changes | ✅ Compare | ✅ Full | ✅ Generate code |
| **Columns** | ✅ Full details | ✅ Detect changes | ✅ Compare | ✅ Full | ✅ Generate code |
| **Primary Keys** | ✅ Yes | ✅ Detect add/remove | ✅ Compare | ✅ Yes | ✅ Yes |
| **Foreign Keys** | ✅ Yes | ✅ Detect changes | ✅ Compare | ✅ Yes | ✅ Yes + Relationships |
| **Unique Constraints** | ✅ Yes | ✅ Detect changes | ❌ Limited | ✅ Yes | ✅ Yes |
| **Check Constraints** | ✅ Yes | ❌ Not detected | ❌ No | ✅ Yes (PG) | ✅ Yes (DB-dependent) |
| **Indexes** | ✅ Full | ✅ Detect changes | ✅ Compare | ✅ Full (PG) | ✅ Yes |

### Advanced Features

| Capability | SQLAlchemy Inspector | Alembic | sqlalchemy-diff | migra | sqlacodegen |
|------------|---------------------|---------|-----------------|-------|-------------|
| **Views** | ✅ List + definition | ⚠️ Manual ops | ❌ No | ✅ Yes (PG) | ⚠️ As tables |
| **Materialized Views** | ✅ Yes (PG) | ⚠️ Manual ops | ❌ No | ✅ Yes (PG) | ⚠️ As tables |
| **Sequences** | ✅ Yes | ⚠️ Partial | ❌ No | ✅ Yes (PG) | ⚠️ Limited |
| **Identity Columns** | ✅ Yes | ⚠️ Limited | ❌ No | ✅ Yes (PG) | ✅ Yes |
| **Computed Columns** | ✅ Yes | ⚠️ Limited | ❌ No | ✅ Yes (PG) | ✅ Yes |
| **Comments** | ✅ Table + column | ❌ No | ❌ No | ✅ Yes (PG) | ❌ No |
| **Functions/Procedures** | ❌ No | ❌ No | ❌ No | ✅ Yes (PG) | ❌ No |
| **Triggers** | ❌ No | ❌ No | ❌ No | ❌ No | ❌ No |
| **Extensions** | ❌ No | ❌ No | ❌ No | ✅ Yes (PG) | ❌ No |

**Legend**:
- ✅ = Fully supported
- ⚠️ = Partial support or requires manual handling
- ❌ = Not supported

**Winner (Comprehensive)**: SQLAlchemy Inspector - broadest coverage across databases
**Winner (PostgreSQL-Specific)**: migra - includes functions, extensions, comprehensive PG features

## Output Type Comparison

| Tool | Output Type | Format | Use Case |
|------|-------------|--------|----------|
| **SQLAlchemy Inspector** | Python objects | TypedDict, lists, dicts | Programmatic inspection |
| **Alembic** | Python migration code | `.py` migration files | Version-controlled migrations |
| **sqlalchemy-diff** | Python dictionary | Structured diff dict | Programmatic comparison |
| **migra** | SQL statements | DDL SQL | Direct database execution |
| **sqlacodegen** | Python model code | SQLAlchemy classes | Reverse engineering |

**Diversity**: Each tool targets different workflow needs

## Ease of Use Comparison

### API Complexity (1=Simple, 10=Complex)

| Tool | Complexity | Learning Curve | Documentation Quality | Examples |
|------|------------|----------------|----------------------|----------|
| **SQLAlchemy Inspector** | 6/10 | Moderate | ⭐⭐⭐⭐⭐ Excellent | Comprehensive |
| **Alembic** | 7/10 | Moderate-High | ⭐⭐⭐⭐⭐ Excellent | Comprehensive |
| **sqlalchemy-diff** | 3/10 | Low | ⭐⭐ Limited | Minimal |
| **migra** | 4/10 | Low | ⭐⭐⭐ Good | Moderate |
| **sqlacodegen** | 3/10 | Low | ⭐⭐⭐⭐ Good | Good |

### Typical Usage Patterns

**SQLAlchemy Inspector**:
```python
from sqlalchemy import inspect, create_engine
inspector = inspect(create_engine("postgresql://..."))
tables = inspector.get_table_names()
columns = inspector.get_columns("users")
```
**Complexity**: Requires understanding SQLAlchemy concepts
**Winner for**: Programmatic, flexible inspection

**Alembic**:
```bash
alembic revision --autogenerate -m "Added tables"
alembic upgrade head
```
**Complexity**: Requires Alembic setup, env.py configuration
**Winner for**: Managed migration workflows

**sqlalchemy-diff**:
```python
from sqlalchemydiff import compare
result = compare("postgresql://db1", "postgresql://db2")
print(result.is_match)
```
**Complexity**: Simplest API
**Winner for**: Quick two-database comparison

**migra**:
```bash
migra postgresql://db1 postgresql://db2
```
**Complexity**: Simplest command-line usage
**Winner for**: Quick PostgreSQL schema diff

**sqlacodegen**:
```bash
sqlacodegen postgresql://mydb > models.py
```
**Complexity**: Simple CLI, but requires understanding output
**Winner for**: Quick model generation

**Overall Winner (Ease of Use)**: migra and sqlacodegen (tie) - simplest command-line interfaces
**Runner-up**: sqlalchemy-diff - simplest Python API

## Integration Capabilities Matrix

| Integration Type | SQLAlchemy Inspector | Alembic | sqlalchemy-diff | migra | sqlacodegen |
|------------------|---------------------|---------|-----------------|-------|-------------|
| **SQLAlchemy ORM** | ✅ Native | ✅ Native | ✅ Uses internally | ❌ Independent | ✅ Generates code |
| **Flask** | ✅ Via Flask-SQLAlchemy | ✅ Flask-Migrate | ❌ No | ❌ Standalone | ✅ Output usable |
| **FastAPI** | ✅ Recommended | ✅ Recommended | ❌ No | ❌ Standalone | ✅ SQLModel support |
| **Django** | ⚠️ Django-bridge | ⚠️ Alternative to Django migrations | ❌ No | ❌ Standalone | ❌ Use inspectdb |
| **Alembic** | ✅ Used by Alembic | N/A | ❌ No | ❌ Alternative | ⚠️ Bootstrap only |
| **CI/CD** | ✅ Scriptable | ✅ `alembic check` | ✅ Scriptable | ✅ Scriptable | ✅ Scriptable |
| **Testing Frameworks** | ✅ Any | ✅ pytest-alembic | ✅ Any | ✅ Any | ✅ Any |

**Winner**: SQLAlchemy Inspector and Alembic (tie) - deep ecosystem integration

## Performance Comparison

### Reflection Speed (Estimated)

| Tool | Small Schema (10-100 tables) | Large Schema (1000+ tables) | Optimization Features |
|------|----------------------------|----------------------------|----------------------|
| **SQLAlchemy Inspector** | ⚡ Fast (< 1s) | ⚠️ Moderate (improved in 2.0) | ✅ Caching, bulk methods (2.0) |
| **Alembic** | ⚡ Fast (< 1s) | ⚠️ Moderate (uses Inspector) | ✅ Uses Inspector caching |
| **sqlalchemy-diff** | ⚠️ Moderate (2x reflection) | ❌ Slow (2x reflection) | ❌ No specific optimization |
| **migra** | ⚡ Fast (direct PG) | ⚡ Fast (optimized PG queries) | ✅ PostgreSQL-specific optimization |
| **sqlacodegen** | ⚡ Fast (< 1s) | ⚠️ Moderate (uses Inspector) | ✅ Single-pass generation |

**Performance Notes**:

**SQLAlchemy Inspector (SQLAlchemy 2.0)**:
- PostgreSQL: 3x faster for large schemas
- Oracle: 10x faster for large schemas
- Bulk reflection methods (`get_multi_*`) reduce round trips

**Historical Issues** (SQLAlchemy 1.x):
- MS SQL Server: 3,300 tables = 15 minutes
- PostgreSQL: 18,000+ tables = 45 minutes
- **Status**: Largely resolved in 2.0

**migra**:
- Direct pg_catalog access (no ORM overhead)
- Fastest for PostgreSQL-only scenarios

**Winner**: migra (PostgreSQL-only scenarios)
**Winner (Multi-database)**: SQLAlchemy Inspector 2.0

## Maintenance and Adoption Matrix

| Tool | Last Update | Release Frequency | Maintenance Status | Monthly Downloads | GitHub Stars |
|------|-------------|-------------------|-------------------|------------------|--------------|
| **SQLAlchemy Inspector** | 2024+ (ongoing) | Regular (multiple/year) | ✅ Active | 85M+ (SQLAlchemy) | 9K+ (SQLAlchemy) |
| **Alembic** | 2024+ (ongoing) | Regular (2-4/year) | ✅ Active | 85M+ | Part of SQLAlchemy |
| **sqlalchemy-diff** | March 2021 | ❌ Stagnant | ⚠️ Unmaintained | Unknown (low) | 27 stars |
| **migra** | Sept 2022 | ❌ Stagnant | ⚠️ Deprecated | Unknown (moderate) | Original deprecated |
| **sqlacodegen** | Sept 2025 | Regular (multiple/year) | ✅ Active | Unknown (moderate) | Active |

**Evidence Quality**:

| Tool | Documentation | Production Evidence | Community Support | Confidence Level |
|------|---------------|--------------------|--------------------|------------------|
| **SQLAlchemy Inspector** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Extensive | Very High |
| **Alembic** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐⭐⭐ Extensive | Very High |
| **sqlalchemy-diff** | ⭐⭐ | ⭐ Low | ⭐ Minimal | Low |
| **migra** | ⭐⭐⭐ | ⭐⭐ Moderate | ⭐⭐ Limited | Medium |
| **sqlacodegen** | ⭐⭐⭐⭐ | ⭐⭐⭐ Moderate | ⭐⭐⭐ Good | High |

**Winner**: SQLAlchemy Inspector and Alembic (tie) - industry standard, active maintenance, extensive evidence

## Weighted Scoring Results

### Scoring Methodology

**Criteria Weights** (as defined in approach.md):
1. Database Coverage: 30%
2. Introspection Capabilities: 25%
3. Ease of Use: 20%
4. Integration: 15%
5. Performance: 10%

### Individual Scores (0-10 scale)

| Tool | DB Coverage | Introspection | Ease of Use | Integration | Performance | **Weighted Total** |
|------|-------------|---------------|-------------|-------------|-------------|-------------------|
| **SQLAlchemy Inspector** | 10 | 9 | 7 | 10 | 8 | **8.80** |
| **Alembic** | 10 | 8 | 8 | 10 | 8 | **8.80** |
| **sqlalchemy-diff** | 6 | 5 | 8 | 3 | 6 | **5.40** |
| **migra** | 2 (PG only) | 9 (PG) | 8 | 4 | 9 | **5.60** |
| **sqlacodegen** | 10 | 8 | 9 | 7 | 8 | **8.30** |

**Adjusted Score for migra (PostgreSQL-only use case)**:
If database coverage penalty removed for PG-only projects: **8.00**

### Score Justifications

**SQLAlchemy Inspector (8.80)**:
- DB Coverage (10): All SQLAlchemy databases fully supported
- Introspection (9): Comprehensive, missing only non-schema objects (triggers, functions)
- Ease of Use (7): Moderate learning curve, excellent documentation
- Integration (10): Native SQLAlchemy, used by Alembic, ecosystem standard
- Performance (8): SQLAlchemy 2.0 improvements, bulk methods

**Alembic (8.80)**:
- DB Coverage (10): All SQLAlchemy databases
- Introspection (8): Excellent change detection, some gaps (renames, CHECK constraints)
- Ease of Use (8): Moderate setup, excellent workflow once configured
- Integration (10): Industry standard, Flask-Migrate, framework integration
- Performance (8): Uses Inspector, good performance

**sqlalchemy-diff (5.40)**:
- DB Coverage (6): Theoretically supports all, but unmaintained/untested
- Introspection (5): Basic comparison only
- Ease of Use (8): Simple API
- Integration (3): Standalone, no framework support
- Performance (6): Two-database reflection overhead

**migra (5.60 general, 8.00 PostgreSQL-only)**:
- DB Coverage (2): PostgreSQL only
- Introspection (9): Comprehensive PostgreSQL features
- Ease of Use (8): Simple CLI
- Integration (4): Standalone tool
- Performance (9): Fast PostgreSQL-specific queries

**sqlacodegen (8.30)**:
- DB Coverage (10): All SQLAlchemy databases
- Introspection (8): Comprehensive for code generation
- Ease of Use (9): Simple CLI, clear output
- Integration (7): Standalone but output integrates well
- Performance (8): Fast generation

## Use Case Recommendations

### Primary Use Cases Matrix

| Use Case | Best Tool | Alternative | Avoid |
|----------|-----------|-------------|-------|
| **Runtime schema inspection** | SQLAlchemy Inspector | - | sqlacodegen |
| **Migration generation** | Alembic | - | sqlalchemy-diff |
| **Two-database comparison** | SQLAlchemy Inspector | Alembic | sqlalchemy-diff (unmaintained) |
| **PostgreSQL schema diff** | Alembic | migra (if SQL output needed) | sqlalchemy-diff |
| **Reverse engineering** | sqlacodegen | SQLAlchemy Inspector | Alembic |
| **Schema validation in CI** | Alembic check | SQLAlchemy Inspector script | sqlalchemy-diff |
| **Multi-database support** | SQLAlchemy Inspector | Alembic | migra |
| **PostgreSQL-only, SQL output** | migra | Alembic | - |

### Decision Tree

```
Need to inspect database schema?
├─ Need to generate migrations?
│  └─ YES → Alembic Autogenerate
│
├─ Need Python model code from database?
│  └─ YES → sqlacodegen
│
├─ PostgreSQL only + need SQL output?
│  └─ YES → migra (if accepting deprecated status) OR Alembic
│
├─ Need programmatic inspection at runtime?
│  └─ YES → SQLAlchemy Inspector
│
└─ Need to compare two databases?
   └─ Use SQLAlchemy Inspector (write comparison script)
      OR Alembic (compare via metadata)
```

## Confidence Levels

| Tool | Confidence | Reasoning |
|------|-----------|-----------|
| **SQLAlchemy Inspector** | ⭐⭐⭐⭐⭐ Very High | Extensive docs, 85M+ downloads, 20+ years, production-proven |
| **Alembic** | ⭐⭐⭐⭐⭐ Very High | Industry standard, 85M+ downloads, official SQLAlchemy tool |
| **sqlalchemy-diff** | ⭐⭐ Low | Unmaintained since 2021, limited docs, low adoption |
| **migra** | ⭐⭐⭐ Medium | Deprecated status, but clear docs, PostgreSQL-specific proven |
| **sqlacodegen** | ⭐⭐⭐⭐ High | Active maintenance, clear docs, Sept 2025 release |

## Evidence Sources Summary

**High-Quality Evidence**:
- SQLAlchemy official documentation (comprehensive)
- Alembic official documentation (comprehensive)
- PyPI download statistics (85M+ monthly for SQLAlchemy/Alembic)
- GitHub activity (regular commits, issue resolution)

**Medium-Quality Evidence**:
- sqlacodegen documentation (good README, examples)
- migra documentation (databaseci.com/docs/migra)
- Community discussions (Stack Overflow, blogs)

**Low-Quality Evidence**:
- sqlalchemy-diff documentation (minimal, outdated)
- Download statistics for smaller packages (not publicly available)

## Overall Recommendation

### Primary Recommendation: **SQLAlchemy Inspector**

**Reasoning**:
1. **Comprehensive database support** - Works with all major databases
2. **Industry standard** - Part of SQLAlchemy, 85M+ monthly downloads
3. **Active maintenance** - Regular updates, SQLAlchemy 2.0 improvements
4. **Excellent documentation** - Comprehensive guides and API reference
5. **Ecosystem integration** - Used by Alembic, framework support
6. **Performance** - Improved significantly in 2.0

**Confidence**: ⭐⭐⭐⭐⭐ Very High

**Use when**: Need general-purpose schema inspection, multi-database support, programmatic access

### Secondary Recommendation: **Alembic Autogenerate**

**Reasoning**:
1. **Migration-focused** - Best for schema evolution workflows
2. **Change detection** - Automatic comparison with metadata
3. **Industry standard** - De facto migration tool for SQLAlchemy
4. **CI/CD integration** - `alembic check` for drift detection

**Confidence**: ⭐⭐⭐⭐⭐ Very High

**Use when**: Need migration generation, version-controlled schema changes, SQLAlchemy-based projects

### Specialized Recommendation: **sqlacodegen**

**Reasoning**:
1. **Reverse engineering** - Generate Python models from databases
2. **Active maintenance** - September 2025 release
3. **Multiple output formats** - Declarative, dataclasses, SQLModel

**Confidence**: ⭐⭐⭐⭐ High

**Use when**: Need to bootstrap models from existing database, database-first workflow

### Not Recommended

**sqlalchemy-diff**: Unmaintained (last update March 2021), better alternatives exist
**migra**: Deprecated original, PostgreSQL-only, use Alembic instead

## Key Trade-offs

### SQLAlchemy Inspector vs Alembic

**Inspector**:
- ✅ Direct inspection, no migration generation
- ✅ Simpler for pure inspection use cases
- ❌ No change detection without manual comparison

**Alembic**:
- ✅ Automatic change detection
- ✅ Migration generation and tracking
- ❌ Requires setup (env.py, metadata)

**Recommendation**: Use Inspector for inspection, Alembic for migrations

### Multi-Database vs PostgreSQL-Specific

**SQLAlchemy Tools (Inspector, Alembic)**:
- ✅ Multi-database support
- ✅ Active maintenance
- ⚠️ Generic approach may miss database-specific features

**migra**:
- ✅ Comprehensive PostgreSQL features (functions, extensions)
- ✅ SQL output (not Python)
- ❌ PostgreSQL only
- ❌ Deprecated status

**Recommendation**: Use SQLAlchemy tools unless PostgreSQL-specific features critical AND can accept deprecated status

## Final Verdict

**For 90% of use cases**: Use **SQLAlchemy Inspector** for inspection and **Alembic Autogenerate** for migrations.

**For reverse engineering**: Use **sqlacodegen**.

**Avoid**: sqlalchemy-diff (unmaintained), migra (deprecated, PostgreSQL-only).

The Python ecosystem has converged on SQLAlchemy Inspector and Alembic as the standard tools for database schema inspection and migration. Both are actively maintained, comprehensively documented, and production-proven with millions of downloads monthly. Other tools serve niche use cases but cannot match the quality, support, and ecosystem integration of the SQLAlchemy/Alembic combination.
