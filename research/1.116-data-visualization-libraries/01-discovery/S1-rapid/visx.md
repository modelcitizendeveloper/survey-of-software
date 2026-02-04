# visx

> "A collection of expressive, low-level visualization primitives for React."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 19,000 |
| npm Weekly Downloads | ~350K |
| Rendering | SVG |
| License | MIT |
| Maintainer | Airbnb |
| Production Use | 3+ years at Airbnb |

## What Is visx?

visx (formerly vx) is Airbnb's answer to "D3 + React": it wraps D3's calculation power in React components, giving you the best of both worlds.

**Key insight**: D3 for math, React for DOM.

## Why visx?

| Problem | visx Solution |
|---------|---------------|
| D3 + React DOM conflict | D3 calculates, React renders |
| D3 learning curve | React component API |
| High-level libraries too limiting | Low-level primitives |
| Bundle size concerns | Pick only packages you need |

## The visx Philosophy

1. **Un-opinionated**: Bring your own styles, animations, state
2. **Modular**: 30+ packages, use what you need
3. **Low-level**: Primitives, not pre-made charts
4. **D3 hidden**: Use D3 power without learning D3

## Package Structure

```
@visx/axis        - Axes (bottom, left, top, right)
@visx/grid        - Grid lines
@visx/group       - SVG group element
@visx/scale       - D3 scales wrapped
@visx/shape       - Lines, bars, areas, arcs
@visx/tooltip     - Tooltip primitives
@visx/zoom        - Zoom behavior
@visx/brush       - Selection brush
@visx/geo         - Geographic maps
@visx/hierarchy   - Trees, treemaps
@visx/network     - Force-directed graphs
@visx/heatmap     - Heatmaps
...and more
```

## Basic Example

```tsx
import { scaleLinear, scaleBand } from '@visx/scale'
import { Bar } from '@visx/shape'
import { Group } from '@visx/group'
import { AxisBottom, AxisLeft } from '@visx/axis'

const data = [
  { letter: 'A', frequency: 0.08 },
  { letter: 'B', frequency: 0.15 },
  { letter: 'C', frequency: 0.12 },
]

const width = 500
const height = 300
const margin = { top: 20, right: 20, bottom: 40, left: 40 }

function BarChart() {
  const xMax = width - margin.left - margin.right
  const yMax = height - margin.top - margin.bottom

  const xScale = scaleBand({
    domain: data.map(d => d.letter),
    range: [0, xMax],
    padding: 0.4,
  })

  const yScale = scaleLinear({
    domain: [0, Math.max(...data.map(d => d.frequency))],
    range: [yMax, 0],
  })

  return (
    <svg width={width} height={height}>
      <Group left={margin.left} top={margin.top}>
        {data.map(d => (
          <Bar
            key={d.letter}
            x={xScale(d.letter)}
            y={yScale(d.frequency)}
            width={xScale.bandwidth()}
            height={yMax - yScale(d.frequency)}
            fill="#6c5ce7"
          />
        ))}
        <AxisBottom scale={xScale} top={yMax} />
        <AxisLeft scale={yScale} />
      </Group>
    </svg>
  )
}
```

## When to Choose visx

**Choose visx when:**
- Need custom visualizations beyond Recharts
- Want D3 power with React idioms
- Building a reusable chart library
- Need network graphs, hierarchies, geo maps
- Care about bundle size (pick only what you need)

**Choose Recharts instead when:**
- Need standard charts quickly
- Team less experienced with visualization
- Don't need customization

## visx vs D3 vs Recharts

| Aspect | D3 | visx | Recharts |
|--------|-----|------|----------|
| Flexibility | Maximum | High | Limited |
| Learning curve | Steep | Moderate | Easy |
| React integration | Manual | Native | Native |
| Pre-made charts | None | None | Many |
| Bundle control | Good | Excellent | All-or-nothing |

## Resources

- [Official Docs](https://airbnb.io/visx/)
- [GitHub](https://github.com/airbnb/visx)
- [Gallery](https://airbnb.io/visx/gallery)
- [Airbnb Blog Post](https://medium.com/airbnb-engineering/introducing-visx-from-airbnb-fd6155ac4658)
