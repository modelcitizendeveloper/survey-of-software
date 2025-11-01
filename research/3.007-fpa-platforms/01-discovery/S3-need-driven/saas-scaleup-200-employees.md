# S3 Scenario: SaaS Scale-Up (200 Employees)

**Experiment**: 3.007 FP&A Platforms
**Stage**: S3 - Need-Driven Discovery
**Date**: November 1, 2025
**Scenario Type**: Generic Profile (not client-specific)

---

## Scenario Context

**Company Profile**:
- Stage: Series B-C SaaS company
- Employee count: 200 (current), projecting 280 by Year 3
- Revenue: $25M ARR (current), targeting $60M ARR in 24 months
- Funding: $40M Series C raised, growth-stage scaling
- Growth rate: 40% YoY revenue growth, 25% headcount growth
- Business model: B2B SaaS, annual contracts with monthly billing

**Finance Team**:
- CFO: Full-time (Series A hire, 3 years tenure)
- VP Finance: 1 FTE (reporting, analysis, board prep)
- Finance Analysts: 2 FTEs (FP&A, budgeting, forecasting)
- Accounting team: 3 FTEs (separate from FP&A)
- Current tools: Excel + Looker dashboards (semi-automated)

**Technical Environment**:
- Data Warehouse: Snowflake (2 years old, central data platform)
- ERP: NetSuite (18 months old, migrated from QBO)
- HRIS: Gusto (200 employees, 4 years old)
- CRM: Salesforce (sales pipeline, customer data)
- BI Tool: Looker (dashboards for product, sales, finance)

**Pain Points**:
- Excel still source of truth (Looker for actuals, Excel for planning)
- SaaS metrics complex (cohort analysis, NDR, LTV:CAC requires manual SQL)
- Data warehouse integration missing (finance pulls Snowflake data manually)
- Quarterly board decks take 1-2 weeks to prepare (cross-functional data)
- NetSuite integration manual (daily CSV exports, reconciliation errors)

---

## Requirements Analysis

### Primary Requirements

**1. Snowflake Data Warehouse Integration**
- Critical need: Pull product usage metrics (DAU, feature adoption, engagement)
- Current process: Finance analyst writes SQL queries, exports CSVs, imports to Excel
- Desired state: Direct Snowflake connection for unit economics (CAC, LTV, payback)
- Impact: Eliminate 10-15 hours/week manual data pipeline work

**2. Flexible Modeling for SaaS Metrics**
- Metrics needed: ARR, net revenue retention (NRR), gross revenue retention (GRR), cohort analysis
- Constraint: Cannot use pre-defined financial templates (business model complexity)
- Technical team: Finance analysts comfortable with SQL (technical background)
- Modeling need: Custom formulas for unit economics (CAC recovery, LTV:CAC by segment)

**3. NetSuite ERP Integration**
- Historical data: 18 months in NetSuite, 3+ years in QBO legacy
- Chart of accounts: 400+ accounts (multi-department, project tracking)
- Sync frequency: Daily minimum (real-time preferred)
- Subsidiaries: Single entity now, planning 2-3 subsidiaries in 12-18 months

**4. Budget ($25K-80K/Year)**
- Series B-C budget: More flexible than startup, but cost-conscious
- Current spend: $0 for FP&A tool (Excel-based)
- 3-year TCO target: $100K-250K total (finance team can justify)
- Avoid: Enterprise pricing ($200K+/year overkill at 200 employees)

**5. 4-8 Week Implementation**
- Constraint: Q4 planning cycle starts in 8 weeks (need platform live)
- Resource availability: Finance analyst dedicated 50% time to implementation
- Technical support: Data engineer can assist Snowflake integration (20 hours)
- Acceptable: Guided setup with vendor support (not Big 4 consulting)

### Secondary Requirements

**6. Salesforce CRM Integration**
- Use case: Pipeline-based revenue forecasting (weighted pipeline close rates)
- Current gap: Manual Salesforce exports weekly (pipeline stages, close dates)
- Nice-to-have: Live pipeline sync for real-time forecast updates

**7. Scenario Planning**
- Board requirement: Quarterly forecasts with upside/downside scenarios
- Use cases: Sensitivity analysis (churn +1%, expansion +2%)
- Scenarios: 5-10 simultaneous scenarios (base + sensitivity variations)

**8. Scalability to 500+ Employees**
- Growth plan: 200 → 500 employees in 3-4 years
- Avoid: Outgrowing platform (e.g., Runway may not scale to 500+)
- Future needs: Multi-entity consolidation as international expansion begins

---

## Applying S2 Catalog Data

### Step 1: Filter by Data Warehouse Integration

**Critical Requirement: Native Snowflake Integration**

From S2 Integration Matrix (Data Warehouse Support):
- ✅ **Causal**: Native Snowflake integration (data-warehouse-native) (S2 Integrations, line 118)
- ✅ **Anaplan**: Native Snowflake via CloudWorks (S2 Integrations, line 111)
- ✅ **OneStream**: Native Snowflake connector (S2 Integrations, line 111)
- ✅ **Runway**: Native Snowflake integration (Gold-tier) (S2 Integrations, line 121)
- ⚠️ **Adaptive**: API available (requires custom development) (S2 Integrations, line 111)
- ⚠️ **Planful**: iPaaS required (Workato/Boomi) (S2 Integrations, line 111)
- ⚠️ **Prophix**: API available (not native) (S2 Integrations, line 111)
- ⚠️ **Vena**: API available (not native) (S2 Integrations, line 111)

**Result**: Causal, Anaplan, OneStream, Runway offer native Snowflake connectors.

**Integration Setup Time** (From S2):
- Causal: Direct query (SQL-based), 1-3 days setup
- Anaplan: CloudWorks connector, 3-5 days setup
- OneStream: Native connector, 3-5 days setup
- Runway: Gold-tier integration, 2-3 days setup

---

### Step 2: Filter by NetSuite ERP Integration

**Important Requirement: NetSuite Integration**

From S2 Integration Matrix (ERP Support):
- ✅ **All enterprise/mid-market platforms**: Native NetSuite integration
  - Planful: 600+ NetSuite customers, 2-3 day setup (S2 Integrations, line 243)
  - Adaptive: Native NetSuite, 3-5 day setup (S2 Integrations, line 243)
  - Prophix: Native NetSuite, 3-5 day setup (S2 Integrations, line 243)
  - Anaplan: Native NetSuite, 3-5 day setup (S2 Integrations, line 243)
  - OneStream: Native NetSuite, 3-5 day setup (S2 Integrations, line 243)
  - Vena: Native NetSuite, 3-5 day setup (S2 Integrations, line 243)
  - Runway: Native NetSuite, 2-3 day setup (S2 Integrations, line 243)
  - Causal: API available, 5-7 days setup (S2 Integrations, line 243)

**Result**: All platforms support NetSuite (table stakes for mid-market).

**Best NetSuite Integration**: Planful (600+ NetSuite customers, deepest partnership)

---

### Step 3: Filter by Budget Constraints

**Requirement: $25K-80K/Year (3-Year TCO $100K-250K)**

From S2 Pricing Analysis (200 Employees):

| Platform | Year 1 | Year 2 | Year 3 | 3-Year Total | Within Budget? |
|----------|--------|--------|--------|--------------|----------------|
| **Runway** | $25K + $5K impl | $27K | $29K | **$106K** ✅ |
| **Causal** | $20K + $3K impl | $22K | $24K | **$89K** ✅ |
| **Vena** | $55K + $20K impl | $60K | $65K | **$250K** ✅ (upper limit) |
| **Prophix** | $75K + $30K impl | $80K | $85K | **$345K** ❌ |
| **Planful** | $120K + $60K impl | $130K | $140K | **$510K** ❌ |
| **Adaptive** | $150K + $75K impl | $160K | $170K | **$630K** ❌ |
| **OneStream** | $250K + $150K impl | $270K | $290K | **$1,110K** ❌ |
| **Anaplan** | $300K + $150K impl | $320K | $340K | **$1,260K** ❌ |

**Result**: Runway ($106K), Causal ($89K), and Vena ($250K) meet budget. Prophix+ exceed budget by 40-400%.

---

### Step 4: Filter by Implementation Timeline

**Requirement: 4-8 Week Implementation**

From S2 Implementation Complexity Matrix:
- 🟢 **Runway**: 1-2 weeks typical (S2 Implementation, line 35)
- 🟢 **Causal**: 1-2 weeks typical (S2 Implementation, line 36)
- 🟡 **Vena**: 4-12 weeks (guided setup) (S2 Implementation, line 37)
- 🟡 **Prophix**: 6-12 weeks (professional services) (S2 Implementation, line 38)
- 🔴 **Others**: 8-48 weeks (too slow)

**Result**: Runway, Causal, Vena meet 4-8 week timeline.

---

### Step 5: Cross-Reference Feature Requirements

**Flexible Modeling for SaaS Metrics**:

From S2 Feature Matrix:
- **Causal**: Human-readable formulas, SQL query support, data-warehouse-native (S2 Features, line 99)
- **Runway**: Pre-built SaaS templates (ARR, MRR, cohorts) but less flexible
- **Vena**: Excel-native (full flexibility via formulas)

**Scalability to 500+ Employees**:

From S2 Pricing (500-employee scenario):
- **Runway**: May stretch at 500+ (designed for <500) (S2 Pricing, line 242)
- **Causal**: Pricing uncertainty post-LucaNet (S2 Pricing, line 110)
- **Vena**: Designed for 100-2,000 employees (scales well) (S2 Pricing, line 277)

---

## Platform Matching Results

### Platforms Matching All Requirements

**1. Causal**

**Match Score**: 90% (best fit for data-warehouse-native, technical finance team)

**Strengths for This Scenario**:
- **Data warehouse native**: Direct Snowflake query (eliminates manual SQL exports)
- **Flexible modeling**: Human-readable formulas for complex SaaS metrics (NRR, cohort LTV)
- **SQL support**: Finance analysts can write custom queries (technical team advantage)
- **NetSuite integration**: API available (5-7 day setup)
- **Budget**: $89K 3-year TCO (most affordable option)
- **Fast implementation**: 1-2 weeks (S2 Implementation, line 36)

**Limitations for This Scenario**:
- **Gusto HRIS integration**: None (S2 Integrations, line 39) - manual employee sync required
- **NetSuite integration**: Not as seamless as Planful (API vs native)
- **Pre-built reports**: Limited (must build custom dashboards)
- **Post-acquisition uncertainty**: LucaNet pricing changes unclear (S2 Pricing, line 110)
- **Scalability question**: Will LucaNet raise prices as company scales?

**Data from S2**:
- Snowflake integration: Direct query, native (S2 Integrations, line 118)
- Implementation: 1-2 weeks, self-service (S2 Implementation, line 36)
- Pricing: $20K-24K/year for 200 employees (S2 Pricing, line 242)
- Data warehouse focus: Core differentiator (S2 Integrations, line 350)

**Why This Fits**:
- Company already Snowflake-centric (data warehouse as source of truth)
- Finance analysts technical (SQL comfortable)
- Unit economics in Snowflake (CAC, LTV, payback) → direct integration eliminates manual exports
- Flexible enough for complex SaaS metrics (not limited to pre-built templates)

---

**2. Runway**

**Match Score**: 80% (good fit, but less flexible modeling than Causal)

**Strengths for This Scenario**:
- **Snowflake integration**: Native Gold-tier (2-3 day setup) (S2 Integrations, line 121)
- **NetSuite integration**: Native (2-3 day setup) (S2 Integrations, line 243)
- **Gusto HRIS integration**: Native (S2 Integrations, line 39) - automates headcount planning
- **Pre-built SaaS templates**: ARR, MRR, cohort analysis ready-made
- **Fast implementation**: 1-2 weeks (S2 Implementation, line 35)
- **Budget**: $106K 3-year TCO (within budget)
- **Modern collaboration**: Real-time, @mentions, mobile (S2 Features, line 143)

**Limitations for This Scenario**:
- **Modeling flexibility**: Pre-built templates less flexible than Causal custom formulas
- **Scalability concern**: Designed for <500 employees (may outgrow in 3-4 years) (S2 Pricing, line 242)
- **Complex SaaS metrics**: Cohort LTV, NRR by segment may require workarounds
- **No consolidation**: If multi-entity needed in 2 years, may need migration (S2 Features, line 62)

**Data from S2**:
- Snowflake integration: Gold-tier, native (S2 Integrations, line 121)
- Gusto integration: Native (S2 Integrations, line 39)
- Implementation: 1-2 weeks, self-service (S2 Implementation, line 59)
- Pricing: $25K-29K/year for 200 employees (S2 Pricing, line 242)
- Scalability: 200-500 employees (may stretch) (S2 Pricing, line 242)

**Why This Fits**:
- Turnkey SaaS solution (pre-built templates faster than Causal custom build)
- HRIS integration advantage (Gusto native vs Causal manual)
- Modern UX (Series B company expects consumer-grade tools)

**Why This Might Not Fit Long-Term**:
- May outgrow at 500+ employees (platform designed for <500)
- Limited consolidation (if international expansion requires multi-entity)

---

**3. Vena**

**Match Score**: 70% (fits budget/timeline, but Excel-native may not appeal to technical team)

**Strengths for This Scenario**:
- **NetSuite integration**: Native (3-5 day setup) (S2 Integrations, line 243)
- **Flexible modeling**: Excel interface (unlimited flexibility via formulas)
- **Scalability**: Designed for 100-2,000 employees (will scale to 500+) (S2 Pricing, line 277)
- **Budget**: $250K 3-year TCO (upper limit but acceptable) (S2 Pricing, line 324)
- **Implementation**: 4-12 weeks (guided setup within requirement) (S2 Implementation, line 37)
- **Consolidation ready**: Multi-entity support for future expansion (S2 Features, line 59)

**Limitations for This Scenario**:
- **Snowflake integration**: API only (not native) (S2 Integrations, line 111) - requires iPaaS or custom
- **Excel-native UX**: Not modern web-based (may not appeal to technical finance team)
- **Gusto HRIS**: No native integration (S2 Integrations, line 439)
- **Real-time collaboration**: Limited (Excel-based) (S2 Features, line 140)
- **Cost**: 3x more expensive than Causal ($250K vs $89K)

**Data from S2**:
- NetSuite integration: Native, 3-5 day setup (S2 Integrations, line 243)
- Snowflake integration: API available (not native) (S2 Integrations, line 111)
- Implementation: 1-3 months typical (S2 Implementation, line 37)
- Pricing: $55K-65K/year for 200 employees (S2 Pricing, line 277)
- Scalability: 100-2,000 employees (S2 Pricing, line 277)

**Why This Fits**:
- Scales to 500+ employees (won't outgrow)
- Multi-entity consolidation ready (future-proof)
- Excel familiarity (if team prefers Excel vs web-based)

**Why This Might Not Fit**:
- Excel-native step backwards (company moved from Excel to Looker for modern BI)
- Snowflake integration not native (manual setup required)
- 3x cost of Causal (harder to justify if Causal meets needs)

---

### Platforms NOT Matching Requirements

**4. Prophix**

**Why Excluded**:
- ❌ $345K 3-year TCO (38% over budget) (S2 Pricing, line 325)
- ⚠️ Snowflake API only (not native) (S2 Integrations, line 111)
- Better fit for 500-2,000 employees (slight overkill at 200)

**5. Planful**

**Why Excluded**:
- ❌ $510K 3-year TCO (2x over budget) (S2 Pricing, line 326)
- ⚠️ Snowflake requires iPaaS (not native) (S2 Integrations, line 111)
- ✅ Best NetSuite integration (600+ customers) but doesn't justify 5x cost premium
- Enterprise pricing inappropriate for 200-employee scale-up

**6. Adaptive, OneStream, Anaplan**

**Why Excluded**:
- ❌ $630K-$1.26M 3-year TCO (2.5-5x over budget) (S2 Pricing, lines 327-328)
- ❌ 8-48 week implementations (miss Q4 planning cycle) (S2 Implementation, lines 39-42)
- ❌ Professional services required ($50K-500K) (S2 Implementation, lines 214-217)
- Target market: 500-50,000 employees (massive overkill at 200)

---

## Key Trade-offs

### Causal vs Runway vs Vena Decision Framework

**Choose Causal if**:
- Data warehouse is central data platform (Snowflake as source of truth)
- Finance analysts technical (comfortable writing SQL, custom formulas)
- Budget tightest constraint ($89K vs $106K vs $250K)
- Willing to build custom SaaS metrics dashboards (no pre-built templates)
- Can accept manual HRIS sync (4-6 hours/month)

**Choose Runway if**:
- Want turnkey SaaS solution (pre-built templates vs custom build)
- HRIS automation critical (Gusto native integration)
- Prefer modern collaboration (real-time, @mentions, mobile)
- Company likely to stay <500 employees next 3-4 years
- Budget allows $106K (17% premium over Causal)

**Choose Vena if**:
- Excel familiarity preferred over web-based UX
- Confident company will scale to 500+ employees (need scalable platform)
- Multi-entity consolidation likely in 18-24 months (international expansion)
- Budget allows $250K (2.8x Causal, 2.4x Runway)
- Willing to invest in iPaaS for Snowflake integration ($10K-20K/year)

---

### Quantified Trade-off Analysis

**Causal vs Runway**: $17K difference over 3 years

**Runway Advantages** (worth $17K?):
- Gusto HRIS integration: Save 4-6 hours/month × 36 months = 144-216 hours
- Pre-built SaaS templates: Save 20-40 hours initial setup
- **Total time savings**: 164-256 hours × $100/hour (analyst rate) = $16,400-25,600

**Answer**: Runway HRIS automation + templates justify $17K premium IF headcount planning is major pain point.

**Causal Advantages** (worth saving $17K?):
- Direct Snowflake query: Save 10-15 hours/week manual SQL exports = 40-60 hours/month
- 3-year savings: 1,440-2,160 hours × $100/hour = $144,000-216,000

**Answer**: If Snowflake integration eliminates 10+ hours/week manual work, Causal advantage is massive (10x ROI on $17K savings).

**Key Question**: Is manual SQL export pain greater than manual HRIS sync pain?

**For This Scenario**: Snowflake pain is 10-15 hours/week (VP Finance + analyst time). HRIS pain is 4-6 hours/month. **Causal wins** (10x more painful problem solved).

---

**Vena vs Causal**: $161K difference over 3 years

**Vena Advantages** (worth $161K premium?):
- Scalability to 500+ employees: Avoid platform migration cost ($30K-100K)
- Multi-entity consolidation: Future-proof for international expansion
- Excel flexibility: Unlimited custom formulas (if team prefers Excel)

**Causal Advantages** (worth $161K savings?):
- Direct Snowflake integration (native vs Vena API + iPaaS)
- Modern UX (web-based vs Excel-native)
- Faster implementation (1-2 weeks vs 4-12 weeks)

**Key Question**: Will company reach 500+ employees AND need multi-entity consolidation in 3-4 years?

**If Yes**: Vena worth premium (avoid migration cost)
**If No**: Causal wins ($161K savings fund platform migration later if needed)

---

## Implementation Considerations

### Causal Implementation Path (1-2 Weeks)

**Week 1: Data Connections**
- Day 1-2: Connect Snowflake (SQL credentials, database permissions)
- Day 3: Configure Snowflake queries (pull DAU, engagement, product metrics)
- Day 4-5: Connect NetSuite API (chart of accounts, 18-month historical actuals)
- Day 5: Connect Salesforce API (pipeline data, close rates)

**Week 2: Model Building**
- Day 6-8: Build custom headcount model (department-level, salary bands)
- Day 8-10: Build revenue forecast (ARR, churn, expansion, cohort-based)
- Day 10-12: Build unit economics (CAC by channel, LTV by cohort, payback period)
- Day 12-14: Create SaaS metrics dashboards (NRR, GRR, LTV:CAC, Rule of 40)

**Week 3: Launch**
- Day 15-16: Build 5 scenarios (base + sensitivity: churn ±1%, expansion ±2%)
- Day 17-18: Train finance team (SQL queries, custom formulas)
- Day 18-20: Prepare board deck, present to CFO

**Total Time**: 80-120 hours (finance analyst + data engineer)

**Success Factors**:
- Clean Snowflake schema (product metrics tables well-documented)
- NetSuite API access (IT team provides credentials)
- SQL skills (finance analyst comfortable with Snowflake SQL syntax)

---

### Runway Implementation Path (1-2 Weeks)

**Week 1: Integrations**
- Day 1-2: Connect NetSuite (native connector, automated setup)
- Day 3-4: Connect Gusto HRIS (employee data, salaries, departments)
- Day 5-6: Connect Snowflake Gold-tier (product metrics)
- Day 7: Connect Salesforce (pipeline data)

**Week 2: Model Building**
- Day 8-9: Choose SaaS template (pre-built ARR, MRR, cohort models)
- Day 10-11: Customize headcount plan (hiring pipeline from Gusto)
- Day 12-13: Build department budgets (OpEx by team)
- Day 13-14: Create scenarios, dashboards

**Week 3: Launch**
- Day 15-17: Train finance team (2-4 hours sessions)
- Day 17-20: Board deck preparation, stakeholder review

**Total Time**: 60-80 hours (finance analyst, less time due to pre-built templates)

**Success Factors**:
- Pre-built SaaS template fits business model (may need customization)
- Gusto HRIS data complete (salaries, start dates, departments)
- Acceptance of Runway's modeling structure (less flexible than Causal)

---

## Cost Analysis (3-Year TCO)

### Causal Total Cost of Ownership

**Software Costs**:
- Year 1: $20,000 (200 employees) + $3,000 implementation = $23,000
- Year 2: $22,000 (240 employees, 20% growth)
- Year 3: $24,000 (280 employees, 17% growth)
- **Total Software**: $69,000

**Implementation Costs**:
- Self-service setup: $0 vendor fees
- Finance analyst time: 80-120 hours × $100/hour = $8,000-12,000
- Data engineer support: 20 hours × $150/hour = $3,000
- **Total Implementation**: $14,000

**Ongoing Costs**:
- Manual HRIS sync: 4 hours/month × 36 months × $100/hour = $14,400
- Training: $1,000/year (3 years = $3,000)
- Snowflake query costs: $500/year (incremental queries, 3 years = $1,500)
- **Total Ongoing**: $18,900

**3-Year TCO**: $69,000 + $14,000 + $18,900 = **$101,900**

**Cost Per Employee**: $101,900 ÷ 240 avg employees ÷ 3 years = **$142/employee/year**

---

### Runway Total Cost of Ownership

**Software Costs**:
- Year 1: $25,000 (200 employees) + $5,000 implementation = $30,000
- Year 2: $27,000 (240 employees)
- Year 3: $29,000 (280 employees)
- **Total Software**: $86,000

**Implementation Costs**:
- Guided setup: $2,000 vendor support
- Finance analyst time: 60-80 hours × $100/hour = $6,000-8,000
- Data engineer support: 10 hours × $150/hour = $1,500
- **Total Implementation**: $11,000

**Ongoing Costs**:
- HRIS integration: $0 (automated)
- Training: $1,000/year (3 years = $3,000)
- Integration maintenance: $0 (native connectors)
- **Total Ongoing**: $3,000

**3-Year TCO**: $86,000 + $11,000 + $3,000 = **$100,000**

**Cost Per Employee**: $100,000 ÷ 240 avg employees ÷ 3 years 139/employee/year**

---

### Vena Total Cost of Ownership

**Software Costs**:
- Year 1: $55,000 (200 employees) + $20,000 implementation = $75,000
- Year 2: $60,000 (240 employees)
- Year 3: $65,000 (280 employees)
- **Total Software**: $180,000

**Implementation Costs**:
- Guided setup: $15,000 vendor professional services
- Finance analyst time: 100-120 hours × $100/hour = $10,000-12,000
- Integration specialist: 40 hours × $150/hour = $6,000 (Snowflake iPaaS)
- **Total Implementation**: $36,000

**Ongoing Costs**:
- iPaaS for Snowflake: $10,000/year × 3 years = $30,000
- Training: $2,000/year (3 years = $6,000)
- Manual HRIS sync: 4 hours/month × 36 months × $100/hour = $14,400
- **Total Ongoing**: $50,400

**3-Year TCO**: $180,000 + $36,000 + $50,400 = **$266,400**

**Cost Per Employee**: $266,400 ÷ 240 avg employees ÷ 3 years = **$370/employee/year**

---

### Cost-Benefit Analysis (All Platforms)

**Finance Team Time Savings** (Snowflake Integration):
- Eliminate manual SQL exports: 10-15 hours/week × 52 weeks = 520-780 hours/year
- Automated actuals sync: 5-8 hours/month × 12 months = 60-96 hours/year
- Faster board deck prep: 1-2 days/quarter × 4 quarters = 32-64 hours/year
- **Total Time Savings**: 612-940 hours/year × $100/hour = **$61,200-94,000/year**

**3-Year Benefit**: $183,600-282,000

**ROI Calculation**:
- Causal: $282,000 benefit ÷ $101,900 cost = **277% ROI** (payback 4 months)
- Runway: $282,000 benefit ÷ $100,000 cost = **282% ROI** (payback 4 months)
- Vena: $282,000 benefit ÷ $266,400 cost = **106% ROI** (payback 11 months)

**Insight**: Causal and Runway nearly identical ROI (both excellent). Vena ROI positive but 2.7x higher cost reduces return.

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 300+
**Purpose**: Generic scenario demonstrating data warehouse integration requirements
**Approach**: Hardware store model (show options, not prescribe choice)

**Key Pattern Demonstrated**:
1. Requirements → Data warehouse integration (Causal, Anaplan, OneStream, Runway pass)
2. Data warehouse → Budget filtering (Causal, Runway, Vena pass; others fail)
3. Budget → Modeling flexibility (Causal wins for SQL-based customization)
4. Quantified trade-off: Snowflake pain (10-15 hr/week) >> HRIS pain (4-6 hr/month)

**Limitations**:
- Generic scenario (not real client)
- Assumes Snowflake schema well-documented (reality varies)
- ROI calculation assumes full time savings (conservative: 70-80% actual)
- Scalability concern for Runway at 500+ employees (may require migration in 3-4 years)
