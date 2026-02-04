# S1 Rapid Discovery: Database Schema Inspection Libraries

## Executive Summary

**Top 3 Candidates:**
1. **SQLAlchemy Inspector** - Industry standard, built-in introspection for all SQLAlchemy dialects
2. **Alembic Autogenerate** - Migration-focused schema comparison, built on Inspector
3. **sqlacodegen** - Reverse engineering tool for code generation from schemas

**Key Differentiators:**
- **Introspection**: SQLAlchemy Inspector (read-only schema examination)
- **Comparison**: Alembic Autogenerate, migra (schema diffing for migrations)
- **Code Generation**: sqlacodegen, Django inspectdb (ORM model creation)

**Critical Finding**: The landscape splits into three distinct use cases rather than one unified solution. SQLAlchemy Inspector is the foundational layer that other tools build upon.

---

## Library Profiles

### 1. SQLAlchemy Inspector (`sqlalchemy.inspect`)

**Maintenance Status:** Actively maintained (latest release 2.0.44, October 2025)

**Database Coverage:**
- PostgreSQL, MySQL, SQLite, Oracle, MS SQL Server
- Any database with SQLAlchemy dialect support
- Dialect-agnostic with backend-specific implementations

**Key Capabilities:**
- Tables: `get_table_names()`, `get_temp_table_names()`
- Columns: `get_columns()` with type information
- Indexes: `get_indexes()`
- Constraints: Foreign keys, primary keys, unique constraints
- Views: `get_view_names()`, `get_view_definition()`
- Sequences, schemas, materialized views (dialect-dependent)

**API Quality:**
- Excellent official documentation (SQLAlchemy 2.0 docs)
- Comprehensive API reference
- Extensive examples and tutorials
- Part of core SQLAlchemy, extremely well-documented

**Ecosystem Position:**
- 11.1k GitHub stars (SQLAlchemy)
- Industry standard for Python database work
- Foundation for Alembic, sqlacodegen, and other tools

**License:** MIT

**Pros:**
- Built into SQLAlchemy, no extra dependencies
- Production-ready, battle-tested
- Supports all major databases
- Caching support for performance
- Consistent interface across dialects

**Cons:**
- Read-only introspection (no comparison logic)
- Some methods unsupported by certain dialects (e.g., temp tables)
- Database-specific types returned (requires dialect awareness)

**Quick Verdict:** **MUST INCLUDE** - Foundation layer for all database introspection work in Python.

---

### 2. Alembic Autogenerate (`alembic.autogenerate`)

**Maintenance Status:** Actively maintained (latest release 1.17.1, 2024-2025)

**Database Coverage:**
- PostgreSQL, MySQL, SQLite, Oracle, MS SQL Server
- Inherits SQLAlchemy dialect support
- Dialect-specific migration operations

**Key Capabilities:**
- Schema comparison: `compare_metadata()` - compares MetaData vs database
- Migration generation: `produce_migrations()` - creates migration scripts
- Detects: Added/removed tables, columns, indexes, constraints
- Generates: DDL operations (CREATE, ALTER, DROP)

**API Quality:**
- Excellent documentation (Alembic 1.17.1 docs)
- Comprehensive autogenerate guide
- Cookbook with advanced patterns
- Clear limitations documented

**Ecosystem Position:**
- Part of Alembic migration framework
- Industry standard for database migrations
- Used by Flask-Migrate, SQLAlchemy-Migrate
- Maintained by same author as SQLAlchemy (Mike Bayer)

**License:** MIT

**Pros:**
- Purpose-built for schema comparison
- Generates migration scripts automatically
- Handles complex changes (constraints, indexes)
- Extensible comparison hooks
- Production-proven

**Cons:**
- Not perfect - manual review required
- Cannot detect: Table renames, column renames (shows as add/drop)
- Some constraint types unsupported (CHECK, EXCLUDE)
- Requires MetaData models (not pure DB-to-DB comparison)

**Quick Verdict:** **MUST INCLUDE** - Best-in-class for migration-oriented schema comparison.

---

### 3. sqlalchemy-diff

**Maintenance Status:** ABANDONED (last commit March 2021, 3+ years dormant)

**Database Coverage:**
- Any SQLAlchemy-supported database
- Built on SQLAlchemy Inspector

**Key Capabilities:**
- DB-to-DB schema comparison: `compare(uri_left, uri_right)`
- Returns diff structure with `is_match` boolean
- Identifies schema differences between databases

**API Quality:**
- Basic documentation on ReadTheDocs
- Limited examples
- Small API surface

**Ecosystem Position:**
- Created by student.com
- GitHub: gianchub/sqlalchemy-diff
- Limited adoption
- No PyPI download stats available

**License:** Apache 2.0

**Pros:**
- Simple API for DB-to-DB comparison
- No model definitions required

**Cons:**
- Abandoned (no updates since 2021)
- Incompatible with SQLAlchemy 2.0 (likely)
- Limited feature set
- No community support

**Quick Verdict:** **ELIMINATE** - Abandoned, superseded by Alembic autogenerate.

---

### 4. migra

**Maintenance Status:** DEPRECATED (Python version officially deprecated)

**Database Coverage:**
- PostgreSQL only (PostgreSQL >= 9)
- Highly PostgreSQL-specific

**Key Capabilities:**
- Pure PostgreSQL schema diff
- Generates SQL migration scripts
- DB-to-DB comparison (no models required)
- Detects: Tables, columns, indexes, constraints, views, sequences

**API Quality:**
- Good documentation (for deprecated version)
- CLI-focused tool
- Python library API available

**Ecosystem Position:**
- GitHub: djrobstep/migra (marked DEPRECATED)
- Had strong community interest (Hacker News discussions)
- TypeScript port available (maintained alternative)
- Alternatives: pg-schema-diff (Stripe), Tusker, postgres_migrator

**License:** Not specified in search results

**Pros:**
- PostgreSQL-native (uses pg_catalog)
- No ORM models required
- Direct SQL diff output
- Accurate for PostgreSQL-specific features

**Cons:**
- Python version DEPRECATED
- PostgreSQL-only (not multi-database)
- Known issues with DDL generation (ADD/DROP vs RENAME)
- No longer maintained

**Quick Verdict:** **ELIMINATE** - Deprecated, PostgreSQL-only. Use TypeScript port or pg-schema-diff if PostgreSQL-specific tool needed.

---

### 5. sqlacodegen

**Maintenance Status:** Actively maintained (latest release 3.1.1, September 2024)

**Database Coverage:**
- PostgreSQL, MySQL, SQLite, Oracle
- Any SQLAlchemy-supported database
- Special support: PostgreSQL pgvector extension

**Key Capabilities:**
- Reverse engineering: Database schema → SQLAlchemy models
- Output formats: Declarative classes, Table objects, dataclasses
- Detects: Tables, columns, relationships, foreign keys
- Generation options: Inflect naming, joined-table inheritance, bidirectional relationships

**API Quality:**
- Good PyPI documentation
- Command-line focused
- Clear usage examples
- Active GitHub discussions

**Ecosystem Position:**
- GitHub: agronholm/sqlacodegen (2.2k stars)
- Well-known in SQLAlchemy community
- Forks: flask-sqlacodegen, sqlacodegen-v2 (for SQLAlchemy 2.0)
- Author: Alex Grönholm (maintainer of several Python projects)

**License:** MIT

**Pros:**
- Actively maintained (2024 releases)
- Multi-database support
- Flexible output formats
- Good for bootstrapping ORM models
- CLI tool with library API

**Cons:**
- Code generation focus (not introspection/comparison)
- Generated code requires manual review
- Self-referential relationships use `_reverse` suffix
- Maintainer has limited availability

**Quick Verdict:** **INCLUDE** - Best tool for reverse engineering models, complementary use case.

---

### 6. Django inspectdb

**Maintenance Status:** Actively maintained (part of Django core)

**Database Coverage:**
- PostgreSQL, MySQL, SQLite, Oracle, MS SQL
- Any Django-supported database backend

**Key Capabilities:**
- Introspection: Database schema → Django models
- Command: `python manage.py inspectdb`
- Detects: Tables, columns, foreign keys
- Options: --database flag, table filtering

**API Quality:**
- Excellent Django documentation
- Well-documented limitations
- Extensive tutorials and examples

**Ecosystem Position:**
- Part of Django core framework
- Used by millions of developers
- Maintained by Django Software Foundation
- Industry standard for Django projects

**License:** BSD

**Pros:**
- Django ecosystem integration
- Production-ready, well-tested
- Creates Django ORM models
- Supports all Django database backends

**Cons:**
- Django-specific (requires Django framework)
- Creates unmanaged models (`managed = False`)
- Limited foreign key detection (PostgreSQL + specific MySQL)
- Not a standalone library
- Code generation only (not introspection API)

**Quick Verdict:** **ELIMINATE** - Django-specific, not general-purpose. Relevant only if already using Django.

---

## Comparison Matrix

| Library | DB Coverage | Introspection | Comparison | Code Gen | Active | Verdict |
|---------|------------|---------------|------------|----------|--------|---------|
| **SQLAlchemy Inspector** | All SQLAlchemy dialects | Yes (comprehensive) | No | No | Yes (2025) | TOP CHOICE |
| **Alembic Autogenerate** | All SQLAlchemy dialects | Yes (via Inspector) | Yes (MetaData vs DB) | Yes (migrations) | Yes (2025) | TOP CHOICE |
| **sqlalchemy-diff** | All SQLAlchemy dialects | No | Yes (DB vs DB) | No | No (2021) | ELIMINATED |
| **migra** | PostgreSQL only | Yes (PostgreSQL) | Yes (DB vs DB) | Yes (SQL) | No (deprecated) | ELIMINATED |
| **sqlacodegen** | All SQLAlchemy dialects | Yes (via Inspector) | No | Yes (ORM models) | Yes (2024) | INCLUDE |
| **Django inspectdb** | Django backends | Yes (Django) | No | Yes (Django models) | Yes (Django core) | ELIMINATED |

---

## Top 3 Candidates

### 1. SQLAlchemy Inspector (`sqlalchemy.inspect`)

**Why it made the cut:**
- **Foundation layer**: Every other tool builds on this
- **Industry standard**: 11.1k stars, part of core SQLAlchemy
- **Comprehensive introspection**: Tables, columns, indexes, constraints, views
- **Multi-database**: Works with any SQLAlchemy dialect (PostgreSQL, MySQL, SQLite, Oracle, MSSQL)
- **Production-ready**: Actively maintained, latest release October 2025
- **No extra dependencies**: Built into SQLAlchemy

**Use case:** Direct database introspection for validation, documentation, or custom tooling.

---

### 2. Alembic Autogenerate (`alembic.autogenerate`)

**Why it made the cut:**
- **Schema comparison**: Purpose-built to compare MetaData vs database schema
- **Migration generation**: Automatically generates migration scripts
- **Production-proven**: Industry standard for database migrations
- **Actively maintained**: Latest release 1.17.1, same maintainer as SQLAlchemy
- **Extensible**: Hooks for custom comparison logic
- **Best-in-class**: No better alternative for migration-focused comparison

**Use case:** Migration generation, schema drift detection, CI/CD validation.

---

### 3. sqlacodegen

**Why it made the cut:**
- **Reverse engineering**: Best tool for generating ORM models from existing databases
- **Actively maintained**: 2024 releases, 2.2k GitHub stars
- **Multi-database**: PostgreSQL, MySQL, SQLite, Oracle support
- **Flexible output**: Declarative classes, Table objects, dataclasses
- **Complementary**: Solves code generation problem (not overlap with Inspector)

**Use case:** Bootstrapping projects with existing databases, documentation generation.

---

## Eliminated Candidates

### sqlalchemy-diff
**Why eliminated:** Abandoned since March 2021 (3+ years). Likely incompatible with SQLAlchemy 2.0. Alembic autogenerate provides superior functionality with active maintenance.

### migra
**Why eliminated:** Python version officially DEPRECATED. PostgreSQL-only (not multi-database). Use TypeScript port or pg-schema-diff (Stripe) if PostgreSQL-specific tool needed.

### Django inspectdb
**Why eliminated:** Django-specific, requires Django framework. Not a general-purpose library. Only relevant for existing Django projects (use Django's native tools in that context).

---

## Key Findings

### 1. Three Distinct Use Cases
The ecosystem splits cleanly into three categories:
- **Introspection**: SQLAlchemy Inspector (read-only schema examination)
- **Comparison**: Alembic Autogenerate (schema diffing for migrations)
- **Code Generation**: sqlacodegen (reverse engineering ORM models)

### 2. SQLAlchemy is the Foundation
All non-framework-specific tools build on SQLAlchemy Inspector. It's the foundational API.

### 3. Migration Tools Have Limitations
Alembic autogenerate (and migra) cannot detect:
- Table/column renames (appear as add/drop pairs)
- Some constraint types (CHECK, EXCLUDE)
- All changes require manual review

### 4. PostgreSQL-Specific Tools are Deprecated
migra (Python) is deprecated. For PostgreSQL-specific needs, use:
- pg-schema-diff (Stripe, Go)
- migra TypeScript port
- Alembic autogenerate (general-purpose)

### 5. No "Perfect" All-in-One Solution
No single library handles introspection + comparison + code generation well. Combine tools:
- Inspector for introspection
- Alembic for comparison/migrations
- sqlacodegen for code generation

---

## Surprising Findings

1. **migra is deprecated**: The popular Python PostgreSQL diff tool is no longer maintained. TypeScript port continues.

2. **sqlalchemy-diff abandoned**: Despite being a useful concept (DB-to-DB diff), abandoned for 3+ years. Market consolidated around Alembic.

3. **No pure introspection library**: All tools either:
   - Use Inspector directly (foundational API)
   - Build comparison/generation on top of Inspector
   - No "enhanced Inspector" library exists

4. **Alembic dominance**: Alembic autogenerate is the de-facto standard for schema comparison. No active competitors in Python ecosystem.

5. **Framework lock-in**: Django inspectdb is excellent but Django-only. No standalone equivalent for other frameworks.

---

## Next Steps for S2 Deep Dive

### SQLAlchemy Inspector
- Test introspection coverage across databases (PostgreSQL, MySQL, SQLite)
- Benchmark Inspector API methods
- Document dialect-specific limitations
- Test caching behavior
- Create example code for common introspection tasks

### Alembic Autogenerate
- Test comparison accuracy (what it detects vs misses)
- Benchmark comparison performance on large schemas
- Document autogenerate limitations in detail
- Test extensibility (custom comparison functions)
- Compare MetaData-first vs DB-first workflows

### sqlacodegen
- Test code generation quality across databases
- Evaluate generated code accuracy
- Test relationship detection
- Compare declarative vs dataclass output
- Benchmark generation speed

### Cross-Library Testing
- Inspector + Alembic integration patterns
- Inspector + sqlacodegen workflows
- Performance comparison (introspection speed)
- Feature matrix (what each can/cannot introspect)

### Research Questions
1. Can Alembic autogenerate work without ORM models (MetaData-only)?
2. What Inspector methods are dialect-specific?
3. How does sqlacodegen handle complex relationships?
4. Are there any emerging competitors to Alembic?
5. Performance implications of Inspector caching?
