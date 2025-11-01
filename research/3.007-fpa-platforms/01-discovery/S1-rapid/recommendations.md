# S1 Rapid Discovery - Recommendations

**Experiment**: 3.007 FP&A Platforms
**Stage**: S1 - Rapid Discovery
**Date**: November 1, 2025

---

## S1 Research Summary

**Platforms Analyzed**: 8
- **Full depth** (500+ lines): Runway, Planful (forum post platforms)
- **Reduced depth** (~390 lines avg): Causal, Vena, Prophix, Adaptive Insights, Anaplan, OneStream

**Total Research Output**: ~3,500 lines of platform catalog content

---

## Market Structure

### Tier 1: Startup FP&A ($3K-30K/year, 20-500 employees)

**Platforms**: Runway, Causal

**Characteristics**:
- Fast implementation (1-4 weeks)
- Self-service or light consulting
- Modern HRIS integration (Runway) or data warehouse native (Causal)
- SaaS-focused features (ARR, MRR, cohort analysis)

**Key Finding**: **HRIS integration quality is competitive differentiator**
- Runway won forum post deal due to native Rippling integration
- Planful lost deal because no direct Rippling support

### Tier 2: Mid-Market FP&A ($15K-100K/year, 250-2000 employees)

**Platforms**: Vena, Prophix, Adaptive Insights

**Characteristics**:
- 1-3 month implementation
- Required consulting ($10K-50K)
- Driver-based planning, workforce planning, basic consolidation
- ERP integration focused (NetSuite, Sage Intacct, Microsoft Dynamics)

**Key Finding**: **Platform choice often driven by existing tech stack**
- Vena for Microsoft 365 shops
- Adaptive for Workday HCM customers
- Prophix for automation focus

### Tier 3: Enterprise CPM ($50K-500K/year, 2000+ employees)

**Platforms**: Planful, Anaplan, OneStream

**Characteristics**:
- 3-12 month implementation
- Heavy consulting required ($50K-300K)
- Advanced consolidation (multi-entity, multi-currency, multi-GAAP)
- Connected planning (finance + sales + supply chain + HR)

**Key Finding**: **Consolidation complexity determines platform need**
- Companies with 10+ entities need enterprise platforms
- Single-entity companies overpay for unused consolidation features

---

## Critical Integration Patterns

### HRIS Integration Quality Spectrum

**Strong SMB HRIS Integration**:
- **Runway**: Native Rippling, Gusto, BambooHR (1-click setup)
- **Causal**: Via API (moderate complexity)

**Weak SMB HRIS Integration**:
- **Planful**: ❌ No Rippling integration (cost them forum post deal)
- **Anaplan**: Via API only
- **OneStream**: Enterprise HRIS only (Workday, Oracle)

**Strong Enterprise HRIS Integration**:
- **Adaptive Insights**: Native Workday HCM
- **Anaplan**: Workday, Oracle HCM, SAP SuccessFactors

**Insight**: Mid-market buyers (50-500 employees) using modern HRIS (Rippling, Gusto) are locked into Runway/Causal due to integration gap at enterprise platforms.

### ERP Integration Patterns

**NetSuite Leaders**:
- **Planful**: 600+ NetSuite customers (strongest pairing)
- **OneStream**: NetSuite support
- **Adaptive**: NetSuite native

**SAP/Oracle Leaders**:
- **Anaplan**: SAP/Oracle native
- **OneStream**: SAP/Oracle/PeopleSoft
- **Planful**: Oracle partnership (Oracle financials)

**SMB Accounting Leaders**:
- **Runway**: QuickBooks Online, Xero (fast setup)
- **Causal**: QuickBooks, Xero, NetSuite

### Data Warehouse Integration

**Data Warehouse Native**:
- **Causal**: Snowflake/BigQuery primary integration (built data-warehouse-first)

**Data Warehouse Supported**:
- **Runway**: Snowflake, BigQuery, Redshift (Gold tier)
- **Anaplan**: Snowflake support

**Data Warehouse Via ETL**:
- **Planful**: Requires iPaaS/ETL (not native)
- **Vena**: Custom integration
- **Prophix**: Not documented

---

## Pricing & Cost Patterns

### Transparent Pricing (Rare)

**Only 1 of 8 platforms publishes pricing**:
- **Causal**: $250/mo Launch tier (transparent)

**All others**: Custom quotes only (sales-led process)

### Estimated 3-Year TCO by Tier

| Tier | Platform | Software (3yr) | Implementation | Total 3yr |
|------|----------|----------------|----------------|-----------|
| **Tier 1** | Causal | $9K | $2K | $11K |
| **Tier 1** | Runway | $30K | $8K | $38K |
| **Tier 2** | Vena | $90K | $30K | $120K |
| **Tier 2** | Prophix | $120K | $40K | $160K |
| **Tier 2** | Adaptive | $180K | $50K | $230K |
| **Tier 3** | Planful | $300K | $150K | $450K |
| **Tier 3** | Anaplan | $450K | $200K | $650K |
| **Tier 3** | OneStream | $534K | $200K | $734K |

**Pattern**: 70x cost difference between cheapest (Causal $11K) and most expensive (OneStream $734K) over 3 years.

### Implementation Time vs Cost Trade-off

| Platform | Setup Time | Implementation Cost | Trade-off |
|----------|-----------|---------------------|-----------|
| **Runway** | 1-2 weeks | $2K-10K | Fast & cheap |
| **Causal** | 1-2 weeks | $0-5K | Fast & cheap |
| **Vena** | 1-3 months | $15K-40K | Moderate |
| **Prophix** | 2-3 months | $10K-50K | Moderate |
| **Adaptive** | 2-4 months | $20K-60K | Moderate |
| **Planful** | 3-6 months | $50K-200K | Slow & expensive |
| **Anaplan** | 4-12 months | $50K-300K | Very slow & expensive |
| **OneStream** | 4-12 months | $50K-300K | Very slow & expensive |

**Insight**: Startup platforms (Runway, Causal) achieve 12-50x faster implementation than enterprise platforms.

---

## AI Capabilities Landscape (2025)

### AI Maturity Spectrum

**Production AI** (launched 2024-2025):
- **Runway**: Ambient Intelligence (July 2024), Copilot scenario generation
- **Planful**: Plan Assistant (2025), Analyst Assistant
- **OneStream**: AI Agents (May 2025) - Finance Analyst, Operations Analyst
- **Vena**: Copilot (2025), Insights

**Predictive AI** (established):
- **Adaptive Insights**: AI/ML predictive forecasts (2020+)
- **Anaplan**: PlanIQ predictive analytics (2018+)

**No Significant AI** (yet):
- **Causal**: Flexible modeling focus, AI not emphasized
- **Prophix**: Automation focus, AI not primary differentiator

### AI Feature Patterns

**Background AI** (ambient):
- **Runway Ambient Intelligence**: Auto-explains terms, detects variances, summarizes scenarios - **no chat interface needed**

**Chat-Based AI**:
- **Planful Plan Assistant**: Natural language model building ("Increase Q2 hiring by 10 engineers")
- **OneStream AI Agents**: Natural language queries to Finance Analyst agent

**Prediction AI**:
- **Adaptive Insights**: ML forecasting accuracy improvements
- **Anaplan PlanIQ**: Predictive scenario generation

### AI Hype vs Reality Assessment

**Proven** (2+ years in production):
- Adaptive predictive AI
- Anaplan PlanIQ

**Too New to Evaluate** (<1 year):
- Runway Ambient Intelligence (July 2024)
- Planful Plan Assistant (2025)
- OneStream AI Agents (May 2025)
- Vena Copilot/Insights (2025)

**Recommendation**: Don't overpay for AI today. Features will be table stakes by 2027-2028. Evaluate platforms on core capabilities (planning, consolidation, integrations) not AI hype.

---

## Vendor Viability & Acquisition Risk

### Ownership Patterns

**Public Companies** (lowest risk):
- **OneStream**: Public (IPO July 2024, $4.38B valuation)
- **Adaptive Insights**: Owned by Workday (public)

**Private Equity Owned** (low risk, stable):
- **Planful**: Marlin Equity Partners (2021)
- **Anaplan**: Thoma Bravo (2022, $10.4B acquisition)
- **Prophix**: Private (38 years old, mature)

**VC-Backed** (medium risk):
- **Runway**: a16z-backed ($33.5M raised, 20x revenue growth)
- **Vena**: K1 Investment Management

**Recently Acquired** (low risk post-acquisition):
- **Causal**: Acquired by LucaNet (October 2024)

### 5-Year Acquisition Predictions

**High Acquisition Probability** (60%+):
- **Runway**: Likely acquirer = Intuit, Rippling, Workday (2027-2029)
- **Vena**: Likely acquirer = Microsoft, Intuit (Excel positioning attractive)

**Medium Acquisition Probability** (30-50%):
- **Planful**: Possible acquirer = Oracle, SAP, Workday

**Low Acquisition Probability** (<20%):
- **OneStream**: Just went public (2024), unlikely re-acquisition for 5+ years
- **Adaptive**: Already owned by Workday
- **Anaplan**: Recently acquired by Thoma Bravo (2022), 3-5 year hold
- **Prophix**: 38 years independent, stable private company

---

## Key Research Gaps for S2-S4

### S2 Comprehensive (Next Phase)

**Feature Matrix Needed**:
- Detailed comparison: Workforce planning capabilities across all 8 platforms
- Consolidation feature depth (Planful vs Anaplan vs OneStream)
- Workflow automation comparison (approval routing, audit trails)
- AI capabilities detailed breakdown (hype vs substance)

**Integration Deep Dive**:
- HRIS integration quality matrix (Rippling, Gusto, BambooHR, Workday, ADP, Oracle)
- ERP integration complexity (NetSuite, Oracle, SAP, Microsoft Dynamics)
- Data warehouse integration architecture (Snowflake, BigQuery)

**TCO Detailed Analysis**:
- Per-module pricing breakdowns
- User license types and costs
- Hidden costs (training, ongoing consulting, support tiers)
- Migration costs (switching from one platform to another)

### S3 Need-Driven (Scenario Mapping)

**Scenarios to map** (generic, not client-specific):
- Tech startup (50 employees, Rippling, need fast setup)
- SaaS scale-up (200 employees, Snowflake data warehouse, technical finance team)
- Manufacturing mid-market (500 employees, NetSuite, multi-entity consolidation)
- Enterprise migration (2000 employees, leaving Oracle HCM, need cost reduction)
- Private equity portfolio (10+ entities, need consolidation + sub-consolidation)

### S4 Strategic (Frameworks)

**Graduation Triggers**:
- Excel → FP&A platform (when? 50 employees? 100 tabs? $10M revenue?)
- Cash flow tools (3.004) → FP&A platform (headcount planning need? consolidation?)
- Tier 1 → Tier 2 → Tier 3 (employee count thresholds, feature complexity)

**Build vs Buy Analysis**:
- When does custom FP&A system make sense? (almost never?)
- DIY cost vs platform cost breakeven analysis
- Data warehouse-native modeling (dbt + Snowflake) vs FP&A platform

**AI Evolution Outlook** (2025-2030):
- Which AI features will commoditize? (variance explanations, scenario generation)
- Which will remain differentiators? (predictive accuracy, workflow automation)
- Custom LLM opportunities (train on company-specific financial policies)

---

## Critical Findings from S1

### Finding #1: HRIS Integration Quality is Deal-Breaker

**Evidence**: Forum post - Planful lost deal to Runway due to **no direct Rippling integration**

**Implication**: Mid-market buyers (50-500 employees) using modern HRIS (Rippling, Gusto, BambooHR) cannot choose enterprise platforms (Planful, Anaplan) due to integration gap.

**Market Impact**: Runway/Causal capture SMB market due to HRIS integration strength. Enterprise platforms (Planful, Anaplan, OneStream) compete only for companies using enterprise HRIS (Workday, Oracle, ADP).

### Finding #2: 70x Price Variance Across Market

**Evidence**: Causal ($11K 3-year TCO) vs OneStream ($734K 3-year TCO)

**Implication**: Platform selection must match company budget, not just features.

**Reality Check**:
- Startups (<100 employees) priced out of enterprise platforms
- Enterprises (2000+ employees) should not use startup platforms (lack consolidation)

### Finding #3: Implementation Time = Hidden Cost

**Evidence**: Runway (1-2 weeks) vs Anaplan (4-12 months)

**Implication**:
- Time-to-value matters: Board needs budget in 30 days? Only Runway/Causal viable.
- Opportunity cost: 6-month Planful implementation = 6 months of manual Excel work

### Finding #4: AI Features Too New to Evaluate

**Evidence**:
- Runway Ambient Intelligence (July 2024)
- Planful Plan Assistant (2025)
- OneStream AI Agents (May 2025)

**Implication**:
- Don't pay premium for AI features (<1 year old)
- Wait 12-24 months for customer feedback before trusting AI ROI claims
- AI will be table stakes by 2027 (don't overpay today)

### Finding #5: Data Warehouse Integration Emerging

**Evidence**:
- Causal built data-warehouse-first (Snowflake/BigQuery)
- Runway supports data warehouses (Gold tier)
- Enterprise platforms require ETL (not native)

**Implication**:
- Companies with Snowflake/BigQuery increasingly want FP&A platform to connect directly
- Technical finance teams prefer SQL-based modeling
- Trend: FP&A platforms will add data warehouse support (2025-2027)

---

## S1 Completeness Assessment

**✅ Completed**:
- 8 platform profiles (2 full depth, 6 reduced depth)
- Company overview, funding, market position
- Core modules and capabilities
- Target market and pricing
- Key differentiators
- Integration capabilities
- Strengths and limitations
- Competitive positioning

**⏭️ Deferred to S2**:
- Feature-by-feature comparison matrix
- Detailed pricing breakdowns (user licenses, add-on modules)
- Implementation complexity analysis
- AI capabilities detailed evaluation
- Integration architecture diagrams

**⏭️ Deferred to S3**:
- Scenario-based platform recommendations
- Company size/tech stack matching
- Migration paths between platforms

**⏭️ Deferred to S4**:
- Vendor viability deep dive (financial health, acquisition analysis)
- Graduation triggers framework
- Build vs buy decision tree
- 2030 AI evolution predictions

---

## Document Status

**Created**: November 1, 2025
**Purpose**: Synthesize S1 rapid discovery findings
**Scope**: 8 FP&A platforms across 3 market tiers
**Key Insight**: HRIS integration quality (specifically Rippling support) determined forum post platform selection (Runway won, Planful lost)
**Next Phase**: S2 Comprehensive Analysis (feature matrices, detailed TCO, integration deep dive)
