# Use Case: Data Engineers

## Who Needs This

**Persona:** Data engineers, ETL developers, data platform builders

**Context:**
- Comparing database states (before/after migrations)
- Validating ETL pipeline outputs (source vs transformed data)
- Monitoring data quality (detecting unexpected changes)
- Reconciling data between systems (source vs destination)
- Testing data transformations

**Scale:**
- 1000s-millions of records per comparison
- JSON, XML, CSV, Parquet data formats
- Nested structures (JSON objects with deep nesting)
- Daily reconciliation jobs (automated comparisons)

**Constraints:**
- Performance critical (large datasets, frequent comparisons)
- Type-awareness required (number vs string matters)
- Ignore rules needed (timestamps, IDs, auto-generated fields)
- Serializable diffs (save to database, analyze later)
- Production reliability (data pipelines depend on this)

## Why They Need It

**Problem:** Comparing structured data to detect unexpected changes:
1. After database migrations: did data transform correctly?
2. ETL validation: does output match expected transformations?
3. Data quality: are there unexpected schema/type changes?
4. System reconciliation: are two databases in sync?

**Requirements:**
- **MUST**: Compare structured data (JSON, XML, Python objects)
- **MUST**: Type-aware (int vs str, list vs tuple)
- **MUST**: Handle nested structures (deep recursion)
- **MUST**: Ignore specific fields (timestamps, auto-IDs)
- **MUST**: Performant (millions of comparisons)
- **SHOULD**: Serializable diffs (save for audit trail)
- **SHOULD**: Delta application (replay changes)

**Anti-Requirements:**
- Not for text files (use difflib for logs)
- Not for git integration (comparing data, not code)
- Not for semantic code analysis (data, not source code)

## Library Fit Analysis

### Recommended Solutions

**For Python objects / JSON:**
→ **DeepDiff**
- ✅ Type-aware comparison (detects schema changes)
- ✅ Deep recursion (handles nested JSON)
- ✅ Ignore rules (`exclude_paths` for timestamps)
- ✅ Delta support (serializable change sets)
- ✅ Custom operators (define comparison for custom types)
- ✅ JSON export (save diffs to database)
- ✅ Very active (15M downloads/month)

**For JSON (standards-focused):**
→ **jsondiff**
- ✅ RFC 6902 JSON Patch format (standardized)
- ✅ Multiple output syntaxes (compact, explicit)
- ✅ CLI tool (command-line comparisons)
- ⚠️ Less flexible than DeepDiff (fewer ignore options)
- ⚠️ Maintenance mode (stable but infrequent updates)

**For XML:**
→ **xmldiff**
- ✅ XML structure-aware (elements, attributes, namespaces)
- ✅ Patch generation/application (XUpdate format)
- ✅ Handles attribute order, whitespace normalization
- ⚠️ Requires lxml (C extension dependency)

**For CSV (after loading):**
→ **DeepDiff** on loaded data structures
- Load CSV into list of dicts (pandas, csv module)
- Use DeepDiff to compare
- Alternative: pandas DataFrame comparison (built-in)

### Decision Matrix

| Data Format | Primary Choice | Alternative | When Alternative |
|-------------|---------------|-------------|------------------|
| JSON | DeepDiff | jsondiff | Need RFC 6902 standard |
| Python objects | DeepDiff | - | Only realistic option |
| XML | xmldiff | difflib | Text diff sufficient |
| CSV | pandas | DeepDiff | Complex comparisons |
| Parquet | pandas | - | Use DataFrame API |
| Database rows | DeepDiff | - | After loading to dicts |

### Anti-Patterns

**❌ DON'T use difflib for structured data:**
- Loses structure (converts to text)
- Can't ignore specific fields
- Not type-aware (int vs str undetected)
- Unreadable output for nested JSON

**❌ DON'T use GitPython:**
- No benefit (not working with git repos)
- Process spawn overhead
- Requires git installed

**❌ DON'T use python-Levenshtein:**
- Edit distance only (doesn't show what changed)
- Character-level (wrong granularity for data)

### Decision Factors

**Choose DeepDiff when:**
- Comparing JSON, Python objects, nested structures
- Need type awareness (schema validation)
- Want ignore rules (timestamps, auto-generated fields)
- Need serializable diffs (save to database)

**Choose jsondiff when:**
- JSON-only comparisons
- Need RFC 6902 standard format (interoperability)
- Using CLI tools (command-line workflow)

**Choose xmldiff when:**
- XML-specific comparisons
- Structure matters (attribute order shouldn't cause failures)

**Choose pandas when:**
- Already using pandas for data processing
- CSV/Parquet/table comparisons
- Need DataFrame-level operations

## Validation Criteria

**You picked the right library if:**
- ✅ Detects type changes (int → str caught)
- ✅ Ignores irrelevant fields (timestamps don't fail comparisons)
- ✅ Shows exact path to changed fields (nested structures)
- ✅ Fast enough for production (handles large datasets)
- ✅ Diffs are serializable (can save for audit)

**Red flags (wrong choice):**
- ❌ Type changes go undetected (int vs str both pass)
- ❌ Can't ignore timestamps (every comparison fails)
- ❌ Unreadable output (can't find what changed)
- ❌ Too slow for production (minutes to compare)
- ❌ Can't save diffs (need audit trail)

## Common Patterns

**Pattern: ETL validation**
```
# Compare source records vs transformed records
source_data = fetch_from_source()
transformed = run_etl_pipeline()

diff = DeepDiff(
    source_data,
    transformed,
    exclude_paths=["root[*]['timestamp']", "root[*]['id']"],
    ignore_order=True  # List order doesn't matter
)

if diff:
    log_error(f"Unexpected changes: {diff}")
    save_diff_to_db(diff.to_json())
```

**Pattern: Database reconciliation**
```
# Compare two database states
db1_records = query_db1()
db2_records = query_db2()

diff = DeepDiff(db1_records, db2_records)

if diff:
    reconcile(diff)  # Fix inconsistencies
```

**Pattern: Schema validation**
```
# Detect unexpected type changes
expected_schema = load_schema()
actual_data = fetch_data()

diff = DeepDiff(
    expected_schema,
    actual_data,
    view='tree'  # Tree view for type changes
)

if 'type_changes' in diff:
    raise SchemaViolation(diff['type_changes'])
```

## Real-World Example

**Scenario:** Validating a database migration (millions of records)

**Requirements:**
- Compare pre-migration vs post-migration state
- Ignore auto-generated fields (created_at, updated_at, id)
- Detect type changes (schema validation)
- Save diff for audit trail
- Fast enough for production (complete in minutes)

**Solution:** DeepDiff with ignore rules
1. Export pre-migration records to JSON
2. Run migration
3. Export post-migration records
4. DeepDiff with `exclude_paths` for ignored fields
5. Verify only expected transformations present
6. Save diff.to_json() to audit database

**Why not difflib:** Loses structure, can't ignore fields, not type-aware

**Why not jsondiff:** Less flexible ignore rules, harder to integrate with audit database
