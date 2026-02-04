# S4 Strategic: Build vs Buy Analysis

**Research ID**: 3.074 - Production Scheduling (Commercial Kitchen)
**Discovery Phase**: S4 Strategic
**Date**: November 24, 2025

---

## Decision Framework

### Option 1: Buy SaaS Platform
**Cost**: $1,200-12,420/year (depending on platform)
**Implementation**: 1-8 weeks
**Risk**: Vendor lock-in, feature limitations

### Option 2: Optimize Spreadsheets
**Cost**: $0 software, but high opportunity cost
**Implementation**: 1-2 weeks to standardize templates
**Risk**: Doesn't scale, manual errors, time waste

### Option 3: Build Custom Solution
**Cost**: $30K-100K+ (development + ongoing maintenance)
**Implementation**: 3-6 months
**Risk**: Development delays, maintenance burden, vendor dependency on dev shop

### Option 4: Open Source Self-Hosted
**Cost**: $600-2,400/year (hosting + setup time)
**Implementation**: 2-4 weeks (if technical capacity exists)
**Risk**: Technical expertise required, limited support

---

## Build vs Buy Economics

### Break-Even Analysis by Operation Size

#### Scenario 1: 5-Employee Catering Company ($500K revenue)

**SaaS Option** (CaterZen $1,200/year):
- Year 1: $1,200
- Year 2-5: $1,200/year × 4 = $4,800
- **5-Year Total**: $6,000

**Custom Build Option**:
- Development: 100 hours × $150/hr = $15,000
- Hosting: $50/mo × 12 = $600/year
- Maintenance: 10 hours/year × $150/hr = $1,500/year
- Year 1: $15,000 + $600 + $1,500 = $17,100
- Year 2-5: ($600 + $1,500) × 4 = $8,400
- **5-Year Total**: $25,500

**Break-Even**: Never (SaaS always cheaper for small operations)

**Decision**: ✅ **BUY SaaS** (CaterZen $1,200/year)

---

#### Scenario 2: 50-Employee Wholesale Bakery ($2.5M revenue)

**SaaS Option** (FlexiBake $12,420/year):
- Year 1: $12,420
- Year 2-5: $12,420/year × 4 = $49,680
- **5-Year Total**: $62,100

**Custom Build Option**:
- Development: 400 hours × $150/hr = $60,000
- Hosting: $200/mo × 12 = $2,400/year
- Maintenance: 40 hours/year × $150/hr = $6,000/year
- Year 1: $60,000 + $2,400 + $6,000 = $68,400
- Year 2-5: ($2,400 + $6,000) × 4 = $33,600
- **5-Year Total**: $102,000

**Break-Even**: Year 7 (SaaS cumulative cost exceeds custom build)

**Decision**: ⚠️ **BUY SaaS** for first 3-5 years, reconsider custom build if:
- FlexiBake doesn't meet needs after 3 years (feature gaps)
- OR operation scales to 100+ employees (custom ROI improves)
- OR have in-house dev team (reduce build cost)

---

#### Scenario 3: 200-Employee Multi-Facility Bakery ($15M revenue)

**SaaS Option** (BatchMaster ~$50K/year estimated):
- Year 1: $100,000 (implementation + licenses)
- Year 2-5: $50,000/year × 4 = $200,000
- **5-Year Total**: $300,000

**Custom Build Option**:
- Development: 1,500 hours × $150/hr = $225,000
- Hosting: $500/mo × 12 = $6,000/year
- Maintenance: 200 hours/year × $150/hr = $30,000/year
- Year 1: $225,000 + $6,000 + $30,000 = $261,000
- Year 2-5: ($6,000 + $30,000) × 4 = $144,000
- **5-Year Total**: $405,000

**Break-Even**: Year 7 (but closer than Scenario 2)

**Decision**: ⚠️ **BUY SaaS** initially, but **custom build becomes viable** at this scale if:
- Unique requirements (BatchMaster doesn't fit workflows)
- OR have in-house dev team (reduce build cost to $100K-150K)
- OR 10-year horizon (custom cheaper long-term)

**Hybrid Option**: Buy SaaS (BatchMaster) + custom integrations ($50K) = $350K total over 5 years (middle ground)

---

## Spreadsheet Optimization vs SaaS Purchase

### When Spreadsheets Are "Good Enough"

**Acceptable for**:
- <5 employees
- <20 SKUs
- Single location
- Simple production (no multi-day sequencing, no equipment constraints)
- <$500K annual revenue

**Example**: Home bakery (1-2 people) making 10 products for farmers market
- Production planning: 1-2 hours/week
- Opportunity cost: Minimal (can't capture equipment optimization gains at this scale)
- SaaS cost: $1,200-3,000/year (not justified)

**Decision**: ✅ **Keep Spreadsheets** (optimize templates, standardize format)

---

### When Spreadsheets Become Liability

**Spreadsheets break down when**:
- >10 employees
- >50 SKUs
- Multi-location
- Equipment bottlenecks (idle capacity represents lost revenue)
- >$1M annual revenue

**Example**: Wholesale bakery from S3 (50 employees, $2.5M revenue)
- Production planning: 8-10 hours/week (production manager)
- Opportunity cost: $650K+/year (equipment under-utilization + waste)
- SaaS cost: $12,420/year (FlexiBake)
- **ROI**: 52× ($650K ÷ $12K)

**Decision**: ❌ **Abandon Spreadsheets** - Opportunity cost 52× higher than software cost

---

## Total Cost of Ownership (10-Year Horizon)

### SaaS Platforms

| Platform | Year 1 | Years 2-10 (annual) | 10-Year Total | Notes |
|----------|--------|---------------------|---------------|-------|
| **Craftybase** | $228 | $228/year | **$2,280** | Micro makers |
| **MRPeasy** | $1,788 | $1,788/year | **$17,880** | Small mfg |
| **CaterZen** | $2,400 | $2,400/year | **$24,000** | Catering |
| **Katana** | $9,588 | $9,588/year | **$95,880** | Food mfg |
| **FlexiBake** | $12,420 | $12,420/year | **$124,200** | Wholesale bakery |
| **BatchMaster** | $100,000 | $50,000/year | **$550,000** | Enterprise (estimated) |

**Key Insight**: SaaS cost scales linearly with time. No reduction after Year 1 (except potential price increases).

---

### Custom Build

| Component | Year 1 | Years 2-10 (annual) | 10-Year Total | Notes |
|-----------|--------|---------------------|---------------|-------|
| **Development** | $30,000-100,000 | $0 | $30,000-100,000 | One-time |
| **Hosting** | $600-6,000 | $600-6,000/year | $6,000-60,000 | Scales with usage |
| **Maintenance** | $1,500-30,000 | $1,500-30,000/year | $15,000-300,000 | Bug fixes, updates |
| **Feature additions** | $5,000-20,000 | $5,000-20,000/year | $50,000-200,000 | New features |
| **Total** | **$37K-156K** | **$7K-56K/year** | **$101K-660K** | Depends on complexity |

**Key Insight**: Custom build has high upfront cost, then lower ongoing cost. Becomes cheaper than SaaS after break-even point (5-10 years depending on scale).

---

### Break-Even Comparison

| Operation Size | SaaS Platform | SaaS 10-Year Cost | Custom Build 10-Year Cost | Break-Even Year | Winner |
|----------------|---------------|-------------------|---------------------------|-----------------|--------|
| **Micro** (1-5 employees) | Craftybase $228/yr | $2,280 | $101K | Never | ✅ SaaS |
| **Small** (5-20 employees) | MRPeasy $1,788/yr | $17,880 | $120K | Never | ✅ SaaS |
| **Medium** (20-100 employees) | Katana $9,588/yr | $95,880 | $200K | Year 8 | ⚠️ SaaS (barely) |
| **Large** (100-500 employees) | FlexiBake $12,420/yr | $124,200 | $300K | Year 10 | ⚠️ Tie |
| **Enterprise** (500+ employees) | BatchMaster $50K/yr | $550,000 | $400K | Year 6 | ✅ Custom |

**Pattern**:
- Micro/Small operations: **SaaS always wins** (custom never pays back)
- Medium operations: **SaaS wins short-term** (3-7 years), custom wins long-term (8+ years)
- Enterprise: **Custom wins long-term** (6+ years)

---

## Open Source Self-Hosted Analysis

### Option 1: Odoo Manufacturing (Community Edition - Free)

**What it is**:
- Open source ERP (free Community Edition or paid Enterprise)
- Manufacturing/MRP module included
- Recipe management (BOM), production scheduling, inventory
- Self-hosted or cloud hosting

**Cost**:
- Software: **Free** (Community Edition)
- Hosting: $50-200/mo ($600-2,400/year) on DigitalOcean, AWS, Linode
- Setup: 40-80 hours × $100/hr consultant = $4,000-8,000 (one-time)
- Maintenance: 20 hours/year × $100/hr = $2,000/year
- **Year 1 Total**: $6,600-12,400
- **Year 2+ Annual**: $2,600-4,400/year
- **5-Year Total**: $17,000-29,600

**Comparison to SaaS** (FlexiBake $62,100 over 5 years):
- **Savings**: $32,500-45,100 over 5 years (52-73% cheaper)

**Trade-offs**:
- ✅ Save $32K-45K over 5 years
- ✅ Data ownership (self-hosted)
- ✅ Unlimited customization
- ❌ Requires technical expertise (devops, system admin)
- ❌ No support (community forums only)
- ❌ Steeper learning curve vs SaaS
- ❌ Setup time (4-8 weeks vs 2-4 weeks SaaS)

**When Odoo Makes Sense**:
- Have in-house technical team (sysadmin, developer)
- OR partnered with Odoo implementation consultant
- Want data ownership (not SaaS vendor dependency)
- Long-term horizon (5+ years)
- Willing to trade convenience for cost savings

**When Odoo Doesn't Make Sense**:
- No technical capacity (can't manage servers, troubleshoot)
- Need fast implementation (Odoo takes 4-8 weeks vs 1-2 weeks SaaS)
- Want vendor support (Odoo Community = DIY)

---

### Option 2: ERPNext (Free Open Source)

**Similar to Odoo** but smaller community, less mature.

**Cost**: Similar to Odoo ($6K-12K Year 1, $2.6K-4.4K/year ongoing)

**When to Choose ERPNext over Odoo**:
- Prefer Python/Frappe framework (vs Odoo's Python/PostgreSQL)
- ERPNext has feature Odoo doesn't (rare)

**Generally**: Odoo has larger community, more mature, better choice for food production.

---

## Build Custom with OR-Tools (1.096 Scheduling Libraries)

### When Algorithmic Approach Makes Sense

**Scenario**: Multi-facility bakery with complex equipment capacity optimization problem

**Problem**:
- 3 facilities, 24 ovens total
- 200 SKUs with different bake times, temperatures
- Want to maximize oven utilization (currently 60%, opportunity to reach 85%+)
- SaaS platforms (FlexiBake, Katana) have basic scheduling, no deep optimization

**Solution**: Custom constraint solver using OR-Tools (Google's optimization library)

**Approach**:
1. Use SaaS for basic production management (FlexiBake for recipes, orders, inventory)
2. Build custom optimization engine for equipment scheduling
3. Export production schedule from custom engine → import to FlexiBake

**Cost**:
- Development: 200-400 hours × $150/hr = $30,000-60,000 (one-time)
- Hosting: $100/mo = $1,200/year
- Maintenance: 40 hours/year × $150/hr = $6,000/year
- **Year 1**: $37,200-67,200
- **Year 2+ Annual**: $7,200/year
- **5-Year Total**: $66,000-96,000

**Value**:
- Equipment optimization: Increase oven utilization 60% → 85% = 42% more capacity
- Revenue opportunity: $2.5M × 42% = **$1.05M additional revenue**
- Margin: $1.05M × 30% = **$315K additional profit/year**

**ROI**:
- Cost: $67K (Year 1)
- Value: $315K/year
- **ROI**: 370% (Year 1), ongoing $315K/year benefit

**Decision**: ✅ **Build custom optimization engine** - Massive ROI ($315K/year value vs $67K cost)

**Key Insight**: Don't build *entire* production management system. Build **optimization module** only, integrate with SaaS for everything else.

---

### Hybrid: SaaS + Custom Optimization

**Best of Both Worlds**:
- **SaaS** (FlexiBake, Katana): Recipe management, inventory, orders, user interface
- **Custom** (OR-Tools): Equipment capacity optimization, production scheduling algorithm

**Total Cost**:
- SaaS: $10K-12K/year
- Custom optimization: $67K Year 1, $7K/year ongoing
- **Year 1**: $77K-79K
- **Year 2+ Annual**: $17K-19K/year

**When This Makes Sense**:
- Medium-large operations ($5M+ revenue)
- Equipment capacity is bottleneck (significant idle time or over-utilization)
- SaaS platforms don't solve optimization problem deeply enough
- Have technical capacity to build/maintain custom module

**Examples**:
- Multi-facility bakery (oven scheduling across 24 ovens)
- Commissary kitchen (shared equipment scheduling across 10 clients)
- Meal prep service (batch cooking schedule optimization)

---

## Vendor Lock-In Analysis

### FlexiBake Lock-In Risk: ⚠️ MEDIUM

**Switching Barriers**:
- Recipe database (200 recipes + nutritional analysis)
- Customer accounts (75 wholesale accounts)
- Historical production data (3+ years)
- Staff training (learning curve 4-8 weeks)

**Data Export**:
- ⚠️ Limited export capability (must contact support for full data export)
- Recipes exportable to CSV
- Production history not easily exportable

**Switching Cost**:
- Data migration: 40-80 hours × $100/hr = $4,000-8,000
- New platform setup: 2-4 weeks
- Staff retraining: 20 hours × 20 employees = 400 hours = $14,400 (opportunity cost)
- **Total**: $18,400-22,400

**Mitigation**:
- Annual data export (back up recipes, customer data)
- Document production workflows (independent of FlexiBake)
- Negotiate data export clause in contract

---

### Katana Lock-In Risk: ⚠️ MEDIUM-LOW

**Switching Barriers**:
- Modern platform with good API (easier to export data)
- Integration ecosystem (Shopify, accounting) = vendor dependencies

**Data Export**:
- ✅ REST API (can programmatically extract all data)
- ✅ CSV exports for most data

**Switching Cost**: $10,000-15,000 (lower than FlexiBake due to better API)

**Mitigation**: Leverageopen API for regular backups

---

### CaterZen Lock-In Risk: ⚠️ MEDIUM

**Switching Barriers**:
- Event history (150-200 events/year)
- Client contact database
- Recipe database

**Data Export**:
- ⚠️ Limited (catering platforms typically have basic export)
- Event history exportable to CSV
- Recipes may need manual re-entry

**Switching Cost**: $5,000-10,000

**Mitigation**: Maintain separate client CRM (not just in CaterZen)

---

### Open Source (Odoo) Lock-In Risk: ✅ LOW

**Switching Barriers**:
- Self-hosted = full data ownership
- Can export entire database (PostgreSQL dump)

**Data Export**:
- ✅ Full database access (PostgreSQL)
- ✅ Can migrate to any platform

**Switching Cost**: $3,000-5,000 (just data transformation, no vendor barriers)

**Advantage**: Lowest lock-in risk (own your data)

---

## Recommendation Framework

### By Operation Size

| Revenue | Employees | Recommendation | Rationale |
|---------|-----------|----------------|-----------|
| <$500K | 1-5 | ✅ Spreadsheets or Craftybase ($19/mo) | ROI not justified for full MRP |
| $500K-1M | 5-15 | ✅ SaaS (CaterZen $1.2K-3.6K or MRPeasy $1.8K) | Simple, affordable, fast implementation |
| $1M-5M | 15-50 | ✅ SaaS (FlexiBake $12K, Katana $10K, MRPeasy $2K) | Proven platforms, low risk |
| $5M-20M | 50-200 | ⚠️ SaaS or Open Source (Odoo $17K-30K 5-year) | Consider open source if have technical capacity |
| $20M+ | 200+ | ⚠️ SaaS (BatchMaster) or Custom Build | Custom build starts making economic sense |

---

### By Technical Capacity

| Technical Capacity | Recommendation |
|--------------------|----------------|
| **None** (no IT staff) | ✅ Buy SaaS (FlexiBake, Katana, CaterZen) |
| **Basic** (use cloud tools, can hire consultant) | ⚠️ Open Source (Odoo Community + consultant setup) |
| **Advanced** (in-house dev team, devops) | ✅ Custom Build or Open Source (Odoo with custom modules) |

---

### By Time Horizon

| Planning Horizon | Recommendation |
|------------------|----------------|
| **1-3 years** | ✅ Buy SaaS (fastest ROI, lowest risk) |
| **3-7 years** | ⚠️ SaaS or Open Source (depends on technical capacity) |
| **7-10+ years** | ✅ Custom Build or Open Source (long-term TCO advantage) |

---

## Strategic Decision Matrix

```
DECISION MATRIX:

IF revenue <$1M AND technical_capacity = None:
   → Buy SaaS (CaterZen, MRPeasy, BakeSmart)

ELSE IF revenue $1M-5M AND technical_capacity = None:
   → Buy SaaS (FlexiBake, Katana)

ELSE IF revenue $1M-5M AND technical_capacity = Basic:
   → Consider Open Source (Odoo) - save 50-70% over 5 years

ELSE IF revenue $5M-20M AND technical_capacity = Advanced:
   → Hybrid (SaaS + Custom Optimization Module)

ELSE IF revenue >$20M AND technical_capacity = Advanced AND horizon >7 years:
   → Custom Build (break-even 6-8 years, then cheaper long-term)

ELSE:
   → Buy SaaS (default - lowest risk, proven solutions)
```

---

## Conclusion

**Build vs Buy**:
- **Micro/Small** (<$1M revenue): ✅ **Buy SaaS** - custom never pays back
- **Medium** ($1M-5M revenue): ✅ **Buy SaaS** - unless have technical capacity, then consider open source
- **Large** ($5M-20M revenue): ⚠️ **Hybrid** - SaaS + custom optimization modules
- **Enterprise** (>$20M revenue): ⚠️ **Custom Build** - break-even 6-8 years

**Open Source Opportunity**:
- Odoo Community can save **50-70% over 5 years** vs SaaS ($17K-30K vs $62K-95K)
- Requires technical capacity (sysadmin, developer) or partnership with consultant
- Best for medium operations ($1M-5M revenue) with 5+ year horizon

**Hybrid Approach Wins at Scale**:
- Use SaaS for 80% of features (recipes, orders, inventory, UI)
- Build custom optimization for 20% of high-value problems (equipment scheduling)
- Example: FlexiBake ($12K/year) + custom OR-Tools optimization ($67K Year 1, $7K/year ongoing) = $315K/year value

**Spreadsheets Are False Economy**:
- Opportunity cost ($20K-650K/year in wasted time + equipment under-utilization)
- Far exceeds SaaS cost ($1K-12K/year)
- Only acceptable for micro operations (<$500K revenue, <5 employees)

**Next**: S4 Vendor Viability (will FlexiBake, Katana, CaterZen survive 5-10 years?)
