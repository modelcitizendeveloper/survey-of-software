# SQLAlchemy Inspector (Built-in Reflection)

**Category:** Built-in Reflection API
**Package:** sqlalchemy.engine.reflection
**Date Evaluated:** December 4, 2025

## Overview

SQLAlchemy Inspector is the built-in reflection API for introspecting database schemas. It's part of SQLAlchemy Core and provides programmatic access to database metadata without requiring predefined ORM models.

## Popularity Metrics

- **Distribution:** Bundled with SQLAlchemy (no separate package)
- **SQLAlchemy Stars:** 9.5k+ GitHub stars
- **SQLAlchemy Downloads:** 80M+ monthly downloads (PyPI)
- **Status:** Actively maintained, core feature since SQLAlchemy 0.8

## Primary Use Case

Runtime database schema introspection for:
- Dynamic metadata discovery
- Database migration tools (used by Alembic)
- Schema validation and comparison
- Documentation generation

## Key Capabilities

### What It Does Well

1. **Comprehensive Reflection**
   - Tables, columns, data types
   - Primary keys, foreign keys
   - Indexes and unique constraints
   - Check constraints (database-dependent)
   - Views (basic support)

2. **Database Agnostic**
   - PostgreSQL, MySQL, SQLite, Oracle, SQL Server
   - Dialect-specific features supported
   - Consistent API across databases

3. **Programmatic Access**
   ```python
   from sqlalchemy import create_engine, inspect

   engine = create_engine('postgresql://...')
   inspector = inspect(engine)

   tables = inspector.get_table_names()
   columns = inspector.get_columns('users')
   pk = inspector.get_pk_constraint('users')
   fks = inspector.get_foreign_keys('users')
   indexes = inspector.get_indexes('users')
   ```

4. **Integration Ready**
   - Used by Alembic for autogenerate
   - Foundation for schema comparison tools
   - Powers MetaData.reflect()

## Limitations

1. **No Code Generation:** Returns data structures, doesn't generate ORM models
2. **No Comparison:** Single-point-in-time inspection only
3. **Limited View Support:** Basic view reflection, no view dependencies
4. **No Migration Generation:** Raw data only, no migration scripts

## When to Use

**Best For:**
- Building custom schema inspection tools
- Runtime schema validation
- Dynamic table access patterns
- Foundation for migration/comparison tools

**Not Suitable For:**
- Generating ORM model code (use sqlacodegen)
- Comparing schemas across environments (use sqlalchemy-diff)
- Creating migration scripts (use Alembic)

## Verdict

**Essential foundation tool.** Every SQLAlchemy schema tool builds on Inspector. Use directly when you need programmatic access to schema metadata. For higher-level tasks (code generation, migrations), use specialized tools that leverage Inspector underneath.
