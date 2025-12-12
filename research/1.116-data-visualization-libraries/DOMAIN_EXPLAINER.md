# Data Visualization Libraries: Domain Explainer

## What Problem Do They Solve?

Turning raw data into visual insights is complex:
- Mapping values to positions, sizes, colors
- Creating axes, legends, labels
- Handling user interaction (hover, zoom, pan)
- Animations and transitions
- Responsive sizing
- Accessibility

Visualization libraries provide these capabilities so you can focus on your data.

## Key Concepts

### Rendering Technologies

**SVG (Scalable Vector Graphics)**
```html
<svg>
  <rect x="0" y="0" width="100" height="50" fill="blue" />
  <text x="50" y="25">Label</text>
</svg>
```
- DOM elements (selectable, stylable with CSS)
- Good for < 1000 elements
- Interactive (click, hover on individual elements)
- Accessible (screen readers can parse)

**Canvas**
```javascript
const ctx = canvas.getContext('2d')
ctx.fillRect(0, 0, 100, 50)
ctx.fillText('Label', 50, 25)
```
- Bitmap rendering (like painting)
- Handles 1000-50000 elements
- No individual element access
- Less accessible

**WebGL**
- GPU-accelerated 3D/2D
- Handles 50000+ elements
- Complex setup
- Used by ECharts-GL, deck.gl

### Performance Rule of Thumb

| Elements | Best Renderer |
|----------|---------------|
| < 1000 | SVG |
| 1000 - 50000 | Canvas |
| > 50000 | WebGL |

### Scales

Scales map data values to visual values:

```javascript
// Linear scale: 0-100 → 0-500px
const scale = d3.scaleLinear()
  .domain([0, 100])    // Data range
  .range([0, 500])     // Pixel range

scale(50)  // → 250px
```

Types of scales:
- **Linear**: Continuous numeric (temperature, sales)
- **Band**: Discrete categories (months, products)
- **Time**: Dates and times
- **Log**: Exponential data
- **Color**: Values to colors

### Axes

Visual representation of scales:
- Tick marks at regular intervals
- Labels for values
- Title describing the dimension
- Grid lines for reading values

### Data Binding

The core concept: connecting data to visual elements.

```javascript
// D3 approach
svg.selectAll('rect')
  .data([10, 20, 30])
  .join('rect')
  .attr('height', d => d * 10)

// React approach
data.map(d => <rect height={d * 10} />)
```

### Marks

Visual primitives that represent data:
- **Points**: Scatter plots
- **Lines**: Time series
- **Bars**: Comparisons
- **Areas**: Cumulative values
- **Arcs**: Part-to-whole (pie, donut)

### Channels

Visual properties that encode data:
- **Position**: x, y coordinates (most accurate)
- **Length/Size**: Bar height, circle radius
- **Color**: Hue, saturation, lightness
- **Shape**: Triangle, square, circle
- **Angle**: Pie slices (hard to compare)

### Chart Types

| Chart | Best For |
|-------|----------|
| Line | Trends over time |
| Bar | Comparing categories |
| Pie | Part of whole (< 6 parts) |
| Scatter | Relationship between variables |
| Area | Cumulative trends |
| Heatmap | Density, patterns |
| Treemap | Hierarchical data |
| Sankey | Flow, connections |
| Network | Relationships |

## High-Level vs Low-Level Libraries

### High-Level (Recharts, Chart.js, Nivo)

```tsx
// Tell library WHAT to draw
<LineChart data={data}>
  <Line dataKey="sales" />
</LineChart>
```

Pros:
- Fast development
- Built-in interactivity
- Consistent styling

Cons:
- Limited customization
- Opinionated design

### Low-Level (D3, visx)

```tsx
// Tell library HOW to draw
const scale = scaleLinear().domain([0, 100]).range([0, 500])
{data.map(d => <circle cx={scale(d.x)} cy={scale(d.y)} r={5} />)}
```

Pros:
- Complete control
- Any visualization possible

Cons:
- More code
- Steeper learning curve

## React Integration Patterns

### Pattern 1: Library handles everything
```tsx
<LineChart data={data} />
```
Libraries: Recharts, Victory, Nivo

### Pattern 2: D3 for math, React for DOM
```tsx
const scale = d3.scaleLinear().domain([0, 100]).range([0, 500])
{data.map(d => <rect height={scale(d.value)} />)}
```
Libraries: visx

### Pattern 3: D3 takes over DOM (anti-pattern in React)
```tsx
useEffect(() => {
  d3.select(ref.current)
    .selectAll('rect')
    .data(data)
    .join('rect')
}, [data])
```
Problem: React doesn't know about DOM changes

## Responsive Design

Charts must adapt to container size:

```tsx
// Recharts
<ResponsiveContainer width="100%" height={300}>
  <LineChart />
</ResponsiveContainer>

// Chart.js
options: { responsive: true }

// DIY
const { width } = useContainerSize(ref)
```

## Interactivity

Common interactive features:
- **Tooltip**: Information on hover
- **Legend**: Show/hide series
- **Zoom**: Focus on region
- **Pan**: Navigate large datasets
- **Brush**: Select range
- **Click**: Drill down

## Animation

Smooth transitions improve comprehension:

```tsx
// Recharts (built-in)
<Line animationDuration={500} />

// visx + react-spring
const spring = useSpring({ y: targetY })
<animated.rect y={spring.y} />
```

## Accessibility

Charts should be accessible:
- Alt text for images (Canvas)
- ARIA labels for SVG elements
- Keyboard navigation
- Color contrast
- Screen reader descriptions

SVG is inherently more accessible than Canvas.

## Common Patterns

### Composable Charts
Combine multiple chart types:
```tsx
<ComposedChart>
  <Bar dataKey="sales" />
  <Line dataKey="trend" />
  <Area dataKey="forecast" />
</ComposedChart>
```

### Faceted Charts (Small Multiples)
Same chart repeated for categories:
```tsx
{categories.map(cat => (
  <LineChart key={cat} data={dataByCategory[cat]} />
))}
```

### Connected Charts
Linked brushing across charts:
```tsx
// Selecting in one chart highlights in another
const [selection, setSelection] = useState(null)
```

## Common Misconceptions

### "More chart types = better library"
Most dashboards use 3-4 chart types. Focus on those, not variety.

### "D3 is the best because it's most powerful"
Power comes with complexity. For standard charts, high-level libraries are better.

### "Canvas is always faster than SVG"
Under 1000 elements, the difference is negligible. SVG is easier to work with.

### "3D charts are impressive"
3D usually makes data harder to read. Use sparingly and purposefully.

### "Pie charts are bad"
Pie charts are fine for 2-5 slices showing part-to-whole. They're overused, not inherently bad.

## Evolution of the Space

### 2011: D3.js Released
Mike Bostock creates D3, establishing the foundation.

### 2015-2018: Wrapper Libraries
Recharts, Victory, Nivo wrap D3 for React.

### 2020: visx (Airbnb)
Bridge between D3 control and React patterns.

### 2025 Trends
- Recharts dominates React (9M downloads)
- Canvas/WebGL for performance
- AI-assisted chart generation emerging
- Accessibility focus increasing

---

**Last Updated**: 2025-12-12
**Related Research**: 1.111 (State Management), 1.113 (UI Components), 1.115 (Forms)
