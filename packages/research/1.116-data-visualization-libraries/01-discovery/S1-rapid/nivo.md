# Nivo

> "Supercharged React dataviz components, built on top of D3."

## Quick Facts

| Metric | Value |
|--------|-------|
| GitHub Stars | 13,600 |
| npm Weekly Downloads | ~500K |
| Rendering | SVG/Canvas/HTML |
| License | MIT |

## What Sets Nivo Apart?

Nivo offers unique features not found in other React chart libraries:

1. **Server-Side Rendering**: API for rendering charts on server
2. **Multiple renderers**: SVG, Canvas, and HTML
3. **Theming**: Deep theme customization
4. **Motion**: Built-in smooth animations
5. **Patterns & gradients**: Decorative fills

## Server-Side Rendering (Unique Feature)

Nivo can render charts on the server via HTTP API:

```bash
# Generate chart image via API
curl "https://nivo.rocks/r/line/svg?width=800&height=400&data=[...]"
```

Use cases:
- Email reports with embedded charts
- Static site generation
- PDF generation
- Social media previews

## Chart Types

Nivo has excellent variety:

**Standard:**
- Line, Bar, Pie, Area
- Scatter, Heatmap

**Advanced:**
- Chord diagram
- Sankey
- Network (force-directed)
- Treemap, Sunburst
- Waffle
- Bump chart
- Calendar heatmap
- Radar, Funnel

## Basic Usage

```tsx
import { ResponsiveLine } from '@nivo/line'

const data = [
  {
    id: 'sales',
    data: [
      { x: 'Jan', y: 100 },
      { x: 'Feb', y: 200 },
      { x: 'Mar', y: 150 },
    ],
  },
]

function Chart() {
  return (
    <div style={{ height: 400 }}>
      <ResponsiveLine
        data={data}
        margin={{ top: 50, right: 110, bottom: 50, left: 60 }}
        xScale={{ type: 'point' }}
        yScale={{ type: 'linear', min: 'auto', max: 'auto' }}
        axisBottom={{ legend: 'Month' }}
        axisLeft={{ legend: 'Sales' }}
        pointSize={10}
        useMesh={true}
        legends={[
          {
            anchor: 'bottom-right',
            direction: 'column',
            translateX: 100,
            itemWidth: 80,
            itemHeight: 20,
          },
        ]}
      />
    </div>
  )
}
```

## Theming

Nivo supports deep theming:

```tsx
const theme = {
  background: '#1a1a2e',
  textColor: '#eee',
  fontSize: 12,
  axis: {
    domain: { line: { stroke: '#777' } },
    ticks: { text: { fill: '#eee' } },
  },
  grid: { line: { stroke: '#333' } },
  legends: { text: { fill: '#eee' } },
}

<ResponsiveLine theme={theme} {...props} />
```

## Patterns & Gradients

Unique decorative features:

```tsx
<ResponsiveBar
  defs={[
    {
      id: 'dots',
      type: 'patternDots',
      background: 'inherit',
      color: '#38bcb2',
      size: 4,
    },
  ]}
  fill={[{ match: { id: 'sales' }, id: 'dots' }]}
/>
```

## Renderer Options

Choose based on your needs:

| Renderer | Best For |
|----------|----------|
| SVG | Interactivity, small datasets |
| Canvas | Large datasets, performance |
| HTML | Accessibility, SEO |

```tsx
import { ResponsiveBar } from '@nivo/bar'       // SVG
import { ResponsiveBarCanvas } from '@nivo/bar' // Canvas
```

## Limitations

1. **Smaller community**: Less tutorials, fewer Stack Overflow answers
2. **Bundle size**: Larger than Recharts
3. **Learning curve**: Many options to configure
4. **React only**: No vanilla JS option

## Nivo vs Recharts

| Aspect | Nivo | Recharts |
|--------|------|----------|
| Downloads | 500K/week | 9M/week |
| SSR | Built-in API | Manual |
| Chart variety | 20+ | 12 |
| Theming | Deep | Basic |
| Learning curve | Moderate | Easy |
| Community | Smaller | Larger |

## When to Use Nivo

**Choose Nivo when:**
- Need server-side chart rendering
- Want advanced chart types (chord, sankey, bump)
- Need deep theming
- Want patterns/gradients
- Building data-heavy applications

**Choose Recharts when:**
- Want larger community support
- Need simple, quick setup
- Standard charts sufficient

## Resources

- [Official Docs](https://nivo.rocks/)
- [GitHub](https://github.com/plouc/nivo)
- [Interactive Docs](https://nivo.rocks/components)
- [Storybook](https://nivo.rocks/storybook/)
