# S3 Need-Driven Discovery - Synthesis

**Experiment**: 3.007 FP&A Platforms
**Stage**: S3 - Need-Driven Discovery
**Date**: November 1, 2025
**Document Type**: Cross-Scenario Patterns & Methodology

---

## Overview

This document synthesizes patterns from 5 generic scenarios (tech startup, SaaS scale-up, manufacturing mid-market, enterprise migration, PE portfolio consolidation) to demonstrate HOW to apply the S1/S2 FP&A platform catalog to ANY business context.

**Hardware Store Principle**: S3 scenarios show catalog application methodology, NOT prescriptive "choose Platform X" recommendations. Like a hardware store, we show which tools match requirements, but customers choose based on their specific needs.

---

## Cross-Scenario Patterns

### Pattern 1: Integration Requirements as Primary Filter

**Observation**: Integration requirements eliminate 50-75% of platforms immediately.

**Evidence from 5 Scenarios**:

1. **Tech Startup (50 employees)**: Rippling HRIS integration → only Runway matches (7/8 platforms eliminated)
2. **SaaS Scale-Up (200 employees)**: Snowflake data warehouse → Causal, Anaplan, OneStream, Runway match (4/8 remain)
3. **Manufacturing (500 employees)**: Multi-entity consolidation → excludes Runway, Causal (6/8 remain)
4. **Enterprise Migration (2,000 employees)**: Oracle Financials → excludes Runway, Causal (6/8 remain)
5. **PE Portfolio (10 companies)**: Multi-ERP (7 systems) → Prophix best (5/6 native), Vena good (4/6 native)

**Key Insight**: Integration requirements are BINARY filters (platform either integrates or doesn't), making them the most efficient first filter.

**Application Methodology**:
```
Step 1: List ALL systems of record
  - ERP (NetSuite, QBO, SAP, Oracle, Dynamics, Sage, Xero)
  - HRIS (Workday, Rippling, Gusto, ADP, BambooHR, Paycom)
  - CRM (Salesforce, HubSpot, Pipedrive)
  - Data Warehouse (Snowflake, BigQuery, Redshift)

Step 2: Cross-reference S2 Integration Matrix
  - Native integrations (✅): 1-2 day setup
  - API integrations (⚠️): 1-2 week setup
  - iPaaS required (🔧): 2-4 week setup, $10K-50K/year cost
  - Not supported (❌): Platform eliminated

Step 3: Calculate integration setup time + cost
  - Native: 2-5 days × number of systems
  - API: 1-2 weeks × number of systems
  - iPaaS: Add $20K-100K to 3-year TCO

Step 4: Eliminate platforms with missing critical integrations
  - Critical integration = daily/weekly data sync required
  - Nice-to-have integration = manual export acceptable
```

---

### Pattern 2: Budget Constraints as Secondary Filter

**Observation**: Budget eliminates another 40-60% of remaining platforms after integration filtering.

**Evidence from 5 Scenarios**:

| Scenario | Budget Range | Platforms Meeting Budget | Platforms Eliminated |
|----------|--------------|-------------------------|---------------------|
| Tech Startup (50) | $5K-30K/year | Runway, Causal (2/8) | Vena, Prophix, Planful, Adaptive, OneStream, Anaplan (6/8) |
| SaaS Scale-Up (200) | $25K-80K/year | Runway, Causal, Vena (3/8) | Prophix+, Planful, Adaptive, OneStream, Anaplan (5/8) |
| Manufacturing (500) | $50K-150K/year | Vena, Prophix, Planful (3/8) | Adaptive, OneStream, Anaplan (3/8) |
| Enterprise (2,000) | $100K-350K/year (cost reduction) | Vena, Prophix (2/8) | Planful, Adaptive, OneStream, Anaplan (4/8) |
| PE Portfolio (10 co's) | $150K-300K/year | Vena, Prophix (2/8) | Planful, Adaptive, OneStream, Anaplan (4/8) |

**Key Insight**: Budget is CONTINUOUS filter (platforms fall along cost spectrum), with clear price tiers:
- **Tier 1 (Startup)**: $5K-30K/year (Runway, Causal)
- **Tier 2 (Growth)**: $30K-100K/year (Vena, Prophix)
- **Tier 3 (Enterprise)**: $100K-500K/year (Planful, Adaptive, OneStream, Anaplan)

**Application Methodology**:
```
Step 1: Define 3-year TCO budget (not annual software cost)
  - Software subscription (primary cost)
  - Implementation (one-time, often 10-50% of Year 1 software)
  - Integration costs (iPaaS, custom API, data warehouse)
  - Training (often underestimated, $5K-50K over 3 years)
  - Ongoing consulting (enterprise platforms often require $20K-100K/year)

Step 2: Cross-reference S2 Pricing Analysis for employee count
  - Startup (50): Use "Startup 50" scenario pricing
  - Mid-market (500): Use "Mid-Market 500" scenario pricing
  - Enterprise (2,000): Use "Enterprise 2,000" scenario pricing
  - Adjust for complexity multipliers:
    - Multi-entity (+20-40%)
    - Multi-GAAP (+10-30%)
    - Complex integrations (+10-50%)

Step 3: Apply hidden cost catalog (from S2 Pricing doc)
  - iPaaS tools: $10K-50K/year
  - Custom API development: $10K-30K one-time
  - Data warehouse: $2K-20K/year
  - Ongoing consulting: $0-100K/year (enterprise platforms)

Step 4: Eliminate platforms >20% over budget
  - Slight overage (10-20%): Negotiate or consider
  - Significant overage (>20%): Eliminate (too expensive)
```

---

### Pattern 3: Implementation Timeline as Tertiary Filter

**Observation**: Implementation timeline eliminates another 20-40% of remaining platforms after integration + budget filtering.

**Evidence from 5 Scenarios**:

| Scenario | Timeline Requirement | Platforms Meeting Timeline | Platforms Eliminated |
|----------|---------------------|---------------------------|---------------------|
| Tech Startup (50) | 2-4 weeks | Runway, Causal (2/8) | All others (6/8) |
| SaaS Scale-Up (200) | 4-8 weeks | Runway, Causal, Vena (3/8) | Prophix, Planful, Adaptive, OneStream, Anaplan (5/8) |
| Manufacturing (500) | 8-16 weeks | Vena, Prophix (2/8) | Planful, Adaptive, OneStream, Anaplan (4/8) |
| Enterprise (2,000) | 4-6 months | Vena, Prophix (2/8) | Planful, Adaptive, OneStream, Anaplan (4/8) |
| PE Portfolio (10 co's) | 3-6 months | Vena, Prophix (2/8) | Planful, Adaptive, OneStream, Anaplan (4/8) |

**Key Insight**: Implementation timeline roughly correlates with platform complexity:
- **Startup platforms** (Runway, Causal): 1-2 weeks (self-service)
- **Mid-market platforms** (Vena, Prophix): 4-12 weeks (guided setup)
- **Enterprise platforms** (Planful, Adaptive): 3-6 months (professional services)
- **Complex enterprise** (OneStream, Anaplan): 6-18 months (Big 4 consulting)

**Application Methodology**:
```
Step 1: Identify business constraint driving timeline
  - Board meeting deadline (common: 4-8 weeks)
  - Budget cycle start (common: 3-6 months)
  - Fiscal year-end close (common: 6-12 months)
  - Legacy platform EOL (varies)

Step 2: Add buffer time (25-50% padding)
  - Optimistic timeline: S2 Implementation "Minimum" column
  - Realistic timeline: S2 Implementation "Typical" column
  - Conservative timeline: S2 Implementation "Maximum" column
  - Add complexity multipliers:
    - Legacy migration (Hyperion, SAP BPC): +2-4 months
    - Multi-entity (>5 entities): +1-3 months
    - Custom integrations (>3 systems): +1-2 months

Step 3: Cross-reference S2 Implementation Complexity Matrix
  - Self-service platforms: 1-4 weeks (Runway, Causal)
  - Guided setup: 4-16 weeks (Vena, Prophix)
  - Professional services: 12-24 weeks (Planful, Adaptive)
  - Implementation partner: 16-48 weeks (OneStream, Anaplan)

Step 4: Eliminate platforms exceeding timeline by >25%
  - Example: 8-week timeline → eliminate platforms >10 weeks
```

---

### Pattern 4: Feature Requirements as Final Filter

**Observation**: After integration + budget + timeline filtering, 2-4 platforms typically remain. Feature requirements differentiate final choice.

**Evidence from 5 Scenarios**:

| Scenario | Finalists (Post-Budget/Timeline) | Feature Differentiators | Winner |
|----------|----------------------------------|------------------------|---------|
| Tech Startup (50) | Runway vs Causal | Rippling HRIS integration (Runway yes, Causal no) | Runway |
| SaaS Scale-Up (200) | Causal vs Runway vs Vena | Snowflake native + SQL modeling (Causal yes, Runway good, Vena no) | Causal |
| Manufacturing (500) | Vena vs Prophix | Driver-based automation (Prophix best, Vena good) | Prophix |
| Enterprise (2,000) | Vena vs Prophix | Modern web UX (Prophix yes, Vena Excel-native) | Prophix |
| PE Portfolio (10 co's) | Vena vs Prophix | Multi-ERP native integrations (Prophix 5/6, Vena 4/6) | Prophix |

**Key Insight**: Feature requirements are QUALITATIVE differentiators (not binary). Requires trade-off analysis.

**Application Methodology**:
```
Step 1: Categorize features by criticality
  - Must-have: Platform eliminated without this feature
  - Should-have: Significant value, willing to pay 10-20% premium
  - Nice-to-have: Marginal value, not worth premium

Step 2: Cross-reference S2 Feature Matrix
  - Full support (✅): Production-ready, documented
  - Partial support (⚠️): Limited, beta, or workarounds
  - Not supported (❌): Feature unavailable

Step 3: Build feature comparison matrix (finalists only)
  - List must-have features (eliminate platforms missing these)
  - List should-have features (calculate value premium justified)
  - List nice-to-have features (tiebreaker only)

Step 4: Quantify trade-offs (feature value vs price premium)
  - Example (Manufacturing scenario):
    - Prophix driver-based automation value: $63K-126K over 3 years
    - Prophix price premium vs Vena: $95K over 3 years
    - ROI: Automation value justifies premium (7-33% return)
```

---

## Catalog Application Methodology (Step-by-Step)

**Universal 5-Step Process** (applies to ANY scenario):

### Step 1: Document Business Context

**Critical Inputs**:
- Company size (employees, revenue)
- Growth stage (startup, scale-up, mid-market, enterprise)
- Industry (SaaS, manufacturing, services, etc.)
- Structure (single entity, multi-entity, complex ownership)
- Tech stack (ERP, HRIS, CRM, data warehouse, BI tools)

**Output**: Scenario profile (generic, not client-specific)

---

### Step 2: Extract Requirements from Context

**Requirements Hierarchy**:
1. **Integration requirements** (primary filter)
   - Which systems must integrate? (ERP, HRIS, CRM, data warehouse)
   - Sync frequency? (real-time, daily, weekly, monthly)
   - Historical data? (1 year, 3 years, 5+ years)

2. **Budget constraints** (secondary filter)
   - Annual budget range? ($5K-30K, $30K-100K, $100K-500K, $500K+)
   - 3-year TCO target? (multiply annual × 3, add implementation 20-50%)
   - Hidden costs acceptable? (iPaaS, consulting, training)

3. **Timeline constraints** (tertiary filter)
   - Business deadline? (board meeting, budget cycle, fiscal year-end)
   - Resource availability? (finance team bandwidth, IT support)
   - Risk tolerance? (self-service vs guided setup vs professional services)

4. **Feature requirements** (final filter)
   - Must-have features? (consolidation, multi-currency, driver-based planning)
   - Should-have features? (mobile access, real-time collaboration, AI)
   - Nice-to-have features? (tiebreakers)

**Output**: Prioritized requirements list (must-have, should-have, nice-to-have)

---

### Step 3: Apply Integration Filter (S2 Integration Matrix)

**Process**:
1. List all systems requiring integration (ERP, HRIS, CRM, data warehouse)
2. Cross-reference S2 Integration Deep Dive document:
   - HRIS matrix (line 31-42): 8 platforms × 10 HRIS systems
   - ERP matrix (line 69-79): 8 platforms × 8 ERP systems
   - Data warehouse matrix (line 109-115): 8 platforms × 5 warehouses
   - CRM matrix (line 133-140): 8 platforms × 4 CRM systems

3. Score platforms by integration coverage:
   - Native (✅): 3 points
   - API (⚠️): 2 points
   - iPaaS (🔧): 1 point
   - None (❌): 0 points (eliminate if critical integration)

4. Calculate total integration score: Sum across all required systems
5. Eliminate platforms with missing critical integrations

**Output**: 2-6 platforms remaining (50-75% eliminated)

---

### Step 4: Apply Budget Filter (S2 Pricing Analysis)

**Process**:
1. Select pricing scenario from S2 matching company size:
   - Startup (50 employees): S2 Pricing line 310-334
   - Mid-market (500 employees): S2 Pricing line 336-362
   - Enterprise (2,000 employees): S2 Pricing line 364-389

2. Adjust for complexity multipliers:
   - Multi-entity (>3 entities): +20-40% software cost
   - Multi-GAAP: +10-30% software cost
   - Complex integrations (>5 systems): +10-50% implementation cost

3. Add hidden costs (S2 Pricing line 483-587):
   - Implementation: 10-50% of Year 1 software cost
   - iPaaS tools: $10K-50K/year (if needed)
   - Custom API: $10K-30K one-time
   - Data warehouse: $2K-20K/year
   - Training: $5K-50K over 3 years
   - Ongoing consulting: $0-100K/year (enterprise platforms)

4. Calculate 3-year TCO for each remaining platform
5. Eliminate platforms >20% over budget (negotiate 10-20% overage)

**Output**: 1-4 platforms remaining (40-60% eliminated)

---

### Step 5: Apply Timeline Filter (S2 Implementation Complexity)

**Process**:
1. Define business timeline constraint (weeks or months)
2. Cross-reference S2 Implementation Complexity Matrix:
   - Self-service platforms: 1-4 weeks (line 35-36: Runway, Causal)
   - Guided setup: 4-16 weeks (line 37-38: Vena, Prophix)
   - Professional services: 12-24 weeks (line 39-40: Planful, Adaptive)
   - Implementation partner: 16-48 weeks (line 41-42: OneStream, Anaplan)

3. Add complexity buffers:
   - Legacy migration (Hyperion, SAP BPC): +2-4 months
   - Multi-entity (>5 entities): +1-3 months
   - Custom integrations (>3 systems): +1-2 months
   - Data cleansing: +2-8 weeks (often underestimated)

4. Apply 25-50% buffer to S2 "Typical" timeline (reality: implementations often delayed)
5. Eliminate platforms exceeding timeline by >25%

**Output**: 1-3 platforms remaining (20-40% eliminated)

---

### Step 6: Compare Feature Trade-offs (S2 Feature Matrix)

**Process**:
1. For remaining 1-3 platforms, build feature comparison matrix
2. Cross-reference S2 Feature Matrix categories:
   - Workforce planning (line 30-45)
   - Financial consolidation (line 54-69)
   - Planning capabilities (line 78-95)
   - Reporting & analytics (line 104-119)
   - Workflow & collaboration (line 129-143)
   - Scenario modeling (line 153-166)
   - AI & automation (line 176-189)
   - Capital planning (line 200-209)

3. Score each platform on must-have features:
   - Full support (✅): 3 points
   - Partial support (⚠️): 1 point
   - Not supported (❌): 0 points (eliminate if must-have)

4. Calculate feature coverage score: Sum across must-have features
5. Identify should-have feature gaps (quantify value if available)

**Output**: 1-2 platform finalists with quantified trade-offs

---

### Step 7: Quantify Trade-offs (Final Decision)

**Process**:
1. For 1-2 finalists, calculate:
   - **Price premium**: Difference in 3-year TCO between finalists
   - **Feature value**: Quantify time savings or capabilities of premium features
   - **ROI**: Feature value ÷ price premium (justify if ROI >0%)

2. Build trade-off matrix:
   ```
   Platform A vs Platform B: $X difference over 3 years

   Platform A Advantages (worth $X premium?):
   - Feature 1 value: $Y (time savings × hourly rate)
   - Feature 2 value: $Z (avoid future migration cost)
   - Total value: $Y + $Z

   Platform B Advantages (worth $X savings?):
   - Budget savings: $X
   - Faster implementation: $W (time-to-value)
   - Total value: $X + $W

   Key Question: Which advantage more critical for this scenario?
   ```

3. Present objective trade-off (not prescriptive choice):
   - "Choose Platform A if [feature advantage] critical"
   - "Choose Platform B if [budget/timeline constraint] priority"
   - "Key question: Is [feature pain point] worth $X premium?"

**Output**: Objective trade-off analysis (hardware store model: show options, don't prescribe)

---

## Cross-Scenario Learnings

### Learning 1: Integration Drives 70% of Platform Elimination

**Pattern**: Across all 5 scenarios, integration requirements eliminated 50-75% of platforms before considering budget, timeline, or features.

**Implication**: Always start with integration mapping. No point evaluating features if platform can't integrate with existing tech stack.

**Exception**: Greenfield implementations (new company, no existing systems). In this case, budget becomes primary filter.

---

### Learning 2: Budget Tiers Naturally Cluster Platforms

**Pattern**: Platforms fall into clear price tiers:
- **Tier 1 (Startup)**: Runway, Causal ($5K-30K/year)
- **Tier 2 (Growth/Mid-Market)**: Vena, Prophix ($30K-150K/year)
- **Tier 3 (Enterprise)**: Planful, Adaptive, OneStream, Anaplan ($150K-1M+/year)

**Implication**: Budget constraint narrows choice to 2-4 platforms within same tier. Rarely compare across tiers (e.g., Runway vs Anaplan) because use cases non-overlapping.

**Exception**: Enterprise migration seeking cost reduction (e.g., Hyperion → Prophix). Here, Tier 2 platform replaces Tier 3 incumbent.

---

### Learning 3: Implementation Timeline Often Underestimated

**Pattern**: S2 "Typical" implementation timelines often 25-50% longer in reality due to:
- Data cleansing (fix GL errors before migration)
- Resource constraints (finance team bandwidth)
- Parallel runs (validate new platform before cutover)
- Change management (user adoption takes longer than training)

**Implication**: Always add 25-50% buffer to S2 "Typical" timeline. Use "Maximum" column for conservative planning.

**Exception**: Greenfield implementations (no legacy migration, clean data). Here, S2 "Minimum" timeline achievable.

---

### Learning 4: Feature Trade-offs Require Quantification

**Pattern**: Final platform choice (between 1-2 finalists) requires quantifying feature value vs price premium. All 5 scenarios demonstrated this:
- Tech Startup: Rippling automation value ($10.8K-21.6K) vs Runway premium ($10K)
- SaaS Scale-Up: Snowflake integration time savings ($144K-216K) vs Causal savings ($17K)
- Manufacturing: Prophix automation value ($63K-126K) vs price premium ($95K)
- Enterprise: Prophix web UX value ($348K-456K) vs price premium ($290K)
- PE Portfolio: Prophix onboarding + ERP automation ($266K) vs price premium ($300K)

**Implication**: Cannot make informed choice without quantifying trade-offs. "Better features" must translate to $ value (time savings, avoid future costs).

**Exception**: Strategic priorities override ROI (e.g., "must escape Oracle lock-in" regardless of cost).

---

### Learning 5: No Single "Best" Platform Across Scenarios

**Pattern**: Different platforms won across 5 scenarios:
- Tech Startup (50): Runway
- SaaS Scale-Up (200): Causal
- Manufacturing (500): Prophix
- Enterprise (2,000): Prophix (cost reduction) or Planful (feature-first)
- PE Portfolio (10 co's): Prophix

**Implication**: "Best platform" depends entirely on context (company size, tech stack, budget, timeline, features). S3 demonstrates HOW to apply catalog, not WHAT to choose universally.

**Insight**: This validates hardware store model. No single tool right for all jobs. Show customers which tools match their requirements, let them choose based on priorities.

---

## Catalog Application Patterns by Company Stage

### Startup Stage (50-200 Employees)

**Typical Requirements**:
- Integration: SMB HRIS (Rippling, Gusto, BambooHR), SMB accounting (QBO, Xero)
- Budget: $5K-30K/year (capital-efficient)
- Timeline: 2-4 weeks (fast time-to-value)
- Features: Headcount planning, cash runway, scenario modeling

**Typical Finalists**: Runway, Causal
**Primary Differentiator**: HRIS integration (Runway native, Causal manual)

**Application Example**: Tech Startup scenario (lines 1-300, tech-startup-50-employees.md)

---

### Growth/Scale-Up Stage (200-500 Employees)

**Typical Requirements**:
- Integration: Enterprise ERP (NetSuite, Sage Intacct), data warehouse (Snowflake)
- Budget: $25K-100K/year (growth-stage investment)
- Timeline: 4-12 weeks (balance speed + functionality)
- Features: Data warehouse integration, flexible modeling, SaaS metrics

**Typical Finalists**: Causal, Runway, Vena
**Primary Differentiator**: Data warehouse native (Causal yes, Runway yes, Vena no)

**Application Example**: SaaS Scale-Up scenario (lines 1-300, saas-scaleup-200-employees.md)

---

### Mid-Market Stage (500-2,000 Employees)

**Typical Requirements**:
- Integration: Enterprise ERP (NetSuite, Dynamics, SAP), enterprise HRIS (Workday, ADP)
- Budget: $50K-300K/year (mature finance budget)
- Timeline: 8-16 weeks (guided setup acceptable)
- Features: Multi-entity consolidation, driver-based planning, audit reporting

**Typical Finalists**: Vena, Prophix, Planful
**Primary Differentiator**: Consolidation complexity (Prophix best, Vena good, Planful enterprise-grade)

**Application Example**: Manufacturing scenario (lines 1-300, manufacturing-500-employees.md)

---

### Enterprise Stage (2,000+ Employees)

**Typical Requirements**:
- Integration: Enterprise ERP (Oracle, SAP), complex systems landscape
- Budget: $150K-1M+/year (enterprise IT budget)
- Timeline: 3-12 months (professional services expected)
- Features: Complex consolidation, multi-GAAP, regulatory reporting, scalability

**Typical Finalists**: Prophix, Planful, Adaptive, OneStream, Anaplan
**Primary Differentiator**: Use case (consolidation vs connected planning vs unified CPM)

**Application Example**: Enterprise Migration scenario (lines 1-300, enterprise-migration-2000-employees.md)

---

### Special Case: PE Portfolio Consolidation

**Typical Requirements**:
- Integration: Multi-ERP (heterogeneous landscape), sub-consolidation
- Budget: $150K-300K/year (centralized PE budget)
- Timeline: 3-6 months (phased rollout)
- Features: Complex ownership, minority interest, rapid new company onboarding

**Typical Finalists**: Prophix, Vena
**Primary Differentiator**: Multi-ERP native coverage (Prophix 5/6, Vena 4/6)

**Application Example**: PE Portfolio scenario (lines 1-300, pe-portfolio-consolidation.md)

---

## Common Pitfalls in Catalog Application

### Pitfall 1: Skipping Integration Analysis

**Error**: Starting with features or budget before mapping integrations.

**Consequence**: Shortlist platforms that can't integrate with existing tech stack (wasted evaluation time).

**Correction**: ALWAYS start with S2 Integration Matrix. Map all systems requiring integration, eliminate platforms with missing critical connectors.

**Example**: Tech Startup scenario evaluated Planful (strong features, within budget) but eliminated due to no Rippling integration.

---

### Pitfall 2: Underestimating Hidden Costs

**Error**: Comparing only annual software subscription costs (ignoring implementation, iPaaS, training, consulting).

**Consequence**: $50K/year platform becomes $150K/year after hidden costs (budget blown).

**Correction**: Always calculate 3-year TCO using S2 Pricing hidden costs catalog (lines 483-587):
- Implementation: 10-50% of Year 1 software
- iPaaS: $10K-50K/year (if needed)
- Training: $5K-50K over 3 years
- Consulting: $0-100K/year (enterprise platforms)

**Example**: PE Portfolio scenario Planful ($1.59M software) + iPaaS ($300K) = $1.89M total (89% over budget vs 59% software-only).

---

### Pitfall 3: Using Optimistic Implementation Timelines

**Error**: Planning for S2 "Minimum" implementation timeline without buffer.

**Consequence**: Miss business deadline (e.g., budget cycle, fiscal year-end), disrupt planning process.

**Correction**: Use S2 "Typical" timeline + 25-50% buffer. Add complexity multipliers:
- Legacy migration: +2-4 months
- Multi-entity: +1-3 months
- Data cleansing: +2-8 weeks

**Example**: Enterprise Migration scenario added 2-3 months for Hyperion migration complexity (Prophix 6-12 weeks baseline → 5-7 months total).

---

### Pitfall 4: Comparing Platforms Across Non-Overlapping Use Cases

**Error**: Comparing Runway (startup, 50 employees) to Anaplan (enterprise, 5,000+ employees) for 200-employee company.

**Consequence**: False choice (both inappropriate for use case, but for different reasons).

**Correction**: Filter by budget + integration + timeline FIRST, then compare within shortlist. Don't evaluate every platform for every scenario.

**Example**: SaaS Scale-Up scenario eliminated Runway (may not scale to 500+) and Anaplan (2.5x over budget) before comparing Causal vs Vena.

---

### Pitfall 5: Ignoring Qualitative Trade-offs

**Error**: Choosing lowest-cost platform without quantifying feature value lost.

**Consequence**: Save $100K upfront, spend $200K manual labor over 3 years (false economy).

**Correction**: Always quantify feature trade-offs (time savings, avoid future costs). Calculate ROI for premium features.

**Example**: Manufacturing scenario Vena ($250K) vs Prophix ($345K). Prophix automation value ($63K-126K) justified $95K premium.

---

## Synthesis Summary

### Key Takeaways

1. **Integration is primary filter** (eliminates 50-75% of platforms immediately)
2. **Budget is secondary filter** (narrows to 2-4 platforms within same tier)
3. **Timeline is tertiary filter** (eliminates slow implementations)
4. **Features differentiate finalists** (requires quantified trade-off analysis)
5. **No universal "best" platform** (depends on company size, tech stack, budget, timeline, features)

### When to Use This Methodology

**Appropriate use cases**:
- Company evaluating FP&A platform purchase (internal decision)
- Consultant advising client on FP&A platform selection (billable engagement)
- PE firm evaluating portfolio-wide FP&A tool (centralized decision)
- Finance leader researching options (pre-RFP phase)

**Inappropriate use cases**:
- Vendor sales (use vendor-specific pitch, not objective catalog)
- Academic research (S3 is practitioner-focused, not peer-reviewed)
- Marketing content (S3 is technical analysis, not promotional)

---

### How to Apply to New Scenarios

**Step-by-Step Process**:
1. Document company context (size, stage, industry, tech stack)
2. Extract requirements (integration, budget, timeline, features)
3. Apply integration filter (S2 Integration Matrix) → eliminate 50-75%
4. Apply budget filter (S2 Pricing Analysis) → eliminate 40-60%
5. Apply timeline filter (S2 Implementation Complexity) → eliminate 20-40%
6. Compare feature trade-offs (S2 Feature Matrix) → 1-2 finalists
7. Quantify trade-offs (time savings, avoid future costs) → objective choice

**Output**: 1-2 platform finalists with quantified trade-offs (hardware store model: show options, don't prescribe).

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 250+
**Purpose**: Cross-scenario pattern synthesis + catalog application methodology
**Approach**: Hardware store model (show HOW to apply catalog, not WHAT to choose)

**Key Contribution**: Universal 7-step methodology for applying S1/S2 catalog to ANY business scenario (startup to enterprise, simple to complex).

**Limitations**:
- Methodology assumes S1/S2 catalog up-to-date (requires quarterly refresh)
- Quantified trade-offs use estimated time savings (actual savings vary by company)
- Integration matrix may have gaps (new ERPs, HRIS, data warehouses emerge)
- Pricing estimates may vary 20-50% (vendor negotiations, discounts, promotions)

**Next Steps (S4 Strategic)**:
- Graduation frameworks (when to move between tiers: Runway → Vena → Planful)
- Vendor viability analysis (acquisition risk, product roadmap, market position)
- Build-vs-buy economics (when to build custom FP&A tool vs buy platform)
