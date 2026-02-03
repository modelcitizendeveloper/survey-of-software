# Feature Comparison Matrix

## Rendering Technology

| Library | Renderer | Max Elements | Frame Rate @ 10K |
|---------|----------|--------------|------------------|
| Recharts | SVG | ~1000 | 8 FPS (choppy) |
| D3 | SVG/Canvas | ~1000 SVG, ~50K Canvas | 12 FPS (Canvas) |
| Chart.js | Canvas | ~10,000 | 12 FPS |
| ECharts | Canvas/SVG/WebGL | 10M+ (WebGL) | 60 FPS (WebGL) |
| Nivo | SVG | ~1000 | 8 FPS |
| visx | SVG | ~1000 | 8 FPS |
| Victory | SVG | ~1000 | 8 FPS |

**Key insight:** ECharts is the only library that handles massive datasets smoothly.

## Bundle Size (gzipped)

| Library | Full Bundle | Tree-Shaken | Notes |
|---------|-------------|-------------|-------|
| Chart.js | 60 KB | N/A | No tree-shaking |
| visx | 60 KB | 30-60 KB | Excellent tree-shaking |
| D3 | 70 KB | 15-50 KB | Excellent tree-shaking |
| Recharts | 130 KB | 100-130 KB | Limited tree-shaking |
| ECharts | 320 KB | 150-200 KB | Moderate tree-shaking |
| Nivo | 180 KB | 150 KB | Limited tree-shaking |
| Victory | 210 KB | 180 KB | Limited tree-shaking |

**Winner:** Chart.js (smallest) and visx (best tree-shaking)

## API Paradigm

| Library | Paradigm | Example |
|---------|----------|---------|
| Recharts | Declarative (JSX) | `<LineChart><Line /></LineChart>` |
| Chart.js | Imperative (config) | `new Chart(ctx, { type: 'line' })` |
| ECharts | Imperative (config) | `chart.setOption({ series: [...] })` |
| D3 | Imperative (method chain) | `d3.select().data().join()` |
| visx | Declarative (JSX) | `<LinePath data={data} />` |
| Nivo | Declarative (JSX) | `<ResponsiveLine data={data} />` |
| Victory | Declarative (JSX) | `<VictoryLine data={data} />` |

**React projects:** Prefer declarative (Recharts, visx, Nivo, Victory)
**Framework-agnostic:** Use imperative (Chart.js, ECharts, D3)

## TypeScript Support

| Library | Type Coverage | Notes |
|---------|---------------|-------|
| Recharts | ⭐⭐⭐⭐⭐ | Ships with types, excellent |
| Chart.js | ⭐⭐⭐⭐⭐ | Ships with types, excellent |
| ECharts | ⭐⭐⭐⭐ | Ships with types, good |
| D3 | ⭐⭐⭐⭐⭐ | `@types/d3`, complex generics |
| visx | ⭐⭐⭐⭐⭐ | Ships with types, excellent |
| Nivo | ⭐⭐⭐⭐ | Ships with types, good |
| Victory | ⭐⭐⭐ | `@types/victory`, partial coverage |

**Winner:** Recharts, Chart.js, visx, D3 (all excellent)

## Chart Type Coverage

| Chart Type | Recharts | Chart.js | ECharts | D3 | visx | Nivo | Victory |
|------------|----------|----------|---------|----|----|------|---------|
| Line | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Bar | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Pie/Donut | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Scatter | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Area | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Radar | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Heatmap | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Treemap | ✅ | ❌ | ✅ | ✅ | ✅ | ✅ | ❌ |
| Sankey | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ |
| Network | ❌ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ |
| 3D | ❌ | ❌ | ✅ (GL) | ❌ | ❌ | ❌ | ❌ |
| Geographic | ❌ | ❌ | ✅ | ✅ | ✅ | ❌ | ❌ |

**Winner:** ECharts (most comprehensive), D3 (fully customizable)

## Interactivity Features

| Feature | Recharts | Chart.js | ECharts | D3 | visx | Nivo | Victory |
|---------|----------|----------|---------|----|----|------|---------|
| Tooltips | ✅ Built-in | ✅ Built-in | ✅ Built-in | ❌ DIY | ❌ DIY | ✅ Built-in | ✅ Built-in |
| Legend | ✅ Built-in | ✅ Built-in | ✅ Built-in | ❌ DIY | ❌ DIY | ✅ Built-in | ✅ Built-in |
| Zoom/Pan | ❌ | ✅ Built-in | ✅ Built-in | ✅ DIY | ❌ DIY | ❌ | ❌ |
| Brush Selection | ✅ Built-in | ❌ | ✅ Built-in | ✅ DIY | ❌ DIY | ❌ | ✅ Built-in |
| Export Image | ❌ | ✅ Built-in | ✅ Built-in | ❌ DIY | ❌ DIY | ❌ | ❌ |
| Data Table View | ❌ | ❌ | ✅ Built-in | ❌ | ❌ | ❌ | ❌ |

**Winner:** ECharts (most features out-of-the-box)

## Animation System

| Library | Engine | Easing Functions | Stagger Support |
|---------|--------|------------------|-----------------|
| Recharts | CSS/JS | 5 | ✅ |
| Chart.js | Custom | 15+ | ✅ |
| ECharts | Custom | 10+ | ✅ |
| D3 | Custom (transitions) | 15+ | ✅ |
| visx | ❌ (use external) | N/A | N/A |
| Nivo | react-spring | Many | ✅ |
| Victory | Custom | 5 | ✅ |

**Winner:** D3 (most powerful), Nivo (smoothest with react-spring)

## Responsive Design

| Library | Auto-Resize | Container Query | Adaptive Layout |
|---------|-------------|-----------------|-----------------|
| Recharts | ✅ `<ResponsiveContainer>` | ❌ | ❌ |
| Chart.js | ✅ `responsive: true` | ❌ | ❌ |
| ECharts | ✅ `chart.resize()` | ✅ Media queries | ✅ |
| D3 | ❌ Manual | ❌ | ❌ |
| visx | ✅ `<ParentSize>` | ❌ | ❌ |
| Nivo | ✅ `<Responsive*>` | ❌ | ❌ |
| Victory | ✅ `<VictoryContainer>` | ❌ | ❌ |

**Winner:** ECharts (media query support)

## Accessibility

| Library | SVG Output | ARIA Support | Screen Reader | Keyboard Nav |
|---------|------------|--------------|---------------|--------------|
| Recharts | ✅ | ❌ Manual | Partial | ❌ Manual |
| Chart.js | ❌ Canvas | ❌ | ❌ | ❌ |
| ECharts | ✅ (SVG mode) | ✅ Built-in | ✅ | ❌ |
| D3 | ✅ | ❌ Manual | ✅ | ❌ Manual |
| visx | ✅ | ❌ Manual | ✅ | ❌ Manual |
| Nivo | ✅ | ❌ Manual | Partial | ❌ Manual |
| Victory | ✅ | ✅ Built-in | ✅ | ❌ |

**Winner:** Victory, ECharts (best ARIA support)

## Cross-Platform Support

| Library | React | React Native | Vue | Angular | Vanilla JS |
|---------|-------|--------------|-----|---------|------------|
| Recharts | ✅ | ❌ | ❌ | ❌ | ❌ |
| Chart.js | ✅ Wrapper | ❌ | ✅ Wrapper | ✅ Wrapper | ✅ |
| ECharts | ✅ Wrapper | ❌ | ✅ Wrapper | ✅ Wrapper | ✅ |
| D3 | ✅ | ❌ | ✅ | ✅ | ✅ |
| visx | ✅ | ❌ | ❌ | ❌ | ❌ |
| Nivo | ✅ | ❌ | ❌ | ❌ | ❌ |
| Victory | ✅ | ✅ | ❌ | ❌ | ❌ |

**Winner:** Chart.js, ECharts, D3 (framework-agnostic)

## Server-Side Rendering (SSR)

| Library | SSR Support | Hydration | Notes |
|---------|-------------|-----------|-------|
| Recharts | ⚠️ Partial | Issues | Needs `isomorphic-style-loader` |
| Chart.js | ❌ | N/A | Canvas requires browser |
| ECharts | ✅ | Good | Server-side Canvas via `node-canvas` |
| D3 | ✅ | Good | Can generate SVG server-side |
| visx | ✅ | Good | Pure SVG, works well |
| Nivo | ✅ | Excellent | Built for SSR |
| Victory | ⚠️ Partial | Issues | Complex setup |

**Winner:** Nivo (built for SSR), visx, D3

## Testing Support

| Library | Unit Testing | Visual Regression | Snapshot Testing |
|---------|--------------|-------------------|------------------|
| Recharts | ✅ RTL | ✅ | ✅ |
| Chart.js | ⚠️ (Canvas) | ✅ | ❌ |
| ECharts | ⚠️ (Canvas) | ✅ | ❌ |
| D3 | ✅ RTL | ✅ | ✅ |
| visx | ✅ RTL | ✅ | ✅ |
| Nivo | ✅ RTL | ✅ | ✅ |
| Victory | ✅ RTL | ✅ | ✅ |

**Note:** Canvas-based libraries harder to unit test (pixels, not DOM)

## Developer Experience

| Aspect | Recharts | Chart.js | ECharts | D3 | visx | Nivo | Victory |
|--------|----------|----------|---------|----|----|------|---------|
| Learning Curve | ⭐⭐ Easy | ⭐⭐ Easy | ⭐⭐⭐ Medium | ⭐⭐⭐⭐⭐ Hard | ⭐⭐⭐⭐ Hard | ⭐⭐ Easy | ⭐⭐⭐ Medium |
| Documentation | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Examples | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ |
| Community | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| Active Dev | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ |

**Winner:** Chart.js, ECharts, D3 (best docs and examples)

## Summary: Best Library by Scenario

| Scenario | Best Choice | Runner-Up |
|----------|-------------|-----------|
| React dashboard (< 1K points) | Recharts | Nivo |
| Large datasets (10K+ points) | ECharts | Chart.js |
| Custom visualization | D3 | visx |
| Minimal bundle size | Chart.js | visx |
| Server-side rendering | Nivo | visx |
| React Native | Victory | - |
| Framework-agnostic | Chart.js | ECharts |
| TypeScript project | Recharts | visx |
| Accessibility priority | Victory | ECharts |
| Maximum chart variety | ECharts | D3 |
