# Cookie-Less Tracking: What We Can Track Without Browser Storage

**Key Question:** Can we track hotel scan → business visit without cookies or login?

**Answer:** Yes—using QR code tokens, aggregate patterns, and probabilistic matching.

---

## Method 1: Token-in-URL (Most Reliable, No Cookies)

### How It Works

**Each QR code has a unique token built-in:**

```
Hotel A, Card A♥ (Romantic Dinner):
→ QR code links to: mztape.com/c/a3k9f2

Token "a3k9f2" tells us:
• Source: Hotel A
• Card: A♥
• Category: Romantic Dinner
```

---

**When guest scans at hotel:**

```
1. Guest scans QR code on card A♥
2. URL: mztape.com/c/a3k9f2
3. System generates unique session token: t=g7x3k9
4. Redirects to: mztape.com/recommendations?source=a3k9f2&t=g7x3k9

Now we know:
• This guest came from Hotel A, Card A♥
• Their session token is g7x3k9
```

---

**All links include token:**

```
Recommendation page shows Giuseppe's:
→ Link: mztape.com/giuseppe?t=g7x3k9

"Get Directions" button:
→ Link: maps.google.com?q=giuseppe&ref=g7x3k9
   (Token passed through, even to external links)

"Call Restaurant" button:
→ tel:555-1234
   (Can't track phone calls, but URL clicks tracked)
```

---

**When guest scans tent card at Giuseppe's:**

```
Tent card QR code:
→ mztape.com/b/giuseppe/checkin

Guest scans → Redirects to:
→ mztape.com/b/giuseppe/checkin?t=g7x3k9
   (Token in URL from earlier, OR asks: "Did you scan from a hotel?")

If token present:
✅ Match! Same session (g7x3k9) viewed Giuseppe's at hotel, now at business
✅ Conversion confirmed

If token NOT present:
❓ New session—ask: "Did you hear about us from a hotel?"
   → Guest clicks "Yes, Hotel A"
   → Partial attribution (self-reported)
```

---

### What We Can Track (No Cookies Needed)

**Individual Guest Journey:**
```
Session: g7x3k9
6:15 PM: Scanned at Hotel A (Card A♥)
6:18 PM: Viewed Giuseppe's (clicked from recommendation page)
6:20 PM: Viewed Espresso Vivace
6:25 PM: Clicked "Get Directions" to Giuseppe's
6:52 PM: Scanned tent card at Giuseppe's ← CONVERSION
8:15 PM: Scanned tent card at Canon ← 2nd CONVERSION
```

**Pros:**
- ✅ No cookies required (token in URL)
- ✅ Works even if browser storage disabled
- ✅ Privacy-friendly (token is random, not tied to identity)
- ✅ Survives browser restarts (if guest keeps link open)

**Cons:**
- ❌ If guest closes browser and reopens later, token lost
- ❌ If different person scans tent card, token may be from previous guest
- ❌ URLs are long/ugly (but functional)

---

## Method 2: Aggregate Patterns (No Individual Tracking)

### What We Track at System Level

**Even without tracking individuals, we can see patterns:**

**Hotel Side:**
```
Hotel A, Last 30 Days:
• Card A♥ (Romantic Dinner) scanned: 87 times
• Giuseppe's viewed: 58 times (67% of A♥ scans)
• Giuseppe's "Get Directions" clicked: 42 times (72% of views)
```

**Business Side:**
```
Giuseppe's, Last 30 Days:
• Tent card scanned: 180 times
• Time distribution:
  - 6-7 PM: 80 scans (peak dinner arrival)
  - 7-8 PM: 60 scans
  - 8-9 PM: 30 scans
  - 9+ PM: 10 scans
```

**Aggregate Conversion (Probabilistic):**
```
Hotel A shows Giuseppe's to 58 guests
Giuseppe's tent card scanned 180 times total

Assuming:
• Hotel A is 1 of 3 hotels recommending Giuseppe's
• 180 scans / 3 hotels ≈ 60 scans attributable to Hotel A
• 60 scans / 58 views = 103% conversion rate

Wait, that's >100%? Means:
• Some guests visit without scanning recommendation first (walk-ins)
• OR multiple guests from same hotel table scan tent card
• OR guests visit multiple times

Adjusted estimate: ~40-60% conversion rate (reasonable range)
```

---

### What We Can Infer Without Cookies

**Time-Based Correlation:**
```
6:15 PM: Hotel A guest scans, views Giuseppe's
6:52 PM: Someone scans tent card at Giuseppe's

Time gap: 37 minutes (reasonable walk time: 0.3 mi × 20 min/mi = 6 min walk + 30 min browsing)

Confidence: 70% (probably the same guest, but could be coincidence)
```

**Volume Correlation:**
```
Week 1: Hotel A shows Giuseppe's to 58 guests
        → Giuseppe's tent card scanned 60 times

Week 2: Hotel A stops recommending Giuseppe's (testing)
        → Giuseppe's tent card scanned 22 times

Difference: 38 fewer scans when Hotel A not recommending
→ Proves Hotel A drives ~38 visits/week (even without individual tracking)
```

**Day-of-Week Patterns:**
```
Hotel A check-ins: Peak Friday-Saturday (weekend travelers)
Giuseppe's tent card scans: Peak Saturday-Sunday (day after check-in)

→ Lag correlation suggests hotel guests visit next day
```

---

## Method 3: Probabilistic Matching (No Cookies, No Tokens)

### Device Fingerprinting (Privacy-Friendly Version)

**What we can detect without cookies:**

**Browser metadata (automatically sent in HTTP headers):**
```
User-Agent: Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)...
Accept-Language: en-US,en;q=0.9
Screen Resolution: 390×844 (iPhone 14)
Timezone: America/Los_Angeles
```

**Fingerprint hash:**
```
Guest scans at hotel:
• Device: iPhone 14, iOS 17, Safari, PST timezone
• Fingerprint: hash = f8a3b2c1

Guest scans at business 37 minutes later:
• Device: iPhone 14, iOS 17, Safari, PST timezone
• Fingerprint: hash = f8a3b2c1

Match! 85% confidence same device = same guest
```

---

### Probabilistic Match Criteria

**Combine multiple signals:**

```
Hotel scan (6:15 PM):
• Device: iPhone 14, Safari, iOS 17
• Location: Hotel A (IP address in hotel range)
• Actions: Viewed Giuseppe's, Espresso Vivace, Canon
• Time: 6:15 PM

Business scan (6:52 PM):
• Device: iPhone 14, Safari, iOS 17 (MATCH)
• Location: Near Giuseppe's (IP/GPS)
• Time: 37 min after hotel scan (reasonable)
• Business: Giuseppe's (MATCH - was viewed at hotel)

Confidence score:
• Device match: +40%
• Location match: +20%
• Time gap reasonable: +20%
• Business viewed at hotel: +15%
• Total: 95% confidence = CONVERSION
```

---

### Confidence Thresholds

**Set thresholds for attribution:**

```
>90% confidence: Count as confirmed conversion
70-90% confidence: Count as probable conversion
<70% confidence: Don't count (too uncertain)
```

**Result:**
```
Giuseppe's, Last 30 Days:
• 180 tent card scans total
• 72 confirmed conversions (>90% confidence) from Hotel A
• 18 probable conversions (70-90% confidence)
• 90 uncertain (walk-ins, other hotels, locals)

Reported to hotel: "72 confirmed visits from your recommendations"
```

---

## Method 4: Self-Reported Attribution (Ask the Guest)

### Tent Card Prompt

**When guest scans tent card at business:**

```
┌─────────────────────────────────────────────────────┐
│ Welcome to Giuseppe's! 🍝                           │
│                                                     │
│ How did you hear about us?                          │
│                                                     │
│ [ ] Recommended by my hotel                         │
│     └─ Which hotel? [Dropdown: Hotel A, Hotel B...] │
│                                                     │
│ [ ] Walking by / Saw the sign                       │
│ [ ] Google / Yelp                                   │
│ [ ] Friend recommended                              │
│ [ ] Other                                           │
│                                                     │
│ [Continue]                                          │
└─────────────────────────────────────────────────────┘
```

**Pros:**
- ✅ 100% accurate (guest tells you)
- ✅ No tracking technology needed
- ✅ Privacy-friendly

**Cons:**
- ❌ Not all guests will answer (50-70% response rate)
- ❌ Recall bias ("I think it was Hotel A? Or B?")
- ❌ Extra friction (guest has to click through)

---

### Incentivize Self-Reporting

**Offer small reward for answering:**

```
"How did you hear about us?
 Answer to unlock a special offer!"

After answering:
"Thanks! Here's 10% off your next visit:
 [QR code for discount]"
```

**Response rate increases from 50% → 80%**

---

## Method 5: Business POS Integration (Gold Standard)

### Partner with Restaurant POS Systems

**Flow:**

```
1. Guest makes reservation via mztape link
   → Name: "Sarah Johnson", Party of 2, 7:00 PM
   → Reservation includes token: ref=g7x3k9

2. Restaurant POS (Toast, Square, Resy) records reservation
   → Captures token in notes field

3. Guest arrives, checks in at host stand
   → POS confirms: "Sarah Johnson, party of 2"
   → Confirms token: ref=g7x3k9

4. mztape receives webhook from POS:
   → "Reservation g7x3k9 checked in at 6:52 PM"
   → 100% confirmed conversion
```

**Pros:**
- ✅ 100% accurate (POS confirms arrival)
- ✅ Can track spend (if POS shares: "Sarah spent $85")
- ✅ No guest friction (POS tracks automatically)

**Cons:**
- ❌ Requires POS integration (complex, not all restaurants use same system)
- ❌ Privacy concern (POS shares guest name + spend)
- ❌ Only works for reservations (not walk-ins)

---

## What We CAN Track Without Cookies

### Individual Level (With URL Tokens)

```
✅ Guest scanned at Hotel A
✅ Guest viewed Giuseppe's
✅ Guest clicked "Get Directions"
✅ Guest scanned tent card at Giuseppe's (if token in URL)
✅ Time lag: 37 minutes
✅ Multi-hop: Also visited Canon (if token persists)
```

**Limitations:**
- Token lost if browser closed
- Token may be from different guest if shared link

---

### Aggregate Level (No Tokens Needed)

```
✅ Hotel A shows Giuseppe's to 58 guests/month
✅ Giuseppe's tent card scanned 180 times/month
✅ Correlation: When Hotel A stops recommending, scans drop 40%
✅ Time patterns: Peak scans 30-60 min after hotel scans
✅ Day-of-week: Hotel check-ins Friday → Giuseppe's scans Saturday
```

**Limitations:**
- Can't attribute individual conversions (only aggregate trends)
- Correlation ≠ causation (other factors may influence scans)

---

### Probabilistic Level (Device Fingerprinting)

```
✅ Device match: Same iPhone 14 scanned at hotel + business
✅ Time gap: 37 minutes (reasonable)
✅ Location: Giuseppe's (matches recommendation viewed at hotel)
✅ Confidence: 95% → Count as conversion
```

**Limitations:**
- Not 100% certain (could be different person with similar device)
- Privacy concerns (fingerprinting feels invasive, even if no PII)

---

### Self-Reported Level (Guest Tells You)

```
✅ Guest clicks: "Recommended by Hotel A"
✅ 100% accurate (guest confirms)
```

**Limitations:**
- 50-80% response rate (not all guests answer)
- Recall bias (guest may misremember)

---

## Recommended Approach: Layered Tracking

### Tier 1: URL Tokens (Primary Method)

```
Every QR code has unique token
→ Token passed through all links
→ If guest scans tent card with token → 100% confirmed conversion
```

**Coverage: 40-60% of conversions** (guests who keep browser open)

---

### Tier 2: Probabilistic Matching (Fallback)

```
If token not present:
→ Use device fingerprint + time + location
→ If 90%+ confidence → Count as probable conversion
```

**Coverage: +20-30% of conversions** (guests who closed browser)

---

### Tier 3: Self-Reported (For Remaining)

```
If token not present AND fingerprint uncertain:
→ Ask: "Did you hear about us from a hotel?"
→ 50-80% response rate
```

**Coverage: +10-20% of conversions** (guests who answer)

---

### Tier 4: Aggregate Analysis (System-Wide)

```
For any remaining conversions:
→ Track aggregate patterns (volume, time, day-of-week)
→ Report to hotel: "We estimate 40-60 conversions from your recommendations"
   (conservative range based on aggregate data)
```

**Coverage: 100%** (all conversions, but less precise)

---

## Privacy-Friendly Tracking: What We DON'T Store

### No PII (Personally Identifiable Information)

```
❌ Guest name
❌ Email address
❌ Phone number
❌ Credit card info
❌ Precise GPS location (only city-level)
❌ IP address (only used for probabilistic matching, not stored)
```

---

### Only Anonymous Tokens

```
✅ Session token: g7x3k9 (random, not tied to identity)
✅ Device fingerprint: hash (anonymous)
✅ Timestamps: When scanned
✅ Actions: Which businesses viewed/visited
✅ Source: Which hotel/card
```

**Like Google Analytics:**
- Tracks behavior, not identity
- No way to reverse-engineer who the guest is

---

## Summary: Tracking Without Cookies

### What Works Best (No Cookies Required):

**1. URL Tokens (40-60% coverage, 100% accuracy)**
```
QR code → Token in URL → Passed through all links → Tent card scan includes token
= Confirmed conversion
```

**2. Aggregate Patterns (100% coverage, 80% accuracy)**
```
Hotel shows Giuseppe's to 58 guests
Giuseppe's scans increase by 40 that week
= Estimated 40 conversions from hotel
```

**3. Probabilistic Matching (20-30% coverage, 85-95% accuracy)**
```
Same device fingerprint + reasonable time gap + viewed at hotel
= Probable conversion
```

**4. Self-Reported (10-20% coverage, 100% accuracy)**
```
Guest clicks: "I heard about you from Hotel A"
= Confirmed conversion
```

---

### Recommended Tracking Stack:

```
Primary: URL tokens (build into every QR code)
Fallback: Probabilistic matching (for guests who closed browser)
Supplemental: Self-reported (for uncertain cases)
Reporting: Aggregate analysis (for system-wide trends)
```

**Result:**
- 60-80% of conversions tracked with high confidence
- 100% of conversions estimated via aggregate patterns
- Zero cookies, zero PII stored
- Privacy-friendly, GDPR-compliant

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Purpose:** Define what's trackable without cookies or browser storage
**Key Insight:** URL tokens + probabilistic matching + aggregate patterns = 60-80% conversion tracking without cookies
