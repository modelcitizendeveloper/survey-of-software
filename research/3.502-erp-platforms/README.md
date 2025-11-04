# 3.502: ERP Platforms Research

**Status**: 🔄 In Progress
**Started**: November 2, 2025
**Research Method**: MPSE v3.0 (Multi-Phase Synthesis Engine)

---

## Overview

Enterprise Resource Planning (ERP) platforms are comprehensive, integrated business management systems that unify core business processes into a single system of record. Unlike standalone accounting software (3.006), ERPs provide end-to-end coverage across:

- **Financial Management**: General ledger, A/R, A/P, financial reporting
- **Supply Chain**: Procurement, inventory, order management
- **Manufacturing**: Production planning, MRP, shop floor control
- **Human Resources**: Payroll, benefits, time tracking, talent management
- **Customer Relationship Management**: Sales pipeline, customer service
- **Project Management**: Project accounting, resource allocation, time tracking
- **Business Intelligence**: Reporting, dashboards, analytics

---

## Key Research Questions

1. **When to Graduate from Accounting to ERP?**
   - Revenue triggers ($5M? $10M? $50M?)
   - Operational complexity indicators (multi-entity, manufacturing, etc.)
   - Integration pain threshold with point solutions

2. **Open Source vs Commercial ERP**
   - Odoo/ERPNext vs NetSuite/Dynamics - TCO comparison
   - When does self-hosted make sense? (data sovereignty, customization)
   - Community support vs vendor support trade-offs

3. **Cloud vs On-Premise**
   - Modern cloud-first ERPs (NetSuite, Dynamics 365) vs legacy migration (SAP)
   - Data residency, compliance, latency requirements
   - CapEx vs OpEx considerations

4. **Modular vs All-in-One**
   - Can best-of-breed (Xero + Inventory + CRM) delay ERP?
   - When does integration complexity justify unified system?
   - Lock-in vs flexibility trade-offs

5. **Industry Specialization**
   - Vertical ERPs (manufacturing, distribution, services) vs horizontal
   - How much customization is typical/required?
   - Industry-specific modules and compliance

---

## Research Structure

```
3.502-erp-platforms/
├── metadata.yaml                          # Research metadata
├── README.md                              # This file
├── DOMAIN_EXPLAINER.md                    # ERP fundamentals and decision framework
├── SECTION_0_STANDARDS.md                 # ERP standards and integration protocols
│
└── 01-discovery/
    ├── S1-rapid/                          # Quick platform overview (2-4 hours)
    │   ├── approach.md
    │   ├── provider-netsuite.md
    │   ├── provider-sap-business-one.md
    │   ├── provider-dynamics365.md
    │   ├── provider-odoo.md
    │   ├── provider-oracle-erp.md
    │   ├── provider-acumatica.md
    │   └── recommendation.md
    │
    ├── S2-comprehensive/                  # Deep comparison (1-2 days)
    │   ├── feature-matrix.md
    │   ├── pricing-matrix.md
    │   ├── compliance-matrix.md
    │   ├── integration-ecosystem.md
    │   └── ai-capabilities-coverage.md
    │
    ├── S3-need-driven/                    # Use case matching (1 day)
    │   ├── use-case-matching.md
    │   ├── migration-guide.md
    │   └── graduation-triggers.md
    │
    └── S4-strategic/                      # Long-term analysis (1 day)
        ├── vendor-viability.md
        ├── lock-in-analysis.md
        └── build-vs-buy-analysis.md
```

---

## Platform Scope

### Mid-Market ERPs ($10M-$500M revenue)
- **NetSuite** (Oracle) - Cloud-native, strong financials
- **Microsoft Dynamics 365** - Azure integration, modular
- **SAP Business One** - Manufacturing-focused
- **Odoo Enterprise** - Open-source core, modular, customizable
- **Acumatica** - Cloud ERP, consumption pricing
- **Epicor** - Industry-specific verticals

### Enterprise ERPs ($500M+ revenue)
- **SAP S/4HANA** - Enterprise standard, complex
- **Oracle ERP Cloud** - Full suite, cloud migration
- **Workday** - Financial management, HCM-focused
- **Infor CloudSuite** - Industry cloud suites

### Open Source ERPs (Self-hosted)
- **Odoo Community** - Modular, Python/PostgreSQL
- **ERPNext** - Modern UX, Frappe framework
- **Dolibarr** - SMB-focused, European
- **Tryton** - Three-tier architecture

---

## Integration Points

**Relationships to other research:**
- **3.006 Accounting Software**: ERP includes accounting as core module (graduation path)
- **1.139 Self-hosted Business Apps**: Open source ERP options (Odoo, ERPNext)
- **3.070 Inventory Management**: Often bundled in ERP
- **3.501 CRM Platforms**: ERP typically includes CRM module
- **3.503 HRIS/HCM**: HR/payroll often part of ERP suite
- **3.044 Data Warehouse**: ERPs generate data for warehouse/analytics

**Cross-cutting platforms:**
- Odoo appears in both 1.139 (open source) and 3.502 (managed SaaS)
- NetSuite appears in both 3.006 (accounting module) and 3.502 (full ERP)

---

## Success Criteria

**S1 Complete When:**
- [ ] 6-8 major ERP platforms profiled
- [ ] Quick recommendation for common scenarios
- [ ] Platform positioning understood (SMB vs Enterprise)

**S2 Complete When:**
- [ ] Feature matrix across 20+ ERP capabilities
- [ ] Pricing models documented (user-based, consumption, etc.)
- [ ] Compliance and industry certifications mapped

**S3 Complete When:**
- [ ] Use case decision trees created
- [ ] Migration paths documented (accounting → ERP)
- [ ] Graduation triggers clearly defined

**S4 Complete When:**
- [ ] Vendor health and viability assessed
- [ ] Lock-in risks analyzed (data export, API openness)
- [ ] Build vs Buy framework created (when to use open source ERP)

---

## Next Steps

1. ✅ Create directory structure
2. 🔄 S1 Rapid discovery - profile major platforms
3. ⏳ S2 Comprehensive comparison
4. ⏳ S3 Need-driven use cases
5. ⏳ S4 Strategic analysis
6. ⏳ Write DOMAIN_EXPLAINER.md

---

**Related Research:**
- [3.006 Accounting Software](/research/3.006-accounting-software/)
- [3.501 CRM Platforms](/research/3.501-crm-platforms/)
- [1.139 Self-hosted Business Apps](/experiments/1.139-self-hosted-business-apps/)
