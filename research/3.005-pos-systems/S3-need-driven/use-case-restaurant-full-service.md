# S3-Need-Driven: Full-Service Restaurant (Table Service)

## Scenario Overview

### Business Description
Full-service restaurants where customers are seated, served by waitstaff, and pay at the table or checkout counter. Includes casual dining, fine dining, bistros, and family restaurants.

### Typical Characteristics
- **Service model:** Table service with servers
- **Seating:** 30-150 seats typically
- **Staff:** 5-30 employees (servers, hosts, kitchen, management)
- **Transaction volume:** 100-500 covers per day
- **Average check:** $25-$75 per person
- **Monthly revenue:** $50,000-$300,000 (varies widely by size)
- **Complexity:** Multi-course meals, modifiers, split bills, tip management

### Common Pain Points
- **Manual table management:** Paper seating charts, server section confusion
- **Order errors:** Miscommunication between front-of-house and kitchen
- **Slow kitchen communication:** Handwritten tickets hard to read, get lost
- **Split bill headaches:** Guests want to split by item, seat, or custom amounts
- **Tip distribution:** Manual calculation of tip pooling and distribution
- **Inventory waste:** No tracking of food waste or recipe costs
- **Lack of insights:** Don't know best-selling items, labor costs, or margins

### POS Requirements

**Critical (Must-Have):**
- ✅ Visual floor plan with table status (open, occupied, reserved)
- ✅ Server sections and assignment
- ✅ Menu modifiers (no onions, extra cheese, dressing on side, etc.)
- ✅ Kitchen routing (send orders to specific stations: grill, fryer, salad, dessert)
- ✅ Split bills (by item, by seat, custom amounts)
- ✅ Tip tracking and reporting
- ✅ Course management (hold entrees until appetizers sent)

**Important (Strong Preference):**
- ✅ Kitchen Display System (KDS) - digital screens replace paper tickets
- ✅ Tableside ordering (servers enter orders at table on handheld device)
- ✅ 86'ing items (mark items out of stock during service)
- ✅ Recipe costing and food cost tracking
- ✅ Third-party delivery integration (DoorDash, Uber Eats, Grubhub)
- ✅ Online ordering (commission-free preferred)
- ✅ Reporting (sales, labor costs, menu performance)

**Nice-to-Have (Optional):**
- ✅ Reservation system integration
- ✅ Customer profiles and loyalty program
- ✅ Inventory management for dry goods and supplies
- ✅ Labor forecasting
- ✅ Gift cards

---

## Primary Recommendation: Toast POS

### Platform: Toast
**Plan:** Point of Sale Plan ($69/month)
**Why Toast is the Best Fit:**

1. **Purpose-built for restaurants:** Every feature designed for food service
2. **Industry-leading table management:** Visual floor plans, server sections, table transfers
3. **Excellent kitchen operations:** Best-in-class Kitchen Display System (KDS)
4. **Comprehensive features:** All critical and most important features included
5. **Market leader:** 21.74% market share, trusted by 100,000+ restaurants
6. **Commission-free online ordering:** Build direct customer relationships
7. **Robust reporting:** Food cost, labor cost, menu performance analytics

### Expected Monthly Costs

**Hypothetical Restaurant:** 50-seat casual dining, $100,000/month revenue, 15 employees

| Cost Category | Amount |
|---------------|--------|
| **Software** | $69/mo (Point of Sale plan) |
| **Payment Processing** | ~$2,490/mo (2.49% on $100K revenue) |
| **Payroll Module (optional)** | $90/mo + $135 (15 employees × $9) = $225/mo |
| **Total Monthly (no payroll)** | **~$2,559/mo** |
| **Total Monthly (with payroll)** | **~$2,784/mo** |

**Hardware (One-Time):**
- 2× Toast Flex terminals (POS + handheld): $1,600
- 1× Kitchen Display System: $700
- 1× Receipt printer + cash drawer: $500
- **Total Hardware:** ~$2,800

**Year 1 Total Cost (without payroll):** $2,559 × 12 + $2,800 = **$33,508**

### Implementation Timeline
- **Week 1:** Order hardware, menu setup, staff accounts
- **Week 2:** Hardware delivery and installation
- **Week 3:** Staff training (2-3 hours for servers, 4-6 hours for managers)
- **Week 4:** Parallel testing (run Toast alongside old system)
- **Go-Live:** End of Week 4

---

## Setup Guide

### Hardware Needed
- **POS terminals:** 1-2 Toast Flex devices (for checkout/manager station)
- **Handheld devices:** 1 per 3-4 servers (Toast Go for tableside ordering)
- **Kitchen Display System:** 1-2 screens (depending on kitchen layout)
- **Receipt printer:** 1 at checkout, optional at bar
- **Cash drawer:** 1 at checkout
- **Kitchen printers:** Backup option if not using KDS

### Software Configuration Steps
1. **Menu setup:**
   - Import or manually enter all menu items
   - Create modifiers (no X, extra Y, dressing on side, etc.)
   - Set up menu categories (appetizers, entrees, desserts, drinks)
   - Assign prices and tax rates

2. **Floor plan:**
   - Design visual floor plan matching restaurant layout
   - Number all tables
   - Create server sections

3. **Kitchen routing:**
   - Set up kitchen stations (grill, fryer, salad, dessert, etc.)
   - Route menu items to appropriate stations
   - Configure KDS display settings

4. **Staff accounts:**
   - Create account for each employee with PIN
   - Assign roles (server, bartender, host, manager)
   - Set permissions (servers can't comp items, managers can)

5. **Payment processing:**
   - Activate Toast Payments (required)
   - Configure tip prompts and suggestions
   - Set up split bill options

### Integration Checklist
- ✅ **Accounting:** Connect QuickBooks or Xero for automatic sales export
- ✅ **Delivery:** Integrate DoorDash, Uber Eats, Grubhub (if used)
- ✅ **Online Ordering:** Set up Toast Online Ordering (commission-free)
- ✅ **Reservations (optional):** Integrate OpenTable or Resy
- ✅ **Payroll (optional):** Add Toast Payroll or integrate with Gusto/ADP

### Training Requirements
**Servers (2 hours):**
- Logging in with PIN
- Taking orders, adding modifiers
- Transferring tables, splitting bills
- Processing payments and tips
- Handling voids/refunds

**Managers (4-6 hours):**
- All server functions
- Opening/closing procedures
- Running reports
- Managing 86'd items
- Handling exceptions and comps
- Reviewing daily sales

**Kitchen Staff (1 hour):**
- Reading KDS
- Bumping completed orders
- Managing ticket times

### Time to Go-Live
**4 weeks** for smooth implementation with parallel testing

---

## Alternative Options

### Alternative #1: TouchBistro
**When to choose:** Prioritize offline reliability, want standard iPads, need processor flexibility

**Pros vs Toast:**
- ✅ Best offline mode (hybrid cloud + local server)
- ✅ Works with standard iPads (easier/cheaper to replace)
- ✅ Can choose payment processor (not locked in)
- ✅ Commission-free online ordering included

**Cons vs Toast:**
- ❌ Less transparent pricing (must contact sales)
- ❌ Smaller ecosystem and fewer integrations
- ❌ Many features are add-ons (cost adds up)
- ❌ Requires local server for best offline mode ($500-$1,000)

**Expected Cost:** Similar to Toast (~$2,500-$2,800/mo) but hardware may cost more with local server

**Choose TouchBistro if:**
- Internet reliability is a major concern
- You want to own standard iPads instead of Toast-branded hardware
- You want to shop around for payment processors
- You prefer local server backup

### Alternative #2: Lightspeed Restaurant
**When to choose:** Inventory management critical, need advanced recipe costing

**Pros vs Toast:**
- ✅ Better inventory management (ingredient tracking, suppliers)
- ✅ Advanced recipe costing and waste tracking
- ✅ No long-term contract (month-to-month)
- ✅ Works with standard iPads

**Cons vs Toast:**
- ❌ More expensive (starts $189/mo for full features vs Toast $69/mo)
- ❌ Steeper learning curve
- ❌ Fewer integrations than Toast
- ❌ Less market presence in full-service segment

**Expected Cost:** ~$2,689/mo ($189 software + 2.6% processing on $100K)

**Choose Lightspeed Restaurant if:**
- Recipe costing and food cost control are top priorities
- You need advanced inventory with supplier management
- You value month-to-month flexibility
- You're willing to invest time in learning curve

### Budget Alternative: Square for Restaurants (Plus Plan)
**When to choose:** Budget constrained, simpler operations acceptable

**Pros vs Toast:**
- ✅ Lower monthly cost ($69/mo same, but 2.6% vs 2.49% processing)
- ✅ Simpler interface (easier to learn)
- ✅ No contract commitment (month-to-month)
- ✅ Cheaper hardware (Square Terminal $299 vs Toast Flex $799)

**Cons vs Toast:**
- ❌ Less robust table management
- ❌ More basic KDS
- ❌ Limited recipe costing
- ❌ Not purpose-built for full-service restaurants
- ❌ Higher processing fees (0.11% more = $110/mo on $100K revenue)

**Expected Cost:** ~$2,669/mo ($69 software + 2.6% processing on $100K) + cheaper hardware

**Choose Square if:**
- You're budget-constrained and need lower upfront hardware cost
- Your operations are simpler (limited menu, fewer modifiers)
- You value month-to-month flexibility
- You want the simplest possible system

---

## Avoid These Platforms

### ❌ Clover
**Why it doesn't fit:**
- Designed for retail and QSR, not full-service restaurants
- Table management basic compared to Toast
- Kitchen operations not as advanced
- Sold through resellers (pricing varies, less transparent)

**Common misconception:** "Clover can do everything via apps"
**Reality:** App marketplace doesn't match purpose-built restaurant POS features

### ❌ Shopify POS
**Why it doesn't fit:**
- No table management
- No kitchen display system
- No course management
- Designed for retail and omnichannel, not restaurants

**When Shopify might work:** Quick-service counter (no tables), but Square better for that

### ❌ Lightspeed Retail (Wrong Product)
**Why it doesn't fit:**
- This is Lightspeed's retail product, not restaurant product
- Use Lightspeed Restaurant instead if considering Lightspeed

---

## Real-World Cost Example

### Scenario: 60-seat Italian Bistro
- **Concept:** Casual full-service Italian restaurant
- **Hours:** Dinner service, 5pm-10pm, Tue-Sun
- **Covers:** ~250/day average (1,750/week, 7,000/month)
- **Average check:** $45 per person
- **Monthly revenue:** $315,000 (7,000 covers × $45)
- **Staff:** 20 employees (servers, kitchen, management)

### Toast POS - Month 1 Costs

**Software:**
- Point of Sale plan: $69/mo
- Toast Payroll (optional): $90 + (20 × $9) = $270/mo
- **Software Total:** $339/mo

**Payment Processing:**
- Processing rate: 2.49% + 15¢
- $315,000 × 0.0249 = $7,844
- 7,000 transactions × $0.15 = $1,050
- **Processing Total:** $8,894/mo

**Hardware (One-Time):**
- 3× Toast Flex (2 POS, 1 manager): $2,400
- 5× Toast Go (tableside ordering): $2,500
- 2× Kitchen Display Systems: $1,400
- 1× Receipt printer + cash drawer: $500
- **Hardware Total:** $6,800

**Month 1 Total:** $339 + $8,894 + $6,800 = **$16,033**

### Ongoing Monthly Costs
- Software: $339/mo
- Processing: ~$8,894/mo
- **Total:** **~$9,233/mo**

### Year 1 Total Cost of Ownership
$9,233 × 12 + $6,800 (hardware) = **$117,596**

### Cost as % of Revenue
$117,596 / ($315,000 × 12) = $117,596 / $3,780,000 = **3.11% of revenue**

**Industry benchmark:** 2.5-3.5% for payment processing + POS is normal

---

## Implementation Checklist

### Pre-Purchase Tasks
- [ ] Calculate expected costs at your revenue volume
- [ ] Request Toast demo (schedule with sales)
- [ ] Visit restaurant using Toast (ask owner about experience)
- [ ] Review contract terms (typically 24-month commitment)
- [ ] Verify internet reliability (or plan for backup internet)
- [ ] Measure kitchen for KDS placement
- [ ] List all menu items, modifiers, and special requests

### Purchase/Signup Process
- [ ] Sign contract with Toast
- [ ] Provide restaurant details (EIN, owner info, banking)
- [ ] Choose hardware configuration
- [ ] Schedule installation date
- [ ] Arrange for internet install/upgrade if needed

### Hardware Setup
- [ ] Receive and unbox hardware
- [ ] Install terminals at checkout/bar
- [ ] Mount KDS in kitchen (visible to all stations)
- [ ] Connect printers and cash drawer
- [ ] Test internet connectivity for all devices
- [ ] Charge handheld devices

### Software Configuration
- [ ] Complete menu setup (items, modifiers, prices)
- [ ] Design floor plan matching restaurant layout
- [ ] Configure kitchen routing to stations
- [ ] Create staff accounts with PINs
- [ ] Set up payment processing and tip prompts
- [ ] Configure tax rates
- [ ] Test complete order flow (order → kitchen → payment)

### Staff Training
- [ ] Train managers first (4-6 hours)
- [ ] Schedule server training sessions (2 hours each, small groups)
- [ ] Train kitchen staff on KDS (1 hour)
- [ ] Provide quick reference guides
- [ ] Run mock service (practice with fake orders)

### Go-Live Checklist
- [ ] Run parallel with old system for 3-7 days
- [ ] Compare end-of-day totals (Toast vs old POS)
- [ ] Verify accounting export works
- [ ] Confirm all staff comfortable with system
- [ ] Have Toast support contact ready
- [ ] Go live during slower shift if possible (not Friday/Saturday night)
- [ ] Decommission old POS after 1 week of successful operation

---

## Success Metrics

### How to Measure POS ROI

**Operational Efficiency:**
- **Order accuracy:** Track voids/comps due to errors (should decrease)
- **Table turn time:** Measure average table turn (should improve with efficiency)
- **Kitchen ticket time:** Average time from order to ready (KDS should improve)
- **Staff productivity:** Sales per labor hour (should increase)

**Financial Performance:**
- **Food cost %:** Track with Toast's recipe costing (target: 28-35%)
- **Labor cost %:** Monitor with Toast reporting (target: 25-35%)
- **Processing costs:** Compare to previous processor (should be competitive)
- **Revenue growth:** Multi-channel (dine-in + online ordering)

**Customer Experience:**
- **Order errors:** Reduction in wrong orders (KDS eliminates illegible tickets)
- **Bill splitting:** Faster guest checkout (split bills easier)
- **Online orders:** Revenue from commission-free online ordering
- **Customer data:** Build email list for marketing

### Key Performance Indicators (KPIs)

**Weekly:**
- Sales by day of week
- Average check size
- Labor cost as % of sales
- Food cost as % of sales (if tracking inventory)

**Monthly:**
- Total revenue vs plan
- Revenue by channel (dine-in, online, delivery)
- Top-selling menu items
- Server performance (sales per server)
- Customer count and average frequency

**Quarterly:**
- Year-over-year revenue growth
- Menu performance (add/remove items)
- Staffing levels optimization
- Technology ROI (has POS paid for itself in efficiency?)

### Optimization Tips

**First 30 Days:**
- Run daily reports to understand sales patterns
- Identify and 86 underperforming menu items
- Optimize kitchen routing based on ticket times
- Adjust tip prompts if needed

**First 90 Days:**
- Implement online ordering if not already live
- Set up loyalty program or email marketing
- Integrate accounting software if not done
- Review and optimize menu pricing

**First Year:**
- Analyze full year sales data for seasonality
- Adjust staffing based on labor cost %
- Optimize menu mix (remove low-margin items)
- Expand to additional revenue channels (catering, events)

---

## Next Steps

1. **Request Toast demo:** Visit pos.toasttab.com or call sales
2. **Calculate your costs:** Use your expected revenue to estimate processing fees
3. **Visit Toast restaurant:** Ask to see the system in action during service
4. **Review alternatives:** Read TouchBistro and Lightspeed Restaurant profiles if interested
5. **Verify contract terms:** Ensure you're comfortable with 24-month commitment
6. **Plan implementation:** Schedule go-live during slower period, allow 4 weeks
7. **Train staff:** Invest time in proper training for smooth transition

---

**For detailed Toast feature breakdown, see S2-Comprehensive/provider-toast.md**
**For Toast vs competitors comparison, see S2-Comprehensive/feature-comparison.md**
**For long-term considerations, see S4-Strategic**

---

**Last Updated:** October 20, 2025
**Category:** 3.005 Point of Sale Systems
**MPSE Level:** S3-Need-Driven
**Use Case:** Full-Service Restaurant (Table Service)
