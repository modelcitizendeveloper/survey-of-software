# S3 Scenario: Enterprise Migration (2,000 Employees)

**Experiment**: 3.007 FP&A Platforms
**Stage**: S3 - Need-Driven Discovery
**Date**: November 1, 2025
**Scenario Type**: Generic Profile (not client-specific)

---

## Scenario Context

**Company Profile**:
- Industry: Professional services (consulting, staffing)
- Employee count: 2,000 (current), stable headcount
- Revenue: $800M (current), 5-8% organic growth
- Structure: Single legal entity, 8 business units, 25 offices (US + Canada)
- Ownership: Public company (regional exchange)

**Finance Team**:
- CFO: Full-time (5 years tenure)
- VP FP&A: 1 FTE (oversees planning, forecasting, board reporting)
- FP&A Managers: 3 FTEs (corporate, business unit, operational planning)
- Finance Analysts: 8 FTEs (division-level budgeting, variance analysis, ad-hoc)
- Accounting/Reporting: 15 FTEs (separate from FP&A)
- Current FP&A tools: Oracle Hyperion Planning (10+ years old), Excel supplements

**Technical Environment**:
- ERP: Oracle E-Business Suite (Financials only, 15+ years old)
- Legacy FP&A: Oracle Hyperion Planning (on-premise, EOL approaching)
- HRIS: Migrating from Oracle HCM Cloud to Paycom (implementation in progress)
- BI Tool: Tableau (operational dashboards, not integrated with FP&A)

**Migration Context**:
- Oracle HCM Cloud sunset: Migrating to Paycom (cost reduction, modern UX)
- Oracle Hyperion EOL: Oracle forcing migration to Oracle Cloud EPM (expensive, low satisfaction)
- Current Hyperion cost: $500K+/year (licenses + infrastructure + support + consultants)
- Migration drivers: Reduce cost, improve UX, escape Oracle lock-in

**Pain Points**:
- Oracle Hyperion slow (10-15 minute load times for reports)
- Hyperion UX terrible (1990s interface, extensive training required)
- Oracle Cloud EPM migration: Oracle quoting $1.2M+ 3-year TCO (unaffordable)
- On-premise infrastructure: $100K+/year maintenance (servers, DBAs, backups)
- Consultant dependency: $150K/year ongoing Oracle Hyperion support

---

## Requirements Analysis

### Primary Requirements

**1. Oracle Financials ERP Integration (Must Keep)**
- Constraint: Cannot migrate Oracle Financials (15+ years customization, $5M+ re-implementation cost)
- Historical data: 15+ years in Oracle EBS (General Ledger, AP, AR, Fixed Assets)
- Chart of accounts: 2,000+ accounts (complex business unit, office, project tracking)
- Customizations: 50+ custom GL segments, custom workflow approvals
- Sync frequency: Daily (month-end close requires up-to-date actuals)

**2. Cost Reduction (Target: 50% Reduction)**
- Current FP&A total cost: $500K+/year (Hyperion licenses $200K, infrastructure $100K, consultants $150K, internal support $50K)
- Target 3-year TCO: $750K-1M total (vs $1.5M+ current trajectory)
- Desired savings: $250K-500K/year (50%+ reduction)
- Justification: CFO mandate to reduce IT spend, improve efficiency

**3. Improved User Experience**
- Current pain: Hyperion 1990s interface (extensive training, low adoption)
- Desired state: Modern web-based UX (Tableau-like experience)
- Adoption goal: Reduce training time 75% (from 3-day bootcamp to half-day onboarding)
- Mobile access: Board wants iPad access (Hyperion desktop-only)

**4. Paycom HRIS Integration**
- Migration status: Oracle HCM Cloud → Paycom (go-live in 3 months)
- Headcount planning: 2,000 employees across 8 business units, 25 offices
- Current gap: Hyperion has Oracle HCM integration (will break when Paycom goes live)
- Need: Paycom integration to maintain headcount planning automation

**5. Implementation Timeline (4-6 Months)**
- Constraint: Annual budget cycle starts in 6 months (need platform live)
- Resource availability: FP&A team 50% time, IT support 20 hours/week
- Consulting acceptable: Implementation partner with Oracle Hyperion migration experience
- Avoid: Disruption to current planning cycle (parallel run acceptable)

### Secondary Requirements

**6. Maintain Current Functionality**
- Hyperion features in use: Driver-based planning, multi-level approvals, complex workflows
- Historical models: 10+ years budget/forecast history (must migrate or archive)
- User base: 150+ users (executives, managers, analysts across business units)
- Reporting: 200+ pre-built reports (board decks, variance analysis, KPIs)

**7. Scalability (Stable Headcount, Growing Complexity)**
- Headcount: 2,000 employees stable (not growing)
- Business complexity: Growing (new service lines, geographic expansion)
- Future needs: Potential international expansion (multi-currency) in 3-5 years

**8. Avoid Oracle Lock-In**
- Strategic mandate: Reduce Oracle footprint (keeping Oracle Financials, exit everything else)
- Oracle Cloud EPM rejected: Expensive ($1.2M+ 3-year TCO), forced migration
- Vendor preference: Independent software vendor (not Oracle, not SAP)

---

## Applying S2 Catalog Data

### Step 1: Filter by Oracle Financials ERP Integration

**Critical Requirement: Oracle EBS / Oracle Financials Cloud Support**

From S2 Integration Matrix (Oracle ERP Support):
- ✅ **Adaptive**: Native Oracle integration (S2 Integrations, line 77)
- ✅ **Anaplan**: Native Oracle integration (CloudWorks) (S2 Integrations, line 77)
- ✅ **OneStream**: Native Oracle integration (S2 Integrations, line 77)
- ✅ **Planful**: Native Oracle integration (S2 Integrations, line 77)
- ✅ **Prophix**: Native Oracle integration (S2 Integrations, line 77)
- ⚠️ **Vena**: API available (not native) (S2 Integrations, line 77)
- ❌ **Runway**: No Oracle support (SMB focus) (S2 Integrations, line 77)
- ❌ **Causal**: No Oracle support (S2 Integrations, line 77)

**Result**: Adaptive, Anaplan, OneStream, Planful, Prophix support Oracle natively. Runway and Causal excluded (SMB-focused).

**Oracle Integration Setup** (From S2):
- Standard: 3-5 days for native connectors
- Complex: 2-4 weeks for custom GL segments, workflows

---

### Step 2: Filter by Cost Reduction Target

**Requirement: 50% Cost Reduction (Current $500K+/year → Target $250K/year max)**

**Current Oracle Hyperion Total Cost**:
- Licenses: $200K/year
- Infrastructure: $100K/year (on-premise servers, DBAs)
- Consultants: $150K/year (ongoing support)
- Internal support: $50K/year (FP&A team time)
- **Total**: $500K+/year

**Target 3-Year TCO**: $750K-1M total ($250K-330K/year average)

From S2 Pricing Analysis (2,000 Employees):

| Platform | Year 1 | Year 2 | Year 3 | 3-Year Total | Cost Reduction? |
|----------|--------|--------|--------|--------------|-----------------|
| **Vena** | $120K + $30K impl | $130K | $140K | **$540K** ✅ (64% savings) |
| **Prophix** | $180K + $50K impl | $200K | $220K | **$830K** ✅ (45% savings) |
| **Planful** | $350K + $150K impl | $380K | $410K | **$1,440K** ⚠️ (4% savings) |
| **Adaptive** | $350K + $150K impl | $380K | $410K | **$1,440K** ⚠️ (4% savings) |
| **OneStream** | $400K + $200K impl | $430K | $460K | **$1,690K** ❌ (13% increase) |
| **Anaplan** | $500K + $250K impl | $550K | $600K | **$2,150K** ❌ (43% increase) |

**Current 3-Year Trajectory**: $500K × 3 years = $1.5M (excluding infrastructure decommission savings)

**Result**: Vena ($540K) and Prophix ($830K) achieve cost reduction targets. Planful/Adaptive marginal savings. OneStream/Anaplan cost increases.

**Note**: Vena and Prophix also eliminate $100K/year infrastructure costs (on-premise → SaaS), adding $300K savings over 3 years.

**Adjusted TCO** (including infrastructure savings):
- **Vena**: $540K - $300K = **$240K net** (84% cost reduction)
- **Prophix**: $830K - $300K = **$530K net** (65% cost reduction)

---

### Step 3: Filter by Implementation Timeline

**Requirement: 4-6 Month Implementation (Pre-Budget Cycle)**

From S2 Implementation Complexity Matrix (Oracle Hyperion Migration):
- 🟡 **Vena**: 4-12 weeks typical, but Hyperion migration adds 2-3 months (total 4-5 months)
- 🟡 **Prophix**: 6-12 weeks typical, Hyperion migration adds 2-3 months (total 4-6 months)
- 🔴 **Planful**: 12-24 weeks baseline, Hyperion migration adds 2-4 months (total 6-10 months)
- 🔴 **Adaptive**: 8-16 weeks baseline, Hyperion migration adds 2-3 months (total 5-8 months)
- 🔴 **OneStream**: 12-24 weeks baseline, Hyperion migration adds 3-6 months (total 7-12 months)
- 🔴 **Anaplan**: 16-48 weeks baseline, Hyperion migration adds 4-6 months (total 8-16 months)

**Result**: Vena (4-5 months) and Prophix (4-6 months) fit timeline. Others exceed 6 months.

**Migration Complexity Factors**:
- Historical data: 10+ years Hyperion budgets/forecasts (data extraction, cleansing)
- Model complexity: Driver-based planning, workflow approvals (re-build in new platform)
- User training: 150+ users (Hyperion experts must learn new platform)
- Parallel run: 2-3 month-end cycles (Hyperion + new platform side-by-side)

---

### Step 4: Filter by Paycom HRIS Integration

**Requirement: Paycom Integration (Launching in 3 Months)**

From S2 Integration Matrix (Paycom HRIS Support):
- ⚠️ **Adaptive**: iPaaS required (Boomi, Workato) (S2 Integrations, line 42)
- ❌ **Anaplan**: No documented Paycom integration (S2 Integrations, line 42)
- ❌ **OneStream**: No documented Paycom integration (S2 Integrations, line 42)
- 🔧 **Planful**: iPaaS required (S2 Integrations, line 42)
- 🔧 **Prophix**: iPaaS required (S2 Integrations, line 42)
- ⚠️ **Runway**: API available (S2 Integrations, line 42)
- 🔧 **Vena**: iPaaS required (S2 Integrations, line 42)

**Result**: No platform offers native Paycom integration (Paycom enterprise HRIS less common). All require iPaaS or custom API.

**iPaaS Cost** (From S2):
- iPaaS tools: $10K-50K/year (Boomi, Workato, Mulesoft)
- Setup: 2-4 weeks, $10K-30K one-time
- Ongoing maintenance: $5K-10K/year

**Note**: Paycom integration cost similar across platforms (table stakes enterprise iPaaS requirement).

---

### Step 5: Cross-Reference UX & Feature Parity

**Modern UX Requirement**:

From S2 Feature Matrix (User Experience):
- **Vena**: Excel-native (familiar but not web-native modern UX) (S2 Features, line 430)
- **Prophix**: Web-based (modern UX improvements in Prophix One 2024) (S2 Features, line 294)
- **Planful**: Web-based, dynamic planning grid (S2 Features, line 289)
- **Adaptive**: Web-based (Workday design language) (S2 Features, line 269)
- **OneStream**: Web-based (enterprise UX) (S2 Features, line 284)
- **Anaplan**: Web-based (enterprise UX) (S2 Features, line 274)

**Hyperion Feature Parity**:

From S2 Feature Matrix (Driver-Based Planning, Workflows):
- ✅ **All platforms**: Driver-based planning, multi-level approvals, complex workflows supported (S2 Features, lines 83-143)

**Mobile Access**:

From S2 Feature Matrix:
- ✅ **Most platforms**: Mobile view access (read-only or limited edit) (S2 Features, line 143)

---

## Platform Matching Results

### Platforms Matching All Requirements

**1. Prophix**

**Match Score**: 90% (best balance of cost reduction + Oracle integration + timeline + UX)

**Strengths for This Scenario**:
- **Cost reduction**: $530K 3-year net TCO (65% savings vs current $1.5M) (S2 Pricing, line 381)
- **Oracle Financials integration**: Native (S2 Integrations, line 77)
- **Implementation**: 4-6 months (fits budget cycle timeline)
- **Modern UX**: Prophix One unified platform (2024 launch) (S2 Features, line 294)
- **Hyperion migration**: Established migration path (10+ years competitors)
- **Driver-based planning**: Core strength (automation focus) (S2 Features, line 294)
- **No Oracle lock-in**: Independent vendor (not Oracle/SAP)

**Limitations for This Scenario**:
- **Paycom integration**: iPaaS required ($10K-30K setup, $10K-20K/year ongoing) (S2 Integrations, line 42)
- **Mid-market positioning**: Stretching to 2,000 employees (designed for 500-2,000) (S2 Pricing, line 211)
- **Feature depth**: Less comprehensive than Anaplan/OneStream (82% coverage vs 88-90%) (S2 Features, line 228)

**Data from S2**:
- Oracle integration: Native connector (S2 Integrations, line 77)
- Implementation: 6-12 weeks, Hyperion migration adds 2-3 months (S2 Implementation, line 38)
- Pricing: $180K-220K/year for 2,000 employees (S2 Pricing, line 211)
- Cost reduction: $1.5M current → $830K new = $670K savings (45% reduction)
- Infrastructure savings: $300K (on-premise → SaaS) = **$970K total savings** (65%)

**Why This Fits**:
- **Cost-driven migration**: 65% total cost reduction (CFO mandate met)
- **Fast implementation**: 4-6 months (fits budget cycle)
- **Oracle independence**: Escape Oracle lock-in (strategic goal)
- **Mid-market leader**: 2,000 employees upper range but supported

---

**2. Vena**

**Match Score**: 80% (best cost reduction, but Excel-native UX may not meet "modern" requirement)

**Strengths for This Scenario**:
- **Cost reduction**: $240K 3-year net TCO (84% savings vs current $1.5M) (S2 Pricing, line 382)
- **Oracle integration**: API available (not native, but workable) (S2 Integrations, line 77)
- **Implementation**: 4-5 months (fits budget cycle timeline)
- **Excel familiarity**: Zero learning curve for Excel-based team (may reduce training time)
- **Scalability**: 100-2,000 employees sweet spot (S2 Pricing, line 277)

**Limitations for This Scenario**:
- **UX concern**: Excel-native (not web-based modern UX) - may not meet "improve UX" requirement
- **Oracle integration**: API-based (not native) - requires 1-2 weeks custom setup (S2 Integrations, line 77)
- **Paycom integration**: iPaaS required ($10K-30K setup, $10K-20K/year ongoing)
- **Excel dependency**: May feel like lateral move (Hyperion → Excel-based platform)

**Data from S2**:
- Oracle integration: API available (S2 Integrations, line 77)
- Implementation: 1-3 months baseline, Hyperion migration adds 2-3 months (S2 Implementation, line 37)
- Pricing: $120K-140K/year for 2,000 employees (S2 Pricing, line 277)
- Cost reduction: $1.5M current → $540K new = $960K savings (64% reduction)
- Infrastructure savings: $300K = **$1.26M total savings** (84%)

**Why This Fits**:
- **Maximum cost reduction**: 84% savings (best financial outcome)
- **Fast implementation**: 4-5 months (meets timeline)
- **Excel familiarity**: Reduce training burden (10+ years Excel supplements)

**Why This Might Not Fit**:
- **UX expectation**: Excel-native may not satisfy "modern UX" requirement (CFO wants Tableau-like)
- **Strategic vision**: Excel feels like step backwards (not transformational)

---

### Platforms NOT Matching Requirements (But Worth Considering)

**3. Planful**

**Match Score**: 60% (marginal cost reduction, long implementation)

**Why Considered**:
- ✅ Oracle Financials integration: Native (S2 Integrations, line 77)
- ✅ Enterprise-grade: 2,000 employees well within range (S2 Pricing, line 171)
- ✅ Feature depth: 87% coverage (S2 Features, line 226)

**Why Excluded**:
- ❌ Cost reduction: Only 4% savings ($1.44M vs $1.5M) (S2 Pricing, line 379)
- ❌ Implementation: 6-10 months (misses budget cycle timeline) (S2 Implementation, line 40)
- ⚠️ Cost justification: Hard to justify migration for 4% savings (disruption not worth it)

**Scenario Where Planful Fits**:
- If cost reduction NOT primary driver (focus on functionality upgrade)
- If 6-10 month timeline acceptable (budget cycle can wait)
- If need enterprise-grade platform (future-proof for 5,000+ employees)

---

**4. Adaptive Insights**

**Match Score**: 55% (marginal cost reduction, Workday ecosystem bias)

**Why Considered**:
- ✅ Oracle integration: Native (S2 Integrations, line 77)
- ✅ Enterprise-grade: 2,000 employees within range (S2 Pricing, line 171)
- ✅ #1 satisfaction: G2 leader (S2 Features, line 412)

**Why Excluded**:
- ❌ Cost reduction: Only 4% savings ($1.44M vs $1.5M) (S2 Pricing, line 380)
- ❌ Workday bias: Optimized for Workday HCM customers (not applicable with Paycom) (S2 Integrations, line 326)
- ❌ Implementation: 5-8 months (may miss budget cycle) (S2 Implementation, line 39)

**Scenario Where Adaptive Fits**:
- If company using Workday HCM (not Paycom) - native integration advantage
- If cost reduction secondary to functionality (willing to pay premium)

---

**5. OneStream**

**Match Score**: 45% (cost increase, slow implementation)

**Why Considered**:
- ✅ Unified CPM: Consolidation + planning + close + reporting (one platform) (S2 Features, line 284)
- ✅ Oracle integration: Native (S2 Integrations, line 77)
- ✅ Enterprise-grade: 2,000-50,000 employees (S2 Pricing, line 135)

**Why Excluded**:
- ❌ **Cost increase**: $1.69M 3-year TCO (13% more expensive than current $1.5M) (S2 Pricing, line 386)
- ❌ Implementation: 7-12 months (far exceeds timeline) (S2 Implementation, line 41)
- ❌ Defeats purpose: Migration to reduce cost, OneStream increases cost

**Scenario Where OneStream Fits**:
- If company needs unified CPM (close + consolidation + planning in one platform)
- If cost reduction NOT priority (willing to pay premium for functionality)
- If 7-12 month timeline acceptable

---

**6. Anaplan**

**Match Score**: 35% (major cost increase, very long implementation)

**Why Considered**:
- ✅ Connected planning: Finance + sales + supply chain (S2 Features, line 274)
- ✅ Oracle integration: Native via CloudWorks (S2 Integrations, line 77)

**Why Excluded**:
- ❌ **Cost increase**: $2.15M 3-year TCO (43% more expensive than current) (S2 Pricing, line 377)
- ❌ Implementation: 8-16 months (far exceeds timeline) (S2 Implementation, line 42)
- ❌ Overkill: Connected planning not needed (finance-only use case)

---

## Key Trade-offs

### Prophix vs Vena Decision Framework

**Choose Prophix if**:
- Modern web-based UX critical (strategic mandate to escape Hyperion 1990s interface)
- Driver-based planning automation important (capacity utilization, project-based drivers)
- Willing to accept 65% cost savings vs 84% (moderate cost reduction acceptable)
- Oracle native integration preferred (vs API-based)
- Budget allows $830K vs $540K (32% premium for web-native UX)

**Choose Vena if**:
- Maximum cost reduction priority (84% savings vs 65%)
- Excel familiarity valued (reduce training, leverage existing Excel expertise)
- Can accept Excel-native UX (not web-based modern)
- API-based Oracle integration acceptable (1-2 weeks custom setup)
- Budget tightest constraint ($240K net TCO vs $530K)

---

### Quantified Trade-off Analysis

**Prophix vs Vena**: $290K difference over 3 years ($530K vs $240K net TCO)

**Prophix Advantages** (worth $290K premium?):
- **Web-based UX**: Reduce training time 75% (from 3-day bootcamp to half-day) = 150 users × 16 hours saved × $100/hour = $240,000 one-time
- **Driver-based automation**: Save 20-40 hours/month manual Excel driver updates = 240-480 hours/year × $150/hour = $36,000-72,000/year × 3 years = $108,000-216,000
- **Total value**: $348,000-456,000

**Answer**: Prophix web UX + automation justifies $290K premium (ROI 20-57%).

**Vena Advantages** (worth $290K savings?):
- **Maximum cost reduction**: $290K savings vs Prophix
- **Excel familiarity**: Leverage 10+ years Excel expertise (minimal training)
- **Faster implementation**: 4-5 months vs 4-6 months (save 2-4 weeks)

**Key Question**: Is modern web-based UX strategic priority or nice-to-have?

**If Strategic Priority** (CFO mandate to improve UX): **Prophix wins** (web UX value $348K-456K > $290K cost)
**If Cost Reduction Primary**: **Vena wins** ($290K savings direct to bottom line)

---

## Implementation Considerations

### Prophix Hyperion Migration Path (4-6 Months)

**Month 1: Discovery & Planning**
- Hyperion audit: Document models, workflows, reports (200+ reports inventory)
- Requirements: Oracle Financials integration, Paycom iPaaS, driver-based planning
- Data extraction: 10+ years Hyperion budgets/forecasts (metadata mapping)
- Project plan: Milestones, resources, parallel run strategy

**Month 2-3: Configuration & Development**
- Oracle Financials integration: Configure connector, test 2,000+ GL accounts
- Paycom iPaaS: Boomi/Workato setup (2-4 weeks)
- Model migration: Rebuild Hyperion models in Prophix (driver-based planning)
- Workflow setup: Multi-level approvals, business unit routing

**Month 4: Data Migration & Testing**
- Historical data: 3-5 years actuals + budgets (test data integrity)
- Model testing: Driver-based calculations, workflow approvals
- User acceptance testing: 150+ users (executives, managers, analysts)
- Performance testing: Report load times (10-15 min Hyperion → <1 min Prophix target)

**Month 5-6: Training & Go-Live**
- Administrator training: 3-day session (FP&A managers)
- Power user training: 2-day session (finance analysts)
- End user training: Half-day workshops (executives, managers)
- Parallel run: 2-3 month-end cycles (Hyperion + Prophix side-by-side)
- Go-live: Cutover for annual budget cycle
- Hyperion decommission: Archive data, shut down servers (save $100K/year infrastructure)

**Total Time**: 800-1,200 hours (FP&A team + IT + implementation partner)

**Success Factors**:
- Clean Hyperion data export (metadata integrity)
- Oracle Financials custom GL segment mapping (50+ custom segments)
- User buy-in (150+ users must adopt new platform)
- Executive sponsorship (CFO champions migration)

---

### Vena Hyperion Migration Path (4-5 Months)

**Month 1: Discovery & Planning**
- Hyperion audit: Document Excel supplements (leverage existing Excel expertise)
- Requirements: Oracle API integration, Paycom iPaaS, Excel template migration
- Data extraction: 10+ years Hyperion data

**Month 2-3: Configuration & Development**
- Oracle API integration: Custom connector setup (1-2 weeks)
- Paycom iPaaS: Boomi setup
- Excel template migration: Convert Hyperion models to Vena Excel templates
- Leverage existing Excel supplements: Minimal re-build (team already uses Excel)

**Month 4-5: Testing & Go-Live**
- Data migration: 3-5 years actuals + budgets
- User acceptance testing: Excel-native (minimal training needed)
- Parallel run: 2 month-end cycles
- Go-live: Annual budget cycle
- Hyperion decommission: Save $100K/year infrastructure

**Total Time**: 600-800 hours (less than Prophix due to Excel familiarity)

**Success Factors**:
- Leverage existing Excel expertise (10+ years supplements)
- Oracle API integration (test custom GL segments)
- Accept Excel-native UX (strategic alignment question)

---

## Cost Analysis (3-Year TCO)

### Prophix Total Cost of Ownership

**Software Costs**:
- Year 1: $180,000 + $50,000 implementation = $230,000
- Year 2: $200,000
- Year 3: $220,000
- **Total Software**: $600,000

**Implementation Costs**:
- Professional services: $40,000 (Hyperion migration specialist)
- Internal team time: 800-1,200 hours × $150/hour = $120,000-180,000
- Paycom iPaaS: $20,000 setup, $15,000/year ongoing × 3 years = $65,000
- **Total Implementation**: $230,000

**Ongoing Costs**:
- iPaaS maintenance: Included above
- Training: $10,000/year × 3 years = $30,000
- Ongoing consulting: $0 (self-sufficient after migration)
- **Total Ongoing**: $30,000

**3-Year TCO**: $600,000 + $230,000 + $30,000 = **$860,000**

**Infrastructure Savings**: Decommission Hyperion on-premise = $100,000/year × 3 years = $300,000

**Net 3-Year TCO**: $860,000 - $300,000 = **$560,000**

**Current Trajectory**: $500,000/year × 3 years = $1,500,000

**Cost Reduction**: $1,500,000 - $560,000 = **$940,000 savings (63%)**

---

### Vena Total Cost of Ownership

**Software Costs**:
- Year 1: $120,000 + $30,000 implementation = $150,000
- Year 2: $130,000
- Year 3: $140,000
- **Total Software**: $390,000

**Implementation Costs**:
- Professional services: $25,000 (guided setup)
- Internal team time: 600-800 hours × $150/hour = $90,000-120,000
- Oracle API integration: $10,000 custom setup
- Paycom iPaaS: $20,000 setup, $15,000/year × 3 years = $65,000
- **Total Implementation**: $215,000

**Ongoing Costs**:
- iPaaS maintenance: Included above
- Training: $5,000/year × 3 years = $15,000
- Oracle API maintenance: $5,000/year × 3 years = $15,000
- **Total Ongoing**: $30,000

**3-Year TCO**: $390,000 + $215,000 + $30,000 = **$635,000**

**Infrastructure Savings**: $300,000

**Net 3-Year TCO**: $635,000 - $300,000 = **$335,000**

**Cost Reduction**: $1,500,000 - $335,000 = **$1,165,000 savings (78%)**

---

### Cost-Benefit Analysis

**Finance Team Time Savings** (Both Platforms):
- Eliminate Hyperion slow load times: 10-15 min → <1 min per report = 150 reports/day × 14 min × 240 days = 8,400 hours/year
- Modern UX (web vs desktop): Save 2-3 hours/week per user × 150 users = 300-450 hours/week × 48 weeks = 14,400-21,600 hours/year
- Infrastructure elimination: Save $100,000/year
- **Total Time Savings**: 22,800-30,000 hours/year × $100/hour = **$2.28M-3M/year**

**3-Year Benefit**: $6.84M-9M (massive time savings)

**ROI Calculation**:
- Prophix: $9M benefit ÷ $560K cost = **1,507% ROI** (payback 2 months)
- Vena: $9M benefit ÷ $335K cost = **2,585% ROI** (payback 1 month)

**Insight**: Both platforms have exceptional ROI. Hyperion inefficiency so severe that ANY modern platform delivers 15-25x ROI.

---

## Document Metadata

**Created**: November 1, 2025
**Lines**: 300+
**Purpose**: Generic scenario demonstrating enterprise migration cost reduction requirements
**Approach**: Hardware store model (show options, not prescribe choice)

**Key Pattern Demonstrated**:
1. Requirements → Oracle Financials integration (excludes Runway, Causal)
2. Oracle → Cost reduction filtering (excludes OneStream, Anaplan; marginal for Planful/Adaptive)
3. Cost reduction → Prophix/Vena emerge (65-78% savings)
4. Quantified trade-off: Prophix web UX value ($348K-456K) vs Vena cost savings ($290K)

**Limitations**:
- Generic scenario (not real client)
- Assumes Hyperion inefficiency severe (10-15 min load times)
- ROI calculation assumes full time savings (conservative: 50-70% actual)
- Paycom iPaaS cost similar across platforms (not differentiator)
