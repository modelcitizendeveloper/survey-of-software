# 1.049.1 Database Schema Inspection - Discovery Table of Contents

**Research Code**: 1.049.1
**Domain**: Database Schema Inspection, Diffing, and Migration Generation
**Methodology**: MPSE v3.0 (S1-S4 Parallel Discovery)
**Date Compiled**: December 4, 2025

---

## Executive Summary

### Strategic Winners (December 2025)

| Tool | Viability | Use Case | Key Insight |
|------|-----------|----------|-------------|
| **SQLAlchemy Inspector** | 95% | Schema introspection | Foundation - built into SQLAlchemy |
| **Alembic** | 90% | Migration generation | Industry standard, autogenerate |
| **sqlacodegen** | 60% | Reverse engineering | Useful but moderate risk |
| **sqlalchemy-diff** | 30% | Schema comparison | HIGH RISK - avoid |

**Key Insight**: Build on SQLAlchemy foundation (Inspector + Alembic). Avoid third-party tools with maintenance risk.

---

## Critical Question: What Does Alembic Autogenerate Miss?

| Feature | Alembic Detects | Notes |
|---------|-----------------|-------|
| Table add/drop | ✅ Yes | Reliable |
| Column add/drop | ✅ Yes | Reliable |
| Column type change | ✅ Yes | Reliable |
| Index add/drop | ✅ Yes | Reliable |
| Foreign key add/drop | ✅ Yes | Reliable |
| **Table/column renames** | ❌ No | Shows as drop+add |
| **CHECK constraints** | ❌ No | Not implemented |
| **PRIMARY KEY changes** | ❌ No | Not implemented |
| **Views** | ❌ No | Not handled |
| **Triggers/Functions** | ❌ No | Not detected |

**Recommendation**: Always review autogenerate output. Never blindly apply migrations.

---

## Methodology Convergence

| Method | Primary Recommendation | Confidence | Key Rationale |
|--------|----------------------|------------|---------------|
| S1 Rapid | Inspector + Alembic + sqlacodegen | High | Ecosystem standard |
| S2 Comprehensive | Inspector + Alembic (core), sqlacodegen (tactical) | High | Feature analysis |
| S3 Need-Driven | Context-dependent (5 use cases) | High | Workflow matching |
| S4 Strategic | Inspector + Alembic (long-term safe) | High | 3-5 year viability |

**Convergence Level**: HIGH (4/4 methodologies align)

---

## S1: Rapid Library Search

**Location**: `S1-rapid/`

### Files
- `approach.md` - S1 methodology
- `sqlalchemy-inspector.md` - Built-in reflection
- `alembic.md` - Migration generation
- `sqlalchemy-diff.md` - Schema comparison (maintenance concerns)
- `sqlacodegen.md` - Reverse engineering
- `django-inspectdb.md` - Django comparison
- `prisma-introspect.md` - Node.js comparison
- `recommendation.md` - Final recommendations

### Key Findings
- **SQLAlchemy Inspector**: Foundation for all tools, 27M+ weekly downloads
- **Alembic**: 25M+ monthly downloads, essential for migrations
- **sqlacodegen**: 350K+ monthly, actively maintained, SQLAlchemy 2.0 support
- **sqlalchemy-diff**: Maintenance concerns, not recommended

---

## S2: Comprehensive Solution Analysis

**Location**: `S2-comprehensive/`

### Files
- `approach.md` - S2 methodology
- `library-sqlalchemy-inspector.md` - Detailed analysis
- `library-alembic-autogenerate.md` - Detailed analysis
- `library-sqlalchemy-diff.md` - Analysis (unmaintained)
- `library-sqlacodegen.md` - Detailed analysis
- `feature-comparison.md` - Cross-tool capability matrix
- `accuracy-analysis.md` - What each tool misses
- `recommendation.md` - Evidence-based guidance

### Weighted Scoring Results

| Tool | Score | Verdict |
|------|-------|---------|
| SQLAlchemy Inspector | 8.80/10 | Primary |
| Alembic Autogenerate | 8.80/10 | Primary |
| sqlacodegen | 8.30/10 | Specialized |
| sqlalchemy-diff | 5.40/10 | Not recommended |

### sqlacodegen Accuracy

- **Accuracy Rating**: 75-85% for typical schemas
- **Works well**: Basic tables, columns, simple FK
- **Requires refinement**: Self-referential, many-to-many, inheritance
- **Recommendation**: Use as starting point, expect 15-25% manual work

---

## S3: Need-Driven Discovery

**Location**: `S3-need-driven/`

### Files
- `approach.md` - S3 methodology
- `use-case-legacy-reverse-engineering.md` - Generate models from DB
- `use-case-ci-migration-validation.md` - Validate in CI/CD
- `use-case-multi-environment-sync.md` - Dev/staging/prod sync
- `use-case-greenfield-project.md` - New project setup
- `use-case-database-first.md` - DB-driven development
- `recommendation.md` - Best-fit solutions

### Use Case Recommendations

| Use Case | Primary Tool | Alternative |
|----------|-------------|-------------|
| Legacy reverse engineering | sqlacodegen | Manual + Inspector |
| CI/CD migration validation | Alembic + pytest | migra (PostgreSQL) |
| Multi-environment sync | Alembic + migra | Custom scripts |
| Greenfield project | Alembic | Django migrations |
| Database-first development | sqlacodegen + Alembic | Inspector scripts |

---

## S4: Strategic Solution Selection

**Location**: `S4-strategic/`

### Files
- `approach.md` - S4 methodology
- `sqlalchemy-ecosystem.md` - SQLAlchemy 2.0 trajectory
- `alembic-viability.md` - Long-term assessment
- `sqlalchemy-diff-viability.md` - Project health (HIGH RISK)
- `sqlacodegen-viability.md` - Project health (MODERATE RISK)
- `ecosystem-trajectory.md` - 2025-2030 trends
- `recommendation.md` - Strategic guidance

### 3-Year Viability Scores

| Tool | Survival | Risk | Key Factor |
|------|----------|------|------------|
| **SQLAlchemy Inspector** | 95% | Very Low | Core SQLAlchemy |
| **Alembic** | 90% | Low | Industry standard |
| **sqlacodegen** | 60% | Moderate | Single maintainer |
| **sqlalchemy-diff** | 30% | High | Unmaintained 3.5+ years |

### Ecosystem Trends (2025-2030)

1. **SQLAlchemy 2.0**: Complete migration, now table stakes
2. **Async adoption**: Growing to 50-60% of new projects
3. **Schema-as-code**: Atlas, Prisma patterns emerging
4. **Type annotations**: Becoming expected, not optional
5. **AI tooling**: Emerging 2026-2027, augments not replaces

---

## Decision Framework

### By Scenario

```
New SQLAlchemy project?
└── Alembic (migrations from day 1)

Existing database, need models?
└── sqlacodegen (75-85% accuracy, refine manually)

Schema validation in CI?
└── Alembic check + pytest (or migra for PostgreSQL)

Schema comparison needed?
└── Inspector + custom scripts (NOT sqlalchemy-diff)

Long-term strategic choice?
└── SQLAlchemy Inspector + Alembic (95%/90% survival)
```

### What to Avoid

- **sqlalchemy-diff**: Unmaintained since 2021
- **migra**: Deprecated in 2024
- **Custom ORM tools**: Stick with SQLAlchemy ecosystem

---

## Total Research Volume

| Phase | Files | Lines |
|-------|-------|-------|
| S1 Rapid | 8 | ~600 |
| S2 Comprehensive | 8 | ~1,500 |
| S3 Need-Driven | 7 | ~2,100 |
| S4 Strategic | 7 | ~2,400 |
| **Total** | **30** | **~6,600** |

---

## Research Disclaimer

This research is provided for informational purposes only and should not be considered professional advice. Tool capabilities, maintenance status, and ecosystem dynamics change frequently. No warranty is provided regarding accuracy, completeness, or fitness for a particular purpose.

**Methodology Transparency**: See metadata.yaml for data sources and attribution.

---

**Date compiled**: December 4, 2025
