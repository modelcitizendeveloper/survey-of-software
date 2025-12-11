# spawn-experiments Database Strategy

**Application**: spawn-experiments (Methodology Research Framework)
**Current State**: Markdown-based experiment tracking (43+ experiments)
**Strategic Question**: When and how to migrate from markdown to database-driven tracking?
**Date**: October 31, 2025

---

## Executive Summary

**Recommendation**: **SQLite → PostgreSQL migration path** with dual-mode operation (markdown + database)

**Timeline**:
- **Phase 1 (Week 1-2)**: SQLite foundation, import 43 experiments
- **Phase 2 (Ongoing)**: Dual-mode operation (markdown narrative + database queries)
- **Phase 3 (6-12 months)**: PostgreSQL migration if multi-researcher access needed

**Investment**:
- Initial: 8-16 hours (schema design + migration script)
- Ongoing: 0-2 hours/experiment (automatic logging)
- Future PostgreSQL: $0-25/month (Neon/Supabase)

**ROI**:
- **Time savings**: 5-10 hours/month (automated queries vs manual markdown search)
- **New capabilities**: Cross-experiment analysis, pattern validation tracking, automated reporting
- **Risk reduction**: Structured data prevents inconsistencies in experiment metadata

---

## Problem Statement

### Current Markdown System

**What Works**:
- ✅ Human-readable documentation (EXPERIMENT_INDEX.md, EXPERIMENT_HISTORY.md)
- ✅ Version control via git (full audit trail)
- ✅ GitHub-friendly (renders beautifully in browser)
- ✅ Easy to edit (no database setup)
- ✅ Great for narrative documentation (research history, findings evolution)

**Pain Points**:
- ❌ **No queryability**: "Show all experiments where Method 2 won" requires manual search
- ❌ **Manual aggregation**: Calculating average Method 4 quality scores requires spreadsheets
- ❌ **Relationship tracking**: Experiments → Findings → Patterns tracked in prose, not structured
- ❌ **Cross-repository queries**: Cannot easily link spawn-experiments ↔ spawn-solutions research
- ❌ **Scaling challenges**: 43 experiments manageable, but 100+ becomes unwieldy
- ❌ **Data inconsistencies**: Experiment metadata format varies across markdown files

### Critical Use Cases Not Supported

1. **Pattern Validation Tracking**
   - "Show Finding #15 validation progression: N=1 (PROVISIONAL) → N=5 (VERY STRONG)"
   - Currently: Manual search through 5+ experiment reports
   - With database: 1 SQL query with join across experiments and findings

2. **Methodology Performance Analysis**
   - "What's average Method 2 quality score in LLM Creative domain?"
   - Currently: Open 6 experiment reports, extract scores, manual calculation
   - With database: Single aggregation query

3. **Research Gap Identification**
   - "Which spawn-solutions libraries (1.XXX) have methodology validation in spawn-experiments?"
   - Currently: Cross-reference two repositories manually
   - With database: Join query across repos

4. **Experiment Planning**
   - "What experiments are needed to reach ROBUST confidence (N=4) for DES pattern?"
   - Currently: Manual tracking in NEXT_EXPERIMENTS_CHECKLIST.md
   - With database: Automatic confidence calculation, gap analysis

---

## Solution: Three-Path Database Strategy

### Path 1 (DIY): SQLite Local Database ⭐ **RECOMMENDED START**

**Why SQLite?**
- Aligns with spawn-solutions philosophy: "DIY first to learn"
- Zero infrastructure cost ($0/month)
- File-based: `spawn_experiments.db` can be git-versioned (with careful schema design)
- Perfect for single researcher or small team (<5 people)
- Query via Python without server setup

**From spawn-solutions 3.040 research**:
> "DIY makes sense for <$5,000/month managed database spend"
>
> spawn-experiments: 0-100 researchers × $0/month = **DIY optimal**

**Technical Stack** (validated by spawn-experiments 1.800-1.802):
```python
sqlite3           # Python stdlib (zero dependencies)
sqlalchemy==2.0+  # ORM - Method 2 won 95/100 in 1.800
alembic==1.13+    # Migrations - Method 3 won 98/100 in 1.801
faker==22.0+      # Seeding - Method 3 won 94/100 in 1.802
```

**Setup Time**: 8-16 hours
- Schema design: 4-6 hours
- Migration script (markdown → SQLite): 2-4 hours
- Validation queries: 2-4 hours
- Documentation: 2-4 hours

**Ongoing Cost**: 0 hours/month (automatic logging from experiment framework)

### Path 2 (Open Standards): PostgreSQL Portability Layer

**Why PostgreSQL?**
- From spawn-solutions 2.050 research: "PostgreSQL = database portability standard"
- Zero vendor lock-in (portable across 50+ providers)
- Switch backends via config (1 hour) vs complete rewrite (20-40 hours)
- When standards exist, they're usually optimal choice

**Provider Options** (from 3.040 Database Services research):

| Provider | Free Tier | Paid Tier | Use Case |
|----------|-----------|-----------|----------|
| **Neon** | 0.5GB, scale-to-zero | $19/mo (always-on) | Best for serverless, database branching |
| **Supabase** | 500MB, 2 CPU-hours/day | $25/mo (8GB + auth + storage) | Best for bundle (auth + DB + storage) |
| **Railway** | $5 credit/month | Usage-based | Best for dev teams, simple pricing |
| **Render** | 90-day free PostgreSQL | $7/mo (256MB RAM) | Best for budget-conscious |

**When to Migrate from SQLite → PostgreSQL**:
- Multiple researchers need simultaneous access (SQLite = 1 writer limit)
- Need web interface for experiment queries
- >500 experiments (PostgreSQL performance benefits)
- Want advanced features (full-text search, JSON queries, vector extensions)

**Migration Complexity**: 4-8 hours
- SQLite schema → PostgreSQL schema (2-3 hours)
- Data export/import via pg_dump (1-2 hours)
- Update application config (1 hour)
- Validation (1-2 hours)

**From spawn-solutions 2.050 research**:
> "PostgreSQL portability means switching providers = 1-5 hours (config only)"

### Path 3 (Managed Services): Full Backend-as-a-Service

**When BaaS Makes Sense**:
- Need complete backend: Database + Auth + File Storage + Real-time
- Building web interface for public experiment explorer
- Multi-tenant deployment (separate databases per research team)

**Provider**: Supabase ($25/month)
- PostgreSQL (8GB)
- Row-level security (multi-tenant isolation)
- Auto-generated REST API (query experiments via HTTP)
- Real-time subscriptions (live experiment updates)
- Auth + Storage bundled (if web interface needed)

**From spawn-solutions 3.400 research**:
> "Supabase Pro $25/month = PostgreSQL + Auth + Storage versus $67+ unbundled"

**Current Assessment**: **NOT NEEDED**
- spawn-experiments = local research, not web service
- No auth requirements (local-only or SSH access)
- No file storage needs (experiment files in git)
- Verdict: **Overengineering for current needs**

---

## Recommended Architecture

### Dual-Mode Operation: Markdown + Database

**Philosophy**: Best of both worlds
- **Markdown**: Primary documentation (human-readable narrative)
- **Database**: Structured data (queryable metrics and relationships)
- **Auto-generation**: Database → Markdown index updates

**Data Flow**:
```
Experiment Completion
       ↓
  Log to Database (structured metrics)
       ↓
  Write to Markdown (narrative report)
       ↓
  Auto-generate updated EXPERIMENT_INDEX.md from DB
       ↓
  Git commit (markdown + sqlite file)
```

**What Stays in Markdown**:
- ✅ EXPERIMENT_REPORT.md (rich narrative, code samples, analysis)
- ✅ EXPERIMENT_HISTORY.md (chronological research story)
- ✅ Individual experiment findings (qualitative insights)
- ✅ README.md, guides, documentation

**What Moves to Database**:
- ✅ Experiment metadata (ID, tier, domain, status, dates)
- ✅ Methodology results (timing, LOC, quality scores, rankings)
- ✅ Findings (confidence levels, N-values, validation progression)
- ✅ Patterns (optimal methods, score ranges, experiment counts)
- ✅ Relationships (experiment → findings, patterns, components)

**Benefits**:
1. **Preserve git workflow**: Markdown still version-controlled
2. **GitHub-friendly**: Reports render beautifully in browser
3. **Enable queries**: Database unlocks analytics
4. **Automatic index generation**: EXPERIMENT_INDEX.md always up-to-date
5. **No breaking changes**: Existing tools/workflows continue working

---

## Database Schema

### Core Tables

```sql
-- Experiments: Core experiment metadata
CREATE TABLE experiments (
    id TEXT PRIMARY KEY,              -- '1.608', '1.608.A', '1.702'
    tier INTEGER NOT NULL,            -- 1, 2, 3, 4
    domain TEXT NOT NULL,             -- 'LLM Integration', 'Database', 'DES'
    domain_code TEXT,                 -- '1.6XX', '1.8XX', '1.7XX'

    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT,                   -- 'LLM Creative', 'Library Wrapper', 'DES'
    research_question TEXT,

    status TEXT CHECK(status IN ('planned', 'in_progress', 'completed', 'blocked')),
    priority TEXT CHECK(priority IN ('HIGH', 'MEDIUM', 'LOW', 'COMPLETE')),

    completed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Cross-references
    related_spawn_solutions TEXT,     -- JSON: ['1.127', '1.120']
    key_finding TEXT,
    report_path TEXT                  -- 'experiments/1.608-story-to-haiku/EXPERIMENT_REPORT.md'
);

-- Methodology Results: Performance metrics for each method
CREATE TABLE methodology_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id TEXT NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    method_number INTEGER NOT NULL CHECK(method_number BETWEEN 1 AND 4),
    method_name TEXT NOT NULL,        -- 'Immediate', 'Spec-Driven', 'TDD', 'Adaptive TDD'

    -- Core metrics
    time_minutes REAL,
    lines_of_code INTEGER,
    test_lines INTEGER,
    quality_score INTEGER CHECK(quality_score BETWEEN 0 AND 100),
    test_count INTEGER,
    coverage_percent REAL,

    -- Winner tracking
    is_winner BOOLEAN DEFAULT FALSE,
    rank INTEGER CHECK(rank BETWEEN 1 AND 4),

    -- Quality breakdown
    code_quality INTEGER,             -- /30
    test_quality INTEGER,             -- /30
    implementation_quality INTEGER,   -- /40

    -- Notes
    implementation_notes TEXT,
    strengths TEXT,
    weaknesses TEXT,

    UNIQUE(experiment_id, method_number)
);

-- Research Findings: Validated research discoveries
CREATE TABLE findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_number INTEGER UNIQUE NOT NULL,  -- 9, 10, 13, 14, 15, 16
    title TEXT NOT NULL,
    description TEXT NOT NULL,

    confidence_level TEXT NOT NULL CHECK(confidence_level IN
        ('PROVISIONAL', 'MODERATE', 'ROBUST', 'VERY STRONG', 'PROVEN')),
    n_value INTEGER NOT NULL,         -- Sample size (N=1, N=4, N=5)

    domain TEXT,                      -- 'LLM Creative', 'Library Wrapper', 'DES'
    category TEXT,                    -- 'Methodology Performance', 'Prompt Engineering'

    date_discovered DATE NOT NULL,
    date_validated DATE,
    status TEXT CHECK(status IN ('active', 'revised', 'rejected', 'superseded')),

    revision_notes TEXT,
    superseded_by INTEGER REFERENCES findings(id)
);

-- Experiment-Finding Relationships
CREATE TABLE experiment_findings (
    experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,
    finding_id INTEGER REFERENCES findings(id) ON DELETE CASCADE,
    contribution_type TEXT CHECK(contribution_type IN
        ('discovered', 'validated', 'refined', 'contradicted')),
    notes TEXT,
    PRIMARY KEY (experiment_id, finding_id)
);

-- Patterns: Domain-specific methodology patterns
CREATE TABLE patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,        -- 'LLM Creative Tasks', 'Library Wrapper', 'DES'
    optimal_method INTEGER NOT NULL CHECK(optimal_method BETWEEN 1 AND 4),
    method_name TEXT NOT NULL,

    confidence TEXT NOT NULL,         -- 'PROVISIONAL', 'ROBUST', 'VERY STRONG'
    n_experiments INTEGER NOT NULL,   -- How many experiments validate this

    typical_score_range TEXT,         -- '88-96/100'
    characteristic TEXT,              -- 'Complex error handling, prompt engineering'

    -- When to use this pattern
    use_when TEXT,
    examples TEXT,                    -- JSON array of experiment IDs

    created_date DATE,
    last_validated DATE
);

-- Experiment-Pattern Relationships
CREATE TABLE experiment_patterns (
    experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,
    pattern_id INTEGER REFERENCES patterns(id) ON DELETE CASCADE,
    validates_pattern BOOLEAN DEFAULT TRUE,
    deviates_from_pattern BOOLEAN DEFAULT FALSE,
    deviation_notes TEXT,
    PRIMARY KEY (experiment_id, pattern_id)
);
```

### Supporting Tables

```sql
-- Components: Reusable code from Tier 1 experiments
CREATE TABLE components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    path TEXT NOT NULL,
    experiment_created TEXT REFERENCES experiments(id),
    component_type TEXT,              -- 'function', 'class', 'module'
    description TEXT,
    reused_count INTEGER DEFAULT 0
);

CREATE TABLE experiment_components (
    experiment_id TEXT REFERENCES experiments(id) ON DELETE CASCADE,
    component_id INTEGER REFERENCES components(id) ON DELETE CASCADE,
    usage_type TEXT CHECK(usage_type IN ('created', 'reused', 'discovered', 'ignored')),
    discovery_method TEXT,            -- 'guided', 'autonomous', 'none'
    notes TEXT,
    PRIMARY KEY (experiment_id, component_id)
);

-- spawn-solutions Cross-References
CREATE TABLE spawn_solutions_research (
    id TEXT PRIMARY KEY,              -- '1.127', '3.040', '2.050'
    tier INTEGER,
    title TEXT NOT NULL,
    domain TEXT,
    status TEXT,
    synergy_notes TEXT,
    has_methodology_validation BOOLEAN DEFAULT FALSE
);

CREATE TABLE spawn_experiments_validation (
    spawn_solutions_id TEXT REFERENCES spawn_solutions_research(id),
    spawn_experiments_id TEXT REFERENCES experiments(id),
    validation_type TEXT,             -- 'library_wrapper', 'use_case', 'integration'
    notes TEXT,
    PRIMARY KEY (spawn_solutions_id, spawn_experiments_id)
);

-- Planned Experiments Checklist
CREATE TABLE planned_experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id TEXT UNIQUE,        -- '1.703', '1.620', '1.810'
    title TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('HIGH', 'MEDIUM', 'LOW')),
    category TEXT,                    -- 'Simulation', 'Financial', 'API', 'Database'

    depends_on TEXT,                  -- JSON: ['1.700', '1.701']
    expected_pattern TEXT,            -- 'Method 3 (Pure TDD) should win'
    spawn_solutions_synergy TEXT,    -- '1.127 Financial Simulation libraries'

    estimated_hours REAL,
    expected_confidence_level TEXT,   -- 'Will reach ROBUST at N=4'

    is_completed BOOLEAN DEFAULT FALSE,
    completed_experiment_id TEXT REFERENCES experiments(id),
    completion_date DATE
);
```

### Query Examples

**Pattern Validation Tracking**:
```sql
-- Track Finding #15 (Library Wrapper) validation progression
SELECT
    e.id,
    e.title,
    e.completed_date,
    f.confidence_level,
    f.n_value,
    mr.quality_score
FROM experiments e
JOIN experiment_findings ef ON e.id = ef.experiment_id
JOIN findings f ON ef.finding_id = f.id
JOIN methodology_results mr ON e.id = mr.experiment_id
    AND mr.method_number = 4  -- Method 4 wins library wrappers
WHERE f.finding_number = 15
ORDER BY e.completed_date;

-- Expected output:
-- 1.610 | Text Processing | 2025-10-12 | PROVISIONAL | 1 | 92
-- 1.611 | Time Series     | 2025-10-14 | PROVISIONAL | 2 | 96
-- 1.612 | Gradient Boost  | 2025-10-16 | ROBUST      | 3 | 98
-- 1.617 | REST API Client | 2025-10-28 | ROBUST      | 4 | 95
-- 1.623 | Financial Calc  | 2025-10-24 | VERY STRONG | 5 | 96
```

**Methodology Performance by Domain**:
```sql
-- Average scores by methodology and domain
SELECT
    e.domain,
    mr.method_number,
    mr.method_name,
    COUNT(*) as experiment_count,
    ROUND(AVG(mr.quality_score), 1) as avg_quality,
    ROUND(AVG(mr.time_minutes), 1) as avg_time,
    COUNT(CASE WHEN mr.is_winner THEN 1 END) as wins
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE e.status = 'completed'
GROUP BY e.domain, mr.method_number
ORDER BY e.domain, avg_quality DESC;
```

**Research Gap Analysis**:
```sql
-- spawn-solutions libraries WITHOUT methodology validation
SELECT
    ss.id,
    ss.title,
    ss.domain,
    ss.status
FROM spawn_solutions_research ss
WHERE ss.tier = 1  -- Libraries (1.XXX)
  AND ss.has_methodology_validation = FALSE
  AND ss.status = 'completed'
ORDER BY ss.id;
```

**Next Experiment Priority**:
```sql
-- High priority experiments to reach ROBUST confidence
SELECT
    pe.experiment_id,
    pe.title,
    pe.category,
    pe.expected_confidence_level,
    p.n_experiments as current_n,
    p.confidence as current_confidence
FROM planned_experiments pe
JOIN patterns p ON pe.expected_pattern LIKE '%' || p.name || '%'
WHERE pe.priority = 'HIGH'
  AND pe.is_completed = FALSE
  AND p.confidence IN ('PROVISIONAL', 'MODERATE')
ORDER BY pe.priority, current_n DESC;
```

---

## Migration Roadmap

### Phase 1: SQLite Foundation (Week 1-2)

**Goal**: Create local database with 43 experiments imported

**Tasks**:
1. **Schema Design** (4-6 hours)
   - Create `database/schema.sql` with tables above
   - Set up Alembic for migrations
   - Create SQLAlchemy models (leverage 1.800 learnings)

2. **Migration Script** (2-4 hours)
   - Parse EXPERIMENT_INDEX.md → experiments table
   - Parse EXPERIMENT_HISTORY.md → findings table
   - Parse NEXT_EXPERIMENTS_CHECKLIST.md → planned_experiments table
   - Validate data integrity

3. **Validation Queries** (2-4 hours)
   - Test 10 example queries
   - Verify data accuracy vs markdown
   - Document common queries

4. **Documentation** (2-4 hours)
   - README for database setup
   - Query cookbook
   - Contribution guide

**Deliverables**:
- `spawn_experiments.db` (SQLite file)
- `database/schema.sql`
- `scripts/migrate_from_markdown.py`
- `scripts/query_examples.py`

**Validation Criteria**:
- ✅ All 43 experiments imported
- ✅ Methodology results match EXPERIMENT_INDEX.md
- ✅ 10 example queries return correct results
- ✅ Database file <10MB (git-friendly)

### Phase 2: Dual-Mode Operation (Ongoing)

**Goal**: Maintain markdown + database in sync

**Implementation**:
```python
# experiments/framework/experiment_logger.py
class ExperimentLogger:
    def log_completion(self, experiment_id, results):
        # 1. Write to database (structured)
        self.db.save_experiment(experiment_id, results)

        # 2. Write markdown report (narrative)
        self.markdown.generate_report(experiment_id, results)

        # 3. Auto-update EXPERIMENT_INDEX.md
        self.markdown.regenerate_index_from_db()

        # 4. Git commit
        self.git.commit(f"Complete {experiment_id}")
```

**Tasks**:
1. **Logging Integration** (4-6 hours)
   - Hook into existing experiment framework
   - Automatic database logging on completion
   - Manual fallback for historical experiments

2. **Auto-Generation** (3-5 hours)
   - Generate EXPERIMENT_INDEX.md from database
   - Generate pattern summary tables
   - Update finding confidence levels

3. **Query Interface** (Optional, 4-8 hours)
   - Streamlit dashboard for visual queries
   - Export query results to markdown
   - Bookmark common queries

**Benefits**:
- ⏱️ **Time savings**: 5-10 hours/month (no manual index updates)
- 🔍 **Queryability**: Instant answers to research questions
- 📊 **Analytics**: Automated trend analysis
- ✅ **Consistency**: Database validates data integrity

### Phase 3: PostgreSQL Migration (Optional, 6-12 Months)

**Trigger Conditions**:
- Multiple researchers need simultaneous access
- Need web interface (public experiment explorer)
- >500 experiments (performance optimization)
- Want advanced PostgreSQL features (full-text search, JSON queries)

**Migration Path**:
```bash
# 1. Export SQLite schema
sqlite3 spawn_experiments.db .schema > schema.sql

# 2. Convert to PostgreSQL
# (minor syntax changes: AUTOINCREMENT → SERIAL, etc.)

# 3. Export data
sqlite3 spawn_experiments.db .dump > data.sql

# 4. Import to PostgreSQL
psql $DATABASE_URL < schema.sql
psql $DATABASE_URL < data.sql

# 5. Update application config
export DATABASE_URL="postgresql://user:pass@neon.tech/spawn_experiments"

# 6. Validate
python scripts/validate_migration.py
```

**Cost Analysis**:
- **Neon**: $0/month (0.5GB free tier) → $19/month (scale-to-zero paid)
- **Supabase**: $0/month (500MB free) → $25/month (8GB + auth + storage)
- **Railway**: $5/month credit → usage-based

**From spawn-solutions 3.040 research**:
> "Managed database saves $6,000-12,000/month engineering opportunity cost"

**spawn-experiments calculation**:
- SQLite maintenance: 0-2 hours/month = $0-300/month opportunity cost
- PostgreSQL cost: $0-25/month
- **Verdict**: SQLite sufficient unless multi-user access needed

---

## ROI Analysis

### Time Investment

**Initial Setup**:
- SQLite schema + migration: 8-16 hours
- Testing & validation: 2-4 hours
- Documentation: 2-4 hours
- **Total: 12-24 hours (1.5-3 days)**

**Ongoing Maintenance**:
- Automatic logging: 0 hours/experiment (integrated into framework)
- Manual queries: -5 hours/month (time saved vs manual markdown search)
- Database updates: 0-1 hours/month (schema evolution)
- **Net time savings: 4-5 hours/month**

**Break-even**: 3-5 months (12-24 hours initial ÷ 4-5 hours/month saved)

### Cost Investment

**SQLite Path (Current)**:
- Infrastructure: $0/month
- Engineering time: 0-2 hours/month = $0-300/month opportunity cost
- **Total: $0-300/month**

**PostgreSQL Path (Future, if needed)**:
- Infrastructure: $0-25/month (Neon/Supabase)
- Engineering time: 0-1 hours/month = $0-150/month
- **Total: $0-175/month** (20-58% reduction in time)

### Value Creation

**Queryability**:
- Before: "Show Method 2 wins in LLM domain" = 15-30 min manual search
- After: 1 SQL query, <10 seconds
- **Value: 15-30 minutes saved per query × 10 queries/month = 2.5-5 hours/month**

**Pattern Validation**:
- Before: Track Finding #15 validation manually across 5 experiments
- After: Automatic N-value tracking, confidence level progression
- **Value: Instant validation status, prevents missed experiments**

**Research Planning**:
- Before: Manually identify gaps (which patterns need more experiments?)
- After: Query "patterns with N<4" shows exact gap
- **Value: Data-driven experiment prioritization**

**Cross-Repository Integration**:
- Before: Manually cross-reference spawn-experiments ↔ spawn-solutions
- After: Join query shows validated vs unvalidated libraries
- **Value: Systematic coverage analysis**

### Total ROI

**First Year**:
- Investment: 12-24 hours + $0 (SQLite)
- Savings: 48-60 hours (4-5 hours/month × 12 months)
- **Net ROI: 24-48 hours saved (200-400% return)**

**At PostgreSQL Migration** (if needed):
- Additional investment: 4-8 hours + $0-300/year
- Additional savings: Multi-user access (unmeasurable value)
- **Net ROI: Depends on team size (2+ researchers = justified)**

---

## Risk Assessment

### Technical Risks

**Risk 1: Database file size exceeds git limits**
- **Likelihood**: Low (current 43 experiments = ~500KB, 500 experiments = ~5MB)
- **Impact**: Medium (need git-lfs or separate storage)
- **Mitigation**: Monitor file size, set 10MB threshold for git-lfs

**Risk 2: SQLite corruption**
- **Likelihood**: Very Low (SQLite is battle-tested)
- **Impact**: High (data loss)
- **Mitigation**:
  - Regular backups (git commits)
  - Validate integrity: `PRAGMA integrity_check`
  - Write-ahead logging: `PRAGMA journal_mode=WAL`

**Risk 3: Schema evolution complexity**
- **Likelihood**: Medium (research evolves, schema changes needed)
- **Impact**: Low (Alembic handles migrations)
- **Mitigation**: Use Alembic from day 1 (validated in 1.801)

### Process Risks

**Risk 4: Markdown-database sync failures**
- **Likelihood**: Medium (manual updates might skip database)
- **Impact**: Medium (data inconsistency)
- **Mitigation**:
  - Automatic logging in experiment framework
  - Validation script: compare markdown vs database
  - Documentation: "Always log to database first"

**Risk 5: Query complexity discourages usage**
- **Likelihood**: Low-Medium (SQL learning curve)
- **Impact**: Low (falls back to markdown)
- **Mitigation**:
  - Query cookbook with examples
  - Helper functions: `query_method_wins(domain='LLM')`
  - Optional Streamlit UI for non-SQL queries

### Organizational Risks

**Risk 6: Team resistance to new workflow**
- **Likelihood**: Low (single researcher currently)
- **Impact**: Low (optional tool, not required)
- **Mitigation**:
  - Gradual adoption (dual-mode operation)
  - Demonstrate value with example queries
  - Keep markdown as primary documentation

---

## Decision Framework

### When to Use SQLite (Current Recommendation)

**Use SQLite if**:
- ✅ Single researcher or small team (<5 people)
- ✅ Local development only
- ✅ <500 experiments
- ✅ Query complexity is moderate (no full-text search needed)
- ✅ Cost sensitivity (prefer $0/month infrastructure)

**spawn-experiments current state**: ✅ All criteria met → **SQLite optimal**

### When to Migrate to PostgreSQL

**Migrate to PostgreSQL if**:
- Multiple researchers need simultaneous write access
- Building web interface for public experiment explorer
- >500 experiments (performance optimization)
- Need advanced features:
  - Full-text search across experiment reports
  - JSON query operations (complex metadata)
  - Vector extensions (ML on experiment results)
  - Row-level security (multi-tenant research teams)

**spawn-experiments 6-12 month projection**: Likely still SQLite-appropriate

### When to Use Backend-as-a-Service

**Use Supabase/Firebase if**:
- Building public-facing web application
- Need authentication + database + storage + real-time
- Want auto-generated REST API
- Multi-tenant deployment (separate DBs per research group)

**spawn-experiments current state**: ❌ Not needed (local research tool)

---

## Implementation Plan

### Immediate Next Steps (This Week)

1. **Create directory structure** ✅ DONE
   ```
   spawn-solutions/applications/spawn-experiments/
   ├── DATABASE_STRATEGY.md          # This document
   ├── schema.sql                    # SQLite schema
   ├── models.py                     # SQLAlchemy models
   └── migration/
       ├── migrate_from_markdown.py  # Import script
       └── validate_data.py          # Validation
   ```

2. **Design schema** (4-6 hours)
   - Implement tables from "Database Schema" section
   - Create Alembic migration (leverage 1.801 learnings)
   - Test schema with sample data

3. **Write migration script** (2-4 hours)
   - Parse EXPERIMENT_INDEX.md → experiments + methodology_results
   - Parse findings from markdown → findings table
   - Validate data integrity

4. **Validate with queries** (2-4 hours)
   - Test 10 example queries from "Query Examples" section
   - Verify results match manual markdown search
   - Document any discrepancies

### Short-Term (Next 2-4 Weeks)

5. **Complete tables** (3-5 hours)
   - Add Findings table (parse from findings/ directory)
   - Add Patterns table (LLM Creative, Library Wrapper, DES)
   - Add spawn-solutions cross-references

6. **Auto-generation** (4-6 hours)
   - Script to generate EXPERIMENT_INDEX.md from database
   - Compare auto-generated vs current (validate accuracy)
   - Add auto-update to experiment logging

7. **Query cookbook** (2-3 hours)
   - Document 20-30 useful queries
   - Create helper functions for common queries
   - Add examples to README

### Medium-Term (1-2 Months)

8. **Integration with experiment framework** (6-8 hours)
   - Automatic database logging on experiment completion
   - Validate data before commit
   - Error handling and recovery

9. **Analytics dashboard** (Optional, 8-12 hours)
   - Streamlit app for visual queries
   - Charts: methodology performance over time
   - Pattern validation tracking visualization

10. **Documentation** (4-6 hours)
    - README: Setup, usage, contribution guide
    - Query examples with explanations
    - Troubleshooting guide

### Long-Term (3-6 Months)

11. **PostgreSQL evaluation** (if needed)
    - Monitor: Are multiple researchers blocked by SQLite?
    - Benchmark: Does query performance degrade at 200-300 experiments?
    - Decide: Is $0-25/month PostgreSQL justified?

12. **Advanced features** (if valuable)
    - Full-text search across experiment reports
    - ML on experiment results (predict optimal methodology)
    - Public API for experiment data

---

## Success Metrics

### Adoption Metrics

- **Query usage**: 5+ database queries per week (vs manual markdown search)
- **Auto-generation**: EXPERIMENT_INDEX.md updated from database 100% of time
- **Time savings**: 5-10 hours/month (tracked via experiment logging timestamps)

### Data Quality Metrics

- **Completeness**: 100% of experiments have methodology_results entries
- **Accuracy**: Database values match markdown reports (spot-check 10%)
- **Consistency**: Experiment IDs follow naming convention (T.DCC.V format)

### Research Velocity Metrics

- **Pattern validation**: Finding confidence levels update automatically
- **Gap identification**: Queries identify missing experiments (e.g., "need N=1 more for ROBUST")
- **Cross-repo integration**: spawn-solutions libraries have methodology validation tracking

---

## Conclusion

**Recommendation**: Implement SQLite database with dual-mode operation (markdown + database)

**Rationale**:
1. **Aligns with spawn-solutions philosophy**: DIY first (Path 1), learn before scaling
2. **Zero infrastructure cost**: SQLite = $0/month vs PostgreSQL = $19-25/month
3. **Validated approach**: spawn-experiments 1.800-1.802 validated SQLAlchemy + Alembic + Faker
4. **Incremental adoption**: Dual-mode preserves existing workflows while adding queryability
5. **Clear migration path**: SQLite → PostgreSQL when multi-user access needed (6-12 months)

**Next Action**: Create `schema.sql` and `migrate_from_markdown.py` this week

**Expected Outcome**:
- 12-24 hours initial investment
- 4-5 hours/month time savings (200-400% first-year ROI)
- Queryable experiment database unlocking pattern validation tracking, gap analysis, and cross-repository integration

---

**Document Version**: 1.0
**Last Updated**: October 31, 2025
**Next Review**: After Phase 1 completion (2-4 weeks)
**Owner**: spawn-experiments research team
