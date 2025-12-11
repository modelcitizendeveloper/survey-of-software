# Schema Design: Tier 3 Services (Priority 1)

**Application**: Research Lineage System for Spawn Solutions Framework
**Date**: October 17, 2025
**Status**: Schema Specification
**Priority**: Tier 3 (Managed Services) - Highest vendor gaming risk

---

## Why Tier 3 First?

**Vendor Stakes Are Highest**:
- Businesses choosing providers based on our analysis
- Vendors have direct financial incentive to manipulate data
- Section 0 documents already exist (8 complete)
- Provider recommendations directly impact vendor revenue

**Gaming Attack Surface**:
- Cost data can be manipulated (vendors change pricing, hide fees)
- Migration estimates can be disputed ("It's easier than you say!")
- Lock-in claims can be challenged ("We're not lock-in!")
- Provider features can be exaggerated (fake case studies, testimonials)

**Timeline Risk**:
- Phase 2 just completed (Oct 17, 2025)
- Public cookbooks launching soon (6-12 months)
- Vendors will notice when traffic increases
- Need lineage BEFORE vendor gaming begins

---

## Tier 3 File Structure

```
research/3.040-database-services/
  data/
    section0/
      standards_assessment.json      # Does Tier 2 standard exist?
      path2_viability.json            # Portability analysis
      path_comparison.json            # DIY vs Standards vs Managed
      decision_framework.json         # When to choose each path
    providers/
      supabase.json                   # Provider-specific data
      neon.json
      aws-rds.json
      postgresql-selfhosted.json      # DIY option
    comparisons/
      cost_comparison.json            # 3-year TCO analysis
      feature_matrix.json             # Feature comparison table
      lock_in_assessment.json         # Provider lock-in risks
    migrations/
      supabase_to_neon.json          # Migration scenario
      dynamodb_to_postgresql.json
      # ... all documented migration paths
    synthesis/
      recommendations.json            # Final recommendations
      criteria_weights.json           # How criteria were weighted

  SECTION_0_STANDARDS.md              # Generated from JSON
  SERVICE_EXPLAINER.md                # Generated from JSON
```

---

## Schema 1: Standards Assessment (section0/standards_assessment.json)

**Purpose**: Document whether Tier 2 standard exists for this service category

```json
{
  "research_id": "3.040-database-services",
  "service_category": "Database Services",
  "last_updated": "2025-10-17T10:00:00Z",

  "tier2_standard": {
    "exists": true,
    "standard_id": "2.050-postgresql-sql",
    "standard_name": "PostgreSQL SQL",
    "what_standardized": [
      "SQL dialect (PostgreSQL-flavored SQL)",
      "Wire protocol (PostgreSQL connection protocol)",
      "Extensions ecosystem (PostGIS, pgvector, TimescaleDB)",
      "Dump/restore format (pg_dump/pg_restore)"
    ],
    "governance": {
      "body": "PostgreSQL Global Development Group",
      "type": "community_led",
      "stability_years": 30,
      "maturity_level": "graduated"
    },
    "evidence": {
      "source_url": "https://www.postgresql.org/about/",
      "timestamp": "2025-10-17T10:05:00Z",
      "credibility": "first_party",
      "retrieval_method": "documentation_review"
    }
  },

  "historical_attempts": [
    {
      "name": "SQL Standard (ANSI SQL)",
      "status": "partial",
      "reason": "Every database extends standard differently, limited portability",
      "evidence": {
        "source_url": "https://en.wikipedia.org/wiki/SQL",
        "timestamp": "2025-10-17T10:10:00Z",
        "credibility": "third_party"
      }
    }
  ]
}
```

**Why This Matters**:
- **Vendor dispute**: "PostgreSQL isn't a real standard!" → Show evidence
- **Gaming detection**: If governance info changes (Wikipedia vandalism), detect it
- **Historical tracking**: Document failed standardization attempts

---

## Schema 2: Path 2 Viability (section0/path2_viability.json)

**Purpose**: Assess portability within standard ecosystem

```json
{
  "research_id": "3.040-database-services",
  "tier2_standard_id": "2.050-postgresql-sql",
  "last_updated": "2025-10-17T11:00:00Z",

  "portability_level": "HIGH",
  "portability_justification": "50+ compatible providers, pg_dump/restore is universal, 8-40 hour migrations documented",

  "compatible_providers": {
    "count": 50,
    "categories": {
      "self_hosted": [
        {
          "name": "PostgreSQL",
          "type": "reference_implementation",
          "url": "https://www.postgresql.org",
          "evidence": {
            "source_url": "https://www.postgresql.org/download/",
            "timestamp": "2025-10-17T11:05:00Z",
            "credibility": "first_party"
          }
        }
      ],
      "managed_postgresql": [
        {
          "name": "Supabase",
          "compatibility": "100%",
          "url": "https://supabase.com",
          "evidence": {
            "source_url": "https://supabase.com/docs/guides/database",
            "timestamp": "2025-10-17T11:10:00Z",
            "credibility": "first_party",
            "quote": "Supabase is PostgreSQL with additional features"
          }
        },
        {
          "name": "Neon",
          "compatibility": "100%",
          "url": "https://neon.tech",
          "evidence": {
            "source_url": "https://neon.tech/docs/introduction",
            "timestamp": "2025-10-17T11:12:00Z",
            "credibility": "first_party",
            "quote": "Neon is fully compatible with PostgreSQL"
          }
        }
      ],
      "postgresql_compatible": [
        {
          "name": "CockroachDB",
          "compatibility": "95%",
          "compatibility_notes": "PostgreSQL wire protocol, some features differ",
          "url": "https://www.cockroachlabs.com",
          "evidence": {
            "source_url": "https://www.cockroachlabs.com/docs/stable/postgresql-compatibility.html",
            "timestamp": "2025-10-17T11:15:00Z",
            "credibility": "first_party"
          }
        }
      ]
    }
  },

  "migration_complexity": {
    "typical_time_hours": {
      "min": 8,
      "max": 40,
      "median": 20
    },
    "method": "pg_dump/pg_restore (standard tools)",
    "code_changes_required": false,
    "dashboard_changes_required": false,
    "data_migration_only": true,
    "evidence": {
      "source_url": "https://www.postgresql.org/docs/current/backup-dump.html",
      "timestamp": "2025-10-17T11:20:00Z",
      "credibility": "first_party",
      "based_on": "PostgreSQL official documentation"
    }
  },

  "lock_in_risk": "LOW",
  "lock_in_justification": "Standard protocol, standard tools, 50+ compatible providers"
}
```

**Vendor Gaming Defenses**:
- **Provider count**: Track over time (detect if providers disappear or appear suspiciously)
- **Compatibility claims**: Link to official docs (detect if vendor changes claims)
- **Migration estimates**: Based on documented evidence (not vendor marketing)

---

## Schema 3: Provider Data (providers/supabase.json)

**Purpose**: Structured data for each provider

```json
{
  "research_id": "3.040-database-services",
  "provider": {
    "name": "Supabase",
    "type": "managed_postgresql",
    "official_url": "https://supabase.com",
    "founded_year": 2020,
    "company_stage": "Series B (2023, $80M)",
    "last_updated": "2025-10-17T12:00:00Z"
  },

  "standard_compliance": {
    "tier2_standard_id": "2.050-postgresql-sql",
    "compliance_level": "100%",
    "evidence": {
      "source_url": "https://supabase.com/docs/guides/database",
      "timestamp": "2025-10-17T12:05:00Z",
      "credibility": "first_party",
      "quote": "Supabase is PostgreSQL with authentication, instant APIs, and realtime subscriptions"
    }
  },

  "pricing": {
    "free_tier": {
      "exists": true,
      "limits": {
        "storage_gb": 500,
        "egress_gb": 5,
        "database_size_mb": 500,
        "concurrent_connections": 100
      },
      "evidence": {
        "source_url": "https://supabase.com/pricing",
        "timestamp": "2025-10-17T12:10:00Z",
        "credibility": "first_party"
      }
    },
    "paid_tiers": [
      {
        "tier_name": "Pro",
        "monthly_cost_usd": 25,
        "limits": {
          "storage_gb": "unlimited",
          "egress_gb": 250,
          "database_size_gb": 8,
          "concurrent_connections": 500
        },
        "evidence": {
          "source_url": "https://supabase.com/pricing",
          "timestamp": "2025-10-17T12:10:00Z",
          "credibility": "first_party"
        }
      }
    ],
    "cost_tracking": [
      {
        "date": "2025-10-17",
        "pro_tier_cost": 25,
        "source_url": "https://supabase.com/pricing",
        "note": "Initial capture"
      }
    ]
  },

  "features": {
    "standard_features": [
      {
        "feature": "PostgreSQL database",
        "portable": true,
        "description": "Full PostgreSQL 15 compatibility"
      },
      {
        "feature": "SQL queries",
        "portable": true,
        "description": "Standard PostgreSQL SQL"
      }
    ],
    "proprietary_features": [
      {
        "feature": "Supabase Auth",
        "portable": false,
        "lock_in_severity": "medium",
        "migration_effort_hours": 20,
        "description": "User management, row-level security integration",
        "evidence": {
          "source_url": "https://supabase.com/docs/guides/auth",
          "timestamp": "2025-10-17T12:20:00Z",
          "credibility": "first_party"
        }
      },
      {
        "feature": "Realtime subscriptions",
        "portable": false,
        "lock_in_severity": "medium",
        "migration_effort_hours": 20,
        "description": "WebSocket-based database change subscriptions",
        "evidence": {
          "source_url": "https://supabase.com/docs/guides/realtime",
          "timestamp": "2025-10-17T12:25:00Z",
          "credibility": "first_party"
        }
      }
    ]
  },

  "production_usage": [
    {
      "company": "Company X",
      "use_case": "SaaS application backend",
      "scale": "50K users",
      "evidence_type": "case_study",
      "evidence": {
        "source_url": "https://supabase.com/customers/company-x",
        "timestamp": "2025-10-17T12:30:00Z",
        "credibility": "second_party",
        "note": "Official Supabase case study (vendor provided)"
      }
    }
  ],

  "lock_in_assessment": {
    "overall_risk": "MEDIUM",
    "justification": "PostgreSQL core is portable (LOW lock-in), but Auth/Realtime features create soft lock-in (MEDIUM)",
    "migration_away": {
      "time_hours_min": 20,
      "time_hours_max": 60,
      "challenges": [
        "Reimplement Supabase Auth with alternative (Auth0, Keycloak)",
        "Reimplement Realtime subscriptions (custom WebSocket, Pusher, Ably)",
        "Migrate row-level security policies (manual SQL)"
      ]
    }
  }
}
```

**Gaming Detection**:
- **Pricing tracking**: `cost_tracking` array detects price changes over time
- **Feature claims**: Evidence links detect if vendor removes/changes features
- **Production usage**: Track if case studies disappear (fake testimonials removed)

---

## Schema 4: Cost Comparison (comparisons/cost_comparison.json)

**Purpose**: 3-year TCO comparison across paths

```json
{
  "research_id": "3.040-database-services",
  "comparison_scenario": "1M active series, 3 years",
  "last_updated": "2025-10-17T13:00:00Z",

  "paths": {
    "path1_diy": {
      "option": "Self-hosted PostgreSQL",
      "costs": {
        "year1_monthly_usd": 200,
        "year2_monthly_usd": 200,
        "year3_monthly_usd": 200,
        "total_3_years_usd": 7200,
        "breakdown": [
          {"item": "VPS hosting", "monthly_usd": 100},
          {"item": "Backup storage", "monthly_usd": 50},
          {"item": "Monitoring tools", "monthly_usd": 50}
        ],
        "evidence": {
          "source_url": "https://www.hetzner.com/cloud",
          "timestamp": "2025-10-17T13:05:00Z",
          "credibility": "first_party",
          "note": "Hetzner Cloud CX31 pricing"
        }
      },
      "operational_cost": {
        "hours_per_month": 10,
        "hourly_rate_usd": 300,
        "monthly_usd": 3000,
        "total_3_years_usd": 108000,
        "justification": "DBA time: backups, updates, scaling, monitoring",
        "evidence": {
          "source_url": "https://www.glassdoor.com/Salaries/database-administrator-salary",
          "timestamp": "2025-10-17T13:10:00Z",
          "credibility": "third_party",
          "note": "Based on DBA hourly rates"
        }
      },
      "true_tco_3_years_usd": 115200
    },

    "path2_standards": {
      "option": "Neon (managed PostgreSQL)",
      "costs": {
        "year1_monthly_usd": 19,
        "year2_monthly_usd": 19,
        "year3_monthly_usd": 19,
        "total_3_years_usd": 684,
        "breakdown": [
          {"item": "Neon Scale plan", "monthly_usd": 19}
        ],
        "evidence": {
          "source_url": "https://neon.tech/pricing",
          "timestamp": "2025-10-17T13:15:00Z",
          "credibility": "first_party"
        }
      },
      "operational_cost": {
        "hours_per_month": 0,
        "monthly_usd": 0,
        "total_3_years_usd": 0,
        "justification": "Fully managed, zero operational burden"
      },
      "true_tco_3_years_usd": 684
    },

    "path3_proprietary": {
      "option": "MongoDB Atlas (NoSQL, proprietary)",
      "costs": {
        "year1_monthly_usd": 57,
        "year2_monthly_usd": 57,
        "year3_monthly_usd": 57,
        "total_3_years_usd": 2052,
        "breakdown": [
          {"item": "MongoDB Atlas M10", "monthly_usd": 57}
        ],
        "evidence": {
          "source_url": "https://www.mongodb.com/pricing",
          "timestamp": "2025-10-17T13:20:00Z",
          "credibility": "first_party"
        }
      },
      "operational_cost": {
        "hours_per_month": 0,
        "monthly_usd": 0,
        "total_3_years_usd": 0,
        "justification": "Fully managed"
      },
      "migration_away_cost": {
        "time_hours": 200,
        "hourly_rate_usd": 300,
        "total_usd": 60000,
        "justification": "NoSQL → SQL schema redesign, query rewrite, data migration"
      },
      "true_tco_3_years_usd": 2052
    }
  },

  "savings_analysis": {
    "neon_vs_selfhosted": {
      "savings_usd": 114516,
      "savings_percent": 99.4,
      "note": "Managed PostgreSQL massively cheaper when accounting for ops burden"
    },
    "neon_vs_mongodb": {
      "savings_usd": 1368,
      "savings_percent": 66.7,
      "note": "Standards-based cheaper, avoids lock-in"
    }
  }
}
```

**Gaming Detection**:
- **Price tracking**: Historical pricing snapshots detect sudden changes
- **Evidence links**: Pricing URLs can be revalidated to detect gaming
- **Operational cost transparency**: Show assumptions (can be challenged but are documented)

---

## Schema 5: Migration Scenarios (migrations/supabase_to_neon.json)

**Purpose**: Document migration paths with effort estimates

```json
{
  "research_id": "3.040-database-services",
  "migration": {
    "from_provider": "Supabase",
    "to_provider": "Neon",
    "migration_type": "postgresql_to_postgresql",
    "last_updated": "2025-10-17T14:00:00Z"
  },

  "motivation": "Cost optimization, want serverless scaling",

  "effort_estimate": {
    "total_hours_min": 8,
    "total_hours_max": 20,
    "median_hours": 12,
    "confidence": "high",
    "based_on": "Standard PostgreSQL migration process, both providers 100% compatible",
    "evidence": {
      "source_url": "https://www.postgresql.org/docs/current/backup-dump.html",
      "timestamp": "2025-10-17T14:05:00Z",
      "credibility": "first_party"
    }
  },

  "steps": [
    {
      "step": 1,
      "action": "Create Neon database",
      "time_hours": 1,
      "complexity": "low",
      "instructions": "Sign up for Neon, create new PostgreSQL database"
    },
    {
      "step": 2,
      "action": "pg_dump from Supabase",
      "time_hours_min": 1,
      "time_hours_max": 4,
      "complexity": "low",
      "instructions": "pg_dump -h supabase-host -U postgres dbname > dump.sql",
      "variables": "Time depends on database size"
    },
    {
      "step": 3,
      "action": "pg_restore to Neon",
      "time_hours_min": 2,
      "time_hours_max": 8,
      "complexity": "medium",
      "instructions": "pg_restore -h neon-host -U postgres -d dbname dump.sql",
      "variables": "Time depends on database size"
    },
    {
      "step": 4,
      "action": "Update connection strings",
      "time_hours": 1,
      "complexity": "low",
      "instructions": "Update DATABASE_URL in application environment"
    },
    {
      "step": 5,
      "action": "Test application",
      "time_hours_min": 2,
      "time_hours_max": 4,
      "complexity": "medium",
      "instructions": "Run test suite, verify functionality"
    },
    {
      "step": 6,
      "action": "Migrate traffic",
      "time_hours": 1,
      "complexity": "medium",
      "instructions": "Blue-green deployment or DNS switch"
    }
  ],

  "code_changes_required": false,
  "code_changes_justification": "Both are standard PostgreSQL, same SQL dialect",

  "gotchas": [
    {
      "issue": "Supabase Auth features",
      "severity": "high",
      "mitigation": "Need to migrate to alternative auth solution (Auth0, Keycloak, etc.)",
      "effort_hours_additional": 20,
      "evidence": {
        "source_url": "https://supabase.com/docs/guides/auth",
        "timestamp": "2025-10-17T14:10:00Z",
        "credibility": "first_party"
      }
    },
    {
      "issue": "Row-level security policies",
      "severity": "medium",
      "mitigation": "Neon supports RLS, but no GUI - need to migrate policies via SQL",
      "effort_hours_additional": 2,
      "evidence": {
        "source_url": "https://www.postgresql.org/docs/current/ddl-rowsecurity.html",
        "timestamp": "2025-10-17T14:15:00Z",
        "credibility": "first_party"
      }
    }
  ],

  "downtime_required": false,
  "downtime_justification": "Can run parallel (Supabase + Neon), switch DNS when ready",

  "cost_change": {
    "from_monthly_usd": 25,
    "to_monthly_usd": 19,
    "savings_monthly_usd": 6,
    "savings_annual_usd": 72
  },

  "when_worth_it": "Team spending >4 hours/month on database operations, or need serverless scaling"
}
```

**Gaming Defense**:
- **Effort transparency**: Step-by-step breakdown prevents "It's easier!" disputes
- **Gotchas documented**: Proactively address migration challenges
- **Evidence-based**: Link to official docs (not vendor marketing)

---

## Schema 6: Lock-in Assessment (comparisons/lock_in_assessment.json)

**Purpose**: Compare vendor lock-in risks

```json
{
  "research_id": "3.040-database-services",
  "last_updated": "2025-10-17T15:00:00Z",

  "providers": {
    "supabase": {
      "overall_risk": "MEDIUM",
      "standard_features": {
        "risk": "LOW",
        "features": [
          {"name": "PostgreSQL database", "portable": true},
          {"name": "SQL queries", "portable": true},
          {"name": "Extensions (PostGIS, pgvector)", "portable": true}
        ]
      },
      "proprietary_features": {
        "risk": "MEDIUM",
        "features": [
          {
            "name": "Supabase Auth",
            "lock_in_severity": "medium",
            "migration_effort_hours": 20,
            "alternative": "Auth0, Keycloak, custom"
          },
          {
            "name": "Realtime subscriptions",
            "lock_in_severity": "medium",
            "migration_effort_hours": 20,
            "alternative": "Pusher, Ably, custom WebSocket"
          },
          {
            "name": "Storage (S3-like)",
            "lock_in_severity": "low",
            "migration_effort_hours": 4,
            "alternative": "Cloudflare R2, Backblaze B2, AWS S3"
          }
        ]
      },
      "migration_away_total_hours": {
        "min": 20,
        "max": 60,
        "median": 40
      },
      "evidence": {
        "source_url": "https://supabase.com/docs",
        "timestamp": "2025-10-17T15:05:00Z",
        "credibility": "first_party"
      }
    },

    "mongodb_atlas": {
      "overall_risk": "VERY HIGH",
      "standard_features": {
        "risk": "VERY HIGH",
        "features": []
      },
      "proprietary_features": {
        "risk": "VERY HIGH",
        "features": [
          {
            "name": "MongoDB query language",
            "lock_in_severity": "very_high",
            "migration_effort_hours": 80,
            "alternative": "SQL (complete rewrite)"
          },
          {
            "name": "MongoDB data model (NoSQL)",
            "lock_in_severity": "very_high",
            "migration_effort_hours": 80,
            "alternative": "Relational schema design from scratch"
          },
          {
            "name": "MongoDB drivers/ODMs",
            "lock_in_severity": "very_high",
            "migration_effort_hours": 40,
            "alternative": "SQL ORMs (Prisma, SQLAlchemy)"
          }
        ]
      },
      "migration_away_total_hours": {
        "min": 100,
        "max": 300,
        "median": 200
      },
      "evidence": {
        "source_url": "https://www.mongodb.com/docs",
        "timestamp": "2025-10-17T15:10:00Z",
        "credibility": "first_party"
      }
    }
  },

  "comparison_matrix": {
    "columns": ["Provider", "Standard Features Risk", "Proprietary Features Risk", "Overall Risk", "Migration Hours"],
    "rows": [
      {
        "provider": "Supabase",
        "standard_risk": "LOW",
        "proprietary_risk": "MEDIUM",
        "overall_risk": "MEDIUM",
        "migration_hours": "20-60"
      },
      {
        "provider": "Neon",
        "standard_risk": "LOW",
        "proprietary_risk": "LOW",
        "overall_risk": "LOW",
        "migration_hours": "8-20"
      },
      {
        "provider": "MongoDB Atlas",
        "standard_risk": "VERY HIGH",
        "proprietary_risk": "VERY HIGH",
        "overall_risk": "VERY HIGH",
        "migration_hours": "100-300"
      }
    ]
  }
}
```

---

## Database Schema (SQLite)

**Tables for Tier 3 data**:

```sql
-- Research items (Tier 3 services)
CREATE TABLE tier3_research (
  id INTEGER PRIMARY KEY,
  research_id VARCHAR(255) UNIQUE NOT NULL, -- "3.040-database-services"
  category VARCHAR(255), -- "Database Services"
  tier2_standard_id VARCHAR(255), -- "2.050-postgresql-sql" or NULL
  standard_exists BOOLEAN,
  portability_level VARCHAR(50), -- "ZERO", "LOW", "MEDIUM", "HIGH", "VERY_HIGH"
  last_updated TIMESTAMPTZ
);

-- Providers
CREATE TABLE providers (
  id INTEGER PRIMARY KEY,
  research_id VARCHAR(255) REFERENCES tier3_research(research_id),
  name VARCHAR(255), -- "Supabase"
  type VARCHAR(100), -- "managed_postgresql", "proprietary_nosql"
  official_url TEXT,
  tier2_compliant BOOLEAN,
  overall_lock_in VARCHAR(50), -- "LOW", "MEDIUM", "HIGH", "VERY_HIGH"
  last_updated TIMESTAMPTZ
);

-- Provider pricing (temporal tracking)
CREATE TABLE provider_pricing (
  id INTEGER PRIMARY KEY,
  provider_id INTEGER REFERENCES providers(id),
  tier_name VARCHAR(100), -- "Free", "Pro", "Enterprise"
  monthly_cost_usd NUMERIC,

  -- Lineage
  source_url TEXT NOT NULL,
  timestamp TIMESTAMPTZ NOT NULL,
  credibility VARCHAR(50),

  -- Temporal
  captured_at TIMESTAMPTZ DEFAULT NOW()
);

-- Provider features
CREATE TABLE provider_features (
  id INTEGER PRIMARY KEY,
  provider_id INTEGER REFERENCES providers(id),
  feature_name VARCHAR(255),
  portable BOOLEAN, -- Is this feature portable?
  lock_in_severity VARCHAR(50), -- "none", "low", "medium", "high", "very_high"
  migration_effort_hours INTEGER,

  -- Lineage
  source_url TEXT,
  timestamp TIMESTAMPTZ,
  credibility VARCHAR(50)
);

-- Cost comparisons
CREATE TABLE cost_comparisons (
  id INTEGER PRIMARY KEY,
  research_id VARCHAR(255) REFERENCES tier3_research(research_id),
  scenario_description TEXT, -- "1M active series, 3 years"
  path VARCHAR(50), -- "path1_diy", "path2_standards", "path3_proprietary"
  provider_name VARCHAR(255),
  total_3_years_usd NUMERIC,
  true_tco_3_years_usd NUMERIC, -- Includes operational cost

  -- Lineage
  calculation_timestamp TIMESTAMPTZ,
  evidence_json TEXT -- Link to detailed breakdown
);

-- Migration scenarios
CREATE TABLE migration_scenarios (
  id INTEGER PRIMARY KEY,
  research_id VARCHAR(255) REFERENCES tier3_research(research_id),
  from_provider VARCHAR(255),
  to_provider VARCHAR(255),
  migration_type VARCHAR(100), -- "postgresql_to_postgresql", "nosql_to_sql"

  -- Effort
  total_hours_min INTEGER,
  total_hours_max INTEGER,
  median_hours INTEGER,
  confidence VARCHAR(50), -- "low", "medium", "high"

  -- Lineage
  based_on TEXT, -- Evidence description
  source_url TEXT,
  timestamp TIMESTAMPTZ
);

-- Migration gotchas
CREATE TABLE migration_gotchas (
  id INTEGER PRIMARY KEY,
  migration_scenario_id INTEGER REFERENCES migration_scenarios(id),
  issue TEXT,
  severity VARCHAR(50), -- "low", "medium", "high"
  mitigation TEXT,
  effort_hours_additional INTEGER,

  -- Lineage
  source_url TEXT,
  timestamp TIMESTAMPTZ
);

-- Lock-in assessments
CREATE TABLE lock_in_assessments (
  id INTEGER PRIMARY KEY,
  provider_id INTEGER REFERENCES providers(id),
  overall_risk VARCHAR(50), -- "LOW", "MEDIUM", "HIGH", "VERY_HIGH"
  migration_away_hours_min INTEGER,
  migration_away_hours_max INTEGER,
  migration_away_hours_median INTEGER,
  justification TEXT,

  -- Lineage
  assessed_at TIMESTAMPTZ,
  evidence_url TEXT
);
```

---

## Queries We Can Run

```sql
-- Which Tier 3 services have open standards?
SELECT research_id, category, tier2_standard_id
FROM tier3_research
WHERE standard_exists = true;

-- Show providers with LOW lock-in
SELECT p.name, p.type, l.overall_risk, l.migration_away_hours_median
FROM providers p
JOIN lock_in_assessments l ON p.id = l.provider_id
WHERE l.overall_risk = 'LOW'
ORDER BY l.migration_away_hours_median ASC;

-- Cost comparison: Show cheapest option per research
SELECT
  c.research_id,
  c.provider_name,
  c.true_tco_3_years_usd,
  c.path
FROM cost_comparisons c
WHERE c.true_tco_3_years_usd = (
  SELECT MIN(c2.true_tco_3_years_usd)
  FROM cost_comparisons c2
  WHERE c2.research_id = c.research_id
);

-- Migration difficulty matrix
SELECT
  from_provider,
  to_provider,
  migration_type,
  median_hours,
  confidence
FROM migration_scenarios
ORDER BY median_hours ASC;

-- Detect pricing changes (vendor gaming)
SELECT
  p.name,
  pp.tier_name,
  pp.monthly_cost_usd,
  pp.captured_at,
  LAG(pp.monthly_cost_usd) OVER (
    PARTITION BY pp.provider_id, pp.tier_name
    ORDER BY pp.captured_at
  ) AS previous_cost,
  pp.monthly_cost_usd - LAG(pp.monthly_cost_usd) OVER (
    PARTITION BY pp.provider_id, pp.tier_name
    ORDER BY pp.captured_at
  ) AS price_change
FROM provider_pricing pp
JOIN providers p ON pp.provider_id = p.id
WHERE price_change IS NOT NULL
ORDER BY ABS(price_change) DESC;
```

---

## Vendor Gaming Detection Queries

```sql
-- Detect sudden pricing spikes
SELECT
  p.name,
  pp.tier_name,
  pp.monthly_cost_usd,
  pp.captured_at,
  (pp.monthly_cost_usd - LAG(pp.monthly_cost_usd) OVER w) / LAG(pp.monthly_cost_usd) OVER w * 100 AS percent_change
FROM provider_pricing pp
JOIN providers p ON pp.provider_id = p.id
WINDOW w AS (PARTITION BY pp.provider_id, pp.tier_name ORDER BY pp.captured_at)
HAVING ABS(percent_change) > 50; -- Flag >50% price changes

-- Detect disappearing features (vendor removes capabilities)
SELECT
  p.name,
  pf.feature_name,
  pf.timestamp,
  'Feature removed from documentation' AS alert
FROM provider_features pf
JOIN providers p ON pf.provider_id = p.id
WHERE pf.source_url NOT IN (
  -- Subquery to check if URL is still valid (would need external validation)
  SELECT source_url FROM provider_features WHERE source_url IS NOT NULL
);

-- Detect compliance claim changes
SELECT
  p.name,
  p.tier2_compliant,
  p.last_updated,
  LAG(p.tier2_compliant) OVER (PARTITION BY p.id ORDER BY p.last_updated) AS previous_compliance
FROM providers p
WHERE p.tier2_compliant != LAG(p.tier2_compliant) OVER (PARTITION BY p.id ORDER BY p.last_updated);
```

---

## Next Steps

1. **Prototype**: Build with 1 Tier 3 research item (3.040-database-services)
2. **Validate**: Generate SECTION_0_STANDARDS.md from JSON, compare with existing
3. **Backfill**: Migrate remaining 7 Tier 3 Section 0 documents
4. **Queries**: Test vendor gaming detection on real data

**Timeline**: 20-30 hours for Tier 3 prototype + migration

---

**Status**: Schema Defined (Tier 3 Priority)
**Next**: Prototype with 3.040-database-services
**Nomenclature**: Will use "research" terminology in all schemas
