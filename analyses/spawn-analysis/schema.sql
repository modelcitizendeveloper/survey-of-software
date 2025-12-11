# spawn-analysis Content Delivery Database Schema

**Purpose**: Track conversation analyses, content chunks, recipients, deliveries, and feedback
**Database**: SQLite 3.x
**Version**: 1.0
**Date**: October 31, 2025

---

## Summary

This database enables **progressive content delivery** for spawn-analysis decision reports:

1. **Conversations**: Track decision analyses (e.g., "008-eric-makerspace")
2. **Content Chunks**: Break reports into deliverable sections (executive summary, methodologies, appendices)
3. **Recipients**: Track who receives analyses (clients, colleagues, advisors)
4. **Deliveries**: Record what was sent when, to whom, via what method
5. **Feedback**: Capture recipient responses, requests, questions
6. **Analytics**: Measure engagement (views, time spent, drop-off points)

**Key Innovation**: **Progressive disclosure** - send small chunks, get feedback, send more based on interest

---

## Quick Start

```bash
# Create database
sqlite3 spawn_analysis.db < schema.sql

# Verify
sqlite3 spawn_analysis.db "SELECT * FROM schema_version;"
# Output: 1.0.0|2025-10-31|Initial schema for content delivery tracking
```

---

## Core Tables

```sql
-- ============================================================================
-- CONVERSATIONS & METHODOLOGIES
-- ============================================================================

-- Conversations: Decision analyses
CREATE TABLE IF NOT EXISTS conversations (
    id TEXT PRIMARY KEY,              -- '008-eric-makerspace-business-model'
    title TEXT NOT NULL,
    question TEXT NOT NULL,
    context TEXT,

    analysis_date DATE,
    analyst TEXT,                      -- 'Ivan'
    recipient_primary TEXT,            -- Primary recipient name

    status TEXT CHECK(status IN ('draft', 'in_progress', 'completed', 'delivered')) DEFAULT 'draft',
    total_lines INTEGER,               -- 13,020
    total_size_kb INTEGER,            -- 270

    prior_confidence REAL,             -- 0.65
    final_confidence REAL,             -- 0.78
    confidence_change REAL,            -- +0.13

    directory_path TEXT,               -- '/home/user/spawn-analysis/conversations/008-eric-makerspace'

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_conversations_status ON conversations(status);
CREATE INDEX IF NOT EXISTS idx_conversations_analyst ON conversations(analyst);
CREATE INDEX IF NOT EXISTS idx_conversations_date ON conversations(analysis_date);

-- Methodologies: Individual card analyses
CREATE TABLE IF NOT EXISTS methodologies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,

    methodology_number INTEGER,        -- 1-12
    methodology_name TEXT NOT NULL,    -- 'Optimizer', 'Strategist', 'Synthesizer'

    file_path TEXT,                    -- '01-optimizer.md'
    line_count INTEGER,                -- 834
    size_kb REAL,                      -- 31.3

    credibility_weight REAL,           -- 0.85
    recommendation_summary TEXT,       -- Short 1-2 sentence summary
    confidence_impact TEXT,            -- 'Increased +5%' or 'Decreased -3%'

    generated_at TIMESTAMP,

    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    UNIQUE(conversation_id, methodology_number)
);

CREATE INDEX IF NOT EXISTS idx_methodologies_conv ON methodologies(conversation_id);
CREATE INDEX IF NOT EXISTS idx_methodologies_name ON methodologies(methodology_name);

-- ============================================================================
-- CONTENT CHUNKING
-- ============================================================================

-- Content Chunks: Deliverable sections
CREATE TABLE IF NOT EXISTS content_chunks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,

    chunk_type TEXT NOT NULL,          -- 'executive_summary', 'methodology_deep_dive', 'appendix', 'personal_note'
    section_title TEXT NOT NULL,
    section_number INTEGER,            -- Ordering (1, 2, 3...)

    content_markdown TEXT NOT NULL,    -- Original markdown content
    content_html TEXT,                 -- HTML version (for email)
    word_count INTEGER,
    estimated_read_minutes INTEGER,    -- word_count / 200

    related_methodology TEXT,          -- 'optimizer', 'strategist', etc. (NULL for summaries)

    priority TEXT CHECK(priority IN ('HIGH', 'MEDIUM', 'LOW', 'OPTIONAL')) DEFAULT 'MEDIUM',
    stage INTEGER,                     -- 1, 2, 3 (delivery stage)

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_chunks_conv ON content_chunks(conversation_id);
CREATE INDEX IF NOT EXISTS idx_chunks_stage ON content_chunks(stage);
CREATE INDEX IF NOT EXISTS idx_chunks_type ON content_chunks(chunk_type);

-- Content Tags: Categorize chunks
CREATE TABLE IF NOT EXISTS content_tags (
    chunk_id INTEGER NOT NULL,
    tag TEXT NOT NULL,

    PRIMARY KEY (chunk_id, tag),
    FOREIGN KEY (chunk_id) REFERENCES content_chunks(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_content_tags_tag ON content_tags(tag);

-- ============================================================================
-- RECIPIENTS & DELIVERIES
-- ============================================================================

-- Recipients: People receiving analyses
CREATE TABLE IF NOT EXISTS recipients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    email TEXT,
    role TEXT,                         -- 'client', 'colleague', 'advisor', 'stakeholder'

    communication_preference TEXT,     -- 'email', 'notion', 'pdf', 'web'
    pacing_preference TEXT,            -- 'all_at_once', 'staged', 'on_demand'

    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_recipients_name ON recipients(name);

-- Deliveries: Tracking what was sent when
CREATE TABLE IF NOT EXISTS deliveries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    recipient_id INTEGER NOT NULL,

    stage INTEGER,                     -- 1, 2, 3, or NULL for custom
    delivery_method TEXT,              -- 'email', 'pdf', 'notion', 'web_link', 'print'

    sent_at TIMESTAMP NOT NULL,
    opened_at TIMESTAMP,               -- Email tracking (if available)
    last_viewed_at TIMESTAMP,          -- Web link tracking

    chunks_sent TEXT,                  -- JSON array of chunk IDs: [1, 2, 3]
    total_word_count INTEGER,
    total_read_minutes INTEGER,

    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES recipients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_deliveries_conv ON deliveries(conversation_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_recipient ON deliveries(recipient_id);
CREATE INDEX IF NOT EXISTS idx_deliveries_sent ON deliveries(sent_at);

-- ============================================================================
-- FEEDBACK & ENGAGEMENT
-- ============================================================================

-- Feedback: Recipient responses
CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id INTEGER NOT NULL,
    recipient_id INTEGER NOT NULL,

    feedback_type TEXT,                -- 'email_reply', 'meeting_notes', 'survey_response', 'comment'
    feedback_text TEXT,
    sentiment TEXT CHECK(sentiment IN ('positive', 'neutral', 'negative', 'mixed')),

    requested_content TEXT,            -- JSON array: ['experimentalist', 'gamification_details']
    questions_raised TEXT,             -- JSON array of questions
    decisions_made TEXT,               -- JSON array of decisions influenced

    received_at TIMESTAMP NOT NULL,
    processed BOOLEAN DEFAULT 0,

    FOREIGN KEY (delivery_id) REFERENCES deliveries(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES recipients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_feedback_delivery ON feedback(delivery_id);
CREATE INDEX IF NOT EXISTS idx_feedback_recipient ON feedback(recipient_id);

-- Engagement Analytics: Track what content resonates
CREATE TABLE IF NOT EXISTS engagement_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    delivery_id INTEGER NOT NULL,
    chunk_id INTEGER NOT NULL,

    views INTEGER DEFAULT 0,
    time_spent_seconds INTEGER,
    scroll_depth_percent REAL,         -- 0-100 (how far down did they scroll?)

    clicked_links TEXT,                -- JSON array of URLs clicked
    highlighted_text TEXT,             -- JSON array of text they highlighted/copied

    drop_off_point TEXT,               -- Section where they stopped reading

    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (delivery_id) REFERENCES deliveries(id) ON DELETE CASCADE,
    FOREIGN KEY (chunk_id) REFERENCES content_chunks(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_engagement_delivery ON engagement_analytics(delivery_id);
CREATE INDEX IF NOT EXISTS idx_engagement_chunk ON engagement_analytics(chunk_id);

-- ============================================================================
-- TEMPLATES & SCHEDULING
-- ============================================================================

-- Delivery Templates: Reusable email/web templates
CREATE TABLE IF NOT EXISTS delivery_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    template_name TEXT UNIQUE NOT NULL,
    template_type TEXT,                -- 'email', 'pdf', 'web', 'notion'

    subject_template TEXT,
    intro_template TEXT,
    content_template TEXT,
    outro_template TEXT,

    variables TEXT,                    -- JSON: ['recipient_name', 'conversation_title', 'analyst_name']

    created_at TIMESTAMP,
    last_used_at TIMESTAMP
);

-- Delivery Schedules: Plan future deliveries
CREATE TABLE IF NOT EXISTS delivery_schedules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    recipient_id INTEGER NOT NULL,

    stage INTEGER,
    scheduled_for TIMESTAMP,
    trigger_condition TEXT,            -- 'after_feedback', 'after_24_hours', 'after_48_hours', 'manual'

    chunks_to_send TEXT,               -- JSON array of chunk IDs
    status TEXT CHECK(status IN ('pending', 'sent', 'cancelled')) DEFAULT 'pending',

    created_at TIMESTAMP,
    sent_at TIMESTAMP,

    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (recipient_id) REFERENCES recipients(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_schedules_status ON delivery_schedules(status);
CREATE INDEX IF NOT EXISTS idx_schedules_scheduled ON delivery_schedules(scheduled_for);

-- ============================================================================
-- RELATIONSHIPS
-- ============================================================================

-- Conversation Relationships: Link related analyses
CREATE TABLE IF NOT EXISTS conversation_relationships (
    parent_conversation_id TEXT NOT NULL,
    child_conversation_id TEXT NOT NULL,
    relationship_type TEXT,            -- 'follow_up', 'refinement', 'related_question', 'round_2'
    notes TEXT,

    PRIMARY KEY (parent_conversation_id, child_conversation_id),
    FOREIGN KEY (parent_conversation_id) REFERENCES conversations(id) ON DELETE CASCADE,
    FOREIGN KEY (child_conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- View: Conversations with delivery status
CREATE VIEW IF NOT EXISTS v_conversations_with_status AS
SELECT
    c.id,
    c.title,
    c.analyst,
    c.recipient_primary,
    c.final_confidence,
    c.status,
    COUNT(DISTINCT d.id) as delivery_count,
    MAX(d.sent_at) as last_delivered,
    COUNT(DISTINCT f.id) as feedback_count
FROM conversations c
LEFT JOIN deliveries d ON c.id = d.conversation_id
LEFT JOIN feedback f ON d.id = f.delivery_id
GROUP BY c.id;

-- View: Recipient engagement summary
CREATE VIEW IF NOT EXISTS v_recipient_engagement AS
SELECT
    r.name,
    r.email,
    COUNT(DISTINCT d.id) as deliveries_received,
    COUNT(DISTINCT f.id) as feedback_given,
    AVG(ea.views) as avg_views_per_chunk,
    AVG(ea.time_spent_seconds) as avg_time_spent,
    AVG(ea.scroll_depth_percent) as avg_scroll_depth
FROM recipients r
LEFT JOIN deliveries d ON r.id = d.recipient_id
LEFT JOIN feedback f ON r.id = f.recipient_id
LEFT JOIN engagement_analytics ea ON d.id = ea.delivery_id
GROUP BY r.id;

-- View: Most requested methodologies
CREATE VIEW IF NOT EXISTS v_methodology_popularity AS
SELECT
    methodology_name,
    COUNT(*) as times_generated,
    AVG(credibility_weight) as avg_credibility,
    SUM(CASE WHEN recommendation_summary IS NOT NULL THEN 1 ELSE 0 END) as has_recommendation_count
FROM methodologies
GROUP BY methodology_name
ORDER BY times_generated DESC;

-- View: Content chunk performance
CREATE VIEW IF NOT EXISTS v_chunk_performance AS
SELECT
    cc.chunk_type,
    cc.section_title,
    COUNT(DISTINCT ea.delivery_id) as deliveries,
    AVG(ea.views) as avg_views,
    AVG(ea.time_spent_seconds) as avg_time_spent,
    AVG(ea.scroll_depth_percent) as avg_scroll_depth,
    cc.stage
FROM content_chunks cc
LEFT JOIN engagement_analytics ea ON cc.id = ea.chunk_id
GROUP BY cc.id
ORDER BY avg_views DESC;

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert default delivery templates
INSERT OR IGNORE INTO delivery_templates (template_name, template_type, subject_template, intro_template, outro_template, variables) VALUES
('Stage 1: Executive Summary', 'email',
 'Analysis: {{conversation_title}} (Stage 1/3)',
 'Hi {{recipient_name}},\n\nI''ve completed the decision analysis for "{{conversation_title}}". Here''s the executive summary to get us started.',
 'Want more details? Just reply with which sections interest you:\n- Full synthesis\n- Specific methodology analyses\n- All deep dives',
 '["recipient_name", "conversation_title", "analyst_name"]'
),

('Stage 2: Synthesis + Top Methodologies', 'email',
 'Analysis: {{conversation_title}} (Stage 2/3)',
 'Hi {{recipient_name}},\n\nBased on your feedback, here''s the full synthesis plus the methodology analyses you requested.',
 'Let me know if you need any clarifications or want to see additional perspectives!',
 '["recipient_name", "conversation_title", "analyst_name"]'
),

('Full Report (All-at-Once)', 'email',
 'Complete Analysis: {{conversation_title}}',
 'Hi {{recipient_name}},\n\nHere''s the complete decision analysis including all 8 methodology perspectives.',
 'This is comprehensive (~13,000 words). Feel free to jump to sections that interest you most using the table of contents.',
 '["recipient_name", "conversation_title", "analyst_name"]'
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
('1.0.0', 'Initial schema for content delivery tracking');

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
