# 3.503: HRIS/HCM Platforms - Experiment Scope

**Experiment ID**: 3.503
**Category**: Business Platforms (3.500-599)
**Status**: In Progress - S1 Rapid Discovery
**Started**: October 31, 2025
**Research Lead**: Ivan

---

## Experiment Trigger

**Market Validation**: Real CFO LinkedIn Community post (October 31, 2025):

> "I am researching the use of Paycom as a replacement for Oracle HCM for a former employer. The organization is considering moving away from Oracle HCM but keeping Financials & SCM... 2k employees with UKG for time capture."

**Key Issues Identified**:
- User experience challenges with Oracle HCM
- Difficulty retaining functional/technical expertise
- Need to keep costs flat
- Avoid disrupting payroll/accounting processes
- Integration complexity (time tracking, accounting, benefits)

**Strategic Importance**:
- Every company 10+ employees needs HRIS
- High-value decisions ($50K-500K annual spend)
- Integration affects multiple systems (accounting, FP&A, payroll)
- Critical operations (payroll cannot fail)

---

## Domain Definition

**HRIS**: Human Resources Information System
**HCM**: Human Capital Management (broader than HRIS, includes talent management)

**Core Scope**: Systems that manage employee data, payroll, benefits, time tracking, recruiting, performance, and learning.

**NOT in Scope**:
- Pure ATS (Applicant Tracking Systems) without full HRIS features
- Learning Management Systems (LMS) as standalone products
- Background check services
- Benefits brokers/PEO services (unless technology platform)

---

## Research Questions

### Primary Questions

1. **When to use HRIS vs PEO vs Payroll-Only Service?**
   - Company size triggers (10 vs 50 vs 250 vs 2000 employees)
   - Complexity factors (multi-state, international, benefits)
   - Control vs outsourcing trade-offs

2. **Oracle HCM Migration Framework**
   - Why do companies leave Oracle HCM? (Post 2 scenario)
   - What are viable alternatives at 2000+ employee scale?
   - How to minimize disruption during payroll cutover?

3. **Integration Architecture**
   - HRIS → Accounting (payroll journal entries)
   - HRIS → FP&A (headcount forecasting)
   - Time tracking → Payroll (UKG, Kronos, Deputy)
   - Benefits administration → Insurance carriers

4. **Build vs Buy Decision**
   - When is custom payroll system justified? (Tier 1 DIY)
   - When to use payroll APIs (Gusto, Check, Finch)? (Tier 2)
   - When to use full HRIS platforms? (Tier 3)

5. **Employee Count Graduation Triggers**
   - 1-10 employees: Manual/spreadsheet → ?
   - 10-50 employees: ? (Gusto, Rippling, Justworks)
   - 50-250 employees: ? (BambooHR, Paylocity, Namely)
   - 250-2000 employees: ? (Paycom, ADP Workforce Now, UKG Pro)
   - 2000+ employees: ? (Workday, Oracle HCM, SAP SuccessFactors)

### Secondary Questions

6. **AI Capabilities** (MPSE v3.0)
   - Conversational HR assistants
   - Predictive analytics (turnover prediction, flight risk)
   - Resume parsing and candidate matching
   - Policy question answering
   - Performance review analysis

7. **Single-Platform vs Best-of-Breed**
   - All-in-one (Rippling, Paycom) vs modular (BambooHR + Gusto + Lattice)
   - Integration overhead vs single vendor lock-in
   - Cost comparison: bundled vs unbundled

8. **Implementation Complexity**
   - Payroll cutover strategies (parallel runs, validation)
   - Historical data migration (7+ years required)
   - Benefits enrollment timing (avoid open enrollment)
   - Employee self-service adoption

9. **Compliance & Security**
   - Multi-state tax compliance
   - International payroll (Canada, UK, global)
   - SOC 2, GDPR, data privacy
   - Audit trails and reporting

10. **Cost Structure**
    - Per-employee-per-month (PEPM) pricing models
    - Implementation fees (setup, migration, training)
    - Annual vs monthly contracts
    - Hidden costs (integrations, customizations, support tiers)

---

## Platform Universe (Initial List)

### Tier 1: Startup/SMB (10-250 employees)

**All-in-One Platforms**:
- **Rippling** - Modern, fast setup, device management included
- **Gusto** - Payroll-first, simple, popular with startups
- **Justworks** - PEO model, outsourced HR + benefits
- **Paycor** - SMB focus, strong payroll + HR

**HR-First (No Payroll)**:
- **BambooHR** - HR management, integrates with payroll providers
- **Namely** - HR + payroll + benefits for 25-1000 employees

**Payroll-Only (Lightweight)**:
- **OnPay** - Simple payroll, no HR bells/whistles
- **SurePayroll** - Paychex's SMB product

### Tier 2: Mid-Market (250-2000 employees)

- **Paycom** - Single database, employee self-service (Beti)
- **ADP Workforce Now** - Established, comprehensive
- **Paylocity** - Strong payroll + HR, modern interface
- **UKG Pro** - Formerly Ultimate Software, enterprise-lite
- **Namely** - Scales from 25-1000 employees

### Tier 3: Enterprise (2000+ employees)

- **Workday HCM** - Modern cloud, comprehensive, expensive
- **Oracle HCM Cloud** - Complex, powerful, requires expertise
- **SAP SuccessFactors** - Global, compliance-heavy
- **ADP Vantage** - Enterprise tier of ADP

### Time & Attendance Specialists

Often integrated WITH HRIS rather than replaced by it:
- **UKG Dimensions** - Formerly Kronos, time/scheduling
- **ADP Time & Attendance** - Standalone or bundled
- **Deputy** - Modern, SMB-focused time tracking
- **When I Work** - Scheduling + time for hourly workers

### International Payroll

For companies with global employees:
- **Deel** - Contractor + employee payroll, 150+ countries
- **Oyster** - Global employment platform
- **Remote** - International payroll + compliance
- **Papaya Global** - Enterprise global payroll

---

## MPSE Discovery Plan

### S1: Rapid Discovery (Week 1)

**Goal**: Quick platform overviews, establish baseline understanding

**8 Platforms to Profile**:
1. Rippling (startup all-in-one)
2. Gusto (startup payroll-first)
3. BambooHR (HR-only, SMB)
4. Paycom (mid-market single database)
5. ADP Workforce Now (mid-market established)
6. Paylocity (mid-market modern)
7. Workday HCM (enterprise modern)
8. Oracle HCM Cloud (enterprise traditional)

**Per Platform** (~30-45 minutes each):
- Company overview, founding, scale
- Core modules (payroll, benefits, time, recruiting, performance, learning)
- Target market (employee count, company type)
- Pricing model (PEPM, setup fees, contracts)
- Key differentiators
- Notable customers
- Integration capabilities

**Deliverable**: 8 markdown files in `01-discovery/S1-rapid/`

---

### S2: Comprehensive Discovery (Week 2)

**Goal**: Deep feature comparison, integration analysis, pricing/TCO

**Approach Document**: `01-discovery/S2-comprehensive/approach.md`

**Feature Matrix**: Compare all 8+ platforms across:
- Payroll (tax filing, multi-state, direct deposit, checks)
- Benefits (medical, dental, 401k, FSA, COBRA)
- Time & Attendance (clock in/out, PTO, scheduling, overtime)
- Recruiting (job posting, ATS, onboarding, I-9/E-Verify)
- Performance (reviews, goals, 360 feedback, calibration)
- Learning (training, certifications, compliance tracking)
- Reporting (standard reports, custom reports, dashboards)
- Mobile (iOS, Android, offline capabilities)

**Integration Analysis**:
- Accounting systems (QuickBooks, Xero, NetSuite)
- FP&A tools (Runway, Planful, Causal)
- Time clocks (UKG, Deputy, When I Work)
- Benefits carriers (health insurance, 401k providers)
- Background check (Checkr, HireRight)
- APIs (Finch, Merge, webhook quality)

**Pricing & TCO**:
- PEPM pricing by employee count tiers
- Implementation fees
- Annual contract requirements
- Per-module add-on costs
- Integration costs
- Support tier pricing

**AI Capabilities Coverage** (MPSE v3.0):
- Conversational HR assistants
- Turnover prediction
- Resume screening
- Policy Q&A
- Performance insights
- Path A/B/C decision tree

**Deliverables**:
- `feature-matrix.md`
- `integrations.md`
- `pricing-tco.md`
- `ai-capabilities-coverage.md`
- `synthesis.md`

---

### S3: Need-Driven Discovery (Week 3)

**Goal**: Map platforms to specific business scenarios

**3 Scenarios**:

**Scenario 1: Tech Startup (10-50 employees)**
- Profile: SaaS company, seed to Series A, California-based
- Needs: Fast setup, modern UI, employee self-service
- Budget: <$50/employee/month
- Integration: QuickBooks Online, no legacy systems
- Decision: Rippling vs Gusto vs Justworks

**Scenario 2: Growing Business (50-250 employees)**
- Profile: E-commerce or services, Series B-C, multi-state
- Needs: Recruiting + performance management, benefits administration
- Budget: $50-100/employee/month
- Integration: NetSuite or Xero, need strong reporting
- Decision: BambooHR + Gusto vs Paylocity vs Namely

**Scenario 3: Enterprise Migration (2000+ employees)**
- Profile: Traditional company, leaving Oracle HCM (Post 2 scenario)
- Needs: Payroll cutover without disruption, reduce admin burden
- Budget: $40-80/employee/month (lower than Oracle)
- Integration: Keep Oracle Financials/SCM, UKG for time
- Decision: Paycom vs ADP vs Workday vs UKG Pro

**Per Scenario**:
- Requirements analysis
- Platform shortlist (3-4 options)
- Comparison across key factors
- Recommendation with rationale
- Implementation roadmap
- TCO calculation

**Deliverables**:
- `01-discovery/S3-need-driven/tech-startup.md`
- `01-discovery/S3-need-driven/growing-business.md`
- `01-discovery/S3-need-driven/enterprise-migration.md`
- `01-discovery/S3-need-driven/synthesis.md`

---

### S4: Strategic Discovery (Week 4)

**Goal**: Long-term frameworks, vendor viability, future outlook

**Strategic Frameworks**:

1. **Graduation Triggers**
   - When to move from Gusto → Paycom → Workday?
   - Employee count thresholds (50, 250, 2000)
   - Complexity factors (multi-state, international, union)
   - Feature needs (performance management, learning, analytics)

2. **PEO vs HRIS Decision Framework**
   - What is a PEO? (Professional Employer Organization)
   - When to use PEO (Justworks, TriNet) vs HRIS (Rippling, Gusto)?
   - Co-employment implications
   - Cost comparison
   - Migration path (PEO → HRIS when?)

3. **Build vs Buy Analysis**
   - When to build custom payroll? (almost never)
   - When to use payroll APIs? (Gusto API, Check API, Finch aggregator)
   - When to use full platform? (most companies >10 employees)

4. **Vendor Viability Analysis**
   - Public companies (ADP, Workday, Paychex) vs private (Rippling, Justworks)
   - Funding and runway (does Rippling have staying power?)
   - 10-year survival probability
   - Acquisition risk (getting absorbed into Oracle/ADP/Workday)

5. **AI Evolution (5-Year Outlook)**
   - 2025: Basic AI (resume parsing, policy Q&A)
   - 2027: Conversational HR (natural language interfaces)
   - 2030: Predictive workforce planning (turnover, performance, compensation)
   - Custom LLM opportunities (train on company HR policies)

**Deliverables**:
- `01-discovery/S4-strategic/graduation-frameworks.md`
- `01-discovery/S4-strategic/peo-vs-hris.md`
- `01-discovery/S4-strategic/vendor-viability.md` (with 5-year AI outlook)
- `01-discovery/S4-strategic/synthesis.md`

---

## Success Criteria

**S1 Complete**: 8 platform profiles exist, baseline understanding established
**S2 Complete**: Feature matrix covers 100+ features, pricing data for all platforms
**S3 Complete**: 3 scenarios have clear recommendations with rationale
**S4 Complete**: Decision frameworks answer "when to graduate?" and "build vs buy?"

**Full Experiment Complete**:
- CFO from Post 2 could use this research to choose Paycom alternative
- Startup could choose between Rippling, Gusto, Justworks with confidence
- Framework exists for HRIS → FP&A → Accounting integration architecture

---

## Integration with Other Experiments

**Upstream Dependencies**:
- **3.006 Accounting Software** - HRIS integrates with accounting for payroll journal entries
- **3.007 FP&A Platforms** - HRIS provides headcount data to FP&A tools (Runway needs Rippling data)

**Downstream Opportunities**:
- **3.008 AP Automation** - Expense management connects to HRIS employee data
- **3.504 Performance Management** - Standalone tools (Lattice, 15Five) vs HRIS-native

**Cross-Cutting**:
- Integration quality is critical (Finch API, Merge.dev, native connections)
- API ecosystem analysis needed (who provides best integration layer?)

---

## Expected Artifacts

**Documentation** (4 weeks):
- `S0-EXPERIMENT-SCOPE.md` (this file)
- `DOMAIN_EXPLAINER.md` (what is HRIS/HCM?)
- `metadata.yaml` (experiment tracking)
- S1-S4 discovery documents (~20-30 files)

**Frameworks** (post-discovery):
- Decision tree: PEO vs HRIS vs Payroll-only
- Graduation triggers by company size
- Oracle HCM migration playbook
- Integration architecture patterns

**Data**:
- Feature matrix (8+ platforms × 100+ features)
- Pricing table (PEPM by employee count)
- Integration compatibility matrix
- AI capabilities coverage matrix

---

## Timeline

**Week 1** (Oct 31 - Nov 6): S1 Rapid Discovery (8 platforms)
**Week 2** (Nov 7 - Nov 13): S2 Comprehensive (features, pricing, integrations, AI)
**Week 3** (Nov 14 - Nov 20): S3 Need-Driven (3 scenarios)
**Week 4** (Nov 21 - Nov 27): S4 Strategic (frameworks, viability, 5-year outlook)

**Total**: 4 weeks, ~40-60 hours research time

---

## Notes

**Market Validation**: This experiment was triggered by real CFO need (Post 2), not speculative research.

**High Business Value**: HRIS decisions are:
- Frequent (companies change HRIS every 5-7 years)
- Expensive ($50K-500K annual spend)
- High-risk (payroll errors cause employee lawsuits)
- Complex (30+ integration points)

**CFO Audience Entry Point**:
- Strategic consulting: $5K-15K for HRIS selection project
- Query service: $200 for "best HRIS for 75-person SaaS company"
- Subscription: $2K/year for unlimited HRIS guidance

---

**Status**: S0 Complete, S1 In Progress
**Next**: Create S1 rapid platform profiles (Rippling first)
