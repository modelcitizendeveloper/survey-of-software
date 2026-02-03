# S1 Rapid Search Recommendations: Database Schema Inspection

**Research Domain:** 1.049.1 Database Schema Inspection
**Date Compiled:** December 4, 2025
**Methodology:** S1 - Rapid Library Search

## Executive Summary

The Python/SQLAlchemy ecosystem provides robust schema inspection capabilities through a **modular toolkit approach** rather than an integrated solution. Success requires understanding which tool to use for each specific task.

**Key Finding:** Unlike Prisma's unified approach, Python developers combine 3-4 specialized tools for complete schema lifecycle management. This offers flexibility but requires orchestration.

## Tool Selection Matrix

| Use Case | Recommended Tool | Alternative | Status |
|----------|-----------------|-------------|--------|
| **Programmatic Schema Introspection** | SQLAlchemy Inspector | N/A | Essential |
| **Generate ORM Models from DB** | sqlacodegen | Django inspectdb (Django only) | Recommended |
| **Create Migrations from Model Changes** | Alembic autogenerate | N/A | Essential |
| **Compare Database Schemas** | Custom Inspector scripts | migra, sqlalchemy-diff | Build Custom |
| **Database-First Development** | sqlacodegen + Alembic | N/A | Combined |
| **Model-First Development** | Alembic autogenerate | N/A | Standard |

## Primary Recommendations

### 1. SQLAlchemy Inspector (Built-in)

**Verdict:** Essential foundation - master this first

**Use When:**
- Building custom schema tools
- Runtime schema validation
- Dynamic database access
- Foundation for other tools

**Why:**
- Zero additional dependencies
- Rock-solid reliability
- Powers all other tools
- Complete database coverage

**Getting Started:**
```python
from sqlalchemy import create_engine, inspect

engine = create_engine('postgresql://...')
inspector = inspect(engine)

# Core operations
tables = inspector.get_table_names()
columns = inspector.get_columns('users')
indexes = inspector.get_indexes('users')
fks = inspector.get_foreign_keys('users')
```

### 2. sqlacodegen (Reverse Engineering)

**Verdict:** Best-in-class for database → code

**Use When:**
- Integrating legacy databases
- Bootstrapping new projects from existing schemas
- Generating initial models
- Database documentation

**Why:**
- Active maintenance (SQLAlchemy 2.0 support)
- Comprehensive output (models, relationships, constraints)
- Multiple output formats
- 350k+ monthly downloads

**Critical Practice:**
- ALWAYS review and refactor generated code
- Treat output as scaffolding, not production-ready
- Customize relationships and naming
- Add business logic manually

**Getting Started:**
```bash
# Install
uv pip install sqlacodegen

# Basic usage
sqlacodegen postgresql://user:pass@host/db > models.py

# Modern dataclass style (SQLAlchemy 2.0)
sqlacodegen --generator dataclasses postgresql://... > models.py

# Specific tables
sqlacodegen --tables users,posts postgresql://... > models.py
```

### 3. Alembic (Migration Framework)

**Verdict:** Non-negotiable for schema evolution

**Use When:**
- Managing schema changes over time
- Team collaboration on databases
- Production deployment pipelines
- Autogenerating migrations from model changes

**Why:**
- Official SQLAlchemy project
- 25M+ monthly downloads
- Version-controlled migrations
- Autogenerate saves hours

**Critical Practice:**
- Autogenerate is a starting point, not final product
- ALWAYS review migrations before applying
- Test migrations in staging first
- Version control all migration scripts

**Getting Started:**
```bash
# Install
uv pip install alembic

# Initialize
alembic init alembic

# Configure alembic.ini and alembic/env.py

# Create migration from model changes
alembic revision --autogenerate -m "add user fields"

# Review and edit generated migration!

# Apply
alembic upgrade head
```

## Secondary Recommendations

### 4. Schema Comparison Tools

**Status:** Gap in ecosystem - build custom or use specialized tools

**Options:**

**A. Custom Inspector Script (Recommended)**
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

    # Compare columns for common tables...
    return {
        'added_tables': added,
        'removed_tables': removed,
        # ... detailed diffs
    }
```

**Why Custom:**
- Full control over comparison logic
- Tailored to your specific needs
- No maintenance dependency risk
- Leverage Inspector's reliability

**B. migra (PostgreSQL-Specific)**
- GitHub: https://github.com/djrobstep/migra
- 3k+ stars, active maintenance
- Generates migration SQL
- PostgreSQL only
- Better than sqlalchemy-diff for Postgres

**C. sqlalchemy-diff (Use with Caution)**
- 15k monthly downloads
- Limited maintenance (last update 2023)
- OK for dev/debugging
- Risky for production workflows

**Recommendation:** Start with custom Inspector scripts. Invest time once, own it forever. Use migra if PostgreSQL-only.

## Workflow Patterns

### Pattern 1: Legacy Database Integration

**Goal:** Integrate existing database with new Python application

**Steps:**
1. Use sqlacodegen to generate initial models
2. Review and refactor generated code
3. Set up Alembic for future changes
4. Create baseline migration (current state)
5. Manage changes through Alembic going forward

**Tools:** sqlacodegen → manual refinement → Alembic

### Pattern 2: Greenfield Development

**Goal:** Build new application with schema evolution

**Steps:**
1. Define models manually
2. Set up Alembic from start
3. Use autogenerate for migrations
4. Review all migrations before applying

**Tools:** Manual models → Alembic autogenerate

### Pattern 3: Multi-Environment Sync

**Goal:** Ensure dev, staging, prod schemas match

**Steps:**
1. Use custom Inspector script to compare
2. Identify differences
3. Create Alembic migration to reconcile
4. Apply through standard deployment

**Tools:** Custom Inspector → Alembic migration

### Pattern 4: Database-First Prototyping

**Goal:** Rapid iteration on schema design

**Steps:**
1. Design schema in database directly (SQL, GUI tool)
2. Use sqlacodegen to generate models
3. Test in application
4. Iterate (repeat 1-3)
5. When stable, switch to model-first + Alembic

**Tools:** Database → sqlacodegen → Application → Alembic (when stable)

## Ecosystem Gaps

### What's Missing (vs Prisma)

1. **Unified Tool:** No single tool for introspect + migrate + ORM
2. **Bidirectional Sync:** No easy "push schema to DB" from models
3. **Incremental Codegen:** sqlacodegen is one-time, not incremental
4. **Type Safety:** Python type hints optional, not enforced
5. **CLI Integration:** Each tool has different CLI patterns

### Why This Matters

**Advantages of Modular Approach:**
- Flexibility: Mix and match tools
- Maturity: Each tool focused and stable
- Choice: Multiple solutions for each problem

**Disadvantages:**
- Complexity: Learn multiple tools
- Integration: Manual orchestration required
- Consistency: Different conventions across tools

**Recommendation:** Accept the modular nature. Invest time learning the core three tools (Inspector, sqlacodegen, Alembic). Build custom glue code for your specific workflows.

## Common Pitfalls

### Pitfall 1: Trusting Autogenerate Blindly

**Problem:** Alembic autogenerate is not perfect
- Misses column renames (sees drop + add)
- May not detect all constraint changes
- Can generate incorrect migrations

**Solution:** ALWAYS review generated migrations. Test in staging first.

### Pitfall 2: Using Generated Models Without Refactoring

**Problem:** sqlacodegen output is mechanical, not optimized
- Awkward relationship names
- Missing business logic
- No validators or custom methods

**Solution:** Treat generated code as scaffolding. Refactor before production use.

### Pitfall 3: Ignoring Schema Drift

**Problem:** Dev and prod schemas diverge over time
- Manual fixes applied only to prod
- Migrations not applied consistently
- Unclear schema state

**Solution:** Version control all migrations. Use Inspector scripts for validation. Never manual schema changes in prod.

### Pitfall 4: Over-Reliance on Third-Party Comparison Tools

**Problem:** Tools like sqlalchemy-diff have maintenance risk
- May lag SQLAlchemy updates
- Limited community support
- Bugs may not be fixed

**Solution:** Build critical comparison logic on Inspector (stable foundation). Use third-party tools for convenience, not critical workflows.

## Quick Start Guide

### Day 1: Foundation

1. Learn SQLAlchemy Inspector
   - Read docs: https://docs.sqlalchemy.org/en/20/core/reflection.html
   - Write small script to introspect a database
   - Understand get_table_names(), get_columns(), get_foreign_keys()

2. Set up Alembic
   - Install: `uv pip install alembic`
   - Initialize: `alembic init alembic`
   - Configure database connection
   - Create first migration

### Week 1: Core Tools

3. Try sqlacodegen
   - Install: `uv pip install sqlacodegen`
   - Generate models from a test database
   - Compare output to manual models
   - Understand when to use

4. Practice Alembic autogenerate
   - Make model changes
   - Run autogenerate
   - Review generated migration
   - Apply and test

### Month 1: Advanced Workflows

5. Build custom comparison script
   - Use Inspector to compare two databases
   - Generate diff report
   - Understand what's easy vs hard to detect

6. Establish team workflow
   - Define migration practices
   - Set up CI/CD validation
   - Document when to use each tool

## Final Recommendation

**For Most SQLAlchemy Projects:**

**Essential Stack:**
1. SQLAlchemy Inspector (learn deeply)
2. Alembic (essential for migrations)
3. sqlacodegen (for reverse engineering needs)

**Optional/Situational:**
4. Custom Inspector scripts (for comparisons)
5. migra (if PostgreSQL-only)

**Avoid:**
- sqlalchemy-diff (maintenance concerns)
- Building your own migration framework
- One-off manual schema changes in production

**Success Formula:**
- Master the core three tools
- Build custom glue code for your workflows
- Accept modular nature as feature, not bug
- Version control everything (models, migrations, comparison scripts)

**Investment:** 2-4 days to learn core tools well. Pays dividends for years.
