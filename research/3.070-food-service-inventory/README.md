# 3.070: Food Service Inventory Management

**Status**: S1 Complete (Nov 30, 2025) | S2-S4 Planned
**Category**: Tier 3 - Managed Services (SaaS + Open Source ERP)
**Domain**: Restaurant, bar, hotel F&B inventory management and waste reduction

---

## Quick Start

**Need a platform recommendation right now?** → Read [`01-discovery/S1-rapid/00-SYNTHESIS-quick-recommendations.md`](01-discovery/S1-rapid/00-SYNTHESIS-quick-recommendations.md)

**5-minute decision shortcuts**:
- **Bar/nightclub** → WISK ($249/mo, hardware scales, 99.7% accuracy)
- **Toast POS user** → xtraCHEF ($149/mo, seamless integration)
- **Multi-location (3-10 outlets)** → ERPNext+URY (free software) or MarketMan ($300-400/mo)
- **Budget <$150/month** → BlueCart (supplier network, predictive AI)
- **Budget <$100/month** → Odoo Community (open-source ERP + $50/mo hosting)

---

## Research Overview

### Problem Statement

Commercial kitchens (restaurants, bars, hotels, catering) waste 4-10% of food costs annually ($20K-$100K for medium restaurant). Systematic inventory management reduces waste 2-6 percentage points, delivering 400-1150% ROI.

**Key Pain Points**:
- Manual inventory counts take 4-6 hours/month (error-prone spreadsheets)
- Food waste from spoilage, over-ordering, lack of visibility
- Bar shrink from overpouring, theft, spillage (5-15% typical loss)
- Invoice processing delays (manual data entry, price discrepancies)
- Recipe costing inaccuracies (theoretical vs. actual usage variance)
- Multi-location inconsistency (different processes per location)

### Platforms Evaluated (S1)

**7 Solutions** (5 SaaS + 2 Open Source):

1. **MarketMan** - Comprehensive SaaS ($200-400/mo), AI forecasting, multi-location
2. **xtraCHEF by Toast** - Invoice automation SaaS ($149/mo), Toast POS integration
3. **BlueCart** - Supplier marketplace SaaS ($0.01-150/mo), predictive ordering AI
4. **Craftable** - Bar/hotel specialization SaaS ($150-300/mo est), fast counts (30-45 min)
5. **WISK** - Premium bar SaaS ($249/mo), hardware scales, 99.7% accuracy
6. **Odoo** - Open-source ERP (Community free, Enterprise $35-150/user), restaurant modules
7. **ERPNext + URY** - Open-source ERP with restaurant extension (free, proven 10+ outlets)

### Key Findings (S1)

**ROI Potential**:
- Food waste reduction: $11,700-$18,000/year (3-4% savings on $450K food cost)
- Bar shrink reduction: $4,500-$12,500/year (5-point shrink reduction on $250K beverage cost)
- Invoice automation: $1,500/year time savings (50 invoices/month × 5 min saved)
- Procurement savings (BlueCart): $22,500/year (5% supplier cost reduction)

**Platform Positioning**:
- **Lowest cost**: BlueCart ($150/mo SaaS) or Odoo Community (~$50/mo hosting)
- **Best Toast integration**: xtraCHEF (owned by Toast, real-time COGS sync)
- **Bar specialization**: WISK (hardware scales), Craftable Bevager
- **Multi-location scale**: ERPNext+URY (free software, 10+ outlets proven) or MarketMan (centralized HQ)
- **Fastest implementation**: BlueCart, xtraCHEF (days), Open-source (weeks with consultant)

---

## Research Structure

### S1: Rapid Search (COMPLETE - Nov 30, 2025)

**Time**: 4 hours
**Deliverables**: 8 documents (7 platform profiles + synthesis)

**Platform Profiles**:
- [01-marketman.md](01-discovery/S1-rapid/01-marketman.md) - Market leader, AI forecasting
- [02-xtrachef-toast.md](01-discovery/S1-rapid/02-xtrachef-toast.md) - Toast POS integration
- [03-bluecart.md](01-discovery/S1-rapid/03-bluecart.md) - Supplier marketplace
- [04-craftable.md](01-discovery/S1-rapid/04-craftable.md) - Bar/hotel specialization
- [05-wisk.md](01-discovery/S1-rapid/05-wisk.md) - Premium bar inventory
- [06-odoo.md](01-discovery/S1-rapid/06-odoo.md) - Open-source ERP (40K+ apps)
- [07-erpnext-ury.md](01-discovery/S1-rapid/07-erpnext-ury.md) - Open-source + restaurant extension

**Quick Recommendations**:
- [00-SYNTHESIS-quick-recommendations.md](01-discovery/S1-rapid/00-SYNTHESIS-quick-recommendations.md) - Decision tree, ROI analysis, scenario matching

**Value**: 70-80% of decision-making information. Most restaurants can select platform based on S1 alone.

### S2: Comprehensive Analysis (PLANNED)

**Time Estimate**: 6-8 hours
**Goal**: Deep feature comparison, TCO modeling, waste reduction benchmarks

**Planned Deliverables**:
- `feature-matrix.md` - 100+ features × 7 platforms comparison
- `pricing-tco.md` - 6 scenarios (cafe, restaurant, bar, multi-location, hotel, budget) × 7 platforms × 3 years
- `waste-reduction-benchmarks.md` - Industry studies, vendor claims validation, ROI sensitivity analysis
- `integration-complexity.md` - POS integration depth, accounting sync, supplier EDI, time to first inventory
- `synthesis.md` - Comprehensive platform comparison

**Value**: Detailed analysis for multi-location operations (>$5M revenue) or complex requirements.

### S3: Need-Driven Scenarios (PLANNED)

**Time Estimate**: 8-10 hours
**Goal**: 8 restaurant archetypes with platform matching

**Planned Scenarios**:
- `small-cafe.md` - <$300K revenue, 10-20 menu items, simple inventory
- `food-truck-catering.md` - Mobile operations, offline mode, fast setup
- `single-restaurant.md` - $500K-$1.5M revenue, 30-50 menu items
- `multi-location-group.md` - 3-10 locations, centralized management
- `bar-nightclub.md` - High shrink (15%+), spirits inventory, variance analysis
- `hotel-fb.md` - Multiple outlets, F&B + non-F&B inventory
- `bakery-production.md` - Batch production, perishables, multi-day planning
- `budget-constrained-diy.md` - <$100/month, technical resources available

**Value**: Match restaurant type → platform shortlist with implementation roadmap.

### S4: Strategic Analysis (PLANNED)

**Time Estimate**: 4-6 hours
**Goal**: Long-term platform viability, vendor consolidation, ecosystem strategy

**Planned Deliverables**:
- `vendor-viability.md` - 5/10-year survival probability, acquisition risk, funding status
- `market-consolidation.md` - Toast ecosystem strategy, MarketMan M&A trajectory, open-source sustainability
- `open-source-sustainability.md` - Odoo/ERPNext community health, URY longevity risk
- `toast-ecosystem-strategy.md` - POS+inventory bundle analysis, switching costs over time

**Value**: Strategic decision-making for 5+ year platform commitment, vendor lock-in mitigation.

---

## Integration Relationships

**Upstream Dependencies** (Data Flows IN):
- **3.005 POS Systems** → Sales data feeds inventory depletion (xtraCHEF+Toast, MarketMan POS integrations)
- **3.072 Food Service Suppliers** → Supplier ordering, EDI price updates (BlueCart marketplace, distributor integrations)

**Downstream Consumers** (Data Flows OUT):
- **3.006 Accounting Software** → COGS flows to P&L (QuickBooks, Xero integrations for all platforms)

**Parallel Complementary**:
- **3.075 Labor Scheduling** → Labor (30-35%) + Inventory (25-35%) = 60% of restaurant costs (combined optimization)
- **3.074 Production Scheduling** → Inventory availability constrains kitchen production (recipe ingredients, equipment)

**Related DIY Alternatives** (Tier 1):
- **1.096 Scheduling Libraries** → DIY reordering algorithms (par levels, lead times with OR-Tools, PuLP)
- **1.120 Simulation Libraries** → Inventory optimization modeling (SimPy discrete event simulation)

---

## ROI Quick Reference

| Restaurant Type | Revenue | Food Cost | Current Waste | Savings (3%) | Platform Cost | Net ROI | ROI % |
|---|---|---|---|---|---|---|---|
| Small Cafe | $500K | $150K (30%) | $12K (8%) | $4,500 | $1,800 (BlueCart) | $2,700 | 150% |
| Single Restaurant | $1.5M | $450K (30%) | $36K (8%) | $13,500 | $3,600 (MarketMan) | $9,900 | 275% |
| Multi-Location (5) | $7.5M | $2.25M (30%) | $180K (8%) | $67,500 | $18,000 (MarketMan) | $49,500 | 275% |
| Multi-Location ERP | $7.5M | $2.25M (30%) | $180K (8%) | $67,500 | $6,000 (ERPNext) | $61,500 | 1,025% |
| Bar (high shrink) | $1M | $250K (25%) | $37.5K (15%) | $12,500 (5pt) | $2,988 (WISK) | $9,512 | 318% |

**Critical Finding**: Even conservative 3% waste reduction delivers 150-1,025% ROI depending on platform choice.

**Bar Insight**: High-shrink bars (15%+) see 318-421% ROI from variance analysis platforms (WISK, Craftable).

---

## Technical Concepts

**Domain Explainer**: Will be created after S2-S4 completion (MPSE methodology guideline).

**Terms tracked for explanation** (see `01-discovery/TERMS-TO-EXPLAIN.md`):
- Recipe explosion / BOM (Bill of Materials)
- COGS (Cost of Goods Sold) automation
- Variance analysis (theoretical vs. actual usage)
- Shrink, overpouring, waste tracking
- Par levels and automated reordering
- Invoice digitization / OCR processing
- Multi-location centralized management
- Perishable inventory / batch tracking with expiry
- EDI (Electronic Data Interchange) for suppliers
- Kitchen Display System (KDS) integration

---

## Timeline & Status

| Phase | Status | Date | Time | Documents |
|---|---|---|---|---|
| S1 Rapid | ✅ Complete | Nov 30, 2025 | 4h | 8 files (588 KB) |
| S2 Comprehensive | 📋 Planned | Dec 2025 | 6-8h | 6 files est |
| S3 Need-Driven | 📋 Planned | Dec 2025 | 8-10h | 9 files est |
| S4 Strategic | 📋 Planned | Dec 2025 | 4-6h | 5 files est |
| Domain Explainer | 📋 After S2-S4 | Dec 2025 | 2-3h | 1 file |
| **Total** | **25% Complete** | | **26-31h** | **29 files** |

---

## Usage Notes

**For Restaurant Operators**:
1. Start with [S1 Synthesis](01-discovery/S1-rapid/00-SYNTHESIS-quick-recommendations.md) (5-10 min decision)
2. Use decision tree to shortlist 2-3 platforms
3. Request demos from shortlisted platforms
4. Calculate YOUR specific ROI (current waste audit + platform cost)
5. Pilot 1-2 locations for 30-60 days before full rollout (multi-location)

**For Consultants/Advisors**:
- S1 provides client-facing recommendations (generic catalog)
- S2-S4 provides deep analysis for custom implementations
- ROI models customizable to client-specific waste levels
- Implementation roadmaps in S3 scenarios

**For Developers**:
- Integration APIs documented in S2 (POS, accounting, supplier EDI)
- Open-source ERP setup guides in platform profiles
- DIY alternatives cross-referenced (1.096 Scheduling, 1.120 Simulation)

---

## Disclaimer

**Research Disclaimer**:
This research is provided for informational purposes only and should not be considered professional advice. Platform capabilities, pricing, and features change frequently. Waste reduction ROI depends on current waste levels - audit before platform selection. No warranty regarding accuracy, completeness, or fitness for a particular purpose.

**Methodology Transparency**:
See `metadata.yaml` for data sources and attribution. Vendor pricing from official pages (accessed Nov 30, 2025). ROI calculations based on industry benchmarks (ReFED, Supy, CrunchTime, MarketMan studies). Independent validation recommended.

---

**Created**: 2025-11-30
**Updated**: 2025-11-30
**Version**: 1.0 (S1 Complete)
