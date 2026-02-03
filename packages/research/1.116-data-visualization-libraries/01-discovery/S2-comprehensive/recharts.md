# Recharts - Technical Architecture

## Rendering Architecture

### Component Hierarchy

```
ResponsiveContainer
  └─ LineChart (Coordinate System)
      ├─ CartesianGrid (Background Layer)
      ├─ XAxis / YAxis (Axis Layer)
      ├─ Tooltip (Interaction Layer)
      ├─ Legend (Meta Layer)
      └─ Line (Graph Layer)
          └─ Curve (Geometry)
              └─ <path> (SVG Element)
```

### Rendering Pipeline

```javascript
// 1. Data normalization
data → validateData() → normalizedData

// 2. Scale generation (uses D3 scales)
domain: [minValue, maxValue]
range: [0, chartWidth]
scale = d3.scaleLinear().domain(domain).range(range)

// 3. Coordinate calculation
dataPoint.x → scale(dataPoint.x) → pixelX

// 4. Path generation (uses D3 shape generators)
d3.line()
  .x(d => scale(d.x))
  .y(d => scale(d.y))
  .curve(d3.curveMonotoneX) // smoothing algorithm

// 5. SVG rendering
<path d="M 0,100 L 50,200 L 100,150" />
```

## D3 Integration

Recharts uses D3 for **math only**, not DOM manipulation:

**D3 modules used:**
- `d3-scale` - Scale generation (linear, band, time, log)
- `d3-shape` - Path generators (line, area, arc, pie)
- `d3-interpolate` - Animation interpolation
- `d3-array` - Data statistics (min, max, extent)

**NOT used:**
- `d3-selection` - DOM selection/manipulation (React handles this)
- `d3-transition` - DOM animations (Recharts uses CSS/JS)

## Performance Characteristics

### Benchmark Results

| Data Points | Render Time | Frame Rate |
|-------------|-------------|------------|
| 100 | ~5ms | 200 FPS |
| 500 | ~20ms | 50 FPS |
| 1000 | ~50ms | 20 FPS |
| 2000 | ~120ms | 8 FPS (choppy) |
| 5000 | ~400ms | Unusable |

**Performance wall: ~1000 SVG elements**

### Why SVG Slows Down

1. **Layout thrashing**: Browser recalculates layout for each element
2. **Paint complexity**: Each element painted separately
3. **Memory overhead**: Each DOM node has event listeners, properties
4. **GC pressure**: Creating/destroying many objects

### Optimization Strategies

**1. Data Sampling**
```tsx
const sampledData = data.length > 1000
  ? sampleData(data, 1000)
  : data
```

**2. Virtualization** (not built-in)
Only render visible portion of chart

**3. Disable Animations**
```tsx
<Line isAnimationActive={false} />
```

**4. Debounce Updates**
```tsx
const debouncedData = useDebounce(data, 300)
```

## Bundle Size Analysis

```
recharts: 417 KB (uncompressed)
├─ d3-scale: 85 KB
├─ d3-shape: 73 KB
├─ d3-interpolate: 45 KB
├─ recharts core: 214 KB
└─ Total gzipped: ~130 KB
```

**Tree-shaking:** Partial support
- Can import specific charts: `import { LineChart } from 'recharts'`
- D3 dependencies bundle together
- Typical real-world gzipped: 110-130 KB

## TypeScript Support

**Type Coverage:** Excellent (ships with types)

```typescript
interface DataPoint {
  name: string
  value: number
  category?: string
}

interface CustomTooltipProps {
  active?: boolean
  payload?: Array<{
    name: string
    value: number
    dataKey: string
    color: string
  }>
  label?: string
}

const CustomTooltip: React.FC<CustomTooltipProps> = ({
  active,
  payload,
  label
}) => {
  // Fully typed
}
```

## Animation System

### Built-in Animations

Recharts uses CSS/JS animations (not D3 transitions):

```tsx
<Line
  animationDuration={1000}        // Duration in ms
  animationEasing="ease-in-out"   // CSS easing function
  animationBegin={0}              // Delay before start
/>
```

**Easing options:**
- `ease`, `ease-in`, `ease-out`, `ease-in-out`
- `linear`
- Custom cubic-bezier

### Animation Implementation

```javascript
// Simplified internals
const animate = (from, to, duration, easing) => {
  const startTime = Date.now()

  const frame = () => {
    const elapsed = Date.now() - startTime
    const progress = Math.min(elapsed / duration, 1)
    const easedProgress = easingFunctions[easing](progress)

    const current = from + (to - from) * easedProgress
    render(current)

    if (progress < 1) {
      requestAnimationFrame(frame)
    }
  }

  requestAnimationFrame(frame)
}
```

## Responsive Design

### Container Size Detection

Recharts uses `ResizeObserver` (with polyfill):

```tsx
<ResponsiveContainer width="100%" height={300}>
  <LineChart>...</LineChart>
</ResponsiveContainer>
```

**Implementation:**
```javascript
// Simplified
const observer = new ResizeObserver(entries => {
  const { width, height } = entries[0].contentRect
  setDimensions({ width, height })
})

observer.observe(containerRef.current)
```

### Adaptive Rendering

Charts adjust based on size:
- **< 400px**: Hide legend, reduce tick labels
- **400-800px**: Normal rendering
- **> 800px**: Show all features

## Customization Architecture

### Extension Points

1. **Custom Shapes**
```tsx
const CustomBar = (props) => {
  const { x, y, width, height, fill } = props
  return <rect x={x} y={y} width={width} height={height} fill={fill} rx={5} />
}

<Bar shape={<CustomBar />} />
```

2. **Custom Labels**
```tsx
const CustomLabel = ({ x, y, value }) => (
  <text x={x} y={y} textAnchor="middle">{value}</text>
)

<Line label={<CustomLabel />} />
```

3. **Custom Tooltips** (as seen earlier)

4. **Custom Legends**
```tsx
const CustomLegend = ({ payload }) => (
  <ul>
    {payload.map(entry => (
      <li key={entry.value} style={{ color: entry.color }}>
        {entry.value}
      </li>
    ))}
  </ul>
)

<Legend content={<CustomLegend />} />
```

## Accessibility

### Built-in Features

- SVG elements are inherently accessible (DOM nodes)
- Screen readers can access SVG text elements
- Keyboard navigation requires custom implementation

### Accessibility Gaps

**Missing:**
- ARIA labels on chart elements
- Keyboard shortcuts for data point navigation
- High contrast mode support
- Sonification (audio representation)

**Recommended additions:**
```tsx
<LineChart aria-label="Sales data over time">
  <Line aria-label="Monthly sales" />
</LineChart>
```

## Memory Management

### Potential Leaks

1. **Event Listeners**
```tsx
// Recharts handles this internally
useEffect(() => {
  const handler = () => {}
  element.addEventListener('mousemove', handler)
  return () => element.removeEventListener('mousemove', handler)
}, [])
```

2. **Animation Frames**
- Recharts cleans up on unmount
- Manual animations need cleanup

3. **D3 Scales**
- Recreated on each render (GC pressure)
- Consider memoization for large datasets

## Testing Strategy

### Unit Testing (Jest + React Testing Library)

```tsx
import { render, screen } from '@testing-library/react'
import { LineChart, Line, XAxis, YAxis } from 'recharts'

test('renders line chart', () => {
  const data = [{ x: 1, y: 2 }, { x: 2, y: 4 }]

  render(
    <LineChart width={500} height={300} data={data}>
      <XAxis dataKey="x" />
      <YAxis />
      <Line dataKey="y" />
    </LineChart>
  )

  // SVG elements rendered
  expect(screen.getByRole('img')).toBeInTheDocument()
})
```

### Visual Regression Testing (Chromatic, Percy)

- Capture screenshots of charts
- Detect unintended visual changes
- Critical for chart libraries

## Build Requirements

**Peer Dependencies:**
- `react` >= 16.8.0
- `react-dom` >= 16.8.0

**Bundler Support:**
- Webpack: Works out of the box
- Vite: Works with default config
- Next.js: Requires transpilation (not ESM)

**Next.js Config:**
```javascript
module.exports = {
  transpilePackages: ['recharts']
}
```

## Key Strengths

1. **React-native API** - JSX feels natural
2. **D3 math** - Solid calculations
3. **TypeScript** - Full type safety
4. **Composition** - Mix chart types easily

## Key Limitations

1. **SVG only** - Performance ceiling at 1000 points
2. **Limited chart types** - No network graphs, Sankey diagrams
3. **Animation control** - Less flexible than D3
4. **Bundle size** - 130KB gzipped (large)

## When to Use Recharts

**Ideal for:**
- React dashboards with standard charts
- < 1000 data points
- Teams prioritizing developer experience
- TypeScript projects

**Not ideal for:**
- Large datasets (use ECharts)
- Custom visualizations (use visx/D3)
- Minimal bundle size (use lightweight alternatives)
