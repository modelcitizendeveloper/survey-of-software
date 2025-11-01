# S3 Need-Driven Discovery - Approach

**Experiment**: 3.007 FP&A Platforms
**Stage**: S3 - Need-Driven Discovery
**Date**: November 1, 2025

---

## Methodology

**Goal**: Map generic business scenarios to FP&A platform requirements using S1/S2 catalog data.

**Scope**: 5 representative scenarios spanning startup to enterprise, applying feature/integration matrices from S2.

**Time Investment**: 3-5 days

---

## Hardware Store Application Model

**Critical Distinction**:
- **S1/S2 = Generic Catalog**: Platform facts, features, integrations, pricing (timeless)
- **S3 = Scenario Mapping**: Apply catalog to generic business contexts (repeatable patterns)
- **Client Engagement = Specific Application**: Client context → platform shortlist (billable consulting)

**S3 Purpose**: Demonstrate HOW to apply catalog data, not WHICH platform to choose for a specific client.

---

## 5 Generic Scenarios

### Scenario 1: Tech Startup (50 Employees)
**Profile**: Series A SaaS company, rapid hiring, modern tech stack
**Requirements**: Fast setup (weeks not months), HRIS integration, affordable ($5K-30K/year)
**Tech Stack**: Rippling (HRIS), QuickBooks Online (accounting), Stripe (billing)
**Constraint**: Cannot wait 3-6 months for implementation

**Scenario Mapping**: Which platforms match these requirements based on S2 integration/implementation data?

---

### Scenario 2: SaaS Scale-Up (200 Employees)
**Profile**: Series B-C company, technical finance team, data warehouse in place
**Requirements**: Snowflake integration, flexible modeling, SaaS metrics (ARR, cohorts)
**Tech Stack**: Snowflake (data warehouse), NetSuite (ERP), Salesforce (CRM), Gusto (HRIS)
**Constraint**: Finance team prefers SQL-based modeling

**Scenario Mapping**: Which platforms support data warehouse-native integration?

---

### Scenario 3: Manufacturing Mid-Market (500 Employees)
**Profile**: Traditional manufacturer, multi-entity (3 subsidiaries), NetSuite ERP
**Requirements**: Multi-entity consolidation, NetSuite integration, driver-based planning
**Tech Stack**: NetSuite (ERP), ADP Workforce Now (HRIS)
**Constraint**: Need consolidation but not full enterprise CPM complexity

**Scenario Mapping**: Mid-market platforms with strong NetSuite + consolidation?

---

### Scenario 4: Enterprise Migration (2,000 Employees)
**Profile**: Large company leaving Oracle HCM, need cost reduction vs current FP&A spend
**Requirements**: Oracle Financials integration (keeping), reduce cost, improve UX vs legacy
**Tech Stack**: Oracle Financials (ERP), migrating from Oracle HCM → Paycom (HRIS)
**Constraint**: Must reduce total FP&A cost (currently $500K+/year)

**Scenario Mapping**: Enterprise platforms cheaper than incumbent, better UX?

---

### Scenario 5: Private Equity Portfolio (10 Entities)
**Profile**: PE firm with 10 portfolio companies, need consolidated view
**Requirements**: Sub-consolidation, multi-GAAP, roll-up across different ERP systems
**Tech Stack**: Mixed (each portfolio company has different ERP)
**Constraint**: Complex ownership structures, frequent acquisitions/dispositions

**Scenario Mapping**: Which platforms handle complex consolidation with mixed ERP?

---

## Scenario Document Structure

Each scenario file includes:

1. **Scenario Context** (generic business profile)
2. **Requirements Analysis** (derived from scenario, not client-specific)
3. **Platform Matching** (apply S2 feature/integration matrices)
4. **Key Trade-offs** (feature coverage vs cost vs implementation time)
5. **Implementation Considerations** (timeline, consulting needs, risks)
6. **Cost Analysis** (3-year TCO for this scenario)

**NOT Included**: Prescriptive "Choose Platform X" recommendations. Instead: "Platforms matching requirements include..." with objective data.

---

## Value Demonstration

**S3 shows HOW to use the catalog**, not WHAT to buy:
- Requirements → Feature needs
- Tech stack → Integration requirements
- Budget → TCO constraints
- Timeline → Implementation complexity
- Catalog data → Platform shortlist (objective matching)

**Client application** (separate from research):
- Specific company context → Customized analysis
- Negotiation support, vendor introductions, implementation oversight
- Billable consulting engagement ($5K-15K)

---

## Deliverables

- `approach.md` (this file)
- `tech-startup-50-employees.md`
- `saas-scaleup-200-employees.md`
- `manufacturing-500-employees.md`
- `enterprise-migration-2000-employees.md`
- `pe-portfolio-consolidation.md`
- `synthesis.md`

---

## Next Steps After S3

**S4 Strategic**: Graduation frameworks (when to move between tiers), vendor viability, build-vs-buy economics
