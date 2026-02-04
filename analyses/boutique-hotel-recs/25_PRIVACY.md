# Privacy-First Architecture

## Executive Summary

**QRCards is privacy-first by design, not as an afterthought.**

Traditional recommendation systems require:
- ❌ App installation
- ❌ Account creation
- ❌ Login credentials
- ❌ Location tracking
- ❌ Check-ins
- ❌ Personal data collection

**QRCards requires NONE of these.**

**Our Approach:**
- ✅ Physical cards (tangible keepsake guests can take home)
- ✅ Digital mobile experience (scan QR code → instant access)
- ✅ Privacy-first (no guest login, no tracking by default)
- ✅ Hospitality-specific workflow (staff conversations, not surveillance)

**Result:** Guests get personalized recommendations without sacrificing privacy. Hotels get feedback loop without creepy tracking.

---

**Key Insight: The Privacy Paradox**
- **Public codes (shared QR) = Maximum privacy** - Because they're public, they're inherently private. System can't identify who scanned.
- **Unique cards (per-card QR) = Trackable** - Because each card is unique, hotel CAN track distribution (if they choose).
- See [Technical Implementation](#technical-implementation) for details.

---

## Table of Contents

1. [Why Privacy Matters](#why-privacy-matters)
2. [What We Don't Collect](#what-we-dont-collect)
3. [What We Do Collect (And Why)](#what-we-do-collect-and-why)
4. [Privacy Levels Explained](#privacy-levels-explained)
5. [How This Compares to Competitors](#how-this-compares-to-competitors)
6. [Technical Implementation](#technical-implementation)
7. [Age-Gating for Restricted Content](#7-age-gating-for-restricted-content)
8. [Privacy as a Feature](#privacy-as-a-feature)
9. [Privacy Policy (Plain English)](#privacy-policy-plain-english)

---

## Why Privacy Matters

### The Problem with Traditional Apps

**Most recommendation apps track everything:**
```
User downloads app
  ↓
Creates account (email, phone, password)
  ↓
Grants location permission
  ↓
App tracks: Where you go, when you go, how long you stay, who you're with
  ↓
Data sold to advertisers, aggregated, shared with third parties
  ↓
User has no control, no visibility, no opt-out
```

**Guest experience:**
- "I just wanted restaurant recommendations, why does it need my location?"
- "Why do I need to create an account?"
- "I don't want another app on my phone"
- "I don't want the hotel tracking everywhere I go"

**Hotel concerns:**
- "Are we liable if guest data is breached?"
- "What if a guest complains about being tracked?"
- "Do we need GDPR/CCPA compliance for this?"

---

### The QRCards Approach: Privacy-First

**No app, no account, no tracking:**
```
Guest picks physical card from shared pool (3♥ - Romantic Dinner)
  ↓
Scans QR code with phone camera (built-in, no app needed)
  ↓
Mobile web page opens instantly (no login, no account)
  ↓
Sees recommendations: "Giuseppe's - ❤️ Loved by 12 guests"
  ↓
Guest taps "Card Directory" → Browses other cards (Cocktail Bars, Live Music, etc.)
  ↓
Switches to "Cocktail Bars" → Sees those recommendations
  ↓
(Hotel does NOT see: Guest browsed other cards - private exploration)
  ↓
Taps "Get Directions" → Opens in Maps app
  ↓
Visits restaurant (QRCards doesn't know, doesn't track)
  ↓
Mid-stay: Staff asks "Any favorite meals?"
  ↓
Guest shares verbally → Staff enters feedback
  ↓
Feedback captured, aggregated, shown to future guests as count only
```

**Guest experience:**
- "I just scanned a card and got recommendations—that's it?"
- "No app to download? No account to create? Perfect."
- "Wait, I can browse ALL the cards from here? I don't have to go back to the desk?"
- "And they're not tracking what I look at? Even better."

**Hotel benefits:**
- No liability (no personal data collected)
- No compliance headaches (GDPR/CCPA minimal impact)
- Guest-friendly (privacy = trust)

---

## What We Don't Collect

### 1. No Personal Information
- ❌ Name
- ❌ Email address
- ❌ Phone number
- ❌ Credit card
- ❌ Address
- ❌ Birthdate
- ❌ Social media profiles

**Why:** We don't need it. Recommendations work without knowing who you are.

---

### 2. No Location Tracking
- ❌ GPS coordinates
- ❌ "Where are you now?"
- ❌ "Where have you been?"
- ❌ Geofencing ("Did you visit Giuseppe's?")
- ❌ Background location tracking

**Why:** Creepy and unnecessary. If you want directions, you tap "Get Directions" and your phone's Maps app handles it (not us).

---

### 3. No Check-Ins
- ❌ "Check in at Giuseppe's to unlock badge"
- ❌ "Share your check-in on social media"
- ❌ "Prove you visited by checking in"

**Why:** We're not Foursquare. You don't need to perform for us.

---

### 4. No Account Creation
- ❌ Username/password
- ❌ "Sign in with Google/Facebook"
- ❌ Email verification
- ❌ Profile creation

**Why:** Friction. Guests just want recommendations, not another account to manage.

---

### 5. No App Installation
- ❌ "Download our app from the App Store"
- ❌ 50MB download
- ❌ Permissions requests (location, camera, contacts)
- ❌ Another app taking up space on phone

**Why:** Barrier to entry. QR codes work with phone's built-in camera—instant access, zero friction.

---

### 6. No Clickstream Tracking (By Default)
- ❌ "What recommendations did you click?"
- ❌ "How long did you look at each business?"
- ❌ "What order did you view them in?"
- ❌ "Did you tap directions?"
- ❌ "Which cards did you browse via card directory?"

**Why (MVP):** Not needed for feedback loop. Staff conversation captures what matters: "Did you go? Did you like it?"

**Card Directory Browsing (Private):**
- Guest picks "Romantic Dinner" card but browses "Cocktail Bars" and "Live Music" via card directory
- Hotel does NOT see: "Guest viewed Cocktail Bars, Live Music"
- Only tracked: Initial card scan (if unique card) or aggregate usage (if shared code)
- **Privacy protection:** Guest can explore all interests without hotel knowing

**Why (V2):** If we add personalization features (⭐ Save buttons, swipe), these are PRIVATE to the guest unless they explicitly share via QR code.

---

## What We Do Collect (And Why)

### Level 1: Aggregate Data (Always Collected)

**This data is anonymous and aggregated—no individual tracking:**

**1. Card Scans (Aggregate)**

**Shared codes (inherently private):**
```
"Romantic Dinner shared code scanned 47 times this month"
```
- **What:** Total scans of shared public QR code
- **Why:** Hotel learns which topics are popular
- **Privacy:** Maximum privacy - CANNOT identify individuals (shared by everyone)

**Unique cards (trackable if hotel logs distribution):**
```
"3♥ card type was scanned 47 times this month across all physical cards"
"Card apple-bicycle-12345 was scanned 3 times"
```
- **What:** Scan count per card type (3♥, A♠, etc.) and per physical card token
- **Why:** Hotel learns which card types are popular; can track individual card usage
- **Privacy:** Card token is NOT linked to guest identity (unless hotel manually tracks distribution)

**2. Business Views (Aggregate)**
```
"Giuseppe's was viewed 230 times from 3♥ card scans this month"
```
- **What:** Total views per business (across all guests)
- **Why:** Hotel learns which recommendations get attention
- **Privacy:** No link to individual guests, no timestamps

**3. Guest Feedback (Aggregated)**
```
"Giuseppe's: 13 mentions, avg 4.7/5, ❤️ loved by 12 guests"
```
- **What:** Staff captures guest feedback mid-stay
- **Why:** Hotel learns what works (improve recommendations)
- **Privacy:** Individual comments are hotel-only. Guests only see aggregate count.

---

### Level 2: Individual Tracking (Opt-In Only - V2 Feature)

**This data is ONLY collected if guest explicitly opts in via "Share My Places" QR code:**

**⭐ Saved Places (Private to Guest)**
```
Guest saves: Giuseppe's, Cara Mia
→ Appears in "My Saved Places" (private list)
→ Hotel NEVER sees this unless guest shares
```
- **What:** Guest's private wishlist
- **Why:** So guest can remember what they wanted to try
- **Privacy:** Completely private. Guest must generate QR code to share.

**Guest-Initiated Sharing (Explicit Consent)**
```
Guest taps "Share My Places" → Generates QR code → Shows to staff
Staff scans QR code → Sees guest's saved list
```
- **What:** Guest's saved places (Giuseppe's, Cara Mia)
- **Why:** Staff can ask targeted questions ("Did you make it to Giuseppe's?")
- **Privacy:**
  - Guest initiates sharing (not hotel)
  - Obvious what's being shared (just saved list)
  - Time-limited (QR expires after 7 days)
  - Can share with hotel OR friends/family

---

## Privacy Levels Explained

### MVP: Option C (No Individual Features)

**What guest sees:**
```
┌─────────────────────────────────────────────────────┐
│ Welcome! Here are your romantic dinner spots:       │
│                                                     │
│ 🍝 Giuseppe's Ristorante ❤️ Loved by 12 guests     │
│ 📍 0.3 mi from hotel                                │
│ Italian • $$ • 0.3 miles                            │
│                                                     │
│ [Get Directions]                                    │
└─────────────────────────────────────────────────────┘
```

**What we collect:**
- Aggregate card scans: "3♥ scanned 47 times this month"
- Aggregate business views: "Giuseppe's viewed 230 times"
- Staff-captured feedback: "Guest said Giuseppe's was amazing" → internal 5/5 rating
- Aggregate count shown: "❤️ Loved by 12 guests"

**What we DON'T collect:**
- No individual clickstream ("Alice clicked Giuseppe's at 7:15pm")
- No personal info (name, email, phone)
- No location tracking
- No saved places (no ⭐ Save button in MVP)

**Result:** Complete privacy. Guest gets recommendations, hotel gets feedback loop, zero tracking.

---

### V2: Option B (Private Personalization)

**What guest sees:**
```
┌─────────────────────────────────────────────────────┐
│ Welcome! Here are your romantic dinner spots:       │
│                                                     │
│ 🍝 Giuseppe's Ristorante ❤️ Loved by 12 guests     │
│ 📍 0.3 mi • [⭐ Save]                                │
│                                                     │
│ 🍝 Lombardi's Trattoria ❤️ Loved by 8 guests       │
│ 📍 0.5 mi • [⭐ Save]                                │
└─────────────────────────────────────────────────────┘

Guest taps ⭐ Save → Saved to "My Saved Places" (private)
```

**What we collect:**
- Same as MVP (aggregate data)
- Guest's saved places (stored locally in browser, NOT on server)

**What we DON'T collect:**
- Hotel NEVER sees saved list (even if guest uses Save button)
- No sharing mechanism (guest keeps list private)

**Result:** Guest gets personalization, complete privacy from hotel.

---

### V2: Option A (Guest-Initiated Sharing)

**What guest sees:**
```
Same as Option B, but with additional "Share My Places" button:

┌─────────────────────────────────────────────────────┐
│ My Saved Places                                     │
│                                                     │
│ 🍝 Giuseppe's Ristorante                            │
│ 🍝 Cara Mia                                         │
│                                                     │
│ [Share My Places] ← Generates QR code               │
└─────────────────────────────────────────────────────┘
```

**What we collect:**
- Same as Option B (saved places private by default)
- IF guest generates QR code and shows to staff:
  - Staff sees: "Guest saved Giuseppe's, Cara Mia"
  - Staff can ask: "Did you make it to Giuseppe's?"
  - Staff enters feedback based on conversation

**What we DON'T collect:**
- Nothing shared unless guest explicitly generates QR code
- No automatic sharing
- No "opt-in prompt" (signals we don't track by default)

**Result:** Guest controls sharing. Hotel gets better feedback if guest opts in. Falls back gracefully if guest doesn't share.

---

## How This Compares to Competitors

| Feature | QRCards | TripAdvisor | Google Maps | Yelp | Foursquare |
|---------|---------|-------------|-------------|------|------------|
| **Account Required** | ❌ No | ✅ Yes | ⚠️ Optional | ⚠️ Optional | ✅ Yes |
| **App Install** | ❌ No (web) | ⚠️ Optional | ⚠️ Optional | ⚠️ Optional | ✅ Yes |
| **Location Tracking** | ❌ Never | ✅ Yes | ✅ Yes | ✅ Yes | ✅ Yes |
| **Check-Ins** | ❌ No | ❌ No | ⚠️ Reviews | ⚠️ Reviews | ✅ Core feature |
| **Personal Data** | ❌ None | ✅ Email, profile | ✅ Google account | ✅ Email, profile | ✅ Email, profile |
| **Data Sold** | ❌ Never | ⚠️ Yes (ads) | ⚠️ Yes (ads) | ⚠️ Yes (ads) | ⚠️ Yes (ads) |
| **GDPR Compliance** | ✅ Minimal | ⚠️ Complex | ⚠️ Complex | ⚠️ Complex | ⚠️ Complex |
| **Physical Keepsake** | ✅ Yes (card) | ❌ No | ❌ No | ❌ No | ❌ No |
| **Hospitality Focus** | ✅ Yes | ❌ No | ❌ No | ❌ No | ❌ No |

**Key Differentiators:**
1. **No app, no account** = Zero friction, zero personal data
2. **No location tracking** = No creepy surveillance
3. **Physical cards** = Tangible keepsake (guests take home, share with friends)
4. **Privacy-first** = Design principle, not afterthought
5. **Hospitality workflow** = Staff conversations, not check-ins
6. **Privacy paradox** = Public codes are inherently private; unique cards are trackable only if hotel chooses

---

## Technical Implementation

### How We Achieve Privacy

**1. Two Types of QR Codes: Shared vs Unique**

**Type A: Shared Public Codes (Inherently Private)**
```
QR code contains: https://mztape.com/hideaway-hotel-seattle/romantic-dinner-shared
                  ↑ custom hotel path   ↑ shared token (same for all guests)

Used in:
→ Tent cards at restaurants (public, anyone can scan)
→ Posters in hotel lobby (public, anyone can scan)
→ Printed materials left in rooms (shared across all guests)
→ "Clip and Save" strategy (14_CLIP_AND_SAVE.md)

Privacy characteristics:
→ Same token for everyone who scans it
→ INHERENTLY PRIVATE because it's PUBLIC
→ System CANNOT identify who scanned (could be any guest, or non-guest)
→ Tracks: "Shared code 'romantic-dinner-shared' scanned 47 times this month"
→ Cannot track: Who scanned it, when individual guests scanned

Result: Maximum privacy. Shared codes are anonymous by design.
```

**Type B: Unique Physical Cards (Inherently Trackable)**
```
QR code contains: https://mztape.com/hideaway-hotel-seattle/apple-bicycle-12345
                  ↑ custom hotel path   ↑ unique card token (per physical card)

Used in:
→ Physical cards handed to guests at check-in
→ Cards guests pick from shared display
→ Tangible keepsakes guests take home

Physical appearance:
→ All "3♥ Romantic Dinner" cards look identical (same design, same printed text)
→ Only difference: QR code contains unique token (apple-bicycle-12345 vs orange-sunset-67890)
→ Guest has no way to know their card is "unique" (looks mass-produced)

Privacy characteristics:
→ Each physical card gets its own unique token
→ Card token is NOT linked to guest at generation time
→ INHERENTLY TRACKABLE if hotel records which guest picked/received which card
→ Hotel CAN track: "Card apple-bicycle-12345 was scanned 3 times this week"
→ Hotel CANNOT identify WHO scanned it (unless they track distribution)

Result: Privacy depends on hotel practice. Trackable if hotel records distribution,
        anonymous if hotel treats like brochures.
```

**The Paradox:**
- **Public codes = MORE private** (shared by everyone, can't identify individuals)
- **Unique cards = LESS private** (one-to-one mapping possible if hotel tracks)

**When to Use Which:**

**Use Shared Codes when:**
- Privacy is paramount (guest never identifiable)
- Content is public/semi-public (tent cards, lobby posters)
- No need to track individual card usage
- Guest takes card home as keepsake but code is shared

**Use Unique Cards when:**
- Hotel wants usage analytics per card (e.g., "Card #17 gets scanned most, Card #8 never used")
- Inventory tracking (know which physical cards are in circulation)
- Possible to link card to guest (if hotel records distribution)
- Trade-off: Better operations data, but privacy depends on hotel practice

**Privacy Decision Tree:**
```
Does hotel need to track which physical card is which?
│
├─ NO → Use shared codes (one QR per card type, inherently private)
│   Example: All "3♥ Romantic Dinner" cards have same QR code
│   Privacy: Maximum (can't identify individuals)
│
└─ YES → Use unique cards (one QR per physical card, trackable if hotel logs distribution)
    Example: Card #1 = apple-bicycle-12345, Card #2 = orange-sunset-67890
    Privacy: Depends on hotel practice (trackable if they record who got which card)
```

---

**2. No Cookies (MVP)**
```
Mobile page loads → No session cookies set
Guest views recommendations → No tracking
Guest leaves → No data persisted
```

**Why:** Stateless by default. Recommendations work without sessions.

**3. Client-Side Storage Only (V2 - If Save Feature Added)**
```
Guest taps ⭐ Save → Saved to localStorage (browser)
localStorage is device-specific → NOT synced to server
Guest clears browser data → Saved places deleted (we don't have backup)
```

**Why:** Guest owns their data. We never see it unless they share.

**4. Anonymous Feedback**
```sql
CREATE TABLE guest_feedback (
  id UUID PRIMARY KEY,
  card_id UUID, -- "3♥" (not guest-specific)
  business_id UUID, -- Giuseppe's
  guest_token UUID, -- Random token (NOT linked to name/email)
  internal_rating INT, -- 1-5 (staff-assigned)
  text TEXT,
  created_at TIMESTAMP
);
```

**What's missing:**
- ❌ No guest_name
- ❌ No guest_email
- ❌ No room_number
- ❌ No IP address
- ❌ No device fingerprint

**Why:** We don't need to know WHO gave feedback. We just need to know WHAT was said.

**5. Staff Attribution (Not Guest)**
```
When staff captures feedback:
→ Staff member's ID recorded (for hotel tracking)
→ Guest identity NOT recorded
→ Hotel sees: "Sarah (front desk) captured this feedback"
→ Hotel does NOT see: "John Smith from Room 302 said this"
```

**Why:** Accountability for staff, privacy for guest.

---

**6. Hotel Best Practices: Guest Picks Card from Shared Pool**

**Typical workflow:**
```
Guest checks in
  ↓
Front desk: "Pick a card—we have recommendations for different interests"
  ↓
Guest picks 3♥ card from shared display/holder
  ↓
Guest takes card to room
```

**Privacy-first approach (recommended):**
```
Guest picks card from shared pool
  ↓
NO RECORD in system: "Room 302 picked card apple-bicycle-12345"
  ↓
Guest scans card → System tracks "apple-bicycle-12345 scanned 3 times"
  ↓
Hotel CANNOT identify: "That was Alice from Room 302"
  ↓
Result: Anonymous usage tracking
```

**Trackable approach (possible, likely, maybe desirable):**
```
Guest picks card from shared pool
  ↓
Front desk records: "Room 302 picked card apple-bicycle-12345" (manually or via PMS)
  ↓
Guest scans card → System tracks "apple-bicycle-12345 scanned"
  ↓
Hotel CAN identify: "Alice from Room 302 scanned this at 7:15pm"
  ↓
Result: Individual tracking (theoretically trackable, hard to prevent)
```

**Reality:**
- **Theoretically trackable:** Hotel can record which card guest picked (if they want to)
- **Hard to prevent:** If hotel wants to track card distribution, they can
- **Not automatic:** System doesn't force tracking, but hotel can add it to their workflow
- **Guest has agency:** Guest picks card (not assigned), so there's consent in selection
- **Hotel might want this:** Knowing "Room 302 picked Romantic Dinner and Cocktail Bars" signals guest interests
- **Trade-off:** Better personalization (hotel knows interests) vs privacy (guest remains anonymous)

**Best practice (our recommendation):**
- Don't track which guest picked which card (treat like picking up a brochure)
- Let guests take multiple cards if they want
- Mid-stay conversation: "Did you use any of our recommendation cards? Which one?" (guest self-reports)
- This maintains privacy-first spirit while acknowledging tracking is technically possible
- If hotel wants to track interests: Make it explicit ("We can note your preferences for future visits—would you like that?")

**Card Directory Feature (Important Privacy Protection + Age-Gating Challenge):**
```
Guest picks "3♥ Romantic Dinner" card from desk
  ↓
Scans QR code → Sees Romantic Dinner recommendations
  ↓
Taps "Card Directory" → Sees ALL available cards
  ↓
Switches to "Cocktail Bars" → AGE GATE REQUIRED (21+)
  ↓
Switches to "Cannabis Dispensaries" → AGE GATE REQUIRED (21+)
  ↓
Switches to "Adult Entertainment" → AGE GATE REQUIRED (18+ or 21+)
  ↓
Guest can explore ALL content without going back to desk
  (BUT must pass age verification for restricted content)
```

**What hotel knows:**
- ✅ Hotel knows: "Guest picked 3♥ Romantic Dinner card" (if they tracked distribution)
- ❌ Hotel does NOT know: Guest also viewed Cocktail Bars, Live Music, Coffee Shops
- **Privacy win:** Picking one card ≠ limiting guest to that content
- **Key insight:** Physical card is "entry point" but guest can browse everything

**Why this matters for privacy:**
- Even if hotel tracks "Room 302 picked Romantic Dinner card"
- Hotel CANNOT track: What else did guest explore via card directory
- Guest has privacy to explore all interests without front desk knowing
- Physical card choice signals ONE interest, but guest can explore others privately

**But: Age-gating creates new privacy considerations:**
- Card directory allows browsing ALL content (good for privacy)
- BUT some content is age-restricted (bars, dispensaries, adult businesses)
- Need age verification WITHOUT collecting personal data
- Challenge: How to gate content while maintaining privacy-first approach?

**Privacy spectrum:**
```
Most Private                                                    Least Private
│                                                                          │
Guest picks,                Guest picks,              Front desk asks
no tracking                 PMS tracks pick           "What interests you?"
(treat like brochure)       (for personalization)     then hands specific card
                            BUT guest can browse      + records in PMS
                            ALL cards via directory   + tracks all views
                            (other views private)
```

**Why guest-picking + card directory is better:**
- ✅ Guest has agency (they choose what interests them)
- ✅ Self-selection (not forced personalization)
- ✅ Natural workflow (like picking up a brochure)
- ✅ Can take multiple cards (not limited to one)
- ✅ Can explore all content digitally (via card directory, private from hotel)
- ⚠️ Initial card pick theoretically trackable (if hotel chooses to record distribution)
- ✅ But browsing behavior via card directory is private (hotel doesn't see it)

---

**7. Age-Gating for Restricted Content**

**The Challenge:**
- Card directory allows guests to browse ALL cards (privacy win)
- BUT some cards contain age-restricted content (bars, dispensaries, adult businesses)
- Need to prevent minors from accessing restricted content
- Must maintain privacy-first approach (no personal data collection)
- **Critical issue:** If parent picks up 21+ card, child can scan it → Need age gate at point of scan, not distribution

**Content Categories:**
```
All-Ages Content:
- ☕ Coffee shops
- 🥐 Breakfast spots
- 👨‍👩‍👧‍👦 Family activities
- 🏛️ Museums
- 🌳 Parks

21+ Content (Alcohol):
- 🍺 Cocktail bars (21+)
- 🍻 Breweries (21+)
- 🍷 Wine bars (21+)
- 💃 Nightclubs (21+)

21+ Content (Cannabis - where legal):
- 🌿 Dispensaries (21+)
- 🌿 Cannabis lounges (21+)
- 💊 CBD shops (18+)

18+ or 21+ (Adult Content):
- 🔞 Strip clubs (18+ or 21+)
- 🔞 Adult entertainment (18+)
- 🔞 Adult shops (18+)
```

---

**Recommended Solution: Password Gate (Simple, Cheap, Private)**

**How It Works:**
```
Guest receives all-ages cards only:
- ☕ Coffee Shops
- 🥐 Breakfast Spots
- 👨‍👩‍👧‍👦 Family Activities
- 🎵 Live Music
- etc.

21+ content only accessible via card directory with password
```

**Printed Collateral (Discreet Password Disclosure):**
```
On lobby materials, in-room guidebook, or welcome card:

"Explore all our recommendations by tapping Card Directory.

 For 21+ recommendations (bars, breweries, nightlife),
 enter password: nighttime"
```

**Digital Age Gate (In Card Directory):**
```
Guest taps "Card Directory" → Sees available cards
  ↓
Card directory shows:
- ☕ Coffee Shops
- 🥐 Breakfast Spots
- 👨‍👩‍👧‍👦 Family Activities
- 🎵 Live Music
- 🔒 21+ Recommendations (password required)
  ↓
Guest taps "🔒 21+ Recommendations"
  ↓
Prompt: "This section contains age-restricted content (bars, breweries, nightlife).
         You must be 21+ to access. Enter password:"
  ↓
[________] [Cancel] [Submit]
  ↓
If correct password → Shows 21+ cards:
  - 🍺 Cocktail Bars
  - 🍻 Breweries
  - 🌿 Dispensaries (where legal)
  - 💃 Nightclubs

If wrong password → "Incorrect password"
If Cancel → Return to card directory
```

**Why Password Is Better:**
- ✅ **Much cheaper:** No need to print restricted content cards for every guest
- ✅ **Discreet:** Adults see password on printed materials (lobby, room guidebook)
- ✅ **No front desk interaction:** Guest doesn't have to ask for 21+ cards
- ✅ **Parental control:** Children don't have password unless parent shares
- ✅ **Small barrier:** Prevents accidental access by minors
- ✅ **Privacy-first:** No tracking, no personal data, no age stored

**Privacy:**
- ✅ Zero data collection (password check is local, no logging)
- ✅ No tracking of who accessed 21+ content
- ✅ Stateless (password not stored in session)
- ✅ No cookies, no personal data

**Legal protection:**
- ✅ Good faith effort to prevent minor access
- ✅ Password acts as age barrier (similar to "Enter birthdate" on alcohol sites)
- ✅ Clear labeling on printed materials (21+ content)
- ✅ Hotel can show: "We gated content behind password disclosed only to adults"

**User experience:**
- ✅ Guest picks up any card → Scans → Browses card directory
- ✅ Sees password on lobby materials or in-room guidebook
- ✅ Enters password discreetly on phone (no front desk interaction)
- ✅ Access to all 21+ content without awkwardness

**Password Placement Options:**
```
Option 1: Lobby materials (near card display)
→ Discreet note: "21+ recommendations password: nighttime"

Option 2: In-room guidebook
→ Page about hotel amenities: "For nightlife recommendations, use password: nighttime"

Option 3: Check-in materials (for adults only)
→ Key card envelope or welcome card

Option 4: QR code on printed materials
→ Scan QR → Shows password page (only visible to person who scans)
```

**Sensitive Content (Extra Layer):**
For highly sensitive content (dispensaries, adult entertainment):

```
21+ section has two tiers:

Tier 1 (Password: "nighttime"):
- 🍺 Cocktail Bars
- 🍻 Breweries
- 💃 Nightclubs

Tier 2 (Password: "afterhours"):
- 🌿 Dispensaries (21+)
- 🔞 Adult Entertainment (18+)

"Afterhours" password only printed in-room (not in lobby)
Or: Not printed at all (must ask front desk discreetly)
```

**Cost Savings:**
- ❌ Don't print: Full decks with 21+ cards for every guest
- ✅ Do print: All-ages cards + one lobby sign with password
- **Result:** Significant cost savings on printing, no wasted restricted cards

---

**Last Resort: Room Key Integration (Only if Legally Required)**

```
Guest checks in → Hotel verifies ID (standard practice for age 21+)
  ↓
Hotel PMS records: "Guest is 21+" (boolean flag, not birthdate)
  ↓
Guest scans any QR card → URL includes room-key token or guest token
  ↓
System checks: "Is this guest 21+?" (query PMS)
  ↓
If yes → No age prompts shown (automatic access to all content)
If no → Age prompts shown for 21+ content or content hidden
```

**Privacy:**
- ❌ Requires linking card scan to guest identity (defeats privacy-first principle)
- ❌ Hotel knows: Which guest scanned which card
- ⚠️ May require account or room number entry
- ✅ Only stores boolean flag (21+ yes/no), not birthdate

**Legal protection:**
- ✅ Very strong - ID verified at check-in (standard hotel practice)
- ✅ System enforces age gating automatically

**User experience:**
- ✅ Zero friction - no prompts, automatic age gating
- ⚠️ Requires room key integration or guest identification

**Trade-off:**
- Better age verification, but sacrifices privacy-first architecture
- Only use if legal counsel advises it's necessary

---

**Age-Gating Summary:**

| Approach | Privacy | Legal Protection | User Experience | Cost | Recommended For |
|----------|---------|------------------|-----------------|------|-----------------|
| **Password Gate** | ✅ Maximum | ✅ Good | ✅ Excellent | ✅ Low | **MVP, recommended** |
| Two-Tier Password (sensitive content) | ✅ Maximum | ✅ Good | ✅ Good | ✅ Low | Dispensaries, adult content |
| Room Key Integration | ❌ Minimal | ✅ Very strong | ✅ Automatic | ⚠️ Medium | Last resort (legal requirement) |

**Best Practice (MVP):**
- **Print only all-ages cards** (☕ Coffee, 🥐 Breakfast, 👨‍👩‍👧‍👦 Family, 🎵 Live Music)
- **Password disclosed on printed materials:** "For 21+ recommendations, password: nighttime"
- **21+ content in card directory only:** Requires password to access
- **Cost savings:** No need to print 21+ cards for every guest
- **Privacy:** No tracking, no personal data, discreet access

**For Sensitive Content (Optional):**
- **Two-tier passwords:** "nighttime" (bars/breweries), "afterhours" (dispensaries/adult)
- **"Afterhours" disclosed in-room only** (not in lobby)

**Last Resort:**
- **Room key integration** (only if legal counsel requires verified age gating)

---

## Privacy as a Feature

### Marketing Message

**"Privacy-first recommendations. No app, no account, no tracking."**

**Landing Page Copy:**
```
Tired of apps that track everywhere you go?

QRCards is different:
• No app to download
• No account to create
• No location tracking
• No check-ins

Just scan a card, get recommendations, enjoy your stay.

Your privacy is not our product.
```

---

### Guest-Facing Messaging

**On mobile page (footer):**
```
🔒 Privacy: We don't track your location or require an account.
   Recommendations are curated by [Hotel Name], not algorithms.
   Feedback is aggregated—we never share individual reviews.
   [Learn more]
```

**On "Learn more" page:**
```
How QRCards Protects Your Privacy

✅ No app installation required
   Scan QR code with your phone's built-in camera.

✅ No account creation
   No username, no password, no email required.

✅ No location tracking
   We don't track where you go or how long you stay.

✅ No personal data
   We don't collect your name, email, phone, or credit card.

✅ Browse all recommendations privately
   Pick one card, but explore ALL cards via card directory.
   Hotel doesn't see what else you browse—your interests stay private.

✅ Aggregated feedback only
   When you share feedback, it's aggregated with other guests.
   Future guests see "Loved by 12 guests," not your individual review.

✅ You control sharing
   In V2, you can save places privately or share with hotel via QR code.
   Sharing is optional and explicit.

Questions? Email privacy@mztape.com
```

---

### Hotel-Facing Messaging

**Sales Pitch:**
```
"QRCards is privacy-first, which means:

1. No liability
   - You don't collect guest PII (name, email, phone)
   - No data breach risk
   - No GDPR/CCPA headaches

2. Guest-friendly
   - Guests love "no app, no account, no tracking"
   - Higher engagement (no friction)
   - Builds trust ("this hotel respects my privacy")

3. Better feedback
   - Guests feel safe sharing honest feedback
   - Staff conversations are more natural than online reviews
   - Mid-stay capture = higher quality data

Privacy is a feature, not a limitation."
```

---

## Privacy Policy (Plain English)

### What We Collect

**When you scan a QR card:**
- ✅ Card ID (e.g., "3♥") - tells us which card you scanned
- ✅ Timestamp (when you scanned)
- ❌ NOT your name, email, or phone number
- ❌ NOT your location

**When you view recommendations:**
- ✅ Aggregate view counts (e.g., "Giuseppe's was viewed 230 times this month")
- ❌ NOT individual clickstreams ("You clicked Giuseppe's at 7:15pm")

**When you give feedback:**
- ✅ Your comment and rating (shared with hotel staff only)
- ✅ Aggregated count (shown to future guests: "Loved by 12 guests")
- ❌ NOT your name or individual review (not shown to other guests)

**When you use Save feature (V2 only):**
- ✅ Saved places stored in your browser (client-side only)
- ❌ NOT synced to our servers (unless you share via QR code)

---

### How We Use Your Data

**Aggregate analytics:**
- Hotel sees: "3♥ card scanned 47 times this month"
- Hotel sees: "Giuseppe's viewed 230 times, loved by 12 guests"
- Purpose: Help hotel improve recommendations

**Feedback curation:**
- Hotel sees: Your feedback text + internal rating (1-5 stars)
- Hotel uses: To decide whether to keep/remove/update recommendations
- Future guests see: Aggregate count only ("Loved by 12 guests")

**We NEVER:**
- ❌ Sell your data to third parties
- ❌ Share individual reviews publicly
- ❌ Track your location
- ❌ Use data for advertising

---

### Your Rights

**You have the right to:**
- ✅ Use QRCards without creating an account
- ✅ Request deletion of your feedback (email privacy@mztape.com)
- ✅ Opt out of data collection (don't scan the card)
- ✅ Clear your saved places (clear browser data)

**GDPR (EU) and CCPA (California):**
- Minimal data collected = minimal compliance burden
- No personal data = no data breach risk
- Aggregate data = no individual tracking

---

### Contact

**Questions about privacy?**
- Email: privacy@mztape.com
- We respond within 48 hours
- We're transparent about what we collect and why

---

## Summary: Privacy as Competitive Advantage

**Most apps:**
- Require app installation, account creation, location tracking
- Collect personal data, sell to advertisers
- Complex GDPR/CCPA compliance
- Guest friction, privacy concerns

**QRCards:**
- No app, no account, no tracking (by design)
- Zero personal data collected (MVP)
- Minimal compliance burden
- Guest-friendly, trust-building

**Result:**
- ✅ Higher guest engagement (no friction)
- ✅ Better hotel reputation (respects privacy)
- ✅ No liability (no PII collected)
- ✅ Unique positioning (privacy-first recommendations)

**Tagline:**
"Privacy-first recommendations. No app, no account, no tracking."

---

**Document Version:** 1.2
**Date:** October 17, 2025
**Purpose:** Define privacy-first architecture as core feature and competitive advantage

**Key Insights:**
1. **Privacy is not a limitation—it's a selling point.** Guests want recommendations without surveillance. Hotels want feedback without liability. QRCards delivers both.
2. **The Privacy Paradox:** Public codes (shared QR) are inherently private because they're public. Unique cards (per-card QR) are trackable only if hotel records distribution.
3. **Card Directory enables privacy:** Guest picks one card but can browse all content digitally, without hotel seeing what else they explore.
4. **Age-gating solution:** Password gate for 21+ content. Print only all-ages cards (cost savings), disclose password on printed materials (e.g., "password: nighttime"), 21+ content accessible via card directory with password. Two-tier passwords for extra-sensitive content.
