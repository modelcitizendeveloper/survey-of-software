# S3 Need-Driven: Scenario 3 - Enterprise Cloud Migration (PeopleSoft → Modern Cloud HCM)

**Company Profile**: Meridian Financial Services
**Industry**: Regional bank + wealth management
**Employees**: 5,000 (3,500 US, 1,000 Canada, 500 UK)
**Current State**: PeopleSoft HRMS 9.2 (on-premises, implemented 2008)
**Strategic Driver**: Board mandate to move all systems to cloud by 2027 (data center decommissioning)
**Oracle Relationship**: Deep (Oracle Database 19c, Oracle EBS Financials 12.2, 20+ years)

---

## Current State: PeopleSoft Pain Points

### System Overview

**PeopleSoft HRMS 9.2**:
- Implemented: 2008 (17 years old)
- Last major upgrade: 2015 (PeopleSoft 9.1 → 9.2)
- Hosting: On-premises data center (Chicago + disaster recovery in Atlanta)
- Annual cost:
  - Oracle support/maintenance: $850K/year (22% of original license cost)
  - Data center (servers, storage, network): $1.2M/year
  - Internal IT team (3 FTE): $450K/year
  - **Total**: **$2.5M/year** ($500/employee/year)

**Modules in Use**:
- Core HR (employee records, org management)
- Payroll (US via ADP integration, Canada/UK via local bureaus)
- Benefits Administration
- Time & Labor
- Recruiting (Taleo, standalone—Oracle acquired 2012, now part of Oracle HCM Cloud)
- Performance Management (custom-built on top of PeopleSoft)

### Pain Points Driving Cloud Migration

**1. User Experience Disaster** (2.5/5 Internal Rating):
- **Green-screen era UI**: PeopleSoft 9.2 interface from 2008 (pre-smartphone era)
- **Mobile nightmare**: No mobile app; employees use Citrix remote desktop on phones (1.2/5 rating)
- **Manager complaints**: "Takes 15 clicks to approve a time off request," "Can't use on phone"
- **HR help desk overwhelmed**: 40% of tickets are "how do I…?" navigation questions

**2. Technical Debt Accumulating**:
- **Customizations**: 200+ custom modifications (custom fields, workflows, reports)
- **Integration fragility**: 35 integrations to downstream systems (benefits, 401k, learning, badging)
- **Upgrade paralysis**: Last upgrade (2015) took 18 months, $3M → hasn't upgraded since (fear of breaking customizations)
- **Security vulnerabilities**: Running on Oracle 19c database (not latest 23c), behind on patches

**3. Compliance & Audit Risk**:
- **SOX compliance**: Manual controls for payroll changes (auditors flagging as high-risk)
- **GDPR**: UK employee data stored in US data center (violation, $2M fine risk)
- **Disaster recovery**: DR site in Atlanta, but last failover test was 2019 (failed after 4 hours downtime)

**4. Recruiting Inefficiency** (Standalone Taleo):
- **Taleo Enterprise**: Separate Oracle product, doesn't integrate well with PeopleSoft
- **Data duplication**: New hire in Taleo → manually re-enter in PeopleSoft (2 hours/hire × 800 hires/year = 1,600 hours)
- **Candidate experience**: Taleo rated 2.1/5 ("worst application process I've ever experienced")

**5. Board Mandate: Data Center Decommissioning**:
- **CFO directive**: Exit Chicago data center by 2027 (lease expiring, cost $3M/year for all systems)
- **Cloud-first strategy**: All applications (ERP, HCM, CRM) must move to SaaS
- **PeopleSoft end-of-life**: Oracle announced PeopleSoft feature development ended 2022 (sustaining support only until 2030)

---

## Strategic Decision: Oracle HCM Cloud vs. Workday HCM

### Evaluation Criteria

1. **User Experience**: Must be modern (mobile-first, consumer-grade UX)
2. **Global HCM**: Support US, Canada, UK with localized payroll/compliance
3. **Implementation Risk**: Minimize disruption to 5,000-employee operations
4. **Total Cost of Ownership**: Lower than $2.5M/year PeopleSoft current state
5. **Oracle Ecosystem**: Leverage existing Oracle EBS Financials, Database relationships
6. **Compliance**: SOX, GDPR, FedRAMP (if government contracts expand)

### Option A: Oracle Fusion HCM Cloud

**Pros**:
- **PeopleSoft migration path**: Oracle offers automated migration tools, data model similar
- **Ecosystem continuity**: Oracle EBS Financials → Oracle ERP Cloud + Oracle HCM Cloud unified
- **Vendor relationship**: 20+ years with Oracle, negotiating leverage
- **Bundled pricing**: Oracle offering 20% discount for HCM + ERP Cloud together
- **Familiar to IT**: Oracle technology stack (Java, Middleware, Database)

**Cons**:
- **Poor UX**: User reviews rate Oracle HCM Cloud 3.5/5 ("consistently bad UI")
- **Quarterly update instability**: "Updates break customizations every 3 months"
- **Test environment costs**: $450K/year for 3 required test environments (hidden tax)
- **Implementation complexity**: 18-24 months (longest in market)

**Pricing** (5,000 employees):
- Software (HCM + Dynamic Skills): $2.1M/year ($32/mo + $3/mo Skills × 5K × 12)
- Test environments (3): $450K/year
- Implementation: $2M (Oracle Consulting + Deloitte)
- **Year 1 Total**: $4.55M
- **Year 2+ Total**: $2.55M/year

**3-Year TCO**: $9.65M ($643/employee/year)

---

### Option B: Workday HCM

**Pros**:
- **Best enterprise UX**: 3.8/5 rating (vs. Oracle 3.5/5), mobile app 3.8/5
- **Skills Cloud included**: vs. Oracle's $180K/year add-on (Dynamic Skills)
- **Free test environments**: 4 environments vs. Oracle's $450K/year
- **Bi-annual upgrades**: More stable than Oracle's quarterly (less testing burden)
- **Single-instance global**: One system for US/Canada/UK vs. Oracle's regional approach

**Cons**:
- **No Oracle ecosystem integration**: Workday HCM + Oracle EBS Financials requires custom integration
- **Vendor switch risk**: Leaving 20-year Oracle relationship
- **Workday Financial Management pressure**: Workday will push to replace Oracle EBS Financials (full platform migration)

**Pricing** (5,000 employees):
- Software (HCM Suite, Skills Cloud included): $900K/year ($180/EE/year)
- Test environments: $0 (free)
- Implementation: $2.5M (Deloitte Workday practice)
- **Year 1 Total**: $3.4M
- **Year 2+ Total**: $900K/year

**3-Year TCO**: $5.2M ($347/employee/year)

**Savings vs. Oracle**: $4.45M over 3 years (46% cheaper)

---

## Decision: Workday HCM ✅

**Final Rationale**:

1. **User Experience Non-Negotiable**: Board explicitly mandated "modern, mobile-first" (Oracle 3.5/5 fails this requirement)
2. **$4.45M Savings Over 3 Years**: CFO's cloud migration budget constrained ($15M for all systems)
3. **Test Environment Savings**: $450K/year = $2.25M over 5 years (Oracle's "hidden tax" eliminated)
4. **Skills Cloud Included**: vs. $900K over 5 years for Oracle Dynamic Skills add-on
5. **Stable Platform**: Bi-annual upgrades more manageable than Oracle's quarterly disruptions
6. **Reference Calls**: 3 peer banks (similar size) all recommend Workday over Oracle for HCM

**Oracle Ecosystem Mitigation**:
- **Keep Oracle EBS Financials** (not migrating to Workday Financials yet—separate 3-year project)
- **Integrate Workday HCM ↔ Oracle EBS**: Via Workday Studio + Oracle Integration Cloud (OIC)
- **Data flow**: Workday (employee, org, comp) → Oracle EBS (cost center, GL reporting)

**Vendor Negotiation**:
- **Oracle counteroffer**: Dropped HCM Cloud to $1.8M/year + free test environments (50% discount) → Board still chose Workday for UX

---

## 18-Month Implementation Journey

### Phase 1: Planning & Preparation (Months 1-3)

**Governance Structure**:
- **Executive Sponsor**: CHRO (reports to CEO monthly)
- **Steering Committee**: CFO, CIO, COO, CHRO, General Counsel (meets bi-weekly)
- **Program Manager**: Deloitte (full-time, 18 months)
- **Core Team**: 10 FTE internal (HR, IT, Finance, Legal, Compliance)
- **Extended Team**: 40 SMEs (part-time, various functions)

**Workstream Formation**:
1. **Core HR**: Employee records, org management, security roles
2. **Talent Management**: Recruiting, performance, learning, succession
3. **Compensation & Benefits**: Payroll, benefits, time & labor
4. **Integrations**: 35 systems to connect (benefits, 401k, learning, badging, etc.)
5. **Data Migration**: PeopleSoft → Workday (17 years of history)
6. **Reporting & Analytics**: Rebuild 150+ PeopleSoft custom reports in Workday
7. **Change Management**: Training, communication, adoption

**Current State Documentation** (8 weeks):
- **PeopleSoft audit**: 200 custom fields, 150 custom workflows, 35 integrations
- **Data quality assessment**: 12,000 employee records, 8% have data issues (missing department, incorrect job code)
- **Process documentation**: 75 HR business processes (hire, promote, transfer, terminate, etc.)

**Future State Design** (4 weeks):
- **Workday org model**: Translate PeopleSoft hierarchies → Workday supervisory orgs
- **Business process design**: Standardize on Workday best practices (reduce customizations)
- **Security model**: Map PeopleSoft roles → Workday security groups (500 users × 20 roles = 10K permissions)

---

### Phase 2: Build & Configure (Months 4-10)

**Workday Tenant Provisioning** (Week 1):
- **Implementation tenant**: Deloitte configures
- **Sandbox tenant**: IT team tests integrations
- **Production tenant**: Go-live environment (locked until cutover)

**Core Configuration** (16 weeks):
- **Organizations**: 3 countries (US, Canada, UK), 12 business units, 45 departments, 300 locations
- **Jobs & Positions**: 250 job profiles (engineer, analyst, teller, wealth advisor, etc.)
- **Compensation**: 25 pay grades, 8 salary bands, 15 bonus plans
- **Benefits**: 12 US medical plans, 8 dental, 6 vision, 401k (Fidelity), HSA, FSA, commuter
- **Security**: 500 managers, 50 HR users, 5 HRIS admins → 20 security roles (granular permissions)

**Talent Modules** (12 weeks):
- **Recruiting**: Career sites (3 languages), 800 job requisitions/year, interview scheduling
- **Performance**: Annual review + continuous feedback, OKRs, 9-box talent review
- **Learning**: Compliance training (AML, BSA, SOX), leadership development programs
- **Succession**: Bench strength for 200 critical roles (VP+, revenue-producing roles)

**Global Payroll Setup** (14 weeks):
- **US**: Workday Payroll (native, 3,500 employees)
- **Canada**: ADP Canada integration (1,000 employees)
- **UK**: CloudPay integration (500 employees)

**Integrations Development** (16 weeks, parallel with config):
- **Benefits**: Benefitfocus (medical, dental, vision carrier feeds)
- **401k**: Fidelity (contribution rates, new hire enrollments, loans)
- **Learning**: Cornerstone OnDemand (LMS for compliance training)
- **Identity**: Okta (SSO, user provisioning/deprovisioning)
- **Badging**: HID (physical access control)
- **Background Checks**: Sterling (candidate screening)
- **Time Clocks**: Kronos (branch locations, physical timeclocks)
- **Financials**: Oracle EBS (employee cost center, GL posting)
- **Total**: 35 integrations (10 real-time API, 25 batch file)

---

### Phase 3: Data Migration & Testing (Months 11-15)

**Data Migration** (12 weeks):

**Iteration 1 (Week 1-2): Current Employees**
- Extract from PeopleSoft: 5,000 active employees
- Data quality issues found:
  - 400 employees missing cost center → HR SMEs research and fix
  - 150 employees with duplicate records → merge duplicates
  - 80 contractors misclassified as FTE → reclassify
- Load to Workday: 4,600 clean records (92% success rate)

**Iteration 2 (Week 3-4): Historical Data**
- Extract: 15,000 terminated employees (7 years retention)
- Extract: Compensation history (annual raises, bonuses, equity)
- Extract: Performance reviews (5 years)
- Load to Workday: 85% success rate (historical data quality worse)

**Iteration 3 (Week 5-6): Benefits & Time**
- Extract: PTO balances (accrued vacation, sick, floating holidays)
- Extract: Benefits enrollments (medical, dental, 401k contributions)
- Load to Workday: 95% success rate (cleaner data)

**Parallel Payroll** (8 weeks):
- Run payroll simultaneously in PeopleSoft AND Workday
- Compare results (net pay, taxes, deductions must match within $0.01)
- **Issues found**:
  - Rounding differences: 35 employees off by $0.01-$0.05 (acceptable)
  - CA SDI calculation: Workday vs. PeopleSoft logic different → fixed Workday rule
  - UK National Insurance: CloudPay integration bug → fixed by CloudPay

**User Acceptance Testing** (8 weeks):
- **Wave 1**: HR team (50 users) → test employee lifecycle (hire, promote, terminate)
- **Wave 2**: Managers (500 users) → test approvals (PTO, job change, performance review)
- **Wave 3**: Employees (500 sample) → test self-service (view pay stub, request PTO, update profile)
- **Defects found**: 127 issues → 98 fixed, 22 documented workarounds, 7 deferred to Phase 2

---

### Phase 4: Training & Change Management (Months 13-18)

**Training Strategy**:

**HR Power Users** (2 days, Month 13):
- 50 HR team members
- Deep-dive: Employee lifecycle, security, reporting, troubleshooting
- Certification: "Workday HR Specialist" (Deloitte-led)

**Managers** (2 hours, Month 15-16):
- 500 people managers
- Topics: Approve PTO, review timecards, initiate job changes, performance reviews
- Format: Lunch-and-learn sessions (25 per session × 20 sessions)
- Attendance: 95% (mandatory, CEO mandate)

**Employees** (1 hour, Month 16-17):
- 5,000 employees
- Topics: Access Workday, view pay stub, request PTO, update profile, enroll benefits
- Format: Self-paced e-learning + optional live webinars
- Completion: 78% (voluntary)

**Training Materials Created**:
- 45 quick-reference guides (1-page PDFs: "How to Request PTO," "How to View Pay Stub")
- 30 video tutorials (2-3 minutes each, Loom recordings)
- Workday Help Center (intranet site with FAQs, contact info)
- Chatbot (basic AI: answers 20 most common questions)

**Communication Campaign** (Month 10-18):
- **Month 10**: CEO announcement ("Why we're migrating to Workday")
- **Month 12**: Monthly newsletter (migration progress, countdown)
- **Month 15**: "Meet Workday" roadshows (10 branch locations, HR team demos)
- **Month 17**: Go-live countdown (daily emails: "T-minus 7 days")
- **Month 18**: Go-live celebration (company-wide event, Workday launch party)

**Resistance Management**:
- **Concern**: "PeopleSoft works fine, why change?" (60% of employees surveyed)
- **Response**: Demos showing mobile app, faster workflows, modern UX → 80% buy-in after seeing
- **Concern**: "I don't want to learn a new system" (40% of managers)
- **Response**: Manager 1:1s with HR Director, explain training support, address fears

---

### Phase 5: Go-Live & Hypercare (Month 18+)

**Go-Live Strategy**: **Big Bang** (all 5,000 employees, all 3 countries, same day)

**Why Big Bang** (vs. Phased):
- **Payroll imperative**: Can't run dual payroll for multiple pay periods (too risky)
- **Org chart integrity**: Need full org in Workday for reporting/approvals to work
- **Board mandate**: CFO wants "rip the band-aid" (fast, decisive cutover)

**Go-Live Date**: January 1, 2027 (chosen deliberately)
- **Rationale**: Start of year (clean break, no mid-year complexities)
- **Risk**: Employees on holiday break, limited support staff → Mitigated with extended hypercare team

**Cutover Weekend** (December 28-31):
- **Friday 12/28 5pm**: PeopleSoft goes read-only (no more updates)
- **Saturday 12/29-Sunday 12/30**: Final data migration (5,000 employees, YTD payroll, benefits)
- **Monday 12/31**: Smoke testing (login, key workflows, reports)
- **Tuesday 1/1/2027**: Workday goes live (employees can access)

**Hypercare** (Months 1-3):
- **War room**: 20-person team (HR, IT, Deloitte) in office 7am-7pm daily (first 2 weeks)
- **Help desk surge**: 3x normal staffing (15 agents vs. usual 5)
- **Ticket volume**:
  - Week 1: 1,200 tickets (80% "how do I…?" password resets, navigation)
  - Week 2: 800 tickets (50% system issues, 50% navigation)
  - Week 4: 400 tickets (back to normal)
- **Issues**:
  - **Payroll**: 12 employees missing first paycheck (data migration issue) → manual checks issued
  - **Benefits**: 50 employees' medical coverage not in carrier system → Benefitfocus integration bug → fixed Week 2
  - **Time**: 100 employees can't punch in (Kronos timeclock integration) → Deloitte on-site, fixed Week 1
  - **Mobile**: 30% of employees can't log in (MFA not set up) → IT help desk walkthrough

**Stabilization** (Months 4-6):
- **Post-launch optimizations**:
  - 22 deferred UAT issues resolved
  - 15 custom reports added (not in scope, but HR team requests)
  - 5 business process tweaks (approval workflows too slow, streamlined)
- **Knowledge transfer**: Deloitte → Internal HRIS team (handoff complete Month 6)

---

## Results: Year 1 Post-Launch

### User Satisfaction

**Employee NPS** (Net Promoter Score):
- **PeopleSoft** (pre-migration): 12 (2.5/5 internal rating)
- **Workday** (Month 3): 45 (3.6/5)
- **Workday** (Month 12): 58 (3.9/5) — improves as employees learn platform

**Feedback Themes**:
- **Positive**: "Mobile app is amazing," "So much faster than PeopleSoft," "Clean, modern interface"
- **Negative**: "Too many clicks to request PTO," "Search doesn't always work," "Miss some PeopleSoft reports"

**Manager Satisfaction**:
- **Approval time**: 15 clicks in PeopleSoft → 4 clicks in Workday (73% reduction)
- **Mobile approvals**: 0% in PeopleSoft (Citrix unusable) → 65% in Workday (approve PTO on phone)

---

### Operational Efficiency

**HR Help Desk Volume**:
- **Pre-migration**: 400 tickets/month (40% "how do I…?" PeopleSoft navigation)
- **Post-launch (Month 1-3)**: 600 tickets/month (hypercare surge)
- **Post-launch (Month 12)**: 250 tickets/month (**37% reduction vs. PeopleSoft**)

**Why Lower**:
- Workday's intuitive UX → fewer "how do I…?" tickets
- Mobile app → employees self-serve (view pay stub, request PTO)
- Chatbot handles 20% of tickets (automated responses)

**Recruiting Efficiency** (Workday Recruiting vs. Standalone Taleo):
- **Time-to-hire**: 42 days → 35 days (17% faster)
- **Data entry time**: 2 hours/hire → 5 minutes (integrated with Core HR)
- **Annual savings**: 1,600 hours/year (800 hires × 2 hrs saved) = **$120K/year** (HR coordinator time)

**Reporting Agility**:
- **PeopleSoft**: Custom reports took 2-4 weeks (IT had to write SQL queries)
- **Workday**: Self-service reporting (HR can build reports in 1-2 hours)
- **Business impact**: Headcount report for M&A due diligence → 3 days (PeopleSoft) → 2 hours (Workday)

---

### Compliance & Risk

**SOX Compliance**:
- **PeopleSoft**: Manual controls (HR emails approver, tracks in Excel) → Auditors flagged as "high risk"
- **Workday**: Automated audit trail (all changes logged, approval workflows enforced) → Auditors upgraded to "low risk"

**GDPR Compliance**:
- **PeopleSoft**: UK data in US data center → $2M fine risk
- **Workday**: UK data in Workday's EU data center (Dublin) → compliant

**Disaster Recovery**:
- **PeopleSoft**: DR site in Atlanta, last test failed (4 hours downtime)
- **Workday**: Cloud provider (AWS) → 99.9% uptime SLA, automatic failover

---

### Financial: 3-Year TCO Comparison

| Cost Category | PeopleSoft (Stay) | Workday (Migrate) | Savings |
|---------------|-------------------|-------------------|---------|
| **Year 1** |  |  |  |
| Software/maintenance | $2.5M | $900K | $1.6M |
| Implementation | $0 | $2.5M | ($2.5M) |
| **Year 1 Total** | **$2.5M** | **$3.4M** | **($900K)** |
| **Year 2** |  |  |  |
| Software/maintenance | $2.5M | $900K | $1.6M |
| PeopleSoft sustaining (no upgrades) | $0 | $0 | $0 |
| **Year 2 Total** | **$2.5M** | **$900K** | **$1.6M** |
| **Year 3** |  |  |  |
| Software/maintenance | $2.5M | $945K (5% increase) | $1.555M |
| **Year 3 Total** | **$2.5M** | **$945K** | **$1.555M** |
| **3-Year Total** | **$7.5M** | **$5.245M** | **$2.255M** |

**Savings**: **$2.255M over 3 years** (30% reduction)

**Break-Even**: Month 18 (after implementation, Year 2 savings begin)

**5-Year Savings**: $6.6M (including Oracle test environments saved: $2.25M)

---

## Lessons Learned: Enterprise Cloud Migration

### 1. User Experience Was the Killer App

**Decision Driver**: Board mandated "modern, mobile-first" → Oracle 3.5/5 UX disqualified despite ecosystem fit

**Lesson**: For enterprise transformations, **UX is not a "nice-to-have"**—it's a strategic imperative. Employee adoption depends on UX quality.

**Quantified Impact**:
- Help desk tickets: 400/month (PeopleSoft) → 250/month (Workday) = **37% reduction**
- Mobile approval adoption: 0% (PeopleSoft Citrix) → 65% (Workday) = **faster manager decisions**

---

### 2. Oracle's "Hidden Tax" (Test Environments) Was a Deal-Breaker

**Oracle Quote**: $2.1M/year software + **$450K/year for 3 test environments** = **$2.55M/year total**

**Workday Quote**: $900K/year software + **$0 for 4 test environments** = **$900K/year total**

**Impact**: Test environment cost swung $450K/year ($2.25M over 5 years) → **Board couldn't justify**

**Lesson**: Enterprise buyers MUST ask "How much for test environments?" during RFP. This line item is often buried in contracts.

---

### 3. Big Bang Go-Live Was Right Choice (Despite Risk)

**Alternative Considered**: Phased rollout (US → Canada → UK over 6 months)

**Why Big Bang Won**:
- **Payroll constraint**: Can't run dual payroll for extended period (error risk, audit complexity)
- **Org chart integrity**: Partial org in Workday breaks reporting, approval workflows
- **Executive appetite**: CFO wanted decisive cutover ("rip the band-aid")

**Risk Mitigation**:
- 3-month hypercare (20-person war room, 3x help desk staffing)
- January 1 go-live (clean year-start, no mid-year complexities)
- Parallel payroll (8 weeks testing ensured accuracy)

**Result**: 12 payroll errors (out of 5,000 employees) = 0.24% error rate → acceptable

**Lesson**: Big Bang is riskier but faster to stabilize. Phased rollouts prolong pain.

---

### 4. Change Management Was 30% of Budget (Worth It)

**Change Management Investment**:
- Training: $500K (materials, instructor time, employee hours)
- Communication: $200K (videos, roadshows, intranet site)
- Deloitte change mgmt consultants: $800K
- **Total**: **$1.5M** (30% of $5M total project)

**Why Worth It**:
- Employee NPS: 12 (PeopleSoft) → 58 (Workday, Month 12)
- Manager adoption: 95% completed training (mandatory, but willing participation)
- Help desk surge: Returned to normal by Month 4 (without change mgmt, could take 12+ months)

**Lesson**: Enterprise transformations fail when change management is <10% of budget. Invest 25-30% for successful adoption.

---

### 5. Oracle Offered 50% Discount (Too Late)

**Timeline**:
- **Month 6**: Meridian selects Workday (Board approval)
- **Month 8**: Oracle Account Team learns of decision
- **Month 9**: Oracle executive escalation (SVP flies to Meridian)
- **Oracle Counteroffer**:
  - Drop HCM Cloud price: $2.1M → $1.05M/year (50% discount)
  - Free test environments: $450K → $0
  - Accelerated implementation: 18 months → 12 months (Oracle Fast Start program)
  - **Total**: $1.05M/year vs. Workday $900K/year

**Board Decision**: Declined Oracle, proceeded with Workday

**Why**:
- **Too late**: 8 months into Workday project, $1M sunk cost
- **Trust eroded**: "If Oracle can discount 50%, what's the real price? Feels like we're being manipulated"
- **UX still poor**: Even at 50% discount, Oracle 3.5/5 UX doesn't solve employee experience problem

**Lesson**: Oracle's aggressive discounting (common in enterprise sales) backfires when discovered mid-project. Transparency builds trust.

---

## Decision Framework: Enterprise Cloud HCM Migration

### When to Migrate from PeopleSoft/Legacy

**Trigger Points**:
1. **Board mandate**: Data center decommissioning, cloud-first strategy
2. **Oracle end-of-life**: PeopleSoft sustaining support ends 2030 (no new features since 2022)
3. **UX crisis**: Employee/manager revolt (mobile app demanded)
4. **Compliance risk**: GDPR, SOX, disaster recovery failures
5. **M&A integration**: Acquiring companies, need unified HCM (can't bolt on to PeopleSoft)

**Don't Migrate If**:
- **PeopleSoft works**: Recent upgrade (2020+), low customizations, users satisfied
- **Budget constrained**: Implementation $2-3M, can't afford disruption
- **Other priorities**: ERP or CRM migration underway (don't stack transformations)

---

### Oracle HCM Cloud vs. Workday Decision Matrix

| Factor | Choose Oracle HCM Cloud | Choose Workday HCM |
|--------|------------------------|-------------------|
| **Oracle Ecosystem** | Deep investment (ERP Cloud, Database, Middleware) | Minimal Oracle footprint OR migrating ERP away from Oracle |
| **User Experience Priority** | Low (functional > beautiful) | High (employee experience critical) |
| **Budget** | Oracle offers 30%+ discount (bundled HCM+ERP) | Willing to pay market rate for best product |
| **Customization** | Need extensive custom fields/workflows (Oracle more flexible) | Willing to adopt standard processes (Workday enforces best practices) |
| **Implementation Timeline** | 18-24 months acceptable (complex custom migration) | 12-18 months target (faster to value) |
| **Test Environments** | Budget allows $450K/year for 3 test environments | Want free test environments (save $2.25M over 5 years) |
| **Skills Intelligence** | Don't need skills ontology OR willing to pay $180K/year add-on (Dynamic Skills) | Want Skills Cloud included (strategic workforce planning) |
| **PeopleSoft Migration** | Prefer Oracle migration path (familiar data model) | Willing to use any vendor (best product wins) |

**Most Common Outcome**: **Workday wins 60-70% of PeopleSoft replacement RFPs** (per Gartner), Oracle wins when ecosystem lock-in is strong

---

## Alternative Path: Oracle HCM Cloud (What If?)

**Hypothetical**: Meridian chose Oracle instead of Workday

**3-Year TCO** (with Oracle's 50% discount offer):
- Year 1: $1.05M + $2M implementation = $3.05M
- Year 2-3: $1.05M/year × 2 = $2.1M
- **Total**: $5.15M (vs. Workday $5.245M → **$95K cheaper**)

**Why Meridian Still Chose Workday** (despite Oracle being cheaper):
1. **UX**: Oracle 3.5/5 vs. Workday 3.8/5 → employee experience matters
2. **Test environment trust**: Oracle "giving up" $450K made Board question pricing integrity
3. **Bi-annual vs. quarterly updates**: Workday more stable (fewer integration breakages)
4. **Skills Cloud**: Included in Workday vs. Oracle add-on
5. **Reference calls**: 3 peer banks recommended Workday over Oracle

**When Oracle Would Have Won**:
- If Meridian was implementing **Oracle ERP Cloud simultaneously** (bundled 30% discount on HCM+ERP = $3M savings)
- If **customizations were critical** (Oracle allows more than Workday's standard processes)
- If **PeopleSoft-to-Oracle migration tools** significantly de-risked implementation (Meridian deemed this overrated)

---

## Final State: Post-Migration (Year 2)

**HRIS Architecture**:
- **Workday HCM**: Core HR, recruiting, performance, learning, succession, time & labor
- **Workday Payroll** (US): 3,500 employees
- **ADP Canada**: 1,000 employees (integrated with Workday)
- **CloudPay UK**: 500 employees (integrated with Workday)
- **35 integrations**: Benefits, 401k, learning, badging, timeclocks, financials

**Annual Cost**:
- Workday HCM: $900K/year
- ADP Canada: $50K/year
- CloudPay UK: $30K/year
- Integration monitoring (1 FTE): $120K/year
- **Total**: **$1.1M/year** ($220/employee/year)

**Savings vs. PeopleSoft**: $2.5M - $1.1M = **$1.4M/year** (56% reduction)

**HR Team**:
- 1 CHRO
- 3 VP HR (US, Canada, UK)
- 10 HR Business Partners
- 5 Recruiting
- 5 HRIS (3 Workday admins, 2 integration specialists)
- 2 Compensation & Benefits
- **Total**: 26 FTE (1:192 ratio, improved from 1:200 on PeopleSoft)

**Business Outcomes**:
- **Employee NPS**: 12 → 58 (46-point improvement)
- **Help desk volume**: 400/month → 250/month (37% reduction)
- **Time-to-hire**: 42 days → 35 days (17% faster)
- **Mobile adoption**: 0% → 65% (managers approve on phone)
- **SOX compliance**: High risk → Low risk (automated audit trails)
- **GDPR compliance**: Violation → Compliant (EU data residency)

**Next Evolution**: Year 5, evaluate **Workday Financial Management** (replace Oracle EBS Financials, achieve unified HCM+Finance platform)

---

## Document Status

✅ **S3 Complete**: All 3 scenarios documented

**Key Takeaways**:
1. **Scenario 1** (Startup): Start simple (Gusto), migrate proactively at 100 EE (Rippling)
2. **Scenario 2** (Mid-market): Consolidate acquisitions fast, best-of-breed beats all-in-one for industry-specific needs
3. **Scenario 3** (Enterprise): Workday beats Oracle for PeopleSoft replacements (UX + cost, despite Oracle ecosystem)

**Next**: S4 Strategic Discovery (vendor viability, AI evolution, graduation frameworks)
