# Product Roadmap: Future Features

## Overview

This document outlines features planned for future releases after the core product (cards + recommendations + staff workflow) is validated with pilot hotels.

---

## Guest Review Loop

**Timeline:** Month 2-3 after validating core product with pilot hotels

**Status:** Planned (not yet built)

**Build Effort:** 1-2 weeks MVP

**See also:** [26_GUEST_REVIEW_LOOP_GAP_ANALYSIS.md](./26_GUEST_REVIEW_LOOP_GAP_ANALYSIS.md) for implementation details

---

### The Problem: How Recommendations Are Currently Given

**Hard Recs (Concierge-arranged):**
- Concierge makes reservation, has restaurant relationship
- Tight feedback loop: concierge hears "How was dinner?" at checkout
- Works well, but doesn't scale (limited to front desk hours)

**Soft Recs (Handouts, verbal suggestions):**
- "Here are some spots near the Space Needle you might try"
- NO feedback loop: hotel never learns what worked
- Recommendations stagnate (same photocopied list for years)

**The Gap:** Soft recs have no feedback mechanism, leading to stale recommendations and missed opportunities for improvement.

---

### The Solution: mztape™ Guest Review Loop

mztape™ for guests introduces feedback for soft recs, while strengthening the loop for hard recs.

**How It Works:**

1. **Guest sees aggregate trust signals**
   - Guest scans QR card → sees recommendations + aggregate trust signal (❤️ "Loved by X guests")
   - Example: "Giuseppe's – ❤️ loved by 13 guests"

2. **Staff captures feedback mid-stay**
   - Staff asks: "What were your favorite meals?"
   - Staff captures 20-second note with internal 1-5 rating
   - Low friction: verbal conversation, not forms

3. **System updates aggregates**
   - If 4-5 stars → ❤️ love count increments for that business
   - Next guest sees updated count: "Giuseppe's – ❤️ loved by 14 guests"
   - Aggregate count only, no individual reviews shown to guests

4. **Hotel learns and curates**
   - Hotel dashboard shows internal ratings and trends
   - Hotel learns what works, removes spots getting negative feedback
   - Data-driven decisions replace gut feelings

5. **Continuous improvement**
   - Recommendations improve over time (data-driven, privacy-first)
   - Every guest becomes a secret shopper (unpaid quality control)
   - Scales without concierge effort (system captures knowledge, shared across team)

---

### Value Proposition

**Result:** Soft recs become data-driven and self-improving, filling the gap between "expensive concierge service" and "stale photocopied handout."

**Benefits:**
- **For Hotels:** Data-driven curation, quality control, no added staff time
- **For Guests:** Trust signals from peer recommendations, better recommendations over time
- **Competitive Advantage:** None of our competitors offer this feature

---

### Technical Requirements

**MVP Scope (Month 2-3):**
- Database tables: `guest_feedback`, `business_ratings`
- API endpoints: Staff feedback submission, guest aggregate display, hotel dashboard
- UI components: Guest display (❤️ count), staff form, hotel dashboard

**See:** [26_GUEST_REVIEW_LOOP_GAP_ANALYSIS.md](./26_GUEST_REVIEW_LOOP_GAP_ANALYSIS.md) for detailed implementation plan

---

### Implementation Strategy

**Phase 1: Manual Tracking (Month 0-3)**
- Hotels track feedback in Google Sheet
- Founder manually updates aggregate counts in CMS
- Validates value proposition before building automation

**Phase 2: Automated System (Month 2-3)**
- Build MVP (1-2 weeks)
- Staff tablet interface for feedback capture
- Hotel dashboard showing trends and recommendations
- Automatic aggregate updates

**Phase 3: Advanced Features (Month 6+)**
- Guest-submitted reviews (online form)
- Advanced analytics (trends, common themes)
- AI-powered recommendations (suggest what to add/remove)

---

### Privacy Considerations

**Privacy-First Design:**
- Individual feedback is hotel-only (never shown to other guests)
- Guests see only aggregate counts: "❤️ Loved by X guests"
- No guest identification required
- Internal ratings (1-5 stars) for hotel tracking only
- Public display: Only 4-5 star ratings shown as aggregate count

**See:** [25_PRIVACY.md](./25_PRIVACY.md) for complete privacy architecture

---

### Success Metrics

**Validation Criteria (Month 2):**
- 50% of pilot hotels actively capture feedback
- Average 3+ feedback entries per hotel per week
- Hotel reports using data to make curation decisions

**Rollout Criteria (Month 3):**
- <5 minutes to capture feedback (staff time)
- Positive feedback from hotel staff (ease of use)
- Guests notice and trust aggregate counts

---

## Future Features (Beyond Guest Review Loop)

### PMS Integration (Month 6-9)
- Sync with Property Management Systems (Cloudbeds, Mews)
- Auto-link cards to guest reservations
- Pre-arrival card customization based on guest profile

### Mobile App (Month 9-12)
- Native iOS/Android app (optional, web works well)
- Offline access to recommendations
- Push notifications for new recommendations

### Publishing Platform (Year 2)
- Hotels publish digital guidebooks
- Print-on-demand option (30% revenue share)
- White-label for luxury properties

### AI Recommendations (Year 2)
- Auto-suggest businesses to add based on guest preferences
- Sentiment analysis of feedback comments
- Predictive analytics: "This restaurant quality is declining"

---

**Document Version:** 1.0
**Date:** October 17, 2025
**Purpose:** Roadmap of future features planned after core product validation
**Next Update:** After Month 0 pilot results
