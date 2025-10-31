# HRIS/HCM Domain Explainer

**Experiment**: 3.503
**Domain**: Human Resources Information Systems (HRIS) / Human Capital Management (HCM)
**Last Updated**: October 31, 2025

---

## What is HRIS/HCM?

### Simple Definition

**HRIS (Human Resources Information System)**: Software that manages employee data, payroll, benefits, time tracking, and basic HR processes.

**HCM (Human Capital Management)**: Broader than HRIS - includes talent management (recruiting, performance, learning, succession planning) in addition to core HR/payroll functions.

**In Practice**: Most modern "HRIS" platforms include HCM features. The terms are often used interchangeably. "HCM" suggests a more strategic, talent-focused approach.

---

## Core Modules

### Must-Have (Core HRIS)

**1. Payroll**
- Salary calculations
- Tax withholding (federal, state, local)
- Direct deposit / check printing
- Tax filing (W-2, 1099, quarterly reports)
- Multi-state compliance
- Garnishments, deductions

**2. Benefits Administration**
- Health insurance enrollment
- Dental, vision plans
- 401(k) retirement plans
- FSA, HSA (flexible spending, health savings)
- Life insurance, disability
- COBRA administration
- Open enrollment workflow
- Carrier integrations (UnitedHealthcare, Fidelity, etc.)

**3. Time & Attendance**
- Clock in/out (web, mobile, physical time clocks)
- PTO tracking (vacation, sick leave)
- Overtime calculations
- Scheduling
- Approval workflows
- Integration with payroll

**4. Employee Self-Service**
- View pay stubs, W-2s
- Update personal information
- Request time off
- Enroll in benefits
- Access company documents/handbook

**5. HR Data Management**
- Employee records (personal info, job title, department)
- Organizational chart
- Document storage (I-9, W-4, offer letters)
- Compliance tracking (certifications, training)
- Reporting and analytics

### Common Add-Ons (HCM Features)

**6. Recruiting & Applicant Tracking (ATS)**
- Job posting to multiple boards
- Applicant tracking and screening
- Interview scheduling
- Offer letter generation
- Onboarding workflows
- I-9 and E-Verify integration
- Background checks

**7. Performance Management**
- Goal setting and tracking (OKRs, MBOs)
- Performance reviews (annual, 360-degree)
- Continuous feedback
- Calibration sessions
- Development plans

**8. Learning Management (LMS)**
- Training courses and content
- Compliance training (harassment, safety)
- Certification tracking
- Course assignments
- Learning paths

**9. Compensation Management**
- Salary planning and budgeting
- Merit increase cycles
- Bonus calculations
- Equity management
- Comp band analysis

**10. Succession Planning**
- Talent reviews
- High-potential identification
- Succession readiness
- Career pathing

---

## Who Needs HRIS/HCM?

### Company Size Stages

**1-10 Employees**
- **Need**: Payroll only
- **Options**: Gusto, QuickBooks Payroll, manual processing
- **Why**: Limited complexity, few benefits, minimal compliance

**10-50 Employees**
- **Need**: Payroll + benefits + time tracking
- **Options**: Gusto, Rippling, Justworks, BambooHR + payroll integration
- **Why**: Benefits administration starts, multi-state complexity, need for automation

**50-250 Employees**
- **Need**: Full HRIS with recruiting and performance
- **Options**: Paylocity, Namely, BambooHR + Gusto, ADP Workforce Now
- **Why**: Hiring ramps up, performance management needed, compliance burden increases

**250-2000 Employees**
- **Need**: Comprehensive HCM with analytics
- **Options**: Paycom, ADP Workforce Now, UKG Pro, Paylocity
- **Why**: Complex organizational structures, talent management critical, multi-location

**2000+ Employees**
- **Need**: Enterprise HCM with global capabilities
- **Options**: Workday HCM, Oracle HCM Cloud, SAP SuccessFactors
- **Why**: International payroll, complex compliance, executive dashboards, SOX compliance

---

## HRIS vs Related Services

### HRIS vs PEO (Professional Employer Organization)

**HRIS** (Technology Platform):
- You remain the employer
- Software to manage HR processes
- You handle compliance, benefits selection
- Examples: Rippling, Gusto, Paycom

**PEO** (Co-Employment Model):
- PEO becomes co-employer
- Access to PEO's benefits plans (often better rates)
- PEO handles compliance, risk, HR support
- Examples: Justworks, TriNet, Insperity
- **Trade-off**: Less control, harder to leave PEO, cost can be higher

**When to use PEO**:
- Small company wanting Fortune 500 benefits
- High-risk industry (need workers' comp, liability coverage)
- Don't want to manage HR/compliance
- International employees

**When to use HRIS**:
- Want full control over HR processes
- Have (or plan to hire) internal HR team
- Want flexibility to change benefits brokers
- Growing fast (PEOs harder to scale out of)

### HRIS vs Payroll Service vs Accounting Software

**Payroll Service** (Paychex, ADP Run):
- Payroll processing only
- Tax filing
- No or minimal HRIS features
- Often paper-based or legacy software

**HRIS/HCM** (Gusto, Rippling, Workday):
- Payroll + benefits + time + recruiting + performance + learning
- Modern, self-service interfaces
- API integrations
- Employee mobile apps

**Accounting Software** (QuickBooks, Xero, NetSuite):
- General ledger, A/R, A/P, financial reporting
- MAY include basic payroll (QuickBooks Payroll)
- NOT an HRIS - limited to payroll journal entries
- **Integration**: HRIS posts payroll journal entries to accounting software

**Typical Stack**:
- HRIS (Rippling) → Payroll journal entry → Accounting (QuickBooks)
- Employees see HRIS, accounting team sees QuickBooks

---

## Key Decision Factors

### 1. Employee Count
- Pricing is usually PEPM (per employee per month)
- Platforms have sweet spots (Gusto: 10-100, Paycom: 250-2000, Workday: 2000+)

### 2. Modules Needed
- **Just payroll**: Gusto, OnPay
- **Payroll + benefits**: Rippling, Justworks
- **Add recruiting**: BambooHR, Workday
- **Add performance + learning**: Workday, Oracle, SAP

### 3. Integration Requirements
- **Accounting**: Does it integrate with your accounting software?
- **Time clocks**: Does it support your physical time clocks (UKG, Kronos)?
- **Benefits**: Does it have carrier integrations (UnitedHealthcare, Fidelity)?
- **Background checks**: Checkr, HireRight integration?
- **APIs**: Can your other tools connect? (Finch, Merge.dev aggregators)

### 4. Complexity
- **Multi-state payroll**: Tax complexity increases dramatically
- **International**: Need global payroll provider (Deel, Remote) or enterprise HCM
- **Union employees**: Specialized payroll rules
- **Tipped employees**: Restaurant-specific requirements

### 5. Implementation Effort
- **Light** (1-2 weeks): Gusto, Rippling, BambooHR
- **Moderate** (1-3 months): Paycom, ADP Workforce Now, Paylocity
- **Heavy** (3-12 months): Workday, Oracle HCM, SAP SuccessFactors
- **Critical**: Payroll cutover - cannot miss a paycheck

### 6. User Experience
- **Modern** (consumer-grade): Rippling, Gusto, Workday
- **Functional** (gets job done): Paycom, Paylocity, ADP
- **Complex** (requires training): Oracle HCM, SAP SuccessFactors

### 7. Cost
- **Startup**: $35-50/employee/month (Gusto, Rippling)
- **Mid-market**: $50-100/employee/month (Paycom, ADP, Paylocity)
- **Enterprise**: $80-150+/employee/month (Workday, Oracle, SAP)
- **Plus**: Setup fees ($2K-50K), implementation ($10K-500K), training, integrations

---

## Common Pain Points

### Why Companies Change HRIS

**1. Outgrowing Current System**
- Started with Gusto (50 employees), now at 250 and need performance management
- Need recruiting features that startup HRIS doesn't have

**2. User Experience Issues**
- Oracle HCM is clunky, employees complain (Post 2 scenario)
- Too many clicks to do simple tasks
- Mobile app is poor

**3. Integration Failures**
- HRIS doesn't integrate with new accounting software (QuickBooks → NetSuite)
- FP&A tool (Runway) requires HRIS integration (Rippling) that Planful doesn't have (Post 1)

**4. Implementation Never Finished**
- Bought Workday 2 years ago, still not fully deployed
- Too complex for internal team to configure

**5. Cost Escalation**
- Started at $40/employee, now paying $120/employee after add-ons
- Vendor raises prices 10-20% annually

**6. Can't Retain Expertise**
- Oracle HCM requires specialized admins
- Turnover means losing institutional knowledge (Post 2 scenario)

**7. Vendor Being Acquired**
- Platform gets absorbed into larger company, roadmap dies
- Integration with other tools breaks

---

## Migration Challenges

### Payroll Cutover
**The Critical Path**: Cannot miss a paycheck or make tax filing error

**Best Practices**:
1. **Parallel Runs**: Run old and new systems simultaneously for 1-3 pay periods
2. **Validation**: Compare paychecks from both systems, ensure exactness
3. **Tax Mapping**: Ensure all tax jurisdictions mapped correctly
4. **Employee Communication**: Warn employees of potential hiccups
5. **Contingency Plan**: Keep old system accessible for 1-2 months

**Timing Considerations**:
- Avoid year-end (W-2 complications)
- Avoid open enrollment (benefits chaos)
- Avoid busy season (retail: avoid Q4, accounting: avoid tax season)
- Best: Start of quarter, mid-year

### Data Migration
**Historical Data Requirements**:
- Payroll: 7+ years (audits, corrections)
- Benefits: 7+ years (COBRA eligibility)
- Performance reviews: 3-5 years
- Training records: Depends on compliance requirements

**Migration Complexity**:
- Employee data (names, addresses, SSNs)
- Organizational structure (departments, managers, roles)
- Compensation history (salary, bonuses, raises)
- PTO balances (accruals, carryover rules)
- Benefits enrollments (current elections, dependents)
- Tax setup (W-4 elections, state registrations)

### Integration Reconnection
**Must Re-Integrate**:
- Accounting software (chart of accounts mapping)
- Time clocks (employee ID mapping)
- Benefits carriers (enrollment feeds)
- 401(k) provider (deduction feeds, employee data)
- Background check service
- Applicant tracking system (if separate)

---

## Build vs Buy Analysis

### When to Build Custom Payroll? (Almost Never)

**Why NOT to build**:
- **Tax Compliance**: 50 states × 1000s of municipalities = nightmarish complexity
- **Regulation Changes**: Tax laws change constantly (infrastructure act, COVID relief, etc.)
- **Liability**: Payroll errors lead to lawsuits, fines, IRS audits
- **Security**: PII + financial data = huge security burden (SOC 2, data encryption)
- **Maintenance**: Full-time team required just to keep current

**Rare Exceptions**:
- Very large companies (10,000+ employees) with unique needs (Google, Amazon level)
- Payroll processing companies themselves (ADP, Paychex)
- Countries with simple tax systems (Singapore, Hong Kong - but even then, risky)

### When to Use Payroll APIs? (Tier 2 Build)

**Use Case**: Building product that needs payroll features

**Options**:
- **Gusto API**: Embed Gusto payroll into your product
- **Check API**: Developer-first payroll API
- **Finch API**: Aggregator - connect to any HRIS
- **Merge.dev**: Unified HRIS API (integration layer)

**Good For**:
- FinTech products (lending, banking needing income verification)
- HR tech startups (add payroll to your performance management tool)
- Vertical SaaS (industry-specific tools needing HR data)

**Example**: Build workforce management tool for construction, embed Check API for payroll

### When to Use Full HRIS Platform? (Tier 3 Buy)

**Answer**: Almost always, for companies 10+ employees

**Why Buy**:
- **Time to Value**: 1-4 weeks vs 12-24 months to build
- **Compliance Included**: Vendors handle tax law changes
- **Integrations Included**: 100+ pre-built integrations
- **Support Included**: Dedicated support for payroll issues
- **Updates Included**: New features, mobile apps, security patches

**Cost Comparison**:
- **Buy**: $50/employee/month × 50 employees = $2,500/month = $30K/year
- **Build**: 2 engineers × $150K + security + compliance + maintenance = $400K+/year

**ROI**: Buy HRIS almost always cheaper unless you're a 10,000+ employee company

---

## Integration Architecture Patterns

### Pattern 1: HRIS as Source of Truth

```
HRIS (Rippling, Gusto, Workday)
  ↓ Employee data
  ↓ Payroll journal entries → Accounting (QuickBooks, NetSuite)
  ↓ Headcount data → FP&A (Runway, Planful)
  ↓ Time punches ← Time clock (UKG, Deputy)
  ↓ Benefits elections → Insurance carrier (UnitedHealthcare)
  ↓ 401(k) deductions → 401(k provider (Fidelity)
```

**HRIS owns**: Employee records, comp, org chart
**Other systems consume**: HRIS pushes data outward

### Pattern 2: Best-of-Breed (Multiple Systems)

```
BambooHR (HR data, recruiting, performance)
  ↓ Employee list → Gusto (payroll, benefits)
  ↓ Time data ← Deputy (time tracking)
  ↓ Performance data → Lattice (performance management)
  ↓ All data → Finch API → Accounting (NetSuite)
```

**Trade-off**: More flexible, but integration overhead and data sync issues

### Pattern 3: All-in-One Platform

```
Rippling (or Paycom, or Workday)
  ↓ Single database, no integrations needed
  ↓ Payroll journal entry → Accounting (only external integration)
```

**Trade-off**: Vendor lock-in, but no data sync issues

---

## AI Capabilities (2025 State of the Art)

### Available Today

**1. Conversational HR Assistants**
- Ask policy questions: "What's the parental leave policy?"
- Chatbot handles common employee questions
- Reduces HR ticket volume

**2. Resume Parsing & Candidate Matching**
- Auto-extract skills, experience from resumes
- Match candidates to job requirements
- Score applicants

**3. Predictive Turnover**
- Analyze patterns (tenure, performance, comp, engagement surveys)
- Flag employees at flight risk
- Recommend interventions (raise, promotion, development plan)

**4. Policy Q&A**
- RAG (Retrieval-Augmented Generation) on company handbook
- Instant policy answers for employees
- Reduces HR admin workload

**5. Performance Insights**
- Analyze review text for sentiment, themes
- Flag potential bias in reviews
- Suggest calibration adjustments

### Coming 2027-2030

**6. Workforce Planning AI**
- Predict hiring needs based on growth projections
- Recommend org structure changes
- Compensation optimization (find underpaid talent)

**7. Skills Gap Analysis**
- Map current skills → future needs
- Recommend upskilling/reskilling programs
- Predict internal mobility opportunities

**8. Conversational Interfaces**
- Full natural language HRIS: "Give me a raise breakdown for the engineering team"
- Voice interfaces: Ask Alexa for your PTO balance
- Proactive suggestions: "3 employees eligible for promotion this quarter"

---

## Key Terminology

**PEPM**: Per Employee Per Month (pricing model)
**PEO**: Professional Employer Organization (co-employment model)
**ATS**: Applicant Tracking System (recruiting module)
**LMS**: Learning Management System (training module)
**HRIS**: Human Resources Information System (core HR + payroll)
**HCM**: Human Capital Management (HRIS + talent management)
**SOC 2**: Security compliance certification (critical for HRIS vendors)
**W-2**: Annual wage and tax statement (U.S. payroll)
**W-4**: Employee tax withholding form
**I-9**: Employment eligibility verification (U.S. citizens and work authorization)
**COBRA**: Health insurance continuation after employment ends
**FLSA**: Fair Labor Standards Act (overtime, minimum wage)
**FMLA**: Family and Medical Leave Act (unpaid leave)
**ACA**: Affordable Care Act (healthcare compliance)
**Finch, Merge**: API aggregators (connect to any HRIS with one API)

---

## Decision Framework Preview

### Key Questions to Answer (S1-S4 Will Address)

1. **What modules do I need?** (Payroll only? + Benefits? + Recruiting? + Performance?)
2. **How many employees?** (10? 100? 1000? 10,000?)
3. **How complex is my payroll?** (Single state? Multi-state? International? Union?)
4. **PEO or HRIS?** (Want control vs want outsourcing?)
5. **All-in-one or best-of-breed?** (Single vendor vs multiple specialists?)
6. **What integrations are critical?** (Accounting? FP&A? Time clocks?)
7. **What's my budget?** ($50/employee? $100/employee?)
8. **How fast do I need to implement?** (1 week? 3 months? 12 months?)
9. **How important is user experience?** (Consumer-grade vs functional?)
10. **Am I migrating or starting fresh?** (Cutover complexity vs greenfield)

**S1-S4 Research Goal**: Provide data-driven answers to all 10 questions with platform recommendations.

---

## Document Status

**Created**: October 31, 2025
**Purpose**: Foundational domain knowledge for 3.503 HRIS/HCM research
**Next**: S1 Rapid Discovery (8 platform profiles)
