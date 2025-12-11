# Boutique Hotel Recommendations: Fractional CTO Advice

**Scenario:** Hotel GM comes to fractional CTO with request for guest recommendation system

---

## The Conversation

**GM:** "We're spending hours every day creating personalized recommendations for guests. We print Google Maps directions, handwrite notes on hotel stationery, it's inconsistent, and we have no idea if guests actually use them. Can we build something?"

**Fractional CTO:** "Hold on - before we talk about building anything, let's see if you can **buy** something off-the-shelf. Building custom software is expensive and time-consuming. Rule #1: If you can buy it, buy it."

---

## Level 0: Buy Off-the-Shelf Software ✅ CHECK FIRST

**CTO:** "Let me check if software already exists for this..."

**[Searches for 5 minutes]**

**CTO:** "Okay, I found a few options:

### Option 1: QRCards (mztape™) - Vertical SaaS
- **What it is:** Purpose-built platform for hospitality recommendations via QR codes
- **Features:** Staff creates guest cards (3-5 min), QR code printed, guest scans → sees recommendations + map
- **Pricing:** Probably $100-200/month (need to get quote)
- **Setup:** 1-2 weeks
- **Pros:** Purpose-built for hotels, turnkey, no maintenance
- **Cons:** Monthly cost, platform dependency

### Option 2: TouchStay - Competitor
- **What it is:** Digital guidebooks for vacation rentals/hotels
- **Features:** Static guidebook (same for all guests), QR code access
- **Pricing:** $20-100/month
- **Pros:** Established, cheaper
- **Cons:** Static (not personalized per guest), vacation rental focus

### Option 3: GuestJoy - Competitor
- **What it is:** Guest messaging + upsell platform
- **Features:** SMS-based recommendations, no printed cards
- **Pricing:** $99-299/month
- **Pros:** Full guest communication platform
- **Cons:** No printed cards, expensive, SMS-only

**My recommendation: Try QRCards first.**

**Why:**
1. **Matches your use case exactly:** Personalized cards, QR codes, staff workflow optimized for hotels
2. **Fast deployment:** 1-2 weeks vs 6-12 weeks if we build custom
3. **No maintenance burden:** They handle updates, hosting, security
4. **Cost-effective:** $100-200/month vs $6,000 to build + ongoing maintenance

**Next step: Sign up for free trial, test it for 2 weeks. If it works, buy it. Done."**

---

## But What About... (Common Objections)

### Objection 1: "We need it to integrate with our PMS (Property Management System)"

**CTO:** "Good point. Does QRCards integrate with your PMS?"

**[Checks QRCards features]**

**CTO:** "Looks like PMS integration is on their roadmap but not available yet. Here's what we can do:

**Option A: Manual entry (for now)**
- Staff enters guest name when creating card (30 seconds)
- When QRCards adds PMS integration (Q2 2026), you upgrade
- **Trade-off:** 30 seconds manual work vs waiting 6 months to build custom

**Option B: Middleware integration**
- If QRCards has an API, we can build a small connector ($2,000-3,000 one-time)
- Connector pulls guest data from your PMS → Creates QRCards automatically
- **Trade-off:** Upfront cost, but saves staff time long-term

**Option C: Wait for QRCards to build it**
- Ask QRCards when PMS integration is coming
- If it's 3-6 months, wait
- If it's 12+ months, consider custom build

**My recommendation: Start with Option A (manual entry). It's only 30 seconds per guest. If it becomes a bottleneck after 3 months, we build Option B (middleware). Don't block on this - the core value is there even without PMS integration."**

---

### Objection 2: "What if we want to customize the workflow?"

**CTO:** "What specific customization do you need?"

**GM:** "We want to add a field for guest dietary restrictions, and automatically filter recommendations based on that."

**CTO:** "Let me check if QRCards supports that..."

**[Checks QRCards features]**

**CTO:** "Doesn't look like custom fields are available out-of-box. Here's your decision:

**Option A: Ask QRCards to add it**
- Submit feature request
- If they add it in 1-3 months, you get the feature + ongoing updates
- **Trade-off:** Wait time, depends on their roadmap

**Option B: Workaround within QRCards**
- Staff manually filters recommendations when creating card
- Use recommendation tags: 'vegetarian', 'gluten-free', etc.
- **Trade-off:** Not fully automated, but still saves time vs current manual process

**Option C: Build custom solution**
- Build exactly what you want ($6,000-10,000)
- You own it, full control
- **Trade-off:** Upfront cost, ongoing maintenance, no automatic updates

**My recommendation: Try Option B (workaround). If dietary restrictions are critical and QRCards won't add it, we can build custom. But don't build custom until you've validated that the workaround doesn't work. Most of the time, the workaround is good enough."**

---

### Objection 3: "What if QRCards goes out of business?"

**CTO:** "Valid concern. Here's the risk assessment:

**Risk:** QRCards shuts down → You lose access to guest recommendation system

**Mitigation:**
1. **Data export:** Before signing up, confirm QRCards allows data export (recommendation library, guest cards)
2. **Low switching cost:** Creating recommendation cards is quick (3-5 min) - not mission-critical
3. **Fallback plan:** If QRCards disappears, you go back to manual process for 2-4 weeks while we find replacement

**Risk level: Low**
- This isn't your booking system (mission-critical)
- This is a 'nice-to-have' that improves guest experience
- If it disappears, you revert to old process (Excel, Google Maps) - hotel still operates

**My recommendation: Accept the risk. The cost of building custom ($6,000+) to avoid dependency isn't worth it for a non-mission-critical feature. Plus, QRCards can become mission-critical only AFTER you validate it works for your guests."**

---

### Objection 4: "We want to own our data, not give it to a third party."

**CTO:** "What data are we talking about?"

**GM:** "Guest names, which recommendations they received, scan analytics."

**CTO:** "Let's be clear about data sensitivity:

**Not sensitive (okay to share with QRCards):**
- Guest first names (public info, used for personalization)
- Recommendation library (restaurants, attractions - public info)
- Scan counts (anonymous analytics - no PII)

**Sensitive (should NOT share):**
- Guest full names, addresses, credit cards (PII)
- Room numbers, check-in dates (security)
- Guest spending, loyalty points (business-critical)

**QRCards likely only needs:**
- Guest first name (optional, for 'Welcome, Sarah!')
- Recommendations assigned to this guest
- Scan timestamps (anonymous)

**They DON'T need:**
- Full guest profile
- Payment info
- PMS data

**My recommendation: Review QRCards privacy policy. If they only collect first name + scan data, that's fine. If they require full guest profiles, that's a red flag - we negotiate or build custom."**

---

## The "Before" State: Excel Hell

**CTO:** "Let's be honest about what you're doing today:

**Current Process (Manual):**
1. Guest checks in, asks for recommendations
2. Front desk staff opens Excel spreadsheet (or mental list)
3. Staff Googles 3-4 places ('best Italian restaurant near hotel')
4. Staff prints Google Maps directions on printer
5. Staff handwrites note on hotel stationery: 'Try Giuseppe's - great pasta!'
6. Staff hands paper to guest
7. **Time:** 15-30 minutes per guest
8. **Quality:** Inconsistent (depends on which staff member)
9. **Tracking:** Zero (no idea if guest went to Giuseppe's)

**Cost Analysis:**
- 15 guests/day × 20 minutes × 30 days = 150 hours/month
- 150 hours × $20/hour (front desk wage) = **$3,000/month in staff time**

**With QRCards:**
- 15 guests/day × 3 minutes × 30 days = 22.5 hours/month
- 22.5 hours × $20/hour = **$450/month in staff time**
- QRCards cost: ~$150/month
- **Net savings:** $3,000 - $450 - $150 = **$2,400/month**

**ROI:**
- Cost: $150/month
- Savings: $2,400/month
- **ROI: 16x** (pays for itself 16 times over)

**My recommendation: This is a no-brainer. Buy QRCards. Even if it only saves 10 hours/month, it pays for itself."**

---

## Integration with Property Management System

**CTO:** "Let's talk about PMS integration. Your PMS (Opera, Mews, Cloudbeds, etc.) has:

**Guest data PMS stores:**
- Guest name, email, phone
- Check-in / check-out dates
- Room number, rate, booking source
- Guest preferences (if manually entered)
- Payment info, loyalty points

**What QRCards needs from PMS:**
- Guest name (for personalization)
- Check-in date (to create card at check-in)
- Check-out date (to auto-archive card after stay)

**Integration Options:**

### Option 1: No Integration (Manual Entry)
- **Process:** Staff enters guest name when creating QRCards
- **Time:** 30 seconds per guest
- **Pros:** Zero integration cost, works immediately
- **Cons:** Manual work (30 sec per guest = 7.5 hours/month for 15 guests/day)

### Option 2: QRCards Native PMS Integration (Future)
- **Process:** QRCards builds integration with top 5 PMSs (Opera, Mews, Cloudbeds, etc.)
- **Time:** Available Q2 2026 (hypothetical - ask QRCards for timeline)
- **Pros:** Automatic, zero manual work
- **Cons:** Wait time, depends on QRCards roadmap

### Option 3: Custom Middleware (DIY Integration)
- **Process:** Build API connector between your PMS and QRCards
- **Cost:** $2,000-3,000 one-time (20-30 hours development)
- **Process flow:**
  1. Guest checks in → PMS creates guest record
  2. Middleware listens for new guest → Calls QRCards API
  3. QRCards creates card automatically → Prints at front desk
- **Pros:** Fully automated, custom logic (e.g., assign recommendations based on booking source)
- **Cons:** Upfront cost, requires developer, maintenance burden

### Option 4: Zapier/Make.com (No-Code Integration)
- **Process:** Use no-code automation to connect PMS → QRCards
- **Cost:** $20-50/month (Zapier/Make subscription)
- **Process flow:**
  1. PMS webhooks new guest → Zapier catches it
  2. Zapier calls QRCards API → Creates card
- **Pros:** No developer needed, cheap
- **Cons:** Requires QRCards API + PMS webhooks (may not exist)

**My recommendation:**

**Phase 1 (Week 1-3 months):** Manual entry (Option 1)
- Start with manual workflow, validate QRCards works for your guests
- 30 seconds per guest is acceptable for first 100 guests

**Phase 2 (Month 4-6):** Evaluate integration need
- If manual entry becomes painful (>15 min/day), consider integration
- Check if QRCards added PMS integration (Option 2) - use that if available
- If not, build middleware (Option 3) or Zapier (Option 4)

**Don't block on PMS integration. The core value is there even without it."**

---

## Excel/Spreadsheet Management

**CTO:** "You mentioned you're using Excel today. Let's talk about how QRCards replaces that:

**Current Excel Usage:**
- **Sheet 1: Recommendation Library**
  - Columns: Name, Address, Phone, Category, Notes
  - Rows: 20-50 local restaurants, attractions, activities
  - **Problem:** Hard to search/filter, no images, no maps

- **Sheet 2: Guest Recommendations (maybe?)**
  - Columns: Guest Name, Room, Check-in, Recommendations Given
  - **Problem:** Manual entry, no tracking if guest used recommendations

**With QRCards:**
- **Replaces Sheet 1:** Recommendation library in QRCards admin
  - Add restaurant → Upload photo, description, address (auto-completes with maps)
  - Tag with categories (Italian, Seafood, Family-friendly, etc.)
  - Easy search/filter when creating guest cards

- **Replaces Sheet 2:** QRCards tracks which guests got which recommendations
  - Dashboard shows: 50 cards created, 180 scans, Giuseppe's recommended 45 times
  - Analytics replace manual tracking

**Migration Plan:**

**Step 1: Export Excel Recommendation Library**
- Export Excel → CSV (Name, Address, Category, Notes)

**Step 2: Bulk Import to QRCards**
- Upload CSV → QRCards creates recommendation library
- Add photos manually (10-15 minutes per place)
- **Time:** 2-4 hours one-time setup

**Step 3: Retire Excel, Use QRCards Going Forward**
- Staff stops updating Excel
- All new recommendations added to QRCards
- Old Excel becomes archive (read-only)

**Time to migrate: 4-8 hours** (mostly adding photos to recommendations)"**

---

## Final CTO Recommendation

**CTO:** "Here's my advice:

### Week 1: Trial QRCards
1. Sign up for free trial (or request demo)
2. Import your recommendation library (Excel → QRCards)
3. Create 5 test guest cards
4. Have staff test workflow (front desk creates card in 3-5 min)
5. Test guest experience (scan QR, view on phone)
6. **Decision point:** Does it work? Does staff like it? Do guests use it?

### Week 2-4: Pilot Launch
1. If trial successful → Subscribe to QRCards ($100-200/month)
2. Train all front desk staff (1 hour training)
3. Start creating cards for 50% of guests (test group)
4. Track: How many scans? Any issues? Staff feedback?

### Month 2-3: Full Rollout
1. If pilot successful → Create cards for 100% of guests
2. Gather guest feedback (checkout survey: 'Did you use the recommendation card?')
3. Optimize recommendation library (remove unpopular places, add new ones)

### Month 4-6: Evaluate Integration Need
1. Track staff time: Is manual entry (30 sec per guest) a bottleneck?
2. If yes → Build PMS integration ($2,000-3,000)
3. If no → Keep manual entry, re-evaluate every 6 months

**Total Cost Year 1:**
- QRCards: $1,200-2,400/year (subscription)
- Setup: 8 hours staff time (migrate Excel, train team)
- Integration (optional): $2,000-3,000 if needed
- **Total: $1,200-5,400**

**Savings Year 1:**
- Staff time: 127.5 hours/month saved × 12 months = 1,530 hours
- 1,530 hours × $20/hour = **$30,600 saved**

**Net benefit: $25,200-29,400 Year 1** 🎉

**Build custom only if:**
- QRCards trial fails (doesn't work for your workflow)
- Missing critical feature QRCards won't add (e.g., dietary restriction filtering)
- QRCards pricing >$300/month (too expensive)

**Otherwise: Buy QRCards. Don't build."**

---

## Summary: Fractional CTO Decision Framework

```
GM Request: "We need a guest recommendation system"
         ↓
CTO: "Can we BUY off-the-shelf software?" (Level 0)
         ↓
    Search for solutions...
         ↓
    ┌────────────────────────┐
    │ Found: QRCards         │
    │ (Vertical SaaS)        │
    │ $100-200/month         │
    │ 1-2 weeks setup        │
    └────────────────────────┘
         ↓
    Trial for 2 weeks
         ↓
    ┌─────────────┬─────────────┐
    │ Works? ✅   │ Doesn't? ❌ │
    └─────────────┴─────────────┘
         ↓                  ↓
    BUY IT!        Identify gap:
    Done.          - Too expensive? → Try TouchStay ($20/mo)
                   - Missing feature? → Ask QRCards to add it
                   - Major gap? → Build custom (Level 2/3)
```

**Key principle: Exhaust Level 0 (buy) before considering Level 1+ (build)**

**Why:**
- Level 0 (buy): $1,200-2,400/year, 1-2 weeks, zero maintenance
- Level 2 (build): $6,000 one-time + maintenance, 4-6 weeks, ongoing burden

**Building is 3-5x more expensive and 3x slower than buying.**

**Only build when buying doesn't work.**

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Perspective:** Fractional CTO advising hotel GM
**Key Message:** "If you can buy it, buy it. QRCards exists - try it before building anything."
