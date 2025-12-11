-- Common Queries for spawn-experiments Database
-- SQLite 3.x compatible
-- Usage: sqlite3 spawn_experiments.db < common_queries.sql

-- ============================================================================
-- EXPERIMENT TRACKING QUERIES
-- ============================================================================

-- Query 1: All experiments by status
-- Use: Get overview of experiment pipeline
.mode column
.headers on
.width 12 40 20 12 15

SELECT
    id,
    title,
    domain,
    status,
    completed_date
FROM experiments
ORDER BY
    CASE status
        WHEN 'completed' THEN 1
        WHEN 'in_progress' THEN 2
        WHEN 'planned' THEN 3
        WHEN 'blocked' THEN 4
    END,
    tier,
    id;

-- Query 2: Completed experiments with winners
SELECT
    e.id,
    e.title,
    e.domain,
    mr.method_name AS winner,
    mr.quality_score,
    mr.time_minutes,
    e.completed_date
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE e.status = 'completed'
  AND mr.is_winner = 1
ORDER BY e.completed_date DESC
LIMIT 20;

-- Query 3: Experiments by tier and domain
SELECT
    tier,
    domain,
    COUNT(*) as experiment_count,
    SUM(CASE WHEN status='completed' THEN 1 ELSE 0 END) as completed,
    SUM(CASE WHEN status='in_progress' THEN 1 ELSE 0 END) as in_progress,
    SUM(CASE WHEN status='planned' THEN 1 ELSE 0 END) as planned
FROM experiments
GROUP BY tier, domain
ORDER BY tier, domain;

-- ============================================================================
-- METHODOLOGY PERFORMANCE QUERIES
-- ============================================================================

-- Query 4: Average quality scores by methodology
SELECT
    method_number,
    method_name,
    COUNT(*) as experiment_count,
    ROUND(AVG(quality_score), 1) as avg_quality,
    ROUND(AVG(time_minutes), 1) as avg_time,
    MIN(quality_score) as min_quality,
    MAX(quality_score) as max_quality,
    SUM(CASE WHEN is_winner THEN 1 ELSE 0 END) as wins
FROM methodology_results
WHERE quality_score IS NOT NULL
GROUP BY method_number
ORDER BY avg_quality DESC;

-- Query 5: Best methodology by domain
WITH domain_stats AS (
    SELECT
        e.domain,
        mr.method_number,
        mr.method_name,
        COUNT(*) as experiment_count,
        ROUND(AVG(mr.quality_score), 1) as avg_quality,
        SUM(CASE WHEN mr.is_winner THEN 1 ELSE 0 END) as wins
    FROM experiments e
    JOIN methodology_results mr ON e.id = mr.experiment_id
    WHERE e.status = 'completed' AND mr.quality_score IS NOT NULL
    GROUP BY e.domain, mr.method_number
)
SELECT
    domain,
    method_name,
    wins,
    avg_quality,
    experiment_count
FROM domain_stats
WHERE wins > 0
ORDER BY domain, wins DESC;

-- Query 6: Method 2 vs Method 3 vs Method 4 head-to-head
SELECT
    e.domain,
    e.id,
    e.title,
    MAX(CASE WHEN mr.method_number = 2 THEN mr.quality_score END) as m2_quality,
    MAX(CASE WHEN mr.method_number = 3 THEN mr.quality_score END) as m3_quality,
    MAX(CASE WHEN mr.method_number = 4 THEN mr.quality_score END) as m4_quality,
    CASE
        WHEN mr2.is_winner = 1 THEN 'M2'
        WHEN mr3.is_winner = 1 THEN 'M3'
        WHEN mr4.is_winner = 1 THEN 'M4'
        ELSE 'M1'
    END as winner
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
LEFT JOIN methodology_results mr2 ON e.id = mr2.experiment_id AND mr2.method_number = 2
LEFT JOIN methodology_results mr3 ON e.id = mr3.experiment_id AND mr3.method_number = 3
LEFT JOIN methodology_results mr4 ON e.id = mr4.experiment_id AND mr4.method_number = 4
WHERE e.status = 'completed'
GROUP BY e.id
ORDER BY e.domain, e.completed_date DESC;

-- ============================================================================
-- RESEARCH FINDINGS QUERIES
-- ============================================================================

-- Query 7: Finding validation progression
SELECT
    f.finding_number,
    f.title,
    f.confidence_level,
    f.n_value,
    f.domain,
    COUNT(ef.experiment_id) as validating_experiments,
    GROUP_CONCAT(ef.experiment_id, ', ') as experiments
FROM findings f
LEFT JOIN experiment_findings ef ON f.id = ef.finding_id
WHERE f.status = 'active'
GROUP BY f.id
ORDER BY f.confidence_level DESC, f.n_value DESC;

-- Query 8: Finding #15 (Library Wrapper) validation timeline
SELECT
    e.id,
    e.title,
    e.completed_date,
    ef.contribution_type,
    ROW_NUMBER() OVER (ORDER BY e.completed_date) as n_value,
    mr.quality_score
FROM experiment_findings ef
JOIN experiments e ON ef.experiment_id = e.id
LEFT JOIN methodology_results mr ON e.id = mr.experiment_id AND mr.method_number = 4
WHERE ef.finding_id = (SELECT id FROM findings WHERE finding_number = 15)
ORDER BY e.completed_date;

-- Query 9: Active findings by confidence level
SELECT
    confidence_level,
    COUNT(*) as finding_count,
    GROUP_CONCAT(finding_number || ': ' || title, ' | ') as findings
FROM findings
WHERE status = 'active'
GROUP BY confidence_level
ORDER BY
    CASE confidence_level
        WHEN 'PROVEN' THEN 1
        WHEN 'VERY STRONG' THEN 2
        WHEN 'ROBUST' THEN 3
        WHEN 'MODERATE' THEN 4
        WHEN 'PROVISIONAL' THEN 5
    END;

-- ============================================================================
-- PATTERN VALIDATION QUERIES
-- ============================================================================

-- Query 10: Pattern validation summary
SELECT
    p.name,
    p.optimal_method,
    p.method_name,
    p.confidence,
    p.n_experiments,
    p.typical_score_range,
    COUNT(ep.experiment_id) as actual_validations
FROM patterns p
LEFT JOIN experiment_patterns ep ON p.id = ep.pattern_id AND ep.validates_pattern = 1
GROUP BY p.id
ORDER BY p.confidence DESC, p.n_experiments DESC;

-- Query 11: Experiments validating each pattern
SELECT
    p.name as pattern,
    e.id,
    e.title,
    e.completed_date,
    mr.quality_score,
    CASE WHEN ep.validates_pattern THEN 'VALIDATES' ELSE 'DEVIATES' END as status
FROM patterns p
JOIN experiment_patterns ep ON p.id = ep.pattern_id
JOIN experiments e ON ep.experiment_id = e.id
LEFT JOIN methodology_results mr ON e.id = mr.experiment_id
    AND mr.method_number = p.optimal_method
ORDER BY p.name, e.completed_date;

-- Query 12: Patterns needing more experiments for ROBUST confidence
SELECT
    p.name,
    p.confidence,
    p.n_experiments,
    4 - p.n_experiments as experiments_needed,
    p.optimal_method,
    p.method_name
FROM patterns
WHERE p.n_experiments < 4
  AND p.confidence NOT IN ('ROBUST', 'VERY STRONG', 'PROVEN')
ORDER BY p.n_experiments DESC;

-- ============================================================================
-- PLANNING QUERIES
-- ============================================================================

-- Query 13: High priority planned experiments
SELECT
    pe.experiment_id,
    pe.title,
    pe.category,
    pe.priority,
    pe.expected_pattern,
    pe.spawn_solutions_synergy,
    CASE WHEN pe.is_completed THEN 'DONE' ELSE 'TODO' END as status
FROM planned_experiments pe
WHERE pe.priority = 'HIGH'
  AND pe.is_completed = 0
ORDER BY pe.category;

-- Query 14: Next experiments to reach ROBUST confidence (N=4)
WITH pattern_needs AS (
    SELECT
        p.name,
        p.n_experiments,
        4 - p.n_experiments as needed,
        p.confidence
    FROM patterns
    WHERE p.n_experiments < 4
)
SELECT
    pe.experiment_id,
    pe.title,
    pe.category,
    pn.name as pattern_name,
    pn.n_experiments as current_n,
    pn.needed as experiments_needed,
    pn.confidence as current_confidence
FROM planned_experiments pe
LEFT JOIN pattern_needs pn
    ON pe.expected_pattern LIKE '%' || REPLACE(pn.name, ' Tasks', '') || '%'
WHERE pe.is_completed = 0
  AND pe.priority = 'HIGH'
  AND pn.needed IS NOT NULL
ORDER BY pn.needed ASC, pe.category;

-- Query 15: Completed vs planned experiments by category
SELECT
    COALESCE(e.domain, pe.category) as category,
    COUNT(DISTINCT e.id) as completed,
    COUNT(DISTINCT CASE WHEN pe.is_completed = 0 THEN pe.id END) as planned,
    COUNT(DISTINCT e.id) + COUNT(DISTINCT CASE WHEN pe.is_completed = 0 THEN pe.id END) as total
FROM experiments e
FULL OUTER JOIN planned_experiments pe ON e.domain = pe.category
GROUP BY category
ORDER BY total DESC;

-- ============================================================================
-- CROSS-REPOSITORY QUERIES
-- ============================================================================

-- Query 16: spawn-solutions libraries WITHOUT methodology validation
SELECT
    ss.id,
    ss.title,
    ss.domain,
    ss.tier,
    ss.status,
    CASE WHEN ss.has_methodology_validation THEN 'Validated' ELSE 'NEEDS VALIDATION' END as validation_status
FROM spawn_solutions_research ss
WHERE ss.tier = 1  -- Libraries only
  AND ss.has_methodology_validation = 0
  AND ss.status = 'completed'
ORDER BY ss.id;

-- Query 17: spawn-solutions experiments WITH spawn-experiments methodology data
SELECT
    ss.id as solutions_id,
    ss.title as solutions_title,
    se.id as experiments_id,
    se.title as experiments_title,
    sev.validation_type,
    mr.method_number as optimal_method,
    mr.method_name,
    mr.quality_score
FROM spawn_solutions_research ss
JOIN spawn_experiments_validation sev ON ss.id = sev.spawn_solutions_id
JOIN experiments se ON sev.spawn_experiments_id = se.id
LEFT JOIN methodology_results mr ON se.id = mr.experiment_id AND mr.is_winner = 1
ORDER BY ss.id;

-- ============================================================================
-- COMPONENT REUSE TRACKING
-- ============================================================================

-- Query 18: Components created and reused
SELECT
    c.name,
    e_created.id as created_in,
    e_created.title as created_experiment,
    c.reused_count,
    GROUP_CONCAT(e_reused.id, ', ') as reused_in
FROM components c
JOIN experiments e_created ON c.experiment_created = e_created.id
LEFT JOIN experiment_components ec ON c.id = ec.component_id AND ec.usage_type = 'reused'
LEFT JOIN experiments e_reused ON ec.experiment_id = e_reused.id
GROUP BY c.id
HAVING c.reused_count > 0
ORDER BY c.reused_count DESC;

-- Query 19: Component discovery success rate
SELECT
    e.tier,
    COUNT(DISTINCT e.id) as total_experiments,
    COUNT(DISTINCT CASE WHEN ec.usage_type = 'discovered' THEN e.id END) as discovered_components,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN ec.usage_type = 'discovered' THEN e.id END) / COUNT(DISTINCT e.id), 1) as discovery_rate
FROM experiments e
LEFT JOIN experiment_components ec ON e.id = ec.experiment_id
WHERE e.tier >= 2  -- CLI and above should discover components
GROUP BY e.tier
ORDER BY e.tier;

-- ============================================================================
-- STATISTICS & ANALYTICS
-- ============================================================================

-- Query 20: Database statistics
SELECT 'Experiments' as table_name, COUNT(*) as count FROM experiments
UNION ALL
SELECT 'Methodology Results', COUNT(*) FROM methodology_results
UNION ALL
SELECT 'Findings', COUNT(*) FROM findings
UNION ALL
SELECT 'Patterns', COUNT(*) FROM patterns
UNION ALL
SELECT 'Planned Experiments', COUNT(*) FROM planned_experiments
UNION ALL
SELECT 'Components', COUNT(*) FROM components
UNION ALL
SELECT 'spawn-solutions References', COUNT(*) FROM spawn_solutions_research;

-- Query 21: Experiment velocity (completions per month)
SELECT
    strftime('%Y-%m', completed_date) as month,
    COUNT(*) as experiments_completed,
    GROUP_CONCAT(id, ', ') as experiment_ids
FROM experiments
WHERE status = 'completed' AND completed_date IS NOT NULL
GROUP BY month
ORDER BY month DESC
LIMIT 12;

-- Query 22: Quality trends over time
SELECT
    strftime('%Y-%m', e.completed_date) as month,
    mr.method_name,
    ROUND(AVG(mr.quality_score), 1) as avg_quality,
    COUNT(*) as experiment_count
FROM experiments e
JOIN methodology_results mr ON e.id = mr.experiment_id
WHERE e.status = 'completed'
  AND e.completed_date IS NOT NULL
  AND mr.quality_score IS NOT NULL
GROUP BY month, mr.method_number
ORDER BY month DESC, mr.method_number;

-- ============================================================================
-- VIEWS (Use for simpler queries)
-- ============================================================================

-- Use pre-built views for common queries
.print "\n=== Pre-built Views ==="

SELECT * FROM v_experiments_with_winners LIMIT 10;
SELECT * FROM v_finding_validation;
SELECT * FROM v_pattern_summary;
SELECT * FROM v_methodology_performance;
