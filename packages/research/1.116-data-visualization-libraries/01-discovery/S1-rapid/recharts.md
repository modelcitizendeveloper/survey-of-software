# Recharts

> "A composable charting library built on React components."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 25,600 |
| npm Weekly Downloads | ~9M |
| Rendering | SVG |
| License | MIT |
| React Requirement | Yes |

## Why Recharts Dominates

Recharts is the **default choice** for React charts:

1. **Most popular**: 9M weekly downloads (32x more than Nivo)
2. **Declarative**: JSX-based API feels like React
3. **D3 foundation**: Solid math under the hood
4. **TypeScript**: Excellent type support
5. **Maintained**: Active development

## Core Concept: Composable Components

Each chart element is a React component:

```tsx
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'

const data = [
  { month: 'Jan', sales: 400, returns: 24 },
  { month: 'Feb', sales: 300, returns: 13 },
  { month: 'Mar', sales: 600, returns: 42 },
]

function SalesChart() {
  return (
    <ResponsiveContainer width="100%" height={400}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="month" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="sales" stroke="#8884d8" />
        <Line type="monotone" dataKey="returns" stroke="#82ca9d" />
      </LineChart>
    </ResponsiveContainer>
  )
}
```

## Chart Types

Recharts includes all common chart types:

- LineChart, AreaChart
- BarChart (horizontal/vertical)
- PieChart, RadarChart
- ScatterChart
- ComposedChart (mix types)
- Treemap, Sankey

## Key Components

### ResponsiveContainer
Always wrap charts for responsiveness:
```tsx
<ResponsiveContainer width="100%" height={300}>
  <LineChart>...</LineChart>
</ResponsiveContainer>
```

### Tooltip
Built-in hover information:
```tsx
<Tooltip
  formatter={(value, name) => [`$${value}`, name]}
  labelFormatter={(label) => `Month: ${label}`}
/>
```

### Legend
Chart legend with click-to-hide:
```tsx
<Legend onClick={(data) => console.log(data)} />
```

### Reference Lines/Areas
Annotate charts:
```tsx
<ReferenceLine y={500} stroke="red" label="Target" />
<ReferenceArea y1={200} y2={300} fill="yellow" fillOpacity={0.3} />
```

## Customization

### Custom Shapes
```tsx
const CustomDot = ({ cx, cy, value }) => (
  <circle cx={cx} cy={cy} r={value > 500 ? 8 : 4} fill="#8884d8" />
)

<Line dot={<CustomDot />} />
```

### Custom Tooltips
```tsx
const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload) return null
  return (
    <div className="tooltip">
      <p>{label}: ${payload[0].value}</p>
    </div>
  )
}

<Tooltip content={<CustomTooltip />} />
```

## Limitations

1. **SVG only**: Slows with 1000+ data points
2. **Limited chart types**: No network graphs, force layouts
3. **Animation limits**: Less control than D3
4. **No 3D**: Flat charts only

## When to Use Recharts

**Choose Recharts when:**
- Building React dashboards
- Need standard chart types
- Data points < 1000
- Want fast development

**Choose alternatives when:**
- Need 1000+ data points → ECharts
- Need custom visualizations → visx/D3
- Need cross-platform → Victory
- Need 3D → Plotly

## Resources

- [Official Docs](https://recharts.org/)
- [GitHub](https://github.com/recharts/recharts)
- [Examples](https://recharts.org/en-US/examples)
