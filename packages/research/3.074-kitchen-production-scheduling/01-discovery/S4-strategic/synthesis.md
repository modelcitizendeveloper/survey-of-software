# S4 Strategic Discovery: Synthesis

**Research ID**: 3.074 - Production Scheduling (Commercial Kitchen)
**Discovery Phase**: S4 Strategic
**Date**: November 24, 2025

---

## Executive Summary

**Core Finding**: Production scheduling platform decisions must balance three dimensions: **economic viability** (build vs buy), **vendor survival risk**, and **lock-in exposure**. The optimal choice varies dramatically by operation size, technical capacity, and risk tolerance.

**Decision Framework**:
```
Operation Size × Technical Capacity × Risk Tolerance → Platform Choice

Micro (<$500K) + No tech + Risk averse → Spreadsheets or Craftybase ($240/year)
Small ($500K-2M) + No tech + Balanced → Katana ($10K/year) or CaterZen ($2K/year)
Medium ($2M-10M) + No tech + Risk tolerant → FlexiBake ($12K/year)
Medium ($2M-10M) + Has tech + Risk averse → Odoo self-hosted ($3K/year)
Large ($10M+) + Has tech + Balanced → Odoo + custom modules ($50K-80K/year)
Enterprise ($20M+) + Has tech + Risk tolerant → Custom build ($100K-150K/year ongoing)
```

**Key Insight**: The **5-year TCO inflection point** occurs at $2M-5M revenue. Below this, SaaS always wins. Above this, open source or custom builds become competitive—but only with technical capacity.

---

## Integrated Analysis: Build vs Buy × Vendor Viability

### Micro Operations (<$500K revenue)

| Dimension | Analysis | Recommendation |
|-----------|----------|----------------|
| **Economic** | SaaS: $240-1,200/year<br>Custom: $25K+ Year 1<br>**Winner: SaaS** (100× cheaper) | Use cheap SaaS or spreadsheets |
| **Vendor Risk** | Craftybase: 60% survival<br>Airtable: 95% survival | Accept risk (switching cost low) |
| **Lock-In** | Craftybase: Low (CSV export)<br>Airtable: Low (CSV + API) | Export data quarterly |
| **Final Choice** | **Craftybase ($240/year)** or **Airtable ($240/year)** or **Spreadsheets ($0)** | Balance cost vs functionality |

**Rationale**: At micro scale, custom build never pays back. SaaS cost is trivial ($240-1,200/year). Even if vendor shuts down (40% risk over 10 years), switching cost is low ($1K-3K). Export data quarterly and move on if needed.

**Anti-Pattern**: Spending $25K on custom build for $500K operation. Payback never occurs (33+ years).

---

### Small Operations ($500K-2M revenue)

| Dimension | Make-to-Order (Catering) | Make-to-Stock (Bakery) |
|-----------|--------------------------|------------------------|
| **Economic (5-year)** | CaterZen: $6K-18K<br>Custom: $100K+<br>**Winner: SaaS** | Katana: $48K<br>Odoo: $15K (with tech)<br>Custom: $100K+<br>**Winner: SaaS or Odoo** |
| **Vendor Risk** | CaterZen: 70% survival<br>Risk: Moderate | Katana: 80% survival<br>Risk: Low |
| **Lock-In** | CaterZen: Moderate<br>Switching: $6K-12K | Katana: Low (good API)<br>Switching: $3K-6K |
| **Final Choice** | **CaterZen ($1.2K-3.6K/year)**<br>Switching plan: Export to ClickUp if shuts down | **Katana ($10K/year)** OR<br>**Odoo ($3K/year if have tech capacity)** |

**Make-to-Order (Catering)**:
- **Primary: CaterZen** ($1,200-3,600/year) - Purpose-built, affordable, 70% survival acceptable because low switching cost
- **Backup Plan**: ClickUp ($1,800/year) + Excel for recipe scaling (if CaterZen shuts down)
- **Custom Build**: Not viable (break-even 28 years)

**Make-to-Stock (Bakery)**:
- **No Tech Capacity**: Katana ($10K/year) - Modern MRP, 80% survival, low lock-in
- **Has Tech Capacity**: Odoo ($3K/year) - Zero vendor risk, 50% cost savings, requires sysadmin
- **Custom Build**: Not viable (break-even 12 years)

**Key Insight**: At $500K-2M revenue, SaaS dominates unless have technical capacity (then Odoo becomes attractive). Custom builds don't pay back until $5M+ revenue.

---

### Medium Operations ($2M-10M revenue)

| Dimension | No Tech Capacity | Has Tech Capacity |
|-----------|------------------|-------------------|
| **Economic (5-year)** | FlexiBake: $62K<br>Katana: $48K<br>Custom: $102K<br>**Winner: SaaS** | Odoo: $17K<br>FlexiBake: $62K<br>Custom: $102K<br>**Winner: Odoo** (73% savings) |
| **Vendor Risk** | FlexiBake: 95% survival<br>Katana: 80% survival | Odoo: Zero risk (open source) |
| **Lock-In** | FlexiBake: High (switching $50K)<br>Katana: Low (switching $6K) | Odoo: Zero (full database access) |
| **Final Choice** | **FlexiBake ($12K/year)** if need bakery features<br>**Katana ($10K/year)** if general MRP | **Odoo ($3K/year)** - eliminates vendor risk + 73% cost savings |

**No Tech Capacity (Typical Wholesale Bakery)**:
- **Primary: FlexiBake** ($12,420/year) - Industry standard, 95% survival, bakery-specific features (nutritional analysis, HACCP, FDA compliance)
- **Vendor Risk Acceptable**: 95% survival + switching cost ($50K) is 8% of equipment optimization value ($650K)
- **Lock-In Mitigation**: Maintain parallel recipe database (Airtable), export data quarterly, negotiate data portability clause

**Has Tech Capacity (Progressive Bakery with Sysadmin)**:
- **Primary: Odoo Community** ($3,000/year hosting) - Zero vendor risk, 73% cost savings vs FlexiBake, full customization
- **Trade-off**: Must hire sysadmin ($60K-80K/year) OR have existing technical staff
- **Break-Even**: Odoo $63K total (hosting + sysadmin ÷ business units), FlexiBake $62K (pure software). **Break-even at 1 bakery, Odoo wins at 2+ locations** (amortize sysadmin cost).

**Key Insight**: Technical capacity unlocks 73% cost savings + zero vendor risk. At 2+ locations or 100+ employees, hiring sysadmin pays for itself via Odoo savings.

---

### Large Operations ($10M+ revenue, 100+ employees)

| Dimension | Analysis | Recommendation |
|-----------|----------|----------------|
| **Economic (5-year)** | BatchMaster: $300K<br>Odoo: $25K-50K<br>Custom: $405K (break-even Year 7)<br>**Winner: Odoo or SaaS** | Odoo preferred, custom viable at scale |
| **Vendor Risk** | BatchMaster: 98% survival<br>Odoo: Zero risk | Both acceptable |
| **Lock-In** | BatchMaster: High (switching $100K-200K)<br>Odoo: Zero | Odoo advantage |
| **Final Choice** | **Odoo ($5K-10K/year)** with custom modules<br>OR **BatchMaster ($60K+/year)** if need process mfg | Hybrid: Odoo core + custom optimization |

**Primary: Odoo + Custom Modules** ($50K-80K/year total):
- Base: Odoo Community self-hosted ($5K-10K/year infrastructure)
- Custom: Equipment optimization module ($40K-70K/year development + maintenance)
- **Why**: Zero vendor risk, full customization, 70-85% cost savings vs BatchMaster
- **Break-Even vs BatchMaster**: Year 1 (Odoo $80K, BatchMaster $100K+)

**Alternative: BatchMaster** ($60K-100K/year):
- **When**: Process manufacturing complexity (temperature control, quality testing, regulatory reporting)
- **Trade-Off**: 98% survival justifies lock-in risk, but 2-5× more expensive than Odoo

**Custom Build** ($100K-150K/year ongoing):
- **When**: Multi-facility ($50M+ revenue), 500+ employees, need competitive advantage from scheduling algorithms
- **Break-Even**: Year 6-8 vs Odoo, Year 5-7 vs BatchMaster
- **Hybrid Approach**: Odoo for 80% (UI, recipes, orders) + custom for 20% (equipment optimization, process control)

**Key Insight**: At $10M+ revenue, open source (Odoo) + custom modules is optimal. Pure custom build only makes sense at $20M+ revenue (competitive advantage justifies investment).

---

## Risk-Adjusted Platform Selection Matrix

### Risk Averse (Prioritize Vendor Survival + Low Lock-In)

| Revenue | Production Model | Recommendation | Rationale |
|---------|------------------|----------------|-----------|
| <$500K | Any | **Airtable** ($240/year) | 95% survival + low lock-in |
| $500K-2M | Make-to-order | **ClickUp** ($1,800/year) | 90% survival + low lock-in |
| $500K-2M | Make-to-stock | **Odoo** ($3K/year, need tech) | Zero vendor risk |
| $2M-10M | Any | **Odoo** ($3K-5K/year) | Zero vendor risk + cost savings |
| $10M+ | Any | **Odoo + custom** ($50K-80K/year) | Zero vendor risk + full control |

**Pattern**: Risk-averse operations should choose **open source** (if have tech capacity) or **general tools** (Airtable, ClickUp) over specialized platforms. Accept lower functionality for higher survival probability + portability.

---

### Balanced (Accept Moderate Risk for Better Features)

| Revenue | Production Model | Recommendation | Rationale |
|---------|------------------|----------------|-----------|
| <$500K | Any | **Craftybase** ($240-600/year) | 60% survival acceptable, low switching cost |
| $500K-2M | Make-to-order | **CaterZen** ($1.2K-3.6K/year) | 70% survival, moderate lock-in, purpose-built |
| $500K-2M | Make-to-stock | **Katana** ($10K/year) | 80% survival, low lock-in, modern MRP |
| $2M-10M | Bakery | **FlexiBake** ($12K/year) | 95% survival, high lock-in justified by features |
| $2M-10M | General mfg | **Katana** ($10K/year) | 80% survival, low lock-in |
| $10M+ | Process mfg | **BatchMaster** ($60K+/year) | 98% survival, high lock-in justified by stability |

**Pattern**: Balanced operations choose **best-fit platforms** (FlexiBake for bakeries, CaterZen for catering) even if higher lock-in or moderate vendor risk. Prioritize functionality over portability.

---

### Risk Tolerant (Accept High Lock-In for Optimal Fit)

| Revenue | Production Model | Recommendation | Rationale |
|---------|------------------|----------------|-----------|
| $2M-10M | Bakery | **FlexiBake** ($12K/year) | Industry standard, nutritional analysis, HACCP |
| $10M+ | Process mfg | **BatchMaster** ($60K+/year) | Enterprise features, process controls |
| $20M+ | Multi-facility | **Custom build** ($150K+/year) | Competitive advantage from scheduling algorithms |

**Pattern**: Risk-tolerant operations accept **high lock-in** to established platforms (FlexiBake 20+ years, BatchMaster 30+ years) with strong survival probability (95-98%). At $20M+ revenue, custom builds provide competitive advantage.

---

## Strategic Decision Tree

```
START: What's your annual revenue?

├─ <$500K (Micro)
│  └─ Use cheap SaaS (Craftybase $240/year) or spreadsheets ($0)
│     - Custom build never pays back (33+ year break-even)
│     - Accept vendor risk (60% survival), switching cost low ($1K-3K)
│
├─ $500K-2M (Small)
│  ├─ Have technical capacity? (sysadmin/developer)
│  │  ├─ YES → Odoo ($3K/year) - zero vendor risk, 70% savings
│  │  └─ NO → What's your production model?
│  │     ├─ Make-to-order → CaterZen ($2K/year) or ClickUp ($1.8K/year)
│  │     └─ Make-to-stock → Katana ($10K/year) or MRPeasy ($2K/year)
│  └─ Custom build not viable (break-even 12-28 years)
│
├─ $2M-10M (Medium)
│  ├─ Have technical capacity?
│  │  ├─ YES → Odoo ($3K/year) - STRONG WINNER (73% savings + zero risk)
│  │  └─ NO → Are you a bakery?
│  │     ├─ YES → FlexiBake ($12K/year) - bakery-specific features justify lock-in
│  │     └─ NO → Katana ($10K/year) - modern MRP, low lock-in
│  └─ Custom build marginally viable (break-even 7-10 years, but Odoo better)
│
└─ $10M+ (Large/Enterprise)
   ├─ Have technical capacity?
   │  ├─ YES → Odoo + custom modules ($50K-80K/year) - OPTIMAL CHOICE
   │  │   - Base: Odoo Community ($5K-10K/year)
   │  │   - Custom: Equipment optimization ($40K-70K/year)
   │  │   - Zero vendor risk + 70-85% savings vs enterprise SaaS
   │  │
   │  └─ NO → Need process manufacturing features?
   │     ├─ YES → BatchMaster ($60K-100K/year) - enterprise-grade
   │     └─ NO → Katana ($10K/year) or FlexiBake ($12K/year)
   │
   └─ Custom build viable if:
      - >$20M revenue (competitive advantage justifies investment)
      - OR multi-facility complexity (500+ employees)
      - Break-even: Year 6-8 vs Odoo, Year 5-7 vs BatchMaster
```

---

## Lock-In Mitigation Strategies (All Operations)

### Before Contract Signing

1. ✅ **Negotiate data portability clause**
   - Full data export (all tables, all fields) in CSV or JSON
   - Vendor assistance with export (included, not upcharge)
   - 60-90 day data retention post-cancellation
   - No hostage clauses (can export even if payment in arrears)

2. ✅ **Verify API availability**
   - Test API before committing (read + write access)
   - Check rate limits (sufficient for data migration)
   - Review documentation (comprehensive migration guides)

3. ✅ **Evaluate switching cost**
   - Request data schema/field mapping
   - Estimate hours to migrate to alternative platform
   - Budget 10-15% of annual platform cost for switching (contingency)

---

### During Implementation

1. ✅ **Maintain parallel systems** (first 3-6 months)
   - Keep spreadsheets active until confident in platform
   - Export data monthly (verify export process works)

2. ✅ **Create neutral recipe database**
   - Maintain recipes in Airtable or Google Sheets (parallel to platform)
   - Update frequency: Quarterly (not real-time)
   - Insurance: If platform shuts down, recipes are safe

3. ✅ **Document workflows**
   - Screenshot configuration, custom fields, reports
   - Create runbook for staff (how to use platform)
   - If need to rebuild on new platform, documentation accelerates setup (save 20-40 hours)

---

### Quarterly Data Hygiene

1. ✅ **Export full data**
   - Recipes, inventory, orders, production schedules, customer data
   - Store in cloud (Dropbox, Google Drive) separate from platform
   - Test restoration: Import into Excel/Airtable (verify completeness)

2. ✅ **Monitor platform health**
   - Check Crunchbase for acquisition rumors, funding rounds
   - Monitor support quality (response time, resolution rate)
   - Watch for warning signs: Slow support, no feature updates, layoffs
   - If see red flags, accelerate exit planning (identify alternative, test data export)

3. ✅ **Review alternative platforms** (annually)
   - Market evolves: New platforms emerge, existing platforms improve
   - Re-evaluate: Is current platform still best fit?
   - Budget permitting, test alternative platform (parallel run 1-2 months)

---

## Acquisition Scenario Planning

### FlexiBake Acquisition (20-30% probability, 5 years)

**Most Likely Acquirer**: Infor (food & beverage ERP), SAP, or PE firm

**Expected Outcomes**:
- ✅ Product continues (95% probability) - too specialized to kill
- ⚠️ Price increase 30-50% over 3 years (historical pattern)
- ⚠️ Support degradation (offshore support, longer response times)
- ⚠️ Forced migration to acquirer platform (5-7 years post-acquisition)

**Mitigation Strategy**:
- **Contract**: Negotiate 3-5 year price lock before acquisition
- **Parallel System**: Maintain recipe database in Airtable (updated quarterly)
- **Budget**: Plan for migration in Year 5-7 post-acquisition ($50K-80K switching cost)
- **Trigger**: If price increases >50% OR support becomes unacceptable → migrate to Odoo or Katana

**Where to Switch**:
1. **Odoo** (if developed technical capacity) - zero future vendor risk
2. **Katana** (if workflows are make-to-order) - low lock-in, modern platform
3. **BatchMaster** (if need enterprise features) - higher cost but stable

---

### Katana Acquisition (30% probability, 5 years)

**Most Likely Acquirer**: Shopify (manufacturing for e-commerce), legacy MRP (Infor, IFS), or PE firm

**Expected Outcomes**:
- **Best Case** (Shopify, 50% probability): Product continues, better integration, pricing stable
- **Medium Case** (Legacy MRP, 30% probability): Product continues, support degrades, price +20-30%
- **Worst Case** (PE, 20% probability): Price +40-50%, innovation stops, support minimal

**Mitigation Strategy**:
- **Low Risk**: Katana has good API + low lock-in (switching cost $3K-6K)
- **Timeline**: Wait-and-see (6-12 months post-acquisition to assess impact)
- **Trigger**: If PE acquisition + support degrades → migrate to MRPeasy or Odoo

**Where to Switch**:
1. **MRPeasy** ($2K/year) - similar features, 70% cost savings
2. **Odoo** ($3K/year) - de-risk vendor dependence entirely
3. **FlexiBake** ($12K/year) - if need more bakery-specific features

---

### CaterZen Shutdown (30% probability, 10 years)

**Triggers**: Can't compete with ClickUp/Monday.com, founder exits, niche market too small

**Expected Timeline**: 3-6 months notice (SaaS standard practice)

**Mitigation Strategy**:
- **Moderate Risk**: 70% survival probability, but niche market is concern
- **Preparation**: Export data quarterly (CSV), document workflows
- **Backup Plan**: ClickUp ($1,800/year) + Excel for recipe scaling
- **Switching Cost**: $3K-6K (low, due to moderate lock-in)

**Where to Switch**:
1. **ClickUp** ($1,800/year) - general project management, 90% of CaterZen functionality
2. **Total Party Planner** ($780-2,340/year) - alternative catering platform
3. **Custom build** ($25K-50K) - only if operation scaled to $5M+ revenue

---

## Technical Capacity Assessment

### Do You Have Technical Capacity for Open Source?

**Requirements for Odoo/ERPNext**:
1. **Sysadmin** (20-40 hours/month) - Server management, updates, backups, monitoring
2. **Developer** (10-20 hours/month) - Module configuration, custom reports, workflow automation
3. **Total**: 30-60 hours/month = 0.2-0.3 FTE = $3K-5K/month = $36K-60K/year

**When You Have Capacity**:
- ✅ Already employ sysadmin/developer (can add Odoo to their workload)
- ✅ Multi-location operation (amortize technical staff across 2+ facilities)
- ✅ IT budget >$100K/year (technical staff already planned)

**When You DON'T Have Capacity**:
- ❌ No technical staff (would need to hire)
- ❌ Single location, <50 employees (can't justify technical staff)
- ❌ Outsourcing complexity (prefer vendor handles infrastructure)

### Break-Even Analysis: Hiring Tech Staff for Odoo

**Scenario**: 50-employee wholesale bakery ($2.5M revenue)

**Option A: FlexiBake** (No tech staff needed)
- Software: $12,420/year
- Support: Included
- **Total**: $12,420/year

**Option B: Odoo** (Must hire tech staff)
- Software: $3,000/year (hosting)
- Sysadmin: $60,000/year (shared with other systems)
- **Total**: $63,000/year

**Odoo LOSES at single location** (5× more expensive when include sysadmin)

**Scenario**: 2-location bakery ($5M revenue)

**Option A: FlexiBake** (2 instances)
- Software: $12,420 × 2 = $24,840/year

**Option B: Odoo** (1 sysadmin, 2 instances)
- Software: $3,000 × 2 = $6,000/year (hosting)
- Sysadmin: $60,000/year (shared across both locations)
- **Total**: $66,000/year

**Odoo still LOSES** (2.7× more expensive)

**Scenario**: 4-location bakery ($10M revenue)

**Option A: FlexiBake** (4 instances)
- Software: $12,420 × 4 = $49,680/year

**Option B: Odoo** (1 sysadmin, 4 instances)
- Software: $3,000 × 4 = $12,000/year
- Sysadmin: $60,000/year (shared across all locations)
- **Total**: $72,000/year

**Odoo still LOSES** (1.4× more expensive)

**Break-Even Point**: 6-8 locations OR when sysadmin is shared across OTHER systems (not just Odoo)

**Key Insight**: **Odoo only wins if you ALREADY HAVE technical staff** (for other IT systems) and can add Odoo to their workload. Hiring sysadmin JUST FOR Odoo rarely makes economic sense.

**When Odoo Makes Sense**:
- ✅ Already have IT department (sysadmin managing email, network, ERP) → add Odoo to workload
- ✅ 6+ locations (amortize sysadmin across many instances)
- ✅ Need heavy customization (SaaS platforms too rigid)
- ✅ Risk-averse about vendor lock-in (willing to pay premium for control)

---

## 5-Year Strategic Scenarios (2025-2030)

### Scenario 1: SaaS Consolidation (60% probability)

**What Happens**:
- Toast, Square, Lightspeed acquire more restaurant/food tech platforms
- Small platforms (BakeSmart, CaterZen) acquired or shut down
- Surviving platforms (FlexiBake, Katana, BatchMaster) raise prices 20-40%

**Winners**: Platforms with strong moat (FlexiBake bakery-specific, BatchMaster enterprise) + open source (Odoo)

**Losers**: Small platforms (BakeSmart, Craftybase), general PM tools (ClickUp loses to integrated solutions)

**Implication**:
- **If using small platform** (BakeSmart, CaterZen) → plan for migration to Katana or Odoo by 2028-2030
- **If using FlexiBake/Katana** → expect 20-40% price increase post-acquisition → budget increases
- **If using Odoo** → unaffected (open source immune to consolidation)

---

### Scenario 2: Open Source Gains Share (25% probability)

**What Happens**:
- Odoo manufacturing module improves significantly (better UX, more features)
- Mid-market operations (50-200 employees) migrate from SaaS to Odoo (cost savings 60-80%)
- Managed Odoo hosting becomes mainstream (Odoo.sh, third-party hosts)

**Winners**: Odoo, operations with technical capacity, managed hosting providers

**Losers**: Mid-market SaaS (FlexiBake, Katana) lose share to Odoo

**Implication**:
- **If $2M-10M revenue** → re-evaluate Odoo annually (as it improves, becomes more attractive)
- **If using FlexiBake** → monitor customer base (if many migrate to Odoo, platform at risk)
- **If using Katana** → less risk (modern platform, but Odoo price advantage is significant)

---

### Scenario 3: AI-Assisted Scheduling Emerges (15% probability)

**What Happens**:
- Production scheduling platforms add AI optimization (equipment utilization, staff allocation)
- Early adopters (Katana, Odoo with AI modules) gain competitive advantage
- Legacy platforms (FlexiBake, BatchMaster) slow to adopt (technical debt)

**Winners**: Modern platforms (Katana), open source with AI modules (Odoo + custom ML), custom builds with optimization algorithms

**Losers**: Legacy platforms (FlexiBake, BatchMaster) lose ground if don't modernize

**Implication**:
- **If using FlexiBake** → monitor AI feature releases (if slow, consider Katana or custom optimization layer)
- **If using Katana** → early adopter advantage (modern tech stack enables AI features)
- **If using Odoo** → integrate open source AI/ML libraries (scikit-learn, OR-Tools) for custom optimization

---

## Final Strategic Recommendations

### For Micro Operations (<$500K)

**Recommendation**: **Spreadsheets** ($0) or **Craftybase** ($240/year)

**Rationale**: Any other investment doesn't pay back. Custom build break-even 33+ years. Accept vendor risk (60% survival) because switching cost is low ($1K-3K).

**Lock-In Mitigation**: Export data quarterly (CSV backup).

---

### For Small Operations ($500K-2M)

**No Technical Capacity**:
- **Make-to-order**: CaterZen ($1.2K-3.6K/year) or ClickUp ($1.8K/year)
- **Make-to-stock**: Katana ($10K/year) or MRPeasy ($2K/year)

**Has Technical Capacity**:
- **Odoo Community** ($3K/year) - 70% cost savings + zero vendor risk

**Rationale**: SaaS dominates at this scale. Custom build doesn't pay back (12-28 years). Odoo is ONLY attractive if already have technical staff.

**Lock-In Mitigation**: Choose platforms with low lock-in (Katana, CaterZen) + good API. Export data quarterly.

---

### For Medium Operations ($2M-10M)

**No Technical Capacity**:
- **Bakery**: FlexiBake ($12K/year) - bakery-specific features justify premium + lock-in
- **General Manufacturing**: Katana ($10K/year) - modern MRP, low lock-in

**Has Technical Capacity**:
- **Odoo Community** ($3K/year) - STRONG WINNER (73% savings + zero vendor risk)

**Rationale**: This is the inflection point. Odoo becomes VERY attractive if have technical capacity (73% savings + zero vendor risk). FlexiBake justified for bakeries due to nutritional analysis, HACCP, FDA compliance (competitors don't have these features).

**Lock-In Mitigation**:
- **FlexiBake**: Maintain parallel recipe database (Airtable), negotiate data portability clause, export data quarterly
- **Odoo**: No mitigation needed (full database access, zero lock-in)

---

### For Large Operations ($10M+)

**Has Technical Capacity** (Recommended):
- **Odoo + Custom Modules** ($50K-80K/year) - Zero vendor risk + 70-85% savings + competitive advantage

**No Technical Capacity**:
- **Process Manufacturing**: BatchMaster ($60K-100K/year) - enterprise features, 98% survival
- **General Manufacturing**: Katana ($10K/year) or FlexiBake ($12K/year)

**Rationale**: At this scale, technical capacity is critical. Odoo + custom optimization modules provide competitive advantage (better equipment utilization, inventory management, staff allocation). Pure custom build break-even 6-8 years vs Odoo, so hybrid (Odoo 80% + custom 20%) is optimal.

**Lock-In Mitigation**: Odoo eliminates vendor risk. BatchMaster requires quarterly data exports + contract negotiation.

---

### For Enterprise ($20M+, Multi-Facility)

**Recommendation**: **Custom Build** ($150K+/year ongoing) OR **Odoo + Heavy Customization** ($100K-150K/year)

**Rationale**: At this scale, custom scheduling algorithms provide competitive advantage (5-10% efficiency gains = $1M-2M value). Pure custom build break-even 5-7 years. Hybrid approach (Odoo core + custom optimization) faster time-to-value.

**Lock-In Mitigation**: Custom build = zero vendor lock-in, but high switching cost to maintain code.

---

## Conclusion

**Core Insight**: The optimal production scheduling solution is NOT a single platform, but a **risk-adjusted choice** based on operation size, technical capacity, and risk tolerance.

**Decision Framework**:
1. **<$2M revenue**: SaaS always wins (Craftybase, CaterZen, Katana) unless have existing technical capacity (then Odoo)
2. **$2M-10M revenue**: Odoo becomes VERY attractive (73% savings) IF have technical capacity. Otherwise FlexiBake (bakeries) or Katana (general mfg)
3. **$10M+ revenue**: Odoo + custom modules is optimal (zero vendor risk + competitive advantage)
4. **$20M+ revenue**: Custom build or heavy Odoo customization (competitive advantage justifies investment)

**Lock-In Mitigation is Critical**:
- Export data quarterly (all operations)
- Maintain parallel recipe database (FlexiBake users)
- Negotiate data portability clause (before signing contract)
- Monitor platform health (quarterly review)

**Open Source = Strategic Advantage**:
- Zero vendor risk (survives even if company shuts down)
- 50-80% cost savings over SaaS (5-year TCO)
- Full customization (competitive advantage)
- **BUT**: Requires technical capacity (sysadmin + developer)

**Next Steps**: Create overall 3.074 synthesis document integrating S1-S4 findings into actionable recommendations.
