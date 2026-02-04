# Digital Publishing Platform: Technical Implementation

**Date:** October 13, 2025
**Status:** TECHNICAL SPECIFICATION (Month 12-15 implementation)
**Context:** Technical architecture for hosting, rendering, and managing hotel guidebooks as published content

---

## Overview

**What we're building:**
- Guidebook generator (database → web/PDF)
- Hosting platform (guidebooks.mztape.com)
- Marketplace (discovery, browsing, purchasing)
- Analytics (traffic, engagement, conversions)
- Custom domain support (seattleguide.hotelballard.com)

**What we're NOT building:**
- New database (reuse existing QRCards schema)
- New CMS (hotels already manage content)
- New templates (adapt Convention City Seattle trail templates)

---

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│ Hotel Dashboard (existing)                      │
│ - Manage destinations, activities, reviews      │
│ - Click "Publish Guidebook"                     │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Guidebook Generator Service                     │
│ - Query database (destinations, activities)     │
│ - Aggregate reviews                             │
│ - Apply template                                │
│ - Generate static HTML + PDF                    │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Publishing Platform (guidebooks.mztape.com)     │
│ - Static site hosting (Vercel/Cloudflare)      │
│ - Individual guidebook pages                    │
│ - Marketplace homepage                          │
│ - Search/filter                                 │
└─────────────────┬───────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────┐
│ Customer Experience                              │
│ - Browse marketplace                             │
│ - Read guidebook online                         │
│ - Buy print version                              │
│ - Hotel custom domain                            │
└─────────────────────────────────────────────────┘
```

---

## Database Schema (Extensions)

**Existing tables (no changes needed):**
- `hotels` (hotel info)
- `destinations` (Giuseppe's, Space Needle, etc.)
- `activities` (card-specific experiences)
- `reviews` (guest feedback)
- `cards` (A♥, 3♣, etc.)

**New tables for publishing:**

### `guidebooks`

```sql
CREATE TABLE guidebooks (
  id UUID PRIMARY KEY,
  hotel_id UUID REFERENCES hotels(id),

  -- Publishing status
  status VARCHAR(20), -- 'draft', 'published', 'archived'
  published_at TIMESTAMP,
  last_updated TIMESTAMP,

  -- URLs
  slug VARCHAR(100) UNIQUE, -- 'hotel-ballard-seattle'
  custom_domain VARCHAR(255), -- 'seattleguide.hotelballard.com'

  -- Content
  title VARCHAR(255), -- "The Hotel Ballard Guide to Seattle"
  subtitle VARCHAR(255), -- "Curated by our staff, refined by our guests"
  description TEXT, -- For SEO meta description

  -- Design
  template VARCHAR(50), -- 'classic', 'visual', 'pocket', 'coffee-table'
  cover_image_url TEXT,
  brand_colors JSONB, -- {primary: '#123456', secondary: '#abcdef'}

  -- Stats (cached)
  total_destinations INT,
  total_reviews INT,
  avg_rating DECIMAL(3,2),
  pageviews INT DEFAULT 0,

  -- Settings
  include_reviews BOOLEAN DEFAULT true,
  include_photos BOOLEAN DEFAULT true,
  include_maps BOOLEAN DEFAULT true,
  languages TEXT[], -- ['en', 'es', 'zh']

  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_guidebooks_hotel ON guidebooks(hotel_id);
CREATE INDEX idx_guidebooks_slug ON guidebooks(slug);
CREATE INDEX idx_guidebooks_status ON guidebooks(status);
```

### `guidebook_analytics`

```sql
CREATE TABLE guidebook_analytics (
  id UUID PRIMARY KEY,
  guidebook_id UUID REFERENCES guidebooks(id),

  -- Event tracking
  event_type VARCHAR(50), -- 'pageview', 'download', 'purchase', 'share'
  event_date DATE,

  -- Traffic source
  referrer_domain VARCHAR(255), -- 'google.com', 'instagram.com'
  utm_source VARCHAR(100),
  utm_medium VARCHAR(100),
  utm_campaign VARCHAR(100),

  -- User (anonymous)
  session_id VARCHAR(255),
  user_agent TEXT,
  country VARCHAR(2),
  city VARCHAR(100),

  -- Page details
  page_url TEXT, -- Which destination/section viewed
  time_on_page INT, -- seconds

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_analytics_guidebook ON guidebook_analytics(guidebook_id, event_date);
CREATE INDEX idx_analytics_event ON guidebook_analytics(event_type);
```

### `marketplace_reviews`

```sql
CREATE TABLE marketplace_reviews (
  id UUID PRIMARY KEY,
  guidebook_id UUID REFERENCES guidebooks(id),

  -- Review content
  rating INT CHECK (rating >= 1 AND rating <= 5),
  title VARCHAR(255),
  comment TEXT,

  -- Reviewer
  reviewer_name VARCHAR(100), -- "Sarah M." (anonymized)
  verified_reader BOOLEAN DEFAULT false, -- Read full guide

  -- Moderation
  status VARCHAR(20), -- 'pending', 'approved', 'rejected'
  moderated_at TIMESTAMP,

  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_marketplace_reviews_guidebook ON marketplace_reviews(guidebook_id);
```

---

## Guidebook Generator Service

### Input (from database)

```javascript
// Hotel clicks "Publish Guidebook" button
const guidebookData = {
  hotel: {
    id: 'uuid',
    name: 'Hotel Ballard',
    location: 'Ballard, Seattle',
    logo_url: 'https://...',
    brand_colors: {primary: '#123456', secondary: '#abcdef'}
  },

  cards: [
    {
      id: 'A♥',
      name: 'Romantic Dinner',
      description: '...',
      activities: [
        {
          destination: 'Giuseppe\'s Italian',
          name: 'Date Night Dinner',
          content: '...',
          reviews: [
            {rating: 5, text: 'Carbonara was incredible!', date: '2025-09-15'},
            {rating: 5, text: 'Perfect for anniversary', date: '2025-08-20'}
          ],
          avg_rating: 4.8,
          review_count: 34
        }
      ]
    },
    // ... 51 more cards
  ],

  stats: {
    total_destinations: 85,
    total_reviews: 547,
    avg_rating: 4.6,
    date_range: '2024-10-13 to 2025-10-13'
  }
};
```

### Template System

**Reuse Convention City Seattle trail templates:**

```
/templates/
├── classic/          (Text-focused, print-friendly)
│   ├── layout.tsx
│   ├── card-section.tsx
│   ├── destination.tsx
│   └── styles.css
│
├── visual/           (Photo-heavy, coffee table)
│   ├── layout.tsx
│   ├── card-section.tsx
│   └── styles.css
│
├── pocket/           (Compact, mobile-first)
│   └── ...
│
└── coffee-table/     (Premium, full-color)
    └── ...
```

**Each template implements:**
- `render(guidebookData)` → HTML
- `renderPDF(guidebookData)` → PDF
- `getSEO(guidebookData)` → metadata

### Generator Process

```javascript
// Triggered when hotel clicks "Publish Guidebook"
async function generateGuidebook(hotelId, options) {
  // 1. Query database
  const data = await fetchGuidebookData(hotelId);

  // 2. Select template
  const template = templates[options.template || 'classic'];

  // 3. Generate HTML (for web)
  const html = await template.render(data);

  // 4. Generate PDF (for export/print)
  const pdf = await template.renderPDF(data);

  // 5. Deploy to static hosting
  const slug = generateSlug(data.hotel.name); // 'hotel-ballard-seattle'
  await deployToVercel({
    slug,
    html,
    pdf,
    assets: data.images
  });

  // 6. Update database
  await db.guidebooks.upsert({
    hotel_id: hotelId,
    slug,
    status: 'published',
    published_at: new Date(),
    ...options
  });

  // 7. Notify hotel
  await sendEmail({
    to: data.hotel.email,
    subject: 'Your guidebook is live!',
    body: `View at: guidebooks.mztape.com/${slug}`
  });

  return {
    url: `https://guidebooks.mztape.com/${slug}`,
    pdf_url: `https://guidebooks.mztape.com/${slug}/export.pdf`
  };
}
```

---

## Static Site Generation

### Why Static?

**Benefits:**
- Fast (no server rendering)
- Cheap (Vercel/Cloudflare free tier)
- SEO-friendly (pre-rendered HTML)
- Reliable (no database queries on page load)
- Scalable (CDN handles traffic)

**Trade-offs:**
- Not real-time (regenerate to update)
- Solution: Regenerate nightly + on-demand when hotel updates

### Build Process

```javascript
// Next.js app at guidebooks.mztape.com

// Generate static pages for all published guidebooks
export async function getStaticPaths() {
  const guidebooks = await db.guidebooks.findMany({
    where: {status: 'published'}
  });

  return {
    paths: guidebooks.map(g => ({params: {slug: g.slug}})),
    fallback: 'blocking' // Generate new guidebooks on-demand
  };
}

export async function getStaticProps({params}) {
  const guidebook = await fetchGuidebookData(params.slug);

  return {
    props: {guidebook},
    revalidate: 86400 // Regenerate daily
  };
}

// Page component
export default function GuidebookPage({guidebook}) {
  return (
    <GuidebookLayout guidebook={guidebook}>
      {guidebook.cards.map(card => (
        <CardSection key={card.id} card={card} />
      ))}
    </GuidebookLayout>
  );
}
```

### Hosting Stack

**Production:**
```
Domain: guidebooks.mztape.com
Hosting: Vercel (Next.js, automatic CDN)
DNS: Cloudflare (custom domain support)
Storage: S3 (PDF exports, images)
Database: Existing QRCards database (Supabase)
```

**Cost (100 guidebooks):**
- Vercel: Free (up to 100GB bandwidth)
- Cloudflare: Free (DNS + CDN)
- S3: $5/month (PDF storage)
- Total: **$5/month**

**Cost (1,000 guidebooks):**
- Vercel: $20/month (Pro plan)
- Cloudflare: Free
- S3: $20/month
- Total: **$40/month**

---

## Marketplace Platform

### Homepage (guidebooks.mztape.com)

```javascript
// /app/page.tsx

export default function MarketplaceHome() {
  const featured = await getFeaturedGuidebooks();
  const recent = await getRecentGuidebooks();
  const popular = await getPopularGuidebooks();

  return (
    <>
      <Hero />

      <SearchBar />

      <FeaturedSection guidebooks={featured} />

      <CategoryBrowser
        categories={[
          'Romantic Getaways',
          'Family Adventures',
          'Business Travel',
          'Solo Exploration'
        ]}
      />

      <CityBrowser
        cities={['Seattle', 'Portland', 'San Francisco', 'Austin']}
      />

      <RecentGuidebooks guidebooks={recent} />

      <PopularGuidebooks guidebooks={popular} />
    </>
  );
}
```

### Individual Guidebook Page

```javascript
// /app/[slug]/page.tsx

export default function GuidebookPage({params}) {
  const guidebook = await getGuidebook(params.slug);
  const hotel = guidebook.hotel;
  const reviews = await getMarketplaceReviews(guidebook.id);

  return (
    <>
      {/* Hero section */}
      <GuidebookHero
        title={guidebook.title}
        subtitle={guidebook.subtitle}
        coverImage={guidebook.cover_image_url}
        stats={{
          destinations: guidebook.total_destinations,
          reviews: guidebook.total_reviews,
          rating: guidebook.avg_rating
        }}
        actions={[
          {label: 'Read Online', href: `/${params.slug}/read`},
          {label: 'Buy Print $20', href: `/${params.slug}/buy`},
          {label: 'Export PDF', href: `/${params.slug}/export.pdf`}
        ]}
      />

      {/* About section */}
      <AboutGuidebook
        description={guidebook.description}
        hotel={hotel}
        updated={guidebook.last_updated}
      />

      {/* Preview: Top destinations */}
      <TopDestinations
        destinations={guidebook.top_destinations}
        limit={10}
      />

      {/* Reader reviews */}
      <MarketplaceReviews
        reviews={reviews}
        avgRating={calculateAvgRating(reviews)}
      />

      {/* About the hotel */}
      <HotelCard
        hotel={hotel}
        bookingLink={hotel.website}
      />
    </>
  );
}
```

### Reading Experience

```javascript
// /app/[slug]/read/page.tsx

export default function ReadGuidebook({params}) {
  const guidebook = await getGuidebook(params.slug);

  return (
    <ReadingLayout guidebook={guidebook}>
      {/* Table of contents (sticky sidebar) */}
      <TOC cards={guidebook.cards} />

      {/* Main content */}
      <MainContent>
        <Introduction content={guidebook.introduction} />

        {guidebook.cards.map(card => (
          <CardSection key={card.id} card={card}>
            {card.activities.map(activity => (
              <ActivityDetail
                key={activity.id}
                activity={activity}
                reviews={activity.reviews}
              />
            ))}
          </CardSection>
        ))}

        <Conclusion content={guidebook.conclusion} />
      </MainContent>

      {/* Bottom CTA */}
      <StickyFooter>
        <Button href={`/${params.slug}/buy`}>
          Buy Print Version $20
        </Button>
        <Button variant="secondary" href={hotel.booking_url}>
          Book Hotel
        </Button>
      </StickyFooter>
    </ReadingLayout>
  );
}
```

---

## Custom Domain Support

### How It Works

**Hotel wants:** `seattleguide.hotelballard.com`

**Setup process:**
1. Hotel enters custom domain in dashboard
2. System generates DNS instructions:
   ```
   CNAME: seattleguide.hotelballard.com → guidebooks.mztape.com
   ```
3. Hotel adds CNAME to their DNS (or we do it via API if we manage their DNS)
4. System verifies DNS propagation
5. System provisions SSL cert (Let's Encrypt via Vercel)
6. Custom domain live (5-60 min)

**Technical implementation:**

```javascript
// Vercel domains API
async function addCustomDomain(guidebookId, domain) {
  // 1. Add domain to Vercel project
  await vercel.domains.add({
    name: domain,
    projectId: process.env.VERCEL_PROJECT_ID
  });

  // 2. Wait for DNS verification
  await waitForDNS(domain);

  // 3. Provision SSL
  await vercel.domains.configureSSL(domain);

  // 4. Update database
  await db.guidebooks.update({
    where: {id: guidebookId},
    data: {custom_domain: domain}
  });

  // 5. Rewrite routing (Next.js middleware)
  // When request comes to seattleguide.hotelballard.com,
  // serve content from guidebooks.mztape.com/hotel-ballard-seattle

  return {success: true, domain};
}
```

**Pricing:**
- Free tier: guidebooks.mztape.com/your-hotel
- Premium tier (+$29/month): Custom domain + white label

---

## Analytics Platform

### Tracking Events

```javascript
// Client-side tracking (lightweight, privacy-focused)
// No cookies, no personal data, no device fingerprinting

// On page load
trackEvent({
  event: 'pageview',
  guidebook_id: guidebook.id,
  page_url: window.location.pathname,
  referrer: document.referrer,
  session_id: getOrCreateSessionId(), // Random UUID, expires in 30 min
  timestamp: new Date()
});

// On PDF download
trackEvent({
  event: 'download',
  guidebook_id: guidebook.id,
  format: 'pdf'
});

// On print purchase
trackEvent({
  event: 'purchase',
  guidebook_id: guidebook.id,
  amount: 20.00,
  format: 'print'
});

// On social share
trackEvent({
  event: 'share',
  guidebook_id: guidebook.id,
  platform: 'twitter'
});
```

### Hotel Dashboard

```javascript
// /app/dashboard/guidebook/[id]/analytics

export default function GuidebookAnalytics({guidebookId}) {
  const stats = await getGuidebookStats(guidebookId);

  return (
    <DashboardLayout>
      <StatsOverview
        pageviews={stats.pageviews}
        downloads={stats.downloads}
        purchases={stats.purchases}
        revenue={stats.revenue}
        dateRange={stats.dateRange}
      />

      <TrafficSources
        sources={stats.referrers}
        // google.com: 2,400 visits (45%)
        // instagram.com: 800 visits (15%)
        // direct: 1,200 visits (22%)
      />

      <TopDestinations
        destinations={stats.popularDestinations}
        // Giuseppe's: 1,800 views
        // Pike Place Market: 1,500 views
      />

      <ConversionFunnel
        funnel={[
          {step: 'Viewed guidebook', count: 5,000},
          {step: 'Read full guide', count: 1,200},
          {step: 'Clicked booking link', count: 300},
          {step: 'Purchased print', count: 50}
        ]}
      />

      <GeographicBreakdown
        countries={stats.countries}
        cities={stats.cities}
      />
    </DashboardLayout>
  );
}
```

---

## SEO Strategy

### On-Page SEO

**Individual guidebook pages:**

```html
<head>
  <!-- Title -->
  <title>The Hotel Ballard Guide to Seattle | 547 Guest Reviews</title>

  <!-- Meta description -->
  <meta name="description" content="Discover Seattle through the eyes of 547 Hotel Ballard guests. Romantic dinners, family adventures, hidden gems, and local favorites curated by our staff.">

  <!-- Open Graph (social sharing) -->
  <meta property="og:title" content="The Hotel Ballard Guide to Seattle">
  <meta property="og:description" content="547 guest reviews, 52 experiences, curated by Hotel Ballard staff">
  <meta property="og:image" content="https://guidebooks.mztape.com/hotel-ballard/cover.jpg">
  <meta property="og:url" content="https://guidebooks.mztape.com/hotel-ballard-seattle">

  <!-- Twitter Card -->
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="The Hotel Ballard Guide to Seattle">

  <!-- Schema.org structured data -->
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "Book",
    "name": "The Hotel Ballard Guide to Seattle",
    "author": {
      "@type": "Organization",
      "name": "Hotel Ballard"
    },
    "aggregateRating": {
      "@type": "AggregateRating",
      "ratingValue": "4.8",
      "reviewCount": "547"
    },
    "offers": {
      "@type": "Offer",
      "price": "20.00",
      "priceCurrency": "USD"
    }
  }
  </script>
</head>
```

**Content structure for SEO:**

```html
<!-- H1: Main title -->
<h1>The Hotel Ballard Guide to Seattle</h1>

<!-- H2: Card sections -->
<h2>Romantic Dinner Experiences</h2>

<!-- H3: Individual destinations -->
<h3>Giuseppe's Italian Restaurant</h3>

<!-- Rich content -->
<p>Located in Capitol Hill, Giuseppe's has been a favorite among
Hotel Ballard guests for romantic dinners...</p>

<!-- Review snippets -->
<blockquote>
  "Best carbonara in Seattle!" - Guest review, Sept 2025
</blockquote>

<!-- Internal links -->
<a href="#family-adventures">See family-friendly options</a>
```

### Sitemap

```xml
<!-- /sitemap.xml -->
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <!-- Marketplace homepage -->
  <url>
    <loc>https://guidebooks.mztape.com</loc>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>

  <!-- Individual guidebooks -->
  <url>
    <loc>https://guidebooks.mztape.com/hotel-ballard-seattle</loc>
    <lastmod>2025-10-13</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>

  <!-- City pages -->
  <url>
    <loc>https://guidebooks.mztape.com/cities/seattle</loc>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

### Target Keywords

**Long-tail, high-intent:**
- "best romantic dinner Capitol Hill Seattle"
- "family-friendly restaurants Seattle with kids"
- "hidden gems Pike Place Market"
- "Seattle boutique hotel recommendations"
- "authentic Seattle experiences locals"
- "where to eat in Seattle not touristy"

**Strategy:**
- Each guidebook = 200+ pages of content
- 100 guidebooks = 20,000 pages indexed by Google
- Target 50+ long-tail keywords per guidebook
- Combined: 5,000+ keyword rankings across platform

---

## PDF Export

### Generation Process

```javascript
// Using Puppeteer for HTML → PDF conversion

async function generatePDF(guidebookId, options = {}) {
  const guidebook = await getGuidebook(guidebookId);
  const template = templates[options.template || 'classic'];

  // 1. Render HTML (with print-specific CSS)
  const html = await template.render(guidebook, {
    mode: 'print',
    includePhotos: options.includePhotos ?? true,
    includeReviews: options.includeReviews ?? true
  });

  // 2. Launch headless browser
  const browser = await puppeteer.launch();
  const page = await browser.newPage();

  // 3. Load HTML
  await page.setContent(html);

  // 4. Wait for images to load
  await page.waitForSelector('img', {timeout: 10000});

  // 5. Generate PDF
  const pdf = await page.pdf({
    format: 'Letter', // 8.5" × 11"
    printBackground: true,
    margin: {
      top: '0.75in',
      right: '0.5in',
      bottom: '0.75in',
      left: '0.5in'
    },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: `
      <div style="font-size: 10px; text-align: center; width: 100%;">
        <span class="pageNumber"></span> / <span class="totalPages"></span>
      </div>
    `
  });

  await browser.close();

  // 6. Upload to S3
  const key = `guidebooks/${guidebookId}/export.pdf`;
  await s3.putObject({
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: pdf,
    ContentType: 'application/pdf',
    ACL: 'public-read'
  });

  return {
    url: `https://cdn.mztape.com/${key}`,
    size: pdf.length
  };
}
```

### Print-Ready Specifications

**For print partners (Blurb, Lulu, PrintNinja):**

```javascript
const printSpecs = {
  // Page size
  trim: {
    pocket: {width: '5in', height: '7in'},
    standard: {width: '6in', height: '9in'},
    coffeeTable: {width: '8in', height: '11in'}
  },

  // Bleed
  bleed: '0.125in', // Extend images beyond trim

  // Color mode
  colorMode: 'CMYK', // Not RGB (for print)

  // Resolution
  imageResolution: '300dpi', // Minimum for print quality

  // Fonts
  embedFonts: true, // Ensure fonts render correctly

  // PDF version
  pdfVersion: 'PDF/X-1a:2001' // Industry standard for print
};
```

---

## White Label Support

**Premium tier feature: Remove mztape branding**

### Default (Free tier):

```html
<!-- Footer on every page -->
<footer>
  <p>Powered by <a href="https://mztape.com">mztape</a></p>
</footer>
```

### White label (Premium tier):

```html
<!-- No mztape branding -->
<footer>
  <p>© 2025 Hotel Ballard. All rights reserved.</p>
</footer>
```

**Implementation:**

```javascript
// Check hotel's tier
const hotel = await getHotel(guidebook.hotel_id);
const isPremium = hotel.subscription_tier === 'premium';

// Conditionally render branding
<Footer>
  {!isPremium && (
    <BrandingLink href="https://mztape.com">
      Powered by mztape
    </BrandingLink>
  )}

  <Copyright hotel={hotel} />
</Footer>
```

---

## Development Roadmap

### Phase 1: Core Publishing (Month 12-13, 6 weeks)

**Build:**
- [ ] Guidebook generator service
  - [ ] Query builder (database → guidebook data)
  - [ ] Template system (adapt CCS trail templates)
  - [ ] HTML renderer
  - [ ] PDF generator (Puppeteer)
- [ ] Static site setup
  - [ ] Next.js app at guidebooks.mztape.com
  - [ ] Individual guidebook pages
  - [ ] Deploy to Vercel
- [ ] Hotel dashboard integration
  - [ ] "Publish Guidebook" button
  - [ ] Preview before publishing
  - [ ] Regenerate button (update content)

**Test:**
- [ ] Generate 5 test guidebooks
- [ ] Verify rendering (web + PDF)
- [ ] Check mobile responsiveness
- [ ] Validate SEO (meta tags, schema.org)

---

### Phase 2: Marketplace (Month 13-14, 4 weeks)

**Build:**
- [ ] Marketplace homepage
  - [ ] Featured guidebooks
  - [ ] Search/filter
  - [ ] City browser
  - [ ] Category browser
- [ ] Individual guidebook pages
  - [ ] Hero section
  - [ ] Preview content
  - [ ] Reader reviews
  - [ ] Hotel info
- [ ] Reading experience
  - [ ] Full guidebook renderer
  - [ ] Table of contents
  - [ ] Print CTA
  - [ ] Hotel booking CTA

**Test:**
- [ ] User testing (browse, search, read)
- [ ] Mobile experience
- [ ] Load testing (100 guidebooks)

---

### Phase 3: Analytics (Month 14-15, 2 weeks)

**Build:**
- [ ] Event tracking (client-side)
- [ ] Analytics database (guidebook_analytics table)
- [ ] Hotel dashboard
  - [ ] Pageviews
  - [ ] Traffic sources
  - [ ] Popular destinations
  - [ ] Conversion funnel
  - [ ] Geographic breakdown

**Test:**
- [ ] Track 1,000 pageviews
- [ ] Verify accuracy (compare to Vercel analytics)
- [ ] Dashboard usability

---

### Phase 4: Premium Features (Month 15-16, 4 weeks)

**Build:**
- [ ] Custom domain support
  - [ ] Vercel domains API integration
  - [ ] DNS verification
  - [ ] SSL provisioning
  - [ ] Routing middleware
- [ ] White label
  - [ ] Conditional branding
  - [ ] Custom CSS
  - [ ] Hotel-specific footer
- [ ] Email capture
  - [ ] Newsletter signup forms
  - [ ] Mailchimp/ConvertKit integration
  - [ ] Export subscriber list

**Test:**
- [ ] Set up custom domain for 3 test hotels
- [ ] Verify white label works
- [ ] Test email integration

---

### Phase 5: Polish & Launch (Month 16-17, 4 weeks)

**Build:**
- [ ] SEO optimization
  - [ ] Meta tags for all pages
  - [ ] Schema.org markup
  - [ ] Sitemap generation
  - [ ] robots.txt
- [ ] Social sharing
  - [ ] Open Graph tags
  - [ ] Twitter Cards
  - [ ] Share buttons
- [ ] Performance
  - [ ] Image optimization (Next.js Image)
  - [ ] Lazy loading
  - [ ] CDN caching
- [ ] Documentation
  - [ ] Hotel publishing guide
  - [ ] Custom domain setup instructions
  - [ ] SEO best practices

**Launch:**
- [ ] 10 pilot hotels publish guidebooks
- [ ] Press release
- [ ] Social media announcement
- [ ] Monitor analytics

---

## Technical Stack Summary

**Frontend:**
- Next.js 14 (App Router, SSG)
- React 18
- Tailwind CSS
- TypeScript

**Backend:**
- Existing QRCards API (Supabase)
- Vercel Serverless Functions (API routes)
- Puppeteer (PDF generation)

**Hosting:**
- Vercel (static site + serverless)
- Cloudflare (DNS + CDN)
- AWS S3 (PDF storage)

**Database:**
- Existing QRCards database (Supabase/Postgres)
- New tables: guidebooks, guidebook_analytics, marketplace_reviews

**Integrations:**
- Vercel Domains API (custom domains)
- Stripe API (print purchases - future)
- Mailchimp/ConvertKit API (email capture)
- Blurb/Lulu API (print fulfillment - future)

**Cost (100 guidebooks):**
- Vercel: Free
- Cloudflare: Free
- S3: $5/month
- Puppeteer: $0 (run on Vercel)
- **Total: $5/month**

---

## Success Metrics

### Technical Metrics

**Month 13 (Launch):**
- 10 guidebooks published
- 1,000 pageviews
- <2s page load time
- 0 errors
- 100% uptime

**Month 18 (Growth):**
- 50 guidebooks published
- 10,000 pageviews/month
- 95+ Lighthouse score
- <1% error rate
- 99.9% uptime

**Year 2 (Scale):**
- 250 guidebooks published
- 100,000 pageviews/month
- <1s page load time
- Top 10 Google rankings for target keywords

---

### Business Metrics

**Month 13:**
- 5 hotels opt for custom domain (+$29/month)
- 50 PDF downloads
- 10 print purchases

**Month 18:**
- 20 hotels on premium tier ($580/month)
- 1,000 PDF downloads/month
- 500 print purchases/month

**Year 2:**
- 100 hotels on premium tier ($2,900/month)
- 10,000 PDF downloads/month
- 5,000 print purchases/month
- SEO driving 50% of marketplace traffic

---

## Risk Mitigation

### Risk 1: PDF generation slow/expensive

**Mitigation:**
- Generate PDFs asynchronously (background job)
- Cache PDFs (regenerate only when content updated)
- Use Puppeteer efficiently (reuse browser instances)
- Consider alternative: LaTeX or headless Chrome via API

### Risk 2: Static site doesn't scale

**Mitigation:**
- Vercel auto-scales (handles 1M+ pageviews)
- CDN caching (edge servers worldwide)
- If needed: Migrate to Cloudflare Pages (unlimited bandwidth)

### Risk 3: Custom domains complex

**Mitigation:**
- Start without custom domains (Month 12-15)
- Add later once core proven (Month 15+)
- Clear documentation for DNS setup
- Offer managed DNS service ($10/month)

### Risk 4: SEO doesn't work

**Mitigation:**
- Focus on hotel's own marketing (email, social) first
- SEO is bonus, not dependency
- Build content depth (200+ pages per guidebook)
- Get backlinks (hotel websites link to guidebook)

---

## Recommendation

**Phase 1-2 are MVP (Month 12-14, 10 weeks):**
- Core publishing (generate, host, display)
- Marketplace (discovery, browsing)
- No premium features yet

**Phase 3-4 add monetization (Month 14-16, 6 weeks):**
- Analytics (prove value to hotels)
- Custom domains + white label (premium tier)

**Phase 5 is polish (Month 16-17, 4 weeks):**
- SEO, performance, docs
- Launch to 10 pilot hotels

**Total timeline: 5 months (Month 12-17)**
**Team: 1 full-stack developer**
**Cost: $5-40/month infrastructure**

---

**Document Version:** 1.0
**Date:** October 13, 2025
**Purpose:** Technical specification for digital guidebook publishing platform
**Timeline:** Month 12-17 (5 months development)
**Key Insight:** Reuse existing QRCards infrastructure + CCS trail templates = Fast MVP
