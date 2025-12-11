# Guest Review Loop: Accumulated Guest Knowledge Model

## Executive Summary

**Current State:**

**Hard Recs (Concierge-arranged):**
- Concierge makes reservation, has restaurant relationship
- Tight feedback loop: concierge hears "How was dinner?" at checkout
- Works well, but doesn't scale (limited to front desk hours)

**Soft Recs (Handouts, verbal suggestions):**
- "Here are some spots near the Space Needle you might try"
- NO feedback loop: hotel never learns what worked
- Recommendations stagnate (same photocopied list for years)

**QR Cards Innovation:**

**Brings feedback loop to soft recs (MVP):**
- Guest scans QR card → sees recommendations + aggregate trust signal (❤️ "Loved by X guests")
- Mid-stay: "What were your favorite meals?" → staff captures 20-second note with internal 1-5 rating
- If 4-5 stars → ❤️ love count increments for that business
- Next guest sees: "Giuseppe's – ❤️ loved by 13 guests" (aggregate count only, no individual reviews)
- Hotel learns what works (internal ratings), removes spots getting negative feedback
- Recommendations improve over time (data-driven, privacy-first)
- **Every guest becomes a secret shopper** (unpaid quality control)
- **Scales without concierge effort** (system captures knowledge, shared across team)

**Result:** Soft recs become data-driven and self-improving, filling the gap between "expensive concierge service" and "stale photocopied handout."

**V2 Features (not in MVP):** ⭐ Save buttons, personalization, guest-initiated QR sharing

---

## Table of Contents

1. [The Core Concept](#the-core-concept)
2. [Old Model vs New Model](#old-model-vs-new-model)
3. [How It Works](#how-it-works)
   - [Step 1: Guest Receives Card](#step-1-guest-receives-card)
   - [Step 2: Guest Sees Recommendations + Aggregate Favorites](#step-2-guest-sees-recommendations--aggregate-favorites)
   - [Step 3: Guest Visits Restaurant](#step-3-guest-visits-restaurant)
   - [Step 4A: Staff Captures Guest Feedback (Mid-Stay)](#step-4a-staff-captures-guest-feedback-primary-method)
   - [Step 4B: Guest Submits Feedback Online (Optional)](#step-4b-guest-submits-review-online-secondary-method--more-detail)
   - [Step 5: Hotel Reviews and Curates](#step-5-review-goes-to-hotel-for-approval-optional)
   - [Step 6: Aggregate Favorites Shown to Future Guests](#step-6-favorites-accumulate-on-card)
   - [Step 7: Hotel Learns and Iterates](#step-7-hotel-learns-and-iterates)
4. [Privacy & Opt-In Design](#guest-swipefilter-feature-private-to-guest)
5. [Card-Specific Review Visibility](#card-specific-review-visibility)
6. [Proof of Visit](#proof-of-visit-photos-essays-photoessays)
7. [Incentive Structure](#incentive-structure-why-guests-review)
8. [Hotel Value Proposition](#hotel-value-prop-accumulated-guest-knowledge)
9. [Async Micro-Community](#async-micro-community-the-3-guests)
10. [Living Guest Book](#living-guest-book-every-guest-is-a-secret-shopper)
11. [Reputation System](#incentivize-repeat-visits-reputation-system)
12. [Technical Implementation](#technical-implementation)
13. [Tent Cards (Future Product)](#tent-cards-separate-loop-inter-destination-network)
14. [Summary](#summary-why-this-model-is-better)
15. [Next Steps](#next-steps-implement-review-loop)

---

## The Core Concept

**The Pivot:** Instead of tracking hotel → business attribution, create a feedback loop where guest feedback accumulates internally at the hotel level. Hotel uses this data to curate better recommendations. Future guests see aggregate signals ("Favorited by 12 guests"), not individual reviews.

**The Insight:** Close the loop between recommendations and feedback (not recommendations and destinations).

**The Simplification:** Guest doesn't have to do data entry! Hotel staff captures feedback during mid-stay conversation ("What were your favorite meals? Any places we should know about?") and enters gist of response in system. No hard proof needed (not anonymous—hotel knows guest was there). Much lower friction than online review submission.

**Privacy First:** Individual feedback is hotel-only (for curation). Guests never see other guests' individual reviews. Only aggregate counts shown: "Favorited by X guests."

---

## Old Model vs New Model

### Old Model: Static Recommendations (What Hotels Actually Do Today)

**Option 1: Photocopied Handout**
```
Hotel creates list of recommendations
  ↓
Prints 500 copies
  ↓
Hands to guests at check-in
  ↓
Guest visits (maybe?)
  ↓
Hotel has NO IDEA if guest liked it
  ↓
Same list used for years (stagnant, no updates)
```

**Option 2: Concierge Recommendations**
```
Guest asks concierge for dinner recommendation
  ↓
Concierge recommends Giuseppe's (based on gut/relationship)
  ↓
Guest visits
  ↓
Guest returns, tells concierge "It was great!"
  ↓
Feedback captured (in concierge's head only)
  ↓
Doesn't scale (only works during concierge hours, not shared with team)
```

**Problems with Old Model:**
- ❌ No feedback loop (hotel never learns what worked)
- ❌ Recommendations stagnate (same list for years)
- ❌ Doesn't scale (concierge limited to front desk hours)
- ❌ Knowledge siloed (concierge knows, but not captured in system)
- ❌ No data-driven curation (gut feeling, not guest feedback)

---

### New Model: Guest Feedback Loop (Privacy-First)

```
Hotel recommends Giuseppe's on Card 3♥
  ↓
Guest A receives Card 3♥, scans
  ↓
Guest A sees: "Giuseppe's - ❤️ Loved by 8 guests" (aggregate only)
  ↓
Guest A visits Giuseppe's, loves it
  ↓
Mid-stay: Staff asks "Any favorite meals?"
  ↓
Guest A: "Giuseppe's was amazing! The carbonara was incredible."
  ↓
Staff captures feedback (internal): ★★★★★ (5/5) - "Carbonara incredible"
  ↓
Feedback saved to hotel database (NEVER shown to other guests)
  ↓
Aggregate count updates: "Giuseppe's - ❤️ Loved by 9 guests" (was 8, now 9)
  ↓
Guest B receives Card 3♥ next week, scans
  ↓
Guest B sees: "Giuseppe's - ❤️ Loved by 9 guests" (just the count, no details)
  ↓
Guest B visits Giuseppe's (trust signal from aggregate count)
  ↓
Guest B gives feedback: "Giuseppe's was great!" → ❤️ count becomes 10
  ↓
Meanwhile: Java Junction getting negative feedback
  ↓
Hotel dashboard shows:
  - Giuseppe's: 12 mentions, avg 4.7/5, ❤️ loved by 12 → KEEP
  - Java Junction: 5 mentions, avg 2.4/5, ❤️ loved by 1 → REMOVE
  ↓
Hotel updates Card 3♥: Remove Java Junction, add Canon Bar
  ↓
Future guests see improved recommendations (bad spots removed)
```

**Value:**
- ✅ No tracking businesses (loop closes at hotel level)
- ✅ Accumulated guest knowledge (each guest contributes via staff conversation)
- ✅ Hotel learns what works ("Giuseppe's = 4.7/5, Java Junction = 2.4/5")
- ✅ Future guests benefit (see aggregate trust signal: "❤️ Loved by X guests")
- ✅ Privacy-first (individual feedback never shown publicly, only ❤️ count)
- ✅ No cookies needed (feedback captured by staff, not clickstream tracking)
- ✅ Async micro-community (3♥ guests help curate over time, but privately)

---

## How It Works

### Step 1: Guest Receives Card

**Hotel A hands Guest A the 3♥ card (Romantic Dinner):**
```
Card shows:
• Giuseppe's Ristorante
• Lombardi's Trattoria
• Cara Mia

Guest scans QR code
```

---

### Step 2: Guest Sees Recommendations + Aggregate Love Count

**Mobile page (Privacy-first - ONLY aggregate counts shown):**
```
┌─────────────────────────────────────────────────────┐
│ Welcome! Here are your romantic dinner spots:       │
│                                                     │
│ 🍝 Giuseppe's Ristorante ❤️ Loved by 12 guests     │
│ 📍 0.3 mi from hotel                                │
│ Italian • $$ • 0.3 miles                            │
│                                                     │
│ [Get Directions]                                    │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ 🍝 Lombardi's Trattoria ❤️ Loved by 8 guests       │
│ 📍 0.5 mi from hotel                                │
│ Italian • $$ • 0.5 miles                            │
│                                                     │
│ [Get Directions]                                    │
│                                                     │
│ ─────────────────────────────────────────────────   │
│                                                     │
│ 🍝 Cara Mia ❤️ Loved by 4 guests                   │
│ 📍 0.7 mi from hotel                                │
│ Italian • $$$ • 0.7 miles                           │
│                                                     │
│ [Get Directions]                                    │
└─────────────────────────────────────────────────────┘
```

**Key:**
- Guest sees ONLY aggregate counts (❤️ "Loved by X guests")
- Hearts = post-visit positive feedback (guests who went and loved it)
- NO individual guest reviews or comments shown
- Trust signal comes from the number (12 > 8 > 4)
- Hotel can optionally add curated descriptions (not guest quotes)

---

### Step 3: Guest Visits Restaurant

Guest A goes to Giuseppe's, has carbonara, loves it.

---

### Step 4A: Staff Captures Guest Feedback (Primary Method)

**IMPORTANT: Privacy & Opt-In Design**

Two levels of tracking:

**Level 1: Always happens (no consent needed)**
- Aggregate card usage: "3♥ card was scanned 47 times this month"
- Anonymous business views: "Giuseppe's was viewed 23 times from 3♥ scans"
- Staff sees: "Guest in Room 302 used cards: Yes/No"

**Level 2: Individual tracking (requires opt-in)**
- Staff sees specific guest activity: "Alice viewed Giuseppe's at 7:15pm"
- Enables targeted questions: "I see you looked at Giuseppe's - how was it?"
- Guest must explicitly consent

---

**Option A: Guest-initiated sharing (QR code - CLEANEST APPROACH)**

**No opt-in prompt shown** - signals "we don't track by default"

**Guest scans card, sees recommendations:**
```
┌─────────────────────────────────────────────────────┐
│ Welcome! Here are your romantic dinner spots:       │
│                                                     │
│ 🍝 Giuseppe's Ristorante ❤️ Loved by 12 guests     │
│ 📍 0.3 mi • [⭐ Save]                                │
│                                                     │
│ 🍝 Lombardi's Trattoria ❤️ Loved by 8 guests       │
│ 📍 0.5 mi • [⭐ Save]                                │
│                                                     │
│ 🍝 Cara Mia ❤️ Loved by 4 guests                   │
│ 📍 0.7 mi • [⭐ Save]                                │
└─────────────────────────────────────────────────────┘

❤️ Loved by X = Post-visit outcome (guests who went and loved it)
⭐ Save = Pre-visit intent (I want to try this)
```

**Guest taps "⭐ Save" on places they're interested in:**
```
Giuseppe's saved → Appears in "My Saved Places"
Lombardi's skipped
Cara Mia saved → Appears in "My Saved Places"
```

**Guest navigates to "My Saved Places":**
```
┌─────────────────────────────────────────────────────┐
│ My Saved Places                                     │
│                                                     │
│ 🍝 Giuseppe's Ristorante                            │
│ 📍 0.3 mi • [Get Directions] [Remove]               │
│                                                     │
│ 🍝 Cara Mia                                         │
│ 📍 0.7 mi • [Get Directions] [Remove]               │
│                                                     │
│ ──────────────────────────────────────────────      │
│                                                     │
│ Want suggestions? Share your list with the hotel!   │
│                                                     │
│ [Share My Places] ← Generates QR code               │
└─────────────────────────────────────────────────────┘
```

**Guest clicks "Share My Places":**
```
┌─────────────────────────────────────────────────────┐
│ Share Your Saved Places                             │
│                                                     │
│ Show this QR code to hotel staff to get             │
│ personalized suggestions during your stay.          │
│                                                     │
│ Or share it with friends/family!                    │
│                                                     │
│         ┌─────────────────┐                         │
│         │  █▀▀▀▀▀█ ▀ █▀▀  │                         │
│         │  █ ███ █ ▄█ ▀█  │                         │
│         │  █ ▀▀▀ █ █▀ ▄▀  │                         │
│         │  ▀▀▀▀▀▀▀ ▀ ▀ ▀  │                         │
│         │  ▄█▄ █▀ ▀█▀▄█   │                         │
│         │  █▀▀▀▀▀█ ▄█ ▄▀  │                         │
│         └─────────────────┘                         │
│                                                     │
│ This QR code links to your saved places.            │
│ Valid for 7 days.                                   │
│                                                     │
│ [Done]                                              │
└─────────────────────────────────────────────────────┘
```

**Guest shows QR code to hotel staff mid-stay:**
```
Staff scans guest's QR code → Sees guest's saved list:

Staff tablet shows:
┌─────────────────────────────────────────────────────┐
│ Guest's Saved Places (Room 302)                     │
│ • Giuseppe's Ristorante ✓                           │
│ • Cara Mia ✓                                        │
│                                                     │
│ Staff can now ask targeted questions:                │
│ "I see you saved Giuseppe's—did you make it there?" │
└─────────────────────────────────────────────────────┘

Staff: "I see you saved Giuseppe's—did you make it there?"
Guest: "Yes! It was amazing!"
Staff: "Great! Since you liked Giuseppe's, you might also like Canon Bar—
        our guests love it. Want me to add it to your card?"
```

**Why this is best:**
- ✅ **No opt-in prompt** = signals "we don't track you"
- ✅ **Guest-initiated** = 100% explicit consent (they generate the QR code)
- ✅ **Obvious what's being shared** = just their saved list, nothing else
- ✅ **Can share with anyone** = hotel, friends, family (not just hotel-specific)
- ✅ **Time-limited** = QR code expires after 7 days (guest controls duration)
- ✅ **Works for sensitive categories** = guest chooses what to save/share
- ✅ **Enables targeted questions** = if guest wants them
- ✅ **Falls back gracefully** = if guest doesn't share, staff asks general questions

---

**Option B: Private personalization (Swipe/save - No sharing with hotel)**

**Guest can save places for themselves, but never shares with hotel:**

```
Guest scans card, sees recommendations with [♡ Save] buttons
Guest saves places they're interested in
→ Appears in "My Saved Places" (private to guest)
→ Can swipe to refine, get automated suggestions
→ NO "Share My Places" button (guest keeps list private)

Guest's "My Saved Places":
┌─────────────────────────────────────────────────────┐
│ My Saved Places                                     │
│                                                     │
│ 🍝 Giuseppe's Ristorante                            │
│ 📍 0.3 mi • [Get Directions] [Remove]               │
│                                                     │
│ 🍝 Cara Mia                                         │
│ 📍 0.7 mi • [Get Directions] [Remove]               │
│                                                     │
│ (No sharing feature)                                │
└─────────────────────────────────────────────────────┘
```

**What hotel staff sees:**
```
Staff tablet shows:
┌─────────────────────────────────────────────────────┐
│ Guest: Room 302                                     │
│ Card Usage: Used 2 cards during stay                │
│                                                     │
│ [Ask general feedback question]                     │
└─────────────────────────────────────────────────────┘

Staff asks general question:
"How's your stay going? Any favorite meals or spots you've discovered?"

Guest: "Yes! We went to Giuseppe's last night—it was amazing!"

Staff: "Wonderful! I'm so glad to hear that."
→ Enters feedback (no need to know guest saved it on card)
```

**Why this works:**
- ✅ Guest gets personalized experience (saves places, automated suggestions)
- ✅ Complete privacy (hotel never sees saved list, swipes, or clickstream)
- ✅ Still captures feedback (via general mid-stay questions)
- ✅ Works for sensitive categories (guest curates privately)
- ⚠️ Trade-off: Staff can't ask targeted questions (only general)

---

**Option C: No individual features at all (Simplest - RECOMMENDED FOR MVP)**

**Guest sees static list, no saving/swiping features:**

```
Guest scans card → Sees list of recommendations with aggregate love count
No [⭐ Save] buttons, no personalization features
Just: Business name, distance, "❤️ Loved by X guests", directions

Staff tablet shows:
┌─────────────────────────────────────────────────────┐
│ Guest: Room 302                                     │
│ Card Usage: Used 2 cards during stay                │
│                                                     │
│ [Ask general feedback question]                     │
└─────────────────────────────────────────────────────┘

Staff asks general question mid-stay:
"Any favorite meals or spots you've discovered?"

Guest: "Giuseppe's was amazing!"

Staff enters feedback:
→ Giuseppe's: ★★★★★ (5/5 internal rating) - "Amazing"
→ ❤️ Aggregate count updates for future guests (12 → 13)
```

**Why this is best for MVP:**
- ✅ Simplest to build (no save/swipe UI, no personalization engine)
- ✅ Complete privacy (no individual tracking whatsoever)
- ✅ Still captures core value (mid-stay feedback loop)
- ✅ No consent mechanism needed
- ✅ Focus on the key insight: staff conversations scale concierge knowledge
- ⚠️ Trade-off: No personalization features for guest

**What guests see:**
- ❤️ Hearts = "Loved by X guests" (post-visit positive feedback count)
- NO ⭐ save buttons (that's Option A/B - V2 feature)

---

**Recommendation: Start with Option C (simplest), add Option A in V2**

**Rationale:**
1. **Core value is feedback loop** - Staff conversations, not personalization features
2. **Simplest to build** - No save/swipe UI, no QR code generation, no personalization engine
3. **Complete privacy** - No individual tracking whatsoever, no consent needed
4. **General questions work fine** - "Any favorite meals?" captures feedback without tracking
5. **Mid-stay conversations** are the key insight (scale concierge knowledge)
6. **Option A can come later** - Guest-initiated QR sharing is elegant, but not needed for MVP

**What to build for MVP (Option C):**
- Guest scans card → sees static list with aggregate love count ("❤️ Loved by X guests")
- NO ⭐ save buttons, no personalization features
- Mid-stay feedback capture (staff asks general questions, no individual tracking)
- Aggregate card usage stats (hotel sees "3♥ scanned 47 times this month")
- Staff tablet shows: "Room 302 used cards: Yes/No" (binary flag, not clickstream)
- Staff enters feedback → internal 1-5 ⭐ rating → ❤️ count updates if 4-5 stars

**V2 features (add later if needed):**
- **Option A:** ⭐ Save buttons + guest-initiated QR sharing (elegant consent model)
- **Option B:** ⭐ Private save/swipe features (personalization without sharing)

**Why Option A (QR sharing) is brilliant for V2:**
- ⭐ Save button = "I want to try this" (pre-visit intent, private)
- Guest can generate QR code to share their saved list with hotel/friends
- No opt-in prompt = signals "we don't track by default"
- Guest-initiated = 100% explicit consent
- Can share with hotel OR friends/family (not just hotel-specific)
- Falls back gracefully if guest doesn't share

---

### Privacy Levels Summary

**Across all three options:**

| Data | Guest Sees | Hotel Sees | Other Guests See |
|------|-----------|-----------|-----------------|
| ⭐ Saves (intent) | ✅ Private ("My Saved Places") | ❌ Never (unless guest shares QR) | ❌ Never |
| Guest-shared list (Option A) | ✅ Guest generates QR to share | ✅ Only if guest shows QR code | ❌ Never |
| Staff feedback (+/-) | ✅ Guest knows they gave feedback | ✅ Hotel staff only (internal 1-5 rating) | ❌ Never (only heart count) |
| ❤️ Love count (outcome) | ✅ "❤️ Loved by 12 guests" | ✅ Dashboard stats (avg rating, trends) | ✅ "❤️ Loved by 12 guests" |
| Individual clickstream | ❌ N/A | ❌ Never (even in Option A) | ❌ Never |

**Key principle:** Individual data stays private unless guest explicitly shares (Option A: QR code generation)

**Icon meanings:**
- ⭐ Stars = Pre-visit intent ("I want to try this") - Private saves/bookmarks
- ❤️ Hearts = Post-visit outcome ("I went and loved it") - Aggregate count from staff feedback

---

**FALLBACK VERSION: Guest didn't scan any cards**

**Guest B checks out (staff sees no card activity):**
```
Staff tablet shows:
┌─────────────────────────────────────────────────────┐
│ Guest: Bob Smith (Room 405)                         │
│ Card Activity:                                      │
│ • No cards scanned                                  │
└─────────────────────────────────────────────────────┘

Front desk: "Any favorite meals or spots you discovered during your stay?"

Bob: "Yeah, I found this great ramen place—Ooink Ramen—it was fantastic!"

Front desk enters feedback:
→ Ooink Ramen: "Great ramen, guest discovered on their own"
  Internal rating: ★★★★★ (5/5)
  Note: Guest did not use cards, organic discovery

→ Clicks "Save"
```

**Why fallback still works:**
- ✅ Captures organic discoveries (places hotel didn't recommend)
- ✅ Helps hotel expand recommendations (add Ooink Ramen to future cards)
- ✅ Shows which guests aren't engaging with cards (product improvement signal)

---

**ALTERNATIVE: Specific question (if card known):**

**Guest A checks out (staff knows they got 3♥ card):**
```
Front desk: "Hey, how was Giuseppe's?"
Guest A: "Oh it was amazing! The carbonara was so good. We sat by the window—super romantic."

Front desk opens mztape admin (tablet):
→ Finds Card 3♥, Giuseppe's
→ Quick entry form:
  Notes: "Carbonara amazing. Window table romantic."
  Internal rating: ★★★★★ (5/5)

→ Clicks "Save"
→ Done (15 seconds)
```

**Why specific question still works:**
- ✅ Lower friction (guest doesn't have to do anything)
- ✅ Natural conversation (part of checkout, not extra step)
- ✅ Hotel controls quality (can clarify ambiguous feedback)
- ✅ No proof needed (hotel knows guest stayed there)
- ✅ Higher submission rate (30-50% vs 10-20% online)

**Recommendation: Use open-ended question ("What were your favorite meals? Any places we should know about?") as default. Captures both recommended AND discovered places, plus problems.**

**Internal Rating Guide for Staff:**
- ★★★★★ (5) = Guest loved it, highly recommend
- ★★★★ (4) = Guest liked it, positive experience
- ★★★ (3) = Guest was neutral, mixed feedback
- ★★ (2) = Guest had issues, negative experience
- ★ (1) = Guest hated it, do not recommend

**What Guests See:**
- Only places with 4-5 stars shown as "Favorited by X guests"
- 1-3 star feedback is internal only (helps hotel track problems)
- Negative feedback comments NOT shown to future guests (hotel uses them to decide whether to remove spot)

---

### Step 4B: Guest Submits Review Online (Secondary Method - More Detail)

**If guest wants to submit detailed review, email next day:**
```
Subject: How was Giuseppe's?

Hi [Guest A],

You visited Giuseppe's yesterday (from your 3♥ card).
Help future guests—share your experience!

[Leave a Review]
```

**Guest clicks → Add to favorites form:**
```
┌─────────────────────────────────────────────────────┐
│ Add Giuseppe's Ristorante to your favorites         │
│                                                     │
│ What did you love about it?                         │
│ [Text box]                                          │
│ "The carbonara was amazing! Ask for table by the    │
│  window—super romantic. Portions are huge, we       │
│  shared one entree and it was perfect."             │
│                                                     │
│ Add a photo (optional):                             │
│ [Upload photo of carbonara]                         │
│                                                     │
│ Proof of visit (optional, helps future guests):    │
│ [ ] Photo of receipt (with total blurred)          │
│ [ ] Photo of restaurant exterior                    │
│ [ ] Photo of your dish                              │
│                                                     │
│ [Add to Favorites]                                  │
│                                                     │
│ Your favorite will be visible to future guests who  │
│ receive the 3♥ card from Hotel A.                   │
└─────────────────────────────────────────────────────┘
```

---

### Step 5: Review Goes to Hotel for Approval (Optional)

**Hotel dashboard shows pending favorites:**
```
┌─────────────────────────────────────────────────────┐
│ Pending Favorites (2)                               │
│                                                     │
│ 1. Giuseppe's - Guest A                             │
│    "The carbonara was amazing! Ask for table..."    │
│    [Photo: Carbonara dish]                          │
│    [Approve] [Edit] [Reject]                        │
│                                                     │
│ 2. Pike Place Market - Guest C                      │
│    "So fun! Get there early (7am) to avoid crowds"  │
│    [Approve] [Edit] [Reject]                        │
└─────────────────────────────────────────────────────┘
```

**Hotel decides:**
- Approve → Review goes live (visible to future guests)
- Edit → Suggest changes to guest ("Can you clarify what happened?")
- Reject → Review hidden (but hotel sees it for curation purposes)

**Why hotel approval?**
- Quality control (no spam, no abuse)
- Brand protection (hotel doesn't want offensive reviews visible)
- But: Hotel sees ALL reviews (even rejected ones) for learning

---

### Step 6: Aggregate Love Count Shown to Future Guests

**Next week, Guest B receives 3♥ card:**
```
Mobile page now shows:

🍝 Giuseppe's ❤️ Loved by 13 guests ← Updated (was 12)
📍 0.3 mi from hotel
Italian • $$ • 0.3 miles

[Get Directions]
```

**What changed:**
- ❤️ Count incremented from 12 → 13 (Guest A's positive feedback added)
- NO individual comments shown
- Trust signal: Higher number = more guests loved it after visiting
- Hotel uses internal feedback (5-star rating system) to decide: Keep/Remove/Update description

---

### Step 7: Hotel Learns and Iterates

**Hotel dashboard shows aggregated insights:**
```
┌─────────────────────────────────────────────────────┐
│ Card Performance: 3♥ (Romantic Dinner)              │
│                                                     │
│ Giuseppe's Ristorante                               │
│ • 13 mentions, avg 4.7/5 ⭐ ← KEEP                  │
│ • ❤️ Loved by: 12 guests (shown to future guests)  │
│ • Common themes: "Carbonara," "Romantic," "Window"  │
│ • Trend: Consistent 4-5 stars over 6 weeks          │
│                                                     │
│ Lombardi's Trattoria                                │
│ • 8 mentions, avg 4.1/5 ⭐ ← KEEP                   │
│ • ❤️ Loved by: 7 guests (shown to future guests)   │
│ • Common themes: "Quieter," "Good for conversation" │
│ • Trend: Stable performance                         │
│                                                     │
│ Java Junction                                       │
│ • 5 mentions, avg 2.4/5 ⚠️ ← REMOVE IMMEDIATELY    │
│ • ❤️ Loved by: 1 guest (shown to future guests)    │
│ • Common complaints: "Cold coffee," "Slow service"  │
│ • Trend: Declining from 3 to 2 stars               │
│                                                     │
│ Suggested action:                                   │
│ → Remove Java Junction from 3♥ card                │
│ → Add Canon Bar (avg 4.8/5 from 6♣ card testing)   │
└─────────────────────────────────────────────────────┘
```

**Hotel updates 3♥ card:**
- Removes Java Junction (low internal rating, multiple complaints)
- Adds Canon Bar (tested well on other cards)

**Next guest who gets 3♥ sees improved recommendations** (data-driven curation)

**Key insight:** Internal ratings (1-5 ⭐) help hotel track performance trends and make curation decisions. Only positive feedback (4-5 stars) is shown to guests as "❤️ Loved by X guests"

---

## Card-Specific Review Visibility

### Rule: Reviews are scoped to card type

**Guest receives 3♥ (Romantic Dinner):**
- Sees reviews from other 3♥ guests
- Does NOT see reviews from A♠ (Adventure Dinner) guests
- Why: Different context (romantic couples vs solo adventurers)

---

### Alternative Rules (Configurable):

**Option A: Suit-level visibility (broader)**
```
Guest receives 3♥ (Romantic Dinner)
→ Sees reviews from ALL ♥ cards (romantic theme)
  - A♥ (romantic spots)
  - 2♥ (romantic breakfast)
  - 3♥ (romantic dinner)
  - etc.
```

**Option B: Value-level visibility (category-specific)**
```
Guest receives 3♥ (Romantic Dinner)
→ Sees reviews from ALL "3" cards (dinner category)
  - 3♥ (romantic dinner)
  - 3♠ (adventure dinner)
  - 3♦ (luxury dinner)
  - 3♣ (family dinner)
```

**Option C: Hotel-wide visibility (everything)**
```
Guest receives 3♥
→ Sees reviews from ALL cards (hotel-wide knowledge base)
→ But: Reviews tagged with card type ("This review is from a 3♥ guest")
```

**Recommendation: Start with Option A (suit-level)**
- Romantic guests see romantic reviews (relevant context)
- Family guests see family reviews (relevant context)
- Not so broad that reviews are irrelevant
- Not so narrow that there are too few reviews

---

## Proof of Visit: Photos, Essays, Photoessays

### Why Proof of Visit Matters

**Problem:** Without proof, anyone can write fake reviews

**Solutions:**

### 1. Photo of Dish
```
Guest uploads: [Photo of carbonara]
→ Proves: They were at restaurant (saw the dish)
→ Confidence: 70% (could be Google image)
→ Benefit: Future guests see what dish looks like
```

### 2. Photo of Receipt (Total Blurred)
```
Guest uploads: [Photo of Giuseppe's receipt, $85 total blurred]
→ Proves: They paid there (high confidence)
→ Confidence: 95%
→ Privacy: Total blurred (only restaurant name + date visible)
```

### 3. Photo of Restaurant Exterior
```
Guest uploads: [Photo of Giuseppe's storefront]
→ Proves: They were physically there
→ Confidence: 80%
→ Benefit: Future guests see what entrance looks like ("Look for red door")
```

### 4. Photoessay (Multiple Photos)
```
Guest uploads:
- Photo of exterior
- Photo of interior (ambiance)
- Photo of dish
- Photo of dessert
→ Proves: They spent significant time there (high confidence)
→ Confidence: 95%
→ Benefit: Rich storytelling for future guests
```

### 5. Essay (No Photo, Just Text)
```
Guest writes 200+ words:
"We arrived at 6pm and were seated immediately. The ambiance
 was romantic—dim lighting, candles on tables. We ordered the
 carbonara (highly recommended by previous guests) and it was
 phenomenal. The portions are huge—we shared one entree and
 were stuffed. Service was friendly, we asked for the table by
 the window and they accommodated. Total for 2 with wine: ~$85.
 Would absolutely return."

→ Proves: Detailed, specific experience (high confidence)
→ Confidence: 90%
→ Benefit: Rich context for future guests
```

**Recommendation: Encourage photoessays (photos + text)**
- Most authentic (hard to fake)
- Most valuable to future guests (visual + context)
- Optional (guests can submit text-only if prefer privacy)

---

## Incentive Structure: Why Guests Review

### Incentive 1: Help Future Guests (Altruism)

**Messaging:**
```
"You benefited from previous guests' reviews.
 Help the next guest—share your experience!"
```

**Emotional hook:** Pay it forward (you received value, give back)

---

### Incentive 2: Influence Hotel's Recommendations (Agency)

**Messaging:**
```
"Your review helps [Hotel Name] curate better recommendations.
 If a spot didn't work for you, future guests won't get it."
```

**Emotional hook:** You have power (hotel listens to you)

---

### Incentive 3: See Your Impact (Gamification)

**After review submitted:**
```
"Thanks! Your review has been viewed by 12 guests so far.
 3 guests visited Giuseppe's because of your recommendation."
```

**Emotional hook:** Status (your review matters)

---

### Incentive 4: Unlock Future Reviews (Reciprocity)

**Rule: Submit review → Unlock ability to see full reviews**

```
Guest A submits review → Can now see full reviews (not just snippets)
Guest B doesn't submit review → Only sees snippets ("Get the carbonara..." [Read more])
```

**Emotional hook:** Reciprocity (contribute to see more)

---

### Incentive 5: Build Reputation (Repeat Guests)

**For repeat guests:**
```
"Welcome back, [Guest Name]!
 Your previous reviews have been helpful to 47 guests.
 You're a Trusted Reviewer ⭐"
```

**Emotional hook:** Status + recognition (build reputation over time)

---

### Incentive 6: No Explicit Incentive (Just Ask)

**Sometimes, just asking works:**
```
Email next day:
"How was Giuseppe's?
[Leave a review]"

→ 20-30% of guests will review (no incentive needed)
```

---

## Hotel Value Prop: Accumulated Guest Knowledge

### Before: Hotel curates blindly

```
Hotel adds Giuseppe's to recommendations
→ Guests visit (maybe?)
→ Hotel has NO IDEA if it was good
→ Hotel keeps recommending (or removes based on gut feeling)
```

---

### After: Hotel curates with data

```
Hotel adds Giuseppe's
→ 13 guests review (4.7/5 avg)
→ Hotel sees: "Carbonara is a hit, portions are huge, get there early"
→ Hotel updates recommendation description:
  "Giuseppe's: Try the carbonara! Portions are huge (share one entree).
   Arrive by 6pm or expect a wait."
→ Future guests have better experience (thanks to previous guests' wisdom)
```

**Result:** Hotel recommendations improve over time (data-driven, not gut-driven)

---

## Async Micro-Community: The "3♥ Guests"

### The Concept:

**All guests who receive 3♥ card form a community** (without realizing it):
- They don't meet each other
- They don't chat in real-time
- But they contribute to shared knowledge base
- Over time, 3♥ recommendations get better (because community curates)

---

### Example: 3♥ Community Over 6 Months

**Month 1: Giuseppe's recommended (hotel's gut choice)**
```
5 guests receive 3♥, 3 submit reviews:
- "Great!" (5/5)
- "Carbonara was amazing" (5/5)
- "Romantic but loud" (4/5)

Avg: 4.7/5 → Hotel keeps Giuseppe's
```

**Month 2: More reviews accumulate**
```
10 guests receive 3♥, 7 submit reviews:
- "Service was slow this time" (3/5)
- "Still love the carbonara" (5/5)
- "Too crowded on Saturday night" (3/5)

Avg drops to 4.3/5 → Hotel notes: "Avoid Saturdays"
```

**Month 3: Hotel updates description**
```
Giuseppe's description now says:
"Great for weeknights (avoid Saturdays—too crowded).
 Service can be slow, but food is worth it."

Guests now have realistic expectations → Reviews improve to 4.5/5
```

**Month 4: Community discovers hidden gem**
```
One guest writes:
"Giuseppe's was good, but we stumbled on Canon Bar next door—
 even better atmosphere and faster service!"

Hotel investigates Canon Bar → Adds to 3♥ card

Next month:
- Giuseppe's: 4.5/5 (still good)
- Canon Bar: 4.9/5 (new favorite)
```

**Month 6: 3♥ recommendations are now battle-tested**
```
- Giuseppe's: 4.5/5 (35 reviews) ← Proven winner
- Canon Bar: 4.9/5 (18 reviews) ← Community discovery
- Cara Mia: REMOVED (was 3.8/5, too many complaints)

3♥ card is now BETTER than any guidebook (crowdsourced + curated)
```

---

## Living Guest Book: Every Guest is a Secret Shopper

### The Old Model: Secret Shoppers

**Restaurants hire secret shoppers:**
- Paid to visit, evaluate, report back
- Expensive ($50-200 per visit)
- One-time snapshot (not ongoing)

---

### The New Model: Guests Are Secret Shoppers (Unpaid)

**Every guest who reviews becomes a secret shopper:**
- Visits restaurant, evaluates, reports back (via review)
- Free (guests volunteer because they benefit)
- Ongoing (every guest adds data)

**Result:** Hotel has 100+ "secret shoppers" per month (every guest who reviews)

---

### Hotel Benefits:

**1. Quality Control**
```
If Giuseppe's quality drops:
→ Reviews drop from 4.7 to 3.8
→ Hotel sees trend, investigates
→ Hotel either removes Giuseppe's or talks to them ("We're getting complaints")
```

**2. Discover New Spots**
```
Guest mentions Canon Bar in review
→ Hotel investigates
→ Adds to recommendations
→ Future guests benefit (would never have found it otherwise)
```

**3. Optimize Descriptions**
```
Reviews reveal patterns:
- "Portions are huge" (mentioned 8 times)
- "Get there early" (mentioned 5 times)
- "Ask for table by window" (mentioned 4 times)

Hotel updates description:
"Giuseppe's: Huge portions (share one entree). Arrive by 6pm to avoid wait.
 Ask for table by window for romantic ambiance."
```

---

## Incentivize Repeat Visits: Reputation System

### For Repeat Guests:

**First stay:**
```
Guest submits 3 reviews
→ Unlocks: "Trusted Reviewer" badge
→ Future reviews have ⭐ icon
```

**Second stay (6 months later):**
```
Guest returns, receives 6♣ card (family activities)
→ Mobile page says:
  "Welcome back! You're a Trusted Reviewer ⭐
   Your previous reviews helped 47 guests."

Guest submits 2 more reviews
→ Unlocks: "Super Reviewer" badge
→ Hotel comps dessert at next visit (optional perk)
```

**Third stay (1 year later):**
```
Guest returns, receives 10♦ card (luxury full day)
→ Mobile page says:
  "Welcome back! You're a Super Reviewer 🌟
   You've submitted 8 reviews across 3 stays.
   Your insights have been viewed 142 times."

Guest writes detailed photoessay
→ Hotel features review on website: "Guest spotlight: [Name]'s Seattle guide"
→ Guest feels recognized (status + belonging)
```

**Result:** Repeat guests are incentivized to contribute more (build reputation over time)

---

## Technical Implementation

### Database Schema

**Guest Feedback Table:**
```sql
CREATE TABLE guest_feedback (
  id UUID PRIMARY KEY,
  hotel_id UUID,
  card_id UUID, -- e.g., "3♥" or "A♠"
  business_id UUID, -- Giuseppe's
  guest_token UUID, -- Anonymous (not tied to name/email)
  internal_rating INT, -- 1-5 (staff-assigned, NOT shown to guests)
  text TEXT, -- Guest's comment
  photos JSONB, -- Array of photo URLs
  proof_of_visit JSONB, -- {type: "receipt", url: "..."}
  status VARCHAR, -- "pending", "approved", "rejected"
  created_at TIMESTAMP,
  approved_at TIMESTAMP,
  captured_by VARCHAR -- "staff" or "guest_online"
);
```

**Aggregated Ratings (Cached):**
```sql
CREATE TABLE business_ratings (
  id UUID PRIMARY KEY,
  hotel_id UUID,
  card_id UUID, -- e.g., "3♥"
  business_id UUID,
  avg_internal_rating FLOAT, -- 4.7 (for hotel dashboard only)
  total_mentions INT, -- 13 (all feedback, any rating)
  favorite_count INT, -- 12 (only 4-5 star ratings, shown to guests)
  last_updated TIMESTAMP
);
```

**Key Fields:**
- `avg_internal_rating`: Average of all staff-assigned 1-5 ratings (hotel tracking only)
- `total_mentions`: Total feedback count (positive + negative)
- `favorite_count`: Count of 4-5 star ratings only (displayed to guests as "Favorited by X guests")

---

### Feedback Submission Flow

**Flow A: Staff captures feedback at checkout (Primary)**

**1. Staff enters feedback:**
```
POST /api/feedback/staff
{
  "card_token": "a3k9f2",
  "business_id": "giuseppe-123",
  "internal_rating": 5, // Staff-assigned 1-5 rating
  "text": "Carbonara incredible. Window table romantic.",
  "captured_by": "staff"
}
```

**2. Feedback saved with approved status:**
```sql
INSERT INTO guest_feedback (
  internal_rating = 5,
  status = 'approved', -- Staff-captured is pre-approved
  captured_by = 'staff'
)
```

**3. Aggregated ratings update immediately:**
```sql
UPDATE business_ratings
SET avg_internal_rating = (
      SELECT AVG(internal_rating)
      FROM guest_feedback
      WHERE status = 'approved' AND business_id = 'giuseppe-123'
    ),
    total_mentions = (
      SELECT COUNT(*)
      FROM guest_feedback
      WHERE status = 'approved' AND business_id = 'giuseppe-123'
    ),
    favorite_count = (
      SELECT COUNT(*)
      FROM guest_feedback
      WHERE status = 'approved'
        AND business_id = 'giuseppe-123'
        AND internal_rating >= 4  -- Only 4-5 star counts as "favorite"
    )
WHERE business_id = 'giuseppe-123' AND card_id = '3♥'
```

**4. Future guests see updated favorite count:**
```
Mobile page now shows: Giuseppe's ⭐ Favorited by 13 guests
```

---

**Flow B: Guest submits feedback online (Secondary)**

**1. Guest submits feedback:**
```
POST /api/feedback/guest
{
  "card_token": "a3k9f2",
  "business_id": "giuseppe-123",
  "text": "The carbonara was amazing!",
  "photos": ["carbonara.jpg"],
  "captured_by": "guest_online"
}
```

**2. Feedback goes to pending status:**
```sql
INSERT INTO guest_feedback (
  internal_rating = NULL, -- Staff will assign rating during approval
  status = 'pending',
  captured_by = 'guest_online'
)
```

**3. Hotel dashboard shows pending feedback:**
```
Hotel logs in → Sees "1 pending feedback"
→ Reviews feedback
→ Assigns internal rating (1-5 stars)
→ Clicks "Approve"
```

**4. Feedback status changes to approved:**
```sql
UPDATE guest_feedback
SET status = 'approved',
    internal_rating = 5,  -- Staff assigns rating
    approved_at = NOW()
WHERE id = '...'
```

**5. Aggregated ratings update (same as Flow A)**

---

## Tent Cards: Separate Loop (Inter-Destination Network)

**The user's insight:** Tent cards can still exist, but for a DIFFERENT loop:

### Old idea (didn't work): Hotel → Business attribution
### New idea: Business → Business network

**Concept:**
```
Giuseppe's has tent card on table:
"While you're in the neighborhood, check out:
 • Canon Bar (next door)
 • Espresso Vivace (2 blocks)
 • Pike Place Market (5 min walk)"

Guest scans tent card → Discovers other businesses
→ Multi-hop behavior (Giuseppe's → Canon → Espresso Vivace)
→ Builds neighborhood ecosystem (businesses help each other)
```

**This is a separate product:**
- mztape for Hotels (main product)
- mztape for Businesses (separate product, launches later)
- Businesses pay for tent cards ($25/month) to cross-promote

**But: Not critical for hotel launch** (focus on guest review loop first)

---

## Summary: Why This Model is Better

### Old Model (Static Recommendations):
- ❌ No feedback loop (hotel never learns what worked)
- ❌ Recommendations stagnate (same photocopied list for years)
- ❌ Doesn't scale (concierge knowledge siloed, limited to front desk hours)
- ❌ Gut-driven curation (not data-driven)
- ❌ Hotel has no idea if guests liked recommendations

### New Model (Guest Feedback Loop):
- ✅ Tight feedback loop (mid-stay conversations capture guest experiences)
- ✅ Accumulated guest knowledge (each guest contributes via staff conversation)
- ✅ Hotel learns what works ("Giuseppe's = 4.7/5, Java Junction = 2.4/5")
- ✅ Future guests benefit (see aggregate trust signal: "Favorited by X guests")
- ✅ Privacy-first (individual feedback hotel-only, only aggregate counts shown)
- ✅ No cookies needed (feedback captured by staff, not clickstream tracking)
- ✅ Scales without concierge (system captures knowledge, shared across team)
- ✅ Living guest book (every guest is a "secret shopper")
- ✅ Hotel recommendations improve over time (data-driven curation)
- ✅ Async micro-community (3♥ guests help curate over time, but privately)

---

## Next Steps: Implement Review Loop

### Month 0 (Add to existing roadmap):

**Week 1: Design review UI (4 hours)**
```
[ ] Sketch review submission form (rating + text + photo upload)
[ ] Sketch mobile page with reviews (how future guests see them)
[ ] Sketch hotel dashboard (pending reviews, approval flow)
```

**Week 2: Build MVP (20 hours)**
```
[ ] Database schema (reviews table, aggregated ratings)
[ ] Review submission API
[ ] Hotel approval dashboard (simple admin UI)
[ ] Mobile page: Show reviews when guest scans card
```

**Week 3: Test with 5 hotels (manual)**
```
[ ] Ask 5 test hotels to request reviews from guests (manual email)
[ ] Collect 10-20 reviews
[ ] Show reviews to next guests
[ ] Gather feedback: Do reviews help? Are they trustworthy?
```

**Week 4: Iterate**
```
[ ] Add photo upload (if demand exists)
[ ] Add "proof of visit" (receipt photo, dish photo)
[ ] Add review moderation (approve/reject flow)
```

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Purpose:** Define guest review loop model as alternative to business attribution tracking
**Key Insight:** Close the loop between recommendations and reviews (not recommendations and destinations). Create async micro-community of guests who help hotel curate better over time. Every guest becomes a "secret shopper" contributing to living guest book.
