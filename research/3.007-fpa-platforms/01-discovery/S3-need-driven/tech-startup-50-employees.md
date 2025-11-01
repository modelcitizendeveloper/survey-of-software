# S3 Scenario: Tech Startup (50 Employees)

**Experiment**: 3.007 FP&A Platforms
**Stage**: S3 - Need-Driven Discovery
**Date**: November 1, 2025
**Scenario Type**: Generic Profile (not client-specific)

---

## Scenario Context

**Company Profile**:
- Stage: Series A SaaS company
- Employee count: 50 (current), projecting 75 by Year 3
- Revenue: $3M ARR (current), targeting $10M ARR in 18 months
- Funding: $10M Series A raised, 24-month runway at current burn
- Growth rate: Hiring 3-5 employees per month
- Business model: B2B SaaS, monthly subscriptions

**Finance Team**:
- CFO: Fractional (3 days/week), transitioning to full-time
- Finance Manager: 1 FTE (handles AP/AR, monthly close, budgeting)
- Current tools: Excel spreadsheets (50+ tabs), emailed weekly

**Technical Environment**:
- Accounting: QuickBooks Online (3 years historical data)
- HRIS: Rippling (6 months old, migrated from spreadsheets)
- CRM: HubSpot (sales pipeline tracking)
- Payments: Stripe (subscription billing)

**Pain Points**:
- Excel version control chaos (20+ budget versions emailed)
- Monthly budget vs actuals takes 8-10 hours to reconcile
- Hiring plan disconnected from budget (manual employee list)
- Board meetings require 2-3 days prep (manual deck creation)
- No scenario planning (optimistic/base/pessimistic cases)

---

## Requirements Analysis

### Primary Requirements

**1. Fast Implementation (Weeks, Not Months)**
- Constraint: Cannot wait 3-6 months for implementation
- Reason: Board meeting in 6 weeks needs new forecast model
- Timeline need: Operational within 2-4 weeks maximum
- Resource constraint: Finance manager has 10 hours/week for setup

**2. Affordable Budget ($5K-30K/Year)**
- Funding stage: Series A (capital-efficient mindset)
- Current spend: $0 (Excel-based)
- Budget range: $5K-30K/year maximum
- 3-year TCO target: Under $100K total

**3. Rippling HRIS Integration**
- Critical need: Automate headcount planning
- Current process: Manual employee export weekly (error-prone)
- Desired state: Real-time employee sync (names, salaries, departments)
- Impact: Eliminate 4-6 hours/month manual data entry

**4. Modern User Experience**
- Team expectation: Consumer-grade UX (Slack, Notion, Linear quality)
- Change resistance: Finance manager comfortable with web apps
- Collaboration need: CFO + finance manager + department heads access
- Mobile access: CFO wants board deck on iPad

**5. Self-Service Setup**
- Consulting budget: $0-5K maximum
- In-house expertise: Finance manager technical (former analyst)
- Support need: Documentation + async chat support (not on-site consulting)

### Secondary Requirements

**6. QuickBooks Online Integration**
- Historical data: 3 years actuals needed for trending
- Sync frequency: Daily (acceptable), real-time (nice-to-have)
- Chart of accounts: 150 accounts (standard SaaS expense structure)

**7. Scenario Modeling**
- Use case: Board presentations (optimistic/base/pessimistic)
- Scenarios needed: 3-5 simultaneous scenarios
- Toggle speed: Real-time switching during board meetings

**8. SaaS Metrics Support**
- Key metrics: ARR, MRR, CAC, LTV, burn multiple, months to breakeven
- Data sources: Stripe (billing), HubSpot (pipeline)
- Reporting: SaaS-specific dashboards (not generic financial reports)

---

## Applying S2 Catalog Data

### Step 1: Filter by Integration Requirements

**Critical Integration: Rippling HRIS**

From S2 Integration Matrix:
- ✅ **Runway**: Native Rippling integration (1-2 day setup)
- ❌ **Adaptive**: No SMB HRIS support
- ❌ **Anaplan**: No Rippling integration
- ❌ **Causal**: No Rippling integration
- ❌ **OneStream**: No Rippling integration
- ❌ **Planful**: No Rippling integration (lost deal to Runway in forum post)
- ❌ **Prophix**: No Rippling integration
- ❌ **Vena**: No Rippling integration

**Result**: Only Runway offers native Rippling integration.

**Important Integration: QuickBooks Online**

From S2 Integration Matrix:
- ✅ **Runway**: Native QBO integration (1-2 day setup)
- ✅ **Causal**: Native QBO integration
- ✅ **Prophix**: Native QBO integration
- ⚠️ **Adaptive**: API available (requires custom work)
- ⚠️ **Anaplan**: API available
- ⚠️ **Planful**: API available
- ⚠️ **OneStream**: API available
- ⚠️ **Vena**: API available

**Result**: Runway, Causal, Prophix offer native QBO connectors.

### Step 2: Filter by Implementation Timeline

**Requirement: 2-4 Week Implementation**

From S2 Implementation Complexity Matrix:
- 🟢 **Runway**: 1-2 weeks typical (self-service)
- 🟢 **Causal**: 1-2 weeks typical (self-service)
- 🟡 **Vena**: 4-12 weeks (guided setup required)
- 🟡 **Prophix**: 6-12 weeks (consulting required)
- 🔴 **Adaptive**: 8-16 weeks (professional services required)
- 🔴 **Planful**: 12-24 weeks (professional services required)
- 🔴 **OneStream**: 12-24 weeks (implementation partner required)
- 🔴 **Anaplan**: 16-48 weeks (Big 4 consulting required)

**Result**: Only Runway and Causal meet 2-4 week timeline.

### Step 3: Filter by Budget Constraints

**Requirement: $5K-30K/Year (3-Year TCO <$100K)**

From S2 Pricing Analysis (Startup 50 Employees):

| Platform | Year 1 | Year 2 | Year 3 | 3-Year Total |
|----------|--------|--------|--------|--------------|
| **Runway** | $12K + $2K impl | $13K | $14K | **$41K** ✅ |
| **Causal** | $8K + $1K impl | $10K | $12K | **$31K** ✅ |
| **Vena** | $30K + $15K impl | $32K | $34K | **$111K** ❌ |
| **Prophix** | $25K + $20K impl | $28K | $30K | **$123K** ❌ |
| **Planful** | $75K + $50K impl | $80K | $85K | **$340K** ❌ |
| **Adaptive** | $80K + $60K impl | $85K | $90K | **$395K** ❌ |
| **OneStream** | N/A | N/A | N/A | N/A (not sold to <500 employees) |
| **Anaplan** | N/A | N/A | N/A | N/A (not sold to <500 employees) |

**Result**: Runway ($41K) and Causal ($31K) meet budget.

### Step 4: Cross-Reference Feature Requirements

**SaaS-Specific Features Needed**:

From S2 Feature Matrix:
- **Runway**: Pre-built SaaS templates, ARR/MRR modeling, cohort analysis, burn multiple tracking
- **Causal**: Flexible modeling, data warehouse integration (if using), scenario modeling

**Collaboration Features Needed**:

From S2 Feature Matrix:
- **Runway**: Real-time collaboration, @mentions, mobile access (full), modern UX
- **Causal**: Real-time collaboration, version control, modern UX

---

## Platform Matching Results

### Platforms Matching All Requirements

**1. Runway**

**Match Score**: 95% (meets all critical + most secondary requirements)

**Strengths for This Scenario**:
- Native Rippling integration (1-2 day setup) - SOLVES major pain point
- Native QBO integration (1-2 day setup)
- 1-2 week implementation (self-service)
- $41K 3-year TCO (within budget)
- Pre-built SaaS templates (ARR, MRR, cohort analysis)
- Modern collaboration (real-time, @mentions, mobile)
- Self-service onboarding (no consulting required)

**Limitations for This Scenario**:
- No multi-entity consolidation (not needed for 50-employee startup)
- No capital planning module (not needed for SaaS OpEx-focused model)
- Limited custom reporting (pre-built SaaS reports sufficient)

**Data from S2**:
- Implementation: 1-2 weeks, $0-2K setup cost (S2 Implementation Complexity, line 59)
- Pricing: $10K-25K/year for 50-200 employees (S2 Pricing, line 241)
- Rippling integration: Native, 1-2 day setup (S2 Integrations, line 246)
- User license: Unlimited users (no per-seat fees) (S2 Pricing, line 251)

**Why This Fits**:
- Designed for Series A-C startups (exact target market)
- Fast time-to-value: Board deck in 2-3 weeks (S2 Implementation, line 410)
- Modern UX: Consumer-grade (addresses UX requirement)
- SMB HRIS leader: Rippling, Gusto, BambooHR native (S2 Integrations, line 418)

---

**2. Causal**

**Match Score**: 75% (meets critical requirements, missing HRIS integration)

**Strengths for This Scenario**:
- Native QBO integration (fast setup)
- 1-2 week implementation (self-service)
- $31K 3-year TCO (most affordable option)
- Flexible modeling (human-readable formulas)
- Real-time collaboration
- Data warehouse integration (if using Snowflake/BigQuery)

**Limitations for This Scenario**:
- **No Rippling integration** (dealbreaker if HRIS sync critical)
- Minimal HRIS support overall (S2 Integrations, line 356)
- No pre-built SaaS templates (must build custom)
- Post-LucaNet acquisition pricing uncertainty (S2 Pricing, line 110)
- Limited pre-built connectors (15 vs 50+ for enterprise) (S2 Integrations, line 170)

**Data from S2**:
- Implementation: 1-2 weeks, $0-2K setup cost (S2 Implementation Complexity, line 36)
- Pricing: $8K-12K/year estimated (post-acquisition) (S2 Pricing, line 111)
- QBO integration: Native connector (S2 Integrations, line 74)
- HRIS integration: None for Rippling (S2 Integrations, line 38)

**Why This Doesn't Fit as Well**:
- Missing Rippling integration eliminates headcount automation benefit
- Manual employee data entry continues (doesn't solve pain point)
- Best for data-warehouse-native companies (not applicable here)

---

### Platforms NOT Matching Requirements

**3. Prophix**

**Why Excluded**:
- ❌ No Rippling integration (S2 Integrations, line 404)
- ❌ $123K 3-year TCO (3x over budget) (S2 Pricing, line 325)
- ❌ 6-12 week implementation with consulting (S2 Implementation, line 38)
- Designed for mid-market (500-2,000 employees), overkill for 50

**4. Vena**

**Why Excluded**:
- ❌ No Rippling integration (S2 Integrations, line 438)
- ❌ $111K 3-year TCO (2.7x over budget) (S2 Pricing, line 324)
- ❌ Excel-native UX (doesn't meet modern UX requirement)
- Excel dependency is step backwards from modern workflow

**5. Planful, Adaptive, OneStream, Anaplan**

**Why Excluded**:
- ❌ No Rippling integration (S2 Integrations, lines 38-42)
- ❌ $340K-$395K 3-year TCO (8-10x over budget) (S2 Pricing, lines 326-327)
- ❌ 3-12 month implementations (S2 Implementation, lines 40-42)
- ❌ Professional services required ($50K-250K) (S2 Implementation, line 217)
- Target market: 500-50,000 employees (not applicable to 50-employee startup)

---

## Key Trade-offs

### Runway vs Causal Decision Framework

**Choose Runway if**:
- Rippling integration is critical (automate headcount planning)
- Need pre-built SaaS templates (faster setup)
- Want modern collaboration features (@mentions, real-time)
- Prefer turnkey solution (less configuration)
- Budget allows $41K 3-year TCO

**Choose Causal if**:
- Budget is tightest constraint ($31K vs $41K 3-year TCO)
- Already have data warehouse (Snowflake, BigQuery)
- Comfortable building custom models (technical finance team)
- Can live with manual HRIS data entry
- Prefer human-readable formulas vs spreadsheet syntax

**Key Question**: Is Rippling automation worth $10K over 3 years?

**Quantified Trade-off**:
- Manual HRIS export: 4-6 hours/month × 36 months = 144-216 hours
- Finance manager fully-loaded cost: $75-100/hour
- Manual process cost: $10,800-21,600 over 3 years
- **Answer**: Yes, Rippling automation pays for price difference

---

## Implementation Considerations

### Runway Implementation Path (1-2 Weeks)

**Week 1: Foundations**
- Day 1-2: Connect Rippling integration (1-2 day setup per S2)
- Day 2-3: Connect QuickBooks Online (import 3 years actuals)
- Day 3-4: Import employee data from Rippling (names, salaries, departments)
- Day 4-5: Map QBO chart of accounts to expense categories

**Week 2: Model Building**
- Day 6-7: Choose SaaS template (ARR, MRR, cohort modeling)
- Day 7-8: Build headcount plan (hiring pipeline from Rippling)
- Day 8-9: Create department budgets (engineering, sales, marketing, G&A)
- Day 9-10: Model revenue forecast (ARR growth, churn assumptions)

**Week 3: Launch**
- Day 11-12: Create 3 scenarios (optimistic, base, pessimistic)
- Day 12-13: Build board deck dashboards
- Day 13-14: Train CFO + finance manager (2-4 hours total)
- Day 14: Present to board (live dashboards on iPad)

**Total Time**: 40-80 hours finance manager time (S2 Implementation, line 75)

**Success Factors**:
- Clean QBO data (fix GL errors before import)
- Complete Rippling employee data (salaries, start dates, departments)
- CFO availability for requirements review (2-3 sessions)

---

### Causal Implementation Path (1-2 Weeks)

**Week 1: Foundations**
- Day 1-2: Connect QuickBooks Online integration
- Day 2-3: Import 3 years historical actuals
- Day 3-5: Manual employee data entry (Rippling export to CSV)
- Day 5: Chart of accounts mapping

**Week 2: Model Building**
- Day 6-8: Build custom headcount model (no pre-built template)
- Day 8-10: Build revenue forecast model (ARR, churn, expansion)
- Day 10-12: Create expense budget by department

**Week 3: Launch**
- Day 13-14: Create scenarios, build dashboards
- Day 14: Train team, present to board

**Total Time**: 60-100 hours finance manager time (higher than Runway due to custom modeling)

**Success Factors**:
- Technical finance team (comfortable building models from scratch)
- Manual HRIS process acceptable (4-6 hours/month ongoing)
- Focus on cost savings over convenience

---

## Cost Analysis (3-Year TCO)

### Runway Total Cost of Ownership

**Software Costs**:
- Year 1: $12,000 (50 employees) + $2,000 implementation = $14,000
- Year 2: $13,000 (60 employees, 20% growth)
- Year 3: $14,000 (70 employees, 17% growth)
- **Total Software**: $41,000

**Implementation Costs**:
- Self-service setup: $0
- Finance manager time: 40-80 hours × $75/hour = $3,000-6,000
- **Total Implementation**: $5,000 (loaded cost)

**Ongoing Costs**:
- Training: $500/year (video tutorials, documentation)
- Support: Included (chat/email support)
- Integration maintenance: $0 (native connectors)
- **Total Ongoing**: $1,500 (3 years)

**3-Year TCO**: $41,000 + $5,000 + $1,500 = **$47,500**

**Cost Per Employee**: $47,500 ÷ 60 avg employees ÷ 3 years = **$264/employee/year**

---

### Causal Total Cost of Ownership

**Software Costs**:
- Year 1: $8,000 (50 employees) + $1,000 implementation = $9,000
- Year 2: $10,000 (60 employees, price increase assumed)
- Year 3: $12,000 (70 employees, continued price adjustment)
- **Total Software**: $31,000

**Implementation Costs**:
- Self-service setup: $0
- Finance manager time: 60-100 hours × $75/hour = $4,500-7,500
- **Total Implementation**: $6,000 (loaded cost)

**Ongoing Costs**:
- Manual HRIS sync: 4 hours/month × 36 months × $75/hour = $10,800
- Training: $500/year
- **Total Ongoing**: $12,300 (includes manual work cost)

**3-Year TCO**: $31,000 + $6,000 + $12,300 = **$49,300**

**Cost Per Employee**: $49,300 ÷ 60 avg employees ÷ 3 years = **$274/employee/year**

**Insight**: Causal lower software cost ($31K vs $41K) is offset by manual HRIS sync labor ($10.8K over 3 years), resulting in similar true TCO.

---

### Cost-Benefit Analysis

**Finance Team Time Savings** (Both Platforms):
- Excel version control: Save 2-3 hours/month = 72-108 hours/year
- Budget vs actuals reconciliation: Save 6-8 hours/month = 72-96 hours/year
- Board deck preparation: Save 1-2 days/quarter = 32-64 hours/year
- **Total Time Savings**: 176-268 hours/year × $75/hour = **$13,200-20,100/year**

**3-Year Benefit**: $39,600-60,300

**ROI Calculation**:
- Runway: $60,300 benefit ÷ $47,500 cost = **127% ROI** (payback 18 months)
- Causal: $60,300 benefit ÷ $49,300 cost = **122% ROI** (payback 20 months)

**Qualitative Benefits** (Not Quantified):
- Faster decision-making (scenarios in minutes, not days)
- Board confidence (real-time dashboards vs static Excel)
- Reduced hiring errors (automated headcount plan vs manual)
- Scalability (grows to 200+ employees without re-implementation)

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 300+
**Purpose**: Generic scenario demonstrating HOW to apply S2 catalog data
**Approach**: Hardware store model (show options, not prescribe choice)

**Key Pattern Demonstrated**:
1. Requirements → Integration filtering (Rippling = Runway only)
2. Integration → Budget filtering (Runway + Causal only)
3. Budget → Feature matching (Runway wins on HRIS, Causal wins on cost)
4. Quantified trade-off: $10K price difference vs $10.8K manual labor cost

**Limitations**:
- Generic scenario (not real client)
- Pricing estimates may vary 20-50% based on negotiation
- Implementation time assumes clean data (reality: data cleansing adds time)
- ROI calculation assumes full time savings realized (conservative: 60-80% actual)
