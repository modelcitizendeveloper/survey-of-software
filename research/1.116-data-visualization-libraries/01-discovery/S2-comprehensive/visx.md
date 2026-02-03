# visx - Technical Architecture

## Core Philosophy

visx (from Airbnb) provides **low-level React primitives** for building custom visualizations. It's the bridge between D3's power and React's declarative model.

```tsx
// visx: D3 for math, React for rendering
import { scaleLinear } from '@visx/scale'
import { LinePath } from '@visx/shape'

const xScale = scaleLinear({ domain: [0, 100], range: [0, width] })
const yScale = scaleLinear({ domain: [0, 100], range: [height, 0] })

<LinePath
  data={data}
  x={d => xScale(d.x)}
  y={d => yScale(d.y)}
/>
```

**Key insight:** visx is **not a charting library** - it's a **component library** for building charts.

## Architecture

### Package Structure

visx is **modular** - 30+ independent packages:

```javascript
import { scaleLinear } from '@visx/scale'
import { AxisBottom, AxisLeft } from '@visx/axis'
import { LinePath, Bar } from '@visx/shape'
import { Group } from '@visx/group'
import { GridRows, GridColumns } from '@visx/grid'
import { localPoint } from '@visx/event'
import { useTooltip } from '@visx/tooltip'
```

### Core Packages

**Scales** (`@visx/scale`)
- Wrappers around D3 scales
- Same API as D3: `scaleLinear`, `scaleBand`, `scaleTime`, etc.

**Shapes** (`@visx/shape`)
- React components for SVG elements
- `LinePath`, `Bar`, `AreaClosed`, `Pie`, `Arc`, `Circle`

**Axes** (`@visx/axis`)
- `AxisBottom`, `AxisTop`, `AxisLeft`, `AxisRight`
- Customizable tick formatting, orientation

**Grid** (`@visx/grid`)
- `GridRows`, `GridColumns` - Background grid lines

**Tooltip** (`@visx/tooltip`)
- `useTooltip` hook, `Tooltip` component, `TooltipWithBounds`

**Event** (`@visx/event`)
- `localPoint` - Get mouse coordinates relative to SVG
- Touch event helpers

**Responsive** (`@visx/responsive`)
- `ParentSize` - Measure parent container
- `ScaleSVG` - Scale SVG to fit

## The visx Pattern

### Build, Don't Configure

Unlike Recharts (declarative) or Chart.js (config), visx is **compositional**:

```tsx
function LineChart({ data, width, height }) {
  // 1. Create scales
  const xScale = scaleLinear({
    domain: [0, data.length - 1],
    range: [0, width]
  })

  const yScale = scaleLinear({
    domain: [0, Math.max(...data.map(d => d.value))],
    range: [height, 0]
  })

  return (
    <svg width={width} height={height}>
      {/* 2. Render grid */}
      <GridRows scale={yScale} width={width} />
      <GridColumns scale={xScale} height={height} />

      {/* 3. Render axes */}
      <AxisBottom top={height} scale={xScale} />
      <AxisLeft scale={yScale} />

      {/* 4. Render data */}
      <LinePath
        data={data}
        x={(d, i) => xScale(i)}
        y={d => yScale(d.value)}
        stroke="#000"
      />
    </svg>
  )
}
```

**Pros:**
- Full control over every element
- Can create any visualization
- React-idiomatic (components, hooks)

**Cons:**
- More code than Recharts
- No built-in interactivity
- Steeper learning curve

## Component API

### LinePath

```tsx
import { LinePath } from '@visx/shape'
import { curveMonotoneX } from '@visx/curve'

<LinePath
  data={data}
  x={d => xScale(d.x)}          // Accessor function
  y={d => yScale(d.y)}
  stroke="blue"
  strokeWidth={2}
  curve={curveMonotoneX}        // D3 curve algorithm
/>
```

### Bar

```tsx
import { Bar } from '@visx/shape'

data.map((d, i) => (
  <Bar
    key={i}
    x={xScale(i)}
    y={yScale(d.value)}
    width={xScale.bandwidth()}
    height={height - yScale(d.value)}
    fill="steelblue"
    onClick={() => console.log(d)}
  />
))
```

### AreaClosed

```tsx
import { AreaClosed } from '@visx/shape'

<AreaClosed
  data={data}
  x={d => xScale(d.x)}
  y={d => yScale(d.y)}
  yScale={yScale}               // Used for baseline
  fill="url(#gradient)"
  curve={curveBasis}
/>
```

### Pie

```tsx
import { Pie } from '@visx/shape'

<Pie
  data={data}
  pieValue={d => d.value}
  outerRadius={100}
  innerRadius={50}              // 0 = pie, > 0 = donut
>
  {pie => {
    return pie.arcs.map((arc, i) => (
      <g key={i}>
        <path d={pie.path(arc)} fill={colors[i]} />
        <text {...pie.getArcLabel(arc)}>
          {arc.data.label}
        </text>
      </g>
    ))
  }}
</Pie>
```

## Scales (D3 Wrappers)

visx re-exports D3 scales with better defaults:

```tsx
import { scaleLinear, scaleBand, scaleTime, scaleOrdinal } from '@visx/scale'

// Linear scale
const yScale = scaleLinear({
  domain: [0, 100],
  range: [height, 0],
  nice: true,         // Round domain to nice numbers
  clamp: true         // Clamp output to range
})

// Band scale (for bar charts)
const xScale = scaleBand({
  domain: categories,
  range: [0, width],
  padding: 0.2        // 20% padding between bars
})

// Time scale
const timeScale = scaleTime({
  domain: [startDate, endDate],
  range: [0, width]
})

// Ordinal scale (for colors)
const colorScale = scaleOrdinal({
  domain: ['A', 'B', 'C'],
  range: ['red', 'green', 'blue']
})
```

## Responsive Patterns

### ParentSize

```tsx
import { ParentSize } from '@visx/responsive'

function ResponsiveChart() {
  return (
    <ParentSize>
      {({ width, height }) => (
        <LineChart width={width} height={height} />
      )}
    </ParentSize>
  )
}
```

**Implementation:**
- Measures parent container using `ResizeObserver`
- Passes dimensions to child render function
- Re-renders on resize

### ScaleSVG

```tsx
import { ScaleSVG } from '@visx/responsive'

<ScaleSVG width={400} height={300}>
  <LineChart width={400} height={300} />
</ScaleSVG>
```

Scales SVG to fit container while maintaining aspect ratio.

## Tooltip Pattern

```tsx
import { useTooltip, TooltipWithBounds } from '@visx/tooltip'
import { localPoint } from '@visx/event'

function Chart() {
  const {
    showTooltip,
    hideTooltip,
    tooltipData,
    tooltipLeft,
    tooltipTop
  } = useTooltip()

  const handleMouseMove = (event) => {
    const point = localPoint(event)
    const x = xScale.invert(point.x)  // Convert pixels → data
    const y = yScale.invert(point.y)

    showTooltip({
      tooltipData: { x, y },
      tooltipLeft: point.x,
      tooltipTop: point.y
    })
  }

  return (
    <>
      <svg onMouseMove={handleMouseMove} onMouseLeave={hideTooltip}>
        {/* Chart elements */}
      </svg>

      {tooltipData && (
        <TooltipWithBounds left={tooltipLeft} top={tooltipTop}>
          x: {tooltipData.x}, y: {tooltipData.y}
        </TooltipWithBounds>
      )}
    </>
  )
}
```

## Animation

visx doesn't include animations - integrate with React animation libraries:

### react-spring

```tsx
import { useSpring, animated } from 'react-spring'

function AnimatedBar({ x, y, width, height }) {
  const props = useSpring({
    from: { height: 0 },
    to: { height }
  })

  return (
    <animated.rect
      x={x}
      y={props.height.to(h => y + height - h)}
      width={width}
      height={props.height}
    />
  )
}
```

### react-transition-group

```tsx
import { TransitionGroup, CSSTransition } from 'react-transition-group'

<TransitionGroup component="g">
  {data.map(d => (
    <CSSTransition key={d.id} timeout={500} classNames="bar">
      <Bar ... />
    </CSSTransition>
  ))}
</TransitionGroup>
```

## Performance

visx renders **SVG** - same performance as Recharts:

| Data Points | Render Time |
|-------------|-------------|
| 100 | ~5ms |
| 500 | ~20ms |
| 1000 | ~50ms |
| 2000 | ~120ms (choppy) |

**Performance ceiling: ~1000 SVG elements**

### Optimization: Memoization

```tsx
import { useMemo } from 'react'

const xScale = useMemo(
  () => scaleLinear({ domain: [0, 100], range: [0, width] }),
  [width]  // Recreate only when width changes
)

const pathData = useMemo(
  () => data.map(d => ({ x: xScale(d.x), y: yScale(d.y) })),
  [data, xScale, yScale]
)
```

## Bundle Size

```
@visx/scale: 85 KB → 25 KB gzipped
@visx/shape: 45 KB → 14 KB gzipped
@visx/axis: 30 KB → 9 KB gzipped
@visx/tooltip: 15 KB → 5 KB gzipped

Typical bundle (for basic chart): ~60 KB gzipped
```

**Comparison:**
- visx (basic chart): 60 KB gzipped
- Recharts: 130 KB gzipped ✓ (visx is smaller)
- Chart.js: 60 KB gzipped (same)

visx is lighter because you only import what you need.

## TypeScript Support

**Type Coverage:** Excellent (ships with types)

```typescript
import { scaleLinear, ScaleLinear } from '@visx/scale'
import { LinePath } from '@visx/shape'

interface DataPoint {
  x: number
  y: number
}

const xScale: ScaleLinear<number, number> = scaleLinear({
  domain: [0, 100],
  range: [0, width]
})

<LinePath<DataPoint>
  data={data}
  x={d => xScale(d.x)}  // d is typed as DataPoint
  y={d => yScale(d.y)}
/>
```

## Accessibility

visx renders **SVG** - inherently more accessible than Canvas:

```tsx
<svg aria-label="Sales trend over time">
  <g aria-label="X axis">
    <AxisBottom ... />
  </g>
  <g aria-label="Sales data">
    <LinePath ... />
  </g>
</svg>
```

**Best practices:**
- Add ARIA labels to chart sections
- Include alt text for key insights
- Use semantic grouping (`<g>` elements)
- Ensure color contrast

## Use Cases

### Custom Dashboards

visx excels when you need **pixel-perfect** control:

```tsx
// Recharts: limited customization
<LineChart><Line /></LineChart>

// visx: full control
<svg>
  <defs>
    <linearGradient id="gradient">...</linearGradient>
  </defs>
  <GridRows />
  <LinePath fill="url(#gradient)" />
  <circle cx={x} cy={y} r={5} />  {/* Custom marker */}
  <text x={x} y={y}>Custom label</text>
</svg>
```

### Unusual Chart Types

visx can create anything D3 can, but in React:

- Heatmaps
- Network graphs (with force simulation)
- Hierarchical visualizations (trees, treemaps)
- Geographic maps
- Custom statistical plots

### Learning D3 in React

visx is a **gateway to D3**:
- Scales work like D3
- Shapes map to D3 shape generators
- Easier than raw D3 (no `.join()`, `.enter()`, `.exit()`)
- React lifecycle instead of D3 selections

## Key Strengths

1. **React-native** - Components, not config objects
2. **Flexible** - Build any visualization
3. **Modular** - Tree-shakeable, small bundle
4. **Type-safe** - Excellent TypeScript support
5. **D3 power** - All D3 capabilities available

## Key Limitations

1. **More code** - Requires building charts from scratch
2. **No built-in interactivity** - Must implement tooltips, legends, etc.
3. **Steeper learning curve** - Need D3 knowledge
4. **SVG performance** - Same 1000-point ceiling as Recharts

## When to Use visx

**Ideal for:**
- Custom, pixel-perfect visualizations
- Teams comfortable with D3
- React projects prioritizing flexibility
- Learning D3 in a React context

**Not ideal for:**
- Standard charts (use Recharts)
- Tight deadlines (use Recharts)
- Large datasets (use ECharts)
- Teams new to D3 (use Recharts)

## visx vs Recharts

| Aspect | visx | Recharts |
|--------|------|----------|
| Abstraction | Low-level primitives | High-level components |
| Code | More verbose | More concise |
| Flexibility | Maximum | Limited |
| Learning curve | Steeper | Gentler |
| Bundle size | 60 KB | 130 KB |
| Built-in features | Minimal | Tooltips, legends, etc. |
| Best for | Custom charts | Standard charts |

**Rule of thumb:**
- Standard dashboard → Recharts
- Custom visualization → visx
