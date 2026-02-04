# Boutique-Hotel-Recs: CTO Cookbook Analysis

**Application Idea Stage Analysis**

---

## Use Case Description

**"I want to build a system that provides personalized recommendations to hotel guests via QR codes on printed cards, with staff-editable recommendation pages."**

### The Problem

A boutique hotel wants to enhance guest experience with personalized recommendations:
- **Guest experience:** Check-in → receive printed card with QR code → scan → see personalized recommendations and map
- **Staff workflow:** Update recommendations for specific guests (restaurants, attractions, events)
- **Output:** Web page with curated content + interactive map
- **Physical artifact:** Printed card with QR code (generated at check-in)

### Required Capabilities

1. **Guest Management:** Track guests (name, check-in date, preferences)
2. **Recommendation Content:** Create/edit recommendations (restaurants, attractions, activities)
3. **Personalization:** Assign specific recommendations to specific guests
4. **QR Code Generation:** Generate unique QR code for each guest
5. **Guest-Facing Web Page:** Mobile-friendly page showing recommendations + map
6. **Staff Interface:** Easy way for front desk/concierge to update guest recommendations
7. **Printing:** Generate printable card with QR code (PDF or direct print)
8. **Map Integration:** Show recommended locations on interactive map

---

## Constraint Analysis

### Business Constraints
- **Hotel size:** Boutique hotel (assume 20-50 rooms)
- **Daily check-ins:** 5-20 guests per day
- **Total active guests:** ~40-100 at any time (multi-day stays)
- **Staff users:** 3-10 (front desk, concierge)
- **Budget:** Small business budget (prefer $0-100/month, max $500/month)
- **Timeline:** Want to launch for summer season (2-3 months)

### Technical Constraints
- **No login for guests:** Guests just scan QR code (no account creation)
- **Mobile-first:** Guests view on phones
- **Print integration:** Must generate printer-ready cards
- **Map integration:** Google Maps or similar
- **Content updates:** Staff needs to update recommendations in real-time
- **Low tech barrier:** Staff not developers (need simple interface)

### User Experience Constraints
- **Guest flow:** Scan QR → instantly see recommendations (no login, no app install)
- **Staff flow:** Add guest → assign recommendations → print card (5 minutes max)
- **Freshness:** Recommendations updated daily (new restaurant openings, events)

---

## Level Elimination Analysis

### Level 0: Packaged Software ❓ CHECK FIRST

**Could we buy software that does this?**

#### Potential Categories to Investigate:

**1. Guest Experience Platforms**
- **Canary Technologies** - Guest messaging and upsell platform
- **GuestJoy** - Pre-arrival messaging and local recommendations
- **Kipsu** - Guest messaging platform
- **TouchStay** - Vacation rental guidebooks

**Evaluation questions:**
- Do any support **QR code generation** for per-guest access?
- Do any support **printed cards** at check-in?
- Do any allow **staff to customize recommendations per guest**?
- Do any work for **boutique hotels** (not just large chains)?

**Quick research (hypothetical):**
- **GuestJoy:** $99-299/month, SMS-based, no QR code cards
- **TouchStay:** $20-100/month, designed for vacation rentals, QR code support, but static guidebooks (not personalized per guest)
- **Canary:** $300+/month, enterprise-focused, too expensive
- **Kipsu:** $500+/month, messaging platform, not guidebook focused

**2. QR Code Menu/Guidebook Platforms**
- **MustHaveMenus** - QR code menus for restaurants
- **Beaconstac** - QR code management platform
- **QR Code Generator PRO** - Generic QR platform

**Evaluation:**
- These generate QR codes but don't have **per-guest customization** or **hotel recommendation features**

**3. Custom Concierge Apps**
- **Concierge services** that provide city guides
- Typically **not hotel-specific** or **not per-guest personalized**

#### Verdict: Level 0 ❌ ELIMINATED

**Reason for elimination:**
- ❌ No packaged software found that combines:
  - QR code generation per guest
  - Personalized recommendations (not just generic hotel guidebook)
  - Staff-editable content for specific guests
  - Printed card generation
  - Price point appropriate for boutique hotel
- **Closest match:** TouchStay ($20-100/month) but it's designed for vacation rentals with **static guidebooks** (same content for all guests), not **personalized per-guest recommendations**

**If this breaks → Go to Level 1**

---

### Level 1: Enterprise Platform / SaaS ❓ EVALUATE

**WordPress / Wix / Squarespace + Plugins?**

#### WordPress with Plugins Approach

**Core setup:**
- **WordPress site** (free, self-hosted or $5-25/month managed)
- **Custom Post Type:** "Guest Recommendations" (one post per guest)
- **QR Code Plugin:** QR Code Generator plugin (free)
- **Map Plugin:** WP Google Maps plugin (free tier)
- **Access Control Plugin:** Password protect pages or use unique URL slugs

**Staff workflow:**
1. Guest checks in → Staff creates new "Guest Recommendations" page
2. Select recommendations from library (restaurants, attractions)
3. Add custom notes for this guest
4. Generate QR code pointing to guest-specific URL
5. Print card using browser print function

**Guest workflow:**
1. Scan QR code on card
2. Opens WordPress page at `hotelname.com/guest/guest-12345`
3. See personalized recommendations + map
4. No login required (public URL, but unique/hard to guess)

#### Advantages ✅
- **Low cost:** $25-50/month (managed WordPress hosting)
- **Easy for staff:** WordPress admin interface (point-and-click)
- **Content library:** Create master list of recommendations, assign to guests
- **Flexible:** Can customize appearance, add features
- **No coding:** Can accomplish with visual page builders (Elementor, Divi)
- **Print-friendly:** Can style page for printing (CSS media queries)

#### Disadvantages ❌
- **Setup complexity:** Need to configure plugins, custom post types, templates
- **No native guest management:** Need to manually create page per guest
- **No automated QR generation:** Staff must manually generate QR code for each guest
- **No check-out cleanup:** Old guest pages accumulate (need manual deletion)
- **Map integration:** Plugin-dependent, may not be as smooth as custom build

#### When This Works ✅
- ✅ Budget-constrained (<$100/month)
- ✅ Willing to do 20-40 hours initial setup (configure WordPress, plugins, templates)
- ✅ Staff comfortable with WordPress admin interface
- ✅ Can live with manual QR code generation workflow
- ✅ Don't need automated guest lifecycle (check-in to check-out)

#### When This Breaks ❌
- ❌ Want fully automated workflow (check-in → auto-generate page + QR code)
- ❌ Need guest lifecycle management (auto-archive after check-out)
- ❌ Want staff mobile app (WordPress admin mobile experience is clunky)
- ❌ Need reservation system integration (PMS integration)

#### Verdict: Level 1 ⚠️ VIABLE BUT CLUNKY

**This could work, but feels like "bending WordPress to do something it wasn't designed for."**

**Trade-offs:**
- ✅ **Low cost** ($25-50/month)
- ✅ **Fast setup** (2-3 weeks if familiar with WordPress)
- ⚠️ **Manual workflow** (staff must create page, generate QR, print card)
- ❌ **No guest lifecycle automation** (pages accumulate, need manual cleanup)

**Better options below? Let's check Level 2.**

---

### Level 2: Backend-as-a-Service / BaaS ⭐ STRONG CONTENDER

**Supabase / Firebase / PocketBase**

#### Supabase Approach (Recommended)

**Database Schema:**

```
Table: Guests
├── guest_id (UUID, primary key, auto-generated)
├── guest_name (text)
├── room_number (text)
├── check_in_date (date)
├── check_out_date (date)
├── preferences (text) - dietary restrictions, interests, etc.
├── status (text) - "checked_in", "checked_out", "archived"
└── created_at (timestamp)

Table: Recommendations
├── rec_id (UUID, primary key)
├── category (text) - "restaurant", "attraction", "activity", "event"
├── name (text)
├── description (text)
├── address (text)
├── lat (float)
├── lng (float)
├── image_url (text)
├── tags (text array) - "italian", "outdoor", "kids-friendly", etc.
└── active (boolean)

Table: GuestRecommendations (Junction Table)
├── guest_id (foreign key → Guests)
├── rec_id (foreign key → Recommendations)
├── staff_notes (text) - custom message for this guest
├── added_by (text) - staff member who added it
└── added_at (timestamp)
```

**Architecture:**

```
┌─────────────────────────────────────────┐
│         Supabase Backend                │
│  ┌─────────────────────────────────┐   │
│  │  PostgreSQL Database            │   │
│  │  • Guests                       │   │
│  │  • Recommendations              │   │
│  │  • GuestRecommendations         │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Supabase Auth (optional)       │   │
│  │  • Staff login only             │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Supabase Storage (optional)    │   │
│  │  • Recommendation images        │   │
│  └─────────────────────────────────┘   │
│                                         │
│  ┌─────────────────────────────────┐   │
│  │  Supabase Edge Functions        │   │
│  │  • Generate QR code             │   │
│  │  • Generate printable PDF card  │   │
│  └─────────────────────────────────┘   │
└──────────┬──────────────────┬───────────┘
           │                  │
    ┌──────▼───────┐   ┌──────▼──────────┐
    │ Staff Web    │   │ Guest Web Page  │
    │ App (React)  │   │ (Next.js)       │
    │              │   │                 │
    │ • Add guest  │   │ • View recs     │
    │ • Assign recs│   │ • Map view      │
    │ • Print card │   │ • No login      │
    └──────────────┘   └─────────────────┘
```

**Staff Workflow:**

1. **Guest checks in:**
   - Staff opens staff web app (tablet or computer)
   - Click "New Guest"
   - Enter: Name, Room #, Check-in/out dates, Preferences
   - Click "Save" → Guest record created in Supabase

2. **Assign recommendations:**
   - Staff sees library of recommendations (restaurants, attractions)
   - Filter by tags (e.g., "italian", "outdoor", "family-friendly")
   - Click recommendations to add to this guest
   - Add custom notes (e.g., "You mentioned you love pasta - try their carbonara!")
   - Click "Finalize"

3. **Generate & print card:**
   - Staff clicks "Print Card"
   - Supabase Edge Function generates:
     - Unique URL: `hotelrecs.com/g/abc123def456`
     - QR code pointing to that URL
     - PDF with hotel branding + QR code + "Scan for your personalized recommendations"
   - PDF downloads → Staff prints on cardstock → Hands to guest

**Guest Workflow:**

1. Guest receives printed card at check-in
2. Scan QR code with phone camera
3. Opens URL: `hotelrecs.com/g/abc123def456`
4. Page loads instantly (no login, no app install)
5. Sees:
   - Personalized greeting: "Welcome, Sarah!"
   - Recommendations with photos, descriptions, addresses
   - Interactive map showing all locations
   - Staff notes (e.g., "The concierge recommends...")

**Technical Implementation:**

**Frontend 1: Staff Web App (React)**
- **Framework:** React + Vite (or Next.js)
- **UI Library:** Tailwind CSS + Headless UI (or Shadcn)
- **Supabase Client:** `@supabase/supabase-js`
- **Features:**
  - Staff login (Supabase Auth)
  - Guest management (CRUD)
  - Recommendation library (CRUD)
  - Assign recommendations to guests
  - Generate QR code (call Edge Function)
  - Download PDF card

**Frontend 2: Guest Web Page (Next.js)**
- **Framework:** Next.js (SSR for fast load, SEO)
- **Styling:** Tailwind CSS
- **Map:** Google Maps Embed API (free tier: 25,000 loads/month)
- **Features:**
  - Load guest data by ID from URL (e.g., `/g/abc123`)
  - Display recommendations (image, name, description, address)
  - Show map with pins for all recommendations
  - Mobile-responsive (phone-optimized)
  - No login required (public access via unique URL)

**Backend: Supabase Edge Functions**

**Function 1: Generate QR Code**
```javascript
// Input: guest_id
// Output: QR code image (base64 or URL)
import QRCode from 'qrcode'

export async function generateQRCode(guest_id) {
  const url = `https://hotelrecs.com/g/${guest_id}`
  const qrCodeDataURL = await QRCode.toDataURL(url)
  return qrCodeDataURL
}
```

**Function 2: Generate PDF Card**
```javascript
// Input: guest_id, guest_name, qr_code_image
// Output: PDF file
import PDFDocument from 'pdfkit'

export async function generatePDFCard(guest_id, guest_name, qrCodeImage) {
  const doc = new PDFDocument({ size: 'A6' }) // postcard size

  // Add hotel logo
  doc.image('hotel-logo.png', 50, 50, { width: 100 })

  // Add guest name
  doc.fontSize(18).text(`Welcome, ${guest_name}!`, 50, 180)

  // Add instructions
  doc.fontSize(12).text('Scan the QR code below for personalized recommendations', 50, 220)

  // Add QR code
  doc.image(qrCodeImage, 150, 260, { width: 150, height: 150 })

  // Generate PDF
  return doc // Stream to response
}
```

#### Advantages ✅
- **Perfect capability match:** BaaS excels at CRUD operations (guests, recommendations)
- **Database included:** PostgreSQL with relationships (guests → recommendations)
- **Auth included:** Staff login (email/password or SSO)
- **API auto-generated:** REST and GraphQL endpoints for all tables
- **Real-time updates:** Staff updates recommendations → guest page updates instantly (Supabase Realtime)
- **Serverless functions:** Generate QR codes and PDFs without managing servers
- **Free tier:** 500MB database, 1GB bandwidth, 2GB storage → Easily covers boutique hotel
- **Fast development:** 2-3 weeks to MVP (vs 8 weeks for custom backend)
- **Modern stack:** React/Next.js → Easy to find developers

#### Disadvantages ❌
- **Requires frontend development:** Need to build React staff app + Next.js guest site (20-30 hours)
- **Learning curve:** Staff needs to learn new interface (not as familiar as WordPress)
- **Lock-in:** Supabase-specific APIs (75/100 lock-in) → 20-40 hours to migrate to different backend
- **No visual page builder:** Can't drag-and-drop like WordPress (need developer to change layout)

#### Pricing Analysis

**Supabase Free Tier:**
- ✅ 500MB database (plenty for 1000s of guests + recommendations)
- ✅ 1GB file storage (recommendation images)
- ✅ 2GB bandwidth/month (assume 100 guests/month × 5 page loads × 200KB = 100MB → well under limit)
- ✅ 500K Edge Function invocations (QR code generation ~100/month → 0.02% of limit)

**Likely cost: $0/month** (free tier sufficient for years)

**If exceed free tier:**
- **Pro Plan:** $25/month (8GB database, 100GB bandwidth, 100GB storage)

**Other costs:**
- **Google Maps Embed API:** Free (25,000 loads/month → 100 guests × 5 loads = 500/month)
- **Domain:** $12/year (`hotelrecs.com`)
- **Hosting:** $0 (Supabase hosts backend, Vercel free tier hosts Next.js frontend)

**Total: $0-25/month** 🎉

#### When This Works ✅
- ✅ Need custom frontend (mobile-optimized guest page)
- ✅ Want real-time updates (staff changes recs → guest page updates)
- ✅ Budget-conscious ($0-25/month)
- ✅ Have developer or willing to hire contractor (20-30 hours initial, 2-5 hours/month maintenance)
- ✅ Want automated workflow (check-in → generate QR → print card)
- ✅ Want guest lifecycle management (auto-archive after check-out)

#### When This Breaks ❌
- ❌ No developer available (need no-code solution)
- ❌ Need complex business logic (route optimization, AI-powered recommendations)
- ❌ Need integration with Property Management System (PMS) via custom APIs

#### Verdict: Level 2 ⭐ **STRONG WINNER**

**Why this is likely the best choice:**

1. **Perfect capability match:** BaaS designed for exactly this use case (database + auth + API + serverless functions)
2. **Cost:** $0-25/month (free tier likely sufficient forever)
3. **Development time:** 2-3 weeks (vs 8 weeks for custom backend from scratch)
4. **Modern UX:** Custom React/Next.js apps → Better UX than WordPress plugins
5. **Automated workflow:** Staff app streamlined for hotel check-in process
6. **Scalability:** Free tier handles 100s of guests easily, Pro tier ($25/month) handles 1000s

**Only move to Level 3 if:**
- Need complex business logic BaaS can't handle (AI recommendations, PMS integration)
- Need specific algorithm libraries (route optimization, machine learning)

**Let's check Level 3 anyway to see if custom backend is worth it...**

---

### Level 3: Platform-as-a-Service / PaaS ⚠️ LIKELY OVER-ENGINEERING

**Flask/Django/Express on Render/Railway/PythonAnywhere**

#### When You'd Consider This

**If you need custom business logic BaaS can't handle:**
- **AI-powered recommendations:** Use GPT-4 to generate personalized recommendations based on guest preferences
- **Route optimization:** Calculate optimal walking/driving routes between recommendations
- **PMS integration:** Connect to hotel's Property Management System (Opera, Mews, Cloudbeds) to auto-import guest data
- **Advanced analytics:** Track which recommendations guests view, click, visit

#### Implementation Approach

**Backend:** Flask (Python) on PythonAnywhere ($5-19/month)
- **Database:** PostgreSQL (same schema as Supabase)
- **QR generation:** `qrcode` library (Python)
- **PDF generation:** `reportlab` library (Python)
- **Map integration:** Google Maps API
- **AI recommendations:** OpenAI API (GPT-4 for personalization)
- **Route optimization:** Google Routes API or custom algorithm

**Frontend:** Same as Level 2 (React staff app + Next.js guest site)

**Custom backend endpoints:**
```
POST /api/guests - Create guest
GET /api/guests/:id - Get guest details
POST /api/recommendations - Create recommendation
GET /api/guests/:id/recommendations - Get guest's recs
POST /api/generate-qr - Generate QR code
POST /api/generate-pdf - Generate printable card
POST /api/ai-recommend - AI-powered recommendation suggestions
```

#### Advantages ✅
- **Full control:** Can implement any custom logic
- **Algorithm libraries:** Can use scikit-learn, NetworkX, etc.
- **PMS integration:** Can build custom API connectors
- **AI-powered features:** Can integrate OpenAI, Claude, etc.
- **Advanced analytics:** Can track user behavior, A/B test

#### Disadvantages ❌
- **Development time:** 4-6 weeks (vs 2-3 weeks for BaaS)
- **Higher cost:** $19/month (PythonAnywhere) + $25/month (PostgreSQL hosting) = $44/month (vs $0 for BaaS)
- **More maintenance:** Need to manage database, server, deployments
- **More complexity:** More code = more bugs, more time to fix

#### When This Works ✅
- ✅ Need AI-powered recommendations (GPT-4 suggestions)
- ✅ Need PMS integration (auto-import guests from Opera, Mews, etc.)
- ✅ Need advanced analytics (which recs guests visit)
- ✅ Need route optimization (shortest path between 5 restaurants)

#### When This Breaks ❌
- ❌ None of above features needed (Level 2 sufficient)
- ❌ Budget-constrained (Level 2 is free, Level 3 is $44/month)
- ❌ Time-constrained (Level 2 is 2-3 weeks, Level 3 is 4-6 weeks)

#### Verdict: Level 3 ❌ **OVER-ENGINEERING FOR MVP**

**Unless hotel specifically asks for:**
- AI-powered recommendations
- PMS integration
- Advanced analytics
- Route optimization

**Then Level 2 (BaaS) is simpler, cheaper, faster.**

**Recommendation:** Start with Level 2, add Level 3 features later if demand.

---

### Level 4: Infrastructure-as-a-Service / IaaS ❌ ELIMINATED

**AWS EC2 / Azure VMs**

**When This Breaks:**
- ❌ Boutique hotel doesn't need IaaS scale
- ❌ BaaS/PaaS costs <<< $1,000/month threshold
- ❌ No OS-level control needed
- ❌ Massive over-engineering

**Verdict:** Not applicable.

---

## Recommended Decision Path

### First: Validate Packaged Software Again

**Before building anything, do 1-hour trial:**

1. **TouchStay** ($20-100/month):
   - Trial: Can you create **per-guest guidebooks** (not just one guidebook for all guests)?
   - Trial: Does QR code → guest-specific page work?
   - Check: Can staff update recommendations in real-time?

   **If YES → TouchStay wins!** (Cheaper than building, zero development time)

2. **Beaconstac** ($15-50/month):
   - Trial: QR code management + custom landing pages
   - Check: Can you create unique landing page per guest?

   **If YES → Beaconstac wins!**

### If Packaged Software Doesn't Fit:

**Recommended: Level 2 (BaaS - Supabase) ⭐**

**Why:**
1. **Perfect capability match:** Database + Auth + API + Serverless functions = exactly what you need
2. **Cost:** $0/month (free tier) for years
3. **Development time:** 2-3 weeks MVP
4. **Modern UX:** Custom React/Next.js → Better than WordPress plugins
5. **Automated workflow:** Streamlined for hotel check-in process
6. **Scalability:** Handles 100s-1000s of guests easily

**Only choose Level 1 (WordPress) if:**
- No developer available
- Willing to accept manual workflow (staff generates QR codes manually)
- Can live with clunky admin interface

**Only choose Level 3 (PaaS) if:**
- Need AI-powered recommendations (GPT-4)
- Need PMS integration (Opera, Mews API)
- Need advanced analytics or route optimization

---

## Architecture Recommendation: Supabase (Level 2)

### Complete Tech Stack

```
Backend (Supabase - Free Tier)
├── PostgreSQL Database (guests, recommendations, junction table)
├── Supabase Auth (staff login)
├── Supabase Storage (recommendation images)
├── Supabase Edge Functions (QR generation, PDF generation)
└── Supabase Realtime (optional: live updates)

Frontend 1: Staff Web App
├── Framework: React + Vite
├── UI: Tailwind CSS + Shadcn UI
├── Hosting: Vercel (free tier)
└── Features: Guest CRUD, Assign recs, Print cards

Frontend 2: Guest Web Page
├── Framework: Next.js (SSR for fast load)
├── UI: Tailwind CSS
├── Hosting: Vercel (free tier)
├── Map: Google Maps Embed API (free: 25K loads/month)
└── Features: View recs, Map, Mobile-optimized

Printing
├── QR Code: qrcode library (npm package)
├── PDF: jsPDF library (browser-based PDF generation)
└── Workflow: Generate PDF in browser → Print from browser
```

### Development Timeline

**Week 1: Database & Auth**
- [ ] Set up Supabase project
- [ ] Create database schema (Guests, Recommendations, GuestRecommendations)
- [ ] Configure row-level security (staff only)
- [ ] Set up Supabase Auth (email/password for staff)

**Week 2: Staff Web App**
- [ ] Build React app (Vite + Tailwind + Shadcn)
- [ ] Guest management (add, edit, view, archive)
- [ ] Recommendation library (add, edit, view)
- [ ] Assign recommendations to guest
- [ ] Generate QR code (call Supabase Edge Function)
- [ ] Generate PDF card (jsPDF in browser)

**Week 3: Guest Web Page**
- [ ] Build Next.js app
- [ ] Guest page (`/g/[guest_id]`)
- [ ] Fetch guest recommendations from Supabase
- [ ] Display recommendations (images, descriptions, addresses)
- [ ] Integrate Google Maps (embed with pins)
- [ ] Mobile-responsive design
- [ ] Deploy to Vercel

**Week 4: Edge Functions & Testing**
- [ ] Build Supabase Edge Function for QR generation
- [ ] Build Supabase Edge Function for PDF generation (optional - or do in browser)
- [ ] End-to-end testing (staff creates guest → assigns recs → prints card → guest scans)
- [ ] UAT with hotel staff
- [ ] Refinements based on feedback

**Total: 4 weeks** (one developer, part-time)

**Or: 2 weeks** (one developer, full-time)

---

## Cost Breakdown

### Development (One-Time)
- **Week 1-2:** Database, Auth, Staff App (30 hours × $100/hour = $3,000)
- **Week 3:** Guest Web Page (15 hours × $100/hour = $1,500)
- **Week 4:** Edge Functions, Testing (15 hours × $100/hour = $1,500)
- **Total:** **$6,000** (contractor) or **$0** (build yourself)

### Monthly Costs
- **Supabase:** $0/month (free tier)
- **Vercel:** $0/month (free tier)
- **Google Maps Embed API:** $0/month (free: 25K loads/month)
- **Domain:** $1/month (`hotelrecs.com`)
- **Total:** **$1/month** 🎉

### ROI Analysis

**Current state (manual recommendations):**
- Staff time: 10 minutes per guest × 15 guests/day × 30 days = 75 hours/month
- Cost: 75 hours × $20/hour (front desk wage) = **$1,500/month**
- Quality: Inconsistent (some guests get great recs, others get generic advice)

**With automated system:**
- Staff time: 5 minutes per guest × 15 guests/day × 30 days = 37.5 hours/month
- Cost: 37.5 hours × $20/hour = **$750/month**
- Time saved: **37.5 hours/month → $750/month**
- Quality: Consistent, professional, always up-to-date

**Break-even:**
- Development cost: $6,000
- Monthly savings: $750
- Break-even: **8 months**

**3-year ROI:**
- Savings: $750/month × 36 months = $27,000
- Cost: $6,000 development + $36 monthly fees = $6,036
- **Net benefit: $20,964** 💰

Plus intangible benefits:
- Better guest experience → Higher review scores
- More professional brand perception
- Staff spend more time on high-value interactions (less time explaining where restaurants are)

---

## Alternatives & Trade-offs

### Alternative 1: WordPress (Level 1)

**If no developer available:**

**Setup:**
- WordPress managed hosting ($25/month)
- QR code plugin (free)
- Custom post type for guests (free)
- Map plugin (free)

**Trade-offs:**
- ✅ Lower development cost ($1,000 for setup vs $6,000 for custom)
- ⚠️ Manual workflow (staff generates QR codes manually)
- ⚠️ Clunky admin interface (not optimized for hotel workflow)
- ❌ No automated guest lifecycle (pages accumulate)

**Cost:** $25/month + $1,000 setup

**Verdict:** Acceptable if no developer, but clunkier UX

---

### Alternative 2: No-Code Tools (Airtable + Softr)

**If want visual builder:**

**Setup:**
- **Airtable** (database): $20/month (Pro plan for more records)
- **Softr** (frontend builder): $29/month (build web app from Airtable)
- **QR code generation:** Integromat/Make.com ($9/month)

**Workflow:**
1. Staff adds guest to Airtable (form or table view)
2. Assigns recommendations (linked records)
3. Softr auto-generates guest page at `/guest/[guest_id]`
4. Make.com automation generates QR code
5. Staff prints card

**Trade-offs:**
- ✅ No coding required (visual builders)
- ✅ Fast setup (1 week vs 4 weeks custom)
- ⚠️ Higher monthly cost ($58/month vs $1/month custom)
- ⚠️ Less flexible (limited by Softr templates)
- ⚠️ Higher lock-in (Airtable + Softr specific)

**Cost:** $58/month + $500 setup (no-code consultant)

**Verdict:** Good for non-technical team, but $58/month ongoing

---

### Alternative 3: Static Site + Google Sheets

**If ultra-budget-constrained:**

**Setup:**
- **Google Sheets** (database): Free
- **Google Apps Script** (backend): Free
- **GitHub Pages** (hosting): Free
- **QR code:** Free online generator

**Workflow:**
1. Staff adds guest to Google Sheet
2. Assigns recommendations (dropdown selections)
3. Apps Script generates static HTML page per guest
4. Deploys to GitHub Pages
5. Staff uses free QR generator → Print

**Trade-offs:**
- ✅ $0/month (completely free)
- ⚠️ Manual QR generation (no automation)
- ⚠️ No real-time updates (static HTML pages)
- ⚠️ No staff login (anyone with Sheet access can edit)
- ❌ Very manual (not automated workflow)

**Cost:** $0/month + $2,000 setup (need developer to build Apps Script)

**Verdict:** Only if absolutely budget-constrained AND can live with very manual process

---

## Final Recommendation

**Recommended Solution: Supabase (Level 2 BaaS) ⭐**

**Why:**
1. **Best capability match:** Database + Auth + API + Functions = exactly what you need
2. **Best cost:** $1/month ongoing (vs $25-58/month alternatives)
3. **Best UX:** Custom apps optimized for hotel workflow
4. **Best automation:** Staff workflow streamlined (5 minutes per guest)
5. **Best scalability:** Free tier handles 100s-1000s of guests
6. **Best ROI:** Break-even in 8 months, $20K net benefit over 3 years

**Critical validation step:**
- **Before building:** 1-hour trial of TouchStay ($20-100/month) to see if it supports per-guest customization
- **If TouchStay works:** Buy instead of build! (Saves $6,000 development)
- **If TouchStay doesn't work:** Build with Supabase (4 weeks, $6,000, then $1/month)

**Only choose alternative if:**
- No developer available → WordPress or Airtable+Softr
- Ultra budget-constrained → Google Sheets + Apps Script
- Need AI/PMS integration → PaaS (Level 3)

---

## Next Steps

### Step 1: Validate Packaged Software (2 hours)
- [ ] Trial TouchStay (does it support per-guest guidebooks?)
- [ ] Trial Beaconstac (QR code management + custom landing pages?)
- [ ] If either works → Decision made! Buy instead of build.

### Step 2: If Packaged Software Doesn't Fit, Validate Supabase (4 hours)
- [ ] Create free Supabase account
- [ ] Create database schema (Guests, Recommendations tables)
- [ ] Build simple proof-of-concept:
  - Add 1 guest
  - Add 2 recommendations
  - Assign recommendations to guest
  - Generate guest page URL
  - Manually create QR code pointing to URL
- [ ] Show to hotel staff → Does this workflow make sense?

### Step 3: Decision
- **If POC works → Hire developer** (4 weeks, $6,000) or **Build yourself** (4 weeks part-time)
- **If too complex → No-code alternative** (Airtable + Softr, 1 week, $500 setup + $58/month)

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Status:** Idea stage - awaiting packaged software trial and technical validation
**Confidence:** High (85%) that Supabase BaaS is optimal for MVP
