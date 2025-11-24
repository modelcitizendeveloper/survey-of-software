# S3 Need-Driven Discovery: Synthesis

**Research ID**: 3.074 - Production Scheduling (Commercial Kitchen)
**Discovery Phase**: S3 Synthesis
**Date**: November 24, 2025

---

## Use Case Comparison Summary

| Dimension | Wholesale Bakery | Catering Company |
|-----------|-----------------|------------------|
| **Revenue** | $2.5M | $1.2M |
| **Employees** | 50 | 15 |
| **Production Model** | 70% make-to-stock, 30% make-to-order | 100% make-to-order |
| **Production Volume** | 15K-20K units/week (continuous) | 150-200 events/year (discrete projects) |
| **Planning Horizon** | Weekly recurring | Per-event (2-8 weeks advance) |
| **Key Challenge** | Equipment optimization, recipe consistency | Multi-day sequencing, last-minute changes |
| **Current Time Waste** | 8-10 hours/week | 10-15 hours/week |
| **Opportunity Cost** | $650K-795K/year | $41K-50K/year |
| **Best Platform** | FlexiBake Professional ($12.4K/year) | CaterZen ($1.2K-3.6K/year) |
| **ROI** | 3,333-4,508% | 658-2,569% |
| **Payback Period** | 7-10 days | 14-48 days |

---

## Pattern Recognition: Platform Selection by Production Model

### Make-to-Stock (Continuous Production)
**Examples**: Wholesale bakery (bread production), meal prep service (weekly batches)

**Requirements**:
- Recipe standardization (consistency across shifts)
- Equipment capacity optimization (maximize throughput)
- Inventory integration (ingredient availability)
- Lot tracking and traceability (regulatory compliance)
- Production forecasting (demand-driven scheduling)

**Best Platforms**:
1. **FlexiBake** - Bakery-specific (nutritional analysis, FDA compliance)
2. **Katana MRP** - General food manufacturing (modern UI, unlimited users)
3. **MRPeasy** - Budget-friendly MRP (simple implementation)

**Cost Range**: $1,788-12,420/year (depends on features needed)

---

### Make-to-Order (Event/Project-Driven)
**Examples**: Catering company (custom events), custom cake bakery

**Requirements**:
- Event-driven workflows (each event is discrete project)
- Multi-day production sequencing (prep over 3-5 days)
- Recipe scaling (adjust for guest count/order size)
- Last-minute change handling (menu changes, headcount updates)
- Client communication (menu approval, order status)

**Best Platforms**:
1. **CaterZen** - Catering-specific (event management + production)
2. **ClickUp / Monday.com** - General project management (flexible, affordable)
3. **Spreadsheets** - DIY (high time cost but zero software cost)

**Cost Range**: $0-3,588/year (much cheaper than manufacturing MRP)

**Key Insight**: Event-driven businesses don't need manufacturing MRP (Katana, FlexiBake). They need **project management + recipe scaling**. CaterZen or ClickUp are better fits.

---

### Hybrid (Make-to-Stock + Make-to-Order)
**Examples**: Retail bakery with wholesale accounts (stock items + custom cakes)

**Requirements**:
- Both workflows (recurring production + custom orders)
- Production priority management (rush custom orders interrupt stock production)
- Multi-location (retail storefront + production facility)

**Best Platforms**:
1. **FlexiBake** - Handles both workflows (make-to-stock + make-to-order)
2. **BakeSmart** - Retail bakery focus (POS integration + production)
3. **Katana** - Flexible MRP (can model both workflows)

**Cost Range**: $1,188-12,420/year

**Key Insight**: Hybrid operations need full MRP (FlexiBake, Katana) that can handle both production models. Project management tools (ClickUp) too simplistic.

---

## Equipment Capacity Optimization: The $650K Question

### Wholesale Bakery Equipment Analysis
- **Current utilization**: Ovens 100% utilized 6am-2pm, 30% utilized 2pm-6pm
- **Opportunity**: Increase afternoon utilization to 60-70%
- **Additional capacity**: 30-40% more production without buying new ovens
- **Revenue opportunity**: $625K-750K/year (at current margins)

### Why Equipment Optimization Matters
- **Capital cost**: Commercial oven = $15K-50K
- **If can optimize existing equipment** → avoid $120K-400K investment (8 ovens)
- **Software cost**: $12K/year (FlexiBake) vs $120K-400K capital expenditure
- **ROI of software**: 10-33× better than buying new equipment

**Key Finding**: Production scheduling software is **NOT about saving time** (though that's nice). It's about **maximizing equipment ROI** and **avoiding capital expenditure**.

### Platforms with Equipment Capacity Modeling
✅ **Advanced**:
- BatchMaster (enterprise-grade, complex capacity planning)

⚠️ **Basic**:
- FlexiBake (can schedule equipment, but no deep optimization)
- Katana (visual dashboard, basic resource management)
- MRPeasy (basic capacity planning, backward scheduling)

❌ **None**:
- BakeSmart, Craftybase, CaterZen, ClickUp

**Gap**: No mid-market platform ($100-500/mo) has advanced equipment capacity optimization. Either pay enterprise prices (BatchMaster $50K+/year) or use basic tools (FlexiBake, Katana) and manually optimize.

**Workaround**: Use FlexiBake/Katana for scheduling + custom spreadsheet for equipment optimization analysis.

---

## Recipe Management: Consistency vs Flexibility

### Wholesale Bakery (Consistency Critical)
- **Problem**: 3 shifts using different recipes for same product
- **Impact**: Quality variance, customer complaints, returns
- **Solution**: Centralized recipe database with version control
- **Best Platforms**: FlexiBake (recipe versioning, nutritional analysis), Katana, MRPeasy

### Catering Company (Flexibility Critical)
- **Problem**: Every event has custom menu, need to scale recipes quickly
- **Impact**: Time waste (manually calculate ingredient quantities)
- **Solution**: Recipe scaling automation
- **Best Platforms**: CaterZen (recipe scaling built-in), Katana (BOM scaling)

**Key Insight**: Bakeries need **recipe standardization**. Caterers need **recipe flexibility**. Different requirements = different platforms.

---

## Integration Ecosystem Analysis

### Accounting Integration (Critical for COGS)
- **Best**: MRPeasy (QuickBooks certified), Katana (strong QB/Xero), CaterZen (QB integration)
- **Good**: FlexiBake (accounting sync), Craftybase
- **Limited**: BakeSmart (basic export)

**Why it matters**: Product profitability analysis requires accurate COGS. Without accounting integration, COGS data is manual (error-prone, time-consuming).

### POS Integration (Critical for Retail Bakeries)
- **Best**: BakeSmart (native POS connectors)
- **Gap**: FlexiBake, Katana, MRPeasy don't integrate with POS (Toast, Square, Lightspeed)
- **Workaround**: Middleware (Zapier) or manual data entry

**Why it matters**: Retail bakeries with storefronts need POS sales data to flow into production planning (demand forecasting). Current platforms don't integrate well.

### Inventory Systems (3.070 platforms)
- **Gap**: Production scheduling platforms include their own inventory modules
- **No integration** with standalone inventory platforms (MarketMan, xtraCHEF)
- **Implication**: Must buy bundled MRP (production + inventory) or maintain dual systems

**Why it matters**: If bakery already uses MarketMan for inventory, adding Katana for production = dual inventory systems (data sync issues, duplicate entry).

---

## Total Cost of Ownership Reality Check

### Hidden Costs in Per-User Pricing

**FlexiBake**:
- Advertised: $295-375/mo
- Reality (5 users): $295 + ($165 × 4) = **$955/mo = $11,460/year**
- **Per-user fees add 70-80% to base cost**

**Katana**:
- Advertised: $799/mo (Professional)
- Reality (unlimited users): **$799/mo = $9,588/year**
- **No per-user fees = huge cost savings for growing teams**

**MRPeasy**:
- Advertised: $49-149/mo
- Reality (tier-based, user limits unclear): Estimated **$1,788/year**
- **Most affordable, but less feature-rich**

**Key Insight**: FlexiBake's per-user pricing makes it **6× more expensive** than MRPeasy for same 5-user team ($11,460 vs $1,788).

**When FlexiBake is worth it**: Bakery-specific features (nutritional analysis, FDA compliance, HACCP) justify 6× cost premium. General food manufacturers should choose Katana or MRPeasy.

---

## Platform Selection Decision Tree

```
START: What's your production model?

├─ MAKE-TO-STOCK (continuous production)
│  │
│  ├─ Are you a BAKERY?
│  │  ├─ YES → Need FDA compliance / nutritional labels?
│  │  │  ├─ YES → FlexiBake ($12K/year)
│  │  │  └─ NO → Katana ($10K/year) or MRPeasy ($2K/year)
│  │  │
│  │  └─ NO (general food mfg) → Katana ($10K/year) or MRPeasy ($2K/year)
│  │
│  └─ Budget constraint?
│     ├─ <$5K/year → MRPeasy ($2K/year)
│     ├─ $5K-15K/year → Katana ($10K/year) or FlexiBake ($12K/year)
│     └─ >$15K/year → BatchMaster Enterprise (custom pricing)
│
├─ MAKE-TO-ORDER (event-driven)
│  │
│  ├─ Are you a CATERING company?
│  │  ├─ YES → CaterZen ($1.2K-3.6K/year)
│  │  └─ NO → ClickUp ($1.8K/year) or Monday.com ($2.4K/year)
│  │
│  └─ Budget constraint?
│     ├─ <$2K/year → ClickUp ($1.8K/year) or Spreadsheets ($0)
│     └─ $2K-5K/year → CaterZen ($1.2K-3.6K/year)
│
└─ HYBRID (make-to-stock + make-to-order)
   │
   ├─ Bakery with retail + wholesale?
   │  ├─ Small (5-20 employees) → BakeSmart ($1.2K/year)
   │  └─ Medium+ (20+ employees) → FlexiBake ($12K/year)
   │
   └─ General food manufacturer
      └─ Katana ($10K/year) - handles both workflows
```

---

## ROI Thresholds: When Does Software Pay for Itself?

### Wholesale Bakery (FlexiBake $12K/year)
**Pays for itself if**:
- Capture 2% of equipment optimization opportunity ($650K × 2% = $13K)
- OR reduce ingredient waste by $12K/year
- OR save production manager 3 hours/week ($156 hours/year × $36/hr = $5.6K) + reduce waste $6K

**Payback**: 7-10 days (equipment optimization)

---

### Catering Company (CaterZen $1.2K-3.6K/year)
**Pays for itself if**:
- Save head chef 1 hour/week ($52 hours/year × $36/hr = $1.9K)
- OR reduce ingredient rush orders by $1.2K/year
- OR handle menu changes 50% faster (save $1K/year)

**Payback**: 14-48 days (time savings + waste reduction)

---

### General Threshold
**Production scheduling software ROI-positive when**:
- Operation has $500K+ annual revenue
- OR 10+ employees
- OR 50+ SKUs
- OR multi-location complexity

**Below threshold**: Spreadsheets may be adequate (time cost < software cost)

**Above threshold**: Opportunity cost (equipment optimization, waste reduction, time savings) far exceeds software cost

---

## Common Mistakes in Platform Selection

### Mistake 1: Buying Manufacturing MRP for Event-Driven Business
**Example**: Catering company buys Katana ($10K/year) because "it's the best MRP"
**Problem**: Event-driven business doesn't need MRP. Needs project management + recipe scaling.
**Cost**: Wasting $8K/year (Katana $10K vs CaterZen $2K)

### Mistake 2: Choosing Software Based on UI, Not Fit
**Example**: Bakery chooses Katana (modern UI) over FlexiBake (dated UI)
**Problem**: Loses nutritional analysis, HACCP compliance, bakery-specific workflows
**Cost**: Must buy separate nutrition software ($2K-5K/year), manual HACCP tracking

### Mistake 3: Ignoring Per-User Pricing
**Example**: Chooses FlexiBake ($375/mo advertised) without realizing per-user fees ($165/user)
**Reality**: 5 users = $955/mo ($11.5K/year) not $375/mo ($4.5K/year)
**Surprise**: 2.5× higher cost than expected

### Mistake 4: Under-Estimating Opportunity Cost
**Example**: Stays with spreadsheets to "save money" (avoid $1K/year software cost)
**Reality**: Wasting $20K-50K/year in time + waste + equipment under-utilization
**Cost**: Saving $1K, losing $20K-50K

---

## Next Steps (S4 Strategic)

### S4 Focus Areas

1. **Build vs Buy Analysis**
   - When does custom build make sense?
   - Spreadsheet optimization vs software purchase
   - TCO analysis (5-year horizon)

2. **Vendor Viability**
   - Will FlexiBake, Katana, CaterZen be around in 5 years?
   - Market consolidation risks
   - Data portability and exit strategies

3. **Lock-In Risks**
   - How hard is it to switch platforms?
   - Data export capabilities
   - Integration dependencies

4. **Open Source Alternatives**
   - Odoo Manufacturing module (free, self-hosted)
   - ERPNext (free, self-hosted)
   - Custom builds with OR-Tools (1.096 Scheduling Libraries)
   - When does open source make sense? (defer detailed analysis to 1.096)

---

## S3 Conclusion

**Key Findings**:

1. **Production model determines platform** - Make-to-stock needs MRP (Katana, FlexiBake), make-to-order needs project management (CaterZen, ClickUp)

2. **Equipment optimization is primary ROI driver** - Not time savings. $650K revenue opportunity from better oven utilization dwarfs $12K software cost.

3. **Bakery-specific platforms justify premium** - FlexiBake 6× more expensive than MRPeasy, but nutritional analysis + HACCP compliance worth it for bakeries.

4. **Per-user pricing is hidden cost multiplier** - FlexiBake $375/mo becomes $955/mo with 5 users. Katana unlimited users = major advantage.

5. **Event-driven businesses vastly overpay for MRP** - Catering companies don't need Katana ($10K/year). CaterZen ($2K/year) or ClickUp ($1.8K/year) better fit.

**Recommendations by segment**:
- **Wholesale bakery** → FlexiBake ($12K/year) - industry standard
- **Catering company** → CaterZen ($2K/year) - event-driven workflows
- **General food mfg** → Katana ($10K/year) or MRPeasy ($2K/year) - modern MRP
- **Budget-constrained** → MRPeasy ($2K/year) or ClickUp ($1.8K/year)
- **Enterprise** → BatchMaster ($50K+/year) - process manufacturing

**Proceed to S4** for strategic analysis (build vs buy, vendor viability, lock-in risks).
