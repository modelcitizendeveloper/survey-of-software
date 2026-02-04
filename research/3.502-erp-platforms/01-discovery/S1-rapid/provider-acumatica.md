# Acumatica Cloud ERP

**Platform Type**: Cloud ERP (SaaS + Private Cloud + Perpetual)
**Owner**: Acumatica, Inc. (part of EQT private equity)
**Target Market**: Small to mid-market ($5M-$500M revenue, 25-500 employees)
**First Released**: 2008

---

## Quick Summary

Acumatica is a modern, cloud-first ERP with unique consumption-based pricing (unlimited users). Strong in manufacturing, distribution, and professional services. Known for flexibility, modern architecture, and transparent pricing. **Best for**: Growing companies that need unlimited user access and prefer consumption-based pricing over per-user fees.

---

## Pricing Overview

### Unique Pricing Model: Consumption-Based (Not Per-User)
Unlike most ERPs (NetSuite, Dynamics, SAP), Acumatica charges based on **resource consumption** (computing power, storage, transactions) rather than per-user.

**Key benefit**: **Unlimited users** - no per-seat licensing.

### Pricing Tiers (2024-2025)
Acumatica offers four tiers based on transaction volume and functionality:

1. **Essentials Edition**
   - Target: Small organizations (up to 2,000 monthly transactions, ~25 concurrent users)
   - Cost: Starting at **$1,500-$1,800/month**
   - Features: Basic financials, inventory, order management

2. **Select Edition**
   - Target: Small businesses requiring advanced financial capabilities
   - Cost: Estimated **$2,500-$4,000/month**
   - Features: Advanced financials, project accounting

3. **Prime Edition**
   - Target: Lower mid-market (up to 5,000 monthly transactions, ~50 concurrent users)
   - Cost: Estimated **$4,000-$7,000/month**
   - Features: Manufacturing, CRM, field service

4. **Enterprise Edition**
   - Target: Mid-market to large (20,000-100,000+ monthly transactions, ~100+ concurrent users)
   - Cost: Estimated **$8,000-$15,000+/month**
   - Features: Advanced manufacturing, multi-entity, advanced financial controls

### Total Cost Estimate (50-person company)
- **Prime Edition**: ~$5,000/month = **$60,000/year** (unlimited users)
- **Implementation**: $30,000-$100,000
- **Training**: $5,000-$15,000

### First-Year TCO
**$95,000-$175,000** (software + implementation + training)

**Comparison**:
- Cheaper than NetSuite ($150K-$250K) for same-sized company
- More expensive than Dynamics BC ($50K-$100K) but includes unlimited users
- Similar to Odoo Enterprise at scale, but more polished

---

## Transaction Volume Pricing

Acumatica's pricing is based on **monthly commercial transactions**:
- Sales orders
- Purchase orders
- Invoices
- Journal entries
- Inventory movements

**Example tiers**:
- **Small**: Up to 2,000 transactions/month (~25 concurrent users)
- **Medium**: Up to 5,000 transactions/month (~50 concurrent users)
- **Large**: Up to 20,000 transactions/month (~100 concurrent users)
- **Extra Large**: 100,000+ transactions/month

**Note**: Internal transactions (transfers, adjustments) typically don't count toward limit.

---

## Core Capabilities

### Financial Management ⭐⭐⭐⭐⭐
- **Strengths**: Excellent financial management
- General ledger, A/R, A/P, cash management, fixed assets
- Multi-entity, inter-company transactions
- Multi-currency, multi-GAAP support
- Advanced allocations, deferred revenue (ASC 606)
- Real-time financial dashboards
- **Verdict**: On par with NetSuite and Dynamics BC

### Manufacturing ⭐⭐⭐⭐
- **Strengths**: Strong manufacturing module
- Production management, MRP, capacity planning
- Work orders, BOMs, routing, work centers
- Engineering change orders (ECO)
- Quality management, shop floor data collection
- **Verdict**: Competitive with SAP B1, better than NetSuite for manufacturing

### Supply Chain & Distribution ⭐⭐⭐⭐⭐
- **Strengths**: Excellent for distribution businesses
- Advanced inventory management (multi-warehouse, lot/serial)
- Order management, fulfillment, replenishment
- Warehouse management (WMS module)
- Drop-ship, back-to-back sales orders
- **Verdict**: Best-in-class for distribution and wholesale

### Project Management ⭐⭐⭐⭐⭐
- **Strengths**: Exceptional project accounting
- Project planning, budgeting, time & expense
- Change orders, contract billing
- Resource allocation, profitability analysis
- **Verdict**: Best project accounting among mid-market ERPs (advantage over NetSuite, Dynamics)

### CRM ⭐⭐⭐
- Contact management, opportunity pipeline
- Marketing campaigns, lead management
- **Limitations**: CRM is functional but basic compared to Salesforce/HubSpot
- **Verdict**: Adequate CRM for integrated use, may supplement with external CRM

### Construction Management ⭐⭐⭐⭐⭐
- **Strengths**: Strong construction-specific edition
- Job costing, change orders, subcontractor management
- AIA billing, compliance, certified payroll
- **Verdict**: Excellent for construction and contractors (specialized edition)

### Field Service ⭐⭐⭐⭐
- Work order management, scheduling, dispatch
- Mobile app for technicians
- **Verdict**: Strong field service capabilities (advantage over NetSuite, Dynamics)

---

## Technical Architecture

### Deployment Options
- **Acumatica Cloud (SaaS)**: Hosted by Acumatica
- **Private Cloud**: Deploy on your own cloud (AWS, Azure, Google Cloud)
- **On-Premise**: Install on own servers (perpetual license option)

### Customization
- **Low-Code Platform**: Acumatica Framework (customization without heavy coding)
- **Generic Inquiries**: Build custom reports/dashboards without code
- **Workflow Engine**: Automate business processes
- **API**: REST, OData, SOAP APIs for integration
- **Flexibility**: High - easier to customize than NetSuite or Dynamics

### Integration
- **REST API**: Modern RESTful API
- **Pre-built connectors**: Salesforce, Shopify, WooCommerce, QuickBooks, Excel
- **EDI Integration**: B2B trading partner integration
- **iPaaS support**: Zapier, Workato, Celigo
- **Verdict**: Strong integration capabilities, modern API

### Technology Stack
- **Backend**: .NET (Microsoft stack)
- **Database**: Microsoft SQL Server
- **Frontend**: HTML5, responsive web UI
- **Modern**: Yes - modern web architecture, mobile-first design

---

## Target Company Profile

### Ideal Fit
✅ **Company size**: 25-500 employees, $5M-$500M revenue
✅ **Industries**:
   - **Distribution and wholesale** (strongest fit)
   - **Manufacturing** (discrete, job shop, make-to-order)
   - **Professional services** (consulting, engineering, architecture)
   - **Construction** (contractors, specialty trades)
   - **Field service** (HVAC, equipment service, repairs)
✅ **User base**: Need unlimited user access (salespeople, warehouse, field staff)
✅ **Growth trajectory**: Companies planning to scale rapidly (pricing scales with transactions)
✅ **Budget**: $95K-$175K first year
✅ **Technical maturity**: Appreciate modern technology, cloud-first approach

### Not a Good Fit
❌ **Very small businesses**: <10 employees, <$1M revenue (overkill, → QuickBooks, Xero)
❌ **Process manufacturing**: Complex batch processing, formulation management (→ SAP, Epicor)
❌ **Global multinationals**: Very complex multi-entity, multi-currency needs (→ NetSuite, Oracle)
❌ **Budget-constrained**: $95K+ first year too high (→ Odoo, Dynamics BC)
❌ **Microsoft ecosystem requirement**: If deeply tied to Microsoft (→ Dynamics BC)

---

## Migration Path

### Typical Migration FROM
- QuickBooks Enterprise (outgrown, need manufacturing/distribution features)
- Sage 100/300 (legacy system, want cloud)
- Microsoft Dynamics GP (end of life, moving to cloud)
- NetSuite (cost reduction, want unlimited users)
- Spreadsheets + QuickBooks (growing distribution/manufacturing companies)

### Typical Migration TO
- NetSuite or Oracle (if need more sophisticated multi-entity/international)
- Rare - most companies stay long-term due to unlimited user model

---

## Strengths

1. **Unlimited users**: No per-seat licensing (huge advantage for growing teams)
2. **Consumption pricing**: Pay for what you use (transactions), not headcount
3. **Modern UX**: Clean, intuitive interface (better than NetSuite, SAP B1)
4. **Flexibility**: Multiple deployment options (cloud, private cloud, on-premise)
5. **Strong verticals**: Construction, distribution, manufacturing editions
6. **Project accounting**: Best-in-class project management and billing
7. **Customization**: Easier to customize than NetSuite (low-code platform)
8. **Transparent pricing**: Clear pricing tiers (vs opaque NetSuite pricing)
9. **Partner ecosystem**: Strong North American partner network

---

## Weaknesses

1. **Brand awareness**: Less well-known than NetSuite, Dynamics, SAP
2. **International**: Not as strong as NetSuite for global operations (fewer localizations)
3. **CRM**: Built-in CRM is basic (may need external CRM)
4. **Ecosystem size**: Smaller ISV/add-on ecosystem vs NetSuite
5. **Enterprise readiness**: Not ideal for very large enterprises (>$1B revenue)
6. **Implementation**: Still requires 3-6 months, experienced partner needed
7. **Support**: Support quality varies by partner

---

## Competitive Position

### vs NetSuite
- **Acumatica wins on**: Unlimited users, pricing transparency, modern UX, project accounting
- **NetSuite wins on**: Financial sophistication, global reach, e-commerce, brand recognition

### vs Microsoft Dynamics 365 BC
- **Acumatica wins on**: Unlimited users, modern UX, project accounting, construction/field service
- **Dynamics wins on**: Price (per-user model cheaper for small teams), Microsoft ecosystem, AI features

### vs SAP Business One
- **Acumatica wins on**: Cloud-first, modern UX, unlimited users, easier implementation
- **SAP wins on**: Manufacturing depth, global localization, SAP ecosystem, brand

### vs Odoo
- **Acumatica wins on**: Enterprise support, construction/field service, professional services
- **Odoo wins on**: Price (5x cheaper), flexibility, e-commerce, open source option

---

## Decision Framework

**Choose Acumatica if:**
- You need **unlimited users** (warehouse staff, field techs, remote sales, partners)
- You're in **distribution, manufacturing, construction, or professional services**
- You want transparent, consumption-based pricing (vs per-user)
- You need strong **project accounting** and billing capabilities
- You value modern UX and cloud-first architecture
- Budget allows $95K-$175K first year
- You want deployment flexibility (cloud, private cloud, on-premise)

**Choose something else if:**
- Small team (<15 users) where per-user pricing is cheaper (→ Dynamics BC)
- Very tight budget (→ Odoo)
- Need strongest financial/multi-entity capabilities (→ NetSuite)
- Need native e-commerce platform (→ NetSuite, Odoo)
- Deeply integrated with Microsoft ecosystem (→ Dynamics BC)

---

## Unlimited Users Use Cases

**Warehouse staff**: 50 warehouse workers need to scan barcodes, update inventory
- **Acumatica**: $5K/month (unlimited users)
- **NetSuite**: $5K/month + (50 × $129) = $11,450/month
- **Savings**: $6,450/month = $77,400/year

**Field service techs**: 30 technicians need mobile access for work orders
- **Acumatica**: Included in base price
- **Dynamics BC**: 30 × $110 = $3,300/month extra
- **Savings**: $39,600/year

**Verdict**: Acumatica's unlimited user model is transformative for businesses with large operational workforces.

---

## Industry-Specific Editions

Acumatica offers tailored editions:
1. **Distribution Edition**: Wholesale, retail, e-commerce
2. **Manufacturing Edition**: Discrete and job shop manufacturing
3. **Construction Edition**: General contractors, specialty trades
4. **Commerce Edition**: Omnichannel retail
5. **Professional Services Edition**: Consulting, engineering (launched Oct 2024)

Each edition includes industry-specific features and best practices.

---

## Market Position

- **Customers**: 8,000+ customers (smaller than NetSuite's 37,000, but growing fast)
- **Partner network**: 300+ VARs in North America (strongest), Europe, Asia-Pacific
- **G2 rating**: 4.4/5.0 (400+ reviews) - **Highest rated among cloud ERPs**
- **Gartner**: Niche player (Cloud ERP for Product-Centric Midmarket Companies)
- **Growth**: 25%+ annual growth (2022-2025)
- **Awards**: Consistently wins "Best Cloud ERP" awards from industry publications

---

## Key Takeaways

Acumatica is the **best value cloud ERP for companies needing unlimited users**, especially in distribution, construction, and professional services. The consumption-based pricing model is disruptive and can save $50K-$100K/year vs NetSuite for companies with large operational teams.

**Best use case**: 150-person distribution company ($75M revenue), 100 warehouse/field staff, strong project accounting needs, budget of $120K first year. Acumatica saves $80K/year vs NetSuite due to unlimited users.

**Worst use case**: 15-person SaaS startup needing just accounting + CRM, no warehouse or field staff. Dynamics BC at $110/user/mo ($19,800/year) is far cheaper than Acumatica ($60K+/year).

---

## Acumatica vs NetSuite: Head-to-Head

| Feature | Acumatica | NetSuite |
|---------|-----------|----------|
| **Pricing Model** | Consumption-based | Per-user |
| **Users** | Unlimited | Pay per user |
| **50-user cost** | ~$60K/year | ~$130K/year |
| **UX** | Modern, clean | Functional, dated |
| **Financials** | Excellent | Best-in-class |
| **Manufacturing** | Very good | Good |
| **Project Accounting** | Excellent | Good |
| **E-commerce** | Via integration | Native |
| **Global** | Good | Excellent |
| **Brand** | Growing | Market leader |

**Verdict**: Acumatica for **distribution, construction, professional services** with large teams; NetSuite for **global, multi-entity, e-commerce, SaaS** companies.

---

**Sources**:
- Acumatica official website and pricing
- G2, Capterra, SelectHub reviews
- ERP partner pricing data
- Industry analyst reports (Gartner, Forrester)
