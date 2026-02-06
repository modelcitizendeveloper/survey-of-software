# Use Case: Legacy Database Reverse Engineering

## Scenario Description

You've inherited a legacy database with 50+ tables, minimal documentation, and no ORM models. Your task: generate SQLAlchemy models to build a modern Python API on top of the existing schema without disrupting current systems.

## Primary Requirements

### Must-Have Features
1. **Automatic model generation** from existing database schema
2. **Relationship inference** from foreign keys
3. **Data type mapping** from database to SQLAlchemy types
4. **Index and constraint preservation**
5. **Support for database-specific features** (PostgreSQL arrays, JSON columns, etc.)

### Operational Constraints
- Cannot modify existing database schema
- Must maintain backward compatibility
- Need one-time generation, not continuous sync
- Multiple developers need consistent models

## Recommended Toolchain

### Primary Tool: sqlacodegen

**Why sqlacodegen:**
- Specifically designed for model generation from existing schemas
- Excellent relationship inference
- Supports advanced SQLAlchemy features (hybrid properties, composites)
- Handles edge cases (self-referential relationships, many-to-many)

**Installation:**
```bash
uv pip install sqlacodegen
```

**Basic Usage:**
```bash
sqlacodegen postgresql://user:pass@localhost/legacy_db > models.py
```

### Advanced Options

**Generate declarative models with relationships:**
```bash
sqlacodegen \
  --outfile models.py \
  --generator declarative \
  postgresql://user:pass@localhost/legacy_db
```

**Include table comments and metadata:**
```bash
sqlacodegen \
  --tables users,orders,products \
  --generator dataclasses \
  postgresql://user:pass@localhost/legacy_db
```

## Workflow Integration

### Phase 1: Initial Generation
1. Inspect database to understand structure
2. Run sqlacodegen with appropriate options
3. Review generated models for accuracy
4. Manual cleanup of naming conventions

### Phase 2: Refinement
1. Add custom methods to models
2. Create mixins for common patterns
3. Document relationships and business logic
4. Establish model organization (single vs. multiple files)

### Phase 3: Maintenance
1. Version control generated models
2. Document manual modifications separately
3. Establish process for schema changes
4. Consider migration to Alembic for future changes

## Common Pitfalls

### 1. Over-reliance on Auto-generation
**Problem:** Generated models may not match business logic conventions

**Solution:**
- Treat generated code as starting point
- Refactor for clarity and maintainability
- Rename classes/columns to match Python conventions

### 2. Complex Relationship Inference
**Problem:** sqlacodegen may misinterpret relationships

**Solution:**
```python
# Review and correct relationship directions
# Before (auto-generated):
orders = relationship('Order', back_populates='user')

# After (corrected):
orders = relationship('Order', back_populates='customer', lazy='dynamic')
```

### 3. Database-Specific Types
**Problem:** Custom PostgreSQL types may not map cleanly

**Solution:**
```python
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

# Manually verify and adjust type mappings
metadata = Column(JSONB)
tags = Column(ARRAY(String))
```

### 4. Missing Indexes and Constraints
**Problem:** Performance-critical indexes may not be obvious in generated models

**Solution:**
- Cross-reference with database indexes
- Add missing indexes explicitly
- Document performance considerations

## Alternative Approaches

### For Simple Schemas: Manual Writing
If schema is small (<10 tables), manual model writing may be faster and cleaner.

### For Django Projects: Django inspectdb
```bash
python manage.py inspectdb > models.py
```

Django's built-in tool generates Django ORM models instead of SQLAlchemy.

### For Read-Only Access: SQL Reflection
```python
from sqlalchemy import MetaData, Table
metadata = MetaData()
users = Table('users', metadata, autoload_with=engine)
```

For reporting/analytics, reflection may be sufficient without model generation.

## Success Metrics

### Technical Success
- All tables successfully mapped to models
- Relationships correctly inferred
- Foreign keys and constraints preserved
- Type mappings accurate and functional

### Operational Success
- Models are readable and maintainable
- Team can extend models easily
- Clear documentation of manual modifications
- Reduced time to implement new features

## Example Workflow

```bash
# Step 1: Generate initial models
sqlacodegen postgresql://localhost/legacy_db > models_raw.py

# Step 2: Review and organize
# Manually split into logical modules: users.py, orders.py, products.py

# Step 3: Refactor for conventions
# Rename classes, add docstrings, organize imports

# Step 4: Add business logic
# Include custom methods, validators, computed properties

# Step 5: Set up Alembic for future changes
alembic init alembic
alembic revision --autogenerate -m "Initial schema from legacy db"
```

## When NOT to Use This Approach

- Active schema development (use Alembic migrations instead)
- Database schema changes frequently
- Need continuous synchronization
- Schema is trivial (manual writing faster)

Date compiled: December 4, 2025
