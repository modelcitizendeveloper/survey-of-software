# S0: Experiment Scoping - Accounting Software

**Experiment ID:** 3.006-accounting-software
**Category:** Revenue Infrastructure & Financial Management
**Created:** October 22, 2025
**Status:** Scoping Complete → Ready for S1

---

## Challenge Definition

Every business needs to track financial transactions, generate reports, and comply with tax regulations. Founders and finance teams need to decide between:

1. **Spreadsheets** (DIY bookkeeping with Excel/Sheets)
2. **Small business accounting software** (QuickBooks, Xero, FreshBooks, Wave)
3. **Mid-market accounting platforms** (Sage Intacct, NetSuite accounting module)
4. **Full ERP systems** (NetSuite, SAP, Dynamics - see 3.502)

**Core Question:** What accounting software exists across the small business to mid-market spectrum, and when should you use accounting software vs graduating to a full ERP?

---

## Experiment Scope

### **In Scope**
- General ledger and chart of accounts
- Accounts receivable (A/R) and invoicing
- Accounts payable (A/P) and bill management
- Bank reconciliation and transaction categorization
- Financial reporting (P&L, balance sheet, cash flow statements)
- Tax preparation support and compliance
- Multi-currency and international operations
- Payroll integration capabilities
- Inventory accounting (COGS tracking)
- Project/job costing and tracking
- Subscription billing and recurring revenue
- Multi-entity and consolidation features
- Cloud-based and desktop solutions
- Integration ecosystem (banks, payment processors, CRM, payroll)
- Small business (freelancers to 50 employees)
- Mid-market (50-500 employees)

### **Out of Scope**
- Full ERP systems (covered in 3.502 ERP Platforms)
  - NetSuite full platform, SAP S/4HANA, Oracle ERP Cloud, Microsoft Dynamics 365 (full suite)
  - Note: NetSuite accounting module and Dynamics Business Central included as they're marketed as accounting software
- Cash flow forecasting tools (covered in 3.004 Cash Flow & Financial Planning)
  - Pulse, Fathom, Finmark, Jirav, Causal - these COMPLEMENT accounting software
- Financial simulation libraries (covered in 1.127)
  - Developer tools for custom modeling, not accounting systems
- Personal finance software (Mint, YNAB, Personal Capital)
- Consumer tax filing services (TurboTax, H&R Block Online)
- Custom enterprise solutions requiring extensive professional services
- Region-specific solutions unavailable in North America/Europe
- Specialty accounting (fund accounting for nonprofits - brief mention only)

---

## Key Discovery Questions

### S1: Rapid Library Search
- What are the major accounting platforms by market segment?
  - Small business (freelancers, sole proprietors, <50 employees)
  - Mid-market (50-500 employees, multi-entity)
- Which solutions are most commonly used?
- What's the "default choice" for different business sizes?
- Free vs paid: When is Wave sufficient vs QuickBooks/Xero?

### S2: Comprehensive Solution Analysis
- Full landscape: Small business → Mid-market → ERP continuum
- Feature comparison: Core accounting, invoicing, expense tracking, reporting, multi-currency, consolidation
- Pricing models: Free with paid add-ons, monthly subscription, user-based, tiered plans
- Integration ecosystems: Banking (Plaid), payroll (Gusto, ADP), payment processors (Stripe, Square), e-commerce (Shopify)
- Cloud vs desktop: QuickBooks Online vs Desktop, Xero cloud-only
- Accountant/bookkeeper ecosystem: Which platforms do professionals prefer?
- Industry-specific features: Service businesses, product/inventory, construction, SaaS/subscriptions

### S3: Need-Driven Discovery
- **Use case:** Solo freelancer (simple invoicing + expense tracking)
- **Use case:** Product-based small business (inventory + COGS)
- **Use case:** SaaS startup (subscription revenue recognition, deferred revenue)
- **Use case:** Multi-location retail/restaurant chain (consolidation, job costing)
- **Use case:** Professional services firm (project tracking, billable hours)
- **Use case:** International business (multi-currency, VAT/GST)
- **Use case:** Growing company approaching ERP decision point
- Requirements-to-solution matching framework

### S4: Strategic Selection
- **Decision tree:** Accounting software vs ERP - when to graduate?
- **Integration strategy:** How accounting fits with cash flow tools (3.004), payment processing (3.001), ERP (3.502)
- **Trade-offs:** Simplicity vs features, cost vs scalability, lock-in vs flexibility
- **Migration paths:** Starting with Wave/FreshBooks → QuickBooks/Xero → Intacct/NetSuite
- **TCO analysis:** Subscription + implementation + training + add-ons + accountant fees
- **Accountant compatibility:** How important is your accountant's platform preference?
- **Vendor viability:** Public companies (Intuit, Oracle) vs private (Xero, Sage)
- Future-proofing: When does QuickBooks/Xero become a bottleneck?

---

## Expected Outcomes

### Deliverables
1. **S1:** Quick reference list of top 10-15 accounting platforms (segmented by size)
2. **S2:** Comprehensive provider catalog with features/pricing/integrations
3. **S3:** Use case → solution matching guide (by business type, size, industry)
4. **S4:** Strategic decision framework with clear selection criteria
5. **SYNTHESIS:** Executive summary with decision tree (accounting vs ERP graduation)

### Key Decision Frameworks

**Framework 1: Accounting Software vs ERP**
```
QUESTION: When do you need ERP instead of accounting software?

SIGNALS FOR ACCOUNTING SOFTWARE (3.006):
→ Single entity or simple consolidation
→ <$10M revenue, <100 employees
→ Accounting is primary need (finance-focused)
→ Limited manufacturing/complex supply chain
→ Standard business processes

SIGNALS FOR ERP (3.502):
→ Multi-entity complex consolidation
→ >$20M revenue, >100 employees, multiple departments
→ Need integrated: accounting + inventory + manufacturing + HR + CRM
→ Complex supply chain, job costing, project management
→ Extensive customization and workflow automation needed
```

**Framework 2: Free vs Paid Small Business**
```
QUESTION: When is free Wave sufficient vs paid QuickBooks/Xero?

FREE (Wave) WORKS WHEN:
→ <$500K revenue, solo or very small team
→ Simple invoicing + expense tracking
→ Don't need inventory management
→ Don't need complex reporting
→ Can tolerate limited integrations

PAID (QuickBooks/Xero/FreshBooks) NEEDED WHEN:
→ >$500K revenue or growing fast
→ Need inventory/COGS tracking
→ Need multi-user collaboration
→ Need accountant/bookkeeper collaboration
→ Need advanced reporting and forecasting
→ Need extensive integrations (payroll, e-commerce, etc.)
```

**Framework 3: Small Business vs Mid-Market**
```
QUESTION: When to graduate from QuickBooks/Xero to Sage Intacct/NetSuite?

STAY WITH SMALL BUSINESS ACCOUNTING WHEN:
→ Single entity or 2-3 simple entities
→ <$5M revenue
→ <25 employees
→ Single currency or simple multi-currency
→ Standard reporting sufficient

GRADUATE TO MID-MARKET WHEN:
→ Multi-entity with complex consolidation
→ >$5M revenue, growing to $20M+
→ 25-200 employees
→ Complex multi-currency with intercompany transactions
→ Need custom reports, dashboards, analytics
→ Need role-based access control (RBAC) for larger teams
→ Outgrowing QuickBooks entity limits or performance
```

---

## Success Criteria

**S0 is complete when:**
- ✅ Challenge clearly defined (accounting software landscape + ERP decision)
- ✅ Scope boundaries set (what's in/out - excludes ERP, cash flow tools, tax software)
- ✅ Discovery questions articulated for S1-S4
- ✅ Expected outcomes and deliverables defined
- ✅ Ready to begin S1 rapid search

**Experiment is complete when:**
- Business owner can quickly identify accounting platforms by size/need (S1)
- Business owner can compare features/pricing/integrations (S2)
- Business owner can match their requirements to best-fit solution (S3)
- Business owner can make strategic choice with confidence, including knowing when to graduate to ERP (S4)
- Decision framework enables accounting vs ERP decision
- Clear integration guidance with 3.004 (cash flow tools), 3.502 (ERP), 1.127 (financial simulation)

---

## Context Notes

### Why This Experiment Matters

**Real-world insight:** Many businesses start with spreadsheets, graduate to QuickBooks/Xero, then face a painful migration to NetSuite/Intacct when they outgrow small business accounting. Understanding the continuum upfront helps avoid costly migrations.

**Cost of wrong choice:**
- Stay too long in spreadsheets → Tax compliance errors, missed deductions, audit risk
- Choose wrong small business platform → Poor accountant compatibility, migration pain
- Graduate to ERP too early → Overpay for unneeded features, complex implementation
- Graduate to ERP too late → Outgrow platform limits, workarounds, data integrity issues

**Ideal outcome:** Clear decision framework that optimizes for current needs while planning for future growth.

### Critical Relationships

**3.004 Cash Flow & Financial Planning:**
- Cash flow tools (Pulse, Fathom, Finmark) INTEGRATE WITH accounting software
- They don't replace accounting - they add forecasting and scenario planning
- Decision: Accounting software is required first, cash flow tools are optional add-ons

**3.502 ERP Platforms:**
- ERP includes accounting as one module among many (+ inventory, manufacturing, HR, CRM)
- Decision: When accounting is 20%+ of your software needs, stay with accounting software
- When accounting is <20% of needs (manufacturing, supply chain dominant), consider ERP

**1.127 Financial Simulation Libraries:**
- Developer tools for custom financial modeling (Monte Carlo, scenario planning)
- Complements accounting software for custom analysis
- Decision: Use accounting for transactional data, simulation libraries for custom forecasting

---

## Experiment Methodology

Following MPSE_V3 framework:
- **S0:** ✅ Scoping (this document)
- **S1:** Rapid search (30-45 min - identify top providers by segment)
- **S2:** Comprehensive analysis (3-4 hours - full landscape across tiers)
- **S3:** Need-driven discovery (2-3 hours - use case matching by business type)
- **S4:** Strategic selection (1-2 hours - graduation framework, TCO, viability)
- **SYNTHESIS:** Executive summary (30-45 min - consolidate findings, decision trees)

**Total estimated time:** 7-10 hours of focused research

---

## Priority Research Questions

1. **When to graduate from QuickBooks/Xero to Sage Intacct/NetSuite?** (S4)
2. **How do cash flow tools (3.004) complement accounting software?** (S4, cross-reference)
3. **What triggers the need for full ERP (3.502)?** (S4, decision framework)
4. **When is free Wave sufficient vs paid solutions?** (S3)
5. **How important is accountant/bookkeeper ecosystem compatibility?** (S2, S4)
6. **What's the true TCO including implementation, training, and add-ons?** (S2, S4)
7. **Industry-specific requirements:** SaaS subscription revenue, construction job costing, inventory COGS (S3)

---

**Status:** S0 Complete - Ready for S1
**Next Step:** Begin S1 rapid library search
**Key Focus:** Small business → Mid-market continuum + ERP graduation decision framework
