# Conversion Tracking: Hotel Scan → Business Visit

**The Problem:** We know guests scan at hotels and click on recommendations—but do they actually visit the business?

**The Solution:** Tent cards at businesses with "Check-in QR" codes = physical foot traffic attribution

---

## The Full Tracking Loop

### Step 1: Guest Scans at Hotel (Awareness)

```
Guest checks into Hotel A
→ Receives laminated sheet
→ Scans QR code for "Dinner recommendations"
→ Sees Giuseppe's Ristorante
→ Clicks to view details

System tracks:
• Guest ID: anonymous token (e.g., g7x3k9)
• Timestamp: 6:15 PM
• Action: Viewed Giuseppe's
• Source: Hotel A, Card A♥
```

---

### Step 2: Guest Goes to Giuseppe's (Intent)

**Guest walks to Giuseppe's (6:45 PM)**

Giuseppe's has tent card on table:

```
┌─────────────────────────────┐
│                             │
│  Thanks for visiting!       │
│                             │
│  Recommended by:            │
│  [Hotel logos]              │
│                             │
│  Scan to discover more      │
│  local favorites:           │
│                             │
│     [QR Code]               │
│                             │
│  [Giuseppe's logo]          │
│                             │
└─────────────────────────────┘
```

---

### Step 3: Guest Scans at Business (Conversion)

```
Guest scans tent card QR at Giuseppe's

System tracks:
• Same guest ID: g7x3k9 (via browser cookie/session)
• Timestamp: 6:52 PM
• Location: Giuseppe's
• Action: Scanned check-in QR

System connects the dots:
6:15 PM: Guest viewed Giuseppe's at Hotel A
6:52 PM: Same guest scanned at Giuseppe's
= CONVERSION CONFIRMED (37 minutes from view → visit)
```

---

### Step 4: Guest Sees "More Recommendations"

**After scanning at Giuseppe's:**

```
┌─────────────────────────────────────────────────────┐
│ Thanks for visiting Giuseppe's! 🍝                  │
│                                                     │
│ You were recommended by: Hotel A                    │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ While you're in the neighborhood, check out:        │
│                                                     │
│ ☕ Espresso Vivace (2 blocks away)                  │
│    "Best cappuccino in Seattle"                     │
│    [View details]                                   │
│                                                     │
│ 🍸 Canon Whiskey Bar (next door)                   │
│    "200+ whiskeys, craft cocktails"                 │
│    [View details]                                   │
│                                                     │
│ 🛍️ Pike Place Market (5 min walk)                  │
│    "Fresh produce, local crafts"                    │
│    [View details]                                   │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ Enjoying your trip? Rate this recommendation:       │
│ ⭐⭐⭐⭐⭐ [Optional feedback]                        │
└─────────────────────────────────────────────────────┘
```

**Result:**
- Guest discovers 3 more places
- Extends their neighborhood exploration
- You track multi-hop behavior (hotel → restaurant → coffee → bar)

---

## What You Can Track (Without Guest Login)

### Anonymous Tracking (Cookie/Session-Based)

**No PII required:**
```
Guest session: g7x3k9
Browser: Safari iOS
Session start: 6:15 PM

Actions:
• 6:15 PM: Scanned at Hotel A
• 6:18 PM: Viewed Giuseppe's (Dinner)
• 6:20 PM: Viewed Espresso Vivace (Coffee)
• 6:25 PM: Viewed Canon (Drinks)
• 6:52 PM: Scanned at Giuseppe's ← CONVERSION
• 8:15 PM: Scanned at Canon ← 2nd CONVERSION
```

**What you learn:**
- Guest viewed 3 places, visited 2 (67% conversion rate)
- Time lag: 37 minutes from view → visit (Giuseppe's)
- Multi-hop: Dinner → Drinks (cross-category behavior)

---

## Key Metrics You Can Now Track

### 1. Scan → Visit Conversion Rate

**By Recommendation:**
```
Giuseppe's Ristorante:
• 450 views (guests clicked to see details at hotel)
• 180 check-ins (guests scanned tent card at restaurant)
• Conversion rate: 40%

Espresso Vivace:
• 380 views
• 95 check-ins
• Conversion rate: 25%

Insight: Dinner recommendations convert 2x better than coffee
```

---

### 2. Time-to-Visit

**How long from view → visit?**
```
Dinner:
• Average: 45 minutes (guest scans at hotel 6pm, arrives at restaurant 6:45pm)
• Mode: 30-60 minutes (peak dinner time)

Coffee:
• Average: 12 hours (guest scans at hotel 8pm, visits coffee shop 8am next day)
• Mode: Morning after arrival

Insight: Guests act on dinner recommendations immediately, coffee recommendations next morning
```

---

### 3. Multi-Hop Behavior

**Do guests visit multiple places in one trip?**
```
Single visit: 55% of guests
- Scanned at hotel → Visited 1 place → Done

Two visits: 30% of guests
- Scanned at hotel → Visited restaurant → Visited bar
- Average time between: 90 minutes

Three+ visits: 15% of guests
- Scanned at hotel → Coffee → Lunch → Attraction → Dinner
- Power users (exploring neighborhood)

Insight: 45% of guests visit multiple places = cross-promotion works
```

---

### 4. Hotel Attribution

**Which hotels drive most foot traffic?**
```
Hotel A (40 rooms):
• 360 guests/month
• 216 scans (60% scan rate)
• 87 business check-ins (40% conversion)

Hotel B (30 rooms):
• 270 guests/month
• 162 scans (60% scan rate)
• 32 business check-ins (20% conversion)

Insight: Hotel A drives 3x more conversions (better recommendations? Better guest profile?)
```

---

### 5. Geographic Clustering

**Do guests stay in neighborhood?**
```
Hotel A → Giuseppe's (0.3 mi away):
• 180 visits (high)

Hotel A → Restaurant across town (2.5 mi away):
• 12 visits (low)

Insight: Guests prefer walkable recommendations (<0.5 mi from hotel)
→ Optimize recommendations by distance
```

---

## The Value of This Data

### For You (mztape):

**1. Proof of ROI for Hotel Sales**
```
Sales pitch to Hotel B:
"Hotel A uses mztape. Here's what happened:
• 87 guests visited recommended businesses last month
• 40% conversion rate (scan → visit)
• Average 1.6 places visited per guest

Your guests want local recommendations. We have the data to prove it works."
```

---

**2. Optimize Recommendations Algorithm**
```
Machine learning input:
• Giuseppe's: 40% conversion (feature more prominently)
• Low-conversion restaurant: 8% conversion (investigate why)
  - Too far? (Check distance)
  - Wrong price point? (Check guest demographics)
  - Misleading description? (Update copy)

Result: Improve recommendations over time (data-driven curation)
```

---

**3. Prove Value for Fundraising**
```
Pitch to investors:
"We're not just a QR code generator. We're foot traffic attribution for local businesses.

Proof:
• 87 confirmed visits last month (scan → business check-in)
• 40% conversion rate (4x higher than digital ad click-through)
• 1.6 places visited per guest (network effect)

TAM: 15,000 boutique hotels × $948 LTV = $14.2M ARR opportunity"
```

---

### For Hotels:

**1. See What's Working**
```
Hotel admin dashboard:
"Your Top Recommendations (Last 30 Days):
1. Giuseppe's - 180 views, 72 visits (40% conversion) ⭐
2. Espresso Vivace - 95 views, 24 visits (25% conversion)
3. Pike Place Market - 89 views, 15 visits (17% conversion)

Insight: Giuseppe's is a hit! Consider featuring it on A♥ card."
```

---

**2. Prove Value to Guests**
```
Hotel marketing:
"Our local recommendations aren't just suggestions—87% of our guests
 visit at least one spot we recommend. We know the neighborhood."

→ Differentiation from chain hotels (Marriott can't prove this)
```

---

### For Businesses:

**1. Attribution (Which Hotels Drive Traffic)**
```
Giuseppe's owner dashboard:
"Customers from Hotel Recommendations (Last 30 Days):
• Hotel A: 72 visits
• Hotel B: 18 visits
• Hotel C: 12 visits

Total: 102 visits from hotels (vs 450 total customers = 23% of traffic)

Insight: Hotels drive 1 in 4 customers!"
```

---

**2. Monetization Opportunity**
```
Giuseppe's owner thinks:
"Hotels send me 100+ customers/month. Should I pay for premium placement?
 Or give Hotel A a commission/referral fee?"

→ Opens door to business-side monetization
```

---

## Technical Implementation

### How to Track Anonymous Sessions (No Login)

**Option 1: Browser Session/Cookie (Simple)**
```
When guest first scans at hotel:
1. Generate unique token: g7x3k9
2. Store in browser cookie (expires in 7 days)
3. Every subsequent scan includes token in URL

Example:
• Hotel scan: mztape.com/c/a3k9f2?session=g7x3k9
• Business scan: mztape.com/b/giuseppe?session=g7x3k9

System matches: Same session = conversion tracked
```

**Pros:**
- No login required
- Works on any browser
- Privacy-friendly (no PII stored)

**Cons:**
- If guest clears cookies → Can't track
- If different person scans tent card → False positive
- Cross-device tracking doesn't work (scan on hotel, different phone at business)

---

**Option 2: Token-in-URL (More Reliable)**
```
When guest first scans at hotel:
1. Generate unique token: g7x3k9
2. Include token in ALL subsequent links

Example:
Hotel scan → Recommendation page for Giuseppe's:
• URL: mztape.com/giuseppe?t=g7x3k9
• "Get Directions" button: maps.google.com?q=giuseppe&ref=g7x3k9
• If guest scans tent card at Giuseppe's: mztape.com/b/giuseppe?checkin=g7x3k9

System matches: Same token = conversion tracked
```

**Pros:**
- Works even if cookies disabled
- Survives browser restarts
- Token visible in URL (transparency)

**Cons:**
- Long URLs (ugly, but functional)
- Guest can't easily share URL (token embedded)

---

**Option 3: Probabilistic Matching (Advanced)**
```
No explicit token—match based on behavior patterns:

Hotel scan (6:15 PM):
• Device fingerprint: Safari iOS, 390×844 screen, San Francisco timezone
• Actions: Viewed Giuseppe's, Espresso Vivace, Canon

Business scan (6:52 PM):
• Same device fingerprint
• Location: Giuseppe's (matches viewed recommendation)
• Time gap: 37 minutes (reasonable walk time)

→ 85% confidence = same guest (probabilistic match)
```

**Pros:**
- No cookies, no tokens (privacy-friendly)
- Can't be circumvented

**Cons:**
- False positives (different guests with similar devices)
- Complex to implement

**Recommendation: Start with Option 1 (cookies), add Option 2 (tokens) if needed**

---

## Tent Card Design for Businesses

### Card Front (On Table)

```
┌─────────────────────────────┐
│                             │
│   Thanks for visiting       │
│   Giuseppe's! 🍝            │
│                             │
│   Recommended by:           │
│   [Hotel A logo]            │
│   [Hotel B logo]            │
│   [Hotel C logo]            │
│                             │
│   Scan to discover more     │
│   local favorites:          │
│                             │
│       [QR Code]             │
│       (Large, 2" × 2")      │
│                             │
│   mztape.com/giuseppe       │
│                             │
└─────────────────────────────┘
```

---

### Card Back (Optional)

```
┌─────────────────────────────┐
│                             │
│  Explore the neighborhood:  │
│                             │
│  ☕ Espresso Vivace          │
│     (2 blocks north)        │
│                             │
│  🍸 Canon Whiskey Bar       │
│     (next door)             │
│                             │
│  🛍️ Pike Place Market       │
│     (5 min walk)            │
│                             │
│  Scan front for full map    │
│                             │
└─────────────────────────────┘
```

---

## Pitch to Businesses

### "Why Should We Participate?"

**Hotel to Giuseppe's owner:**
```
"We want to feature you on our guest recommendation sheet.
 360 guests/month will see your restaurant.

 To track how many guests actually visit, we'll give you this
 tent card for your tables. When guests scan it, we both see
 the data:
 • You see: 'Hotel A sent you 72 customers last month'
 • We see: '40% of guests who clicked on Giuseppe's visited'

 Plus, guests who scan discover OTHER local spots—so you're
 helping the neighborhood (and looking like a good community partner)."
```

---

### "What If We Don't Want to Track?"

**Hotel to business:**
```
"No problem—you don't have to use the tent card. We'll still
 recommend you to our guests.

 But you won't know how many customers we're sending you.
 And we can't prove ROI (so we may recommend competitors instead)."
```

**Gentle pressure:** Most businesses will want the data.

---

## Revenue Opportunities from Conversion Data

### 1. Charge Hotels More for "Conversion Analytics"

**Pricing tiers:**

**Basic ($39/month):**
- Laminated sheet template
- Track scans at hotel
- Basic analytics (view counts)

**Professional ($129/month):**
- 52-card deck + customization
- **Conversion tracking** (see which guests visited businesses)
- Advanced analytics (conversion rate, time-to-visit, multi-hop)

**Upsell:** "Want to see which recommendations actually drive foot traffic? Upgrade to Professional."

---

### 2. Charge Businesses for Premium Placement

**Business monetization:**

**Free tier:**
- Businesses listed in hotel recommendations
- No tent card (no tracking)

**Basic ($25/month per business):**
- Tent card provided (track conversions)
- Dashboard: See which hotels send traffic

**Premium ($99/month per business):**
- Featured placement on hotel sheets (top 3)
- Priority in recommendations (shown first)
- Analytics: Guest demographics, peak times, average spend

**Example:**
```
Giuseppe's pays $99/month for premium
→ Gets featured on 10 hotel sheets (top 3 placement)
→ 10 hotels × 360 guests = 3,600 impressions/month
→ 40% conversion = 1,440 visits/month
→ Avg spend $30 = $43,200/month revenue from hotel referrals
→ ROI: $43,200 / $99 = 437x
```

---

### 3. Commission Model (Like DoorDash)

**Alternative to subscription:**
```
Business pays commission per confirmed visit:
• $1-3 per visit (confirmed via tent card scan)
• No upfront cost
• Pay only for results

Example:
• Giuseppe's: 180 visits/month × $2 = $360/month
• vs flat $99/month → Hotels prefer variable cost
```

**Pros:**
- Businesses only pay for results
- Easy to justify ROI

**Cons:**
- Variable revenue (harder to forecast)
- Requires robust conversion tracking

---

## Data Privacy Considerations

### What Data Do You Collect?

**Anonymous (No PII):**
```
✅ Session token (e.g., g7x3k9)
✅ Timestamp of scans
✅ Which businesses viewed/visited
✅ Device type (iOS, Android)
✅ Geographic location (city-level, not GPS)
✅ Time spent on pages
```

**Not Collected:**
```
❌ Guest name
❌ Email address
❌ Phone number
❌ Credit card info
❌ Precise GPS location
```

---

### GDPR/Privacy Compliance

**Key principle: Anonymous tracking (like Google Analytics)**

**User consent:**
```
When guest first scans:
"We use cookies to improve recommendations. [Learn more] [Accept]"

Privacy policy:
"We track which recommendations you view and visit (anonymously)
 to improve our service. No personal information is collected."
```

**Data retention:**
```
Session data: Deleted after 30 days
Aggregate data: Kept indefinitely (anonymous stats like "40% conversion rate")
```

---

## Summary: The Missing Piece

### Before (Hotel Tracking Only):

```
Hotel knows:
✅ Guest scanned card
✅ Guest clicked on Giuseppe's
❌ Did guest visit? (Unknown)

Result: Can't prove ROI
```

---

### After (Conversion Tracking with Tent Cards):

```
Hotel knows:
✅ Guest scanned card
✅ Guest clicked on Giuseppe's
✅ Guest visited Giuseppe's (confirmed via tent card scan)
✅ Time lag: 37 minutes
✅ Multi-hop: Also visited Canon later

Result: Provable ROI ("40% of guests visit recommended businesses")
```

---

### The Value:

**For you (mztape):**
- Proof of concept for investors
- Data-driven recommendation optimization
- New revenue stream (charge businesses for placement)

**For hotels:**
- See what's working (Giuseppe's = 40% conversion, feature it more)
- Prove value to guests ("87% of our guests visit our recommendations")

**For businesses:**
- Attribution (Hotel A sends 72 customers/month)
- Justify paying for premium placement (ROI = 437x)

---

### The Tent Card Strategy:

**Not just amplification—it's conversion tracking.**

**Cost:**
- $3 per tent card
- 50 businesses × $3 = $150

**Value:**
- Track 180+ conversions/month
- Prove 40% scan→visit rate
- Unlock business-side monetization ($25-99/month per business)

**ROI:** $150 one-time → $1,250-4,950/month revenue (8-33x per month)

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Purpose:** Define conversion tracking strategy using tent cards at businesses
**Key Insight:** Tent cards aren't just for amplification—they close the attribution loop (hotel scan → business visit = provable ROI)
