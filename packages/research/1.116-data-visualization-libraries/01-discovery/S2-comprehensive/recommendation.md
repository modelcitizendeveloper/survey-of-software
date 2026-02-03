# S2 Recommendation: Technical Architecture Insights

## Key Technical Findings

### 1. Rendering Pipeline is the Performance Bottleneck

**SVG ceiling: ~1000 elements**
- Recharts, Nivo, visx, Victory: All hit same wall
- DOM overhead (layout, paint, GC) becomes prohibitive
- Solution: Switch to Canvas (Chart.js, ECharts)

**Canvas scales to ~10,000 elements**
- Chart.js: 10K points at 12 FPS (acceptable)
- ECharts: 10K points at 60 FPS (smooth)
- Trade-off: Lose DOM access, harder accessibility

**WebGL handles millions**
- ECharts-GL: 10M+ points smoothly
- GPU-accelerated geometry
- Complex setup, debugging harder

### 2. API Paradigm Affects Developer Productivity

**Declarative (Recharts, visx, Nivo) = Faster for React**
```tsx
// 5 lines, clear intent
<LineChart data={data}>
  <Line dataKey="value" />
</LineChart>
```

**Imperative (Chart.js, ECharts) = More powerful**
```javascript
// More verbose, but handles edge cases
chart.setOption({
  series: [{ type: 'line', data: [...] }]
})
```

**Low-level (D3, visx) = Maximum control**
```tsx
// 20+ lines, but pixel-perfect
<svg>
  {data.map(d => <circle cx={scale(d.x)} />)}
</svg>
```

**Recommendation:** Match paradigm to team skillset and project needs.

### 3. Bundle Size vs Features Trade-off

**Minimal (Chart.js: 60 KB)** → Few features, great performance
**Medium (Recharts: 130 KB)** → Good balance for dashboards
**Large (ECharts: 150-320 KB)** → Enterprise features justify size

**Tree-shaking winners:**
- visx: Excellent (30-60 KB for custom builds)
- D3: Excellent (15-50 KB for custom builds)
- ECharts: Moderate (150 KB minimum)

### 4. TypeScript Coverage is Uniformly Excellent

All modern libraries ship with types or have high-quality `@types/*` packages.

**Exception:** Victory has partial coverage.

### 5. Accessibility Requires SVG Rendering

**SVG libraries** (Recharts, D3, visx) → Screen readers can parse
**Canvas libraries** (Chart.js, ECharts) → Need ARIA workarounds

**Best accessibility:** Victory (built-in ARIA), ECharts SVG mode

### 6. React Integration Patterns

**Pattern 1: Library owns DOM** (Recharts, Nivo)
- Easiest, least flexible

**Pattern 2: D3 math, React rendering** (visx)
- More code, full control

**Pattern 3: D3 controls DOM** (anti-pattern)
- Don't do this in React

### 7. Animation Systems Vary Widely

**Built-in** (Recharts, Chart.js, ECharts, Victory)
- Convenient, limited customization

**Bring your own** (visx)
- Pair with react-spring or framer-motion
- More work, smoother results

**D3 transitions**
- Most powerful, but imperative API

## Decision Matrix by Technical Requirements

### Performance Requirements

**< 1000 points:**
- Any SVG library works (Recharts, visx, Nivo)
- Choose based on API preference

**1000-10,000 points:**
- Chart.js (simple) or ECharts (features)

**10,000+ points:**
- ECharts (Canvas or WebGL)
- Consider data decimation/sampling

### Bundle Size Constraints

**< 100 KB budget:**
- Chart.js (60 KB) or visx (30-60 KB)

**100-200 KB budget:**
- Recharts (130 KB) or ECharts tree-shaken (150 KB)

**No budget constraint:**
- ECharts full (320 KB) for maximum features

### Customization Needs

**Standard charts only:**
- Recharts (React) or Chart.js (agnostic)

**Pixel-perfect control:**
- visx (React) or D3 (agnostic)

**Novel visualizations:**
- D3 only (or visx for React)

### Framework Constraints

**React-only:**
- Recharts, visx, Nivo (declarative)
- Chart.js, ECharts (wrappers)

**Framework-agnostic:**
- Chart.js, ECharts, D3

**React Native:**
- Victory (only option)

### Accessibility Requirements

**Critical:**
- Victory (best built-in support)
- ECharts SVG mode (good ARIA)
- Avoid Canvas-only libraries

**Nice-to-have:**
- Any SVG library + manual ARIA

### SSR Requirements

**Must work:**
- Nivo (designed for SSR)
- visx (pure SVG, no issues)
- D3 (can generate server-side)

**Problematic:**
- Chart.js (Canvas requires browser)
- Recharts (hydration issues)

## Architecture Recommendations

### For Standard React Dashboards

**Stack:**
- Recharts (< 1K points) or ECharts (> 1K points)
- TypeScript for type safety
- Visual regression testing (Chromatic, Percy)

**Why:**
- Recharts: Easiest React API, covers 80% of cases
- ECharts: Handles performance edge cases
- TypeScript: Catches data shape errors early
- Visual regression: Charts are visual, test them visually

### For Custom React Visualizations

**Stack:**
- visx for React primitives
- D3 scales and shape generators
- react-spring for animations
- Memoize scales to prevent re-renders

**Why:**
- visx: Best of D3 power + React patterns
- react-spring: Smoothest animations
- Memoization: Critical for performance with low-level APIs

### For High-Performance Dashboards

**Stack:**
- ECharts with Canvas renderer
- Data decimation/sampling
- Virtual scrolling (data zoom)
- WebGL for > 100K points

**Why:**
- ECharts: Only library handling massive datasets
- Decimation: Preserve visual shape, gain 10x performance
- Virtual scrolling: Render only visible data
- WebGL: GPU acceleration for millions of points

### For Framework-Agnostic Libraries

**Stack:**
- Chart.js for simplicity
- ECharts for features
- D3 for custom work

**Why:**
- All three work in any framework or vanilla JS
- Chart.js: Smallest, easiest
- ECharts: Most features
- D3: Most powerful

## Technical Red Flags to Avoid

### 1. D3 Controlling DOM in React

```tsx
// ❌ DON'T
useEffect(() => {
  d3.select(ref.current).selectAll('rect').data(data).join('rect')
}, [data])
```

React doesn't know about D3's DOM changes = hydration errors, race conditions.

### 2. Not Memoizing Scales

```tsx
// ❌ DON'T
function Chart({ data }) {
  const scale = scaleLinear()  // New scale every render!
  return <LinePath x={d => scale(d.x)} />
}

// ✅ DO
const scale = useMemo(() => scaleLinear(), [width])
```

### 3. Rendering Too Many SVG Elements

```tsx
// ❌ DON'T (10K circles)
{data.map(d => <circle cx={d.x} cy={d.y} />)}

// ✅ DO (sample or use Canvas)
{sampleData(data, 1000).map(d => <circle />)}
```

### 4. Blocking Animations

```javascript
// ❌ DON'T (blocks main thread)
for (let i = 0; i < 1000; i++) {
  chart.update()  // Synchronous update
}

// ✅ DO (use requestAnimationFrame)
chart.update()  // Library handles async
```

### 5. Not Cleaning Up Event Listeners

```tsx
// ❌ DON'T
useEffect(() => {
  element.addEventListener('mousemove', handler)
  // Missing cleanup!
}, [])

// ✅ DO
useEffect(() => {
  element.addEventListener('mousemove', handler)
  return () => element.removeEventListener('mousemove', handler)
}, [])
```

## Final Recommendation

**Default choice for most teams:** Recharts
- React-idiomatic, well-documented, covers common cases
- Switch to ECharts only when hitting performance limits

**Advanced teams:** visx
- Full D3 power in React
- Worth the learning curve for custom work

**Enterprise dashboards:** ECharts
- Handles massive datasets
- Rich feature set justifies bundle size

**Framework-agnostic:** Chart.js
- Smallest, simplest, works everywhere
- Upgrade to ECharts if you need more chart types

**Novel visualizations:** D3
- Only tool that can create anything
- Use visx wrapper if in React

---

**Next steps after S2:**
- S3: Identify specific use cases and user personas
- S4: Evaluate long-term ecosystem viability
