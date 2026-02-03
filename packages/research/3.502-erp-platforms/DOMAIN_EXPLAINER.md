# ERP Platforms: Domain Explainer

**Category**: 3.502 - ERP Platforms (Managed Services)
**Date**: November 2, 2025
**Purpose**: Comprehensive guide to Enterprise Resource Planning (ERP) systems

---

## Table of Contents

1. [What is ERP?](#i-what-is-erp)
2. [ERP vs Accounting Software](#ii-erp-vs-accounting-software)
3. [ERP Components](#iii-erp-components)
4. [When to Adopt ERP](#iv-when-to-adopt-erp)
5. [ERP Platform Types](#v-erp-platform-types)
6. [ERP Selection Framework](#vi-erp-selection-framework)
7. [Implementation Approach](#vii-implementation-approach)
8. [Common Pitfalls](#viii-common-pitfalls)
9. [Three Paths Pattern](#ix-three-paths-pattern)
10. [The Bottom Line](#x-the-bottom-line)

---

## I. What is ERP?

### Definition

**ERP (Enterprise Resource Planning)** is an integrated business management software platform that unifies core business processes—financials, inventory, manufacturing, sales, purchasing, HR, and more—into a single system of record.

**Key Characteristics**:
- **Integrated**: All modules share one database (no data silos)
- **Real-time**: Changes in one module instantly update others
- **Comprehensive**: Covers end-to-end business processes
- **Scalable**: Designed to support growth from $5M to $500M+ revenue

**ERP is the "operating system" for your business** - just as Windows runs your computer, ERP runs your company.

---

### Brief History

**1960s-1970s**: **MRP** (Material Requirements Planning)
- Manufacturing companies need to plan material purchases based on production schedules
- IBM develops early inventory management systems
- Mainframe-based, expensive, limited to large manufacturers

**1980s-1990s**: **MRP II** → **ERP**
- MRP expands to cover manufacturing + financials + HR
- SAP R/3 (1992) and Oracle Applications define "ERP" category
- Client-server architecture, still expensive ($1M-$10M+)
- Limited to Fortune 500 companies

**2000s-2010s**: **Cloud ERP Emerges**
- NetSuite (1998, launched as "NetLedger") pioneers cloud ERP
- Salesforce proves SaaS model (CRM, then platform)
- Cloud ERP makes enterprise software accessible to mid-market
- Cost drops from $1M-$10M to $50K-$500K

**2015-2025**: **Modern Cloud ERP**
- Microsoft Dynamics 365 Business Central (cloud-first ERP)
- Acumatica (consumption-based pricing, unlimited users)
- Odoo (open-source ERP for SMBs)
- AI integration (Copilot in Dynamics 365 BC, 2024-2025)

**2025 and Beyond**: **AI-Powered ERP**
- Generative AI (chatbots, financial analysis, automated workflows)
- Predictive analytics (demand forecasting, churn prediction)
- Autonomous ERP (self-managing, self-optimizing)
- ERP becomes intelligent assistant, not just system of record

---

## II. ERP vs Accounting Software

### The Critical Decision

**This is the #1 question**: Do we need ERP, or is accounting software (QuickBooks, Xero) enough?

### Accounting Software (QuickBooks, Xero, FreshBooks)

**Core Focus**: **Financial accounting** (general ledger, A/R, A/P, banking)

**What You Get**:
- Chart of accounts and double-entry bookkeeping
- Invoicing and billing customers
- Paying bills and managing vendors
- Bank reconciliation
- Basic financial reports (P&L, balance sheet, cash flow)
- Tax preparation support

**What You Don't Get**:
- ❌ Inventory management (or very basic)
- ❌ Manufacturing (BOMs, work orders, production tracking)
- ❌ Advanced order management
- ❌ Project accounting (time tracking, project P&L)
- ❌ Multi-location / multi-entity support
- ❌ Advanced reporting and BI

**Best For**:
- Service businesses (consulting, agencies, freelancers)
- Small retailers (1 location, simple inventory)
- Companies <$5M revenue, <25 employees
- Businesses without inventory or manufacturing

**Cost**: $30-$200/month ($360-$2,400/year)

---

### ERP (NetSuite, Dynamics, SAP, Odoo, Acumatica)

**Core Focus**: **Entire business** (financials + operations + supply chain + manufacturing + projects + HR)

**What You Get**:
- Everything from accounting software, PLUS:
- ✅ Full inventory management (multi-location, lot/serial tracking, WMS)
- ✅ Manufacturing (BOMs, work orders, MRP, shop floor, quality)
- ✅ Advanced order management (drop-ship, back-orders, kitting)
- ✅ Project accounting (time & expense, billing, project P&L)
- ✅ Multi-entity consolidation (parent + subsidiaries)
- ✅ CRM integration (sales pipeline → orders → invoices → revenue)
- ✅ Supply chain (procurement, vendor management, purchasing)
- ✅ Advanced BI and reporting (dashboards, KPIs, drill-down)
- ✅ Workflow automation (approvals, alerts, business rules)

**Best For**:
- Manufacturing companies (need BOMs, work orders, MRP)
- Distribution/wholesale (multi-warehouse inventory)
- E-commerce businesses (order management + inventory sync)
- Multi-entity companies (parent + subsidiaries)
- Companies >$5M revenue, >25 employees
- Businesses with operational complexity

**Cost**: $15,000-$500,000/year (depending on platform and users)

---

### Side-by-Side Comparison

| Feature | Accounting Software | ERP |
|---------|---------------------|-----|
| **General Ledger** | ✅ Yes | ✅ Yes (more advanced) |
| **A/R, A/P** | ✅ Yes | ✅ Yes |
| **Bank Reconciliation** | ✅ Yes | ✅ Yes |
| **Basic Financial Reports** | ✅ Yes | ✅ Yes |
| **Multi-Entity Consolidation** | ❌ Limited | ✅ Yes |
| **Inventory (Multi-Location)** | ⚠️ Basic | ✅ Advanced |
| **Manufacturing (BOMs, MRP)** | ❌ No | ✅ Yes |
| **Order Management** | ⚠️ Basic | ✅ Advanced |
| **Project Accounting** | ⚠️ Limited | ✅ Full |
| **CRM Integration** | ⚠️ Via add-ons | ✅ Native |
| **Warehouse Management** | ❌ No | ✅ Yes |
| **Supply Chain** | ❌ No | ✅ Yes |
| **Advanced BI/Dashboards** | ⚠️ Limited | ✅ Yes |
| **Workflow Automation** | ⚠️ Limited | ✅ Extensive |
| **SOX Compliance** | ⚠️ Limited | ✅ Yes |
| **Users** | 1-25 | 10-10,000+ |
| **Cost** | $0.4K-$2K/year | $15K-$500K/year |

---

### Decision Framework: Accounting vs ERP

**Choose Accounting Software (QuickBooks/Xero) if**:
- Revenue <$5M, <25 employees
- Simple operations (services, freelancing, small retail)
- No inventory or basic inventory (1 location)
- No manufacturing
- Budget <$50K/year for business software

**Choose ERP if**:
- Revenue >$5M or >25 employees
- Manufacturing operations (BOMs, work orders, production tracking)
- Multi-location inventory (2+ warehouses)
- Complex order management (drop-ship, kitting, configurations)
- Multi-entity (parent + subsidiaries needing consolidation)
- Planning to go public (SOX compliance)
- Spending >10 hours/week on spreadsheets (inventory, costing, reporting)

**Graduation Path**: Most companies start with QuickBooks/Xero, then graduate to ERP at $5M-$10M revenue

[See `01-discovery/S3-need-driven/graduation-triggers.md` for detailed migration triggers]

---

## III. ERP Components (Modules)

### Core ERP Modules

**1. Financial Management** (Always included)
- General ledger, A/R, A/P, fixed assets
- Bank reconciliation, cash management
- Multi-currency, multi-GAAP
- Financial reporting and consolidation

**2. Order Management** (Always included)
- Sales orders, purchase orders
- Quotes, invoicing, fulfillment
- Drop-ship, back-orders, returns

**3. Inventory Management** (Usually included)
- Item master, SKUs, BOMs
- Multi-location, multi-warehouse
- Lot/serial tracking, expiration dates
- Inventory valuation (FIFO, LIFO, Average)

---

### Optional/Add-On Modules

**4. Manufacturing** (Often separate module)
- Work orders, production scheduling
- Bill of materials (BOMs), routing
- MRP (Material Requirements Planning)
- Shop floor management, quality control

**5. Warehouse Management System (WMS)** (Often separate)
- Bin/zone management
- Wave picking, batch picking
- Mobile barcode scanning
- Cycle counting, inventory adjustments

**6. Project Accounting** (Often separate)
- Project planning, budgeting
- Time & expense tracking
- Project billing (T&M, fixed, milestone)
- Project profitability and WIP

**7. CRM** (Customer Relationship Management)
- Lead management, opportunity pipeline
- Contact management, activities
- Marketing automation (basic)
- Sales forecasting

**8. Human Resources** (Often separate or minimal)
- Employee master, organizational chart
- Time tracking, attendance
- Payroll (basic or via integration)
- Benefits, recruiting (advanced HR)

**9. E-Commerce** (Platform-specific)
- Native online store (NetSuite SuiteCommerce, Odoo eCommerce)
- Or integration with Shopify, WooCommerce, Magento
- Real-time inventory sync

**10. Business Intelligence** (Usually included)
- Dashboards, KPIs, reports
- Drill-down and ad-hoc queries
- Data visualization
- Power BI integration (Dynamics BC)

---

### Module Architecture

**All-in-One Suite** (NetSuite, Oracle ERP Cloud):
- All modules in one platform
- Single database, deep integration
- Higher cost, less flexibility

**Modular / Best-of-Breed** (Dynamics 365, Acumatica):
- Pick the modules you need
- Start with financials, add manufacturing later
- More flexible, but integration complexity

**Open Source / Flexible** (Odoo):
- 80+ apps, pick what you need
- Free (Community) or paid (Enterprise)
- Most flexible, requires technical expertise

---

## IV. When to Adopt ERP

### Revenue & Size Triggers

| Revenue | Employees | Typical System | Notes |
|---------|-----------|----------------|-------|
| **<$1M** | 1-10 | QuickBooks/Xero | Too early for ERP |
| **$1M-$5M** | 10-25 | QuickBooks Enterprise | Consider ERP if manufacturing |
| **$5M-$25M** | 25-100 | **Evaluate ERP** | Common graduation point |
| **$25M-$100M** | 100-500 | **ERP Required** | Operations too complex for accounting software |
| **$100M-$500M** | 500-2,000 | **ERP (Mid-Market)** | NetSuite, Dynamics, Acumatica |
| **$500M+** | 2,000+ | **Enterprise ERP** | Oracle ERP Cloud, SAP S/4HANA |

---

### Operational Complexity Triggers

**Immediate ERP Need** (regardless of size):
- **Manufacturing operations** (need BOMs, work orders, MRP)
- **Multi-location inventory** (2+ warehouses, need real-time visibility)
- **Multi-entity** (parent + subsidiaries, need consolidation)

**Strong ERP Candidate**:
- Complex order management (drop-ship, kitting, configurations)
- Project-based business (time tracking, project billing, WIP)
- E-commerce + warehouse (need real-time inventory sync)

**Consider ERP**:
- Spending >10 hours/week on spreadsheets (inventory, job costing, reporting)
- Integration pain (manual data entry between systems)
- Hitting user or transaction limits in accounting software

[See `01-discovery/S3-need-driven/graduation-triggers.md` for full decision tree]

---

## V. ERP Platform Types

### Type 1: Cloud SaaS (Most Common)

**Examples**: NetSuite, Dynamics 365 BC, Acumatica (SaaS deployment)

**Characteristics**:
- Hosted by vendor (no infrastructure management)
- Subscription pricing (monthly or annual)
- Automatic updates (quarterly releases typical)
- Multi-tenant (data segregated, infrastructure shared)
- Accessible from anywhere (browser-based)

**Pros**: No infrastructure, always up-to-date, scalable, lower upfront cost
**Cons**: Less control, vendor lock-in, recurring cost

**Best For**: Most companies (90%+ of new ERP deployments are cloud)

---

### Type 2: On-Premise (Legacy)

**Examples**: SAP Business One (on-prem), Odoo Community (self-hosted)

**Characteristics**:
- Installed on your own servers
- Perpetual license (one-time purchase) or subscription
- You manage infrastructure (servers, backups, security)
- Single-tenant (dedicated environment)
- Updates are manual (major version upgrades)

**Pros**: Full control, data sovereignty, no recurring cost (perpetual), can run in air-gapped environment
**Cons**: High upfront cost, infrastructure management, slower updates, scalability limited by hardware

**Best For**: Regulated industries (data residency), air-gapped environments, companies with strong IT teams

**Trend**: Declining (cloud adoption is 80%+ of new ERP)

---

### Type 3: Open Source (Self-Hosted or SaaS)

**Examples**: Odoo Community (self-hosted), Odoo Enterprise (SaaS), ERPNext

**Characteristics**:
- Source code available (LGPL, MIT, etc.)
- Self-hosted (infrastructure you manage) or vendor-hosted (SaaS)
- Free (Community) or paid (Enterprise with support)
- Community-driven development
- Fork-able (can modify and maintain your own version)

**Pros**: Zero software cost (Community), no vendor lock-in, maximum flexibility, community support
**Cons**: Requires technical expertise, support quality varies, upgrade complexity

**Best For**: Budget-constrained companies with technical resources, want maximum control

---

### Type 4: Hybrid (Private Cloud)

**Examples**: Acumatica (private cloud), SAP Business One (private cloud), Odoo (Odoo.sh)

**Characteristics**:
- Hosted on your own cloud (AWS, Azure, GCP)
- You control infrastructure but in cloud (not on-premise)
- Vendor provides software, you manage hosting
- More control than SaaS, more flexible than on-premise

**Pros**: Control + cloud flexibility, data residency options, easier scaling than on-premise
**Cons**: More expensive than SaaS, requires cloud expertise

**Best For**: Companies needing data residency + cloud benefits, hybrid IT strategy

---

## VI. ERP Selection Framework

### The ERP Selection Process (Step-by-Step)

**Phase 1: Requirements Definition (2-4 weeks)**
1. Document current pain points with existing system
2. Define must-have features vs nice-to-have
3. Map business processes (order-to-cash, procure-to-pay, manufacturing)
4. Identify integrations needed (e-commerce, CRM, payment, shipping)
5. Define success criteria (what does "good" look like?)

**Phase 2: Platform Shortlisting (2-4 weeks)**
1. Use this research to shortlist 3-4 platforms
2. Quick evaluation:
   - Budget fit ($50K/year → Dynamics BC; $200K/year → NetSuite)
   - Industry fit (manufacturing → SAP B1; e-commerce → NetSuite or Odoo)
   - Technical fit (Microsoft shop → Dynamics; technical team → Odoo)
3. Request demos from shortlisted vendors

**Phase 3: Vendor Demos & Evaluation (4-8 weeks)**
1. Schedule demos (2-3 hours each)
2. Focus demos on YOUR workflows (not generic features)
3. Test with real data (not dummy data)
4. Involve key users (accounting, operations, warehouse, sales)
5. Score each platform (feature fit, ease of use, cost)

**Phase 4: Reference Checks (2-3 weeks)**
1. Request 3-5 references from vendor (companies in your industry, similar size)
2. Ask tough questions:
   - What went wrong during implementation?
   - What would you do differently?
   - How is support quality?
   - Would you choose this ERP again?
3. Check online reviews (G2, Capterra, Reddit)

**Phase 5: Partner Selection (2-4 weeks)**
1. If using implementation partner, select carefully
2. Interview 2-3 partners
3. Check partner references (3-5 implementations they've done)
4. Negotiate fixed-price vs time & materials
5. Define success criteria and acceptance testing

**Phase 6: Contract Negotiation (2-4 weeks)**
1. Negotiate software pricing (multi-year discounts, upfront payment discounts)
2. Negotiate implementation pricing (fixed-price preferred)
3. Define exit terms (data export, contract termination)
4. Get legal review (especially for NetSuite, Oracle - Oracle is aggressive)

**Total Timeline**: 3-6 months from requirements to signed contract

[See `01-discovery/S1-rapid/recommendation.md` for platform shortlisting guidance]

---

### Key Selection Criteria

**1. Industry Fit** (30% weight)
- Does the ERP support your industry? (manufacturing, distribution, services, etc.)
- Are there industry-specific modules or editions?
- Do references include companies in your industry?

**2. Functional Fit** (25% weight)
- Does it have the features you need? (manufacturing, project accounting, e-commerce)
- How much customization is required? (less is better)
- Are there gaps that require workarounds?

**3. Cost** (20% weight)
- First-year total cost (software + implementation + training)
- 5-year TCO (total cost of ownership)
- ROI potential (productivity gains, error reduction, better decisions)

**4. Ease of Use** (15% weight)
- Is the UI intuitive? (less training required)
- How long to train users? (1 week vs 1 month)
- User satisfaction (G2 ratings, references)

**5. Vendor Viability** (10% weight)
- Is the vendor financially stable?
- Is the product growing or declining?
- What's the 5-10 year outlook?

[See `01-discovery/S2-comprehensive/feature-matrix.md` for detailed feature comparison]

---

## VII. Implementation Approach

### Implementation Timeline

**Typical ERP Implementation**: 3-6 months (mid-market)

| Phase | Duration | Activities | Deliverables |
|-------|----------|------------|--------------|
| **Discovery** | 2-4 weeks | Requirements, process mapping, design | Requirements doc, design doc |
| **Configuration** | 3-6 weeks | Setup ERP, configure modules, customize | Configured sandbox |
| **Data Migration** | 4-8 weeks | Extract, transform, load (2-3 iterations) | Migrated data, reconciliation |
| **Testing** | 2-4 weeks | UAT (user acceptance testing) | UAT sign-off |
| **Training** | 2-4 weeks | Train users (8-16 hours per user) | Trained users |
| **Cutover** | 1 weekend | Go-live, final data migration | Production system |
| **Hypercare** | 2-4 weeks | Post-go-live support, issue resolution | Stabilized system |

**Total**: 16-30 weeks (4-7.5 months)

---

### Implementation Success Factors

**Critical Success Factor #1: Executive Sponsorship**
- CEO or CFO must champion the project
- ERP implementation is 80% change management, 20% technology
- Without executive support, users will resist

**Critical Success Factor #2: Experienced Implementation Partner**
- Partner experience matters more than ERP choice
- Check references (3-5 implementations in your industry)
- Fixed-price projects force partner accountability

**Critical Success Factor #3: Clean Data**
- Garbage in = garbage out
- Budget 20-40 hours for data cleanup before migration
- Archive old/obsolete records (don't migrate everything)

**Critical Success Factor #4: Dedicated Project Team**
- Full-time project manager (internal)
- Key users from each department (50% time)
- Don't try to implement while running day-to-day operations

**Critical Success Factor #5: Training Investment**
- Budget 10-20% of implementation cost for training
- 8-16 hours hands-on training per user
- Create video tutorials and quick reference guides

[See `01-discovery/S3-need-driven/migration-guide.md` for detailed implementation playbook]

---

## VIII. Common Pitfalls

### Pitfall #1: Underestimating Implementation Cost

**Problem**: Budget $50K for ERP software, forget about $50K-$150K implementation

**Reality**:
- Implementation costs 50-200% of annual software cost
- Dynamics 365 BC: $35K/year software → $20K-$35K implementation
- NetSuite: $60K/year software → $60K-$120K implementation

**Solution**: Budget 1.5-2x annual software cost for first-year total

---

### Pitfall #2: Rushing Implementation

**Problem**: Go-live in 2 months (vs recommended 4-6 months)

**Consequences**:
- Insufficient testing (discover bugs in production)
- Poor training (users don't know how to use system)
- Data migration errors (reconciliation issues)
- Go-live failure (rollback and restart)

**Solution**: Follow 4-6 month timeline, don't cut corners

---

### Pitfall #3: Over-Customization

**Problem**: Customize ERP to match current processes exactly

**Consequences**:
- High customization cost ($50K-$200K)
- Difficult upgrades (customizations break)
- Vendor lock-in (can't switch without losing customizations)
- Longer implementation (6-12 months vs 4-6)

**Solution**: Adapt processes to ERP best practices (80% standard, 20% custom)

---

### Pitfall #4: Choosing Wrong Platform

**Problem**: Choose NetSuite ($200K first year) when Dynamics BC ($65K) would suffice

**Consequences**:
- 3x higher cost
- More complex implementation
- Feature overkill (paying for features you don't need)

**Solution**: Match platform to company size and complexity (use this research!)

---

### Pitfall #5: Poor Change Management

**Problem**: Focus on technology, ignore people

**Consequences**:
- User resistance ("I liked QuickBooks better")
- Workarounds (spreadsheets, manual processes)
- Low adoption (ERP not used properly)
- Failed implementation (abandon ERP, go back to old system)

**Solution**: 80% effort on change management, 20% on technology
- Involve users early (requirements gathering, UAT)
- Train extensively (8-16 hours per user)
- Celebrate wins (month-end close in 2 days vs 5 days)

---

## IX. Three Paths Pattern

### Path 1: DIY (Spreadsheets + Accounting Software)

**Approach**: Use QuickBooks/Xero + Excel for everything else

**Cost**: $2K-$10K/year (accounting software + labor)

**When to Use**:
- Revenue <$1M
- <10 employees
- Simple operations (no manufacturing, no complex inventory)

**Pros**: Cheapest, flexible, full control
**Cons**: Manual, error-prone, doesn't scale, spreadsheet hell

---

### Path 2: Open Source ERP (Odoo Community)

**Approach**: Self-hosted open source ERP

**Cost**: $20K-$100K first year (implementation + infrastructure + developer time)

**When to Use**:
- Budget <$100K/year
- Have Python/PostgreSQL expertise in-house
- Want maximum flexibility and zero vendor lock-in
- Revenue $5M-$50M

**Pros**: No software cost, full control, no lock-in
**Cons**: Requires technical expertise, community support only, upgrade complexity

[See `01-discovery/2.XXX-self-hosted` for open source ERP options - reference 1.139]

---

### Path 3: Commercial Cloud ERP (NetSuite, Dynamics, Acumatica)

**Approach**: SaaS ERP from established vendor

**Cost**: $50K-$500K/year (software + support + implementation)

**When to Use**:
- Budget >$50K/year
- Revenue >$10M or operational complexity
- Want proven, polished, enterprise-ready solution
- Need vendor support and SLAs

**Pros**: Proven, polished, scalable, vendor support, regular updates
**Cons**: Expensive, vendor lock-in, less control

---

### Recommended Path by Company Stage

| Stage | Revenue | Path | Platform Examples |
|-------|---------|------|-------------------|
| **Startup** | <$1M | Path 1 (DIY) | QuickBooks Online + Excel |
| **Early Growth** | $1M-$5M | Path 1 or 2 | QuickBooks Enterprise or Odoo Community |
| **Mid-Growth** | $5M-$25M | Path 2 or 3 | Odoo Enterprise or Dynamics 365 BC |
| **Scaling** | $25M-$100M | Path 3 | Dynamics 365 BC, Acumatica, or NetSuite |
| **Mid-Market** | $100M-$500M | Path 3 | NetSuite or Acumatica |
| **Enterprise** | $500M+ | Path 3 (Enterprise) | Oracle ERP Cloud or SAP S/4HANA |

---

## X. The Bottom Line

### Quick Decision Guide

**If you're under $5M revenue and have simple operations**:
→ Stick with **QuickBooks or Xero** (you're not ready for ERP)

**If you're $5M-$25M with manufacturing or multi-location inventory**:
→ Choose **Dynamics 365 BC** ($50K-$100K/year, best value)
→ OR **Odoo Enterprise** ($15K-$70K/year, if budget-constrained with technical team)

**If you're $25M-$100M with growing complexity**:
→ Choose **Dynamics 365 BC** (best value, AI features)
→ OR **Acumatica** (if need unlimited users for distribution/construction)
→ OR **NetSuite** (if SaaS company planning IPO)

**If you're $100M-$500M**:
→ Choose **NetSuite** (proven at scale, best multi-entity)
→ OR **Acumatica** (if distribution with large operational teams)

**If you're $500M+ revenue**:
→ Choose **Oracle ERP Cloud** or **SAP S/4HANA** (enterprise scale)

---

### Best Value Recommendations (November 2025)

**🥇 Best Overall Value**: **Microsoft Dynamics 365 Business Central**
- $80-$110/user/month
- Copilot AI included free (financial analysis, reconciliation)
- Power Platform integration (1,000+ connectors)
- 5-year TCO: $205K-$575K (50% less than NetSuite)
- Best features-to-price ratio in mid-market

**🥈 Best Budget Option**: **Odoo Enterprise**
- $25-$37/user/month
- Native e-commerce (Odoo eCommerce)
- 80+ integrated apps
- 5-year TCO: $95K-$225K (10x cheaper than NetSuite)
- Open source core = no lock-in

**🥉 Best for Manufacturing**: **SAP Business One**
- €91/user/month (~$100 USD)
- Best MRP, shop floor, quality management for SMB
- Strong in Europe, Asia, pharma/life sciences
- 5-year TCO: $510K

**🏆 Best for SaaS/IPO**: **NetSuite**
- $129-$199/user/month
- Industry standard for SaaS IPOs
- Best multi-entity consolidation
- 5-year TCO: $530K-$3.15M (premium pricing)

**🎯 Best for Unlimited Users**: **Acumatica**
- Consumption pricing (not per-user)
- Unlimited users (warehouse, field staff)
- Best for distribution, construction, field service
- 5-year TCO: $460K-$1.8M (saves $50K-$100K/year vs NetSuite for 75+ users)

---

### Key Takeaways

1. **ERP is for companies >$5M revenue** or with manufacturing/multi-location inventory
2. **Dynamics 365 BC = best value** for 80% of mid-market companies
3. **Odoo = best budget option** (10x cheaper than NetSuite)
4. **NetSuite = best for SaaS IPOs** (SOX compliance, proven)
5. **Implementation costs 50-200% of annual software** (don't underestimate)
6. **Plan 4-6 months for implementation** (don't rush)
7. **Change management is 80% of success** (technology is only 20%)

**Most Important**: **Match ERP to your company size, industry, and technical capabilities** - don't overbuy (NetSuite) or underbuy (staying on QuickBooks too long)

---

## Related Research

- **[S1 Rapid Discovery](./01-discovery/S1-rapid/recommendation.md)**: Quick platform selection (30-min decision guide)
- **[S2 Comprehensive](./01-discovery/S2-comprehensive/feature-matrix.md)**: Deep feature comparison across 6 platforms
- **[S3 Need-Driven](./01-discovery/S3-need-driven/use-case-matching.md)**: Industry and use-case matching
- **[S4 Strategic](./01-discovery/S4-strategic/build-vs-buy-analysis.md)**: Open source vs commercial analysis
- **[3.006 Accounting Software](../3.006-accounting-software/)**: When to stick with QuickBooks/Xero
- **[3.501 CRM Platforms](../3.501-crm-platforms/)**: CRM vs ERP CRM modules
- **[1.139 Self-Hosted Business Apps](../../experiments/1.139-self-hosted-business-apps/)**: Open source ERP options

---

**Last Updated**: November 2, 2025
**Version**: 1.0
**Research Coverage**: 6 platforms (NetSuite, Dynamics 365 BC, SAP Business One, Odoo, Acumatica, Oracle ERP Cloud)
