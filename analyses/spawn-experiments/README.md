# spawn-experiments Database System

**Purpose**: Database-driven tracking for spawn-experiments methodology research, replacing manual markdown aggregation with queryable structured data.

**Status**: Phase 1 - SQLite Foundation
**Version**: 1.0
**Date**: October 31, 2025

---

## Overview

This database system tracks the complete experiment lifecycle:

1. **Roadmap** → Long-term research priorities (1-2 year vision)
2. **Next Experiments** → Short-term checklist (HIGH/MEDIUM/LOW priority)
3. **Experiment Index** → All experiments (planned + in-progress + completed)
4. **Completed Experiments** → Finished experiments with methodology results
5. **Findings** → Research discoveries with validation progression
6. **Patterns** → Domain-specific methodology patterns

**Key Innovation**: Dual-mode operation (markdown + database)
- Markdown: Primary documentation (narrative, human-readable)
- Database: Structured data (queryable, analyzable)
- Auto-sync: Database updates markdown indexes automatically

---

## Quick Start

### 1. Create Database

```bash
# From spawn-solutions/applications/spawn-experiments/
sqlite3 spawn_experiments.db < schema.sql

# Verify creation
sqlite3 spawn_experiments.db "SELECT * FROM schema_version;"
# Output: 1.0.0|2025-10-31|Initial schema
```

### 2. Import Existing Experiments

```bash
# Run migration script (creates ~43 experiment records)
python migrate_from_markdown.py

# Verify import
sqlite3 spawn_experiments.db "SELECT COUNT(*) FROM experiments;"
# Output: 43

sqlite3 spawn_experiments.db "SELECT COUNT(*) FROM methodology_results;"
# Output: 172  (43 experiments × 4 methods)
```

### 3. Query Examples

```bash
# All completed experiments
sqlite3 spawn_experiments.db "SELECT id, title, domain FROM experiments WHERE status='completed';"

# Method 2 wins in LLM domain
sqlite3 spawn_experiments.db "SELECT * FROM v_experiments_with_winners WHERE domain='LLM Integration' AND method_number=2;"

# Finding validation progression
sqlite3 spawn_experiments.db "SELECT * FROM v_finding_validation ORDER BY n_value DESC;"
```

---

## Experiment Lifecycle Tracking

### Stage 1: Roadmap (Long-Term Planning)

**Source**: FUTURE_EXPERIMENTS_ROADMAP.md → `planned_experiments` table

**Columns**:
- `experiment_id`: Proposed ID (e.g., '1.810', '1.620')
- `title`: Experiment name
- `priority`: HIGH / MEDIUM / LOW
- `category`: Domain grouping (Simulation, Financial, API, Database)
- `depends_on`: JSON array of prerequisite experiments
- `expected_pattern`: Hypothesis about optimal methodology
- `is_completed`: FALSE (roadmap items not started yet)

**Query**:
```sql
-- High priority experiments not yet completed
SELECT experiment_id, title, category, expected_pattern
FROM planned_experiments
WHERE priority = 'HIGH' AND is_completed = 0
ORDER BY category;
```

**Example Data**:
```sql
INSERT INTO planned_experiments (experiment_id, title, priority, category, expected_pattern, estimated_hours)
VALUES
('1.810', 'REST API on Database Foundation', 'HIGH', 'Database', 'Method 2 or Method 3', 8.0),
('1.620', 'Cash Flow NPV Calculator', 'HIGH', 'Financial', 'Method 3 (deterministic algorithms)', 6.0),
('1.617', 'REST API Client', 'HIGH', 'API', 'Method 4 (library wrapper pattern)', 5.0);
```

### Stage 2: Next Experiments (Short-Term Checklist)

**Source**: NEXT_EXPERIMENTS_CHECKLIST.md → `planned_experiments` table

Same table as roadmap, but with:
- More detailed `spawn_solutions_synergy` notes
- Specific `expected_confidence_level` targets
- Cleared `depends_on` (prerequisites already met)

**Query**:
```sql
-- Next 5 experiments to execute
SELECT
    experiment_id,
    title,
    priority,
    spawn_solutions_synergy,
    expected_confidence_level
FROM planned_experiments
WHERE is_completed = 0
ORDER BY
    CASE priority
        WHEN 'HIGH' THEN 1
        WHEN 'MEDIUM' THEN 2
        WHEN 'LOW' THEN 3
    END,
    category
LIMIT 5;
```

**Workflow**:
1. Researcher picks experiment from checklist
2. Creates experiment directory: `experiments/1.810-rest-api/`
3. Updates `planned_experiments.is_completed = 1`
4. Creates new `experiments` record with `status = 'in_progress'`

### Stage 3: Experiment Index (All Experiments)

**Source**: EXPERIMENT_INDEX.md → `experiments` table

**Status Values**:
- `planned`: In roadmap or checklist, not started
- `in_progress`: Currently being executed
- `completed`: Finished with all 4 methodology results
- `blocked`: Waiting on dependencies or external factors

**Query**:
```sql
-- Complete experiment index
SELECT
    id,
    tier,
    domain,
    title,
    status,
    priority,
    completed_date
FROM experiments
ORDER BY
    status DESC,  -- completed first
    tier,
    id;
```

**Auto-Generation**:
```bash
# Generate updated EXPERIMENT_INDEX.md from database
python generate_index.py > ../../spawn-experiments/docs/EXPERIMENT_INDEX.md
```

### Stage 4: Completed Experiments

**Source**: Individual EXPERIMENT_REPORT.md files → `experiments` + `methodology_results` tables

**Data Captured**:
- Experiment metadata (tier, domain, title, dates)
- 4 methodology results (timing, LOC, quality, winner)
- Findings discovered/validated
- Patterns confirmed/deviated
- Components created/reused

**Query**:
```sql
-- All completed experiments with winners
SELECT
    e.id,
    e.title,
    e.domain,
    e.completed_date,
    mr.method_name AS winner,
    mr.quality_score,
    mr.time_minutes
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE e.status = 'completed'
  AND mr.is_winner = 1
ORDER BY e.completed_date DESC;
```

**Rich Queries**:
```sql
-- Average Method 4 quality by domain
SELECT
    e.domain,
    COUNT(*) as experiment_count,
    ROUND(AVG(mr.quality_score), 1) as avg_quality,
    MIN(mr.quality_score) as min_quality,
    MAX(mr.quality_score) as max_quality
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE mr.method_number = 4 AND e.status = 'completed'
GROUP BY e.domain
ORDER BY avg_quality DESC;
```

---

## Tracking Research Progress

### Finding Validation Progression

**Use Case**: Track how Finding #15 (Library Wrapper) evolved from N=1 to N=5

```sql
-- Finding #15 validation timeline
SELECT
    e.id,
    e.title,
    e.completed_date,
    ef.contribution_type,
    ROW_NUMBER() OVER (ORDER BY e.completed_date) as n_value
FROM experiment_findings ef
JOIN experiments e ON ef.experiment_id = e.id
WHERE ef.finding_id = (SELECT id FROM findings WHERE finding_number = 15)
ORDER BY e.completed_date;

-- Output:
-- 1.610 | Text Processing      | 2025-10-12 | discovered | 1  (N=1 PROVISIONAL)
-- 1.611 | Time Series          | 2025-10-14 | validated  | 2  (N=2)
-- 1.612 | Gradient Boosting    | 2025-10-16 | validated  | 3  (N=3)
-- 1.617 | REST API Client      | 2025-10-28 | validated  | 4  (N=4 ROBUST)
-- 1.623 | Financial Calculator | 2025-10-24 | validated  | 5  (N=5 VERY STRONG)
```

**Update Confidence**:
```sql
-- When N=4 reached, upgrade to ROBUST
UPDATE findings
SET confidence_level = 'ROBUST',
    n_value = 4,
    date_validated = '2025-10-28'
WHERE finding_number = 15;
```

### Pattern Validation Tracking

**Use Case**: Monitor DES pattern confidence (PROVISIONAL → ROBUST → VERY STRONG)

```sql
-- Pattern validation count
SELECT
    p.name,
    p.optimal_method,
    p.confidence,
    p.n_experiments,
    COUNT(ep.experiment_id) as actual_validations,
    GROUP_CONCAT(e.id || ' (' || mr.quality_score || ')', ', ') as results
FROM patterns p
JOIN experiment_patterns ep ON p.id = ep.pattern_id
JOIN experiments e ON ep.experiment_id = e.id
JOIN methodology_results mr ON e.id = mr.experiment_id
    AND mr.method_number = p.optimal_method
WHERE p.name = 'Discrete Event Simulation'
GROUP BY p.id;

-- Output:
-- DES | 3 | ROBUST | 4 | 4 | 1.700 (100), 1.701 (98), 1.702 (98), 1.703 (99)
```

**Auto-Update Pattern**:
```sql
-- After completing 1.703 (4th DES experiment)
UPDATE patterns
SET confidence = 'ROBUST',
    n_experiments = 4,
    last_validated = '2025-10-20'
WHERE name = 'Discrete Event Simulation';
```

### Research Gap Analysis

**Use Case**: Identify spawn-solutions libraries without methodology validation

```sql
-- spawn-solutions libraries (1.XXX) needing validation
SELECT
    ss.id,
    ss.title,
    ss.domain,
    CASE
        WHEN ss.id IN (SELECT spawn_solutions_id FROM spawn_experiments_validation)
        THEN 'Validated'
        ELSE 'NEEDS VALIDATION'
    END as status
FROM spawn_solutions_research ss
WHERE ss.tier = 1  -- Libraries only
  AND ss.status = 'completed'
ORDER BY status, ss.id;

-- Example output:
-- 1.022 | Optimization Libraries    | NEEDS VALIDATION
-- 1.033 | NLP Libraries             | NEEDS VALIDATION
-- 1.056 | JSON Libraries            | NEEDS VALIDATION
-- 1.060 | Cryptographic Libraries   | NEEDS VALIDATION
-- 1.120 | DES Libraries             | Validated (via 1.700-1.703)
-- 1.127 | Financial Simulation      | Validated (via 1.611, 1.623)
```

---

## Database Queries by Use Case

### Methodology Performance Analysis

```sql
-- Best methodology by domain
WITH domain_winners AS (
    SELECT
        e.domain,
        mr.method_number,
        mr.method_name,
        COUNT(*) as wins,
        ROUND(AVG(mr.quality_score), 1) as avg_quality
    FROM experiments e
    JOIN methodology_results mr ON e.id = mr.experiment_id
    WHERE mr.is_winner = 1 AND e.status = 'completed'
    GROUP BY e.domain, mr.method_number
)
SELECT
    domain,
    method_name,
    wins,
    avg_quality,
    RANK() OVER (PARTITION BY domain ORDER BY wins DESC) as rank
FROM domain_winners
ORDER BY domain, rank;
```

### Experiment Planning Priorities

```sql
-- Next experiments to reach ROBUST confidence
SELECT
    pe.experiment_id,
    pe.title,
    pe.category,
    p.name as pattern_name,
    p.n_experiments as current_n,
    p.confidence,
    CASE
        WHEN p.n_experiments >= 4 THEN 'ROBUST (complete)'
        WHEN p.n_experiments = 3 THEN '1 more for ROBUST'
        WHEN p.n_experiments = 2 THEN '2 more for ROBUST'
        ELSE 'NEW PATTERN'
    END as gap_analysis
FROM planned_experiments pe
LEFT JOIN patterns p ON pe.category LIKE '%' || REPLACE(p.name, ' Tasks', '') || '%'
WHERE pe.is_completed = 0
  AND pe.priority = 'HIGH'
ORDER BY p.n_experiments DESC;
```

### Cross-Repository Integration

```sql
-- spawn-solutions experiments with spawn-experiments methodology data
SELECT
    ss.id as solutions_id,
    ss.title as solutions_title,
    se.id as experiments_id,
    se.title as experiments_title,
    sev.validation_type,
    mr.method_number as optimal_method,
    mr.quality_score
FROM spawn_solutions_research ss
JOIN spawn_experiments_validation sev ON ss.id = sev.spawn_solutions_id
JOIN experiments se ON sev.spawn_experiments_id = se.id
JOIN methodology_results mr ON se.id = mr.experiment_id AND mr.is_winner = 1
ORDER BY ss.id;
```

### Component Reuse Tracking

```sql
-- Components created in Tier 1, reused in Tier 2
SELECT
    c.name as component,
    e_created.id as created_in,
    e_created.title as created_experiment,
    COUNT(ec_reused.experiment_id) as reuse_count,
    GROUP_CONCAT(e_reused.id, ', ') as reused_in
FROM components c
JOIN experiments e_created ON c.experiment_created = e_created.id
LEFT JOIN experiment_components ec_reused ON c.id = ec_reused.component_id
    AND ec_reused.usage_type = 'reused'
LEFT JOIN experiments e_reused ON ec_reused.experiment_id = e_reused.id
GROUP BY c.id
HAVING reuse_count > 0
ORDER BY reuse_count DESC;
```

---

## Dual-Mode Operation Workflow

### Adding a New Experiment

**Step 1: Plan Experiment** (in roadmap or checklist)
```sql
-- Add to planned_experiments
INSERT INTO planned_experiments (experiment_id, title, priority, category, expected_pattern)
VALUES ('1.810', 'REST API on Database', 'HIGH', 'Database', 'Method 2 or Method 3');
```

**Step 2: Start Experiment**
```sql
-- Create experiment record
INSERT INTO experiments (id, tier, domain, title, status, task_type)
VALUES ('1.810', 1, 'Database Integration', 'REST API on Database Foundation', 'in_progress', 'Layered Architecture');

-- Mark planned experiment as started
UPDATE planned_experiments
SET is_completed = 1,
    completed_experiment_id = '1.810',
    completion_date = DATE('now')
WHERE experiment_id = '1.810';
```

**Step 3: Log Methodology Results** (as experiment progresses)
```sql
-- Method 1 completed
INSERT INTO methodology_results (experiment_id, method_number, method_name, time_minutes, lines_of_code, quality_score, rank)
VALUES ('1.810', 1, 'Immediate', 8.5, 245, 78, 4);

-- Method 2 completed
INSERT INTO methodology_results (experiment_id, method_number, method_name, time_minutes, lines_of_code, quality_score, rank, is_winner)
VALUES ('1.810', 2, 'Specification-Driven', 12.0, 456, 94, 1, 1);

-- ... Method 3 and 4
```

**Step 4: Complete Experiment**
```sql
-- Mark as completed
UPDATE experiments
SET status = 'completed',
    completed_date = DATE('now'),
    key_finding = 'Database API layer favors upfront design (Method 2)'
WHERE id = '1.810';

-- Link to findings (if validates existing finding)
INSERT INTO experiment_findings (experiment_id, finding_id, contribution_type)
VALUES ('1.810', (SELECT id FROM findings WHERE finding_number = 17), 'validated');

-- Link to patterns
INSERT INTO experiment_patterns (experiment_id, pattern_id, validates_pattern)
VALUES ('1.810', (SELECT id FROM patterns WHERE name = 'Database Models'), 1);
```

**Step 5: Auto-Generate Markdown**
```bash
# Regenerate EXPERIMENT_INDEX.md from database
python generate_index.py > ../../spawn-experiments/docs/EXPERIMENT_INDEX.md

# Regenerate NEXT_EXPERIMENTS_CHECKLIST.md
python generate_checklist.py > ../../spawn-experiments/docs/NEXT_EXPERIMENTS_CHECKLIST.md

# Git commit (markdown + sqlite updated)
git add docs/EXPERIMENT_INDEX.md docs/NEXT_EXPERIMENTS_CHECKLIST.md applications/spawn-experiments/spawn_experiments.db
git commit -m "Complete 1.810: REST API on Database (Method 2 winner: 94/100)"
```

---

## File Structure

```
spawn-solutions/applications/spawn-experiments/
├── README.md                      # This file
├── DATABASE_STRATEGY.md           # Strategic analysis & decision framework
├── schema.sql                     # SQLite schema (tables, indexes, views)
├── spawn_experiments.db           # SQLite database file
│
├── migration/
│   ├── migrate_from_markdown.py   # Import EXPERIMENT_INDEX.md → database
│   ├── migrate_findings.py        # Import findings from markdown
│   ├── migrate_patterns.py        # Import patterns
│   └── validate_data.py           # Verify database vs markdown consistency
│
├── queries/
│   ├── query_helpers.py           # Python helper functions
│   ├── common_queries.sql         # Cookbook of useful queries
│   ├── finding_validation.sql     # Finding progression queries
│   └── pattern_analysis.sql       # Pattern validation queries
│
└── generators/
    ├── generate_index.py          # Database → EXPERIMENT_INDEX.md
    ├── generate_checklist.py      # Database → NEXT_EXPERIMENTS_CHECKLIST.md
    └── generate_summary.py        # Database → research summary reports
```

---

## Next Steps

### Immediate (This Week)

1. ✅ Create schema.sql
2. ✅ Write DATABASE_STRATEGY.md
3. ✅ Write README.md (this file)
4. ⏳ Create `migrate_from_markdown.py` script
5. ⏳ Test with 5-10 sample experiments

### Short-Term (Next 2-4 Weeks)

6. Import all 43 experiments
7. Create query helper functions
8. Build auto-generation scripts (markdown from database)
9. Integrate with experiment framework

### Medium-Term (1-2 Months)

10. Streamlit dashboard for visual queries
11. Automated finding confidence upgrades
12. Cross-repository gap analysis

---

## Support

**Documentation**:
- Database schema: `schema.sql`
- Strategic rationale: `DATABASE_STRATEGY.md`
- Query examples: `queries/common_queries.sql`

**Common Issues**:
- Database locked: Close all sqlite3 connections
- Schema errors: Check SQLite version (`sqlite3 --version` should be 3.35+)
- Migration failures: Validate markdown format first

**Contact**: spawn-experiments research team

---

**Version**: 1.0
**Last Updated**: October 31, 2025
**Next Review**: After Phase 1 completion (2-4 weeks)
