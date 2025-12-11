# QRCards Implementation Plan: Decision Analysis Pages

**Target Pages**:
- https://cfo.inversefractional.com/decision-analysis (CFO audience)
- https://app.ivantohelpyou.com/decision-analysis (General business audience)

**Future Domains** (same structure):
- https://cto.inversefractional.com (CTO/engineering audience)
- https://cmo.inversefractional.com (CMO/marketing audience)
- Additional role-specific subdomains as needed

**Implementation Tool**: QRCards with Augment agent
**Date**: November 12, 2025
**Updated Price**: $99 per session
**URL Structure**: Flat (no hierarchy in paths)

---

## Overview

Progressive enhancement of decision analysis pages across multiple audience-specific domains with:

1. **Case Studies** - Added as completed, showcasing real decision analysis work
2. **Research-Based Category Pages** - Flat URLs (e.g., `/fpa-platforms`, `/data-warehouse`)
3. **Interactive Flip Cards** - "What would YOU choose?" decision trees on category pages
4. **Landing Page Strategy** - Category pages act as both research content AND lead generation
5. **Multi-Domain Architecture** - Role-specific subdomains with shared content, audience-specific tone

---

## Multi-Domain Architecture

### Domain Strategy

**Role-Specific Subdomains** (audience segmentation):
```
cfo.inversefractional.com       → CFO/finance audience
cto.inversefractional.com       → CTO/engineering audience
cmo.inversefractional.com       → CMO/marketing audience
app.ivantohelpyou.com           → General business audience (existing)
```

**Same Content, Different Tone**:
- URL structure identical across domains
- Category pages shared (FP&A, Data Warehouse, etc.)
- Tone/copy adjusted per audience in components
- Analytics track which domain drives conversions

**Example**:
```
cfo.inversefractional.com/fpa-platforms
→ "CFO Decision Analysis: Which FP&A Platform Fits Your Budget?"
→ Focus: TCO, ROI, financial impact

cto.inversefractional.com/fpa-platforms
→ "Technical Analysis: FP&A Platform Architecture & Integrations"
→ Focus: APIs, data models, technical debt

cmo.inversefractional.com/fpa-platforms
→ "Marketing Ops: FP&A Platforms for Campaign ROI Tracking"
→ Focus: Attribution, marketing metrics, campaign planning
```

---

## Page Architecture

### Primary Pages (Already Live)

**Domain 1**: https://cfo.inversefractional.com
- **Audience**: CFOs, finance leaders at $5M-$500M companies
- **Tone**: Executive, high-level, ROI-focused
- **Routes**:
  - `/decision-analysis` - Main service page
  - `/fpa-platforms` - FP&A category (FLAT URL)
  - `/data-warehouse` - Data warehouse category (FLAT URL)
  - `/accounting-software` - Future category (FLAT URL)

**Domain 2**: https://app.ivantohelpyou.com
- **Audience**: General business audience, broader decision-makers
- **Tone**: Accessible, educational, methodology-focused
- **Routes**: Same as cfo.inversefractional.com (identical structure)

**Domain 3**: https://cto.inversefractional.com (Future)
- **Audience**: CTOs, VPs Engineering, technical decision-makers
- **Tone**: Technical, architecture-focused, integration-heavy
- **Routes**: Same structure, different copy emphasis

**Domain 4**: https://cmo.inversefractional.com (Future)
- **Audience**: CMOs, VPs Marketing, growth leaders
- **Tone**: Growth-focused, metrics-driven, campaign-oriented
- **Routes**: Same structure, marketing-specific angle

**Relationship**: Same service, multiple audience entry points

---

### New Category Pages (Research Landing Pages)

Create category-specific pages with **FLAT URL STRUCTURE** that serve dual purpose:

**Purpose 1: Research Showcase**
- Deep dive into specific category (FP&A, Data Warehouse, etc.)
- Interactive flip cards with scenarios
- Links to full spawn-solutions research

**Purpose 2: Lead Generation**
- Standalone landing page for targeted marketing
- QR code destination (physical postcards)
- Category-specific CTAs

**Purpose 3: Multi-Audience Flexibility**
- Same URL structure across all role-specific domains
- Audience-specific tone/copy via domain detection
- Shared components with audience props

---

## URL Structure: Flat (No Hierarchy)

**Decision**: Use flat URLs for category pages (not nested under /decision-analysis)

**Rationale**:
1. **Shorter URLs** - Better for QR codes, easier to share
2. **SEO-friendly** - Top-level pages have more authority
3. **Standalone marketing** - Each category is independent landing page
4. **Multi-domain ready** - Same structure works across cfo/cto/cmo subdomains

**URL Pattern Across All Domains**:
```
{domain}/decision-analysis      → Main service page
{domain}/fpa-platforms          → FP&A decision tree (FLAT)
{domain}/data-warehouse         → Data warehouse decision tree (FLAT)
{domain}/accounting-software    → Accounting decision tree (FLAT)
{domain}/hris-hcm              → HRIS decision tree (FLAT)

Where {domain} = cfo|cto|cmo.inversefractional.com or app.ivantohelpyou.com
```

**Examples**:
```
CFO Audience:
https://cfo.inversefractional.com/decision-analysis
https://cfo.inversefractional.com/fpa-platforms
https://cfo.inversefractional.com/data-warehouse

CTO Audience (future):
https://cto.inversefractional.com/decision-analysis
https://cto.inversefractional.com/fpa-platforms
https://cto.inversefractional.com/data-warehouse

CMO Audience (future):
https://cmo.inversefractional.com/decision-analysis
https://cmo.inversefractional.com/fpa-platforms
https://cmo.inversefractional.com/data-warehouse

General Audience:
https://app.ivantohelpyou.com/decision-analysis
https://app.ivantohelpyou.com/fpa-platforms
https://app.ivantohelpyou.com/data-warehouse
```

**Hierarchy Shown Via**:
- Breadcrumbs: `Home › Decision Analysis › FP&A Platforms`
- Navigation: Visual grouping under "Decision Analysis"
- Structured data: Schema.org metadata
- Internal linking: Cross-references between pages

---

## Implementation Phases

### Phase 1: Case Studies Section (Both Main Pages)

**Goal**: Add case studies to both decision analysis pages as they're completed

**Scope**:
- Create `CaseStudyCard` component (reusable)
- Section on both pages: "Decision Analysis in Action"
- Horizontal scrollable cards (2-3 visible, more off-screen)
- Progressive: Start with 1 case study, add more as completed

**Case Study Card Structure**:
```jsx
<CaseStudyCard
  title="Saved $60K/year choosing Prophix over Adaptive"
  client="$80M Manufacturing Company"
  challenge="Replace Excel-based FP&A with enterprise platform"
  finalists={["Adaptive", "Planful", "Prophix"]}
  methodology={[
    "Integration requirements mapping",
    "3-year TCO comparison",
    "Implementation timeline analysis",
    "Feature trade-off quantification"
  ]}
  outcome="Prophix selected"
  result="$60K/year savings vs Adaptive"
  roi="3-month payback"
  link="/case-studies/manufacturing-fpa" // Optional deep dive
  cta="Book $99 Decision Analysis"
/>
```

**Data Source**: JSON file in QRCards project
```json
// qrcards/data/case-studies.json
{
  "case_studies": [
    {
      "id": "manufacturing-fpa",
      "title": "Saved $60K/year choosing Prophix over Adaptive",
      "client": {
        "industry": "Manufacturing",
        "size": "$80M revenue",
        "anonymized": true
      },
      "challenge": "Replace Excel-based FP&A with enterprise platform",
      "finalists": ["Adaptive Insights", "Planful", "Prophix"],
      "methodology": [
        "Integration requirements mapping (NetSuite ERP)",
        "3-year TCO comparison ($345K vs $405K vs $465K)",
        "Implementation timeline analysis (12-16 weeks)",
        "Feature trade-off quantification (automation value $63K-126K)"
      ],
      "outcome": "Prophix selected",
      "result": "$60K/year savings vs Adaptive",
      "roi": "3-month payback period",
      "research_source": "3.007-fpa-platforms/S3-need-driven/manufacturing-500-employees.md",
      "date": "2025-11-01"
    },
    {
      "id": "werise-engagement",
      "title": "TBD - WeRise Restaurant Platform Decision",
      "client": {
        "industry": "Hospitality/Restaurant",
        "size": "TBD",
        "anonymized": false
      },
      "challenge": "TBD",
      "status": "in_progress",
      "date": "2025-11-XX"
    }
  ]
}
```

**Progressive Enhancement**:
1. Start with 1 case study (manufacturing FP&A from research)
2. Add WeRise case study when completed (task #74-103 in decision-analysis.yaml)
3. Add new case studies as engagements complete
4. No redesign needed - just add new `CaseStudyCard` to array

**Implementation**:
- [ ] Create `CaseStudyCard.tsx` component
- [ ] Create `case-studies.json` data file
- [ ] Add "Decision Analysis in Action" section to both pages
- [ ] Wire up horizontal scroll (mobile: swipe, desktop: arrow buttons)
- [ ] Add first case study (manufacturing FP&A)

**Effort**: 3-4 hours

---

### Phase 2: FP&A Platforms Sub-Page

**Goal**: Create standalone landing page with interactive flip cards for FP&A platform decisions

**URL**:
- https://cfo.inversefractional.com/fpa-platforms
- https://app.ivantohelpyou.com/fpa-platforms

**Page Structure**:

```
┌─────────────────────────────────────────────┐
│ HERO SECTION                                │
│                                             │
│ "Which FP&A Platform is Right for YOU?"    │
│                                             │
│ Based on 13,700 lines of research across   │
│ 9 platforms | 82 features compared         │
│                                             │
│ [Book Decision Analysis $99]               │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ INTERACTIVE FLIP CARDS (3×3 Grid)          │
│                                             │
│ "What Would YOU Choose?"                   │
│                                             │
│ [Card 1] [Card 2] [Card 3]                 │
│ [Card 4] [CTA 5] [Card 6]                  │
│ [Card 7] [Card 8] [Card 9]                 │
│                                             │
│ Click any scenario to see recommendation   │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ METHODOLOGY SECTION                         │
│                                             │
│ "How We Analyze FP&A Platforms"            │
│                                             │
│ ✓ Integration requirements (eliminates 70%)│
│ ✓ Budget constraints (narrows to 2-4)      │
│ ✓ Implementation timeline                   │
│ ✓ Feature trade-offs (quantified)          │
│                                             │
│ [Learn More About Our Process]             │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ PLATFORM OVERVIEW (9 Platforms)            │
│                                             │
│ Tier 1 (Startup): Runway, Causal           │
│ Tier 2 (Growth): Cube, Vena, Prophix       │
│ Tier 3 (Enterprise): Planful, Adaptive,    │
│                      OneStream, Anaplan     │
│                                             │
│ [View Full Comparison Matrix]              │
└─────────────────────────────────────────────┘

┌─────────────────────────────────────────────┐
│ CTA SECTION                                 │
│                                             │
│ "Not Sure Which Scenario Matches You?"     │
│                                             │
│ Book a $99 Decision Analysis session       │
│ Custom analysis for YOUR specific context  │
│                                             │
│ [Book Now] [View Case Studies]             │
└─────────────────────────────────────────────┘
```

**Data Source**: JSON file (already structured in proposal)
```json
// qrcards/data/decision-trees/fpa-platforms.json
{
  "category": "FP&A Platforms",
  "research_source": "3.007-fpa-platforms",
  "research_depth": "13,700 lines, 9 platforms, 82 features",
  "last_updated": "2025-11-05",
  "scenarios": [
    {
      "id": 1,
      "front": {
        "title": "Seed Startup",
        "details": ["15 employees", "Rippling HRIS", "$3M revenue"],
        "icon": "fa-user-laptop"
      },
      "back": {
        "recommendation": "RUNWAY",
        "rationale": [
          "Rippling integration",
          "Fast: 1-2 weeks",
          "$5K-8K/year"
        ],
        "tier": 1,
        "confidence": "High",
        "research_link": "/research/fpa-platforms/seed-startup"
      }
    }
    // ... 8 more scenarios (from proposal)
  ],
  "platforms": [
    {
      "name": "Runway",
      "tier": 1,
      "price_range": "$5K-15K/year",
      "best_for": "Startup 15-200 employees",
      "key_features": ["HRIS integration", "Headcount planning", "Scenario modeling"]
    }
    // ... 8 more platforms
  ]
}
```

**Components**:
1. `FlipCardGrid.tsx` - 3×3 responsive grid
2. `FlipCard.tsx` - Individual card with CSS flip animation
3. `CTACard.tsx` - Center card (position 5), no flip
4. `PlatformOverview.tsx` - Platform tier visualization
5. `MethodologySection.tsx` - Decision framework explanation

**Content Source**:
- Flip card content: `/home/ivanadamin/spawn-solutions/calendar/decision-trees/fpa-platforms-postcard-copy.md`
- Methodology: `/home/ivanadamin/spawn-solutions/research/3.007-fpa-platforms/01-discovery/S3-need-driven/synthesis.md`

**QR Code Integration**:
- Physical postcard QR codes point to this page
- URL parameter tracking: `?source=FPA-001` (from postcard)
- Analytics: Track conversions from physical cards

**Implementation**:
- [ ] Create sub-page route in QRCards
- [ ] Extract flip card content to JSON
- [ ] Build `FlipCardGrid` + `FlipCard` components
- [ ] Add methodology section
- [ ] Add platform overview
- [ ] Test QR code → landing page flow
- [ ] Deploy to both domains

**Effort**: 8-12 hours

---

### Phase 3: Data Warehouse Sub-Page

**Goal**: Second research landing page for data warehouse decisions

**URL**:
- https://cfo.inversefractional.com/data-warehouse
- https://app.ivantohelpyou.com/data-warehouse

**Structure**: Same as FP&A sub-page (reuse components)

**New Work Required**:
1. Create S3 scenarios for 3.044 (6-8 scenarios)
2. Write scenario descriptions (front side)
3. Write recommendations (back side)
4. Extract to JSON

**Scenarios** (proposed):
1. Seed startup (100GB, QBO) → BigQuery
2. SaaS scale-up (5TB, analytics team) → Snowflake
3. Data-intensive (clickstream, IoT) → ClickHouse
4. ML-heavy (feature store) → Databricks
5. Multi-cloud (AWS + GCP) → BigQuery or Snowflake
6. Cost-conscious (open source) → ClickHouse
7. Enterprise (complex governance) → Snowflake
8. Real-time analytics (sub-second) → ClickHouse

**Data Source**:
- Platform research: `/home/ivanadmin/spawn-solutions/research/3.044-data-warehouse/01-discovery/S1-rapid/`
- Need to create: S3 scenarios (follow 3.007 methodology)

**Implementation**:
- [ ] Write 6-8 S3 scenarios for data warehouse
- [ ] Create `data-warehouse.json` flip card data
- [ ] Reuse FlipCardGrid components
- [ ] Add data warehouse-specific methodology section
- [ ] Deploy to both domains

**Effort**: 10-14 hours (includes S3 scenario creation)

---

### Phase 4: Additional Category Sub-Pages

**Future Categories** (prioritize based on demand):
1. Accounting Software (3.006)
2. HRIS/HCM (3.503)
3. Team Task Management (3.131)

**Each Requires**:
- S3 scenario creation (6-8 scenarios)
- JSON data file
- Sub-page deployment
- QR code postcards (optional)

**Timeline**: 1-2 categories per month

---

## QRCards Project Structure

### Directory Layout

```
qrcards/
├── src/
│   ├── pages/
│   │   ├── decision-analysis.tsx           # Main decision analysis page (all domains)
│   │   ├── fpa-platforms.tsx               # FP&A category page (FLAT URL)
│   │   ├── data-warehouse.tsx              # Data warehouse category (FLAT URL)
│   │   └── ...                              # Future category pages (FLAT)
│   │
│   ├── components/
│   │   ├── Hero.tsx                        # Audience-aware hero section
│   │   ├── CaseStudyCard.tsx               # Case study component
│   │   ├── FlipCardGrid.tsx                # 3×3 flip card container
│   │   ├── FlipCard.tsx                    # Individual flip card
│   │   ├── CTACard.tsx                     # Center CTA card
│   │   ├── PlatformOverview.tsx            # Platform tier visualization
│   │   ├── MethodologySection.tsx          # Decision framework
│   │   ├── RecommendationModal.tsx         # "Learn More" modal
│   │   ├── Breadcrumb.tsx                  # Shows hierarchy (flat URLs)
│   │   └── AudienceDetector.tsx            # Domain → audience mapper
│   │
│   ├── data/
│   │   ├── case-studies.json               # Case study data
│   │   ├── audience-config.json            # Domain-specific copy
│   │   └── decision-trees/
│   │       ├── fpa-platforms.json          # FP&A flip cards
│   │       ├── data-warehouse.json         # Data warehouse flip cards
│   │       └── ...                          # Future categories
│   │
│   └── utils/
│       ├── getAudience.ts                   # Domain → audience detection
│       └── getCopy.ts                       # Audience-specific copy loader
│
├── public/
│   └── research/                            # Static research pages
│       ├── fpa-platforms/
│       │   ├── seed-startup.md             # Deep dive pages
│       │   ├── series-a.md
│       │   └── ...
│       └── data-warehouse/
│           └── ...
│
├── config/
│   └── domains.json                         # Domain configuration
│       {
│         "cfo.inversefractional.com": "cfo",
│         "cto.inversefractional.com": "cto",
│         "cmo.inversefractional.com": "cmo",
│         "app.ivantohelpyou.com": "general"
│       }
│
└── styles/
    ├── flip-cards.css                       # CSS animations
    ├── audience-cfo.css                     # CFO-specific styles
    ├── audience-cto.css                     # CTO-specific styles
    └── audience-cmo.css                     # CMO-specific styles
```

---

## Component Specifications

### 1. CaseStudyCard Component

```tsx
// src/components/CaseStudyCard.tsx
interface CaseStudyCardProps {
  id: string;
  title: string;
  client: string;
  challenge: string;
  finalists: string[];
  methodology: string[];
  outcome: string;
  result: string;
  roi: string;
  link?: string; // Optional deep dive link
}

export function CaseStudyCard(props: CaseStudyCardProps) {
  return (
    <div className="case-study-card">
      <h3>{props.title}</h3>
      <div className="client-info">
        <span className="badge">{props.client}</span>
      </div>
      <p className="challenge">{props.challenge}</p>

      <div className="finalists">
        <strong>Evaluated:</strong> {props.finalists.join(", ")}
      </div>

      <div className="methodology">
        <strong>Decision Analysis Applied:</strong>
        <ul>
          {props.methodology.map(m => <li key={m}>✓ {m}</li>)}
        </ul>
      </div>

      <div className="outcome">
        <strong>Outcome:</strong> {props.outcome}
        <br />
        <strong>Result:</strong> {props.result}
        <br />
        <strong>ROI:</strong> {props.roi}
      </div>

      {props.link && (
        <a href={props.link} className="read-more">
          Read Full Case Study →
        </a>
      )}
    </div>
  );
}
```

**Styling**: Card with shadow, hover lift, responsive

---

### 2. FlipCard Component

```tsx
// src/components/FlipCard.tsx
interface FlipCardProps {
  front: {
    title: string;
    details: string[];
    icon?: string; // Font Awesome class
  };
  back: {
    recommendation: string;
    rationale: string[];
    tier: 1 | 2 | 3;
    confidence: "High" | "Medium" | "Low";
    research_link?: string;
  };
  onLearnMore?: () => void;
}

export function FlipCard({ front, back, onLearnMore }: FlipCardProps) {
  const [isFlipped, setIsFlipped] = useState(false);

  return (
    <div
      className={`flip-card ${isFlipped ? 'flipped' : ''}`}
      onClick={() => setIsFlipped(!isFlipped)}
    >
      <div className="flip-card-inner">
        {/* Front Side */}
        <div className="flip-card-front">
          {front.icon && <i className={`fa ${front.icon}`}></i>}
          <h3>{front.title}</h3>
          <ul className="details">
            {front.details.map(d => <li key={d}>{d}</li>)}
          </ul>
          <span className="tap-hint">Tap to reveal →</span>
        </div>

        {/* Back Side */}
        <div className={`flip-card-back tier-${back.tier}`}>
          <h3>→ {back.recommendation}</h3>
          <ul className="rationale">
            {back.rationale.map(r => <li key={r}>✓ {r}</li>)}
          </ul>
          <div className="actions">
            <button
              onClick={(e) => {
                e.stopPropagation();
                onLearnMore?.();
              }}
            >
              Learn More
            </button>
            <a
              href="#booking"
              onClick={(e) => e.stopPropagation()}
            >
              Book Analysis
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
```

**CSS Animation** (from proposal):
```css
.flip-card {
  perspective: 1000px;
  cursor: pointer;
  height: 280px;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transition: transform 0.6s;
  transform-style: preserve-3d;
}

.flip-card.flipped .flip-card-inner {
  transform: rotateY(180deg);
}

.flip-card-front, .flip-card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  border-radius: 12px;
  padding: 24px;
}

.flip-card-back {
  transform: rotateY(180deg);
}

/* Tier-specific gradients */
.flip-card-back.tier-1 {
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
}

.flip-card-back.tier-2 {
  background: linear-gradient(135deg, #a1c4fd 0%, #c2e9fb 100%);
}

.flip-card-back.tier-3 {
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}
```

---

### 3. FlipCardGrid Component

```tsx
// src/components/FlipCardGrid.tsx
interface FlipCardGridProps {
  scenarios: Scenario[];
  ctaContent: {
    title: string;
    subtitle: string;
    features: string[];
    cta_text: string;
    cta_link: string;
  };
}

export function FlipCardGrid({ scenarios, ctaContent }: FlipCardGridProps) {
  const [modalScenario, setModalScenario] = useState<Scenario | null>(null);

  return (
    <>
      <div className="flip-card-grid">
        {scenarios.map((scenario, index) => (
          index === 4 ? (
            // Center card (position 5) is CTA
            <CTACard key="cta" {...ctaContent} />
          ) : (
            <FlipCard
              key={scenario.id}
              front={scenario.front}
              back={scenario.back}
              onLearnMore={() => setModalScenario(scenario)}
            />
          )
        ))}
      </div>

      {modalScenario && (
        <RecommendationModal
          scenario={modalScenario}
          onClose={() => setModalScenario(null)}
        />
      )}
    </>
  );
}
```

**Grid Layout**:
```css
.flip-card-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

@media (max-width: 768px) {
  .flip-card-grid {
    grid-template-columns: 1fr;
  }
}
```

---

## Progressive Enhancement Strategy

### Week 1: Case Studies (Both Pages)

**Deliverable**: Case studies section live on both decision analysis pages

**Tasks**:
1. Create `CaseStudyCard` component
2. Create `case-studies.json` data file
3. Add first case study (manufacturing FP&A from research)
4. Add section to both pages
5. Deploy

**Success**: 1 case study visible on both pages

---

### Week 2-3: FP&A Sub-Page

**Deliverable**: `/fpa-platforms` live on both domains with flip cards

**Tasks**:
1. Extract flip card content from postcard copy
2. Create `fpa-platforms.json` data file
3. Build flip card components (`FlipCard`, `FlipCardGrid`, `CTACard`)
4. Create sub-page with hero, flip cards, methodology, CTA sections
5. Test QR code flow
6. Deploy

**Success**:
- 9 flip cards interactive
- QR code from physical postcard works
- At least 1 "Learn More" click tracked in analytics

---

### Week 4: WeRise Case Study

**Deliverable**: Second case study added (real client)

**Tasks**:
1. Complete WeRise engagement (per decision-analysis.yaml task)
2. Document case study (anonymize or get approval)
3. Add to `case-studies.json`
4. Deploy

**Success**: 2 case studies visible on both pages

---

### Month 2: Data Warehouse Sub-Page

**Deliverable**: `/data-warehouse` live with flip cards

**Tasks**:
1. Write 6-8 S3 scenarios for 3.044 data warehouse
2. Create `data-warehouse.json` data file
3. Reuse flip card components
4. Create sub-page
5. Deploy

**Success**: Second category live, components fully reusable

---

### Month 3+: Additional Categories

**Ongoing**: Add categories as research matures and demand emerges

**Priority**:
1. Accounting Software (3.006) - if CFO audience requests
2. HRIS/HCM (3.503) - if HR adjacent audience emerges
3. Team Task Management (3.131) - if productivity audience emerges

---

## Audience-Specific Customization

### Implementation Pattern

**Component with Domain Detection**:
```tsx
// src/components/Hero.tsx
interface HeroProps {
  audience: 'cfo' | 'cto' | 'cmo' | 'general';
  category?: string;
}

export function Hero({ audience, category }: HeroProps) {
  const copy = {
    cfo: {
      title: 'CFO Decision Analysis',
      subtitle: 'Data-driven platform selection for finance leaders',
      cta: 'Book Strategic Session'
    },
    cto: {
      title: 'Technical Architecture Analysis',
      subtitle: 'Engineering-first platform evaluation framework',
      cta: 'Book Technical Review'
    },
    cmo: {
      title: 'Marketing Stack Analysis',
      subtitle: 'Growth-focused platform selection for marketing leaders',
      cta: 'Book Strategy Session'
    },
    general: {
      title: 'Software Decision Analysis',
      subtitle: 'Expert guidance for complex platform decisions',
      cta: 'Book Decision Session'
    }
  };

  return (
    <section className={`hero hero-${audience}`}>
      <h1>{copy[audience].title}</h1>
      <p>{copy[audience].subtitle}</p>
      <button>{copy[audience].cta} - $99</button>
    </section>
  );
}
```

---

### CFO Domain (cfo.inversefractional.com)

**Tone**: Executive, ROI-focused, financial impact

**Copy Adjustments**:
- Hero: "CFO Decision Analysis"
- CTAs: "Book Strategic Session"
- Case studies: TCO, ROI, payback periods, budget impact
- Flip cards: Emphasize pricing, implementation timeline, financial metrics
- Scenarios: Company size, revenue, budget constraints

**Visual**: Professional, darker blues/grays, financial charts

**Category Angle**:
- `/fpa-platforms`: "Which platform fits YOUR budget?"
- `/data-warehouse`: "TCO comparison: $55/month to $150K/year"

---

### CTO Domain (cto.inversefractional.com) - Future

**Tone**: Technical, architecture-focused, integration-heavy

**Copy Adjustments**:
- Hero: "Technical Architecture Analysis"
- CTAs: "Book Technical Review"
- Case studies: API quality, data models, technical debt, migration complexity
- Flip cards: Emphasize integrations, APIs, data formats, scalability
- Scenarios: Tech stack, data volume, engineering team size, technical constraints

**Visual**: Developer-friendly, monospace fonts, code snippets, architecture diagrams

**Category Angle**:
- `/fpa-platforms`: "API architecture & integration patterns"
- `/data-warehouse`: "Query performance: sub-second to minutes"

---

### CMO Domain (cmo.inversefractional.com) - Future

**Tone**: Growth-focused, metrics-driven, campaign-oriented

**Copy Adjustments**:
- Hero: "Marketing Stack Analysis"
- CTAs: "Book Strategy Session"
- Case studies: Attribution, campaign ROI, conversion rates, growth metrics
- Flip cards: Emphasize marketing features, attribution, analytics
- Scenarios: Marketing channels, campaign volume, team structure, growth stage

**Visual**: Vibrant colors, growth charts, conversion funnels

**Category Angle**:
- `/fpa-platforms`: "Marketing budget planning & campaign ROI tracking"
- `/data-warehouse`: "Customer data platform for attribution modeling"

---

### General Domain (app.ivantohelpyou.com)

**Tone**: Accessible, educational, methodology-focused

**Copy Adjustments**:
- Hero: "Software Decision Analysis"
- CTAs: "Book Decision Session"
- Case studies: Methodology, decision framework, outcomes
- Flip cards: Balanced emphasis (features, pricing, use cases)
- Scenarios: General business context, broad applicability

**Visual**: Lighter, friendlier, approachable colors

**Category Angle**:
- `/fpa-platforms`: "Compare 9 platforms: features, pricing, best fit"
- `/data-warehouse`: "Choose the right analytics database for your needs"

---

## QR Code Integration

### Physical Postcards → Sub-Pages

**Flow**:
1. CFO picks up FPA-001 postcard at event
2. Scans QR code
3. Lands on `/fpa-platforms?source=FPA-001`
4. Interacts with flip cards
5. Books $99 decision analysis session

**Tracking**:
- URL parameter: `?source=FPA-001` (postcard ID)
- UTM parameters: `&utm_source=card-fpa-001&utm_medium=postcard&utm_campaign=cfo-networking-nov-2025`
- GA4 events: Card scan → flip card interaction → booking

**Postcard QR URLs** (Audience-Specific):
```
CFO Events:
FPA-001: https://cfo.inversefractional.com/fpa-platforms?source=FPA-001&utm_source=card-fpa-001&utm_medium=postcard&utm_campaign=cfo-networking-nov-2025
DW-001: https://cfo.inversefractional.com/data-warehouse?source=DW-001&utm_source=card-dw-001&utm_medium=postcard&utm_campaign=cfo-networking-nov-2025

CTO Events (future):
FPA-001-CTO: https://cto.inversefractional.com/fpa-platforms?source=FPA-001-CTO&utm_source=card-fpa-001-cto&utm_medium=postcard&utm_campaign=cto-devops-days-2026
DW-001-CTO: https://cto.inversefractional.com/data-warehouse?source=DW-001-CTO&utm_source=card-dw-001-cto&utm_medium=postcard&utm_campaign=cto-devops-days-2026

CMO Events (future):
FPA-001-CMO: https://cmo.inversefractional.com/fpa-platforms?source=FPA-001-CMO&utm_source=card-fpa-001-cmo&utm_medium=postcard&utm_campaign=cmo-saas-growth-2026

General/Multi-Audience:
FPA-001-GEN: https://app.ivantohelpyou.com/fpa-platforms?source=FPA-001-GEN&utm_source=card-fpa-001&utm_medium=postcard&utm_campaign=general-business-2026
```

**Same content, audience-specific entry point + tracking**

---

## Analytics & Tracking

### Key Events

**Page-Level**:
- Page view (main decision analysis page)
- Page view (category sub-page)
- QR code scan detected (`?source=*` parameter)

**Engagement**:
- Case study card viewed (scrolled into view)
- Case study "Read More" clicked
- Flip card clicked (which card #)
- Flip card flipped back
- "Learn More" clicked (modal opened)

**Conversion**:
- CTA clicked (which placement)
- Calendly opened
- Booking completed ($99 payment)

**Funnel**:
```
Sub-page view → Flip card interaction → Learn More → CTA click → Booking
```

---

## Success Metrics

### Phase 1: Case Studies (Week 1)

- [ ] 1 case study live on both pages
- [ ] 0 layout issues or bugs
- [ ] Component reusable (easy to add more)

---

### Phase 2: FP&A Sub-Page (Week 2-3)

- [ ] Sub-page live on both domains
- [ ] 9 flip cards interactive
- [ ] QR code flow tested (physical postcard → landing page)
- [ ] 50+ flip card interactions (first 30 days)
- [ ] 10+ "Learn More" clicks
- [ ] 2+ bookings from sub-page

---

### Phase 3: Data Warehouse Sub-Page (Month 2)

- [ ] Second category live
- [ ] Components fully reusable (no FP&A-specific code)
- [ ] 100+ combined flip card interactions across both categories
- [ ] 5+ bookings from sub-pages

---

### Long-Term (Month 3+)

- [ ] 3+ case studies live
- [ ] 3+ category sub-pages live
- [ ] 500+ total flip card interactions
- [ ] 10+ bookings/month from enhanced pages ($990/month revenue)
- [ ] QR code postcards generating measurable traffic

---

## Technical Considerations for Augment

### Key Augment Instructions

**Component Reusability**:
- Build components to accept props (don't hardcode FP&A content)
- Use JSON data files (easy to add categories)
- Separate layout from content

**Responsive Design**:
- Mobile: 1 column, accordion or swipe
- Tablet: 2 columns
- Desktop: 3×3 grid

**Performance**:
- Lazy load flip card images/icons
- CSS animations only (no JS animations)
- Static JSON files (no API calls initially)

**Accessibility**:
- Keyboard navigation (space/enter to flip)
- ARIA labels for screen readers
- Focus states on interactive elements

**SEO**:
- Server-side render sub-pages (Next.js or similar)
- Meta tags with category-specific descriptions
- Structured data (JSON-LD) for case studies

---

## Content Migration Checklist

### From spawn-solutions → QRCards

**FP&A Platforms** (3.007):
- [ ] Extract 9 scenarios from `fpa-platforms-postcard-copy.md`
- [ ] Create `fpa-platforms.json` data file
- [ ] Copy methodology text from `synthesis.md`
- [ ] Link to S3 scenarios as "Learn More" pages

**Data Warehouse** (3.044):
- [ ] Write 6-8 S3 scenarios (NEW WORK)
- [ ] Create `data-warehouse.json` data file
- [ ] Extract methodology from S1/S2
- [ ] Create scenario pages

**Case Studies**:
- [ ] Anonymize manufacturing FP&A scenario
- [ ] Write WeRise case study (when complete)
- [ ] Create `case-studies.json` data file

---

## Next Actions for Augment Implementation

### Immediate (This Week)

1. **Set up QRCards project structure**
   - [ ] Create directories (pages, components, data, utils, config)
   - [ ] Initialize routing for category pages (FLAT URLs)
   - [ ] Set up multi-domain config (cfo/cto/cmo/general)
   - [ ] Create domain detection utility (`getAudience.ts`)
   - [ ] Create audience config JSON file

2. **Build audience-aware components**
   - [ ] `Hero.tsx` with audience prop
   - [ ] `Breadcrumb.tsx` for visual hierarchy
   - [ ] `AudienceDetector.tsx` wrapper

3. **Build CaseStudyCard component**
   - [ ] Component file + props interface
   - [ ] Styling (card, shadow, hover)
   - [ ] Responsive layout
   - [ ] Audience-specific emphasis

4. **Add first case study**
   - [ ] Create `case-studies.json`
   - [ ] Add manufacturing FP&A case
   - [ ] Deploy to cfo.inversefractional.com
   - [ ] Deploy to app.ivantohelpyou.com

### Next Week

5. **Build flip card components**
   - [ ] `FlipCard.tsx` with CSS animation
   - [ ] `FlipCardGrid.tsx` with 3×3 layout
   - [ ] `CTACard.tsx` for center card
   - [ ] Test flip interaction
   - [ ] Audience-aware copy in cards

6. **Create FP&A category page** (FLAT URL)
   - [ ] Extract content to `fpa-platforms.json`
   - [ ] Build page layout (hero, flip cards, methodology, CTA)
   - [ ] Wire up audience detection
   - [ ] Deploy to cfo.inversefractional.com/fpa-platforms
   - [ ] Deploy to app.ivantohelpyou.com/fpa-platforms
   - [ ] Test QR code flow (CFO postcard → CFO domain)

### Following Weeks

7. **Write Data Warehouse scenarios**
   - [ ] Create 6-8 S3 scenarios for 3.044
   - [ ] Follow 3.007 S3 methodology
   - [ ] Create `data-warehouse.json`
   - [ ] Multi-audience angles (CFO: TCO, CTO: architecture, CMO: attribution)

8. **Build Data Warehouse category page** (FLAT URL)
   - [ ] Reuse flip card components
   - [ ] Deploy to both active domains
   - [ ] Prepare for future CTO/CMO domains

9. **Add more case studies**
   - [ ] WeRise engagement (when complete)
   - [ ] Future client engagements
   - [ ] Audience-specific case study angles

### Future (Month 2+)

10. **Launch CTO domain** (when ready)
   - [ ] Set up cto.inversefractional.com DNS/SSL
   - [ ] Create CTO-specific copy in audience-config.json
   - [ ] Deploy existing category pages with CTO tone
   - [ ] Create CTO-specific QR postcards
   - [ ] Test at engineering events

11. **Launch CMO domain** (when ready)
   - [ ] Set up cmo.inversefractional.com DNS/SSL
   - [ ] Create CMO-specific copy in audience-config.json
   - [ ] Deploy existing category pages with CMO tone
   - [ ] Create CMO-specific QR postcards
   - [ ] Test at marketing events

---

## Files to Reference

**From spawn-solutions**:
- FP&A content: `/home/ivanadamin/spawn-solutions/calendar/decision-trees/fpa-platforms-postcard-copy.md`
- FP&A methodology: `/home/ivanadamin/spawn-solutions/research/3.007-fpa-platforms/01-discovery/S3-need-driven/synthesis.md`
- Data warehouse research: `/home/ivanadamin/spawn-solutions/research/3.044-data-warehouse/01-discovery/S1-rapid/`
- Decision analysis workflow: `/home/ivanadamin/spawn-solutions/applications/inverse-fractional/decision-analysis-workflow.md`
- Enhancement proposal: `/home/ivanadamin/spawn-solutions/applications/inverse-fractional/DECISION_ANALYSIS_ENHANCEMENT_PROPOSAL.md`

---

**Last Updated**: November 12, 2025
**Status**: Ready for implementation
**Next Step**: Start with CaseStudyCard component + first case study
