# Use Case: Reverse Engineer Models

## Pattern Definition

### Requirement Statement

**Need**: Generate programming language code (Python classes, ORM models) from an existing database schema to create a starting point for application development or to document legacy databases.

**Why This Matters**: Applications need to:
- Work with legacy databases without existing models
- Bootstrap new projects from existing schemas
- Generate documentation from database structure
- Create migration baselines for databases without version control
- Support database-first development workflows

### Input Parameters

| Parameter | Range | Impact |
|-----------|-------|--------|
| Database Size | 5-500 tables | Generated code size |
| Relationship Complexity | Simple to many-to-many | Relationship detection |
| Target Framework | SQLAlchemy, Django, Pydantic | Output format |
| Code Style | Declarative, Dataclasses, Tables | API preference |
| Naming Conventions | snake_case, camelCase | Code generation |

### Success Criteria

**Must Achieve**:
1. Generate class/table definitions for all tables
2. Map database types to correct Python/ORM types
3. Identify primary keys correctly
4. Generate foreign key relationships
5. Include indexes and unique constraints
6. Produce valid, executable code
7. Handle edge cases (reserved keywords, special characters)

**Performance Target**: <5 seconds for 100-table database

**Accuracy**: 100% valid code (no syntax errors, runs without modification)

### Constraints

- Generated code should follow framework best practices
- Must handle naming conflicts (Python reserved words)
- Should detect relationships even without explicit FKs
- Code should be human-readable and maintainable
- Must support database-specific types (PostgreSQL arrays, MySQL enums)

## Library Fit Analysis

### Option 1: sqlacodegen

**Installation**:
```bash
pip install sqlacodegen
```

**Basic Usage**:
```bash
# Generate SQLAlchemy models
sqlacodegen postgresql://user:pass@localhost/mydb

# Generate with specific options
sqlacodegen \
  --generator declarative \
  --outfile models.py \
  postgresql://user:pass@localhost/mydb

# Generate dataclasses (modern Python)
sqlacodegen \
  --generator dataclasses \
  --outfile models.py \
  postgresql://user:pass@localhost/mydb

# Generate only specific tables
sqlacodegen \
  --tables users,orders \
  postgresql://user:pass@localhost/mydb
```

**Generated Output Example**:
```python
# Declarative style
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    name = Column(String(100))

    orders = relationship('Order', back_populates='user')

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total = Column(Numeric(10, 2))

    user = relationship('User', back_populates='orders')
```

**Strengths**:
- **Multiple Generators**: Declarative, dataclasses, tables, SQLModels
- **Relationship Detection**: Automatically generates relationships from FKs
- **Type Mapping**: Accurate SQLAlchemy type conversion
- **Modern Python**: Supports Python 3.8+ features
- **Framework Support**: Works with Flask-SQLAlchemy, FastAPI
- **CLI Tool**: Easy to use from command line
- **Active Maintenance**: Regular updates, Python 3.12 support
- **Selective Generation**: Generate subset of tables

**Limitations**:
- **FK-Dependent Relationships**: Only detects relationships with explicit foreign keys
- **Naming Conventions**: Uses database names as-is (may need manual cleanup)
- **No Django Support**: SQLAlchemy only (but see alternatives)
- **One-Way Generation**: No round-trip (generate → modify → sync back)

**Evidence from Documentation**:
> "sqlacodegen is a tool that reads the structure of an existing database and generates the appropriate SQLAlchemy model code, using the declarative style if possible."
>
> - sqlacodegen PyPI Page

**Generation Options**:
```bash
# Declarative (classic ORM)
--generator declarative

# Dataclasses (modern Python 3.7+)
--generator dataclasses

# Tables (SQLAlchemy Core)
--generator tables

# SQLModel (FastAPI integration)
--generator sqlmodels
```

**Best For**:
- SQLAlchemy-based projects
- Need working code immediately
- Want relationship detection
- Modern Python projects (dataclasses support)
- FastAPI applications (SQLModel support)

### Option 2: sqlacodegen-v2

**Installation**:
```bash
pip install sqlacodegen-v2
```

**Overview**:
Fork of original sqlacodegen specifically for SQLAlchemy 2.0+ compatibility.

**Strengths**:
- **SQLAlchemy 2.0**: Full support for newest SQLAlchemy version
- **Modern Patterns**: Uses SQLAlchemy 2.0 idioms
- **Same API**: Drop-in replacement for sqlacodegen

**Limitations**:
- **Alternative Fork**: Not official continuation
- **Less Mature**: Newer, less battle-tested
- **Feature Parity**: May lag behind original in features

**Evidence from Research**:
> "sqlacodegen-v2 is an automatic model code generator for SQLAlchemy 2.0"
>
> - GitHub Repository

**Best For**:
- Projects using SQLAlchemy 2.0+
- Want latest SQLAlchemy features
- Original sqlacodegen incompatible

### Option 3: Django inspectdb

**Usage**:
```bash
# Generate Django models
python manage.py inspectdb > models.py

# Generate for specific database (multi-db setup)
python manage.py inspectdb --database legacy_db

# Generate specific tables only
python manage.py inspectdb users orders > app/models.py
```

**Generated Output Example**:
```python
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.CharField(unique=True, max_length=255)
    name = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'

class Order(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', models.DO_NOTHING)
    total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orders'
```

**Strengths**:
- **Django Native**: Built into Django, no installation needed
- **Django Conventions**: Follows Django model patterns
- **Multi-Database**: Works with all Django-supported databases
- **managed=False**: Marks models as not managed by migrations
- **Type Mapping**: Django field type conversion

**Limitations**:
- **Django Only**: Not usable outside Django projects
- **Manual Cleanup**: Generated code needs review and editing
- **Relationship Issues**: May not detect all relationships correctly
- **No Choices Detection**: Doesn't generate choices for enums
- **managed=False**: Requires manual override if you want migrations

**Evidence from Documentation**:
> "inspectdb introspects the database tables in the database pointed-to by the NAME setting and outputs a Django model module (a models.py file) to standard output."
>
> - Django Documentation

**Best For**:
- Django projects exclusively
- Want framework-native tool
- Legacy database integration
- Quick prototyping

### Option 4: Manual Reflection + Code Generation

**API Example**:
```python
from sqlalchemy import inspect, MetaData
from jinja2 import Template

def generate_models(engine):
    """Generate model code from database inspection"""
    inspector = inspect(engine)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    template = Template("""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

{% for table in tables %}
class {{ table.name | title }}(Base):
    __tablename__ = '{{ table.name }}'

    {% for column in table.columns %}
    {{ column.name }} = Column({{ column.type }}, primary_key={{ column.primary_key }})
    {% endfor %}

    {% for fk in table.foreign_keys %}
    {{ fk.target_table }} = relationship('{{ fk.target_table | title }}')
    {% endfor %}
{% endfor %}
    """)

    return template.render(tables=metadata.tables.values())
```

**Strengths**:
- **Full Control**: Custom template, naming, structure
- **Flexible**: Generate any output format needed
- **Multi-Target**: Generate for different frameworks
- **Custom Logic**: Handle edge cases specifically

**Limitations**:
- **Manual Implementation**: Write generation logic yourself
- **Template Maintenance**: Keep templates updated
- **Testing Burden**: Ensure generated code is valid
- **Type Mapping**: Implement type conversions manually

**Best For**:
- Need custom output format
- Multi-framework code generation
- Special naming conventions
- Learning exercise

## Comparison Matrix

| Criterion | sqlacodegen | sqlacodegen-v2 | Django inspectdb | Manual |
|-----------|-------------|----------------|------------------|--------|
| Framework | SQLAlchemy 1.4 | SQLAlchemy 2.0 | Django | Any |
| Relationship Detection | Excellent | Excellent | Good | Custom |
| Type Accuracy | Excellent | Excellent | Good | Manual |
| Modern Python | Yes (dataclasses) | Yes | No | Custom |
| Maintenance | Active | Active | Built-in | Self |
| CLI Tool | Yes | Yes | Yes | No |
| Customization | Limited | Limited | None | Full |
| Learning Curve | Low | Low | Low | High |
| Multi-DB | Yes | Yes | Yes | Yes |

## Recommendations

### Primary: sqlacodegen (SQLAlchemy Projects)

**Rationale**:
1. **Complete Solution**: Generates working code immediately
2. **Multiple Generators**: Declarative, dataclasses, tables, SQLModels
3. **Active Maintenance**: Regular updates, Python 3.12 support
4. **Production-Ready**: Widely used, battle-tested
5. **Framework Integration**: Works with Flask, FastAPI, standalone

**Workflow**:
```bash
# 1. Generate initial models
sqlacodegen --generator dataclasses postgresql://localhost/db > models.py

# 2. Review and customize generated code
# - Add business logic methods
# - Adjust naming conventions
# - Add validation logic

# 3. Create initial Alembic migration from models
alembic revision --autogenerate -m "Initial schema from reverse engineering"

# 4. Future changes tracked through normal migration workflow
```

**Example for FastAPI**:
```bash
# Generate SQLModel classes for FastAPI
sqlacodegen \
  --generator sqlmodels \
  --outfile app/models.py \
  postgresql://localhost/mydb

# Generated code ready to use with FastAPI
from app.models import User, Order
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
def get_user(user_id: int, db: Session):
    return db.query(User).filter(User.id == user_id).first()
```

**Confidence**: High (90%)

### Use sqlacodegen-v2 if SQLAlchemy 2.0+

**Rationale**:
If project uses SQLAlchemy 2.0+, use sqlacodegen-v2 for proper 2.0 idioms.

**Check SQLAlchemy Version**:
```bash
pip show sqlalchemy | grep Version

# If Version: 2.x.x
pip install sqlacodegen-v2
sqlacodegen-v2 postgresql://localhost/db > models.py
```

**Confidence**: High (85%)

### Use Django inspectdb for Django Projects

**Rationale**:
Built-in Django tool, no additional dependencies, follows Django conventions.

**Workflow**:
```bash
# 1. Generate initial models
python manage.py inspectdb > myapp/models.py

# 2. Review generated code
# - Remove managed=False for tables you want to manage
# - Add choices for enum fields
# - Fix relationship names
# - Add model methods

# 3. Create migration from cleaned models
python manage.py makemigrations myapp

# 4. Apply to create Django's migration history
python manage.py migrate --fake-initial
```

**Confidence**: High (85%)

### Not Recommended: Manual Generation

**Reason**: sqlacodegen already solves this problem comprehensively. Custom generation only makes sense for very specific requirements not met by existing tools.

**Exception**: Multi-framework generation (generate both Django and SQLAlchemy from same database).

## Advanced Patterns

### Pattern 1: Incremental Reverse Engineering

**Problem**: Large database, only need subset of tables.

**Solution**:
```bash
# Generate only needed tables
sqlacodegen \
  --tables users,orders,products \
  --outfile core_models.py \
  postgresql://localhost/db

# Later, add more tables to separate file
sqlacodegen \
  --tables analytics_events,logs \
  --outfile analytics_models.py \
  postgresql://localhost/db
```

### Pattern 2: Multi-Database Legacy Integration

**Problem**: Application needs to integrate with multiple legacy databases.

**Solution**:
```bash
# Generate models for each database
sqlacodegen \
  --outfile models/legacy_crm.py \
  postgresql://localhost/crm_db

sqlacodegen \
  --outfile models/legacy_billing.py \
  mysql://localhost/billing_db

# Use separate Base for each database
# models/legacy_crm.py
Base_CRM = declarative_base()
class Customer(Base_CRM):
    __bind_key__ = 'crm'
    ...

# models/legacy_billing.py
Base_Billing = declarative_base()
class Invoice(Base_Billing):
    __bind_key__ = 'billing'
    ...
```

### Pattern 3: Reverse Engineering for Documentation

**Problem**: Need to document legacy database structure.

**Solution**:
```python
# Generate models, then convert to docs
import sqlacodegen
import inspect

# 1. Generate models to temporary file
# 2. Import generated models
# 3. Use introspection to create docs

def generate_schema_docs(models_module):
    """Generate markdown docs from generated models"""
    docs = ["# Database Schema\n"]

    for name, cls in inspect.getmembers(models_module, inspect.isclass):
        if hasattr(cls, '__tablename__'):
            docs.append(f"\n## {name}\n")
            docs.append(f"Table: `{cls.__tablename__}`\n")
            docs.append("\n### Columns\n")

            for col in cls.__table__.columns:
                docs.append(
                    f"- **{col.name}**: {col.type} "
                    f"{'PRIMARY KEY' if col.primary_key else ''} "
                    f"{'NOT NULL' if not col.nullable else ''}\n"
                )

    return "\n".join(docs)
```

## Confidence Level

**High (90%)** - sqlacodegen is the clear best-fit for SQLAlchemy projects, Django inspectdb for Django.

**Evidence Quality**: Excellent
- sqlacodegen widely documented and used in production
- Django inspectdb is official Django feature
- Clear use cases and limitations understood
- Active maintenance confirmed via PyPI and GitHub
