# Django inspectdb

**Category:** Reverse Engineering (Django ORM)
**Package:** django (built-in command)
**Documentation:** https://docs.djangoproject.com/en/stable/ref/django-admin/#inspectdb
**Date Evaluated:** December 4, 2025

## Overview

Django's inspectdb is a built-in management command that introspects database tables and generates Django ORM model code. It's the Django ecosystem's equivalent to sqlacodegen, tightly integrated with Django's ORM conventions.

## Popularity Metrics

- **Django Stars:** 78k+ GitHub stars
- **Django Downloads:** 25M+ monthly (PyPI)
- **Status:** Built-in Django feature since early versions
- **Maintenance:** Active (part of Django core)

## Primary Use Case

Generating Django models from existing databases:
- Integrating legacy databases with Django
- Rapid prototyping from existing schemas
- Database migration from other frameworks
- Quick model scaffolding

## Key Capabilities

### What It Does Well

1. **Seamless Django Integration**
   ```bash
   python manage.py inspectdb > models.py
   python manage.py inspectdb table1 table2 > models.py  # Specific tables
   ```

2. **Django-Specific Features**
   - Generates Django Field types (CharField, ForeignKey, etc.)
   - Creates Meta classes with db_table
   - Includes managed=False for legacy databases
   - Auto-detects primary keys
   - Handles Django naming conventions

3. **Output Example**
   ```python
   class User(models.Model):
       id = models.BigAutoField(primary_key=True)
       username = models.CharField(max_length=100)
       email = models.EmailField()
       created_at = models.DateTimeField()

       class Meta:
           managed = False
           db_table = 'users'
   ```

4. **Database Support**
   - PostgreSQL, MySQL, SQLite
   - Oracle, MariaDB
   - Any Django-supported database

## Limitations

1. **Django-Locked**
   - Only generates Django models (not SQLAlchemy)
   - Requires Django installation
   - Bound to Django ORM patterns
   - Not useful outside Django projects

2. **Basic Feature Set**
   - Less sophisticated than sqlacodegen
   - Simple relationship inference
   - Limited customization options
   - No modern syntax variants

3. **Manual Cleanup Required**
   - Generated code needs review
   - Field types may not be optimal
   - Relationships require manual refinement
   - Validators and constraints missing

4. **No Incremental Updates**
   - One-time generation only
   - Manual synchronization if schema changes
   - Overwrites existing files

## When to Use

**Best For (Django Projects Only):**
- Integrating Django with legacy databases
- Quick model prototyping
- Learning existing database structures
- Initial model scaffolding

**Advantages:**
- Zero additional dependencies (built into Django)
- Perfect Django conventions
- Fast and simple
- Well-documented

**Not Suitable For:**
- Non-Django projects (use sqlacodegen for SQLAlchemy)
- Production-ready models without review
- Ongoing schema synchronization
- Complex ORM patterns

## Comparison to sqlacodegen

| Feature | Django inspectdb | sqlacodegen |
|---------|------------------|-------------|
| Target ORM | Django only | SQLAlchemy only |
| Installation | Built-in | Separate package |
| Relationship Detection | Basic | Advanced |
| Customization | Limited | Extensive |
| Output Formats | Django models | Multiple formats |
| Maintenance | Django core team | Independent project |

## Verdict

**Standard tool for Django + legacy database scenarios.** If you're using Django ORM, inspectdb is the obvious choice for reverse engineering databases. It's built-in, well-documented, and generates idiomatic Django code.

**Recommendation:**
- Use for all Django-based database reverse engineering
- Not applicable for SQLAlchemy projects (use sqlacodegen instead)
- Treat output as starting point, not final code
- Essential tool in Django developer toolkit

**Key Insight:** This comparison highlights that schema inspection tools are ORM-specific. Django and SQLAlchemy have parallel ecosystems with similar tools serving the same purposes.
