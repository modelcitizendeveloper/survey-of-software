# S3 Recommendation: Matching Libraries to User Needs

## Key Insight: One Size Does NOT Fit All

The "best" data visualization library **depends entirely on who you are and what you need**.

### The Anti-Pattern: Choosing by Popularity

**Common mistake:**
- See Recharts has 9M downloads
- Assume "most popular = best for me"
- Pick Recharts without evaluating needs

**Reality:**
- Recharts great for React dashboards (< 1K points)
- Terrible for 100K point datasets (use ECharts)
- Terrible for custom charts (use visx or D3)

**Lesson:** Match library to **your specific needs**, not just popularity.

## Decision Tree by User Type

### Are you building a React dashboard?

**YES** → Continue to React decision tree
**NO** → Jump to framework-agnostic options

#### React Dashboard Decision Tree

**1. Data size?**
- < 1000 points → Standard charts? (YES: Recharts, NO: visx)
- 1000-10K points → ECharts (Canvas)
- 10K+ points → ECharts (WebGL)

**2. Standard vs Custom?**
- Standard charts (line, bar, pie) → Recharts
- Custom designs → visx
- Novel visualizations → D3

**3. Team experience?**
- Junior team → Recharts (easier)
- Senior team + D3 knowledge → visx (more control)

**4. SSR required?**
- YES → Nivo (best SSR), visx (good SSR)
- NO → Recharts (simpler)

### Are you building a React Native app?

**YES** → Victory Native (only viable option)

### Are you framework-agnostic or using Vue/Angular?

**1. Data size?**
- < 10K points → Chart.js (simplest, smallest)
- 10K+ points → ECharts (performance)

**2. Feature richness?**
- Need 100+ chart types → ECharts
- Standard charts sufficient → Chart.js

**3. Custom visualizations?**
- YES → D3 (maximum power)
- NO → Chart.js or ECharts

## User Persona Summary

| Persona | Primary Need | Recommended Library | Why |
|---------|--------------|---------------------|-----|
| React Dashboard Developer | Fast development, standard charts | Recharts | JSX API, built-in features, 9M downloads |
| Data Scientist | Large datasets, interactivity | ECharts | 100K+ points, Canvas/WebGL, data zoom |
| Custom Designer | Pixel-perfect, unique charts | visx | D3 + React, full control, small bundle |
| Mobile Developer | React Native, touch gestures | Victory Native | Native support, touch interactions |
| Full-Stack (SSR) | Server-side rendering | Nivo | Built for SSR, beautiful defaults |
| Agency (Multi-framework) | Works everywhere | Chart.js | 60 KB, framework-agnostic, simple |
| Data Journalist | Custom storytelling | D3 | Novel visualizations, maximum flexibility |

## Common Scenarios

### Scenario 1: Internal Analytics Dashboard

**Context:** Small startup, internal tools, 2 frontend developers

**Needs:**
- Quick development (ship weekly)
- Standard charts (revenue, users, funnels)
- < 1000 data points
- React stack

**Recommendation:** **Recharts**

**Why:**
- Fastest time to first chart (< 1 hour)
- JSX feels natural to React developers
- Built-in tooltips, legends (don't rebuild)
- 9M downloads = mature, stable

**Not ECharts:** Overkill for small datasets, config API slower to learn
**Not D3/visx:** Too much code for standard charts

### Scenario 2: Real-Time Monitoring Dashboard

**Context:** DevOps team, monitoring metrics, 10K-100K data points

**Needs:**
- Handle 10K+ points smoothly
- Real-time updates (every second)
- Zoom/pan (explore time windows)
- Framework-agnostic (Vue stack)

**Recommendation:** **ECharts**

**Why:**
- Canvas rendering handles 100K points
- Built-in data zoom, pan controls
- Progressive rendering for real-time
- Works in any framework

**Not Recharts:** SVG chokes at 2K points
**Not Chart.js:** Ceiling at 10K points, missing features

### Scenario 3: Marketing Website Infographic

**Context:** Design agency, client work, custom branded visualization

**Needs:**
- Pixel-perfect match to Figma design
- Custom animations (staggered entry)
- Unique chart type (not standard)
- React stack

**Recommendation:** **visx + react-spring**

**Why:**
- Full control over every pixel
- D3 scales (don't reimplement math)
- React components (not DOM mutations)
- react-spring for smooth animations

**Not Recharts:** Can't match custom designs
**Not D3 alone:** Imperative API conflicts with React

### Scenario 4: Fitness Tracking Mobile App

**Context:** Solo mobile developer, React Native, iOS + Android

**Needs:**
- React Native compatibility
- Touch-optimized (no hover)
- Offline-capable
- Cross-platform (single codebase)

**Recommendation:** **Victory Native**

**Why:**
- Built for React Native (not web port)
- Touch gestures built-in
- Works offline (no web dependencies)
- iOS + Android support

**Not Recharts:** Web-only, doesn't work in RN
**Not Chart.js:** Requires Canvas polyfill

### Scenario 5: Scientific Research Platform

**Context:** Research team, Python + web frontend, large datasets

**Needs:**
- 100K-1M data points (sensor data)
- 3D visualizations (parameter spaces)
- Export charts (publications)
- Framework-agnostic (minimal JS)

**Recommendation:** **ECharts + echarts-gl**

**Why:**
- WebGL handles 1M+ points
- 3D charts built-in (scatter3D, surface3D)
- Export to PNG (publication-ready)
- Simple JavaScript (minimal learning)

**Not Plotly:** Performance ceiling at 50K points
**Not D3:** Too much JavaScript expertise required

## Red Flags: When You've Chosen Wrong

### You picked Recharts, but...

**Red flag 1:** Charts lag with 2K points
→ **Fix:** Switch to ECharts (Canvas)

**Red flag 2:** Design team wants custom aesthetics
→ **Fix:** Switch to visx (more control)

**Red flag 3:** Need React Native version
→ **Fix:** Switch to Victory Native

### You picked D3, but...

**Red flag 1:** Spending weeks on standard bar chart
→ **Fix:** Use Recharts for standard charts, D3 for custom

**Red flag 2:** Hydration errors in React
→ **Fix:** Use visx (D3 math, React rendering)

**Red flag 3:** Junior team struggling with API
→ **Fix:** Use Recharts (gentler learning curve)

### You picked ECharts, but...

**Red flag 1:** Only have 500 data points
→ **Fix:** Use Recharts or Chart.js (simpler, smaller)

**Red flag 2:** Bundle size is critical (mobile)
→ **Fix:** Use Chart.js (60 KB vs 150 KB)

**Red flag 3:** Need pixel-perfect custom design
→ **Fix:** Use D3 or visx (more control)

## Migration Paths

### From Recharts to ECharts (performance)

**When:** Hitting 1K+ point performance wall

**Effort:** 1-2 weeks (API change: JSX → config)

**Strategy:**
1. Migrate one chart at a time
2. Run both libraries temporarily
3. Use ECharts only for large datasets

### From Recharts to visx (customization)

**When:** Design requirements exceed Recharts capabilities

**Effort:** 2-4 weeks (learning D3 + visx)

**Strategy:**
1. Keep Recharts for standard charts
2. Use visx only for custom visualizations
3. Share reusable visx components

### From vanilla D3 to visx (React integration)

**When:** D3 DOM mutations causing React bugs

**Effort:** 1-2 weeks (same D3 concepts, different rendering)

**Strategy:**
1. Keep D3 scales and math
2. Replace `.select().join()` with JSX
3. Migrate chart by chart

## Final Recommendations by Priority

### Priority 1: Match Your Data Size

| Data Points | Library |
|-------------|---------|
| < 1000 | Any SVG library (Recharts, visx, Nivo) |
| 1K-10K | Canvas library (Chart.js, ECharts) |
| 10K+ | ECharts (Canvas or WebGL) |

**Most common mistake:** Using SVG for large datasets.

### Priority 2: Match Your Framework

| Framework | Library |
|-----------|---------|
| React (standard charts) | Recharts |
| React (custom charts) | visx |
| React Native | Victory Native |
| Vue/Angular/None | Chart.js or ECharts |

**Most common mistake:** Fighting framework integration.

### Priority 3: Match Your Team Skills

| Experience | Library |
|------------|---------|
| Junior (< 2 years) | Recharts, Chart.js |
| Mid (2-5 years) | ECharts, Nivo |
| Senior (5+ years) | visx, D3 |

**Most common mistake:** Picking advanced library for junior team.

### Priority 4: Match Your Timeline

| Timeline | Library |
|----------|---------|
| Days | Recharts, Chart.js |
| Weeks | ECharts, Nivo, Victory |
| Months | visx, D3 |

**Most common mistake:** Picking D3 with tight deadline.

## Conclusion

**The "best" library is the one that:**
1. Handles your data size
2. Works in your framework
3. Matches your team's skills
4. Fits your timeline
5. Meets your customization needs

**Default recommendations:**
- **React dashboard:** Recharts (until you hit limits)
- **Large datasets:** ECharts (performance matters)
- **Custom designs:** visx (control matters)
- **Mobile:** Victory Native (only choice)
- **Framework-agnostic:** Chart.js (simplest)

**When in doubt:** Start simple (Recharts, Chart.js), upgrade when needed.

---

**Next step:** S4 (strategic analysis) evaluates long-term viability and ecosystem health.
