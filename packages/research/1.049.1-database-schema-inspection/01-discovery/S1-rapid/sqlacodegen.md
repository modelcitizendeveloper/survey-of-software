# sqlacodegen

**Category:** Reverse Engineering / Code Generator
**Package:** sqlacodegen
**GitHub:** https://github.com/agronholm/sqlacodegen
**Date Evaluated:** December 4, 2025

## Overview

sqlacodegen automatically generates SQLAlchemy ORM model code from existing databases. It's the go-to tool for reverse engineering legacy databases, bootstrapping new projects, or documenting existing schemas through code.

## Popularity Metrics

- **GitHub Stars:** 1.8k+
- **PyPI Downloads:** 350k+ monthly
- **Maintenance:** Active (maintained by Alex Gronholm)
- **First Release:** 2012
- **Latest Version:** 3.0+ (Dec 2025, SQLAlchemy 2.0 support)

## Primary Use Case

Generating SQLAlchemy ORM models from existing databases:
- Legacy database integration
- Rapid prototyping from existing schemas
- Database documentation as code
- Migration from other ORMs

## Key Capabilities

### What It Does Well

1. **Comprehensive Code Generation**
   ```bash
   sqlacodegen postgresql://user:pass@host/db > models.py
   ```
   Generates:
   - SQLAlchemy declarative models
   - Column definitions with types
   - Primary and foreign keys
   - Indexes and constraints
   - Relationships (with options)

2. **SQLAlchemy 2.0 Support**
   - Modern declarative syntax
   - Mapped columns
   - Type annotations (with --generator dataclasses)
   - Async support options

3. **Flexible Output Modes**
   - **Declarative:** Standard ORM models
   - **Dataclasses:** SQLAlchemy 2.0 dataclass style
   - **Tables:** Core Table definitions
   - Customizable templates

4. **Relationship Detection**
   ```python
   # Automatically generates relationships from foreign keys
   class User(Base):
       __tablename__ = 'users'
       id = mapped_column(Integer, primary_key=True)
       posts = relationship('Post', back_populates='user')

   class Post(Base):
       __tablename__ = 'posts'
       user_id = mapped_column(ForeignKey('users.id'))
       user = relationship('User', back_populates='posts')
   ```

5. **Database Support**
   - PostgreSQL, MySQL, SQLite
   - Oracle, SQL Server
   - Any SQLAlchemy-supported database

6. **Filtering Options**
   - Select specific tables/schemas
   - Exclude system tables
   - Pattern matching
   - Custom naming conventions

### Advanced Features

- **--generator dataclasses:** Modern SQLAlchemy 2.0 dataclass style
- **--noclasses:** Generate Table objects only
- **--nojoined:** Skip relationship inference for joined table inheritance
- **--noinflect:** Disable automatic pluralization
- **--outfile:** Write to file instead of stdout

## Limitations

1. **Generated Code Requires Review**
   - Relationship names may be awkward
   - Back-populates can be incorrect for complex schemas
   - Type choices may not match intent
   - Needs manual cleanup for production use

2. **Limited Inference**
   - Can't detect business logic constraints
   - No validation rules
   - Missing domain-specific annotations
   - One-size-fits-all relationship patterns

3. **No Incremental Updates**
   - Full regeneration only
   - Manual merging if schema changes
   - Overwrites custom modifications
   - Not a schema synchronization tool

4. **Complex Schemas Can Be Messy**
   - Large schemas produce huge files
   - Circular relationships can be confusing
   - Many-to-many detection not perfect
   - Inheritance hierarchies simplified

## When to Use

**Best For:**
- Integrating with legacy databases
- Jumpstarting new projects from existing schemas
- Generating initial models (then customize)
- Database documentation
- Learning database structure quickly

**Workflow:**
1. Run sqlacodegen to generate initial models
2. Review and refactor output
3. Customize relationships and constraints
4. Add business logic and validations
5. Maintain models manually going forward

**Not Suitable For:**
- Ongoing schema synchronization (use Alembic)
- Production code without review
- Incremental model updates
- Complex domain modeling (generates generic models)

## Integration Notes

```bash
# Basic usage
sqlacodegen postgresql://localhost/mydb

# With filtering
sqlacodegen postgresql://localhost/mydb --tables users,posts,comments

# Modern dataclass style
sqlacodegen --generator dataclasses postgresql://localhost/mydb

# To file
sqlacodegen postgresql://localhost/mydb --outfile models.py

# Schema-specific (PostgreSQL)
sqlacodegen postgresql://localhost/mydb --schema public
```

## Verdict

**Essential tool for database reverse engineering.** sqlacodegen excels at bootstrapping ORM models from existing databases. The generated code is a starting point, not a final product. Always review, refactor, and customize the output.

**Recommendation:**
- Use to accelerate initial model creation (saves hours of manual typing)
- Treat output as scaffolding, not production code
- Essential for legacy database integration projects
- Great learning tool for understanding database schemas
- Don't use for ongoing synchronization (that's Alembic's job)

**Quality:** High-quality, well-maintained project. Actively updated for SQLAlchemy 2.0+. Reliable for its intended purpose.
