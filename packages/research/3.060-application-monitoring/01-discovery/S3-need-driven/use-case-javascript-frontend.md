# Use Case: JavaScript Frontend Application
## Client-Side Error Tracking for SPAs

**Pattern**: Frontend-focused application with API backend
**Stack**: React/Vue/Next.js, TypeScript, REST/GraphQL API
**Example**: Modern SPA dashboard, e-commerce frontend, mobile web app

---

## Scenario Description

### Who This Is For

- Frontend teams building React/Vue/Next.js applications
- Single-page applications (SPAs) with client-side routing
- Progressive web apps (PWAs)
- JAMstack sites with dynamic features
- Mobile-responsive web applications

### Typical Architecture

```
Browser → React/Vue SPA → REST/GraphQL API
   ↓
localStorage/IndexedDB
   ↓
Third-party scripts (Analytics, Chat, Ads)
```

### Pain Points to Solve

1. JavaScript errors breaking UI (null reference, undefined variables)
2. Network failures from API calls (500 errors, timeouts)
3. Cross-browser compatibility issues (Safari vs Chrome)
4. Third-party script errors (ad blockers, privacy extensions)
5. Performance issues (slow renders, memory leaks)
6. User-reported "broken page" with no details

---

## Requirements Profile

### Must-Have Features

- **JavaScript SDK** optimized for bundle size (<10KB gzipped)
- **Source map support** to debug minified production code
- **Breadcrumbs** showing user clicks, navigations, API calls
- **Session replay** (video-like playback of user actions)
- **Network monitoring** (XHR/Fetch request tracking)
- **Browser context** (OS, browser version, screen size)
- **Error filtering** (block third-party script noise)

### Nice-to-Have Features

- Framework integrations (React Error Boundary, Vue error handler)
- Performance monitoring (Core Web Vitals, LCP, FID, CLS)
- Release tracking (correlate errors with deployments)
- User feedback widget (let users report issues)
- Privacy controls (PII scrubbing, GDPR compliance)

### Budget Reality

- Side project: $0/month (free tier)
- Startup: $25-100/month
- Growth: $100-500/month
- Enterprise: $500-2,000/month

### Error Volume Estimate

- Low traffic (10K pageviews/month): 1K-5K errors/month
- Medium traffic (100K pageviews/month): 10K-50K errors/month
- High traffic (1M pageviews/month): 100K-500K errors/month
- Very high traffic (10M pageviews/month): 1M+ errors/month

---

## Provider Fit Analysis

### Sentry (Score: 90/100)

**Strengths:**
- Excellent React/Vue integrations with Error Boundaries
- Source map upload for production debugging
- Session replay (paid feature)
- Performance monitoring (Core Web Vitals)
- Privacy controls (beforeSend hook for PII scrubbing)

**Pricing for Frontend:**
- Free: 5K errors/month
- Team ($26/mo): 50K errors/month
- Business ($80/mo): 500K errors/month + session replay

**Bundle Size:** 22KB gzipped (React SDK)

**TCO (12 months):**
- Low traffic: $0 (free tier)
- Medium traffic: $312/year (Team)
- High traffic: $960/year (Business)

**Integration Effort:** 2 hours (NPM install, source map setup)

### TrackJS (Score: 95/100)

**Strengths:**
- Purpose-built for JavaScript (smallest bundle: 8KB gzipped)
- Telemetry timeline (visual playback of events before error)
- Network monitoring (all XHR/Fetch calls)
- Console monitoring (captured console.log/warn/error)
- Visitor timeline (see all errors from one user)
- No source map requirement (optional)

**Pricing for Frontend:**
- Starter ($49/mo): 100K pageviews, unlimited users
- Standard ($99/mo): 500K pageviews
- Premium ($249/mo): 2M pageviews

**Bundle Size:** 8KB gzipped (smallest in market)

**TCO (12 months):**
- Low traffic: $588/year (Starter)
- Medium traffic: $588/year (Starter)
- High traffic: $1,188/year (Standard)

**Integration Effort:** 1 hour (CDN or NPM, no build config)

### Bugsnag (Score: 82/100)

**Strengths:**
- Session tracking (errors per session)
- Breadcrumbs with automatic click tracking
- Release stages (dev, staging, production)
- Good React Native support (if adding mobile)

**Pricing for Frontend:**
- Free: 7,500 events/month
- Lite ($18/mo): 50K events/month
- Standard ($59/mo): 200K events/month

**Bundle Size:** 15KB gzipped

**TCO (12 months):**
- Low traffic: $0 (free tier)
- Medium traffic: $216/year (Lite)
- High traffic: $708/year (Standard)

**Integration Effort:** 2 hours (NPM install, React plugin)

### Rollbar (Score: 85/100)

**Strengths:**
- Telemetry (DOM events, console, network)
- People tracking (group errors by user)
- RQL for custom queries
- Spike protection (no overage charges)
- Good Next.js support

**Pricing for Frontend:**
- Free: 5K errors/month
- Essentials ($24.17/mo): 50K errors/month
- Advanced ($99/mo): 500K errors/month

**Bundle Size:** 18KB gzipped

**TCO (12 months):**
- Low traffic: $0 (free tier)
- Medium traffic: $290/year (Essentials)
- High traffic: $1,188/year (Advanced)

**Integration Effort:** 3 hours (NPM + telemetry config)

### Honeybadger (Score: 75/100)

**Strengths:**
- Simple pricing (unlimited users)
- Uptime monitoring included
- Good documentation
- Privacy-focused (GDPR compliant)

**Weaknesses:**
- Less feature-rich for frontend than Sentry/TrackJS
- No session replay
- Larger bundle size

**Pricing for Frontend:**
- Free: 5K errors/month
- Small ($39/mo): 150K errors/month
- Medium ($89/mo): 600K errors/month

**Bundle Size:** 25KB gzipped (largest)

**TCO (12 months):**
- Low traffic: $0 (free tier)
- Medium traffic: $468/year (Small)
- High traffic: $468/year (Small)

**Integration Effort:** 2 hours (NPM install)

### Datadog Real User Monitoring (Score: 78/100)

**Strengths:**
- Full observability (RUM + APM + Logs)
- Advanced analytics and dashboards
- Heatmaps and session replay
- Best for teams already using Datadog backend

**Weaknesses:**
- Expensive for frontend-only use case
- Complex pricing
- Heavier bundle

**Pricing for Frontend:**
- RUM: $1.50 per 1,000 sessions
- Session Replay: Additional $3.60 per 1,000 replays
- Typical: 100K sessions/month = $150/month base

**Bundle Size:** 30KB+ gzipped

**TCO (12 months):**
- Low traffic: $180/year (10K sessions)
- Medium traffic: $1,800/year (100K sessions)
- High traffic: $18,000/year (1M sessions)

**Integration Effort:** 4 hours (CDN + RUM config + dashboards)

---

## Recommendation

### Top Choice: TrackJS (95/100)

**Why TrackJS wins for JavaScript frontends:**
1. **Purpose-built for frontend** - Every feature designed for browser errors
2. **Telemetry timeline** - Visual playback better than breadcrumbs
3. **Smallest bundle** - 8KB won't hurt performance
4. **Network monitoring** - See all failed API calls
5. **Simple pricing** - Based on pageviews, not errors

**When to choose TrackJS:**
- Pure frontend/SPA application
- Performance-sensitive (every KB matters)
- High error volume (pageview pricing is predictable)
- Team focused on user experience

**Migration Path:**
- Start: Starter plan ($49/mo) for 100K pageviews
- Growth: Standard plan ($99/mo) at 500K pageviews
- Scale: Premium plan ($249/mo) at 2M pageviews

### Runner-Up: Sentry (90/100)

**When to choose Sentry:**
- You have both frontend AND backend (unified platform)
- You need session replay (visual recording)
- You want performance monitoring (Core Web Vitals)
- You're already using Sentry for backend

**Trade-offs vs TrackJS:**
- Larger bundle (22KB vs 8KB)
- Event-based pricing (can get expensive)
- Better integration ecosystem
- More features beyond error tracking

### Budget Alternative: Bugsnag (82/100)

**When to choose Bugsnag:**
- Budget-constrained startup
- Need mobile + web (React Native)
- Prioritize cost over features
- Don't need session replay

---

## Cost Comparison: 12-Month TCO

### Low Traffic (50K pageviews/month, 3K errors/month)
- **Sentry**: $0 (free)
- **TrackJS**: $588/year ($49/mo)
- **Bugsnag**: $0 (free)
- **Rollbar**: $0 (free)
- **Honeybadger**: $0 (free)
- **Datadog RUM**: $180/year

**Winner: Sentry/Bugsnag/Rollbar/Honeybadger (free)**

### Medium Traffic (500K pageviews/month, 30K errors/month)
- **Sentry**: $312/year (Team)
- **TrackJS**: $588/year (Starter covers 100K pageviews - needs upgrade to $1,188 Standard)
- **Bugsnag**: $216/year (Lite)
- **Rollbar**: $290/year (Essentials)
- **Honeybadger**: $468/year (Small)
- **Datadog RUM**: $1,800/year

**Winner: Bugsnag ($216/year), but Sentry better value for features**

### High Traffic (5M pageviews/month, 300K errors/month)
- **Sentry**: $960/year (Business + session replay)
- **TrackJS**: $2,988/year (Premium)
- **Bugsnag**: $708/year (Standard)
- **Rollbar**: $1,188/year (Advanced)
- **Honeybadger**: $468/year (Small)
- **Datadog RUM**: $9,000/year (expensive!)

**Winner: Honeybadger ($468/year), but lacks session replay**

---

## Bundle Size Impact

**Performance Matters for Frontend:**

- **TrackJS**: 8KB (best)
- **Bugsnag**: 15KB
- **Rollbar**: 18KB
- **Sentry**: 22KB
- **Honeybadger**: 25KB
- **Datadog**: 30KB+ (worst)

For performance-critical apps (e-commerce, media), every KB counts. TrackJS's 8KB bundle won't impact Core Web Vitals.

---

## Implementation Guide

### TrackJS Setup (Recommended for Pure Frontend)

```javascript
// NPM installation
npm install trackjs

// src/index.js or App.jsx
import { TrackJS } from 'trackjs';

TrackJS.install({
  token: 'YOUR_TOKEN',
  application: 'my-react-app',

  // Capture everything before errors
  console: {
    enabled: true,
    display: true,
  },
  network: {
    enabled: true,
    error: true,
  },

  // Privacy controls
  onError: function(payload) {
    // Scrub PII before sending
    payload.message = payload.message.replace(/\b[\w._%+-]+@[\w.-]+\.[A-Z]{2,}\b/gi, '[email]');
    return true; // return false to ignore error
  },
});

// React Error Boundary (optional)
class ErrorBoundary extends React.Component {
  componentDidCatch(error, errorInfo) {
    TrackJS.track(error);
  }
  render() {
    return this.props.children;
  }
}
```

**Time to first error:** 10 minutes
**Time to full setup:** 1 hour

### Sentry Setup (Recommended for Full-Stack)

```javascript
// NPM installation
npm install @sentry/react

// src/index.js
import * as Sentry from "@sentry/react";
import { BrowserTracing } from "@sentry/tracing";

Sentry.init({
  dsn: "https://[key]@sentry.io/[project]",
  integrations: [
    new BrowserTracing(),
    new Sentry.Replay({
      maskAllText: true,
      blockAllMedia: true,
    }),
  ],

  // Performance Monitoring
  tracesSampleRate: 0.1, // 10% of transactions

  // Session Replay
  replaysSessionSampleRate: 0.1, // 10% of sessions
  replaysOnErrorSampleRate: 1.0, // 100% of sessions with errors

  // Environment
  environment: "production",
  release: "my-app@1.0.0",

  // Privacy
  beforeSend(event) {
    // Scrub sensitive data
    if (event.request) {
      delete event.request.cookies;
    }
    return event;
  },
});

// React Error Boundary (built-in)
import { ErrorBoundary } from "@sentry/react";

function App() {
  return (
    <ErrorBoundary fallback={<ErrorPage />}>
      <YourApp />
    </ErrorBoundary>
  );
}
```

**Time to first error:** 15 minutes
**Time to full setup:** 2 hours (with source maps)

---

## Key Takeaways

1. **TrackJS for pure frontend** - Best telemetry, smallest bundle, predictable pricing
2. **Sentry for full-stack** - Unified platform if you have backend errors too
3. **Watch bundle size** - Frontend performance matters (8KB vs 30KB)
4. **Session replay is critical** - See what users saw when error occurred
5. **Free tiers work for low traffic** - Sentry/Bugsnag free until 5K errors/month
6. **Avoid Datadog RUM for frontend-only** - 10x more expensive than alternatives
