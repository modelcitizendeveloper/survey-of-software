# S3 Scenario: Manufacturing Mid-Market (500 Employees)

**Experiment**: 3.007 FP&A Platforms
**Stage**: S3 - Need-Driven Discovery
**Date**: November 1, 2025
**Scenario Type**: Generic Profile (not client-specific)

---

## Scenario Context

**Company Profile**:
- Industry: Manufacturing (industrial equipment)
- Employee count: 500 (current), projecting 550 by Year 3
- Revenue: $120M (current), targeting $160M in 3 years
- Structure: Parent company + 3 subsidiaries (2 US, 1 Canada)
- Business model: B2B manufacturing, project-based revenue
- Ownership: Private equity backed (acquired 2 years ago)

**Finance Team**:
- CFO: Full-time (PE-appointed, 18 months tenure)
- Controller: 1 FTE (technical accounting, consolidation)
- FP&A Manager: 1 FTE (budgeting, forecasting, board reporting)
- Finance Analysts: 2 FTEs (division-level budgeting, variance analysis)
- Accounting team: 5 FTEs (AP/AR, payroll, month-end close)
- Current tools: Excel consolidation templates (10+ years old), QlikView dashboards

**Technical Environment**:
- ERP: NetSuite OneWorld (3 subsidiaries, implemented 2.5 years ago)
- HRIS: ADP Workforce Now (500 employees, payroll + HR)
- Legacy systems: SAP ECC on-premise (decommissioned 1 year ago, historical data archived)
- BI Tool: QlikView (operational dashboards, not integrated with FP&A)

**Entity Structure**:
- Parent: Holding company (corporate G&A)
- Subsidiary 1: US East manufacturing facility (250 employees, $60M revenue)
- Subsidiary 2: US West distribution center (150 employees, $40M revenue)
- Subsidiary 3: Canada manufacturing facility (100 employees, $20M revenue CAD)
- Intercompany transactions: Significant (parts transfers, management fees)

**Pain Points**:
- Excel consolidation takes 5-7 days each month-end (manual eliminations)
- Multi-currency translation manual (CAD → USD FX adjustments)
- Driver-based planning missing (capacity utilization, production volume drivers)
- PE reporting requirements: Monthly board pack (15+ reports), quarterly lender covenant compliance
- NetSuite reporting insufficient (financial statements only, no variance analysis)

---

## Requirements Analysis

### Primary Requirements

**1. Multi-Entity Consolidation**
- Critical need: Automated intercompany eliminations (300+ transactions/month)
- Current process: Excel VLOOKUP matching (error-prone, 2-3 days reconciliation)
- Entity structure: 3 subsidiaries now, potential 2 more in 18-24 months (PE add-on acquisitions)
- Ownership: 100% owned subsidiaries (simple structure), no minority interests

**2. NetSuite Integration**
- Historical data: 2.5 years in NetSuite OneWorld, 5+ years in SAP ECC (archived)
- Chart of accounts: 800+ accounts (manufacturing cost detail: materials, labor, overhead)
- Consolidation segments: 3 subsidiaries × 5 departments × 10 cost centers = 150+ dimensions
- Sync frequency: Daily (month-end close requires up-to-date actuals)
- NetSuite customization: Custom fields (project codes, cost centers, product lines)

**3. Multi-Currency Support**
- Currencies: USD (primary), CAD (Canada subsidiary)
- Translation: Monthly FX rates (average for P&L, spot for balance sheet)
- Current gap: Manual FX adjustments in Excel (historical rates, CTA calculation)
- Future need: EUR if European expansion (PE strategy includes international growth)

**4. Driver-Based Planning**
- Manufacturing drivers: Production volume (units), capacity utilization (%), headcount by shift
- Revenue drivers: Project pipeline (quoted, won, delivered), pricing per unit
- Cost drivers: Material cost per unit, labor hours per unit, overhead allocation %
- Current gap: Static expense budgets (no linkage to production volume)

**5. Budget ($50K-150K/Year)**
- Mid-market budget: PE expects professionalization (invest in FP&A tools)
- Current spend: $12K/year (QlikView licenses, Excel-based)
- 3-year TCO target: $200K-500K total
- PE expectation: Efficiency gains justify investment (reduce close cycle time)

### Secondary Requirements

**6. ADP Workforce Now Integration**
- Use case: Headcount planning (manufacturing shifts, salary bands)
- Current gap: Biweekly ADP exports to Excel (payroll actuals)
- Desired state: Automated headcount sync (actual vs budget variance by department)

**7. 8-16 Week Implementation**
- Constraint: Month-end close cannot be disrupted (avoid Q4 busy season)
- Resource availability: FP&A manager + controller 50% time to implementation
- Consulting acceptable: Guided setup with NetSuite consolidation expertise
- Timeline: Q1 implementation (Jan-Mar), go-live for Q2 budget cycle (April)

**8. Audit-Ready Reporting**
- Use case: PE lender covenant compliance (EBITDA, leverage ratios)
- PE requirement: Monthly board pack (actual vs budget vs forecast, variance explanations)
- Audit trail: SOX-lite controls (approval workflows, version control)

---

## Applying S2 Catalog Data

### Step 1: Filter by Consolidation Requirements

**Critical Requirement: Multi-Entity Consolidation + Intercompany Eliminations**

From S2 Feature Matrix (Consolidation Features):
- ✅ **Adaptive**: Full consolidation, automated IC eliminations (S2 Features, line 60)
- ✅ **Anaplan**: Full consolidation, automated IC eliminations (S2 Features, line 60)
- ✅ **OneStream**: Full consolidation, automated IC eliminations (unified CPM) (S2 Features, line 60)
- ✅ **Planful**: Full consolidation + Consolidations Premium add-on (S2 Features, line 60)
- ✅ **Prophix**: Full consolidation, Sigma Conso (140+ audit reports) (S2 Features, line 68)
- ✅ **Vena**: Full consolidation, automated IC eliminations (S2 Features, line 60)
- ⚠️ **Runway**: Basic multi-entity, no IC eliminations (S2 Features, line 59)
- ❌ **Causal**: No consolidation support (S2 Features, line 59)

**Result**: Adaptive, Anaplan, OneStream, Planful, Prophix, Vena support consolidation. Runway and Causal excluded.

**Consolidation Leaders** (From S2):
- **OneStream**: Unified CPM (consolidation + planning + close + reporting)
- **Prophix**: Sigma Conso acquisition (140+ audit reports)
- **Planful**: Consolidations Premium add-on (2025 launch)

---

### Step 2: Filter by NetSuite Integration

**Critical Requirement: NetSuite OneWorld Integration**

From S2 Integration Matrix (NetSuite Support):
- ✅ **All consolidation platforms**: Native NetSuite integration
  - **Planful**: 600+ NetSuite customers, 2-3 day setup (S2 Integrations, line 98)
  - **Prophix**: Native NetSuite, 3-5 day setup (S2 Integrations, line 72)
  - **Adaptive**: Native NetSuite, 3-5 day setup (S2 Integrations, line 72)
  - **Vena**: Native NetSuite, 3-5 day setup (S2 Integrations, line 72)
  - **Anaplan**: Native NetSuite, 3-5 day setup (S2 Integrations, line 72)
  - **OneStream**: Native NetSuite, 3-5 day setup (S2 Integrations, line 72)

**Result**: All remaining platforms offer native NetSuite integration (table stakes for mid-market).

**Best NetSuite Partnership**: Planful (600+ NetSuite customers, deepest integration history)

---

### Step 3: Filter by Budget Constraints

**Requirement: $50K-150K/Year (3-Year TCO $200K-500K)**

From S2 Pricing Analysis (500 Employees):

| Platform | Year 1 | Year 2 | Year 3 | 3-Year Total | Within Budget? |
|----------|--------|--------|--------|--------------|----------------|
| **Vena** | $55K + $20K impl | $60K | $65K | **$250K** ✅ |
| **Prophix** | $75K + $30K impl | $80K | $85K | **$345K** ✅ |
| **Adaptive** | $150K + $75K impl | $160K | $170K | **$630K** ❌ (26% over) |
| **Planful** | $120K + $60K impl | $130K | $140K | **$510K** ✅ (upper limit) |
| **OneStream** | $250K + $150K impl | $270K | $290K | **$1,110K** ❌ (2.2x over) |
| **Anaplan** | $300K + $150K impl | $320K | $340K | **$1,260K** ❌ (2.5x over) |

**Result**: Vena ($250K), Prophix ($345K), and Planful ($510K) meet budget. Adaptive, OneStream, Anaplan too expensive.

**Note**: Adaptive slightly over budget (26%), but may negotiate down. OneStream and Anaplan significantly over budget (enterprise-focused).

---

### Step 4: Filter by Implementation Timeline

**Requirement: 8-16 Week Implementation (Q1 Jan-Mar)**

From S2 Implementation Complexity Matrix:
- 🟡 **Vena**: 4-12 weeks typical (S2 Implementation, line 37)
- 🟡 **Prophix**: 6-12 weeks typical (S2 Implementation, line 38)
- 🔴 **Planful**: 12-24 weeks typical (S2 Implementation, line 40)
- 🔴 **Adaptive**: 8-16 weeks typical (S2 Implementation, line 39)
- 🔴 **OneStream**: 12-24 weeks (S2 Implementation, line 41)
- 🔴 **Anaplan**: 16-48 weeks (S2 Implementation, line 42)

**Result**: Vena (4-12 weeks) and Prophix (6-12 weeks) fit 8-16 week timeline. Planful at upper limit (12-24 weeks). Adaptive borderline (8-16 weeks).

---

### Step 5: Cross-Reference Multi-Currency & Driver-Based Planning

**Multi-Currency Translation**:

From S2 Feature Matrix:
- ✅ **All consolidation platforms**: Full multi-currency support (S2 Features, line 61)
- Automated FX translation (monthly rates, CTA calculation)

**Driver-Based Planning**:

From S2 Feature Matrix:
- ✅ **All platforms**: Driver-based planning support (S2 Features, line 83)
- **Prophix**: Automation leader (driver-based planning core differentiator) (S2 Features, line 294)

---

## Platform Matching Results

### Platforms Matching All Requirements

**1. Vena**

**Match Score**: 85% (best budget + timeline + consolidation fit for mid-market)

**Strengths for This Scenario**:
- **Multi-entity consolidation**: Automated IC eliminations (S2 Features, line 60)
- **NetSuite integration**: Native, 3-5 day setup (S2 Integrations, line 72)
- **Multi-currency**: Full translation support (CAD → USD) (S2 Features, line 61)
- **Excel-native**: Familiar interface for 10-year Excel-based team
- **Budget**: $250K 3-year TCO (best value for consolidation) (S2 Pricing, line 352)
- **Implementation**: 4-12 weeks (guided setup) (S2 Implementation, line 37)
- **Scalability**: 100-2,000 employees (room to grow) (S2 Pricing, line 277)

**Limitations for This Scenario**:
- **ADP integration**: No native ADP Workforce Now (S2 Integrations, line 36) - manual HRIS sync
- **Excel dependency**: Not web-native (limits real-time collaboration)
- **Driver-based planning**: Good, but not best-in-class (Prophix stronger)

**Data from S2**:
- Consolidation: Full support, automated IC eliminations (S2 Features, line 60)
- NetSuite integration: Native, 3-5 day setup (S2 Integrations, line 72)
- Implementation: 1-3 months, $10K-20K standard (S2 Implementation, line 295)
- Pricing: $55K-65K/year for 500 employees (S2 Pricing, line 277)
- Multi-currency: Full support (S2 Features, line 61)

**Why This Fits**:
- Excel-native reduces change management (team comfortable with Excel)
- Best value for consolidation ($250K vs $345K+ alternatives)
- Microsoft Dynamics promo available (40% off implementation if applicable) (S2 Pricing, line 297)
- Mid-market sweet spot (500-2,000 employees)

---

**2. Prophix**

**Match Score**: 90% (best consolidation + automation + driver-based planning)

**Strengths for This Scenario**:
- **Consolidation excellence**: Sigma Conso acquisition (140+ audit reports) (S2 Features, line 68)
- **Driver-based planning**: Automation leader (core differentiator) (S2 Features, line 294)
- **NetSuite integration**: Native, 3-5 day setup (S2 Integrations, line 72)
- **Multi-currency**: Full translation support (S2 Features, line 61)
- **Implementation**: 6-12 weeks (fits timeline) (S2 Implementation, line 38)
- **Audit reporting**: 140+ pre-built audit reports (PE compliance) (S2 Features, line 68)
- **Budget**: $345K 3-year TCO (38% higher than Vena, but within upper budget) (S2 Pricing, line 353)

**Limitations for This Scenario**:
- **Cost**: $95K more than Vena over 3 years (31% premium)
- **ADP integration**: No native ADP Workforce Now (S2 Integrations, line 36)
- **Innovation pace**: Slower than newer platforms (S2 Features, line 413)

**Data from S2**:
- Consolidation: Sigma Conso (140+ audit reports) (S2 Features, line 68)
- NetSuite integration: Native, 3-5 day setup (S2 Integrations, line 399)
- Implementation: 6-12 weeks, $10K-30K standard (S2 Implementation, line 38)
- Pricing: $75K-85K/year for 500 employees (S2 Pricing, line 211)
- Driver-based planning: Automation focus (S2 Features, line 294)

**Why This Fits**:
- Manufacturing focus (capacity utilization, production volume drivers)
- Audit reporting (PE lender covenant compliance, 140+ reports)
- Automation reduces manual Excel work (driver-based planning strength)
- Mid-market leader (500-2,000 employees sweet spot)

---

**3. Planful**

**Match Score**: 80% (enterprise-grade consolidation, but expensive + long implementation)

**Strengths for This Scenario**:
- **NetSuite partnership**: 600+ customers, best integration (S2 Integrations, line 98)
- **Consolidations Premium**: 2025 add-on for complex consolidation (S2 Features, line 69)
- **Multi-entity**: Full support, automated IC eliminations (S2 Features, line 60)
- **Multi-currency**: Full translation (S2 Features, line 61)
- **Scalability**: Enterprise-grade (scales to 5,000+ employees) (S2 Pricing, line 171)

**Limitations for This Scenario**:
- **Budget**: $510K 3-year TCO (2x Vena, upper limit of budget) (S2 Pricing, line 351)
- **Implementation**: 12-24 weeks (may miss Q1 timeline) (S2 Implementation, line 40)
- **Complexity**: Professional services required ($50K-100K) (S2 Implementation, line 194)
- **ADP integration**: No native ADP Workforce Now (S2 Integrations, line 388)

**Data from S2**:
- NetSuite integration: 600+ customers, 2-3 day setup (S2 Integrations, line 98)
- Consolidations Premium: Add-on module (2025) (S2 Features, line 69)
- Implementation: 3-6 months, $50K-100K typical (S2 Implementation, line 194)
- Pricing: $120K-140K/year for 500 employees (S2 Pricing, line 171)

**Why This Fits (with caveats)**:
- Best NetSuite integration (600+ customers)
- Enterprise-grade (won't outgrow if PE adds acquisitions)
- Consolidations Premium (advanced features for complex consolidation)

**Why This Might Not Fit**:
- 2x cost of Vena (harder to justify at 500 employees)
- 12-24 week implementation (may miss Q1 go-live)
- Overkill for 3-subsidiary structure (enterprise features not needed yet)

---

### Platforms NOT Matching Requirements

**4. Adaptive Insights**

**Why Excluded**:
- ❌ $630K 3-year TCO (26% over budget) (S2 Pricing, line 350)
- ⚠️ Workday ecosystem focus (not applicable without Workday HCM/Financials)
- Implementation: 8-16 weeks (borderline for timeline)
- Best fit: Mid-market with Workday (not NetSuite)

**5. OneStream**

**Why Excluded**:
- ❌ $1.11M 3-year TCO (2.2x over budget) (S2 Pricing, line 353)
- ❌ $150K-500K implementation (enterprise consulting required) (S2 Implementation, line 156)
- ❌ 12-24 week implementation (may miss Q1 timeline) (S2 Implementation, line 41)
- Target market: 2,000-50,000 employees (massive overkill for 500)

**6. Anaplan**

**Why Excluded**:
- ❌ $1.26M 3-year TCO (2.5x over budget) (S2 Pricing, line 354)
- ❌ $100K-500K implementation (Big 4 consulting) (S2 Implementation, line 161)
- ❌ 16-48 week implementation (far exceeds timeline) (S2 Implementation, line 42)
- Target market: Fortune 500 (not mid-market 500 employees)

**7. Runway & Causal**

**Why Excluded**:
- ❌ No intercompany elimination support (S2 Features, lines 60-61)
- ❌ No multi-entity consolidation (basic roll-ups only)
- Target market: Startups (50-200 employees), not 500-employee manufacturers

---

## Key Trade-offs

### Vena vs Prophix vs Planful Decision Framework

**Choose Vena if**:
- Budget tightest constraint ($250K vs $345K vs $510K)
- Excel familiarity critical (minimize change management)
- 3-subsidiary structure sufficient (no complex consolidation needs)
- Can accept manual ADP HRIS sync (8-10 hours/month)
- Fast implementation priority (4-12 weeks vs 6-12 vs 12-24 weeks)

**Choose Prophix if**:
- Driver-based planning critical (capacity utilization, production volume)
- Audit reporting important (PE compliance, 140+ reports)
- Manufacturing focus (automation reduces manual Excel work)
- Budget allows $345K (38% premium over Vena justifiable)
- Willing to invest in best-in-class consolidation (Sigma Conso)

**Choose Planful if**:
- NetSuite partnership critical (600+ customers, deepest integration)
- Confident PE will add 2-3 more subsidiaries (scale to complex consolidation)
- Budget allows $510K (2x Vena, but enterprise-grade)
- Can accept 12-24 week implementation (Q2 go-live instead of Q1)
- Want future-proof platform (won't outgrow at 1,000+ employees)

---

### Quantified Trade-off Analysis

**Vena vs Prophix**: $95K difference over 3 years

**Prophix Advantages** (worth $95K premium?):
- **140+ audit reports**: Save 20-40 hours/year PE compliance reporting = 60-120 hours × $150/hour = $9,000-18,000
- **Driver-based automation**: Save 10-20 hours/month manual Excel drivers = 120-240 hours/year × $150/hour = $18,000-36,000/year × 3 years = $54,000-108,000
- **Total value**: $63,000-126,000 over 3 years

**Answer**: Prophix driver-based automation justifies $95K premium IF manufacturing drivers complex (capacity utilization, production volume, overhead allocation).

**Vena Advantages** (worth $95K savings?):
- Excel familiarity: Reduce training time (40-60 hours) = $6,000-9,000
- Faster implementation: 4-12 weeks vs 6-12 weeks (save 2-4 weeks consultant fees) = $10,000-20,000

**Key Question**: Is driver-based automation critical pain point?

**For This Scenario**: Manufacturing company needs capacity utilization, production volume drivers. **Prophix wins** (automation value $63K-126K > $95K cost).

---

**Prophix vs Planful**: $165K difference over 3 years

**Planful Advantages** (worth $165K premium?):
- **NetSuite partnership**: Save 1-2 weeks integration setup = $5,000-10,000
- **Consolidations Premium**: Advanced consolidation features (sub-consolidation, complex ownership)
- **Scalability**: Handle 10+ subsidiaries (PE add-on acquisitions)

**Prophix Advantages** (worth $165K savings?):
- **Driver-based automation**: Manufacturing-specific (capacity, production volume)
- **140+ audit reports**: PE compliance (vs Planful custom reports)
- **Faster implementation**: 6-12 weeks vs 12-24 weeks (2-3 month time savings)

**Key Question**: Will PE add 5+ more subsidiaries in 3 years (complex consolidation)?

**If Yes**: Planful worth premium (enterprise-grade consolidation)
**If No (3-5 subsidiaries)**: Prophix wins ($165K savings fund future migration if needed)

---

## Implementation Considerations

### Prophix Implementation Path (6-12 Weeks)

**Weeks 1-2: Discovery & Planning**
- Requirements workshops: Consolidation rules, IC eliminations, FX translation
- NetSuite data mapping: Chart of accounts, subsidiaries, cost centers
- Driver-based planning: Capacity utilization, production volume, overhead allocation
- Project plan: Milestones, resources, go-live date

**Weeks 3-6: Configuration & Development**
- NetSuite integration: Configure connector, test data sync
- Entity structure: 3 subsidiaries, intercompany relationships
- Multi-currency: CAD → USD translation, monthly FX rates
- Driver-based models: Production volume → labor hours → overhead
- Consolidation rules: IC eliminations (300+ transactions), CTA calculation

**Weeks 7-10: Data Migration & Testing**
- Historical data: 2.5 years NetSuite actuals
- Consolidation testing: Validate IC eliminations (spot check 50+ transactions)
- FX testing: Compare Excel manual translation vs Prophix automated
- User acceptance testing: FP&A manager + controller validate reports

**Weeks 11-12: Training & Go-Live**
- Administrator training: 2-day session (FP&A manager + controller)
- Power user training: 1-day session (finance analysts)
- Parallel run: Prophix + Excel consolidation (1 month-end cycle)
- Go-live: Switch to Prophix for Q2 budget cycle (April)

**Total Time**: 320-480 hours (FP&A manager + controller + analysts)

**Success Factors**:
- Clean NetSuite data (fix GL errors before migration)
- Complete IC transaction mapping (identify all intercompany accounts)
- Manufacturing driver documentation (production capacity, labor standards)

---

### Vena Implementation Path (4-12 Weeks)

**Weeks 1-3: Requirements & Configuration**
- Discovery: Consolidation requirements, NetSuite integration
- NetSuite connector setup: 3-5 days
- Entity structure: 3 subsidiaries, IC eliminations
- Multi-currency: CAD → USD, FX rates

**Weeks 4-8: Model Building**
- Excel templates: Migrate existing Excel consolidation to Vena
- Driver-based planning: Build formulas (capacity utilization, production volume)
- Consolidation rules: IC eliminations, CTA calculation
- Budget templates: Department-level budgets (5 departments × 3 subsidiaries)

**Weeks 9-12: Testing & Go-Live**
- Data migration: 2.5 years NetSuite actuals
- Consolidation testing: Validate IC eliminations
- Training: Excel-native (minimal training needed)
- Go-live: Q2 budget cycle

**Total Time**: 240-360 hours (less than Prophix due to Excel familiarity)

**Success Factors**:
- Leverage existing Excel templates (migrate vs rebuild)
- Excel expertise (team comfortable with Vena Excel interface)

---

## Cost Analysis (3-Year TCO)

### Prophix Total Cost of Ownership

**Software Costs**:
- Year 1: $75,000 (500 employees) + $30,000 implementation = $105,000
- Year 2: $80,000 (525 employees, 5% growth)
- Year 3: $85,000 (550 employees, 5% growth)
- **Total Software**: $240,000

**Implementation Costs**:
- Professional services: $25,000 (guided setup, NetSuite integration)
- Internal team time: 320-480 hours × $150/hour (loaded) = $48,000-72,000
- **Total Implementation**: $78,000

**Ongoing Costs**:
- Manual ADP sync: 8 hours/month × 36 months × $100/hour = $28,800
- Training: $3,000/year × 3 years = $9,000
- Ongoing consulting: $5,000/year × 3 years = $15,000 (workflow updates)
- **Total Ongoing**: $52,800

**3-Year TCO**: $240,000 + $78,000 + $52,800 = **$370,800**

**Cost Per Employee**: $370,800 ÷ 525 avg employees ÷ 3 years = **$235/employee/year**

---

### Vena Total Cost of Ownership

**Software Costs**:
- Year 1: $55,000 (500 employees) + $20,000 implementation = $75,000
- Year 2: $60,000 (525 employees)
- Year 3: $65,000 (550 employees)
- **Total Software**: $180,000

**Implementation Costs**:
- Professional services: $15,000 (guided setup)
- Internal team time: 240-360 hours × $150/hour = $36,000-54,000
- **Total Implementation**: $56,000

**Ongoing Costs**:
- Manual ADP sync: 8 hours/month × 36 months × $100/hour = $28,800
- Training: $2,000/year × 3 years = $6,000
- Ongoing support: $2,000/year × 3 years = $6,000
- **Total Ongoing**: $40,800

**3-Year TCO**: $180,000 + $56,000 + $40,800 = **$276,800**

**Cost Per Employee**: $276,800 ÷ 525 avg employees ÷ 3 years = **$176/employee/year**

---

### Cost-Benefit Analysis

**Finance Team Time Savings** (Automated Consolidation):
- Eliminate manual IC eliminations: 2-3 days/month × 12 months = 24-36 days/year = 192-288 hours/year
- Automated FX translation: 4-6 hours/month × 12 months = 48-72 hours/year
- Driver-based planning: Save 10-20 hours/month = 120-240 hours/year
- **Total Time Savings**: 360-600 hours/year × $150/hour = **$54,000-90,000/year**

**3-Year Benefit**: $162,000-270,000

**ROI Calculation**:
- Prophix: $270,000 benefit ÷ $370,800 cost = **73% ROI** (payback 20 months)
- Vena: $270,000 benefit ÷ $276,800 cost = **98% ROI** (payback 12 months)

**Insight**: Both platforms excellent ROI. Vena faster payback (lower cost), Prophix higher long-term value (automation).

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 300+
**Purpose**: Generic scenario demonstrating consolidation requirements for mid-market manufacturing
**Approach**: Hardware store model (show options, not prescribe choice)

**Key Pattern Demonstrated**:
1. Requirements → Consolidation filtering (excludes Runway, Causal)
2. Consolidation → Budget filtering (excludes Adaptive, OneStream, Anaplan)
3. Budget → Feature matching (Prophix automation vs Vena Excel familiarity vs Planful NetSuite partnership)
4. Quantified trade-off: Prophix automation value ($63K-126K) > $95K premium over Vena

**Limitations**:
- Generic scenario (not real client)
- Assumes 3-subsidiary structure stable (PE may add more acquisitions)
- ROI calculation assumes full time savings (conservative: 70-80% actual)
- Driver-based planning complexity varies by manufacturing process
