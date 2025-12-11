-- spawn-experiments Database Schema
-- SQLite 3.x compatible
-- Version: 1.0
-- Date: October 31, 2025

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- Experiments: Core experiment metadata
CREATE TABLE IF NOT EXISTS experiments (
    id TEXT PRIMARY KEY,
    tier INTEGER NOT NULL,
    domain TEXT NOT NULL,
    domain_code TEXT,

    title TEXT NOT NULL,
    description TEXT,
    task_type TEXT,
    research_question TEXT,

    status TEXT CHECK(status IN ('planned', 'in_progress', 'completed', 'blocked')) DEFAULT 'planned',
    priority TEXT CHECK(priority IN ('HIGH', 'MEDIUM', 'LOW', 'COMPLETE')),

    completed_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    -- Cross-references
    related_spawn_solutions TEXT,
    key_finding TEXT,
    report_path TEXT
);

CREATE INDEX IF NOT EXISTS idx_experiments_domain ON experiments(domain);
CREATE INDEX IF NOT EXISTS idx_experiments_status ON experiments(status);
CREATE INDEX IF NOT EXISTS idx_experiments_task_type ON experiments(task_type);
CREATE INDEX IF NOT EXISTS idx_experiments_completed_date ON experiments(completed_date);

-- Methodology Results: Performance metrics for each method
CREATE TABLE IF NOT EXISTS methodology_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id TEXT NOT NULL,
    method_number INTEGER NOT NULL CHECK(method_number BETWEEN 1 AND 4),
    method_name TEXT NOT NULL,

    -- Core metrics
    time_minutes REAL,
    lines_of_code INTEGER,
    test_lines INTEGER,
    quality_score INTEGER CHECK(quality_score BETWEEN 0 AND 100),
    test_count INTEGER,
    coverage_percent REAL,

    -- Winner tracking
    is_winner BOOLEAN DEFAULT 0,
    rank INTEGER CHECK(rank BETWEEN 1 AND 4),

    -- Quality breakdown
    code_quality INTEGER,
    test_quality INTEGER,
    implementation_quality INTEGER,

    -- Notes
    implementation_notes TEXT,
    strengths TEXT,
    weaknesses TEXT,

    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE,
    UNIQUE(experiment_id, method_number)
);

CREATE INDEX IF NOT EXISTS idx_methodology_experiment ON methodology_results(experiment_id);
CREATE INDEX IF NOT EXISTS idx_methodology_method ON methodology_results(method_number);
CREATE INDEX IF NOT EXISTS idx_methodology_winner ON methodology_results(is_winner);
CREATE INDEX IF NOT EXISTS idx_methodology_quality ON methodology_results(quality_score);

-- ============================================================================
-- RESEARCH FINDINGS & PATTERNS
-- ============================================================================

-- Research Findings: Validated research discoveries
CREATE TABLE IF NOT EXISTS findings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    finding_number INTEGER UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,

    confidence_level TEXT NOT NULL CHECK(confidence_level IN
        ('PROVISIONAL', 'MODERATE', 'ROBUST', 'VERY STRONG', 'PROVEN')),
    n_value INTEGER NOT NULL,

    domain TEXT,
    category TEXT,

    date_discovered DATE NOT NULL,
    date_validated DATE,
    status TEXT CHECK(status IN ('active', 'revised', 'rejected', 'superseded')) DEFAULT 'active',

    revision_notes TEXT,
    superseded_by INTEGER,

    FOREIGN KEY (superseded_by) REFERENCES findings(id)
);

CREATE INDEX IF NOT EXISTS idx_findings_number ON findings(finding_number);
CREATE INDEX IF NOT EXISTS idx_findings_domain ON findings(domain);
CREATE INDEX IF NOT EXISTS idx_findings_confidence ON findings(confidence_level);
CREATE INDEX IF NOT EXISTS idx_findings_status ON findings(status);

-- Experiment-Finding Relationships
CREATE TABLE IF NOT EXISTS experiment_findings (
    experiment_id TEXT NOT NULL,
    finding_id INTEGER NOT NULL,
    contribution_type TEXT CHECK(contribution_type IN
        ('discovered', 'validated', 'refined', 'contradicted')),
    notes TEXT,

    PRIMARY KEY (experiment_id, finding_id),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE,
    FOREIGN KEY (finding_id) REFERENCES findings(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_exp_findings_exp ON experiment_findings(experiment_id);
CREATE INDEX IF NOT EXISTS idx_exp_findings_finding ON experiment_findings(finding_id);

-- Patterns: Domain-specific methodology patterns
CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    optimal_method INTEGER NOT NULL CHECK(optimal_method BETWEEN 1 AND 4),
    method_name TEXT NOT NULL,

    confidence TEXT NOT NULL,
    n_experiments INTEGER NOT NULL,

    typical_score_range TEXT,
    characteristic TEXT,

    use_when TEXT,
    examples TEXT,

    created_date DATE,
    last_validated DATE
);

CREATE INDEX IF NOT EXISTS idx_patterns_name ON patterns(name);
CREATE INDEX IF NOT EXISTS idx_patterns_confidence ON patterns(confidence);

-- Experiment-Pattern Relationships
CREATE TABLE IF NOT EXISTS experiment_patterns (
    experiment_id TEXT NOT NULL,
    pattern_id INTEGER NOT NULL,
    validates_pattern BOOLEAN DEFAULT 1,
    deviates_from_pattern BOOLEAN DEFAULT 0,
    deviation_notes TEXT,

    PRIMARY KEY (experiment_id, pattern_id),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE,
    FOREIGN KEY (pattern_id) REFERENCES patterns(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_exp_patterns_exp ON experiment_patterns(experiment_id);
CREATE INDEX IF NOT EXISTS idx_exp_patterns_pattern ON experiment_patterns(pattern_id);

-- ============================================================================
-- COMPONENT TRACKING & REUSE
-- ============================================================================

-- Components: Reusable code from Tier 1 experiments
CREATE TABLE IF NOT EXISTS components (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    path TEXT NOT NULL,
    experiment_created TEXT,
    component_type TEXT,
    description TEXT,
    reused_count INTEGER DEFAULT 0,

    FOREIGN KEY (experiment_created) REFERENCES experiments(id)
);

CREATE INDEX IF NOT EXISTS idx_components_experiment ON components(experiment_created);

-- Experiment-Component Relationships
CREATE TABLE IF NOT EXISTS experiment_components (
    experiment_id TEXT NOT NULL,
    component_id INTEGER NOT NULL,
    usage_type TEXT CHECK(usage_type IN ('created', 'reused', 'discovered', 'ignored')),
    discovery_method TEXT,
    notes TEXT,

    PRIMARY KEY (experiment_id, component_id),
    FOREIGN KEY (experiment_id) REFERENCES experiments(id) ON DELETE CASCADE,
    FOREIGN KEY (component_id) REFERENCES components(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_exp_components_exp ON experiment_components(experiment_id);
CREATE INDEX IF NOT EXISTS idx_exp_components_comp ON experiment_components(component_id);

-- ============================================================================
-- CROSS-REPOSITORY INTEGRATION
-- ============================================================================

-- spawn-solutions Research Cross-References
CREATE TABLE IF NOT EXISTS spawn_solutions_research (
    id TEXT PRIMARY KEY,
    tier INTEGER,
    title TEXT NOT NULL,
    domain TEXT,
    status TEXT,
    synergy_notes TEXT,
    has_methodology_validation BOOLEAN DEFAULT 0
);

CREATE INDEX IF NOT EXISTS idx_spawn_solutions_tier ON spawn_solutions_research(tier);
CREATE INDEX IF NOT EXISTS idx_spawn_solutions_status ON spawn_solutions_research(status);

-- spawn-experiments Validation Links
CREATE TABLE IF NOT EXISTS spawn_experiments_validation (
    spawn_solutions_id TEXT NOT NULL,
    spawn_experiments_id TEXT NOT NULL,
    validation_type TEXT,
    notes TEXT,

    PRIMARY KEY (spawn_solutions_id, spawn_experiments_id),
    FOREIGN KEY (spawn_solutions_id) REFERENCES spawn_solutions_research(id),
    FOREIGN KEY (spawn_experiments_id) REFERENCES experiments(id) ON DELETE CASCADE
);

-- ============================================================================
-- EXPERIMENT PLANNING
-- ============================================================================

-- Planned Experiments Checklist
CREATE TABLE IF NOT EXISTS planned_experiments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    experiment_id TEXT UNIQUE,
    title TEXT NOT NULL,
    priority TEXT CHECK(priority IN ('HIGH', 'MEDIUM', 'LOW')),
    category TEXT,

    depends_on TEXT,
    expected_pattern TEXT,
    spawn_solutions_synergy TEXT,

    estimated_hours REAL,
    expected_confidence_level TEXT,

    is_completed BOOLEAN DEFAULT 0,
    completed_experiment_id TEXT,
    completion_date DATE,

    FOREIGN KEY (completed_experiment_id) REFERENCES experiments(id)
);

CREATE INDEX IF NOT EXISTS idx_planned_priority ON planned_experiments(priority);
CREATE INDEX IF NOT EXISTS idx_planned_completed ON planned_experiments(is_completed);
CREATE INDEX IF NOT EXISTS idx_planned_category ON planned_experiments(category);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Experiments with winner methodology
CREATE VIEW IF NOT EXISTS v_experiments_with_winners AS
SELECT
    e.id,
    e.title,
    e.domain,
    e.completed_date,
    mr.method_number,
    mr.method_name,
    mr.quality_score,
    mr.time_minutes,
    mr.lines_of_code
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE mr.is_winner = 1
  AND e.status = 'completed';

-- View: Finding validation progression
CREATE VIEW IF NOT EXISTS v_finding_validation AS
SELECT
    f.finding_number,
    f.title,
    f.confidence_level,
    f.n_value,
    COUNT(ef.experiment_id) as experiment_count,
    GROUP_CONCAT(ef.experiment_id, ', ') as experiments
FROM findings f
LEFT JOIN experiment_findings ef ON f.id = ef.finding_id
WHERE f.status = 'active'
GROUP BY f.id;

-- View: Pattern performance summary
CREATE VIEW IF NOT EXISTS v_pattern_summary AS
SELECT
    p.name,
    p.optimal_method,
    p.method_name,
    p.confidence,
    p.n_experiments,
    p.typical_score_range,
    COUNT(ep.experiment_id) as validation_count,
    GROUP_CONCAT(ep.experiment_id, ', ') as validating_experiments
FROM patterns p
LEFT JOIN experiment_patterns ep ON p.id = ep.pattern_id
    AND ep.validates_pattern = 1
GROUP BY p.id;

-- View: Methodology performance by domain
CREATE VIEW IF NOT EXISTS v_methodology_performance AS
SELECT
    e.domain,
    mr.method_number,
    mr.method_name,
    COUNT(*) as experiment_count,
    ROUND(AVG(mr.quality_score), 1) as avg_quality,
    ROUND(AVG(mr.time_minutes), 1) as avg_time,
    SUM(CASE WHEN mr.is_winner THEN 1 ELSE 0 END) as wins,
    MIN(mr.quality_score) as min_quality,
    MAX(mr.quality_score) as max_quality
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE e.status = 'completed'
GROUP BY e.domain, mr.method_number;

-- View: Research gaps (spawn-solutions without validation)
CREATE VIEW IF NOT EXISTS v_research_gaps AS
SELECT
    ss.id,
    ss.title,
    ss.domain,
    ss.tier,
    ss.status,
    ss.has_methodology_validation
FROM spawn_solutions_research ss
WHERE ss.tier = 1  -- Libraries
  AND ss.has_methodology_validation = 0
  AND ss.status = 'completed'
ORDER BY ss.id;

-- ============================================================================
-- INITIAL DATA: Core Patterns
-- ============================================================================

-- Insert validated patterns from spawn-experiments research
INSERT OR IGNORE INTO patterns (name, optimal_method, method_name, confidence, n_experiments, typical_score_range, characteristic, created_date) VALUES
('LLM Creative Tasks', 2, 'Specification-Driven', 'VERY STRONG', 6, '88-96/100', 'Complex error handling, prompt engineering, creative synthesis', '2025-10-25'),
('Library Wrapper', 4, 'Adaptive TDD', 'VERY STRONG', 5, '92-96/100', 'Strategic testing, clean interfaces, defensive error handling', '2025-10-24'),
('Discrete Event Simulation', 3, 'Pure TDD', 'ROBUST', 4, '94-99/100', 'Test-first validation, incremental development, event-driven', '2025-10-20'),
('Database Models', 2, 'Specification-Driven', 'PROVISIONAL', 1, '95/100', 'Comprehensive constraints, relationship design', '2025-10-29'),
('Database Migrations', 3, 'Pure TDD', 'PROVISIONAL', 1, '98/100', 'Incremental validation, data safety, rollback integrity', '2025-10-29'),
('Database Seeding', 3, 'Pure TDD', 'PROVISIONAL', 1, '94/100', 'Edge case handling, data generation, referential integrity', '2025-10-31');

-- Insert key research findings
INSERT OR IGNORE INTO findings (finding_number, title, description, confidence_level, n_value, domain, category, date_discovered, status) VALUES
(9, 'Prompt Engineering as Force Multiplier (Domain-Specific)', 'Optimized prompts improve speed by 22-36% AND quality by 1-7 points in creative LLM tasks, but SLOW analytical tasks by -34%', 'ROBUST', 8, 'LLM Integration', 'Prompt Engineering', '2025-09-30', 'active'),
(10, 'Monte Carlo Methodology Sampling', 'Generate N samples → Judge → Pick best = 20% quality improvement for creative outputs', 'ROBUST', 4, 'LLM Integration', 'Sampling Strategy', '2025-09-30', 'active'),
(13, 'Wrapper Quality Affects LLM Output', 'Code quality directly affects LLM output quality - better error handling produces better creative outputs (92% poetry win rate)', 'VERY STRONG', 3, 'LLM Integration', 'Code Quality', '2025-09-30', 'active'),
(14, 'Example Bias in LLM Prompts', 'Too many examples bias toward memorization over understanding in analytical tasks', 'PROVISIONAL', 1, 'LLM Integration', 'Prompt Engineering', '2025-10-06', 'active'),
(15, 'Library Wrapper Methodology', 'Method 4 (Adaptive TDD) optimal for ALL library wrappers (92-96/100) regardless of API complexity', 'VERY STRONG', 5, 'Library Integration', 'Methodology Performance', '2025-10-24', 'active'),
(16, 'DES Library Methodology', 'Method 3 (Pure TDD) optimal for discrete event simulation libraries (94-99/100, 100% win rate N=4)', 'ROBUST', 4, 'Simulation', 'Methodology Performance', '2025-10-20', 'active');

-- ============================================================================
-- UTILITY FUNCTIONS (SQLite does not support UDFs in schema, document separately)
-- ============================================================================

-- Note: These would be Python helper functions, not SQL functions
-- See query_helpers.py for implementations:
--
-- def get_method_wins(domain=None, method_number=None)
-- def get_finding_progression(finding_number)
-- def get_pattern_validation(pattern_name)
-- def identify_research_gaps(tier=1)
-- def calculate_avg_scores(domain=None, method_number=None)

-- ============================================================================
-- SCHEMA VERSION
-- ============================================================================

CREATE TABLE IF NOT EXISTS schema_version (
    version TEXT PRIMARY KEY,
    applied_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

INSERT OR IGNORE INTO schema_version (version, description) VALUES
('1.0.0', 'Initial schema with core tables, patterns, and findings');

-- ============================================================================
-- COMPLETION
-- ============================================================================

-- Enable foreign key constraints (must be set per connection in SQLite)
PRAGMA foreign_keys = ON;

-- Enable write-ahead logging for better concurrency
PRAGMA journal_mode = WAL;

-- Optimize for query performance
PRAGMA synchronous = NORMAL;
PRAGMA cache_size = -64000;  -- 64MB cache

-- Database integrity check
PRAGMA integrity_check;
