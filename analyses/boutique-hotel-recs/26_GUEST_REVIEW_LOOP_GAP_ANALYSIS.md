# Guest Review Loop: Gap Analysis

## Executive Summary

**Current State:** ~0% of Guest Review Loop functionality exists in the QRCards codebase.

**What Exists:** Generic rating models (unused infrastructure only)

**What's Missing:** All core functionality - feedback capture, aggregation, staff interface, hotel dashboard, guest display

**Build Effort:** 1-2 weeks for MVP (24-40 hours)

**Recommendation:** Launch cards first (Month 0-1), add review loop in Month 2-3 after validating core product

---

## Business Plan Feature Description

The Guest Review Loop is described as a key innovation in the business plan:

**How it works:**
1. Guest scans QR card → sees recommendations + aggregate trust signal (❤️ "Loved by X guests")
2. Mid-stay: Staff asks "What were your favorite meals?" → captures 20-second note with internal 1-5 rating
3. If 4-5 stars → ❤️ love count increments for that business
4. Next guest sees: "Giuseppe's – ❤️ loved by 13 guests" (aggregate count only, no individual reviews)
5. Hotel dashboard shows data-driven insights: "Giuseppe's: 4.7/5 from 13 reviews = KEEP"
6. Recommendations improve over time through accumulated guest knowledge

**Value proposition:**
- Every guest becomes a secret shopper (unpaid quality control)
- Scales without concierge effort (system captures knowledge)
- Data-driven curation (hotels learn what works)
- Privacy-first (individual feedback hotel-only, guests see aggregates)

---

## Current State Analysis

### What EXISTS in QRCards Codebase

**Location:** `/home/ivanadmin/qrcards/packages/flasklayer/flasklayer/models/admin_models.py`

**Database Models Found:**
```python
# Lines 1093-1294

class Scale(BaseModel):
    """Generic rating scale (1-5, 1-10, etc.)"""
    __tablename__ = 'scale'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    min_value = Column(Integer)
    max_value = Column(Integer)

class Degree(BaseModel):
    """Individual rating points on a scale"""
    __tablename__ = 'degree'
    id = Column(Integer, primary_key=True)
    scale_id = Column(Integer, ForeignKey('scale.id'))
    value = Column(Integer)
    label = Column(String(255))

class ActivityRating(BaseModel):
    """Ratings for activities"""
    __tablename__ = 'activity_rating'
    id = Column(Integer, primary_key=True)
    activity_id = Column(Integer, ForeignKey('activity.id'))
    scale_id = Column(Integer, ForeignKey('scale.id'))
    degree_id = Column(Integer, ForeignKey('degree.id'))
    comment = Column(Text)
    created_at = Column(DateTime)

class DestinationRating(BaseModel):
    """Ratings for destinations"""
    __tablename__ = 'destination_rating'
    # Similar structure

class NeighborhoodRating(BaseModel):
    """Ratings for neighborhoods"""
    __tablename__ = 'neighborhood_rating'
    # Similar structure

class StaffDeck(BaseModel):
    """Placeholder for staff deck feature"""
    __tablename__ = 'staff_deck'
    id = Column(Integer, primary_key=True)
    token = Column(String(255))
    hotel_id = Column(Integer, ForeignKey('hotel.id'))
```

**Status:**
- ✅ Models exist in codebase
- ❌ Never imported or used
- ❌ No migrations applied (tables may not exist in database)
- ❌ No API endpoints reference these models
- ❌ No UI components use these models
- ❌ Generic structure (not hotel/business-specific)

**API Endpoints Found:**
- Location: Multiple Flask routes searched
- Result: 5 mock endpoints exist, but ZERO endpoints for review/feedback functionality
- Files checked:
  - `/home/ivanadmin/qrcards/packages/flasklayer/flasklayer/routes/`
  - No routes for: feedback submission, rating display, dashboard analytics

**UI Components:**
- Location: React/frontend code searched
- Result: NO components for:
  - Guest display showing "❤️ Loved by X guests"
  - Staff tablet interface for capturing feedback
  - Hotel dashboard showing ratings/trends

---

## Gap Analysis: What Needs to Be Built

### 1. Database Schema (Missing)

**Guest Feedback Table:**
```sql
CREATE TABLE guest_feedback (
  id UUID PRIMARY KEY,
  hotel_id UUID NOT NULL,
  card_id UUID NOT NULL,           -- e.g., "3♥" or specific card token
  business_id UUID NOT NULL,        -- Giuseppe's
  guest_token UUID,                 -- Anonymous (NOT linked to name/email)
  internal_rating INT NOT NULL,     -- 1-5 (staff-assigned, hotel-only)
  text TEXT,                        -- Guest's comment
  photos JSONB,                     -- Array of photo URLs
  status VARCHAR DEFAULT 'approved', -- "pending", "approved", "rejected"
  created_at TIMESTAMP DEFAULT NOW(),
  approved_at TIMESTAMP,
  captured_by VARCHAR DEFAULT 'staff' -- "staff" or "guest_online"
);
```

**Business Ratings Aggregate Table:**
```sql
CREATE TABLE business_ratings (
  id UUID PRIMARY KEY,
  hotel_id UUID NOT NULL,
  card_id UUID,                     -- e.g., "3♥" (optional: card-specific)
  business_id UUID NOT NULL,
  avg_internal_rating FLOAT,        -- 4.7 (for hotel dashboard only)
  total_mentions INT DEFAULT 0,     -- 13 (all feedback, any rating)
  favorite_count INT DEFAULT 0,     -- 12 (only 4-5 star ratings, shown to guests)
  last_updated TIMESTAMP DEFAULT NOW(),
  UNIQUE(hotel_id, business_id)     -- One aggregate per hotel-business pair
);
```

**Why these tables:**
- `guest_feedback`: Stores individual feedback (hotel-only, never shown to guests)
- `business_ratings`: Cached aggregates for fast display to guests
- Separates internal ratings (1-5 scale, hotel tracking) from public display (❤️ count)

---

### 2. API Endpoints (Missing)

**Staff Feedback Submission:**
```
POST /api/hotels/{hotel_id}/feedback
Body: {
  card_id: "3♥",
  business_id: "giuseppe-123",
  internal_rating: 5,
  text: "Carbonara incredible. Window table romantic.",
  captured_by: "staff"
}
Response: 201 Created
```

**Guest Display (Aggregate Counts):**
```
GET /api/cards/{card_token}/recommendations
Response: {
  recommendations: [
    {
      business_id: "giuseppe-123",
      name: "Giuseppe's Ristorante",
      favorite_count: 12,  // "❤️ Loved by 12 guests"
      ...
    }
  ]
}
```

**Hotel Dashboard Analytics:**
```
GET /api/hotels/{hotel_id}/analytics/ratings
Response: {
  ratings: [
    {
      business_name: "Giuseppe's Ristorante",
      avg_rating: 4.7,
      total_mentions: 13,
      favorite_count: 12,
      trend: "consistent",
      recommendation: "KEEP"
    },
    {
      business_name: "Java Junction",
      avg_rating: 2.4,
      total_mentions: 5,
      favorite_count: 1,
      trend: "declining",
      recommendation: "REMOVE"
    }
  ]
}
```

**Aggregate Update (Background Job):**
```python
# Runs after feedback submission
def update_business_ratings(hotel_id, business_id):
    """Recalculate aggregates for business"""
    feedback = db.query(guest_feedback)\
        .filter_by(hotel_id=hotel_id, business_id=business_id, status='approved')\
        .all()

    avg_rating = sum(f.internal_rating for f in feedback) / len(feedback)
    favorite_count = sum(1 for f in feedback if f.internal_rating >= 4)

    db.update(business_ratings,
        avg_internal_rating=avg_rating,
        total_mentions=len(feedback),
        favorite_count=favorite_count,
        last_updated=NOW())
```

---

### 3. UI Components (Missing)

**Guest Display: "❤️ Loved by X guests"**

Location: Guest-facing mobile page (scan QR card)

```jsx
// Component: RecommendationCard.jsx
function RecommendationCard({ business }) {
  return (
    <div className="business-card">
      <h3>{business.name}</h3>
      <p>{business.description}</p>

      {business.favorite_count > 0 && (
        <div className="trust-signal">
          ❤️ Loved by {business.favorite_count} guests
        </div>
      )}

      <button>Get Directions</button>
    </div>
  );
}
```

**Staff Interface: Feedback Capture Form**

Location: Staff tablet or hotel admin panel

```jsx
// Component: StaffFeedbackForm.jsx
function StaffFeedbackForm({ cardId, businesses }) {
  const [selectedBusiness, setSelectedBusiness] = useState(null);
  const [rating, setRating] = useState(0);
  const [comment, setComment] = useState('');

  const handleSubmit = async () => {
    await fetch('/api/hotels/123/feedback', {
      method: 'POST',
      body: JSON.stringify({
        card_id: cardId,
        business_id: selectedBusiness.id,
        internal_rating: rating,
        text: comment,
        captured_by: 'staff'
      })
    });

    // Clear form, show success message
  };

  return (
    <form>
      <select onChange={e => setSelectedBusiness(businesses[e.target.value])}>
        <option>Select business...</option>
        {businesses.map(b => <option key={b.id}>{b.name}</option>)}
      </select>

      <div className="star-rating">
        {[1,2,3,4,5].map(star => (
          <button onClick={() => setRating(star)}>
            {star <= rating ? '★' : '☆'}
          </button>
        ))}
      </div>

      <textarea
        placeholder="What did the guest say?"
        value={comment}
        onChange={e => setComment(e.target.value)}
      />

      <button onClick={handleSubmit}>Submit Feedback</button>
    </form>
  );
}
```

**Hotel Dashboard: Ratings & Trends**

Location: Hotel admin dashboard

```jsx
// Component: RatingsDashboard.jsx
function RatingsDashboard({ hotelId }) {
  const [ratings, setRatings] = useState([]);

  useEffect(() => {
    fetch(`/api/hotels/${hotelId}/analytics/ratings`)
      .then(res => res.json())
      .then(data => setRatings(data.ratings));
  }, [hotelId]);

  return (
    <div className="dashboard">
      <h2>Recommendation Performance</h2>

      <table>
        <thead>
          <tr>
            <th>Business</th>
            <th>Avg Rating</th>
            <th>Mentions</th>
            <th>❤️ Count</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {ratings.map(r => (
            <tr key={r.business_id}>
              <td>{r.business_name}</td>
              <td>{r.avg_rating.toFixed(1)}/5</td>
              <td>{r.total_mentions}</td>
              <td>{r.favorite_count}</td>
              <td className={r.recommendation === 'KEEP' ? 'keep' : 'remove'}>
                {r.recommendation}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
```

---

## Build Effort Estimates

### MVP (1-2 weeks total)

**Phase 1: Database & API (24-32 hours)**
- Create database tables: 4 hours
- Write migrations: 2 hours
- API endpoint: Staff feedback submission: 6 hours
- API endpoint: Guest display (with aggregates): 6 hours
- API endpoint: Hotel dashboard analytics: 6 hours
- Background job: Update aggregates: 4 hours
- Testing: 4 hours

**Phase 2: UI Components (12-20 hours)**
- Guest display: "❤️ Loved by X guests": 4 hours
- Staff tablet form: 6 hours
- Hotel dashboard: 8 hours
- Testing/polish: 2-4 hours

**Total MVP: 36-52 hours (1-2 weeks for solo developer)**

---

### V2 Features (Optional, Post-MVP)

**Guest-Submitted Reviews (Month 3+):**
- Online review form for guests: 8 hours
- Email trigger after visit: 4 hours
- Approval workflow (pending → approved): 6 hours
- Photo upload: 4 hours
- Total: ~22 hours

**Advanced Analytics (Month 6+):**
- Trend analysis (ratings over time): 8 hours
- Common themes extraction (NLP): 12 hours
- Comparison across cards: 6 hours
- Export reports: 4 hours
- Total: ~30 hours

**AI Recommendations (Year 2):**
- Suggest which businesses to add/remove: 16 hours
- Auto-categorize feedback sentiment: 12 hours
- Total: ~28 hours

---

## Implementation Roadmap

### Option 1: Build Now (High Risk)

**Timeline:**
- Month 0: Build review loop MVP (1-2 weeks)
- Month 0: Test with 10 pilot hotels (2 weeks)
- Month 1: Launch with full feature set

**Risks:**
- Delays launch by 2-4 weeks
- Building feature before validating core product (cards)
- Hotels may not use feedback capture (wasted effort)
- Complexity may scare away early adopters

**When to choose:** If pilot hotels explicitly request feedback tracking

---

### Option 2: Phase It (Recommended - Low Risk)

**Timeline:**
- Month 0-1: Launch cards ONLY (no review loop)
  - Focus: Cards, recommendations, staff workflow
  - Validate: Hotels will hand out cards, guests will scan

- Month 2-3: Add review loop if demand exists
  - Build MVP (1-2 weeks)
  - Validate: Hotels want data-driven curation

- Month 6+: Add advanced features (V2)
  - Guest-submitted reviews
  - Advanced analytics
  - AI recommendations

**Benefits:**
- Faster initial launch (no delay)
- Validates core product first
- Only builds review loop if hotels want it
- Can gather requirements from pilot hotels

**When to choose:** Default approach (recommended)

---

### Option 3: Manual Tracking (Interim Solution)

**Timeline:**
- Month 0-3: Hotels track feedback manually (spreadsheet)
- Month 3-6: Build review loop based on manual tracking learnings

**How it works:**
- Staff asks mid-stay: "Any favorite meals?"
- Staff records in Google Sheet: Business, Rating 1-5, Comment
- Founder manually updates aggregate counts in CMS
- Hotels see value before automated system built

**Benefits:**
- Zero development time
- Validates feedback loop value proposition
- Builds requirements from real usage
- Can launch immediately

**Drawbacks:**
- Manual effort for founder
- Doesn't scale beyond 10-20 hotels
- No hotel dashboard (manual reports only)

**When to choose:** Bootstrap mode, need to launch ASAP

---

## Business Plan Impact

### Current Business Plan Language (Misleading)

**"Our solution" section says:**
> "Guest Review Loop: Guests review recommended businesses during checkout... Hotel dashboard shows data-driven insights... Recommendations improve over time"

**Problem:** Implies feature exists now, which is false.

---

### Recommended Changes to Business Plan

**Option A: Honest About Build Status**

Change "Our solution" section to:
> "Guest Review Loop (MVP: Month 2-3): After validating core product, we'll add a feedback system where staff captures guest feedback mid-stay. Hotel dashboard will show data-driven insights. Recommendations improve over time through accumulated guest knowledge."

Add to Milestones:
```
Month 2-3: Build Guest Review Loop MVP
[ ] Database tables: guest_feedback, business_ratings
[ ] API endpoints: feedback submission, aggregate display
[ ] UI components: staff form, hotel dashboard, guest display
[ ] Success criteria: 50% of pilot hotels actively capture feedback
Budget: $0 (founder builds, 1-2 weeks)
```

**Option B: Position as Differentiator (Still Honest)**

Keep current description but add footnote:
> "Guest Review Loop: [description]"
>
> *Note: Review loop will be built in Month 2-3 after validating core product with pilot hotels. This feature is our key differentiator—none of our competitors offer data-driven recommendation curation.*

**Option C: Manual Tracking as MVP**

Change to:
> "Guest Review Loop: Staff captures feedback mid-stay ('Any favorite meals?'). In Month 0-3, hotels track in spreadsheet; we manually update aggregate counts. Month 3+ we automate with hotel dashboard showing trends. Recommendations improve through accumulated guest knowledge."

---

## Recommendations

### For Business Plan

**Use Option B:** Position as differentiator, note it's built in Month 2-3

**Rationale:**
- Honest about build status
- Still a competitive advantage (competitors don't have it either)
- De-risks launch (focus on cards first)
- Can gather requirements from pilot hotels

### For Implementation

**Use Option 2 (Phased Approach):**
1. Month 0-1: Launch cards only (no review loop)
2. Month 2-3: Build review loop MVP (1-2 weeks)
3. Month 6+: Add V2 features (guest-submitted reviews, analytics)

**With interim Option 3 (Manual Tracking):**
- Month 0-3: Hotels use Google Sheet to track feedback
- Founder manually updates aggregate counts in CMS
- Validates value before building automation

**Rationale:**
- Fastest path to market
- Validates core product before building complex features
- Builds requirements from real usage
- Can always accelerate if demand is high

### For Pilot Hotels

**Set expectations clearly:**
- "Cards work now, ready to hand out"
- "Feedback tracking starts Month 2 (we'll add dashboard)"
- "For now, let's track manually to learn what you need"

**Benefits:**
- No overpromising
- Builds trust (underpromise, overdeliver)
- Can launch immediately

---

## Appendix: Code Locations

### Database Models (Unused)
- **File:** `/home/ivanadmin/qrcards/packages/flasklayer/flasklayer/models/admin_models.py`
- **Lines:** 1093-1294
- **Models:** Scale, Degree, ActivityRating, DestinationRating, NeighborhoodRating, StaffDeck

### API Routes (No Feedback Endpoints)
- **Directory:** `/home/ivanadmin/qrcards/packages/flasklayer/flasklayer/routes/`
- **Status:** 5 mock endpoints exist, 0 feedback/rating endpoints

### Frontend Components (None for Feedback)
- **Search Results:** No components found for:
  - Guest display showing "❤️ Loved by X guests"
  - Staff feedback capture form
  - Hotel dashboard

---

**Document Version:** 1.0
**Date:** October 17, 2025
**Purpose:** Gap analysis for Guest Review Loop feature vs QRCards codebase
**Key Finding:** ~0% built; 1-2 weeks to MVP; recommend phased approach (launch cards first, add review loop Month 2-3)
