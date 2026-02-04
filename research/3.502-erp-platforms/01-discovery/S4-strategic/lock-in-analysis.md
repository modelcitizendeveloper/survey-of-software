# S4 Strategic: Lock-In Analysis (STUB)

**Date**: November 2, 2025
**Purpose**: Analyze vendor lock-in risks and switching costs for ERP platforms
**Status**: 🚧 Framework Only - Full analysis TBD

---

## Framework for Lock-In Assessment

### Lock-In Dimensions

1. **Data Lock-In** (can you export your data?)
2. **Technical Lock-In** (proprietary technology, APIs, customizations)
3. **Process Lock-In** (workflows embedded in platform)
4. **Integration Lock-In** (ecosystem dependencies)
5. **People Lock-In** (training, expertise, resistance to change)
6. **Financial Lock-In** (switching costs, contract penalties)

---

## Quick Lock-In Summary

| Platform | Data Export | Technical Lock-In | Switching Cost | Lock-In Risk |
|----------|-------------|-------------------|----------------|--------------|
| **NetSuite** | ⭐⭐⭐ Good (CSV, API) | ⭐⭐ High (SuiteScript) | $200K-$500K | ⭐⭐⭐⭐ High |
| **Dynamics 365 BC** | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐ Medium (AL, Power Platform) | $100K-$300K | ⭐⭐⭐ Medium |
| **SAP Business One** | ⭐⭐⭐ Good (SQL access) | ⭐⭐ High (SDK, on-prem) | $150K-$400K | ⭐⭐⭐⭐ High |
| **Odoo** | ⭐⭐⭐⭐⭐ Excellent (open source) | ⭐ Low (open source) | $50K-$150K | ⭐ Very Low |
| **Acumatica** | ⭐⭐⭐⭐ Very Good | ⭐⭐⭐ Medium (C#) | $100K-$250K | ⭐⭐⭐ Medium |
| **Oracle ERP Cloud** | ⭐⭐⭐ Good (API) | ⭐⭐⭐⭐ Very High (Oracle ecosystem) | $500K-$2M+ | ⭐⭐⭐⭐⭐ Very High |

**Winner (Lowest Lock-In)**: **Odoo** (open source = zero vendor lock-in)

---

## Lock-In Risk Assessment by Platform

### NetSuite: ⭐⭐⭐⭐ High Lock-In

**Data Export**: ⭐⭐⭐ Good
- CSV export available for most records
- SuiteTalk API (REST/SOAP) for programmatic export
- No database-level access (SaaS multi-tenant)

**Technical Lock-In**: ⭐⭐ High
- SuiteScript (JavaScript variant, NetSuite-specific)
- SuiteFlow workflows (no export, must recreate)
- Custom records and fields (NetSuite-specific schema)

**Switching Cost**: $200K-$500K
- Reimplementation on new platform: $150K-$400K
- Data migration: $30K-$75K
- Training: $20K-$50K
- Lost productivity: 2-4 months

**Mitigation**:
- Minimize SuiteScript customizations
- Document all custom logic for migration
- Use standard integrations (not custom SuiteTalk)

---

### Dynamics 365 BC: ⭐⭐⭐ Medium Lock-In

**Data Export**: ⭐⭐⭐⭐ Very Good
- SQL Server database (can export entire DB)
- OData API (standard, portable)
- Excel export for all tables

**Technical Lock-In**: ⭐⭐⭐ Medium
- AL language (C#-like, Microsoft-specific)
- Power Platform customizations (Power Apps, Power Automate)
- But: Standard REST APIs reduce lock-in

**Switching Cost**: $100K-$300K
- Reimplementation: $75K-$250K
- Data migration: $15K-$35K
- Training: $10K-$20K

**Mitigation**:
- Use Power Platform (portable to other systems)
- Standard OData APIs (not AL-specific code)
- Keep customizations minimal

---

### SAP Business One: ⭐⭐⭐⭐ High Lock-In

**Data Export**: ⭐⭐⭐ Good
- SQL Server database access (on-premise)
- DI API and Service Layer (can export data)
- Cloud version: Less direct access

**Technical Lock-In**: ⭐⭐ High
- .NET SDK (proprietary)
- Add-ons tightly coupled to SAP B1
- On-premise infrastructure investment

**Switching Cost**: $150K-$400K
- Reimplementation: $100K-$350K
- Data migration: $30K-$60K
- Training: $20K-$40K

**Mitigation**:
- Use Service Layer REST API (more portable)
- Avoid deep SDK customizations
- Document all add-ons and custom logic

---

### Odoo: ⭐ Very Low Lock-In

**Data Export**: ⭐⭐⭐⭐⭐ Excellent
- **PostgreSQL database** (standard, exportable)
- **Full source code access** (open source)
- Can fork entire codebase if needed

**Technical Lock-In**: ⭐ Low
- Python modules (portable language)
- Standard PostgreSQL (any database tool works)
- Open source = no vendor dependency

**Switching Cost**: $50K-$150K
- Reimplementation: $30K-$100K
- Data migration: $10K-$30K (PostgreSQL export easy)
- Training: $10K-$20K

**Mitigation**: Not needed (already lowest lock-in)

**Note**: Odoo is the **only platform with zero vendor lock-in risk** (open source)

---

### Acumatica: ⭐⭐⭐ Medium Lock-In

**Data Export**: ⭐⭐⭐⭐ Very Good
- SQL Server database access
- REST and OData APIs
- Full data export capabilities

**Technical Lock-In**: ⭐⭐⭐ Medium
- C# customizations (portable language)
- Acumatica Framework (proprietary but well-documented)
- Less lock-in than NetSuite/SAP

**Switching Cost**: $100K-$250K
- Reimplementation: $75K-$200K
- Data migration: $15K-$35K
- Training: $10K-$20K

**Mitigation**:
- Use Generic Inquiries (less custom code)
- Standard REST APIs
- Document customizations

---

### Oracle ERP Cloud: ⭐⭐⭐⭐⭐ Very High Lock-In

**Data Export**: ⭐⭐⭐ Good (but limited)
- REST APIs available
- No direct database access (Oracle-managed)
- Large-scale export is complex

**Technical Lock-In**: ⭐⭐⭐⭐ Very High
- Oracle ecosystem (OCI, Oracle DB, Oracle Integration Cloud)
- VBCS customizations (Oracle-specific)
- Deep integration with Oracle stack

**Switching Cost**: $500K-$2M+
- Reimplementation: $400K-$1.5M+
- Data migration: $75K-$300K+
- Training: $50K-$200K+
- Lost productivity: 6-12 months

**Mitigation**: Hard to mitigate (Oracle lock-in is inherent)
- Use standard REST APIs where possible
- Avoid deep customizations
- Document everything

---

## Switching Cost Breakdown

### Cost Categories

1. **New ERP Software** (1 year): $50K-$1M depending on platform
2. **Reimplementation**: $100K-$1.5M (partner services)
3. **Data Migration**: $30K-$300K (extract, transform, load)
4. **Integration Rebuild**: $20K-$200K (Shopify, CRM, etc.)
5. **Customization Rebuild**: $50K-$500K (re-create custom workflows)
6. **Training**: $20K-$200K (retrain entire team)
7. **Productivity Loss**: 2-6 months at 40-60% efficiency
8. **Opportunity Cost**: Projects delayed during migration

**Total Switching Cost**: $300K-$3M+ depending on platform and complexity

---

## Lock-In Mitigation Best Practices

### Practice #1: Clean Data Export Strategy
- **Action**: Export full database quarterly (CSV or JSON)
- **Benefit**: Always have portable data backup
- **Effort**: 2-4 hours per quarter

### Practice #2: Minimize Customization
- **Action**: Use out-of-box features whenever possible
- **Benefit**: Reduces switching cost by 30-50%
- **Trade-off**: May need process changes to fit platform

### Practice #3: Standard APIs Only
- **Action**: Use REST APIs, avoid proprietary integrations
- **Benefit**: Integrations work with any ERP
- **Effort**: May cost 10-20% more upfront

### Practice #4: Document Everything
- **Action**: Maintain documentation of all customizations, workflows, integrations
- **Benefit**: Reduces switching cost (know what to rebuild)
- **Effort**: 5-10 hours per month

### Practice #5: Choose Low Lock-In Platform
- **Action**: Prefer Odoo (open source) or Dynamics BC (standard APIs) over NetSuite/Oracle
- **Benefit**: 50-70% lower switching cost
- **Trade-off**: May sacrifice some features

---

## Contract Lock-In

### Contract Terms Comparison

| Platform | Typical Contract | Early Termination | Auto-Renewal | Notes |
|----------|------------------|-------------------|--------------|-------|
| **NetSuite** | 1-3 years | Fee (1-2 months) | Yes (30-60 day notice) | Hard to cancel mid-contract |
| **Dynamics 365 BC** | Monthly or annual | None (monthly) | Monthly converts | Easiest to cancel |
| **SAP Business One** | 1-3 years (cloud) | Fee varies | Yes | On-prem: Perpetual (no cancel) |
| **Odoo** | Monthly or annual | None | No auto-renew | Flexible |
| **Acumatica** | Annual typical | Varies by partner | Partner-dependent | Check partner terms |
| **Oracle ERP Cloud** | 3-5 years | High penalty | Yes | Difficult to exit |

**Lowest Contract Lock-In**: Dynamics 365 BC (monthly option), Odoo (monthly option)

---

## When Lock-In Doesn't Matter

### Scenarios Where You Can Accept High Lock-In

1. **Platform is market leader** (NetSuite for SaaS companies)
   - Low risk of platform obsolescence
   - Deep ecosystem and support

2. **You're building for 10+ years** (no plan to switch)
   - Long-term commitment justifies customization
   - Switching cost amortized over decade

3. **Platform advantages outweigh lock-in** (Dynamics Copilot AI)
   - Strategic capability only available on this platform
   - Competitive advantage worth the risk

4. **Vendor viability is unquestionable** (Microsoft, Oracle)
   - Zero risk of vendor going out of business
   - Safe long-term bet

---

## Full Analysis TBD

**To Complete This Section**:
1. Detailed switching cost models (by company size and complexity)
2. Real-world case studies (companies that switched ERPs)
3. Data portability testing (actual export/import scenarios)
4. Contract analysis (standard terms, negotiation strategies)
5. ROI models (when to switch despite lock-in)

**Estimated Effort**: 1-2 days research per platform = 6-12 days total

---

**Next**: See `build-vs-buy-analysis.md` for when to use open source vs commercial ERP
