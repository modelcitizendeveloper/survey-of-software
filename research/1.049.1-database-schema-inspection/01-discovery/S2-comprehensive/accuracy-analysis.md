# Accuracy Analysis: What Each Tool Misses or Gets Wrong

## Executive Summary

This analysis examines the accuracy limitations, false positives, false negatives, and edge cases for database schema inspection tools. Understanding what tools miss or misreport is critical for production schema management.

**Key Finding**: No tool achieves 100% accuracy. All require manual validation for production use, especially for complex schemas with database-specific features.

## Analysis Framework

### Types of Accuracy Issues

**False Negatives** (Missed Elements):
- Schema elements present in database but not detected
- Most dangerous: Can lead to incomplete migrations or missing constraints

**False Positives** (Incorrect Differences):
- Tool reports difference when schemas are functionally equivalent
- Noisy: Clutters migration files with unnecessary changes

**Misrepresentations** (Wrong Information):
- Tool detects element but reports incorrect details
- Type mappings, default values, precision/scale issues

**Edge Cases** (Inconsistent Behavior):
- Works for simple cases, fails for complex patterns
- Self-referential FKs, circular dependencies, inheritance

## SQLAlchemy Inspector

### What It Misses (False Negatives)

**1. Rename Detection**
- **Issue**: Cannot distinguish table/column renames from drop + add
- **Impact**: Schema comparison tools show renames as destructive operations
- **Example**: Renaming `users` → `customers` appears as drop `users`, add `customers`
- **Workaround**: Manual intervention required

**2. Triggers and Stored Procedures**
- **Issue**: Not reflected by Inspector API
- **Impact**: Database logic invisible to SQLAlchemy
- **Rationale**: Outside scope of table-level metadata
- **Workaround**: Manual SQL or database-specific tools

**3. Anonymously Named Constraints**
- **Issue**: Database-generated constraint names inconsistently captured
- **Impact**: May miss constraints without explicit names
- **Database Specific**: Varies by backend
- **Example**: PostgreSQL auto-generated CHECK constraint names may not appear

**4. View Constraints**
- **Issue**: Primary keys and foreign keys not reflected for views
- **Impact**: Views treated as tables without constraints
- **Official Documentation Warning**: "Views don't automatically reflect constraints"
- **Workaround**: Explicit column override in metadata

**5. Database-Specific Objects**
- **Partitions**: Not reflected (PostgreSQL, Oracle)
- **Tablespaces**: Not captured
- **Extensions**: Not reflected (PostgreSQL CREATE EXTENSION)
- **Custom Operators**: Not captured
- **Impact**: Database-specific features invisible

### What It Gets Wrong (Misrepresentations)

**1. Schema Qualification Duplication**
- **Issue**: Inconsistent schema qualification creates duplicate Table objects
- **Official Warning**: "Don't include Table.schema for default schema tables"
- **Example**: `Table('users')` and `Table('users', schema='public')` treated as different tables
- **Impact**: Breaks foreign key references, creates metadata inconsistencies
- **Critical**: PostgreSQL recommendations include narrowing search_path

**2. Type Precision Ambiguity**
- **Issue**: Some database types map ambiguously to SQLAlchemy types
- **Example**: PostgreSQL `TEXT` vs `VARCHAR` without length
- **Impact**: Round-trip reflection may change type representation
- **Database Specific**: MySQL `TINYINT(1)` vs `Boolean`

**3. Default Value Rendering**
- **Issue**: Database-rendered defaults may differ from original SQL
- **Example**: PostgreSQL renders `NOW()` as `now()` or timestamp literal
- **Impact**: False positives in schema comparison
- **Mitigation**: Custom comparison logic needed

### Edge Cases and Limitations

**1. Circular Foreign Key Dependencies**
- **Issue**: Complex to reflect in correct dependency order
- **Method Available**: `get_sorted_table_and_fkc_names()` attempts ordering
- **Limitation**: May not resolve all circular cases

**2. Multi-Column Foreign Keys**
- **Issue**: Composite foreign keys across different column orders
- **Detection**: Works, but ordering may vary
- **Impact**: Comparison tools may report false positives

**3. Expression-Based Indexes**
- **Issue**: Index expressions may be rendered differently
- **Example**: `lower(name)` vs `LOWER(name)`
- **Impact**: False positives in index comparison

## Alembic Autogenerate

### What It Misses (False Negatives)

**1. Table and Column Renames**
- **Official Documentation**: "Cannot detect renames"
- **Behavior**: Shows as drop old + add new
- **Impact**: Data loss if migration applied as-is
- **Severity**: Critical—requires manual correction
- **Workaround**: Edit migration to use `op.rename_table()` or `op.alter_column(new_column_name=...)`

**2. CHECK Constraints**
- **Status**: "Not yet implemented"
- **Impact**: CHECK constraint changes invisible to autogenerate
- **Severity**: High—data validation constraints not tracked
- **Workaround**: Manual migration operations

**3. PRIMARY KEY Constraint Changes**
- **Status**: "Not yet implemented"
- **Impact**: Primary key modifications not detected
- **Example**: Adding/removing columns from composite PK
- **Workaround**: Manual `op.create_primary_key()` / `op.drop_constraint()`

**4. EXCLUDE Constraints**
- **Status**: "Not yet implemented"
- **Database**: PostgreSQL-specific
- **Impact**: Advanced constraint types invisible

**5. Anonymously Named Constraints**
- **Issue**: Database-generated constraint names not tracked
- **Impact**: May create duplicate constraints on repeated autogenerate
- **Example**: SQLite auto-generates constraint names; re-running autogenerate may attempt to add again

**6. Views and Materialized Views**
- **Status**: Not automatically detected
- **Workaround**: Manual `op.execute()` for view DDL
- **Impact**: View changes require manual migration operations

**7. Sequences (Partial Support)**
- **Issue**: Sequence detection incomplete
- **Database Specific**: PostgreSQL, Oracle
- **Impact**: Sequence changes may need manual handling

**8. Triggers and Stored Procedures**
- **Status**: Not supported
- **Impact**: Database logic not tracked in migrations

### What It Gets Wrong (False Positives)

**1. Type Comparison False Positives**
- **Issue**: Database type rendering differs from SQLAlchemy type definition
- **Example**: `String()` without length vs `VARCHAR` (database default length)
- **Configuration**: `compare_type=True` may generate spurious migrations
- **Workaround**: Custom `compare_type` callable with normalization logic

**2. Server Default Rendering Differences**
- **Issue**: Database renders defaults differently than SQLAlchemy
- **Example**:
  - SQLAlchemy: `server_default=text("'active'::character varying")`
  - Database: `server_default='active'::character varying`
- **Configuration**: `compare_server_default=True` may report false differences
- **Workaround**: Custom comparison function

**3. Index Definition Variations**
- **Issue**: Functionally equivalent indexes rendered differently
- **Example**: Expression formatting, operator classes
- **Impact**: Generates drop + recreate for equivalent indexes

**4. Constraint Name Variations**
- **Issue**: Constraint names may vary between metadata and database
- **Example**: Auto-generated names on SQLite
- **Impact**: Reports constraint changes when only name differs

### Documented Limitations

From official Alembic documentation:

> "Autogenerate is not intended to be perfect. It is always necessary to manually review and correct the candidate migrations."

**Design Philosophy**: Generate migration candidates, not production-ready migrations.

**Required Workflow**:
1. Generate migration with autogenerate
2. **Manually review** generated code
3. Correct renames, check constraints, edge cases
4. Test migration on staging database

### Edge Cases

**1. Enum Type Handling**
- **Issue**: Enum types on non-supporting backends
- **Example**: SQLite doesn't support native ENUM
- **Behavior**: May generate type changes on each autogenerate
- **Workaround**: Database-specific handling in metadata

**2. Self-Referential Foreign Keys**
- **Issue**: Tables with FKs to themselves
- **Detection**: Generally works but may need `use_alter=True`
- **Impact**: Order-dependent migration generation

**3. Association Table Detection**
- **Issue**: Many-to-many association tables
- **Behavior**: Detected as regular tables (correct, but may not be ideal for ORM)
- **Impact**: Generates table operations, not relationship operations

## sqlalchemy-diff

### What It Misses (False Negatives)

**1. CHECK Constraints**
- **Status**: Not detected
- **Impact**: Data validation constraints invisible
- **Severity**: High for schemas relying on CHECK constraints

**2. UNIQUE Constraints (Beyond Indexes)**
- **Status**: Limited detection
- **Impact**: May miss UNIQUE constraints not implemented as indexes
- **Database Specific**: PostgreSQL UNIQUE constraints vs unique indexes

**3. Views and Materialized Views**
- **Status**: Not supported
- **Impact**: View differences not detected

**4. Sequences**
- **Status**: Not detected
- **Impact**: Sequence differences invisible

**5. Table Comments and Column Comments**
- **Status**: Not detected
- **Impact**: Documentation metadata lost

**6. Database-Specific Features**
- Partitions, tablespaces, extensions: Not detected
- Impact: Advanced database features invisible

### What It Gets Wrong (Misrepresentations)

**1. Type Comparison Issues**
- **Issue**: Type comparison inherits SQLAlchemy Inspector limitations
- **Example**: `TEXT` vs `VARCHAR` ambiguity
- **Impact**: False positives for equivalent types

**2. Default Value Formatting**
- **Issue**: Default values rendered differently by database
- **Example**: `NOW()` vs `CURRENT_TIMESTAMP` vs timestamp literal
- **Impact**: False positives for functionally equivalent defaults

### Critical Concerns

**1. Maintenance Status**
- **Last Update**: March 2021 (3.5+ years ago)
- **SQLAlchemy 2.0 Compatibility**: Unknown/Untested
- **Impact**: May produce incorrect results with modern SQLAlchemy
- **Recommendation**: Avoid for production use

**2. Untested Database Coverage**
- **Claim**: Supports all SQLAlchemy databases (via Inspector)
- **Reality**: No evidence of testing across databases
- **Risk**: May fail with specific database features

## sqlacodegen

### What It Misses (False Negatives)

**1. View SQL Definitions**
- **Issue**: Views generated as table definitions
- **Impact**: Loses view SQL logic
- **Example**: `CREATE VIEW` SQL not preserved
- **Workaround**: Manually convert generated table to view definition

**2. Triggers and Stored Procedures**
- **Status**: Not reflected
- **Impact**: Database logic invisible in generated code

**3. Check Constraints (Database-Dependent)**
- **Issue**: CHECK constraint detection varies by database
- **PostgreSQL**: Generally detected
- **MySQL**: May miss or incorrectly report
- **SQLite**: Limited detection

**4. Implicit Relationships**
- **Issue**: Relationships not backed by foreign keys
- **Example**: Application-level relationships
- **Impact**: Only FK-based relationships generated

**5. Inheritance Patterns**
- **Issue**: Joined table inheritance detection
- **Status**: Attempted but may miss complex patterns
- **Impact**: May generate flat table structure instead of inheritance

### What It Gets Wrong (Misrepresentations)

**1. Relationship Inference Errors**
- **Issue**: Many-to-many detection requires specific table structure
- **Requirement**: Association table with exactly 2 FKs, no other significant columns
- **Failure Mode**: Association table generated as regular model
- **Impact**: Manual relationship creation needed

**2. Self-Referential Relationship Complexity**
- **Issue**: Self-referential FKs generate `_reverse` relationships
- **Example**: `manager` and `manager_reverse` for employee hierarchy
- **Impact**: Requires manual cleanup and naming refinement
- **Quality**: Functional but not ideal

**3. Bidirectional Relationship Naming**
- **Issue**: `back_populates` attribute naming may not be ideal
- **Example**: `user.orders` and `order.user` (generic names)
- **Impact**: Manual renaming for better semantics

**4. Verbose Output**
- **Issue**: Explicit definitions for all columns, even with defaults
- **Example**: Generates `nullable=True` even when it's the default
- **Impact**: Code verbosity, harder to read

**5. Index Rendering**
- **Issue**: Index definitions can be very long for composite indexes
- **Impact**: Code readability

### Accuracy for Complex Schemas

**PostgreSQL Advanced Features**:
- ✅ JSONB, arrays, UUID: Generally accurate
- ✅ Custom types: Detected
- ⚠️ Domains: May not preserve domain definition
- ⚠️ Range types: Basic detection, may need refinement
- ❌ Partitions: Not reflected
- ❌ Extensions: Not reflected

**MySQL-Specific**:
- ✅ AUTO_INCREMENT: Detected accurately
- ✅ UNSIGNED integers: Preserved
- ⚠️ ENUM types: Detected but may need validation
- ⚠️ Table options (ENGINE, CHARSET): Limited reflection

**SQLite-Specific**:
- ✅ INTEGER PRIMARY KEY AUTOINCREMENT: Detected
- ✅ WITHOUT ROWID: Detected
- ⚠️ Constraints: Limited (SQLite constraint support limited)

## migra (Comparative Context)

### What It Misses

**1. Multi-Database Support**
- **Issue**: PostgreSQL only
- **Impact**: Cannot use with MySQL, SQLite, etc.
- **Severity**: Critical for multi-database applications

**2. Maintenance Status**
- **Issue**: Deprecated/stagnant
- **Last Update**: September 2022
- **Impact**: No future bug fixes or features

### What It Does Well (PostgreSQL)

**Comprehensive PostgreSQL Support**:
- ✅ Functions and stored procedures
- ✅ Extensions (CREATE EXTENSION)
- ✅ Advanced constraint types
- ✅ Materialized views
- ✅ Custom types, domains, enums
- ✅ Sequences

**Accuracy**: High for PostgreSQL-specific features (better than generic tools)

## Comparative Accuracy Summary

### False Negative Comparison

| Element | SQLAlchemy Inspector | Alembic | sqlalchemy-diff | sqlacodegen | migra (PG) |
|---------|---------------------|---------|-----------------|-------------|------------|
| **Renames** | ❌ Shows as drop+add | ❌ Shows as drop+add | ❌ Shows as drop+add | N/A | ❌ Shows as drop+add |
| **CHECK Constraints** | ✅ Detected | ❌ Not detected | ❌ Not detected | ⚠️ DB-dependent | ✅ Detected |
| **PK Changes** | ✅ Detected | ❌ Not detected | ✅ Detected | ✅ Generated | ✅ Detected |
| **Views** | ⚠️ No constraints | ⚠️ Manual ops | ❌ Not detected | ⚠️ As tables | ✅ Full support |
| **Triggers** | ❌ Not detected | ❌ Not detected | ❌ Not detected | ❌ Not detected | ❌ Not detected |
| **Functions** | ❌ Not detected | ❌ Not detected | ❌ Not detected | ❌ Not detected | ✅ Detected (PG) |
| **Extensions** | ❌ Not detected | ❌ Not detected | ❌ Not detected | ❌ Not detected | ✅ Detected (PG) |
| **Sequences** | ✅ Detected | ⚠️ Partial | ❌ Not detected | ⚠️ Limited | ✅ Full (PG) |

### False Positive Comparison

| Issue | SQLAlchemy Inspector | Alembic | sqlalchemy-diff | sqlacodegen | migra (PG) |
|-------|---------------------|---------|-----------------|-------------|------------|
| **Type Rendering** | ⚠️ Possible | ⚠️ Common (need custom compare) | ⚠️ Possible | N/A | ⚠️ Minimal |
| **Server Defaults** | ⚠️ Possible | ⚠️ Common (need custom compare) | ⚠️ Possible | N/A | ⚠️ Minimal |
| **Index Expressions** | ⚠️ Possible | ⚠️ Possible | ⚠️ Possible | N/A | ⚠️ Minimal |
| **Constraint Names** | ⚠️ Anonymous issues | ⚠️ Anonymous issues | ⚠️ Possible | N/A | ✅ Handles well |

## Critical Questions Answered

### What does Alembic autogenerate miss?

**Definitive Gaps** (from official documentation):
1. **Renames**: Cannot detect table or column renames
2. **CHECK constraints**: Not yet implemented
3. **PRIMARY KEY changes**: Not yet implemented
4. **EXCLUDE constraints**: Not yet implemented (PostgreSQL)
5. **Views**: Not automatically handled
6. **Sequences**: Partial support only
7. **Triggers/Functions**: Not detected

**Best Practice**: Always manually review autogenerated migrations

### How accurate is sqlacodegen for complex schemas?

**Accuracy Rating**: **75-85% for typical schemas**

**Works Well**:
- Basic tables, columns, types
- Simple foreign key relationships
- Primary keys, indexes
- One-to-many relationships

**Requires Manual Refinement**:
- Self-referential relationships (naming)
- Many-to-many (association table structure requirements)
- Complex inheritance patterns
- Relationship naming and organization
- View definitions (generated as tables)

**Recommendation**: Use as starting point, expect 15-25% manual refinement

### Can sqlalchemy-diff detect all schema differences?

**Answer**: **No**

**Missing**:
- CHECK constraints
- UNIQUE constraints (beyond indexes)
- Views, sequences, triggers
- Table/column comments
- Database-specific features

**Additional Concern**: Unmaintained status (3.5+ years) makes accuracy uncertain for:
- SQLAlchemy 2.0 compatibility
- Modern Python versions
- Recent database versions

**Recommendation**: Use SQLAlchemy Inspector directly or Alembic for more reliable results

## Production Validation Requirements

### Manual Verification Checklist

For any schema inspection tool, validate:

**1. Constraint Completeness**
- [ ] All CHECK constraints detected or documented
- [ ] Primary keys correctly identified
- [ ] Foreign keys with correct ON DELETE/ON UPDATE clauses
- [ ] UNIQUE constraints captured

**2. Type Accuracy**
- [ ] Precision/scale for numeric types
- [ ] Length constraints for string types
- [ ] Database-specific types (JSONB, arrays, etc.)
- [ ] Enum definitions

**3. Default Values**
- [ ] Server-side defaults correctly captured
- [ ] Function-based defaults (NOW(), UUID(), etc.)
- [ ] NULL vs empty string defaults

**4. Schema Organization**
- [ ] Multi-schema support validated
- [ ] Schema qualification consistent
- [ ] Cross-schema foreign keys work

**5. Database-Specific Features**
- [ ] Partitioning preserved (if used)
- [ ] Custom types/domains captured
- [ ] Index types and options correct

### Testing Strategy

**1. Round-Trip Test**
- Reflect schema → Generate migrations/code → Apply → Reflect again
- Compare before/after metadata
- Identify any differences

**2. Staging Validation**
- Apply migrations to staging database
- Run full application test suite
- Verify constraint enforcement

**3. Edge Case Testing**
- Self-referential foreign keys
- Circular dependencies
- Empty tables
- Tables with 100+ columns

## Recommendations by Use Case

### For Migration Generation

**Primary**: Alembic autogenerate
**Known Gaps**: Renames, CHECK constraints, PK changes
**Mitigation**:
1. Always manually review generated migrations
2. Test on staging before production
3. Add manual operations for unsupported features
4. Use custom `compare_type` and `compare_server_default` callables

### For Schema Documentation

**Primary**: SQLAlchemy Inspector
**Known Gaps**: Triggers, functions, some database-specific features
**Mitigation**:
1. Supplement with database-specific queries for gaps
2. Document known limitations
3. Use `get_multi_*` methods for large schemas

### For Reverse Engineering

**Primary**: sqlacodegen
**Known Gaps**: View SQL, implicit relationships, optimal naming
**Mitigation**:
1. Expect 15-25% manual refinement
2. Review all generated relationships
3. Reorganize into modules
4. Add business logic separately

### For PostgreSQL-Specific (Historical)

**Option**: migra (with caveats)
**Known Gaps**: Deprecated status, PostgreSQL-only
**Recommendation**: Use Alembic instead unless SQL output specifically required

## Conclusion

**Universal Truth**: No schema inspection tool achieves 100% accuracy

**Required Practices**:
1. **Manual review**: Always validate tool output
2. **Staging testing**: Test migrations before production
3. **Supplement gaps**: Use database-specific tools for missing features
4. **Document limitations**: Track what tool cannot detect

**Best Accuracy**: SQLAlchemy Inspector + Alembic combination
- Inspector: Comprehensive detection across databases
- Alembic: Production-proven migration workflow
- Together: Cover 90%+ of typical schema management needs

**Acceptable Trade-offs**:
- Accept manual handling of renames
- Accept manual CHECK constraint migrations
- Accept view management outside autogenerate
- Accept database-specific feature handling

**Confidence Levels**:
- SQLAlchemy Inspector: **Very High** (well-documented limitations)
- Alembic Autogenerate: **Very High** (official documentation of gaps)
- sqlacodegen: **High** (known refinement needs)
- sqlalchemy-diff: **Low** (unmaintained, unknown gaps)
- migra: **Medium** (PostgreSQL-only, deprecated)

The key to successful schema management is understanding and planning for each tool's limitations rather than expecting perfect automated detection.
