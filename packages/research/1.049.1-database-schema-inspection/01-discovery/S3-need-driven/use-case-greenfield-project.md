# Use Case: Greenfield SQLAlchemy Project

## Scenario Description

You're starting a new Python web application with SQLAlchemy and PostgreSQL. You need a schema management strategy from day one that supports rapid development, maintains data integrity, and scales with the project. This is the ideal time to establish best practices.

## Primary Requirements

### Must-Have Features
1. **Version-controlled schema changes** from the start
2. **Automatic migration generation** from model changes
3. **Rollback capability** for development iterations
4. **Team collaboration** without schema conflicts
5. **Production-ready** migration workflow

### Operational Constraints
- Rapid iteration during early development
- Clear migration history for auditing
- Easy onboarding for new team members
- Support for both local and CI/CD environments
- Minimal overhead during prototyping

## Recommended Toolchain

### Primary Tool: Alembic (with SQLAlchemy)

**Why Alembic:**
- Official SQLAlchemy migration tool
- Auto-generates migrations from model changes
- Supports complex schema operations
- Production-proven and actively maintained
- Excellent documentation and community

**Installation:**
```bash
uv pip install alembic sqlalchemy psycopg2-binary
```

## Workflow Integration

### Phase 1: Project Initialization

**Project Structure:**
```
myproject/
  models/
    __init__.py
    base.py
    user.py
    product.py
  alembic/
    env.py
    script.py.mako
    versions/
  alembic.ini
  database.py
  config.py
```

**Initialize Alembic:**
```bash
# Initialize Alembic in your project
alembic init alembic

# This creates:
# - alembic/ directory with configuration
# - alembic.ini configuration file
# - alembic/env.py for environment setup
```

**Configure Alembic:**
```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Import your models' Base
from myproject.models.base import Base

# This is the Alembic Config object
config = context.config

# Set the SQLAlchemy metadata
target_metadata = Base.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()
```

### Phase 2: Model Development

**Base Model Setup:**
```python
# models/base.py
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, DateTime
from datetime import datetime

class Base(DeclarativeBase):
    """Base class for all models"""
    pass

class TimestampMixin:
    """Mixin for created_at/updated_at timestamps"""
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

**Example Model:**
```python
# models/user.py
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from .base import Base, TimestampMixin

class User(Base, TimestampMixin):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    username = Column(String(100), unique=True, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    # Relationships
    posts = relationship('Post', back_populates='author', lazy='dynamic')
```

### Phase 3: Migration Workflow

**Create Initial Migration:**
```bash
# Generate migration from current models
alembic revision --autogenerate -m "Initial schema"

# Review the generated migration in alembic/versions/
# This is important! Always review auto-generated migrations
```

**Generated Migration Example:**
```python
# alembic/versions/001_initial_schema.py
"""Initial schema

Revision ID: 001
Revises:
Create Date: 2025-12-04
"""
from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)

def downgrade():
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
```

**Apply Migration:**
```bash
# Apply migration to database
alembic upgrade head

# Check current revision
alembic current

# View migration history
alembic history --verbose
```

### Phase 4: Iterative Development

**Development Iteration Pattern:**

1. **Modify Models:**
```python
# models/user.py - Add new field
class User(Base, TimestampMixin):
    __tablename__ = 'users'
    # ... existing fields ...
    phone_number = Column(String(20), nullable=True)  # New field
```

2. **Generate Migration:**
```bash
alembic revision --autogenerate -m "Add phone number to users"
```

3. **Review Migration:**
```python
# Always check auto-generated migration!
# Alembic might miss:
# - Renamed columns (looks like drop + add)
# - Changed constraints
# - Data migrations needed
```

4. **Apply and Test:**
```bash
alembic upgrade head
# Test your application with new schema

# If issues found, rollback:
alembic downgrade -1
```

## Best Practices for Greenfield Projects

### 1. Model Organization

**Separate models by domain:**
```
models/
  __init__.py        # Import all models here
  base.py           # Base class and mixins
  user.py           # User-related models
  product.py        # Product models
  order.py          # Order models
```

**models/__init__.py:**
```python
from .base import Base
from .user import User, UserProfile
from .product import Product, Category
from .order import Order, OrderItem

# Ensure all models are imported before generating migrations
__all__ = ['Base', 'User', 'UserProfile', 'Product', 'Category', 'Order', 'OrderItem']
```

### 2. Migration Naming Conventions

```bash
# Good: Descriptive names
alembic revision --autogenerate -m "Add user authentication fields"
alembic revision --autogenerate -m "Create product catalog tables"

# Bad: Vague names
alembic revision --autogenerate -m "Update schema"
alembic revision --autogenerate -m "Changes"
```

### 3. Testing Migrations

**Test Migration in Fresh Database:**
```bash
# Create test database
createdb myproject_test

# Run migrations from scratch
alembic -c alembic_test.ini upgrade head

# Verify schema
psql myproject_test -c "\dt"
psql myproject_test -c "\d users"
```

### 4. Environment-Specific Configuration

```python
# config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/myproject_dev'

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/myproject_test'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
```

## Common Pitfalls

### 1. Forgetting to Import Models
**Problem:** Alembic doesn't detect new models

**Solution:**
```python
# models/__init__.py - Always import all models
from .user import User
from .new_model import NewModel  # Don't forget this!
```

### 2. Not Reviewing Auto-Generated Migrations
**Problem:** Migrations contain unintended changes

**Solution:** Always manually review before applying:
- Check column types match expectations
- Verify indexes are created
- Ensure foreign keys are correct
- Confirm no accidental drops

### 3. Data Migrations in Schema Changes
**Problem:** Adding non-nullable columns to existing tables

**Solution:**
```python
def upgrade():
    # Add column as nullable first
    op.add_column('users', sa.Column('role', sa.String(50), nullable=True))

    # Populate data
    op.execute("UPDATE users SET role = 'user' WHERE role IS NULL")

    # Make non-nullable
    op.alter_column('users', 'role', nullable=False)
```

### 4. Merge Conflicts in Migrations
**Problem:** Multiple developers create migrations simultaneously

**Solution:**
```bash
# Create merge migration
alembic merge heads -m "Merge feature branches"
```

## Development Tools

### Database Management Script

```python
# scripts/db.py
import click
from alembic import command
from alembic.config import Config

@click.group()
def cli():
    """Database management commands"""
    pass

@cli.command()
def init():
    """Initialize database schema"""
    config = Config("alembic.ini")
    command.upgrade(config, "head")
    click.echo("Database initialized")

@cli.command()
def reset():
    """Reset database (destructive!)"""
    if click.confirm("This will delete all data. Continue?"):
        config = Config("alembic.ini")
        command.downgrade(config, "base")
        command.upgrade(config, "head")
        click.echo("Database reset complete")

@cli.command()
@click.option('--message', '-m', required=True)
def migrate(message):
    """Generate new migration"""
    config = Config("alembic.ini")
    command.revision(config, autogenerate=True, message=message)
    click.echo(f"Migration created: {message}")

if __name__ == '__main__':
    cli()
```

**Usage:**
```bash
python scripts/db.py init
python scripts/db.py migrate -m "Add user roles"
python scripts/db.py reset
```

## Success Metrics

### Technical Success
- All schema changes version-controlled
- Zero manual SQL for schema changes
- Migrations apply cleanly in all environments
- Clear rollback strategy for every change

### Operational Success
- New developers can set up database in < 5 minutes
- Schema history provides clear audit trail
- CI/CD applies migrations automatically
- Team avoids schema conflicts

## Example Project Timeline

**Week 1: Setup**
```bash
# Initialize project
alembic init alembic
# Create base models
# Generate initial migration
alembic revision --autogenerate -m "Initial schema"
```

**Week 2-4: Core Development**
```bash
# Add features iteratively
alembic revision --autogenerate -m "Add product catalog"
alembic revision --autogenerate -m "Add shopping cart"
alembic revision --autogenerate -m "Add order processing"
```

**Week 5+: Refinement**
```bash
# Add indexes for performance
alembic revision --autogenerate -m "Add performance indexes"
# Add constraints
alembic revision --autogenerate -m "Add business rule constraints"
```

## When NOT to Use This Approach

- Prototypes that won't reach production
- Single-script projects
- Databases managed by external tools (e.g., PostGIS extensions)
- Projects with infrequent schema changes

Date compiled: December 4, 2025
