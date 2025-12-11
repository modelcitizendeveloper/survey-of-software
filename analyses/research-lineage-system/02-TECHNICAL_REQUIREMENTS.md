# Technical Requirements: Research Data Lineage System

**Application**: Research Lineage System for Spawn Solutions Framework
**Date**: October 17, 2025
**Status**: Requirements Definition
**Related Experiment**: [3.064-metadata-management](../../research/3.064-metadata-management/) (S1 complete)

---

## Core Requirements

### 1. Data Lineage Tracking (CRITICAL)

**Requirement**: Every piece of data must have traceable provenance

**What to Track**:
- **Source URL**: Where data came from (GitHub, PyPI, blog post, official docs)
- **Timestamp**: When data was captured (ISO 8601 format)
- **Retrieval Method**: Web search, API call, manual entry, LLM generation
- **LLM Attribution**: Which LLM call generated conclusions (request ID, model, prompt hash)
- **Source Credibility**: First-party (official), second-party (trusted), third-party (unverified)
- **Data Freshness**: Age of data (detect stale sources)

**Example**:
```json
{
  "fact": "Library X has 50,000 GitHub stars",
  "source_url": "https://github.com/org/library-x",
  "timestamp": "2025-10-17T14:30:00Z",
  "retrieval_method": "github_api",
  "source_credibility": "first_party",
  "data_freshness_days": 0
}
```

---

### 2. MPSE Phase Data Capture (CRITICAL)

**Requirement**: Capture structured data from all four MPSE phases

#### S1 Rapid Discovery

**Data to Capture**:
- Library candidates list (names, URLs)
- GitHub metrics (stars, forks, issues, last commit date)
- PyPI metrics (downloads/month, version, release frequency)
- Initial categorization (ecosystem, maturity, adoption)
- Web search results (top 10 URLs per query)
- Quick comparison table (feature matrix)

**Schema**:
```json
{
  "phase": "S1",
  "research_id": "1.096-scheduling-libraries",
  "timestamp": "2025-10-17T14:00:00Z",
  "candidates": [
    {
      "name": "APScheduler",
      "github_url": "https://github.com/agronholm/apscheduler",
      "github_stars": 5800,
      "github_stars_source": {
        "url": "https://api.github.com/repos/agronholm/apscheduler",
        "timestamp": "2025-10-17T14:05:00Z",
        "method": "github_api"
      },
      "pypi_downloads_month": 12000000,
      "pypi_downloads_source": {
        "url": "https://pypistats.org/packages/apscheduler",
        "timestamp": "2025-10-17T14:07:00Z",
        "method": "web_scrape"
      }
    }
  ],
  "web_search_results": [
    {
      "query": "python scheduling library comparison",
      "results": [
        {
          "url": "https://realpython.com/python-task-scheduling/",
          "title": "Python Task Scheduling Guide",
          "snippet": "APScheduler is the most popular...",
          "timestamp": "2025-10-17T14:10:00Z",
          "credibility": "second_party"
        }
      ]
    }
  ]
}
```

---

#### S2 Comprehensive Discovery

**Data to Capture**:
- Performance benchmarks (throughput, latency, resource usage)
- Benchmark source (official, third-party, self-conducted)
- Ecosystem analysis (plugin count, community size, documentation quality)
- Integration complexity (setup time, learning curve, dependencies)
- Production usage evidence (companies using, case studies, testimonials)
- Code quality metrics (test coverage, code complexity, maintainer activity)

**Schema**:
```json
{
  "phase": "S2",
  "research_id": "1.096-scheduling-libraries",
  "library": "APScheduler",
  "benchmarks": [
    {
      "metric": "throughput_jobs_per_second",
      "value": 1000,
      "source_url": "https://github.com/agronholm/apscheduler/wiki/Performance",
      "source_credibility": "first_party",
      "benchmark_conditions": "10 concurrent workers, in-memory job store",
      "timestamp": "2025-10-17T15:00:00Z"
    }
  ],
  "production_usage": [
    {
      "company": "Airbnb",
      "evidence_url": "https://medium.com/airbnb-engineering/task-scheduling",
      "evidence_type": "blog_post",
      "source_credibility": "second_party",
      "timestamp": "2025-10-17T15:30:00Z"
    }
  ]
}
```

---

#### S3 Need-Driven Discovery

**Data to Capture**:
- Use case mapping (which library fits which use case)
- Requirements checklist (must-have, nice-to-have features)
- When to use / when not to use (decision criteria)
- Real-world examples (code samples, integration patterns)
- Failure scenarios (known limitations, edge cases)

**Schema**:
```json
{
  "phase": "S3",
  "research_id": "1.096-scheduling-libraries",
  "use_cases": [
    {
      "name": "Cron-style periodic tasks",
      "requirements": [
        {"feature": "cron_syntax", "importance": "must_have"},
        {"feature": "timezone_support", "importance": "must_have"}
      ],
      "library_fit": [
        {
          "library": "APScheduler",
          "fit_score": 0.95,
          "reasoning": "Native cron syntax, excellent timezone support",
          "reasoning_source": {
            "llm_model": "claude-sonnet-4",
            "llm_request_id": "req_abc123",
            "prompt_hash": "sha256:...",
            "timestamp": "2025-10-17T16:00:00Z"
          }
        }
      ]
    }
  ]
}
```

---

#### S4 Strategic Discovery

**Data to Capture**:
- Long-term viability assessment (vendor stability, funding, governance)
- Lock-in analysis (migration cost, API portability, ecosystem dependencies)
- Future trajectory (roadmap, upcoming features, breaking changes)
- Competitive positioning (strengths vs alternatives, market share)
- Risk assessment (security vulnerabilities, legal issues, community health)

**Schema**:
```json
{
  "phase": "S4",
  "research_id": "1.096-scheduling-libraries",
  "library": "APScheduler",
  "viability": {
    "maintainer_stability": "high",
    "funding_model": "open_source_volunteer",
    "evidence": [
      {
        "fact": "Single maintainer (agronholm) active for 10+ years",
        "source_url": "https://github.com/agronholm/apscheduler/graphs/contributors",
        "timestamp": "2025-10-17T17:00:00Z",
        "credibility": "first_party"
      }
    ]
  },
  "lock_in": {
    "migration_difficulty": "medium",
    "migration_hours_estimate": 20,
    "reasoning": "Custom API, but standard scheduling concepts",
    "reasoning_source": {
      "llm_model": "claude-sonnet-4",
      "llm_request_id": "req_def456",
      "timestamp": "2025-10-17T17:30:00Z"
    }
  }
}
```

---

### 3. Synthesis Data Capture (CRITICAL)

**Requirement**: Final recommendations must link back to supporting data

**What to Capture**:
- Recommendation text (which library is recommended)
- Confidence score (cross-methodology agreement %)
- Supporting evidence (which S1-S4 data points support this)
- Decision criteria weighting (how much each factor mattered)
- Alternative recommendations (second-best, third-best choices)

**Schema**:
```json
{
  "research_id": "1.096-scheduling-libraries",
  "synthesis": {
    "primary_recommendation": {
      "library": "APScheduler",
      "confidence": 0.92,
      "reasoning": "Best balance of features, performance, and ecosystem maturity",
      "supporting_evidence": [
        {"phase": "S1", "data_id": "github_stars", "weight": 0.2},
        {"phase": "S2", "data_id": "performance_benchmark", "weight": 0.3},
        {"phase": "S3", "data_id": "use_case_fit_cron", "weight": 0.3},
        {"phase": "S4", "data_id": "viability_assessment", "weight": 0.2}
      ],
      "criteria_weights": {
        "performance": 0.3,
        "ecosystem": 0.2,
        "use_case_fit": 0.3,
        "viability": 0.2
      }
    },
    "alternatives": [
      {"library": "Celery Beat", "confidence": 0.75, "reason": "More heavyweight, better for distributed systems"}
    ]
  }
}
```

---

### 4. Temporal Tracking (HIGH)

**Requirement**: Track how data changes over time

**What to Track**:
- Historical snapshots (GitHub stars 6 months ago vs today)
- Drift detection (when did recommendation change?)
- Source freshness (when was source last updated?)
- Revalidation schedule (when should we re-check this data?)

**Example**:
```json
{
  "library": "APScheduler",
  "metric": "github_stars",
  "history": [
    {"value": 5000, "timestamp": "2025-04-17T12:00:00Z"},
    {"value": 5500, "timestamp": "2025-07-17T12:00:00Z"},
    {"value": 5800, "timestamp": "2025-10-17T12:00:00Z"}
  ],
  "trend": "growing",
  "revalidate_at": "2026-01-17T12:00:00Z"
}
```

---

### 5. Vendor Gaming Detection (MEDIUM-HIGH)

**Requirement**: Detect suspicious patterns that indicate data manipulation

**Detection Patterns**:
- **Sudden spikes**: GitHub stars increase 10x in 1 month (bot farming)
- **Source proliferation**: 50 new blog posts appear in 1 week (coordinated campaign)
- **Review manipulation**: 100 positive Stack Overflow answers appear overnight
- **Benchmark gaming**: Official benchmarks contradict third-party benchmarks

**Schema**:
```json
{
  "library": "Library X",
  "suspicious_patterns": [
    {
      "pattern": "sudden_spike",
      "metric": "github_stars",
      "details": {
        "previous_value": 1000,
        "current_value": 15000,
        "time_period_days": 30,
        "expected_value": 1200,
        "anomaly_score": 0.95
      },
      "detected_at": "2025-10-17T18:00:00Z",
      "flagged_for_review": true
    }
  ]
}
```

---

### 6. Sensitivity Analysis Support (MEDIUM)

**Requirement**: Enable testing different criteria weightings

**What to Support**:
- Criteria reweighting (change performance from 0.3 to 0.7)
- Recommendation recalculation (how does recommendation change?)
- Context profiles (startup, enterprise, performance-critical presets)
- Comparison reports (side-by-side recommendations with different weights)

**Example Query**:
```python
# Test how recommendation changes with different weightings
result = sensitivity_analysis(
    research_id="1.096-scheduling-libraries",
    criteria_weights={
        "performance": 0.7,  # Was 0.3
        "ecosystem": 0.1,    # Was 0.2
        "use_case_fit": 0.1, # Was 0.3
        "viability": 0.1     # Was 0.2
    }
)

# Result: Recommendation changes from APScheduler to Celery (performance-optimized)
```

---

### 7. LLM Cost Optimization (MEDIUM)

**Requirement**: Reduce expensive LLM calls by caching structured data

**Strategies**:
- **Cache LLM responses**: Store full LLM response with prompt hash
- **Incremental updates**: Only re-query LLM for changed data
- **Local ML inference**: Use local models for simple queries (embeddings, classification)
- **Query structured data first**: Check if answer exists in structured data before LLM call

**Example**:
```python
# Instead of asking LLM "Which library is fastest?"
# Query structured data directly:
fastest_library = query(
    metric="throughput_jobs_per_second",
    order_by="DESC",
    limit=1
)
# No LLM call needed, instant response
```

---

## Functional Requirements

### FR1: Data Ingestion

**Requirement**: Import research data from various sources

**Sources**:
- Web search results (URLs, snippets)
- GitHub API (stars, forks, issues, commits)
- PyPI API (downloads, versions, release dates)
- LLM responses (analysis, conclusions)
- Manual entry (benchmark data, production usage evidence)

**Interface**:
```python
# Ingest web search results
ingest_web_search(
    research_id="1.096-scheduling-libraries",
    phase="S1",
    query="python scheduling libraries",
    results=[
        {"url": "...", "title": "...", "snippet": "...", "timestamp": "..."}
    ]
)

# Ingest GitHub metrics
ingest_github_metrics(
    research_id="1.096-scheduling-libraries",
    library="APScheduler",
    stars=5800,
    forks=800,
    timestamp="2025-10-17T12:00:00Z"
)

# Ingest LLM analysis
ingest_llm_analysis(
    research_id="1.096-scheduling-libraries",
    phase="S3",
    library="APScheduler",
    analysis="APScheduler fits cron-style use cases well due to...",
    llm_model="claude-sonnet-4",
    llm_request_id="req_abc123",
    prompt_hash="sha256:..."
)
```

---

### FR2: Data Querying

**Requirement**: Query structured data efficiently

**Query Patterns**:
- **Fact lookup**: "What are APScheduler's GitHub stars?"
- **Comparison**: "Compare APScheduler vs Celery on performance"
- **Trend analysis**: "How have APScheduler's stars changed over time?"
- **Sensitivity**: "What if we prioritize cost over performance?"
- **Provenance**: "Where did this benchmark data come from?"

**Interface**:
```python
# Simple fact lookup
stars = query_metric(
    library="APScheduler",
    metric="github_stars",
    as_of="2025-10-17"
)

# Comparison
comparison = compare_libraries(
    libraries=["APScheduler", "Celery"],
    metrics=["github_stars", "pypi_downloads", "performance"],
    phase="S2"
)

# Trend analysis
trend = analyze_trend(
    library="APScheduler",
    metric="github_stars",
    time_range="6_months"
)

# Sensitivity analysis
recommendation = sensitivity_analysis(
    research_id="1.096-scheduling-libraries",
    criteria_weights={"performance": 0.7, "cost": 0.3}
)

# Provenance trace
lineage = trace_provenance(
    fact="APScheduler has 5800 GitHub stars",
    research_id="1.096-scheduling-libraries"
)
# Returns: source URL, timestamp, retrieval method, credibility score
```

---

### FR3: Data Validation

**Requirement**: Validate data integrity and detect anomalies

**Validation Rules**:
- **Range checks**: GitHub stars must be >= 0
- **Timestamp validation**: Timestamps must be <= current time
- **URL validation**: URLs must be reachable (HTTP 200)
- **Consistency checks**: Cross-reference data (GitHub stars match GitHub API)
- **Anomaly detection**: Flag suspicious patterns (sudden spikes, well-poisoning)

**Interface**:
```python
# Validate all data for an experiment
validation_report = validate_experiment(
    research_id="1.096-scheduling-libraries"
)

# Report shows:
# - Missing data (which phases have incomplete data?)
# - Invalid data (which facts failed validation?)
# - Anomalies (which metrics show suspicious patterns?)
# - Stale data (which sources need revalidation?)
```

---

### FR4: Historical Reproduction

**Requirement**: Reproduce historical decisions with data lineage

**Capabilities**:
- Query data "as of" specific timestamp
- Reproduce recommendations with historical data
- Compare historical vs current recommendations
- Explain why recommendation changed

**Interface**:
```python
# Reproduce recommendation as of 6 months ago
historical_recommendation = reproduce_recommendation(
    research_id="1.096-scheduling-libraries",
    as_of="2025-04-17T12:00:00Z"
)

# Compare with current recommendation
current_recommendation = get_current_recommendation(
    research_id="1.096-scheduling-libraries"
)

# Explain change
change_explanation = explain_recommendation_change(
    research_id="1.096-scheduling-libraries",
    from_date="2025-04-17",
    to_date="2025-10-17"
)

# Result: "Recommendation changed from Celery to APScheduler due to:
#  - APScheduler stars increased 16% (5000 → 5800)
#  - New production usage evidence (Airbnb blog post)
#  - Performance benchmarks improved 20%"
```

---

### FR5: Export & Reporting

**Requirement**: Generate reports and export data

**Export Formats**:
- **Markdown**: Human-readable summary (current format)
- **JSON**: Structured data for programmatic access
- **CSV**: Tabular data for spreadsheet analysis
- **HTML**: Interactive visualizations

**Reports**:
- **Data lineage report**: Show provenance for all facts
- **Sensitivity analysis report**: Show how recommendations change with different weights
- **Vendor gaming report**: Flag suspicious patterns
- **Historical comparison report**: Show how experiment evolved over time

**Interface**:
```python
# Export to markdown (current format)
export_markdown(
    research_id="1.096-scheduling-libraries",
    output_path="DISCOVERY_SYNTHESIS.md"
)

# Export to JSON (structured data)
export_json(
    research_id="1.096-scheduling-libraries",
    output_path="data.json"
)

# Generate data lineage report
generate_lineage_report(
    research_id="1.096-scheduling-libraries",
    output_path="lineage_report.html"
)
```

---

## Non-Functional Requirements

### NFR1: Performance

- **Query latency**: <100ms for simple queries, <1s for complex queries
- **Import speed**: >100 facts/second
- **Storage efficiency**: <10MB per experiment (compressed)
- **Concurrent users**: Support 10+ concurrent queries

---

### NFR2: Scalability

- **Experiment count**: Support 1,000+ experiments
- **Data points**: Support 100,000+ facts per experiment
- **Historical depth**: Store 5+ years of temporal data
- **Query complexity**: Support multi-table joins, aggregations, time-series queries

---

### NFR3: Reliability

- **Data integrity**: ACID transactions (no partial writes)
- **Backup frequency**: Daily automated backups
- **Disaster recovery**: <1 hour recovery time objective (RTO)
- **Data loss tolerance**: <1 day recovery point objective (RPO)

---

### NFR4: Security

- **Access control**: Read-only public access, write access authenticated
- **Audit logging**: Track all data modifications (who, when, what)
- **Data encryption**: At-rest encryption for sensitive data
- **API security**: Rate limiting, authentication tokens

---

### NFR5: Maintainability

- **Schema versioning**: Support schema migrations without data loss
- **Code quality**: 80%+ test coverage, type hints, documentation
- **Dependency management**: Pin versions, security scanning
- **Monitoring**: Log errors, track query performance, alert on anomalies

---

## Integration Requirements

### INT1: Git Integration

**Requirement**: Structured data stored in git (version control, collaboration)

**Format**: JSON files per experiment
- `research/1.096-scheduling-libraries/data/S1_rapid.json`
- `research/1.096-scheduling-libraries/data/S2_comprehensive.json`
- `research/1.096-scheduling-libraries/data/S3_need_driven.json`
- `research/1.096-scheduling-libraries/data/S4_strategic.json`
- `research/1.096-scheduling-libraries/data/synthesis.json`

**Benefits**:
- Version control (track changes over time)
- Collaboration (multiple contributors)
- Backup (git remote)
- Code review (pull requests for data changes)

---

### INT2: Hugo Integration

**Requirement**: Convert structured data to public cookbooks

**Flow**:
```
Structured Data (JSON) → Conversion Script → Markdown (Hugo) → Public Site
```

**Conversion**:
- Query structured data for final recommendations
- Generate markdown with data lineage links
- Include interactive visualizations (charts, comparisons)

---

### INT3: LLM Integration

**Requirement**: Capture LLM request/response metadata

**What to Capture**:
- Request ID (unique identifier)
- Model (claude-sonnet-4, gpt-4, etc.)
- Prompt hash (detect prompt changes)
- Response text
- Token count (cost tracking)
- Timestamp

**Benefits**:
- Cost tracking (which experiments are most expensive?)
- Reproducibility (re-run with same prompt)
- Drift detection (did prompt change?)

---

### INT4: Metadata Management Integration (3.064)

**Requirement**: Leverage findings from 3.064 Metadata Management experiment

**Related Findings** (from 3.064 S1):
- **OpenMetadata**: Open source, API-first, good lineage
- **DataHub**: LinkedIn-backed, strong lineage, complex setup
- **Amundsen**: Lyft-backed, search-focused, less lineage
- **Atlan**: Modern UI, SaaS, expensive

**Decision**: Start simple (SQLite + JSON files), evolve to OpenMetadata if needed

**Rationale**:
- Research lineage needs are simpler than enterprise data catalog
- Git-based workflow is more important than UI
- Can migrate to OpenMetadata later if lineage needs grow

---

## Success Criteria

### MVP Success (Minimum Viable Product)
- ✅ Capture S1-S4 data for 5 Tier 1 research
- ✅ Query data by library, metric, phase
- ✅ Export to markdown (current format)
- ✅ Track source URLs and timestamps
- ✅ Historical snapshots (1 experiment with 3 months of history)

### V1 Success (Production Ready)
- ✅ Capture S1-S4 data for all 24 Tier 1 research
- ✅ Sensitivity analysis (test criteria reweighting)
- ✅ Vendor gaming detection (flag suspicious patterns)
- ✅ Data lineage reports (provenance for all facts)
- ✅ LLM cost reduction (50%+ for updates)

### V2 Success (Advanced Features)
- ✅ Local ML integration (embeddings, classification)
- ✅ Automated drift detection (alert when recommendations change)
- ✅ Tier 2 & 3 support (extend to standards and services)
- ✅ Public API (programmatic access for cookbooks)

---

## Next Steps

1. **Architecture Options** (next document): Evaluate database choices (SQLite, PostgreSQL, Graph DB)
2. **Schema Design**: Define detailed JSON schema for S1-S4 data
3. **Prototype**: Build MVP with 1 experiment (1.096-scheduling-libraries)
4. **Migration Plan**: Backfill existing 24 Tier 1 research

**Estimated Timeline**: 40-80 hours over 4-8 weeks

---

**Status**: Requirements Defined
**Next**: Architecture Options (database selection, storage design)
**Related Work**: 3.064 Metadata Management experiment (S1 complete, leverage findings)
