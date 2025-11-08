# S3: Need-Driven Discovery Approach

## Methodology Overview

**Core Philosophy**: Start with use cases, identify requirements, find best-fit libraries.

This approach begins with **generic requirement patterns** rather than existing solutions. We analyze what users actually need to accomplish, then evaluate which libraries best satisfy those needs.

## Key Differentiators from Other Stages

- **S1 (Landscape)**: Catalogs all available tools
- **S2 (Feature)**: Compares libraries feature-by-feature
- **S3 (Need-Driven)**: Matches use cases to best solutions
- **S4 (Strategic)**: Long-term viability and ecosystem fit

S3 is unique because it **reverses the analysis direction**: instead of asking "what does this library do?", we ask "which library solves this problem best?"

## Generic Use Case Pattern Framework

### Pattern Definition Structure

Each use case pattern follows this template:

1. **Requirement Statement**: What must be accomplished
2. **Input Parameters**: What varies (database size, complexity, types)
3. **Success Criteria**: How to measure if the need is met
4. **Constraints**: Performance, compatibility, safety requirements
5. **Library Fit Analysis**: Which tools handle this best, with evidence

### Six Core Patterns Analyzed

1. **Introspect Database Schema** - Read existing structure
2. **Detect Schema Differences** - Compare expected vs actual
3. **Validate Migration Safety** - Prevent destructive operations
4. **Reverse Engineer Models** - Generate code from database
5. **Multi-Database Support** - Work across PostgreSQL, MySQL, SQLite
6. **Performance at Scale** - Handle large schemas efficiently

## Analysis Process

### Step 1: Define Generic Pattern

Avoid application-specific scenarios like "validate my e-commerce product catalog" or "check my user authentication schema".

Instead, define generic patterns: "detect when database state differs from code models" or "introspect table structures regardless of domain".

### Step 2: Identify Requirement Variations

Parameters that change the solution fit:
- Database size (10 tables vs 10,000 tables)
- Database type (PostgreSQL vs MySQL vs SQLite)
- Operation type (read-only inspection vs write operations)
- Integration context (standalone tool vs ORM-integrated)
- Performance requirements (<100ms vs <10s)

### Step 3: Evaluate Library Fit

For each pattern, assess libraries against criteria:
- **Coverage**: Does it handle the full requirement?
- **Accuracy**: Are results correct and reliable?
- **Performance**: Speed for typical and large-scale scenarios
- **API Design**: Ease of use, documentation quality
- **Multi-Database**: Works across backends consistently?
- **Maintenance**: Actively developed, community support

### Step 4: Evidence-Based Comparison

Use concrete evidence:
- Official documentation examples
- GitHub issues revealing limitations
- Performance benchmarks
- Community adoption patterns
- Known gaps and workarounds

## Library Candidates Identified

From initial research, five primary libraries emerge:

1. **SQLAlchemy Core Reflection** - Built-in introspection API
2. **SQLAlchemy Inspector** - Low-level schema inspection interface
3. **Alembic Autogenerate** - Schema comparison for migrations
4. **migra** - PostgreSQL-specific diff tool (DEPRECATED but forked)
5. **sqlacodegen** - Reverse engineering to code
6. **sqlalchemy-diff** - Standalone schema comparison

## Evaluation Criteria Matrix

| Criterion | Weight | Rationale |
|-----------|--------|-----------|
| Use Case Coverage | 30% | Must handle majority of patterns |
| Multi-Database Support | 20% | PostgreSQL, MySQL, SQLite minimum |
| Performance | 15% | <1s for typical database |
| API Quality | 15% | Easy to use, well documented |
| Safety Features | 10% | Prevents data loss, accurate diffs |
| Active Maintenance | 10% | Recent updates, community support |

## Expected Outcome

The S3 analysis will produce:

1. **Per-Pattern Best Fit**: Which library handles each use case optimally
2. **Hybrid Recommendation**: When to combine multiple tools
3. **Gap Identification**: Needs not fully met by any library
4. **Confidence Assessment**: Evidence quality for each recommendation

## Methodology Constraints

**Pure S3 Analysis Rules**:
- No access to S1 (landscape survey)
- No access to S2 (feature comparison)
- No access to S4 (strategic analysis)
- Focus solely on matching needs to solutions
- Evidence from public documentation only
- Generic patterns, not specific applications

This ensures S3 provides an independent perspective that can validate or challenge findings from other stages.
