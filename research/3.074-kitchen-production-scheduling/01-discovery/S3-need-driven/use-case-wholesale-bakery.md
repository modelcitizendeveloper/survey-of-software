# S3 Use Case: Wholesale Bakery

**Research ID**: 3.074 - Production Scheduling (Commercial Kitchen)
**Discovery Phase**: S3 Need-Driven
**Date**: November 24, 2025

---

## Business Profile

### Company Overview
**Business Type**: Wholesale bakery with retail storefront
**Annual Revenue**: $2.5M
**Employees**: 50 (30 production, 10 retail, 10 admin/delivery)
**Locations**: 3 (main production facility, 2 retail stores with small production)
**Product Mix**: 200 active SKUs (bread, pastries, cakes, specialty items)

### Production Characteristics
- **Volume**: 15,000-20,000 units/week
- **Production Model**: 70% make-to-stock (bread, standard pastries), 30% make-to-order (custom cakes, catering)
- **Production Schedule**: 7 days/week (overnight baking for bread, day shift for pastries/cakes)
- **Equipment**: 8 ovens, 6 mixers, 4 proofers, 2 sheeters, extensive refrigeration/freezing
- **Delivery**: 3 routes, 5 days/week to 75 wholesale accounts (restaurants, cafes, grocery stores)

### Pain Points
1. **Manual spreadsheet scheduling** - Production manager spends 8 hours/week planning production
2. **Equipment bottlenecks** - Ovens fully utilized 6am-2pm, idle after 3pm
3. **Ingredient shortages** - Discover missing ingredients mid-production 2-3 times/week
4. **Delivery coordination** - Orders go to production but delivery team doesn't know when items will be ready
5. **Product profitability unknown** - Know revenue per product, but not true COGS (ingredient waste, labor allocation)
6. **Recipe inconsistency** - 3 production shifts use slightly different recipes (no version control)
7. **Regulatory compliance burden** - Manual lot tracking, HACCP logs on paper

---

## Current State Analysis

### Current Tools
- **Excel spreadsheets**: Production planning (manually updated daily)
- **QuickBooks**: Accounting, invoicing
- **Paper tickets**: Production orders written by hand
- **Google Calendar**: Delivery routes and custom cake deadlines
- **Square POS**: Retail storefront sales
- **Email/phone**: Wholesale order entry (no online portal)

### Weekly Production Planning Process (Current)
1. **Monday morning** (2 hours): Production manager reviews wholesale orders (email/phone), retail forecast, inventory levels
2. **Create production schedule**: Manually allocate SKUs to production shifts in Excel
3. **Check ingredient availability**: Cross-reference inventory spreadsheet (often out-of-date)
4. **Assign ovens/equipment**: Manually schedule oven slots (bread 6am-10am, pastries 10am-2pm, etc.)
5. **Print production tickets**: Hand-written orders distributed to shift leads
6. **Mid-week adjustments**: Rush orders, equipment breakdowns, ingredient shortages require re-planning (1-2 hours)
7. **Friday review**: Variance analysis (planned vs actual production) - rarely done due to time constraints

**Total Time Spent Planning**: 8-10 hours/week (production manager)

### Pain Point Details

#### 1. Equipment Bottlenecks
- **Problem**: 8 ovens fully utilized 6am-2pm (100% capacity), then 30% utilized 2pm-6pm
- **Root Cause**: No visibility into equipment schedule, production planned by product type not equipment utilization
- **Impact**: Could produce 25-30% more if ovens were scheduled optimally
- **Revenue Opportunity**: $625K-750K additional annual revenue at current margins

#### 2. Ingredient Shortage Discovery
- **Problem**: Discover missing ingredients 2-3 times/week after production has started
- **Root Cause**: Inventory spreadsheet updated weekly (not real-time), no ingredient availability check before scheduling production
- **Impact**: Production delays (1-2 hours), ingredient substitutions (quality issues), rush supplier orders (premium pricing)
- **Cost**: Estimated $15K-25K/year in rush orders and lost productivity

#### 3. Recipe Inconsistency
- **Problem**: Night shift uses different flour ratio than day shift for same bread recipe
- **Root Cause**: No centralized recipe database, bakers use personal notebooks
- **Impact**: Product quality variance, customer complaints, returns/credits
- **Cost**: Estimated $10K-20K/year in returns/credits

#### 4. Unknown Product Profitability
- **Problem**: Know revenue per SKU, but not true COGS (ingredient costs change, labor allocation unclear, overhead not allocated)
- **Root Cause**: No recipe costing system, labor not tracked by product
- **Impact**: May be losing money on some products without knowing
- **Risk**: Selling unprofitable products at volume

---

## Requirements for Production Scheduling Solution

### Critical Requirements (Must-Have)

1. **Multi-location production planning**
   - Schedule production across 3 facilities
   - Main facility: 90% of volume
   - Retail locations: 10% of volume (specialty items, rush orders)

2. **Equipment capacity scheduling**
   - Model 8 ovens, 6 mixers, 4 proofers
   - Visual equipment utilization dashboard
   - Optimize oven usage (reduce idle time 2pm-6pm)

3. **Recipe management with version control**
   - 200 recipes stored centrally
   - Automatic ingredient cost calculations
   - Recipe versioning (track changes, roll back if needed)

4. **Ingredient availability checking**
   - Real-time inventory visibility
   - Check ingredient availability before scheduling production
   - Automatic reorder triggers based on production schedule

5. **Make-to-stock + Make-to-order workflows**
   - 70% make-to-stock (bread, standard items)
   - 30% make-to-order (custom cakes, catering)
   - Production priority management (rush orders)

6. **Lot tracking and traceability**
   - Forward/backward lot traceability
   - HACCP compliance (FDA requirements)
   - Recall readiness

7. **Integration with accounting**
   - QuickBooks integration (already using)
   - COGS calculation and product profitability

8. **Delivery coordination**
   - Link production completion to delivery schedule
   - Visibility for delivery team (when will order be ready?)

### Important (Strong Preference)

9. **Wholesale order portal**
   - Customers place orders online (reduce phone/email order entry)
   - Integration with production scheduling

10. **Production cost tracking**
   - Labor allocation by product
   - Overhead allocation
   - Variance analysis (planned vs actual costs)

11. **Nutritional analysis**
   - Label compliance (FDA Nutrition Facts)
   - Allergen tracking

12. **Multi-shift scheduling**
   - Night shift (bread), day shift (pastries), afternoon shift (cakes)
   - Shift handoff visibility

13. **Mobile access**
   - Production floor staff update status on tablets
   - Managers check production status remotely

### Nice-to-Have

14. **Delivery route optimization**
   - Optimize 3 routes, 75 customers

15. **Customer portal**
   - Customers check order status

16. **Waste/scrap tracking**
   - Track production waste by SKU

---

## Platform Evaluation

### Option 1: FlexiBake Professional ($375/mo + $165 × 4 users = $1,035/mo)

**Fit Analysis**:
✅ **Excellent fit for bakery-specific needs**
- Bakery workflows (mixing, proofing, baking) built-in
- Nutritional analysis and FDA labeling compliance
- Storage room/freezer management
- 20 years bakery domain expertise

✅ **Meets critical requirements**:
- Multi-location production (✅ Enterprise tier needed for 3 locations)
- Recipe management with version control (✅)
- Lot tracking and traceability (✅)
- Make-to-order + make-to-stock (✅)
- QuickBooks integration (✅)
- Online order portal (✅ included in Base+)

⚠️ **Partial fit**:
- Equipment capacity scheduling (⚠️ Basic - can schedule but not deep optimization)
- Delivery route optimization (✅ Included but basic)
- Mobile access (⚠️ Limited mobile features)

❌ **Gaps**:
- Modern UI (❌ Dated interface, feels like 2010s software)
- Deep equipment optimization (❌ Can't model oven utilization to maximize capacity)

**Total Cost**:
- **Setup**: Included (4-8 week implementation)
- **Year 1**: $1,035/mo × 12 = **$12,420**
- **5-Year TCO**: **$62,100**

**Recommendation**: ✅ **BEST FIT** - FlexiBake is industry standard for wholesale bakeries. Bakery-specific features (nutritional analysis, HACCP, bakery workflows) justify higher cost vs general MRP.

**Upgrade Path**: Start with FlexiBake Professional, upgrade to Enterprise when hit multi-facility complexity.

---

### Option 2: Katana Professional ($799/mo, unlimited users)

**Fit Analysis**:
✅ **Strong fit for general food manufacturing**
- Modern, visual interface
- Unlimited users (huge cost savings - 5+ users included vs $165/user FlexiBake)
- Strong integration ecosystem (Shopify, ShipStation, accounting)
- Up to 10 locations supported

✅ **Meets critical requirements**:
- Multi-location production (✅ 10 locations supported)
- Recipe/BOM management (✅)
- Ingredient availability checking (✅)
- Real-time inventory (✅)
- Make-to-order + make-to-stock (✅)
- QuickBooks integration (✅)
- Mobile app (✅ Better than FlexiBake)

⚠️ **Partial fit**:
- Equipment capacity scheduling (⚠️ Basic - visual dashboard but no deep optimization)
- Lot tracking (✅ Good but not bakery-specific HACCP)

❌ **Gaps**:
- No bakery-specific features (❌ No nutritional analysis, no FDA labeling)
- No HACCP compliance tools (❌ Generic lot tracking, not bakery-focused)
- No online order portal (❌ Would need separate system)

**Total Cost**:
- **Setup**: Included (2-4 week implementation)
- **Year 1**: $799/mo × 12 = **$9,588**
- **5-Year TCO**: **$47,940**

**Recommendation**: ⚠️ **GOOD ALTERNATIVE** - If willing to sacrifice bakery-specific features for modern UI and unlimited users. Save $14,160 over 5 years vs FlexiBake.

**Trade-off**: Modern software + cost savings vs bakery domain expertise

---

### Option 3: MRPeasy Professional ($75-149/mo estimated)

**Fit Analysis**:
✅ **Affordable entry point**
- Lowest cost real MRP ($75-149/mo vs $375-799/mo)
- Simple implementation (2-4 weeks)
- QuickBooks integration
- Food production features (expiry, lot tracking)

✅ **Meets critical requirements**:
- Recipe/BOM management (✅)
- Lot tracking (✅)
- Make-to-order + make-to-stock (✅)
- QuickBooks integration (✅ Certified)
- Backward scheduling (✅ NEW 2025 feature)

⚠️ **Partial fit**:
- Multi-location (⚠️ Supported but less robust than FlexiBake/Katana)
- Equipment scheduling (⚠️ Basic capacity planning)

❌ **Gaps**:
- No bakery-specific features (❌)
- No nutritional analysis (❌)
- No HACCP compliance (❌)
- No online order portal (❌)
- Limited warehouse management (❌ Not suitable for complex multi-facility)

**Total Cost**:
- **Setup**: Included
- **Year 1**: $149/mo × 12 = **$1,788** (estimated Professional tier)
- **5-Year TCO**: **$8,940**

**Recommendation**: ⚠️ **BUDGET OPTION** - If budget is primary constraint and willing to sacrifice bakery-specific features. Save $53,160 over 5 years vs FlexiBake.

**Risk**: May outgrow MRPeasy within 2-3 years as complexity increases. Switching costs could negate savings.

---

### Option 4: BatchMaster Enterprise (Custom pricing, estimated $50K-200K Year 1)

**Fit Analysis**:
✅ **Best-in-class for enterprise bakeries**
- SAP Business One foundation
- Advanced HACCP and FDA compliance
- Multi-facility warehouse management
- Side-by-side formula cost comparison
- Advanced production scheduling (MPS + MRP)

✅ **Exceeds all critical requirements**
- Everything FlexiBake does, plus enterprise-grade features
- Best compliance and traceability tools
- Most advanced production scheduling

❌ **Overkill**:
- **Too expensive** for $2.5M revenue bakery (likely $50K-200K Year 1)
- **Too complex** for 50-employee operation (8-16 week implementation)
- **Requires dedicated IT staff** (not justifiable at this scale)

**Total Cost**:
- **Setup**: $20K-100K (professional services, training)
- **Year 1**: $50K-200K+
- **5-Year TCO**: $200K-500K+

**Recommendation**: ❌ **NOT RECOMMENDED** - Overkill for this business size. Consider when revenue hits $10M+ or multi-facility complexity increases 5×.

---

### Option 5: Keep Current System (Excel Spreadsheets)

**Fit Analysis**:
✅ **Zero software cost**
- No monthly fees
- Infinite customization

❌ **Doesn't solve problems**:
- Manual planning (8-10 hours/week wasted)
- No equipment optimization (missing $625K-750K revenue opportunity)
- Ingredient shortage discovery (costing $15K-25K/year)
- Recipe inconsistency (costing $10K-20K/year)
- No product profitability analysis

**Total Cost**:
- **Software**: $0
- **Opportunity cost**: $650K-795K/year (equipment optimization + waste reduction)
- **Time cost**: Production manager salary × 20% = ~$15K/year (8 hours/week @ $75K salary)

**Recommendation**: ❌ **NOT VIABLE** - Opportunity cost far exceeds software investment. Losing $650K+/year in missed revenue/waste.

**Break-even**: FlexiBake ($12K/year) pays for itself if captures just 2% of equipment optimization opportunity ($12K ÷ $650K = 1.8%).

---

## Final Recommendation

### Primary Recommendation: FlexiBake Professional
**Total Cost**: $12,420/year (first year), $1,035/mo ongoing
**Implementation**: 4-8 weeks
**ROI Payback**: <1 month

**Why FlexiBake wins**:
1. **Industry standard** - 500+ bakeries, 20 years proven
2. **Bakery-specific** - Nutritional analysis, HACCP, FDA compliance built-in
3. **Regulatory compliance** - Critical for wholesale bakery (lot tracking, recalls)
4. **Equipment scheduling** - Solves oven bottleneck (even if not deeply optimized)
5. **Recipe standardization** - Eliminates recipe inconsistency issue
6. **Online order portal** - Reduces phone/email order entry (saves admin time)
7. **Mature, stable** - Lower vendor risk than newer platforms

**Expected Benefits (Year 1)**:
- **Equipment optimization**: Increase oven utilization 15-20% = $375K-500K additional revenue (conservative estimate)
- **Ingredient waste reduction**: Eliminate rush orders and shortages = $15K-25K savings
- **Recipe standardization**: Reduce returns/credits = $10K-20K savings
- **Time savings**: Production manager saves 6-8 hours/week = $12K/year value
- **Product profitability**: Identify unprofitable products, adjust pricing = $25K-75K margin improvement

**Total Year 1 Value**: $437K-632K (conservative)
**Year 1 Cost**: $12K
**ROI**: 3,542-5,167%
**Payback Period**: 7-10 days

---

### Alternative Recommendation: Katana Professional (if prioritize modern UX)
**Total Cost**: $9,588/year, $799/mo ongoing
**Savings vs FlexiBake**: $2,832/year ($14,160 over 5 years)

**Trade-offs**:
- ✅ Save $14K over 5 years
- ✅ Modern interface (easier user adoption)
- ✅ Unlimited users (future-proof for team growth)
- ❌ No nutritional analysis (would need separate tool)
- ❌ No HACCP compliance (generic lot tracking only)
- ❌ No online order portal (would need separate system)

**When to choose Katana**:
- If plan to expand beyond bakery (e.g., add meal prep line, catering products)
- If user experience and team adoption are top priorities
- If don't need FDA nutritional labels (only selling to restaurants, not retail packaged)

---

### Budget Recommendation: MRPeasy Professional (if budget-constrained)
**Total Cost**: $1,788/year (estimated)
**Savings vs FlexiBake**: $10,632/year ($53,160 over 5 years)

**Trade-offs**:
- ✅ Save $53K over 5 years
- ✅ Simple, fast implementation
- ✅ QuickBooks integration
- ❌ No bakery-specific features
- ❌ May outgrow within 2-3 years
- ❌ Switching costs later could negate savings

**When to choose MRPeasy**:
- If cash flow is extremely tight (<$100K working capital)
- If want to "test" production scheduling before committing to FlexiBake
- If plan to switch to FlexiBake in 2-3 years anyway (use MRPeasy as stepping stone)

---

## Implementation Plan (FlexiBake)

### Phase 1: Data Preparation (Weeks 1-2)
**Tasks**:
- Recipe documentation (200 recipes → FlexiBake format)
- Ingredient inventory (create SKU list, current quantities)
- Customer account setup (75 wholesale accounts)
- Product catalog (200 SKUs with pricing, recipes)

**Who**: Production manager + FlexiBake onboarding specialist
**Time**: 20-30 hours total

---

### Phase 2: System Configuration (Weeks 3-4)
**Tasks**:
- FlexiBake setup (locations, equipment, users)
- Recipe import and validation
- Inventory import
- QuickBooks integration testing
- Production workflow configuration (make-to-stock, make-to-order)

**Who**: FlexiBake implementation team
**Time**: 2-3 days on-site training/setup

---

### Phase 3: Parallel Run (Weeks 5-6)
**Tasks**:
- Run FlexiBake AND Excel in parallel
- Production manager plans in both systems
- Compare results (FlexiBake schedule vs Excel schedule)
- Identify gaps, adjust FlexiBake configuration
- Train production shift leads (3 shifts × 2 hours = 6 hours training)

**Who**: Production manager, shift leads, FlexiBake support
**Time**: 2 weeks parallel operation

---

### Phase 4: Go-Live (Week 7)
**Tasks**:
- Turn off Excel planning
- Production manager uses FlexiBake exclusively
- Daily check-ins with FlexiBake support (first 2 weeks)
- Address issues as they arise

**Who**: All production staff
**Time**: Ongoing

---

### Phase 5: Optimization (Weeks 8-12)
**Tasks**:
- Analyze equipment utilization reports
- Adjust production schedule based on data
- Enable online order portal for wholesale customers
- Train delivery team on order status visibility
- Product profitability analysis (identify losers, adjust pricing)

**Who**: Production manager, FlexiBake optimization specialist
**Time**: Monthly review meetings (first 3 months)

---

## Success Metrics

### 3 Months Post-Implementation
- ✅ Production planning time reduced 50% (8 hours/week → 4 hours/week)
- ✅ Ingredient shortage incidents reduced 75% (2-3/week → <1/week)
- ✅ Oven utilization increased 10% (baseline improvement)
- ✅ Recipe consistency issues eliminated (zero customer returns due to recipe variance)

### 6 Months Post-Implementation
- ✅ Production planning time reduced 75% (8 hours/week → 2 hours/week)
- ✅ Oven utilization increased 15-20%
- ✅ Product profitability analysis complete (identify 10-15 unprofitable SKUs)
- ✅ Wholesale customers using online order portal (50% adoption)

### 12 Months Post-Implementation
- ✅ Revenue increase 15-20% ($375K-500K) from equipment optimization
- ✅ Ingredient waste reduced $15K-25K
- ✅ Returns/credits reduced $10K-20K
- ✅ Production manager time savings = $12K value
- ✅ **Total value delivered**: $412K-557K
- ✅ **ROI**: 3,333-4,508% (Year 1)

---

## Risk Mitigation

### Risk 1: User adoption (production staff resist new system)
**Mitigation**:
- Involve shift leads in selection process (buy-in)
- Hands-on training (not just manuals)
- Parallel run period (prove it works before forcing adoption)
- Quick wins (show time savings in first 2 weeks)

### Risk 2: Data migration issues (recipe errors, inventory inaccuracies)
**Mitigation**:
- Audit top 50 recipes (80% of volume) before import
- Physical inventory count before go-live
- Validation checks during parallel run

### Risk 3: Integration failures (QuickBooks sync issues)
**Mitigation**:
- Test QuickBooks integration in sandbox environment
- FlexiBake has 20 years of QuickBooks integration experience (low risk)
- Backup plan: Manual accounting sync for first month if needed

### Risk 4: Vendor viability (FlexiBake goes out of business)
**Mitigation**:
- FlexiBake has 500+ customers, 20 years history (low risk)
- Data export capability (can migrate to competitor if needed)
- Alternative: Katana or BatchMaster as backup options

---

## Conclusion

For a 50-employee wholesale bakery doing $2.5M revenue:

**FlexiBake Professional is the clear winner** ($12,420/year).

**ROI is exceptional**: 3,333-4,508% Year 1 (conservative estimate).

**Payback period**: 7-10 days.

**Key success factors**:
1. Equipment optimization (biggest value driver)
2. Recipe standardization (eliminates quality variance)
3. Ingredient availability checking (eliminates rush orders)
4. Product profitability analysis (stop selling losers)

**Implementation risk**: Low (mature platform, proven in 500+ bakeries, 4-8 week implementation).

**Alternative paths**: Katana (modern UX, unlimited users) or MRPeasy (budget option) are viable if FlexiBake's bakery-specific features aren't critical.
