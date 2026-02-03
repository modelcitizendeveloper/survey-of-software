# Deployment Models: Open Source CRM Platforms

**Last Updated**: 2025-10-21

---

## The Lock-in Spectrum (Not a Binary)

Open source CRM platforms offer **three deployment models** on a lock-in spectrum:

```
Zero Lock-in          Low Lock-in           High Lock-in
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pure Self-Hosted      Managed Open Source   Proprietary SaaS
(1.130 self)          (1.130 managed)       (3.501)

YOU run:              THEY run:             THEY run:
- Infrastructure      - Infrastructure      - Infrastructure
- Platform            YOU control:          - Platform
- Data                - Platform choice     - Your data access
                      - Data
                      - Migration path

Examples:             Examples:             Examples:
- Twenty on VPS       - Odoo.sh             - Salesforce
- Odoo Docker         - EspoCRM Cloud       - HubSpot
- SuiteCRM LAMP       - Twenty CloudStation - Pipedrive
- EspoCRM shared host - SuiteCRM On-Demand  - Zoho Bigin
```

---

## Why Managed Open Source ≠ Proprietary SaaS

### Managed Open Source (1.130 managed deployment)

**Pricing**: $15-100/user/month (typically 3-5 user minimum)

**Lock-in Level**: **Low**

**Why**:
1. ✅ Can migrate to self-hosted **SAME platform** (Odoo.sh → self-hosted Odoo)
2. ✅ Can switch to different managed provider (open source portability)
3. ✅ Full data export with no restrictions
4. ✅ Can fork codebase if vendor shuts down
5. ✅ Platform choice preserved (not locked to vendor's platform)

**Migration Cost**: $500-5,000 (mainly infrastructure setup time)

**Examples**:
- **Odoo.sh**: $24-100/user/month (official Odoo managed hosting)
- **EspoCRM Cloud**: $15-69/user/month (official EspoCRM managed)
- **Twenty CloudStation**: $18/month flat (third-party managed)
- **SuiteCRM On-Demand**: $30-100/user/month (official managed)

---

### Proprietary SaaS (3.501)

**Pricing**: $10-300+/user/month

**Lock-in Level**: **Medium to Very High**

**Why**:
1. ❌ Cannot self-host (no option exists)
2. ❌ Must change platforms entirely to leave
3. ❌ Vendor controls platform roadmap and pricing
4. ❌ Cannot fork or modify codebase
5. ❌ Stuck with vendor's infrastructure

**Migration Cost**: $5,000-500,000 (platform change + data migration + automation rebuild)

**Examples**:
- **Salesforce**: Very high lock-in (Apex code, AppExchange, custom objects)
- **HubSpot**: High lock-in (marketing assets, contact-based pricing)
- **Pipedrive**: Medium lock-in (visual pipeline customization)
- **Zoho Bigin**: Low lock-in (simple data model, easy export)

---

## The Key Strategic Difference

### Question: "Odoo.sh vs Salesforce - what's the difference?"

**Odoo.sh** (1.130 managed):
- Open source Odoo, managed by Odoo SA
- **If pricing becomes prohibitive**: Migrate to self-hosted Odoo ($500-2K/year)
- **If vendor shuts down**: Switch to different Odoo host OR self-host
- **If need customization**: Fork Odoo, run self-hosted
- **Platform optionality preserved**

**Salesforce** (3.501):
- Proprietary platform, can ONLY use Salesforce infrastructure
- **If pricing becomes prohibitive**: Must change platforms entirely ($50K-500K migration)
- **If vendor shuts down**: No recourse (cannot self-host Salesforce)
- **If need customization**: Limited to what Salesforce allows
- **Platform lock-in by design**

---

## Deployment Model Decision Tree

```
START: Choosing open source CRM deployment
  │
  ├─ Do you have DevOps capability?
  │   │
  │   ├─ YES, intermediate+ skills
  │   │   └─ → Pure Self-Hosted (Zero lock-in, $500-2K/year)
  │   │       Platforms: All four (Twenty, Odoo, SuiteCRM, EspoCRM)
  │   │       Best for: 10+ users, cost control priority
  │   │
  │   └─ NO OR limited
  │       └─ Do you value open source optionality?
  │           │
  │           ├─ YES → Managed Open Source (Low lock-in, $15-100/user/mo)
  │           │   Examples: Odoo.sh, EspoCRM Cloud, Twenty CloudStation
  │           │   Best for: 5-20 users, want convenience + optionality
  │           │   Can migrate to self-hosted later if gain DevOps capability
  │           │
  │           └─ NO → Consider Proprietary SaaS (see 3.501)
  │               Examples: HubSpot, Salesforce, Pipedrive
  │               Best for: Need ecosystem NOW, tolerate lock-in
```

---

## Migration Paths (The Open Source Advantage)

### Managed Open Source → Self-Hosted (Easy!)

**Complexity**: Low-to-Medium (SAME platform)

**Process**:
1. Backup database from managed service
2. Deploy self-hosted instance (Docker/VPS)
3. Restore database to self-hosted
4. Point DNS to self-hosted
5. Cancel managed service

**Time**: 4-20 hours (mostly infrastructure setup)

**Cost**: $500-2,000 (one-time DevOps time)

**Example**: Odoo.sh ($50/user/mo × 10 users = $6,000/year) → Self-hosted Odoo (~$2,000/year)
**Annual savings**: $4,000/year ongoing

---

### Self-Hosted → Managed Open Source (Easy!)

**Complexity**: Low (SAME platform)

**Process**:
1. Backup self-hosted database
2. Sign up for managed service
3. Restore database to managed
4. Point DNS to managed
5. Shut down self-hosted

**Time**: 2-8 hours

**Cost**: $0-500 (minimal)

**Common Trigger**: Team turnover (lose DevOps capability), want to focus on business

---

### Proprietary SaaS → Open Source (Hard)

**Complexity**: Medium-to-High (PLATFORM change)

**Process**:
1. Export data from proprietary (CSV/API)
2. Deploy open source CRM
3. Import data (mapping required)
4. Rebuild automations (different platform)
5. Retrain team

**Time**: 20-80 hours

**Cost**: $2,500-10,000+

**Common Trigger**: Salesforce pricing becomes prohibitive ($300/user × 100 = $360K/year)

---

## TCO Comparison (10 users, 3 years)

| Deployment Model | Year 1 | Year 2-3 | 3-Year Total | Lock-in Level |
|------------------|--------|----------|--------------|---------------|
| **Pure Self-Hosted** (EspoCRM) | $2-8K | $1.5-6K/yr | $5-20K | None |
| **Managed Open Source** (Odoo.sh) | $3-12K | $3-12K/yr | $9-36K | Low |
| **Proprietary SaaS** (Pipedrive) | $3.5-7K | $3.5-7K/yr | $10.5-21K | Medium |
| **Proprietary SaaS** (Salesforce) | $10-36K | $10-36K/yr | $30-108K | Very High |

**Key Insight**: Managed open source sits between self-hosted and proprietary on BOTH cost AND lock-in.

---

## Why This Matters for Client Recommendations

### Client Question: "Should we use Odoo.sh or self-host Odoo?"

**Answer**: Same platform, different deployment (both 1.130)
- Odoo.sh: Pay for convenience ($50/user/mo), can self-host later
- Self-hosted: Pay for DevOps time ($2K/year ops), more savings

**NOT a lock-in decision** - can switch between these easily.

---

### Client Question: "Should we use Odoo.sh or Salesforce?"

**Answer**: Different tier, different lock-in (1.130 vs 3.501)
- Odoo.sh: Can self-host later (low lock-in), open source optionality
- Salesforce: Cannot self-host ever (very high lock-in), vendor controls destiny

**This IS a lock-in decision** - hard to switch between these.

---

## Research Organization

### 1.130: Open Source CRM Platforms
- Documents **all deployment models** (self-hosted, managed, hybrid)
- Focus: Platforms that CAN be self-hosted
- Key attribute: **Optionality preserved**

### 3.501: Proprietary CRM SaaS
- Documents **only managed** (no self-host option)
- Focus: Platforms that CANNOT be self-hosted
- Key attribute: **Vendor-controlled, lock-in by design**

### 4.090: CRM Architecture Decision
- Guides choice between patterns including:
  - Pattern 3: Self-hosted open source (1.130 self-hosted)
  - Pattern 4a: Managed open source (1.130 managed) - low lock-in
  - Pattern 4b: Proprietary SaaS (3.501) - high lock-in

---

## The "Tier 1 Will Eat Tier 3 for Lunch" Thesis

**Strategic Positioning**:

Open source CRM platforms (1.130) offer **strategic optionality**:
1. Start managed if needed (low DevOps burden)
2. Migrate to self-hosted as capability grows (cost savings)
3. Switch back to managed if circumstances change (team turnover)

Proprietary SaaS (3.501) offers **convenience tax with no exit**:
1. Start managed (only option)
2. Get locked in (no self-host alternative)
3. Cannot switch without platform change ($50K-500K migration)

**Long-term bet**: As open source platforms mature, managed open source will offer "good enough" convenience with strategic optionality, making proprietary SaaS less compelling.

---

**Conclusion**: Managed open source is STILL Tier 1 because the platform is open source and self-hostable. The deployment model is a choice, not a requirement, and that choice preserves optionality.
