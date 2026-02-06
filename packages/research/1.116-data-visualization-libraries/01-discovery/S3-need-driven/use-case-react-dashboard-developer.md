# Use Case: React Dashboard Developer

## Who Needs This

**Persona:** Sarah, Frontend Developer at a Series B SaaS Startup

**Background:**
- 3 years React experience
- Building internal analytics dashboard
- Team of 5 engineers (2 frontend, 3 backend)
- Shipping features weekly

**Technical Context:**
- React 18, TypeScript, Vite
- Existing component library (shadcn/ui)
- Data from REST API (~100-500 data points per chart)
- Desktop-first, responsive secondary

## Why They Need It

### Core Need

Display sales metrics, user growth, and system health on an admin dashboard.

**Chart requirements:**
- Line charts (time series trends)
- Bar charts (category comparisons)
- Pie charts (conversion funnel)
- Standard, not custom designs

### Pain Points Without a Library

**1. Building from scratch is slow**
- Calculating scales manually: 2-3 hours
- Drawing axes with ticks: 2-3 hours
- Adding tooltips: 3-4 hours
- Result: 1 week for a single chart type

**2. Maintaining custom code**
- Edge cases (empty data, single data point)
- Browser compatibility (Safari, Firefox)
- Responsive behavior
- Result: Ongoing maintenance burden

**3. TypeScript integration**
- Need types for data shapes
- Autocomplete for chart options
- Type-safe event handlers

**4. Team velocity**
- Backend expects charts "done in a day"
- Custom code slows feature delivery
- Can't iterate quickly on designs

### What Success Looks Like

**Development speed:**
- First chart: < 1 hour
- Additional charts: < 30 minutes
- Iterate on design: < 15 minutes

**Code quality:**
- Type-safe (no runtime errors)
- Testable (unit + visual regression)
- Maintainable (minimal custom code)

**User experience:**
- Responsive (mobile + desktop)
- Interactive (tooltips, legends)
- Accessible (WCAG AA)

## Requirements Analysis

### Must-Have
- React components (JSX, not config objects)
- TypeScript support (shipped types)
- Standard chart types (line, bar, pie)
- Built-in tooltips and legends
- Responsive container
- Active maintenance (monthly releases)

### Nice-to-Have
- Animation (smooth transitions)
- Customization (colors, styles)
- Small bundle size (< 150 KB)
- Good documentation

### Don't Need
- 10,000+ data points (only ~500)
- Custom chart types (standard is fine)
- Canvas rendering (SVG is fine)
- React Native support

## Library Evaluation

### Option 1: Recharts ⭐ **RECOMMENDED**

**Pros:**
- ✅ Declarative JSX API (feels like React)
- ✅ TypeScript support (excellent)
- ✅ 9M weekly downloads (mature, stable)
- ✅ Built-in tooltips, legends, responsive container
- ✅ Covers all needed chart types
- ✅ Great documentation and examples

**Cons:**
- ❌ 130 KB gzipped (medium-large bundle)
- ❌ SVG only (fine for 500 points)
- ❌ Limited customization (ok for internal tools)

**Code example:**
```tsx
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

function SalesChart({ data }: { data: SalesData[] }) {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="revenue" stroke="#8884d8" />
      </LineChart>
    </ResponsiveContainer>
  )
}
```

**Time to first chart:** 30 minutes (including setup)

### Option 2: Nivo

**Pros:**
- ✅ Declarative React API
- ✅ TypeScript support
- ✅ Beautiful defaults (great aesthetics)
- ✅ More chart types than Recharts

**Cons:**
- ❌ 500K weekly downloads (10x less than Recharts)
- ❌ Smaller community (fewer examples)
- ❌ 180 KB gzipped (larger bundle)

**Why not chosen:** Smaller community, larger bundle, no clear advantage over Recharts.

### Option 3: Chart.js

**Pros:**
- ✅ 60 KB gzipped (smallest)
- ✅ Excellent documentation
- ✅ Handles 1000-10K points

**Cons:**
- ❌ Imperative API (config objects, not JSX)
- ❌ Canvas rendering (less accessible)
- ❌ Feels awkward in React

**Code example:**
```tsx
import { Line } from 'react-chartjs-2'

function SalesChart({ data }: { data: SalesData[] }) {
  return (
    <Line
      data={{
        labels: data.map(d => d.date),
        datasets: [{ data: data.map(d => d.revenue) }]
      }}
      options={{ responsive: true }}
    />
  )
}
```

**Why not chosen:** Imperative API doesn't fit React idioms, Canvas less accessible.

### Option 4: D3 / visx

**Pros:**
- ✅ Maximum flexibility
- ✅ Full control over design

**Cons:**
- ❌ Steep learning curve (D3 knowledge required)
- ❌ More code per chart (20+ lines)
- ❌ No built-in tooltips/legends (build yourself)
- ❌ Slow development (overkill for standard charts)

**Why not chosen:** Overkill for standard charts, slows team velocity.

## Recommended Solution

**Library:** Recharts

**Why:**
1. **Fastest time to value** - JSX API is natural for React developers
2. **Mature ecosystem** - 9M downloads, active maintenance, many examples
3. **Covers all needs** - Line, bar, pie + tooltips, legends, responsive
4. **TypeScript first-class** - Excellent type coverage
5. **Good enough** - Internal tool doesn't need pixel-perfection

**Trade-offs accepted:**
- Bundle size (130 KB) - Acceptable for internal tool
- Limited customization - Standard charts don't need it
- SVG performance ceiling - 500 points is well under limit

## Implementation Plan

**Week 1:**
- Install Recharts + types
- Create reusable chart wrapper components
- Implement first 3 charts (line, bar, pie)
- Set up visual regression tests

**Week 2:**
- Add remaining chart types
- Implement loading states
- Error handling (empty data, API failures)
- Mobile responsive tweaks

**Week 3:**
- Accessibility audit (ARIA labels)
- Performance optimization (memoization)
- Documentation for team

**Expected outcome:** Complete dashboard in 3 weeks, vs 8+ weeks custom-building.

## Success Metrics

**Development:**
- Time to first chart: < 1 hour ✓
- Time per additional chart: < 30 min ✓
- Code duplication: Minimal (reusable wrapper components)

**Runtime:**
- Bundle size impact: +130 KB (acceptable)
- Render time: < 50ms per chart (smooth)
- Accessibility: WCAG AA compliance

**Team:**
- Velocity maintained (weekly feature releases)
- Backend satisfied with chart speed
- No ongoing maintenance burden

## Lessons Learned

**What worked:**
- Recharts JSX API felt natural to team
- TypeScript caught data shape errors early
- Built-in responsiveness saved time

**What didn't:**
- Customization harder than expected (worked around with CSS)
- Animation performance with 500 points (disabled animations)

**Would do differently:**
- Test bundle size impact earlier
- Set up visual regression tests from day 1
- Create design system for chart colors upfront

## Related Personas

- **Junior React Developer** - Same needs, even more benefits from Recharts
- **Freelance Developer** - Recharts speeds up client work
- **Agency Team** - Recharts works well for multiple projects
