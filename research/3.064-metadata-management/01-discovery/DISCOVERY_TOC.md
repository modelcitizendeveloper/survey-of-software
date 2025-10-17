# Metadata Management Discovery: Table of Contents

**Compiled:** 2025-10-13
**Status:** S1-rapid COMPLETE (S2-S4 pending)
**Total Content:** 5 files, ~500 lines (S1 only)
**Research Time:** ~60 minutes (S1 rapid assessment)

This document provides a navigation index for the metadata management platform discovery research. Currently only S1 (Rapid Discovery) is complete, providing initial platform comparison and recommendations.

---

## 1. Executive Summary

### S1: Rapid Discovery Conclusion

**OpenMetadata is the recommended choice for most teams** seeking a comprehensive open-source metadata management platform. It offers the best balance of features (discovery + observability + governance), deployment flexibility (self-hosted or managed via Collate), and active development (164 releases, 373 contributors).

**Alternative Recommendations:**
- **DataHub**: Best for enterprise governance requirements and largest ecosystem
- **Amundsen**: Best for simplest setup and pure discovery focus
- **Atlan**: Best for commercial support and packaged deployment

### Platform Comparison Snapshot

| Platform | Type | Setup Time | Connectors | Best For |
|----------|------|------------|------------|----------|
| OpenMetadata | Open-source | 2-4 hours | 84+ | Unified platform (70% of teams) |
| DataHub | Open-source | 4-8 hours | 50+ | Enterprise governance |
| Amundsen | Open-source | 1-3 hours | 30+ | Simplicity and speed |
| Atlan | Commercial | 1-2 hours | 100+ | Managed service |

---

## 2. Methodology Index

### S1: Rapid Discovery (COMPLETE)

**Purpose:** Identify leading metadata management platforms and compare features
**Files:** 5 documents, ~500 lines
**Time to Read:** 30-40 minutes

#### Files

1. **approach.md** - Methodology for platform selection and comparison
2. **provider-openmetadata.md** - OpenMetadata analysis (⭐⭐⭐⭐½ recommended)
3. **provider-datahub.md** - DataHub analysis (⭐⭐⭐⭐⭐ for enterprise)
4. **provider-amundsen.md** - Amundsen analysis (⭐⭐⭐⭐ for simplicity)
5. **recommendation.md** - Final verdict and decision framework

#### Key Findings

**Platform Landscape:**
- 3 major open-source platforms (OpenMetadata, DataHub, Amundsen)
- 2 commercial leaders (Atlan, Alation)
- Emerging options (Apache Atlas, Marquez, OpenDataDiscovery)

**OpenMetadata Strengths:**
- Unified discovery + observability + governance
- 84+ connectors (broadest ecosystem)
- Column-level lineage
- Built-in data quality features
- Active development (latest: 1.10.1, Oct 9, 2025)
- Managed service option via Collate

**DataHub Strengths:**
- Largest community (300+ contributors, ~15k stars)
- Best governance features (fine-grained access control, PII tagging)
- Proven at scale (LinkedIn, 100+ companies)
- Plugin architecture for extensibility

**Amundsen Strengths:**
- Simplest setup (1-3 hours)
- Clean UI focused on discovery
- Data preview feature (live database queries)
- Backend flexibility (Neo4j, Neptune, Atlas)

#### Confidence Level

**MODERATE (7/10)** - Based on web research and documentation review only. Hands-on testing (S2) required for higher confidence.

#### Time Investment

- Research time: ~60 minutes
- Reading time: ~30 minutes
- Best for: Initial platform comparison and shortlist creation

---

### S2: Comprehensive Testing (PENDING)

**Purpose:** Hands-on deployment and testing of top 3 platforms
**Planned Activities:**
- Deploy OpenMetadata, DataHub, Amundsen via Docker
- Test connector configuration (PostgreSQL, dbt, Tableau)
- Evaluate lineage tracking accuracy
- Compare data quality features
- Assess resource requirements
- Document migration paths

**Estimated Time:** 8-12 hours

---

### S3: Need-Driven Selection (PENDING)

**Purpose:** Match platforms to specific use cases and team sizes
**Planned Use Cases:**
- Small team (< 10 people) discovery needs
- Medium team (10-50 people) governance requirements
- Enterprise (50+ people) compliance needs
- Data quality focused scenarios
- Multi-cloud/hybrid deployments

**Estimated Time:** 6-8 hours

---

### S4: Strategic Assessment (PENDING)

**Purpose:** Long-term viability and ecosystem health analysis
**Planned Research:**
- Governance model comparison
- Community health metrics
- Adoption trajectory analysis
- Vendor backing and commercial ecosystem
- Migration risk assessment

**Estimated Time:** 6-8 hours

---

## 3. Quick Decision Framework

Use this framework to determine which platform fits your needs.

### By Primary Need

**Need: Unified Platform (Discovery + Observability + Governance)**
→ **OpenMetadata** (4.5/5)

**Need: Enterprise Governance (Fine-grained access control, GDPR)**
→ **DataHub** (5/5)

**Need: Simplicity and Speed (Fastest time-to-value)**
→ **Amundsen** (4/5)

**Need: Commercial Support (Managed service, SLAs)**
→ **Atlan** (4.5/5)

### By Team Size

**Small Team (< 10 people)**
1. Amundsen - Simplest setup
2. OpenMetadata - If you need lineage/quality
3. Atlan Free Tier - If you prefer SaaS

**Medium Team (10-50 people)**
1. OpenMetadata - Best feature balance
2. DataHub - If governance is critical
3. Collate (Managed OpenMetadata) - If budget allows

**Large Team (50+ people)**
1. DataHub - Proven at scale
2. OpenMetadata - Modern architecture
3. Atlan/Alation - Commercial support

### By Feature Priority

**Priority: Column-Level Lineage**
→ OpenMetadata or DataHub (Amundsen lacks this)

**Priority: Data Quality**
→ OpenMetadata (built-in) or Atlan

**Priority: Connector Breadth**
→ OpenMetadata (84+) or Atlan (100+)

**Priority: Community Size**
→ DataHub (300+ contributors, ~15k stars)

**Priority: Setup Speed**
→ Amundsen (1-3 hours) or Atlan (managed)

---

## 4. File Directory

### Complete File Listing

#### S1: Rapid Discovery (5 files, ~500 lines)

```
/01-discovery/S1-rapid/
├── approach.md                  # Platform selection methodology
├── provider-openmetadata.md     # OpenMetadata analysis (recommended)
├── provider-datahub.md          # DataHub analysis (enterprise choice)
├── provider-amundsen.md         # Amundsen analysis (simplicity choice)
└── recommendation.md            # Final verdict and decision matrix
```

#### S2: Comprehensive Testing (PENDING)

```
/01-discovery/S2-comprehensive/
└── (To be created)
```

#### S3: Need-Driven Selection (PENDING)

```
/01-discovery/S3-need-driven/
└── (To be created)
```

#### S4: Strategic Assessment (PENDING)

```
/01-discovery/S4-strategic/
└── (To be created)
```

---

## 5. Reading Recommendations

Choose your path based on what you need to learn:

### "Which platform should I choose?" (10 minutes)

**Read:** `/01-discovery/S1-rapid/recommendation.md`

**What you'll learn:**
- Top recommendation: OpenMetadata for 70% of teams
- When to choose DataHub, Amundsen, or commercial options
- Decision matrix by team size and use case

### "Tell me about OpenMetadata" (10 minutes)

**Read:** `/01-discovery/S1-rapid/provider-openmetadata.md`

**What you'll learn:**
- Comprehensive feature set (discovery + observability + governance)
- 84+ connector ecosystem
- Deployment options (self-hosted or Collate managed)
- Strengths vs weaknesses
- Competitive positioning

### "I need enterprise governance" (10 minutes)

**Read:** `/01-discovery/S1-rapid/provider-datahub.md`

**What you'll learn:**
- Fine-grained access control and PII tagging
- Plugin architecture for extensibility
- LinkedIn-scale proven performance
- Managed service via Acryl Data

### "I want the simplest solution" (10 minutes)

**Read:** `/01-discovery/S1-rapid/provider-amundsen.md`

**What you'll learn:**
- Fastest setup (1-3 hours)
- Discovery-focused features
- Data preview capabilities
- Backend flexibility options

### "Compare all three platforms" (30 minutes)

**Read all provider files:**
1. `/01-discovery/S1-rapid/provider-openmetadata.md` (10 min)
2. `/01-discovery/S1-rapid/provider-datahub.md` (10 min)
3. `/01-discovery/S1-rapid/provider-amundsen.md` (10 min)

**What you'll learn:**
- Side-by-side feature comparison
- Strengths and trade-offs of each platform
- Use cases where each excels

---

## 6. Next Steps

### For Further Research

**S2 (Comprehensive Testing)** should focus on:
1. Hands-on deployment of top 3 platforms
2. Connector configuration testing
3. Lineage accuracy validation
4. Data quality feature comparison
5. Resource requirement benchmarking

**S3 (Need-Driven Selection)** should focus on:
1. Use case specific recommendations
2. Team size optimization
3. Feature requirement mapping
4. Cost analysis (self-hosted vs managed)

**S4 (Strategic Assessment)** should focus on:
1. Long-term viability analysis
2. Community health metrics
3. Commercial ecosystem evaluation
4. Migration risk assessment

### Immediate Action Items

**If choosing OpenMetadata:**
- Visit sandbox.open-metadata.org for hands-on testing
- Review documentation at docs.open-metadata.org
- Evaluate Collate managed service if self-hosting is not desired

**If choosing DataHub:**
- Check demo at demo.datahubproject.io
- Join Slack community (5000+ members)
- Evaluate Acryl Data for managed service

**If choosing Amundsen:**
- Review GitHub repo for deployment guides
- Test with Neo4j backend first (simplest)
- Plan for connector configuration time

---

## 7. Appendix: Key Metrics Reference

| Metric | OpenMetadata | DataHub | Amundsen |
|--------|--------------|---------|----------|
| GitHub Stars | 7.7k | ~15k | ~4k |
| Contributors | 373 | 300+ | 100+ |
| Connectors | 84+ | 50+ | 30+ |
| Setup Time | 2-4 hours | 4-8 hours | 1-3 hours |
| Column Lineage | ✅ Yes | ✅ Yes | ❌ No |
| Data Quality | ✅ Built-in | ⚠️ Add-on | ❌ No |
| Managed Service | Collate | Acryl Data | None |
| License | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| Latest Release | 1.10.1 (Oct 9, 2025) | Monthly | Quarterly |
| Best For | Most teams | Enterprise | Simplicity |

---

**Compiled:** 2025-10-13
**Experiment:** 3.070-metadata-management
**Phase:** 01-discovery (S1 COMPLETE, S2-S4 PENDING)
**Status:** Initial rapid assessment complete, hands-on testing pending
**Overall Recommendation:** OpenMetadata for 70% of teams, DataHub for enterprise governance, Amundsen for simplicity
