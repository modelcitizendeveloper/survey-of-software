# spawn-solutions Technology Intelligence Database Schema

**Purpose**: Track technology discoveries, comparisons, recommendations, and survival analysis
**Database**: SQLite 3.x → PostgreSQL migration path
**Version**: 1.0
**Date**: October 31, 2025

---

## Summary

This database enables **queryable technology intelligence** for the "hardware store for software":

1. **Discoveries**: Track 42+ technology research projects (DIY → Standards → Services)
2. **Technologies**: Individual libraries, frameworks, services evaluated
3. **Comparisons**: Head-to-head evaluations with quality scores
4. **Use Cases**: Match technologies to specific project requirements
5. **Migration Paths**: Track technology evolution and upgrade paths
6. **Survival Analysis**: 10-year survival probability tracking
7. **Cross-Validation**: Link to spawn-experiments for empirical testing

**Key Innovation**: **Technology recommendation engine** - query for use case, get ranked recommendations with rationale

---

## Quick Start

```bash
# Create database
sqlite3 spawn_solutions.db < schema.sql

# Verify
sqlite3 spawn_solutions.db "SELECT * FROM schema_version;"
# Output: 1.0.0|2025-10-31|Initial schema for technology intelligence
```

---

## Core Tables

```sql
-- ============================================================================
-- DISCOVERIES & TECHNOLOGIES
-- ============================================================================

-- Discoveries: Research projects in spawn-solutions
CREATE TABLE IF NOT EXISTS discoveries (
    id TEXT PRIMARY KEY,              -- '1.002', '3.040', '2.050'
    tier INTEGER NOT NULL CHECK(tier BETWEEN 1 AND 5),
    domain TEXT NOT NULL,             -- 'DIY', 'Open Standards', 'Managed Services'

    title TEXT NOT NULL,
    description TEXT,
    problem_statement TEXT,

    status TEXT CHECK(status IN ('planned', 'in_progress', 'completed', 'archived')) DEFAULT 'planned',

    -- MPSE Methodology tracking
    stage_1_completed DATE,           -- S1: Define & Research
    stage_2_completed DATE,           -- S2: Select & Compare
    stage_3_completed DATE,           -- S3: Validate
    stage_4_completed DATE,           -- S4: Document & Recommend

    total_technologies_evaluated INTEGER,
    recommended_count INTEGER,

    directory_path TEXT,              -- '/home/user/spawn-solutions/research/1.002-sqlite-postgres'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_discoveries_tier ON discoveries(tier);
CREATE INDEX IF NOT EXISTS idx_discoveries_domain ON discoveries(domain);
CREATE INDEX IF NOT EXISTS idx_discoveries_status ON discoveries(status);

-- Technologies: Individual libraries, frameworks, services
CREATE TABLE IF NOT EXISTS technologies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discovery_id TEXT NOT NULL,

    name TEXT NOT NULL,               -- 'RapidFuzz', 'Supabase', 'PostgreSQL'
    type TEXT NOT NULL CHECK(type IN ('library', 'framework', 'service', 'standard', 'tool')),

    category TEXT,                    -- 'fuzzy_matching', 'database', 'authentication'
    ecosystem TEXT,                   -- 'python', 'javascript', 'multi-language'

    version_evaluated TEXT,           -- '3.9.3', '2.0.0'
    release_date DATE,

    -- Survival & Longevity
    years_since_release REAL,
    survival_10_year_percent REAL,   -- 0-100 probability of surviving 10 years
    maturity TEXT CHECK(maturity IN ('experimental', 'emerging', 'mature', 'legacy')),

    -- Learning & Adoption
    learning_curve_hours REAL,       -- Estimated hours to proficiency
    community_size INTEGER,           -- GitHub stars, npm downloads, etc.
    documentation_quality INTEGER CHECK(documentation_quality BETWEEN 1 AND 10),

    -- Cost & Performance
    cost_model TEXT,                  -- 'free', 'freemium', 'paid', 'enterprise'
    monthly_cost_usd REAL,
    performance_tier TEXT CHECK(performance_tier IN ('low', 'medium', 'high', 'extreme')),

    -- Recommendation
    is_recommended BOOLEAN DEFAULT 0,
    recommendation_rationale TEXT,
    warning_notes TEXT,               -- Known issues, gotchas, limitations

    -- URLs
    homepage_url TEXT,
    documentation_url TEXT,
    repository_url TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (discovery_id) REFERENCES discoveries(id) ON DELETE CASCADE,
    UNIQUE(discovery_id, name)
);

CREATE INDEX IF NOT EXISTS idx_technologies_discovery ON technologies(discovery_id);
CREATE INDEX IF NOT EXISTS idx_technologies_name ON technologies(name);
CREATE INDEX IF NOT EXISTS idx_technologies_type ON technologies(type);
CREATE INDEX IF NOT EXISTS idx_technologies_category ON technologies(category);
CREATE INDEX IF NOT EXISTS idx_technologies_recommended ON technologies(is_recommended);

-- ============================================================================
-- COMPARISONS & EVALUATIONS
-- ============================================================================

-- Comparisons: Head-to-head technology evaluations
CREATE TABLE IF NOT EXISTS comparisons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discovery_id TEXT NOT NULL,

    comparison_title TEXT NOT NULL,   -- 'PostgreSQL vs MySQL vs SQLite'
    comparison_dimension TEXT,        -- 'performance', 'ease_of_use', 'cost', 'features'

    methodology TEXT,                 -- 'benchmark', 'feature_matrix', 'code_review', 'empirical_test'

    winner_technology_id INTEGER,     -- NULL if no clear winner
    winner_rationale TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (discovery_id) REFERENCES discoveries(id) ON DELETE CASCADE,
    FOREIGN KEY (winner_technology_id) REFERENCES technologies(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_comparisons_discovery ON comparisons(discovery_id);

-- Comparison Participants: Technologies in each comparison
CREATE TABLE IF NOT EXISTS comparison_participants (
    comparison_id INTEGER NOT NULL,
    technology_id INTEGER NOT NULL,

    rank INTEGER,                     -- 1, 2, 3 (1 = best)
    score REAL,                       -- 0-100
    pros TEXT,                        -- JSON array of strengths
    cons TEXT,                        -- JSON array of weaknesses

    PRIMARY KEY (comparison_id, technology_id),
    FOREIGN KEY (comparison_id) REFERENCES comparisons(id) ON DELETE CASCADE,
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

-- Quality Metrics: Detailed evaluation scores
CREATE TABLE IF NOT EXISTS quality_metrics (
    technology_id INTEGER NOT NULL,
    metric_name TEXT NOT NULL,        -- 'code_quality', 'test_coverage', 'documentation'

    score INTEGER CHECK(score BETWEEN 0 AND 100),
    weight REAL DEFAULT 1.0,          -- Importance weight (0-1)

    notes TEXT,
    evaluated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    PRIMARY KEY (technology_id, metric_name),
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_quality_metrics_tech ON quality_metrics(technology_id);

-- ============================================================================
-- USE CASES & RECOMMENDATIONS
-- ============================================================================

-- Use Cases: Specific project requirements
CREATE TABLE IF NOT EXISTS use_cases (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    use_case_title TEXT UNIQUE NOT NULL,
    description TEXT,

    -- Requirements
    requirements TEXT,                -- JSON: {'performance': 'high', 'cost': 'low', 'learning_curve': 'short'}
    constraints TEXT,                 -- JSON: {'budget': 50, 'deadline_weeks': 4, 'team_size': 2}

    -- Context
    project_size TEXT CHECK(project_size IN ('small', 'medium', 'large', 'enterprise')),
    team_expertise TEXT,              -- 'beginner', 'intermediate', 'expert'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Technology Recommendations: Match technologies to use cases
CREATE TABLE IF NOT EXISTS recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    use_case_id INTEGER NOT NULL,
    technology_id INTEGER NOT NULL,

    rank INTEGER,                     -- 1, 2, 3 (1 = top recommendation)
    confidence REAL,                  -- 0-1 (how confident in this match?)

    match_score REAL,                 -- 0-100 (composite score)
    rationale TEXT,                   -- Why is this a good fit?

    tradeoffs TEXT,                   -- What are you giving up?
    alternatives TEXT,                -- JSON array of alternative technology IDs

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (use_case_id) REFERENCES use_cases(id) ON DELETE CASCADE,
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE,
    UNIQUE(use_case_id, technology_id)
);

CREATE INDEX IF NOT EXISTS idx_recommendations_usecase ON recommendations(use_case_id);
CREATE INDEX IF NOT EXISTS idx_recommendations_rank ON recommendations(rank);

-- ============================================================================
-- MIGRATION PATHS & EVOLUTION
-- ============================================================================

-- Migration Paths: Technology evolution tracking
CREATE TABLE IF NOT EXISTS migration_paths (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    from_technology_id INTEGER NOT NULL,
    to_technology_id INTEGER NOT NULL,

    migration_type TEXT CHECK(migration_type IN ('upgrade', 'replacement', 'complement')),
    difficulty TEXT CHECK(difficulty IN ('easy', 'moderate', 'hard', 'very_hard')),

    estimated_hours REAL,
    breaking_changes TEXT,            -- JSON array of breaking changes
    migration_steps TEXT,             -- Markdown or JSON with step-by-step guide

    automated_tools TEXT,             -- Tools that can help (alembic, migrate-mongo, etc.)

    completed_migrations INTEGER DEFAULT 0,  -- How many teams have done this?
    success_rate REAL,                -- 0-1 (what % succeeded?)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (from_technology_id) REFERENCES technologies(id) ON DELETE CASCADE,
    FOREIGN KEY (to_technology_id) REFERENCES technologies(id) ON DELETE CASCADE,
    UNIQUE(from_technology_id, to_technology_id)
);

CREATE INDEX IF NOT EXISTS idx_migration_from ON migration_paths(from_technology_id);
CREATE INDEX IF NOT EXISTS idx_migration_to ON migration_paths(to_technology_id);

-- Technology Dependencies: What depends on what?
CREATE TABLE IF NOT EXISTS dependencies (
    parent_technology_id INTEGER NOT NULL,
    dependency_technology_id INTEGER NOT NULL,

    dependency_type TEXT CHECK(dependency_type IN ('required', 'optional', 'peer')),
    version_constraint TEXT,          -- '>=3.0.0', '^2.0.0'

    PRIMARY KEY (parent_technology_id, dependency_technology_id),
    FOREIGN KEY (parent_technology_id) REFERENCES technologies(id) ON DELETE CASCADE,
    FOREIGN KEY (dependency_technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

-- ============================================================================
-- CROSS-REPOSITORY INTEGRATION
-- ============================================================================

-- spawn-experiments Validation: Link to empirical testing
CREATE TABLE IF NOT EXISTS spawn_experiments_validation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology_id INTEGER NOT NULL,
    experiment_id TEXT NOT NULL,      -- '1.800', '1.801', '1.615'

    experiment_title TEXT,
    validation_type TEXT,             -- 'performance', 'feature', 'comparison', 'tutorial'

    optimal_method INTEGER,           -- 1-4 (which method won?)
    quality_score INTEGER CHECK(quality_score BETWEEN 0 AND 100),

    empirical_findings TEXT,          -- Key takeaways from experiment

    validated_at DATE,

    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_validation_tech ON spawn_experiments_validation(technology_id);
CREATE INDEX IF NOT EXISTS idx_validation_experiment ON spawn_experiments_validation(experiment_id);

-- spawn-analysis Usage: Technologies used in decision analyses
CREATE TABLE IF NOT EXISTS spawn_analysis_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    technology_id INTEGER NOT NULL,
    conversation_id TEXT NOT NULL,    -- '008-eric-makerspace'

    usage_context TEXT,               -- 'recommendation', 'comparison', 'risk_analysis'
    methodology_card TEXT,            -- 'optimizer', 'strategist', etc.

    recommended_for TEXT,             -- What was this recommended for?
    decision_outcome TEXT,            -- 'adopted', 'rejected', 'deferred'

    analysis_date DATE,

    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_analysis_usage_tech ON spawn_analysis_usage(technology_id);
CREATE INDEX IF NOT EXISTS idx_analysis_usage_conv ON spawn_analysis_usage(conversation_id);

-- ============================================================================
-- TAGS & CATEGORIZATION
-- ============================================================================

-- Technology Tags: Multi-dimensional categorization
CREATE TABLE IF NOT EXISTS technology_tags (
    technology_id INTEGER NOT NULL,
    tag TEXT NOT NULL,                -- 'real-time', 'scalable', 'beginner-friendly', 'enterprise-ready'

    PRIMARY KEY (technology_id, tag),
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_tech_tags_tag ON technology_tags(tag);

-- Discovery Tags: Categorize research projects
CREATE TABLE IF NOT EXISTS discovery_tags (
    discovery_id TEXT NOT NULL,
    tag TEXT NOT NULL,                -- 'database', 'web-framework', 'authentication', 'testing'

    PRIMARY KEY (discovery_id, tag),
    FOREIGN KEY (discovery_id) REFERENCES discoveries(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_discovery_tags_tag ON discovery_tags(tag);

-- ============================================================================
-- RESEARCH NOTES & DOCUMENTATION
-- ============================================================================

-- Research Notes: Capture learnings during discovery
CREATE TABLE IF NOT EXISTS research_notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    discovery_id TEXT NOT NULL,

    note_type TEXT,                   -- 'insight', 'question', 'warning', 'decision'
    title TEXT,
    content TEXT NOT NULL,

    related_technology_id INTEGER,    -- Optional link to specific technology

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (discovery_id) REFERENCES discoveries(id) ON DELETE CASCADE,
    FOREIGN KEY (related_technology_id) REFERENCES technologies(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_notes_discovery ON research_notes(discovery_id);
CREATE INDEX IF NOT EXISTS idx_notes_type ON research_notes(note_type);

-- External References: Track sources
CREATE TABLE IF NOT EXISTS external_references (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    reference_type TEXT,              -- 'blog_post', 'documentation', 'stackoverflow', 'github_issue'
    url TEXT NOT NULL,
    title TEXT,
    author TEXT,
    published_date DATE,

    summary TEXT,
    key_quotes TEXT,                  -- JSON array of important quotes

    discovery_id TEXT,
    technology_id INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (discovery_id) REFERENCES discoveries(id) ON DELETE SET NULL,
    FOREIGN KEY (technology_id) REFERENCES technologies(id) ON DELETE SET NULL
);

CREATE INDEX IF NOT EXISTS idx_refs_discovery ON external_references(discovery_id);
CREATE INDEX IF NOT EXISTS idx_refs_technology ON external_references(technology_id);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Technology recommendation summary
CREATE VIEW IF NOT EXISTS v_technology_recommendations AS
SELECT
    t.name,
    t.type,
    t.category,
    t.is_recommended,
    t.survival_10_year_percent,
    t.learning_curve_hours,
    t.cost_model,
    d.tier,
    d.domain,
    COUNT(DISTINCT r.use_case_id) as use_case_matches,
    AVG(r.match_score) as avg_match_score,
    COUNT(DISTINCT sev.experiment_id) as validated_by_experiments
FROM technologies t
JOIN discoveries d ON t.discovery_id = d.id
LEFT JOIN recommendations r ON t.id = r.technology_id
LEFT JOIN spawn_experiments_validation sev ON t.id = sev.technology_id
GROUP BY t.id
ORDER BY t.is_recommended DESC, avg_match_score DESC;

-- View: Discovery completion status
CREATE VIEW IF NOT EXISTS v_discovery_progress AS
SELECT
    d.id,
    d.title,
    d.tier,
    d.domain,
    d.status,
    CASE
        WHEN d.stage_4_completed IS NOT NULL THEN 'S4: Complete'
        WHEN d.stage_3_completed IS NOT NULL THEN 'S3: Validated'
        WHEN d.stage_2_completed IS NOT NULL THEN 'S2: Compared'
        WHEN d.stage_1_completed IS NOT NULL THEN 'S1: Researched'
        ELSE 'Not Started'
    END as current_stage,
    COUNT(DISTINCT t.id) as technologies_evaluated,
    SUM(CASE WHEN t.is_recommended THEN 1 ELSE 0 END) as recommended_count
FROM discoveries d
LEFT JOIN technologies t ON d.id = t.discovery_id
GROUP BY d.id
ORDER BY d.tier, d.id;

-- View: Technology comparison matrix
CREATE VIEW IF NOT EXISTS v_technology_comparisons AS
SELECT
    c.comparison_title,
    t.name as technology_name,
    cp.rank,
    cp.score,
    d.title as discovery_title
FROM comparisons c
JOIN comparison_participants cp ON c.id = cp.comparison_id
JOIN technologies t ON cp.technology_id = t.id
JOIN discoveries d ON c.discovery_id = d.id
ORDER BY c.id, cp.rank;

-- View: Migration path recommendations
CREATE VIEW IF NOT EXISTS v_migration_recommendations AS
SELECT
    t_from.name as from_technology,
    t_to.name as to_technology,
    mp.migration_type,
    mp.difficulty,
    mp.estimated_hours,
    mp.success_rate,
    d_from.domain as from_domain,
    d_to.domain as to_domain
FROM migration_paths mp
JOIN technologies t_from ON mp.from_technology_id = t_from.id
JOIN technologies t_to ON mp.to_technology_id = t_to.id
JOIN discoveries d_from ON t_from.discovery_id = d_from.id
JOIN discoveries d_to ON t_to.discovery_id = d_to.id
ORDER BY mp.difficulty, mp.estimated_hours;

-- View: Technology survival analysis
CREATE VIEW IF NOT EXISTS v_survival_analysis AS
SELECT
    t.name,
    t.type,
    t.years_since_release,
    t.survival_10_year_percent,
    t.maturity,
    t.community_size,
    t.is_recommended,
    d.domain
FROM technologies t
JOIN discoveries d ON t.discovery_id = d.id
WHERE t.survival_10_year_percent IS NOT NULL
ORDER BY t.survival_10_year_percent DESC;

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert sample use cases
INSERT OR IGNORE INTO use_cases (use_case_title, description, requirements, project_size, team_expertise) VALUES
('Small Business Web App',
 'Customer-facing web application with user authentication, data storage, and real-time updates',
 '{"performance": "medium", "cost": "low", "learning_curve": "short", "scalability": "medium"}',
 'small',
 'intermediate'
),

('Enterprise Data Analytics Platform',
 'Large-scale data processing with complex queries, reporting, and visualization',
 '{"performance": "high", "cost": "medium", "learning_curve": "medium", "scalability": "high"}',
 'enterprise',
 'expert'
),

('Personal Project / Portfolio',
 'Individual developer building portfolio project with modern tech stack',
 '{"performance": "low", "cost": "free", "learning_curve": "short", "scalability": "low"}',
 'small',
 'beginner'
);

-- ============================================================================
-- SCHEMA VERSION
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT OR IGNORE INTO schema_version (version, description) VALUES
('1.0.0', 'Initial schema for technology intelligence');

-- ============================================================================
-- DATABASE CONFIGURATION
-- ============================================================================

-- Enable foreign key constraints
PRAGMA foreign_keys = ON;

-- Enable write-ahead logging for better concurrency
PRAGMA journal_mode = WAL;

-- Optimize for query performance
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB cache

-- Verify integrity
PRAGMA integrity_check;
