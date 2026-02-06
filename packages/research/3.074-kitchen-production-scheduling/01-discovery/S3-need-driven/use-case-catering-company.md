# S3 Use Case: Catering Company

**Research ID**: 3.074 - Production Scheduling (Commercial Kitchen)
**Discovery Phase**: S3 Need-Driven
**Date**: November 24, 2025

---

## Business Profile

### Company Overview
**Business Type**: Full-service catering (corporate events, weddings, private parties)
**Annual Revenue**: $1.2M
**Employees**: 15 (8 kitchen staff, 5 event staff, 2 admin)
**Location**: Single commissary kitchen
**Events**: 150-200 events/year (3-4 events/week average, 8-10/week during peak season)
**Average Event Size**: 50-150 guests

### Production Characteristics
- **Production Model**: 100% make-to-order (no make-to-stock)
- **Lead Time**: 2 weeks minimum, 4-8 weeks typical for large events
- **Production Schedule**: Event-driven (multi-day prep for large events)
- **Equipment**: 2 ovens, 3 ranges, 2 refrigerators, 1 walk-in cooler, prep tables
- **Menu**: 30 core menu items, custom menus per event

### Pain Points
1. **Multi-day production planning** - Large events require 3-5 days of staggered prep (marinades Monday, prep Tuesday-Wednesday, cook Thursday, deliver Friday)
2. **Equipment conflicts** - Multiple events in same week compete for oven/refrigerator space
3. **Ingredient ordering timing** - Must order ingredients 3-5 days before event, but menu changes happen 1-2 days before
4. **Staff allocation unclear** - Don't know how many kitchen staff needed for each event until mid-week
5. **Last-minute menu changes** - Clients change headcount or menu items 24-48 hours before event
6. **No centralized event calendar** - Events tracked in Google Calendar + email + paper notes (miss details)

---

## Current State Analysis

### Current Tools
- **Google Calendar**: Event bookings and deadlines
- **Excel spreadsheets**: Menu planning, shopping lists, prep schedules (per event)
- **QuickBooks**: Invoicing and accounting
- **Email**: Client communications, menu approvals
- **Paper notes**: Kitchen prep checklists, equipment assignments

### Weekly Production Planning Process (Current)
1. **Monday**: Review upcoming events for week (Google Calendar)
2. **Create shopping lists**: Manually calculate ingredients needed for each event (Excel)
3. **Order ingredients**: Call/email suppliers (2-3 suppliers)
4. **Create prep schedules**: Hand-write multi-day prep plan for each event (Post-It notes on wall calendar)
5. **Equipment conflicts**: Manually resolve oven/refrigerator conflicts (move prep days around)
6. **Staff scheduling**: Assign kitchen staff based on event size (gut feel, no formal calculation)
7. **Ongoing adjustments**: Client changes require re-planning (1-2 hours per change)

**Total Time Spent Planning**: 10-15 hours/week (owner/head chef)

### Pain Point Details

#### 1. Multi-Day Production Sequencing
- **Example**: 150-person wedding (Friday evening)
  - Monday: Marinate proteins, make sauces
  - Tuesday: Prep vegetables, par-cook proteins
  - Wednesday: Bake desserts, prepare side dishes
  - Thursday: Final cooking, plating prep
  - Friday: Finishing touches, pack, deliver 2pm

- **Problem**: No systematic way to plan multi-day sequence
- **Current Method**: Head chef mentally plans or uses hand-written notes
- **Impact**: Forget steps, prep too early (quality degradation), prep too late (rush/stress)

#### 2. Equipment Conflicts
- **Problem**: 2 events in same week both need oven on Wednesday
- **Example**:
  - Event A (Saturday wedding, 120 people): Needs oven Wednesday for desserts
  - Event B (Thursday corporate lunch, 80 people): Needs oven Wednesday for proteins
  - Resolution: Move Event A desserts to Tuesday, but Tuesday is already packed with Event B prep

- **Current Method**: Trial-and-error, move prep days around until conflicts resolve
- **Impact**: Inefficient scheduling, staff overtime, equipment sits idle some days while over-utilized others

#### 3. Ingredient Ordering Timing
- **Problem**: Order ingredients Monday for Friday event, but client changes headcount Thursday (150 → 180 people)
- **Impact**: Rush supplier order (premium pricing or unavailable), substitute ingredients (quality compromise), over-buy for future use (cash flow tied up in inventory)
- **Cost**: Estimated $8K-12K/year in rush orders and over-buying

#### 4. Last-Minute Menu Changes
- **Problem**: Client changes menu 24-48 hours before event (replace chicken with salmon)
- **Impact**: Already ordered chicken (waste or freeze for future use), rush order salmon, re-plan production schedule mid-week
- **Frequency**: 20-30% of events have last-minute changes
- **Cost**: Estimated $5K-10K/year in wasted ingredients and rush orders

---

## Requirements for Production Scheduling Solution

### Critical Requirements (Must-Have)

1. **Event-driven production planning**
   - Each event is a discrete production project
   - Multi-day prep schedules (Day -5 to Day 0)
   - Visual timeline (what's happening each day)

2. **Equipment capacity scheduling**
   - 2 ovens, 3 ranges, refrigerator space
   - Avoid conflicts (flag when 2 events need same equipment same day)
   - Visual equipment calendar

3. **Recipe scaling**
   - Scale recipes for guest count (50 → 150 people)
   - Automatic ingredient quantity calculations
   - Shopping list generation

4. **Ingredient ordering automation**
   - Generate shopping lists from multiple events
   - Consolidate ingredients across events (Event A needs 10 lbs onions, Event B needs 5 lbs = order 15 lbs total)
   - Supplier ordering workflow

5. **Prep sequencing**
   - Multi-day task lists (what to do Monday, Tuesday, etc.)
   - Dependencies (can't cook until marinated 24 hours)
   - Checklist progress tracking

6. **Menu change handling**
   - Quick re-calculation when headcount changes
   - Re-generate shopping lists
   - Flag ingredient availability issues

### Important (Strong Preference)

7. **Client portal** (event details, menu approval, headcount updates)
8. **Staff allocation** (calculate labor hours needed per event)
9. **QuickBooks integration** (invoicing, COGS tracking)
10. **Mobile access** (kitchen staff check prep checklists on tablets)

### Nice-to-Have

11. **Cost estimation** (quote events based on recipe costs + labor)
12. **Profitability analysis** (track margin per event)

---

## Platform Evaluation

### Option 1: Katana MRP ($179-799/mo)

**Fit Analysis**:
⚠️ **Designed for manufacturing, not event-driven catering**

✅ **What works**:
- Recipe/BOM management (✅)
- Make-to-order workflows (✅)
- Ingredient availability checking (✅)
- Multi-day production (✅ Can model)

❌ **What doesn't work**:
- Not event-centric (models continuous production, not discrete events)
- No event calendar integration
- No client portal
- Overkill for 15-employee operation
- **Cost**: $2,148-9,588/year (too expensive for catering company)

**Recommendation**: ❌ **NOT RECOMMENDED** - Wrong fit. Katana is for manufacturers making 1000s of units, not caterers doing 3-4 custom events/week.

---

### Option 2: Project Management Tools (ClickUp, Monday.com)

**Fit Analysis**:
✅ **Event = Project paradigm works well**

**ClickUp** ($10-19/user/month):
- Each event is a project
- Multi-day task lists (prep schedules)
- Equipment resources (assign oven to tasks)
- Shopping list custom fields
- Mobile app for kitchen checklists
- Calendar view (visualize all events)

**What works**:
- ✅ Event-driven workflows (perfect fit)
- ✅ Multi-day task sequencing
- ✅ Visual timeline
- ✅ Mobile checklists
- ✅ Affordable ($150-285/mo for 15 users)

**What doesn't work**:
- ❌ No recipe scaling (manual calculation)
- ❌ No automatic shopping list consolidation
- ❌ No ingredient availability checking
- ❌ No QuickBooks integration (need Zapier)

**Recommendation**: ⚠️ **GOOD FIT** - Best balance of functionality vs cost for small catering company. Addresses 70% of needs at $1,800-3,420/year.

**Gap**: Manual recipe scaling and shopping lists (head chef still does this in Excel).

---

### Option 3: Catering-Specific Software

#### CaterZen ($99-299/mo)
**Focus**: Event management + catering logistics

✅ **What works**:
- Event calendar and booking
- Menu builder with recipe scaling
- Shopping list generation
- Client portal (menu approval, headcount updates)
- QuickBooks integration
- Timeline and task management

❌ **What doesn't work**:
- ❌ No equipment capacity scheduling (can't model oven conflicts)
- ❌ Limited multi-day production sequencing
- ⚠️ Recipe management not as robust as dedicated MRP

**Cost**: $1,188-3,588/year

**Recommendation**: ✅ **STRONG FIT** - Purpose-built for catering. Addresses event management + production planning. Missing deep equipment scheduling but covers 85% of needs.

#### Total Party Planner ($65-195/mo)
**Focus**: Catering events + rentals + staffing

Similar to CaterZen but less production-focused, more event logistics.

**Recommendation**: ⚠️ **ALTERNATIVE** - Good if need rental management (tables, linens, etc.), less good for kitchen production planning.

---

### Option 4: Spreadsheets + Google Calendar (Current State)

**Fit Analysis**:
✅ **Zero cost**
❌ **High time cost** (10-15 hours/week planning)

**Problems**:
- No automatic recipe scaling
- No consolidated shopping lists
- No equipment conflict detection
- Manual multi-day sequencing (Post-It notes)
- High error rate (forget prep steps, ingredient shortages)

**Opportunity Cost**:
- Head chef time: 15 hours/week × $75K salary ÷ 2080 hours = $540/week = **$28K/year**
- Ingredient waste (rush orders, last-minute changes): **$13K-22K/year**
- Total opportunity cost: **$41K-50K/year**

**Recommendation**: ❌ **NOT VIABLE** - Wasting $41K-50K/year to avoid $1K-4K/year software cost.

---

### Option 5: Custom Build (Event scheduling app)

**Fit Analysis**:
✅ **Perfect fit** (could build exactly what's needed)
❌ **Expensive and risky**

**Build Scope**:
- Event calendar + multi-day task scheduling
- Recipe database + scaling
- Shopping list consolidation
- Equipment resource management
- Mobile app for kitchen checklists

**Cost Estimate**:
- Development: 200-300 hours × $150/hr = **$30K-45K**
- Hosting: $50-100/mo = **$600-1,200/year**
- Maintenance: 20 hours/year × $150/hr = **$3K/year**
- **Year 1 Total**: $33K-49K
- **Year 2+ Annual**: $3.6K-4.2K/year

**Break-Even vs CaterZen** ($2,400/year):
- Break-even: 14-21 years
- Not viable unless operation scales to 10× size

**Recommendation**: ❌ **NOT RECOMMENDED** - Too expensive for 15-employee catering company. Would need $5M+ revenue to justify custom build.

---

## Final Recommendation

### Primary Recommendation: CaterZen ($99-299/mo)
**Total Cost**: $1,188-3,588/year
**Implementation**: 1-2 weeks

**Why CaterZen wins**:
1. **Purpose-built for catering** - Event-driven workflows (vs manufacturing-focused Katana)
2. **Recipe scaling + shopping lists** - Automates manual Excel work (biggest time sink)
3. **Client portal** - Reduces email back-and-forth, clients update headcount directly
4. **QuickBooks integration** - COGS tracking and invoicing
5. **Affordable** - $1,188-3,588/year vs $28K/year opportunity cost
6. **Fast implementation** - 1-2 weeks vs 4-8 weeks for Katana

**Missing Features**:
- ⚠️ Equipment capacity scheduling (can't model oven conflicts)
  - **Workaround**: Continue using Google Calendar for equipment, CaterZen for events/recipes/shopping
- ⚠️ Multi-day production sequencing not as detailed as custom build
  - **Workaround**: Use CaterZen task lists + manual timeline planning (still better than Post-It notes)

**Expected Benefits (Year 1)**:
- **Time savings**: Head chef saves 8-10 hours/week (from 15 hours → 5 hours planning)
  - Value: 10 hours/week × $75K salary ÷ 2080 hours = **$361/week = $18.7K/year**
- **Ingredient waste reduction**: Reduce rush orders and over-buying by 50%
  - Value: $13K-22K × 50% = **$6.5K-11K/year**
- **Menu change handling**: Faster re-planning (30 min vs 2 hours per change)
  - Value: 30% of events × 1.5 hours saved × $36/hr = **$2K/year**
- **Total Year 1 Value**: **$27.2K-31.7K**

**ROI**:
- Cost: $1,188-3,588/year
- Value: $27.2K-31.7K/year
- **ROI**: 658-2,569%
- **Payback**: 14-48 days

---

### Alternative Recommendation: ClickUp Pro ($10/user/mo = $150/mo for 15 users)
**Total Cost**: $1,800/year
**Savings vs CaterZen**: $612/year (if CaterZen Starter vs ClickUp)

**Trade-offs**:
- ✅ Save $612/year
- ✅ More flexible (general project management tool)
- ✅ Excellent mobile app
- ❌ No recipe scaling (still manual in Excel)
- ❌ No automatic shopping list consolidation
- ❌ No QuickBooks integration (need Zapier = $29-73/mo extra)

**When to choose ClickUp**:
- If already using ClickUp for other business operations (event staffing, client communications)
- If willing to keep Excel for recipe scaling/shopping lists
- If want maximum flexibility (ClickUp can do more than just catering)

**Hybrid Approach**: ClickUp ($1,800/year) + Zapier ($348/year) + keep Excel for recipes = **$2,148/year total** (still cheaper than CaterZen $2,400/year Grow plan, but more manual work)

---

### Budget Recommendation: Keep Spreadsheets + Improve Process
**Cost**: $0 software, but high opportunity cost

**Improvements to current process** (if can't afford software yet):
1. **Standardize Excel templates** (event planning template, shopping list template)
2. **Use Google Calendar for equipment** (create calendar entries for "Oven 1", "Oven 2")
3. **Create recipe database in Google Sheets** (centralize recipes, add scaling formulas)
4. **Use Google Forms for client approvals** (menu changes, headcount updates)

**Expected impact**:
- Reduce planning time 20-30% (15 hours/week → 10-11 hours/week)
- Value: **$7K-10K/year**
- **Still leaves $18K-22K/year on table** vs CaterZen

**Recommendation**: ⚠️ **Only if cash flow extremely tight** - But should upgrade to CaterZen within 6-12 months. Wasting $20K+/year to save $1.2K/year software cost doesn't make sense.

---

## Implementation Plan (CaterZen)

### Week 1: Setup
- Create CaterZen account (Starter $99/mo or Grow $249/mo)
- Import 30 core recipes
- Set up client accounts (active clients for next 3 months)
- Import upcoming events (next 30 days)
- QuickBooks integration setup

**Who**: Owner + CaterZen onboarding
**Time**: 8-10 hours

### Week 2: Parallel Run
- Use CaterZen for new event inquiries
- Continue using Google Calendar + Excel for existing events
- Test recipe scaling, shopping list generation on 1-2 small events

**Who**: Owner + head chef
**Time**: 4-6 hours

### Week 3: Full Transition
- Move all events to CaterZen
- Stop using Excel for shopping lists
- Train kitchen staff on mobile checklist app

**Who**: All staff
**Time**: 2-3 hours training

### Week 4+: Optimization
- Enable client portal (clients can view/approve menus)
- Analyze event profitability reports
- Adjust pricing based on actual COGS data

---

## Success Metrics

### 3 Months Post-Implementation
- ✅ Event planning time reduced 50% (15 hours/week → 7-8 hours/week)
- ✅ Ingredient rush orders reduced 30-50%
- ✅ Menu changes processed in 30 min (vs 1-2 hours)

### 6 Months Post-Implementation
- ✅ Event planning time reduced 60-70% (15 hours/week → 5-6 hours/week)
- ✅ Clients using portal (50% adoption for menu approvals)
- ✅ Event profitability analysis complete (identify low-margin events, adjust pricing)

### 12 Months Post-Implementation
- ✅ Time savings: $18.7K/year (head chef productivity)
- ✅ Ingredient waste reduction: $6.5K-11K/year
- ✅ **Total value delivered**: $25K-30K/year
- ✅ **Cost**: $1,188-3,588/year
- ✅ **ROI**: 597-2,426%

---

## Conclusion

For a 15-employee catering company doing $1.2M revenue:

**CaterZen is the clear winner** ($1,188-3,588/year).

**ROI is strong**: 658-2,569% Year 1.

**Payback period**: 14-48 days.

**Key success factors**:
1. Recipe scaling automation (eliminates Excel manual work)
2. Shopping list consolidation (saves time, reduces errors)
3. Client portal (reduces email back-and-forth, handles menu changes faster)

**Implementation risk**: Low (1-2 week setup, catering-specific so proven workflows).

**Alternative**: ClickUp ($1,800/year) if want general project management flexibility, but sacrifice catering-specific features (recipe scaling, shopping lists).

**Bottom line**: Spending $1K-4K/year to save $25K-30K/year is a no-brainer. Current spreadsheet approach is costing $20K+/year in wasted time.
